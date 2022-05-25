
import scrapy

class PostSpider(scrapy.Spider):
   name = 'quotes'
   fruitsAndVegetables=[ 'https://talesofindia.com.au/product-category/fruits-vegetables',
        'https://talesofindia.com.au/product-category/fruits-vegetables/page/2']
   
   bakery_Biscuits_Snacks=["https://talesofindia.com.au/product-category/bakery-dairy-rusks/biscuits-rusk-khari/bakery-biscuits-snacks"]
   start_urls = fruitsAndVegetables


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[6]/div'):
            try:
                yield{
                "name":products.css("h3.wd-entities-title").css('a::text').get().replace('\u2013'),
                "imageLink":products.css('a.product-image-link').xpath('img').attrib['src'],
                "price":products.xpath('span/span/bdi').css('bdi::text').get()
                }
            except:
                yield{
                 "name":products.css("h3.wd-entities-title").css('a::text').get(),
                "imageLink":products.css('a.product-image-link').xpath('img').attrib['src'],
                "price":products.xpath('span/span/bdi').css('bdi::text').get()
                }
       

        
