import requests
from lxml import html

class Organization:
    def __init__(self):
        self.url = None
        self.organization_name = None
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
    
    def __str__(self):
        return str(vars(self))

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
    
    def get_by_key_and_year(self, key, year):
        index = self.years.index(str(year))
        return self.data[key][index]
    
    def get_keys(self):
        return list(self.data.keys())
    
    def __str__(self):
        return str(vars(self))

class Man:
    def __init__(self):
        self.url = None
        self.name = None
        self.INN = None
        self.leader = []
        self.founder = []
        
        self.ORGN = None
        self.status = None
        self.registration_date = None
        self.legal_address = None
        self.OKVED = None
        self.adding_OKVED = []
        
    def __str__(self):
        return str(vars(self))

class SearchResult:
    def __init__(self):
        self.url = None
        self.organization_name = None
        self.status = None
        self.type = None
        self.leader = None
        self.INN = None
        self.address = None
    
    def __str__(self):
        return str(vars(self))
        
    def get_profile(self, report=True):
        return Parser().parse(self.url, report)

class SearchResultWithType:
    def __init__(self):
        self.url = None
        self.organization_name = None
        self.status = None
        self.type = None
        self.INN = None
        self.address = None
        
    def __str__(self):
        return str(vars(self))
        
    def get_profile(self, report=True):
        return Parser().parse(self.url, report)

def get_text(root, arg):
    try:
        if(arg.endswith("/text()")):
            return root.xpath(arg)[0]
        else:
            return root.xpath(arg)[0].text_content()
    except IndexError:
        return None

def get_from_dict(input_dict, key):
    try:
        return input_dict[key]
    except KeyError:
        return None

def get_element_by_text(root, element_text):
    return root.xpath("//*[. = '" + element_text + "']")

def clean_string(string):
    return " ".join(string.strip().replace("  ", " ").split())

def parse_p(root, element_text):
    res = dict()
    elements = get_element_by_text(root, element_text)
    if elements is not None:
        element = elements[0]
        next_element = element.getnext()
        for i in next_element.xpath(".//p"):
            res[clean_string(i.xpath(".//i")[0].text_content())] = clean_string(" ".join(i.xpath(".//text()[not(self::i)]")[1:]))
    return res

def parse_table(root, element_text):
    res = dict()
    elements = get_element_by_text(root, element_text)
    if elements is not None:
        element = elements[0]
        next_element = element.getnext()
        for i in next_element.xpath(".//table/tr"):
            res[clean_string(i.xpath(".//td")[0].text_content())] = clean_string(i.xpath(".//td")[1].text_content())
    return res

class Parser:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    def parse(self, url, report=True):
        res = Organization()
        page = requests.get(url, headers=self.headers)
        root = html.fromstring(page.text)
        res.url = url
        
        res.organization_name = get_element_by_text(root, "Полное юридическое наименование:")[0].getnext().text
        
        try:
            general_information = parse_table(root, "Общие сведения:Дерево связейНа картеОтчетность")#################
        except IndexError:
            general_information = parse_table(root, "Общие сведения:Дерево связейНа карте")
        
        res.leader = get_from_dict(general_information, 'Руководитель:')
        res.INNKPP = get_from_dict(general_information, 'ИНН / КПП:')
        res.authorized_capital = get_from_dict(general_information, 'Уставной капитал:')
        res.number_of_staff = get_from_dict(general_information, 'Численность персонала:')
        res.number_of_founders = get_from_dict(general_information, 'Количество учредителей:')
        res.registration_date = get_from_dict(general_information, 'Дата регистрации:')
        res.status = get_from_dict(general_information, 'Статус:')
        
        contacts = parse_p(root, "Контактная информация:")
        res.index = get_from_dict(contacts, 'Индекс:')
        res.address = get_from_dict(contacts, 'Адрес:')
        res.coordinates = get_from_dict(contacts, 'GPS координаты:')
        res.legal_address = get_from_dict(contacts, 'Юридический адрес:')
        res.phone = get_from_dict(contacts, 'Телефон:')
        res.fax = get_from_dict(contacts, 'Факс:')
        res.email = get_from_dict(contacts, 'E-mail:')
        res.website = get_from_dict(contacts, 'Сайт:')
        
        requisites = parse_p(root, "Реквизиты компании:")
        res.INN = get_from_dict(requisites, 'ИНН:')
        res.KPP = get_from_dict(requisites, 'КПП:')
        res.OKPO = get_from_dict(requisites, 'ОКПО:')
        res.OGRN = get_from_dict(requisites, 'ОГРН:')
        res.OKFS = get_from_dict(requisites, 'ОКФС:')
        res.OKOGU = get_from_dict(requisites, 'ОКОГУ:')
        res.OKOPF = get_from_dict(requisites, 'ОКОПФ:')
        res.OKTMO = get_from_dict(requisites, 'ОКТМО:')
        res.OKATO = get_from_dict(requisites, 'ОКАТО:')
        
        if report:
            res.report = self.parse_report(url)
        return res
    
    def parse_report(self, url):
        res = Report()
        page = requests.get(url + "/report", headers=self.headers)
        if page.status_code != 200:
            return None
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
            for i in range(1, 101):
                if(len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResult()
                    temp.url = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.organization_name = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].text_content()
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
            for i in range(1, 101):
                if(len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.url = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.organization_name = root.xpath("/html/body/div/div[2]/div[1]/p[" + str(i) + "]/label/a")[0].text_content()
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
            if(page.url == "https://www.list-org.com/bot"):
                print("Смени ip")
            for i in range(1, 33):
                if(len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.url = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.organization_name = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].text_content()
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
            for i in range(1, 33):
                if(len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.url = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.organization_name = root.xpath("/html/body/div/div[2]/div[2]/p[" + str(i) + "]/label/a")[0].text_content()
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
            for i in range(1, 101):
                if(len(root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]")) == 0):
                    raise IndexError()
                span_length = len(root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/span"))
                try:
                    temp = SearchResultWithType()
                    temp.url = "https://www.list-org.com" + root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/a")[0].get("href")
                    temp.organization_name = root.xpath("/html/body/div/div[2]/div/p[" + str(i) + "]/label/a")[0].text_content()
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