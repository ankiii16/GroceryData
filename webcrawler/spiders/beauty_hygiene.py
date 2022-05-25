
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

