# load modules
import os
import glob, numpy as np, pandas as pd, random

green_b  = "\033[1;32m"
purple_b = "\033[1;35m"
yellow   = "\033[33m"
purple   = "\033[35m"
reset    = "\033[0m"

if __name__ == '__main__':
    # List the available records (in .txt format)
    current_path = os.getcwd()
    available_records = sorted(  glob.glob(  os.path.join(current_path, 'N1*.csv')  )  )
    for item in available_records:
        print(os.path.basename(item))
    # Read the prompt from input
    number = input(f"{yellow}Enter the unit (example: 1, 2, 3, etc.): {reset}")
    number = int(number)
    # Read the record
    fpath = glob.glob(  os.path.join( current_path, f"N1.Unit{number}.*.csv" )  )[0]
    ftype = 'csv'
    
    
    ''' ###############################
    When file is csv:
    ############################### '''
    if ftype == 'csv':
        df = pd.read_csv(fpath, names=['A', 'B', 'C'])
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
        for section in sectionList:
            print(purple, section, reset)
            if section == '# 第二順位：組合動詞':
                prompt = "Show next term? (y or [n]): "
                o_next_default = 'n'
            else:
                prompt = "Show next term? ([y] or n): "
                o_next_default = 'y'
            df_filtered = df[df['D'] == section].reset_index(drop=True)
            len_df = len(df_filtered)
            indices_rnd = np.random.permutation(len_df)
            for i, idx in enumerate(indices_rnd):
                list_tmp = df_filtered.loc[idx, ['A', 'B', 'C']].tolist()
                
                for _ in range(2):
                    if np.nan in list_tmp: list_tmp.remove(np.nan)
                
                for element in list_tmp:
                    # ........
                    if element == list_tmp[0]:
                        print(f"{yellow}({i+1}/{len_df}){reset} {element}", end='')
                        continue
                    # ........
                    o_next = input(f"{green_b}{prompt}{reset}")
                    o_next = o_next_default if len(o_next) == 0 else o_next
                    o_next = True if o_next == 'y' else False
                    if o_next:
                        print(element, end='')
                    else:
                        continue
                input('')
        print( green_b, 'Review Done.', reset )