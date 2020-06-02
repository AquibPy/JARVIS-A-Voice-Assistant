import pywhatkit as kit
phNo = input('Enter Mobile number with country code')
msg = input('enter msg')
hour = int(input('enter the hour'))
minute = int(input('enter the min'))
kit.sendwhatmsg(phNo,msg,hour,minute)