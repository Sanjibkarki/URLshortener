from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.core.cache import cache
import random
import requests

from urllib.parse import urlparse

symbols = "abcdefghijklmnopqrstuvwxyz1234567890"

class Index(View):
    def get(self, request):
        base_url = f"{request.scheme}://{request.get_host()}"
        return render(request, "index.html")

    def post(self, request):
        urlPath = request.POST.get('url')
        urlname = ""
        for i in range(5):
            ran = random.choice(symbols)
            urlname += ran

        urlname = f"http://127.0.0.1:8000/{urlname}"

        try:
            response = requests.get(urlPath)
            if response.status_code == 404:
                return render(request, 'index.html', context={"error": "The Page does not exist"})
        except requests.exceptions.RequestException:
            return render(request, 'index.html', context={"error": "Invalid URL or failed request"})

        cache.set(urlname, urlPath, timeout=120)
        return render(request, "urlpage.html", context={'urlpath': urlname})

class URL(View):
    def get(self, request, slug):
        base_url = f"{request.scheme}://{request.get_host()}"
        base_url = base_url+"/"+slug
        urlPath = cache.get(base_url)
        if urlPath:
            return redirect(urlPath)  
        else:
            return HttpResponse("Sorry, this shortened URL does not exist.")
