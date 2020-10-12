#%%
# 获取cookie以便自动登录
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

driver = webdriver.Chrome()
driver.get("https://www.xiami.com/")

# 睡眠时间手动登录
time.sleep(40)

with open('xiami_cookies.txt','w') as xmck:
    xmck.write(json.dumps(driver.get_cookies()))
# %%
