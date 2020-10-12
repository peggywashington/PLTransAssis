#%%
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

desired_capabilities = DesiredCapabilities.CHROME
# 仅对html的内容进行下载解析,不等待整个界面加载完成（如JS文件，图片等，不包括ajax）
desired_capabilities["pageLoadStrategy"] = "eager"
driver = webdriver.Chrome()
driver.get("https://www.xiami.com/")

# 睡眠时间 手动登录
time.sleep(20)

with open('xiami_cookies.txt','w') as xmck:
	# todo：自动判断是否成功
    xmck.write(json.dumps(driver.get_cookies()))


# %%
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import json

# desired_capabilities = DesiredCapabilities.CHROME
# # 仅对html的内容进行下载解析,不等待整个界面加载完成（如JS文件，图片等，不包括ajax）
# desired_capabilities["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get("https://www.xiami.com/")

# 自动登录
# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()
# 加载cookie
with open('xiami_cookies.txt','r') as xmck:
    #使用json读取cookies 注意读取的是文件 所以用load而不是loads
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

# 自动刷新更新登录状态
driver.refresh()

# new window
# 转到导入歌单页 据说由于中间有selenium代码的话 无法保持webdriver=undifined 所以直接重新execute然后get新连接
# driver.find_element_by_css_selector(".top-nav-wrapper > .links a:nth-of-type(2)").click()
# WebDriverWait(driver, 50, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".collect-btn")))
# export_btn = driver.find_element_by_css_selector(".collect-btn > .button").click()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get("https://emumo.xiami.com/space/import/u/445322139")

# pl_links = ["https://music.163.com/playlist?id=721552788","https://music.163.com/playlist?id=97289683","https://music.163.com/playlist?id=362059808","https://music.163.com/playlist?id=728889315","https://music.163.com/playlist?id=485406552","https://music.163.com/playlist?id=91545874","https://music.163.com/playlist?id=733122887","https://music.163.com/playlist?id=149984759","https://music.163.com/playlist?id=66369560","https://music.163.com/playlist?id=504347934","https://music.163.com/playlist?id=892310633","https://music.163.com/playlist?id=446662147","https://music.163.com/playlist?id=317670234","https://music.163.com/playlist?id=381714674","https://music.163.com/playlist?id=898072985","https://music.163.com/playlist?id=86215731","https://music.163.com/playlist?id=15046759","https://music.163.com/playlist?id=961091458","https://music.163.com/playlist?id=51555949","https://music.163.com/playlist?id=25695362","https://music.163.com/playlist?id=155900119","https://music.163.com/playlist?id=16654576","https://music.163.com/playlist?id=409419348","https://music.163.com/playlist?id=94820063","https://music.163.com/playlist?id=91202366","https://music.163.com/playlist?id=517078488","https://music.163.com/playlist?id=363939653","https://music.163.com/playlist?id=368819170","https://music.163.com/playlist?id=709435407","https://music.163.com/playlist?id=371960051","https://music.163.com/playlist?id=879546259","https://music.163.com/playlist?id=959551760","https://music.163.com/playlist?id=109233835","https://music.163.com/playlist?id=90662917","https://music.163.com/playlist?id=81078037","https://music.163.com/playlist?id=2039073542","https://music.163.com/playlist?id=68942220","https://music.163.com/playlist?id=395678641","https://music.163.com/playlist?id=865708457","https://music.163.com/playlist?id=2040279275","https://music.163.com/playlist?id=2004326663","https://music.163.com/playlist?id=2096594353","https://music.163.com/playlist?id=156934569","https://music.163.com/playlist?id=32574245","https://music.163.com/playlist?id=627153744","https://music.163.com/playlist?id=608659376","https://music.163.com/playlist?id=1983404863","https://music.163.com/playlist?id=424363280","https://music.163.com/playlist?id=403271795","https://music.163.com/playlist?id=2156539320","https://music.163.com/playlist?id=784135469","https://music.163.com/playlist?id=698794948","https://music.163.com/playlist?id=2502287927","https://music.163.com/playlist?id=639748708","https://music.163.com/playlist?id=2082494553","https://music.163.com/playlist?id=2053195842","https://music.163.com/playlist?id=564638266","https://music.163.com/playlist?id=578452156","https://music.163.com/playlist?id=2649139759","https://music.163.com/playlist?id=2767320996","https://music.163.com/playlist?id=2301805180","https://music.163.com/playlist?id=2705328630","https://music.163.com/playlist?id=2842949865","https://music.163.com/playlist?id=2714529484","https://music.163.com/playlist?id=742670360","https://music.163.com/playlist?id=742464987","https://music.163.com/playlist?id=730404067","https://music.163.com/playlist?id=571370230","https://music.163.com/playlist?id=588396391","https://music.163.com/playlist?id=534069161","https://music.163.com/playlist?id=457324180","https://music.163.com/playlist?id=444769692","https://music.163.com/playlist?id=552845994","https://music.163.com/playlist?id=569763103","https://music.163.com/playlist?id=444747783","https://music.163.com/playlist?id=444781984","https://music.163.com/playlist?id=444804122","https://music.163.com/playlist?id=429239543","https://music.163.com/playlist?id=364784997","https://music.163.com/playlist?id=725746795","https://music.163.com/playlist?id=173642679","https://music.163.com/playlist?id=704584657","https://music.163.com/playlist?id=706241523","https://music.163.com/playlist?id=707112258","https://music.163.com/playlist?id=707546993","https://music.163.com/playlist?id=709577245","https://music.163.com/playlist?id=2664184763","https://music.163.com/playlist?id=2301557416","https://music.163.com/playlist?id=2600506003","https://music.163.com/playlist?id=2305449854","https://music.163.com/playlist?id=2755737993","https://music.163.com/playlist?id=2013636881","https://music.163.com/playlist?id=444773150","https://music.163.com/playlist?id=2382122096","https://music.163.com/playlist?id=2734432453","https://music.163.com/playlist?id=2224949018","https://music.163.com/playlist?id=2479737685","https://music.163.com/playlist?id=2184766344","https://music.163.com/playlist?id=2217122565","https://music.163.com/playlist?id=2144517233","https://music.163.com/playlist?id=3091184317","https://music.163.com/playlist?id=3122151115","https://music.163.com/playlist?id=416091600","https://music.163.com/playlist?id=444761673","https://music.163.com/playlist?id=444750174","https://music.163.com/playlist?id=444751795","https://music.163.com/playlist?id=316735633","https://music.163.com/playlist?id=3107077430","https://music.163.com/playlist?id=3159082853","https://music.163.com/playlist?id=93666003"]
pl_links = ["https://music.163.com/#/playlist?id=3122151115","https://music.163.com/#/playlist?id=427456152","https://music.163.com/#/playlist?id=427456152","https://music.163.com/#/playlist?id=3122151115"]
# www.com 源错误 测试通过
# https://music.163.com/#/playlist?id=151354 曲库没有任何一首 测试通过
# https://music.163.com/#/playlist?id=5283975496 空歌单 测试通过
# https://music.163.com/#/playlist?id=427456152 特殊字符 测试通过
# https://music.163.com/#/playlist?id=310692271 正常（大歌单
# https://music.163.com/#/playlist?id=3122151115 正常（小歌单
# 判断源
source = 0
if("music.163" in pl_links[0]):
	source = 1
elif("y.qq" in pl_links[0]):
	source = 2
elif("kugou" in pl_links[0]):
	source = 3
elif("kuwo" in pl_links[0]):
	source = 4
else:
	driver.execute_script("alert('并非网易云/qq/酷狗/酷我的歌单链接，请检查、更换链接并重新运行main.py');")
	print("Error - 并非网易云/qq/酷狗/酷我的链接，请检查、更换链接并重新运行main.py")

curr_time = datetime.datetime.now()
with open('fail_log.txt','a') as fl:
    fl.write('\n')
    fl.write('----------'+datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')+'----------')
for pl_link in pl_links:
	if source == 0:
		break
	elif source == 1:
		WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtWangyi")))
		driver.find_element_by_id("txtWangyi").clear()
		driver.find_element_by_id("txtWangyi").send_keys(pl_link)
	elif source == 2:
		driver.find_element_by_id("tabNavQQ").click()
		WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtQQ")))
		driver.find_element_by_id("txtQQ").clear()
		driver.find_element_by_id("txtQQ").send_keys(pl_link)
	elif source == 3:
		driver.find_element_by_id("tabNavKuGou").click()
		WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtKuGou")))
		driver.find_element_by_id("txtKuGou").clear()
		driver.find_element_by_id("txtKuGou").send_keys(pl_link)
	elif source == 4:
		driver.find_element_by_id("tabNavKuWo").click()
		WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#txtKuWo")))
		driver.find_element_by_id("txtKuWo").clear()
		driver.find_element_by_id("txtKuWo").send_keys(pl_link)
    # todo:拖滑块
	WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text > span > b')))
	WebDriverWait(driver, 600, 0.5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#nc_1__scale_text > span > b'),'验证通过'))
	# print(driver.find_element_by_css_selector("#nc_1__scale_text > span > b").text)
	driver.find_element_by_id("btnGetData").click()


	WebDriverWait(driver, 60, 0.5).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loading')))
	try:
		# loading消失之后立马检测
		WebDriverWait(driver, 1, 0.5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#toast")))
		fail_info = driver.find_element_by_id("toast-info").text
		print("System msg - "+fail_info)
		if(fail_info.find("导入失败")!=-1):
			log = "歌单： "+pl_link+" 导入失败，很可能因为虾米的曲库中没有歌单中任何一首歌。"
			print("Warning - "+log)
			with open('fail_log.txt','a') as fl:
				fl.write('\n')
				fl.write(log)
		elif(fail_info.find("正在帮你")!=-1):
			log = "歌单： "+pl_link+" 很可能原本就为空。"
			print("Warning - "+log)
			with open('fail_log.txt','a') as fl:
				fl.write('\n')
				fl.write(log)
		elif(fail_info.find("系统错误")!=-1):
			log = "从歌单： "+pl_link+" 开始未成功，请删除pl_links中已成功的歌单链接并重新运行main.py。"
			print("Warning - "+log)
			with open('fail_log.txt','a') as fl:
				fl.write('\n')
				fl.write(log)
		elif(fail_info.find("操作频繁")!=-1):
			log = "从歌单： "+pl_link+" 开始未成功，近期歌单导入次数已达上限，明天再试叭（实测几个小时是不够的）。"
			print("Warning - "+log)
			with open('fail_log.txt','a') as fl:
				fl.write('\n')
				fl.write(log)
	except TimeoutException:
		WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#post-data')))
		driver.find_element_by_id("btnPostData").click()
		# 等loading消失
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
				# todo: 最好能alert。。但是很快就过去了 不知咋回事
				print("Advice - 请删除歌单名称中的特殊字符之后手动点击导入歌单按钮，直到成功，给你60秒")
				try:
					WebDriverWait(driver, 60, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#toastSuccess")))
					driver.find_element_by_id("toast-success-info-close").click()
				except TimeoutException:
					log = "从歌单： "+pl_link+" 开始未成功，该歌单名称含有特殊字符，请删除已导入歌单链接后重新运行main.py，提示“创建失败”后在60s内删除特殊字符并手动点击“导入歌单”。"
					print("Warning - "+log)
					with open('fail_log.txt','a') as fl:
						fl.write('\n')
						fl.write(log)
	

# %%
