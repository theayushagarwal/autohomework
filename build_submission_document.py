import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import hashlib

THEMES = {
    "navy": {
        "name": "Classic Academic Navy",
        "primary_rgb": (0, 51, 102),        # #003366
        "secondary_rgb": (44, 82, 130),     # #2C5282
        "shading_hex": "EBF3FB",
        "border_hex": "B0C4DE",
        "text_dark": (34, 34, 34),
        "wm_rgb": (0.2, 0.35, 0.55),
    },
    "emerald": {
        "name": "Forest Emerald",
        "primary_rgb": (27, 77, 62),        # #1B4D3E
        "secondary_rgb": (46, 125, 50),     # #2E7D32
        "shading_hex": "E8F5E9",
        "border_hex": "A5D6A7",
        "text_dark": (28, 40, 34),
        "wm_rgb": (0.2, 0.45, 0.3),
    },
    "burgundy": {
        "name": "Crimson Burgundy",
        "primary_rgb": (107, 23, 36),       # #6B1724
        "secondary_rgb": (139, 0, 0),       # #8B0000
        "shading_hex": "FDF2F2",
        "border_hex": "FEB2B2",
        "text_dark": (45, 25, 30),
        "wm_rgb": (0.5, 0.2, 0.25),
    },
    "slate": {
        "name": "Modern Slate",
        "primary_rgb": (45, 55, 72),        # #2D3748
        "secondary_rgb": (74, 85, 104),     # #4A5568
        "shading_hex": "EDF2F7",
        "border_hex": "CBD5E0",
        "text_dark": (30, 35, 45),
        "wm_rgb": (0.35, 0.4, 0.45),
    },
    "indigo": {
        "name": "Royal Indigo",
        "primary_rgb": (49, 46, 129),       # #312E81
        "secondary_rgb": (67, 56, 202),     # #4338CA
        "shading_hex": "EEF2FF",
        "border_hex": "C7D2FE",
        "text_dark": (30, 30, 50),
        "wm_rgb": (0.3, 0.3, 0.6),
    },
    "amber": {
        "name": "Warm Amber Bronze",
        "primary_rgb": (120, 53, 15),       # #78350F
        "secondary_rgb": (146, 64, 14),     # #92400E
        "shading_hex": "FEF3C7",
        "border_hex": "FDE68A",
        "text_dark": (45, 35, 25),
        "wm_rgb": (0.5, 0.35, 0.2),
    },
}

FONTS = {
    "arial": "Arial",
    "calibri": "Calibri",
    "times": "Times New Roman",
    "segoe": "Segoe UI",
    "georgia": "Georgia"
}

def resolve_style_for_student(student_name, theme="auto", font="auto", header_style="auto"):
    student_clean = (student_name or "Ayush Agarwal").strip()
    seed = int(hashlib.md5(student_clean.lower().encode('utf-8')).hexdigest(), 16)
    
    header_keys = ["classic", "formal", "modern", "minimal"]
    
    if "ayush" in student_clean.lower():
        sel_theme = "navy" if theme == "auto" else theme
        sel_font = "arial" if font == "auto" else font
        sel_header = "classic" if header_style == "auto" else header_style
    else:
        # Friends get distinct non-navy themes and distinct fonts automatically
        friend_themes = ["emerald", "burgundy", "slate", "indigo", "amber"]
        friend_fonts = ["calibri", "times", "segoe", "georgia"]
        
        sel_theme = friend_themes[seed % len(friend_themes)] if theme == "auto" else theme
        sel_font = friend_fonts[(seed // 5) % len(friend_fonts)] if font == "auto" else font
        sel_header = header_keys[(seed // 11) % len(header_keys)] if header_style == "auto" else header_style

    sel_theme = sel_theme.lower()
    if sel_theme not in THEMES:
        sel_theme = "navy"
    sel_font = sel_font.lower()
    if sel_font not in FONTS:
        sel_font = "arial"
    sel_header = sel_header.lower()
    if sel_header not in header_keys:
        sel_header = "classic"

    return sel_theme, FONTS[sel_font], sel_header

def set_cell_border(cell, color="CCCCCC"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{color}"/></w:tcBorders>'
    )
    tcPr.append(tcBorders)

def set_cell_shading(cell, color="E8EEF5"):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def make_watermark_overlay(width=612, height=792, text="AYUSH AGARWAL", color_rgb=(0.4, 0.4, 0.4), alpha=0.25, angle=45):
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color
    import pypdf
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(Color(color_rgb[0], color_rgb[1], color_rgb[2], alpha=alpha))
    c.setFont("Helvetica-Bold", 15)
    
    x_positions = [70, 250, 430, 580]
    y_positions = [90, 270, 460, 660]
    
    for y in y_positions:
        for x in x_positions:
            c.saveState()
            c.translate(x, y)
            c.rotate(angle)
            c.drawCentredString(0, 0, text)
            c.restoreState()
            
    c.save()
    packet.seek(0)
    return pypdf.PdfReader(packet).pages[0]

def apply_pdf_watermark(pdf_path, text="AYUSH AGARWAL", theme_cfg=None, angle=45, alpha=0.25):
    import pypdf
    color_rgb = theme_cfg.get("wm_rgb", (0.4, 0.4, 0.4)) if theme_cfg else (0.4, 0.4, 0.4)
    wm_page = make_watermark_overlay(text=text, color_rgb=color_rgb, alpha=alpha, angle=angle)
    reader = pypdf.PdfReader(str(pdf_path))
    writer = pypdf.PdfWriter()
    
    for page in reader.pages:
        page.merge_page(wm_page)
        writer.add_page(page)
        
    temp_path = str(pdf_path) + ".tmp"
    with open(temp_path, "wb") as f:
        writer.write(f)
    os.replace(temp_path, str(pdf_path))
    print(f"[✓] Applied '{text}' watermark overlay (angle={angle}°, theme_tint={color_rgb}) to PDF: {Path(pdf_path).resolve()}")

def convert_to_pdf(docx_path, pdf_path):
    print("[*] Converting Word Document to PDF...")
    # Method 1: Microsoft Word via docx2pdf (Windows with Word installed)
    if sys.platform == "win32":
        try:
            from docx2pdf import convert
            convert(str(docx_path), str(pdf_path))
            if Path(pdf_path).exists() and Path(pdf_path).stat().st_size > 0:
                print(f"[✓] Created PDF via Microsoft Word: {Path(pdf_path).resolve()}")
                return True
        except Exception as e:
            print(f"[*] docx2pdf note: {e}. Checking for LibreOffice...")

    # Method 2: LibreOffice (Linux, Mac, GitHub Actions, or Windows without Word)
    import subprocess
    import shutil
    libreoffice_cmd = shutil.which("soffice") or shutil.which("libreoffice")
    if not libreoffice_cmd and sys.platform == "win32":
        for cand in [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]:
            if Path(cand).exists():
                libreoffice_cmd = cand
                break

    if libreoffice_cmd:
        try:
            out_dir = str(Path(pdf_path).parent.resolve())
            cmd = [libreoffice_cmd, "--headless", "--convert-to", "pdf", "--outdir", out_dir, str(docx_path)]
            subprocess.run(cmd, check=True)
            if Path(pdf_path).exists():
                print(f"[✓] Created PDF via LibreOffice: {Path(pdf_path).resolve()}")
                return True
        except Exception as e:
            print(f"[-] LibreOffice error: {e}")

    print("[-] Could not convert to PDF automatically. Please install Microsoft Word or LibreOffice.")
    return False

def create_lab_manual(student_name="Ayush Agarwal", theme="auto", font="auto", header_style="auto", screenshot_dir=None, docx_path=None, pdf_path=None):
    chosen_theme, chosen_font, chosen_header = resolve_style_for_student(student_name, theme, font, header_style)
    theme_cfg = THEMES[chosen_theme]

    print("\n" + "=" * 60)
    print("    LAB MANUAL SUBMISSION GENERATOR")
    print("=" * 60)
    print(f"[*] Student Name : {student_name}")
    print(f"[*] Theme        : {theme_cfg['name']} ({chosen_theme})")
    print(f"[*] Typography   : {chosen_font}")
    print(f"[*] Header Style : {chosen_header}")
    print("=" * 60)

    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)
        header = section.header
        p_head = header.paragraphs[0]
        p_head.text = ""

        if chosen_header == "formal":
            p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_l = p_head.add_run("Lab Record: Python Programming")
            r_l.font.name = chosen_font
            r_l.font.size = Pt(8.5)
            r_l.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])
            from docx.enum.text import WD_TAB_ALIGNMENT
            p_head.paragraph_format.tab_stops.add_tab_stop(Inches(7.2), WD_TAB_ALIGNMENT.RIGHT)
            r_r = p_head.add_run(f"\t{student_name}")
            r_r.font.name = chosen_font
            r_r.font.size = Pt(8.5)
            r_r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        elif chosen_header == "modern":
            p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_head = p_head.add_run(f"{student_name} — NeoColab Practical Record (CSE1001)")
            r_head.font.name = chosen_font
            r_head.font.size = Pt(8.5)
            r_head.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])
        elif chosen_header == "minimal":
            p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_head = p_head.add_run(f"{student_name}")
            r_head.font.name = chosen_font
            r_head.font.size = Pt(8.5)
            r_head.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        else:  # classic
            p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_head = p_head.add_run(f"{student_name} | Python Lab Submission")
            r_head.font.name = chosen_font
            r_head.font.size = Pt(8.5)
            r_head.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    normal_style = doc.styles['Normal']
    normal_style.font.name = chosen_font
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(*theme_cfg['text_dark'])

    if screenshot_dir is None:
        screenshot_dir = Path(__file__).resolve().parent / "lab_screenshots"
    else:
        screenshot_dir = Path(screenshot_dir).resolve()

    exercises = [
        {
            "id": 2,
            "title": "Ex:2 Basic Datatypes",
            "aim": "To understand the basic data types and escape sequences available in Python, and to learn how to execute Python programs using the Command Prompt and Python IDLE.",
            "content_type": "ex2",
            "result": "The Python programs were executed successfully using the Command Prompt and Python IDLE. The concepts of basic data types and escape sequences in Python were understood.",
            "questions": [
                {
                    "tag": "Ex2:a",
                    "sub_title": "Ex2:a Identify Data Types",
                    "code_img": "01_Ex2_a_IdentifyDatatype_1_code.png",
                    "out_img": "01_Ex2_a_IdentifyDatatype_2_output.png"
                },
                {
                    "tag": "Ex2:b",
                    "sub_title": "Ex2:b Predict the Output",
                    "code_img": "02_Ex2_b_PredictOutput_1_code.png",
                    "out_img": "02_Ex2_b_PredictOutput_2_output.png"
                },
                {
                    "tag": "Ex2:c",
                    "sub_title": "Ex2:c Which of the following are valid?",
                    "code_img": "03_Ex2_c_ValidVariables_1_code.png",
                    "out_img": "03_Ex2_c_ValidVariables_2_output.png"
                },
                {
                    "tag": "Ex2:d",
                    "sub_title": "Ex2:d Correct the Errors",
                    "code_img": "04_Ex2_d_CorrectErrors_1_code.png",
                    "out_img": "04_Ex2_d_CorrectErrors_2_output.png"
                },
                {
                    "tag": "Ex2:e",
                    "sub_title": "Ex2:e Print 'Hello World'",
                    "code_img": "05_Ex2_e_HelloWorld_1_code.png",
                    "out_img": "05_Ex2_e_HelloWorld_2_output.png"
                }
            ]
        },
        {
            "id": 3,
            "title": "Ex:3 Python Strings and Built in functions",
            "aim": "To write a python program for the following problems.",
            "content_type": "ex3",
            "result": "The python programs are written and executed successfully.",
            "questions": [
                {
                    "tag": "Ex3:1",
                    "sub_title": "Ex3:1 First, Fifth and Last Character of 'Python Programming'",
                    "code_img": "06_Ex3_Q1_Chars_1_code.png",
                    "out_img": "06_Ex3_Q1_Chars_2_output.png"
                },
                {
                    "tag": "Ex3:2",
                    "sub_title": "Ex3:2 String Slicing on 'Python Programming'",
                    "code_img": "07_Ex3_Q2_Slicing_1_code.png",
                    "out_img": "07_Ex3_Q2_Slicing_2_output.png"
                },
                {
                    "tag": "Ex3:3",
                    "sub_title": "Ex3:3 Negative Indexing on 'Vellore'",
                    "code_img": "08_Ex3_Q3_NegIndex_1_code.png",
                    "out_img": "08_Ex3_Q3_NegIndex_2_output.png"
                },
                {
                    "tag": "Ex3:4",
                    "sub_title": "Ex3:4 Print 'A' Without Typing 'A'",
                    "code_img": "09_Ex3_Q4_PrintA_1_code.png",
                    "out_img": "09_Ex3_Q4_PrintA_2_output.png"
                },
                {
                    "tag": "Ex3:5",
                    "sub_title": "Ex3:5 ASCII (Unicode) Values of 'A', 'a', 'Z', '0', '@'",
                    "code_img": "10_Ex3_Q5_ASCII_1_code.png",
                    "out_img": "10_Ex3_Q5_ASCII_2_output.png"
                },
                {
                    "tag": "Ex3:6",
                    "sub_title": "Ex3:6 Characters for ASCII Values 65, 97, 48, 36, 90",
                    "code_img": "11_Ex3_Q6_Chr_1_code.png",
                    "out_img": "11_Ex3_Q6_Chr_2_output.png"
                }
            ]
        },
        {
            "id": 4,
            "title": "Ex:4 Understanding the basics of Python",
            "aim": "To write a python program for the given problems.",
            "content_type": "ex4",
            "result": "The python programs are written and executed successfully.",
            "questions": [
                {
                    "tag": "Ex4:1",
                    "sub_title": "Ex4:1 Student Bio Card",
                    "code_img": "12_Ex4_Q1_BioCard_1_code.png",
                    "out_img": "12_Ex4_Q1_BioCard_2_output.png"
                },
                {
                    "tag": "Ex4:2",
                    "sub_title": "Ex4:2 Single Assignment Statement (Name, Age, CGPA)",
                    "code_img": "13_Ex4_Q2_SingleAssign_1_code.png",
                    "out_img": "13_Ex4_Q2_SingleAssign_2_output.png"
                },
                {
                    "tag": "Ex4:3",
                    "sub_title": "Ex4:3 Single Character Unicode Value",
                    "code_img": "14_Ex4_Q3_UnicodeChar_1_code.png",
                    "out_img": "14_Ex4_Q3_UnicodeChar_2_output.png"
                },
                {
                    "tag": "Ex4:4",
                    "sub_title": "Ex4:4 String Character Indexing (First, Last, Second, Second Last)",
                    "code_img": "15_Ex4_Q4_StringIndex_1_code.png",
                    "out_img": "15_Ex4_Q4_StringIndex_2_output.png"
                }
            ]
        },
        {
            "id": 5,
            "title": "Ex:5 Python Operators",
            "aim": "To write a python program for the given problems.",
            "content_type": "ex5",
            "result": "The python programs are written and executed successfully.",
            "questions": [
                {
                    "tag": "Ex5:1",
                    "sub_title": "Ex5:1 Supermarket Bill Arithmetic Analysis",
                    "code_img": "16_Ex5_Q1_Supermarket_1_code.png",
                    "out_img": "16_Ex5_Q1_Supermarket_2_output.png"
                },
                {
                    "tag": "Ex5:2",
                    "sub_title": "Ex5:2 Relational Operations on Student Marks",
                    "code_img": "17_Ex5_Q2_Relational_1_code.png",
                    "out_img": "17_Ex5_Q2_Relational_2_output.png"
                },
                {
                    "tag": "Ex5:3",
                    "sub_title": "Ex5:3 Smart Door Lock Bitwise Operations",
                    "code_img": "18_Ex5_Q3_Bitwise_1_code.png",
                    "out_img": "18_Ex5_Q3_Bitwise_2_output.png"
                },
                {
                    "tag": "Ex5:4",
                    "sub_title": "Ex5:4 Operator Precedence Evaluation",
                    "code_img": "19_Ex5_Q4_Precedence_1_code.png",
                    "out_img": "19_Ex5_Q4_Precedence_2_output.png"
                }
            ]
        },
        {
            "id": 6,
            "title": "Ex:6 Decision Making in Python",
            "aim": "To write a python program for the given problem statements.",
            "content_type": "ex6",
            "result": "Thus, the python code is developed and the output is observed for the given problems.",
            "questions": [
                {
                    "tag": "Ex6:1",
                    "sub_title": "Ex6:1 Attendance Percentage Check (>=75%)",
                    "code_img": "20_Ex6_Q1_Attendance_1_code.png",
                    "out_img": "20_Ex6_Q1_Attendance_2_output.png"
                },
                {
                    "tag": "Ex6:2",
                    "sub_title": "Ex6:2 Multiple of 2 or 5 Check",
                    "code_img": "21_Ex6_Q2_Multiple_1_code.png",
                    "out_img": "21_Ex6_Q2_Multiple_2_output.png"
                },
                {
                    "tag": "Ex6:3",
                    "sub_title": "Ex6:3 Greatest of Three Numbers",
                    "code_img": "22_Ex6_Q3_Greatest_1_code.png",
                    "out_img": "22_Ex6_Q3_Greatest_2_output.png"
                },
                {
                    "tag": "Ex6:4",
                    "sub_title": "Ex6:4 Grade Scoring System (S, A, B, C, D, Pass, Fail)",
                    "code_img": "23_Ex6_Q4_Grades_1_code.png",
                    "out_img": "23_Ex6_Q4_Grades_2_output.png"
                },
                {
                    "tag": "Ex6:5",
                    "sub_title": "Ex6:5 House Rent Allowance Check (6% of Salary)",
                    "code_img": "24_Ex6_Q5_Rent_1_code.png",
                    "out_img": "24_Ex6_Q5_Rent_2_output.png"
                }
            ]
        },
        {
            "id": 7,
            "title": "Ex:7 Python Loops - While",
            "aim": "To write a python program for the given problem statements.",
            "content_type": "ex7",
            "result": "Thus, the python code is developed and the output is observed for the given problems.",
            "questions": [
                {
                    "tag": "Ex7:1",
                    "sub_title": "Ex7:1 Factorial Using While Loop",
                    "code_img": "25_Ex7_Q1_Factorial_1_code.png",
                    "out_img": "25_Ex7_Q1_Factorial_2_output.png"
                },
                {
                    "tag": "Ex7:2",
                    "sub_title": "Ex7:2 Multiplication Table Using While Loop",
                    "code_img": "26_Ex7_Q2_Table_1_code.png",
                    "out_img": "26_Ex7_Q2_Table_2_output.png"
                },
                {
                    "tag": "Ex7:3",
                    "sub_title": "Ex7:3 Reverse Digits Using While Loop (Arithmetic Only)",
                    "code_img": "27_Ex7_Q3_ReverseDigits_1_code.png",
                    "out_img": "27_Ex7_Q3_ReverseDigits_2_output.png"
                }
            ]
        },
        {
            "id": 8,
            "title": "Ex:8 Python Loops - For and While",
            "aim": "To write a python program for the given problem statements.",
            "content_type": "ex8",
            "result": "Thus, the python code is developed and the output is observed for the given problems.",
            "questions": [
                {
                    "tag": "Ex8:1",
                    "sub_title": "Ex8:1 Currency Denomination Breakdown Using Loops",
                    "code_img": "28_Ex8_Q1_Denomination_1_code.png",
                    "out_img": "28_Ex8_Q1_Denomination_2_output.png"
                },
                {
                    "tag": "Ex8:2",
                    "sub_title": "Ex8:2 Descending Number Pattern Using Loops",
                    "code_img": "29_Ex8_Q2_NumberPattern_1_code.png",
                    "out_img": "29_Ex8_Q2_NumberPattern_2_output.png"
                },
                {
                    "tag": "Ex8:3",
                    "sub_title": "Ex8:3 Star Pyramid Pattern Using Loops",
                    "code_img": "30_Ex8_Q3_StarPattern_1_code.png",
                    "out_img": "30_Ex8_Q3_StarPattern_2_output.png"
                }
            ]
        }
    ]

    for ex_idx, ex in enumerate(exercises):
        # -------------------------------------------------------------
        # 1. QUESTION SHEET PAGE
        # -------------------------------------------------------------
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_title = p_title.add_run(ex["title"])
        run_title.font.name = chosen_font
        run_title.font.size = Pt(15)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(*theme_cfg['primary_rgb'])
        p_title.paragraph_format.space_after = Pt(10)

        p_aim = doc.add_paragraph()
        r_aim_lbl = p_aim.add_run("Aim:\n")
        r_aim_lbl.font.name = chosen_font
        r_aim_lbl.font.bold = True
        r_aim_lbl.font.size = Pt(11)
        r_aim_lbl.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])
        r_aim_txt = p_aim.add_run(ex["aim"])
        r_aim_txt.font.name = chosen_font
        r_aim_txt.font.size = Pt(10.5)
        p_aim.paragraph_format.space_after = Pt(12)

        ctype = ex["content_type"]

        if ctype == "ex2":
            p = doc.add_paragraph()
            r = p.add_run("a. Identify the datatype")
            r.font.name = chosen_font
            r.font.bold = True
            r.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])

            table_a = doc.add_table(rows=1, cols=2)
            table_a.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr = table_a.rows[0].cells
            hdr[0].paragraphs[0].add_run("Value").bold = True
            hdr[1].paragraphs[0].add_run("Data Type").bold = True
            set_cell_shading(hdr[0], theme_cfg['shading_hex'])
            set_cell_shading(hdr[1], theme_cfg['shading_hex'])
            set_cell_border(hdr[0], theme_cfg['border_hex'])
            set_cell_border(hdr[1], theme_cfg['border_hex'])

            vals_a = [
                ("25", "int"), ("25.0", "float"), ('"25"', "str"), ("'Python'", "str"),
                ("True", "bool"), ("False", "bool"), ("3+4j", "complex"), ("-18", "int"),
                ('"True"', "str"), ("0.0", "float"), ('"3+4j"', "str"), ("0", "int")
            ]
            for val, dt in vals_a:
                row = table_a.add_row().cells
                row[0].paragraphs[0].add_run(val)
                row[1].paragraphs[0].add_run(dt)
                set_cell_border(row[0], theme_cfg['border_hex'])
                set_cell_border(row[1], theme_cfg['border_hex'])

            doc.add_paragraph().paragraph_format.space_after = Pt(6)

            p = doc.add_paragraph()
            r = p.add_run("b. Predict the Output")
            r.font.name = chosen_font
            r.font.bold = True
            r.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])

            table_b = doc.add_table(rows=1, cols=2)
            table_b.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr_b = table_b.rows[0].cells
            hdr_b[0].paragraphs[0].add_run("Code").bold = True
            hdr_b[1].paragraphs[0].add_run("Output").bold = True
            set_cell_shading(hdr_b[0], theme_cfg['shading_hex'])
            set_cell_shading(hdr_b[1], theme_cfg['shading_hex'])
            set_cell_border(hdr_b[0], theme_cfg['border_hex'])
            set_cell_border(hdr_b[1], theme_cfg['border_hex'])

            codes_b = [
                ("x = 25\nprint(type(x))", "<class 'int'>"),
                ("x = 25.0\nprint(type(x))", "<class 'float'>"),
                ("x = 100\nx = \"VIT\"\nprint(type(x))", "<class 'str'>"),
                ("a = \"Python\"\nprint(a)", "Python"),
                ("x = 2+5j\nprint(type(x))", "<class 'complex'>"),
                ("print(\"Hello\\nPython\")", "Hello\nPython"),
                ("print(\"Name\\tAge\")", "Name    Age"),
                ("print(\"VIT\\\\Python\")", "VIT\\Python"),
                ("print(\"He said \\\"Hello\\\"\")", 'He said "Hello"'),
                ("print('It\\'s Python')", "It's Python")
            ]
            for c_txt, o_txt in codes_b:
                row = table_b.add_row().cells
                row[0].paragraphs[0].add_run(c_txt)
                row[1].paragraphs[0].add_run(o_txt)
                set_cell_border(row[0], theme_cfg['border_hex'])
                set_cell_border(row[1], theme_cfg['border_hex'])

            doc.add_paragraph().paragraph_format.space_after = Pt(6)

            p = doc.add_paragraph()
            r = p.add_run("c. Which of the following are valid?")
            r.font.name = chosen_font
            r.font.bold = True
            r.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])

            table_c = doc.add_table(rows=1, cols=2)
            table_c.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr_c = table_c.rows[0].cells
            hdr_c[0].paragraphs[0].add_run("Variable Assignment").bold = True
            hdr_c[1].paragraphs[0].add_run("Validity & Reason").bold = True
            set_cell_shading(hdr_c[0], theme_cfg['shading_hex'])
            set_cell_shading(hdr_c[1], theme_cfg['shading_hex'])
            set_cell_border(hdr_c[0], theme_cfg['border_hex'])
            set_cell_border(hdr_c[1], theme_cfg['border_hex'])

            vars_c = [
                ('name = "Rahul"', 'Valid string assignment'),
                ('city = Chennai', 'Invalid (Chennai is not enclosed in quotes)'),
                ('cgpa = 8.75', 'Valid float assignment'),
                ('student = True', 'Valid boolean assignment'),
                ('number = 3+5i', 'Invalid (Python uses j for imaginary part, not i)'),
                ("language = 'Python'", 'Valid string assignment')
            ]
            for v_txt, valid_txt in vars_c:
                row = table_c.add_row().cells
                row[0].paragraphs[0].add_run(v_txt)
                row[1].paragraphs[0].add_run(valid_txt)
                set_cell_border(row[0], theme_cfg['border_hex'])
                set_cell_border(row[1], theme_cfg['border_hex'])

            doc.add_paragraph().paragraph_format.space_after = Pt(6)

            p = doc.add_paragraph()
            r = p.add_run("d. Correct the errors")
            r.font.name = chosen_font
            r.font.bold = True
            r.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])

            table_d = doc.add_table(rows=1, cols=2)
            table_d.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr_d = table_d.rows[0].cells
            hdr_d[0].paragraphs[0].add_run("Erroneous Code").bold = True
            hdr_d[1].paragraphs[0].add_run("Corrected Code").bold = True
            set_cell_shading(hdr_d[0], theme_cfg['shading_hex'])
            set_cell_shading(hdr_d[1], theme_cfg['shading_hex'])
            set_cell_border(hdr_d[0], theme_cfg['border_hex'])
            set_cell_border(hdr_d[1], theme_cfg['border_hex'])

            errs_d = [
                ("name = Rahul\nprint(name)", 'name = "Rahul"\nprint(name)'),
                ('city = "Chennai\'', 'city = "Chennai"'),
                ('age = "18', 'age = 18'),
                ('print("Hello)', 'print("Hello")'),
                ('x = 3+4i', 'x = 3+4j')
            ]
            for e_txt, corr_txt in errs_d:
                row = table_d.add_row().cells
                row[0].paragraphs[0].add_run(e_txt)
                row[1].paragraphs[0].add_run(corr_txt)
                set_cell_border(row[0], theme_cfg['border_hex'])
                set_cell_border(row[1], theme_cfg['border_hex'])

            doc.add_paragraph().paragraph_format.space_after = Pt(6)

            p = doc.add_paragraph()
            r = p.add_run("e. Write a simple python code to print “Hello World” and execute the same using command line interface. (Both windows command line and IDLE)")
            r.font.bold = True
            p.paragraph_format.space_after = Pt(8)

        elif ctype == "ex3":
            q_list = [
                "1. Write a Python program to declare the string \"Python Programming\" and print:\n   • First character\n   • Fifth character\n   • Last character",
                "2. Write a Python program to declare “Python Programming”. Print the following using slicing:\n   • Python\n   • Programming\n   • gram\n   • Pro\n   • ming",
                "3. Write a Python program to declare “Vellore”. Print:\n   • Last character\n   • Second last character\n   • Third last character\n   using negative indexing.",
                "4. Without typing the letter A anywhere in the program, print A.",
                "5. Write a Python program to print the ASCII (Unicode) value of:\n   • A\n   • a\n   • Z\n   • 0\n   • @",
                "6. Write a Python program to print the characters corresponding to:\n   • 65\n   • 97\n   • 48\n   • 36\n   • 90"
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(5)

        elif ctype == "ex4":
            q_list = [
                "1. Write a Python program to read the following details from the user:\n   • Name, Age, Department, University, Mobile Number\n   Display the details in a formatted STUDENT BIO CARD.",
                "2. Write a Python program to assign your name, age, and CGPA to three variables using a single assignment statement and print the values.",
                "3. Write a Python program to read a single character from the user and display its Unicode value.",
                "4. Write a Python program to read a string from the user and display:\n   • First character\n   • Last character\n   • Second character\n   • Second last character"
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(6)

        elif ctype == "ex5":
            q_list = [
                "1. Supermarket Bill Analysis:\n   A customer purchases two products from a supermarket. Write a Python program to read the price of two products and display: Total price, Price difference, Product of prices, Division of first by second, Remainder, Floor division.",
                "2. Student Marks Comparison:\n   A college wants to compare marks of Student A and Student B. Read marks and display relational operations: ==, !=, >, <, >=, <=.",
                "3. Smart Door Lock Bitwise Operations:\n   Read two integer permission codes. Display binary representations and perform: Bitwise AND, OR, XOR, Bitwise Complement of code1, Left shift by 1, Right shift by 1. Display both decimal and binary.",
                "4. Operator Precedence:\n   Evaluate and display the following expressions:\n   • 5 + 3 * 2\n   • (5 + 3) * 2\n   • 2 ** 3 * 2\n   • 2 ** 3 ** 2"
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(6)

        elif ctype == "ex6":
            q_list = [
                "1. Attendance Percentage Check:\n   Get the attendance percentage of a student. If >= 75 print 'Student is permitted', else 'Student not permitted'.",
                "2. Multiple of 2 or 5:\n   Find if the given number is a multiple of 2 or 5 or neither of them.",
                "3. Greatest of Three Numbers:\n   Find the greatest of three given numbers.",
                "4. Grade Scoring:\n   Get mark in computer science and print grade: >=91: S, 81-90: A, 71-80: B, 61-70: C, 51-60: D, 50: Pass, <50: Fail.",
                "5. House Rent Allowance:\n   Get salary and house rent. Compute 6% of salary. If rent <= 6% print 'Rent allowance matched', else 'Rent allowance not matched'."
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(6)

        elif ctype == "ex7":
            q_list = [
                "1. Factorial Using While Loop:\n   Write a Python program using while loop to print the factorial of a given number.",
                "2. Multiplication Table Using While Loop:\n   Write a Python program using while loop to print the multiplication table of the given number.",
                "3. Reverse Digits Using While Loop:\n   Write a Python program to get an integer and display the digits in reverse order using while loop (using arithmetic operators only, without string concepts)."
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(6)

        elif ctype == "ex8":
            q_list = [
                "1. Currency Denomination:\n   Write a Python program using loops to print the denomination breakdown of a given amount.",
                "2. Descending Number Pattern:\n   Write a Python program using loops to print the following number pattern:\n   5  4  3  2  1\n   4  3  2  1\n   3  2  1\n   2  1\n   1",
                "3. Star Pyramid Pattern:\n   Write a Python program using loops to print the following star pyramid pattern:\n      *\n     ***\n    *****\n   *******"
            ]
            for q_item in q_list:
                p = doc.add_paragraph()
                r = p.add_run(q_item)
                r.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(6)

        # Result section
        p_res = doc.add_paragraph()
        r_res_lbl = p_res.add_run("Result:\n")
        r_res_lbl.font.name = chosen_font
        r_res_lbl.font.bold = True
        r_res_lbl.font.size = Pt(11)
        r_res_lbl.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])
        r_res_txt = p_res.add_run(ex["result"])
        r_res_txt.font.name = chosen_font
        r_res_txt.font.size = Pt(10.5)
        p_res.paragraph_format.space_before = Pt(10)
        p_res.paragraph_format.space_after = Pt(10)

        # -------------------------------------------------------------
        # 2. SUB-QUESTIONS ANSWERS (CODE & OUTPUT SCREENSHOTS)
        # -------------------------------------------------------------
        for q in ex["questions"]:
            doc.add_page_break()

            # Sub-question heading (matching sample PDF: e.g. Ex2:a, Ex3:1, Ex4:1)
            p_sub = doc.add_paragraph()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_tag = p_sub.add_run(f"{q['tag']}\n")
            r_tag.font.name = chosen_font
            r_tag.font.size = Pt(16)
            r_tag.font.bold = True
            r_tag.font.color.rgb = RGBColor(*theme_cfg['primary_rgb'])

            r_sub_desc = p_sub.add_run(f"{q['sub_title']}")
            r_sub_desc.font.name = chosen_font
            r_sub_desc.font.size = Pt(10.5)
            r_sub_desc.font.color.rgb = RGBColor(*theme_cfg['secondary_rgb'])
            p_sub.paragraph_format.space_after = Pt(4)

            # Code Screenshot
            code_path = screenshot_dir / q["code_img"]
            if code_path.exists():
                p_img1 = doc.add_paragraph()
                p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img1.paragraph_format.space_after = Pt(2)
                p_img1.add_run().add_picture(str(code_path), width=Inches(6.3))

            # Output Screenshot
            out_path = screenshot_dir / q["out_img"]
            if out_path.exists():
                p_img2 = doc.add_paragraph()
                p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img2.paragraph_format.space_after = Pt(2)
                p_img2.add_run().add_picture(str(out_path), width=Inches(6.3))

        # Add page break before next exercise question sheet
        if ex_idx < len(exercises) - 1:
            doc.add_page_break()

    if docx_path is None:
        out_docx = Path(__file__).resolve().parent / "Python_Lab_Manual_Submission.docx"
    else:
        out_docx = Path(docx_path).resolve()

    doc.save(str(out_docx))
    print(f"[✓] Created Word document: {out_docx.resolve()}")

    if pdf_path is None:
        out_pdf = Path(__file__).resolve().parent / "Python_Lab_Manual_Submission.pdf"
    else:
        out_pdf = Path(pdf_path).resolve()

    if convert_to_pdf(out_docx, out_pdf):
        seed = int(hashlib.md5(student_name.strip().lower().encode('utf-8')).hexdigest(), 16)
        angles = [45, 30, -45, 35]
        chosen_angle = 45 if "ayush" in student_name.lower() else angles[seed % len(angles)]
        print(f"[*] Applying watermark overlay for '{student_name.upper()}' (Theme: {chosen_theme}, Angle: {chosen_angle}°)...")
        apply_pdf_watermark(out_pdf, student_name.upper(), theme_cfg=theme_cfg, angle=chosen_angle)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Python Lab Manual Submission with Custom Themes and Watermarks")
    parser.add_argument("--name", "-n", default=None, help="Student name for header & watermark (e.g. 'Ayush Agarwal')")
    parser.add_argument("--theme", "-t", choices=["auto", "navy", "emerald", "burgundy", "slate", "indigo", "amber"], default="auto", help="Visual color theme (default: auto - assigns unique theme based on student name)")
    parser.add_argument("--font", "-f", choices=["auto", "arial", "calibri", "times", "segoe", "georgia"], default="auto", help="Typography font family (default: auto)")
    parser.add_argument("--header-style", "-s", choices=["auto", "classic", "formal", "modern", "minimal"], default="auto", help="Page header style (default: auto)")
    parser.add_argument("--screenshots", default=None, help="Directory containing lab screenshots (default: lab_screenshots)")
    parser.add_argument("--output", "-o", default=None, help="Custom output filename base (e.g. Python_Lab_Manual_Rahul)")
    args = parser.parse_args()

    name = args.name
    if not name:
        try:
            name = input("Enter student name for watermark & header [default: Ayush Agarwal]: ").strip()
        except (EOFError, KeyboardInterrupt):
            name = ""
    if not name:
        name = "Ayush Agarwal"

    docx_file = None
    pdf_file = None
    if args.output:
        base = Path(args.output)
        docx_file = base.with_suffix(".docx")
        pdf_file = base.with_suffix(".pdf")

    create_lab_manual(
        student_name=name,
        theme=args.theme,
        font=args.font,
        header_style=args.header_style,
        screenshot_dir=args.screenshots,
        docx_path=docx_file,
        pdf_path=pdf_file
    )

