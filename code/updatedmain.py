import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

start = time.time()
# -----------------------------
# INPUT DATA
# -----------------------------

filenames = [
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010092.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010068.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010098.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010118.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010135.jpg",
    r"/Users/amelialuongo/Desktop/comp bme/Module-3-Fibrosis/images/6 images/MASK_SK658 Slobe ch010104.jpg",
]

depths = [15, 1000, 3000, 5300, 7000, 9900]

# -----------------------------
# VALIDATION
# -----------------------------

if len(filenames) != len(depths):
    raise ValueError("Number of filenames must match number of depths!")

# -----------------------------
# PROCESS IMAGES
# -----------------------------

results = []

for filename, depth in zip(filenames, depths):
    img = cv2.imread(filename, 0)

    if img is None:
        print(f"⚠️ Warning: Could not load image: {filename}")
        continue

    # Convert to binary
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Count pixels
    white = np.sum(binary == 255)
    black = np.sum(binary == 0)
    total = white + black

    # Avoid divide-by-zero
    white_percent = (100 * white / total) if total > 0 else 0

    # Store results
    results.append({
        "Filename": filename,
        "Depth": depth,
        "White Pixels": white,
        "Black Pixels": black,
        "White Percent": white_percent
    })

    # Print nicely
    print(f"\n📄 {filename}")
    print(f"Depth: {depth} microns")
    print(f"White pixels: {white}")
    print(f"Black pixels: {black}")
    print(f"White %: {white_percent:.2f}%")

# -----------------------------
# SAVE TO CSV
# -----------------------------

df = pd.DataFrame(results)
df.to_csv("Percent_White_Pixels.csv", index=False)

print("\n✅ CSV file 'Percent_White_Pixels.csv' created.")

# -----------------------------
# OPTIONAL: PLOT RESULTS
# -----------------------------

plt.figure()
plt.scatter(df["Depth"], df["White Percent"])
plt.xlabel("Depth (microns)")
plt.ylabel("White Pixels (%)")
plt.title("White Pixel Percentage vs Depth")
plt.grid()
plt.show()

end = time.time()
print(f"\n⏱️ Total runtime: {end - start:.3f} seconds")