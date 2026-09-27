"""
Thin wrapper around MediaPipe Hands plus small helper functions for
turning raw landmarks into (id, x, y) lists and up/down finger states.
"""

import mediapipe as mp

from . import config


class HandTracker:
    """Wraps mediapipe.solutions.hands with sane defaults and cleanup."""

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
        """Run hand detection on an RGB frame and return mediapipe results."""
        return self.hands.process(img_rgb)

    def draw_landmarks(self, img, hand_landmarks):
        """Draw the hand skeleton on the given (BGR) frame in place."""
        self.mp_draw.draw_landmarks(
            img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
        )

    def close(self):
        """Release mediapipe resources. Safe to call multiple times."""
        self.hands.close()

    # Allow use as a context manager: `with HandTracker() as tracker:`
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_landmark_list(hand_landmarks, frame_w, frame_h):
    """
    Convert normalized mediapipe landmarks into a list of
    (landmark_id, pixel_x, pixel_y) tuples for the given frame size.
    """
    lm_list = []
    for idx, lm in enumerate(hand_landmarks.landmark):
        cx, cy = int(lm.x * frame_w), int(lm.y * frame_h)
        lm_list.append((idx, cx, cy))
    return lm_list


def fingers_up(lm_list):
    """
    Given a 21-point landmark list, return [thumb, index, middle, ring, pinky]
    where 1 means the finger is extended ("up") and 0 means it is folded down.

    Note: this assumes a mirrored (selfie-view) image, which is what the
    main loop produces via cv2.flip(img, 1).
    """
    if len(lm_list) < 21:
        # Not enough landmarks detected this frame; treat as "no fingers up"
        return [0, 0, 0, 0, 0]

    fingers = []
    tips_ids = [4, 8, 12, 16, 20]

    # Thumb: compare x-coordinates (works for a mirrored/selfie view)
    if lm_list[tips_ids[0]][1] > lm_list[tips_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers: tip is "up" if it's above (smaller y) its PIP joint
    for i in range(1, 5):
        if lm_list[tips_ids[i]][2] < lm_list[tips_ids[i] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers
