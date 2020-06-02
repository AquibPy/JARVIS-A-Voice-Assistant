import speech_recognition as sr
r1 = sr.Recognizer()
r2 = sr.Recognizer()
print('listen..')
with sr.Microphone() as source:
    audio = r1.listen(source)
    query=r1.recognize_google(audio,language='eng-in')
    print(query)
# with sr.Microphone() as source:
#     audio = r2.listen(source)
#     query1 =r2.recognize_google(audio,language='eng-in')
#     print(query1)
    
# add = query +query1
# print(add)    
