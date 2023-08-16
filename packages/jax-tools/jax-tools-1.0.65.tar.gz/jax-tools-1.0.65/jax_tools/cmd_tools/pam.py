#! env python3
# -*- coding:utf-8 -*-
"""
Password Manager
"""
import json
import os
import pyperclip
import sys
from jax_tools.encrypt import AESCipher
from jax_tools.utils.settings import JAX_DATA_DIR


class PasswordManager(object):
    """
    Password Manager
    """
    # Define pam data file
    data_file = os.path.join(JAX_DATA_DIR, '.pam.json')
    if os.path.exists(data_file):
        data_list = json.loads(open(data_file, 'r').read())
    else:
        data_list = list()

    # Define string
    NAME = 'name'
    USERNAME = 'username'
    PASSWORD = 'password'
    DUPLICATE_ACCOUNT = u'您输入的账号名在系统中已存在，请修改账号名进行区分'
    ACCOUNT_CREATED = u'账号{}已创建成功'
    ACCOUNT_DELETED = u'账号{}已删除成功'
    NUM_OF_ACCOUNT = u'第{0}个账号信息: {1}'
    ACCOUNT_NOT_FOUND = u'账号{}没有找到格，如果您输入的账号信息含空格，请将完整的账号引号"包裹起来'

    def get_password(self, search_str=None):
        """
        Get Password
        Args:
            search_str: Search string

        Returns: password

        """
        # If search string is integer, get password by num
        try:
            pyperclip.copy(self.__get_pw_by_num(int(search_str)))
        # If search string is not integer, get password by name
        except ValueError:
            pw = self.__search_by_equal(search_str)
            if pw:
                pyperclip.copy(pw)
            elif self.__search_by_start(search_str):
                pyperclip.copy(self.__search_by_start(search_str))
            else:
                pyperclip.copy(self.__search_by_contains(search_str))

    def __search_by_start(self, search_str):
        """
        Search by start
        Args:
            search_str (str): Search string

        Returns:

        """
        # Reverse data list
        for encrypted_pw_info in self.data_list:
            # Decrypt password info
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            # Get account name
            name = pw_info.get(self.NAME)
            # If name equals search string, copy password to clipboard
            if name.startswith(search_str):
                return pw_info.get(self.PASSWORD)

    def __search_by_contains(self, search_str):
        """
        Search by contains
        Args:
            search_str (str): Search string

        Returns:

        """
        # Reverse data list
        for encrypted_pw_info in self.data_list:
            # Decrypt password info
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            # Get account name
            name = pw_info.get(self.NAME)
            # If name equals search string, copy password to clipboard
            if name.__contains__(search_str):
                return pw_info.get(self.PASSWORD)
        return str()

    def __get_pw_by_num(self, num):
        """
        Get password by num
        Args:
            num (int): Num

        Returns:

        """
        try:
            encrypted_pw_info = self.data_list[num - 1]
        except IndexError:
            print('Jax Remind: The account number you entered does not exist')
            sys.exit(1)
        pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
        return pw_info.get(self.PASSWORD)

    def __search_by_equal(self, search_str):
        """
        Search by equal
        Args:
            search_str (str): Search string

        Returns:

        """
        # Reverse data list
        for encrypted_pw_info in self.data_list:
            # Decrypt password info
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            # Get account name
            name = pw_info.get(self.NAME)
            # If name equals search string, copy password to clipboard
            if name == search_str:
                return pw_info.get(self.PASSWORD)

    @classmethod
    def print_account_list(cls):
        """
        Print account list
        Returns:

        """
        # Define max length
        max_name_len = 4
        max_username_len = 8
        min_serial_len = 3
        max_serial_len = len(str(len(cls.data_list)))
        space_len = 2
        if max_serial_len < min_serial_len:
            max_serial_len = min_serial_len
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            name = pw_info.get(cls.NAME)
            username = pw_info.get(cls.USERNAME)
            if len(name) > max_name_len:
                max_name_len = len(name)
            if len(username) > max_username_len:
                max_username_len = len(username)
        head_and_tail_str = '+' + '-' * (max_serial_len + space_len) + '+' + '-' * (
                    max_name_len + space_len) + '+' + '-' * (max_username_len + space_len) + '+'
        print('Jax Remind: You have {} accounts'.format(len(cls.data_list)))
        print('Use "jax-pam NUM" to get the password for the specified NUM to the clipboard， exp: jax-pam 6,'
              ' then you can paste the password to the specified location')
        print(head_and_tail_str)
        print(f'| {"NUM".ljust(max_serial_len)} | {"NAME".ljust(max_name_len)} | {"USERNAME".ljust(max_username_len)} |'
              )
        print(head_and_tail_str)
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            name = pw_info.get(cls.NAME)
            username = pw_info.get(cls.USERNAME)
            serial_num = cls.data_list.index(encrypted_pw_info) + 1
            print(
                f'| {str(serial_num).ljust(max_serial_len)} | {name.ljust(max_name_len)} |'
                f' {username.ljust(max_username_len)} |')
        print(head_and_tail_str)

    @classmethod
    def delete_account(cls, name):
        """
        Delete account
        Args:
            name: Account name

        Returns:

        """
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            account_name = pw_info.get(cls.NAME)
            if name == account_name:
                cls.data_list.remove(encrypted_pw_info)
                # dump account list to json
                data_json = json.dumps(cls.data_list)
                # write to data file
                open(cls.data_file, 'w').write(data_json)
                # Print finally message
                print(cls.ACCOUNT_DELETED.format(name))
                return
        print(cls.ACCOUNT_NOT_FOUND.format(name))

    @classmethod
    def add_account(cls, name, username, password):
        """
        Add Account to data file
        Args:
            name: Account name
            username: Username
            password: Password

        Returns:

        """
        # Traverse encrypted account list
        for encrypted_pw_info in cls.data_list:
            # Get account information
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            account_name = pw_info.get(cls.NAME)
            # If new name is duplicate with exist name, return and print a message
            if name == account_name:
                print(cls.DUPLICATE_ACCOUNT)
                return
        # Define account information use a dict
        account_info = {cls.NAME: name, cls.USERNAME: username, cls.PASSWORD: password}
        # Define encrypted account information
        encrypted_account_info = AESCipher().encrypt(json.dumps(account_info))
        # Add new account to account list
        cls.data_list.append(encrypted_account_info)
        # dump account list to json
        data_json = json.dumps(cls.data_list)
        # write to data file
        open(cls.data_file, 'w').write(data_json)
        # Print finally message
        print(cls.ACCOUNT_CREATED.format(name))


if __name__ == '__main__':
    try:
        PasswordManager().get_password(sys.argv[1])
    except IndexError:
        pass
