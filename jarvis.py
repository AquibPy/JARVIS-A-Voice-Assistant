import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import pyowm
import numpy as np
import matplotlib.pyplot as plt
import cv2
import subprocess
import speedtest
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
import pywhatkit as kit
from googletrans import Translator
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import youtube_dl
from PIL import ImageGrab



engine = pyttsx3.init('sapi5')  # windows inbuilt voices
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# rate = engine.getProperty('rate')
# newrate = 130
# engine.setProperty('rate',newrate)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning!')
    elif hour >= 12 and hour < 18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening')
    speak("Hello!!! I am Jarvis. How can i help you")


def NewsFromBBC():
    main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=72bbae4d6dca4b3f8dfab5d7e8f87f3e"
    open_bbc_page = requests.get(main_url).json()
    article = open_bbc_page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])
    for i in range(len(results)):
        print(i + 1, results[i])


def sketch(image):
    # convert image to gray scale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Clean up image using gaussian blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # extract edges
    canny_edges = cv2.Canny(img_gray_blur, 20, 50)
    # do an invert binarize the image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask


def takeCommand():
    # it takes microphone input from user and return string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.non_speaking_duration=0.6
        # r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        # language='en-in'
        print(f"User said: {query}\n")

    except Exception as e:
        print('Say it again please...')
        return 'None'
    return query

def Translate():
    speak('what should i translate??')
    sentence = takeCommand()
    trans = Translator()
    trans_res = trans.translate(sentence,src='en',dest='fr')
    print(trans_res.text)
    speak(trans_res.text)


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        # logic for executing task based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)  # sentences: kitne sentences chaiye
            speak('According to Wikipedia')
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open('youtube.com')

        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')

        elif ('play music') in query:
            music_dir = 'E:\\MCA\\Python\\JARVIS AI\\Music'
            songs = os.listdir(music_dir)
            # list dir meri directory ki sari file ko list krlga
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"The time is {strTime}")
        elif 'open code' in query:
            codePath = "C:\\Users\\mohda\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'my location' in query:
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            city = data['city']
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            print("Latitude : ", latitude)
            print("Longitude : ", longitude)
            print("City : ", city)
            speak('your latitude is' + latitude)
            speak('your longitude is' + longitude)
            speak("your city is" + city)
        elif 'temperature' in query:
            owm = pyowm.OWM('6508d855eb9cf52ea4f4ff85f17ce548')
            location = owm.weather_at_place('Aligarh')
            weather = location.get_weather()
            temp = weather.get_temperature('celsius')  # temp ek dictionary hai
            a = temp['temp']
            b = temp['temp_max']
            c = temp['temp_min']
            humidity = weather.get_humidity()
            print(f"Temperature in Celsius:{a} celsius")
            print(f"Maximum Temperature:{b} celsius")
            print(f"Minimum Temperature:{c} celsius")
            print(f"Humdity:{humidity}%")
            speak('the current temperature report is')
            speak(f"{a}degree celsius")
            speak(f"humidity is {humidity}%")

        elif 'sin vs cos' in query:
            x = np.linspace(-2 * np.pi, 2 * np.pi, 50000)
            sin = np.sin(x)
            cos = np.cos(x)
            plt.plot(x, sin, x, cos)
            plt.title('Graph of Trigonometric Function')
            plt.xlabel('X value from -2pi to 2pi')
            plt.ylabel('Graph of sin(x) vs cos(x)')
            speak('here it is sin vs cos graph')
            plt.legend(['Sin', 'Cos'])
            plt.show()

        elif 'periodic table' in query:
            webbrowser.open_new_tab('http://mendeleev.herokuapp.com/')
        elif 'news' in query:
            speak('top 10 trending news are here')
            NewsFromBBC()
        elif 'motion detector' in query:
            speak('opening motion detector')
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = ""

            color = (0, 0, 255)  # BGR

            cap = cv2.VideoCapture(0)  # 0 means first webcam

            frames = []
            counter = 0

            threshold = 1

            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame,
                                    cv2.COLOR_BGR2GRAY)  # converts captured frame to Grayscale for easier analysis

                frames.append(gray)
                cv2.putText(frame, text, (5, 30), font, 1, color, 3, cv2.LINE_AA)  # may need to change some arguments

                cv2.imshow('Motion Detector', frame)

                if counter > 0:
                    difference = cv2.subtract(cv2.medianBlur(frames[counter], 15),
                                              cv2.medianBlur(frames[counter - 1], 15))
                    # applies median blur before subtracting for noise reduction
                    # cv2.imshow('difference',difference)
                    mean = np.mean(difference)
                    # print(mean)
                    if mean > threshold:
                        text = "Motion Detected"
                    else:
                        text = ""

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press q to quit video capture
                    break

                counter = counter + 1
            cap.release()
            cv2.destroyAllWindows()
        elif 'live sketcher' in query:
            speak('opening live sketcher')
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Live Sketcher', sketch(frame))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        elif 'wifi password' in query:
            a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
            a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
            for i in a:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', i, 'key=clear']).decode(
                    'utf-8').split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    print("{:<30}| {:<}".format(i, results[0]))
                except IndexError:
                    print("{:<30}| {:<}".format(i, ""))
        elif 'speed test' in query:
            st = speedtest.Speedtest()
            option = int(input('''What speed do you want to test:
            1. Downloading Speed
            2. Upload Speed
            3. Ping
            Your Choice: '''))
            if option == 1:
                print(st.download())
            elif option == 2:
                print(st.upload())
            elif option == 3:
                servernames = []
                st.get_servers(servernames)
                print(st.results.ping)
            else:
                print("Invalid Choice!!!")
        elif 'service provider' in query:
            speak('Enter Mobile Number with Country Code')
            mobileNo = input('Enter Mobile Number with Country Code:')
            service = phonenumbers.parse(mobileNo)
            output = carrier.name_for_number(service,'en')
            loc = geocoder.description_for_number(service,'en')
            speak("Your Service Provider is "+output)
            speak('location of this number is'+ loc)
            print(output)
            print(loc)
        elif 'whatsapp' in query:
            speak('Enter Mobile Number with Country Code')
            phNo = input('Enter Mobile Number with Country Code:')
            speak('Enter your message please')
            msg = input('enter msg')
            speak('enter the hour at which you want to send message')
            hour = int(input('enter the hour'))
            speak('enter the minute at which you want to send message')
            minute = int(input('enter the min'))
            speak('thank you sir!!! i will send this message within a minute')
            kit.sendwhatmsg(phNo,msg,hour,minute)
        elif 'translate' in query:
            Translate()
        elif 'youtube downloader' in query:
            root=tk.Tk()
            root.title('Youtube downloader V-2.1')
            root.geometry("350x140")
            root.config(bg='#dfe6e9')
            ydl_opts = {}
            def shutcom():
                global key
                key=0
                buttonshut = tk.Button(root, text="yes", command=shutcom,state=DISABLED,bg='#dfe6e9',fg= '#f2f2f2')
                buttonshut.grid(row=4, column=1)
            def download(link):
                link_of_the_video = link
                zxt = link_of_the_video.strip()
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([zxt])


            def downloadall():
                for i in range(4):
                    if i==0 :
                        if text1.get()!='paste link 1 here...':
                            pro1.start()
                            download(text1.get())
                            pro1.destroy()
                            lable1=Label(root,text='completed!').grid(row=0,column=1)
                            
                    if i==1:

                        if text2.get() != 'paste link 2 here...':
                            
                            pro2.start()
                            
                            download(text2.get())
                            pro2.destroy()
                            lable2 = Label(root, text='completed!').grid(row=1, column=1)

                    if i==2:
                        if text3.get() != 'paste link 3 here...':
                            
                            pro3.start()
                            
                            download(text3.get())
                            pro3.destroy()
                            lable3 = Label(root, text='completed!').grid(row=2, column=1)

                    if i==3:
                        if text4.get() != 'paste link 4 here...':
                            
                            pro4.start()
                            
                            download(text4.get())
                            pro4.destroy()
                            lable4 = Label(root, text='completed!').grid(row=3, column=1)


                if key==0:
                    os.system("shutdown /s /t 1")


            key=1
            text1=tk.Entry(root,width=50,bg='#dfe6e9',fg='#0984e3')
            text2=tk.Entry(root,width=50,bg='#dfe6e9',fg='#0984e3')
            text3=tk.Entry(root,width=50,bg='#dfe6e9',fg='#0984e3')
            text4=tk.Entry(root,width=50,bg='#dfe6e9',fg='#0984e3')

            text1.insert(string='paste link 1 here...',index=1)
            text2.insert(string='paste link 2 here...',index=1)
            text3.insert(string='paste link 3 here...',index=1)
            text4.insert(string='paste link 4 here...',index=1)
            button=tk.Button(root,text='download all',command=downloadall,bg='#dfe6e9',fg= '#0984e3')
            button.config(highlightbackground='#f2f2f2')
            shutlabel=tk.Label(root,text="do you want to shutdown after all downloads:",bg='#dfe6e9',fg= '#0984e3')
            buttonshut=tk.Button(root ,text="yes",command=shutcom,bg='#dfe6e9',fg= '#0984e3')

            text1.grid(row=0,column=0,columnspan=2)
            text2.grid(row=1,column=0,columnspan=2)
            text3.grid(row=2,column=0,columnspan=2)
            text4.grid(row=3,column=0,columnspan=2)
            button.grid(row=5,column=0)
            shutlabel.grid(row=4,column=0)
            buttonshut.grid(row=4,column=1)

            pro1=Progressbar(root,length = 100,orient=HORIZONTAL,mode='indeterminate')
            pro1.grid(row=0,column=1)
            pro2=Progressbar(root,length = 100,orient=HORIZONTAL,mode='indeterminate')
            pro2.grid(row=1,column=1)
            pro3=Progressbar(root,length = 100,orient=HORIZONTAL,mode='indeterminate')
            pro3.grid(row=2,column=1)
            pro4=Progressbar(root,length = 100,orient=HORIZONTAL,mode='indeterminate')
            pro4.grid(row=3,column=1)

            root.mainloop()
        
        elif 'screen recorder' in query:
            speak('Opening Screen Recorder')
            #four character code object for video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi',fourcc,5.0,(1920,1080))

            while True:
                img = ImageGrab.grab()
                img_np = np.array(img)

                frame = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
                cv2.imshow('Screen',frame)
                out.write(frame)

                if cv2.waitKey(1) == ord('q'):
                    break
                        
            