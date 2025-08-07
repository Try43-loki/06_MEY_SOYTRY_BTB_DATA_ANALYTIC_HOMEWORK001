# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


class TestimonialsPipeline:

    def __init__(self):
        self.testimonials = []

    def process_item(self, item, spider):
        if spider.name == "testimonial":
            self.testimonials.append(dict(item))
        return item
    def close_spider(self,spider):
        if spider.name == "testimonial":
            with open("testimonial.json", 'w', encoding='utf-8') as file:
                json.dump({"testimonials":self.testimonials},file,ensure_ascii=False,indent=4)
