from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import News, Category
# def ListPageView(request):
#     news_list = News.published.all()
#     context = {
#         'news_list': news_list,
#     }
#     return render(request, 'news_list.html', context)
class ListPageView(View):
    pass
def DetailPageView(request, id):
    # try:
    #     news_detail = News.published.get(id=id)
    # except News.DoesNotExist:
    #     raise Http404('News not found')
    news_detail = get_object_or_404(News, id=id, status=News.Status.Published)
    context = {
        'news_detail': news_detail,
    }
    return render(request, 'news_detail.html', context)


class HomePageView(View):
    def get(self, request):
        news_list = News.published.all()
        categories = Category.objects.all()
        context = {
            'news_list': news_list,
            'categories': categories,
        }
        return render(request, 'home.html', context)

class ContactPageView(View):
    def get(self, request):
        return render(request, 'contact.html')