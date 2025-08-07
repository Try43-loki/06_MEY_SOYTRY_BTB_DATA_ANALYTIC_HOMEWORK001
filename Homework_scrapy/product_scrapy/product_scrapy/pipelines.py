# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


class ProductScrapyPipeline:
    def __init__(self):
        self.data = {}
    def process_item(self, item, spider):
        if spider.name == "product":
            category = item.get('categoryType','Unknown')
            if category not in self.data:
                self.data[category] = []
            self.data[category].append(dict(item))
            return item
    def close_spider(self, spider):
        with open('grouped_products102.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)



            
