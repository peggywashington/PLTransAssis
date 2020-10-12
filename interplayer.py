from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

import time
import datetime
import random


class Transfer:
	@classmethod
	def to_xiami(cls, driver: WebDriver, url_src_playlists: list, _from: int=1, transfer_entry: str=None):
		"""

		:param driver:
		:param url_src_playlists:
		:param _from:
		:param transfer_entry: 虾米导入歌单页面url
		:return:
		"""
		if transfer_entry is None:
			driver.get('https://www.xiami.com/')
			# xiami-specific
			# handle 签到页面
			time.sleep(1)
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

		cls.__transfer(driver, url_src_playlists, _from, 'xiami')

	@classmethod
	def __transfer(cls, driver: WebDriver, url_src_playlists: list, _from=None, _to='xiami'):
		if _from is None:
			if "music.163" in url_src_playlists[0]:
				_from = 1
			elif "y.qq" in url_src_playlists[0]:
				_from = 2
			elif "kugou" in url_src_playlists[0]:
				_from = 3
			elif "kuwo" in url_src_playlists[0]:
				_from = 4
			else:
				driver.execute_script("alert('并非网易云/qq/酷狗/酷我的歌单链接，请检查、更换链接并重新运行main.py');")
				print("Error - 并非网易云/qq/酷狗/酷我的链接，请检查、更换链接并重新运行main.py")

		curr_time = datetime.datetime.now()
		with open('fail_log.txt', 'a') as fl:
			fl.write('\n')
			fl.write('----------' + datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S') + '----------')

		for url_src_playlist in url_src_playlists:
			# input url
			if _from == 0:
				break
			elif _from == 1:
				WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtWangyi")))
				driver.find_element_by_id("txtWangyi").clear()
				driver.find_element_by_id("txtWangyi").send_keys(url_src_playlist)
			elif _from == 2:
				driver.find_element_by_id("tabNavQQ").click()
				WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtQQ")))
				driver.find_element_by_id("txtQQ").clear()
				driver.find_element_by_id("txtQQ").send_keys(url_src_playlist)
			elif _from == 3:
				driver.find_element_by_id("tabNavKuGou").click()
				WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtKuGou")))
				driver.find_element_by_id("txtKuGou").clear()
				driver.find_element_by_id("txtKuGou").send_keys(url_src_playlist)
			elif _from == 4:
				driver.find_element_by_id("tabNavKuWo").click()
				WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtKuWo")))
				driver.find_element_by_id("txtKuWo").clear()
				driver.find_element_by_id("txtKuWo").send_keys(url_src_playlist)

			# auto slide
			time.sleep(1)
			slider_captcha = driver.find_element_by_id('nc_1__scale_text')
			slider_captcha_width = slider_captcha.size['width']
			offset = [slider_captcha_width / 8, slider_captcha_width * 3 / 8, slider_captcha_width / 2]
			action = ActionChains(driver)
			action.click_and_hold(slider_captcha)
			for x in offset:
				action.move_by_offset(xoffset=x, yoffset=0)
			action.release().perform()
			time.sleep(random.randint(1, 3))

			# wait for prompt
			WebDriverWait(driver, 600, 0.5).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text > span > b')))
			WebDriverWait(driver, 600, 0.5).until(
				EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#nc_1__scale_text > span > b'), '验证通过'))
			# print(driver.find_element_by_css_selector("#nc_1__scale_text > span > b").text)
			driver.find_element_by_id("btnGetData").click()

			WebDriverWait(driver, 60, 0.5).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loading')))

			try:
				# loading消失之后立马检测
				WebDriverWait(driver, 1, 0.5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#toast")))
				fail_info = driver.find_element_by_id("toast-info").text
				print("System msg - " + fail_info)
				if fail_info.find("导入失败") != -1:
					log = "歌单： " + url_src_playlist + " 导入失败，很可能因为虾米的曲库中没有歌单中任何一首歌。"
					print("Warning - " + log)
					with open('fail_log.txt', 'a', encoding='utf-8') as fl:
						fl.write('\n')
						fl.write(log)
				elif fail_info.find("正在帮你") != -1:
					log = "歌单： " + url_src_playlist + " 很可能原本就为空。"
					print("Warning - " + log)
					with open('fail_log.txt', 'a', encoding='utf-8') as fl:
						fl.write('\n')
						fl.write(log)
				elif fail_info.find("系统错误") != -1:
					log = "从歌单： " + url_src_playlist + " 开始未成功，请删除pl_links中已成功的歌单链接并重新运行main.py。"
					print("Warning - " + log)
					with open('fail_log.txt', 'a', encoding='utf-8') as fl:
						fl.write('\n')
						fl.write(log)
				elif fail_info.find("操作频繁") != -1:
					log = "从歌单： " + url_src_playlist + " 开始未成功，近期歌单导入次数已达上限，明天再试叭（实测几个小时是不够的）。"
					print("Warning - " + log)
					with open('fail_log.txt', 'a', encoding='utf-8') as fl:
						fl.write('\n')
						fl.write(log)
				WebDriverWait(driver, 60, 0.5).until_not(
					EC.visibility_of_element_located((By.CSS_SELECTOR, '#toast')))
			except TimeoutException:
				WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#post-data')))
				driver.find_element_by_id("btnPostData").click()
				# 等loading消失
				WebDriverWait(driver, 60, 0.5).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loading')))
				# WebDriverWait(driver, 60, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id^="toast"]')))
				success = driver.find_element_by_id("toastSuccess").get_attribute("style")
				success_start = success.find("display")
				if success_start != -1 and success[success_start:success_start + 14].find("block") != -1:
					driver.find_element_by_id("toast-success-info-close").click()
				else:
					fail_info = driver.find_element_by_id("toast-info").text
					print("System msg - " + fail_info)
					if fail_info.find("创建失败") != -1:
						# todo: 最好能alert。。但是很快就过去了 不知咋回事
						print("Advice - 请删除歌单名称中的特殊字符之后手动点击导入歌单按钮，直到成功，给你60秒")
						try:
							WebDriverWait(driver, 60, 0.5).until(
								EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastSuccess")))
							driver.find_element_by_id("toast-success-info-close").click()
						except TimeoutException:
							log = "从歌单： " + url_src_playlist + " 开始未成功，该歌单名称含有特殊字符，请删除已导入歌单链接后重新运行main.py，提示“创建失败”后在60s内删除特殊字符并手动点击“导入歌单”。"
							print("Warning - " + log)
							with open('fail_log.txt', 'a', encoding='utf-8') as fl:
								fl.write('\n')
								fl.write(log)
