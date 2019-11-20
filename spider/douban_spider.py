import requests
import xlwt
from bs4 import BeautifulSoup

def getHTMLText(url, start):
    try:
        kv = {'start': start, 'type': 'S'}
        r= requests.request('GET',url, params = kv, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == '__main__':
    douban_title = []
    douban_info = []
    douban_rating_nums = []
    for i in range(50):
        start = str(i *20)
        # "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=0&type=T"
        url = "https://book.douban.com/tag/科幻"
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        douban = getHTMLText(url, start)
        soup = BeautifulSoup(douban,"html.parser")
        # info = soup.select('.info')  #通过类名查找
        # print(info[0])
        titles = soup.select('.subject-item .info h2 a')
        infos = soup.select('.pub')
        rate_nums = soup.select('.rating_nums')
        for title in titles:
            result_title = title.text.replace('\n','')
            result_title = result_title.replace(' ','')
            douban_title.append(result_title)

        for info in infos:
            result_info = info.text.replace('\n','')
            result_info = result_info.replace(' ', '')
            douban_info.append(result_info)
            print(result_info)

        for rate_num in rate_nums:
            result_rate  = rate_num.text.replace('\n','')
            result_rate = result_rate.replace(' ', '')
            douban_rating_nums.append(result_rate)

    file = xlwt.Workbook(encoding='utf-8')
    table = file.add_sheet('data', cell_overwrite_ok=True)
    table_head = ['title', 'info','rate']
    table.write(0, 0, '书名')
    table.write(0, 1, '详细信息')
    table.write(0, 2, '评分')
    for i in range(len(douban_title)):
        table.write(i+1, 0,'《'+douban_title[i]+'》')
        table.write(i+1, 1, douban_info[i])
        table.write(i + 1, 2, douban_rating_nums[i])
    file.save('book.xls')


    # title = h2.get_text();
    # print(title)