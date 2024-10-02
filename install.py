import os
import sys
import platform
import subprocess
import shutil
import time

def clear_screen():
    if sys.platform.startswith('linux'):
        print("\033c", end="")
    elif sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('darwin'):
        print("\033c", end="")
    else:
        print("\033c", end="")


os.system("python -m  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests bs4 rich")
clear_screen()

#安装wget
if sys.platform.startswith('linux'):
    system_info = platform.platform()
    if "ubuntu" in system_info.lower():
        os.system("apt install wget")
        print("安装成功,将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
    elif "debian" in system_info.lower():
        os.system("apt install wget")
        print("安装成功,将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
    elif "centos" in system_info.lower():
        os.system("yum install wget")
        print("安装成功,将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
    else:
        os.system("apt install wget")
        os.system("yum install wget")
        os.system("pacman -S wget")
        print("安装成功,将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
elif sys.platform.startswith('win'):
    if platform.machine().endswith('64'):
            import requests 
            url = 'https://eternallybored.org/misc/wget/1.21.4/64/wget.exe' 
            print("正在下载wget程序，请稍等")
            file = requests.get(url) 
            time.sleep(1)
            open('wget.exe','wb').write(file.content)
            clear_screen()
            print("注:64位的System32是64位系统文件夹,而SysWOW64是32位文件夹")
            a = input("是否将wget写入到PATH中(复制到System32)[y/n]")
            if (a == "y"):
                windir = os.environ.get("windir")
                system32 = windir + "\System32"
                src_path = "wget.exe"
                dst_path = system32 + "\wget.exe"
                shutil.copy(src_path, dst_path)
                os.remove("wget.exe")
                print("安装成功,将在三秒后关闭程序")
                time.sleep(3)
                sys.exit()
            else:
                if not os.path.exists('res'):
                  os.makedirs('res')
                src_path = "wget.exe"
                dst_path = "res" + "\wget.exe"
                shutil.copy(src_path, dst_path)
                os.remove("wget.exe")
                print("安装成功,将在三秒后关闭程序")
                time.sleep(3)
                sys.exit()

    else:
            import requests 
            url = 'https://eternallybored.org/misc/wget/1.21.4/32/wget.exe' 
            print("正在下载wget程序，请稍等")
            file = requests.get(url) 
            open('wget.exe','wb').write(file.content)
            clear_screen()
            print("注:32位的System32是32位系统文件夹,而System是16位文件夹")
            a = input("是否将wget写入到PATH中(复制到System32)}[y/n]")
            if (a == "y"):
                windir = os.environ.get("windir")
                system32 = windir + "\System32"
                src_path = "wget.exe"
                dst_path = system32 + "\wget.exe"
                shutil.copy(src_path, dst_path)
                os.remove("wget.exe")
                print("安装成功,将在三秒后关闭程序")
                time.sleep(3)
                sys.exit()
            else:
                if not os.path.exists('res'):
                  os.makedirs('res')
                src_path = "wget.exe"
                dst_path = "res" + "\wget.exe"
                shutil.copy(src_path, dst_path)
                os.remove("wget.exe")
                print("安装成功,将在三秒后关闭程序")
                time.sleep(3)
                sys.exit()

elif sys.platform.startswith('darwin'):
    result = subprocess.run(['wget'], capture_output=True, text=True)


    if (result.stdout == "-bash: wget: command not found"):
        os.system("/bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'")
        os.system("brew install wget")
        print("如果报错zsh: command not found: brew")
        print("请前往https://zhuanlan.zhihu.com/p/463849226自行按教程安装")
        print("安装成功,将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
    else:
        print("已安装wget")
        print("将在三秒后关闭程序")
        time.sleep(3)
        sys.exit()
else:
    print('未知系统')
    print("将在三秒后关闭程序")
    time.sleep(3)
    sys.exit()

