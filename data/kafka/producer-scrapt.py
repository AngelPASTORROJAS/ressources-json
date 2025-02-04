import requests
from bs4 import BeautifulSoup
import pandas as pd
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
job_elements = soup.find_all("div", class_="card-content")
liste = []
for i in range(0,len(job_elements)):  
        title = job_elements[i].find("h2").contents[0].strip()
        company = job_elements[i].find("h3").contents[0].strip()
        location = job_elements[i].find("p", {"class":"location"}).contents[0].strip()
        liste.append((title, company, location))
       
df = pd.DataFrame(liste, columns=["title", "company", "location"])
df
