import time
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from testimonials.items import TestimonialsItem
class TestimonialSpider(scrapy.Spider):
    name = "testimonial"
    allowed_domains = ["web-scraping.dev"]

    def start_requests(self):
        url = 'https://web-scraping.dev/login?cookies='
        yield SeleniumRequest(url= url, callback=self.parse  )

    def accept_cookie(self,driver):
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="cookie-ok"]').click()

    def perform_login(self,driver):
        time.sleep(1)
        driver.find_element(By.NAME, 'username').send_keys("user123")
        driver.find_element(By.NAME, 'password').send_keys("password")
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    def perform_auto_scroll(self,driver):
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="navbarContent"]/ul[1]/li[4]/a').click()
        
        # auto scroll
        driver.maximize_window()
        last_height = 0
        while True:
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(1)  

            new_height = driver.execute_script("return document.body.scrollHeight")
            print(f"{new_height} {last_height}")

            if new_height == last_height:
                break
            last_height = new_height

    def parse(self, response):
        driver = response.meta['driver']
        self.accept_cookie(driver)
        self.perform_login(driver)
        self.perform_auto_scroll(driver)

        testimonials_contianer = driver.find_element(By.XPATH,'//div[@class="testimonials"]')
        testimonials = testimonials_contianer.find_elements(By.XPATH,'.//div[@class="testimonial"]')
        
        for testimonial in testimonials:
            item = TestimonialsItem()
            item['testimonial'] = testimonial.find_element(By.XPATH,'.//p[@class="text"]').text.strip()
            rating_count =  testimonial.find_elements(By.CSS_SELECTOR, 'span.rating svg')
            item['ratings'] = len(rating_count)
            yield item

