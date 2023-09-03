from django.contrib import sitemaps
from django.urls import reverse

class SpammersViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['email_list', 'home']

    def location(self, item):
        return reverse(item)
