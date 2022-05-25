
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
            item["category"]="Snacks Yummies"
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



            