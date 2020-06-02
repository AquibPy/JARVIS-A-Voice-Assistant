import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder

mobileNo = input('Enter Mobile Number with Country Code:')
service = phonenumbers.parse(mobileNo)
print(carrier.name_for_number(service,'en'))
loc = geocoder.description_for_number(service,'en')
print(loc)