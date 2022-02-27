from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BlogEntry, Tagline
from django.template import loader
import random

from django.http import Http404
import re

def Homepage(request):
    template = loader.get_template("SiteTemplates/Homepage.html")

    context = {
        #put plain text replacements here
    }
    render = str(template.render(context, request))
    #Use str.replace() for any text with html data, template.render doesn't like it
    response = HttpResponse(render)

    return response


def EntryHomepageLine(entry, id):
    line = ""
    title = str(entry.blog_title)
    title = f"<a href=\"{id}\">" + title + "</a>"
    date = format_date(str(entry.pub_date))
    words = str(entry.num_words)
    tags = str(entry.blog_tags)
    line += f"{str(id + 1)}) {title} {date}. {words} words. Tags: {tags}<br />"
    return line
def BlogosphereHome(request):
    template = loader.get_template("SiteTemplates/BlogosphereMainPage.html")
    html = "The main body here!"
    words = get_total_words()
    total = words[0]
    posts = words[1]
    title = "Latest entry: "
    entries = BlogEntry.objects.all()
    id = len(entries) - 1
    #id = 0
    latest = entries[id]
    style = str(latest.style)
    title += str(latest.blog_title)
    # control for ellipses
    title = title.replace("...", "")
    title += "..."
    cent = str(latest.text_body)
    #just get the first paragraph
    html = cent
    word_count = str(latest.num_words)
    lines = "<br />"
    i = 0
    for i in range(len(entries)):
        j = len(entries) - i - 1
        entry = entries[j]
        lines += EntryHomepageLine(entry, j)
    i = 0
    for i in range(len(html)):
        if html[i : i + 4] == "</p>":
            html = html[:i]
            break
    #gets the list of all possible taglines
    taglines = Tagline.objects.all()
    tagline = str(taglines[random.randint(0, len(taglines) - 1)])
    context = {
        "TOTAL_WORDS" : total,
        "TOTAL_POSTS" : posts,
        "DATE" : format_date(str(latest.pub_date)),
        "NUM_WORDS" : word_count,
        #"TEXT_HTML" : html,
        "TITLE" : title,
        "ID" : str(id),
        "TAGLINE" : tagline,

}
    render = str(template.render(context, request))
    render = render.replace("TEXT_HTML", html)
    render = render.replace("LINES", lines)
    render = render.replace("STYLE", style)
    response = HttpResponse(render)

    return response

def format_date(date : str):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    parts = date.split("-")
    ret = f"{months[int(parts[1]) - 1]} {parts[2]}, {parts[0]}"
    return ret

def get_total_words():
    entries = BlogEntry.objects.all()
    total_words = 0
    posts = 0
    for e in entries:
        #not sure why it even enters a loop with an empty list
        if e == None:
            break

        #print(e)
        if (e.num_words == None):
            #intentionally pointless ;)
            total_words += 0
            posts += 1
            continue
        total_words += int(e.num_words)
        posts += 1
    total_words = str(total_words)
    posts = str(posts)
    return (total_words, posts)

def entry(request, id):
    ###THIS IS A TEST HTML FILE,
    # TODO replace with how we actually get the html file
    #html = open("E:\Documents\Code\Python\Website\HTML_files\BlogosphereEntryTemplate.html", "r").read()
    entries = BlogEntry.objects.all()
    if (id >= len(entries) or id < 0):
        raise Http404("Blog Entry does not exist!")
    entry = entries[id]

    words = get_total_words()
    total_words = words[0]
    posts = words[1]
    title = str(entry.blog_title)
    #control for ellipses
    title = title.replace("...", "")
    title += "..."
    date = str(entry.pub_date)
    date = format_date(date)
    words = str(entry.num_words)
    html = entry.raw_text
    html = entry.text_body
    style = entry.style
    #gets the html representation of a blog entry
    #html_template = open(r".\Blogosphere\templates\SiteTemplates\BlogosphereEntryTemplate.html", "r").read()
    template = loader.get_template("SiteTemplates/BlogosphereEntryTemplate.html")

    context = {
        "TOTAL_POSTS" : posts,
        "TOTAL_WORDS" : total_words,
        "TITLE" :  title,
        "DATE" : date,
        "NUM_WORDS" : words,
        #"TEXT_HTML" : html
   }
    render = str(template.render(context, request))
    render = render.replace("TEXT_HTML", html)
    render = render.replace("STYLE", style)

    return HttpResponse(render)