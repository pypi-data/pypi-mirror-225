# -*- coding:utf-8 -*-
import os


def mkdirs(file_path):
    """
    判断文件路径所在的目录是否存在，如果不存在则创建目录
    :param file_path: 文件路径
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_file(path):
    """
    This function checks if a file path exists and returns the type of the path.

    :param path: The path to the file.
    :type path: str
    :return: A string indicating the type of path. Possible values are 'File', 'Directory', or ''.
    :rtype: str
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            return "File"
        elif os.path.isdir(path):
            return "Directory"
    else:
        return ""
