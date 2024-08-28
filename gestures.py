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