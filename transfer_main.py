from selenium import webdriver

import playlist_loader
import interplayer

import time
import random

import browser_cookie3
from urllib.parse import urlparse


driver = webdriver.Chrome()
driver.maximize_window()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 避免检测
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

# 要先打开网址，再加cookie
SRC_ENTRY = 'https://music.163.com/'
DST_ENTRY = 'https://www.xiami.com/'


domain_names = list()
for url in [SRC_ENTRY, DST_ENTRY]:
	netloc = urlparse(url)[1]
	for word in netloc.split('.')[:-1]:
		if word != 'www':
			domain_names.append(word)

driver.get(SRC_ENTRY)
driver.get(DST_ENTRY)

cj_list = [browser_cookie3.chrome(domain_name=name) for name in domain_names]

for cj in cj_list:
	for cookie in cj:
		# cookie_dict: A dictionary object, with required keys - "name" and "value";
		# optional keys - "path", "domain", "secure", "expiry"
		try:
			cookie_dict = dict()
			cookie_dict['name'] = cookie.name
			cookie_dict['value'] = cookie.value
			cookie_dict['path'] = cookie.path
			cookie_dict['domain'] = cookie.domain
			cookie_dict['secure'] = True if cookie.secure == 1 else False
			cookie_dict['expiry'] = cookie.expires
			driver.add_cookie(cookie_dict)
		except:
			continue
print("cookies loaded")


# 获取src playlist
url_src_playlists = playlist_loader.from_file()
print(url_src_playlists)

interplayer.Transfer.to_xiami(driver, url_src_playlists)
