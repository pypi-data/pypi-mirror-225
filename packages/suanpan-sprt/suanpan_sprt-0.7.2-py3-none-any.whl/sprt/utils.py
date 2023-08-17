import os
import hashlib
import base64


def safe_mkdirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
    return path


def safe_mkdirs_for_file(filepath):
    return safe_mkdirs(os.path.dirname(os.path.abspath(filepath)))


def md5(filepath, block_size=64 * 1024):
    with open(filepath, "rb") as f:
        _md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            _md5.update(data)
    return base64.b64encode(_md5.digest()).decode()


def should_log_rollover(filename, max_bytes=10485760):
    if not os.path.exists(filename):
        return False

    st = os.stat(filename)
    return st.st_size > max_bytes


def do_log_rollover(filename, backup_count=3):
    if backup_count > 0:
        for i in range(backup_count - 1, 0, -1):
            sfn = f'{filename}.{i}'
            dfn = f'{filename}.{i + 1}'
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)
        dfn = f'{filename}.{1}'
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(filename, dfn)
    else:
        os.remove(filename)
