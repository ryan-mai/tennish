from pathlib import Path

video_file = r'input_videos\us_open_final_2025_9s.mp4'

def check_bounds(frame1, frame2):
    valid = True
    if (frame1.xcenter == 0):
        if (frame1.x + frame1.xoffset > 1) or (frame1.x > 1):
            print("Crop 1: X-Coordinates are out of bounds!")
            valid = False
    if (frame1.ycenter == 0):
        if (frame1.y + frame1.yoffset > 1) or (frame1.y > 1):
            print("Crop 1: Y-Coordinates are out of bounds!")
            valid = False
    if (frame2.xcenter == 0):
        if (frame2.x + frame2.xoffset > 1) or (frame2.x > 1):
            print("Crop 2: X-Coordinates are out of bounds!")
            valid = False
    if (frame2.ycenter == 0):
        if (frame2.y + frame2.yoffset > 1) or (frame2.y > 1):
            print("Crop 2: Y-Coordinates are out of bounds!")
            valid = False
    return valid

def check_file(file):
    if not Path(file).exists():
        print(f"Video file: {file} does not exist!")
        return False
    return True

def calculate_pixels(frame, width, height):
    frame.x = int(width * frame.x)
    frame.y = int(height * frame.y)

    if frame.xcenter:
        frame.xoffset = int((width - frame.x)/2)
    else:
        frame.xoffset = int(width * frame.xoffset)

    if frame.ycenter:
        frame.yoffset = int((height - frame.y)/2)
    else:
        frame.yoffset = int(height * frame.yoffset)

    return frame

def determinant(a, b):
    return a[0] * b[1] - a[1] * b[0]
    #eg. 1 2 = a[0] a[1]
    #    3 4 = b[0] b[1]

def find_intersection(line1, line2, x1, x2, y1, y2):
    # line1 = ((1, 2), (4, 6))
    # line2 = ((1, 5)) (4, 3))
    if not line1 or not line2:
        return None
    
    line1_p1, line1_p2 = line1
    line2_p1, line2_p2 = line2

    x_diff = (line1_p1[0] - line1_p2[0], line2_p1[0] - line2_p1[1]) # 1 - 4 = -3
    y_diff = (line1_p1[1] - line1_p2[1], line2_p1[1] - line2_p1[1]) # 2 - 6 = -4
    
    det_diff = determinant(x_diff, y_diff)
    if det_diff == 0:
        print("Points are parallel")
        return None
    
    det = (determinant(*line1), determinant(*line2))
    x = int(determinant(det, x_diff) / det_diff)
    y = int(determinant(det, y_diff) / det_diff)
    if (x < x1) or (x > x2) or (y < y1) or (y > y2):
        return None
    return x, y