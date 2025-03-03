# Attendance_via_Telegram

This Python script automates logging into the **SRMIST Student Portal**, solving the CAPTCHA using **Tesseract OCR**, and interacting with a **Telegram Bot** to receive messages and respond with a **full-page screenshot** of the student portal.

## Features
- **Automated login** to SRMIST Student Portal
- **CAPTCHA recognition** using Tesseract OCR
- **Telegram Bot integration** to receive commands
- **Automated screenshot capture** of the webpage
- **Sends screenshots to Telegram** upon receiving "hi"

## Requirements

Make sure you have the following installed:
- Python 3.x
- Google Chrome
- Chrome WebDriver (Ensure compatibility with your Chrome version)
- Tesseract OCR ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))
- Required Python libraries:

```sh
pip install requests selenium pillow pytesseract
```

## Setup

### 1. Configure Tesseract OCR
Set the correct path for Tesseract in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
```

### 2. Replace the following placeholders in the script:
- **Telegram Bot API Token** (`TELEGRAM_API_TOKEN = ''`)
- **Chat ID** (`CHAT_ID = ''`)
- **SRM Login Credentials** (inside `driver.find_element().send_keys()`) 

### 3. Run the Script
```sh
python script.py
```

## How It Works
1. The script launches **headless Chrome** and navigates to the login page.
2. It extracts the CAPTCHA image and deciphers it using **Tesseract OCR**.
3. Logs in using the provided **credentials and CAPTCHA**.
4. Waits for the Telegram command "hi".
5. Upon receiving "hi", it captures a **full-page screenshot** and sends it to Telegram.
6. Runs in a loop, checking for new messages.

## Notes
- **Headless Mode**: The script runs without opening a visible browser window.
- **Captcha Accuracy**: Tesseract OCR may have issues with complex CAPTCHAs.
- **WebDriver Compatibility**: Ensure the correct ChromeDriver version.

## License
MIT License

