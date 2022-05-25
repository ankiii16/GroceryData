
from email.mime import image
import scrapy

import functools

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    name=scrapy.Field()
    small_image=scrapy.Field()
    price=scrapy.Field()
    title=scrapy.Field()
    big_image=scrapy.Field()
    description=scrapy.Field()
    ingridients=scrapy.Field()
    expiry=scrapy.Field()
    weight=scrapy.Field()
    brand=scrapy.Field()
    category=scrapy.Field()
    sub_category=scrapy.Field()
    super_category=scrapy.Field()
    discounted_price=scrapy.Field()

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
            price=products.xpath('span/span/bdi').css('bdi::text').get()
            discounted_price=""
            if price is None:
                if products.xpath('span/ins/span/bdi').css('bdi::text') is not None:
                    discounted_price=products.xpath('span/ins/span/bdi').css('bdi::text').get()
            
            item = DmozItem()
            item["name"]=products.css("h3.wd-entities-title").css('a::text').get()
            item["small_image"]=image_url
            item["price"]=price
            item["discounted_price"]=discounted_price
            item["category"]="Rice Flours Lentils Oils Spice"
            item["sub_category"]=category
            item["super_category"]=sub_category
            href=products.xpath("h3/a").attrib['href']
            url = response.urljoin(href)
            callback = functools.partial(self.parse_dir_contents,item)
            yield scrapy.Request(url, callback = callback)   

    
   def parse_dir_contents(self,item, response):
 
    #   item["link"] = response.url
      item["title"] = ""
      item["big_image"] = ""
      item["description"] = ""
      item["ingridients"] = ""
      item["expiry"] = ""
      item["weight"] = ""
      item["brand"] = ""
      summary_element=response.css('div.woocommerce-product-details__short-description')
      if(summary_element is not None):
          if summary_element.xpath("h2/em//text()").extract() is not None:
            item["title"]=''.join(summary_element.xpath("h2/em//text()").extract())
          for paragraphs in summary_element.css("p"):
            if paragraphs.css("::text").getall() is not None:
               text=paragraphs.css("::text").extract()
               completeText = ''.join([str(elem) for elem in text])
               print("completeText",completeText)
               if 'Ingredients:' in completeText:
                    item["ingridients"]=completeText
               elif 'Best Before:' in completeText:
                     item["expiry"]=completeText
               else:
                   matches=["Packaging details:","Origin:","Delivery"]
                   if not any(x.lower() in completeText.lower() for x in matches):
                        item["description"]=item["description"]+completeText
                        if summary_element.xpath("ul/li") is not None:
                            for li in summary_element.xpath("ul/li"):
                                if li.css("::text").get() is not None:
                                    item["description"]=item["description"]+ li.css("::text").get() 

          if response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--weight").css("td::text").get() is not None:
            item["weight"]="".join(response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--weight").css("td::text").get())
          if response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_brand").xpath("td/p//text()").extract() is not None:
            item["brand"]="".join(response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_brand").xpath("td/p//text()").extract())
          if response.css("div.product-image-wrap").xpath("figure/a/img") is not None:
            item["big_image"]=response.css("div.product-image-wrap").xpath("figure/a/img").attrib['data-srcset']
         
      return item



            