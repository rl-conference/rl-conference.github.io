#!/usr/bin/env python3
"""Update schedule.html from RLCSchedyle.csv."""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "RLCSchedyle.csv"
DEFAULT_HTML = ROOT / "schedule.html"

DAYS = [
    {"id": "friday", "col": 1, "label": "Fri Aug 14", "title": "Friday, August 14"},
    {
        "id": "saturday",
        "col": 2,
        "label": "Sat Aug 15 (Workshops)",
        "title": "Saturday, August 15 (Workshops)",
    },
    {"id": "sunday", "col": 3, "label": "Sun Aug 16", "title": "Sunday, August 16"},
    {"id": "monday", "col": 4, "label": "Mon Aug 17", "title": "Monday, August 17"},
    {"id": "tuesday", "col": 5, "label": "Tue Aug 18", "title": "Tuesday, August 18"},
]

DEFAULT_DAY = "saturday"

BUTTON_CLASSES = (
    "day-btn bg-rldarkblue-200 text-rldarkblue-900 px-4 py-2 sm:px-6 sm:py-3 "
    "rounded-lg font-semibold text-sm sm:text-base hover:bg-rldarkblue-300 transition-colors"
)

WORKSHOP_TIME_RE = re.compile(r"^Workshops\s*-\s*(.+)$", re.I)

WORKSHOPS = [
    (
        "Continual Reinforcement Learning Workshop",
        "https://sites.google.com/view/continual-learning",
        "B-4205",
    ),
    (
        "Model-Based Reinforcement Learning in the Era of Generative World Models",
        "https://worldmodels-rlc.github.io/",
        "B-4215",
    ),
    (
        "Reinforcement Learning and Video Games",
        "https://sites.google.com/view/rlvg-2026/home",
        "B-4225",
    ),
    (
        "Reinforcement Learning in Big Worlds",
        "https://rlinbigworlds.ca/",
        "B-4315",
    ),
    (
        "Workshop on Reinforcement Learning Beyond Rewards: Towards Scalable General-Purpose Agents",
        "https://rlbrew-workshop.github.io/",
        "B-4325",
    ),
    (
        "Finding the Frame: A Workshop for Examining Conceptual Frameworks in RL",
        "https://sites.google.com/view/findingtheframe/home",
        "B-4335",
    ),
    (
        "Automated RL",
        "https://sites.google.com/view/automatedrl/home",
        "B-4345",
    ),
]

PARALLEL_TRACKS_DETAIL = "4 parallel tracks: B-2305, B-0325, B-2325, B-0305"

EVENT_LOCATIONS: dict[tuple[str, str], str] = {
    ("saturday", "Lunch"): "B-2294_532",
    ("saturday", "Light reception"): "On campus",
    ("sunday", "Opening comments"): "532B",
    ("sunday", "Keynote: Marc Bellemare"): "532B",
    ("sunday", "Presentation schedule"): "Parallel track rooms",
    ("sunday", "Lunch"): "B-2294_532",
    ("sunday", "Poster session"): "Poster area",
    ("sunday", "Cirque du Soleil"): "TBD",
    ("sunday", "Reception"): "TBD",
    ("monday", "Keynote: Sheila McIlraith"): "532B",
    ("monday", "Presentation schedule"): "Parallel track rooms",
    ("monday", "Lunch"): "B-2294_532",
    ("monday", "Keynote: Danijar Hafner"): "532B",
    ("monday", "Poster session"): "Poster area",
    ("tuesday", "Keynote: Rika Antonova"): "B-0245 and B-2245",
    ("tuesday", "Presentation schedule"): "Parallel track rooms",
    ("tuesday", "Lunch"): "B-2294_532",
    ("tuesday", "Townhall"): "Salle Claude-Champagne",
    ("tuesday", "Keynote: Balaraman Ravindran"): "B-0245 and B-2245",
    ("tuesday", "Poster session"): "Poster area",
}

TIME_RANGE_RE = re.compile(r"\(([^)]+)\)\s*$")
INLINE_TIME_RE = re.compile(r"\s*\(([^)]+)\)\s*$")
BREAK_RE = re.compile(r"^Break\s*\((\d+)\s*min\)\s*$", re.I)
KEYNOTE_RE = re.compile(r"^Keynote Speaker\s*-\s*(.+)$", re.I)
DETAIL_RE = re.compile(
    r"^(\d+\s+parallel\s+sessions|\d+\s+posters\b.*|Provided by RLC|Salle .+)$",
    re.I,
)
SKIP_FRIDAY_RE = re.compile(r"^(Registration Desk|Setup)$", re.I)
OPEN_ENDED_RE = re.compile(r"\.\.\.|…", re.I)

NAME_FIXUPS = {
    "Rika Anntonova": "Rika Antonova",
    "Danijar Hafnar": "Danijar Hafner",
    "Balaraman Rivindran": "Balaraman Ravindran",
}


@dataclass
class ScheduleEvent:
    kind: str  # "event" or "break"
    title: str
    time_display: str = ""
    details: list[str] = field(default_factory=list)
    bold: bool = False
    location: str = ""


@dataclass
class DaySchedule:
    subtitle_parts: list[str] = field(default_factory=list)
    items: list[ScheduleEvent] = field(default_factory=list)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def fix_name(name: str) -> str:
    cleaned = normalize_whitespace(name)
    return NAME_FIXUPS.get(cleaned, cleaned)


def parse_time_token(token: str) -> tuple[int, int] | None:
    token = token.strip().lower()
    if not token or OPEN_ENDED_RE.search(token):
        return None

    token = token.replace(";", ":")
    token = re.sub(r"noon", "pm", token)
    if token.endswith("am") or token.endswith("pm"):
        period = token[-2:]
        body = token[:-2].strip()
    else:
        return None

    if body in {"12", "12:"}:
        hour, minute = 12, 0
    elif ":" in body:
        hour_str, minute_str = body.split(":", 1)
        hour = int(hour_str)
        minute = int(minute_str or "0")
    else:
        hour = int(body)
        minute = 0

    if period == "am":
        if hour == 12:
            hour = 0
    elif hour != 12:
        hour += 12

    return hour, minute


def format_time(hour: int, minute: int) -> str:
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12
    if display_hour == 0:
        display_hour = 12
    if minute:
        return f"{display_hour}:{minute:02d} {period}"
    return f"{display_hour} {period}"


def parse_time_range(raw: str) -> str:
    raw = normalize_whitespace(raw)
    if OPEN_ENDED_RE.search(raw):
        left = raw.split("-", 1)[0].strip()
        start = parse_time_token(left)
        if start:
            return f"{format_time(*start)}+"
        return raw

    if "-" not in raw:
        parsed = parse_time_token(raw)
        return format_time(*parsed) if parsed else raw

    start_raw, end_raw = raw.split("-", 1)
    start = parse_time_token(start_raw)
    end = parse_time_token(end_raw)
    if start and end:
        return f"{format_time(*start)} – {format_time(*end)}"
    return raw


def looks_like_time_range(text: str) -> bool:
    lowered = text.lower()
    if OPEN_ENDED_RE.search(lowered):
        return True
    return bool(re.search(r"\d", lowered) and re.search(r"(am|pm|noon)", lowered))


def extract_inline_time(line: str) -> tuple[str, str | None]:
    match = INLINE_TIME_RE.search(line)
    if not match or not looks_like_time_range(match.group(1)):
        return line, None
    title = normalize_whitespace(line[: match.start()])
    return title, parse_time_range(match.group(1))


def is_subtitle_line(line: str) -> bool:
    lowered = line.lower()
    return (
        "coffee/tea" in lowered
        or "coffee / tea" in lowered
        or "breakfast" in lowered
    )


def subtitle_from_line(line: str) -> str | None:
    lowered = line.lower()
    if "coffee/tea" in lowered or "coffee / tea" in lowered:
        match = re.search(r"\(([^)]+)\)", line)
        if match:
            return f"All-day coffee and tea ({match.group(1)})"
        return "All-day coffee and tea"
    if "breakfast" in lowered:
        match = re.search(r"(\d+\s*am-\d+\s*am)", line, re.I)
        if match:
            return f"Light breakfast ({match.group(1)})"
        return "Light breakfast"
    return None


def clean_title(title: str) -> str:
    title = normalize_whitespace(title)
    if title.lower().startswith("keynote speaker -"):
        name = fix_name(title.split("-", 1)[1])
        return f"Keynote: {name}"
    replacements = {
        "Lunch Break": "Lunch",
        "RLC Light Reception": "Light reception",
        "Opening Comments": "Opening comments",
        "Poster Session": "Poster session",
        "Orals": "Presentation schedule",
    }
    for old, new in replacements.items():
        if title.lower() == old.lower():
            return new
    if title.lower().startswith("poster session"):
        return "Poster session"
    return title


def should_skip_friday_block(lines: list[str]) -> bool:
    joined = " ".join(lines).lower()
    if "registration desk" in joined and "setup" in joined:
        return True
    if any(SKIP_FRIDAY_RE.match(normalize_whitespace(line)) for line in lines):
        if not any("early check-in" in line.lower() for line in lines):
            return True
    return False


def parse_block(day_id: str, lines: list[str]) -> list[ScheduleEvent]:
    if day_id == "friday" and should_skip_friday_block(lines):
        return []

    events: list[ScheduleEvent] = []
    current: ScheduleEvent | None = None

    def finalize_current() -> None:
        nonlocal current
        if current is None:
            return
        current.title = clean_title(current.title)
        if current.kind == "event" and current.title.lower().startswith("keynote:"):
            current.bold = True
        if current.kind == "event" and current.title.lower() == "poster session":
            current.bold = True
        events.append(current)
        current = None

    for raw_line in lines:
        line = normalize_whitespace(raw_line)
        if not line:
            continue

        if BREAK_RE.match(line):
            finalize_current()
            duration = BREAK_RE.match(line).group(1)
            current = ScheduleEvent(kind="break", title=f"{duration} min break")
            continue

        if DETAIL_RE.match(line):
            detail = normalize_whitespace(line)
            if current is not None:
                current.details.append(detail)
            elif events:
                events[-1].details.append(detail)
            continue

        if line.startswith("(") and line.endswith(")"):
            inner = line[1:-1]
            if looks_like_time_range(inner):
                time_display = parse_time_range(inner)
                if current is None:
                    if events and not events[-1].time_display:
                        events[-1].time_display = time_display
                    continue
                if current.kind == "break":
                    current.time_display = time_display
                    finalize_current()
                else:
                    current.time_display = time_display
                    finalize_current()
                continue

        workshop_time_match = WORKSHOP_TIME_RE.match(line)
        if workshop_time_match:
            time_display = parse_time_range(workshop_time_match.group(1))
            if current is not None and "workshop" in current.title.lower():
                current.time_display = time_display
                current.title = "Workshops"
                continue
            finalize_current()
            current = ScheduleEvent(
                kind="event",
                title="Workshops",
                time_display=time_display,
            )
            continue

        lunch_match = re.match(
            r"^Lunch Break\s*\(([^)]+)\)\s*(Provided by RLC)?$",
            line,
            re.I,
        )
        if lunch_match:
            finalize_current()
            details = []
            if lunch_match.group(2):
                details.append("Provided by RLC")
            current = ScheduleEvent(
                kind="event",
                title="Lunch",
                time_display=parse_time_range(lunch_match.group(1)),
                details=details,
            )
            finalize_current()
            continue

        title, inline_time = extract_inline_time(line)
        keynote_match = KEYNOTE_RE.match(title)
        if keynote_match:
            title = f"Keynote: {fix_name(keynote_match.group(1))}"

        if re.fullmatch(r"\d+\s+Workshops?", title, re.I):
            if current is not None and "workshop" in current.title.lower():
                continue
            finalize_current()
            current = ScheduleEvent(kind="event", title="Workshops")
            continue

        poster_match = re.match(r"^Poster Session\s*\((.+)\)$", title, re.I)
        if poster_match:
            finalize_current()
            current = ScheduleEvent(
                kind="event",
                title="Poster session",
                details=[normalize_whitespace(poster_match.group(1))],
                bold=True,
            )
            continue

        if inline_time:
            finalize_current()
            poster_count_match = re.search(r"\((\d+\s+posters?[^)]*)\)", line, re.I)
            details: list[str] = []
            if poster_count_match:
                details.append(normalize_whitespace(poster_count_match.group(1)))
            current = ScheduleEvent(
                kind="event",
                title=clean_title(title),
                time_display=inline_time,
                details=details,
                bold=title.lower().startswith("keynote:"),
            )
            finalize_current()
            continue

        if current is not None and current.kind == "break" and not current.time_display:
            # Time-only line after break label without parentheses handled above.
            maybe_time = parse_time_range(line.strip("()"))
            if maybe_time:
                current.time_display = maybe_time
                finalize_current()
                continue

        if current is not None and current.title and not current.time_display:
            # Continuation line (e.g., keynote name then time on next row).
            if title.startswith("("):
                current.time_display = parse_time_range(title.strip("()"))
                finalize_current()
                continue

        finalize_current()
        current = ScheduleEvent(kind="event", title=title)

    finalize_current()
    return events


def merge_registration_block(events: list[ScheduleEvent]) -> list[ScheduleEvent]:
    merged: list[ScheduleEvent] = []
    idx = 0
    while idx < len(events):
        event = events[idx]
        if (
            event.title.lower() == "registration"
            and idx + 1 < len(events)
            and events[idx + 1].title.lower() == "early check-in"
        ):
            time_display = events[idx + 1].time_display or event.time_display
            merged.append(
                ScheduleEvent(
                    kind="event",
                    title="Registration / Early Check-In",
                    time_display=time_display,
                )
            )
            idx += 2
            continue
        merged.append(event)
        idx += 1
    return merged


def normalize_detail(detail: str) -> str:
    return re.sub(r"\s*\(including journal-to-conference track\)", "", detail, flags=re.I).strip()


def apply_locations(day_id: str, items: list[ScheduleEvent]) -> None:
    for item in items:
        if item.kind != "event":
            continue
        item.location = EVENT_LOCATIONS.get((day_id, item.title), "")
        item.details = [normalize_detail(detail) for detail in item.details]
        if item.title == "Presentation schedule":
            item.details = [PARALLEL_TRACKS_DETAIL]
        if item.title == "Townhall":
            item.details = [detail for detail in item.details if detail != "Salle Claude-Champagne"]


def parse_time_only_block(lines: list[str]) -> str | None:
    if len(lines) != 1:
        return None
    line = normalize_whitespace(lines[0])
    if line.startswith("(") and line.endswith(")"):
        inner = line[1:-1]
        if looks_like_time_range(inner):
            return parse_time_range(inner)
    return None


def parse_day_column(day_id: str, column_values: list[str | None]) -> DaySchedule:
    schedule = DaySchedule()
    blocks: list[list[str]] = []
    current_block: list[str] = []

    for value in column_values:
        if value and normalize_whitespace(value):
            current_block.append(normalize_whitespace(value))
        elif current_block:
            blocks.append(current_block)
            current_block = []
    if current_block:
        blocks.append(current_block)

    for block in blocks:
        if all(is_subtitle_line(line) for line in block):
            for line in block:
                subtitle = subtitle_from_line(line)
                if subtitle:
                    schedule.subtitle_parts.append(subtitle)
            continue

        subtitle_lines = [line for line in block if is_subtitle_line(line)]
        content_lines = [line for line in block if not is_subtitle_line(line)]

        for line in subtitle_lines:
            subtitle = subtitle_from_line(line)
            if subtitle:
                schedule.subtitle_parts.append(subtitle)

        if not content_lines:
            continue

        orphan_time = parse_time_only_block(content_lines)
        if orphan_time and schedule.items:
            schedule.items[-1].time_display = orphan_time
            continue

        schedule.items.extend(parse_block(day_id, content_lines))

    if day_id == "friday":
        schedule.items = merge_registration_block(schedule.items)

    if day_id == "saturday":
        schedule.subtitle_parts.append("Lunch provided")

    for day in ("sunday", "monday", "tuesday"):
        if day_id == day and "Lunch provided" not in schedule.subtitle_parts:
            schedule.subtitle_parts.append("Lunch provided")

    apply_locations(day_id, schedule.items)

    return schedule


def load_csv(path: Path) -> dict[str, DaySchedule]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))

    schedules: dict[str, DaySchedule] = {}
    for day in DAYS:
        col = day["col"]
        column_values = [
            row[col].strip() if col < len(row) and row[col].strip() else None
            for row in rows[3:]
        ]
        schedules[day["id"]] = parse_day_column(day["id"], column_values)
    return schedules


def render_subtitle(parts: list[str]) -> str:
    deduped: list[str] = []
    for part in parts:
        if part not in deduped:
            deduped.append(part)
    return " · ".join(html.escape(part) for part in deduped)


def render_location_html(location: str) -> str:
    if not location:
        return ""
    return (
        f'                                <div class="md:p-2 md:m-2 p-1 m-1 italic md:text-right">'
        f"📍 {html.escape(location)}</div>\n"
    )


def render_event_card(event: ScheduleEvent) -> str:
    if event.kind == "break":
        return (
            f'                        <h3 class="text-base sm:text-xl mb-3 text-blue '
            f'text-center mx-auto m-4 p-4">{html.escape(event.title)}</h3>\n'
        )

    title_class = "font-semibold" if event.bold else ""
    title_html = html.escape(event.title)
    if title_class:
        title_html = f'<div class="{title_class}">{title_html}</div>'

    details_html = ""
    for detail in event.details:
        details_html += (
            f'\n                                    <div class="text-sm text-gray-600 mt-1">'
            f"{html.escape(detail)}</div>"
        )

    workshops_html = ""
    if "workshop" in event.title.lower() and event.time_display:
        workshop_items = []
        for name, url, room in WORKSHOPS:
            workshop_items.append(
                '                                <div class="grid md:grid-cols-2 grid-cols-1 items-center">\n'
                '                                    <div class="md:p-2 md:m-2 p-1 m-1 text-left">\n'
                f'                                        <a href="{html.escape(url)}" '
                'class="text-blue hover:text-rldarkblue-500 underline" '
                f'target="_blank" rel="noopener noreferrer">{html.escape(name)}</a>\n'
                "                                    </div>\n"
                f'                                    <div class="md:p-2 md:m-2 p-1 m-1 italic md:text-right">'
                f"📍 {html.escape(room)}</div>\n"
                "                                </div>"
            )
        workshops_html = (
            '\n                            <div class="text-center mb-4 font-medium">'
            "Workshops</div>\n"
            '                            <div class="space-y-3">\n'
            + "\n".join(workshop_items)
            + "\n                            </div>"
        )
        title_html = ""

    time_heading = ""
    if event.time_display:
        time_heading = (
            f'                            <h3 class="text-base sm:text-xl font-medium mb-3 text-rldarkblue-900 text-center mx-auto">'
            f"{html.escape(event.time_display)}</h3>\n"
        )

    body_html = title_html + details_html
    if workshops_html:
        return (
            '                        <div class="bg-rldarkblue-50/50 rounded-lg p-4 border-blue m-2">\n'
            f"{time_heading}"
            f"{workshops_html}\n"
            "                        </div>\n"
        )

    if body_html.strip():
        body_section = (
            '                            <div class="grid md:grid-cols-2 grid-cols-1 items-center">\n'
            f'                                <div class="md:p-2 md:m-2 p-1 m-1 text-left">{body_html}\n'
            "                                </div>\n"
            f"{render_location_html(event.location)}"
            "                            </div>\n"
        )
    else:
        body_section = ""

    return (
        '                        <div class="bg-rldarkblue-50/50 rounded-lg p-4 border-blue m-2">\n'
        f"{time_heading}"
        f"{body_section}"
        "                        </div>\n"
    )


def render_day(day: dict[str, str], schedule: DaySchedule) -> str:
    subtitle = render_subtitle(schedule.subtitle_parts)
    subtitle_html = (
        f'                        <div class="text-sm font-roboto italic text-center mb-10">{subtitle}</div>\n'
        if subtitle
        else ""
    )

    items_html = "".join(render_event_card(item) for item in schedule.items)

    comment = day["title"].split(",")[0]
    return (
        f"\n                <!-- {comment} -->\n"
        f'                <div id="day-{day["id"]}" class="day-content mb-16">\n'
        '                    <div class="rounded-lg p-1 md:p-6">\n'
        f'                        <h2 class="text-base sm:text-2xl font-roboto text-blue font-semibold text-center mb-2">'
        f'{html.escape(day["title"])}</h2>\n'
        f"{subtitle_html}"
        f"{items_html}"
        "                    </div>\n"
        "                </div>\n"
    )


def render_nav_buttons() -> str:
    lines = [
        '            <div class="sticky top-0 z-20 bg-white/95 backdrop-blur-md flex flex-wrap justify-center gap-2 sm:gap-4 mb-8 p-4">'
    ]
    for day in DAYS:
        lines.append(
            f'                <button onclick="scrollToDay(\'{day["id"]}\')" id="btn-{day["id"]}"\n'
            f'                        class="{BUTTON_CLASSES}">\n'
            f'                    {html.escape(day["label"])}\n'
            "                </button>"
        )
    lines.append("            </div>")
    return "\n".join(lines) + "\n"


def render_schedule_script() -> str:
    valid_days = ", ".join(f"'{day['id']}'" for day in DAYS)
    return f"""<script>
    function highlightDayButton(dayId) {{
        const buttons = document.querySelectorAll('.day-btn');
        buttons.forEach(btn => {{
            btn.classList.remove('bg-blue', 'text-white');
            btn.classList.add('bg-rldarkblue-200', 'text-rldarkblue-900');
        }});

        const selectedButton = document.getElementById('btn-' + dayId);
        if (selectedButton) {{
            selectedButton.classList.remove('bg-rldarkblue-200', 'text-rldarkblue-900');
            selectedButton.classList.add('bg-blue', 'text-white');
        }}
    }}

    function scrollToDay(dayId) {{
        const section = document.getElementById('day-' + dayId);
        if (section) {{
            section.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
        highlightDayButton(dayId);
        window.history.replaceState(null, null, '#' + dayId);
    }}

    const validDays = [{valid_days}];

    document.addEventListener('DOMContentLoaded', function () {{
        const hash = window.location.hash.substring(1);
        if (hash && validDays.includes(hash)) {{
            highlightDayButton(hash);
            const section = document.getElementById('day-' + hash);
            if (section) {{
                section.scrollIntoView({{ block: 'start' }});
            }}
        }}
    }});

    window.addEventListener('hashchange', function () {{
        const hash = window.location.hash.substring(1);
        if (hash && validDays.includes(hash)) {{
            scrollToDay(hash);
        }}
    }});
</script>"""


def render_schedule_content(schedules: dict[str, DaySchedule]) -> str:
    body = '            <div class="p-1 sm:p-2 text-sm sm:text-base max-w-5xl mx-auto">\n'
    for day in DAYS:
        body += render_day(day, schedules[day["id"]])
    body += "\n            </div>\n"
    return body


def update_html(html_path: Path, schedules: dict[str, DaySchedule]) -> None:
    content = html_path.read_text(encoding="utf-8")

    nav_pattern = re.compile(
        r"(<!-- DAY NAVIGATION BUTTONS -->\n).*?(<!-- SCHEDULE CONTENT -->)",
        re.DOTALL,
    )
    content, count = nav_pattern.subn(
        r"\1" + render_nav_buttons() + r"\n            \2",
        content,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not locate day navigation section in schedule.html")

    schedule_pattern = re.compile(
        r"(<!-- SCHEDULE CONTENT -->\n).*?(\n        </div>\n\n        <div class=\"grid grid-cols-4 items-center\">)",
        re.DOTALL,
    )
    content, count = schedule_pattern.subn(
        r"\1" + render_schedule_content(schedules) + r"\2",
        content,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not locate schedule content section in schedule.html")

    script_pattern = re.compile(
        r"<script>\s*function highlightDayButton\(dayId\).*?</script>",
        re.DOTALL,
    )
    content, count = script_pattern.subn(render_schedule_script(), content, count=1)
    if count != 1:
        raise RuntimeError("Could not locate schedule navigation script in schedule.html")

    html_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to schedule CSV")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML, help="Path to schedule.html")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1
    if not args.html.exists():
        print(f"HTML not found: {args.html}", file=sys.stderr)
        return 1

    schedules = load_csv(args.csv)
    update_html(args.html, schedules)
    print(f"Updated {args.html} from {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
