from django.shortcuts import render
import requests

# Create your views here.


def index(request):
    url = 'https://www.avito.ru/web/6/user/167e9ed21083de7ccd4230e5dda1fc4d/ratings?summary_redesign=1'
    response = requests.get(url).json()['entries']
    feedback = {
        'score': response[0]['value']['score'],
        'review_count': response[0]['value']['reviewCount'],
        'reviews': [
            {
                'name': review['value']['title'],
                'avatar': review['value']['avatar'],
                'text': review['value']['textSections'][0]['text'],
                'score': range(review['value']['score']),
                'rated': review['value']['rated'],
            }

            for review in response[2:]]
    }
    return render(request, 'main/index.html', feedback)
