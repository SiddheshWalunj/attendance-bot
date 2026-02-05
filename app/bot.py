import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv
from app.config import *

# ======================
# CONFIG
# ======================
DRY_RUN = True          # 🔒 TRUE = no real attendance, FALSE = real punch
HEADLESS = False        # False = see browser, True = headless (cloud)
SCREENSHOT_DIR = "logs"

# ======================
# ENV & LOGGING
# ======================
load_dotenv()
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logging.basicConfig(
    filename="logs/attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ======================
# CORE FUNCTION
# ======================
def mark_attendance(action: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            page = browser.new_page()

            logging.info("Opening GreatHR")
            page.goto(os.getenv("GREATHR_URL"), timeout=60000)

            # ✅ WAIT FOR ANGULAR LOGIN COMPONENT
            logging.info("Waiting for Angular login component")
            page.wait_for_selector("app-login", timeout=60000)

            # ✅ NOW WAIT FOR INPUTS
            page.wait_for_selector("input#username", timeout=30000)
            page.wait_for_selector("input#password", timeout=30000)

            # ✅ FILL LOGIN
            page.fill("input#username", os.getenv("GREATHR_USERNAME"))
            page.fill("input#password", os.getenv("GREATHR_PASSWORD"))

            # ✅ SUBMIT LOGIN
            page.click("button[type='submit']")
            logging.info("Login submitted")

            # ✅ WAIT FOR DASHBOARD LOAD
            page.wait_for_load_state("networkidle", timeout=60000)
            logging.info("Login successful")

            # ======================
            # DRY RUN / REAL ACTION
            # ======================
            if DRY_RUN:
                logging.info(
                    f"DRY RUN ENABLED — would have punched {action.upper()}"
                )
            else:
                if action == "in":
                    page.click(PUNCH_IN_BUTTON)
                elif action == "out":
                    page.click(PUNCH_OUT_BUTTON)
                else:
                    raise ValueError("Invalid action type")

            # ======================
            # SCREENSHOT
            # ======================
            screenshot_path = (
                f"{SCREENSHOT_DIR}/"
                f"{action}_{'dryrun' if DRY_RUN else 'live'}_{timestamp}.png"
            )
            page.screenshot(path=screenshot_path)
            logging.info(f"Screenshot saved: {screenshot_path}")

            browser.close()

    except Exception as e:
        logging.error(f"Attendance {action} failed: {e}")
        raise
