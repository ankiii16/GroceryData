
from email.mime import image
import scrapy


# --run command scrapy crawl rice_flours_lentils_oils_spices -O RiceFloursLentilsOilsSpices.json 
class RiceFloursLentilsOilsSpices(scrapy.Spider):
   name = 'rice_flours_lentils_oils_spices'
   
   start_urls = [

    # Atta, & Flours
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/flour/atta/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/flour/other-flours/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/flour/suji-maida-besan/",

    # Dals & Pulses
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/lentils/chole-channa-moong/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/lentils/organic-dals/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/lentils/soya-millets/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/lentils/toor-rajma-masoor/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/lentils/urid/",

    # Food Colours & Essence
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/foodessence/",

    # Oils & Ghee
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/oils-ghee/ghee/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/oils-ghee/sesame-peanut-coconut-oil/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/oils-ghee/mustard-oil/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/oils-ghee/sunflower-canola-vegetable-oil/",

    # Rice & Rice Products
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/basmati/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/idly-jeerasala-rice/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/other-rice/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/poha-sago-mamra/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/boiled-rice/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/rice/sona-masoori/",

    # Salt, Sugar, Jaggery & Nuts
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/salt-sugar-gur-nuts/nuts-herbs-seeds/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/salt-sugar-gur-nuts/salt/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/salt-sugar-gur-nuts/sugar-jaggery/",

    # Spices & Pastes
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/masala-spices/blended-spices/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/masala-spices/cooking-pastes/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/masala-spices/powdered-spices/",
    "https://talesofindia.com.au/product-category/foodgrains-oils-masalas/masala-spices/whole-spices/"


   ]


   def parse(self, response):
       xpath="/html/body/div[1]/div/div[2]/div/div/div[6]/div"
       if "other-flours" in response.url or "suji-maida-besan" in response.url or "foodessence" in response.url:
            xpath="/html/body/div[1]/div/div[2]/div/div/div[7]/div"
       sub_category= response.css('h1.entry-title.title::text').get()
       for products in response.xpath(xpath):
            category=""
            if "flour" in response.url:
                category="Atta, & Flours"
            elif "lentils" in response.url:
                category="Dals & Pulses"
            elif "foodessence" in response.url:
                category="Food Colours & Essence"
                sub_category="none"
            elif "oils-ghee" in response.url:
                category="Oils & Ghee"
            elif "rice" in response.url:
                category="Rice & Rice Products"
            elif "salt-sugar-gur-nuts" in response.url:
                category="Salt, Sugar, Jaggery & Nuts"
            elif "masala-spices" in response.url:
                category="Masala Spices"
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
       

        
