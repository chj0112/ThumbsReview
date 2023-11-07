import pandas as pd
import numpy as np
import re
from konlpy.tag import Okt
from tqdm.notebook import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from keras.models import load_model
import pickle

def Our_model(data_path):
    model = load_model('modules/mdl_1029.h5')
    model.summary()
    with open('modules/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    tk = tokenizer

    test = pd.read_csv(data_path, index_col=0, sep='\t', encoding='utf-8')
    test = test.reset_index(drop = True)
    test['review'] = test.review.map(lambda x: re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', x))
    test['review'] = test.review.map(lambda x: re.sub('\s{2,}', ' ', x))

    tagger = Okt()
    test_data = []

    s_w = set(['은', '는', '이', '가', '를', '들', '에게', '의', '을', '도', '으로', '만', '라서', '하다',
            '아', '로', '저', '즉', '곧', '제', '좀', '참', '응', '그', '딱', '어', '네', '예', '게', '고',
            '하', '에', '한', '어요', '것', '았', '네요', '듯', '같', '나', '있', '었', '지', '하고', '먹다',
            '습니다', '기', '시', '과', '수', '먹', '와', '적', '보', '에서', '곳', '너무', '정말', '진짜',
            '있다', '다', '더', '인', '집', '면', '내', '라', '원', '요', '또', '하나', '전', '거', '엔',
            '이다', '되다', '까지', '인데', '정도', '나오다', '주문', '시키다'])

    for i in tqdm(test['review']):
        tk_d = tagger.morphs(i, stem=True)  # clean_X의 형태소 추출
        tk_d = [w for w in tk_d if w not in s_w] # 불용어 제거
        test_data.append(' '.join(tk_d)) # 공백을 기준으로 문자열로 조인

    X_t = tk.texts_to_sequences(test_data)
    X_t = pad_sequences(X_t, maxlen=20)
    X_t = np.array(X_t)

    predict_result = np.array(list(map(lambda x: np.round(x, 0),model.predict(X_t))))
    result = pd.DataFrame(predict_result, columns = ['tastereview', 'tastep_or_n', 'servicereview', 'servicep_or_n'])
    test = pd.read_csv(data_path, index_col=0, sep='\t', encoding='utf-8')
    result.insert(0,'review', value = test['review'], allow_duplicates=False)
    result.to_csv('modules/output.tsv',  sep='\t',encoding = 'utf-8')
    # print(result)
    # return 'success'
    # return result

# if __name__ == '__main__':
#     predict_result = Our_model('test_data.tsv').to_numpy()
#     test = pd.read_csv('test_data.tsv', index_col=0,sep='\t', encoding='utf-8')
#     answer = test[['tastereveiw', 'tastep_or_n', 'servicereview', 'servicep_or_n']]
#     answer = answer.to_numpy()
    
#     cnt = 0
#     for i in range(len(answer)):
#         if predict_result[i][1] == answer[i][0]:
#             cnt += 1
#     print('tastereview : ', cnt / len(answer) * 100)
    
#     # tastep_or_n
#     cnt = 0
#     for i in range(len(answer)):
#         if predict_result[i][2] == answer[i][1]:
#             cnt += 1
#     print('tastep_or_n : ', cnt / len(answer) * 100)
    
#     # servicereview
#     cnt = 0
#     for i in range(len(answer)):
#         if predict_result[i][3] == answer[i][2]:
#             cnt += 1
#     print('servicereview : ', cnt / len(answer) * 100)
    
#     # servicep_or_n
#     cnt = 0
#     for i in range(len(answer)):
#         if predict_result[i][4] == answer[i][3]:
#             cnt += 1
#     print('servicep_or_n : ', cnt / len(answer) * 100)
    
    # -----------------------------------------------------------------------------------------------
    
    
# import pandas as pd
# import numpy as np
# import re
# from konlpy.tag import Okt
# from tqdm.notebook import tqdm
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from sklearn.model_selection import train_test_split

# from tensorflow.keras.models import Sequential
# from tensorflow.keras import layers
# from tensorflow.keras.callbacks import EarlyStopping
# from keras.models import load_model
# import pickle

# def Our_model(data_path):
#     model = load_model('mdl_1029.h5')
#     model.summary()
#     with open('tokenizer.pickle', 'rb') as handle:
#         tokenizer = pickle.load(handle)
#     tk = tokenizer

#     test = pd.read_csv(data_path, index_col=0)
#     test = test.reset_index(drop = True)
#     test['review'] = test.review.map(lambda x: re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', x))
#     test['review'] = test.review.map(lambda x: re.sub('\s{2,}', ' ', x))

#     tagger = Okt()
#     test_data = []

#     s_w = set(['은', '는', '이', '가', '를', '들', '에게', '의', '을', '도', '으로', '만', '라서', '하다',
#             '아', '로', '저', '즉', '곧', '제', '좀', '참', '응', '그', '딱', '어', '네', '예', '게', '고',
#             '하', '에', '한', '어요', '것', '았', '네요', '듯', '같', '나', '있', '었', '지', '하고', '먹다',
#             '습니다', '기', '시', '과', '수', '먹', '와', '적', '보', '에서', '곳', '너무', '정말', '진짜',
#             '있다', '다', '더', '인', '집', '면', '내', '라', '원', '요', '또', '하나', '전', '거', '엔',
#             '이다', '되다', '까지', '인데', '정도', '나오다', '주문', '시키다'])

#     for i in tqdm(test['review']):
#         tk_d = tagger.morphs(i, stem=True)  # clean_X의 형태소 추출
#         tk_d = [w for w in tk_d if w not in s_w] # 불용어 제거
#         test_data.append(' '.join(tk_d)) # 공백을 기준으로 문자열로 조인

#     X_t = tk.texts_to_sequences(test_data)
#     X_t = pad_sequences(X_t, maxlen=20)
#     X_t = np.array(X_t)

#     predict_result = np.array(list(map(lambda x: np.round(x, 0),model.predict(X_t))))
#     result = pd.DataFrame(predict_result, columns = ['tastereview', 'tastep_or_n', 'servicereview', 'servicep_or_n'])
#     test = pd.read_csv(data_path, index_col=0)
#     result.insert(0,'review', value = test['review'], allow_duplicates=False)
#     result.to_csv('result_2.csv', encoding = 'utf-8-sig')
#     # print(result)
#     # return 'success'
#     # return result

# # if __name__ == '__main__':
# #     predict_result = Our_model('test_data.csv').to_numpy()
# #     test = pd.read_csv('test_data.csv', index_col=0)
# #     answer = test[['tastereveiw', 'tastep_or_n', 'servicereview', 'servicep_or_n']]
# #     answer = answer.to_numpy()
    
# #     cnt = 0
# #     for i in range(len(answer)):
# #         if predict_result[i][1] == answer[i][0]:
# #             cnt += 1
# #     print('tastereview : ', cnt / len(answer) * 100)
    
# #     # tastep_or_n
# #     cnt = 0
# #     for i in range(len(answer)):
# #         if predict_result[i][2] == answer[i][1]:
# #             cnt += 1
# #     print('tastep_or_n : ', cnt / len(answer) * 100)
    
# #     # servicereview
# #     cnt = 0
# #     for i in range(len(answer)):
# #         if predict_result[i][3] == answer[i][2]:
# #             cnt += 1
# #     print('servicereview : ', cnt / len(answer) * 100)
    
# #     # servicep_or_n
# #     cnt = 0
# #     for i in range(len(answer)):
# #         if predict_result[i][4] == answer[i][3]:
# #             cnt += 1
# #     print('servicep_or_n : ', cnt / len(answer) * 100)
