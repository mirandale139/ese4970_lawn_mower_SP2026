import os
import subprocess
import time

# =============================
# USER SETTINGS
# =============================
record_time = 10   # seconds (set to 0 for manual stop)

save_dir = "/home/gle/ESE4970/grass_output"

# =============================
# Create timestamp filename
# =============================
timestamp = time.strftime("%Y%m%d-%H%M%S")
video_path = os.path.join(save_dir, f"vid_test_cam_{timestamp}.mp4")

time.sleep(5)

print("Starting recording...")

# If record_time > 0 → fixed duration
if record_time > 0:
    subprocess.run([
        "rpicam-vid",
        "--width", "1920",
        "--height", "1080",
        "--framerate", "30",
        "--nopreview",
        "-t", str(record_time * 1000),  # convert sec → ms
        "-o", video_path
    ])

# If record_time = 0 → press ENTER to stop
else:
    process = subprocess.Popen([
        "rpicam-vid",
        "--width", "1920",
        "--height", "1080",
        "--framerate", "30",
        "--nopreview",
        "-t", "0",
        "-o", video_path
    ])

    input("Press ENTER to stop recording...\n")
    process.terminate()
    process.wait()

print(f"Video saved to {video_path}")
