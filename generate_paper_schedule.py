#!/usr/bin/env python3
"""Generate paper_schedule.html from talk assignments and paper metadata."""

from __future__ import annotations

import argparse
import csv
import html
import re
import ssl
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from itertools import groupby
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "talk_assignment.csv"
DEFAULT_PAPERS_CSV = ROOT / "list_of_papers.csv"
DEFAULT_HTML = ROOT / "paper_schedule.html"
DEFAULT_PROCEEDINGS_URL = "https://rlj.cs.umass.edu/2026/2026issue.html"

REQUIRED_COLUMNS = [
    "Date",
    "Day of week",
    "Time",
    "Track",
    "Room",
    "Number of talk slots in session",
    "Session Themes",
]
TALK_COLUMNS = [f"Talk {i}" for i in range(1, 9)]

MONTH_NAMES = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}

# Poster session times from schedule.html (same-day poster for oral papers).
POSTER_TIMES_BY_DATE = {
    "Aug 16": "1 PM – 2:30 PM",
    "Aug 17": "3 PM – 6 PM",
    "Aug 18": "3 PM – 6 PM",
}

# Presentation session ranges from schedule.html, keyed by session start time.
PRESENTATION_SESSION_TIMES = {
    "11:00 AM": "11:00 AM – 11:50 AM",
    "10:20 AM": "10:20 AM – 11:10 AM",
    "11:40 AM": "11:40 AM – 12:30 PM",
}

CONFERENCE_YEAR = 2026
CONFERENCE_TZ = ZoneInfo("America/Toronto")


@dataclass
class TalkSession:
    date: str
    day_of_week: str
    time: str
    track: str
    room: str
    slot_count: str
    theme: str
    talks: list[str] = field(default_factory=list)

    @property
    def poster_time(self) -> str:
        return POSTER_TIMES_BY_DATE.get(self.date, "")

    @property
    def presentation_session_time(self) -> str:
        return PRESENTATION_SESSION_TIMES.get(self.time, self.time)


@dataclass(frozen=True)
class ProceedingsLinks:
    page_url: str
    pdf_url: str
    authors: str


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def normalize_title(text: str) -> str:
    """Normalize a title for strict matching without changing its words."""
    text = html.unescape(unicodedata.normalize("NFKD", text)).casefold()
    text = "".join(character for character in text if not unicodedata.combining(character))
    return normalize_whitespace(re.sub(r"[\W_]+", " ", text))


class LinkParser(HTMLParser):
    """Collect anchor text and hrefs from a small HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.casefold() == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "a" and self._href is not None:
            self.links.append(
                (normalize_whitespace("".join(self._text)), self._href)
            )
            self._href = None
            self._text = []


class ProceedingsEntryParser(HTMLParser):
    """Collect linked paper titles and italicized authors from list items."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[tuple[str, str, str]] = []
        self._in_list_item = False
        self._in_title = False
        self._in_authors = False
        self._href: str | None = None
        self._title: list[str] = []
        self._authors: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        if tag == "li":
            self._in_list_item = True
            self._href = None
            self._title = []
            self._authors = []
        elif tag == "a" and self._in_list_item:
            self._href = dict(attrs).get("href")
            self._in_title = True
        elif tag == "i" and self._in_list_item:
            self._in_authors = True

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title.append(data)
        if self._in_authors:
            self._authors.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag == "a":
            self._in_title = False
        elif tag == "i":
            self._in_authors = False
        elif tag == "li" and self._in_list_item:
            if self._href is not None:
                self.entries.append(
                    (
                        normalize_whitespace("".join(self._title)),
                        self._href,
                        normalize_whitespace("".join(self._authors)),
                    )
                )
            self._in_list_item = False


def fetch_html(url: str) -> str:
    default_paths = ssl.get_default_verify_paths()
    system_ca_file = Path("/etc/ssl/cert.pem")
    ssl_context = None
    if default_paths.cafile is None and system_ca_file.is_file():
        # Python.org macOS builds do not always use the system CA bundle.
        ssl_context = ssl.create_default_context(cafile=str(system_ca_file))
    request = Request(url, headers={"User-Agent": "RLC paper schedule generator"})
    with urlopen(request, timeout=30, context=ssl_context) as response:
        return response.read().decode("utf-8")


def parse_links(document: str) -> list[tuple[str, str]]:
    parser = LinkParser()
    parser.feed(document)
    return parser.links


def extract_proceedings_entries(
    document: str, proceedings_url: str
) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    seen_titles: set[str] = set()
    parser = ProceedingsEntryParser()
    parser.feed(document)

    for title, href, authors in parser.entries:
        page_url = urljoin(proceedings_url, href)
        if not re.fullmatch(r"/2026/papers/Paper\d+\.html", urlparse(page_url).path):
            continue
        normalized_title = normalize_title(title)
        if not normalized_title:
            raise ValueError(f"Proceedings entry has no title: {page_url}")
        if normalized_title in seen_titles:
            raise ValueError(f"Duplicate proceedings title: {title}")
        if not authors:
            raise ValueError(f"Proceedings entry has no authors: {title}")
        seen_titles.add(normalized_title)
        entries.append((title, page_url, authors))

    if not entries:
        raise ValueError(f"No paper entries found at {proceedings_url}")
    return entries


def extract_pdf_url(document: str, paper_page_url: str) -> str:
    candidates = [
        urljoin(paper_page_url, href)
        for text, href in parse_links(document)
        if normalize_title(text) == "paper"
        and urlparse(urljoin(paper_page_url, href)).path.casefold().endswith(".pdf")
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one direct PDF link at {paper_page_url}, found {len(candidates)}"
        )
    pdf_url = candidates[0]
    if urlparse(pdf_url).scheme != "https":
        raise ValueError(f"Proceedings PDF is not HTTPS: {pdf_url}")
    return pdf_url


def load_proceedings_links(proceedings_url: str) -> dict[str, ProceedingsLinks]:
    entries = extract_proceedings_entries(fetch_html(proceedings_url), proceedings_url)
    return {
        title: ProceedingsLinks(
            page_url=page_url,
            pdf_url=extract_pdf_url(fetch_html(page_url), page_url),
            authors=authors,
        )
        for title, page_url, authors in entries
    }


def match_proceedings_links(
    schedule_titles: list[str],
    proceedings_links: dict[str, ProceedingsLinks],
) -> tuple[dict[str, ProceedingsLinks], list[str], list[str]]:
    proceedings_by_normalized: dict[str, tuple[str, ProceedingsLinks]] = {}
    for title, links in proceedings_links.items():
        normalized = normalize_title(title)
        if normalized in proceedings_by_normalized:
            raise ValueError(f"Duplicate normalized proceedings title: {title}")
        proceedings_by_normalized[normalized] = (title, links)

    matched: dict[str, ProceedingsLinks] = {}
    used_proceedings_titles: set[str] = set()
    unmatched: list[str] = []

    for title in schedule_titles:
        normalized = normalize_title(title)
        entry = proceedings_by_normalized.get(normalized)
        if entry is None:
            unmatched.append(title)
            continue
        proceedings_title, links = entry
        if proceedings_title in used_proceedings_titles:
            raise ValueError(f"Proceedings paper matched more than once: {proceedings_title}")
        used_proceedings_titles.add(proceedings_title)
        matched[title] = links

    unused = [
        title for title in proceedings_links if title not in used_proceedings_titles
    ]
    return matched, unmatched, unused


def parse_time_sort_key(time_str: str) -> tuple[int, int]:
    """Return (hour24, minute) for sorting."""
    time_str = normalize_whitespace(time_str)
    match = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", time_str, re.I)
    if not match:
        return (99, 99)
    hour = int(match.group(1))
    minute = int(match.group(2))
    period = match.group(3).upper()
    if period == "AM":
        if hour == 12:
            hour = 0
    elif hour != 12:
        hour += 12
    return (hour, minute)


def parse_date_sort_key(date_str: str) -> tuple[int, int]:
    """Return (month, day) for sorting."""
    parts = normalize_whitespace(date_str).split()
    if len(parts) != 2:
        return (99, 99)
    month_str, day_str = parts
    month = list(MONTH_NAMES.keys()).index(month_str) + 1 if month_str in MONTH_NAMES else 99
    try:
        day = int(day_str)
    except ValueError:
        day = 99
    return (month, day)


def presentation_end_clock(session: TalkSession) -> str:
    range_str = session.presentation_session_time
    for separator in ("–", "—", "-"):
        if separator in range_str:
            return normalize_whitespace(range_str.rsplit(separator, 1)[-1])
    return session.time


def conference_datetime(date_str: str, time_str: str) -> datetime:
    month, day = parse_date_sort_key(date_str)
    hour, minute = parse_time_sort_key(time_str)
    return datetime(CONFERENCE_YEAR, month, day, hour, minute, tzinfo=CONFERENCE_TZ)


def session_start_iso(session: TalkSession) -> str:
    return conference_datetime(session.date, session.time).isoformat()


def session_end_iso(session: TalkSession) -> str:
    return conference_datetime(session.date, presentation_end_clock(session)).isoformat()


def format_day_title(date_str: str, day_of_week: str) -> str:
    parts = normalize_whitespace(date_str).split()
    if len(parts) == 2:
        month_str, day_str = parts
        month_name = MONTH_NAMES.get(month_str, month_str)
        return f"{day_of_week}, {month_name} {day_str}"
    return f"{day_of_week}, {date_str}"


def session_key(session: TalkSession) -> str:
    return f"{session.date}|{session.track}|{session.time}"


def session_filter_label(session: TalkSession) -> str:
    return f"{format_day_title(session.date, session.day_of_week)} {session.theme}"


def day_id(date_str: str, day_of_week: str) -> str:
    parts = normalize_whitespace(date_str).split()
    if len(parts) == 2:
        month_str, day_str = parts
        return f"{month_str.lower()}-{day_str}"
    return day_of_week.lower()


def load_sessions(path: Path) -> list[TalkSession]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")

        missing = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        sessions: list[TalkSession] = []
        for row in reader:
            date = normalize_whitespace(row.get("Date", ""))
            if not date:
                continue

            talks: list[str] = []
            for col in TALK_COLUMNS:
                title = normalize_whitespace(row.get(col, "") or "")
                if title:
                    talks.append(title)

            slot_count = normalize_whitespace(
                row.get("Number of talk slots in session", "")
            )
            if not slot_count.isdigit() or int(slot_count) != len(talks):
                raise ValueError(
                    f"{path.name}: {date} track {row.get('Track', '')} declares "
                    f"{slot_count or 'no'} talk slots but contains {len(talks)} talks"
                )

            sessions.append(
                TalkSession(
                    date=date,
                    day_of_week=normalize_whitespace(row.get("Day of week", "")),
                    time=normalize_whitespace(row.get("Time", "")),
                    track=normalize_whitespace(row.get("Track", "")),
                    room=normalize_whitespace(row.get("Room", "")),
                    slot_count=slot_count,
                    theme=normalize_whitespace(row.get("Session Themes", "")),
                    talks=talks,
                )
            )

    sessions.sort(
        key=lambda s: (
            parse_date_sort_key(s.date),
            parse_time_sort_key(s.time),
            int(s.track) if s.track.isdigit() else s.track,
        )
    )
    return sessions


def load_paper_ids(path: Path) -> dict[str, int]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path.name}: CSV has no header row")

        missing = [column for column in ("num", "title") if column not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"{path.name}: missing required columns: {', '.join(missing)}"
            )

        paper_ids: dict[str, int] = {}
        seen_ids: set[int] = set()
        for row_number, row in enumerate(reader, start=2):
            title = normalize_whitespace(row.get("title", "") or "")
            try:
                paper_id = int(normalize_whitespace(row.get("num", "") or ""))
            except ValueError as error:
                raise ValueError(
                    f"{path.name}: invalid paper ID on row {row_number}"
                ) from error
            if not title:
                raise ValueError(f"{path.name}: missing title on row {row_number}")
            if title in paper_ids:
                raise ValueError(f"{path.name}: duplicate paper title: {title}")
            if paper_id in seen_ids:
                raise ValueError(f"{path.name}: duplicate paper ID: {paper_id}")
            paper_ids[title] = paper_id
            seen_ids.add(paper_id)

    return paper_ids


def assign_poster_numbers(day_sessions: list[TalkSession]) -> dict[tuple[str, str, int], int]:
    """Assign poster numbers 1..N per day, ordered by track then presentation slot."""
    poster_numbers: dict[tuple[str, str, int], int] = {}
    poster_no = 1

    tracks = sorted(
        {session.track for session in day_sessions},
        key=lambda track: int(track) if track.isdigit() else track,
    )
    for track in tracks:
        track_sessions = sorted(
            (session for session in day_sessions if session.track == track),
            key=lambda session: parse_time_sort_key(session.time),
        )
        for session in track_sessions:
            for slot in range(1, len(session.talks) + 1):
                poster_numbers[(session.track, session.time, slot)] = poster_no
                poster_no += 1

    return poster_numbers


def _icon(path_d: str) -> str:
    return (
        '<svg class="paper-icon" xmlns="http://www.w3.org/2000/svg" fill="none" '
        'viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">'
        f'<path stroke-linecap="round" stroke-linejoin="round" d="{path_d}"/>'
        "</svg>"
    )


ICON_CALENDAR = _icon(
    "M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 "
    "21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 "
    "2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5"
)
ICON_MAP_PIN = _icon(
    "M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 "
    "17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"
)
ICON_CLOCK = _icon(
    "M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
)
ICON_POSTER = _icon(
    "M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 "
    "7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-"
    ".621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-"
    ".504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
)
ICON_TAG = _icon(
    "M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c."
    "699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-"
    "2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z M6 6h.008v.008H6V6Z"
)
ICON_CHEVRON = (
    '<svg class="paper-chevron" xmlns="http://www.w3.org/2000/svg" fill="none" '
    'viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/>'
    "</svg>"
)


def render_paper_row(
    session: TalkSession,
    title: str,
    slot: int,
    poster_no: int,
    proceedings_links: ProceedingsLinks | None = None,
    is_journal_to_conference: bool = False,
) -> str:
    search_parts = [title]
    if proceedings_links:
        search_parts.append(proceedings_links.authors)
    search_text = html.escape(" ".join(search_parts).lower(), quote=True)
    session_key_html = html.escape(session_key(session), quote=True)
    title_text_html = html.escape(title)
    presentation_html = html.escape(session.presentation_session_time)
    poster_html = html.escape(session.poster_time) if session.poster_time else "TBD"
    journal_class = " is-journal" if is_journal_to_conference else ""
    journal_mark_html = ""
    journal_badge_html = ""
    if is_journal_to_conference:
        journal_mark_html = (
            '                                            <span class="journal-mark" '
            'title="Journal-to-Conference">J</span>\n'
        )
        journal_badge_html = (
            '<span class="inline-flex rounded-full bg-rlyellow-100 px-2.5 py-1 '
            'text-xs font-semibold text-rlyellow-900">Journal-to-Conference</span>'
        )

    authors_full_html = ""
    title_html = title_text_html
    pdf_summary_html = ""
    pdf_details_html = ""
    if proceedings_links:
        escaped_page_url = html.escape(proceedings_links.page_url, quote=True)
        escaped_pdf_url = html.escape(proceedings_links.pdf_url, quote=True)
        authors_escaped = html.escape(proceedings_links.authors)
        title_html = (
            f'<a class="paper-title-link underline hover:text-rldarkblue-500" '
            f'href="{escaped_page_url}" target="_blank" rel="noopener noreferrer">'
            f"{title_text_html}</a>"
        )
        authors_full_html = (
            f'<p class="text-sm text-rldarkblue-700">{authors_escaped}</p>'
        )
        pdf_label = html.escape(f"View PDF: {title}", quote=True)
        pdf_summary_html = (
            f'                                            <a class="paper-pdf-link font-medium '
            f'text-blue underline hover:text-rldarkblue-500" href="{escaped_pdf_url}" '
            f'target="_blank" rel="noopener noreferrer" aria-label="{pdf_label}">PDF</a>\n'
        )
        pdf_details_html = (
            f'<a class="font-medium text-blue underline hover:text-rldarkblue-500" '
            f'href="{escaped_pdf_url}" target="_blank" rel="noopener noreferrer">'
            f"PDF</a>"
        )

    details_bits = [bit for bit in (journal_badge_html, authors_full_html) if bit]
    details_bits.append(
        f'<ul class="paper-meta">'
        f"<li>{ICON_CLOCK}<span>"
        f'<span class="font-medium">Presentation</span> Talk {slot} · {presentation_html}'
        f"</span></li>"
        f"<li>{ICON_POSTER}<span>"
        f'<span class="font-medium">Poster</span> #{poster_no} · {poster_html}</span></li>'
        f"</ul>"
    )
    if pdf_details_html:
        details_bits.append(pdf_details_html)
    details_html = "\n                                    ".join(details_bits)

    return (
        f'                                    <details class="paper-item{journal_class}" '
        f'data-search-text="{search_text}" data-session-key="{session_key_html}">\n'
        f'                                        <summary class="paper-summary">\n'
        f'                                            <span class="paper-talk-no">'
        f"Talk {slot}</span>\n"
        f"{journal_mark_html}"
        f'                                            <span class="paper-summary-main">'
        f'<span class="paper-title">{title_html}</span></span>\n'
        f"{pdf_summary_html}"
        f"                                            {ICON_CHEVRON}\n"
        f"                                        </summary>\n"
        f'                                        <div class="paper-expand">\n'
        f"                                    {details_html}\n"
        f"                                        </div>\n"
        f"                                    </details>\n"
    )


def render_session_block(
    session: TalkSession,
    proceedings_links: dict[str, ProceedingsLinks],
    journal_to_conference_titles: set[str],
    poster_numbers: dict[tuple[str, str, int], int],
) -> str:
    papers_html = "".join(
        render_paper_row(
            session,
            title,
            slot,
            poster_numbers[(session.track, session.time, slot)],
            proceedings_links.get(title),
            title in journal_to_conference_titles,
        )
        for slot, title in enumerate(session.talks, start=1)
    )
    if not papers_html:
        return ""

    key_html = html.escape(session_key(session), quote=True)
    theme_html = html.escape(session.theme)
    track_html = html.escape(session.track)
    room_html = html.escape(session.room)
    return (
        f'                            <article class="session-block" '
        f'data-session-key="{key_html}">\n'
        f'                                <header class="session-header">\n'
        f'                                    <h3 class="session-theme">{theme_html}</h3>\n'
        f'                                    <p class="session-meta">'
        f'<span class="session-meta-item">{ICON_TAG}<span>Track {track_html}</span></span>'
        f'<span class="session-meta-item">{ICON_MAP_PIN}<span>Room {room_html}</span></span></p>\n'
        f"                                </header>\n"
        f'                                <div class="paper-list">\n'
        f"{papers_html}"
        f"                                </div>\n"
        f"                            </article>\n"
    )


def render_session_filter_options(sessions: list[TalkSession]) -> str:
    options = [
        '                    <option value="">All sessions</option>\n'
    ]
    seen: set[str] = set()
    for session in sessions:
        key = session_key(session)
        if key in seen:
            continue
        seen.add(key)
        options.append(
            f'                    <option value="{html.escape(key)}">'
            f"{html.escape(session_filter_label(session))}</option>\n"
        )
    return "".join(options)


def render_time_slot(
    slot_sessions: list[TalkSession],
    proceedings_links: dict[str, ProceedingsLinks],
    journal_to_conference_titles: set[str],
    poster_numbers: dict[tuple[str, str, int], int],
) -> str:
    if not slot_sessions:
        return ""
    first = slot_sessions[0]
    sessions_html = "".join(
        render_session_block(
            session,
            proceedings_links,
            journal_to_conference_titles,
            poster_numbers,
        )
        for session in slot_sessions
    )
    if not sessions_html:
        return ""
    start_iso = html.escape(session_start_iso(first), quote=True)
    end_iso = html.escape(session_end_iso(first), quote=True)
    time_html = html.escape(first.presentation_session_time)
    return (
        f'                    <div class="time-slot" data-start="{start_iso}" '
        f'data-end="{end_iso}">\n'
        f'                        <div class="time-slot-heading">'
        f"{ICON_CLOCK}<span>{time_html}</span>"
        f'<span class="live-pill" hidden></span></div>\n'
        f'                        <div class="session-stack">\n'
        f"{sessions_html}"
        f"                        </div>\n"
        f"                    </div>\n"
    )


def render_day_section(
    sessions: list[TalkSession],
    proceedings_links: dict[str, ProceedingsLinks],
    journal_to_conference_titles: set[str],
) -> str:
    if not sessions:
        return ""
    poster_numbers = assign_poster_numbers(sessions)
    slots_html = "".join(
        render_time_slot(
            list(slot_sessions),
            proceedings_links,
            journal_to_conference_titles,
            poster_numbers,
        )
        for _, slot_sessions in groupby(sessions, key=lambda session: session.time)
    )
    if not slots_html:
        return ""
    day_title = html.escape(
        format_day_title(sessions[0].date, sessions[0].day_of_week)
    )
    return (
        f'                <section class="day-section mb-12">\n'
        f'                    <h2 class="day-heading">{ICON_CALENDAR}'
        f"<span>{day_title}</span></h2>\n"
        f"{slots_html}"
        f"                </section>\n"
    )


def render_schedule_sections(
    sessions: list[TalkSession],
    proceedings_links: dict[str, ProceedingsLinks],
    journal_to_conference_titles: set[str],
) -> str:
    if not sessions:
        return '                <p class="text-center text-rldarkblue-900">No papers found.</p>\n'

    sections: list[str] = []
    current_day_id: str | None = None
    day_sessions: list[TalkSession] = []

    def flush_day() -> None:
        if not day_sessions:
            return
        section = render_day_section(
            day_sessions, proceedings_links, journal_to_conference_titles
        )
        if section:
            sections.append(section)

    for session in sessions:
        did = day_id(session.date, session.day_of_week)
        if did != current_day_id:
            if current_day_id is not None:
                flush_day()
                day_sessions = []
            current_day_id = did
        day_sessions.append(session)

    flush_day()
    return "".join(sections)


def render_html(
    sessions: list[TalkSession],
    proceedings_links: dict[str, ProceedingsLinks] | None = None,
    journal_to_conference_titles: set[str] | None = None,
) -> str:
    schedule_sections = render_schedule_sections(
        sessions,
        proceedings_links or {},
        journal_to_conference_titles or set(),
    )
    session_filter_options = render_session_filter_options(sessions)

    return f"""<!doctype html>
<script src="jquery.js"></script>
<script src="data.js"></script>

<!-- Generated by generate_paper_schedule.py -->

<html lang="en-us">
<head>
    <meta charset="UTF-8">
    <title id="mainPageTitleforSEO">Paper Schedule | RLC 2026</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;1,400;1,500&family=Rubik:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap"
        rel="stylesheet">
    <link href="build.css" rel="stylesheet">
    <link rel="icon" type="image/png" href="/favicon-48x48.png" sizes="48x48"/>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
    <link rel="shortcut icon" href="/favicon.ico"/>
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
    <meta name="apple-mobile-web-app-title" content="RLC"/>
    <link rel="manifest" href="/site.webmanifest"/>
    <meta id="seodescription" name="description" content="Paper presentation and poster schedule for RLC 2026 in Montréal.">
    <style>
        .paper-item.hidden-by-search,
        .session-block.hidden-by-search,
        .time-slot.hidden-by-search,
        .day-section.hidden-by-search {{
            display: none;
        }}
        #paperSearch:focus,
        #paperSessionFilter:focus {{
            outline: 2px solid rgb(27 58 158);
            outline-offset: 2px;
        }}
        .day-heading {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0 1.25rem;
            color: rgb(27 58 158);
            font-family: Rubik, sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            line-height: 1.3;
        }}
        .day-heading .paper-icon {{
            width: 1.25rem;
            height: 1.25rem;
        }}
        .time-slot {{
            margin-bottom: 1.75rem;
            scroll-margin-top: 1rem;
        }}
        .time-slot-heading {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem 0.75rem;
            margin-bottom: 0.75rem;
            padding: 0.35rem 0;
            color: rgb(27 58 158);
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.3;
            border-bottom: 2px solid rgba(27, 58, 158, 0.15);
        }}
        .time-slot-heading .paper-icon {{
            width: 1.15rem;
            height: 1.15rem;
        }}
        .live-pill {{
            display: inline-flex;
            align-items: center;
            padding: 0.15rem 0.55rem;
            border-radius: 9999px;
            background: rgb(27 58 158);
            color: white;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .live-pill[hidden] {{
            display: none;
        }}
        .time-slot.is-live {{
            background: rgba(27, 58, 158, 0.04);
            border-radius: 0.75rem;
            padding: 0.75rem 0.75rem 0.25rem;
            outline: 1px solid rgba(27, 58, 158, 0.18);
        }}
        .session-stack {{
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }}
        .session-block {{
            background: rgba(27, 58, 158, 0.05);
            border-radius: 0.75rem;
            padding: 0.85rem 1rem 0.5rem;
        }}
        .session-header {{
            margin-bottom: 0.35rem;
        }}
        .session-theme {{
            margin: 0 0 0.25rem;
            color: rgb(27 58 158);
            font-family: Rubik, sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            line-height: 1.35;
        }}
        .session-meta {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.35rem 1rem;
            margin: 0 0 0.35rem;
            color: rgb(30 41 82);
            font-size: 0.85rem;
        }}
        .session-meta-item {{
            display: inline-flex;
            align-items: center;
        }}
        .session-meta .paper-icon {{
            width: 0.95rem;
            height: 0.95rem;
            margin-right: 0.3rem;
            color: rgb(27 58 158);
            opacity: 0.8;
        }}
        .paper-list {{
            display: flex;
            flex-direction: column;
        }}
        .paper-item {{
            border-top: 1px solid rgba(27, 58, 158, 0.1);
        }}
        .paper-item.is-journal {{
            box-shadow: inset 3px 0 0 rgb(253 224 71);
        }}
        .paper-summary {{
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            padding: 0.45rem 0.15rem;
            cursor: pointer;
            list-style: none;
        }}
        .paper-summary::-webkit-details-marker {{
            display: none;
        }}
        .paper-talk-no {{
            flex-shrink: 0;
            padding-top: 0.15rem;
            color: rgb(27 58 158);
            font-size: 0.75rem;
            font-weight: 700;
            white-space: nowrap;
        }}
        .journal-mark {{
            flex-shrink: 0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.1rem;
            height: 1.1rem;
            margin-top: 0.15rem;
            border-radius: 9999px;
            background: rgb(254 249 195);
            color: rgb(113 63 18);
            font-size: 0.65rem;
            font-weight: 700;
        }}
        .paper-summary-main {{
            flex: 1;
            min-width: 0;
        }}
        .paper-title {{
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
            line-clamp: 2;
            overflow: hidden;
            color: rgb(27 58 158);
            font-size: 0.95rem;
            font-weight: 600;
            line-height: 1.35;
            white-space: normal;
        }}
        .paper-title-link {{
            color: inherit;
            white-space: normal;
        }}
        .paper-pdf-link {{
            flex-shrink: 0;
            padding-top: 0.15rem;
            font-size: 0.8rem;
        }}
        .paper-chevron {{
            flex-shrink: 0;
            width: 1rem;
            height: 1rem;
            margin-top: 0.2rem;
            color: rgb(27 58 158);
            opacity: 0.7;
            transition: transform 0.15s ease;
        }}
        .paper-item[open] .paper-chevron {{
            transform: rotate(180deg);
        }}
        .paper-expand {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            padding: 0 0.15rem 0.7rem 3.15rem;
        }}
        .paper-meta {{
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }}
        .paper-meta li {{
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            color: rgb(30 41 82);
            font-size: 0.9rem;
            line-height: 1.4;
        }}
        .paper-meta .paper-icon {{
            width: 1.05rem;
            height: 1.05rem;
            flex-shrink: 0;
            margin-top: 0.15rem;
            color: rgb(27 58 158);
            opacity: 0.8;
        }}
        @media (max-width: 639px) {{
            .paper-expand {{
                padding-left: 0.15rem;
            }}
        }}
    </style>
</head>

<body class="font-roboto text-rldarkblue-950 bg-white antialiased">

<div class="container mx-auto">
    <div class="flex flex-col min-h-screen justify-between">
        <div>
            <div class="m-2 grid grid-cols-3 items-center rounded-md mt-4 p-2 border-0 border-rldarkblue-900">
                <div class="p-2 w-full rounded-md">
                    <div class="hidden lg:block max-w-60">
                        <a href="index.html"><img alt="Company logo" src="data/logos/rlc-logo.svg"/></a>
                    </div>
                    <div class="block pt-1 lg:hidden max-w-60">
                        <a href="index.html"><img alt="Company logo" src="data/logos/rlc-logo.svg"/></a>
                    </div>
                </div>
                <div></div>
                <div id="largeMenu" class="p-2 m-1 w-full hidden lg:block rounded-md"></div>
                <div id="collapsedMenu" class="p-2 m-1 w-full block lg:hidden rounded-md">
                    <div class="relative flex flex-row-reverse">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                             stroke="currentColor"
                             class="size-10 p-1 font-rubik text-xl m-1 text-rldarkblue-900 hover:text-rldarkblue-500 hover:cursor-pointer"
                             onclick="showMenu()">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                  d="M3.75 5.25h16.5m-16.5 4.5h16.5m-16.5 4.5h16.5m-16.5 4.5h16.5"/>
                        </svg>
                        <div id="collapsedMenuItems"
                             class="absolute top-10 z-10 hidden w-40 shadow-md bg-white/95 backdrop-blur-md rounded-md p-4 m-4 grid grid-cols-1">
                        </div>
                    </div>
                </div>
            </div>

            <h1 class="text-3xl text-blue text-center font-rubik p-2 m-2 mt-20 mb-3">RLC 2026 Paper Schedule</h1>

            <!-- SEARCH + SESSION FILTER -->
            <div class="max-w-4xl mx-auto px-4 mb-8">
                <label for="paperSessionFilter" class="block text-center text-sm text-rldarkblue-600 mb-2">
                    Filter by session
                </label>
                <select id="paperSessionFilter"
                        class="w-full rounded-lg px-6 py-4 text-lg text-rldarkblue-900 bg-rldarkblue-50/50 mb-4">
{session_filter_options}                </select>
                <label for="paperSearch" class="block text-center text-sm text-rldarkblue-600 mb-2">
                    Search by paper title or author
                </label>
                <input id="paperSearch" type="search" placeholder="Search by paper title or author..."
                       class="w-full rounded-lg px-6 py-4 text-lg text-rldarkblue-900 bg-rldarkblue-50/50"
                       autocomplete="off">
                <p id="searchStatus" class="text-center text-sm text-rldarkblue-600 mt-2" aria-live="polite"></p>
            </div>

            <div id="noResults" class="hidden text-center text-rldarkblue-900 text-base mb-8 px-4">
                No papers match your filters.
            </div>

            <!-- PAPER SCHEDULE CONTENT -->
            <div id="scheduleContent" class="p-2 sm:p-4 max-w-5xl mx-auto">
{schedule_sections}
            </div>

        </div>

        <div class="grid grid-cols-4 items-center">
            <div id="footerText"
                 class="p-2 m-2 w-full col-span-3 rounded-md text-rldarkblue-900 font-roboto text-xs sm:text-base">
            </div>
            <div class="p-2 m-1 w-full col-span-1">
                <div class="flex flex-row-reverse p-2 ml-auto max-w-60">
                    <div><img alt="Company logo" class="p-1 m-1 w-60" src="data/logos/rlc-logo.svg"/></div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function applyFilters() {{
        var query = document.getElementById('paperSearch').value.trim().toLowerCase();
        var sessionKey = document.getElementById('paperSessionFilter').value;
        var paperItems = document.querySelectorAll('.paper-item');
        var visibleCount = 0;
        var filtersActive = Boolean(query || sessionKey);

        paperItems.forEach(function (item) {{
            var text = item.getAttribute('data-search-text') || '';
            var itemSession = item.getAttribute('data-session-key') || '';
            var matchesQuery = !query || text.indexOf(query) !== -1;
            var matchesSession = !sessionKey || itemSession === sessionKey;
            var matches = matchesQuery && matchesSession;
            item.classList.toggle('hidden-by-search', !matches);
            if (matches) {{
                visibleCount += 1;
            }}
        }});

        document.querySelectorAll('.session-block').forEach(function (block) {{
            var visiblePapers = block.querySelectorAll('.paper-item:not(.hidden-by-search)');
            block.classList.toggle('hidden-by-search', visiblePapers.length === 0);
        }});
        document.querySelectorAll('.time-slot').forEach(function (slot) {{
            var visibleSessions = slot.querySelectorAll('.session-block:not(.hidden-by-search)');
            slot.classList.toggle('hidden-by-search', visibleSessions.length === 0);
        }});
        document.querySelectorAll('.day-section').forEach(function (day) {{
            var visiblePapers = day.querySelectorAll('.paper-item:not(.hidden-by-search)');
            day.classList.toggle('hidden-by-search', visiblePapers.length === 0);
        }});

        var status = document.getElementById('searchStatus');
        var noResults = document.getElementById('noResults');
        if (filtersActive) {{
            status.textContent = visibleCount + ' paper' + (visibleCount === 1 ? '' : 's') + ' found';
            noResults.classList.toggle('hidden', visibleCount > 0);
        }} else {{
            status.textContent = '';
            noResults.classList.add('hidden');
        }}
    }}

    function syncSessionToUrl(sessionKey) {{
        var url = new URL(window.location.href);
        if (sessionKey) {{
            url.searchParams.set('session', sessionKey);
        }} else {{
            url.searchParams.delete('session');
        }}
        window.history.replaceState(null, '', url);
    }}

    function markLiveSlot() {{
        var slots = document.querySelectorAll('.time-slot[data-end]');
        var now = Date.now();
        var live = null;
        slots.forEach(function (slot) {{
            slot.classList.remove('is-live');
            var pill = slot.querySelector('.live-pill');
            if (pill) {{
                pill.hidden = true;
                pill.textContent = '';
            }}
            var end = Date.parse(slot.getAttribute('data-end'));
            if (!live && !isNaN(end) && end > now) {{
                live = slot;
            }}
        }});
        if (!live) {{
            return null;
        }}
        live.classList.add('is-live');
        var livePill = live.querySelector('.live-pill');
        if (livePill) {{
            var start = Date.parse(live.getAttribute('data-start'));
            livePill.textContent = (!isNaN(start) && now >= start) ? 'Now' : 'Up next';
            livePill.hidden = false;
        }}
        return live;
    }}

    document.addEventListener('DOMContentLoaded', function () {{
        var searchInput = document.getElementById('paperSearch');
        var sessionFilter = document.getElementById('paperSessionFilter');
        var params = new URLSearchParams(window.location.search);
        var sessionFromUrl = params.get('session');
        var skipLiveScroll = false;
        if (sessionFromUrl) {{
            var hasOption = Array.prototype.some.call(sessionFilter.options, function (option) {{
                return option.value === sessionFromUrl;
            }});
            if (hasOption) {{
                sessionFilter.value = sessionFromUrl;
                skipLiveScroll = true;
            }}
        }}

        searchInput.addEventListener('input', applyFilters);
        sessionFilter.addEventListener('change', function () {{
            syncSessionToUrl(sessionFilter.value);
            applyFilters();
        }});
        document.querySelectorAll('.paper-summary a').forEach(function (link) {{
            link.addEventListener('click', function (event) {{
                event.stopPropagation();
            }});
        }});
        applyFilters();
        var live = markLiveSlot();
        if (live && !skipLiveScroll) {{
            live.scrollIntoView({{ block: 'start' }});
        }}
        setInterval(markLiveSlot, 60000);
    }});
</script>

</body>
<script src="menu.js"></script>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv", type=Path, default=DEFAULT_CSV, help="Path to talk_assignment.csv"
    )
    parser.add_argument(
        "--papers-csv",
        type=Path,
        default=DEFAULT_PAPERS_CSV,
        help="Path to list_of_papers.csv",
    )
    parser.add_argument(
        "--html", type=Path, default=DEFAULT_HTML, help="Path to output paper_schedule.html"
    )
    parser.add_argument(
        "--proceedings-url",
        default=DEFAULT_PROCEEDINGS_URL,
        help="RLJ issue page used to resolve direct PDF links",
    )
    args = parser.parse_args()

    for path in (args.csv, args.papers_csv):
        if not path.exists():
            print(f"CSV not found: {path}", file=sys.stderr)
            return 1

    try:
        sessions = load_sessions(args.csv)
        paper_ids = load_paper_ids(args.papers_csv)
        schedule_titles = [
            title for session in sessions for title in session.talks
        ]
        schedule_title_set = set(schedule_titles)
        paper_title_set = set(paper_ids)
        if schedule_title_set != paper_title_set:
            only_in_schedule = sorted(schedule_title_set - paper_title_set)
            only_in_paper_list = sorted(paper_title_set - schedule_title_set)
            details = []
            if only_in_schedule:
                details.append(f"only in schedule: {', '.join(only_in_schedule)}")
            if only_in_paper_list:
                details.append(f"only in paper list: {', '.join(only_in_paper_list)}")
            raise ValueError("paper CSVs do not match (" + "; ".join(details) + ")")
    except ValueError as error:
        print(f"Invalid paper data: {error}", file=sys.stderr)
        return 1

    journal_to_conference_titles = {
        title for title, paper_id in paper_ids.items() if paper_id >= 500
    }
    try:
        available_proceedings_links = load_proceedings_links(args.proceedings_url)
        proceedings_links, unmatched, unused = match_proceedings_links(
            schedule_titles, available_proceedings_links
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Could not load proceedings links: {error}", file=sys.stderr)
        return 1

    args.html.write_text(
        render_html(
            sessions,
            proceedings_links,
            journal_to_conference_titles,
        ),
        encoding="utf-8",
    )
    paper_count = sum(len(session.talks) for session in sessions)
    print(
        f"Generated {args.html} from {args.csv} "
        f"({len(sessions)} sessions, {paper_count} papers, "
        f"{len(proceedings_links)} proceedings links)"
    )
    if unmatched:
        print(f"Unmatched schedule papers ({len(unmatched)}):", file=sys.stderr)
        for title in unmatched:
            print(f"  - {title}", file=sys.stderr)
    if unused:
        print(f"Unused proceedings papers ({len(unused)}):", file=sys.stderr)
        for title in unused:
            print(f"  - {title}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
