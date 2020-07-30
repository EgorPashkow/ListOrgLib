import requests
from lxml import html

class Organization:
    def __init__(self):
        self.link = None
        self.company_name = None
        self.leader = None
        self.INNKPP = None
        self.authorized_capital = None
        self.number_of_staff = None
        self.number_of_founders = None
        self.registration_date = None
        self.status = None
        
        self.index = None
        self.address = None
        self.coordinates = None
        self.legal_address = None
        self.phone = None
        self.fax = None
        self.email = None
        self.website = None
        
        self.INN = None
        self.KPP = None
        self.OKPO = None
        self.OGRN = None
        self.OKFS = None
        self.OKOGU = None
        self.OKOPF = None
        self.OKTMO = None
        self.OKATO = None

        self.report = None
        
class Report:
    def __init__(self):
        self.years = []
        self.data = dict()
    
    def get_by_key(self, key):
        return self.data[key]
    
    def get_by_year(self, year):
        index = self.years.index(str(year))
        res = dict()
        for i in self.data:
            res[i] = self.data[i][index]
        return res
    
    def get_by_year_and_key(self, key, year):
        index = self.years.index(str(year))
        return self.data[key][index]
    
    def get_keys(self):
        return list(self.data.keys())

class SearchResult:
    def __init__(self):
        self.link = None
        self.company_name = None
        self.status = None
        self.type = None
        self.leader = None
        self.INN = None
        self.address = None
        
    def get_profile(self, report=True):
        return Parser().parse(self.Link, report)

class SearchResultWithType:
    def __init__(self):
        self.link = None
        self.company_name = None
        self.status = None
        self.type = None
        self.INN = None
        self.address = None
        
    def get_profile(self, report=True):
        return Parser().parse(self.Link, report)

def get_text(root, arg):
    try:
        if(arg.endswith("/text()")):
            return root.xpath(arg)[0]
        else:
            return root.xpath(arg)[0].text_content()
    except IndexError:
        return None

class Parser:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    def parse(self, url, report=True):
        res = Organization()
        page = requests.get(url, headers=self.headers)
        root = html.fromstring(page.text)
        res.Link = url
        
        res.company_name = get_text(root, "/html/body/div/div[2]/div[3]/p/a")
        
        res.leader = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[1]/td[2]/a")
        res.INNKPP = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[2]/td[2]")
        res.authorized_capital = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[3]/td[2]")
        res.number_of_staff = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[4]/td[2]")
        res.number_of_founders = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[5]/td[2]")
        res.registration_date = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[1]/td[2]/a")
        res.status = get_text(root, "/html/body/div/div[2]/div[3]/table/tr[7]/td[2]")
        
        res.index = get_text(root, "/html/body/div/div[2]/div[6]/p[1]/text()")
        res.address = get_text(root, "/html/body/div/div[2]/div[6]/p[2]/span")
        res.coordinates = get_text(root, "/html/body/div/div[2]/div[6]/p[3]/a")
        res.legal_address = get_text(root, "/html/body/div/div[2]/div[6]/p[4]/span")
        res.phone = get_text(root, "/html/body/div/div[2]/div[6]/p[5]/a[1]")
        res.fax = get_text(root, "/html/body/div/div[2]/div[6]/p[6]/a")
        res.email = get_text(root, "/html/body/div/div[2]/div[6]/p[7]/a")
        res.website = get_text(root, "/html/body/div/div[2]/div[6]/div/p/a")

        res.INN = get_text(root, "/html/body/div/div[2]/div[8]/p[1]/text()")
        res.KPP = get_text(root, "/html/body/div/div[2]/div[8]/p[2]/text()")
        res.OKPO = get_text(root, "/html/body/div/div[2]/div[8]/p[3]/span")
        res.OGRN = get_text(root, "/html/body/div/div[2]/div[8]/p[4]/text()")
        res.OKFS = get_text(root, "/html/body/div/div[2]/div[8]/p[5]/text()")
        res.OKOGU = get_text(root, "/html/body/div/div[2]/div[8]/p[6]/text()")
        res.OKOPF = get_text(root, "/html/body/div/div[2]/div[8]/p[7]/text()")
        res.OKTMO = get_text(root, "/html/body/div/div[2]/div[8]/p[8]/text()")
        res.OKATO = get_text(root, "/html/body/div/div[2]/div[8]/p[9]/a") + get_text(root, "/html/body/div/div[2]/div[8]/p[9]/text()")
        
        if report:
            res.report = self.parse_report(url)
        return res
    
    def parse_report(self, url):
        res = Report()
        page = requests.get(url + "/report", headers=self.headers)
        root = html.fromstring(page.text)
        temp = []
        for i in range(4, len(root.xpath("/html/body/div/div[2]/table/tr[2]")[0].getchildren()) + 1):
            temp.append(get_text(root, "/html/body/div/div[2]/table/tr[2]/td[" + str(i) + "]"))
        res.years = temp
        for i in range(3, len(root.xpath("/html/body/div/div[2]/table/tr")) + 1):
            try:
                key = root.xpath("/html/body/div/div[2]/table/tr[" + str(i) + "]/td[2]/a")[0]
            except IndexError:
                continue
            temp = []
            for j in range(4, len(root.xpath("/html/body/div/div[2]/table/tr[" + str(i) + "]")[0].getchildren()) + 1):
                temp.append(get_text(root, "/html/body/div/div[2]/table/tr[" + str(i) + "]/td[" + str(j) + "]"))
            res.data[key.text_content()] = temp
        return res
    
    def search(self, query, search_type="all", limit=100):
        def handle_page(query, page):
            page = requests.get("https://www.list-org.com/search?type=all&val=%s&page=%s" % (str(query), str(page)), headers=self.headers)
            root = html.fromstring(page.text)
            for i in range(1, 100 + 10):
                if(len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResult()
                    temp.link = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.company_name = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].text_content()
                    if(span_length == 2):
                        temp.status = "НЕ ДЕЙСТВУЮЩЕЕ"
                    else:
                        temp.status = "ДЕЙСТВУЮЩЕЕ"
                    temp.type = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[1]")[0]
                    temp.leader = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[2]")[0][2:]
                    temp.INN = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[3]")[0][2:]
                    temp.address = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[4]")[0][2:]
                    res.append(temp)
                except IndexError:
                    continue
        
        def handle_page_with_type(search_type, query, page):
            page = requests.get("https://www.list-org.com/search?type=%s&val=%s&page=%s" % (str(search_type), str(query), str(page)), headers=self.headers)
            root = html.fromstring(page.text)
            for i in range(1, 100 + 10):
                if(len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.link = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.company_name = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].text_content()
                    if(span_length == 2):
                        temp.status = "НЕ ДЕЙСТВУЮЩЕЕ"
                    else:
                        temp.status = "ДЕЙСТВУЮЩЕЕ"
                    temp.type = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[1]")[0]
                    temp.INN = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[2]")[0][2:]
                    temp.address = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[3]")[0][2:]
                    res.append(temp)
                except IndexError:
                    continue
        res = []
        page = 1
        while(len(res) < limit):
            try:
                if(search_type == "all"):
                    handle_page(query, page)
                else:
                    handle_page_with_type(search_type, query, page)
            except IndexError:
                break
            page += 1
        return res[:limit]
    
    
    def get_OKATO(self, num_OKATO, limit=100):
        def handle_page(page):
            page = requests.get("https://www.list-org.com/list?okato=%s&page=%s" % (str(num_OKATO), str(page)), headers=self.headers)
            root = html.fromstring(page.text)
            for i in range(1, 34):
                if(len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.link = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.company_name = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].text_content()
                    if(span_length == 2):
                        temp.status = "НЕ ДЕЙСТВУЮЩЕЕ"
                    else:
                        temp.status = "ДЕЙСТВУЮЩЕЕ"
                    temp.type = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[1]")[0]
                    temp.INN = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[2]")[0][2:]
                    temp.address = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[3]")[0][2:]
                    res.append(temp)
                except IndexError:
                    continue
        res = []
        page = 1
        while(len(res) < limit):
            try:
                handle_page(page)
            except IndexError:
                break
            page += 1
        return res[:limit]
    
    def get_OKVED(self, num_OKVED, limit=100):
        def handle_page(page):
            page = requests.get("https://www.list-org.com/list?okved2=%s&page=%s" % (str(num_OKVED), str(page)), headers=self.headers)
            root = html.fromstring(page.text)
            for i in range(1, 34):
                if(len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.link = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.company_name = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].text_content()
                    if(span_length == 2):
                        temp.status = "НЕ ДЕЙСТВУЮЩЕЕ"
                    else:
                        temp.status = "ДЕЙСТВУЮЩЕЕ"
                    temp.type = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[1]")[0]
                    temp.INN = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[2]")[0][2:]
                    temp.address = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[3]")[0][2:]
                    res.append(temp)
                except IndexError:
                    continue
        res = []
        page = 1
        while(len(res) < limit):
            try:
                handle_page(page)
            except IndexError:
                break
            page += 1
        return res[:limit]
    
    def get_OKVED_and_OKATO(self, num_OKVED, num_OKATO, limit=100):
        def handle_page(page):
            page = requests.get("https://www.list-org.com/search?type=similar&okved=%s&okato=%s&page=%s" % (str(num_OKVED), str(num_OKATO), str(page)), headers=self.headers)
            root = html.fromstring(page.text)
            for i in range(1, 100 + 10):
                if(len(root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.link = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.company_name = root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/a")[0].text_content()
                    if(span_length == 2):
                        temp.status = "НЕ ДЕЙСТВУЮЩЕЕ"
                    else:
                        temp.status = "ДЕЙСТВУЮЩЕЕ"
                    temp.type = root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[1]")[0]
                    temp.INN = root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[2]")[0][2:]
                    temp.address = root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/span[" + str(span_length) + "]/text()[3]")[0][2:]
                    res.append(temp)
                except IndexError:
                    continue
        res = []
        page = 1
        while(len(res) < limit):
            try:
                handle_page(page)
            except IndexError:
                break
            page += 1
        return res[:limit]