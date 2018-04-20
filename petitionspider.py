import scrapy, datetime


class PetitionCountSpider(scrapy.Spider):


    name = "petitioncountspider"
    collection = None
    petition_number = None

    def parse(self,response):
        fetched = response.xpath('//div/h3/span/text()').extract()
        if fetched is None:
            print("nothing is fetched")
            return
        
        first = fetched[0]

        count = first.replace(',','')
        

        print(count)

        if self.collection is None:
            print("no collection. finish here")
            return

        if self.petition_number is None:
            print("no petition_number defined. abort")
            return
        
        insert_item = {'datetime': datetime.datetime.utcnow(), 'petition_num':self.petition_number,'petition_count':count}
        self.collection.insert_one(insert_item)

        print("insert done")



