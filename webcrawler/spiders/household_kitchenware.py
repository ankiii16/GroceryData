
from email.mime import image
import scrapy


# --run command scrapy crawl household_kitchenware -O HouseholdAndKitchenware.json 
class HouseholdAndKitchenware(scrapy.Spider):
   name = 'household_kitchenware'
   
   start_urls = [
     "https://talesofindia.com.au/product-category/kitchenware-household/cleaning-needs/",

     "https://talesofindia.com.au/product-category/kitchenware-household/kitchenware/clay-kitchenware/",
     "https://talesofindia.com.au/product-category/kitchenware-household/kitchenware/indian-utensils/",
     "https://talesofindia.com.au/product-category/kitchenware-household/kitchenware/indian-utensils-crockery/",
     "https://talesofindia.com.au/product-category/kitchenware-household/kitchenware/indian-mixer-grinders/",
     "https://talesofindia.com.au/product-category/kitchenware-household/kitchenware/pressure-cooker/",

    "https://talesofindia.com.au/product-category/kitchenware-household/party-festive-needs/",

    "https://talesofindia.com.au/product-category/kitchenware-household/toys-games/",


    "https://talesofindia.com.au/product-category/kitchenware-household/indian-tradition-pooja-items/indian-diya-lamps-diwali-essentials/",
    "https://talesofindia.com.au/product-category/kitchenware-household/indian-tradition-pooja-items/indian-fasting/",
    "https://talesofindia.com.au/product-category/kitchenware-household/indian-tradition-pooja-items/incense-sticks/",
    "https://talesofindia.com.au/product-category/kitchenware-household/indian-tradition-pooja-items/pooja-essentials/",
    "https://talesofindia.com.au/product-category/kitchenware-household/indian-tradition-pooja-items/religious-hindu-products/"
   ]


   def parse(self, response):
       xpath="/html/body/div[1]/div/div[2]/div/div/div[6]/div"
       if "cleaning-needs" in response.url:
        xpath="/html/body/div[1]/div/div[2]/div/div/div[7]/div"
       for products in response.xpath(xpath):
            category=""
            sub_category="none"
            
            # categories
            category_cleaning_needs="Cleaning Needs"
            # subcategories

            # categories
            category_kitchenware="Kitchenware"
            # subcategories
            sub_category_clay_kitchenware="Clay Kitchenware"
            sub_category_indian_utensils="Cookware"
            sub_category_indian_utensils_crockery="General Utensils"
            sub_category_indian_mixer_grinders="Mixers & Grinders"
            sub_category_pressure_cooker="Pressure Cookers"

            # categories
            category_party_festive_needs="Party & Festive Needs"
            # subcategories

            # categories
            category_toys_games="Toys & Games"
            # subcategories

            # categories
            category_indian_tradition_pooja_items="Traditional & Pooja Needs"
            # subcategories
            sub_category_indian_diya_lamps_diwali_essentials="Diya, Lamps & Wicks"
            sub_category_indian_fasting="Fasting Essentials"
            sub_category_incense_sticks="Incense Sticks & Dhoop"
            sub_category_pooja_essentials="Other Pooja Needs"
            sub_category_religious_hindu_products="Religious Idols & Items"

            if "cleaning-needs" in response.url:
                category=category_cleaning_needs
                
            elif "kitchenware-household/kitchenware" in response.url:
                category=category_kitchenware
                if 'clay-kitchenware' in response.url:
                    sub_category=sub_category_clay_kitchenware
                elif 'indian-utensils' in response.url and 'crockery' not in response.url:
                    sub_category=sub_category_indian_utensils
                elif 'indian-utensils-crockery' in response.url:
                    sub_category=sub_category_indian_utensils_crockery
                elif 'indian-mixer-grinders' in response.url:
                    sub_category=sub_category_indian_mixer_grinders
                elif 'pressure-cooker' in response.url:
                    sub_category=sub_category_pressure_cooker
                else :
                    sub_category="none"
                
            elif "party-festive-needs" in response.url:
                category=category_party_festive_needs
            elif "toys-games" in response.url:
                category=category_toys_games
            else :
                category=category_indian_tradition_pooja_items
                if 'indian-diya-lamps-diwali-essentials' in response.url:
                    sub_category=sub_category_indian_diya_lamps_diwali_essentials
                elif 'indian-fasting' in response.url and 'crockery' not in response.url:
                    sub_category=sub_category_indian_fasting
                elif 'incense-sticks' in response.url:
                    sub_category=sub_category_incense_sticks
                elif 'pooja-essentials' in response.url:
                    sub_category=sub_category_pooja_essentials
                elif 'religious-hindu-product' in response.url:
                    sub_category=sub_category_religious_hindu_products
                else :
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
       

        
