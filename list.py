from bs4 import BeautifulSoup
import urllib3
import os
import argparse
import sys
import json


class ScrapeRepos:

    def __init__(self, organization, cookiesFile, debugmode):
        cookies_file = open(cookiesFile,'r')
        self.cookies = cookies_file.readline()
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36", 'Cookie': self.cookies[:-1] }
        self.totalpages = 1
        self.debugmode = debugmode
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager()
        self.query(organization)


    def get_soup(self, url):
        response = self.http.request(url=url, headers=self.header, method='GET')
        return BeautifulSoup(response.data, "html.parser")

    def get_image(self, image):
        return self.http.request(url=image, headers=self.header, method='GET')

    def normalize_query(self, query):
        query = query.split()
        return '+'.join(query)

    def query(self, organization):
        url = "https://github.com/" + self.normalize_query(organization) + "/" 
        soup = self.get_soup(url=url)
        repositories = []
        # extract number of pages
        for a in soup.find_all("em", {"class": "current"}):
            if self.debugmode: print ("Total Pages:" + a['data-total-pages'] )
            self.totalpages= a['data-total-pages']

        for page in range(1, int(self.totalpages)+1):
            if self.debugmode: print ("Getting page:" + str(page))
            url = "https://github.com/" + self.normalize_query(organization) + "?page=" + str(page)
            soup = self.get_soup(url=url)
            # extract all the links
            for a in soup.find_all("a", {"class": "d-inline-block"}):
                if not "language" in a['href']:
                    print (a['href'] )


def main():
    parser = argparse.ArgumentParser(description='List github repositories')
    parser.add_argument('--debug', action='store_true' , help='Enable debugging')
    parser.add_argument('-o', '--organization', type=str, help='organization name', required=True)
    parser.add_argument('-c', '--cookiesFile', type=str, help='File containing the needed cookies', required=True)
    args = parser.parse_args()

    organization = args.organization
    cookiesFile = args.cookiesFile
    debugmode = args.debug

    ScrapeRepos(organization=organization,cookiesFile=cookiesFile,debugmode=debugmode)

    sys.exit()


if __name__ == '__main__':
    main()

