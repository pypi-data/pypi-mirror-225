from   bs4      import BeautifulSoup as bs
import time  
import pandas   as pd

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
# import common.urlProc as urlProc
from ..common  import urlProc
    
#######################################################################3    

# Url에서 특정 조회조건의 값을 추출
GetUrlAttrValue = lambda url, key: [x for x in url.split('&') if x[0:len(key)] == key][0].split('=')[1]

def GetBalticIndex(sDate, eDate):
    resData = []
    # 최초 url
    url = "https://www.shippingnewsnet.com/sdata/page.html?term=Search&sDate={}-{}-{}&eDate={}-{}-{}"
    url = url.format(sDate[0:4], sDate[4:6], sDate[6:8], eDate[0:4], eDate[4:6], eDate[6:8])
      
    # res = req.get(url)
    res = urlProc.requests_url_call(url)

    soup = bs(res.text, "html.parser")

    # 전체 데이터 건수 추출 및 url 조건 추가
    firstPgUrl = soup.select_one("ul.pagination > li.pagination-start > a").get('href')
    url = url  + '&total=%s'%( GetUrlAttrValue(firstPgUrl, 'total')) + '&page={}'
    pgNum = 1
    
    while True:    
        time.sleep(0.1)
        for tr in soup.select("table.marbtm-20 > tbody > tr"):
            tds = tr.select("td")
            resData.append([td.string if '-' in td.string else int(td.string.replace(',',''))  for td in tds])

        pgNum += 1

        if  soup.select_one("ul.pagination > li.pagination-next") or \
            str(pgNum) in [x.get_text() for x in soup.select("ul.pagination > li > a")]:    
            
            # res = req.get(url.format(pgNum))
            res = urlProc.requests_url_call(url.format(pgNum))
            soup = bs(res.text, "html.parser")
        else:
            break
    
    resData.sort()
    
    return pd.DataFrame(resData, columns=['일자', 'BDI','BCI','BPI','BSI'])
