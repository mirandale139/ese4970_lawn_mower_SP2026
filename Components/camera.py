import subprocess
import time

# File path to save image
save_dir = "/home/gle/ESE4970/grass_output"
timestamp = time.strftime("%Y%m%d-%H%M%S")
image_path = os.path.join(save_dir, f"test_cam_{timestamp}.jpg")


# Capture image with 2-second preview
subprocess.run(["rpicam-still", "-t", "2000", "-o", image_path])

print(f"Image saved to {image_path}")
