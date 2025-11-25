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

# Average number of colors by individual
color_columns = [col for col in df.columns if col.startswith('Color')]

# Count non-empty colors for each row
df['Color_Count'] = df[color_columns].apply(lambda row: row.notna().sum(), axis=1)

# Calculate average colors per person
avg_colors_by_person = df.groupby('Real Name')['Color_Count'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
avg_colors_by_person.plot(kind='bar')
plt.xlabel('Real Name')
plt.ylabel('Average Number of Colors')
plt.title('Average Number of Colors Reported by Individual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("avg_colors_by_person.png")
plt.show()
print("Graph 5 saved as avg_colors_by_person.png")

# Max colors by individual
max_colors_by_person = df.groupby('Real Name')['Color_Count'].max().sort_values(
    ascending=False
)   
plt.figure(figsize=(12, 6))
max_colors_by_person.plot(kind='bar')
plt.xlabel('Real Name')
plt.ylabel('Maximum Number of Colors')
plt.title('Maximum Number of Colors Reported by Individual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("max_colors_by_person.png")
plt.show()
print("Graph 6 saved as max_colors_by_person.png")
