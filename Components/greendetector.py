import subprocess
import cv2
import numpy as np
import os
import time

# =============================
# 1️⃣ Capture Image
# =============================
save_dir = "/home/gle/ESE4970/grass_output"
os.makedirs(save_dir, exist_ok=True)

timestamp = time.strftime("%Y%m%d-%H%M%S")
raw_path = os.path.join(save_dir, f"raw_{timestamp}.jpg")

# Capture image using rpicam
subprocess.run(["rpicam-still", "-t", "1000", "-o", raw_path])

print("Raw image saved.")

# =============================
# 2️⃣ Load Image
# =============================
frame = cv2.imread(raw_path)
if frame is None:
    print("Failed to load image.")
    exit()

# =============================
# 3️⃣ HSV Threshold Parameters
# =============================
Amin = 500  # Minimum connected component area

Hmin, Hmax = 35, 85
Smin, Smax = 40, 255
Vmin, Vmax = 40, 255

# =============================
# 4️⃣ Convert to HSV
# =============================
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# =============================
# 5️⃣ Grass Color Mask
# =============================
mask = cv2.inRange(hsv,
                   (Hmin, Smin, Vmin),
                   (Hmax, Smax, Vmax))

cv2.imwrite(os.path.join(save_dir, f"mask_{timestamp}.png"), mask)

# =============================
# 6️⃣ Noise Reduction
# =============================
mask_blur = cv2.GaussianBlur(mask, (5,5), 0)
cv2.imwrite(os.path.join(save_dir, f"blur_{timestamp}.png"), mask_blur)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
mask_open = cv2.morphologyEx(mask_blur, cv2.MORPH_OPEN, kernel)
mask_clean = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel)

cv2.imwrite(os.path.join(save_dir, f"filtered_{timestamp}.png"), mask_clean)

# =============================
# 7️⃣ Connected Components
# =============================
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_clean)

# Remove small components
final_mask = np.zeros_like(mask_clean)

for i in range(1, num_labels):  # skip background
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= Amin:
        final_mask[labels == i] = 255

cv2.imwrite(os.path.join(save_dir, f"area_filtered_{timestamp}.png"), final_mask)

# =============================
# 8️⃣ Largest Grass Region
# =============================
num_labels2, labels2, stats2, _ = cv2.connectedComponentsWithStats(final_mask)

largest_area = 0
largest_label = 0

for i in range(1, num_labels2):
    area = stats2[i, cv2.CC_STAT_AREA]
    if area > largest_area:
        largest_area = area
        largest_label = i

grass_region = np.zeros_like(final_mask)
grass_region[labels2 == largest_label] = 255

cv2.imwrite(os.path.join(save_dir, f"grass_region_{timestamp}.png"), grass_region)

# =============================
# 9️⃣ Boundary Mask (Inverse)
# =============================
boundary_mask = cv2.bitwise_not(grass_region)
cv2.imwrite(os.path.join(save_dir, f"boundary_{timestamp}.png"), boundary_mask)

print("Processing complete.")
