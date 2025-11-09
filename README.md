# FitTrack AI - AI-Powered Fitness Trainer

Real-time pose detection and AI voice coaching for your workouts using MediaPipe and Groq LLM.

## Features

- **Real-time Pose Detection** using Google MediaPipe
- **AI Voice Coach** powered by Groq's Llama 3.3 70B
- **3 Exercises:** Squats, Push-ups, Hammer Curls
- **Safety Warnings** for dangerous form
- **Workout Reports** with AI analysis
- **Dashboard** with progress tracking
- **SQLite Database** for persistent storage

---

## Quick Start (Any System)

### 1. Clone the Repository

```bash
git clone https://github.com/sharmi1601/Clarkathon-2025.git
cd Clarkathon-2025
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup API Key

**Create `api_key.txt` file** with your Groq API key:

```bash
echo "your_groq_api_key_here" > api_key.txt
```

**Get your free API key at:** https://console.groq.com/keys

*(Or use the example template: `cp api_key.txt.example api_key.txt` and edit it)*

### 5. Run the App

**Option A: Using setup script (macOS/Linux)**
```bash
source setup_env.sh && python app.py
```

**Option B: Windows**
```cmd
setup_env.bat && python app.py
```

**Option C: Direct run (if API key is in api_key.txt)**
```bash
python app.py
```

### 6. Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

## System Requirements

- Python 3.8+
- Webcam (for pose detection)
- macOS/Linux/Windows
- Microphone-enabled system (for voice feedback)

---

## Camera Permissions (macOS)

If camera doesn't work on Mac:

1. Go to **System Settings** → **Privacy & Security** → **Camera**
2. Enable **Terminal** or **Python**
3. Restart the app

---

## Architecture

```
Camera Feed → MediaPipe Pose (33 landmarks) → Angle Calculation
                                                      ↓
                                            Exercise Tracking
                                                      ↓
                                            Groq LLM Analysis
                                                      ↓
                                            Voice Feedback (TTS)
                                                      ↓
                                            SQLite Database
```

---

## API Key Configuration

### Easy Setup:
1. **Copy the template:**
   ```bash
   cp api_key.txt.example api_key.txt
   ```

2. **Add your key:**
   - Edit `api_key.txt` and replace with your actual key
   - Get free key at: https://console.groq.com/keys

3. **The setup scripts auto-load it!**
   - `setup_env.sh` and `setup_env.bat` automatically read from `api_key.txt`
   - No need to manually export environment variables

### Alternative Methods:
```bash
# Method 1: Direct environment variable (macOS/Linux)
export GROQ_API_KEY="your_key_here"

# Method 2: Direct environment variable (Windows)
set GROQ_API_KEY=your_key_here

# Method 3: Using .env file
echo 'export GROQ_API_KEY="your_key"' > .env
source .env
```

---

## Usage

### Start a Workout:
1. Select exercise (Squat/Push-up/Hammer Curl)
2. Set reps and sets goals
3. Click "Start Workout"
4. AI Coach will provide real-time feedback

### View Progress:
- Click "Dashboard" to see:
  - Total workouts
  - Weekly activity chart
  - Exercise distribution
  - Recent workout history

### AI Voice Coach:
- Toggle voice feedback with "Voice Coach: ON/OFF" button
- Real-time corrections for dangerous form
- Milestone encouragement
- Post-workout performance report

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Pose Detection** | MediaPipe (BlazePose) |
| **AI/LLM** | Groq (Llama 3.3 70B) |
| **Voice** | pyttsx3 / gTTS |
| **Database** | SQLite |
| **Frontend** | HTML/CSS/JavaScript |
| **Charts** | Chart.js |

---

## Project Structure

```
Clarkathon-2025/
├── app.py                      # Main Flask application
├── setup_env.sh               # Easy setup script
├── requirements.txt           # Python dependencies
├── db/
│   ├── workout_logger.py     # Database operations
│   └── workouts.db           # SQLite database
├── ai/
│   ├── groq_client.py        # Groq LLM integration
│   ├── voice_feedback.py     # Text-to-speech system
│   └── coach_coordinator.py  # AI coaching logic
├── exercises/
│   ├── squat.py
│   ├── push_up.py
│   └── hammer_curl.py
├── pose_estimation/
│   ├── estimation.py
│   └── angle_calculation.py
├── feedback/
│   ├── indicators.py
│   ├── layout.py
│   └── information.py
├── templates/
│   ├── index.html
│   └── dashboard.html
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## Troubleshooting

### Camera Not Working
- **macOS:** Grant camera permissions in System Settings
- **Linux:** Check `/dev/video0` permissions
- **Windows:** Allow camera access in Privacy settings

### AI Coach Not Working
- Verify GROQ_API_KEY is set: `echo $GROQ_API_KEY`
- Check internet connection (API requires network)
- View logs for error messages

### Voice Not Working
- Ensure audio output is enabled
- Check system volume
- pyttsx3 requires audio drivers

### Port 5000 Already in Use
```bash
lsof -ti:5000 | xargs kill  # macOS/Linux
```

---

## Credits

- **Pose Estimation:** Google MediaPipe
- **AI/LLM:** Groq (https://groq.com/)
- **Voice:** pyttsx3, gTTS

---

## License

See LICENSE file for details.

---

## Support

For issues or questions:
- Check the logs in terminal
- Review `SETUP_AI_COACH.md` for detailed AI setup
- Review `AI_COACH_IMPLEMENTATION.md` for technical details

---

**Built for Clarkathon 2025** 🏋️

