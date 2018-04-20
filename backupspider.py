import scrapy

class backupspider(scrapy.Spider):


    name = "petitioncountspider"
    start_urls = ['https://www1.president.go.kr/petitions/201953']
    


    def parse(self,response):
        fetched = response.xpath('//div/h3/span/text()').extract()
        if len(fetched)==0:
            print("nothing is fetched")
            return
        
        first = fetched[0]

        count = first.replace(',','')
        

        print(count)