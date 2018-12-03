# 项目概述

## 如何安装
1. 需要环境
    ```
    系统环境: Linux, Mac和Windows
    运行环境: Python3.5+
    ```
2. 打包seed
    ```
    进入seed项目根目录
    运行 python setup.py install
    ```
3. 初始化seed的config文件
    ```
    执行seed init
    ```
4. config文件设置
    ```
    打开用户根目录下的.seed/seed_config.py文件
    进行数据库等相关的配置
    如: vim ~/.seed/seed_config.py
    ```
5. 初始化数据库
    ```
    进行数据库初始化, 执行
    seed upgrade
    即可
    ```
6. 运行web程序
    ```
    执行 seed run web运行web系统
    ```
7. 访问
    ```
    127.0.0.1:5000 可访问系统
    ```

## 如何升级
1、获取到最新代码
2、打包seed
    ```
    进入seed项目根目录
    运行 python setup.py install
    ```
3. 运行web程序
    ```
    执行 seed run web运行web系统
    ```
4. 访问
    ```
    127.0.0.1:5000 可访问系统
    ```

## 开发模式
1. 安装seed的pip运行文件到第三方库中
    ```
    python setup.py develop
    ```
2. 运行seed数据
    ```
    seed init
    ```
3. 设置数据库
    ```
    vim ~/.seed/seed_config.py
    ```
4. 运行web
    ```
    seed run web
    ```