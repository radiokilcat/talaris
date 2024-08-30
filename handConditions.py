import math

def are_fingers_close(landmarks, threshold=0.05):
    index_finger_tip = landmarks[8]
    middle_finger_tip = landmarks[12]

    distance = ((index_finger_tip.x - middle_finger_tip.x) ** 2 +
                (index_finger_tip.y - middle_finger_tip.y) ** 2 +
                (index_finger_tip.z - middle_finger_tip.z) ** 2) ** 0.5

    return distance < threshold

def is_pinch_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    if distance < 0.05:
        return True
    return False


def calculate_angle(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    cosine_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2))
    angle = math.degrees(math.acos(cosine_angle))
    return angle

def is_l_shape_gesture(landmarks, img_w, img_h):
    wrist = [landmarks[0].x * img_w, landmarks[0].y * img_h]
    index_base = [landmarks[5].x * img_w, landmarks[5].y * img_h]
    index_tip = [landmarks[8].x * img_w, landmarks[8].y * img_h]
    middle_base = [landmarks[9].x * img_w, landmarks[9].y * img_h]
    middle_tip = [landmarks[12].x * img_w, landmarks[12].y * img_h]

    index_angle = calculate_angle(wrist, index_base, index_tip)
    middle_angle = calculate_angle(wrist, middle_base, middle_tip)

    if 80 < index_angle < 100 and 80 < middle_angle < 100:
        return True
    return False

def is_fist(landmarks):
    finger_tips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]]
    finger_bases = [landmarks[3], landmarks[6], landmarks[10], landmarks[14], landmarks[18]]
    for tip, base in zip(finger_tips, finger_bases):
        if tip.y < base.y:
            return False
    return True

def is_thumbs_up(landmarks):
    thumb_tip = landmarks[4]
    thumb_base = landmarks[2]
    if thumb_tip.y < thumb_base.y:
        return all(landmarks[i].y > landmarks[i-2].y for i in range(8, 21, 4))
    return False