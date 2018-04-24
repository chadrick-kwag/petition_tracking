from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)




url = "https://www1.president.go.kr/petitions/207045"


raw_html = simple_get(url)
html = BeautifulSoup(raw_html, 'html.parser')

find=html.select('h3.Reply_area_agree span')

if len(find) is not 1:
    print("find result number is not 1. it is {}. something is wrong".format(len(find)))
else:
    
    stringformat = find[0].text
    toint = int(stringformat.replace(',',''))
    print(toint)
    


