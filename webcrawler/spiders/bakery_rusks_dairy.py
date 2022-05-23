
from email.mime import image
import scrapy


# --run command scrapy crawl bakery_rusks_dairy -O BiscuitsRusksAndDairy.json 
class BiscuitsRusksAndDiary(scrapy.Spider):
   name = 'bakery_rusks_dairy'
   
   start_urls = [
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/biscuits-rusk-khari/bakery-biscuits-snacks/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/biscuits-rusk-khari/khari-khakhra/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/biscuits-rusk-khari/rusks/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/indian-dahi/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/dosa-idli-batter/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/indian-makhan-milk/",
   "https://talesofindia.com.au/product-category/bakery-dairy-rusks/dairy/paneer/"
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[7]/div'):
            category=""
            sub_category=""
            
            # categories
            category_dairy="Dairy"
            category_biscuits="Biscuits, Rusk, & Khari"

            #sub categories
            bakery_biscuits_and_snacks="Bakery, Biscuits & Snacks"
            khari_and_khakaras="Khari & Khakaras"
            rusks="Rusks"
            indian_dahi="Dahi / Yogurt"
            dosa_idli_batter="Dosai / Idly Batter"
            milk_and_makhan="Milk & Makhan"
            paneer="Paneer"   

            if "biscuits-rusk-khari" in response.url:
                category=category_biscuits
                if "bakery-biscuits-snacks" in response.url:
                    sub_category=bakery_biscuits_and_snacks
                elif "khari-khakhra" in response.url:
                    sub_category=khari_and_khakaras
                elif "rusks" in response.url:
                    sub_category=rusks   
                else:
                    sub_category="none"  
            else:
                category=category_dairy
                if "indian-dahi" in response.url:
                    sub_category=indian_dahi
                elif "dosa-idli-batter" in response.url:
                    sub_category=dosa_idli_batter
                elif "makhan" in response.url:
                    sub_category=milk_and_makhan
                elif "paneer" in response.url:
                    sub_category=paneer
                else:
                    sub_category="none"

            
            
        
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