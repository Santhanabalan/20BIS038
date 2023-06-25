from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta,time
import requests

# Create your views here.

import requests

def get_authorization_token():
    url = "http://104.211.219.98/train/auth"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
	"companyName": "Train Hub",
	"clientID": "43557eee-a824-4597-a53f-7ad24ef19bc4",
	"clientSecret": "idgAfEcoSKFvxTVC",
	"ownerName": "Santhanabalan",
	"ownerEmail": "santhanabalan.20is@kct.ac.in",
	"rollNo": "20BIS038"
}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        auth_token = response.json().get("access_token")
        return auth_token
    else:
        print("Failed to get authorization token")
        return None


def get_train_schedules(request):
    url = "http://104.211.219.98/train/trains"
    auth_token = get_authorization_token()

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)
    trains = response.json()

    current_time = datetime.now().time()
    current_datetime = datetime.combine(datetime.today(), current_time)
    min_departure_time = current_datetime + timedelta(minutes=30)
    trains = [
        train for train in trains if
        datetime.strptime(
            "{:02d}:{:02d}:{:02d}".format(
                train.get('departureTime', {}).get('Hours', 0),
                train.get('departureTime', {}).get('Minutes', 0),
                train.get('departureTime', {}).get('Seconds', 0),
            ),
            '%H:%M:%S'
        ).time() > min_departure_time.time()
    ]
    trains = [train for train in trains if train.get('departureTime', {}).get('Minutes', 0) >= 30]

    trains = sorted(trains, key=lambda x: (x.get('price', {}).get('sleeper', 0), x.get('seatsAvailable', {}).get('sleeper', 0), -x.get('departureTime', {}).get('Hours', 0), -x.get('departureTime', {}).get('Minutes', 0), -x.get('departureTime', {}).get('Seconds', 0)))

    return JsonResponse({'trains': trains}, safe=False)
