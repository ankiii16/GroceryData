
from email.mime import image
import scrapy


# --run command scrapy crawl health_ayurvedic -O HealthAndAyurvedic.json 
class HealthAndAyurvedic(scrapy.Spider):
   name = 'health_ayurvedic'
   
   start_urls = [
      "https://talesofindia.com.au/product-category/ayurveda/ayurvedic-staples-raw-products/",
      "https://talesofindia.com.au/product-category/ayurveda/herbal-tablets/",
      "https://talesofindia.com.au/product-category/ayurveda/chemical-free-incense-sticks/",
      "https://talesofindia.com.au/product-category/ayurveda/indian-health-remedies/"
   ]


   def parse(self, response):
        xpath="/html/body/div[1]/div/div[2]/div/div/div[6]/div"
        for products in response.xpath(xpath):
            category=""
            sub_category="none"
            
            # categories
            category_ayurvedic_staples_raw_products="Ayurvedic Staples"
            category_herbal_tablets="Ayurvedic Supplements"
            category_chemical_free_incense_sticks="Chemical Free Insense Sticks"
            category_indian_health_remedies="Health Remedies"


            if "ayurvedic-staples-raw-products" in response.url:
                category=category_ayurvedic_staples_raw_products
                
            elif "herbal-tablets" in response.url:
                category=category_herbal_tablets
                
            elif "chemical-free-incense-sticks" in response.url:
                category=category_chemical_free_incense_sticks
            else:
                category=category_indian_health_remedies
        
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
       

        
