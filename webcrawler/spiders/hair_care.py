
import scrapy


# --run command 
# cd Beauty&Hygiene
# scrapy crawl hair_care -O HairCare.json 
class HairCare(scrapy.Spider):
   name = 'hair_care'
   
   start_urls = [ 'https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/hair-care-hair-care/',
   "https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/indian-hair-colours/",
   "https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/hair-oils/"
   
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[6]/div'):
            subtype=""
            hair_care_hair_care="hair-care-hair-care"
            indian_hair_colours="indian-hair-colours"
            hair_oils="hair-oils"
         
            if hair_care_hair_care in response.url:
                subtype="Hair_Ayurvedic"
            elif indian_hair_colours in response.url:
                subtype=indian_hair_colours
            else:
                subtype=hair_oils 
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
       

        
