#python3
#####批量提取文件夹内所有碳谱数据
##########单独提取每个谱图的峰值化学位移值，
###对于预测数据来说，因峰型稳定，无杂质及溶剂干扰，提取效果好
##其中设置峰值peak筛选，height=4，即设置最小峰高为最大峰的4%，这在此类化合物中足够了，碳谱来说，不会有某类碳的个数大于某单碳二十倍以上，故此其峰值不会高出20倍
#distance=1峰间距至少1

import numpy as np
import pandas as pd
import os
from scipy.signal import find_peaks

def read_spectrum(file_path):
    """读取CSV文件并返回排序后的位移和强度数组"""
    df = pd.read_csv(file_path, sep='\t', header=None)
    df.columns = ['shift', 'intensity', "NA"]
    df = df.sort_values(by='shift').reset_index(drop=True)
    return df['shift'].values, df['intensity'].values

def filter_solvent_peaks(shifts, intensities, solvent_regions):
    """过滤溶剂峰区域"""
    # 过滤掉溶剂峰区域对应的数据
    mask = np.ones(len(shifts), dtype=bool)
    for (start, end) in solvent_regions:
        mask &= (shifts < start) | (shifts > end)  # 去掉溶剂峰区域内的峰
    return shifts[mask], intensities[mask]

def detect_peaks(shifts, intensities, height=4, distance=1):
    """
    检测碳谱中的特征峰
    参数：
    height: 最小峰高（相对强度百分比）
    distance: 峰间最小间隔（ppm）
    """
    # 预处理强度数据
    max_intensity = np.max(intensities)
    rel_intensity = intensities / max_intensity * 100  # 转换为百分比强度
    
    # 查找峰值
    peaks, _ = find_peaks(rel_intensity, 
                         height=height,
                         distance=int(distance/0.1))  # 转换为数据点间隔
    
    # 过滤低强度峰
    valid_peaks = shifts[peaks]
    return valid_peaks

def save_peak_data(peaks, original_path):
    """保存峰位移数据"""
    base = os.path.splitext(original_path)[0]
    save_path = f"{base}_peaks.csv"
    
    df = pd.DataFrame({'chemical_shift': peaks})
    df.to_csv(save_path, index=False)
    print(f"Saved peak data to: {save_path}")

def extract_chemical_shifts(file1, solvent_regions=None):
    """主流程，提取单一分子的化学位移值"""
    # 默认溶剂峰设置
    if solvent_regions is None:
        solvent_regions = [(76.5, 77.7)]  # CDCl3,规避其它溶剂请对应添加
    
    # 读取数据
    shifts1, intensities1 = read_spectrum(file1)
    
    # 屏蔽溶剂峰
    shifts1, intensities1 = filter_solvent_peaks(shifts1, intensities1, solvent_regions)
    
    # 进行峰检测
    peaks1 = detect_peaks(shifts1, intensities1, height=4, distance=1)
    
    # 保存峰数据
    #save_peak_data(peaks1, file1)
    
    # 返回化学位移值
    return peaks1
def file_name2(file_dir): #
    #注意返回至文件夹中所有文件，会打开深层文件夹查找
    L=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if 'C.csv' in file:
                L.append(os.path.join(root, file))
    return L

def cv_imread(filePath):#解决中文不识别问题
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img 
dictseq={}
dictseq2={}

for key in file_name2("path_to_csvs"):#存储预测碳谱或实测碳谱原始数据的csv表所在文件夹
    dictseq[key]=1  
    
solvent_regions = [(76.5, 77.7)]  # 溶剂峰区域

with open("path_to_output/chunchemical_shifts.csv", 'w') as f:  
    for key  in dictseq:
        name=key.split("/")[-1]
        chemical_shifts = extract_chemical_shifts(key,solvent_regions)
        #print(name,len(chemical_shifts))
        f.write(name+",")
        for k in chemical_shifts:
            f.write(str(round(k,4))+",")
        f.write("\n")
