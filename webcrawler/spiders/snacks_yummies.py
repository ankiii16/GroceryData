
from email.mime import image
import scrapy


# --run command scrapy crawl snacks_yummies -O SnacksAndYummies.json 
class SnackAndYummies(scrapy.Spider):
   name = 'snacks_yummies'
   
   start_urls = [

    # Biscuits & Cookies
    "https://talesofindia.com.au/product-category/snacks/biscuits/britannia-biscuits/",
    "https://talesofindia.com.au/product-category/snacks/biscuits/cherabs-biscuits/",
    "https://talesofindia.com.au/product-category/snacks/biscuits/more-biscuits/",
   

    # desserts
    "https://talesofindia.com.au/product-category/snacks/desserts/chikki-gajjak/",
    "https://talesofindia.com.au/product-category/snacks/desserts/dessert-mixes/",
    "https://talesofindia.com.au/product-category/snacks/desserts/icecreams/",
    "https://talesofindia.com.au/product-category/snacks/desserts/indian-sweets-prepacked/",

    # Frozen yummies
    "https://talesofindia.com.au/product-category/snacks/frozen-yummies/frozen-snacks/",
    "https://talesofindia.com.au/product-category/snacks/frozen-yummies/frozen-desserts/",
    "https://talesofindia.com.au/product-category/snacks/frozen-yummies/frozen-naan-paratha-chapatti/",
    "https://talesofindia.com.au/product-category/snacks/frozen-yummies/frozen-stuffed-paratha/",

    # Fryums, Papds And Pickels
    "https://talesofindia.com.au/product-category/snacks/papad-pickles/chat-corner/",
    "https://talesofindia.com.au/product-category/snacks/papad-pickles/fryums/",
    "https://talesofindia.com.au/product-category/snacks/papad-pickles/papads/",
    "https://talesofindia.com.au/product-category/snacks/papad-pickles/pickles-murabba/",

    # mukwas and candies
    "https://talesofindia.com.au/product-category/snacks/mouthfreshners/",

    # noodles and vermicilli
    "https://talesofindia.com.au/product-category/snacks/noodles-vermicilli/noodles/",
    "https://talesofindia.com.au/product-category/snacks/noodles-vermicilli/vermicilli/",

    # ready to eat
    "https://talesofindia.com.au/product-category/snacks/rte/heat-eat-curries/",
    "https://talesofindia.com.au/product-category/snacks/rte/instant-mixes-packs/",
    "https://talesofindia.com.au/product-category/snacks/rte/soups/",


    # Snacks & Namkeen
    "https://talesofindia.com.au/product-category/snacks/snacks-namkeen/chips/",
    "https://talesofindia.com.au/product-category/snacks/snacks-namkeen/more-snacks/",
    "https://talesofindia.com.au/product-category/snacks/snacks-namkeen/namkeen-meethay-snacks/",
    

    # spread and chutneys
    "https://talesofindia.com.au/product-category/snacks/sauces-chutneys/"


   ]


   def parse(self, response):
       xpath="/html/body/div[1]/div/div[2]/div/div/div[6]/div"
       if "icecreams" in response.url :
            xpath="/html/body/div[1]/div/div[2]/div/div/div[7]/div"
       sub_category= response.css('h1.entry-title.title::text').get()
       for products in response.xpath(xpath):
            category=""
            if "biscuits" in response.url:
                category="Biscuits & Cookies"
            elif "desserts" in response.url:
                category="Desserts"
            elif "frozen-yummies" in response.url:
                category="Frozen Yummies"
            elif "papad-pickles" in response.url:
                category="Fryums, Papads & Pickles"
            elif "rice" in response.url:
                category="Rice & Rice Products"
            elif "mouthfreshners" in response.url:
                category="Mukhwas & Candies"
                sub_category="none"
            elif "noodles-vermicilli" in response.url:
                category="Noodles & Vermicilli"
            elif "rte" in response.url:
                category="Ready To Eat"
            elif "snacks-namkeen" in response.url:
                category="Snacks & Namkeen"
            elif "sauces-chutneys" in response.url:
                category="Spreads, Sauces & Chutneys"
                sub_category="none"
            else :
                category="none"


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
       

        
