from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sqlite3
import urllib
import gc


def main(max_page):
    for i in range(1, max_page):
        conn = sqlite3.connect("../dogDrip.db")
        cur = conn.cursor()
        address = cur.execute("select address from dogDrip where id={ID}".format(ID=i)).fetchall()[0][0]
        conn.close()
        conn = None
        print(i)
        url = address
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            dog_drip_html = urlopen(request)
            bs_obj = BeautifulSoup(dog_drip_html.read(), "html.parser")
            html = str(bs_obj.find_all('div', class_="ed clearfix margin-vertical-large")[0])\
                .replace('href="', 'href="https://www.dogdrip.net')\
                .replace('src="', 'src="https://www.dogdrip.net')\
                .replace("'", '"')\
                .replace("https://www.dogdrip.nethttps://www.youtube.com/", "https://www.youtube.com/")
            title = str(bs_obj.find_all('h4')[0])\
                .replace("'", '"')
            conn = sqlite3.connect("../dogDrip.db")
            cur = conn.cursor()
            cur.execute("""update dogDrip set HTTP = '{HTTP}' where id={ID}"""
                        .format(HTTP='%s %s' % (title, html), ID=i))
            bs_obj.decompose()
            dog_drip_html.close()
            conn.commit()
            conn.close()
            cur = None
            address = None
            title = None
            html = None
            bs_obj = None
            url = None
            request = None
            dog_drip_html = None
            conn = None
            gc.collect()
        except urllib.error.HTTPError:
            print('Oops! The post is deleted!')
            conn.close()
            gc.collect()


main(100)
