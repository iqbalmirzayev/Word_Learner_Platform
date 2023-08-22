import selenium
from bs4 import BeautifulSoup
import requests

from db_helper import DbHelper
class DataLoader:
    def __init__(self):
        dbhelper = DbHelper("database")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        for page in range(1, 46):
            url=f'https://app.memrise.com/course/1656459/ielts-ramazanee-by-galmeeh/{page}/'
            resp=requests.request(method="GET",url=url, headers=headers)
            soup=BeautifulSoup(resp.text,'lxml')
            data=soup.find_all("div",attrs={"class":"thing text-text"})
            for i in data:
                soz=i.find("div", attrs={"class":"col_a col text"}).text
                mena=i.find("div", attrs={"class":"col_b col text"}).text
                print(f"{soz} --> {mena}")
                dbhelper.add_word(soz, mena)
        
if __name__=="__main__":
    dataLoader=DataLoader()
    
        
        