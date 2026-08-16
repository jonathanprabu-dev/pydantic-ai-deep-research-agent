# Pydantic AI Deep Research Agent

A research agent built with **Pydantic AI**, with a **Gradio** UI. Give it a stock ticker, a company, or any question, and it runs a multi-step Google research pass **in a real Chrome window** and writes a structured, cited report. Runs on Google Gemini or any OpenRouter model, picked in `.env`.

It also keeps the original short-answer chat, on its own tab.

## What it actually does

```
your input ──▶ 1. one Google search to see what's out there
                 │
                 ▼
              2. work out the subject (NVDA → NVIDIA, semiconductors, GPUs, AI)
                 and pick 4 non-overlapping angles
                 │
                 ▼
              3. one Google search per angle, in parallel
                 rank the results, read the best 2 pages, extract facts
                 │
                 ▼
              4. synthesise: executive summary, risks, conflicts, what to watch
                 │
                 ▼
              5. a markdown report where every claim carries its source URL
```

For a ticker the angles are fixed: **SWOT analysis**, **last 12-month stock performance**, **competition and market positioning**, **latest quarterly results and forward guidance**. The last two are steered towards primary sources — SEC filings, earnings releases, investor-relations pages — rather than commentary. For a free-text query the angles are derived from the first search.

Citations are enforced in code, not just asked for: any URL the model produces that wasn't in the search results it was given gets dropped before the report is written.

## Files

| File | What it is |
|---|---|
| `agent.py` | Provider selection, the shared model (concurrency cap + retries), and the chat agent |
| `browser.py` | Google search and page fetching through real Chrome, via Playwright |
| `research.py` | The research pipeline and its three stage agents |
| `research_models.py` | The Pydantic models every stage returns |
| `report.py` | Renders a report to markdown |
| `app.py` | The Gradio UI: Chat tab + Deep Research tab |
| `sources.py` | Prints where a report's citations came from, most-cited first |
| `digest.py` | Builds `digest.md`, one index over every report in the folder |
| `.env` | `MODEL` plus the matching provider key (not committed) |

## Setup (Windows / PowerShell)

**1. Get an API key and put it in `.env`** — copy `.env.example` and fill one in:

```
MODEL=openrouter:nvidia/nemotron-3-super-120b-a12b:free
OPENROUTER_API_KEY=your-key-here
```

Free OpenRouter key: https://openrouter.ai/settings/keys. For Google instead, set `MODEL=google:...` and `GOOGLE_API_KEY` from https://aistudio.google.com/apikey.

Paste keys exactly as issued — formats change (newer Google keys start with `AQ.`), so don't reformat them.

**2. Install and run:**

```powershell
.\run.ps1
```

That creates `.venv` if needed, installs dependencies, and starts the app. If PowerShell blocks scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in that terminal.

Manual equivalent:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**3. Open http://127.0.0.1:7860.**

You need Google Chrome installed — the app drives your real Chrome (`channel="chrome"`), so there is no separate browser download.

## Using it

- **Chat tab** — quick answers, one or two sentences, no web access. Remembers the conversation until you press Clear.
- **Deep Research tab** — enter a ticker or a question and press Research. A Chrome window opens and you'll see live progress. A run takes roughly **1.5–3 minutes**. When it finishes the report renders on the page and a **Download report (.md)** button appears.

From the terminal, without the UI:

```powershell
python research.py "NVDA"
python research.py "how do solid state batteries work"
python browser.py "NVDA"     # just the search layer, prints 5 results
python agent.py              # just the chat agent, one question
```

`research.py` writes `report.md` next to the code.

### The Chrome window

Searches run in a dedicated Chrome profile at `.chrome-profile/`, kept separate from your normal browsing. The window is visible on purpose: if Google ever shows a consent screen or a CAPTCHA, solve it in that window and the profile remembers it. The app tells you when this happens instead of silently returning nothing.

## Looking back at past reports

**The research bar has no memory.** Every submission is a fresh Google search pipeline — it cannot see previous runs, and typing "show me my earlier research" just spends another ~6 requests searching the web for that phrase. Past work lives in the report files on disk, not in the app.

To get one index over everything in the folder:

```powershell
python digest.py
```

That writes `digest.md` — query, angles, citation spread and executive summary for each report, ordered by when the research actually ran. Point it at another folder with `python digest.py path\to\reports`.

## Reading the reports

The reports are cited and the citations are real, but they are still search output. Four things to keep in mind:

**Absence of a finding is not evidence of absence.** The report only knows what your query asked and what Google returned. A run asking "who fills these gaps" reported no terminology-normalisation vendors; a later run that named candidate vendors found a mature market with several established players. The first run wasn't wrong — it was never asked. **If you want to know whether something exists, name it in the query.** That turns the run into a falsification test instead of a fishing trip.

**Source quality varies sharply by topic.** Regulatory and financial questions pull primary sources — `sec.gov`, `fda.gov`, company investor-relations pages — because the ranking is built to prefer them. Market-sizing and vendor-landscape questions attract vendor blogs and market-research firms who profit from large numbers. Check the hosts before trusting a figure:

```powershell
python sources.py report.md
```

That prints which sites the citations actually came from, most-cited first.

**"Conflicting information: none" is weak evidence.** It usually means the sources were too few or too similar to disagree — several citations from one agency, or from vendors describing their own market. Read it as thin diversity, not corroboration.

**Paywalled and bot-walled pages are dropped**, not read. Trade press, Crunchbase and PitchBook rarely make it in, so funding and private-company coverage is systematically thin. If that's what you need, this tool is the wrong instrument.

## Choosing a model

`MODEL` in `.env` picks the provider and model — no code change needed:

```
MODEL=openrouter:nvidia/nemotron-3-super-120b-a12b:free
MODEL=google:gemini-3.6-flash
```

Only the first colon splits the provider, so OpenRouter's `:free` suffix survives.

## Free-tier quota — read this

One research run costs about **6 requests** (one planner + one per angle + one synthesis), plus whatever the chat tab uses.

| Provider | Free daily cap | Runs per day | Raising it |
|---|---|---|---|
| **OpenRouter** `:free` models | 50/day (20/min) | ~8 | 1000/day after buying $10 of credits, ever |
| **Google AI Studio** | 20/day **per project** | ~3 | New project, or enable billing |

The Google cap is per project, not per key — a second key inside the same project shares the same spent quota. When you hit either limit the app says so in plain English on both tabs, and distinguishes a daily cap (retrying won't help) from a per-minute one (retrying will).

Free OpenRouter models that support the tool calling this pipeline needs, largest first:

```
nvidia/nemotron-3-ultra-550b-a55b:free       1M context
nvidia/nemotron-3-super-120b-a12b:free       262k, native structured outputs
google/gemma-4-26b-a4b-it:free               262k, native structured outputs
openai/gpt-oss-20b:free                      131k, native structured outputs
```

## Tuning

In `research.py`:

```python
ANGLE_COUNT = 4          # research angles per report
PAGES_PER_ANGLE = 2      # full pages fetched and read per angle
RESULTS_PER_SEARCH = 10  # Google results collected per search
```

Raising `ANGLE_COUNT` or `PAGES_PER_ANGLE` gives a denser report and costs proportionally more quota and time. `PRIMARY_HOSTS` / `REPUTABLE_HOSTS` / `LOW_QUALITY_HOSTS` in the same file control which sources get read.

To run Chrome without a visible window, set `headless=True` in `browser.py` — but then you cannot solve a CAPTCHA if one appears.

## Troubleshooting

| Problem | Fix |
|---|---|
| `... is not set` | You didn't edit `.env`, or started the app before saving it. Save and restart. The message names the key `MODEL` needs. |
| `... is out of quota for today` | Daily cap hit, ~6 requests per run. See the quota table above. |
| "Google is showing a consent or anti-bot page" | Solve it in the open Chrome window, then search again. It's asked once per profile. |
| "No results parsed" | Google changed its results markup, or the page was blocked. Run `python browser.py "test"` to see what Chrome actually got. |
| Chrome won't launch | Install Google Chrome, or delete `.chrome-profile/` if it got into a bad state. |
| Report says "Partial report" | One angle failed (usually quota running out mid-run). The other angles still produced a report rather than the run being thrown away — the banner names what's missing. |
| A report section has few findings | The sources were paywalled or bot-walled; those pages are dropped rather than fed in as junk. Try a differently-worded query. |
| Port 7860 in use | `demo.launch(server_port=7861)` at the bottom of `app.py`. |
| `Exceeded maximum output retries` | The model can't produce the required structure and repeats the same mistake on retry. Nested JSON strings are already handled (see Notes); anything else means the model is too weak — switch `MODEL` in `.env` to one of the larger free options above. |
| `ModuleNotFoundError` | Activate the venv and re-run `pip install -r requirements.txt`. |

## Notes

- Never commit `.env` — `.gitignore` excludes it, along with `.chrome-profile/` and `report.md`.
- Swap the model by editing `MODEL` in `.env`. No code change, no reinstall.
- The pipeline is deliberately fixed stages in Python rather than one agent holding tools: the stages are known in advance, and structured outputs per stage are what keep every claim tied to a real URL.
- Nested models in `research_models.py` inherit `Nested`, which accepts a JSON *string* where an object is expected. Smaller models routinely double-encode a nested field and repeat the mistake on every retry, which otherwise kills the run outright. Parsing the string costs nothing and is what keeps weaker free models usable.
