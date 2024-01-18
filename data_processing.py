# 필요한 라이브러리 및 패키지를 불러옵니다.
import pandas as pd
import re
import matplotlib.pyplot as plt


# 원하는 csv파일을 불러옵니다.
df = pd.read_csv('데이터 최종본(완).csv')
pd.set_option('display.max_rows', None)

# 새로운 열 이름을 생성하고 열 이름을 변경합니다.
new_columns = ['강좌명','수강생수','가격','평점','수강평수','난이도','강의시간','강의게시일']
df.columns = new_columns


# 각각의 속성을 원하는 시각화를 위해 형태를 바꿔줍니다. -> 시각화를 위한 데이터프레임을 생성합니다.
df['강좌명'] = df['강좌명'].str.replace('\n대시보드', '')
df['강의게시일'] = pd.to_datetime(df['강의게시일'].str.extract(r'(\d+)년 (\d+)월 (\d+)일').agg('-'.join, axis=1))
df['수강평수'] = df['수강평수'].str.extract(r'(\d+)개의').fillna(0).astype(int)
df['수강생수'] = df['수강생수'].str.replace('명', '')
df['수강생수'] = df['수강생수'].str.replace(',', '').astype(int)
df['가격'] = df['가격'].replace('무료', '₩0')
df['가격'] = df['가격'].str.extract(r'₩([^₩]+)$')
df['가격'] = df['가격'].str.replace(',', '').astype(int)
df['시간'] = df['강의시간'].str.extract(r'(\d+)시간', expand=False).fillna(0)
df['분'] = df['강의시간'].str.extract(r'(\d+)분', expand=False).fillna(0)
df['강의시간(분)'] = df['시간'].astype(int)*60 + df['분'].astype(int)
df = df.drop(['시간', '분', '강의시간'], axis=1)
df['평점'] = df['평점'].str.extract(r'([\d.]+)').fillna(0).astype(float)
df['무료/유료'] = df['가격'].apply(lambda x: '무료' if x == 0 else '유료')
df['평가지수'] = df['수강평수'] * df['평점']
# 중복되는 행을 제거해줍니다.
df = df.drop_duplicates('강좌명', keep='first')
#df.to_csv('데이터 시각화용.csv', index=False)




# 상관 분석을 위한 데이터프레임을 생성합니다.
df_corr = df.copy()
df_corr['난이도'] = df['난이도'].apply(lambda x: 0 if x == '입문자' else (1 if x == '초급자' else 2))
df_corr['유료(1)/무료(0)'] = df['무료/유료'].apply(lambda x: 1 if x == '유료' else 0)
df_corr= df_corr.drop(['무료/유료'], axis=1)
#df_corr.to_csv('데이터 상관관계분석용.csv', index=False)
df_corr




# 회귀 분석을 위한 데이터프레임을 생성합니다.
df_regression = df.copy()
df_regression['입문자여부'] = df['난이도'].apply(lambda x: 1 if x == '입문자' else 0)
df_regression['초급자여부'] = df['난이도'].apply(lambda x: 1 if x == '초급자' else 0)
df_regression['유료(1)/무료(0)'] = df['무료/유료'].apply(lambda x: 1 if x == '유료' else 0)
df_regression= df_regression.drop(['난이도', '무료/유료'], axis=1)
#df_regression.to_csv('데이터 회귀분석용.csv', index=False)
df_regression
