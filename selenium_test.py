
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException    #导入NoSuchElementException
import time
from download_driver import auto_download_chromedrive

class MySelenium(object):
    def __init__(self):
        self.basic_url = "https://www.baidu.com/"
        self.executable_path = r"./chromedriver_win32/chromedriver.exe"

    @property
    def start_driver(self):
        try:
            self.browser = webdriver.Chrome(executable_path=self.executable_path)
            self.browser.maximize_window()
        except SessionNotCreatedException:
            print("Chrome version unmatch. ")
            return None
        return 1

    def request_url(self, url):
        """
        :param url:
        """
        self.browser.get(url)

if __name__ == '__main__':
    start_time = time.time()
    ms = MySelenium()
    if not ms.start_driver:
        chrome = auto_download_chromedrive()
        chrome.start()
        ms.start_driver
        ms.request_url(ms.basic_url)
        #ms.close()
    test_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(test_time)