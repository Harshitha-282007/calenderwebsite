# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import defaultdict
import time

# === Setup Chrome Driver ===
# Configure Chrome to run in the background (headless mode)
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Set the path to your ChromeDriver
chrome_driver_path = r"C:\Users\Nikhil\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Start the Chrome browser using Selenium
driver = webdriver.Chrome(service=service, options=chrome_options)

# === Open MLH 2025 Events Page ===
driver.get("https://mlh.io/seasons/2025/events")
time.sleep(5)  # Wait for the page to fully load

# Get the HTML content of the page
html = driver.page_source
driver.quit()  # Close the browser

# === Parse the HTML using BeautifulSoup ===
soup = BeautifulSoup(html, "html.parser")

# Dictionary to group events by their start date
grouped_events = defaultdict(list)

# Loop through each event on the page
for event in soup.find_all("div", class_="event-wrapper"):
    # Get the event details
    title = event.find("h3", class_="event-name").text.strip()
    date = event.find("p", class_="event-date").text.strip()
    location = event.find("div", class_="event-location").text.strip()
    link_tag = event.find("a", href=True)
    link = link_tag["href"] if link_tag else "#"

    # Only take the start date part (e.g., "Apr 12" from "Apr 12 – Apr 14")
    start_date = date.split("–")[0].strip()

    # Create a small HTML card for this event
    card = f"""
        <a class="card" href="{link}" target="_blank">
            <div class="cd"><h2>{title}</h2></div>
            <div class="cd"><strong>Location:</strong> {location}</div>
        </a>
        <div class="space"></div>
    """

    # Group the card under its start date
    grouped_events[start_date].append(card)

# === Create the final HTML content to insert ===
final_html = ""
for date in sorted(grouped_events.keys()):
    final_html += f"<h2 class='date-header'>{date}</h2>\n"
    final_html += "\n".join(grouped_events[date])

# === Inject the HTML into your existing template ===
# Make sure your HTML file has <!-- PLACEHOLDER --> where events should go

template_path = r"hackathon_calender.html"
output_path = r"a_hackathon_calender.html"

with open(template_path, "r", encoding="utf-8") as f:
    html_file = f.read()

if "<!-- PLACEHOLDER -->" not in html_file:
    print("⚠️ Could not find <!-- PLACEHOLDER --> in the template file.")
else:
    updated_html = html_file.replace("<!-- PLACEHOLDER -->", final_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

