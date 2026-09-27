"""
Central place for all tunable constants used by the virtual mouse app.
Adjust these values to tune sensitivity for your webcam / screen setup.
"""

# Webcam capture settings
CAMERA_INDEX = 0
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480

# Display window
WINDOW_NAME = "Virtual Mouse"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Mediapipe Hands settings
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

# Cursor movement smoothing (higher = smoother but laggier)
SMOOTHENING = 7

# Pixels to shave off each edge of the frame so the hand doesn't need to
# reach the very edge of the camera view to hit the edge of the screen
FRAME_REDUCTION = 100

# Minimum seconds between two accepted left-clicks (debounce)
CLICK_DELAY = 0.3

# Distance (in pixels, in frame space) between index and middle fingertip
# below which a "pinch" is registered as a click
CLICK_DISTANCE_THRESHOLD = 40

# Quit key
QUIT_KEY = "q"
