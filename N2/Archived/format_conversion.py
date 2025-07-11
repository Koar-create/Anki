# load modules
import os
import glob, numpy as np, pandas as pd, random
from collections import Counter

green_b  = "\033[1;32m"
purple_b = "\033[1;35m"
yellow   = "\033[33m"
blue     = "\033[34m"
purple   = "\033[35m"
gray     = "\033[90m"
reset    = "\033[0m"

if __name__ == '__main__':
    fname_src_tag = input(f"{yellow}Input the file to be converted: {reset}")
    root_path = 'D:\\Documents\\Anki'
    fpath_src = sorted( glob.glob( f"{root_path}\\N2\\N2.{fname_src_tag}*.txt" ) + glob.glob( f"{root_path}\\N2\\Archived\\N2.{fname_src_tag}*.txt" ) )
    if fpath_src != []:
        fpath_src = fpath_src[0]
    
    fpath = os.path.dirname(fpath_src)
    fname_src = os.path.basename(fpath_src)
    fname_tgt = fname_src.replace('.txt', '.csv')
    
    with open( fpath_src, 'r' ) as f:
        lines = [line.strip().replace(' (see further)', '').replace('= ', '').split('\u3000ー\u3000') for line in f.readlines()]
    A = np.full((len(lines), 3), np.nan).astype(str)
    df = pd.DataFrame(A, columns=[0, 1, 2]).replace('nan', '')
    
    for i, line in enumerate(lines):
        for j, term in enumerate(line):
            df.loc[i, j] = term
    
    df.to_csv(f"{fpath}\\{fname_tgt}", encoding='utf-8', index=False, header=False)
    print(f"{green_b}Successfully convert{fpath_src} to {fname_tgt}!{reset}")
    