# ch06_06_BollingerBand_TrendFollowing.py
import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2023-04-11')

df['MA20'] = df['close'].rolling(window=20).mean() # 20개 종가를 이용해서 평균을 구한다.
df['stddev'] = df['close'].rolling(window=20).std() # 20개 종가를 이용해서 표준편차를 구한 뒤 stddev 칼럼으로 df에 추가한다.
df['upper'] = df['MA20'] + (df['stddev'] * 2) # 중간 볼린저 밴드 + (2 X 표준편차)를 상단 볼린저 밴드로 계산한다.
df['lower'] = df['MA20'] - (df['stddev'] * 2) # 중간 볼린저 밴드 - (2 X 표준편차)를 상단 볼린저 밴드로 계산한다.
df['PB'] = (df['close'] - df['lower'])/(df['upper'] - df['lower']) # (종가 - 하단밴드) / (상단밴드 - 하단밴드)를 구해 %B 칼럼을 생성한다.
df['TP'] = (df['high'] + df['low'] + df['close']) / 3 # 고가, 저가, 종가의 합을 3으로 나눠서 중심 가격 TP(typical price)를 구한다.
df['PMF'] = 0
df['NMF'] = 0
for i in range(len(df.close) - 1): # range 함수는 마지막 값을 포함하지 않으므로 0부터 종가 개수 -2까지 반복한다.
    if df.TP.values[i] < df.TP.values[i+1]:
        # i번째 중심 가격보다 i+1 번째 중심 가격과 i+1 번째 거래량의 곱을 i+1번째 긍정적 현금 흐름 PMF(positive money flow)에 저장한다.
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0 # i+1번째 부정적 현금 흐름 NMF(negative money flow)값은 0으로 저장한다.
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0
 # 10일 동안의 긍정적 현금 흐름의 합을 10일 동안의 부정적 현금 흐름의 합으로 나눈 결과를 현금 흐름 비율 MFR(money flow ratio) 칼럼에 저장한다.
df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
df['MFI10'] = 100 - 100 / (1 + df['MFR']) # 10일 기준으로 현금흐름지수를 계싼한 결과를 MFI10(money flow index 10) 칼럼에 저장한다.
df = df[19:] # 위 내용은 19번째 행까지 NaN이므로 (20개씩 계산) 값이 있는 20번째 행부터 사용한다.

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1) # 기존의 볼린저 밴드 차트를 2행 1열의 그리드에서 1열에 배치한다.
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.plot(df.index, df['close'], color='#0000ff', label='Close') # x좌표 df.index에 해당하는 종가를 y좌표로 설정해 파란색(#0000ff) 실선으로 표시한다.
plt.plot(df.index, df['upper'], 'r--', label='Upper band') # x좌표 df.index에 해당하는 상단 볼린저 밴드값을 y좌표로 설정해 검은 실선(k--)으로 표시한다.
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9') # 상단 볼린저 밴드와 하단 볼린저 밴드 사이를 회색으로 칠한다.
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80: # %b가 0.8보다 크고 10일 기준 MFI가 80보다 크면 (아래 주석)
        # 매수 시점을 나타내기 위해 첫 번째 그래프의 종가 위치에 빨간색 삼각형을 표시한다.
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20: # %b가 0.2보다 작고 10일 기준 MFI가 20보다 작으면 (아래 주석)
        # 매도 시점을 나타내기 위해 첫 번째 그래프의 종가 위치에 파란색 삼각형을 표시한다.
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(2, 1, 2) # %B 차트를 2행 1열의 그리드에서 2열에 배치한다.
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100') # MFI와 비교할 수 있게 %b를 그대로 표시하지 않고 100을 곱해서 푸른색 실선으로 표시한다.
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)') # 10일 기준 MFI를 녹색의 점선으로 표시한다.
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120]) # y축 눈금을 -20부터 120까지 20단위로 표시한다.
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()