"""
AutoCode Lab Runner — Step-by-Step Question Solver & Auto-Paster
Automatically sends each question to Gemini, gets the code, and pastes it into Examly!
"""

import os
import sys
import time
import ctypes
from pathlib import Path

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai
import pyperclip

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# Keyboard simulation via built-in Windows ctypes (no extra install needed!)
def auto_paste_into_editor():
    """Simulates Ctrl+A, Backspace, and Ctrl+V using Windows user32."""
    user32 = ctypes.windll.user32
    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_BACK = 0x08
    VK_V = 0x56
    KEYEVENTF_KEYUP = 0x0002

    # Ctrl + A (Select All)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_A, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

    # Backspace (Delete existing code/comment)
    user32.keybd_event(VK_BACK, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_BACK, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

    # Ctrl + V (Paste code)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)


def clean_code(text: str) -> str:
    """Removes markdown backticks and fences."""
    text = text.strip()
    lines = text.split("\n")
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def solve_question(question_text: str, image_path: str = None) -> str:
    """Sends question to Gemini and gets clean executable Python code."""
    prompt = (
        f"You are writing a Python 3 lab solution for a student at VIT university.\n"
        f"Problem description: {question_text}\n\n"
        f"REQUIREMENTS:\n"
        f"1. Write clean, complete, working Python 3 code.\n"
        f"2. Add clear print statements so the output matches the requirements.\n"
        f"3. Return ONLY raw executable Python code. No markdown code blocks, no explanations, no text outside the code."
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


# All lab questions organized step-by-step
QUESTIONS = [
    # Ex 2
    {
        "id": "Ex 2",
        "title": "Ex:2 Basic Datatypes & Predict the Output",
        "image": "questions/ex_page_1.png",
        "text": "Ex:2 Basic Datatypes. Predict output for data types (int, float, complex, string, escape sequences), corrected code, and Hello World."
    },
    # Ex 3
    {
        "id": "Ex 3 - Q1",
        "title": "Ex:3 Q1 - First, Fifth, Last character",
        "image": "questions/ex_page_2.png",
        "text": "Declare the string 'Python Programming' and print: 1. First character, 2. Fifth character, 3. Last character."
    },
    {
        "id": "Ex 3 - Q2",
        "title": "Ex:3 Q2 - Slicing 'Python Programming'",
        "image": "questions/ex_page_2.png",
        "text": "Declare 'Python Programming'. Print using slicing: 'Python', 'Programming', 'gram', 'Pro', 'ming'."
    },
    {
        "id": "Ex 3 - Q3",
        "title": "Ex:3 Q3 - Negative indexing on 'Vellore'",
        "image": "questions/ex_page_2.png",
        "text": "Declare 'Vellore'. Print Last character, Second last character, Third last character using negative indexing."
    },
    {
        "id": "Ex 3 - Q4",
        "title": "Ex:3 Q4 - Print 'A' without typing 'A'",
        "image": "questions/ex_page_2.png",
        "text": "Without typing the letter A anywhere in the program, print A."
    },
    {
        "id": "Ex 3 - Q5",
        "title": "Ex:3 Q5 - ASCII / Unicode values",
        "image": "questions/ex_page_2.png",
        "text": "Print the ASCII (Unicode) value of characters: 'A', 'a', 'Z', '0', '@'."
    },
    {
        "id": "Ex 3 - Q6",
        "title": "Ex:3 Q6 - Characters corresponding to ASCII values",
        "image": "questions/ex_page_2.png",
        "text": "Print the characters corresponding to ASCII values: 65, 97, 48, 36, 90."
    },
    # Ex 4
    {
        "id": "Ex 4 - Q1",
        "title": "Ex:4 Q1 - Student Bio Card",
        "image": "questions/ex_page_3.png",
        "text": "Read Name, Age, Department, University, Mobile Number from the user and display formatted Student Bio Card."
    },
    {
        "id": "Ex 4 - Q2",
        "title": "Ex:4 Q2 - Single Assignment Statement",
        "image": "questions/ex_page_3.png",
        "text": "Assign your name, age, and CGPA to three variables using a single assignment statement and print them."
    },
    {
        "id": "Ex 4 - Q3",
        "title": "Ex:4 Q3 - Unicode of Single Character",
        "image": "questions/ex_page_3.png",
        "text": "Read a single character from the user and display its Unicode value."
    },
    {
        "id": "Ex 4 - Q4",
        "title": "Ex:4 Q4 - String Characters Display",
        "image": "questions/ex_page_3.png",
        "text": "Read a string from user and display: First character, Last character, Second character, Second last character."
    },
    # Ex 5
    {
        "id": "Ex 5 - Q1",
        "title": "Ex:5 Q1 - Supermarket Bill & Arithmetic Operations",
        "image": "questions/ex_page_4.png",
        "text": "Read price of two products. Display: Total price, Price difference, Product, Division, Remainder, Floor division."
    },
    {
        "id": "Ex 5 - Q2",
        "title": "Ex:5 Q2 - Relational Operations on Student Marks",
        "image": "questions/ex_page_4.png",
        "text": "Read marks of Student A and Student B. Display results of relational operations: ==, !=, >, <, >=, <=."
    },
    {
        "id": "Ex 5 - Q3",
        "title": "Ex:5 Q3 - Bitwise Operations on Smart Lock Permissions",
        "image": "questions/ex_page_4.png",
        "text": "Read two integer permission codes. Display binary representation and perform: Bitwise AND, OR, XOR, Bitwise Complement of first code, Left shift by 1, Right shift by 1. Display both decimal and binary."
    },
    {
        "id": "Ex 5 - Q4",
        "title": "Ex:5 Q4 - Operator Precedence",
        "image": "questions/ex_page_4.png",
        "text": "Evaluate and display: 5+3*2, (5+3)*2, 2**3*2, 2**3**2."
    },
    # Ex 6
    {
        "id": "Ex 6 - Q1",
        "title": "Ex:6 Q1 - Attendance Percentage",
        "image": "questions/ex_page_5.png",
        "text": "Get attendance percentage of a student. If >= 75 print 'Student is permitted', else 'Student not permitted'."
    },
    {
        "id": "Ex 6 - Q2",
        "title": "Ex:6 Q2 - Multiple of 2 or 5",
        "image": "questions/ex_page_5.png",
        "text": "Find if the given number is a multiple of 2 or 5 or neither of them."
    },
    {
        "id": "Ex 6 - Q3",
        "title": "Ex:6 Q3 - Greatest of Three Numbers",
        "image": "questions/ex_page_5.png",
        "text": "Find the greatest of three numbers."
    },
    {
        "id": "Ex 6 - Q4",
        "title": "Ex:6 Q4 - Grade Scoring",
        "image": "questions/ex_page_5.png",
        "text": "Print grade based on marks: >=91: S, 81-90: A, 71-80: B, 61-70: C, 51-60: D, 50: Pass, <50: Fail."
    },
    {
        "id": "Ex 6 - Q5",
        "title": "Ex:6 Q5 - House Rent Allowance",
        "image": "questions/ex_page_5.png",
        "text": "Get salary and house rent. Compute 6% of salary. If house rent is within 6% print 'Rent allowance matched', else 'Rent allowance not matched'."
    },
    # Ex 7
    {
        "id": "Ex 7 - Q1",
        "title": "Ex:7 Q1 - Factorial using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Write a Python program using while loop to print the factorial of a given number."
    },
    {
        "id": "Ex 7 - Q2",
        "title": "Ex:7 Q2 - Multiplication Table using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Write a Python program using while loop to print the multiplication table of a given number."
    },
    {
        "id": "Ex 7 - Q3",
        "title": "Ex:7 Q3 - Reverse Digits using While Loop",
        "image": "questions/ex_page_6.png",
        "text": "Get an integer. Display digits in reverse order using while loop with arithmetic operators only (no string conversion)."
    },
    # Ex 8
    {
        "id": "Ex 8 - Q1",
        "title": "Ex:8 Q1 - Currency Denomination",
        "image": "questions/ex_page_7.png",
        "text": "Write a python program using loops to print the denomination of a given amount."
    },
    {
        "id": "Ex 8 - Q2",
        "title": "Ex:8 Q2 - Patterns",
        "image": "questions/ex_page_7.png",
        "text": "Write a python program using loops to print the number pattern (descending numbers) and star pyramid pattern."
    }
]


def main():
    print("=" * 60)
    print("   AUTO-CODE LAB RUNNER (Examly Automation)   ")
    print("=" * 60)
    print("How it works:")
    print("1. Script calls Gemini to solve the question.")
    print("2. It copies the code and automatically pastes it into your editor.")
    print("3. You run it, take your screenshot, and press Enter for the next one!")
    print("=" * 60)

    for idx, q in enumerate(QUESTIONS):
        print(f"\n[{idx + 1}/{len(QUESTIONS)}] Processing: {q['title']} ({q['id']})")
        print(f"[*] Asking Gemini for solution...")
        
        try:
            code = solve_question(q["text"], q.get("image"))
        except Exception as e:
            print(f"[!] Error calling Gemini: {e}")
            continue

        # Put on clipboard
        pyperclip.copy(code)

        print("\n--- SOLUTION GENERATED ---")
        print(code[:200] + ("..." if len(code) > 200 else ""))
        print("--------------------------")

        print("\n[!] READY TO AUTO-PASTE INTO EXAMLY:")
        print(">> CLICK ONCE INSIDE YOUR EXAMLY CODE BOX NOW!")
        print(">> Auto-pasting in:")
        for i in range(3, 0, -1):
            print(f"   {i}...", end="", flush=True)
            time.sleep(1)
        print(" PASTING NOW!")

        auto_paste_into_editor()
        print("\n[✓] CODE PASTED!")
        print("[✓] Click 'Run' / 'Compile' in Examly and TAKE YOUR SCREENSHOT OF THE OUTPUT.")
        
        user_input = input("\nPress [ENTER] to move to the next question (or 'q' to quit): ").strip()
        if user_input.lower() == 'q':
            print("Exiting. Great job!")
            break


if __name__ == "__main__":
    main()
