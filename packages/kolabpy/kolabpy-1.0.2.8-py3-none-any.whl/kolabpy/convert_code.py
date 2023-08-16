def convert_code(df):
 import pandas as pd
 pd.set_option('mode.chained_assignment',  None)
 name = pd.read_csv('https://drive.google.com/uc?export=download&id=1dgXL5NVgt6Xb52j3K5ROTnctvir-c7Qs', encoding='utf-8') #지역명이 중복되지 않는 지역 목록
 df_sorted = df.sort_values(["C1", "C1_NM"], ascending = (True, True)) #시도명, 시군구명 오름차순 정렬
 df_name = df_sorted.merge(name, on='C1_NM', how='left') 
 df_name['Counter'] = df_name.groupby('C1_NM').cumcount()+1
 df_sigungu = df_name

 for n in df_sigungu.index: #지역명이 중복되는 지역은 따로 입력
 
  if df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '서울특별시 중구'
  elif df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '부산광역시 중구'
  elif df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 3:
            df_sigungu['FULL_NM'][n] = '대구광역시 중구'
  elif df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 4:
            df_sigungu['FULL_NM'][n] = '인천광역시 중구'
  elif df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 5:
            df_sigungu['FULL_NM'][n] = '대전광역시 중구'
  elif df_sigungu['C1_NM'][n] == '중구' and df_sigungu['Counter'][n] == 6:
            df_sigungu['FULL_NM'][n] = '울산광역시 중구'
            
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '부산광역시 동구'
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '대구광역시 동구'
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 3:
            df_sigungu['FULL_NM'][n] = '인천광역시 동구'
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 4:
            df_sigungu['FULL_NM'][n] = '광주광역시 동구'
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 5:
            df_sigungu['FULL_NM'][n] = '대전광역시 동구'
  elif df_sigungu['C1_NM'][n] == '동구' and df_sigungu['Counter'][n] == 6:
            df_sigungu['FULL_NM'][n] = '울산광역시 동구'

  elif df_sigungu['C1_NM'][n] == '남구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '부산광역시 남구'
  elif df_sigungu['C1_NM'][n] == '남구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '대구광역시 남구'
  elif df_sigungu['C1_NM'][n] == '남구' and df_sigungu['Counter'][n] == 3:
            df_sigungu['FULL_NM'][n] = '광주광역시 남구'
  elif df_sigungu['C1_NM'][n] == '남구' and df_sigungu['Counter'][n] == 4:
            df_sigungu['FULL_NM'][n] = '울산광역시 남구'
  elif df_sigungu['C1_NM'][n] == '남구' and df_sigungu['Counter'][n] == 5:
            df_sigungu['FULL_NM'][n] = '경상북도 포항시 남구'

  elif df_sigungu['C1_NM'][n] == '서구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '부산광역시 서구'
  elif df_sigungu['C1_NM'][n] == '서구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '대구광역시 서구'
  elif df_sigungu['C1_NM'][n] == '서구' and df_sigungu['Counter'][n] == 3:
            df_sigungu['FULL_NM'][n] = '인천광역시 서구'
  elif df_sigungu['C1_NM'][n] == '서구' and df_sigungu['Counter'][n] == 4:
            df_sigungu['FULL_NM'][n] = '광주광역시 서구'
  elif df_sigungu['C1_NM'][n] == '서구' and df_sigungu['Counter'][n] == 5:
            df_sigungu['FULL_NM'][n] = '대전광역시 서구'

  elif df_sigungu['C1_NM'][n] == '북구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '부산광역시 북구'
  elif df_sigungu['C1_NM'][n] == '북구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '대구광역시 북구'
  elif df_sigungu['C1_NM'][n] == '북구' and df_sigungu['Counter'][n] == 3:
            df_sigungu['FULL_NM'][n] = '광주광역시 북구'
  elif df_sigungu['C1_NM'][n] == '북구' and df_sigungu['Counter'][n] == 4:
            df_sigungu['FULL_NM'][n] = '울산광역시 북구'
  elif df_sigungu['C1_NM'][n] == '북구' and df_sigungu['Counter'][n] == 5:
            df_sigungu['FULL_NM'][n] = '경상북도 포항시 북구'            

  elif df_sigungu['C1_NM'][n] == '강서구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '서울특별시 강서구'
  elif df_sigungu['C1_NM'][n] == '강서구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '부산광역시 강서구'

  elif df_sigungu['C1_NM'][n] == '강서구' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '서울특별시 강서구'
  elif df_sigungu['C1_NM'][n] == '강서구' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '부산광역시 강서구'

  elif df_sigungu['C1_NM'][n] == '고성군' and df_sigungu['Counter'][n] == 1:
            df_sigungu['FULL_NM'][n] = '강원도 고성군'
  elif df_sigungu['C1_NM'][n] == '고성군' and df_sigungu['Counter'][n] == 2:
            df_sigungu['FULL_NM'][n] = '경상남도 고성군'

  else:
            df_sigungu['FULL_NM'][n] = df_sigungu['FULL_NM'][n]
 
 code = pd.read_csv('https://drive.google.com/uc?export=download&id=1Qk77GoEfJsnHMRqQk38O9rfKbuExtHga', encoding='utf-8') #한국행정구역분류(2021.12.31)
 df_sigungu_code = df_sigungu.merge(code, on='FULL_NM', how='left')
 df_sigungu_code.dropna()
 df_sigungu_code['STAT_CODE'] = df_sigungu_code['STAT_CODE'].astype(str).replace('\.0', '', regex=True)
 df_sigungu_code['ADM_CODE'] = df_sigungu_code['ADM_CODE'].astype(str).replace('\.0', '', regex=True)
 df_sigungu_code['LAW_CODE'] = df_sigungu_code['LAW_CODE'].astype(str).replace('\.0', '', regex=True)
 
 df_sigungu_code_index = df_sigungu_code.drop(['Counter'], axis = 1)
 return df_sigungu_code_index