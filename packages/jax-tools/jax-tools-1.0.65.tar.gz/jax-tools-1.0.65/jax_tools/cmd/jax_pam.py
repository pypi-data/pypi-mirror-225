#!env python3
# -*- coding:utf-8 -*-
"""
Poppy Entrypoint
"""
from jax_tools.cmd_tools.pam import PasswordManager as pm
import sys
import getpass


def print_help():
    """
    Print Help message
    Returns:

    """
    print(u'--help 打印帮助信息')
    print(u'--list 打印账号列表')
    print(u'--delete 删除账号信息,指定账号名,如--delete account1')
    print(u'--add 添加账号信息,指定账号名')
    print(u'输入非上述的--开头的内容，则表示搜索账号，并将搜索到的账号的密码复制到剪贴板')


def main():
    """
    Main Function
    Returns:

    """
    list_sign_list = ['--list', 'list']
    add_sign_list = ['add', '--add']
    help_sign_list = ['--help', '-h']
    delete_sign_list = ['--delete', 'delete']

    try:
        arg_1 = sys.argv[1]
        if arg_1 in list_sign_list:
            pm.print_account_list()
        elif arg_1 in help_sign_list:
            print_help()
        elif arg_1 in add_sign_list:
            name = input(u'请输入您的要新建的账号名称(如:jenkins web root account)：')
            username = input(u'请输入你的登录用户名: ')
            password = getpass.getpass(u'请输入你的登录密码或验证token: ')
            pm.add_account(name, username, password)
        elif arg_1 in delete_sign_list:
            if len(sys.argv) > 2:
                name = '' .join(sys.argv[2:])
                pm.delete_account(name)
            else:
                name = input(u'请输入您想要删除的账号名称：')
                pm.delete_account(name)
        else:
            pm().get_password(sys.argv[1])
    except IndexError:
        print_help()


if __name__ == '__main__':
    main()
