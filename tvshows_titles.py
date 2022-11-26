from requests_html import HTMLSession

session = HTMLSession()

url = 'https://mult.love/'



def getTitles():

    r = session.get(url)

    titles = r.html.find('a')
    data = []

    for i in titles:
        # img = i.find('img', first=True).attrs['src']
        discription = i.find('img', first=True).attrs['alt'].split("(")[1].split(")")[0]
        link = i.attrs['href'] + "/"
        data.append({'title':discription, 'link': link})

    return data
