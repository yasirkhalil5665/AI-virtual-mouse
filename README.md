# Virtual Mouse

Control your OS mouse cursor using hand gestures captured from your webcam,
powered by [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html),
OpenCV, and [pynput](https://pynput.readthedocs.io/).

## Gestures

| Gesture                                   | Action        |
|--------------------------------------------|---------------|
| ☝️ Index finger up, middle finger down     | Move cursor   |
| ✌️ Index + middle finger up, tips pinched  | Left click    |

Press **`q`** with the preview window focused to quit.

## Project structure

```
virtual_mouse/
├── notebooks/
│   └── all.ipynb          # original exploratory notebook
├── src/
│   ├── __init__.py
│   ├── config.py           # tunable constants (sensitivity, thresholds, etc.)
│   ├── hand_tracker.py      # MediaPipe Hands wrapper + landmark helpers
│   ├── mouse_controller.py  # cursor smoothing + click debouncing
│   └── main.py              # main capture/render loop
├── run.py                  # convenience entry point
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate       # on Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

From the project root:

```bash
python run.py
```

or equivalently:

```bash
python -m src.main
```

A window titled **"Virtual Mouse"** will open showing your webcam feed with
hand landmarks drawn on top. Move your hand into frame and use the gestures
above to control the cursor.

## Tuning

All the "feel" knobs live in `src/config.py`:

- `SMOOTHENING` — higher values make cursor movement smoother but laggier.
- `FRAME_REDUCTION` — size (in pixels) of the margin around the camera frame
  that maps to the full screen; a bigger margin means you don't have to
  reach the very edge of the camera view.
- `CLICK_DELAY` — minimum seconds between two accepted clicks (debounce).
- `CLICK_DISTANCE_THRESHOLD` — how close (in pixels) the index and middle
  fingertips must be to register as a "pinch" click.
- `MIN_DETECTION_CONFIDENCE` / `MIN_TRACKING_CONFIDENCE` — MediaPipe
  confidence thresholds; raise them for fewer false positives, lower them
  if your hand isn't being detected reliably.

## What was fixed from the original notebook

- Removed an invalid top-level `global` statement (only valid inside a
  function; it was silently doing nothing at module scope).
- Camera and MediaPipe resources are now released in a `finally` block, so
  they're cleaned up even if an error or Ctrl+C interrupts the loop
  (previously a crash would leave the webcam locked).
- Added a check for a failed frame read (`cap.read()` returning `False`)
  so the loop exits gracefully instead of erroring on `cv2.flip`.
- Guarded `fingers_up()` against a landmark list shorter than 21 points.
- Replaced the magic capture properties `cap.set(3, ...)` / `cap.set(4, ...)`
  with the named `cv2.CAP_PROP_FRAME_WIDTH` / `cv2.CAP_PROP_FRAME_HEIGHT`
  constants for readability.
- Raised a clear error if the camera fails to open instead of silently
  looping on empty frames.
- Split the single notebook cell into reusable, testable modules
  (`config.py`, `hand_tracker.py`, `mouse_controller.py`, `main.py`).

## Notes

- Tested against Python 3.11 (matches the original notebook's kernel).
- On Linux, `pynput` mouse control requires an X11 session (or XWayland);
  pure-Wayland sessions may block synthetic mouse events.
- On macOS, you'll need to grant your terminal/IDE **Accessibility** and
  **Camera** permissions in System Settings for pynput and OpenCV to work.
