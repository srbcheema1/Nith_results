import requests
from os import environ
from bs4 import BeautifulSoup

from .constants import cache_path, base_year

from srblib import Colour, SrbJson, debug, Tabular

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
        self.roll_num = str(roll)

        self.batch = Student.get_batch(roll)
        self.year = Student.get_year(roll)
        self.branch = Student.get_branch(roll)
        self.college = Student.get_college(roll) # bit less used

        self.name = ''
        self.sgpa = ''
        self.cgpa = ''
        self.points = ''

        self.rank = '0' # depends on grouping
        self.g_rank = '0' # genderwise rank
        self.gender = '' # gender


    def set_cached_data(self,name,gender,sgpa,cgpa,points,rank='0',g_rank='0'):
        self.name = name
        self.sgpa = sgpa
        self.cgpa = cgpa
        self.points = points
        self.rank = rank
        self.g_rank = g_rank
        self.gender = gender

    def fetch_data(self):
        cache = SrbJson(cache_path,template={"nith_results":{}}) # load cache
        if(self.roll_num in cache):
            item = cache[self.roll_num]
            self.set_cached_data(item['Name'],item['Gender'],item['Sgpa'],item['Cgpa'],item['Points'])
            if(self.name!='-' and self.cgpa!='0'):
                Colour.print('got chached '+self.roll_num,Colour.BLUE)
                return self.get_cache()
            else:
                Colour.print('Bad chached '+self.roll_num,Colour.YELLOW)

        url = "http://59.144.74.15/"+Student.get_c_id(self.roll_num)+self.batch+"/studentresult/details.asp"
        try:
            page = requests.post(url,data={'RollNumber':self.roll_num},proxies=Student.proxyDict,verify=False)
            soup = BeautifulSoup(page.text,'html.parser')
            try:
                self.all_data = soup.find_all(class_='ewTable')
                self.name=self.all_data[0].find_all('tr')[0].find_all('td')[1].text.strip()
                self.name=self.name.upper()
                res = self.all_data[-1].find_all('tr')[1].find_all('td')
                self.sgpa = res[0].text.strip().split("=")[1]
                cgpa_ = res[2].text.strip()
                self.points = cgpa_.split("/")[0]
                self.cgpa = cgpa_.split("=")[1]
                cache[self.roll_num] = self.get_cache() # store cache
                Colour.print('fetched successfully '+self.roll_num,Colour.BLUE)
                return self.get_cache()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                self.name = '-'
                self.sgpa = self.points = self.cgpa = '0'
                Colour.print('Unable to parse, ' + self.roll_num, Colour.RED)
                if(debug):
                    Colour.print('possibly roll number doesnot exist or site design changed\n' +
                    'contact srbcheema2@gmail.com in case the roll number is availabe on site',Colour.RED)
                return None
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            self.name = '-'
            self.sgpa = self.points = self.cgpa = '0'
            Colour.print('Unable to fetch ' + self.roll_num + ', Please check your internet connection', Colour.RED)
            return None


    def get_result(self):
        out = self.roll_num +"\n\t" + self.name + "\n\t" + self.sgpa + "\n\t" +self.points+ "\n\t" + self.cgpa
        return out

    def __str__(self):
        table = [
            ['Roll num',self.roll_num],
            ['Name',self.name],
            ['Points',self.points],
            ['Cgpa',self.cgpa],
            ['Sgpa',self.sgpa],
            ['Branch',self.branch],
            ['Rank',self.rank],
            ['Gender',self.gender],
            ['Gender rank',self.rank],
        ]
        table = Tabular(table)
        return table.__str__()

    def get_cache(self):
        dictt = {}
        dictt['Rollno'] = self.roll_num
        dictt['Name'] = self.name
        dictt['Gender'] = self.gender
        dictt['Sgpa'] = self.sgpa
        dictt['Cgpa'] = self.cgpa
        dictt['Points'] = self.points
        return dictt

    @staticmethod
    def _is_legacy_roll(roll):
        if(len(roll) == 5): # simply 15535
            return True
        if(len(roll) == 7 and roll[2] == 'm'): # simply legacy dual
            return True
        if(roll[0] == 'i'): # iiitu is still legacy
            return True
        return False

    @staticmethod
    def get_batch(roll): # working with new one
        roll = str(roll)
        if(roll[0]=='i'):#iitu
            year = roll[5:7]
        else:
            year = roll[0:2]
        return year


    @staticmethod
    def get_college(roll): # working with new one
        roll = str(roll)
        if(roll[0]=='i'):#iitu
            college = "iiitu"
        else:
            college = "nith"
        return college

    @staticmethod
    def get_c_id(roll): # working with new one
        roll = str(roll)
        if(roll[0]=='i'):#iitu
            c_id="iiituna"
        else:
            c_id="scheme"
        return c_id

    @staticmethod
    def get_num(roll): # not used anywhere
        roll = str(roll)
        if(Student._is_legacy_roll(roll)):
            if(roll[2]=='m' or roll[2]=='M'):
                num=roll[5:7]
            elif(roll[0]=='i'):
                num=roll[8:10]
            else:
                num=roll[3:5]
            return num
        else: # six digit roll ex. 185535
            last_digits = int(roll[3:6])
            if(last_digits >= 500): last_digits -= 500
            return str(last_digits)


    @staticmethod
    def _get_branch(roll):
        roll = str(roll)
        if(Student._is_legacy_roll(roll)):
            if(roll[2]=='m' or roll[2]=='M'):
                branch=roll[2:4].lower()
                branch+=str(roll[4])
            elif(roll[0]=='i'):
                branch='una'+roll[7]
            else:
                branch=roll[2]
            return branch
        else:
            branch_digit = int(roll[2])
            dual_digit = int(roll[3])
            if(dual_digit >= 5):
                return roll[2] + '5'
            else:
                return roll[2]

    @staticmethod
    def get_branch(roll):
        branch = Student._get_branch(roll)
        branch_data = {
                "1":"Civil",
                "2":"Electrical",
                "3":"Mechanical",
                "4":"Ece",
                "5":"Cse",
                "6":"Architecture",
                "7":"Chemical",
                "8":"Material",

                "mi5":"Cse_dual",
                "55":"Cse_dual",
                "mi4":"Ece_dual",
                "45":"Ece_dual",

                "una1":"Cse_una",
                "una2":"Ece_una",
                "una3":"IT_una",

                "0":"unknown"
        }
        if(branch in branch_data):
            return branch_data[branch]
        else:
            return branch_data['0']


    @staticmethod
    def get_year(roll):
        batch = Student.get_batch(roll)
        year = base_year - int(batch) + 1
        return str(year)
