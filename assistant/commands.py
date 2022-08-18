import speech_recognition
import sys
from datetime import datetime
import datetime
import wikipedia
import webbrowser
import pyautogui
import os
import requests
from playsound import playsound
from win10toast import ToastNotifier
import subprocess
import ctypes
from gtts import gTTS
import locale

locale.setlocale(locale.LC_ALL, '')

recognizer = speech_recognition.Recognizer()


def speak(string):
    tts = gTTS(text=string, lang="tr", slow=False)
    file = "answer.mp3"
    tts.save(file)
    playsound(file)    
    os.remove(file)



def greeting():
    global recognizer   
    
    speak("Gidiyorum gündüz gece bilmiyorum ne haldeyim.")

def goodbye():
    global recognizer
    
    playsound("ending.mp3")
    speak("Görüşürüz.")
    os.system("TASKKILL /F /IM Python.exe")

def sarki():
    global recognizer
    speak("Gidiyoruuuğm gündüüüğz geceeeğ bilmiyoruuuğm ne haaalldeyiiiğm.")

def what_time():
    global recognizer

    clock = datetime.datetime.now()
    saat = datetime.datetime.strftime(clock,'%H:%M')
    speak(f"Saat {saat}.")
    goodbye()

def search_in_wiki():

    global recognizer

    speak("Wikipedia'da ne aramamı istersin?")
    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                wiki = recognizer.recognize_google(audio, language="tr-TR")
                wiki = wiki.lower()
                playsound("ending.mp3")
                results = wikipedia.summary(wiki, sentences = 3)
                done = True

                speak(f"{wiki} için Wikipedia'da bulduklarım: ")
                speak(results)
                goodbye()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")

def open_video_youtube():

    global recognizer

    speak("Youtube'dan hangi videoyu bulmamı istersin?")

    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                VideoName = recognizer.recognize_google(audio, language="tr-Tr")
                VideoName = VideoName.lower()
                playsound("ending.mp3")
                adres = ('https://www.youtube.com/results?search_query=')+VideoName
                webbrowser.get().open(adres)
                pyautogui.moveTo(x=702, y=252)
                pyautogui.click(button='left', clicks=2, interval=7)

                goodbye()

             
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")

def search_google():

    global recognizer

    speak("Google'da ne aramamı istersin?")
    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                search = recognizer.recognize_google(audio, language="tr-TR")
                search = search.lower()
                playsound("ending.mp3")
                adres = ('https://www.google.com/search?q=')+search
                webbrowser.get().open(adres)
                pyautogui.moveTo(x=384, y=368)
                pyautogui.click(button='left',clicks=2,interval=7)  

                speak(f"{search} için Google'da bulduklarım:") 
                goodbye()                
             
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Can not understand")

def open_twitter():
    global recognizer
    
    adres = ('https://www.twitter.com/')
    webbrowser.open_new_tab(adres)
    goodbye()

def open_github():
    global recognizer

    adres = ('https://github.com/')
    webbrowser.open_new_tab(adres)
    goodbye()

def day_week():

    global recognizer
    
    day = datetime.datetime.now()
    today = datetime.datetime.strftime(day, '%A')
    speak(f"Bugün {today}.")
    goodbye()

def current_date():
    global recognizer

    current_date = datetime.datetime.now()
    speak(datetime.datetime.strftime(current_date, '%d %B %Y'))
    goodbye()

def weather_forc():
    global recognizer

    api_key = "4fdba23f173321e0fe76daae49c2d1a1"
    
    speak("Hangi şehir için hava durumunu görmek istiyorsun?")
    
    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                city_name = recognizer.recognize_google(audio, language="tr-Tr")

                
                response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}')
                weatherData = response.json()
                sky_description = weatherData['weather'][0]['description']
                skyTypes = ['clear sky', 'few clouds','overcast clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain', 'thunderstorm','snow','mist']
                skyTypesTR = ['Güneşli', 'Az Bulutlu','Çok Bulutlu(Kapalı)', 'Alçak Bulutlu', 'Yer Yer Açık Bulutlu', 'Sağanak Yağmurlu', 'Yağmurlu', 'Gök Gürültülü Fırtına', 'Karlı', 'Puslu']
                for i in range(len(skyTypes)):
                    if sky_description == skyTypes[i]:
                        sky_description = skyTypesTR[i]
                temp = round((weatherData['main']['temp']-273.15), 1)
                feels_temp = round((weatherData['main']['feels_like']-273.15), 1)
                temp_min = round((weatherData['main']['temp_min']-273.15), 1)
                temp_max = round((weatherData['main']['temp_max']-273.15), 1)

                speak(f"{city_name}için hava durumu raporu, Gökyüzü:{sky_description}, Sıcaklık:{temp}, Hissedilen sıcaklık:{feels_temp}, Minimum sıcaklık:{temp_min}, Maximum Sıcaklık:{temp_max}")
                
                goodbye()
                

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")

def system_shut_down():
    global recognizer
    
    speak("Bilgisayarını kapat istediğine emin misin?")

    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                shutdown = recognizer.recognize_google(audio, language="tr-TR")
                shutdown = shutdown.lower()
                playsound("ending.mp3")
                if shutdown == 'hayır':
                   exit()
                else:
                    os.system("shutdown /s /t 1")           
             
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")

def create_alarm():
    global recognizer

    speak("Alarm saati?")

    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                zamanSaat = recognizer.recognize_google(audio, language="tr-TR")
                zamanSaat = zamanSaat.lower()
                playsound("ending.mp3")

                playsound("opening.mp3")
                speak("Alarm dakikası?")
                audio2 = recognizer.listen(mic)
                zamanDakika = recognizer.recognize_google(audio2,language="tr-Tr")
                zamanDakika = zamanDakika.lower()
                playsound("ending.mp3")

                speak("Alarmına bir isim ver.")
                
                playsound("opening.mp3")
                audio3 = recognizer.listen(mic)
                mesaj = recognizer.recognize_google(audio3, language="tr-Tr")
                mesaj = mesaj.lower()
                playsound("ending.mp3")

                
                speak(f"Saat {zamanSaat} {zamanDakika} için {mesaj} alarmını kuruyorum.")
                
                while True:
                    current_time = datetime.datetime.now()
                    alarm_zaman = str(current_time.hour) + ":" + str(current_time.minute)
                    
                    if alarm_zaman == str(zamanSaat)+ ":" + str (zamanDakika):
                        notification = ToastNotifier()
                        playsound('alarm.mp3')
                        notification.show_toast("Maviş Alarm", mesaj, duration=50)
                        break
                        
                    
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")



def antivirus():
    speak("Bilgisayarını tarıyorum.")
    
    # completed = subprocess.run(["powershell", "Start-MpScan"], capture_output=True)
    # return completed
    os.remove("output.txt")
    output = subprocess.run(["powershell", "Start-MpScan"], capture_output=True)
    output.stdout.decode("utf-8")
    file = open ("output.txt", "a+")
    file.write(str(output))
    file = open("output.txt", "r")
    for line in file.readlines():

        if ("returncode=0" in line):
            notification = ToastNotifier()
            playsound('antivirus.mp3')
            notification.show_toast("Maviş Antivirüs", "Bilgisayarınız korunuyor.", duration=50)
            
        else:
            notification = ToastNotifier()
            playsound('antivirus.mp3')
            notification.show_toast("Maviş Antivirüs", "Bilgisayarınız tehdit altında.", duration=50)
    
    goodbye()
def lock_screen():
    global recognizer

    ctypes.windll.user32.LockWorkStation()

def uygulama_ac():
    global recognizer
    
    speak("Senin için hangi uygulamayı açmamı istersin?")

    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                playsound("opening.mp3")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                uygulama_adi = recognizer.recognize_google(audio, language="tr-TR")
                uygulama_adi = uygulama_adi.lower()
                playsound("ending.mp3")
                if "valorant" in uygulama_adi:
                    os.startfile("C:\Riot Games\Riot Client\RiotClientServices.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                if "photoshop" in uygulama_adi:
                    os.startfile("C:\Program Files\Adobe\Adobe Photoshop 2021\photoshop.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                if "epic games" in uygulama_adi:
                    os.startfile("D:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                if "spotify" in uygulama_adi:
                    os.startfile("C://Users//OUTLIER//AppData//Local//Microsoft//WindowsApps//Spotify.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                if "discord" in uygulama_adi:
                    os.startfile("C://Users//OUTLIER//AppData//Local//Discord//app-1.0.9005//Discord.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                if "chrome" in uygulama_adi:
                    os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
                    speak(f"Senin için {uygulama_adi} adlı uygulamayı açıyorum.")
                    goodbye()
                    

                
                


                      
             
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speak("Anlayamadım")

recognizer = speech_recognition.Recognizer()
    

    