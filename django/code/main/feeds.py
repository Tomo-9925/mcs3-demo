from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import *


class LatestNewsFeed(Feed):
  title = 'Media Creative Supporter - NEWS'
  link = reverse_lazy('main:news_list')
  description = 'Media Creative Supporterから最新ニュースをお届けします。'

  def items(self):
    return News.objects.filter(published_at__lt=timezone.now(), is_draft=False)[:8]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.description

  def item_pubdate(self, item):
    return item.published_at

  def item_link(self, item):
    return reverse('main:news_detail', args=[item.pk])+'?utm_source=feed'

  def item_copyright(self, item):
    return "(c) " + str(timezone.now().year) + ' Media Creative Supporter'


class LatestWorkFeed(Feed):
  latest_year = Work.objects.latest('published_at').published_at.year
  title = 'Media Creative Supporter - WORKS'
  link = reverse_lazy('main:work_list', args=[latest_year])
  description = 'Media Creative Supporterから最新映像をお届けします。'

  def items(self):
    return Work.objects.filter(published_at__lt=timezone.now())[:8]

  def item_title(self, item):
    return item.title

  def item_pubdate(self, item):
    return item.published_at

  def item_link(self, item):
    return reverse('main:work_list', args=[item.published_at.year])+'?utm_source=feed'

  def item_copyright(self, item):
    return "(c) " + str(timezone.now().year) + ' Media Creative Supporter'
