"""Gradio front end: a short-answer chat, and a deep research tab."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

import gradio as gr

from agent import check_backend, get_chat_agent
from browser import SearchBlocked
from combine import combine
from digest import find_reports
from to_docx import convert as to_docx
from to_text import convert as to_text
from report import render_markdown
from research import friendly_error, run_research

REPORT_DIR = Path(tempfile.gettempdir()) / "deep-research-reports"
PROJECT_DIR = Path(__file__).parent
COMBINED_PATH = PROJECT_DIR / "all-reports.md"
# Reports written by the UI land in temp; those written by `python research.py`
# land next to the code. Past reports should show both.
REPORT_DIRS = [PROJECT_DIR, REPORT_DIR]


async def respond(message: str, chat_display: list, history: list):
    """Run one turn of the chat agent and update both the chat and the agent history."""
    message = (message or "").strip()
    if not message:
        return "", chat_display, history

    error = check_backend()
    if error:
        reply = f"⚠️ {error}"
        chat_display = chat_display + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": reply},
        ]
        return "", chat_display, history

    try:
        result = await get_chat_agent().run(message, message_history=history)
        reply = result.output
        # Keep the agent's own message history so the next turn has context.
        history = result.all_messages()
    except Exception as exc:  # surface the failure in the UI instead of a blank reply
        reply = f"⚠️ {friendly_error(exc)}"

    chat_display = chat_display + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return "", chat_display, history


def reset():
    """Clear both the visible chat and the agent history."""
    return [], []


def _downloads(markdown_path: Path) -> list[str]:
    """The one report as both formats: markdown, and Word for anyone who wants it.

    Built here rather than at write time so the Word file always matches the
    markdown next to it — and so reports written by `python research.py`, which
    never makes one, still offer it.
    """
    paths = [markdown_path]
    try:
        paths.append(Path(to_docx(markdown_path, markdown_path.with_suffix(".docx"))))
    except Exception as exc:  # a Word failure must not cost the markdown download
        print(f"[app] could not build {markdown_path.stem}.docx: {exc}", file=sys.stderr)
    return [str(p) for p in paths]


def _report_path(query: str) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")[:40] or "report"
    return REPORT_DIR / f"{slug}.md"


async def research(query: str):
    """Stream the research run so a two-minute wait doesn't look like a hang."""
    query = (query or "").strip()
    if not query:
        yield "Enter a ticker or a question first.", "", gr.update(visible=False)
        return

    error = check_backend()
    if error:
        yield f"⚠️ {error}", "", gr.update(visible=False)
        return

    yield "Starting…", "", gr.update(visible=False)
    try:
        async for status, report in run_research(query):
            if report is None:
                yield status, "", gr.update(visible=False)
                continue
            markdown = render_markdown(report)
            path = _report_path(query)
            path.write_text(markdown, encoding="utf-8")
            yield (
                f"Done — {len(report.sections)} angles, {len(report.sources)} sources.",
                markdown,
                gr.update(value=_downloads(path), visible=True),
            )
    except SearchBlocked as exc:
        yield f"⚠️ {exc}", "", gr.update(visible=False)
    except Exception as exc:
        yield f"⚠️ {friendly_error(exc)}", "", gr.update(visible=False)


def report_choices() -> list[tuple[str, str]]:
    """Dropdown entries for every report on disk, newest first."""
    found = find_reports(REPORT_DIRS, skip=COMBINED_PATH)
    return [(title, str(path)) for title, path in reversed(found)]


def refresh_reports():
    """Re-scan the folders so a run finished in this session appears in the list."""
    return gr.update(choices=report_choices())


def show_report(path: str | None):
    """Render the chosen report and point the download button at it."""
    if not path:
        return "", gr.update(visible=False)
    file = Path(path)
    if not file.is_file():
        return f"⚠️ {file.name} is no longer on disk.", gr.update(visible=False)
    return file.read_text(encoding="utf-8"), gr.update(value=_downloads(file), visible=True)


def _built(count: int, path: Path, what: str):
    """Shared result for both builders: a status line and the download."""
    if not count:
        return "⚠️ No reports found yet — run some research first.", gr.update(visible=False)
    size = path.stat().st_size
    return (
        f"Built {what} from **{count} reports** — `{path.name}`, {size:,} bytes.",
        gr.update(value=str(path), visible=True),
    )


DOWNLOADS = Path.home() / "Downloads"


def make_combined():
    """Every report in full, as Word and markdown.

    Also drops a copy straight into the Downloads folder: browsers block repeated
    downloads from a page, and that block outlives whatever triggered it, so the
    link alone is not a reliable way to get the file out of the app.
    """
    count = combine(REPORT_DIRS, COMBINED_PATH)
    if not count:
        return "⚠️ No reports found yet — run some research first.", gr.update(visible=False)

    built = [
        to_docx(COMBINED_PATH, COMBINED_PATH.with_suffix(".docx")),
        to_text(COMBINED_PATH, COMBINED_PATH.with_suffix(".txt")),
        COMBINED_PATH,
    ]
    saved = ""
    if DOWNLOADS.is_dir():
        blocked = []
        for source in built:
            try:
                shutil.copy2(source, DOWNLOADS / source.name)
            except OSError:  # a locked file must not lose the built document
                blocked.append(source.name)
        saved = f" Also saved to `{DOWNLOADS}`."
        if blocked:
            saved += f" (Open in another program, so not copied: {', '.join(blocked)}.)"

    sizes = ", ".join(f"`{p.name}` {p.stat().st_size:,}b" for p in built)
    return (
        f"Built one document from **{count} reports** — {sizes}.{saved}",
        gr.update(value=[str(p) for p in built], visible=True),
    )


with gr.Blocks(title="Deep Research Agent") as demo:
    gr.Markdown("# Deep Research Agent\nPydantic AI + Gemini, searching Google in real Chrome.")

    with gr.Tabs():
        with gr.Tab("Chat"):
            gr.Markdown("Quick answers, one or two sentences. No web access.")
            chatbot = gr.Chatbot(height=440, label="Chat")
            history_state = gr.State([])

            with gr.Row():
                box = gr.Textbox(
                    placeholder="Ask something...",
                    show_label=False,
                    scale=8,
                    autofocus=True,
                )
                send = gr.Button("Send", variant="primary", scale=1)
                clear = gr.Button("Clear", scale=1)

            inputs = [box, chatbot, history_state]
            outputs = [box, chatbot, history_state]
            box.submit(respond, inputs, outputs)
            send.click(respond, inputs, outputs)
            clear.click(reset, None, [chatbot, history_state])

        with gr.Tab("Deep Research"):
            gr.Markdown(
                "Enter a stock ticker, a company, or any question. This runs several "
                "Google searches in a real Chrome window and takes a few minutes. "
                "If a consent or CAPTCHA page appears, solve it in that window — it "
                "is only asked once."
            )
            with gr.Row():
                research_box = gr.Textbox(
                    placeholder="NVDA   ·   solid state batteries   ·   EU AI Act enforcement",
                    show_label=False,
                    scale=8,
                    autofocus=True,
                )
                run = gr.Button("Research", variant="primary", scale=1)

            status = gr.Markdown("")
            download = gr.File(
                label="Download report — Word (.docx) or markdown (.md)",
                file_count="multiple",
                visible=False,
            )
            report_view = gr.Markdown("")

            research_outputs = [status, report_view, download]

            run.click(research, research_box, research_outputs)
            research_box.submit(research, research_box, research_outputs)

        with gr.Tab("Past reports"):
            gr.Markdown(
                "Every report on disk — from this app and from `python research.py`. "
                "Nothing here costs a model request."
            )
            with gr.Row():
                picker = gr.Dropdown(
                    choices=report_choices(),
                    label="Report",
                    scale=8,
                )
                refresh = gr.Button("Refresh", scale=1)

            # gr.File, not gr.DownloadButton: a DownloadButton starts a download the
            # moment its value is set, so browsing around fires several automatic
            # downloads and Chrome silently blocks them as "multiple downloads".
            # A File renders a link the user clicks, which is never blocked.
            past_download = gr.File(
                label="Download this report — Word (.docx) or markdown (.md)",
                file_count="multiple",
                visible=False,
            )

            combined_button = gr.Button("Build all reports into one document", variant="primary")
            build_status = gr.Markdown("")
            build_download = gr.File(
                label="Download — Word (.docx), plain text (.txt) or markdown (.md)",
                file_count="multiple",
                visible=False,
            )

            past_view = gr.Markdown("")

            picker.change(show_report, picker, [past_view, past_download])
            refresh.click(refresh_reports, None, picker)
            combined_button.click(make_combined, None, [build_status, build_download])


if __name__ == "__main__":
    # Gradio serves no file outside its own temp dir unless the path is allowed,
    # so report downloads 403 without this.
    demo.launch(allowed_paths=[str(PROJECT_DIR), str(REPORT_DIR)])
