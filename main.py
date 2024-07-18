from datetime import datetime, date, timedelta
from Crawler import Crawler
from Gemma import Gemma
from MySQL import MySQL

# 新浪财经网
xlcj = 'https://finance.sina.com.cn' 
# 贵州茅台
gzmt = '贵州茅台'
gzmt_code = "sh600519"
xlcj_gzmt = xlcj + f'/realstock/company/{gzmt_code}/nc.shtml'

# 获取新浪财经网贵州茅台响应
def get_xlcj_gzmt_response():
  crawler = Crawler()
  return crawler.get_response(xlcj_gzmt)
# 获取“公司资讯”响应
def get_news_response(response):
  crawler = Crawler()
  company_news_url = crawler.get_href_by_text(response.text, '公司资讯')[0]
  return crawler.get_response(company_news_url)
# 获取最近3天的新闻标题和描述
def get_datas():
  crawler = Crawler()
  date = datetime.now().date()
  xlcj_gzmt_response = get_xlcj_gzmt_response()
  news_response = get_news_response(xlcj_gzmt_response)
  news_urls = crawler.get_links_with_attribute(news_response.text, 'class', 'datelist')
  news_urls = crawler.filter_dates(news_urls, date.year, date.month, date.day, 3)
  crawler = Crawler()
  title_descriptions = []
  for url in news_urls:
    title_description = crawler.get_title_description(crawler.get_response(url))
    if title_description:
      title_descriptions.append(title_description)
  return title_descriptions
# 将爬取到的数据存储到数据库中
def save_datas_database(title_descriptions):
  sql = MySQL()
  date = datetime.now().date()
  for title_description in title_descriptions:
    sql.insert(date, title_description['title'], title_description['description'])
# 读取数据库中的数据
def read_datas_database(dates):
  sql = MySQL()
  return sql.get_news_by_dates(dates)
# 调用gemma，对新闻进行判断
def gemma_judge(records):
  sql = MySQL()
  gemma = Gemma()
  results = []
  for record in records:
    record = sql.get_news_by_id(record)
    title = record[2]
    description = record[3]
    ask = f'''
    标题为{title}, 描述为{description}的新闻对{gzmt}的股票价格可能产生的影响是什么，
    请回答（正面，负面或中性）中的一个
    '''
    results.append(gemma.chat(ask))
  return results
# 将分析结果存储到数据库中
def save_gemma_judge(records, results):
  sql = MySQL()
  for record, result in zip(records, results):
    sql.update_news_notes(record, result)
# 生成一个简单的报告
def generate_report():
  gemma = Gemma()
  ask = f'''
    根据前面的对话,请你分析一下{gzmt}的股票价格可能的走势
    '''
  ans = gemma.chat(ask)
  report_file = f"reports/{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
  with open(report_file, 'w') as file:
    file.write(ans)

def main():
  title_descriptions = get_datas()
  save_datas_database(title_descriptions)
  today = date.today()
  yesterday = today - timedelta(days=1)
  two_days_ago = yesterday - timedelta(days=1)
  dates = [
    today.strftime("%Y-%m-%d"),
    yesterday.strftime("%Y-%m-%d"),
    two_days_ago.strftime("%Y-%m-%d")
  ]
  records = read_datas_database(dates)
  results = gemma_judge(records)
  save_gemma_judge(records, results)
  generate_report()
  
if __name__ == '__main__':
  main()