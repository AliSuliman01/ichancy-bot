import requests
import json
import time
import random

cookie = "PHPSESSID_3a07edcde6f57a008f3251235df79776a424dd7623e40d4250e37e4f1f15fadf=86b702a44b9ac825520ec5452da41508; languageCode=en_GB; language=English%20%28UK%29; __cf_bm=KDpBUc3Bakv9EE2v59QydUvlxt6iUj3_WSyw9P6frjs-1757110334-1.0.1.1-ASvn1PeGGNTlP.9t0CgrFDg9pgeLb.5FEl.klEjkLKNnCwMKSToBNhw05ZQRx1Yjk.au4oiZgG0sQ4Jl7Z7p5fGU67aP.Ps0Zdy4bf4V8B0; cf_clearance=GBZEf8152k45GcKK6uIfEDmHte5kp9CZbEh21gUZ0BY-1757110409-1.2.1.1-fGXq8h83p1Y_.Wd4iGkksANmsEPiZp1Us.g9e_yAUOFJjs3Jec2MwIJI8OaDje6qaXN3rRSWFmZrIgUCQ4qfDESLvocTkGrg8yUb0gklyNuk.fwolDJfVP7uoDsvxYlcD6eDKDzvlf.rrd5xOYrrDsV3rbW.uRwHo1IMPBSx89MmTuNl1MJCCv8tC_M6uu5IVAXmrd.0ktQzy0ZxSM8VYJbx4jEmW7PTLz5Cxx3IHZs"

def get_players_statistics_pro():
    url = "https://agents.ichancy.com/global/api/Statistics/getPlayersStatisticsPro"

    payload = {}
    headers = {
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://agents.ichancy.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agents.ichancy.com/dashboard',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.184"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Google Chrome";v="138.0.7204.184"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code
        


def get_data():
    url = "https://agents.ichancy.com/global/api/core/getData"

    payload = {}
    headers = {
    'Content-Type': 'application/json',
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def get_agent_wallet():
    url = "https://agents.ichancy.com/global/api/Agent/getAgentWallet"

    payload = {}
    headers = {
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://agents.ichancy.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agents.ichancy.com/dashboard',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.184"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Google Chrome";v="138.0.7204.184"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def get_total_unread_messages_count():
    url = "https://agents.ichancy.com/global/api/Message/getTotalUnreadMessagesCount"

    payload = {}
    headers = {
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://agents.ichancy.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agents.ichancy.com/dashboard',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.184"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Google Chrome";v="138.0.7204.184"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def get_all_user_notifications():
    url = "https://agents.ichancy.com/global/api/UserNotification/getAllUserNotifications"

    payload = {
        "start": 0,
        "limit": 6,
        "filter": {}
    }
    headers = {
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://agents.ichancy.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agents.ichancy.com/dashboard',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.184"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Google Chrome";v="138.0.7204.184"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def get_sub_agent_statistics():
    url = "https://agents.ichancy.com/global/api/Statistics/getSubAgentStatistics"

    payload = {
        "start": 0,
        "limit": 10,
        "filter": {
            "currency": {
                "action": "=",
                "value": "multi",
                "valueLabel": "multi"
            }
        }
    }
    headers = {
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://agents.ichancy.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://agents.ichancy.com/dashboard',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.184"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Google Chrome";v="138.0.7204.184"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


start_time = time.time()

try:
    while True:
        # Randomly select one of the methods
        methods = [
            get_data,
            get_players_statistics_pro,
            get_agent_wallet,
            get_total_unread_messages_count,
            get_all_user_notifications,
            get_sub_agent_statistics
        ]
        
        selected_method = random.choice(methods)
        method_name = selected_method.__name__
        
        print(f"Calling {method_name}...")
        stats = selected_method()
        
        if stats != 200:
            print(f"{method_name} returned status code: ", stats)
            break
            
        # Sleep for random seconds less than 10
        sleep_time = random.uniform(1, 10)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
        
except Exception as e:
    print("Error: ", e)

end_time = time.time()
print("Time taken: ", end_time - start_time)


