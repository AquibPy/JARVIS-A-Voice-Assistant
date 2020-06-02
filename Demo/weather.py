import pyowm
owm = pyowm.OWM('6508d855eb9cf52ea4f4ff85f17ce548')
location = owm.weather_at_place('Aligarh')
weather= location.get_weather()
temp = weather.get_temperature('celsius')
# print(temp)
# print(temp['temp'],temp['temp_max'],temp['temp_min'])
humid = weather.get_humidity()
print(humid)
