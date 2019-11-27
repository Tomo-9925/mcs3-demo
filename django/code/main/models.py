from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit
from django.core.cache import cache

validate_video_id = RegexValidator(regex=r'^[\w-]{11}$', message='YouTubeの動画IDが適切な形ではありません。')

class News(models.Model):
  permalink = models.SlugField('パーマリンク (アドレス名)', max_length=50, primary_key=True, unique=True)
  title = models.CharField('投稿タイトル', max_length=100)
  description = models.TextField('説明', blank=True, null=True)
  content = MarkdownxField('本文 (Markdown形式)')
  # .containerの最大幅x2, Google構造化データ用
  image = ProcessedImageField(verbose_name='画像',
                              blank=True, null=True,
                              upload_to='main/news/',
                              processors=[ResizeToFit(1900, 1900)],
                              format='JPEG',
                              options={'quality': 85})
  # .containerの最大幅
  image_large = ImageSpecField(source='image',
                                processors=[ResizeToFit(950, 950)],
                                format='JPEG',
                                options={'quality': 85})
  # SPのメイン画像，PCのサムネイル画像
  image_medium = ImageSpecField(source='image',
                                processors=[ResizeToFit(350, 350)],
                                format='JPEG',
                                options={'quality': 75})
  # SPのサムネイル画像
  image_small = ImageSpecField(source='image',
                               processors=[ResizeToFit(150, 150)],
                               format='JPEG',
                               options={'quality': 60})
  published_at = models.DateTimeField('投稿公開日', default=now)
  is_draft = models.BooleanField('下書き', default=False)
  created_at = models.DateTimeField('投稿作成日', auto_now_add=True)
  updated_at = models.DateTimeField('投稿更新日', auto_now=True)

  def __str__(self):
    return self.title

  def formatted_markdown(self):
    return markdownify(self.content)

  # 保存時に実行
  def save(self, force_insert=False, force_update=False):
    super().save(force_insert, force_update)
    try:
      cache.clear()  # キャッシュをクリア
      # ping_google()  # Googleにサイトマップを送信
    except Exception:
      pass

  class Meta:
    verbose_name_plural = "News"
    ordering = ('-is_draft', '-published_at', 'title')


class Work(models.Model):
  video_id = models.SlugField('YouTubeの動画ID', max_length=11, primary_key=True, unique=True, validators=[validate_video_id])
  title = models.CharField('動画タイトル', max_length=100)
  published_at = models.DateTimeField('動画投稿日', default=now)
  created_at = models.DateTimeField('情報登録日', auto_now_add=True)
  updated_at = models.DateTimeField('情報更新日', auto_now=True)

  def __str__(self):
    return self.title

  def thumbnail(self):
    url = "https://img.youtube.com/vi/" + self.video_id + "/"
    size = {
      "defalt": url + "default.jpg",  # 120x90
      "mq": url + "mqdefault.jpg",  # 320x180
      "hq": url + "hqdefault.jpg",  # 480x360
      "sd": url + "sddefault.jpg",  # 640x480
      "hd": url + "maxresdefault.jpg"  # 1280x720 or 1920x1080 ...
    }
    return size

  def url(self):
    return "https://youtu.be/" + self.video_id

  def save(self, force_insert=False, force_update=False):
    super().save(force_insert, force_update)
    try:
      cache.clear()
      # ping_google()
    except Exception:
      pass

  class Meta:
    ordering = ('-published_at', 'title')
