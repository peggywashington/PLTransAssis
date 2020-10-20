# %%
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import json

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get("https://www.xiami.com/")

# 加载cookie，自动登录
driver.delete_all_cookies()
with open('xiami_cookies.txt','r') as xmck:
    cookieslist = json.load(xmck)
    # 方法1 将expiry类型变为int
    for cookie in cookieslist:
        #并不是所有cookie都含有expiry 所以要用dict的get方法来获取
        if isinstance(cookie.get('expiry'), float):
            cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)
    #方法2删除该字段
    # for cookie in cookieslist:
    #     #该字段有问题所以删除就可以  浏览器打开后记得刷新页面 有的网页注入cookie后仍需要刷新一下
    #     if 'expiry' in cookie:
    #         del cookie['expiry']
    #     driver.add_cookie(cookie)
driver.refresh()

# 转到导入歌单页
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
# ----------这里替换自己的虾米userid----------
driver.get("https://emumo.xiami.com/space/import/u/<替换userid>")

# ----------这里放歌单链接，例：pl_links = ["https://music.163.com/#/playlist?id=310692271","https://music.163.com/#/playlist?id=2714529484","https://music.163.com/#/playlist?id=117586346"]
pl_links = []

# 判断源
source = ""
if("music.163" in pl_links[0]):
	source = "Wangyi"
elif("y.qq" in pl_links[0]):
	source = "QQ"
elif("kugou" in pl_links[0]):
	source = "KuGou"
elif("kuwo" in pl_links[0]):
	source = "KuWo"
else:
	driver.execute_script("alert('并非网易云/qq/酷狗/酷我的歌单链接，请检查、更换链接并重新运行main.py');")
	print("Error - 并非网易云/qq/酷狗/酷我的链接，请检查、更换链接并重新运行main.py")

curr_time = datetime.datetime.now()
with open('fail_log.txt','a') as fl:
    fl.write('\n')
    fl.write('----------'+datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')+'----------')
for pl_link in pl_links:
	if source == "":
		break
	else:
		if source != "Wangyi":
			driver.find_element_by_id("tabNav"+source).click()
		WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txt"+source)))
		driver.find_element_by_id("txt"+source).clear()
		driver.find_element_by_id("txt"+source).send_keys(pl_link)
    # todo:手动拖滑块
	WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text > span > b')))
	WebDriverWait(driver, 600, 0.5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#nc_1__scale_text > span > b'),'验证通过'))
	# print(driver.find_element_by_css_selector("#nc_1__scale_text > span > b").text)
	driver.find_element_by_id("btnGetData").click()


	WebDriverWait(driver, 60, 0.5).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loading')))
	try:
		WebDriverWait(driver, 1, 0.5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#toast")))
		fail_info = driver.find_element_by_id("toast-info").text
		print("System msg - "+fail_info)
		log = ""
		if(fail_info.find("导入失败")!=-1):
			log = "歌单： "+pl_link+" 导入失败，很可能因为虾米的曲库中没有歌单中任何一首歌。"
		elif(fail_info.find("正在帮你")!=-1):
			log = "歌单： "+pl_link+" 很可能原本就为空。"
		elif(fail_info.find("系统错误")!=-1):
			log = "从歌单： "+pl_link+" 开始未成功，请删除pl_links中已成功的歌单链接并重新运行main.py。"
		elif(fail_info.find("操作频繁")!=-1):
			log = "从歌单： "+pl_link+" 开始未成功，近期歌单导入次数已达上限，明天再试叭（实测几个小时是不够的）。"
		print("Warning - "+log)
		with open('fail_log.txt','a',encoding='utf-8') as fl:
			fl.write('\n')
			fl.write(log)
	except TimeoutException:
		WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#post-data')))
		driver.find_element_by_id("btnPostData").click()
		WebDriverWait(driver, 60, 0.5).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loading')))
		# WebDriverWait(driver, 60, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id^="toast"]')))
		success = driver.find_element_by_id("toastSuccess").get_attribute("style")
		success_start = success.find("display")
		if(success_start!=-1 and success[success_start:success_start+14].find("block")!=-1):
			driver.find_element_by_id("toast-success-info-close").click()
		else:
			fail_info = driver.find_element_by_id("toast-info").text
			print("System msg - "+fail_info)
			if(fail_info.find("创建失败")!=-1):
				print("Advice - 请删除歌单名称中的特殊字符之后手动点击导入歌单按钮，直到成功，给你60秒")
				try:
					WebDriverWait(driver, 60, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastSuccess")))
					driver.find_element_by_id("toast-success-info-close").click()
				except TimeoutException:
					log = "从歌单： "+pl_link+" 开始未成功，该歌单名称含有特殊字符，请删除已导入歌单链接后重新运行main.py，提示“创建失败”后在60s内删除特殊字符并手动点击“导入歌单”。"
					print("Warning - "+log)
					with open('fail_log.txt','a',encoding='utf-8') as fl:
						fl.write('\n')
						fl.write(log)
# %%
