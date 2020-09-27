# Big contest

---------------------

* 활용데이터 set
1. (유동인구[SKTelecom], 카드매출[신한], SNS[와이즈넛], 유통[GS retail], 물류[CJ])
2. 네이버 기사
3. 코로나19 확진자 수

Link : https://drive.google.com/drive/folders/16281I0YEhxgmtqCeuucojg5keX3BfIW9?usp=sharing


## 최종 목표
> 1. 다음 기간 매출 예측
> 2. 오프라인 매장 위기 극복 방안 제시
<br/><br/>
### 프로젝트 순서

<br/>

**1. 필요 데이터 선정 및 수집(2019.02.01 ~ 2020.05.31)**

| 신한카드 매출 데이터(내.외국인) | 네이버 뉴스(사회, 경제, 문화) | 코로나19 확진자 수 |
|:----------:|:----------:|:----------:|
| 업종별 매출액 | 자연어 데이터 | 시계열 데이터 |
| 카테고리별 226일 | 372,384개 | 2020년 114일 |

<br/>

**2. 분석 업종 선정 및 텍스트 전처리**

* 업종분류

| 업종코드 | 분류 |
|:----------:|:----------:|
| 10 | 숙박 |
| 20 | 레저용품 |
| 30, 32 | 가구, 주방용구 |
| 35, 52 | 가전, 사무통신 |
| 40 | 유통업 |
| 42 | 의복 |
| 44 | 신변잡화 |
| 80 | 요식업소 |
| 81 | 음료식품 |

<br/>

* 텍스트 전처리

```
data_preprocessing/News_Labeling.ipynb
```

<br/>

**3. 데이터 분석**

* 텍스트 분석

> BERTClassification 을 활용한 뉴스 텍스트 Tone 분석

**Test ACC : 0.70898**
```
data_analysis/News_Classification_KoBERT.ipynb
```

<br/>

* 텍스트 분석 시각화

```
estimation/News_Estimation.ipynb.ipynb
```

<br/>

* 시계열 분석

> XGBoost Ensemble를 활용한 향후 매출액 예측

**MAPE : 0.1133**
```
data_analysis/XGBoost_baseline.ipynb
```
