"""Regression test: Chrome dies while a page fetch is in flight.

Run it directly: `python test_browser_recovery.py` (exits non-zero on failure).

Case A -- the queue race. fetch_page() used to capture the context, THEN wait for
a free fetch slot. With two slots and a dozen queued fetches that wait lasts
minutes; if Chrome died and relaunched inside it, the queued coroutine still held
the dead context and new_page() raised TargetClosedError -- with a live Chrome
window on screen, which is what the user saw.

Case B -- the residual race. Chrome dies between get_context()'s liveness check
and the new_page() call, so no ordering fix can catch it; _open_page() must
relaunch and retry.
"""

import asyncio
import sys

import browser as B

URL = "data:text/html,<body><p>" + ("lorem ipsum dolor sit amet " * 40) + "</p></body>"


def _check(name: str, text: str) -> int:
    if "lorem ipsum" not in text:
        print(f"FAIL [{name}]: no usable text (got {len(text)} chars)")
        return 1
    print(f"PASS [{name}]: recovered, {len(text)} chars")
    return 0


async def case_a() -> int:
    """Chrome dies while the fetch is queued behind a full semaphore."""
    ctx = await B.get_context()

    await B._fetch_slots.acquire()
    await B._fetch_slots.acquire()
    task = asyncio.create_task(B.fetch_page(URL))
    await asyncio.sleep(2)  # the fetch is now blocked on the semaphore

    await ctx.close()  # Chrome dies during the wait
    await asyncio.sleep(0.5)

    B._fetch_slots.release()
    B._fetch_slots.release()
    try:
        return _check("queue race", await task)
    except Exception as exc:
        print(f"FAIL [queue race]: {type(exc).__name__}: {str(exc)[:100]}")
        return 1


async def case_b() -> int:
    """Chrome dies between the liveness check and new_page()."""
    real_get_context = B.get_context
    killed = False

    async def dying_get_context():
        nonlocal killed
        context = await real_get_context()
        if not killed:  # kill it once, after the check, before the caller uses it
            killed = True
            await context.close()
        return context

    B.get_context = dying_get_context
    try:
        return _check("check/use race", await B.fetch_page(URL))
    except Exception as exc:
        print(f"FAIL [check/use race]: {type(exc).__name__}: {str(exc)[:100]}")
        return 1
    finally:
        B.get_context = real_get_context


async def main() -> int:
    failures = 0
    try:
        failures += await case_a()
        failures += await case_b()
    finally:
        await B.close_browser()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
