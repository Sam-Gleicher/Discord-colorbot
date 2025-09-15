import pandas as pd

import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('colors_names.csv')

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