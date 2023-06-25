from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests

# Create your views here.
def home(request):
    return HttpResponse("Number Management HTTP Microservice")

def get_numbers(request):
    urls = request.GET.getlist('url')
    numbers = []

    for url in urls:
        try:
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                numbers.extend(data['numbers'])
        except requests.exceptions.RequestException:
            continue

    numbers = sorted(set(numbers))

    return JsonResponse({'numbers': numbers}, safe=False)