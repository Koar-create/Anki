# load modules
import os
import glob, numpy as np, pandas as pd, random

green_b  = "\033[1;32m"
purple_b = "\033[1;35m"
yellow   = "\033[33m"
purple   = "\033[35m"
reset    = "\033[0m"

if __name__ == '__main__':
    # ...
    f_des = open('N2.01-01.txt', 'w')
    # List the available records (in .txt format)
    current_path = os.getcwd()
    date_now = pd.Timestamp.now().strftime('%Y-%m-%d')
    available_records = sorted(
        glob.glob(  os.path.join(current_path, f'N2*Next Time：{date_now}*.txt')  )
        )
    large_section_dict = {'# 第一順位：識字': [], 
                          '# 第二順位：組合動詞': [], 
                          '# 第三順位：No Memories': [], 
                          '# 第四順位：Some Memories': [], 
                          '# 第五順位: 外來語': [], 
                          '# 第六順位：words with sequential voicing (Rendaku) phenomena': [], 
                          '# 第七順位（末位）：prefixal/suffixal words': [], }
    for fpath in available_records:
        print(fpath)
        with open(fpath, 'r') as f: lines = f.readlines()
        lines = [line.strip() for line in lines]
        
        splitNodeList = []
        line_index_list = np.arange(len(lines))
        for i in line_index_list:
            if len(lines[i]) == 0:
                splitNodeList.append(i)
        
        section_list = []
        for i, splitNode in enumerate(splitNodeList):
            # (1/3) Append the 1st section
            if splitNode == splitNodeList[0]:
                list_to_be_appended = lines[:splitNode]
                section_list.append(list_to_be_appended)
            else:
                # (2/3) Append the middle sections
                splitNode_last = splitNodeList[i-1]
                list_to_be_appended = lines[splitNode_last+1:splitNode]
                section_list.append(list_to_be_appended)
            # (3/3) Append the last section
            if splitNode == splitNodeList[-1]:
                list_to_be_appended = lines[splitNode+1:]
                section_list.append(list_to_be_appended)
    
        for key, list_tmp in zip(large_section_dict.keys(), section_list):
            list_tmp.remove(list_tmp[0])
            large_section_dict[key] = large_section_dict[key] + list_tmp
    
    for key in large_section_dict.keys():
        f_des.write(key)
        f_des.write('\n')
        for item in large_section_dict[key]:
            f_des.write(item)
            f_des.write('\n')
        f_des.write('\n')
    f_des.close()
    print('Save as N2.01-01.txt')
    