from datetime import datetime
import requests ,math
print(int(datetime.timestamp(datetime.now()))-1)


response = requests.get(f"""
https://sp-today.com/app_api/cur_damascus.json?{int(datetime.timestamp(datetime.now()))-1}""" )
USDDAM = None
for row in response.json():
    if row['name'] == "USD":
        USDDAM = row['bid']

print(USDDAM)
response = requests.get(f"""
https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT""")

print(float(response.json()['price'])*float(USDDAM) + 100.0 +100.0)
x = math.ceil((float(response.json()['price'])*float(USDDAM) + 100.0 +100.0))
while x %100 !=0:
    x-=1
print(x)
