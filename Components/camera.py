import subprocess

# File path to save image
image_path = "/home/pi/Desktop/test2seconds.jpg"

# Capture image with 2-second preview
subprocess.run(["rpicam-still", "-t", "2000", "-o", image_path])

print(f"Image saved to {image_path}")
