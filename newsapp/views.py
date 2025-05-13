from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView
from config.custom_mixins import CheckUserLogin_and_Admin
from .forms import ContactForm, CommentForm
from .models import News, Category, Comment, NewsLike
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.translation import get_language
# def ListPageView(request):
#     news_list = News.published.all()
#     context = {
#         'news_list': news_list,
#     }
#     return render(request, 'news_list.html', context)
class ListPageView(View):
    pass
# @login_required
# def DetailPageView(request, slug):
#     # try:
#     #     news_detail = News.published.get(id=id)
#     # except News.DoesNotExist:
#     #     raise Http404('News not found')
#     news_detail = get_object_or_404(News, slug=slug, status=News.Status.Published)
#     comments = news_detail.comments.filter(active=True)
#     context = {
#         'news_detail': news_detail,
#         'comments': comments
#     }
#     return render(request, 'news_detail.html', context)
class DetailPageView(HitCountDetailView, LoginRequiredMixin, View):
    def get(self, request, slug):
        news_detail = get_object_or_404(News, slug=slug, status=News.Status.Published)
        likes_count = news_detail.likes.count()
        is_liked = news_detail.likes.filter(user=request.user).exists()
        comments = news_detail.comments.filter(active=True)#&
        hit_count = HitCount.objects.get_for_object(news_detail)
        hit_count_response = self.hit_count(request, hit_count)
        hit_count.refresh_from_db()
        coment_count = comments.count()

        comment_form = CommentForm()
        context = {
            'news_detail': news_detail,
            'comments': comments,
            'comment_form': comment_form,
            'hit_count_response': hit_count_response,
            'hit_count': hit_count,
            'coment_count':coment_count,
            'likes_count':likes_count,
            'is_liked': is_liked
        }
        return render(request, 'news_detail.html', context)
    def post(self, request, slug):
        news_detail = get_object_or_404(News, slug=slug, status=News.Status.Published)
        comments = news_detail.comments.filter(active=True)
        new_commnet = None
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_commnet = comment_form.save(commit=False)
            new_commnet.news = news_detail
            new_commnet.user = request.user
            new_commnet.save()
            return redirect('newsapp:detail_page', slug=news_detail.slug)
        context = {
            'news_detail': news_detail,
            'comments': comments,
            'new_commnet': new_commnet,
            'comment_form': comment_form,
        }
        return render(request, 'news_detail.html', context)


class NewsLikeView(View):
    def post(self, request, slug):
        news = get_object_or_404(News, slug=slug)
        try:
            is_liked = news.likes.get(news=news, user=request.user)
            is_liked.delete()
        except NewsLike.DoesNotExist:
            NewsLike.objects.create(news=news, user=request.user)
        return redirect('newsapp:detail_page', slug=news.slug)

def get_category_db(name_uz_val):
    category = Category.objects.filter(name_uz=name_uz_val).first()
    if not category:
        return News.objects.none()
    return News.objects.filter(category=category).order_by('-published_time')[:6]



class HomePageView(View):
    def get(self, request):
        categories = Category.objects.all()
        # print('categories', categories)
        current_language = get_language()
        # print('current_language', current_language)
        # print('categories', categories)
        newslist = News.published.all().order_by('-published_time')[:5]
        latest_newslist = News.published.all().order_by('-published_time')[:5]
        # local_news = News.published.filter(category__name='mahalliy').order_by('-published_time')[:6]
        # xorij_news = News.published.filter(category__name='Xorij').order_by('-published_time')[:6]
        # tehnologiya_news = News.published.filter(category__name='Tehnologiya').order_by('-published_time')[:6]
        # sport_news = News.published.filter(category__name='sport').order_by('-published_time')[:6]
        # xorij_news_one = News.published.filter(category__name='Xorij').order_by('-published_time').first()
        # tehnologiya_news_one = News.published.filter(category__name='Tehnologiya').order_by('-published_time').first()
        # sport_news_one = News.published.filter(category__name='sport').order_by('-published_time').first()
        local_news = get_category_db('mahalliy')
        xorij_news = get_category_db('Xorij')
        tehnologiya_news = get_category_db('Tehnologiya')
        sport_news = get_category_db('sport')
        xorij_news_one = get_category_db('Xorij').first()
        tehnologiya_news_one = get_category_db('Tehnologiya').first()
        sport_news_one = get_category_db('sport').first()
        context = {
            'news_list': newslist,
            'latest_newslist': latest_newslist,
            'categories': categories,
            'local_news': local_news,
            'xorij_news': xorij_news,
            'tehnologiya_news': tehnologiya_news,
            'sport_news': sport_news,
            'xorij_news_one': xorij_news_one,
            'tehnologiya_news_one': tehnologiya_news_one,
            'sport_news_one': sport_news_one,
        }
        return render(request, 'home.html', context)

#
# class ContactPageView(View):
#     def get(self, request):
#         return render(request, 'contact.html')
#

class ContactPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        forms_page = ContactForm()
        context = {
            'forms_page': forms_page,
        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        forms_page = ContactForm(request.POST)
        if forms_page.is_valid():
            forms_page.save()
            return HttpResponse("<h1>Sizning xaabringiz yetib keldi</h1>")
        else:
            context = {
                'forms_page': forms_page,
            }
            return render(request, 'contact.html', context)
            # return self.render_to_response(request)

def get_category_db_(name_uz_val):
    category = Category.objects.filter(name_uz=name_uz_val).first()
    if not category:
        return News.objects.none()
    return News.objects.filter(category=category).order_by('id')


###local news
class LocalNewsViews(ListView):
    model = News
    template_name = 'local_news.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        news = get_category_db_('mahalliy')
        page_size = self.request.GET.get("page_size", 2)
        pagegination = Paginator(news, page_size)
        page_number = self.request.GET.get("page")
        page_obj = pagegination.get_page(page_number)
        return page_obj

class TechnolgyNewsViews(ListView):
    model = News
    template_name = 'technolgy_news.html'
    context_object_name = 'technolgy_news_list'


    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Tehnologiya')
        return news

class XorijNewsViews(ListView):
    model = News
    template_name = 'xorij_news.html'
    context_object_name = 'xorij_news_list'


    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news

class SportNewsViews(ListView):
    model = News
    template_name = 'sport_news.html'
    context_object_name = 'sport_news_list'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='sport')
        return news

class UpdateNewsView(CheckUserLogin_and_Admin, UpdateView):
    model = News
    template_name = 'crud/update_news.html'
    fields = ['title','body', 'image', 'category', 'status',]

class DeleteNewsView(CheckUserLogin_and_Admin, DeleteView):
    model = News
    template_name = 'crud/delete_news.html'
    success_url = reverse_lazy('newsapp:home_page')

class CreateNewsView(CheckUserLogin_and_Admin, CreateView):
    model = News
    template_name = 'crud/create_news.html'
    fields = ['title', 'title_uz', 'title_en', 'title_ru',
              'body', 'body_uz', 'body_en', 'body_ru',
              'image', 'category', 'status']



class SearchListView(ListView):
    model = News
    template_name = 'seaching_list.html'
    context_object_name = 'searching_lists'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.published.all().filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    
class EditCommentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(instance=comment)
        context = {
            "comment": comment,
            'form':form
        }
        return render(request, 'edit_comment.html', context)
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('newsapp:detail_page', slug=comment.news.slug)
        context = {
            "comment": comment,
            'form': form
        }
        return render(request, 'edit_comment.html', context)

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'delete_confirm_comment.html'
    context_object_name = 'delete_comment'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return HttpResponse("Boshqalarning izohlarini o'chira olmaysiz")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('newsapp:detail_page', kwargs={'slug': self.object.news.slug})

