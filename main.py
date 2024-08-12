# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import json
import os
import pathlib
from collections import defaultdict
from datetime import datetime

import frontmatter
import markdown2
import yaml
from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    render_template,
    send_from_directory,
)
from flask_frozen import Freezer
from flaskext.markdown import Markdown
from zoneinfo import ZoneInfo

site_data = {}
by_uid = {}


def assign_session_id(start_time, end_time):
    # Create a unique identifier based on start and end times
    return f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')}"


def format_time_range(start_time, end_time):
    """
    Format a time range in the "8:30 AM - 9:30 AM" format.

    :param start_time: A datetime object representing the start time
    :param end_time: A datetime object representing the end time
    :return: A formatted string representing the time range
    """
    start_str = start_time.strftime("%I:%M %p").lstrip("0")
    end_str = end_time.strftime("%I:%M %p").lstrip("0")
    return f"{start_str} - {end_str}"


def events_by_day(data):
    def extract_date(date_string):
        return datetime.fromisoformat(date_string).date()

    def format_eastern_time(utc_time_str):
        utc_time = datetime.fromisoformat(utc_time_str)
        eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
        return eastern_time.strftime("%H%M")

    def convert_eastern_time(utc_time_str):
        utc_time = datetime.fromisoformat(utc_time_str)
        return utc_time.astimezone(ZoneInfo("America/New_York"))

    # Group events by day
    events_by_day = defaultdict(list)
    session_ids = defaultdict(lambda: defaultdict(lambda: 0))
    ids_by_date = defaultdict(lambda: 0)

    for event in data:
        event_date = extract_date(event["start"])
        formatted_start = format_eastern_time(event["start"])
        formatted_end = format_eastern_time(event["end"])
        event["formatted_time"] = f"time-{formatted_start} / time-{formatted_end}"
        event["time_range"] = format_time_range(
            convert_eastern_time(event["start"]), convert_eastern_time(event["end"])
        )
        session_id = assign_session_id(
            convert_eastern_time(event["start"]), convert_eastern_time(event["end"])
        )
        if session_id in session_ids[event_date]:
            event["session_id"] = f"{session_ids[event_date][session_id]}"
        else:
            ids_by_date[event_date] += 1
            session_ids[event_date][session_id] = ids_by_date[event_date]
            event["session_id"] = f"{session_ids[event_date][session_id]}"

        events_by_day[event_date].append(event)

    # Sort events within each day by start time
    for day, events in events_by_day.items():
        events_by_day[day] = sorted(events, key=lambda x: x["start"])

    print(events_by_day)

    return events_by_day


def main(site_data_path):
    global site_data, extra_files
    site_data_path = pathlib.Path(site_data_path)
    extra_files = [
        "README.md",
        "acknowledgements.md",
        "call_for_papers.md",
        "call_for_workshops.md",
        "review_process.md",
        "review_guidelines.md",
        "accepted_workshops.md",
        "code_of_conduct.md",
        "travel_info.md",
        "hotels.md",
    ]
    site_data["blogs"] = []
    for f in site_data_path.parent.glob("blogs/*.md"):
        post = frontmatter.load(f.as_posix())
        site_data["blogs"].append(
            {
                "title": post.metadata.get("title", "No Title"),
                "file_path": "/blogs/{0}".format(f.with_suffix(".html").name),
                "content": markdown2.markdown(post.content),
            }
        )
    # print(site_data["blogs"])
    # Load all for your sitedata one time.
    for f in site_data_path.glob("*"):
        extra_files.append(f.as_posix())

        if f.suffix == ".json":
            site_data[f.stem] = json.loads(f.read_text())
        elif f.suffix in {".csv", ".tsv"}:
            with f.open() as fp:
                site_data[f.stem] = list(csv.DictReader(fp))
        elif f.suffix == ".yml":
            site_data[f.stem] = yaml.load(f.read_text(), Loader=yaml.SafeLoader)

    for typ in ["papers", "speakers", "workshops"]:
        by_uid[typ] = {}
        for p in site_data[typ]:
            by_uid[typ][p["UID"]] = p

    print("Data Successfully Loaded")
    return extra_files


# ------------- SERVER CODE -------------------->

app = Flask(__name__)
app.config.from_object(__name__)
freezer = Freezer(app)
markdown = Markdown(app)


# MAIN PAGES


def _data():
    data = {}
    data["config"] = site_data["config"]
    return data


@app.route("/")
def index():
    return redirect("/index.html")


# TOP LEVEL PAGES


@app.route("/index.html")
def home():
    data = _data()
    data["readme"] = open("README.md").read()
    for key in site_data["committee"]:
        data[key] = site_data["committee"][key]
    for key in site_data["sponsors"]:
        data[key] = site_data["sponsors"][key]
    data["keynotes"] = site_data["keynotes"]["keynotes"]
    data["acknowledgements"] = open("acknowledgements.md").read()
    return render_template("index.html", **data)


@app.route("/sponsorship.html")
def sponsorship():
    data = _data()
    for key in site_data["sponsors"]:
        data[key] = site_data["sponsors"][key]
    return render_template("sponsorship.html", **data)

@app.route("/panels.html")
def panels():
    data = _data()
    for key in site_data["panelists"]:
        data[key] = site_data["panelists"][key]
    return render_template("panels.html", **data)


@app.route("/help.html")
def about():
    data = _data()
    data["FAQ"] = site_data["faq"]["FAQ"]
    return render_template("help.html", **data)


@app.route("/call_for_papers.html")
def call_for_papers():
    data = _data()
    data["call_for_papers"] = open("call_for_papers.md").read()
    return render_template("call_for_papers.html", **data)


@app.route("/code_of_conduct.html")
def code_of_conduct():
    data = _data()
    data["code_of_conduct"] = open("code_of_conduct.md").read()
    return render_template("code_of_conduct.html", **data)


@app.route("/travel_info.html")
def travel_info():
    data = _data()
    data["travel_info"] = open("travel_info.md").read()
    return render_template("travel_info.html", **data)


@app.route("/hotels.html")
def hotels():
    data = _data()
    data["hotels"] = open("hotels.md").read()
    return render_template("hotels.html", **data)


@app.route("/call_for_workshops.html")
def call_for_workshops():
    data = _data()
    data["call_for_workshops"] = open("call_for_workshops.md").read()
    return render_template("call_for_workshops.html", **data)


@app.route("/review_process.html")
def review_process():
    data = _data()
    data["review_process"] = open("review_process.md").read()
    return render_template("review_process.html", **data)


@app.route("/review_guidelines.html")
def review_guidelines():
    data = _data()
    data["review_guidelines"] = open("review_guidelines.md").read()
    return render_template("review_guidelines.html", **data)


@app.route("/papers.html")
def papers():
    data = _data()
    # data["papers"] = site_data["papers"]
    return render_template("papers.html", **data)


@app.route("/accepted_journal_papers.html")
def accepted_journal_papers():
    data = _data()
    # data["papers"] = site_data["papers"]
    return render_template("accepted_journal_papers.html", **data)


@app.route("/accepted_workshops.html")
def accepted_workshops():
    data = _data()
    data["accepted_workshops"] = open("accepted_workshops.md").read()
    return render_template("accepted_workshops.html", **data)


@app.route("/blogs.html")
def blogs():
    data = _data()
    data["blogs"] = site_data["blogs"]
    return render_template("blogs.html", **data)


@app.route("/<path:file_path>")
def blog_post(file_path):
    file_path = pathlib.Path(file_path)
    # Read and convert the markdown file
    with file_path.with_suffix(".md").open("r") as f:
        post = frontmatter.load(f)
        html_content = markdown2.markdown(post.content)

    # Pass the HTML content to the template
    data = _data()
    rendered_content = render_template("blog_post.html", content=html_content, **data)

    # Return the response with the correct content type
    return Response(rendered_content, mimetype="text/html")


@app.route("/paper_vis.html")
def paper_vis():
    data = _data()
    return render_template("papers_vis.html", **data)


@app.route("/calendar.html")
def schedule():
    data = _data()
    data["day"] = {
        "speakers": site_data["speakers"],
        # "highlighted": [
        #     format_paper(by_uid["papers"][h["UID"]]) for h in site_data["highlighted"]
        # ],
    }
    jsons = (pathlib.Path.cwd() / "sitedata/main_calendar.json").read_text()
    data["calendar"] = json.loads(jsons)
    data["events_by_day"] = events_by_day(data["calendar"])
    return render_template("schedule2.html", **data)


@app.route("/workshops.html")
def workshops():
    data = _data()
    data["workshops"] = [
        format_workshop(workshop) for workshop in site_data["workshops"]
    ]
    return render_template("workshops.html", **data)


def extract_list_field(v, key):
    value = v.get(key, "")
    if isinstance(value, list):
        return value
    else:
        return value.split("|")


def format_paper(v):
    list_keys = ["authors", "keywords", "sessions"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "UID": v["UID"],
        "title": v["title"],
        "forum": v["UID"],
        "authors": list_fields["authors"],
        "keywords": list_fields["keywords"],
        "abstract": v["abstract"],
        "TLDR": v["abstract"],
        "recs": [],
        "sessions": list_fields["sessions"],
        # links to external content per poster
        "pdf_url": v.get("pdf_url", ""),  # render poster from this PDF
        "code_link": "https://github.com/Mini-Conf/Mini-Conf",  # link to code
        "link": "https://arxiv.org/abs/2007.12238",  # link to paper
    }


def format_workshop(v):
    list_keys = ["authors"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["UID"],
        "title": v["title"],
        "organizers": list_fields["authors"],
        "abstract": v["abstract"],
    }


# ITEM PAGES


@app.route("/poster_<poster>.html")
def poster(poster):
    uid = poster
    v = by_uid["papers"][uid]
    data = _data()
    data["paper"] = format_paper(v)
    return render_template("poster.html", **data)


@app.route("/speaker_<speaker>.html")
def speaker(speaker):
    uid = speaker
    v = by_uid["speakers"][uid]
    data = _data()
    data["speaker"] = v
    return render_template("speaker.html", **data)


@app.route("/workshop_<workshop>.html")
def workshop(workshop):
    uid = workshop
    v = by_uid["workshops"][uid]
    data = _data()
    data["workshop"] = format_workshop(v)
    return render_template("workshop.html", **data)


@app.route("/organizers.html")
def organizers():
    data = _data()
    for key in site_data["committee"]:
        data[key] = site_data["committee"][key]
    data["keynotes"] = site_data["keynotes"]["keynotes"]
    data["acknowledgements"] = open("acknowledgements.md").read()
    return render_template("organizers.html", **data)


@app.route("/chat.html")
def chat():
    data = _data()
    return render_template("chat.html", **data)


# FRONT END SERVING


@app.route("/papers.json")
def paper_json():
    json = []
    for v in site_data["papers"]:
        json.append(format_paper(v))
    return jsonify(json)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/serve_<path>.json")
def serve(path):
    return jsonify(site_data[path])


# --------------- DRIVER CODE -------------------------->
# Code to turn it all static


@freezer.register_generator
def generator():
    # TODO(ev) put this back once we have papers
    # for paper in site_data["papers"]:
    #     yield "poster", {"poster": str(paper["UID"])}
    # for speaker in site_data["speakers"]:
    #     yield "speaker", {"speaker": str(speaker["UID"])}
    # for workshop in site_data["workshops"]:
    #     yield "workshop", {"workshop": str(workshop["UID"])}

    for blog in site_data["blogs"]:
        yield "blog_post", {"file_path": blog["file_path"]}

    for key in site_data:
        print(key)
        yield "serve", {"path": key}


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")

    parser.add_argument(
        "--build",
        action="store_true",
        default=False,
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        default=False,
        dest="build",
        help="Convert the site to static assets",
    )

    parser.add_argument("path", help="Pass the JSON data path and run the server")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    site_data_path = args.path
    extra_files = main(site_data_path)

    if args.build:
        freezer.freeze()
    else:
        debug_val = False
        if os.getenv("FLASK_DEBUG") == "True":
            debug_val = True

        app.run(port=5000, debug=debug_val, extra_files=extra_files)
