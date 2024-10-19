import time
import sys

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os

# 打开网页
if sys.platform.startswith('linux'):
    service = Service(executable_path=".../driver/chromedriver", log_path=os.devnull)
else:
    service = Service(executable_path=".../driver/chromedriver.exe", log_path=os.devnull)
options = webdriver.ChromeOptions()
options.use_chromium = True

# 设置参数
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])

# 设置无头参数
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('window-size=1920,1080')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument("--remote-allow-origins=*")
options.add_argument('--no-sandbox')  # 给予root执行权限
options.add_argument('--disable-extensions')  # 禁止拓展
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')

# driver = singleDriver.getDriver()
singleDriver.getPage("https://www.remove.bg/zh/t/change-background")

# 等待几秒以观察结果
time.sleep(5)

# 获取并打印页面标题
# print(driver.title)

# 关闭浏览器
singleDriver.getDriver().quit()
