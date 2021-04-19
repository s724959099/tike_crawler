import httpx
from pyquery import PyQuery as pq
import urllib.parse

bsae_url = 'https://l-tike.com'

urls = """
https://l-tike.com/concert/
https://l-tike.com/sports/
https://l-tike.com/play/
https://l-tike.com/classic/
https://l-tike.com/event/
https://l-tike.com/leisure/
https://l-tike.com/cinema/
https://tour.l-tike.com/#_ga=2.88759259.17573151.1618764214-1487032722.1618764214
"""

urls = urls.strip().split()
url = urls[0]

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en;q=0.8,zh-CN;q=0.7,en-US;q=0.6",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

parsed_urls = set()
order_urls = set()


def req_url(url: str) -> httpx.Response:
    if url in parsed_urls:
        return


def find_urls(client: httpx.Client, url: str):
    if url in parsed_urls:
        return
    if 'https://l-tike' not in url:
        print('not found:', url)
        return
    if not url.startswith('http'):
        return
    print('next: ', url)
    client.cookies = None
    try:
        r = client.get(url)
    except Exception as e:
        find_urls(client, url)
        print('error:', url)
        return

    parsed_urls.add(url)
    dom = pq(r.text)

    for a in dom('main a').items():
        href = a.attr('href')
        href = urllib.parse.urljoin(bsae_url, href)
        if '/order/' in href:
            order_urls.add(href)
            print('order:', len(order_urls))
            continue

        find_urls(client, href)


transport = httpx.HTTPTransport(retries=3)

with httpx.Client(headers=headers, transport=transport) as client:
    find_urls(client, url)

print()
