import mediapipe as mp
from . import config


class HandTracker:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = config.MAX_NUM_HANDS,
        min_detection_confidence: float = config.MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence: float = config.MIN_TRACKING_CONFIDENCE,
    ):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, img_rgb):
        return self.hands.process(img_rgb)

    def draw_landmarks(self, img, hand_landmarks):
        self.mp_draw.draw_landmarks(
            img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
        )

    def close(self):
        self.hands.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_landmark_list(hand_landmarks, frame_w, frame_h):
    lm_list = []
    for idx, lm in enumerate(hand_landmarks.landmark):
        cx, cy = int(lm.x * frame_w), int(lm.y * frame_h)
        lm_list.append((idx, cx, cy))
    return lm_list


def fingers_up(lm_list):
    if len(lm_list) < 21:
        return [0, 0, 0, 0, 0]

    fingers = []
    tips_ids = [4, 8, 12, 16, 20]

    # Thumb
    if lm_list[tips_ids[0]][1] > lm_list[tips_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    for i in range(1, 5):
        if lm_list[tips_ids[i]][2] < lm_list[tips_ids[i] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers
