# load modules
import os, sys
import glob, numpy as np, pandas as pd, random
from collections import Counter

def attach_section_tag(df):
    df = df[~pd.isna(df['A'])].reset_index(drop=True)
    indexList = df[df['A'].str.startswith('#')].index
    sectionList = df[df['A'].str.startswith('#')]['A'].values.tolist()
    for i, idx in enumerate(indexList):
        if i == 0:
            df.loc[1:indexList[1]-1, 'D'] = df.loc[idx, 'A']
        elif i == len(indexList)-1:
            df.loc[idx+1:, 'D'] = df.loc[idx, 'A']
        else:
            df.loc[idx+1:indexList[i+1]-1, 'D'] = df.loc[idx, 'A']
    df = df[~df['A'].str.startswith('#')].reset_index(drop=True)
    return df

red      = "\033[31m"
green_b  = "\033[1;32m"
purple_b = "\033[1;35m"
yellow   = "\033[33m"
blue     = "\033[34m"
purple   = "\033[35m"
gray     = "\033[90m"
reset    = "\033[0m"


if __name__ == '__main__':
    current_path = os.getcwd()
    if current_path.split(os.sep)[-1] != 'Archived': print(red, 'excute this script in archived folder, exit now.', reset); sys.exit()
    
    dfList = []
    fpathList = sorted( glob.glob(f"{current_path}\\*.csv") )
    date_now = pd.Timestamp.now().strftime('%Y-%m-%d')
    fpathList = [fpath for fpath in fpathList if f'Next Time：{date_now}' in fpath]
    for fpath in fpathList:
        print(os.path.basename(fpath))
    
    for fpath in fpathList:
        df_tmp = pd.read_csv(fpath, names=['A', 'B', 'C'])
        df_tmp = attach_section_tag(df_tmp)
        dfList.append(df_tmp)
    
    df = pd.concat(dfList, axis=0).reset_index(drop=True)
    df = df[~np.isin(df['D'], ['# 第二順位：組合動詞', '# 第六順位：words with sequential voicing (Rendaku) phenomena'])].reset_index(drop=True)
    
    df_filtered = df[df['D'] == '# 第一順位：識字'].reset_index(drop=True)
    len_df = len(df_filtered)
    indices_rnd = np.random.permutation(len_df)
    for i, idx in enumerate(indices_rnd):
        # print(purple, df.loc[i, 'D'], reset)
        if '＊' in df_filtered.loc[idx, 'A']:
            prompt = "Show next term? ([y] or n): "
            o_next_default = 'y'
        else:
            prompt = "Show next term? (y or [n]): "
            o_next_default = 'n'
        list_tmp = df_filtered.loc[idx, ['A', 'B', 'C']].tolist()
        
        for _ in range(2):
            if np.nan in list_tmp: list_tmp.remove(np.nan)
        
        for j, element in enumerate(list_tmp):
            # ........
            if element == list_tmp[0]:
                print(f"{yellow}({i+1}/{len_df}){purple} {df_filtered.loc[idx, 'D']}{reset}")
                print(f"\t{element}", end='')
                continue
            if len(list_tmp) > 1:
                if j > 1 and o_next_default == 'n':
                    continue
            # ........
            o_next = input(f"{green_b}{prompt}{reset}")
            o_next = o_next_default if len(o_next) == 0 else o_next
            o_next = True if o_next == 'y' else False
            if o_next:
                print(element, end='')
            else:
                continue
        if len(list_tmp) == 1:
            input('')
        else:
            print()  # input('')
    
    df_filtered = df[df['D'] != '# 第一順位：識字'].reset_index(drop=True)
    len_df = len(df_filtered)
    indices_rnd = np.random.permutation(len_df)
    for i, idx in enumerate(indices_rnd):
        # print(purple, df.loc[i, 'D'], reset)
        if '＊' in df_filtered.loc[idx, 'A']:
            prompt = "Show next term? ([y] or n): "
            o_next_default = 'y'
        else:
            prompt = "Show next term? (y or [n]): "
            o_next_default = 'n'
        list_tmp = df_filtered.loc[idx, ['A', 'B', 'C']].tolist()
        
        for _ in range(2):
            if np.nan in list_tmp: list_tmp.remove(np.nan)
        
        for j, element in enumerate(list_tmp):
            # ........
            if element == list_tmp[0]:
                print(f"{yellow}({i+1}/{len_df}){red} {df_filtered.loc[idx, 'D']}{reset}")
                print(f"\t{element}", end='')
                continue
            if len(list_tmp) > 1:
                if j > 1 and o_next_default == 'n':
                    continue
            # ........
            o_next = input(f"{green_b}{prompt}{reset}")
            o_next = o_next_default if len(o_next) == 0 else o_next
            o_next = True if o_next == 'y' else False
            if o_next:
                print(element, end='')
            else:
                continue
        if len(list_tmp) == 1:
            input('')
        else:
            print()  # input('')

    print( green_b, 'Review Done.', reset )
