from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
from .models import Link

def scraper(request):
    if request.method == "POST":
        site = request.POST.get('site', '')

        if not site:
            return render(request, 'webScraper_app/result.html', {'error': 'No URL provided.'})

        try:
            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                Link.objects.create(address=link_address, name=link_text)

            return HttpResponseRedirect('/')
        except requests.exceptions.MissingSchema:
            return render(request, 'webScraper_app/result.html', {'error': 'Invalid URL format. Please include http:// or https://.'})
        except requests.exceptions.RequestException as e:
            return render(request, 'webScraper_app/result.html', {'error': f'Error fetching the URL: {e}'})
    
    else:
        data = Link.objects.all()

    return render(request, 'webScraper_app/result.html', {'data': data})


def clear(request):
    Link.objects.all().delete()
    return render (request, 'webScraper_app/result.html')