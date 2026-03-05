import os
import subprocess
import time

# =============================
# USER SETTINGS
# =============================
record_time = 60   # seconds (set to 0 for manual stop)

save_dir = "/home/gle/ESE4970/grass_output"

# Ensure directory exists
os.makedirs(save_dir, exist_ok=True)

# =============================
# Create timestamp filename
# =============================
timestamp = time.strftime("%Y%m%d-%H%M%S")
video_path = os.path.join(save_dir, f"vid_test_cam_{timestamp}.mp4")

time.sleep(5)

print("\nStarting recording...\n")

# =============================
# FIXED DURATION RECORDING
# =============================
if record_time > 0:

    subprocess.run([
        "rpicam-vid",
        "--codec", "h264",          # camera encoder
        "--libav-format", "mp4",    # wrap into MP4 container
        "--width", "1920",
        "--height", "1080",
        "--framerate", "30",
        "--nopreview",
        "-t", str(record_time * 1000),  # seconds → milliseconds
        "-o", video_path
    ])

# =============================
# MANUAL STOP RECORDING
# =============================
else:

    process = subprocess.Popen([
        "rpicam-vid",
        "--codec", "h264",
        "--libav-format", "mp4",
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
