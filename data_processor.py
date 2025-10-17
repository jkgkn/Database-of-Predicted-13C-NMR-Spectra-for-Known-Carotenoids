import os
import pandas as pd
from config import FILES_DIRECTORY

class CSVProcessingError(Exception):
    """自定义CSV处理异常"""

def validate_filepath(filename):
    """安全验证文件路径"""
    safe_path = os.path.abspath(os.path.join(FILES_DIRECTORY, filename))
    if not safe_path.startswith(FILES_DIRECTORY):
        raise ValueError(f"非法文件路径: {filename}")
    return safe_path

def load_and_normalize_csv(filenames):
    """
    加载并归一化CSV数据
    返回格式：{x: [], spectra: {filename: y_normalized}}
    """
    all_data = {'x': [], 'spectra': {}}
    
    try:
        for filename in filenames:
            filepath = validate_filepath(filename)
            
            # 读取CSV文件（强制使用制表符分隔）
            try:
                df = pd.read_csv(
                    filepath,
                    sep='\t',
                    header=None,
                    names=['x', 'y','nn'],
                    engine='c',
                    dtype='float64',
                    on_bad_lines='warn'   # 新参数，替代 error_bad_lines/warn_bad_lines
                )
            except pd.errors.ParserError as e:
                raise CSVProcessingError(f"文件 {filename} 解析失败: {str(e)}")
                
            # 数据有效性检查
            if df.shape[1] < 2:
                raise CSVProcessingError(f"文件 {filename} 列数不足")
                
            # 归一化处理
            y_min = df['y'].min()
            y_max = df['y'].max()
            df['y_normalized'] = (df['y'] - y_min) / (y_max - y_min + 1e-9)
            
            # 存储数据
            if not all_data['x']:
                all_data['x'] = df['x'].round(6).tolist()  # 限制小数位数
            all_data['spectra'][filename] = df['y_normalized'].round(6).tolist()
            
        return all_data
    except Exception as e:
        raise CSVProcessingError(str(e))
