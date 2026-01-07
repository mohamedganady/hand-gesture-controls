import cv2
import math
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui

MODEL_PATH = "hand_landmarker.task"

THUMB_TIP = 4
INDEX_TIP = 8

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def to_pixel(lm, w, h):
    return int(lm.x * w), int(lm.y * h)

def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def main():
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

    # Cursor smoothing
    smooth = 0.25
    prev_x, prev_y = screen_w / 2, screen_h / 2
    frame_margin = 0.15

    # Click detection
    pinch_threshold_px = 35
    click_cooldown_s = 0.45
    last_click_time = 0.0
    pinched = False  # state to avoid repeated clicks while holding pinch

    print("✅ Step 5 running (cursor + pinch click). Press q to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)

        h, w, _ = frame.shape

        # safe box
        x1 = int(w * frame_margin)
        y1 = int(h * frame_margin)
        x2 = int(w * (1 - frame_margin))
        y2 = int(h * (1 - frame_margin))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]

            # index tip controls cursor
            index_lm = hand[INDEX_TIP]
            ix, iy = to_pixel(index_lm, w, h)
            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

            nx = (ix - x1) / (x2 - x1)
            ny = (iy - y1) / (y2 - y1)
            nx = clamp(nx, 0.0, 1.0)
            ny = clamp(ny, 0.0, 1.0)

            target_x = nx * screen_w
            target_y = ny * screen_h

            cur_x = prev_x + (target_x - prev_x) * smooth
            cur_y = prev_y + (target_y - prev_y) * smooth
            prev_x, prev_y = cur_x, cur_y

            pyautogui.moveTo(cur_x, cur_y)

            # pinch detection
            thumb = to_pixel(hand[THUMB_TIP], w, h)
            index = to_pixel(hand[INDEX_TIP], w, h)

            cv2.circle(frame, thumb, 8, (255, 255, 255), -1)
            cv2.line(frame, thumb, index, (255, 255, 255), 2)

            d = dist(thumb, index)
            cv2.putText(frame, f"pinch: {int(d)} px", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            now = time.time()
            is_pinch_now = d < pinch_threshold_px

            # Click on pinch "edge" (when pinch starts), plus cooldown
            if is_pinch_now and (not pinched) and (now - last_click_time > click_cooldown_s):
                pyautogui.click()
                last_click_time = now
                pinched = True
                cv2.putText(frame, "CLICK!", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)
            elif not is_pinch_now:
                pinched = False

        cv2.imshow("Project Step 5 - Pinch Click", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
