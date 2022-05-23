
from email.mime import image
import scrapy


# --run command scrapy crawl fruits_vegetables -O FruitsAndVegetables.json 
class FruitsAndVegetables(scrapy.Spider):
   name = 'fruits_vegetables'
   
   start_urls = [
      "https://talesofindia.com.au/product-category/fruits-vegetables/dry-fruits-vegetables/",
      "https://talesofindia.com.au/product-category/fruits-vegetables/fresh-vegetables/",
      "https://talesofindia.com.au/product-category/fruits-vegetables/frozen-fruits/",
      "https://talesofindia.com.au/product-category/fruits-vegetables/frozen-vegetables/"

   ]


   def parse(self, response):
        xpath="/html/body/div[1]/div/div[2]/div/div/div[6]/div"
        if "dry-fruits-vegetables" in response.url:
            xpath="/html/body/div[1]/div/div[2]/div/div/div[7]/div"

        for products in response.xpath(xpath):
            category=""
            sub_category="none"
            
            # categories
            category_dry_fruits_vegetables="Dry Fruits & Vegetables"
            category_fresh_vegetables="Fresh Vegetables"
            category_frozen_fruits="Frozen Fruits"
            category_frozen_vegetables="Frozen Vegetables"


            if "dry-fruits-vegetables" in response.url:
                category=category_dry_fruits_vegetables
                
            elif "fresh-vegetables" in response.url:
                category=category_fresh_vegetables
                
            elif "frozen-fruits" in response.url:
                category=category_frozen_fruits
            else:
                category=category_frozen_vegetables
        
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