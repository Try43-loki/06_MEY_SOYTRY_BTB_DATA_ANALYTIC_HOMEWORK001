# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    categoryType = scrapy.Field()
    prodcut_code = scrapy.Field()
    productName = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    review_count = scrapy.Field()
    image= scrapy.Field()
    pass

class CategoriesItem(scrapy.Item):
    categoryType = scrapy.Field()
    pass
