import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])

import time

import cv2
import tempfile
import pyautogui
import argparse

parser = argparse.ArgumentParser(description='Elden Ring Death Counter.')
parser.add_argument('--dev', action='store_true', help='Activate development mode for additional output.')
args = parser.parse_args()

death_count = 0;

def find_death_screen():

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        screenshot_path = tmp_file.name
        pyautogui.screenshot(screenshot_path)

    image = cv2.imread(screenshot_path)
    template_accept = cv2.imread("IhrSeidGestorben.png")

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_accept_gray = cv2.cvtColor(template_accept, cv2.COLOR_BGR2GRAY)

    result_template_accept_gray = cv2.matchTemplate(image_gray, template_accept_gray, cv2.TM_CCOEFF_NORMED)

    min_val_result_template_accept_gray, \
        max_val_result_template_accept_gray, \
        min_loc_result_template_accept_gray, \
        max_loc_result_template_accept_gray = cv2.minMaxLoc(result_template_accept_gray)

    threshold = 0.32

    if args.dev:
        print(max_val_result_template_accept_gray)

    if max_val_result_template_accept_gray >= threshold:
        return True
    return False


if __name__ == "__main__":
    print("German Elden Ring death counter started successfully!")
    if args.dev:
        print("Started in development mode.")
    try:
        while True:
            if find_death_screen():
                print("You died!")
                death_count += 1
                time.sleep(10)
            if args.dev:
                print("Scanning")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("You died", death_count, "times in total.")
        print("Elden Ring death counter closed.")
