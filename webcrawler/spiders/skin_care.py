
import scrapy


# --run command 
# scrapy crawl skin_care -O SkinCare.json 
class SkinCare(scrapy.Spider):
   name = 'skin_care'
   
   start_urls = [ 'https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/facepacks-facials/',
   "https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/skin-creams/",
   "https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/soaps-facewash/"
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[6]/div'):
            subtype=""
            facepacks_facials="facepacks-facials"
            skin_creams="skin-creams"
            soaps_facewash="soaps-facewash"
          
            if facepacks_facials in response.url:
                subtype=facepacks_facials
            elif skin_creams in response.url:
                subtype=skin_creams
            else:
                subtype=soaps_facewash 
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
       

        
