import os
import cv2
import numpy as np
from crop_video import video_file

os.makedirs("output_videos", exist_ok=True)
out_file = "output_videos/output.mp4"

cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    raise SystemExit(f"Cannot open input video: {video_file}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = getattr(cv2, "VideoWriter_fourcc")(*'mp4v')
out = cv2.VideoWriter(out_file, fourcc, 25.0, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bw = cv2.threshold(gray, 156, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(bw, 100, 200)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=150, minLineLength=100, maxLineGap=10)
    if lines is not None:
        lines = lines.reshape(-1, 4)  # ensure shape (N,4)
        for x1, y1, x2, y2 in lines:
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release()
print("Wrote", out_file)