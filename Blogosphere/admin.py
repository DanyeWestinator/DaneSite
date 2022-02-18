from django.contrib import admin
from .models import BlogEntry, Tagline, RandomDaneFact

class BlogEntryAdmin(admin.ModelAdmin):
    fields = ["docs_url",
              "pub_date",
              "num_words",
              "blog_tags",
              "raw_text",
              "text_body"
              ]

admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Tagline)
admin.site.register(RandomDaneFact)

