# Setup AI Voice Coach Feature

## 🔑 Get Your Groq API Key

1. Visit **[Groq Console](https://console.groq.com/keys)**
2. Sign up for a free account
3. Generate a new API key
4. Copy the key (starts with `gsk_...`)

## 🚀 Configure the App

### **Option 1: Environment Variable (Recommended)**

```bash
# Set the API key for current session
export GROQ_API_KEY="your_groq_api_key_here"

# Then start the app
cd /Users/nishu/Documents/Clarkathon-2025
source venv/bin/activate
python app.py
```

### **Option 2: Permanent Setup (macOS/Linux)**

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Then reload:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

### **Option 3: For Testing Only**

Temporarily set the key in `app.py` line 60:

```python
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or "your_key_here"
```

⚠️ **Never commit API keys to git!**

## ✅ Verify It's Working

1. Start the app
2. Look for this in the logs:
   ```
   ✅ AI Coach with Groq LLM initialized successfully!
   ```

3. Open http://127.0.0.1:5000
4. See green "Voice Coach: ON" button
5. Start a workout and listen for voice feedback!

## 🔇 If AI Coach Doesn't Initialize

The app will still work perfectly - it just won't have voice coaching features. You'll see:

```
⚠️ GROQ_API_KEY environment variable not set
Continuing without AI coaching features
```

## 📚 More Info

- **Groq Documentation:** https://console.groq.com/docs
- **Free Tier:** Very generous limits
- **Fast Inference:** LPU-powered, sub-second responses

