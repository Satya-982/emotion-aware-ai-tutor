import matplotlib
matplotlib.use("Agg")  # Avoid tkinter issues on Python 3.13

import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_PATH = r"C:\Users\Sahai\emotion-tutor\data\sessions.csv"

if not os.path.exists(CSV_PATH):
    print("❌ sessions.csv not found")
    exit()

df = pd.read_csv(CSV_PATH)
print("✅ Data Loaded!")
print(df.head())

# Remove rows without emotions
df = df.dropna(subset=["emotion"])

# ---------- Emotion Frequency ----------
plt.figure(figsize=(7,4))
df["emotion"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Emotion Frequency")
plt.xlabel("Emotion")
plt.ylabel("Count")
plt.savefig("1_emotion_frequency.png")
print("📊 Saved: 1_emotion_frequency.png")

# ---------- Tutor Actions ----------
plt.figure(figsize=(7,4))
df["action"].value_counts().plot(kind="bar", color="orange")
plt.title("Tutor Actions")
plt.xlabel("Action")
plt.ylabel("Count")
plt.savefig("2_tutor_actions.png")
print("📊 Saved: 2_tutor_actions.png")

# ---------- Engagement Timeline ----------
plt.figure(figsize=(10,4))
df["timestamp"] = pd.to_datetime(df["timestamp"])
plt.plot(df["timestamp"], df["emotion"], marker="o")
plt.title("Emotion Trend Over Time")
plt.xlabel("Time")
plt.ylabel("Emotion")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("3_emotion_trend.png")
print("📊 Saved: 3_emotion_trend.png")

# ---------- Quiz Performance ----------
if "quiz_score" in df.columns:
    plt.figure(figsize=(6,4))
    df["quiz_score"].value_counts().plot(kind="bar", color="green")
    plt.title("Quiz Performance")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.savefig("4_quiz_performance.png")
    print("📊 Saved: 4_quiz_performance.png")

# ---------- Hint Success Rate ----------
hint_df = df[df["action"] == "show_hint"]
if not hint_df.empty:
    success_rate = (df["quiz_score"].sum() / max(len(df), 1)) * 100
    print(f"✨ Learning Effectiveness: Hints improved performance by {success_rate:.2f}%")
else:
    print("ℹ️ No hint logs yet / Need more testing")
