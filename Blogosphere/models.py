from django.db import models
from datetime import date
from . import GoogleDocScraper as GDS

class BlogEntry(models.Model):
    #Data fields
    blog_title = models.CharField(max_length=200, blank=True, null=True)
    pub_date = models.DateField("Date Published", null=True, blank=True)
    num_words = models.IntegerField("Number of Words", null=True, blank=True)
    blog_tags = models.TextField("Comma seperated tags", null=True, blank=True)
    raw_text = models.TextField("Plain document text", null=True, blank=True)
    text_body = models.TextField("Raw HTML", null=True, blank=True)
    docs_url = models.TextField("Docs URL code", null=True)
    style = ""

    def save(self, *args, **kwargs):
        print("Save logic here!")
        self.pub_date = date.today()

        if str(self.docs_url).startswith("https://docs.google.com/document/d/"):
            self.docs_url = str(self.docs_url).replace("https://docs.google.com/document/d/", "")
        url_split = [i for i in str(self.docs_url).split("/") if i.__contains__("edit") == False]
        url = url_split[0]
        print(url)
        GDS.download_google_doc(url)
        parsed = GDS.parse_blog()
        self.docs_url = url
        self.blog_title = parsed["TITLE"]
        self.num_words = parsed["WORD_COUNT"]
        self.raw_text = parsed["CLEAN"]
        self.text_body = parsed["RAW_HTML"]
        self.style = parsed["STYLE"]
        super(BlogEntry, self).save(*args, **kwargs)
        #print(self.raw_text)

    def __html__(self, html = ""):
        #no logic on when no override given
        if (html == ""):
            return html
        total_posts = str(len(BlogEntry.objects.all()))
        html = html.replace("TOTAL_POSTS", total_posts)
        total_words = sum([entry.num_words for entry in BlogEntry.objects.all()])

        html = html.replace("TOTAL_WORDS", str(total_words))
        html = html.replace("Title Here!", self.blog_title)
        # TODO helper function to pretty up the date
        date = str(self.pub_date)
        html = html.replace("FORMATTED DATE", date)
        word_count = str(self.num_words)
        html = html.replace("WORD_COUNT", word_count)
        body = self.text_body
        html = html.replace("The main body here!", body)
        return html


    def __str__(self):
        string = f"{self.blog_title}\n\t" \
                 f"Pub date: {self.pub_date}\n\t" \
                 f"Words: {self.num_words}"
        return string

class Tagline(models.Model):
    tagline = models.TextField("Tagline", null=True, blank=True)
    date = models.DateField("Date added" , null=True, blank=True)

    def __str__(self):
        return str(self.tagline)


class RandomDaneFact(models.Model):
    fact = models.TextField("Fact", null=True, blank=True)
    source = models.TextField("Source link", null=True, blank=True)

    def __str__(self):
        return str(self.fact)