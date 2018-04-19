import requests
from os import environ
from bs4 import BeautifulSoup

from util.getter import get_num, get_year, get_branch, get_college, get_c_id, get_branch_name

class Student:
    try:
        proxyDict = {
                    'http_proxy': environ['http_proxy'],
                    'https_proxy': environ['https_proxy'],
                    'ftp_proxy': environ['ftp_proxy']
                }
    except KeyError:
        proxyDict = None

    def __init__(self,roll):
        roll = str(roll)
        self.inflate_data(roll)

    def inflate_data(self,roll):
        self.year = get_year(roll)
        self.num = get_num(roll)
        self.branch = get_branch(roll)
        self.branch_name = get_branch_name(self.branch)
        self.c_id = get_c_id(roll)
        self.college = get_college(roll)
        self.roll_num = self.year+self.branch+self.num
        if(roll[0]=='i'):
            self.roll_num = "iiitu" + self.roll_num
        self.name = ""
        self.sgpa = ""
        self.cgpa = ""
        self.points = ""
        self.rank = '0'
        self.g_rank = '0'
        self.gender = ''

    def cached_data(self,name,gender,sgpa,cgpa,points,rank,g_rank):
        self.name = name
        self.sgpa = sgpa
        self.cgpa = cgpa
        self.points = points
        self.rank = rank
        self.g_rank = g_rank
        self.gender = gender

    def fetch_data(self):
        try:
            url = "http://14.139.56.15/"+self.c_id+self.year+"/studentresult/details.asp"
            page = requests.post(url,data={'RollNumber':self.roll_num},proxies=Student.proxyDict,verify=False)
            soup = BeautifulSoup(page.text,'lxml')
            self.all_data = soup.find_all(class_='ewTable')
            self.name=self.all_data[0].find_all('tr')[0].find_all('td')[1].text.strip()
            res = self.all_data[-1].find_all('tr')[1].find_all('td')
            self.sgpa = res[0].text.strip().split("=")[1]
            cgpa_ = res[2].text.strip()
            self.points = cgpa_.split("/")[0]
            self.cgpa = cgpa_.split("=")[1]
        except:
            self.name = '-'
            self.sgpa = self.points = self.cgpa = '0'

    def get_result(self):
        out = self.roll_num +"\n\t" + self.name + "\n\t" + self.sgpa + "\n\t" +self.points+ "\n\t" + self.cgpa
        return out

