import time
import os
import io
from pathlib import Path
from PIL import Image
import imageio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

ARTIFACT_DIR = Path("/config/.gemini/antigravity/brain/54846652-e351-4098-977e-8123ccdd4921")
VIDEO_PATH = ARTIFACT_DIR / "demo_handover_assistant.mp4"

def record_demo():
    print("Setting up Chrome headless browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=chrome_options)
    frames = []

    def capture_frame(fps_delay=0.15):
        png = driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(png)).convert("RGB")
        frames.append(img)
        time.sleep(fps_delay)

    def record_seconds(duration, fps_delay=0.15):
        end_time = time.time() + duration
        while time.time() < end_time:
            capture_frame(fps_delay)

    try:
        url = "http://localhost:8080"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(2)
        record_seconds(2)

        # 1. Prompt 1: Show P1/P2 Incidents & SLA Risk
        print("Sending Prompt 1...")
        input_box = driver.find_element(By.ID, "input")
        
        prompt_1 = "Show P1/P2 Incidents & SLA Risk"
        for char in prompt_1:
            input_box.send_keys(char)
            capture_frame(0.04)
        
        record_seconds(0.5)
        send_btn = driver.find_element(By.CLASS_NAME, "send-btn")
        send_btn.click()

        print("Waiting for Prompt 1 A2UI cards response...")
        start_wait = time.time()
        while time.time() - start_wait < 30:
            capture_frame(0.2)
            cards = driver.find_elements(By.CLASS_NAME, "a2card")
            if len(cards) > 0:
                print(f"Found {len(cards)} A2UI cards!")
                break

        record_seconds(3)

        # Scroll down chat
        chat_box = driver.find_element(By.ID, "log")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", chat_box)
        record_seconds(2)

        # 2. Prompt 2: Richer prompt (tool call + database lookup + image generation)
        print("Sending Prompt 2...")
        input_box = driver.find_element(By.ID, "input")
        prompt_2 = "Generate visual shift handover dashboard image for Payments API"
        for char in prompt_2:
            input_box.send_keys(char)
            capture_frame(0.04)

        record_seconds(0.5)
        send_btn = driver.find_element(By.CLASS_NAME, "send-btn")
        send_btn.click()

        print("Waiting for Prompt 2 image generation response...")
        start_wait = time.time()
        while time.time() - start_wait < 45:
            capture_frame(0.25)
            # Check for rendered image
            images = driver.find_elements(By.TAG_NAME, "img")
            if len(images) > 0:
                print(f"Found {len(images)} rendered dashboard images!")
                break

        record_seconds(4)

        # Smooth scroll down to view generated image card
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", chat_box)
        record_seconds(4)

    finally:
        driver.quit()

    print(f"Captured {len(frames)} total frames. Compiling MP4 video...")
    writer = imageio.get_writer(str(VIDEO_PATH), fps=6, format="FFMPEG", codec="libx264")
    for frame in frames:
        import numpy as np
        writer.append_data(np.array(frame))
    writer.close()
    print(f"Video recorded successfully to {VIDEO_PATH}")

if __name__ == "__main__":
    record_demo()
