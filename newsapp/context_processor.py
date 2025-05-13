from .models import News, Category

def latest_news(request):
    lates_news_list = News.published.all().order_by('-published_time')[:5]
    categories = Category.objects.all()

    context = {
        'lates_news_list': lates_news_list,
        'categories': categories
    }
    return context