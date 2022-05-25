
import scrapy


# --run command 
# scrapy crawl personal_care -O PersonalCare.json 
class PersonalCare(scrapy.Spider):
   name = 'personal_care'
   
   start_urls = [ 'https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/general-care/',
   "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/heena/",
   "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/oral-care/"
   "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/wax-bleaches/"
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[6]/div'):
            subtype=""
            general_care="general-care"
            heena="heena"
            oral_care="oral-care"
            wax_bleaches="wax-bleaches"
            if general_care in response.url:
                subtype=general_care
            elif heena in response.url:
                subtype="Mehendi"
            elif oral_care in response.url:
                subtype=oral_care
            else:
                subtype=wax_bleaches 
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
       

        
