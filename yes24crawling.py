from bs4 import BeautifulSoup as bs
import json


def parser():
    dic = {}
    with open("logincroller.html") as fp:
        soup = bs(fp, "html.parser")

    for links in soup.find_all("ul", {"data-filterable-for": "dashboard-repos-filter-left"}):
        for link in links.find_all('a'):
            list = link.get('href')
            listArr = list.split('/')
            listArr.remove('')
            print(listArr)
            if(dic.get(listArr[0])):
                dic[listArr[0]].append(listArr[1])
            else:
                dic[listArr[0]] = [listArr[1]]

    print(dic)

    with open('parser.json', 'w', encoding='utf-8') as file:
        json.dump(dic, file, ensure_ascii=False, indent='\t')


parser()
