import codecs
from bs4 import BeautifulSoup
import urllib.request

def download_google_doc(doc_id : str):
    base = "https://docs.google.com/document/d/doc_id/export?format=html"
    url = base.replace("doc_id", doc_id)
    f = urllib.request.urlopen(url).read()
    t = open("test.html", "w")
    t.write(str(f))
    t.close()
    return f
    #parse_blog(f)
    #print(str(f))

def parse_blog(html  = ""):
    if (html == ""):
        html = open("test.html", "r").read()
    soup = BeautifulSoup(html, "html.parser")
    style = str(soup.find_all("style")[0])
    print(style)


    pretty = soup.prettify()
    #print(pretty)
    parsed = {}
    title = soup.h2.text
    #prevent accidental double ellipses, or forgetting them
    title = title.replace("...", "") + "..."
    text = soup.find_all("p")
    '''
    path = "E:\Documents\Code\Python\Website\DaneSite\Blogosphere\\templates\SiteTemplates\BlogosphereEntryTemplate.txt"
    f = open(path)

    template = f.read()
    f.close()
    '''
    raw_html = ""
    word_count = 0
    clean_text = ""
    for i in text:
        i_text = i.text
        #skip blank lines
        if (i_text.strip() == ""):
            continue
        clean_text += i_text + "\n"
        #add num words to total
        word_count += len(i_text.split(" "))
        #line is, by default, the raw html of the line
        line = str(i)

        #add tab and newline chars, both unicode and html
        raw_html += f"&nbsp;{line}"
    parsed["WORD_COUNT"] = word_count
    parsed["CLEAN"] = clean_text
    #TODO
    #somehow, we are getting garbage HTML
    parsed["RAW_HTML"] = raw_html
    parsed["TITLE"] = title
    parsed["STYLE"] = style
    '''
    #TODO finish total posts and total word counter
    template = template.replace("TOTAL_POSTS", "1")
    template = template.replace("TOTAL_WORDS", str(word_count))
    template = template.replace("Dear Irvine...", title)
    template = template.replace("NUM_WORDS", str(word_count))
    #Todo format date correctly
    template = template.replace("FORMATTED_DATE", "Jan 6, 2021")
    template = template.replace("TEXT_HTML", raw_html)
    path = f"E:\Documents\Code\Python\Website\DaneSite\Blogosphere\\templates\SiteTemplates\{title.replace('...', '')}.html"
    f = open(path, "w")
    f.write(template)
    f.close()
    '''
    return parsed

    #print(template)

if __name__ == "__main__":
    id = "19lMWpE3j7Lbhq0pbU2V_nRpcyc9X8BDdG_lAhMidkWU"
    f = open("test.html", "r").read()
    parse_blog(f)
    #download_google_doc(id)