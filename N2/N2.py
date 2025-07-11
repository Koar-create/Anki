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
    available_records = sorted(
        glob.glob(  os.path.join(current_path, 'N2*.txt')  ) +  glob.glob(  os.path.join(current_path, 'N2*.csv')  )
        )
    for item in available_records:
        print(os.path.basename(item))
    # Read the prompt from input
    date = input(f"{yellow}Enter the date (example: 2025-05-09 or 05-09): {reset}")
    date = pd.to_datetime(date) if len(date) == 10 else (pd.to_datetime(f'2025-{date}') if len(date) == 5 else None)
    # Read the record
    fpath = glob.glob(  os.path.join( current_path, f"N2.{date.strftime('%m-%d')}*.txt" )  )
    if len(fpath) != 0:
        fpath = fpath[0]
        ftype = 'txt'
    else:
        fpath = glob.glob(  os.path.join( current_path, f"N2.{date.strftime('%m-%d')}*.csv" )  )[0]
        ftype = 'csv'
    
    
    ''' ###############################
    When file is text:
    ############################### '''
    if ftype == 'txt':
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
        
        # generate the split character here
        split_character = chr(int('3000', 16)) + chr(int('30FC', 16)) + chr(int('3000', 16))
        
        for list_tmp in section_list:
            # print the introductional word
            print( purple, list_tmp[0], reset )
            if list_tmp[0] == '# 第二順位：組合動詞':
                prompt = "Show next term? (y or [n]): "
                o_next_default = 'n'
            else:
                prompt = "Show next term? ([y] or n): "
                o_next_default = 'y'
            
            # ...
            len_list_tmp = len(list_tmp) - 1
            for order, term in enumerate(random.sample(list_tmp[1:], len(list_tmp[1:]))):
                if split_character in term:
                    terms = term.split(split_character)
                    for i, terM in enumerate(terms):
                        if i == 0:
                            print( f"({order+1}/{len_list_tmp}) {terM}", end='\t' )
                        else:
                            o_next = input( f"{green_b}{prompt}{reset}" )
                            if len(o_next) == 0: o_next = o_next_default
                            if o_next == 'y':
                                print(terM, end='\t')
                    print( '\n' )
                else:
                    print( f"({order+1}/{len_list_tmp}) {term}" )
                    input("")
                    
            print( purple_b + '-' * 40 + '\n' + reset )
        
        print( green_b, 'Review Done.', reset )
    
    
    ''' ###############################
    When file is csv:
    ############################### '''
    if ftype == 'csv':
        fname = os.path.basename(fpath)
        flag_archive = fpath.split( os.sep )[-2] == 'Archived'
        round = int( fname.split( '(' )[1].split( '.' )[0] )
        if not flag_archive:
            sub_round = int( fname.split( '(' )[1].split( '.' )[1][0] )
        else:
            sub_round = 2
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
            if (section == '# 第二順位：組合動詞') or (round > 1 and sub_round > 1):
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
                
                for k, element in enumerate(list_tmp):
                    # ........
                    if element == list_tmp[0]:
                        print(f"{yellow}({i+1}/{len_df}){reset} {element}", end='')
                        continue
                    if len(list_tmp) > 1:
                        if k > 1 and o_next_default == 'n':
                            continue
                    # ........
                    o_next = input(f"{green_b}{prompt}{reset}")
                    o_next = o_next_default if len(o_next) == 0 else o_next
                    o_next = True if o_next == 'y' else False
                    if o_next:
                        print(element, end='')
                    else:
                        continue
                print()  # input('')
        print( green_b, 'Review Done.', reset )
    