import requests
import sys
import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_directory_exists('res')

def get_script_path():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        return 'res/DL.sh'
    elif sys.platform.startswith('win'):
        return 'res/DL.bat'
    return 'res/DL.sh'

dl_sh_path = get_script_path()

def remove_existing_script():
    if os.path.exists(dl_sh_path):
        console.log(f"检测到已有的脚本文件: {dl_sh_path}")
        return True
    return False

def command_exists(new_command):
    """检查新命令是否已存在于现有脚本中"""
    if os.path.exists(dl_sh_path):
        # 尝试不同的编码来读取文件
        for encoding in ['UTF-8']:
            try:
                with open(dl_sh_path, 'r', encoding=encoding) as file:
                    existing_commands = file.readlines()
                for command in existing_commands:
                    if new_command in command:
                        return True
                break
            except UnicodeDecodeError:
                console.log(f"无法使用编码 {encoding} 读取文件，尝试其他编码...")
    return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_download_links(article_div, base_url):
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
            link_response = requests.get(href, headers=HEADERS, timeout=10)
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

def get_file_encoding():
    """根据操作系统返回适当的文件编码"""
    if os.name == 'nt':  # Windows 系统
        return 'UTF-8'
    return 'utf-8'  # 其他系统（Linux, macOS）

def save_to_file(link, title):
    """将下载链接和标题保存到文件"""
    # 去除标题中的非法文件名字符并替换空格为下划线
    title = ''.join(c for c in title if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    title = ''.join(c for c in title if c.isalnum() or c in ('strong', '')).strip().replace('strong', '')

    # 确保标题中没有无法编码的字符
    try:
        title.encode('UTF-8')
    except UnicodeEncodeError:
        title = title.encode('UTF-8', 'replace').decode()  # 将无法编码的字符替换为问号

    encoding = 'UTF-8' if sys.platform.startswith('win') else 'utf-8'
    
    new_command = f"wget -O \"{title}.zip\" \"{link}\"\n"
    if not command_exists(new_command):
        with open(dl_sh_path, 'a', encoding=encoding) as file:
            file.write(new_command)
    else:
        console.log(f"命令已存在: {new_command.strip()}")

def scrape_site(base_urls):
    """抓取网站中的下载链接"""
    total_links = 0
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("总链接数: [bold]{task.completed}[/]")
    ) as progress:
        task = progress.add_task("[cyan]抓取中...", total=100)

        for base_url in base_urls:
            while base_url:
                try:
                    console.log(f"请求页面: {base_url}")
                    response = requests.get(base_url, headers=HEADERS, timeout=10)
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
                        download_links, titles = extract_download_links(article, base_url)
                        total_links += len(download_links)
                        for link, title in zip(download_links, titles):
                            save_to_file(link, title)

                next_page_tag = soup.find('div', class_='pagelist').find('a', class_='next fas', title='下一页')
                base_url = next_page_tag.get('href') if next_page_tag else None
                if not base_url:
                    console.log("没有找到下一页链接，结束爬取。")
                    break

                progress.update(task, advance=10)
                progress.update(task, description=f"[cyan]抓取中... 总链接数: {total_links}")

    console.log(f"总共提取到 {total_links} 个下载链接")

if __name__ == "__main__":
    clear_screen()

    # 用户选择是否融合脚本内容
    if remove_existing_script():
        choice = input("是否融合已有脚本内容？（输入 'y' 进行融合，输入 'n' 覆盖文件）: ")
        if choice.lower() == 'n':
            os.remove(dl_sh_path)  # 用户选择覆盖文件，删除旧文件
            console.log(f"已删除旧的 {dl_sh_path} 文件。")
        elif choice.lower() != 'y':
            console.log("无效的选择，退出程序。")
            sys.exit()

    categories = {
        '1': 'baisi-v9l.html',
        '2': 'heisi-z2n.html',
        '3': 'rousi-9sw.html',
        '4': 'wangwa-18v.html',
        '5': {
            '1': '绅士约拍.html',
            '2': '爱丝.html',
            '3': '丝慕.html',
            '4': '丽丝映像.html',
            '5': '奈丝.html',
            '6': '森萝财团.html',
            '7': '猫萌榜.html',
            '8': '风之领域.html',
            '9': '袜涩.html',
            '10': '一千零一夜.html',
            '11': '轻兰映画.html',
            '12': '纳丝摄影.html',
            '13': '丝享家.html',
            '14': 'SIW斯文传媒.html',
            '15': '尤蜜荟.html',
            '16': '壹吻映画.html',
            '17': '异思趣向.html',
            '18': '蜜丝.html',
            '19': '喵糖映画.html',
            '20': '紧急企划.html',
            '21': '网络美女.html',
            '22': 'SSA丝社.html'
        },
        '6': 'search.php?q=',
        '7': ''
    }

    a = input("1.白丝 2.黑丝 3.肉丝 4.网袜 5.自选机构 6.搜索 7.所有 0.退出\n选择一个选项: ")
    base_urls = []

    if a in categories:
        if a == '5':
            clear_screen()
            print("选择机构（输入对应的数字）:")
            for num, name in categories['5'].items():
                print(f"{num}. {name}")
            b = input("输入机构编号: ")
            if b in categories['5']:
                base_urls = ['http://siwake.cc/category-' + categories['5'][b]]
            else:
                console.log("无效的机构编号。")
                sys.exit()
        elif a == '6':
            e = input("输入搜索内容: ")
            if e:
                base_urls = ['http://siwake.cc/' + categories[a] + e]
        elif a == '7':
            base_urls = ['http://siwake.cc/']
        else:
            base_urls = ['http://siwake.cc/tags-' + categories[a]]

    elif a == '0':
        console.log("退出程序。")
        sys.exit()
    else:
        console.log("无效的选项。")
        sys.exit()

    if base_urls:
        scrape_site(base_urls)
    else:
        console.log("没有提供有效的 URL。")
