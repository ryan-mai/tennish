import numpy as np
import cv2
from cv2 import getPerspectiveTransform, warpPerspective, line, circle, perspectiveTransform
from crop_video import video_file, check_file

def open_video(path: str = video_file):
    if not check_file(path):
        raise SystemExit(f"Video file: {path} cannot be found!")

    video = cv2.VideoCapture(path)
    if not video.isOpened():
        raise SystemExit(f"Video file: {path} cannot be opened!")
    return video

width_p = int(967)
height_p = int(1585)

width = int(967)
height = 1585

ratio = np.float32(1097 / 2377)
court_height = int(height * 0.6)
court_width = int(court_height * ratio)

x_offset = int((width - court_width) / 2)
y_offset = int((height - court_height) / 2)

court_top_left = [x_offset, y_offset]
court_top_right = [court_width + x_offset, y_offset]
court_bottom_left = [x_offset, court_height + y_offset]
court_bottom_right = [court_width + x_offset, court_height + y_offset]

def map_court(frame, top_left, top_right, bottom_left, bottom_right):
    pts1 = np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.float32)
    pts2 = np.array([court_top_left, court_top_right, court_bottom_left, court_bottom_right], dtype=np.float32)
    matrix = getPerspectiveTransform(pts1, pts2)
    result = warpPerspective(frame, matrix, (width, height))
    return result, matrix

def show_mapped_lines(frame):
    cv2.rectangle(frame, (0, 0), (width, height), color=(255, 255, 255), thickness=6)
    cv2.rectangle(frame, (x_offset, y_offset), (court_width + x_offset, court_height + y_offset), color=(255, 255, 255), thickness=2)
    # Half Line
    y_half = y_offset + int(court_height * 0.5)
    cv2.line(frame, (x_offset, y_half), (court_width + x_offset, y_half), color=(255, 255, 255), thickness=2)
    
    # Service Box & Boundaries
    cv2.rectangle(frame, (x_offset + int(court_width * 0.124886), y_offset), (court_width + x_offset - int(court_width*0.124886), court_height + y_offset), color=(255, 255, 255), thickness=2)
    cv2.rectangle(frame, (x_offset + int(court_width * 0.124886), y_offset + int(court_height * 0.23054)), (court_width + x_offset - int(court_width * 0.124886), court_height + y_offset - int(court_height * 0.23054)), color=(255, 255, 255), thickness=6)
    cv2.rectangle(frame, (x_offset + int(court_width * 0.5), y_offset + int(court_height * 0.23054)), (court_width + x_offset - int(court_width * 0.5), court_height + y_offset - int(court_height * 0.23054)), color=(255, 255, 255), thickness=6)
    return frame

def show_mapped_point(frame, matrix, point):
    points = np.array([[point]])
    transformed = perspectiveTransform(points, matrix)[0][0]
    cv2.circle(frame, (int(transformed[0]), int(transformed[1])), radius=0, color=(0, 0, 255), thickness=25)
    return frame

def give_mapped_point(matrix, point):
    points = np.array([[point]])
    transformed = perspectiveTransform(points, matrix)[0][0]
    return (int(transformed[0]), int(transformed[1]))