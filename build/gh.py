import requests
import sys
import platform
import os
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console

# 创建 rich 控制台对象
console = Console()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clear_screen():
    if sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('darwin'):
        os.system('clear')
    else:
        os.system('clear')

def delay_request():
    time.sleep(random.uniform(1, 3))  # 随机延迟1-3秒

def extract_download_links(article_div, base_url):
    """从文章 div 中提取下载链接和标题"""
    links = []
    titles = []
    for a_tag in article_div.find_all('a'):
        href = a_tag.get('href')
        title = a_tag.get('title')
        if not href:
            continue

        try:
            console.log(f"请求: {href}")  # 调试输出
            full_href = requests.compat.urljoin(base_url, href)
            response = requests.get(full_href, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            down_2_div = soup.find('div', class_='down_2')
            download_href = down_2_div.find('a').get('href') if down_2_div else '没有下载链接'
        except Exception as e:
            download_href = f'获取下载链接时出错: {e}'

        if download_href and download_href != '没有下载链接':
            links.append(download_href)
            titles.append(title.strip() if title else 'untitled')

    console.log(f"提取到 {len(links)} 个下载链接")  # 调试输出
    return links, titles

def download_file(link, title):
    """下载文件"""
    try:
        response = requests.get(link, headers=HEADERS, stream=True)
        response.raise_for_status()
        filename = f"{title}.zip"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        console.log(f"下载完成: {filename}")
    except Exception as e:
        console.log(f"下载失败: {title}, 错误: {e}")

def download_worker(link, title, executor):
    """下载工作线程"""
    download_file(link, title)

def scrape_site(base_urls):
    """抓取网站中的下载链接"""
    total_links = 0
    current_url = base_urls[0]
    with ThreadPoolExecutor(max_workers=5) as executor:  # 限制最大线程数为5
        while current_url:
            try:
                console.log(f"请求页面: {current_url}")  # 调试输出
                response = requests.get(current_url, headers=HEADERS)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('div', class_='gallery')
                if not articles:
                    console.log("没有找到任何文章。")
                    break

                for article in articles:
                    if article.find('a'):
                        download_links, titles = extract_download_links(article, current_url)
                        total_links += len(download_links)
                        for link, title in zip(download_links, titles):
                            executor.submit(download_worker, link, title, executor)
                delay_request()  # 增加请求间隔

                next_page_tag = soup.find('div', class_='pagelist').find('a', class_='next fas', title='下一页')
                current_url = next_page_tag.get('href') if next_page_tag else None
                if not current_url:
                    console.log("没有找到下一页链接，结束爬取。")
                    break

            except requests.RequestException as e:
                console.log(f"请求错误: {e}")
                break

    console.log(f"总共提取到 {total_links} 个下载链接")

if __name__ == "__main__":
    clear_screen()
    base_urls = ['http://siwake.cc/tags-baisi-v9l.html']
    scrape_site(base_urls)
