import requests
import sys
import platform
from bs4 import BeautifulSoup
import os
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn




# 创建 rich 控制台对象
console = Console()

# 确保保存下载链接的目录存在
if not os.path.exists('res'):
    os.makedirs('res')

# 删除已存在的 DL.sh 文件（如果存在）
if sys.platform.startswith('linux'):
    dl_sh_path = 'res/DL.sh'
elif sys.platform.startswith('win'):
    dl_sh_path = 'res/DL.bat'
elif sys.platform.startswith('darwin'):
    dl_sh_path = 'res/DL.sh'
else:
    dl_sh_path = 'res/DL.sh'


if os.path.exists(dl_sh_path):
    os.remove(dl_sh_path)
    console.log(f"已删除旧的 {dl_sh_path} 文件。")

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

def save_to_file(link, title):
    """将下载链接和标题保存到文件"""
    # 去除标题中的非法文件名字符并替换空格为下划线
    title = ''.join(c for c in title if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    title = ''.join(c for c in title if c.isalnum() or c in ('strong', '')).strip().replace('strong', '')
    
    with open(dl_sh_path, 'a', encoding='UTF-8') as file:
        file.write(f"wget -O \"{title}.zip\" \"{link}\"\n")

def scrape_site(base_urls):
    """抓取网站中的下载链接"""
    total_links = 0
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("总链接数: [bold]{task.completed}[/]")
    ) as progress:
        task = progress.add_task("[cyan]抓取中...", total=100)  # 初始任务进度

        for base_url in base_urls:
            while base_url:
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
                            save_to_file(link, title)

                next_page_tag = soup.find('div', class_='pagelist').find('a', class_='next fas', title='下一页')
                base_url = next_page_tag.get('href') if next_page_tag else None
                if not base_url:
                    console.log("没有找到下一页链接，结束爬取。")
                    break

                progress.update(task, advance=10)  # 更新任务进度
                progress.update(task, description=f"[cyan]抓取中... 总链接数: {total_links}")

    console.log(f"总共提取到 {total_links} 个下载链接")

if __name__ == "__main__":
    clear_screen()
    a = input("1.白丝 2.黑丝 3.肉丝 4.网袜 5.自选机构 6.搜索 7.所有 0.退出\n选择一个选项: ")
    base_urls = []

    if a == "1":
        base_urls = ['http://siwake.cc/tags-baisi-v9l.html']
    elif a == "2":
        base_urls = ['http://siwake.cc/tags-heisi-z2n.html']
    elif a == "3":
        base_urls = ['http://siwake.cc/tags-rousi-9sw.html']
    elif a == "4":
        base_urls = ['http://siwake.cc/tags-wangwa-18v.html']
    elif a == "5":
        clear_screen()
        b = input("1.绅士约拍 2.爱丝 3.丝慕 4.丽丝映像 5.奈丝 6.森萝财团 7.猫萌榜  8.风之领域 9.袜涩 10.一千零一夜 11.轻兰映画 12.纳丝摄影 13.丝享家 14.SIW斯文传媒 15.尤蜜荟 16.壹吻映画 17.异思趣向 18.蜜丝 19.喵糖映画 20.紧急企划 21.网络美女 22.SSA丝社(需要输文字)")
        if b:
            base_urls = ['http://siwake.cc/category-' + b + '.html']
    elif a == "6":
        e = input("输入搜索内容:")
        if e:
            base_urls = ['http://siwake.cc/search.php?q=' + e]
    elif a == "7":
        base_urls = ['http://siwake.cc/']
    elif a == "0":
        console.log("退出程序。")
        exit()
    else:
        console.log("无效的选项。")

    if base_urls:
        scrape_site(base_urls)
    else:
        console.log("没有提供有效的 URL。")
