# 🚀 QUICKSTART GUIDE - FitTrack AI

Get up and running in **under 2 minutes** on any system!

---

## macOS / Linux

### One-Command Setup:

```bash
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
source setup_env.sh && \
python app.py
```

### Or Step-by-Step:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key and run
source setup_env.sh && python app.py
```

---

## Windows

### One-Command Setup:

```cmd
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && setup_env.bat && python app.py
```

### Or Step-by-Step:

```cmd
REM 1. Create virtual environment
python -m venv venv

REM 2. Activate it
venv\Scripts\activate

REM 3. Install dependencies
pip install -r requirements.txt

REM 4. Set API key and run
setup_env.bat
python app.py
```

---

## 🌐 Access the App

Once running, open your browser to:

**http://127.0.0.1:5000**

---

## 🎤 Enable AI Voice Coach

The Groq API key is **pre-configured** in the setup scripts!

**AI Coach automatically activates** when you run through `setup_env.sh` or `setup_env.bat`.

---

## ✅ Verify Setup

Check if everything is working:

```bash
# Check API key is set
echo $GROQ_API_KEY  # macOS/Linux
echo %GROQ_API_KEY%  # Windows

# Check AI Coach status (once app is running)
curl http://127.0.0.1:5000/ai_coach_status
```

---

## 📋 First Workout

1. **Grant Camera Permission** when prompted
2. **Select an exercise** (Squat recommended for first try)
3. **Set goals:** 10 reps, 3 sets
4. **Click "Start Workout"**
5. **Do your exercise** - AI will coach you in real-time!
6. **Click "Stop Workout"** - Get your performance report

---

## 🔧 Troubleshooting

### Camera Not Working
**macOS:** System Settings → Privacy & Security → Camera → Enable Terminal

**Windows:** Settings → Privacy → Camera → Allow apps

**Linux:** Grant camera permissions
```bash
sudo usermod -a -G video $USER
```

### Port 5000 Already in Use
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### AI Coach Not Responding
1. Check internet connection (API requires network)
2. Verify API key: Check if `setup_env.sh` or `setup_env.bat` was sourced
3. Look for errors in terminal logs

---

## 📊 Dashboard

View your progress at: **http://127.0.0.1:5000/dashboard**

- Weekly activity charts
- Exercise distribution
- Recent workout history
- Clear data button

---

## 🎯 What to Expect

### Real-Time Feedback Examples:

**Safety Warning (urgent):**
> "Knees too deep - protect your joints!"

**Milestone Encouragement:**
> "First rep! Focus on perfect form!"

**Technique Cue:**
> "Breathe in, push hips back!"

**Post-Workout Report:**
> "Solid squat session! Key strength: Good depth consistency. Area to improve: Knee alignment. Tip: Keep weight in heels."

---

## 🔐 Security Note

**⚠️ This repository includes the Groq API key for easy demo/hackathon setup.**

**For production use:**
1. Get your own API key at https://console.groq.com/keys
2. Update `setup_env.sh` and `setup_env.bat` with your key
3. Or set as environment variable in your system

---

## 📚 Documentation

- **README.md** - This file
- **SETUP_AI_COACH.md** - Detailed AI coach configuration
- **AI_COACH_IMPLEMENTATION.md** - Technical implementation details
- **AI_FEEDBACK_IMPROVEMENTS.md** - Latest enhancements

---

## 💻 Tech Stack

- **Backend:** Flask
- **AI:** Groq API (Llama 3.3 70B)
- **Pose:** MediaPipe
- **Voice:** pyttsx3
- **Database:** SQLite
- **Frontend:** Vanilla JS + Chart.js

---

**Now go train! Your AI coach is waiting! 💪**

