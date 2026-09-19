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
# Run with interactive variant selection:
python full_auto_neocolab.py

# Or specify a code variant directly:
python full_auto_neocolab.py --variant 2   # Style A (different variables, loops & test data)
python full_auto_neocolab.py --variant 3   # Style B (modular logic & distinct expressions)
```

### What Happens Next:
1. Google Chrome opens automatically with a dedicated profile.
2. Log into your NeoColab account in that Chrome browser once.
3. In your terminal, choose your code variant (`1` for Style A, `2` for Style B) and automation mode (`1` for Fully Automatic).
4. The bot will automatically:
   - Find and activate the Single File Compiler tab
   - Ensure Python (3.8) is selected
   - Inject the selected variant solution directly into the editor
   - Take the code screenshot
   - Click "Compile & Run"
   - Take the output screenshot
   - Repeat hands-free for all 30 questions!
5. All 60 screenshots will be neatly organized in the `lab_screenshots/` folder.

---

## 📄 Generate Complete Lab Manual & Watermarked PDF

After screenshots are taken (or using the pre-bundled screenshots):

### Option A: Run Locally in Terminal
Generate both the formatted Microsoft Word document (`.docx`) and the watermarked PDF (`.pdf`) with your custom name, color theme, and font:

```bash
# Generate for Ayush (Classic Academic Navy + Arial):
python build_submission_document.py --name "Ayush Agarwal"

# Generate for a friend (Automatic unique theme, font, and watermark angle by default!):
python build_submission_document.py --name "Rahul Verma"

# Or pick specific themes and typography:
python build_submission_document.py --name "Rohan Sharma" --theme emerald --font calibri
python build_submission_document.py --name "Priya Patel" --theme burgundy --font georgia
python build_submission_document.py --name "Aditya Rao" --theme slate --font segoe
```

**Available Visual Themes**:
- `navy` (Classic Academic Deep Navy - Ayush's baseline)
- `emerald` (Forest Green & Mint)
- `burgundy` (Crimson Wine & Rose)
- `slate` (Modern Tech Charcoal & Slate)
- `indigo` (Royal Indigo & Lavender)
- `amber` (Warm Amber Bronze)

**Available Fonts**: `calibri`, `times` (Times New Roman), `segoe` (Segoe UI), `georgia`, `arial`.

---

### Option B: 100% Automated on GitHub (Zero Setup for Friends!)
No Python or Microsoft Office required! Anyone who has access to the GitHub repository can generate their custom manual in the cloud:

1. Go to the repository on GitHub (`https://github.com/theayushagarwal/autohomework`).
2. Click on the **Actions** tab at the top.
3. Select **Build Lab Manual & Watermarked PDF** from the left sidebar.
4. Click **Run workflow**:
   - Type your **Name** (e.g. `Rahul Verma`)
   - Select your favorite **Theme** (`auto`, `emerald`, `burgundy`, `slate`, `indigo`, etc.)
   - Select your preferred **Font** (`auto`, `calibri`, `times`, `georgia`, `segoe`)
   - Select your **Header Style** (`auto`, `classic`, `formal`, `modern`, `minimal`)
5. Click the green **Run workflow** button.
6. In under 1 minute, the build will finish. Click the completed run and download the **Python_Lab_Manual_<Your_Name>** ZIP artifact containing your ready-to-submit PDF and Word documents!

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

1. **Ace Editor API Injection**: Instead of slow `.send_keys()` which messes up indentation and triggers auto-closing brackets, it accesses Examly's Ace instance directly:
   ```javascript
   var ed = document.getElementById('programming-answer-ttAnswerEditor1') || document.querySelector('.ace_editor');
   ed.env.editor.setValue(code, 1);
   ```
2. **Listener Disarming**: Disarms `onpaste` event blockers on `window` and `document` so clipboard pasting works smoothly.
3. **Editor Auto-Reset & Scroll**: Automatically clears previous output and scrolls the code view to line 1 (`ed.env.editor.scrollToLine(1)`) so every screenshot is crisp and centered.
