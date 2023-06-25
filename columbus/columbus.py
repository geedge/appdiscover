import copy
import sys
import os
import optparse
import pickle
import logging
import glob
import yaml
from datetime import datetime

from .trie import Trie
from .tags import filtertags

# from trie import Trie
# from tags import filtertags

FILTER_PATH_TOKENS = ['usr', 'bin', 'proc', 'sys', 'etc', 'local', 'src',
                      'dev', 'home', 'root', 'lib', 'pkg', 'sbin', 'share',
                      'cache']

COLUMBUS_CACHE = {}
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False

def refresh_columbus():
    global COLUMBUS_CACHE
    COLUMBUS_CACHE = {}


def columbus(changeset, freq_threshold=1, use_cache=False):
    """ Get labels from single changeset """
    if use_cache:
        key = str(sorted(changeset))
        if key in COLUMBUS_CACHE:
            return COLUMBUS_CACHE[key]
    tags = run_file_paths_discovery2(
        filtertags, changeset, freq_threshold=freq_threshold)
    if use_cache:
        COLUMBUS_CACHE[key] = tags
    sum=0
    for fre in tags.values():
        sum=sum+fre
    for token,fre in tags.items():
        tags[token]=fre/sum

    return tags

def columbus(changeset, freq_threshold=1, use_cache=False):
    """ Get labels from single changeset without fre """
    if use_cache:
        key = str(sorted(changeset))
        if key in COLUMBUS_CACHE:
            return COLUMBUS_CACHE[key]
    tags = run_file_paths_discovery2(
        filtertags, changeset, freq_threshold=freq_threshold)
    if use_cache:
        COLUMBUS_CACHE[key] = tags
    sum=0
    for fre in tags.values():
        sum=sum+fre
    for token,fre in tags.items():
        tags[token]=fre/sum

    return tags


def run_file_paths_discovery2(filtertags, changeset, freq_threshold=1):
    ftrie = Trie(frequency_limit=freq_threshold)
    for filepath in changeset:
        pathtokens = filepath.split('/')
        for token in pathtokens:
            if token not in FILTER_PATH_TOKENS:
                ftrie.insert(token)

    softtags = ftrie.get_all_tags()
    # softtagss=copy.deepcopy(softtags)
    for tag in filtertags:
        softtags.pop(tag, None)
        # softtags={key:value for key,value in softtags.items() if not key.startwith(tag)}
        # for key in softtags.keys():
        #     if key.startswith(tag):
        #         softtagss.pop(key,None)
    softtags = {key: value for key, value in softtags.items() if not is_number(key)}
    return softtags
