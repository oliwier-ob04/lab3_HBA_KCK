import sys
import cv2
import mediapipe as mp
from collections import Counter

if len(sys.argv) < 2:
    print("Użycie:")
    print("  python3 main.py camera")
    print("  python3 main.py video  <ścieżka do pliku>")
    sys.exit(1)

mode = sys.argv[1]

if mode == "camera":
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
elif mode == "video":
    if len(sys.argv) < 3:
        print("Użycie dla trybu video:")
        print("  python3 main.py video <ścieżka_do_pliku_wideo>")
        sys.exit(1)
    video_path = sys.argv[2]
    cap = cv2.VideoCapture(video_path)
else:
    print("Nieznany tryb:", mode)
    print("Dozwolone tryby: 'camera' lub 'video'")
    sys.exit(1)

if not cap.isOpened():
    print("Nie można otworzyć źródła wideo.")
    sys.exit(1)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=0)

history = []
buffer_size = 7

def detect_letter(lm):
    l_sh = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    r_sh = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    l_wr = lm[mp_pose.PoseLandmark.LEFT_WRIST]
    r_wr = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

    tol = 0.15
    i_height = 0.2

    if l_wr.y < l_sh.y - i_height and r_wr.y < r_sh.y - i_height:
        if abs(l_wr.x - l_sh.x) < tol and abs(r_wr.x - r_sh.x) < tol:
            return "I"

    if abs(l_wr.y - l_sh.y) < tol and abs(r_wr.y - r_sh.y) < tol:
        if l_wr.x > l_sh.x and r_wr.x < r_sh.x:
            return "T"

    if l_wr.y < l_sh.y - tol and r_wr.y < r_sh.y - tol:
        if l_wr.x > l_sh.x + 0.1 and r_wr.x < r_sh.x - 0.1:
            return "Y"

    r_up = r_wr.y < r_sh.y - tol and abs(r_wr.x - r_sh.x) < tol
    l_side = abs(l_wr.y - l_sh.y) < tol

    if r_up and l_side:
        return "L"

    return "Brak"

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    current_letter = "Brak"

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        current_letter = detect_letter(results.pose_landmarks.landmark)

        history.append(current_letter)
        if len(history) > buffer_size:
            history.pop(0)

        stable_letter = Counter(history).most_common(1)[0][0]

        cv2.putText(
            frame,
            f"{stable_letter}",
            (50, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3,
        )

    cv2.imshow("Program", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
