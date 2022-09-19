from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.requests
#from pytube import YouTube
import os
from urllib.parse import quote
#import requests

def whitelist_reader() -> [str]:
    f = open("whitelist.txt" , "r")
    return f.readlines()
    

def html_generator(url : str):
    '''
    takes a url str and returns a plaintext string of the html
    '''
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError:
        return None
    return html.decode("utf-8") 

def url_gatherer():
    '''
    goes to the ZP wiki page, then parses the html to find all the links in the page
    outputs all the valid links to 2 text files
    the first one is all the valid links to episodes
    the second one is all the invalid links or to non-episode content
    '''
    base_url = "https://zeropunctuation.fandom.com"
    #wiki = BeautifulSoup("https://zeropunctuation.fandom.com/wiki/Episode_Guide")
    wiki_html = urllib.request.urlopen("https://zeropunctuation.fandom.com/wiki/Episode_Guide").read()
    wiki = BeautifulSoup(wiki_html, "html.parser")
    links = [base_url + link.get("href") for link in wiki.find_all("a") if (link.get("href").startswith("/wiki"))]
    
    
def generate_title(url :str) -> str:
    title = url.replace("https://zeropunctuation.fandom.com/wiki/", "")
    title = title.replace("_", " ")
    title = title.replace("%26" , "&")
    title = title.replace("%27" , "'")
    title = title.replace("%2B" , "+")
    title = title.replace("%C3%A9", "é")
    return title

def html_cleaner(url : str):
    '''
    takes the wiki url of an episode
    and returns the title of the episode
    the ep num, the len, the date, the transcript,
    and the subtitles
    '''
    title, youtube_url, ep_num, ep_len, transcript, subitles, date = None, None, None, None, None, None, None
    text = html_generator(url)
    
    try:
        soup = BeautifulSoup(text, "html.parser")
    except TypeError:
        return None
    raw_text = re.sub("<[^>]+>", "", str(soup))
    raw_text = raw_text[raw_text.find("Basics"):].split("\n")
    raw_text = [item for item in raw_text if item != ""]
    try:
        ep_num = raw_text[raw_text.index("Episode #") + 1]
        ep_len = raw_text[raw_text.index("Length") + 1]
        date = raw_text[raw_text.index("Date") + 1]
    except ValueError:
        pass
    
    title = generate_title(url)
    
    
    
    for link in soup.find_all('a'):
        try:
            if "youtube" in link.get('href'):
                youtube_url = link.get('href')
                break
        except TypeError:
            break
    
    transcript = soup.get_text()
    start = transcript.find("Transcript")
    
    end = transcript.find("Addenda")
    
    if start == -1 or end == -1:
        return None
    transcript = transcript[start + 15: end]
    transcript = transcript.strip()
    
    '''
    print("got here at least")
    try:
        print("got to here")
        source = YouTube(youtube_url)
        print(source)
        print(source.captions.all, "here")
        lang = source.captions.all()[0]
        en_caption = source.captions.get_by_language_code(lang.code)
        subtitles =(en_caption.generate_srt_captions())
    except:
        subtitles = None
    '''
    subtitles = None
    return {"Title" : str(title).strip(),
    "Episode #" : int(ep_num) ,
    "Date" : date ,
     "Length" : str(ep_len).strip(),
      "Transcript" : str(transcript).strip(),
      "Subtitles" : subtitles,
      "Youtube URL" : str(youtube_url).strip()}
    

def ep_txt_writer(episode : dict):
    '''
    takes an episode dictionary
    and writes it to 2 seperate text files
    (or just 1 if there is no subtitles)
    all the info including transcript is in the first one
    '''
    #WILL BE HARDCODED TO WINDOWS PATHS
    #SPECIFICALLY MY PC
    #FIX WHEN MIGRATING TO RASBERRY PI
    
    if episode == None:
        return None
    title = episode["Title"]
    title = title.replace(":" , "COLON")
    title = title.replace(r"/" , "SLASH")
    path = "C:\\Users\\dcars\\Documents\\PythonWork\\Misc\\zp_bot\\episodes"
    ep_txt = open(path + "\\" + title + ".txt", "w", encoding="utf-8")
    ep_txt.write(episode["Title"] + "\n")
    ep_txt.write(episode["Episode #"] + "\n")
    ep_txt.write(episode["Length"] + "\n")
    ep_txt.write(episode["Youtube URL"] + "\n")
    ep_txt.write(episode["Transcript"])
    ep_txt.close()
    
    if episode["Subtitles"] != None:
        ep_subtitles = open(path + "\\" + title + "_TRANSCRIPT.srt", "w", encoding="utf-8")
        
        ep_subtitles.write(episode["Subtitles"])
        ep_subtitles.close()
    
def episode_filler(urls):
    episodes = os.listdir("C:\\Users\\dcars\\Documents\\PythonWork\\Misc\\zp_bot\\episodes")
    blacklist = [i.strip() for i in open("blacklist.txt", "r").readlines()]
    
    i = len(urls)
    for url in urls:
        title = generate_title(url) + ".txt"
        title = title.replace(":", "COLON")
        title = title.replace(r"/" , "SLASH")
        if title not in episodes and url not in blacklist:
            print(title)
            x = html_cleaner(url)
            ep_txt_writer(x)

def urllify(string):
    base1 = "https://www.google.com/search?q="
    base2 = "+site%3Ahttps%3A%2F%2Fzeropunctuation%2Efandom%2Ecom%2F"
    string = string.replace(" ", "+")
    string = quote(string)
    string = string.replace("%2B", "+")
    return base1 + string + base2

def list_links(url):
    urls = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    links = soup.findAll("a")
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        current = re.split(":(?=http)",link["href"].replace("/url?q=",""))[0]
        if current.startswith("https://zeropunctuation.fandom.com/wiki/"):
            end = current.find("&sa=")
            current = current[:end]
            urls.append(current)
    
    return urls
 
def find_loc(string, transcript):
    transcript = transcript.replace("..." , "ELLIPSES")
    #sentence = [sentence + '.' for sentence in transcript.split('.') if string in sentence.lower()][0]
    sentence = [sentence + '.' for sentence in re.split(r"[.?!]\s*", transcript) if string.lower() in sentence.lower()]
    if len(sentence) > 0:
        sentence = sentence[0]
    else:
        return '"' + string + '" was not found in this episode'
    sentence = sentence.replace("ELLIPSES", "...")
    sentence = sentence.replace("\n", "")
    if sentence.startswith('"') and sentence.count('"')%2 != 0:
        sentence = sentence[1:] 
    return sentence

def remove_punctuation(string):
    punctuation = r",.?[]{}%$#@!^&*();:'"
    for item in punctuation:
        string = string.replace(item, " ")
    string = string.replace("  ", " ")
    return string

def timecode_to_secs(timecode):
    timecode = timecode[:timecode.find(",")]
    timecode = timecode.split(":")
    return 60 * 60 * int(timecode[0]) + 60 * int(timecode[1]) + int(timecode[2])


def timecode_generator(sentence, subtitles):
    if subtitles == None:
        return None
    new = subtitles.split("\n")
    srt = []
    for line in new:
        if line != "":
            try:
                int(line)
            except:
                srt.append(line.lower())
    lines = srt[1::2]
    timecodes = srt[::2]
    whole_sentence = sentence
    sentence = [i.lower() for i in sentence.split()]
    for i in range(len(lines)):
        found = False
        if sentence[0] in lines[i]:
            whole_sentence = remove_punctuation(whole_sentence).lower()
            line = remove_punctuation(lines[i] + lines[i + 1] + lines[i + 2]).lower()
            if (line.startswith(whole_sentence) or whole_sentence.startswith(line)):
                return timecodes[i]
            
    return None
    
def best_guess_subtitles(string, episode):
    transcript = episode["Transcript"]
    percent = transcript.find(string) / len(transcript)
    ep_len = 60*int(episode["Length"][0]) + int(episode["Length"][2:])
    #print(ep_len) 
    time = ep_len * percent
    time = int(time - 7)
    if (time <= 7):
        time = 8
    #print(time)
    url = episode["Youtube URL"] + "&feature=youtu.be&t=" + str(time)
    return url

def message_generator(string):
    final = ""
    
    urls = list_links(urllify(string))
    count = 0
    #final += f'"{string}" was found in {str(len(urls))} episodes:\n'
    for url in urls:
        #print("testing", url)
        episode = html_cleaner(url)
        if episode != None:
            #print("found")
            sentence = find_loc(string, episode['Transcript'])
            if sentence.endswith("was not found in this episode") == False:
                count += 1
                temp = f"{episode['Title']} - Episode {episode['Episode #']}, published {episode['Date']}\n\n"
                
                temp += f"{sentence}\n\n"
                temp += "My best guess for the timecode for the quote is "
                temp += best_guess_subtitles(string, episode) + "\n\n"
            
                final += temp
        
    if count == 0:
        final = f'Unfortunately, "{string}" was not found in any episodes'
        final += "\n\nPlease try again with another quote, or try a different spelling\n"
        final += f'You can try googling "{string} site:https://zeropunctuation.fandom.com/wiki/" for better results'  
        return final
    elif count == 1:
        final = f'"{string}" was found in {count} episode:\n' + final
    elif count >= 10:
        final = f'"{string}" was found in at least {count} episodes:\n' + final
    else:
        final = f'"{string}" was found in {count} episodes:\n' + final
    final = "Thank you for choosing to use the ZP Bot!\n\n" + final
    final += f'You can try googling "{string} site:https://zeropunctuation.fandom.com/wiki/" for better results\n\n\n'
    final += "-"*27 + "\n" + "Created by /u/DanyeWest1963\n" + "-"*27
    return final
        
'''
TODO

make the updater so it can check when it last updated
make it so it never makes duplicate files
bug test
its kinda funky tbh
old episodes don't show up
'''

if __name__ == "__main__":
    #print(html_cleaner("https://zeropunctuation.fandom.com/wiki/Inside_%26_Shadow_of_the_Beast")["Transcript"])
    while True:
        text = input("What quote do you want me to search for?\n\n")
        
        print(message_generator(text))
    pass
    
