from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

class PetitionCountCrawler:
    def __init__(self , petition_num  ):
        self.petition_num = petition_num

    def geturl(self):
        base_url = "https://www1.president.go.kr/petitions/"
        return base_url+str(self.petition_num)
    
    def simple_get(self,url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return None
    
    def is_good_response(self,resp):
        """
        Returns true if the response seems to be HTML, false otherwise
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)

    def fetch(self):
        raw_html = self.simple_get(self.geturl())
        if raw_html is None:
            print("fetch failed")
            return None
        
        html = BeautifulSoup(raw_html, 'html.parser')

        find=html.select('h3.Reply_area_agree span')

        if len(find) is not 1:
            print("find result number is not 1. it is {}. something is wrong".format(len(find)))
            return None
        else:
            stringformat = find[0].text
            count = int(stringformat.replace(',',''))
            print("petition_num={}\tcount={}".format(self.petition_num,count))
            return count