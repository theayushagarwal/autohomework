# NeoColab Python Lab Automation (Ex 2 to Ex 8)

Automated Python lab runner for NeoColab / Examly (`vitvellore312.examly.io/ide`).
Automatically injects authentic student code, compiles, runs, and captures code and output screenshots for all **29 individual lab questions**.

---

## 🚀 Quick Start (Zero API Key Needed!)

All 29 solutions are pre-packaged in `solutions/` with zero `#` comments. Anyone can clone and run it directly!

### Step 1: Clone & Navigate
```bash
git clone <your-repo-url>
cd <repo-folder>
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Bot
```bash
python full_auto_neocolab.py
```

### What Happens Next:
1. Google Chrome opens automatically with a dedicated profile.
2. Log into your NeoColab account in that Chrome browser once.
3. In your terminal, type `1` (Fully Automatic) and press Enter.
4. The bot will automatically:
   - Find and activate the Single File Compiler tab
   - Ensure Python (3.8) is selected
   - Inject the solution directly into the editor
   - Take the code screenshot
   - Click "Compile & Run"
   - Take the output screenshot
   - Repeat hands-free for all 29 questions!
5. All 58 screenshots will be neatly organized in the `lab_screenshots/` folder.

---

---

## 2. How to Run

### Method A: Connect to your Existing Logged-in Chrome (Recommended & Safest!)
Since Examly requires student login / SSO:

1. Double-click `start_chrome_debug.bat` (or launch Chrome with `--remote-debugging-port=9222`).
2. Log into `https://vitvellore312.examly.io/ide` and open your coding question/editor tab.
3. Take a screenshot of the question and save it (e.g. `question.png`).
4. Run:
   ```bash
   python gemini_autocode.py question.png --attach
   ```
   The script connects to your active tab and injects the solution into the editor in under 1 second!

---

### Method B: Standalone Chrome Launch
If you want the script to launch a fresh Chrome window automatically:
```bash
python gemini_autocode.py question.png
```
- Chrome will open and navigate to `https://vitvellore312.examly.io/ide`.
- If it asks you to log in, log in and press Enter in the terminal to continue.

---

## 3. Extra Options & Flags

| Flag | Description | Example |
|---|---|---|
| `--lang` | Target programming language (default: `python`) | `python gemini_autocode.py q.png --lang cpp` |
| `--attach` | Attach to Chrome on port 9222 | `python gemini_autocode.py q.png --attach` |
| `--run` | Automatically click Run/Compile after pasting | `python gemini_autocode.py q.png --run` |
| `--url` | Custom URL if different from default | `python gemini_autocode.py q.png --url https://...` |

---

## 4. How It Bypasses Examly's Quirks

1. **Monaco API Injection**: Instead of slow `.send_keys()` which messes up indentation and triggers auto-closing brackets, it runs:
   ```javascript
   window.monaco.editor.getModels()[0].setValue(code);
   ```
2. **Listener Disarming**: Disarms `onpaste` event blockers on `window` and `document` so clipboard pasting works smoothly.
3. **Clipboard Fallback**: Uses `pyperclip` and Selenium ActionChains (`Ctrl+A` -> `Backspace` -> `Ctrl+V`) if the JS API is unreachable.
