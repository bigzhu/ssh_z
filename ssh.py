#!/usr/bin/env python3
# encoding=utf-8
# file_name=ssh.py

# from __future__ import print_function  # 为了让 Python2 的 print() 不要打印成 tuple
import os
import sys
from bigzhu_py.file_z import csv_z
from bigzhu_py.print_z import table_print

file_path = ""


def read_hosts():
    """
    读取置文件
    """
    global file_papth
    file_papth = f"{sys.path[0]}/hosts.csv"
    header, rows = csv_z.read_csv(file_papth)
    return header, rows


# 添加 number 和打印
def print_info(header: list, rows: list):
    header.insert(0, "Number")
    print_rows = [[i] + rows[i] for i in range(len(rows))]
    table_print([header] + print_rows, "    ")


def ssh(ssh_info):
    print(ssh_info)
    user = ssh_info[0]
    ip = ssh_info[1]
    port = ssh_info[3] if len(ssh_info) > 4 else 22
    print("ssh 登录 %s 中......" % ssh_info[1])
    command = "export TERM=xterm;ssh -p %s %s@%s" % (port, user, ip)
    os.system(command)


def add_new():
    user = input("请输入用户名:")
    if user is None:
        raise ValueError("必须输入用户名")
    host = input("请输入ip or hostname:")
    if host is None:
        raise ValueError("必须输入ip or hostname")
    port = input("请输入端口(默认22):").strip() or 22
    description = input("请输入附加说明:").strip() or "无"
    csv_z.write_csv_append(file_papth, [user, host, port, description])
    print("添加成功!")
    main()


def select(header: list, rows: list):
    print_info(header, rows)
    # 输入
    i_value = input("请输入序列号 or ip or hostname (q 退出, a 添加):")
    if i_value == "a":
        add_new()
        return
    if i_value == "q":
        exit(0)
    try:
        # 尝试转为int, 看输入是否为编号
        i_value = int(i_value)
        if i_value <= len(rows):
            ssh(rows[i_value])
            return
        else:
            i_value = str(i_value)
    except ValueError:
        pass
        # print verr

    selected_ssh_infos = []
    for i in rows:
        index = i[1].find(i_value)
        if index != -1:
            selected_ssh_infos.append(i)
        # 也搜索描述
        index = i[3].find(i_value)
        if index != -1:
            selected_ssh_infos.append(i)

    if not selected_ssh_infos:
        print("没找到和这个ip有近似的")
        select(header, rows)
    elif len(selected_ssh_infos) == 1:  # 找到一个，直接登录
        ssh(selected_ssh_infos[0])
        return
    else:
        print("找到%s个匹配%s的, 请再次选择!" % (len(selected_ssh_infos), i_value))
        return select(header, selected_ssh_infos)  # 找到一堆，再过滤


def main():
    header, hosts = read_hosts()
    select(header, hosts)


if __name__ == "__main__":
    main()
