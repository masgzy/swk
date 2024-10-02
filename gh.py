import requests
import sys
import platform
from bs4 import BeautifulSoup
import os
from rich.console import Console

# 创建 rich 控制台对象
console = Console()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clear_screen():
    if sys.platform.startswith('linux'):
        print("\033c", end="")
    elif sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('darwin'):
        print("\033c", end="")
    else:
        print("\033c", end="")

    
def extract_download_links(article_div):
    """从文章 div 中提取下载链接和标题"""
    links = []
    titles = []
    for a_tag in article_div.find_all('a'):
        href = a_tag.get('href')
        title = a_tag.get('title')
        if not href:
            continue

        # 确保 href 链接是完整的
        if not href.startswith('http'):
            href = requests.compat.urljoin(base_url, href)

        try:
            console.log(f"请求: {href}")  # 调试输出
            link_response = requests.get(href, headers=HEADERS)
            link_response.raise_for_status()
            link_soup = BeautifulSoup(link_response.content, 'html.parser')
            down_2_div = link_soup.find('div', class_='down_2')
            if down_2_div:
                download_a_tag = down_2_div.find('a')
                download_href = download_a_tag.get('href') if download_a_tag else '没有下载链接'
            else:
                download_href = '没有下载链接'
        except Exception as e:
            download_href = f'获取下载链接时出错: {e}'

        if download_href and download_href != '没有下载链接':
            links.append(download_href)
            titles.append(title.strip() if title else 'untitled')  # 去除标题中的空格

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

def scrape_site(base_urls):
    """抓取网站中的下载链接"""
    total_links = 0
    for base_url in base_urls:
        try:
            console.log(f"请求页面: {base_url}")  # 调试输出
            response = requests.get(base_url, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            console.log(f"请求错误: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='gallery')
        if not articles:
            console.log("没有找到任何文章。")
            break

        for article in articles:
            if article.find('a'):
                download_links, titles = extract_download_links(article)
                total_links += len(download_links)
                for link, title in zip(download_links, titles):
                    download_file(link, title)

        next_page_tag = soup.find('div', class_='pagelist').find('a', class_='next fas', title='下一页')
        base_url = next_page_tag.get('href') if next_page_tag else None
        if not base_url:
            console.log("没有找到下一页链接，结束爬取。")
            break

    console.log(f"总共提取到 {total_links} 个下载链接")

if __name__ == "__main__":
    clear_screen()
    base_urls = ['http://siwake.cc/']
    scrape_site(base_urls)