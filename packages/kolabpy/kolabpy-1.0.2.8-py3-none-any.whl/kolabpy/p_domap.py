#df(데이터프레임), rv(지역변수, string), dt(분석변수, string)
def p_domap(df, rv, dt, label):
  import geopandas as gpd
  import pandas as pd
  import folium
  import os
  sigungu_geo = 'https://drive.google.com/uc?export=download&id=1lbYoieCkDHljHA6tFFYi2ZRmpFbm_vml'
  df_sigungu_geo = gpd.read_file(sigungu_geo) # 시도/시군구명, geocode, polygon 정보를 담고 있는 geojson 파일을 데이터프레임으로 바꾸어라
  df['SIGUNGU_CD'] = df[rv].apply(str) # sasdataset의 지역변수를 string으로 바꾸어 SAS 데이터프레임의 SIGUNGU_CD 변수로 저장한다
  df_sigungu_merged = df_sigungu_geo.merge(df, on='SIGUNGU_CD') # SAS의 SIGUNGU_CD 데이터셋과 GEOJSON을 데이터프레임으로 변환한 자료를 결합하라(이를 통해 폴리곤 정보가 들어가게 됨)
  df_sigungu_merged['tv']= df_sigungu_merged['SIGUNGU_CD'].str.slice(0, 2) #지역코드(SIGUNGU_CD) 앞 2자리를 자르라
  df_sigungu_merged['nv']= df_sigungu_merged['SIGUNGU_CD'].str.len() #지역코드(SIGUNGU_CD) 문자열의 개수를 반환하라(5 또는 2의 값을 가짐)
  try :
    if df_sigungu_merged.duplicated(['tv', 'year'], keep=False).value_counts()[1] > 0 : # 지역코드 앞 두자리와 연도변수를 종합적으로 고려했을 때 중복의 개수가 0보다 많으면 True, 없으면 KeyError를 반환
      # 데이터셋에서 (중복 관측점 & 지역코드 문자열이 2개를 초과하는 관측점; 이는 시도자료를 제외하고 시군구 자료를 확보하기 위함) OR 중복이 없는 관측점(세종과 제주를 포함하기 위함)
      df_sigungu_merged = df_sigungu_merged[((df_sigungu_merged.duplicated(['tv', 'year'], keep=False)) & (df_sigungu_merged['nv']>2)) | (df_sigungu_merged.duplicated(['tv', 'year'], keep=False)==0)].copy()
  except : # KeyError, IndexError 오류 무시하라(시도 데이터셋인 경우 if문 다음에 바로 여기로 옴)
    pass
  df_sigungu_merged[['SIGUNGU_CD', 'SIGUNGU_NM', 'geometry']].to_file("a.json", driver='GeoJSON') # merge 데이터셋에서 geocode 데이터셋을 a.json으로 저장하라
  m = folium.Map(location=[36, 128], width=800, height=800, tiles="OpenStreetMap", zoom_start=7)
  folium.Choropleth(geo_data="a.json", data=df_sigungu_merged, columns=['SIGUNGU_CD', dt],key_on='feature.properties.SIGUNGU_CD',fill_color='YlOrRd',fill_opacity=0.7,line_opacity=0.5,legend_name=label).add_to(m)
  style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity': 0.1, 'weight': 0.1}
  highlight_function = lambda x: {'fillColor': '#000000','color':'#000000', 'fillOpacity': 0.50, 'weight': 0.1}
  LABEL = folium.features.GeoJson(df_sigungu_merged, style_function=style_function, control=False, highlight_function=highlight_function, 
                                  tooltip=folium.features.GeoJsonTooltip(fields=['SIGUNGU_NM', 'year', dt],aliases=['지역: ', '연도: ', label],style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
  m.add_child(LABEL)
  m.keep_in_front(LABEL)
  folium.LayerControl().add_to(m)
  os.remove("a.json") # a.json을 삭제하라
  return m