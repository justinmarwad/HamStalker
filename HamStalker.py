import requests, time
from bs4 import BeautifulSoup
from TorHandler import TorHandler

class HamStalker: 
    def __init__(self, name, state, results_file_path="results.txt", tor_flag=False):
        self.name = name
        self.state = state
        self.results_file_path = results_file_path
        self.tor_flag = tor_flag
        
        self.urls = []
        self.total_hammers = 0

        print(f"[INFO] Searching for {self.name} in {self.state}")


    def get_results(self, base="http://www.city-data.com/aradio/"):
        requester = self.get_session()

        for i in range(1, 100): 
            if i == 1: 
                url = f"{base}{self.state}.html"
            else:
                url = f"{base}{self.state}{i}.html"
            
            reqs = requester.get(url)
            if reqs.status_code != 404: 
                soup = BeautifulSoup(reqs.text, "html.parser")
                
                for link in soup.find_all("a"):
                    link = link.get("href")
                    
                    if link.startswith("lic-"): 
                        self.urls.append(f"{base}/{link}")

                print(f"[INFO] Found: {url}")

    def search_results(self, TIMEOUT=0.5):
        found_hammers = []

        for url in urls:     
            print(f"[INFO] On city: {url}")
            soup = BeautifulSoup(self.get_session().get(url).text, "html.parser")
            mydivs = soup.find_all("div", class_="well")
            
            hammers = [] 
            for myd in mydivs:
                data = myd.find("b", text="Registrant:").next_sibling
                hammers.append(data) 

            self.total_hammers += len(hammers)    

            for ham in hammers: 
                if self.name in ham: 
                    found_hammers.append(ham)
                    self.write(ham)

            time.sleep(TIMEOUT)

        return found_hammers

    def write(self, ham): 
        result_text = f"[+] Found Hammer {ham}" 

        print(result_text)
        with open(self.results_file_path, "a") as results_file: 
            results_file.write(result_text)    
            results_file.write("\n")    

    def get_session(self):
        if self.tor_flag: 
            return TorHandler().get_session()
        else: 
            return requests.session()




if __name__ == "__main__": 
    hammies = HamStalker(name="Smith", state="Texas", tor_flag=False)

    hammies.get_results()

    for hammer in hammies.search_results(): 
        print(hammer)

    print(f"[+] Searched {hammies.total_hammers} amount of hammers.") 