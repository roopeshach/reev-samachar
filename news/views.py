from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from bs4 import BeautifulSoup as bs
from .models import News
from .forms import NewsForm
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from facebook_scraper import get_posts


def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    host_url = "https://ekantipur.com"
    url = host_url + "/news"
    content = session.get(url, verify=False).content
    soup = bs(content, "html.parser")
    all_news = soup.find_all("article", {"class": "normal"})
    for news in all_news:
        n = NewsForm(
            {
                "title": news.find("h2").text,
                "url": news.find("a")["href"],
                "image": news.find("img")['data-src'],
            }

        )
        if n.is_valid():
            n = n.save()
            single_news = single_news_scrape(request, n.id)
            n.title = single_news["title"]
            n.description = single_news["description"]
            n.date = single_news["date"]
            n.author = single_news["author"]
            n.save()
        else:
            print(n.errors)
    return redirect("/news")
            


def news(request):
    news = News.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(news, 5)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, "news/news.html", {"news": news})


def single_news(request, id):
    news = News.objects.get(id=id)
    return render(request, "news/single_news.html", {"news": news})

def single_news_scrape(request,  id ) :
    news = News.objects.get(id=id)
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    host_url = "https://ekantipur.com"
    url = host_url + news.url
    print(url)
    content = session.get(url, verify=False).content
    soup = bs(content, "html.parser")
    
    news = {}
    #get title inside article-header > h1
    news["title"] = soup.find("div", {"class": "article-header"}).find("h1").text
    #get all p inside description div 
    all_p = soup.find("div", {"class": "description"}).find_all("p")
    #get html of all p and h3 and store in news["description"]
    news["description"] = ""
    for p in all_p:
        if p.find("strong"):
            news["description"] += p.prettify()
        else:
            news["description"] += p.prettify()
    
    #get time inside time tag
    news["date"] = soup.find("time").text
    #get author inside author class span > a 
    news["author"] = soup.find("span", {"class": "author"}).find("a").text

    return news


def facebook_details(request):
    for post in get_posts('nepalpolice', pages=1, cookies='cookies.txt'):
        print(post)
    
    return JsonResponse({"message": "success"})