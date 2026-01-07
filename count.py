import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Landmark indices
TIP_IDS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)  # mirror view
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    finger_count = 0
    finger_states = [0, 0, 0, 0, 0]  # thumb..pinky

    if res.multi_hand_landmarks and res.multi_handedness:
        hand_landmarks = res.multi_hand_landmarks[0]
        handedness = res.multi_handedness[0].classification[0].label  # "Left" or "Right"

        # Convert landmarks to pixel coords
        lm = []
        for i in range(21):
            x = int(hand_landmarks.landmark[i].x * w)
            y = int(hand_landmarks.landmark[i].y * h)
            lm.append((x, y))

        # ---- Thumb (different rule: compare x, depends on left/right) ----
        # Tip x compared to IP joint x (landmark 3)
        if handedness == "Right":
            if lm[TIP_IDS[0]][0] > lm[3][0]:
                finger_states[0] = 1
        else:  # Left hand
            if lm[TIP_IDS[0]][0] < lm[3][0]:
                finger_states[0] = 1

        # ---- Other 4 fingers (tip y compared to PIP y) ----
        # Index tip(8) vs pip(6), Middle tip(12) vs pip(10), Ring tip(16) vs pip(14), Pinky tip(20) vs pip(18)
        pip_ids = [6, 10, 14, 18]
        for idx, tip_id in enumerate(TIP_IDS[1:], start=1):
            pip_id = pip_ids[idx - 1]
            if lm[tip_id][1] < lm[pip_id][1]:  # tip is higher (smaller y) => finger up
                finger_states[idx] = 1

        finger_count = sum(finger_states)

        # Draw landmarks
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show states
        cv2.putText(frame, f"Hand: {handedness}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display count
    cv2.putText(frame, f"Fingers: {finger_count}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    # Optional: show each finger state
    names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    y0 = 120
    for i, name in enumerate(names):
        cv2.putText(frame, f"{name}: {finger_states[i]}", (10, y0 + 30*i),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
