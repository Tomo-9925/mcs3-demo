from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import *


class IndexSitemap(Sitemap):
  priority = 1.0
  protocol = 'https'

  def items(self):
    return ['index']

  def location(self, item):
    return reverse('main:index')

  def lastmod(self, item):
    latest_news_date = News.objects.filter(published_at__lt=timezone.now(), is_draft=False).latest('updated_at').updated_at
    latest_work_date = Work.objects.filter(published_at__lt=timezone.now()).latest('updated_at').updated_at
    return max(latest_work_date, latest_news_date)


class NewsListSitemap(Sitemap):
  priority = 0.8
  protocol = 'https'

  def items(self):
    return ['news_list']

  def location(self, item):
    return reverse('main:news_list')

  def lastmod(self, item):
    return News.objects.latest('updated_at').updated_at


class WorkListSitemap(Sitemap):
  priority = 0.8
  protocol = 'https'

  def items(self):
    return Work.objects.values_list('published_at__year', flat=True).filter(published_at__lt=timezone.now()).order_by('-published_at__year').distinct()

  def location(self, item):
    return reverse('main:work_list', kwargs={'year': item})

  def lastmod(self, item):
    return Work.objects.filter(published_at__year=item).latest('updated_at').updated_at


class NewsDetailSitemap(Sitemap):
  priority = 0.6
  protocol = 'https'

  def items(self):
    return News.objects.filter(published_at__lt=timezone.now(), is_draft=False)

  def location(self, item):
    return reverse('main:news_detail', args=[item.pk])

  def lastmod(self, item):
    return item.updated_at
