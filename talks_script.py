from collections import defaultdict
import pandas as pd
import requests
from io import StringIO
from pathlib import Path

# Configuration
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/10vIj9H787kYQLOmYnfSsFsqHMpBYKA-59kmwNhitP9I/export?format=csv&gid=584174710"

print("Reading data from Google Sheet A15:P27...")

# Read the full sheet
df = pd.read_csv(GOOGLE_SHEET_URL, header=None)

# Extract only A15:P27 (rows 14-26, columns 0-15 in 0-based indexing)
data_range = df.iloc[14:27, 0:16]  # A15:P27

print(f"Data shape: {data_range.shape}")
print("\nRaw data from A15:P27:")
print(data_range.to_string())

# Convert to list of lists for easier processing
raw_data = data_range.values.tolist()

# First row (A15:P15) should be headers
headers = [str(cell).strip() if pd.notna(cell) else f"Col_{i}" for i, cell in enumerate(raw_data[0])]
print(f"\nHeaders: {headers}")

# Process the remaining rows (A16:P27)
talks_by_date = defaultdict(list)

for row_data in raw_data[1:]:  # Skip header row
    if len(row_data) == 0:
        continue
    
    # Convert row to strings, handling NaN values
    row = [str(cell).strip() if pd.notna(cell) and str(cell).strip() else "" for cell in row_data]
    
    # Skip empty rows
    if not any(row):
        continue
    
    print(f"\nProcessing row: {row[:5]}...")  # Show first 5 columns
    
    # Create row dictionary using headers
    row_dict = {}
    for i, header in enumerate(headers):
        if i < len(row):
            row_dict[header] = row[i]
        else:
            row_dict[header] = ""
    
    # Extract date, track, theme
    date = row_dict.get(headers[0], "").strip()  # First column is date
    track = row_dict.get(headers[2], "").strip() if len(headers) > 2 else ""  # Third column is track number (not day of week)
    
    # Look for theme in the available columns
    theme = ""
    for header, value in row_dict.items():
        if "theme" in header.lower() and value:
            theme = value
            break
    
    # Extract talks from remaining columns
    talks = []
    for header, value in row_dict.items():
        if ("talk" in header.lower() and 
            value.strip() and 
            "number" not in header.lower() and  # Skip "Number of talk slots in session"
            "slot" not in header.lower()):      # Extra safety check
            talks.append(value.strip())
    
    # Only add if we have date and talks
    if date and talks:
        talks_by_date[date].append({
            "track": track,
            "theme": theme,
            "talks": talks
        })
        print(f"Added: Date={date}, Track={track}, Theme={theme}, Talks={len(talks)}")

print(f"\nFound data for {len(talks_by_date)} dates")

# Generate HTML
html_part = '''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>RLC 2025 - Schedule</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap"
    rel="stylesheet">
  <link
    href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@200..700&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap"
    rel="stylesheet">
  <link href="build.css" rel="stylesheet">
  <link rel="icon" type="image/png" href="/favicon-48x48.png" sizes="48x48" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <meta name="apple-mobile-web-app-title" content="RLC" />
  <link rel="manifest" href="/site.webmanifest" />
</head>

<body class="bg-rlgrey font-rubik text-rldarkblue-900 p-6">
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

  <!-- Include Menu -->
  <script src="jquery.js"></script>
  <script src="data.js"></script>

  <div class="container mx-auto">
    <div class="flex flex-col min-h-screen justify-between">
      <div>
        <div class="m-2 grid grid-cols-3 items-center rounded-md mt-4 p-2 border-0 border-rldarkblue-900">
          <div class="p-2 w-full rounded-md">
            <div class="hidden lg:block max-w-60">
              <a href="index.html"><img alt="Company logo" src="data/logos/rlc-logo.svg" /></a>
            </div>
            <div class="block pt-1 lg:hidden max-w-60">
              <a href="index.html"><img alt="Company logo" src="data/logos/rlc-logo.svg" /></a>
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
                  d="M3.75 5.25h16.5m-16.5 4.5h16.5m-16.5 4.5h16.5m-16.5 4.5h16.5" />
              </svg>
              <div id="collapsedMenuItems"
                class="absolute top-10 z-10 hidden w-40 shadow-md bg-rlgrey/100 backdrop-blur-md rounded-md p-4 m-4 grid grid-cols-1 border border-black">
              </div>
            </div>
          </div>
        </div>

        <!-- PAGE TITLE -->
        <h1 class="text-4xl  font-bai text-center text-blue mb-10 mt-10">RLC 2025 Schedule: August 5–9</h1>
        
        <!-- EXPORT CONTROLS -->
        <div class="mb-6 text-center">
          <button id="exportCalendar" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
            Export Selected to Calendar
          </button>
          <button id="selectAll" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded mr-2">
            Select All
          </button>
          <button id="deselectAll" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">
            Deselect All
          </button>
          <div id="selectedCount" class="mt-2 text-gray-600">0 events selected</div>
        </div>

        <!-- SCHEDULE -->
        <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          <div class="bg-rllightblue-50 shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-3 text-blue">Tuesday, August 5</h2>
            <div class="grid grid-cols-3">
              <div class="mb-2 p-1">8:30 AM - 5 PM</div>
              <div class="mb-2 col-span-2 p-1">Coffee and drinks</div>
            </div>
                         <div class="grid grid-cols-12 items-center">
               <div class="col-span-1">
                 <input type="checkbox" class="calendar-event" 
                        data-title="Workshops (8 parallel sessions)"
                        data-start="2025-08-05T09:00:00"
                        data-end="2025-08-05T17:00:00"
                        data-location="Conference Center">
               </div>
               <div class="mb-2 p-1 col-span-3">9 AM - 5 PM</div>
               <div class="mb-2 col-span-8 p-1"> <a href="./accepted_workshops.html"
                   class="text-blue hover:text-rldarkblue-500" ">Workshops</a> (8 parallel sessions)</div>
             </div> 
                         <div class=" grid grid-cols-3">
                   <div class="mb-2 p-1">12:30 PM - 2 PM</div>
                   <div class="mb-2 col-span-2 p-1">Lunch</div>
               </div>
               <div class="grid grid-cols-3">
                 <div class="mb-2 p-1">5 PM - 6:30 PM</div>
                 <div class="mb-2 col-span-2 p-1">Reviewer Recognition</div>
               </div>
             </div>

            <!-- Wednesday -->
            <div class=" bg-rllightblue-50 shadow rounded-lg p-6">
              <h2 class="text-xl font-semibold mb-3 text-blue">Wednesday, August 6</h2>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">8:30 AM - 5 PM</div>
                <div class="mb-2 col-span-2 p-1">Coffee and drinks</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">8:45 AM - 9 AM</div>
                <div class="mb-2 col-span-2 p-1">Opening Comments</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">9 AM - 10 AM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Leslie Kaelbling</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">20-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">10:20 AM - 11:15 AM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">30-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">11:45 AM - 12:30 PM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">12:30 PM - 2 PM</div>
                <div class="mb-2 col-span-2 p-1">Lunch</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">2 PM - 3 PM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Dale Schuurmans</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">3 PM - 6 PM</div>
                <div class="mb-2 col-span-2 p-1">Poster Session</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">6 PM</div>
                <div class="mb-2 col-span-2 p-1">Banquet (Edmonton Convention Center)</div>
              </div>
            </div>

            <div class="bg-rllightblue-50 shadow rounded-lg p-6">
              <h2 class="text-xl font-semibold mb-3 text-blue">Thursday, August 7</h2>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">8:30 AM - 5 PM</div>
                <div class="mb-2 col-span-2 p-1">Coffee and drinks</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">9 AM - 10 AM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Joelle Pineau</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">20-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">10:20 AM - 11:15 AM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">30-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">11:45 AM - 12:30 PM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">12:30 PM - 2 PM</div>
                <div class="mb-2 col-span-2 p-1">Lunch</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">2 PM - 3 PM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Michael Littman</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">3 PM - 6 PM</div>
                <div class="mb-2 col-span-2 p-1">Poster Session</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">6 PM</div>
                <div class="mb-2 col-span-2 p-1">Dinner on your own</div>
              </div>
            </div>

            <!-- Friday -->
            <div class="bg-rllightblue-50 shadow rounded-lg p-6">
              <h2 class="text-xl font-semibold mb-3 text-blue">Friday, August 8</h2>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">8:30 AM - 5 PM</div>
                <div class="mb-2 col-span-2 p-1">Coffee and drinks</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">9 AM - 10 AM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Peter Dayan</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">20-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">10:20 AM - 11:15 AM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="text-center">
                <div class="m-2 p-2 font-semibold">30-minute Break</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">11:45 AM - 12:30 PM</div>
                <div class="mb-2 col-span-2 p-1">Orals (4 parallel sessions)</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">12:30 PM - 2 PM</div>
                <div class="mb-2 col-span-2 p-1">Lunch</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">2:00 PM - 3:00 PM</div>
                <div class="mb-2 col-span-2 p-1">Keynote: Richard S. Sutton</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">3 PM - 6 PM</div>
                <div class="mb-2 col-span-2 p-1">Poster Session</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">6 PM</div>
                <div class="mb-2 col-span-2 p-1">Dinner on your own</div>
              </div>
            </div>

            <div class="bg-rllightblue-50 shadow rounded-lg p-6">
              <h2 class="text-xl font-semibold mb-3 text-blue">Saturday, August 9</h2>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">9 AM - 10 AM</div>
                <div class="mb-2 col-span-2 p-1">Breakfast & Meet-ups</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">10 AM - 11 AM</div>
                <div class="mb-2 col-span-2 p-1">Town Hall</div>
              </div>
              <div class="grid grid-cols-3">
                <div class="mb-2 p-1">11 AM - 1 PM</div>
                <div class="mb-2 col-span-2 p-1">Socials, Meet-ups, Excursions</div>
              </div>
            </div>
          </div>
          <h1 class='text-4xl font-bai text-center text-blue mt-20 p-2 m-2'>Oral Talks</h1>
          <div id="oral_talks">
          
          </div>
        </div>
      </div>

      <!-- Load menu functionality -->
      <script src="menu.js"></script>
</body>

</html>'''


# Generate oral talks content
oral_talks_parts = []

for date in sorted(talks_by_date.keys()):
    oral_talks_parts.append(f"<h2 class='text-3xl font-bai text-center text-blue m-4 p-4'>{date}</h2>")
    oral_talks_parts.append("<div class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4'>")
    
    for session in talks_by_date[date]:
        oral_talks_parts.append("<div class='bg-rllightblue-50 shadow rounded-lg p-6'>")
        track_text = f"Track {session['track']}" if session['track'] else "Track"
        theme_text = f": {session['theme']}" if session['theme'] else ""
        oral_talks_parts.append(f"<h3 class='text-xl font-semibold mb-3 text-blue m-2 p-2'>{track_text}{theme_text}</h3>")
        oral_talks_parts.append("<ol class='list-decimal p-2 m-2'>")
        for talk in session['talks']:
            oral_talks_parts.append(f"<li class='p-1'>{talk}</li>")
        oral_talks_parts.append("</ol></div>")
    
    oral_talks_parts.append("</div>")

# Insert the oral talks content into the HTML template
oral_talks_content = "\n".join(oral_talks_parts)
final_html = html_part.replace('<div id="oral_talks">', f'<div id="oral_talks">\n{oral_talks_content}')

# Write HTML
Path("schedule.html").write_text(final_html, encoding="utf-8")
print(f"\nHTML file generated: schedule.html")