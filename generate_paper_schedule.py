#!/usr/bin/env python3
"""Generate paper_schedule.html from TalkSchedule.csv."""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "TalkSchedule.csv"
DEFAULT_HTML = ROOT / "paper_schedule.html"

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


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


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


def format_day_title(date_str: str, day_of_week: str) -> str:
    parts = normalize_whitespace(date_str).split()
    if len(parts) == 2:
        month_str, day_str = parts
        month_name = MONTH_NAMES.get(month_str, month_str)
        return f"{day_of_week}, {month_name} {day_str}"
    return f"{day_of_week}, {date_str}"


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

            sessions.append(
                TalkSession(
                    date=date,
                    day_of_week=normalize_whitespace(row.get("Day of week", "")),
                    time=normalize_whitespace(row.get("Time", "")),
                    track=normalize_whitespace(row.get("Track", "")),
                    room=normalize_whitespace(row.get("Room", "")),
                    slot_count=normalize_whitespace(
                        row.get("Number of talk slots in session", "")
                    ),
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


def render_paper_card(
    session: TalkSession, title: str, slot: int, poster_no: int
) -> str:
    search_text = html.escape(title.lower())
    title_html = html.escape(title)
    date_html = html.escape(format_day_title(session.date, session.day_of_week))
    room_html = html.escape(session.room)
    track_html = html.escape(session.track)
    theme_html = html.escape(session.theme)
    presentation_html = html.escape(session.presentation_session_time)
    poster_html = html.escape(session.poster_time) if session.poster_time else "TBD"

    return (
        f'                            <div class="paper-item bg-rldarkblue-50/50 rounded-lg p-4 sm:p-6 m-2" '
        f'data-search-text="{search_text}">\n'
        f'                                <div class="paper-date">{ICON_CALENDAR}'
        f'<span>{date_html}</span></div>\n'
        f'                                <h4 class="text-base sm:text-lg font-semibold text-blue mb-3">'
        f"{title_html}</h4>\n"
        f'                                <ul class="paper-meta">\n'
        f'                                    <li>{ICON_TAG}<span>'
        f'<span class="font-medium">Track {track_html}</span> · {theme_html}</span></li>\n'
        f'                                    <li>{ICON_MAP_PIN}<span>'
        f'<span class="font-medium">Room</span> {room_html}</span></li>\n'
        f'                                    <li>{ICON_CLOCK}<span>'
        f'<span class="font-medium">Presentation</span> Talk {slot} · {presentation_html}</span></li>\n'
        f'                                    <li>{ICON_POSTER}<span>'
        f'<span class="font-medium">Poster</span> #{poster_no} · {poster_html}</span></li>\n'
        f"                                </ul>\n"
        f"                            </div>\n"
    )


def render_day_section(sessions: list[TalkSession]) -> str:
    poster_numbers = assign_poster_numbers(sessions)
    cards_html = "".join(
        render_paper_card(
            session,
            title,
            slot,
            poster_numbers[(session.track, session.time, slot)],
        )
        for session in sessions
        for slot, title in enumerate(session.talks, start=1)
    )
    if not cards_html:
        return ""

    return (
        f'                <section class="day-section mb-10">\n'
        f'                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-2">\n'
        f"{cards_html}"
        f"                    </div>\n"
        f"                </section>\n"
    )


def render_schedule_sections(sessions: list[TalkSession]) -> str:
    if not sessions:
        return '                <p class="text-center text-rldarkblue-900">No papers found.</p>\n'

    sections: list[str] = []
    current_day_id: str | None = None
    day_sessions: list[TalkSession] = []

    def flush_day() -> None:
        if not day_sessions:
            return
        section = render_day_section(day_sessions)
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


def render_html(sessions: list[TalkSession]) -> str:
    schedule_sections = render_schedule_sections(sessions)

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
        .paper-item.hidden-by-search {{
            display: none;
        }}
        .day-section.hidden-by-search {{
            display: none;
        }}
        #paperSearch:focus {{
            outline: 2px solid rgb(27 58 158);
            outline-offset: 2px;
        }}
        .paper-date {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.75rem;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            background: rgba(27, 58, 158, 0.1);
            color: rgb(27 58 158);
            font-size: 0.8rem;
            font-weight: 600;
            line-height: 1.25;
        }}
        .paper-date .paper-icon {{
            width: 0.95rem;
            height: 0.95rem;
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
        @media (min-width: 640px) {{
            .paper-meta li {{
                font-size: 1rem;
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

            <!-- SEARCH -->
            <div class="max-w-4xl mx-auto px-4 mb-8">
                <label for="paperSearch" class="block text-center text-sm text-rldarkblue-600 mb-2">
                    Search by paper title
                </label>
                <input id="paperSearch" type="search" placeholder="Search by paper title..."
                       class="w-full rounded-lg px-6 py-4 text-lg text-rldarkblue-900 bg-rldarkblue-50/50"
                       autocomplete="off">
                <p id="searchStatus" class="text-center text-sm text-rldarkblue-600 mt-2" aria-live="polite"></p>
            </div>

            <div id="noResults" class="hidden text-center text-rldarkblue-900 text-base mb-8 px-4">
                No papers match your search.
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
    function applySearchFilter() {{
        var query = document.getElementById('paperSearch').value.trim().toLowerCase();
        var paperItems = document.querySelectorAll('.paper-item');
        var visibleCount = 0;

        paperItems.forEach(function (item) {{
            var text = item.getAttribute('data-search-text') || '';
            var matches = !query || text.indexOf(query) !== -1;
            item.classList.toggle('hidden-by-search', !matches);
            if (matches && text) {{
                visibleCount += 1;
            }}
        }});

        document.querySelectorAll('.day-section').forEach(function (day) {{
            var visiblePapers = day.querySelectorAll('.paper-item:not(.hidden-by-search)');
            day.classList.toggle('hidden-by-search', visiblePapers.length === 0);
        }});

        var status = document.getElementById('searchStatus');
        var noResults = document.getElementById('noResults');
        if (query) {{
            status.textContent = visibleCount + ' paper' + (visibleCount === 1 ? '' : 's') + ' found';
            noResults.classList.toggle('hidden', visibleCount > 0);
        }} else {{
            status.textContent = '';
            noResults.classList.add('hidden');
        }}
    }}

    document.addEventListener('DOMContentLoaded', function () {{
        document.getElementById('paperSearch').addEventListener('input', applySearchFilter);
    }});
</script>

</body>
<script src="menu.js"></script>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to TalkSchedule.csv")
    parser.add_argument(
        "--html", type=Path, default=DEFAULT_HTML, help="Path to output paper_schedule.html"
    )
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    sessions = load_sessions(args.csv)
    args.html.write_text(render_html(sessions), encoding="utf-8")
    paper_count = sum(len(session.talks) for session in sessions)
    print(f"Generated {args.html} from {args.csv} ({len(sessions)} sessions, {paper_count} papers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
