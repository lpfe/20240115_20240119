import pandas as pd
import matplotlib.pyplot as plt

# 원하는 데이터를 불러옵니다.
df = pd.read_csv('데이터 최종본(완).csv')

# 데이터 확인을 위한 설정을 변경합니다.
pd.set_option('display.max_rows', None)

# 데이터 인덱스를 설정합니다.
df.index = range(1,2728)

# 새로운 열 이름을 생성합니다
new_columns = ['강좌명','수강생수','가격','평점','난이도','강의시간']
df.columns = new_columns

# 전처리를 위하여 각각의 속성을 분석을 위한 형태로 변경합니다. -> 시각화를 위한 데이터프레임을 생성합니다.
df['강좌명'] = df['강좌명'].str.replace('\n대시보드', '')
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

# 회귀 분석을 위한 데이터프레임을 생성합니다. -> 다중공선성 방지 및 One Hot Encoding
df_regression = df.copy()

df_regression['입문자여부'] = df['난이도'].apply(lambda x: 1 if x == '입문자' else 0)
df_regression['초급자여부'] = df['난이도'].apply(lambda x: 1 if x == '초급자' else 0)
df_regression['유료(1)/무료(0)'] = df['무료/유료'].apply(lambda x: 1 if x == '유료' else 0)

df_regression= df_regression.drop(['난이도', '무료/유료'], axis=1)



#시각화 예시를 한 번 만들어보았습니다. 유/무료 강좌 수 여부를 파이차트로 확인합니다.
import plotly.express as px

# '무료/유료' 열 값의 개수를 세기
count_data = df['무료/유료'].value_counts().reset_index()
count_data.columns = ['무료/유료', '강의 수']

# '무료/유료' 열 값의 비율 계산
count_data['비율'] = count_data['강의 수'] / count_data['강의 수'].sum()

# 파이차트 그리기
fig = px.pie(count_data, values='강의 수', names='무료/유료', title='무료/유료 강의 수 비율')
fig.show()
