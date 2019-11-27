from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy

from .models import News, Work

# クラスベースビューの書き方について
# https://docs.djangoproject.com/ja/2.1/topics/class-based-views/


# トップページのビュー
class IndexTemplateView(generic.TemplateView):
  template_name = 'main/index.html'  # テンプレートのアドレス

  # テンプレートに送信するデータの編集
  def get_context_data(self, **kwargs):
    news_len = 5  # Newsの表示件数
    work_len = 4  # Workの表示件数
    work_years = Work.objects.values_list('published_at__year', flat=True).order_by('-published_at__year').distinct()
    work_years_len = 3  # Workの表示年数
    if len(work_years)<work_years_len:
      work_years_len = len(work_years)
    context = {
      'news_list': News.objects.filter(published_at__lt=timezone.now(), is_draft=False)[:news_len],
      'work_list': [ Work.objects.filter(published_at__lt=timezone.now(), published_at__year=year)[:work_len] for year in work_years[:work_years_len] ]  # 内包表記でワンライナーを極めよう！（白目）
    }
    return context


# ページネーションで表示する数値のリストを作成する関数
def get_paginate_range(context):
  num = 5  # 表示する数値の数（5以上はoverflow不可避）
  if context['paginator'].num_pages <= num:
    return context['paginator'].page_range
  else:
    range = [context['page_obj'].number]
    i = 1
    while len(range) < num :
      if 1 <= context['page_obj'].number-i :
        range.insert(0, context['page_obj'].number-i)
      if context['page_obj'].number+i <= context['paginator'].num_pages :
        range.append(context['page_obj'].number+i)
      i+=1
    return range


# ニュース一覧ページのビュー
class NewsListView(generic.ListView):
  model = News  # ビューで使用するモデル
  context_object_name = 'news_list'  # データベースから取得したデータの変数名
  allow_empty = False  # データがないとき404ページを表示
  paginate_by = 10  # 1ページの表示件数

  # データベースから取得するデータの編集
  def get_queryset(self):
    return super().get_queryset().filter(published_at__lt=timezone.now(), is_draft=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    range = get_paginate_range(context)  # 他に良い方法があれば書き換えてください…
    context.update({
      'title': 'NEWS (最新情報)',  # ページタイトル
      # 'description': '何かあれば',  # ページの説明
      # 'image': '何かあれば',  # ogイメージ
      'range': range,
    })
    return context


# ニュース詳細ページのビュー
class NewsDetailView(generic.DetailView):
  model = News

  def get_queryset(self):
    return super().get_queryset().filter(published_at__lt=timezone.now(), is_draft=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    title = context['news'].title
    description = context['news'].description.replace('\n','').replace('\r','')
    image = context['news'].image.url if context['news'].image else None
    context.update({
      'title': title,
      'description': description,
      'image': image,
    })
    return context

# AMP版ニュース詳細ページのビュー
class NewsAMPDetailView(NewsDetailView):
  template_name = "main/news_amp.html"  # テンプレートを変更する以外は継承（オブジェクト指向）


# ワークス最新の一覧ページへのリダイレクトビュー
class WorkRedirectView(generic.RedirectView):
  latest = Work.objects.latest('published_at').published_at.year
  url = reverse_lazy('main:work_list', kwargs={'year': latest})


# ワークス一覧ページのビュー
class WorkListView(generic.ListView):
  model = Work
  context_object_name = 'work_list'
  allow_empty = False

  def get_queryset(self):
    return super().get_queryset().filter(published_at__lt=timezone.now(), published_at__year=self.kwargs['year']).order_by('published_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'title': 'WORKS (制作実績)',
      # 'description': '何かあれば',
      # 'image': '何かあれば',
      'gettable_work_years': Work.objects.values_list('published_at__year', flat=True).order_by('-published_at__year').distinct(),
      'year_displayed': self.kwargs['year'],
    })
    return context


# 404ページのビュー
class Custom404TemplateView(generic.TemplateView):
  template_name = 'main/404.html'

  def get_context_data(self, **kwargs):
    context = {
      'title': 'お探しのページが見つかりませんでした。',
      # 'description': '何かあれば',
      # 'image': '何かあれば',
    }
    return context

  # ステータスコードの変更
  def get(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    return self.render_to_response(context, status=404)
