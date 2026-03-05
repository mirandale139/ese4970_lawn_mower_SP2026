import os
import subprocess
import time

record_time = 60
save_dir = "/home/gle/ESE4970/grass_output"

os.makedirs(save_dir, exist_ok=True)

timestamp = time.strftime("%Y%m%d-%H%M%S")

h264_path = os.path.join(save_dir, f"vid_test_cam_{timestamp}.h264")
mp4_path = os.path.join(save_dir, f"vid_test_cam_{timestamp}.mp4")

print("Recording video...")

subprocess.run([
    "rpicam-vid",
    "--codec", "h264",
    "--width", "1920",
    "--height", "1080",
    "--framerate", "30",
    "--nopreview",
    "-t", str(record_time * 1000),
    "-o", h264_path
])

print("Converting to MP4...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-framerate", "30",
    "-i", h264_path,
    "-c", "copy",
    mp4_path
])

print(f"Video saved to {mp4_path}")
