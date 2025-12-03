import webbrowser, pyautogui, os

def open_website(url):
    webbrowser.open(url)

def type_text(text):
    pyautogui.write(text, interval=0.05)

def take_screenshot(save_path="screenshot.png"):
    img = pyautogui.screenshot()
    img.save(save_path)
    return save_path

def execute_command(command):
    os.system(command)
