from win32com.client import Dispatch
import re
import stat,zipfile,os,psutil
import requests
from lxml import etree
import time

class auto_download_chromedrive(object):
    def __init__(self):
        self.chromedrive_url = "https://chromedriver.chromium.org/downloads"
        self.local_chrome_paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                   r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]

        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    def get_version_via_com(self, filename):
        parser = Dispatch("Scripting.FileSystemObject")
        try:
            version = parser.GetFileVersion(filename)
        except Exception:
            return None
        return version
    def get_chromedriver_urls(self):
        try:
            r = requests.Session()
            response = r.get(self.chromedrive_url, headers=self.headers)
            print(response.status_code, response.encoding)
            html = etree.HTML(response.text, etree.HTMLParser())  # 解析HTML文本内容
            version_href = html.xpath(".//strong//..//@href")
            print("all chrome browser versions can be choosed:")
            for href in version_href:
                print(href)

            return version_href
        except Exception:
            return None
    def download_chromadrive(self, url):
        try:
            r = requests.Session()
            response = r.get(url, headers=self.headers)
            if response.status_code == 200:
                with open("chromedriver_win32.zip", "wb") as f:
                    f.write(response.content)
                    print("下载完成")
                    return 1
            else:
                print('Url请求返回错误，错误码为： %d' % response.status_code)
                return None
        except Exception:
            print("request download chromedriver_win32.zip failed!")
            return None
    def find_local_version(self, loc_ver, all_ver):
        """
        :param loc_ver: 本地浏览器的版本
        :param all_ver: 下载的所有版本浏览器版本
        :return: 找到匹配的，return url,否则return None
        """
        for href in all_ver:
            try:
                res = re.search(r"path=(.*?)/", href)
                find_ver = res.group(1).split(".")[0] #截取大版本
                if loc_ver == find_ver:
                    return href
            except Exception:
                continue

        print("not find match chrome browser{} version!".format(loc_ver))
        return None
    def kill_process(self, process_name):
        print("检测{}进程是否存在，存在则杀掉。".format(process_name))
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                print('{} 存在进程中,杀掉'.format(process_name))
                os.popen('taskkill /f /im %s' %process_name)
                return pid
        print('{} 不存在进程中。'.format(process_name))
        return None

    def unzip(self):
        self.kill_process("chromedriver.exe")
        print("去除旧版本chromedriver_win32文件夹内文件的只读属性(如果是只读)")
        old_driver_path = os.path.join(os.getcwd(), "chromedriver_win32")
        if os.path.exists(old_driver_path):
            for sub_file in os.listdir(old_driver_path):
                os.chmod(os.path.join(old_driver_path, sub_file), stat.S_IRWXU)
        time.sleep(1) #这个delay必须要有，os操作还是需要时间的
        print('''解压 chromedriver_win32.zip,覆盖旧版本''')
        zFile = zipfile.ZipFile(os.path.join(os.getcwd(), "chromedriver_win32.zip"), "r")
        for fileM in zFile.namelist():
            zFile.extract(fileM, old_driver_path)
        zFile.close()


    def start(self):
        '''读取本地chrome version'''
        version = list(filter(None, [self.get_version_via_com(p) for p in self.local_chrome_paths]))[0]
        if not version:
            print("check chrome browser version failed!")
            return None
        print("chrome browser version:", version)
        '''下载网页端与本地匹配的chromedriver.exe'''
        version_href = self.get_chromedriver_urls()
        if not version_href:
            print("request %s failed!"%self.chromedrive_url)
            return None

        find_url = self.find_local_version(version.split(".")[0], version_href)
        print("找到匹配的版本:\n%s"%find_url)
        if not find_url:
            return None
        version_num = re.search(r"path=(.*?)/", find_url).group(1)
        find_url_2 = find_url.rsplit('/', 2)[0]
        new_url = "{}/{}/chromedriver_win32.zip".format(find_url_2, version_num)
        print("downloading......\n%s"%new_url)
        ret = self.download_chromadrive(new_url)
        if not ret:
            return None
        self.unzip()

if __name__ == "__main__":
    chrome = auto_download_chromedrive()
    chrome.start()





