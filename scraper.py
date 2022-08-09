from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import io
from PIL import Image
import time

options = Options()
options.headless = True
driverPath = 'D:\downloads\chromedriver.exe'
wd = webdriver.Chrome(driverPath, chrome_options=options)

searchTerm = "Dog"

def getImage(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)
	wd.get("https://www.google.com")
	googleText = wd.find_element(By.CLASS_NAME, "gLFyf")
	googleText.send_keys(searchTerm)
	googleText.send_keys(Keys.ENTER)
	wd.find_element(By.LINK_TEXT, "Imágenes").click()
	image_urls = set()
	skips = 0
	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = getImage(wd, 1, 1)

for i, url in enumerate(urls):
	download_image("images\\", url, str(i) + ".jpg")

wd.quit()