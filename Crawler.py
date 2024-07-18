import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Crawler:
  _inistance = None
  # 实现单例模式
  def __new__(cls, *args, **kwargs):
    if not cls._inistance:
      cls._inistance = super(Crawler, cls).__new__(cls)
    return cls._inistance

  def __init__(self):
    pass

  def get_response(self, url, params=None, headers=None, cookies=None):
    response = requests.get(
      url, 
      params=params, 
      headers=headers, 
      cookies=cookies,
    )
    response.encoding = 'gbk'
    return response
  
  def get_href_by_tags(self, tags):
    links = []
    for tag in tags:
      link = tag.get('href')
      if link:
        links.append(link)
    return links
    
  # 从原html文本中提取出包含指定文本的链接
  def get_href_by_text(self, text, target_text):
    soup = BeautifulSoup(text, 'html.parser')
    tags = soup.findAll('a', string=target_text)
    return self.get_href_by_tags(tags)
  
  def filter_dates(self, links, now_year, now_month, now_day, diff_days):
    filtered_links = []
    for link in links:
      match = re.search(r'(\d{4})-(\d{2})-(\d{2})', string=link)
      if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        if year == now_year and month == now_month and now_day - day <= diff_days:
          filtered_links.append(link)
    return filtered_links
  
  # 从原html文本中提取出包含指定属性和属性值的链接
  def get_links_with_attribute(self, html_text, attribute, target_value):
    soup = BeautifulSoup(html_text, 'html.parser')
    tags = soup.find_all(attrs={attribute: target_value})
    soup = BeautifulSoup(str(tags), 'html.parser')
    tags = soup.find_all('a')
    links = self.get_href_by_tags(tags)
    return links

  def get_title_description(self, response):
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', property='og:title')
    if not meta_tag:
      return None
    og_title = soup.find('meta', property='og:title')['content']
    og_description = soup.find('meta', property='og:description')['content']
    return {
      'title':  og_title,
      'description': og_description
    }