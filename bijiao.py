#python3
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
from fastdtw import fastdtw
from scipy.optimize import linear_sum_assignment
def find_optimal_matching(a, b, T=0.2):
    """
    改进版匈牙利算法匹配，处理不同长度数据集
    """
    # 创建扩展成本矩阵
    max_len = max(len(a), len(b))
    cost_matrix = np.full((max_len, max_len), 1e6)  # 使用大数表示不匹配
    
    # 填充有效匹配的代价
    for i in range(len(a)):
        for j in range(len(b)):
            diff = abs(a[i] - b[j])
            if diff <= T:
                cost_matrix[i,j] = diff  # 有效匹配代价
            else:
                cost_matrix[i,j] = 1e6  # 无效匹配

    # 添加虚拟节点处理不匹配情况
    for i in range(len(a), max_len):
        cost_matrix[i,:] = 0.5 * T  # 虚拟a节点匹配代价
    for j in range(len(b), max_len):
        cost_matrix[:,j] = 0.5 * T  # 虚拟b节点匹配代价

    # 寻找最优匹配
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # 过滤有效匹配对
    valid_pairs = []
    for i, j in zip(row_ind, col_ind):
        if i < len(a) and j < len(b) and cost_matrix[i,j] <= T:
            valid_pairs.append((i, j))
    return valid_pairs
def euclidean_distance(a, b):
    # 确保两个列表长度相同
    max_len = max(len(a), len(b))
    a.extend([0] * (max_len - len(a)))  # 用0填充
    b.extend([0] * (max_len - len(b)))  # 用0填充
    return np.sqrt(np.sum((np.array(a) - np.array(b)) ** 2))
def manhattan_distance(a, b):
    # 确保两个列表长度相同
    max_len = max(len(a), len(b))
    a.extend([0] * (max_len - len(a)))  # 用0填充
    b.extend([0] * (max_len - len(b)))  # 用0填充
    return np.sum(np.abs(np.array(a) - np.array(b)))
def pearson_correlation(a, b):
    # 确保两个列表长度相同
    max_len = max(len(a), len(b))
    a.extend([0] * (max_len - len(a)))  # 用0填充
    b.extend([0] * (max_len - len(b)))  # 用0填充
    correlation, _ = pearsonr(a, b)
    return correlation
def cosine_similarity_distance(a, b):
    # 确保两个列表长度相同
    max_len = max(len(a), len(b))
    a.extend([0] * (max_len - len(a)))  # 用0填充
    b.extend([0] * (max_len - len(b)))  # 用0填充
    # 计算余弦相似度
    return cosine_similarity([a], [b])[0][0]
def dynamic_time_warping(a, b):
    # 将数据转换为序列对的形式
    A_seq = [(x,) for x in a]
    B_seq = [(x,) for x in b]
    distance, _ = fastdtw(A_seq, B_seq, dist=euclidean)
    return distance
def tanimoto_similarity(an, bn):
    vec_a=generate_fingerprint(an)
    vec_b=generate_fingerprint(bn)
    intersection = np.sum(np.bitwise_and(vec_a, vec_b))
    union = np.sum(vec_a) + np.sum(vec_b) - intersection
    return intersection / union if union != 0 else 0.0
def generate_fingerprint(aligned_values):
    """
    将对齐后的光谱数据（含0填充）转换为分子指纹
    存在非零则为1，0仍为0
    :return: 二进制指纹向量
    """
    fingerprint=[]
    for key in aligned_values:
        if key !=0:fingerprint.append(1)
        else:fingerprint.append(0)
    return fingerprint
def robust_align_spectra(a, b, T=0.2):
    a = np.array(a)
    b = np.array(b)
    
    # 寻找最优匹配
    matched_pairs = find_optimal_matching(a, b, T)
    
    # 创建匹配字典
    a_matched = set(i for i,j in matched_pairs)
    b_matched = set(j for i,j in matched_pairs)
    
    # 构建对齐序列
    an, bn = [], []
    num=0
    numz=0
    
    # 处理a序列
    a_ptr = 0
    for i in range(len(a)):
        if i in a_matched:
            j = [j for (pi, j) in matched_pairs if pi == i][0]
            an.append(a[i])
            bn.append(b[j])
            num+=1
            numz+=1
        else:
            an.append(a[i])
            bn.append(0)
            numz+=1
    
    # 处理未匹配的b元素
    for j in range(len(b)):
        if j not in b_matched:
            an.append(0)
            bn.append(b[j])
            numz+=1
    
    return an, bn,num,numz
##############################################################
#######实测用于比较的数据########################
jky=[12.98,13.31,14.0,16.18,16.49,23.27,26.94,28.15,28.85,29.86,36.19,44.37,51.0746,56.76,69.33,121.54,125.06,126.27,130.15,130.49,130.53,132.58,134.53,135.33,135.48,136.57,137.49,138.2]
jks=[12.8,13.1,13.8,16.3,23.1,26.8,28,28.7,36,44.2,56.6,69.2,121.4,124.9,126.1,130,130.3,130.4,132.4,134.4,135.2,135.3,136.4,137.3,138]
#################################################
#####################################################
#预测的化学位移值库#############
dictseq={}
with open("path_to_output/chunchemical_shifts.csv", 'r') as f:
    lines=f.readlines()
    #print(len(lines))
    for line in lines:
        ll=line.split(",")
        #CA01130_C.csv,13.1645,13.2446,
        key=ll[0].split("_C.csv")[0]
        if len(key)>1:#根据需求设置筛选条件
            i=1
            #print(key)
            dictseq[key]=[]
            while i<len(ll)-1:
                dictseq[key].append(float(ll[i]))
                i+=1
#######################################################################

#####################################################
######比较单独两条数据选用，按需求更改上面jky和jks对应数据即可##############
an, bn,n,m= robust_align_spectra(jky, jks, T=1)
print(str(n)+","+str(m)+","+str(round(dynamic_time_warping(jky, jks),4))+","+str(round(cosine_similarity_distance(an, bn),4))+","+str(round(pearson_correlation(an, bn),4))+","+str(round(manhattan_distance(an, bn),4))+","+str(round(euclidean_distance(an, bn),4))+","+str(round(tanimoto_similarity(an, bn),4))+"\n")

################################################################################
##################使用一条实测数据与所有数据集的数据进行比较选用###########
with open("path_to_output2/jkytestn.csv", 'w') as f:  f.write("key,num,numz,dynamic_time_warping,cosine_similarity_distance,pearson_correlation,manhattan_distance,euclidean_distance,tanimoto_similarity\n")
    
    for key in dictseq:
        an, bn,n,m= robust_align_spectra(jky, dictseq[key], T=1)
        f.write(key+","+str(n)+","+str(m)+","+str(round(dynamic_time_warping(jky, dictseq[key]),4))+","+str(round(cosine_similarity_distance(an, bn),4))+","+str(round(pearson_correlation(an, bn),4))+","+str(round(manhattan_distance(an, bn),4))+","+str(round(euclidean_distance(an, bn),4))+","+str(round(tanimoto_similarity(an, bn),4))+"\n")
########################################################################################################## 

#############################################################################
###########数据集中所有进行两两比对选用#########
#所有比较
dictseq2={}
with open("/storage2/JK49/lipidmapsDB/MNvoa/chunjing/jkytestnss.csv", 'w') as f: 
    f.write("key1,key2,num,numz,dynamic_time_warping,cosine_similarity_distance,pearson_correlation,manhattan_distance,euclidean_distance,tanimoto_similarity\n")
    for key  in dictseq:
        for key2 in dictseq:
            if (key + key2 not in dictseq2) and (key2 + key not in dictseq2):
                dictseq2[key+key2]=1
                dictseq2[key2+key]=1
                an, bn,n,m= robust_align_spectra(dictseq[key], dictseq[key2], T=1)
                f.write(key+","+key2+","+str(n)+","+str(m)+","+str(round(dynamic_time_warping(dictseq[key], dictseq[key2]),4))+","+str(round(cosine_similarity_distance(an, bn),4))+","+str(round(pearson_correlation(an, bn),4))+","+str(round(manhattan_distance(an, bn),4))+","+str(round(euclidean_distance(an, bn),4))+","+str(round(tanimoto_similarity(an, bn),4))+"\n")
######################################################################################################