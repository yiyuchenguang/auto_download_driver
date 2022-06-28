
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException    #导入NoSuchElementException
import time
from download_driver import auto_download_chromedrive

class MySelenium(object):
    def __init__(self):
        self.basic_url = "https://www.baidu.com/"
        self.executable_path = r"./chromedriver_win32/chromedriver.exe"
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    @property
    def start_driver(self):
        try:
            self.browser = webdriver.Chrome(executable_path=self.executable_path)
            self.browser.maximize_window()
        except SessionNotCreatedException:
            print("Chrome version unmatch. ")

            chrome = auto_download_chromedrive()
            if chrome.start():
                return 1
            else:
                return None
        return 1

    def request_url(self, url):
        """
        :param url:
        """
        self.browser.get(url = url)

if __name__ == '__main__':

        start_time = time.time()
        ms = MySelenium()
        print(ms)
        print(ms.start_driver)
        if ms.start_driver:
                ms.request_url(ms.basic_url)
            #ms.close()
        test_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        print(test_time)
