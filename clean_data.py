import csv
import datetime
import zoneinfo

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
        crosswalk[username] = [real_name, location, timezone]        

# Write to CSV
with open("colors_names.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header: Username, Real Name, Location, Date, Time, Color 1...Color N
    header = ["Username", "Real Name", "Location", "Date", "Time", "Timezone"] + [
        f"Color {i+1}" for i in range(max_colors)
    ]
    writer.writerow(header)

    for row in all_rows:
        username = row[0]
        date = row[1]
        time = row[2]
        colors = row[3:]
        real_name, location, timezone = crosswalk.get(username, ("", "", "UTC"))
            
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
        out_row = [username, real_name, location, local_date, local_time, timezone] + colors
        out_row += [""] * (max_colors - len(colors))
        writer.writerow(out_row)
            
print("💾 Finished writing colors_names.csv")