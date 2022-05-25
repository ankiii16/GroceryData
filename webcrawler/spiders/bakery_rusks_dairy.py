
import functools
import scrapy

# item class included here 
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

            discounted_price=""
            price=products.xpath('span/span/bdi').css('bdi::text').get()
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

