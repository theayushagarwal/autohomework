from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
try:
    print("Navigating to https://vitvellore312.examly.io/ide ...")
    driver.get("https://vitvellore312.examly.io/ide")
    print("Page Title:", driver.title)
    elem = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
    )
    print("Monaco editor found successfully!")
    time.sleep(1)
    res = driver.execute_script("""
        if (window.monaco && window.monaco.editor) {
            var models = window.monaco.editor.getModels();
            if (models && models.length > 0) {
                models[0].setValue("print('SUCCESS')");
                return true;
            }
        }
        return false;
    """)
    print("Monaco setValue result:", res)
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
