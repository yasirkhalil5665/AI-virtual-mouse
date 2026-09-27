import cv2
import numpy as np
import tkinter as tk

from . import config
from .hand_tracker import HandTracker, fingers_up, get_landmark_list
from .mouse_controller import VirtualMouse


def get_screen_size():
    root = tk.Tk()
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    return screen_w, screen_h


def run():
    screen_w, screen_h = get_screen_size()
    virtual_mouse = VirtualMouse(screen_w, screen_h)

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera index {config.CAMERA_INDEX}. "
            "Check that a webcam is connected and not in use by another app."
        )

    cv2.namedWindow(config.WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(config.WINDOW_NAME, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    tracker = HandTracker()

    try:
        while True:
            success, img = cap.read()
            if not success:
                print("Warning: failed to read frame from camera, stopping.")
                break

            img = cv2.flip(img, 1)
            frame_h, frame_w, _ = img.shape
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = tracker.process(img_rgb)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                tracker.draw_landmarks(img, hand_landmarks)

                lm_list = get_landmark_list(hand_landmarks, frame_w, frame_h)

                if len(lm_list) != 0:
                    x1, y1 = lm_list[8][1], lm_list[8][2]    # index fingertip
                    x2, y2 = lm_list[12][1], lm_list[12][2]  # middle fingertip

                    fingers = fingers_up(lm_list)

                    # Draw the active tracking region
                    r = config.FRAME_REDUCTION
                    cv2.rectangle(
                        img, (r, r), (frame_w - r, frame_h - r), (255, 0, 255), 2
                    )

                    # Only index finger up -> move cursor
                    if fingers[1] == 1 and fingers[2] == 0:
                        virtual_mouse.move_to(x1, y1, frame_w, frame_h)

                    # Index + middle finger up -> click when pinched
                    if fingers[1] == 1 and fingers[2] == 1:
                        distance = np.hypot(x2 - x1, y2 - y1)
                        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                        if virtual_mouse.maybe_click(distance):
                            cv2.circle(
                                img,
                                ((x1 + x2) // 2, (y1 + y2) // 2),
                                15,
                                (0, 255, 0),
                                cv2.FILLED,
                            )

            cv2.imshow(config.WINDOW_NAME, img)

            if cv2.waitKey(1) & 0xFF == ord(config.QUIT_KEY):
                break

    finally:
        #clear
        cap.release()
        cv2.destroyAllWindows()
        tracker.close()


if __name__ == "__main__":
    run()
