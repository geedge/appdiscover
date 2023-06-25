from sklearn.cluster import DBSCAN

import category_encoders as ce
import pandas as pd

from p_columbus.filetreeinfo import FileInfo
from columbus.columbus import columbus
from p_columbus.applib import applabels


#最长公共子串
def find_lcsubstr(s1, s2):
    # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    m = [[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]
    mmax = 0   # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i+1][j+1] = m[i][j] + 1
                if m[i+1][j+1] > mmax:
                    mmax = m[i+1][j+1]
                    p = i+1
    return mmax   # 返回最长子串及其长度


def get_clusters(filelist):
    # 处理数据，提取特征
    feature_dic = {'ctime': [], 'user': [], 'filename': []}
    cs = []
    for file in filelist:
        fileinfo = FileInfo(file)
        if fileinfo.path.startswith('/sys/') or fileinfo.path.startswith('/proc/') or fileinfo.path.startswith(
                '/var/lib/apt/lists/'):
            continue
        cs.append(FileInfo(file))
    for item in cs:
        feature_dic['user'].append(item.user)
        #     feature_dic['group'].append(item.group)
        feature_dic['ctime'].append(item.ctime)
        filename = ''.join(item.path.split('/')[-3:])  # fn1+fn2+fn3
        filename_vec = sum([ord(chara) for chara in list(filename)])
        feature_dic['filename'].append(filename_vec)
    # 密度聚类
    data = pd.DataFrame.from_dict(feature_dic)
    vec = ce.OneHotEncoder(cols=['user'], use_cat_names=True).fit_transform(data)

    db_X = vec
    db = DBSCAN(eps=2000, min_samples=2).fit(db_X)  # 默认距离是欧几里得距离
    db_Y_pre = db.labels_
    n_clusters_ = len(set(db_Y_pre)) - (1 if -1 in db_Y_pre else 0)
    # 聚类完成

    # 根据标签处理聚类结果
    clusters = []
    noise = []
    for i in range(max(db_Y_pre) + 1):
        clusters.append([])
    for i in range(len(db_Y_pre)):
        if (db_Y_pre[i] != -1):
            clusters[db_Y_pre[i]].append(cs[i].path)
        #         clusters[db_Y_pre[i]].append(feature_dic['ctime'][i])
        else:
            noise.append(feature_dic['filename'][i])
    return clusters


def p_columbus(filelist,k=10,freq_threshold = 2):
    '''

    :param filelist:文件树信息
    :param k: 取top-k的tag
    :param freq_threshold: 频率下限
    :return: 软件列表
    '''
    #处理数据，提取特征
    clusters=get_clusters(filelist)
    #取top-k的tag
    tagss = []
    for cluster in clusters:
        cur_dic = {}
        tag_dict = columbus(cluster, freq_threshold=freq_threshold)
        # have fre
        tags = ['{}:{}'.format(tag, freq) for tag, freq
                in tag_dict.items()]
        if len(tags) > k:
            cur_dic['tags'] = tags
            #         print(tags[0])
            tagss.extend(tags[0:k + 1])
        else:
            tagss.extend(tags)
    #与软件名库匹配
    applist=[]
    for tag in tagss:
        a = 0
        pre_label = tag[:tag.find(':')]
        #     print(pre_label)
        for label in applabels:
            score = find_lcsubstr(label, pre_label) / len(label)
            if score > 0.8:
                applist.append(label)

        # if pre_label in applabels:
        #     applist.append(pre_label)
    return list(set(applist))



