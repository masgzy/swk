2.1为基础的版本
2.2为只有UTF-8的版本
2.3为Windows加入GBK
2.3up为生成静默下载
2.4更新自定义域名(即可以使用镜像，iurl是img.siwake.cc的 wurl是siwake.cc的)
(注:此后脚本都使用静默下载)
2.4m为cloudflare默认镜像

(注:镜像和原站国内应该都难以访问)
(注:现在的程序默认生成为wget的脚本，不自带下载功能)

install.py是一键安装依赖的脚本
res/bm.py是将UTF-8的bat切换为GBK的
csh.sh为termux初始化脚本，请手动修改其中的tm
csh1.sh为正常Linux环境的初始化
初始化时会把swk.sh复制到/usr/bin目录的sw(如果是termux则是/data/data/com.termux/files/usr/bin)，请确保您有权限，默认把sw的权限修改为777
sw是将start.sh复制到/usr/bin目录的swk(如果是termux则是/data/data/com.termux/files/usr/bin)

