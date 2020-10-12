from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import time
import random
class Transfer:
	@classmethod
	def to_xiami(cls, driver: WebDriver, url_src_playlists: list, _from: str='netease', transfer_entry: str=None) -> bool:
		if transfer_entry is None:
			driver.get('https://www.xiami.com/')

			# xiami-specific
			# handle 签到页面
			time.sleep(1)
			print(driver.page_source)
			WebDriverWait(driver, 15, 0.5).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, 'div.user div.avatar img')))
			my_music_ele = driver.find_element_by_partial_link_text('我的音乐')
			my_music_ele.click()
			time.sleep(1)

			WebDriverWait(driver, 15, 0.5).until(
				EC.presence_of_element_located((By.XPATH, "//div[starts-with(text(), '导入歌单')]")))

			import_ele = driver.find_element_by_xpath("//div[starts-with(text(), '导入歌单')]")
			import_ele.click()
			# 导入歌单会在新标签打开，使绕过失效
			driver.switch_to.window(driver.window_handles[1])
			url = driver.current_url
			driver.switch_to.window(driver.window_handles[0])
			driver.get(url)
			driver.switch_to.window(driver.window_handles[1])
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
		else:
			driver.get(transfer_entry)

		# if _from == 'netease':
		# 	for pl_link in url_src_playlists:
		# 		WebDriverWait(driver, 15, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtWangyi")))
		# 		driver.find_element_by_id("txtWangyi").clear()
		# 		driver.find_element_by_id("txtWangyi").send_keys(pl_link)
		# 		time.sleep(1)
		# 		slider_captcha = driver.find_element_by_id('nc_1__scale_text')
		# 		slider_captcha_width = slider_captcha.size['width']
		# 		offset = [slider_captcha_width / 8, slider_captcha_width * 3 / 8, slider_captcha_width / 2]
		# 		action = ActionChains(driver)
		# 		action.click_and_hold(slider_captcha)
		# 		for x in offset:
		# 			action.move_by_offset(xoffset=x, yoffset=0)
		# 		action.release().perform()
		# 		time.sleep(random.randint(1, 3))
		# 		WebDriverWait(driver, 15, 0.5).until(
		# 			EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text > span')))
		# 		WebDriverWait(driver, 15, 0.5).until(
		# 			EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#nc_1__scale_text > span'), '验证通过'))
		# 		print(driver.find_element_by_css_selector("#nc_1__scale_text > span").text)
		# 		time.sleep(random.randint(1, 3))
		# 		driver.find_element_by_id("btnGetData").click()
		# 		WebDriverWait(driver, 15, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#post-data')))
		# 		time.sleep(random.randint(1, 3))
		# 		driver.find_element_by_id("btnPostData").click()
		# 		WebDriverWait(driver, 15, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#toastSuccess')))
		# 		time.sleep(random.randint(1, 3))
		# 		driver.find_element_by_id("toast-success-info-close").click()
		# 	return True
		# return False
