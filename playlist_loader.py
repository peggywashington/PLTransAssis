import time
from selenium.webdriver.chrome.webdriver import WebDriver


def from_netease(driver: WebDriver, playlist_entry: str=None) -> list:
	"""

	:param driver:
	:param playlist_entry: 个人歌单主页，未给则从首页点击进入
	:return:
	"""
	# 获取src playlist
	if playlist_entry is None:
		driver.get('https://music.163.com/')

		# netease-specific
		driver.switch_to.frame('g_iframe')
		time.sleep(1)

		# 前往个人主页
		netease_home_ele = driver.find_element_by_xpath("//a[contains(@href, '/user/home')]")
		netease_home_ele.click()

		time.sleep(1)
	else:
		driver.get(playlist_entry)
		driver.switch_to.frame('g_iframe')
		time.sleep(1)

	# 滚到直到所有歌单都懒加载完毕
	page_content_len = len(driver.page_source)
	top = 5000
	driver.execute_script('document.documentElement.scrollTop={}'.format(top))
	time.sleep(1)

	while page_content_len != len(driver.page_source):
		page_content_len = len(driver.page_source)
		top += 5000
		driver.execute_script('document.documentElement.scrollTop={}'.format(top))
		time.sleep(1)

	# 包含自己创建的和收藏的歌单
	playlist_eles = driver.find_elements_by_css_selector('.msk')
	playlist_urls = list()
	for ele_playlist in playlist_eles:
		playlist_urls.append(ele_playlist.get_attribute('href'))

	return playlist_urls


def from_file(path: str='playlist_urls.txt') -> list:
	playlist_urls = list()
	with open(path, 'r') as f:
		playlist_urls = [url.strip() for url in f.readlines()]
	return playlist_urls
