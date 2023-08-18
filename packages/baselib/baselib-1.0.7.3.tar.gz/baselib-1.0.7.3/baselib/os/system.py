# -*- coding:utf-8 -*-
import subprocess
import sys
import signal


class TimeoutExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutExpired


def run_cmd(
        cmd,
        deamon=False,
        timeout=None,
        return_list=True,
        encoding="utf-8"):
    """
    执行系统命令, 并获取返回值

    :param cmd: str, 要执行的命令
    :param deamon: bool, 是否以守护进程的方式运行命令
    :param timeout: float, 命令执行的最长时间
    :param return_list: bool, 是否返回list类型的结果
    :param encoding: str, 命令执行结果的编码方式，默认为utf-8
    :return: list/str/Popen, 返回命令执行结果，如果deamon=True，则返回Popen对象
    """
    if sys.version_info.major == 2:
        subp = subprocess.Popen(['/bin/sh', '-c', cmd],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    else:
        subp = subprocess.Popen(['/bin/sh', '-c', cmd],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding=encoding)
    if deamon:
        return subp
    out = communicate(subp, timeout)
    if return_list:
        return out[0].split("\n")
    # out format: (stdout_data, stderr_data)
    return out


def communicate(subp, timeout=None):
    if sys.version_info[0] >= 3:
        expired = False
        try:
            return subp.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
        if expired:
            raise TimeoutExpired("Command timed out after {} seconds".format(timeout))

    # Set up a SIGALRM handler to raise an exception after the specified timeout
    if timeout is not None:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)
    try:
        # Write the input data to stdin and read the output from stdout and stderr
        out, err = subp.communicate()
    except TimeoutExpired:
        # If the timeout was reached, kill the child process and raise a TimeoutError
        subp.kill()
        raise TimeoutExpired("Command timed out after {} seconds".format(timeout))
    finally:
        # Reset the SIGALRM handler to its default behavior
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    # Return the output and error as strings
    return out.decode(), err.decode()
