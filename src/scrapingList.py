from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import sqlite3
import gc
from guppy import hpy
h = hpy()


def main(start_page, max_page):

    def get_dog_drip(page):
        url = 'https://www.dogdrip.net/index.php?mid=dogdrip&page=' + str(page)
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            dog_drip_html = urlopen(request)
            bs_obj = BeautifulSoup(dog_drip_html.read(), "html.parser")
            dog_drip_obj = bs_obj.select("tbody > tr")
            dog_drip_html.close()
            bs_obj.decompose()
            return dog_drip_obj
        except urllib.error.HTTPError:
            print('Oops! something wrong T_T')
            return ''

    for i in range(start_page, max_page):
        dog_drip_list = get_dog_drip(i)
        raw_data = BeautifulSoup(str(dog_drip_list), "html.parser")
        # print(raw_data)
        print(h.heap())
        for a in range(0, 20):
            title = raw_data.find_all("span", class_="ed title-link")[a].text
            title = str(title).replace("'", '\'\'')
            address = str(raw_data.find_all('a', class_="ed link-reset")[a]['href'])

            conn = sqlite3.connect("../dogDrip.db")
            cur = conn.cursor()
            cur.execute("""insert into dogDrip(title, address) values ('{TITLE}', '{ADDRESS}')"""
                        .format(TITLE=title, ADDRESS=address))
            conn.commit()
            conn.close()
        raw_data.decompose()
        raw_data = None
        dog_drip_list = None
        raw_data = None
        gc.collect()


main(1, 20)
print('1 done')
main(20, 40)
print('2 done')
main(40, 60)
