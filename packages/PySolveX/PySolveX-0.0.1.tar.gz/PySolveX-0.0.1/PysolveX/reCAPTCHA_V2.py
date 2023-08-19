from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from pydub import AudioSegment
import speech_recognition as sr
import wget

class reCAPTCHA_V2:
    def __init__(self, driver, debug=False):
        self.driver = driver
        self.debug = debug
    def solve(self):
        if self.debug:
            print("[!] The captcha is being bypassed .")
        iframe = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@title="reCAPTCHA"]')))
        self.driver.switch_to.frame(iframe)
        WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))).click()
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 6).until(ec.presence_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checked")))
            if self.debug:
                print(f"[!] The captcha has been Bypassed successfully")
                self.driver.switch_to.default_content()
                return True
        except:
            pass
        iframe = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@title="recaptcha challenge expires in two minutes"]')))
        self.driver.switch_to.frame(iframe)
        if self.debug:
            print("[!] Extracting the audio link ..")
        WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.ID, "recaptcha-audio-button"))).click()
        audio_url = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload-link"))).get_attribute("href")
        if self.debug:
            print("[!] Audio is Downloading ...")
        audio = wget.download(audio_url)
        if self.debug:
            print("[!] The audio is being analyzed and the text is extracted .")
            print("[!] It may take some time ..")
        record = sr.Recognizer()
        sound = AudioSegment.from_mp3(audio)
        wav = sound.export(audio, format="wav")
        with sr.AudioFile(wav) as source:
            audio_source = record.record(source)
            text = record.recognize_google(audio_source, language="en-US")
        print(f"[!] The extracted text is: {text} ...")
        WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.ID, "audio-response"))).send_keys(text)
        WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.ID, "recaptcha-verify-button"))).click()
        try:
            ErrorMsg = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-error-message"))).text
        except:
            ErrorMsg = None
        if ErrorMsg:
            print(f"[!] The captcha was not passed because: {ErrorMsg} .")
        elif not ErrorMsg and self.debug:
            print(f"[!] The captcha has been Bypassed successfully")
        self.driver.switch_to.default_content()
        return True