import time
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from testimonials.items import TestimonialsItem
class TestimonialSpider(scrapy.Spider):
    name = "testimonial"
    allowed_domains = ["web-scraping.dev"]
    def start_requests(self):
        url = 'https://web-scraping.dev/login?cookies='
        yield SeleniumRequest(url= url, callback=self.accept_cookie,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.XPATH,'//div[@class="modal-content"]'))
          )

    def accept_cookie(self,response):
        driver = response.meta['driver']
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="cookie-ok"]').click()
            time.sleep(1)
        except Exception as err:
            self.logger.info(f"Could not found element{err}")
        self.perform_login(driver)
        yield SeleniumRequest(
            url='https://web-scraping.dev/testimonials',
            callback=self.parse,
        )
    def perform_login(self,driver):
        try:
            time.sleep(1)
            driver.find_element(By.NAME, 'username').send_keys("user123")
            driver.find_element(By.NAME, 'password').send_keys("password")
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(1)
        except Exception as err:
            self.logger.info(f"Could not found element {err}")
        
    def parse(self, response):
        driver = response.meta['driver']
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="navbarContent"]/ul[1]/li[4]/a').click()
        MAX_SCROLLS = 50      
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        while scroll_count < MAX_SCROLLS:
         
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1

        testimonials_contianer = driver.find_element(By.XPATH,'//div[@class="testimonials"]')
        testimonials = testimonials_contianer.find_elements(By.XPATH,'.//div[@class="testimonial"]')
        
        for testimonial in testimonials:
            item = TestimonialsItem()
            item['testimonial'] = testimonial.find_element(By.XPATH,'.//p[@class="text"]').text.strip()
            rating_count =  testimonial.find_elements(By.CSS_SELECTOR, 'span.rating svg')
            item['ratings'] = len(rating_count)
            yield item

