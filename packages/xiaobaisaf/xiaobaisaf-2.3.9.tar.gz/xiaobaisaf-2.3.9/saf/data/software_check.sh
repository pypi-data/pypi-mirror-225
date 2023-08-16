#!/bin/bash

# 检测Python是否安装
python_version=$(python --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "Python已安装，版本号：$python_version"
else
    echo "Python未安装，请访问 https://www.python.org/downloads/ 下载并安装。"
fi

# 检测JDK是否安装
jdk_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
if [[ $? -eq 0 ]]; then
    echo "JDK已安装，版本号：$jdk_version"
else
    echo "JDK未安装，请访问 https://www.oracle.com/java/technologies/javase-jdk11-downloads.html 下载并安装。"
fi

# 检测NodeJS是否安装
node_version=$(node --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "NodeJS已安装，版本号：$node_version"
else
    echo "NodeJS未安装，请访问 https://nodejs.org/en/download/ 下载并安装。"
fi

# 检测MAVEN是否安装
maven_version=$(mvn --version 2>&1 | grep "Apache Maven" | awk '{print $3}')
if [[ $? -eq 0 ]]; then
    echo "MAVEN已安装，版本号：$maven_version"
else
    echo "MAVEN未安装，请访问 https://maven.apache.org/download.cgi 下载并安装。"
fi
# 等待用户按下任意键
read -n 1 -s -r -p "按下任意键结束脚本..."

# 结束脚本的执行
exit