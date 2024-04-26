import os
import json
import shutil

def rename_and_move_file(current_directory, crc_value, new_file_name, file_path):
    # 构建目标文件路径
    target_directory = os.path.join(current_directory, *file_path.split('/')[:-1])
    target_file_path = os.path.join(target_directory, new_file_name)
    
    # 在当前根目录中查找与CRC值匹配的文件
    for filename in os.listdir(current_directory):
        if crc_value in filename:
            old_path = os.path.join(current_directory, filename)
            
            # 移动文件到指定目录
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)  # 创建目录（如果不存在）
            shutil.move(old_path, target_file_path)
            print(f"已重命名并移动文件: {old_path} -> {target_file_path}")
            return True
    
    return False

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 读取JSON文件
with open('./MediaCatalog.json', 'r', encoding='utf-8') as file:
    mediajson = json.load(file)

# 遍历每个条目并重命名文件
for table_name, table_details in mediajson["Table"].items():
    # 检查条目中是否包含路径信息和CRC值
    if "Crc" in table_details:
        crc_value = str(table_details["Crc"])  # 将CRC值转换为字符串
    else:
        print(f"警告: 条目 {table_name} 中缺少'Crc'字段，跳过重命名")
        continue
    
    if "FileName" in table_details:
        new_file_name = table_details["FileName"]
    else:
        print(f"警告: 条目 {table_name} 中缺少'FileName'字段，跳过重命名")
        continue
    
    if "path" in table_details:
        file_path = table_details["path"]
    else:
        print(f"警告: 条目 {table_name} 中缺少'path'字段，无法确定文件目录，跳过移动文件")
        continue
    
    # 重命名并移动文件
    success = rename_and_move_file(current_directory, crc_value, new_file_name, file_path)
    if not success:
        print(f"警告: 条目 {table_name} 中指定的 CRC 值 '{crc_value}' 未在当前根目录中找到对应的文件，跳过重命名")
