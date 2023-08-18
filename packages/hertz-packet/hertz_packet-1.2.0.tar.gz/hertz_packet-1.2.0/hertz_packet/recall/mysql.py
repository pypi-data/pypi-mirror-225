# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : mysql.py
@Date    : 2023/5/19 17:48:39
@Author  : zhchen
@Desc    : 
"""

import subprocess
import pymysql


def get_mysql_databases(host, port, username, password):
    databases = []
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password
        )

        # 创建游标对象
        cursor = connection.cursor()

        # 执行查询数据库名的 SQL 语句
        cursor.execute("SHOW DATABASES")

        # 获取查询结果
        results = cursor.fetchall()

        # 提取数据库名
        for result in results:
            databases.append(result[0])

        # 关闭游标和数据库连接
        cursor.close()
        connection.close()
    except Exception as e:
        print('查询数据库失败:', str(e))
    return databases


def backup_mysql_databases(host, port, username, password, output_dir):
    # 查询所有数据库
    databases = get_mysql_databases(host, port, username, password)
    if not databases:
        print('未找到可备份的数据库。')
        return

    for database in databases:
        # 构建备份命令
        output_path = f'{output_dir}/{database}.sql'
        command = f'mysqldump -h {host} -P {port} -u {username} -p{password} {database} > {output_path}'

        try:
            # 执行备份命令
            subprocess.call(command, shell=True)
            print(f'数据库 {database} 备份成功！')
        except Exception as e:
            print(f'数据库 {database} 备份失败:', str(e))


# 使用示例
# host = 'localhost'  # MySQL 主机名
# port = 3306  # MySQL 端口，默认为 3306
# username = 'your_username'  # MySQL 用户名
# password = 'your_password'  # MySQL 密码
# output_dir = '/path/to/backup'  # 备份文件保存目录
#
# backup_mysql_databases(host, port, username, password, output_dir)
