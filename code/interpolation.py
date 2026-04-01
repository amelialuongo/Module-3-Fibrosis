from termcolor import colored
import cv2
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# -----------------------------
# INPUT DATA
# -----------------------------
filenames = [
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010136.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010068.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010098.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010118.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010135.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010104.jpg",
]

depths = [9200, 9800, 10000, 9900, 9500, 9700]

# -----------------------------
# IMAGE PROCESSING
# -----------------------------
data_rows = []

print(colored("Counts of pixel by color in each image", "yellow"))

for i, (filename, depth) in enumerate(zip(filenames, depths)):
    img = cv2.imread(filename, 0)

    if img is None:
        print(colored(f"Error loading image: {filename}", "red"))
        continue

    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    total_pixels = binary.size
    white = np.count_nonzero(binary)
    black = total_pixels - white
    white_percent = 100 * white / total_pixels

    data_rows.append({
        'Filename': filename,
        'Depth': depth,
        'White percent': white_percent
    })

    print(colored(f"Image {i}", "cyan"))
    print(colored(f"White pixels: {white}", "white"))
    print(colored(f"Black pixels: {black}", "black"))
    print(colored(f"{filename}:", "red"))
    print(f"{white_percent:.2f}% White | Depth: {depth} microns\n")

# -----------------------------
# SAVE CSV
# -----------------------------
df = pd.DataFrame(data_rows)
df.to_csv('Percent_White_Pixels.csv', index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

# -----------------------------
# INTERPOLATION
# -----------------------------
interpolate_depth = float(input(colored(
    "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# Extract from DataFrame
x = df['Depth'].tolist()
y = df['White percent'].tolist()

# Sort data (REQUIRED for interp1d)
sorted_pairs = sorted(zip(x, y))
x, y = zip(*sorted_pairs)
x = list(x)
y = list(y)

# Interpolate
i = interp1d(x, y, kind='quadratic')
interpolate_point = float(i(interpolate_depth))

print(colored(
    f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# Add interpolated point
depths_i = x + [interpolate_depth]
white_percents_i = y + [interpolate_point]

# -----------------------------
# PLOTTING
# -----------------------------
fig, axs = plt.subplots(2, 1)

# Original data
axs[0].scatter(x, y)
axs[0].set_title('Depth vs Percentage White Pixels')
axs[0].set_xlabel('Depth (microns)')
axs[0].set_ylabel('White pixels (%)')
axs[0].grid(True)

# With interpolated point
axs[1].scatter(x, y)
axs[1].scatter(interpolate_depth, interpolate_point, s=100, label='Interpolated point')
axs[1].set_title('Depth vs Percentage White Pixels (with interpolation)')
axs[1].set_xlabel('Depth (microns)')
axs[1].set_ylabel('White pixels (%)')
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show()