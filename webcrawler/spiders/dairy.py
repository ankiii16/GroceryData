
import scrapy


# --run command scrapy crawl dairy -O BiscuitsRusksAndKhari.json 
class Dairy(scrapy.Spider):
   name = 'dairy'
   
   start_urls = [ 'https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/indian-dahi/',
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/dosa-idli-batter/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/indian-makhan-milk/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/paneer/"
   
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[7]/div'):
            subtype=""
            indian_dahi="indian-dahi"
            dosa_idli_batter="dosa-idli-batter"
            indian_makhan_milk="indian-makhan-milk"
            paneer="paneer"
         
            if indian_dahi in response.url:
                subtype=indian_dahi
            elif dosa_idli_batter in response.url:
                subtype=dosa_idli_batter
            elif indian_makhan_milk in response.url:
                subtype=indian_makhan_milk
            else:
                subtype=paneer 
            try:
                yield{
                "name":products.css("h3.wd-entities-title").css('a::text').get().replace('\u2013'),
                "imageLink":products.css('a.product-image-link').xpath('img').attrib['src'],
                "price":products.xpath('span/span/bdi').css('bdi::text').get(),
                "subType":subtype
                }
            except:
                yield{
                 "name":products.css("h3.wd-entities-title").css('a::text').get(),
                "imageLink":products.css('a.product-image-link').xpath('img').attrib['src'],
                "price":products.xpath('span/span/bdi').css('bdi::text').get(),
                "subType":subtype
                }
       

        
