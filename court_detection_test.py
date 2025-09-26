from numpy import pi, ones, zeros, uint8, cos, sin
from cv2 import VideoCapture, cvtColor, Canny, threshold, THRESH_BINARY, dilate, floodFill, erode, VideoWriter, VideoWriter_fourcc #type: ignore
from cv2 import HoughLines, HoughLinesP, line, rectangle, imshow, waitKey, destroyAllWindows, resize, COLOR_BGR2GRAY, COLOR_GRAY2BGR
from crop_video import video_file, find_intersection, calculate_pixels
from court_mapping import width_p, height_p, map_court, show_mapped_lines, give_mapped_point, open_video
from pathlib import Path
import mediapipe as mp
from body_tracking import map_body

video = VideoCapture(video_file)
width = int(video.get(3))
height = int(video.get(4))

output_dir = Path("output_videos")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "output.mp4"

widthP, heightP = width, height
fourcc = VideoWriter_fourcc(*'mp4v') 
clip = VideoWriter(str(output_path), fourcc, 25.0, (widthP, heightP))

if not video.isOpened():
    print("ERROR: failed to open video. Check video_file path and codecs.")
    input("Press Enter to exit...")
    raise SystemExit(1)

extra_len = width // 3

class body1:
    pose = mp_pose

class axis:
    top = [[-extra_len, 0], [width + extra_len, 0]]
    right = [[width + extra_len, 0], [width + extra_len, height]]
    bottom = [[-extra_len, height], [width + extra_len, height]]
    left = [[-extra_len, 0], [-extra_len, height]]

corner_tlp, corner_trp, corner_blp, corner_brp = None, None, None, None


while video.isOpened():
    ret, frame = video.read()
    if not ret or frame is None:
        print("End of video or cannot read frame.")
        break

    gray = cvtColor(frame, COLOR_BGR2GRAY)
    bw = threshold(gray, 156, 255, THRESH_BINARY)[1]
    canny = Canny(bw, 100, 200)
    dilation = dilate(bw, ones((5, 5), uint8), iterations=1)
    non_rect_area = dilation.copy()
    hough_plines = HoughLinesP(canny, 1, pi/180, threshold=150, minLineLength=100, maxLineGap=10)
    if hough_plines is None:
        continue
    for hough_pline in hough_plines:
        coords = hough_pline.squeeze()
        if coords.ndim == 0:
            coords = [coords] * 4
        x1, y1, x2, y2 = map(int, coords)
        floodFill(non_rect_area, zeros((height + 2, width + 2), uint8), (x1, y1), (1, 1, 1))
        floodFill(non_rect_area, zeros((height + 2, width + 2), uint8), (x2, y2), (1, 1, 1))
    dilation[non_rect_area == 255] = 0
    dilation[non_rect_area == 1] = 255
    eroded = erode(dilation, ones((5, 5), dtype=uint8))
    canny_main = Canny(eroded, 100, 100)

    hough_lines = HoughLines(canny_main, 2, pi/180, 300)
    if hough_lines is None:
        continue

    x_left_outer, x_right_outer, x_fault_left, x_fault_right = width + extra_len, 0 - extra_len, width + extra_len, 0 - extra_len
    x_left_outer_line, x_right_outer_line, x_fault_left_line, x_fault_right_line = None, None, None, None
    y_top_outer, y_bottom_outer, y_fault_top, y_fault_bottom = height, 0, height, 0
    y_top_outer_line, y_bottom_outer_line, y_fault_top_line, y_fault_bottom_line = None, None, None, None

    for hough_line in hough_lines:
        vals = hough_line.squeeze()
        if vals.ndim == 0 or len(vals) != 2:
            continue
        rho, theta = map(float, vals)
        a, b = cos(theta), sin(theta)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + width*(-b)), int(y0 + width*(a))
        x2, y2 = int(x0 - width*(-b)), int(y0 - width*(a))

        intersection_xf = find_intersection(axis.bottom, [[x1, y1], [x2, y2]], -extra_len, width + extra_len, 0, height)
        intersection_xo = find_intersection(axis.top, [[x1, y1], [x2, y2]], -extra_len, width + extra_len, 0, height)
        intersection_yf = find_intersection(axis.right, [[x1, y1], [x2, y2]], -extra_len, width + extra_len, 0, height)
        intersection_yo = find_intersection(axis.left, [[x1, y1], [x2, y2]], -extra_len, width + extra_len, 0, height)

        if intersection_xo and intersection_xo[0] < x_left_outer: x_left_outer, x_left_outer_line = intersection_xo[0], [[x1,y1],[x2,y2]]
        if intersection_xo and intersection_xo[0] > x_right_outer: x_right_outer, x_right_outer_line = intersection_xo[0], [[x1,y1],[x2,y2]]
        if intersection_yo and intersection_yo[1] < y_top_outer: y_top_outer, y_top_outer_line = intersection_yo[1], [[x1,y1],[x2,y2]]
        if intersection_yo and intersection_yo[1] > y_bottom_outer: y_bottom_outer, y_bottom_outer_line = intersection_yo[1], [[x1,y1],[x2,y2]]
        if intersection_xf and intersection_xf[0] < x_fault_left: x_fault_left, x_fault_left_line = intersection_xf[0], [[x1,y1],[x2,y2]]
        if intersection_xf and intersection_xf[0] > x_fault_right: x_fault_right, x_fault_right_line = intersection_xf[0], [[x1,y1],[x2,y2]]
        if intersection_yf and intersection_yf[1] < y_fault_top: y_fault_top, y_fault_top_line = intersection_yf[1], [[x1,y1],[x2,y2]]
        if intersection_yf and intersection_yf[1] > y_fault_bottom: y_fault_bottom, y_fault_bottom_line = intersection_yf[1], [[x1,y1],[x2,y2]]

    top_left_p = find_intersection(x_left_outer_line, y_top_outer_line, -extra_len, width + extra_len, 0, height)
    top_right_p = find_intersection(x_right_outer_line, y_fault_top_line, -extra_len, width + extra_len, 0, height)
    bottom_left_p = find_intersection(x_fault_left_line, y_bottom_outer_line, -extra_len, width + extra_len, 0, height)
    bottom_right_p = find_intersection(x_fault_right_line, y_fault_bottom_line, -extra_len, width + extra_len, 0, height)

    if top_left_p and top_right_p and bottom_left_p and bottom_right_p:
        processedFrame, _ = map_court(frame, top_left_p, top_right_p, bottom_left_p, bottom_right_p)
        rectangle(processedFrame, (0, 0), (width_p, height_p), (188, 145, 103), 2000)
        processedFrame = show_mapped_lines(processedFrame)
        imshow("Court Mapping", processedFrame)
        
    imshow("Original Frame", frame)
    if 'canny_main' in locals():
        imshow("Canny Main", canny_main)

        canny_bgr = cvtColor(canny_main, COLOR_GRAY2BGR)
        canny_resized = resize(canny_bgr, (widthP, heightP))
        clip.write(canny_resized)
    key = waitKey(1) & 0xFF
    if key == ord('q'):
        print("User requested exit.")
        break
clip.release()
video.release()
destroyAllWindows()