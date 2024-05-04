import pyautogui
import time

def get_cursor_position():
    try:
        while True:
            x, y = pyautogui.position()
            print('X:', x, 'Y:', y)
            time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("\nProgram terminated.")

if __name__ == "__main__":
    get_cursor_position()