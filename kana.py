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
    fpath = glob.glob(  os.path.join( current_path, f"平仮名バッカ.csv" )  )[0]
    ftype = 'csv'
    
    mode = input(f"{green_b}Choose the mode ([fast] or slow): {reset}")
    mode = 'fast' if len(mode) == 0 else mode
    
    ''' ###############################
    When file is csv:
    ############################### '''
    if ftype == 'csv':
        df = pd.read_csv(fpath, index_col=False)
        if mode == 'fast':
            df = df[df['difficulty'].astype(str).str.endswith('2')].reset_index(drop=True)
        df_filtered = df
        len_df = len(df_filtered)
        indices_rnd = np.random.permutation(len_df)
        for i, idx in enumerate(indices_rnd):
            if str(df_filtered.loc[idx, 'difficulty'])[-1] == '1':
                prompt = "Show next term? (y or [n]): "
                o_next_default = 'n'
            else:
                prompt = "Show next term? ([y] or n): "
                o_next_default = 'y'
            list_tmp = df_filtered.loc[idx, ['term', 'sentence']].tolist()
            
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
            # input('')
            print('\n')
    print( green_b, 'Review Done.', reset )