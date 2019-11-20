import re
import requests
import json
import csv

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern = re.compile('<li>.*?list_num.*?>(.*?)</div>.*?pic.*?src="(.*?)".*?/></a>.*?name"><a.*?title="(.*?)">.*?tuijian">(.*?)</span>.*?publisher_info.*?title="(.*?)".*?biaosheng.*?<span>(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'iamge':item[1],
            'title':item[2],
            'tuijian':item[3],
            'author':item[4],
            'times':item[5],
        }
       # print(item)

def write_content_to_file(content):
    with open('book.csv','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
        
        
      #  w=csv.writer(f)
      #  w.writerows(content)
        
        #f.write(json.dumps(content,ensure_ascii=False) + '\n')
       # f.close()
        
def main(page):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        #print(item)
        write_content_to_file(item)

if __name__ == "__main__":
    for i in range(1,26):
        main(i)
        print(i)