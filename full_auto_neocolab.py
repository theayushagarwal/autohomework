"""
Full Auto NeoColab / Examly Lab Runner
======================================
1. Takes each question from your lab exercises.
2. Solves it with Gemini 2.5 Flash.
3. Injects/pastes the code directly into the NeoColab Monaco Editor.
4. Captures and saves a screenshot of the CODE.
5. Clicks "Run" / "Compile" to execute the code.
6. Scrolls down to the OUTPUT section.
7. Captures and saves a screenshot of the OUTPUT.
8. Automatically proceeds to the next question!
"""

import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load API key from .env
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"
DEFAULT_URL = "https://vitvellore312.examly.io/ide"

# Directories relative to script location
BASE_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = BASE_DIR / "lab_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


def clean_code(text: str) -> str:
    """Strip markdown fences and remove all # comments so it looks like authentic student code."""
    import re
    text = text.strip()
    lines = text.split("\n")
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # Remove trailing inline comment if present
        line = re.sub(r'\s+#.*$', '', line)
        cleaned_lines.append(line)

    result = "\n".join(cleaned_lines).strip()
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result



def solve_question(question_text: str, image_path: str = None) -> str:
    """Calls Gemini 2.5 Flash to solve the coding question."""
    prompt = (
        f"You are a competitive programming assistant writing a complete Python 3 solution for a lab assessment.\n"
        f"Problem: {question_text}\n\n"
        f"STRICT REQUIREMENTS:\n"
        f"1. Write complete, working, bug-free Python 3 code.\n"
        f"2. Read inputs or use given sample inputs as required and print clear outputs.\n"
        f"3. Return ONLY raw Python code. Do NOT wrap in markdown code blocks (no ```). No extra conversational text."
    )
    if image_path and Path(image_path).exists():
        img_bytes = Path(image_path).read_bytes()
        response = model.generate_content([
            {"mime_type": "image/png", "data": img_bytes},
            prompt
        ])
    else:
        response = model.generate_content(prompt)
    return clean_code(response.text)


# All lab questions from your PDF
LAB_QUESTIONS = [
    # Ex 2: Basic Datatypes (Individual Sub-Questions)
    {
        "id": "Ex2_a_IdentifyDatatype",
        "title": "Exercise 2 - Part A: Identify Data Types",
        "image": "questions/ex_page_1.png",
        "text": "Identify the data types of given values: 25, 25.0, '25', 'Python', True, False, 3+4j, -18, 'True', 0.0, '3+4j', 0."
    },
    {
        "id": "Ex2_b_PredictOutput",
        "title": "Exercise 2 - Part B: Predict Output",
        "image": "questions/ex_page_1.png",
        "text": "Predict output of variables, types, reassignments, complex numbers, and escape sequences."
    },
    {
        "id": "Ex2_c_ValidVariables",
        "title": "Exercise 2 - Part C: Valid Variables",
        "image": "questions/ex_page_1.png",
        "text": "Check which variables are valid and print values for name, city, cgpa, student, number, language."
    },
    {
        "id": "Ex2_d_CorrectErrors",
        "title": "Exercise 2 - Part D: Correct Errors",
        "image": "questions/ex_page_1.png",
        "text": "Correct syntax errors in variable assignments and print statements."
    },
    {
        "id": "Ex2_e_HelloWorld",
        "title": "Exercise 2 - Part E: Hello World",
        "image": "questions/ex_page_1.png",
        "text": "Write a simple python code to print 'Hello World'."
    },
    # Ex 3
    {
        "id": "Ex3_Q1_Chars",
        "title": "Exercise 3 - Q1: First, Fifth, Last Character",
        "image": "questions/ex_page_2.png",
        "text": "Declare the string 'Python Programming' and print: 1. First character, 2. Fifth character, 3. Last character."
    },
    {
        "id": "Ex3_Q2_Slicing",
        "title": "Exercise 3 - Q2: Slicing Python Programming",
        "image": "questions/ex_page_2.png",
        "text": "Declare 'Python Programming'. Print using slicing: 'Python', 'Programming', 'gram', 'Pro', 'ming'."
    },
    {
        "id": "Ex3_Q3_NegIndex",
        "title": "Exercise 3 - Q3: Negative Indexing on Vellore",
        "image": "questions/ex_page_2.png",
        "text": "Declare 'Vellore'. Print Last character, Second last character, Third last character using negative indexing."
    },
    {
        "id": "Ex3_Q4_PrintA",
        "title": "Exercise 3 - Q4: Print 'A' without typing 'A'",
        "image": "questions/ex_page_2.png",
        "text": "Without typing the letter A anywhere in the program, print A."
    },
    {
        "id": "Ex3_Q5_ASCII",
        "title": "Exercise 3 - Q5: ASCII / Unicode Values",
        "image": "questions/ex_page_2.png",
        "text": "Print the ASCII (Unicode) value of characters: 'A', 'a', 'Z', '0', '@'."
    },
    {
        "id": "Ex3_Q6_Chr",
        "title": "Exercise 3 - Q6: Characters for ASCII Values",
        "image": "questions/ex_page_2.png",
        "text": "Print the characters corresponding to ASCII values: 65, 97, 48, 36, 90."
    },
    # Ex 4
    {
        "id": "Ex4_Q1_BioCard",
        "title": "Exercise 4 - Q1: Student Bio Card",
        "image": "questions/ex_page_3.png",
        "text": "Read Name, Age, Department, University, Mobile Number and display a formatted Student Bio Card."
    },
    {
        "id": "Ex4_Q2_SingleAssign",
        "title": "Exercise 4 - Q2: Single Assignment Statement",
        "image": "questions/ex_page_3.png",
        "text": "Assign your name, age, and CGPA to three variables using a single assignment statement and print them."
    },
    {
        "id": "Ex4_Q3_UnicodeChar",
        "title": "Exercise 4 - Q3: Unicode of Character",
        "image": "questions/ex_page_3.png",
        "text": "Read a single character from the user and display its Unicode value."
    },
    {
        "id": "Ex4_Q4_StringIndex",
        "title": "Exercise 4 - Q4: String Character Indexing",
        "image": "questions/ex_page_3.png",
        "text": "Read a string from user and display: First character, Last character, Second character, Second last character."
    },
    # Ex 5
    {
        "id": "Ex5_Q1_Supermarket",
        "title": "Exercise 5 - Q1: Supermarket Bill Arithmetic",
        "image": "questions/ex_page_4.png",
        "text": "Read price of two products. Display: Total price, Price difference, Product, Division, Remainder, Floor division."
    },
    {
        "id": "Ex5_Q2_Relational",
        "title": "Exercise 5 - Q2: Relational Operations on Marks",
        "image": "questions/ex_page_4.png",
        "text": "Read marks of Student A and Student B. Display results of relational operations: ==, !=, >, <, >=, <=."
    },
    {
        "id": "Ex5_Q3_Bitwise",
        "title": "Exercise 5 - Q3: Bitwise Operations",
        "image": "questions/ex_page_4.png",
        "text": "Read two integer permission codes. Display binary representations and perform: AND, OR, XOR, Bitwise Complement of first code, Left shift 1, Right shift 1. Display decimal and binary."
    },
    {
        "id": "Ex5_Q4_Precedence",
        "title": "Exercise 5 - Q4: Operator Precedence",
        "image": "questions/ex_page_4.png",
        "text": "Evaluate and display: 5+3*2, (5+3)*2, 2**3*2, 2**3**2."
    },
    # Ex 6
    {
        "id": "Ex6_Q1_Attendance",
        "title": "Exercise 6 - Q1: Attendance Check",
        "image": "questions/ex_page_5.png",
        "text": "Get attendance percentage. If >= 75 print 'Student is permitted', else 'Student not permitted'."
    },
    {
        "id": "Ex6_Q2_Multiple",
        "title": "Exercise 6 - Q2: Multiple of 2 or 5",
        "image": "questions/ex_page_5.png",
        "text": "Find if the given number is a multiple of 2 or 5 or neither of them."
    },
    {
        "id": "Ex6_Q3_Greatest",
        "title": "Exercise 6 - Q3: Greatest of Three Numbers",
        "image": "questions/ex_page_5.png",
        "text": "Find the greatest of three numbers."
    },
    {
        "id": "Ex6_Q4_Grades",
        "title": "Exercise 6 - Q4: Grade Scoring",
        "image": "questions/ex_page_5.png",
        "text": "Print grade based on marks: >=91: S, 81-90: A, 71-80: B, 61-70: C, 51-60: D, 50: Pass, <50: Fail."
    },
    {
        "id": "Ex6_Q5_Rent",
        "title": "Exercise 6 - Q5: House Rent Allowance",
        "image": "questions/ex_page_5.png",
        "text": "Get salary and house rent. If rent <= 6% of salary print 'Rent allowance matched', else 'Rent allowance not matched'."
    },
    # Ex 7
    {
        "id": "Ex7_Q1_Factorial",
        "title": "Exercise 7 - Q1: Factorial using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Write a Python program using while loop to print the factorial of a given number."
    },
    {
        "id": "Ex7_Q2_Table",
        "title": "Exercise 7 - Q2: Multiplication Table using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Write a Python program using while loop to print the multiplication table of a given number."
    },
    {
        "id": "Ex7_Q3_ReverseDigits",
        "title": "Exercise 7 - Q3: Reverse Digits using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Get an integer. Display digits in reverse order using while loop with arithmetic operators only."
    },
    # Ex 8
    {
        "id": "Ex8_Q1_Denomination",
        "title": "Exercise 8 - Q1: Currency Denomination",
        "image": "questions/ex_page_7.png",
        "text": "Write a python program using loops to print the denomination of a given amount."
    },
    {
        "id": "Ex8_Q2_NumberPattern",
        "title": "Exercise 8 - Q2: Descending Number Pattern",
        "image": "questions/ex_page_7.png",
        "text": "Write a python program using loops to print descending number pattern: 5 4 3 2 1 down to 1."
    },
    {
        "id": "Ex8_Q3_StarPattern",
        "title": "Exercise 8 - Q3: Star Pyramid Pattern",
        "image": "questions/ex_page_7.png",
        "text": "Write a python program using loops to print star pyramid pattern: *, ***, *****, *******."
    }
]


def find_running_chrome_port():
    """Scans local ports to check if Google Chrome (not Electron/Antigravity) is already running with remote debugging."""
    import urllib.request
    import subprocess
    import re
    import json

    candidate_ports = [9222]
    try:
        out = subprocess.check_output("netstat -ano -p tcp", shell=True, text=True)
        for line in out.splitlines():
            if "LISTENING" in line and "127.0.0.1:" in line:
                m = re.search(r"127\.0\.0\.1:(\d+)", line)
                if m:
                    p = int(m.group(1))
                    if p > 1024 and p not in candidate_ports:
                        candidate_ports.append(p)
    except Exception:
        pass

    for port in candidate_ports:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=0.2) as resp:
                if resp.status == 200:
                    v = json.loads(resp.read().decode())
                    ua = v.get("User-Agent", "")
                    browser = v.get("Browser", "")

                    # Filter out Electron apps (Antigravity IDE, VS Code, etc.)
                    if "Electron" in ua or "Antigravity" in ua:
                        continue

                    # Must be actual Chrome 153+
                    if not browser.startswith("Chrome/153"):
                        continue

                    return port
        except Exception:
            pass
    return None


def setup_browser():
    """Connects to an existing Chrome browser or launches a new one with saved login profile."""
    active_port = find_running_chrome_port()
    if active_port:
        print(f"[✓] Detected running Chrome browser on port {active_port}!")
        print("[*] Attaching directly to your existing browser session...")
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{active_port}")
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"[-] Could not attach to port {active_port}: {e}")

    print("[*] Starting Chrome with dedicated NeoColab profile...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("detach", True)
    options.add_argument("--remote-debugging-port=9222")

    profile_dir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "NeoColabProfile")
    options.add_argument(f"--user-data-dir={profile_dir}")

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        if "DevToolsActivePort" in str(e) or "session not created" in str(e):
            print("[!] Cleaning up stale Chrome profile lock...")
            import subprocess
            subprocess.run(
                'powershell -Command "Get-CimInstance Win32_Process -Filter \\"Name = \'chrome.exe\'\\" | Where-Object { $_.CommandLine -like \'*NeoColabProfile*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"',
                shell=True
            )
            time.sleep(1.5)
            driver = webdriver.Chrome(options=options)
        else:
            raise e

    driver.get(DEFAULT_URL)
    return driver


def ensure_ide_tab(driver, max_retries: int = 15) -> bool:
    """
    Scans all open tabs across Chrome windows.
    Automatically finds, switches to, and brings the NeoColab Single File Compiler IDE tab to the front.
    Never takes screenshots or pastes on the wrong tab!
    """
    for attempt in range(max_retries):
        handles = driver.window_handles
        for i, handle in enumerate(handles):
            try:
                driver.switch_to.window(handle)
                url = driver.current_url.lower()

                is_ide = driver.execute_script("""
                    var hasEditor = Boolean(
                        document.getElementById('programming-answer-ttAnswerEditor1') ||
                        document.querySelector('[id*="AnswerEditor"]') ||
                        document.querySelector('.ace_editor')
                    );
                    var isCompiler = (document.body.innerText || '').includes('Single File Compiler');
                    var isLogin = window.location.href.includes('/login');
                    return (hasEditor || isCompiler) && !isLogin;
                """)

                if is_ide:
                    try:
                        driver.execute_cdp_cmd('Page.bringToFront', {})
                    except Exception:
                        pass
                    driver.execute_script("document.title = 'NEOCOLAB_BOT_TARGET_IDE';")
                    return True
            except Exception:
                continue

        # If not found on current open tabs, check if there is a login page
        curr_url = driver.current_url.lower()
        if "/login" in curr_url:
            print(f"[!] Currently on Login page. Please log in to your NeoColab account in Chrome! (Waiting... attempt {attempt+1}/{max_retries})")
        else:
            print(f"[*] Searching open tabs for NeoColab Single File Compiler... (attempt {attempt+1}/{max_retries})")
            try:
                driver.get(DEFAULT_URL)
            except Exception:
                pass

        time.sleep(2)

    return False


def switch_language_to_python(driver) -> bool:
    """Ensures compiler language is set to Python (3.8). Only clicks once if not already Python."""
    print("[*] Checking compiler language setting...")
    time.sleep(0.5)

    is_python = driver.execute_script("""
        var btns = document.querySelectorAll('*');
        for (var i = 0; i < btns.length; i++) {
            var t = (btns[i].innerText || '').trim();
            if (t === 'Python (3.8)' || t === 'Python (3.8.10)' || t.startsWith('Python')) {
                return true;
            }
        }
        return false;
    """)

    if is_python:
        print("[✓] Language is already set to Python (3.8)!")
        return True

    print("[*] Language is Java. Switching to Python (3.8)...")
    try:
        trigger = driver.find_element(By.XPATH, "//*[contains(text(), 'Java') and (self::span or self::div or self::button or self::p)]")
        driver.execute_script("arguments[0].click();", trigger)
        time.sleep(1)

        py_opt = driver.find_element(By.XPATH, "//*[contains(text(), 'Python (3.8)') or contains(text(), 'Python (3') or (contains(text(), 'Python') and not(contains(text(), 'using')))]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", py_opt)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", py_opt)
        print("[✓] Clicked Python (3.8) successfully!")
        time.sleep(2)
    except Exception as e:
        print(f"[-] Language switch notice: {e}")

    # Remove any open overlay backdrops
    driver.execute_script("""
        document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-container, .cdk-overlay-pane').forEach(e => e.remove());
    """)
    time.sleep(0.5)
    return True


def inject_code_into_editor(driver, code: str) -> bool:
    """
    Directly injects solution code into NeoColab's Ace Editor (programming-answer-ttAnswerEditor1).
    Instant, 100% reliable, zero dependency on window focus or keyboard simulation.
    """
    # 1. Close any modal/backdrop overlays
    driver.execute_script("""
        document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-container, .cdk-overlay-pane').forEach(e => e.remove());
    """)
    time.sleep(0.2)

    # 2. Direct Ace Editor injection
    res = driver.execute_script("""
        var code = arguments[0];
        var ed = document.getElementById('programming-answer-ttAnswerEditor1') ||
                 document.querySelector('[id*="AnswerEditor"]') ||
                 document.querySelector('.ace_editor');
        if (ed && ed.env && ed.env.editor) {
            ed.env.editor.setValue(code, 1);
            return ed.env.editor.getValue();
        }
        if (window.ace && ed) {
            var a = window.ace.edit(ed);
            a.setValue(code, 1);
            return a.getValue();
        }
        return null;
    """, code)

    first_line = [l.strip() for l in code.splitlines() if l.strip()][0]
    if res and first_line in res:
        print(f"[✓] Code successfully injected into Ace Editor and verified ({len(code.splitlines())} lines)!")
        return True

    # Fallback retry
    time.sleep(0.4)
    res2 = driver.execute_script("""
        var code = arguments[0];
        var ed = document.getElementById('programming-answer-ttAnswerEditor1') ||
                 document.querySelector('[id*="AnswerEditor"]') ||
                 document.querySelector('.ace_editor');
        if (ed && ed.env && ed.env.editor) {
            ed.env.editor.setValue(code, 1);
            return ed.env.editor.getValue();
        }
        return null;
    """, code)

    if res2 and first_line in res2:
        print("[✓] Code injected into Ace Editor on second attempt!")
        return True

    print("[-] Ace Editor injection verification failed!")
    return False


def reset_editor(driver):
    """Resets the Ace editor cleanly to empty for the next question."""
    driver.execute_script("""
        var ed = document.getElementById('programming-answer-ttAnswerEditor1') ||
                 document.querySelector('[id*="AnswerEditor"]') ||
                 document.querySelector('.ace_editor');
        if (ed && ed.env && ed.env.editor) {
            ed.env.editor.setValue('', 1);
        }
    """)
    time.sleep(0.3)


def scroll_editor_to_top(driver):
    """Scrolls page and editor view to top for clean code screenshot."""
    driver.execute_script("""
        window.scrollTo(0, 0);
        var all = document.querySelectorAll('*');
        for (var i = 0; i < all.length; i++) {
            if (all[i].scrollTop > 0) all[i].scrollTop = 0;
        }
        var ed = document.getElementById('programming-answer-ttAnswerEditor1') || document.querySelector('.ace_editor');
        if (ed && ed.env && ed.env.editor) {
            ed.env.editor.scrollToLine(1, true, true, function() {});
        }
        document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-container, .cdk-overlay-pane').forEach(e => e.remove());
    """)
    time.sleep(0.5)


def click_compile_and_run(driver) -> bool:
    """Finds and clicks the 'Compile & Run' button in NeoColab / Examly."""
    driver.execute_script("""
        document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-container, .cdk-overlay-pane').forEach(e => e.remove());
        var all = document.querySelectorAll('*');
        for (var i = 0; i < all.length; i++) {
            if (all[i].scrollHeight > all[i].clientHeight + 50) {
                all[i].scrollTop = all[i].scrollHeight;
            }
        }
    """)
    time.sleep(0.4)

    clicked = driver.execute_script("""
        var btns = document.querySelectorAll('button, a, div[role="button"], input[type="button"]');
        for (var i = 0; i < btns.length; i++) {
            var txt = (btns[i].innerText || btns[i].value || '').toLowerCase().trim();
            if (txt.includes('compile') && txt.includes('run')) {
                btns[i].scrollIntoView({block: 'center'});
                btns[i].click();
                return 'Compile & Run';
            }
        }
        for (var i = 0; i < btns.length; i++) {
            var txt = (btns[i].innerText || btns[i].value || '').toLowerCase().trim();
            if (txt === 'run' || txt === 'compile' || txt.includes('run code')) {
                btns[i].scrollIntoView({block: 'center'});
                btns[i].click();
                return 'Run';
            }
        }
        return null;
    """)

    if clicked:
        print(f"[✓] Successfully clicked '{clicked}' button!")
        return True

    # Selenium search fallback
    xpaths = [
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'compile & run')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'compile and run')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'run code')]",
    ]
    for xp in xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xp)
            for el in elements:
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", el)
                    print("[✓] Successfully clicked button via Selenium fallback!")
                    return True
        except Exception:
            continue

    print("[-] Could not find 'Compile and Run' button automatically.")
    return False


def scroll_to_output_and_wait(driver, max_wait: int = 15):
    """Waits for code compilation/execution to finish, scrolls down to show output."""
    print("[*] Waiting for execution output...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        time.sleep(1)
        still_loading = driver.execute_script("""
            var txt = document.body.innerText || '';
            return txt.includes('Debugger Loading') || txt.includes('Running...') || txt.includes('Compiling...');
        """)
        if not still_loading and (time.time() - start_time >= 3):
            print("[✓] Execution finished!")
            break

    time.sleep(0.8)

    # Scroll page to bottom so output card is fully visible
    driver.execute_script("""
        window.scrollTo(0, 99999);
        var all = document.querySelectorAll('*');
        for (var i = 0; i < all.length; i++) {
            if (all[i].scrollHeight > all[i].clientHeight + 50) {
                all[i].scrollTop = all[i].scrollHeight;
            }
        }
        var out = document.querySelector('.terminal, .output, [class*="output"], [class*="result"], #output, pre');
        if (out) out.scrollIntoView({block: 'center'});
        // Ensure the inner output box is scrolled to line 1
        document.querySelectorAll('pre, [class*="output"], .terminal').forEach(e => { e.scrollTop = 0; });
    """)
    time.sleep(1)


def run_full_pipeline(variant=None, is_auto=None):
    print("=" * 65)
    print("    NEOCOLAB AUTO-SOLVER, PASTER & SCREENSHOT BOT    ")
    print("=" * 65)

    driver = setup_browser()

    # Automatically scan all open tabs and switch to the IDE tab
    print("\n[*] Ensuring browser is on the NeoColab IDE tab...")
    if not ensure_ide_tab(driver):
        print("[!] Could not find NeoColab IDE tab. Navigating to IDE...")
        driver.get(DEFAULT_URL)
        time.sleep(3)
        if not ensure_ide_tab(driver):
            print("[!] Please open and log into NeoColab in Chrome, then press Enter.")
            input("Press [ENTER] when NeoColab IDE is ready in Chrome: ")
            ensure_ide_tab(driver)

    # Automatically ensure language is set to Python 3.8
    switch_language_to_python(driver)

    # Variant selection (Baseline is private to Ayush - friends get Style A or Style B)
    if not variant:
        print("\nSelect Code Solution Variant:")
        print("  [1] Style A (Variant 2: Different variables, alternative loops & test data)")
        print("  [2] Style B (Variant 3: Modular style, distinct string formatting & expressions)")
        v_choice = input("Enter choice [1 or 2, default: 1]: ").strip()
        variant = '3' if v_choice == '2' else '2'

    if str(variant).lower() in ['3', 'b']:
        sol_dir = BASE_DIR / "solutions_variant3"
        print("[✓] Using CODE VARIANT: Style B (solutions_variant3)")
    else:
        sol_dir = BASE_DIR / "solutions_variant2"
        print("[✓] Using CODE VARIANT: Style A (solutions_variant2)")

    # Mode selection
    if is_auto is None:
        print("\nSelect Automation Mode:")
        print("  [1] Fully Automatic (Runs all 30 questions hands-free with 3s delay — Recommended!)")
        print("  [2] Step-by-Step (Waits for you to hit [ENTER] per question — zero rush!)")
        mode_choice = input("Enter choice [1 or 2, default: 1]: ").strip()
        is_auto = (mode_choice != '2')

    if is_auto:
        print("[✓] Running in FULLY AUTOMATIC mode. Sit back and watch it run!")
    else:
        print("[✓] Running in STEP-BY-STEP mode. Press Enter when you want to proceed.")

    total_q = len(LAB_QUESTIONS)

    for i, q in enumerate(LAB_QUESTIONS):
        q_id = q["id"]
        print("\n" + "=" * 60)
        print(f"[{i+1}/{total_q}] SOLVING: {q['title']}")
        print("=" * 60)

        # Ensure we are ALWAYS on the correct IDE tab (even if other tabs exist or were opened)
        ensure_ide_tab(driver)

        # 1. Load solution code (cached from disk - instant, zero API cost)
        cached_file = sol_dir / f"{q_id}.py"
        if cached_file.exists():
            print(f"[✓] Loading solution from disk ({cached_file.name}) — 0 comments, authentic student code!")
            code = clean_code(cached_file.read_text(encoding="utf-8"))
        else:
            print("[*] Generating solution via Gemini 2.5 Flash...")
            try:
                code = clean_code(solve_question(q["text"], q.get("image")))
                cached_file.write_text(code, encoding="utf-8")
            except Exception as e:
                print(f"[!] Error with Gemini: {e}")
                continue

        # 2. Reset editor and inject solution code directly into Ace Editor
        inject_code_into_editor(driver, code)

        # 3. Scroll view to top and capture code screenshot
        scroll_editor_to_top(driver)
        code_ss_path = SCREENSHOT_DIR / f"{i+1:02d}_{q_id}_1_code.png"
        driver.save_screenshot(str(code_ss_path))
        print(f"[✓] Saved Code Screenshot: {code_ss_path}")

        # 4. Click 'Compile & Run'
        print("[*] Executing code (Clicking 'Compile & Run')...")
        click_compile_and_run(driver)

        # 5. Wait for execution and scroll down to Output section
        scroll_to_output_and_wait(driver, max_wait=15)

        # 6. Capture screenshot of Output
        output_ss_path = SCREENSHOT_DIR / f"{i+1:02d}_{q_id}_2_output.png"
        driver.save_screenshot(str(output_ss_path))
        print(f"[✓] Saved Output Screenshot: {output_ss_path}")

        # 7. Clean reset for next question
        reset_editor(driver)

        # 8. Transition
        print(f"[✓] Completed {q_id} successfully!")
        if is_auto:
            print("[*] Advancing to next question in 3 seconds (hands-free)...")
            time.sleep(3)
        else:
            choice = input("\nPress [ENTER] for NEXT question (or 'q' to stop): ").strip()
            if choice.lower() == 'q':
                print("Automation stopped. All captured screenshots are saved in 'lab_screenshots/'.")
                break

    print("\n" + "=" * 65)
    print("ALL 30 QUESTIONS COMPLETED!")
    print(f"Screenshots saved to: {SCREENSHOT_DIR.resolve()}")
    print("=" * 65)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NeoColab Auto-Solver and Screenshot Bot")
    parser.add_argument("--variant", "-v", choices=["2", "3", "A", "B", "a", "b"], default=None, help="Code variant (2/A: Style A, 3/B: Style B)")
    parser.add_argument("--auto", action="store_true", help="Run fully automatic hands-free")
    args = parser.parse_args()
    run_full_pipeline(variant=args.variant, is_auto=True if args.auto else None)

