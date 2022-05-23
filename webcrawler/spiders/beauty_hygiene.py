
from email.mime import image
import scrapy


# --run command scrapy crawl beauty_hygiene -O BeautyAndHygiene.json 
class BeautyAndHygiene(scrapy.Spider):
   name = 'beauty_hygiene'
   
   start_urls = [
       "https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/hair-care-hair-care/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/indian-hair-colours/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/ayurvedic-hair-care/hair-oils/",

       "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/general-care/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/heena/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/oral-care/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/personal-care/wax-bleaches/",

       "https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/facepacks-facials/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/skin-creams/",
       "https://talesofindia.com.au/product-category/indian-cosmetics/skin-care/soaps-facewash/"
   ]


   def parse(self, response):
        for products in response.xpath('/html/body/div[1]/div/div[2]/div/div/div[6]/div'):
            category=""
            sub_category=""
            
            # categories
            category_hair_care="Hair Care"
            category_personal_care="Personal Care"
            category_skin_care="Skin Care"

            #sub categories 1
            hair_care_hair_care="Hair Ayurvedic"
            hair_colour="Hair Colour"
            hair_oils="Hair Oils"

            # sub categories 2
            general_care="General Care"
            mehandi="Mehandi"
            oral_care="Oral Care"
            wax_and_bleaches="Wax & Beaches"

            #sub categories 3
            face_packs_and_facials="Face Packs & Facials"
            skin_creams="Skin Creams"
            soaps_and_facewash="Soaps & Facewash"

            if "ayurvedic-hair-care" in response.url:
                category=category_hair_care
                if "hair-care-hair-care" in response.url:
                    sub_category=hair_care_hair_care
                elif "indian-hair-colours" in response.url:
                    sub_category=hair_colour
                elif "hair-oils" in response.url:
                    sub_category=hair_oils
                else:
                    sub_category="none"  
            elif "personal-care" in response.url:
                category=category_personal_care
                if "general-care" in response.url:
                    sub_category=general_care
                elif "heena" in response.url:
                    sub_category=mehandi
                elif "oral-care" in response.url:
                    sub_category=oral_care
                elif "wax-bleaches" in response.url:
                    sub_category=wax_and_bleaches
                else:
                    sub_category="none"
            else:

                category=category_skin_care
                if "facepacks-facials" in response.url:
                    sub_category=face_packs_and_facials
                elif "skin-creams" in response.url:
                    sub_category=skin_creams
                elif "soaps-facewash" in response.url:
                    sub_category=soaps_and_facewash
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