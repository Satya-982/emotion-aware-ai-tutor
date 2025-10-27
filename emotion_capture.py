import os, cv2, csv, time
from datetime import datetime
from collections import deque
from deepface import DeepFace

# ================= PATHS ================= #
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
LESSON_DIR = os.path.join(BASE, "lesson_content")
CSV_PATH = os.path.join(DATA, "sessions.csv")
LESSON_PATH = os.path.join(LESSON_DIR, "lesson.txt")

os.makedirs(DATA, exist_ok=True)
os.makedirs(LESSON_DIR, exist_ok=True)

# CSV Header Ensure
if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
    with open(CSV_PATH, "w", newline="") as f:
        csv.writer(f).writerow(
            ["timestamp", "user_id", "topic_id", "emotion", "confidence", "action", "quiz_score"]
        )

# ================ LOAD LESSON ================ #
def load_lesson():
    raw = open(LESSON_PATH, "r", encoding="utf-8").read().strip()
    parts = [p.strip() for p in raw.split("\n\n") if p.strip()]
    topic = next((p for p in parts if p.lower().startswith("topic")), "Topic: Lesson")
    slides = [p for p in parts if p.lower().startswith("slide")]
    hints = [p for p in parts if p.lower().startswith("hint")]
    quiz_block = next((p for p in parts if "Quiz" in p), None)
    return topic, slides, hints, quiz_block

TOPIC, SLIDES, HINTS, QUIZ_BLOCK = load_lesson()
if not SLIDES: SLIDES = ["Slide:\nContent not found."]

def draw_text(frame, text, x=20, y=80, color=(0,255,255)):
    for line in text.split("\n"):
        cv2.putText(frame, line, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    color, 2, cv2.LINE_AA)
        y += 26

# ================ TUTOR ACTIONS ================ #
def decide(emotion):
    e = emotion.lower()
    if e in ("sad","angry","fear"): return "show_hint"
    if e == "neutral": return "ask_question"
    if e == "happy": return "next_slide"
    return "none"

# ================ WEBCAM LOOP ================ #
cap = cv2.VideoCapture(0)
csv_file = open(CSV_PATH, "a", newline="")
writer = csv.writer(csv_file)
emotion_buf = deque(maxlen=10)
slide = 0
last = time.time()
interval = 2

print("Press ESC or Q to exit.")

while True:
    ok, frame = cap.read()
    if not ok: break

    try:
        res = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        emotion = res[0]['dominant_emotion']
        score = float(res[0]['emotion'][emotion])
    except:
        emotion, score = "neutral", 0.50

    emotion_buf.append(emotion)
    smooth = max(set(emotion_buf), key=emotion_buf.count)

    # ALWAYS show emotion
    cv2.putText(frame, f"Emotion: {smooth} ({round(score,2)})", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    action = "none"
    if time.time() - last >= interval:
        action = decide(smooth)
        last = time.time()

        # Apply action
        if action == "next_slide":
            slide = min(slide + 1, len(SLIDES)-1)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, "student_01", "python", smooth, round(score,2), action, ""])
        csv_file.flush()
        print(f"LOG: {now} | {smooth} | {action} | slide {slide+1}")

    # Always show slide
    draw_text(frame, SLIDES[slide], y=80, color=(0,255,255))

    # Show hint or quiz overlays
    if action == "show_hint":
        if slide < len(HINTS):
            draw_text(frame, HINTS[slide], y=220, color=(0,200,255))
    if action == "ask_question" and QUIZ_BLOCK:
        draw_text(frame, "QUIZ! Answer in terminal!", y=220, color=(0,255,0))
        print("\n📘 QUIZ!")
        print(QUIZ_BLOCK)
        ans = input("Your Answer (A/B/C/D): ").strip().upper()
        correct = QUIZ_BLOCK.split("Answer:")[-1].strip()[0]

        quiz_score = 1 if ans == correct else 0
        if quiz_score:
            print("✅ Correct!")
            slide = min(slide + 1, len(SLIDES)-1)
            action = "next_slide"
        else:
            print("❌ Incorrect! Showing hint.")
            action = "show_hint"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, "student_01", "python", smooth, round(score,2), action, quiz_score])
        csv_file.flush()

    cv2.imshow("Emotion AI Tutor", frame)
    k = cv2.waitKey(10)
    if k in (27, ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
csv_file.close()
