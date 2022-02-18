from django.test import TestCase
from .models import BlogEntry

# Create your tests here.
class BlogTests(TestCase):
    #tests start with test_
    def test_all_have_titles(self):
        #Returns false for blog entries whose title is ""
        blogs = BlogEntry.objects.all()
        i = 0
        for blog in blogs:
            print(blogs)
            title = str(blog.blog_title).strip()
            msg = f"{i} had a blank title"
            self.assertNotEqual(title, "", msg)
            i += 1
        #blank_title = ""

