"""Google search and page fetching driven through the real Google Chrome browser.

One persistent Chrome profile lives in .chrome-profile/ so a consent screen or
CAPTCHA solved once stays solved. The browser is launched lazily and reused for
the whole process; launching per request would cost seconds and leak processes.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus, urlparse

from playwright.async_api import BrowserContext, Page, async_playwright
from playwright.async_api import Error as PlaywrightError

from research_models import SearchResult

PROFILE_DIR = Path(__file__).parent / ".chrome-profile"

# Google hands out an interstitial instead of results when it doesn't like us.
BLOCK_MARKERS = ("/sorry/", "consent.google.com")
BLOCK_TEXT = ("unusual traffic", "before you continue", "verify you're not a robot")

# Publishers serve bot walls and cookie banners with a 200. Feeding that to the
# analyst as if it were article text is worse than fetching nothing.
JUNK_TEXT = (
    "are you a robot",
    "enable javascript and cookies to continue",
    "checking your browser",
    "captcha",
    "access denied",
    "subscribe to continue reading",
)
MIN_PAGE_CHARS = 400

# Chrome tears the whole context down when its last tab closes, and between
# searches the only tab is the blank one it launched with. An unexplained blank
# tab in a window the user is invited to click into is a tab they will close, so
# say what it is for.
KEEPALIVE_HTML = """
<title>Deep Research Agent</title>
<body style="font:16px system-ui;margin:3rem;color:#333">
<h2>This window belongs to the Deep Research Agent.</h2>
<p>Searches open and close their own tabs here. Please leave this tab open —
closing it shuts the browser down and the app has to start Chrome again.</p>
<p>If a Google consent screen or CAPTCHA appears in another tab, solve it there.
It is only asked once.</p>
</body>
"""

_playwright = None
_context: BrowserContext | None = None
_lock = asyncio.Lock()
# Google gets one tab at a time; page fetches are what we parallelise.
_search_lock = asyncio.Lock()
# ...but only two at a time. Every angle fetching at once means a dozen live tabs.
_fetch_slots = asyncio.Semaphore(2)


class SearchBlocked(RuntimeError):
    """Google served a consent or anti-bot page instead of search results."""


def _forget_context(closed: BrowserContext | None = None) -> None:
    """Drop the cached context so the next call relaunches Chrome.

    Only clears the cache when the dead context is still the cached one. A close
    event can arrive after a relaunch has already replaced it, and clearing then
    would throw away a perfectly good browser and open a second window.

    Deliberately synchronous and lock-free: close() fires this while _lock is
    already held, so taking the lock here would deadlock.
    """
    global _context
    if closed is None or closed is _context:
        _context = None


async def get_context() -> BrowserContext:
    """Return the shared Chrome context, launching it on first use.

    The window is visible so a consent screen can be solved by hand, which means
    the user can also close it — and Chrome can crash on its own. Either leaves a
    dead context in the cache, and handing that back fails every later request
    with "Target page, context or browser has been closed" until the process
    restarts. So check the browser is still connected and relaunch if it is not.
    """
    global _playwright, _context
    async with _lock:
        # The close event covers an orderly shutdown; is_connected catches the
        # chrome.exe process being killed outright, where no event arrives.
        if _context is not None and _context.browser is not None:
            if not _context.browser.is_connected():
                _context = None

        if _context is None:
            # Started once per process: relaunching Chrome must not leak a
            # second driver process each time.
            if _playwright is None:
                _playwright = await async_playwright().start()
            PROFILE_DIR.mkdir(exist_ok=True)
            _context = await _playwright.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                channel="chrome",  # the user's installed Chrome, not a bundled build
                headless=False,  # visible so a consent screen can be solved by hand
                viewport={"width": 1280, "height": 900},
                args=["--disable-blink-features=AutomationControlled"],
            )
            _context.set_default_timeout(20_000)
            _context.on("close", _forget_context)
            if _context.pages:  # the tab Chrome launched with, kept as a keepalive
                await _context.pages[0].set_content(KEEPALIVE_HTML)
    return _context


async def _open_page() -> Page:
    """Open a tab, relaunching Chrome once if the context turns out to be dead.

    get_context() checks the browser is alive, but callers reach here only after
    waiting on a lock or a fetch slot, and that wait can last minutes. Chrome can
    die inside it, so the liveness check that matters is this call itself. Only a
    disconnected browser is retried: a timeout means Chrome is alive but busy, and
    relaunching it would just cost another 20 seconds.
    """
    for attempt in (1, 2):
        context = await get_context()
        try:
            return await context.new_page()
        except PlaywrightError:
            browser = context.browser
            if attempt == 2 or (browser is not None and browser.is_connected()):
                raise
            _forget_context(context)
    raise AssertionError("unreachable")  # the loop either returns or raises


async def _close_page(page: Page) -> None:
    """Close a tab, ignoring a browser that died first — it has no tabs left."""
    try:
        await page.close()
    except PlaywrightError:
        pass


async def close_browser() -> None:
    """Shut the shared browser down. Safe to call when it was never opened."""
    global _playwright, _context
    async with _lock:
        if _context is not None:
            try:
                await _context.close()
            except Exception:  # already dead: cleanup must not mask the real error
                pass
            _context = None
        if _playwright is not None:
            await _playwright.stop()
            _playwright = None


def _looks_blocked(url: str, body: str) -> bool:
    if any(marker in url for marker in BLOCK_MARKERS):
        return True
    head = body[:2000].lower()
    return any(text in head for text in BLOCK_TEXT)


async def google_search(query: str, limit: int = 10) -> list[SearchResult]:
    """Run one Google search in Chrome and return the organic results."""
    url = f"https://www.google.com/search?q={quote_plus(query)}&num=20&hl=en&gl=us"

    async with _search_lock:
        page = await _open_page()
        try:
            await page.goto(url, wait_until="domcontentloaded")
            body = await page.inner_text("body")
            if _looks_blocked(page.url, body):
                raise SearchBlocked(
                    "Google is showing a consent or anti-bot page. Solve it in the "
                    "open Chrome window, then run the search again — the profile "
                    "remembers it."
                )
            # Anchor on <h3>: Google's class names churn, that tag has not.
            raw = await page.evaluate(
                """
                () => {
                  const root = document.querySelector('#rso') || document.querySelector('#search');
                  if (!root) return [];
                  const out = [];
                  for (const h3 of root.querySelectorAll('h3')) {
                    const a = h3.closest('a[href]');
                    if (!a) continue;
                    const block = a.closest('div[data-hveid]') || a.parentElement;
                    let snippet = '';
                    if (block) {
                      const text = block.innerText || '';
                      snippet = text.split('\\n').filter(l => l.length > 60).join(' ');
                    }
                    out.push({title: h3.innerText, url: a.href, snippet});
                  }
                  return out;
                }
                """
            )
        finally:
            await _close_page(page)

    results: list[SearchResult] = []
    seen: set[str] = set()
    for item in raw:
        link = item.get("url") or ""
        host = urlparse(link).netloc
        if not link.startswith("http") or host.endswith("google.com"):
            continue
        if link in seen:
            continue
        seen.add(link)
        results.append(
            SearchResult(
                title=(item.get("title") or "").strip() or link,
                url=link,
                snippet=re.sub(r"\s+", " ", item.get("snippet") or "").strip()[:400],
            )
        )
        if len(results) >= limit:
            break

    if not results:
        raise SearchBlocked(
            f"No results parsed for {query!r}. Google may have changed its result "
            "markup, or the page was blocked."
        )
    return results


async def fetch_page(url: str, max_chars: int = 12_000) -> str:
    """Return the visible text of a page, or '' if it cannot be read.

    A dead link must not kill a research run, so every failure here is swallowed.
    """
    async with _fetch_slots:
        try:
            page = await _open_page()
        except Exception as exc:  # no tab, no page text — but the run carries on
            # Distinguishable from a dead link: silence here would read as every
            # source being unreachable when the real fault is Chrome itself.
            print(f"[browser] cannot open a tab: {exc}", file=sys.stderr)
            return ""
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=20_000)
            text = await page.inner_text("body")
        except Exception:
            return ""
        finally:
            await _close_page(page)

    text = re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()
    if len(text) < MIN_PAGE_CHARS:
        return ""
    if any(marker in text[:1500].lower() for marker in JUNK_TEXT):
        return ""
    return text[:max_chars]


async def _smoke_test(query: str) -> None:
    try:
        for result in (await google_search(query))[:5]:
            print(f"- {result.title}\n  {result.url}")
    finally:
        await close_browser()


if __name__ == "__main__":
    # Result titles carry any script on earth; the Windows console is cp1252.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(_smoke_test(" ".join(sys.argv[1:]) or "NVDA"))
