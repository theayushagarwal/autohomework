from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
try:
    print("Navigating to https://vitvellore312.examly.io/ide ...")
    driver.get("https://vitvellore312.examly.io/ide")
    time.sleep(3)
    print("Title:", driver.title)
    print("Current URL:", driver.current_url)
    
    # Check for monaco editor
    editors = driver.find_elements(By.CSS_SELECTOR, ".monaco-editor")
    print(f"Found {len(editors)} monaco editors.")
    
    # Test setting value
    res = driver.execute_script("""
        if (window.monaco && window.monaco.editor) {
            var models = window.monaco.editor.getModels();
            if (models && models.length > 0) {
                models[0].setValue('# Code injected by AutoCode Script');
                return true;
            }
        }
        return false;
    """)
    print("Injected via JS:", res)
except Exception as e:
    print("Error:", e)
