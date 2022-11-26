from requests_html import HTMLSession

session = HTMLSession()

url = 'https://myfin.by/currency/usd'

def get_best_price():
    r = session.get(url)
    tr = r.html.find('tr.c-currency-table__main-row')
    data = []
    for item in tr:
        td = item.find('td')
        for idx, _ in enumerate(td):
            
            if idx == 2:
                usd_column = td[idx].find('span.best.accent', first=True)
                if usd_column != None:

                    best_price = usd_column.text
                    address = get_address(r, item)
                    data.append({
                        'bank': item.find('td a', first=True).text,
                        'price': best_price,
                        'addresses': address
                    })
    

def get_address(res, item):
    addresses = []
    tr_with_addresses = res.html.find(f"tr#{item.attrs['id'].replace('bank', 'filial')}")
    tr = tr_with_addresses[0].find('tbody tr')
    for element in tr:
        td = element.find('td')
        for idx, i in enumerate(td):
            if i.find('span.best.accent'):
                if td[idx].find('i[data-currency=USD]'):
                    addresses.append({
                        'price': i.find('span.best.accent')[0].text,
                        'address': element.find('td a.c-currency-table__branch-name', first=True).text
                    })

    return addresses



