import cv2
import numpy as np
from crop_video import video_file, find_intersection, calculate_pixels
from court_mapping import width_p, height_p, map_court, show_mapped_lines, give_mapped_point, open_video
from pathlib import Path

video = cv2.VideoCapture(video_file)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

output_dir = Path("output_videos")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "output.mp4"

fourcc = getattr(cv2, "VideoWriter_fourcc")(*'mp4v')
clip = cv2.VideoWriter(video_file, fourcc, 25.0, (width_p, height_p))
processedFrames = None

class crop1:
    x: float = 50/100
    xoffset: float = 0/100
    xcenter: int = 1

    y: float = 33/100
    yoffset: float = 0/100
    ycenter: int = 0

class crop2:
    x: float = 83/100
    xoffset: float = 0/100
    xcenter: int = 1

    y: float = 60/100
    yoffset: float = 40/100
    ycenter: int = 0

crop1 = calculate_pixels(crop1, width, height)
crop2 = calculate_pixels(crop2, width, height)

average_frame = 3
frame_count = 0

while video.isOpened():
    ret, frame = video.read()
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bw = cv2.threshold(gray, 156, 255, cv2.THRESH_BINARY)[1]
    canny = cv2.Canny(bw, 100, 200)

    hough_lines_probability = cv2.HoughLinesP(canny, 1, np.pi/180, threshold=150, minLineLength=100, maxLineGap=10)
    if hough_lines_probability is None:
        clip.write(np.zeros((height_p, width_p, 3), dtype=np.uint8))
        continue

    num_of_intersections = np.zeros((len(hough_lines_probability), 2))
    index = 0

    for hp_line1 in hough_lines_probability:
        if isinstance(hp_line1, np.ndarray) and hp_line1.shape[0] == 4:
            line1_x1, line1_y1, line1_x2, line1_y2 = hp_line1[0]
            line1 = np.array([line1_x1, line1_y1, line1_x2, line1_y2])
            for hp_line2 in hough_lines_probability:
                if isinstance(hp_line2, np.ndarray) and hp_line2.shape[0] == 4:
                    line2_x1, line2_y1, line21_x2, line2_y2 = hp_line2[0]
                    line2 = np.array([line2_x1, line2_y1, line21_x2, line2_y2])

                    if line1 is line2:
                        continue
                    if line1_x1 > line1_x2:
                        line1_x1, line1_x2 = line1_x2, line1_x1
                    if line1_y1 > line1_y2:
                        line1_y1, line1_y2 = line1_y2, line1_y1

                    intersection = find_intersection(line1, line2, line1_x1 - 200, line1_y1 - 200, line1_x2 + 200, line1_y2 + 200)

                    if intersection is not None:
                        num_of_intersections[index][0] += 1
                num_of_intersections[index][1] = index
                index += 1
            index = p = 0
            
            kernel = np.ones((5, 5), np.uint8)
            dilation = cv2.dilate(bw, kernel, iterations=1)
            
            non_court_area = dilation.copy()
            num_of_intersections = num_of_intersections[(-num_of_intersections)[:, 0].argsort()]
            
            for hp_line in hough_lines_probability:
                if isinstance(hp_line, np.ndarray) and hp_line.shape[0] == 4:
                    x1, y1, x2, y2 = hp_line

    cv2.imshow("Court Mapped Test", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
clip.release()
video.release()
cv2.destroyAllWindows()