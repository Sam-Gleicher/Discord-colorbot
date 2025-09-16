import csv
import datetime
import zoneinfo
import requests
# define a "get_weather" function 
def get_weather(lat, lon, date):
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={date}&end_date={date}"
        f"&hourly=temperature_2m,cloudcover"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return "", ""
    data = response.json()
    try:
        temps = data['hourly']['temperature_2m']
        clouds = data['hourly']['cloudcover']
        if temps and clouds:
            avg_temp = round(sum(temps) / len(temps), 1)
            avg_cloud = round(sum(clouds) / len(clouds), 1)
            return avg_temp, avg_cloud
        else:
            return "", ""
    except Exception:
        return "", ""

# Load raw data
all_rows = []
max_colors = 0
with open("colors.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        all_rows.append(row)
        max_colors = max(max_colors, len(row) - 3)
        print(f"📥 Loaded {len(all_rows)} rows from colors.csv")

# Load crosswalk
crosswalk = {}
with open("crosswalk.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        username = row["Username"].strip()
        real_name = row["Real Name"].strip()
        location = row["Location"].strip()
        timezone = row.get("Timezone", "UTC").strip()
        latitude = float(row.get("Latitude", "0").strip())
        longitude = float(row.get("Longitude", "0").strip())
        crosswalk[username] = [real_name, location, timezone, latitude, longitude]
      

# Write to CSV
with open("colors_names.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    header = ["Username", "Real Name", "Location", "Date", "Time", "Timezone", "Avg Temp (C)", "Avg Cloud (%)"] + [
        f"Color {i+1}" for i in range(max_colors)
    ]
    writer.writerow(header)

    for row in all_rows:
        username = row[0]
        date = row[1]
        time = row[2]
        colors = row[3:]
        real_name, location, timezone, latitude, longitude = crosswalk.get(username, ("", "", "UTC", 0.0, 0.0))
            
        # Convert UTC date/time to sender's local timezone
        utc_dt = datetime.datetime.strptime(f"{date}, {time}", "%Y-%m-%d, %H:%M")
        utc_dt = utc_dt.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        try:
            local_dt = utc_dt.astimezone(zoneinfo.ZoneInfo(timezone))
            local_date = local_dt.strftime("%Y-%m-%d")
            local_time = local_dt.strftime("%H:%M")
        except Exception:
            local_date = date
            local_time = time

        # Get weather data for each entry (if location is provided)            
        if latitude != 0.0 and longitude != 0.0:
            try:
                avg_temp, avg_cloud = get_weather(latitude, longitude, local_date)
            except Exception:
                avg_temp, avg_cloud = "", ""
        else:
            avg_temp, avg_cloud = "", ""
        # Set missing weather data to "NA"
        avg_temp = avg_temp if avg_temp != "" else "NA"
        avg_cloud = avg_cloud if avg_cloud != "" else "NA"
        # Convert all colors to lowercase
        color_cells = [c.lower() for c in colors]
        color_cells += [""] * (max_colors - len(color_cells))


        out_row = [username, real_name, location, local_date, local_time, timezone, avg_temp, avg_cloud] + color_cells
        writer.writerow(out_row)

print("💾 Finished writing colors_names.csv")