import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui

MODEL_PATH = "hand_landmarker.task"

INDEX_TIP = 8

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def main():
    # IMPORTANT on macOS: allow accessibility permission for Terminal/Python
    pyautogui.FAILSAFE = False
    screen_w, screen_h = pyautogui.size()

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not opened. Try VideoCapture(1).")
        return

    # Smoothing variables
    smooth = 0.25  # 0.1 = more smooth (slower), 0.4 = faster (less smooth)
    prev_x, prev_y = screen_w / 2, screen_h / 2

    # Region of interest mapping (reduces edge jitter)
    frame_margin = 0.15  # ignore 15% borders

    print("✅ Step 4 running (cursor move). Press q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)

        h, w, _ = frame.shape

        # draw a “safe box” region (where motion maps to the screen)
        x1 = int(w * frame_margin)
        y1 = int(h * frame_margin)
        x2 = int(w * (1 - frame_margin))
        y2 = int(h * (1 - frame_margin))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            lm = hand[INDEX_TIP]

            ix, iy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

            # normalize inside the safe box
            nx = (ix - x1) / (x2 - x1)
            ny = (iy - y1) / (y2 - y1)
            nx = clamp(nx, 0.0, 1.0)
            ny = clamp(ny, 0.0, 1.0)

            # map to screen
            target_x = nx * screen_w
            target_y = ny * screen_h

            # smoothing (low-pass filter)
            cur_x = prev_x + (target_x - prev_x) * smooth
            cur_y = prev_y + (target_y - prev_y) * smooth
            prev_x, prev_y = cur_x, cur_y

            pyautogui.moveTo(cur_x, cur_y)

            cv2.putText(frame, f"cursor: {int(cur_x)}, {int(cur_y)}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Project Step 4 - Cursor Move", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
