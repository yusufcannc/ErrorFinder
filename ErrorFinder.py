import requests
import argparse
from bs4 import BeautifulSoup
import regex
from concurrent.futures import ThreadPoolExecutor

import urllib3
import time 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
start = time.time()
_regex =[
    r"^\Winternal",
    r"(\.*(?i)\bphysical path\b)",
    r"(\.*(?i)\bline\b\s\d\d*)",
    r"(\.*(?i)\bLine Number\b\W\W[0-9]*)",
    r"(\.*(?i)\bArgumentException\b)",
    r"(\.*(?i)\btraceback\b)",
    r"(\.*(?i)\bVersion Information\b\W Microsoft)",
    r"(\.*(?i)\b<role \b)",
    r"(\.*(?i)\bRequest Method\b)",
    r"(\.*(?i)\bErrorException\b)",
    r"(\.*(?i)\bWeb.config\b)",
    r"(\.*(?i)\bFormatException\b)",
    r"(\.*Exception Details)",
    r"(\.*(?i)\bError Occurred While Processing Request\b)",
    r"(\.*(?i)\blocal.ERROR\b)",
    r"(\.*(?i)\bError Log for ROOT\b)",
    r"(\.*(?i)\bApache Tomcat\b\S*)",
    r"(\.*(?i)\b\nginx\b*)",
    r"(\.*(?i)\bApache Tomcat\b*)",
   






]



def __getURLS(argumans):
    urls = []
    with open(argumans, 'r+') as file:
        for i in file:
            urls.append(i.split('\n')[0])
    __requestThread(urls)


def __requestThread(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            executor.submit(getReq, url)






def regexSearch(content, url, regexs):
    regex_match = regex.findall(regexs, str(content))
    if regex_match != None:
        print(f"Found Imprepor Error Page, Match: {regex_match[0]} --> {url}")
    else:
        pass

       


def getReq(url):
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            req = requests.get(url, timeout=5, verify=False)
            soup = BeautifulSoup(req.content, 'lxml')
            for i in _regex:
                executor.submit(regexSearch, str(soup), url, i)     

    except (requests.exceptions.ConnectionError, 
    requests.exceptions.ReadTimeout,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.InvalidURL,
    requests.exceptions.ChunkedEncodingError
    ) as e:
        pass


              

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="File name of urls")
    parser.add_argument("--website", "-w", help="Website")
    argumans = parser.parse_args()
    if argumans.file != None:
        __getURLS(argumans.file)
    else:
        getReq(argumans.website)





if __name__ == "__main__":
    main()
    print(time.time() - start)
