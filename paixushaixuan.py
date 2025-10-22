#python3
import pandas as pd

# 读取文件（无表头）
df = pd.read_csv('Results_Table_with_Molecular_Weight_Information.csv', header=None)

# 添加列名
df.columns = [f'col{i+1}' for i in range(df.shape[1])]

# 将倒数两列转换为浮点数，无法转换的设为NaN
df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
df.iloc[:, -2] = pd.to_numeric(df.iloc[:, -2], errors='coerce')

# 筛选：倒数两列差值绝对值小于1，并显式创建副本
#当无分子量信息时，直接使用原始数据
df_filtered = df[abs(df.iloc[:, -1] - df.iloc[:, -2]) < 1].copy()

# 确保第10列和第5列是数值型
df_filtered.loc[:, df_filtered.columns[9]] = pd.to_numeric(df_filtered[df_filtered.columns[9]], errors='coerce')
df_filtered.loc[:, df_filtered.columns[4]] = pd.to_numeric(df_filtered[df_filtered.columns[4]], errors='coerce')

def top_n_with_ties(group, col_index, n=5, ascending=True):
    """
    对分组数据取前n条，同时保留出现相同值的所有行
    """
    group_sorted = group.sort_values(by=group.columns[col_index], ascending=ascending)
    if len(group_sorted) <= n:
        return group_sorted
    threshold_value = group_sorted.iloc[n-1, col_index]
    return group_sorted[group_sorted.iloc[:, col_index].apply(
        lambda x: x >= threshold_value if not ascending else x <= threshold_value
    )]

# 遍历每个分组，分别取第10列降序和第5列升序前5条（含相同值）
groups = []
for _, group in df_filtered.groupby(df_filtered.columns[0]):
    top_col10 = top_n_with_ties(group, col_index=9, n=5, ascending=False)
    top_col5 = top_n_with_ties(group, col_index=4, n=5, ascending=True)
    combined = pd.concat([top_col10, top_col5])
    groups.append(combined)

# 合并所有分组结果并去重
final_result = pd.concat(groups).drop_duplicates()

# 保存结果
final_result.to_csv('filtered_top5_with_ties.csv', index=False)
print('筛选完成，结果已保存为 filtered_top5_with_ties.csv')