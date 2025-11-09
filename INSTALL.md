# 📦 Installation Guide - FitTrack AI

Complete step-by-step installation instructions for any system.

---

## Prerequisites

- **Python 3.8+** installed
- **Git** installed
- **Webcam** connected
- **Internet connection** (for AI features)

---

## Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sharmi1601/Clarkathon-2025.git
cd Clarkathon-2025
```

### 2️⃣ Create Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**
- Flask 3.0.0
- opencv-python 4.8.1.78
- mediapipe 0.10.8
- numpy 1.24.3
- groq 0.33.0
- pyttsx3 2.99
- gTTS 2.5.4
- pygame 2.6.1

### 4️⃣ Configure API Key

**Option A: Using api_key.txt (Recommended)**

```bash
# Copy template
cp api_key.txt.example api_key.txt

# Edit api_key.txt and add your key
# Get free key at: https://console.groq.com/keys
nano api_key.txt  # or use any text editor
```

**Option B: Set environment variable directly**

macOS/Linux:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Windows:
```cmd
set GROQ_API_KEY=your_groq_api_key_here
```

**Option C: Create .env file**

```bash
echo 'export GROQ_API_KEY="your_key_here"' > .env
```

### 5️⃣ Run the Application

**Easy Method (Uses setup scripts):**

macOS/Linux:
```bash
source setup_env.sh && python app.py
```

Windows:
```cmd
setup_env.bat && python app.py
```

**Direct Method:**
```bash
python app.py
```

### 6️⃣ Access the App

Open browser: **http://127.0.0.1:5000**

---

## Verification

### Check Installation:

```bash
# Verify Python version
python --version  # Should be 3.8+

# Verify packages installed
pip list | grep -E "Flask|opencv|mediapipe|groq"

# Check if API key is set (after sourcing setup script)
echo $GROQ_API_KEY  # macOS/Linux
echo %GROQ_API_KEY%  # Windows
```

### Test the App:

1. Navigate to http://127.0.0.1:5000
2. Check AI Coach status at http://127.0.0.1:5000/ai_coach_status
3. Expected response:
```json
{
  "available": true,
  "model": "llama-3.3-70b-versatile",
  "voice_enabled": true
}
```

---

## Platform-Specific Setup

### macOS

**1. Install Python 3:**
```bash
brew install python3
```

**2. Grant Camera Permissions:**
- System Settings → Privacy & Security → Camera
- Enable Terminal (or iTerm2)

**3. Run the app:**
```bash
source setup_env.sh && python app.py
```

### Linux (Ubuntu/Debian)

**1. Install dependencies:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install python3-opencv portaudio19-dev
```

**2. Grant camera access:**
```bash
sudo usermod -a -G video $USER
```

**3. Run the app:**
```bash
source setup_env.sh && python app.py
```

### Windows

**1. Install Python:**
- Download from python.org
- Check "Add Python to PATH"

**2. Install Visual C++ Build Tools** (if needed):
- Download from Microsoft

**3. Run the app:**
```cmd
setup_env.bat && python app.py
```

---

## Troubleshooting

### Camera Issues

**macOS:**
- Settings → Privacy & Security → Camera → Enable Terminal
- Restart Terminal after enabling

**Linux:**
```bash
# Check camera device
ls /dev/video*

# Test camera
python -c "import cv2; print(cv2.VideoCapture(0).read())"
```

**Windows:**
- Settings → Privacy → Camera → Allow apps
- Check Device Manager for camera

### API Key Not Working

```bash
# Verify file exists
ls -la api_key.txt

# Check content
cat api_key.txt  # Should show your API key

# Manually set and test
export GROQ_API_KEY="your_key"
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

### Package Installation Errors

**On macOS with M1/M2 chip:**
```bash
# Install Rosetta if needed
softwareupdate --install-rosetta

# Use architecture-specific install
arch -arm64 pip install -r requirements.txt
```

**On Linux with missing dependencies:**
```bash
sudo apt install python3-dev libportaudio2 libasound2-dev
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**On Windows with build errors:**
```
# Install Microsoft C++ Build Tools
# Then retry installation
```

### Port 5000 Already in Use

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill
```

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Locked Error

```bash
# Remove lock
rm db/workouts.db-journal

# Or reset database
rm db/workouts.db
```

---

## Database Setup

The SQLite database is created automatically on first run. Location: `db/workouts.db`

**Schema:**
- workouts table: id, date, exercise_type, sets, reps, duration_seconds, created_at

**To reset database:**
```bash
rm db/workouts.db
# Restart app - database will be recreated
```

---

## File Structure After Installation

```
Clarkathon-2025/
├── venv/                    # Virtual environment (created)
├── db/
│   └── workouts.db         # Database (created on first run)
├── api_key.txt             # Your API key (you create this)
├── api_key.txt.example     # Template
├── setup_env.sh            # Setup script (macOS/Linux)
├── setup_env.bat           # Setup script (Windows)
└── ... (rest of project files)
```

---

## Next Steps

1. **Grant camera permissions** (platform-specific)
2. **Test with first workout**
   - Select Squat exercise
   - Set 10 reps, 1 set
   - Click "Start Workout"
3. **Check AI Coach** - Voice feedback should work
4. **View Dashboard** - See your workout logged

---

## Get Help

- **Documentation:** See README.md for full features
- **Quick Start:** See QUICKSTART.md for 2-minute setup
- **AI Setup:** See SETUP_AI_COACH.md for detailed AI configuration

---

**Ready to start training! 💪**

