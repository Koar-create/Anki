import os, sys
sys.path.append('utils')
from common import *


if __name__ == '__main__':
    date_now = pd.Timestamp.now().strftime('%Y-%m-%d')
    date_tomor = (pd.Timestamp.now()+np.timedelta64(1, 'D')).strftime('%Y-%m-%d')
    print_record( date_tomor )
    fnameList = sorted(glob.glob( '*.txt' ) + glob.glob( 'Archived' + os.sep + '*.txt' ) + glob.glob( 'N2' + os.sep + '*.txt' ) + glob.glob( 'N2' + os.sep + 'Archived' + os.sep + '*.txt' ) + \
                       glob.glob( '*.csv' ) + glob.glob( 'Archived' + os.sep + '*.csv' ) + glob.glob( 'N2' + os.sep + '*.csv' ) + glob.glob( 'N2' + os.sep + 'Archived' + os.sep + '*.csv' ) + \
                       glob.glob( 'N1' + os.sep + '*.txt' ) + glob.glob( 'N1' + os.sep + '*.csv' ) + glob.glob( 'N1' + os.sep + 'Archived' + os.sep + '*.txt' ) + glob.glob( 'N1' + os.sep + 'Archived' + os.sep + '*.csv' ))
    
    # screening
    fnameList = [fname for fname in fnameList if date_tomor in fname]
    
    fnameList_EN = [fname for fname in fnameList if ('N2' not in fname) and ('N1' not in fname)]
    fnameList_JA = [fname for fname in fnameList if ('N2'     in fname) or  ('N1'     in fname)]
    
    print(f"{purple}These records should be reviewed today: {reset}")
    print(f"{blue}English: {reset}")
    for fname in fnameList_EN:
        print(green, '\t', fname, reset)
    print(f"{blue}Japanese: {reset}")
    for fname in fnameList_JA:
        print(green, '\t', fname, reset)
    