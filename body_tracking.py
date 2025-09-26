from mediapipe import solutions
from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_RGB2BGR

mp_pose = solutions.pose

def map_body(frame, pose1, pose2, crop1, crop2):
    frame1 = frame[crop1.yoffset:crop1.y + crop1.yoffset]
    frame1 = cvtColor(frame1, COLOR_BGR2RGB)
    results1 = pose1.process(frame1)
    frame1 = cvtColor(frame1, COLOR_RGB2BGR)

    if results1.pose_landmarks is not None:
        left1_foot_x = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * crop1.x) + crop1.xoffset
        left1_foot_y = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]).y * crop1.y) + crop1.yoffset

        right1_foot_x = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * crop1.x) + crop1.xoffset
        right1_foot_y = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]).y * crop1.y) + crop1.yoffset

        left1_hand_x = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HAND_INDEX].x * crop1.x) + crop1.xoffset
        left1_hand_y = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HAND_INDEX]).y * crop1.y) + crop1.yoffset

        right1_hand_x = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HAND_INDEX].x * crop1.x) + crop1.xoffset
        right1_hand_y = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HAND_INDEX]).y * crop1.y) + crop1.yoffset

        nose1_x = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]).x * crop1.x) + crop1.xoffset
        nose1_y = int(results1.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]).y * crop1.y) + crop1.yoffset
    else:
        left1_foot_x = left1_foot_y = None
        right1_foot_x = right1_foot_y = None
        left1_hand_x = left1_hand_y = None
        right1_hand_x = right1_hand_y = None
        nose1_x = nose1_y = None

    frame2 = frame[crop2.yoffset:crop1.y + crop2.yoffset]
    frame2 = cvtColor(frame2, COLOR_BGR2RGB)
    results2 = pose2.process(frame2)
    frame2 = cvtColor(frame2, COLOR_RGB2BGR)

    if results2.pose_landmarks is not None:
        left2_foot_x = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * crop2.x) + crop2.xoffset
        left2_foot_y = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]).y * crop2.y) + crop2.yoffset

        right2_foot_x = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * crop2.x) + crop2.xoffset
        right2_foot_y = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]).y * crop2.y) + crop2.yoffset

        left2_hand_x = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HAND_INDEX].x * crop2.x) + crop2.xoffset
        left2_hand_y = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HAND_INDEX]).y * crop2.y) + crop2.yoffset

        right2_hand_x = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HAND_INDEX].x * crop2.x) + crop2.xoffset
        right2_hand_y = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HAND_INDEX]).y * crop2.y) + crop2.yoffset

        nose2_x = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]).x * crop2.x) + crop2.xoffset
        nose2_y = int(results2.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]).y * crop2.y) + crop2.yoffset
    else:
        left2_foot_x = left2_foot_y = None
        right2_foot_x = right2_foot_y = None
        left2_hand_x = left2_hand_y = None
        right2_hand_x = right2_hand_y = None
        nose2_x = nose2_y = None

    return([[
        [left1_foot_x, left1_foot_y],
        [right1_foot_x, right1_foot_y],
        [left1_hand_x, left1_hand_y],
        [right1_hand_x, right1_hand_y],
        [nose1_x, nose1_y],
        [left2_foot_x, left2_foot_y],
        [right2_foot_x, right2_foot_y],
        [left2_hand_x, left2_hand_y],
        [right2_hand_x, right2_hand_y],
        [nose2_x, nose2_y],
    ]])