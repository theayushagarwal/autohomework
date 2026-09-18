"""
AutoCode — Examly & Monaco Editor Automation
Reads question screenshot/text -> Solves with Gemini -> Auto-pastes code into Examly IDE.

TARGET:
    vitvellore312.examly.io/ide (Examly / NeoColab Monaco Editor)

USAGE:
    # 1. Standard mode (launches Chrome, opens Examly IDE, pastes code):
    python gemini_autocode.py question.png

    # 2. Attach mode (pastes directly into your already OPEN and LOGGED-IN Chrome browser):
    python gemini_autocode.py question.png --attach

    # 3. Specify programming language (default: python):
    python gemini_autocode.py question.png --lang python
    python gemini_autocode.py question.png --lang cpp
    python gemini_autocode.py question.png --lang java

    # 4. Text question instead of image:
    python gemini_autocode.py question.txt
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ========================= CONFIG =========================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
DEFAULT_MODEL = "gemini-2.5-flash"

# Default Target URL for Examly
DEFAULT_URL = "https://vitvellore312.examly.io/ide"

# Supported image file extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
# ============================================================


def clean_markdown_fences(code: str) -> str:
    """Strip markdown code fences (```python ... ```) if Gemini returns them."""
    code = code.strip()
    # Remove leading ```... and trailing ```
    lines = code.split("\n")
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def get_solution_from_gemini(question_source: str, language: str = "python") -> str:
    """Send image or text problem statement to Gemini and receive clean solution code."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError(
            "Gemini API key is not set! Set GEMINI_API_KEY in .env, as an environment "
            "variable, or directly in gemini_autocode.py."
        )

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(DEFAULT_MODEL)

    prompt = (
        f"You are a competitive programming assistant. Solve the coding problem provided.\n"
        f"Target Programming Language: {language.upper()}.\n\n"
        f"STRICT REQUIREMENTS:\n"
        f"1. Write complete, production-ready, highly optimized code in {language}.\n"
        f"2. Read input from standard input (stdin / input()) and write output to standard output (stdout / print()).\n"
        f"3. Handle all edge cases, constraints, and time limits.\n"
        f"4. Return ONLY executable {language} code. Absolutely DO NOT include explanations, "
        f"markdown formatting, code fences (no ```), or any commentary."
    )

    path = Path(question_source)
    if path.is_file():
        suffix = path.suffix.lower()
        if suffix in IMAGE_EXTENSIONS:
            # Multimodal image input
            mime_map = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
            }
            mime_type = mime_map.get(suffix, "image/png")
            image_bytes = path.read_bytes()
            print(f"[*] Sending screenshot ({path.name}) to Gemini ({DEFAULT_MODEL})...")
            response = model.generate_content(
                [{"mime_type": mime_type, "data": image_bytes}, prompt]
            )
        else:
            # Text file input
            problem_text = path.read_text(encoding="utf-8")
            print(f"[*] Sending question text from file ({path.name}) to Gemini...")
            response = model.generate_content([problem_text, prompt])
    else:
        # Direct text prompt
        print("[*] Sending problem text prompt to Gemini...")
        response = model.generate_content([question_source, prompt])

    code = clean_markdown_fences(response.text)
    return code


def paste_into_monaco_editor(driver, code: str) -> bool:
    """
    Pastes code into Examly's Monaco Editor using multiple strategies:
    1. Direct Monaco JS API (bypasses paste-blocking, instant, no keystroke lag)
    2. Clipboard paste (ActionChains Ctrl+A + Ctrl+V)
    3. Standard input fallback
    """
    # Neutralize any anti-paste listeners on the webpage
    try:
        driver.execute_script("""
            window.onpaste = null;
            document.onpaste = null;
            if (document.body) document.body.onpaste = null;
            window.addEventListener('paste', function(e) {
                e.stopImmediatePropagation();
            }, true);
        """)
    except Exception:
        pass

    # Strategy 1: Direct Monaco Editor API injection
    try:
        injected = driver.execute_script("""
            var newCode = arguments[0];
            if (window.monaco && window.monaco.editor) {
                var editors = window.monaco.editor.getEditors();
                if (editors && editors.length > 0) {
                    editors[0].setValue(newCode);
                    return true;
                }
                var models = window.monaco.editor.getModels();
                if (models && models.length > 0) {
                    models[0].setValue(newCode);
                    return true;
                }
            }
            return false;
        """, code)

        if injected:
            print("[OK] Successfully injected code via Monaco Editor API (Instant & Clean)!")
            return True
    except Exception as e:
        print(f"[*] Monaco JS API attempt: {e}. Trying clipboard fallback...")

    # Strategy 2: Focus Monaco Editor & Paste from Clipboard (Ctrl+A -> Ctrl+V)
    try:
        pyperclip.copy(code)

        editor_elem = None
        selectors = [
            ".monaco-editor",
            ".monaco-editor .view-lines",
            ".monaco-editor textarea.inputarea",
            "div[data-keybinding-context]",
            "textarea"
        ]

        for sel in selectors:
            try:
                editor_elem = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if editor_elem and editor_elem.is_displayed():
                    break
            except Exception:
                continue

        if editor_elem:
            actions = ActionChains(driver)
            actions.move_to_element(editor_elem).click().perform()
            time.sleep(0.3)

            # Select all and delete placeholder comment (# Enter your code here)
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            actions.send_keys(Keys.BACKSPACE).perform()
            time.sleep(0.1)

            # Paste code from clipboard
            actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
            print("[OK] Successfully pasted code using clipboard (Ctrl+V)!")
            return True
    except Exception as e:
        print(f"[*] Clipboard paste attempt: {e}. Trying textarea fallback...")

    # Strategy 3: Basic Textarea
    try:
        field = driver.find_element(By.CSS_SELECTOR, "textarea")
        field.click()
        field.clear()
        field.send_keys(code)
        print("[OK] Typed code into textarea.")
        return True
    except Exception as e:
        print(f"[ERR] All paste strategies failed: {e}")
        return False


def click_run_or_submit_button(driver, custom_selector: str = None) -> bool:
    """Attempts to find and click the Run or Submit button."""
    if custom_selector:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, custom_selector))
            )
            btn.click()
            print(f"[OK] Clicked custom button: {custom_selector}")
            return True
        except Exception as e:
            print(f"[-] Could not click custom button: {e}")

    # Search for common Examly button labels
    candidate_xpaths = [
        "//button[contains(translate(text(), 'RUN', 'run'), 'run')]",
        "//button[contains(translate(text(), 'COMPILE', 'compile'), 'compile')]",
        "//button[contains(translate(text(), 'SUBMIT', 'submit'), 'submit')]",
        "//button[contains(translate(text(), 'EXECUTE', 'execute'), 'execute')]",
    ]

    for xpath in candidate_xpaths:
        try:
            btn = driver.find_element(By.XPATH, xpath)
            if btn.is_displayed():
                btn.click()
                print(f"[OK] Clicked button via: {xpath}")
                return True
        except Exception:
            continue

    print("[*] No Run/Submit button automatically clicked.")
    return False


def automate_examly(
    url: str,
    code: str,
    attach: bool = False,
    port: int = 9222,
    auto_run: bool = False,
    submit_selector: str = None,
    keep_open: bool = True
):
    """Automates pasting the code into Examly."""
    options = webdriver.ChromeOptions()

    if attach:
        print(f"[*] Attaching to existing Chrome browser running on port {port}...")
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(options=options)
    else:
        print(f"[*] Launching Chrome browser...")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # Prevent auto-closing when script finishes
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(url)

    try:
        # Wait for Monaco Editor to appear
        print("[*] Waiting for Monaco Editor on Examly page...")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
            )
        except Exception:
            print("\n[!] Monaco Editor not detected immediately.")
            print("[!] If you need to log in to Examly, please log in now in the browser.")
            input("Press [ENTER] here once the IDE code editor is visible on your screen...")

        time.sleep(1)  # Brief pause for Monaco editor scripts to finish initialization

        # Paste the code
        success = paste_into_monaco_editor(driver, code)

        if success and auto_run:
            time.sleep(0.5)
            click_run_or_submit_button(driver, submit_selector)

        print("\n[✓] Automation completed successfully!")
    finally:
        if not keep_open and not attach:
            time.sleep(5)
            driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Examly / NeoColab Code Auto-Paster powered by Gemini"
    )
    parser.add_argument(
        "question",
        help="Path to problem screenshot (PNG/JPG), text file (.txt), or direct text"
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Target Examly URL (default: {DEFAULT_URL})"
    )
    parser.add_argument(
        "--lang",
        default="python",
        help="Programming language for solution (default: python, options: cpp, java, c, etc.)"
    )
    parser.add_argument(
        "--attach",
        action="store_true",
        help="Attach to an already running Chrome browser with debugging port 9222"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9222,
        help="Remote debugging port for Chrome (default: 9222)"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Auto-click the Run / Compile button after pasting"
    )
    parser.add_argument(
        "--submit-selector",
        default=None,
        help="CSS selector for custom Run / Submit button"
    )

    args = parser.parse_args()

    # Step 1: Generate Code with Gemini
    code = get_solution_from_gemini(args.question, language=args.lang)

    print("\n" + "=" * 30 + " GENERATED CODE " + "=" * 30)
    print(code)
    print("=" * 76 + "\n")

    # Step 2: Automate Pasting into Examly
    automate_examly(
        url=args.url,
        code=code,
        attach=args.attach,
        port=args.port,
        auto_run=args.run,
        submit_selector=args.submit_selector,
    )


if __name__ == "__main__":
    main()
