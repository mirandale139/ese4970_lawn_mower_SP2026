import cv2
import numpy as np
import os

# -------- Settings --------
filename = "test_cam_20260218-150219.jpg"
Amin = 500  # Minimum connected component area

# New HSV Range
Hmin, Hmax = 35, 85
Smin, Smax = 25, 150
Vmin, Vmax = 50, 255

# -------- Load Image --------
frame = cv2.imread(filename)

if frame is None:
    print("Failed to load image.")
    exit()

base_name = os.path.splitext(filename)[0]

# -------- Convert to HSV --------
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# -------- Grass Mask --------

mask = cv2.inRange(hsv,
                   (Hmin, Smin, Vmin),
                   (Hmax, Smax, Vmax))
b, g, r = cv2.split(frame)

green_rule = (g > r*0.9) & (g > b*0.9)

mask = mask & (green_rule.astype(np.uint8) * 255)


cv2.imwrite(f"{base_name}_mask.png", mask)

# -------- Morphological Cleaning --------
mask_blur = cv2.GaussianBlur(mask, (5,5), 0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
mask_open = cv2.morphologyEx(mask_blur, cv2.MORPH_OPEN, kernel)
mask_clean = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel)

# -------- Connected Components --------
num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_clean)

final_mask = np.zeros_like(mask_clean)

for i in range(1, num_labels):  # Skip background
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= Amin:
        final_mask[labels == i] = 255

# -------- Largest Grass Region --------
# num_labels2, labels2, stats2, _ = cv2.connectedComponentsWithStats(final_mask)

# largest_area = 0
# largest_label = 0

# for i in range(1, num_labels2):
#     area = stats2[i, cv2.CC_STAT_AREA]
#     if area > largest_area:
#         largest_area = area
#         largest_label = i

# grass_region = np.zeros_like(final_mask)
# grass_region[labels2 == largest_label] = 255

grass_region = final_mask.copy()

cv2.imwrite(f"{base_name}_grass.png", grass_region)

# -------- Draw Red Boundary on Raw Image --------
contours, _ = cv2.findContours(grass_region,
                               cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

overlay = frame.copy()
cv2.drawContours(overlay, contours, -1, (0,0,255), 3)  # Red boundary

cv2.imwrite(f"{base_name}_boundary.png", overlay)

print("Processing complete.")
