# 🎓 Emotion-Aware Adaptive AI Tutor

A real-time AI tutoring system that **detects student emotions** through a webcam and **adapts its teaching style** accordingly — making learning more personalized, engaging, and effective.

---

## 🌟 Features

- 😊 **Real-Time Emotion Detection** — Detects emotions like happy, sad, angry, neutral, surprised using DeepFace
- 📷 **Live Webcam Feed** — Processes video frames using OpenCV in real time
- 🎯 **Adaptive Responses** — Tutor adjusts tone and content difficulty based on student's emotional state
- 🧠 **AI-Powered** — Combines computer vision with intelligent tutoring logic
- ⚡ **Low Latency** — Optimized for real-time performance

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Emotion Detection | DeepFace |
| Computer Vision | OpenCV |
| Backend | Python |
| AI/ML | Deep Learning (FER models) |

---

## 📁 Project Structure

```
emotion-aware-ai-tutor/
│
├── main.py                 # Entry point — webcam + emotion loop
├── tutor.py                # Adaptive tutoring logic
├── emotion_detector.py     # DeepFace integration
├── requirements.txt        # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Webcam
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Satya-982/emotion-aware-ai-tutor.git
cd emotion-aware-ai-tutor

# Install dependencies
pip install -r requirements.txt

# Run the tutor
python main.py
```

---

## 🧠 How It Works

```
Webcam Input → OpenCV Frame Capture → DeepFace Emotion Analysis
       ↓
Emotion Label (happy / sad / confused / neutral)
       ↓
Adaptive Tutor Response (encouragement / simplification / engagement boost)
```

1. **Webcam** captures live video frames
2. **DeepFace** analyzes facial expression every N frames
3. **Tutor engine** selects appropriate teaching response based on detected emotion
4. Student receives personalized guidance in real time

---

## 📸 Demo

> *(Add a screenshot or GIF of the emotion detection + tutor in action)*

---

## 🔮 Future Enhancements

- [ ] Subject-specific question banks
- [ ] Voice-based tutor responses (TTS)
- [ ] Session analytics dashboard
- [ ] Mobile support

---

## 🙋 Author

**Satya Marrivada**  
M.Tech AIML | [GitHub](https://github.com/Satya-982)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
