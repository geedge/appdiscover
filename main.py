import re
import hostinfo
import os
from p_columbus.p_columbus import p_columbus

if __name__ == '__main__':
    print(hostinfo.get_mac_address())
    print(hostinfo.get_operate_sys())

    # path = r"E:\毕业设计\实验\system\client\lxy.txt"
    targetDir = "/"
    path = os.popen('sudo find ' + targetDir + ' | sudo xargs ls -lcd --full-time').readlines()
    with open(path, 'r',encoding='UTF-8') as f:
        files = f.readlines()
    filelist = [re.sub(' +', ' ', file.strip('\n')) for file in files]
    print(p_columbus(filelist))











