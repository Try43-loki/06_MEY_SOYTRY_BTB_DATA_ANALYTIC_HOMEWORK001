from email.policy import default
from itertools import product
import scrapy

from product_scrapy.items import  ProductScrapyItem


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com"]
    def parse(self, response):
        categories = response.xpath('//ul[@id="nav-one"]/li/a')
        categories_text = categories.xpath('text()').getall()
        category_liks = categories.xpath('@href').getall()
        for name, link in zip(categories_text, category_liks):
             yield response.follow(link, callback=self.parse_category, meta={'category': name.strip()})

    #===================== follow link by categories
    def parse_category(self, response):
        category = response.meta.get('category','Unknown')
        products = response.xpath('//div[@class="product-block product-thumb"]')
        for product in products:
            link_detail = product.xpath('.//div[@class="image"]/a/@href').get()
            if link_detail is not None:
                yield response.follow(link_detail, callback=self.parse_product_detail, meta={'category': category})

        next_page = response.xpath('//ul[@class="pagination"]/li[position() = last() - 1]/a/@href').get()
        # print("next_page ===============", next_page)
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse_category,meta={'category': category})
    
    #===================== product detail
    def parse_product_detail(self, response):

        item = ProductScrapyItem()

        product_containt = response.xpath('//div[@id="content"]')
        item['categoryType'] = response.meta.get('category', 'Unknown')
        item['productName'] = product_containt.xpath('.//h3[@class="product-title"]/text()').get(default = "No Name").strip()
        item['brand'] = product_containt.xpath('.//div[1]/div[2]/ul[1]/li[1]/a/text()').get(default = "No Brand") or response.xpath('.//div[1]/div[2]/ul[1]/li/text()').get(default = "No Brand").strip()
        item['prodcut_code'] = product_containt.xpath('.//div[1]/div[2]/ul[1]/li/text()').get(default = "No Code") or product_containt.xpath('.//div[1]/div[2]/ul[1]/li[2]/text()').get(default = "No Code").strip()
        item['price'] = product_containt.xpath('.//div[1]/div[2]/ul[2]/li/h3/text()').get(default = "No Price") or product_containt.xpath('.//div/div[2]/ul[2]/li/h4/text()').get(default = "No Price").strip()
        item['review_count'] = product_containt.xpath('.//div[1]/div[2]/div[1]/a[1]/text()').get(default = "No Review").strip()
        item['image'] = response.xpath('//img[@id="tmzoom"]/@src').get(default = "No Image")
        yield item
         