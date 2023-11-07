import test_h5

#print(test_h5.Our_model('self_test.csv'))

import pandas as pd 

if __name__ == '__main__':
    print(test_h5.Our_model('input.tsv'))
    # test2 = pd.read_csv('self_test2.csv', index_col=0)
    # test1 = pd.read_csv('self_test.csv', index_col=0)

    # print(test2['review'].dtypes, test1['review'].dtypes)