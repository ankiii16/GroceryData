
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
            item["category"]="Bakery Rusks Dairy"
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



            