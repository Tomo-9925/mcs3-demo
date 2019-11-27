from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .sitemaps import *
from .feeds import *
from . import views


"""
# mainアプリの`urlpatterns`について

- IndexやNews，Worksページのビューにはキャッシュを有効にしています．
  - キャッシュの期間については`cache_timeout`の数値で設定してください．
- Sitemapについて
  - https://docs.djangoproject.com/ja/2.1/ref/contrib/sitemaps/
- Feedについて
  - https://docs.djangoproject.com/ja/2.1/ref/contrib/syndication/
"""


cache_timeout = 0 if settings.DEBUG else 15 * 60  # 15分間キャッシュを使用


# サイトマップの表示項目
sitemaps = {
    'index': IndexSitemap,
    'news_list': NewsListSitemap,
    'news_detail': NewsDetailSitemap,
    'work_list': WorkListSitemap,
}


urlpatterns = [
    path('', cache_page(cache_timeout)(views.IndexTemplateView.as_view()), name='index'),
    path('news/', cache_page(cache_timeout)(views.NewsListView.as_view()), name='news_list'),
    path('news/feed/', LatestNewsFeed(), name='news_feed'),
    path("news/amp/<slug:pk>/", cache_page(cache_timeout)(views.NewsAMPDetailView.as_view()), name='news_detail_amp'),
    path('news/<slug:pk>/', cache_page(cache_timeout)(views.NewsDetailView.as_view()), name='news_detail'),
    path('works/', cache_page(cache_timeout)(views.WorkRedirectView.as_view()), name='work_redirect'),
    path('works/feed/', LatestWorkFeed(), name='work_feed'),
    path('works/<int:year>/', cache_page(cache_timeout)(views.WorkListView.as_view()), name='work_list'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
