import bs4
import urllib.request

def GoogleSearcher(quote):
    url = "https://www.google.com/search?q=asdf+site%3Ahttps%3A%2F%2Fzeropunctuation.fandom.com%2Fwiki"
    url = url.replace("asdf", quote)
    print(url)
    search = urllib.request.urlopen(url).read()

    print(search)

if __name__ == "__main__":
    GoogleSearcher("mario")