import pandas as pd

import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('colors_names.csv')
# Drop rows where any cell is "NA"
df = df[~df.apply(lambda row: row.astype(str).str.upper().eq("NA").any(), axis=1)]

# Plot distribution of Color 1
if 'Color 1' in df.columns:
    color1_counts = df['Color 1'].dropna().value_counts()
    plt.figure(figsize=(10, 6))
    color1_counts.plot(kind='bar')
    plt.xlabel('Color Name') 
    plt.ylabel('Count')
    plt.title('Distribution of Primary Colors')
    plt.tight_layout()
    plt.savefig("color1_distribution.png")  # Save as PNG
    plt.show()
    print("Graph 1 saved as color1_distribution.png")
else:
    print("Column 'Color 1' not found in CSV.")

# Plot distribution of all colors
color_columns = [col for col in df.columns if col.startswith('Color')]
all_colors = pd.Series(df[color_columns].values.ravel('K')).dropna()
all_color_counts = all_colors.value_counts()
plt.figure(figsize=(10, 6))
all_color_counts.plot(kind='bar')
plt.xlabel('Color Name')
plt.ylabel('Count')
plt.title('Distribution of All Colors')
plt.tight_layout()
plt.savefig("all_colors_distribution.png")  # Save as PNG
plt.show()
print("Graph 2 saved as all_colors_distribution.png")

# Colors on cloudy vs clear days
clear_days = df[df['Avg Cloud (%)'] < 20]
color1_counts_clear = clear_days['Color 1'].dropna().value_counts()
if not color1_counts_clear.empty:
    plt.figure(figsize=(10, 6))
    color1_counts_clear.plot(kind='bar')
    plt.title('Primary Colors on Clear Days (<20% Cloud Cover)')
    plt.tight_layout()
    plt.savefig("color1_clear_days.png")
    plt.show()
    print("Graph 3 saved as color1_clear_days.png")
else:
    print("No data for clear days (<20% cloud cover).")

cloudy_days = df[df['Avg Cloud (%)'] >= 80]
color1_counts_cloudy = cloudy_days['Color 1'].dropna().value_counts()
if not color1_counts_cloudy.empty:
    plt.figure(figsize=(10, 6))
    color1_counts_cloudy.plot(kind='bar')
    plt.title('Primary Colors on Cloudy Days (>=80% Cloud Cover)')
    plt.tight_layout()
    plt.savefig("color1_cloudy_days.png")
    plt.show()
    print("Graph 4 saved as color1_cloudy_days.png")
else:
    print("No data for cloudy days (>=80% cloud cover).")