from requests_html import HTMLSession
import re

session = HTMLSession()

def Seasons(url):
    seasons = []
    exeptions = ['#']
    r = session.get("https:"+url).html

    numberSeason = r.find('div.numberSeason')
    otherSeasons = r.find('div#otherSeasons a')

    for item in numberSeason:
        a = item.find('a', first=True)
        try:
            if a.attrs['href'] in exeptions:
                pass
            else:
                seasons.append(url + a.attrs['href'])
        except KeyError:
            continue

    for item in otherSeasons:
        try:
            if item.attrs['href'] in exeptions:
                pass
            else:
                seasons.append(url + item.attrs['href'])
        except KeyError:
            continue
    
    seasons.reverse()

    return seasons

def Episodes(season, title_url):
    episodes = []
    r = session.get(f"https:{title_url}season.php?id={season}").html
    td = r.find('td.block_season_top a')
    
    for a in td:
        try:
            episodes.append({
                'episode': a.attrs['href'].split('=')[1][-2:],
                'link': VideoLink(f"https:{title_url}{a.attrs['href']}&voice=5")
            })
            
        except KeyError:
            continue
        
    return episodes
    
def VideoLink(link):
    r = session.get(link).html
    var_player = re.compile('var\s+player\s+=\s+(.*)mp4') 
    file = re.compile('file(.*)mp4')

    all_script = r.find('script')
    for individual_script in all_script:
            all_value =  individual_script.text        

            if all_value:            
                m = var_player.match(all_value.strip())
                if m != None:
                    txt = m.string
                    res = file.search(txt)
                    res = res.group().split("\'")[1]
                    digit = re.search(r'\d+', res).group()
                    res = res.replace(digit, '3', 1)
                    rep_word = res.split('/')[-2]
                    res = res.replace(rep_word, "original")

                    return res


