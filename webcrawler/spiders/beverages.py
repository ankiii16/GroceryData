
from email.mime import image
import scrapy


# --run command scrapy crawl beverages -O Beverages.json 
class Beverages(scrapy.Spider):
   name = 'beverages'
   
   start_urls = [
      "https://talesofindia.com.au/product-category/beverages/juices-softdrinks-sharbats/",
      "https://talesofindia.com.au/product-category/beverages/butter-milk-drinks/",
      "https://talesofindia.com.au/product-category/beverages/tea-coffee/"

   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[7]/div'):
            category=""
            sub_category="none"
            
            # categories
            category_juices_softdrinks_sharbats="Juices, Soft Drinks & Sharbats"
            category_milk_powders_and_drinks="Milk Powders & Drinks"
            category_tea_and_coffee="Tea & Coffee"


            if "juices-softdrinks-sharbats" in response.url:
                category=category_juices_softdrinks_sharbats
                
            elif "butter-milk-drinks" in response.url:
                category=category_milk_powders_and_drinks
            else:
                category=category_tea_and_coffee
        
            try:
                image_url=products.css('a.product-image-link').xpath('img').attrib['data-srcset']
                image_url=image_url.partition(",")[0]
                image_url=image_url.partition(" ")[0]
            except:
                image_url=products.css('a.product-image-link').xpath('img').attrib['data-srcset']
            brand=""
            price=products.xpath('span/span/bdi').css('bdi::text').get()
            if products.css('div.wd-product-brands-links.woodmart-product-brands-links').xpath("a").css("::text").get() is not None:
                brand=products.css('div.wd-product-brands-links.woodmart-product-brands-links').xpath("a").css("::text").get()
            if price is None:
                price=products.xpath('span/ins/span/bdi').css('bdi::text').get()

            try:
                yield{
                "name":products.css("h3.wd-entities-title").css('a::text').get().replace('\u2013'),
                "imageLink":image_url,
                "price":price,
                "category":category,
                "sub_category":sub_category,
                "brand":brand
                }
            except:
                yield{
                 "name":products.css("h3.wd-entities-title").css('a::text').get(),
                "imageLink":image_url,
                "price":price,
                "category":category,
                "sub_category":sub_category,
                "brand":brand
                }