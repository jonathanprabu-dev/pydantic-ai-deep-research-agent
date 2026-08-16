"""The typed contract for the research pipeline.

Every stage agent returns one of these. Structured output is what makes
claim-to-source attribution reliable — asking for citations in prose loses them.
"""

from __future__ import annotations

import json
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class Nested(BaseModel):
    """A model that may arrive as a JSON string instead of an object.

    Smaller models routinely double-encode a nested field — emitting
    `"subject": "{\\"kind\\": \\"ticker\\"}"` where the schema wants an object. The
    content is right and the shape is wrong, and they repeat the mistake on retry,
    so accepting the string costs nothing and keeps weaker models usable.
    """

    @model_validator(mode="before")
    @classmethod
    def _parse_json_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                return value
        return value


class SearchResult(BaseModel):
    """One organic result off a Google results page."""

    title: str
    url: str
    snippet: str = ""


class SourceRef(Nested):
    """A source backing a specific claim."""

    title: str = Field(description="The title of the source page.")
    url: str = Field(description="The exact URL, copied from the supplied sources.")


class Finding(Nested):
    """One substantive fact, number or claim, with the sources that support it."""

    claim: str = Field(description="The finding in one sentence. Include numbers where they exist.")
    detail: str = Field(description="Two or three sentences of supporting detail and context.")
    evidence: list[SourceRef] = Field(
        description="At least one source from the supplied set that supports this claim."
    )


class Section(Nested):
    """The write-up for a single research angle."""

    angle: str = Field(description="The name of the angle this section covers.")
    summary: str = Field(description="A short paragraph answering this angle.")
    findings: list[Finding] = Field(description="Three to six findings for this angle.")


class Subject(Nested):
    """What the user actually asked about, after resolution against search results."""

    kind: Literal["ticker", "query"]
    display_name: str = Field(description="e.g. 'NVIDIA Corporation (NVDA)' or the topic.")
    ticker: str | None = Field(default=None, description="Exchange ticker, if this is a company.")
    sector: str | None = Field(default=None, description="e.g. 'Semiconductors'.")
    context_keywords: list[str] = Field(
        default_factory=list, description="e.g. ['GPU', 'AI accelerators', 'data centre']."
    )


class Angle(Nested):
    """One research direction to chase with its own Google search."""

    name: str = Field(description="Short human-readable angle name.")
    google_query: str = Field(description="The exact query to type into Google.")
    rationale: str = Field(description="Why this angle matters for the subject.")
    prefer_primary_sources: bool = Field(
        default=False,
        description="True for financial angles that need filings, earnings releases or IR pages.",
    )


class ResearchPlan(BaseModel):
    """Stage 2 output: what we are researching and along which angles."""

    subject: Subject
    angles: list[Angle] = Field(description="Three to four non-overlapping angles.")


class Synthesis(Nested):
    """Stage 4 output: the cross-cutting parts of the report."""

    executive_summary: str = Field(description="A tight paragraph or two over all sections.")
    risks_and_uncertainties: list[str]
    conflicting_information: list[str] = Field(
        description="Places where sources disagree, or say so explicitly if they do not."
    )
    what_to_watch_next: list[str] = Field(description="Concrete upcoming events or signals.")


class ResearchReport(BaseModel):
    """The finished report, assembled in Python from the stage outputs."""

    query: str
    subject: Subject
    sections: list[Section]
    synthesis: Synthesis
    sources: list[SearchResult]
    skipped_angles: list[str] = Field(
        default_factory=list,
        description="Angles that failed and are missing from the report, so the "
        "reader knows the coverage is partial.",
    )
