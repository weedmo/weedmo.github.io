# 딥러닝 (분류/회귀)


## 강의_3기_AI개론_7차시__Regression_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_7차시__Regression_.ipynb)

# 7장 선형회귀 (Regression analysis)

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    debconf: unable to initialize frontend: Dialog
    debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 78, <> line 4.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Processing triggers for fontconfig (2.13.1-4.2ubuntu5) ...
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 39 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /usr/share/fonts/truetype: skipping, looped directory detected
    /usr/share/fonts/truetype/humor-sans: skipping, looped directory detected
    /usr/share/fonts/truetype/liberation: skipping, looped directory detected
    /usr/share/fonts/truetype/nanum: skipping, looped directory detected
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3
    Successfully installed torchinfo-1.8.0


* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 폰트 관련 용도
import matplotlib.font_manager as fm

# Colab, Linux
# 나눔 고딕 폰트의 경로 명시
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```


```python
# 파이토치 관련 라이브러리
import torch
from torch import nn, optim
import torch.nn.functional as F
from torchviz import make_dot
from torchinfo import summary

# Boston dataset
import pandas  as pd
```


```python
# 기본 폰트 설정
plt.rcParams['font.family'] = font_name

# 기본 폰트 사이즈 변경
plt.rcParams['font.size'] = 14

# 기본 그래프 사이즈 변경
plt.rcParams['figure.figsize'] = (6,6)

# 기본 그리드 표시
# 필요에 따라 설정할 때는, plt.grid()
plt.rcParams['axes.grid'] = True
plt.rcParams["grid.linestyle"] = ":"

# 마이너스 기호 정상 출력
plt.rcParams['axes.unicode_minus'] = False

# 넘파이 부동소수점 자릿수 표시
np.set_printoptions(suppress=True, precision=4)
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')
```

## 단순 선형 회귀 분석

### 입력 :1 출력 :1인 선형 함수


```python
# 난수 시드값 고정
torch.manual_seed(123)

# 입력 :1 출력 :1 선형 함수의 정의
l1 = nn.Linear(1, 1)

# 선형 함수 확인
print(l1)
# print(list(l1.parameters()))
print(list(l1.named_parameters()))
```

    Linear(in_features=1, out_features=1, bias=True)
    [('weight', Parameter containing:
    tensor([[-0.4078]], requires_grad=True)), ('bias', Parameter containing:
    tensor([0.0331], requires_grad=True))]



```python
### Check named parameters
name, tensor = list(l1.named_parameters())[0]
print(name, tensor[0], tensor[0].shape)
```

    weight tensor([-0.4078], grad_fn=<SelectBackward0>) torch.Size([1])



```python
# 파라미터명, 파라미터 값, shape 표시

for param in l1.named_parameters():
    print('name: ', param[0])
    print('tensor: ', param[1])
    print('shape: ', param[1].shape)
    print("="*50)
```

    name:  weight
    tensor:  Parameter containing:
    tensor([[-0.4078]], requires_grad=True)
    shape:  torch.Size([1, 1])
    ==================================================
    name:  bias
    tensor:  Parameter containing:
    tensor([0.0331], requires_grad=True)
    shape:  torch.Size([1])
    ==================================================



```python
# 초깃값 설정
nn.init.constant_(l1.weight, 2.0)
nn.init.constant_(l1.bias, 1.0)

# 결과 확인
print(l1.weight)
print(l1.bias)
```

    Parameter containing:
    tensor([[2.]], requires_grad=True)
    Parameter containing:
    tensor([1.], requires_grad=True)



```python
# 테스트용 데이터 생성

# x_np를 넘파이 배열로 정의
x_np = np.arange(-2, 2.1, 1) # float64

# 텐서 변수화
x = torch.tensor(x_np) # float32
print("x = \n", x)

# (N,1) 사이즈로 변경
x = x.view(-1,1)
print("x.view(-1,1) = \n", x)

# 결과 확인
print(x.shape)
print(x)
```

    x = 
     tensor([-2., -1.,  0.,  1.,  2.], dtype=torch.float64)
    x.view(-1,1) = 
     tensor([[-2.],
            [-1.],
            [ 0.],
            [ 1.],
            [ 2.]], dtype=torch.float64)
    torch.Size([5, 1])
    tensor([[-2.],
            [-1.],
            [ 0.],
            [ 1.],
            [ 2.]], dtype=torch.float64)


### 입력 :2 개 출력 :1인 선형 함수


```python
# 입력 :2, 출력:1 선형 함수 정의
l2 = nn.Linear(2, 1)
print("Initial weights and bias", "="*50)
print(l2.weight)
print(l2.bias)
print()

# 초깃값 설정
print("constant weights and bias", "="*50)
nn.init.constant_(l2.weight, 1.0)
nn.init.constant_(l2.bias, 2.0)

# 결과 확인
print(l2.weight)
print(l2.bias)
```

    Initial weights and bias ==================================================
    Parameter containing:
    tensor([[-0.3512,  0.2667]], requires_grad=True)
    Parameter containing:
    tensor([-0.6025], requires_grad=True)
    
    constant weights and bias ==================================================
    Parameter containing:
    tensor([[1., 1.]], requires_grad=True)
    Parameter containing:
    tensor([2.], requires_grad=True)



```python
# 2차원 넘파이 배열
x2_np = np.array([[0, 0], [0, 1], [1, 0], [1,1]])

# 텐서 변수화
x2 =  torch.tensor(x2_np).float()

# 결과 확인
print(x2.shape)
print(x2)

# 함수 값 계산
y2 = l2(x2)

# shape 확인
print(y2.shape)

# 값 확인
print(y2.data)
```

    torch.Size([4, 2])
    tensor([[0., 0.],
            [0., 1.],
            [1., 0.],
            [1., 1.]])
    torch.Size([4, 1])
    tensor([[2.],
            [3.],
            [3.],
            [4.]])


### 입력 :2, 출력 :3 선형 함수 정의


```python
# 입력 :2, 출력 :3 선형 함수 정의

l3 = nn.Linear(2, 3)

# 초깃값 설정
nn.init.constant_(l3.weight[0,:], 1.0)
nn.init.constant_(l3.weight[1,:], 2.0)
nn.init.constant_(l3.weight[2,:], 3.0)
nn.init.constant_(l3.bias, 2.0)

# 결과 확인
print(l3.weight)
print(l3.bias)
```

    Parameter containing:
    tensor([[1., 1.],
            [2., 2.],
            [3., 3.]], requires_grad=True)
    Parameter containing:
    tensor([2., 2., 2.], requires_grad=True)



```python
# 함수 값 계산
y3 = l3(x2)

# shape 확인
print(y3.shape)

# 값 확인
print(y3.data)
```

    torch.Size([4, 3])
    tensor([[2., 2., 2.],
            [3., 4., 5.],
            [3., 4., 5.],
            [4., 6., 8.]])


### 클래스를 이용한 모델 정의


```python
# 모델 정의

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        #  부모 클래스 nn.Module 초기화
        super().__init__()

        # 출력층 정의
        self.l1 = nn.Linear(n_input, n_output)

    # 예측 함수 정의
    def forward(self, x):
        x1 = self.l1(x) # 선형 회귀
        return x1

# 더미 입력
inputs = torch.rand(100,1)
labels1 = torch.rand(100,1)

# 인스턴스 생성(１ 입력, 1 출력 선형 모델)
n_input = 1
n_output = 1
net = Net(n_input, n_output)
```


```python
print(net)
print(net.l1)
print(net.l1.weight)
print(net.l1.bias)

```

    Net(
      (l1): Linear(in_features=1, out_features=1, bias=True)
    )
    Linear(in_features=1, out_features=1, bias=True)
    Parameter containing:
    tensor([[0.2678]], requires_grad=True)
    Parameter containing:
    tensor([-0.2211], requires_grad=True)



```python
# 예측
# torch.matmul(inputs, net.l1.weight) + net.l1.bias
outputs = net(inputs)
print("outputs = \n", outputs)
```

    outputs = 
     tensor([[-0.1364],
            [-0.1135],
            [-0.1894],
            [ 0.0004],
            [-0.1188],
            [-0.0443],
            [ 0.0074],
            [-0.0623],
            [-0.0506],
            [ 0.0420],
            [-0.1476],
            [-0.0448],
            [-0.1468],
            [ 0.0084],
            [ 0.0197],
            [-0.2107],
            [ 0.0270],
            [-0.0233],
            [-0.0289],
            [-0.0321],
            [ 0.0241],
            [-0.1049],
            [-0.2005],
            [-0.1257],
            [-0.1815],
            [-0.0784],
            [-0.1122],
            [-0.1590],
            [-0.0994],
            [ 0.0396],
            [-0.0978],
            [-0.0830],
            [-0.1081],
            [-0.0662],
            [ 0.0321],
            [-0.0054],
            [-0.0397],
            [-0.0581],
            [-0.0557],
            [-0.0355],
            [-0.1045],
            [-0.2117],
            [-0.1700],
            [ 0.0270],
            [-0.0792],
            [-0.1957],
            [-0.0661],
            [ 0.0234],
            [-0.2138],
            [-0.1774],
            [-0.1406],
            [-0.0819],
            [-0.1185],
            [-0.1019],
            [-0.2178],
            [-0.0245],
            [ 0.0303],
            [-0.0054],
            [-0.1820],
            [-0.1952],
            [-0.0316],
            [-0.0842],
            [-0.0324],
            [-0.2181],
            [-0.0952],
            [ 0.0072],
            [-0.0251],
            [-0.0823],
            [-0.0609],
            [-0.0999],
            [-0.1608],
            [-0.1378],
            [-0.1688],
            [ 0.0240],
            [-0.0136],
            [-0.0404],
            [-0.1899],
            [ 0.0161],
            [-0.0453],
            [ 0.0054],
            [-0.1399],
            [-0.0589],
            [ 0.0435],
            [ 0.0028],
            [ 0.0201],
            [-0.1153],
            [ 0.0148],
            [-0.1921],
            [-0.0757],
            [-0.1626],
            [-0.1185],
            [-0.1215],
            [-0.0772],
            [ 0.0346],
            [-0.0210],
            [-0.0878],
            [ 0.0078],
            [-0.1558],
            [-0.0182],
            [-0.0997]], grad_fn=<AddmmBackward0>)


### MSELoss 클래스를 이용한 손실 함수


```python
criterion = nn.MSELoss()
```


```python
loss = criterion(outputs, labels1)
print("loss = ", loss)
loss.backward()
```

    loss =  tensor(0.4184, grad_fn=<MseLossBackward0>)



```python
print(net.l1.weight.grad)
print(net.l1.bias.grad)
```

    tensor([[-0.5785]])
    tensor([-1.1541])


## 회귀 분석 예제: Boston dataset


```python
# 학습용 데이터셋 준비

# '보스턴 데이터셋'은 현재 사이킷런 라이브러리에서 가져올 수 있지만,
# 사이킷런에서 앞으로 이 데이터를 사용할 수 없기 때문에 웹 url에서 직접 수집

#  Variables in order:
#  CRIM     per capita crime rate by town
#  ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
#  INDUS    proportion of non-retail business acres per town
#  CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#  NOX      nitric oxides concentration (parts per 10 million)
#  RM       average number of rooms per dwelling
#  AGE      proportion of owner-occupied units built prior to 1940
#  DIS      weighted distances to five Boston employment centres
#  RAD      index of accessibility to radial highways
#  TAX      full-value property-tax rate per $10,000
#  PTRATIO  pupil-teacher ratio by town
#  B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
#  LSTAT    % lower status of the population
#  MEDV     Median value of owner-occupied homes in $1000's

# CRIM: 인구당 마을별 범죄율
# ZN: 25,000 평방피트를 초과하는 주거용 토지 비율
# INDUS: 마을별 비소매업 지역 비율
# CHAS: 찰스강 더미 변수 (강과 접한 지역 = 1, 그렇지 않으면 = 0)
# NOX: 질소 산화물 농도 (1000만 분의 1 단위)
# RM: 주택당 평균 방 개수
# AGE: 1940년 이전에 건축된 자가 소유 주택의 비율
# DIS: 보스턴 주요 고용 센터 5곳까지의 가중 거리
# RAD: 방사형 고속도로 접근성 지수
# TAX: $10,000당 재산세율
# PTRATIO: 마을별 학생-교사 비율
# B: 1000(Bk - 0.63)^2, 여기서 Bk는 마을별 흑인 인구 비율
# LSTAT: 저소득층 인구 비율
# MEDV: 자가 소유 주택의 중간값 ($1000 단위)
```


```python

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+",
                     skiprows=22, header=None)
print(raw_df.head(10))

```

              0      1      2    3      4      5     6       7    8      9     10
    0    0.00632  18.00   2.31  0.0  0.538  6.575  65.2  4.0900  1.0  296.0  15.3
    1  396.90000   4.98  24.00  NaN    NaN    NaN   NaN     NaN  NaN    NaN   NaN
    2    0.02731   0.00   7.07  0.0  0.469  6.421  78.9  4.9671  2.0  242.0  17.8
    3  396.90000   9.14  21.60  NaN    NaN    NaN   NaN     NaN  NaN    NaN   NaN
    4    0.02729   0.00   7.07  0.0  0.469  7.185  61.1  4.9671  2.0  242.0  17.8
    5  392.83000   4.03  34.70  NaN    NaN    NaN   NaN     NaN  NaN    NaN   NaN
    6    0.03237   0.00   2.18  0.0  0.458  6.998  45.8  6.0622  3.0  222.0  18.7
    7  394.63000   2.94  33.40  NaN    NaN    NaN   NaN     NaN  NaN    NaN   NaN
    8    0.06905   0.00   2.18  0.0  0.458  7.147  54.2  6.0622  3.0  222.0  18.7
    9  396.90000   5.33  36.20  NaN    NaN    NaN   NaN     NaN  NaN    NaN   NaN



```python

x_org = np.hstack([raw_df.values[::2, :],
                   raw_df.values[1::2, :2]]) # 짝수줄 전체, 홀 수 줄 [: 2] => Features
# x_org[:10, :5]
```


```python
yt = raw_df.values[1::2, 2] ## Target
feature_names = np.array(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX',
                          'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO','B', 'LSTAT'])

# 결과 확인
print('원본 데이터', x_org.shape, yt.shape)
print('항목명: ', feature_names)
```

    원본 데이터 (506, 13) (506,)
    항목명:  ['CRIM' 'ZN' 'INDUS' 'CHAS' 'NOX' 'RM' 'AGE' 'DIS' 'RAD' 'TAX' 'PTRATIO'
     'B' 'LSTAT']



```python
x_org[:5]
feature_names == 'RM'
```




    array([False, False, False, False, False,  True, False, False, False,
           False, False, False, False])




```python
# 데이터 추출(RM 항목)
x = x_org[:,feature_names == 'RM']
print('추출 후', x.shape)
print(x[:5,:])

# 정답 데이터 y 표시
print('정답 데이터')
print(yt[:5])
```

    추출 후 (506, 1)
    [[6.575]
     [6.421]
     [7.185]
     [6.998]
     [7.147]]
    정답 데이터
    [24.  21.6 34.7 33.4 36.2]



```python
# 산포도 출력

plt.scatter(x, yt, s=10, c='b')
plt.xlabel('Room counts')
plt.ylabel('Price')
plt.title(' Scatter plot between Room counts vs Price ')
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__37_0.webp)
    


### 단순 선형 회귀


```python
## 회귀모델

# 입력 차원수
n_input= x.shape[1]

# 출력 차원수
n_output = 1

print(f'입력 차원수: {n_input}  출력 차원수: {n_output}')

# 머신러닝 모델(예측 모델)의 클래스 정의

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        #  부모 클래스 nn.Module 초기화
        super().__init__()

        # 출력층 정의
        self.l1 = nn.Linear(n_input, n_output)

        # 초깃값을 모두 1로 설정
        # "딥러닝을 위한 수학"과 조건을 맞추기 위함
        # nn.init.constant_(self.l1.weight, 1.0)
        # nn.init.constant_(self.l1.bias, 1.0)

    # 예측 함수 정의
    def forward(self, x):
        x1 = self.l1(x) # 선형 회귀
        return x1
```

    입력 차원수: 1  출력 차원수: 1



```python
# 인스턴스 생성
# １입력 1출력 선형 모델

net = Net(n_input, n_output)

# 모델 안의 파라미터를 확인
for parameter in net.named_parameters():
    print(f'변수명: {parameter[0]}')
    print(f'변숫값: {parameter[1].data}')
print("="*50)
# 파라미터 리스트를 가져오기 위해 parameters 함수를 사용
for parameter in net.parameters():
    print(parameter)
```

    변수명: l1.weight
    변숫값: tensor([[0.4797]])
    변수명: l1.bias
    변숫값: tensor([-0.5425])
    ==================================================
    Parameter containing:
    tensor([[0.4797]], requires_grad=True)
    Parameter containing:
    tensor([-0.5425], requires_grad=True)



```python
print(net)
```

    Net(
      (l1): Linear(in_features=1, out_features=1, bias=True)
    )



```python
# from torchsummary import summary
from torchinfo import summary

summary(net, (1,), device = 'cpu')
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [1]                       --
    ├─Linear: 1-1                            [1]                       2
    ==========================================================================================
    Total params: 2
    Trainable params: 2
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 0.00
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.00
    Estimated Total Size (MB): 0.00
    ==========================================================================================




```python
# 손실 함수： 평균 제곱 오차
criterion = nn.MSELoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)
```


```python
# 입력값 x와 정답 yt의 텐서 변수화
# inputs = torch.tensor(x).float()
# labels = torch.tensor(yt).float()
inputs = torch.tensor(x, dtype = torch.float32)
labels = torch.tensor(yt, dtype = torch.float32)

# 차원 수 확인

print(inputs.shape, inputs.dtype)
print(labels.shape, labels.dtype)
```

    torch.Size([506, 1]) torch.float32
    torch.Size([506]) torch.float32



```python
# 손실 계산을 위해 labels를 (N,1) 차원의 행렬로 변환

labels1 = labels.view((-1, 1))

# 차원 수 확인
print("label shape = ", labels1.shape)

# 예측 계산

outputs = net(inputs)
print(outputs.dtype)
print(outputs.dtype)


# 손실 계산
loss = criterion(outputs, labels1)

# 손실 값 가져오기
print(f'{loss.item():.5f}')
```

    label shape =  torch.Size([506, 1])
    torch.float32
    torch.float32
    482.66223



```python
dict(net.named_parameters())
```




    {'l1.weight': Parameter containing:
     tensor([[0.4797]], requires_grad=True),
     'l1.bias': Parameter containing:
     tensor([-0.5425], requires_grad=True)}




```python
# 손실을 그래프로 나타내기
from torchviz import make_dot

g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__47_0.svg)
    



```python
# 예측 계산
outputs = net(inputs)

# 손실 계산
loss = criterion(outputs, labels1)

# 경사 계산
loss.backward()

# 경사 계산 결과를 취득 가능하도록 함
print("net.l1.weight.grad = ", net.l1.weight.grad)
print("net.l1.bias.grad = ", net.l1.bias.grad)

# 파라미터 수정
optimizer.step()

# 파라미터 확인
print("="*50)
print(net.l1.weight)
print(net.l1.bias)

# 경삿값 초기화
optimizer.zero_grad()

# 경삿값을 모두 0으로 함
print("="*50)
print(net.l1.weight.grad)
print(net.l1.bias.grad)
```

    net.l1.weight.grad =  tensor([[-260.6448]])
    net.l1.bias.grad =  tensor([-40.1214])
    ==================================================
    Parameter containing:
    tensor([[3.0861]], requires_grad=True)
    Parameter containing:
    tensor([-0.1413], requires_grad=True)
    ==================================================
    None
    None


### 경사 하강법을 이용한 학습


```python
# 학습률
lr = 0.01

# 인스턴스 생성(파라미터 값 초기화)
net = Net(n_input, n_output)

# 손실 함수：평균 제곱 오차
criterion = nn.MSELoss()

# 최적화 함수 : 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 50000

# 평가 결과 기록(손실 값만 기록)
history = np.zeros((0,2))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 경삿값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    # "딥러닝을 위한 수학"에 나온 결과와 맞추기 위해 2로 나눈 값을 손실로 정의
    loss = criterion(outputs, labels1) / 2.0

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 100회 마다 도중 경과를 기록
    if ( epoch % 100 == 0):
        history = np.vstack((history, np.array([epoch, loss.item()])))
        print(f'Epoch {epoch} loss: {loss.item():.5f}')
```

    Epoch 0 loss: 299.93127
    Epoch 100 loss: 28.92968
    Epoch 200 loss: 28.76028
    Epoch 300 loss: 28.59489
    Epoch 400 loss: 28.43344
    Epoch 500 loss: 28.27583
    Epoch 600 loss: 28.12196
    Epoch 700 loss: 27.97174
    Epoch 800 loss: 27.82510
    Epoch 900 loss: 27.68194
    Epoch 1000 loss: 27.54218
    Epoch 1100 loss: 27.40574
    Epoch 1200 loss: 27.27254
    Epoch 1300 loss: 27.14251
    Epoch 1400 loss: 27.01557
    Epoch 1500 loss: 26.89165
    Epoch 1600 loss: 26.77067
    Epoch 1700 loss: 26.65256
    Epoch 1800 loss: 26.53726
    Epoch 1900 loss: 26.42470
    Epoch 2000 loss: 26.31482
    Epoch 2100 loss: 26.20755
    Epoch 2200 loss: 26.10282
    Epoch 2300 loss: 26.00059
    Epoch 2400 loss: 25.90078
    Epoch 2500 loss: 25.80334
    Epoch 2600 loss: 25.70822
    Epoch 2700 loss: 25.61536
    Epoch 2800 loss: 25.52471
    Epoch 2900 loss: 25.43621
    Epoch 3000 loss: 25.34982
    Epoch 3100 loss: 25.26547
    Epoch 3200 loss: 25.18313
    Epoch 3300 loss: 25.10275
    Epoch 3400 loss: 25.02428
    Epoch 3500 loss: 24.94767
    Epoch 3600 loss: 24.87288
    Epoch 3700 loss: 24.79987
    Epoch 3800 loss: 24.72860
    Epoch 3900 loss: 24.65902
    Epoch 4000 loss: 24.59109
    Epoch 4100 loss: 24.52477
    Epoch 4200 loss: 24.46003
    Epoch 4300 loss: 24.39683
    Epoch 4400 loss: 24.33513
    Epoch 4500 loss: 24.27490
    Epoch 4600 loss: 24.21610
    Epoch 4700 loss: 24.15870
    Epoch 4800 loss: 24.10266
    Epoch 4900 loss: 24.04795
    Epoch 5000 loss: 23.99454
    Epoch 5100 loss: 23.94240
    Epoch 5200 loss: 23.89150
    Epoch 5300 loss: 23.84181
    Epoch 5400 loss: 23.79330
    Epoch 5500 loss: 23.74594
    Epoch 5600 loss: 23.69971
    Epoch 5700 loss: 23.65458
    Epoch 5800 loss: 23.61051
    Epoch 5900 loss: 23.56750
    Epoch 6000 loss: 23.52551
    Epoch 6100 loss: 23.48451
    Epoch 6200 loss: 23.44449
    Epoch 6300 loss: 23.40542
    Epoch 6400 loss: 23.36728
    Epoch 6500 loss: 23.33005
    Epoch 6600 loss: 23.29370
    Epoch 6700 loss: 23.25821
    Epoch 6800 loss: 23.22357
    Epoch 6900 loss: 23.18975
    Epoch 7000 loss: 23.15673
    Epoch 7100 loss: 23.12450
    Epoch 7200 loss: 23.09304
    Epoch 7300 loss: 23.06232
    Epoch 7400 loss: 23.03233
    Epoch 7500 loss: 23.00305
    Epoch 7600 loss: 22.97447
    Epoch 7700 loss: 22.94658
    Epoch 7800 loss: 22.91933
    Epoch 7900 loss: 22.89275
    Epoch 8000 loss: 22.86679
    Epoch 8100 loss: 22.84145
    Epoch 8200 loss: 22.81671
    Epoch 8300 loss: 22.79255
    Epoch 8400 loss: 22.76898
    Epoch 8500 loss: 22.74596
    Epoch 8600 loss: 22.72349
    Epoch 8700 loss: 22.70155
    Epoch 8800 loss: 22.68013
    Epoch 8900 loss: 22.65923
    Epoch 9000 loss: 22.63881
    Epoch 9100 loss: 22.61889
    Epoch 9200 loss: 22.59944
    Epoch 9300 loss: 22.58045
    Epoch 9400 loss: 22.56191
    Epoch 9500 loss: 22.54381
    Epoch 9600 loss: 22.52615
    Epoch 9700 loss: 22.50890
    Epoch 9800 loss: 22.49206
    Epoch 9900 loss: 22.47563
    Epoch 10000 loss: 22.45958
    Epoch 10100 loss: 22.44391
    Epoch 10200 loss: 22.42862
    Epoch 10300 loss: 22.41369
    Epoch 10400 loss: 22.39911
    Epoch 10500 loss: 22.38488
    Epoch 10600 loss: 22.37099
    Epoch 10700 loss: 22.35743
    Epoch 10800 loss: 22.34419
    Epoch 10900 loss: 22.33126
    Epoch 11000 loss: 22.31865
    Epoch 11100 loss: 22.30633
    Epoch 11200 loss: 22.29431
    Epoch 11300 loss: 22.28257
    Epoch 11400 loss: 22.27111
    Epoch 11500 loss: 22.25992
    Epoch 11600 loss: 22.24900
    Epoch 11700 loss: 22.23834
    Epoch 11800 loss: 22.22793
    Epoch 11900 loss: 22.21777
    Epoch 12000 loss: 22.20785
    Epoch 12100 loss: 22.19816
    Epoch 12200 loss: 22.18871
    Epoch 12300 loss: 22.17948
    Epoch 12400 loss: 22.17047
    Epoch 12500 loss: 22.16167
    Epoch 12600 loss: 22.15308
    Epoch 12700 loss: 22.14470
    Epoch 12800 loss: 22.13652
    Epoch 12900 loss: 22.12853
    Epoch 13000 loss: 22.12073
    Epoch 13100 loss: 22.11312
    Epoch 13200 loss: 22.10568
    Epoch 13300 loss: 22.09842
    Epoch 13400 loss: 22.09134
    Epoch 13500 loss: 22.08442
    Epoch 13600 loss: 22.07767
    Epoch 13700 loss: 22.07108
    Epoch 13800 loss: 22.06465
    Epoch 13900 loss: 22.05836
    Epoch 14000 loss: 22.05223
    Epoch 14100 loss: 22.04624
    Epoch 14200 loss: 22.04040
    Epoch 14300 loss: 22.03469
    Epoch 14400 loss: 22.02912
    Epoch 14500 loss: 22.02369
    Epoch 14600 loss: 22.01838
    Epoch 14700 loss: 22.01319
    Epoch 14800 loss: 22.00814
    Epoch 14900 loss: 22.00320
    Epoch 15000 loss: 21.99837
    Epoch 15100 loss: 21.99367
    Epoch 15200 loss: 21.98907
    Epoch 15300 loss: 21.98459
    Epoch 15400 loss: 21.98021
    Epoch 15500 loss: 21.97593
    Epoch 15600 loss: 21.97176
    Epoch 15700 loss: 21.96769
    Epoch 15800 loss: 21.96371
    Epoch 15900 loss: 21.95982
    Epoch 16000 loss: 21.95603
    Epoch 16100 loss: 21.95233
    Epoch 16200 loss: 21.94872
    Epoch 16300 loss: 21.94519
    Epoch 16400 loss: 21.94175
    Epoch 16500 loss: 21.93839
    Epoch 16600 loss: 21.93510
    Epoch 16700 loss: 21.93190
    Epoch 16800 loss: 21.92877
    Epoch 16900 loss: 21.92572
    Epoch 17000 loss: 21.92274
    Epoch 17100 loss: 21.91983
    Epoch 17200 loss: 21.91699
    Epoch 17300 loss: 21.91422
    Epoch 17400 loss: 21.91151
    Epoch 17500 loss: 21.90886
    Epoch 17600 loss: 21.90629
    Epoch 17700 loss: 21.90377
    Epoch 17800 loss: 21.90131
    Epoch 17900 loss: 21.89891
    Epoch 18000 loss: 21.89656
    Epoch 18100 loss: 21.89428
    Epoch 18200 loss: 21.89205
    Epoch 18300 loss: 21.88986
    Epoch 18400 loss: 21.88773
    Epoch 18500 loss: 21.88565
    Epoch 18600 loss: 21.88363
    Epoch 18700 loss: 21.88165
    Epoch 18800 loss: 21.87971
    Epoch 18900 loss: 21.87782
    Epoch 19000 loss: 21.87598
    Epoch 19100 loss: 21.87419
    Epoch 19200 loss: 21.87243
    Epoch 19300 loss: 21.87071
    Epoch 19400 loss: 21.86904
    Epoch 19500 loss: 21.86740
    Epoch 19600 loss: 21.86581
    Epoch 19700 loss: 21.86425
    Epoch 19800 loss: 21.86274
    Epoch 19900 loss: 21.86125
    Epoch 20000 loss: 21.85980
    Epoch 20100 loss: 21.85839
    Epoch 20200 loss: 21.85701
    Epoch 20300 loss: 21.85566
    Epoch 20400 loss: 21.85434
    Epoch 20500 loss: 21.85306
    Epoch 20600 loss: 21.85180
    Epoch 20700 loss: 21.85058
    Epoch 20800 loss: 21.84939
    Epoch 20900 loss: 21.84822
    Epoch 21000 loss: 21.84708
    Epoch 21100 loss: 21.84597
    Epoch 21200 loss: 21.84488
    Epoch 21300 loss: 21.84382
    Epoch 21400 loss: 21.84278
    Epoch 21500 loss: 21.84177
    Epoch 21600 loss: 21.84079
    Epoch 21700 loss: 21.83983
    Epoch 21800 loss: 21.83889
    Epoch 21900 loss: 21.83797
    Epoch 22000 loss: 21.83707
    Epoch 22100 loss: 21.83620
    Epoch 22200 loss: 21.83535
    Epoch 22300 loss: 21.83451
    Epoch 22400 loss: 21.83370
    Epoch 22500 loss: 21.83291
    Epoch 22600 loss: 21.83213
    Epoch 22700 loss: 21.83138
    Epoch 22800 loss: 21.83063
    Epoch 22900 loss: 21.82991
    Epoch 23000 loss: 21.82921
    Epoch 23100 loss: 21.82852
    Epoch 23200 loss: 21.82785
    Epoch 23300 loss: 21.82720
    Epoch 23400 loss: 21.82655
    Epoch 23500 loss: 21.82593
    Epoch 23600 loss: 21.82532
    Epoch 23700 loss: 21.82473
    Epoch 23800 loss: 21.82415
    Epoch 23900 loss: 21.82358
    Epoch 24000 loss: 21.82302
    Epoch 24100 loss: 21.82249
    Epoch 24200 loss: 21.82196
    Epoch 24300 loss: 21.82144
    Epoch 24400 loss: 21.82094
    Epoch 24500 loss: 21.82045
    Epoch 24600 loss: 21.81997
    Epoch 24700 loss: 21.81950
    Epoch 24800 loss: 21.81904
    Epoch 24900 loss: 21.81860
    Epoch 25000 loss: 21.81817
    Epoch 25100 loss: 21.81774
    Epoch 25200 loss: 21.81732
    Epoch 25300 loss: 21.81692
    Epoch 25400 loss: 21.81652
    Epoch 25500 loss: 21.81614
    Epoch 25600 loss: 21.81576
    Epoch 25700 loss: 21.81540
    Epoch 25800 loss: 21.81503
    Epoch 25900 loss: 21.81468
    Epoch 26000 loss: 21.81434
    Epoch 26100 loss: 21.81401
    Epoch 26200 loss: 21.81368
    Epoch 26300 loss: 21.81336
    Epoch 26400 loss: 21.81305
    Epoch 26500 loss: 21.81275
    Epoch 26600 loss: 21.81245
    Epoch 26700 loss: 21.81216
    Epoch 26800 loss: 21.81188
    Epoch 26900 loss: 21.81161
    Epoch 27000 loss: 21.81133
    Epoch 27100 loss: 21.81107
    Epoch 27200 loss: 21.81082
    Epoch 27300 loss: 21.81056
    Epoch 27400 loss: 21.81032
    Epoch 27500 loss: 21.81008
    Epoch 27600 loss: 21.80985
    Epoch 27700 loss: 21.80962
    Epoch 27800 loss: 21.80940
    Epoch 27900 loss: 21.80918
    Epoch 28000 loss: 21.80897
    Epoch 28100 loss: 21.80877
    Epoch 28200 loss: 21.80856
    Epoch 28300 loss: 21.80837
    Epoch 28400 loss: 21.80817
    Epoch 28500 loss: 21.80799
    Epoch 28600 loss: 21.80781
    Epoch 28700 loss: 21.80762
    Epoch 28800 loss: 21.80745
    Epoch 28900 loss: 21.80728
    Epoch 29000 loss: 21.80712
    Epoch 29100 loss: 21.80695
    Epoch 29200 loss: 21.80679
    Epoch 29300 loss: 21.80664
    Epoch 29400 loss: 21.80649
    Epoch 29500 loss: 21.80634
    Epoch 29600 loss: 21.80619
    Epoch 29700 loss: 21.80605
    Epoch 29800 loss: 21.80592
    Epoch 29900 loss: 21.80578
    Epoch 30000 loss: 21.80565
    Epoch 30100 loss: 21.80552
    Epoch 30200 loss: 21.80540
    Epoch 30300 loss: 21.80528
    Epoch 30400 loss: 21.80516
    Epoch 30500 loss: 21.80504
    Epoch 30600 loss: 21.80493
    Epoch 30700 loss: 21.80482
    Epoch 30800 loss: 21.80471
    Epoch 30900 loss: 21.80461
    Epoch 31000 loss: 21.80450
    Epoch 31100 loss: 21.80440
    Epoch 31200 loss: 21.80431
    Epoch 31300 loss: 21.80421
    Epoch 31400 loss: 21.80411
    Epoch 31500 loss: 21.80403
    Epoch 31600 loss: 21.80394
    Epoch 31700 loss: 21.80385
    Epoch 31800 loss: 21.80376
    Epoch 31900 loss: 21.80368
    Epoch 32000 loss: 21.80360
    Epoch 32100 loss: 21.80352
    Epoch 32200 loss: 21.80344
    Epoch 32300 loss: 21.80337
    Epoch 32400 loss: 21.80330
    Epoch 32500 loss: 21.80322
    Epoch 32600 loss: 21.80315
    Epoch 32700 loss: 21.80309
    Epoch 32800 loss: 21.80302
    Epoch 32900 loss: 21.80295
    Epoch 33000 loss: 21.80289
    Epoch 33100 loss: 21.80283
    Epoch 33200 loss: 21.80277
    Epoch 33300 loss: 21.80271
    Epoch 33400 loss: 21.80265
    Epoch 33500 loss: 21.80259
    Epoch 33600 loss: 21.80254
    Epoch 33700 loss: 21.80249
    Epoch 33800 loss: 21.80243
    Epoch 33900 loss: 21.80238
    Epoch 34000 loss: 21.80233
    Epoch 34100 loss: 21.80228
    Epoch 34200 loss: 21.80224
    Epoch 34300 loss: 21.80219
    Epoch 34400 loss: 21.80214
    Epoch 34500 loss: 21.80210
    Epoch 34600 loss: 21.80206
    Epoch 34700 loss: 21.80202
    Epoch 34800 loss: 21.80197
    Epoch 34900 loss: 21.80193
    Epoch 35000 loss: 21.80189
    Epoch 35100 loss: 21.80186
    Epoch 35200 loss: 21.80181
    Epoch 35300 loss: 21.80178
    Epoch 35400 loss: 21.80174
    Epoch 35500 loss: 21.80171
    Epoch 35600 loss: 21.80168
    Epoch 35700 loss: 21.80164
    Epoch 35800 loss: 21.80161
    Epoch 35900 loss: 21.80158
    Epoch 36000 loss: 21.80155
    Epoch 36100 loss: 21.80152
    Epoch 36200 loss: 21.80149
    Epoch 36300 loss: 21.80146
    Epoch 36400 loss: 21.80143
    Epoch 36500 loss: 21.80140
    Epoch 36600 loss: 21.80138
    Epoch 36700 loss: 21.80135
    Epoch 36800 loss: 21.80132
    Epoch 36900 loss: 21.80130
    Epoch 37000 loss: 21.80128
    Epoch 37100 loss: 21.80125
    Epoch 37200 loss: 21.80123
    Epoch 37300 loss: 21.80120
    Epoch 37400 loss: 21.80119
    Epoch 37500 loss: 21.80116
    Epoch 37600 loss: 21.80114
    Epoch 37700 loss: 21.80112
    Epoch 37800 loss: 21.80110
    Epoch 37900 loss: 21.80108
    Epoch 38000 loss: 21.80106
    Epoch 38100 loss: 21.80105
    Epoch 38200 loss: 21.80102
    Epoch 38300 loss: 21.80101
    Epoch 38400 loss: 21.80099
    Epoch 38500 loss: 21.80097
    Epoch 38600 loss: 21.80095
    Epoch 38700 loss: 21.80094
    Epoch 38800 loss: 21.80092
    Epoch 38900 loss: 21.80091
    Epoch 39000 loss: 21.80090
    Epoch 39100 loss: 21.80088
    Epoch 39200 loss: 21.80087
    Epoch 39300 loss: 21.80085
    Epoch 39400 loss: 21.80083
    Epoch 39500 loss: 21.80083
    Epoch 39600 loss: 21.80081
    Epoch 39700 loss: 21.80080
    Epoch 39800 loss: 21.80079
    Epoch 39900 loss: 21.80078
    Epoch 40000 loss: 21.80076
    Epoch 40100 loss: 21.80075
    Epoch 40200 loss: 21.80074
    Epoch 40300 loss: 21.80073
    Epoch 40400 loss: 21.80072
    Epoch 40500 loss: 21.80071
    Epoch 40600 loss: 21.80070
    Epoch 40700 loss: 21.80069
    Epoch 40800 loss: 21.80068
    Epoch 40900 loss: 21.80067
    Epoch 41000 loss: 21.80066
    Epoch 41100 loss: 21.80065
    Epoch 41200 loss: 21.80064
    Epoch 41300 loss: 21.80063
    Epoch 41400 loss: 21.80062
    Epoch 41500 loss: 21.80062
    Epoch 41600 loss: 21.80061
    Epoch 41700 loss: 21.80060
    Epoch 41800 loss: 21.80059
    Epoch 41900 loss: 21.80058
    Epoch 42000 loss: 21.80058
    Epoch 42100 loss: 21.80057
    Epoch 42200 loss: 21.80056
    Epoch 42300 loss: 21.80056
    Epoch 42400 loss: 21.80055
    Epoch 42500 loss: 21.80054
    Epoch 42600 loss: 21.80054
    Epoch 42700 loss: 21.80053
    Epoch 42800 loss: 21.80052
    Epoch 42900 loss: 21.80052
    Epoch 43000 loss: 21.80051
    Epoch 43100 loss: 21.80051
    Epoch 43200 loss: 21.80050
    Epoch 43300 loss: 21.80050
    Epoch 43400 loss: 21.80049
    Epoch 43500 loss: 21.80049
    Epoch 43600 loss: 21.80048
    Epoch 43700 loss: 21.80047
    Epoch 43800 loss: 21.80047
    Epoch 43900 loss: 21.80047
    Epoch 44000 loss: 21.80046
    Epoch 44100 loss: 21.80046
    Epoch 44200 loss: 21.80045
    Epoch 44300 loss: 21.80045
    Epoch 44400 loss: 21.80045
    Epoch 44500 loss: 21.80044
    Epoch 44600 loss: 21.80044
    Epoch 44700 loss: 21.80043
    Epoch 44800 loss: 21.80043
    Epoch 44900 loss: 21.80043
    Epoch 45000 loss: 21.80042
    Epoch 45100 loss: 21.80042
    Epoch 45200 loss: 21.80042
    Epoch 45300 loss: 21.80041
    Epoch 45400 loss: 21.80041
    Epoch 45500 loss: 21.80041
    Epoch 45600 loss: 21.80040
    Epoch 45700 loss: 21.80040
    Epoch 45800 loss: 21.80040
    Epoch 45900 loss: 21.80040
    Epoch 46000 loss: 21.80039
    Epoch 46100 loss: 21.80039
    Epoch 46200 loss: 21.80039
    Epoch 46300 loss: 21.80038
    Epoch 46400 loss: 21.80038
    Epoch 46500 loss: 21.80038
    Epoch 46600 loss: 21.80038
    Epoch 46700 loss: 21.80037
    Epoch 46800 loss: 21.80037
    Epoch 46900 loss: 21.80037
    Epoch 47000 loss: 21.80037
    Epoch 47100 loss: 21.80036
    Epoch 47200 loss: 21.80036
    Epoch 47300 loss: 21.80036
    Epoch 47400 loss: 21.80036
    Epoch 47500 loss: 21.80035
    Epoch 47600 loss: 21.80035
    Epoch 47700 loss: 21.80035
    Epoch 47800 loss: 21.80035
    Epoch 47900 loss: 21.80035
    Epoch 48000 loss: 21.80035
    Epoch 48100 loss: 21.80035
    Epoch 48200 loss: 21.80034
    Epoch 48300 loss: 21.80034
    Epoch 48400 loss: 21.80034
    Epoch 48500 loss: 21.80034
    Epoch 48600 loss: 21.80034
    Epoch 48700 loss: 21.80034
    Epoch 48800 loss: 21.80034
    Epoch 48900 loss: 21.80033
    Epoch 49000 loss: 21.80033
    Epoch 49100 loss: 21.80033
    Epoch 49200 loss: 21.80033
    Epoch 49300 loss: 21.80033
    Epoch 49400 loss: 21.80033
    Epoch 49500 loss: 21.80033
    Epoch 49600 loss: 21.80033
    Epoch 49700 loss: 21.80032
    Epoch 49800 loss: 21.80032
    Epoch 49900 loss: 21.80032



```python
# 초기 손실값과 최종 손실값

print(f'초기 손실값: {history[0,1]:.5f}')
print(f'최종 손실값: {history[-1,1]:.5f}')
```

    초기 손실값: 299.93127
    최종 손실값: 21.80032



```python
# 학습 곡선 출력(손실)
# 가장 처음 요소는 제외

plt.plot(history[1:,0], history[1:,1], 'b')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__53_0.webp)
    



```python
# 회귀 직선 산출

# x의 최솟값, 최댓값
xse = np.array((x.min(), x.max())).reshape(-1,1)
Xse = torch.tensor(xse).float()

with torch.no_grad():
  Yse = net(Xse)

print(Yse.numpy())

# 산포도와 회귀 직선 출력

plt.scatter(x, yt, s=10, c='b')
plt.xlabel('방 개수')
plt.ylabel('가격')
plt.plot(Xse.data, Yse.data, c='k')
plt.title('산포도와 회귀 직선')
plt.show()
```

    [[-2.2208]
     [45.2137]]



    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__54_1.webp)
    


### 중회귀 모델


```python
# 열(LSTAT: 저소득자 비율) 추가

x_add = x_org[:,feature_names == 'LSTAT']
x2 = np.hstack((x, x_add))

# shape 표시
print(x2.shape)

# 입력 데이터 x 표시
print(x2[:5,:])
```

    (506, 2)
    [[6.575 4.98 ]
     [6.421 9.14 ]
     [7.185 4.03 ]
     [6.998 2.94 ]
     [7.147 5.33 ]]



```python
# 입력 차원수=2

n_input = x2.shape[1]
print(n_input)

# 모델 인스턴스 생성
net = Net(n_input, n_output)
```

    2



```python
# 모델 안의 파라미터 확인
# predict.weight가 2차원으로 바뀜

for parameter in net.named_parameters():
    print(f'변수명: {parameter[0]}')
    print(f'변숫값: {parameter[1].data}')
```

    변수명: l1.weight
    변숫값: tensor([[-0.5142,  0.2712]])
    변수명: l1.bias
    변숫값: tensor([-0.2058])



```python
# 모델의 개요 표시

from torchinfo import summary
summary(net, (2,))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [1]                       --
    ├─Linear: 1-1                            [1]                       3
    ==========================================================================================
    Total params: 3
    Trainable params: 3
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 0.00
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.00
    Estimated Total Size (MB): 0.00
    ==========================================================================================




```python
# 입력 변수 x2를 텐서로 변환
# labels, labels1은 이전과 같음

# inputs = torch.tensor(x2).float()
inputs = torch.tensor(x2, dtype = torch.float32)

# 초기화 처리

# 학습률
# lr = 0.01
lr = 0.001


# 인스턴스 생성(파라미터 값 초기화)
net = Net(n_input, n_output)

# 손실 함수：평균 제곱 오차
criterion = nn.MSELoss()

# 최적화 함수 : 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 50000

# 평가 결과 기록(손실 값만 기록)
history = np.zeros((0,2))

```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 경삿값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 오차 계산
    # "딥러닝을 위한 수학"에 나온 결과와 맞추기 위해 2로 나눈 값을 손실로 정의
    loss = criterion(outputs, labels1) / 2.0

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 100회 마다 도중 경과를 기록
    if ( epoch % 100 == 0):
        history = np.vstack((history, np.array([epoch, loss.item()])))
        print(f'Epoch {epoch} loss: {loss.item():.5f}')
```

    Epoch 0 loss: 529.79584
    Epoch 100 loss: 29.48064
    Epoch 200 loss: 16.83812
    Epoch 300 loss: 15.44524
    Epoch 400 loss: 15.29177
    Epoch 500 loss: 15.27485
    Epoch 600 loss: 15.27296
    Epoch 700 loss: 15.27274
    Epoch 800 loss: 15.27270
    Epoch 900 loss: 15.27268
    Epoch 1000 loss: 15.27265
    Epoch 1100 loss: 15.27264
    Epoch 1200 loss: 15.27262
    Epoch 1300 loss: 15.27260
    Epoch 1400 loss: 15.27258
    Epoch 1500 loss: 15.27256
    Epoch 1600 loss: 15.27254
    Epoch 1700 loss: 15.27252
    Epoch 1800 loss: 15.27250
    Epoch 1900 loss: 15.27248
    Epoch 2000 loss: 15.27246
    Epoch 2100 loss: 15.27244
    Epoch 2200 loss: 15.27242
    Epoch 2300 loss: 15.27240
    Epoch 2400 loss: 15.27239
    Epoch 2500 loss: 15.27237
    Epoch 2600 loss: 15.27235
    Epoch 2700 loss: 15.27233
    Epoch 2800 loss: 15.27231
    Epoch 2900 loss: 15.27229
    Epoch 3000 loss: 15.27227
    Epoch 3100 loss: 15.27225
    Epoch 3200 loss: 15.27223
    Epoch 3300 loss: 15.27222
    Epoch 3400 loss: 15.27220
    Epoch 3500 loss: 15.27217
    Epoch 3600 loss: 15.27216
    Epoch 3700 loss: 15.27214
    Epoch 3800 loss: 15.27212
    Epoch 3900 loss: 15.27210
    Epoch 4000 loss: 15.27208
    Epoch 4100 loss: 15.27207
    Epoch 4200 loss: 15.27205
    Epoch 4300 loss: 15.27203
    Epoch 4400 loss: 15.27201
    Epoch 4500 loss: 15.27199
    Epoch 4600 loss: 15.27197
    Epoch 4700 loss: 15.27195
    Epoch 4800 loss: 15.27193
    Epoch 4900 loss: 15.27192
    Epoch 5000 loss: 15.27189
    Epoch 5100 loss: 15.27188
    Epoch 5200 loss: 15.27186
    Epoch 5300 loss: 15.27184
    Epoch 5400 loss: 15.27182
    Epoch 5500 loss: 15.27180
    Epoch 5600 loss: 15.27179
    Epoch 5700 loss: 15.27177
    Epoch 5800 loss: 15.27175
    Epoch 5900 loss: 15.27173
    Epoch 6000 loss: 15.27171
    Epoch 6100 loss: 15.27170
    Epoch 6200 loss: 15.27168
    Epoch 6300 loss: 15.27166
    Epoch 6400 loss: 15.27164
    Epoch 6500 loss: 15.27162
    Epoch 6600 loss: 15.27160
    Epoch 6700 loss: 15.27158
    Epoch 6800 loss: 15.27157
    Epoch 6900 loss: 15.27155
    Epoch 7000 loss: 15.27153
    Epoch 7100 loss: 15.27151
    Epoch 7200 loss: 15.27149
    Epoch 7300 loss: 15.27148
    Epoch 7400 loss: 15.27146
    Epoch 7500 loss: 15.27144
    Epoch 7600 loss: 15.27142
    Epoch 7700 loss: 15.27140
    Epoch 7800 loss: 15.27139
    Epoch 7900 loss: 15.27137
    Epoch 8000 loss: 15.27135
    Epoch 8100 loss: 15.27133
    Epoch 8200 loss: 15.27131
    Epoch 8300 loss: 15.27129
    Epoch 8400 loss: 15.27128
    Epoch 8500 loss: 15.27126
    Epoch 8600 loss: 15.27124
    Epoch 8700 loss: 15.27122
    Epoch 8800 loss: 15.27121
    Epoch 8900 loss: 15.27119
    Epoch 9000 loss: 15.27117
    Epoch 9100 loss: 15.27115
    Epoch 9200 loss: 15.27114
    Epoch 9300 loss: 15.27112
    Epoch 9400 loss: 15.27110
    Epoch 9500 loss: 15.27109
    Epoch 9600 loss: 15.27107
    Epoch 9700 loss: 15.27105
    Epoch 9800 loss: 15.27103
    Epoch 9900 loss: 15.27101
    Epoch 10000 loss: 15.27100
    Epoch 10100 loss: 15.27098
    Epoch 10200 loss: 15.27096
    Epoch 10300 loss: 15.27094
    Epoch 10400 loss: 15.27093
    Epoch 10500 loss: 15.27091
    Epoch 10600 loss: 15.27089
    Epoch 10700 loss: 15.27087
    Epoch 10800 loss: 15.27085
    Epoch 10900 loss: 15.27084
    Epoch 11000 loss: 15.27082
    Epoch 11100 loss: 15.27080
    Epoch 11200 loss: 15.27079
    Epoch 11300 loss: 15.27077
    Epoch 11400 loss: 15.27075
    Epoch 11500 loss: 15.27073
    Epoch 11600 loss: 15.27072
    Epoch 11700 loss: 15.27070
    Epoch 11800 loss: 15.27068
    Epoch 11900 loss: 15.27067
    Epoch 12000 loss: 15.27065
    Epoch 12100 loss: 15.27063
    Epoch 12200 loss: 15.27061
    Epoch 12300 loss: 15.27060
    Epoch 12400 loss: 15.27058
    Epoch 12500 loss: 15.27057
    Epoch 12600 loss: 15.27055
    Epoch 12700 loss: 15.27053
    Epoch 12800 loss: 15.27051
    Epoch 12900 loss: 15.27050
    Epoch 13000 loss: 15.27048
    Epoch 13100 loss: 15.27047
    Epoch 13200 loss: 15.27045
    Epoch 13300 loss: 15.27043
    Epoch 13400 loss: 15.27041
    Epoch 13500 loss: 15.27040
    Epoch 13600 loss: 15.27038
    Epoch 13700 loss: 15.27036
    Epoch 13800 loss: 15.27035
    Epoch 13900 loss: 15.27033
    Epoch 14000 loss: 15.27032
    Epoch 14100 loss: 15.27029
    Epoch 14200 loss: 15.27028
    Epoch 14300 loss: 15.27026
    Epoch 14400 loss: 15.27025
    Epoch 14500 loss: 15.27023
    Epoch 14600 loss: 15.27021
    Epoch 14700 loss: 15.27020
    Epoch 14800 loss: 15.27018
    Epoch 14900 loss: 15.27017
    Epoch 15000 loss: 15.27015
    Epoch 15100 loss: 15.27013
    Epoch 15200 loss: 15.27011
    Epoch 15300 loss: 15.27010
    Epoch 15400 loss: 15.27008
    Epoch 15500 loss: 15.27007
    Epoch 15600 loss: 15.27005
    Epoch 15700 loss: 15.27003
    Epoch 15800 loss: 15.27002
    Epoch 15900 loss: 15.27000
    Epoch 16000 loss: 15.26999
    Epoch 16100 loss: 15.26997
    Epoch 16200 loss: 15.26995
    Epoch 16300 loss: 15.26993
    Epoch 16400 loss: 15.26992
    Epoch 16500 loss: 15.26990
    Epoch 16600 loss: 15.26989
    Epoch 16700 loss: 15.26987
    Epoch 16800 loss: 15.26986
    Epoch 16900 loss: 15.26984
    Epoch 17000 loss: 15.26982
    Epoch 17100 loss: 15.26981
    Epoch 17200 loss: 15.26979
    Epoch 17300 loss: 15.26977
    Epoch 17400 loss: 15.26976
    Epoch 17500 loss: 15.26974
    Epoch 17600 loss: 15.26973
    Epoch 17700 loss: 15.26971
    Epoch 17800 loss: 15.26969
    Epoch 17900 loss: 15.26968
    Epoch 18000 loss: 15.26966
    Epoch 18100 loss: 15.26965
    Epoch 18200 loss: 15.26963
    Epoch 18300 loss: 15.26962
    Epoch 18400 loss: 15.26960
    Epoch 18500 loss: 15.26958
    Epoch 18600 loss: 15.26957
    Epoch 18700 loss: 15.26955
    Epoch 18800 loss: 15.26954
    Epoch 18900 loss: 15.26952
    Epoch 19000 loss: 15.26951
    Epoch 19100 loss: 15.26949
    Epoch 19200 loss: 15.26947
    Epoch 19300 loss: 15.26946
    Epoch 19400 loss: 15.26944
    Epoch 19500 loss: 15.26943
    Epoch 19600 loss: 15.26941
    Epoch 19700 loss: 15.26939
    Epoch 19800 loss: 15.26938
    Epoch 19900 loss: 15.26936
    Epoch 20000 loss: 15.26935
    Epoch 20100 loss: 15.26933
    Epoch 20200 loss: 15.26932
    Epoch 20300 loss: 15.26930
    Epoch 20400 loss: 15.26929
    Epoch 20500 loss: 15.26927
    Epoch 20600 loss: 15.26926
    Epoch 20700 loss: 15.26924
    Epoch 20800 loss: 15.26923
    Epoch 20900 loss: 15.26921
    Epoch 21000 loss: 15.26919
    Epoch 21100 loss: 15.26918
    Epoch 21200 loss: 15.26916
    Epoch 21300 loss: 15.26915
    Epoch 21400 loss: 15.26913
    Epoch 21500 loss: 15.26912
    Epoch 21600 loss: 15.26910
    Epoch 21700 loss: 15.26909
    Epoch 21800 loss: 15.26907
    Epoch 21900 loss: 15.26906
    Epoch 22000 loss: 15.26904
    Epoch 22100 loss: 15.26903
    Epoch 22200 loss: 15.26901
    Epoch 22300 loss: 15.26900
    Epoch 22400 loss: 15.26898
    Epoch 22500 loss: 15.26897
    Epoch 22600 loss: 15.26895
    Epoch 22700 loss: 15.26894
    Epoch 22800 loss: 15.26892
    Epoch 22900 loss: 15.26891
    Epoch 23000 loss: 15.26889
    Epoch 23100 loss: 15.26888
    Epoch 23200 loss: 15.26886
    Epoch 23300 loss: 15.26885
    Epoch 23400 loss: 15.26883
    Epoch 23500 loss: 15.26881
    Epoch 23600 loss: 15.26880
    Epoch 23700 loss: 15.26879
    Epoch 23800 loss: 15.26877
    Epoch 23900 loss: 15.26875
    Epoch 24000 loss: 15.26874
    Epoch 24100 loss: 15.26873
    Epoch 24200 loss: 15.26871
    Epoch 24300 loss: 15.26870
    Epoch 24400 loss: 15.26868
    Epoch 24500 loss: 15.26867
    Epoch 24600 loss: 15.26865
    Epoch 24700 loss: 15.26864
    Epoch 24800 loss: 15.26863
    Epoch 24900 loss: 15.26861
    Epoch 25000 loss: 15.26859
    Epoch 25100 loss: 15.26858
    Epoch 25200 loss: 15.26857
    Epoch 25300 loss: 15.26855
    Epoch 25400 loss: 15.26854
    Epoch 25500 loss: 15.26852
    Epoch 25600 loss: 15.26851
    Epoch 25700 loss: 15.26849
    Epoch 25800 loss: 15.26848
    Epoch 25900 loss: 15.26846
    Epoch 26000 loss: 15.26845
    Epoch 26100 loss: 15.26844
    Epoch 26200 loss: 15.26842
    Epoch 26300 loss: 15.26840
    Epoch 26400 loss: 15.26839
    Epoch 26500 loss: 15.26838
    Epoch 26600 loss: 15.26836
    Epoch 26700 loss: 15.26835
    Epoch 26800 loss: 15.26833
    Epoch 26900 loss: 15.26832
    Epoch 27000 loss: 15.26830
    Epoch 27100 loss: 15.26829
    Epoch 27200 loss: 15.26828
    Epoch 27300 loss: 15.26826
    Epoch 27400 loss: 15.26825
    Epoch 27500 loss: 15.26824
    Epoch 27600 loss: 15.26822
    Epoch 27700 loss: 15.26821
    Epoch 27800 loss: 15.26819
    Epoch 27900 loss: 15.26818
    Epoch 28000 loss: 15.26816
    Epoch 28100 loss: 15.26815
    Epoch 28200 loss: 15.26814
    Epoch 28300 loss: 15.26812
    Epoch 28400 loss: 15.26811
    Epoch 28500 loss: 15.26809
    Epoch 28600 loss: 15.26808
    Epoch 28700 loss: 15.26806
    Epoch 28800 loss: 15.26805
    Epoch 28900 loss: 15.26804
    Epoch 29000 loss: 15.26802
    Epoch 29100 loss: 15.26801
    Epoch 29200 loss: 15.26800
    Epoch 29300 loss: 15.26798
    Epoch 29400 loss: 15.26797
    Epoch 29500 loss: 15.26795
    Epoch 29600 loss: 15.26794
    Epoch 29700 loss: 15.26793
    Epoch 29800 loss: 15.26791
    Epoch 29900 loss: 15.26790
    Epoch 30000 loss: 15.26789
    Epoch 30100 loss: 15.26787
    Epoch 30200 loss: 15.26786
    Epoch 30300 loss: 15.26785
    Epoch 30400 loss: 15.26783
    Epoch 30500 loss: 15.26782
    Epoch 30600 loss: 15.26780
    Epoch 30700 loss: 15.26779
    Epoch 30800 loss: 15.26778
    Epoch 30900 loss: 15.26776
    Epoch 31000 loss: 15.26775
    Epoch 31100 loss: 15.26774
    Epoch 31200 loss: 15.26772
    Epoch 31300 loss: 15.26771
    Epoch 31400 loss: 15.26769
    Epoch 31500 loss: 15.26768
    Epoch 31600 loss: 15.26767
    Epoch 31700 loss: 15.26766
    Epoch 31800 loss: 15.26764
    Epoch 31900 loss: 15.26763
    Epoch 32000 loss: 15.26761
    Epoch 32100 loss: 15.26760
    Epoch 32200 loss: 15.26759
    Epoch 32300 loss: 15.26757
    Epoch 32400 loss: 15.26756
    Epoch 32500 loss: 15.26755
    Epoch 32600 loss: 15.26753
    Epoch 32700 loss: 15.26752
    Epoch 32800 loss: 15.26751
    Epoch 32900 loss: 15.26749
    Epoch 33000 loss: 15.26748
    Epoch 33100 loss: 15.26747
    Epoch 33200 loss: 15.26745
    Epoch 33300 loss: 15.26744
    Epoch 33400 loss: 15.26743
    Epoch 33500 loss: 15.26741
    Epoch 33600 loss: 15.26740
    Epoch 33700 loss: 15.26739
    Epoch 33800 loss: 15.26738
    Epoch 33900 loss: 15.26736
    Epoch 34000 loss: 15.26735
    Epoch 34100 loss: 15.26733
    Epoch 34200 loss: 15.26732
    Epoch 34300 loss: 15.26731
    Epoch 34400 loss: 15.26730
    Epoch 34500 loss: 15.26728
    Epoch 34600 loss: 15.26727
    Epoch 34700 loss: 15.26726
    Epoch 34800 loss: 15.26724
    Epoch 34900 loss: 15.26723
    Epoch 35000 loss: 15.26722
    Epoch 35100 loss: 15.26720
    Epoch 35200 loss: 15.26719
    Epoch 35300 loss: 15.26718
    Epoch 35400 loss: 15.26717
    Epoch 35500 loss: 15.26715
    Epoch 35600 loss: 15.26714
    Epoch 35700 loss: 15.26713
    Epoch 35800 loss: 15.26712
    Epoch 35900 loss: 15.26710
    Epoch 36000 loss: 15.26709
    Epoch 36100 loss: 15.26707
    Epoch 36200 loss: 15.26707
    Epoch 36300 loss: 15.26705
    Epoch 36400 loss: 15.26704
    Epoch 36500 loss: 15.26702
    Epoch 36600 loss: 15.26701
    Epoch 36700 loss: 15.26700
    Epoch 36800 loss: 15.26699
    Epoch 36900 loss: 15.26697
    Epoch 37000 loss: 15.26696
    Epoch 37100 loss: 15.26695
    Epoch 37200 loss: 15.26694
    Epoch 37300 loss: 15.26692
    Epoch 37400 loss: 15.26691
    Epoch 37500 loss: 15.26690
    Epoch 37600 loss: 15.26689
    Epoch 37700 loss: 15.26687
    Epoch 37800 loss: 15.26686
    Epoch 37900 loss: 15.26685
    Epoch 38000 loss: 15.26684
    Epoch 38100 loss: 15.26682
    Epoch 38200 loss: 15.26681
    Epoch 38300 loss: 15.26680
    Epoch 38400 loss: 15.26679
    Epoch 38500 loss: 15.26677
    Epoch 38600 loss: 15.26676
    Epoch 38700 loss: 15.26675
    Epoch 38800 loss: 15.26674
    Epoch 38900 loss: 15.26673
    Epoch 39000 loss: 15.26671
    Epoch 39100 loss: 15.26670
    Epoch 39200 loss: 15.26669
    Epoch 39300 loss: 15.26667
    Epoch 39400 loss: 15.26666
    Epoch 39500 loss: 15.26665
    Epoch 39600 loss: 15.26664
    Epoch 39700 loss: 15.26663
    Epoch 39800 loss: 15.26661
    Epoch 39900 loss: 15.26660
    Epoch 40000 loss: 15.26659
    Epoch 40100 loss: 15.26657
    Epoch 40200 loss: 15.26656
    Epoch 40300 loss: 15.26655
    Epoch 40400 loss: 15.26654
    Epoch 40500 loss: 15.26653
    Epoch 40600 loss: 15.26651
    Epoch 40700 loss: 15.26650
    Epoch 40800 loss: 15.26649
    Epoch 40900 loss: 15.26648
    Epoch 41000 loss: 15.26647
    Epoch 41100 loss: 15.26645
    Epoch 41200 loss: 15.26644
    Epoch 41300 loss: 15.26643
    Epoch 41400 loss: 15.26642
    Epoch 41500 loss: 15.26641
    Epoch 41600 loss: 15.26639
    Epoch 41700 loss: 15.26638
    Epoch 41800 loss: 15.26637
    Epoch 41900 loss: 15.26636
    Epoch 42000 loss: 15.26635
    Epoch 42100 loss: 15.26633
    Epoch 42200 loss: 15.26632
    Epoch 42300 loss: 15.26631
    Epoch 42400 loss: 15.26630
    Epoch 42500 loss: 15.26629
    Epoch 42600 loss: 15.26627
    Epoch 42700 loss: 15.26626
    Epoch 42800 loss: 15.26625
    Epoch 42900 loss: 15.26624
    Epoch 43000 loss: 15.26623
    Epoch 43100 loss: 15.26621
    Epoch 43200 loss: 15.26620
    Epoch 43300 loss: 15.26619
    Epoch 43400 loss: 15.26618
    Epoch 43500 loss: 15.26617
    Epoch 43600 loss: 15.26616
    Epoch 43700 loss: 15.26615
    Epoch 43800 loss: 15.26613
    Epoch 43900 loss: 15.26612
    Epoch 44000 loss: 15.26611
    Epoch 44100 loss: 15.26610
    Epoch 44200 loss: 15.26609
    Epoch 44300 loss: 15.26608
    Epoch 44400 loss: 15.26606
    Epoch 44500 loss: 15.26605
    Epoch 44600 loss: 15.26604
    Epoch 44700 loss: 15.26603
    Epoch 44800 loss: 15.26602
    Epoch 44900 loss: 15.26601
    Epoch 45000 loss: 15.26600
    Epoch 45100 loss: 15.26598
    Epoch 45200 loss: 15.26597
    Epoch 45300 loss: 15.26596
    Epoch 45400 loss: 15.26595
    Epoch 45500 loss: 15.26594
    Epoch 45600 loss: 15.26592
    Epoch 45700 loss: 15.26592
    Epoch 45800 loss: 15.26590
    Epoch 45900 loss: 15.26589
    Epoch 46000 loss: 15.26588
    Epoch 46100 loss: 15.26587
    Epoch 46200 loss: 15.26586
    Epoch 46300 loss: 15.26585
    Epoch 46400 loss: 15.26584
    Epoch 46500 loss: 15.26582
    Epoch 46600 loss: 15.26581
    Epoch 46700 loss: 15.26580
    Epoch 46800 loss: 15.26579
    Epoch 46900 loss: 15.26578
    Epoch 47000 loss: 15.26577
    Epoch 47100 loss: 15.26576
    Epoch 47200 loss: 15.26574
    Epoch 47300 loss: 15.26573
    Epoch 47400 loss: 15.26572
    Epoch 47500 loss: 15.26571
    Epoch 47600 loss: 15.26570
    Epoch 47700 loss: 15.26569
    Epoch 47800 loss: 15.26568
    Epoch 47900 loss: 15.26567
    Epoch 48000 loss: 15.26566
    Epoch 48100 loss: 15.26564
    Epoch 48200 loss: 15.26563
    Epoch 48300 loss: 15.26562
    Epoch 48400 loss: 15.26561
    Epoch 48500 loss: 15.26560
    Epoch 48600 loss: 15.26559
    Epoch 48700 loss: 15.26558
    Epoch 48800 loss: 15.26557
    Epoch 48900 loss: 15.26556
    Epoch 49000 loss: 15.26554
    Epoch 49100 loss: 15.26554
    Epoch 49200 loss: 15.26552
    Epoch 49300 loss: 15.26551
    Epoch 49400 loss: 15.26550
    Epoch 49500 loss: 15.26549
    Epoch 49600 loss: 15.26548
    Epoch 49700 loss: 15.26547
    Epoch 49800 loss: 15.26546
    Epoch 49900 loss: 15.26545



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_7%EC%B0%A8%EC%8B%9C__Regression__62_0.webp)
    



## 강의_3기_AI개론_8차시__Binary_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_8차시__Binary_.ipynb)

# 8장 이진 분류 (Binary classification)

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    debconf: unable to initialize frontend: Dialog
    debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 78, <> line 4.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Processing triggers for fontconfig (2.13.1-4.2ubuntu5) ...
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 39 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /usr/share/fonts/truetype: skipping, looped directory detected
    /usr/share/fonts/truetype/humor-sans: skipping, looped directory detected
    /usr/share/fonts/truetype/liberation: skipping, looped directory detected
    /usr/share/fonts/truetype/nanum: skipping, looped directory detected
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3
    Successfully installed torchinfo-1.8.0


* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 폰트 관련 용도
import matplotlib.font_manager as fm

# Colab, Linux
# 나눔 고딕 폰트의 경로 명시
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```


```python
# 파이토치 관련 라이브러리
import torch
from torch import nn, optim
import torch.nn.functional as F
from torchviz import make_dot
from torchinfo import summary

# Iris dataset
import pandas  as pd
# from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
```


```python
# 기본 폰트 설정
plt.rcParams['font.family'] = font_name

# 기본 폰트 사이즈 변경
plt.rcParams['font.size'] = 14

# 기본 그래프 사이즈 변경
plt.rcParams['figure.figsize'] = (6,6)

# 기본 그리드 표시
# 필요에 따라 설정할 때는, plt.grid()
plt.rcParams['axes.grid'] = True
plt.rcParams["grid.linestyle"] = ":"

# 마이너스 기호 정상 출력
plt.rcParams['axes.unicode_minus'] = False

# 넘파이 부동소수점 자릿수 표시
np.set_printoptions(suppress=True, precision=4)
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')
```

## Iris data 분석

### 데이터 준비


```python
# 학습용 데이터 준비
# 라이브러리 임포트
# import sklearn


# 데이터 불러오기
iris = load_iris()
print(iris.keys())

# 입력 데이터와 정답 데이터
x_org, y_org = iris.data, iris.target

# 결과 확인
print('원본 데이터', x_org.shape, y_org.shape)
```

    dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
    원본 데이터 (150, 4) (150,)



```python
# 데이터 추출
# 클래스는 0 또는 1
# 항목은 sepal_length와 sepal_width

x_data = iris.data[:100,:2] # 2-dim
y_data = iris.target[:100] # 1-dim

print("x data = \n", x_data[:10])
print("y data = \n", y_data[:10])
print("feature names = ", iris.feature_names[:2])
# 결과 확인
print('대상 데이터', x_data.shape, y_data.shape)
```

    x data = 
     [[5.1 3.5]
     [4.9 3. ]
     [4.7 3.2]
     [4.6 3.1]
     [5.  3.6]
     [5.4 3.9]
     [4.6 3.4]
     [5.  3.4]
     [4.4 2.9]
     [4.9 3.1]]
    y data = 
     [0 0 0 0 0 0 0 0 0 0]
    feature names =  ['sepal length (cm)', 'sepal width (cm)']
    대상 데이터 (100, 2) (100,)


### 훈련 데이터와 검증 데이터 분할


```python
# 원본 데이터의 사이즈
print("Original data shape = ")
print(x_data.shape, y_data.shape)

# 훈련 데이터와 검증 데이터로 분할(동시에 셔플)

x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, train_size=70, test_size=30, random_state=123)

print("x_train, x_test, y_train, y_test :")
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
```

    Original data shape = 
    (100, 2) (100,)
    x_train, x_test, y_train, y_test :
    (70, 2) (30, 2) (70,) (30,)


### 산포도 출력


```python
# 산포도 출력

x_t0 = x_train[y_train == 0]
x_t1 = x_train[y_train == 1]
plt.scatter(x_t0[:,0], x_t0[:,1], marker='x', c='b', label='0 (setosa)')
plt.scatter(x_t1[:,0], x_t1[:,1], marker='o', c='k', label='1 (versicolor)')
plt.xlabel('sepal_length')
plt.ylabel('sepal_width')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__16_0.webp)
    


### 모델 정의


```python
# 입력 차원수(지금의 경우는 2)
n_input= x_train.shape[1]

# 출력 차원수
n_output = 1

# 결과 확인
print(f'n_input: {n_input}  n_output:{n_output}')
```

    n_input: 2  n_output:1



```python
# 모델 정의
# 2입력 1출력 로지스틱 회귀 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        super().__init__()
        self.l1 = nn.Linear(n_input, n_output)
        self.sigmoid = nn.Sigmoid()

        # 초깃값을 전부 1로 함
        # "딥러닝을 위한 수학"과 조건을 맞추기 위한 목적
        # self.l1.weight.data.fill_(1.0)
        # self.l1.bias.data.fill_(1.0)

        nn.init.constant_(self.l1.weight, 1.0)
        nn.init.constant_(self.l1.bias, 1.0)


    # 예측 함수 정의
    def forward(self, x):
        # 선형 함수에 입력값을 넣고 계산한 결과
        x1 = self.l1(x)
        # 계산 결과에 시그모이드 함수를 적용
        x2 = self.sigmoid(x1)
        return x2
```


```python
# 인스턴스 생성

net = Net(n_input, n_output)
```

### 모델 확인


```python
# 모델 안의 파라미터 확인
# l1.weight와 l1.bias가 존재함을 알 수 있음

for parameter in net.named_parameters():
    print(parameter[1])
```

    Parameter containing:
    tensor([[1., 1.]], requires_grad=True)
    Parameter containing:
    tensor([1.], requires_grad=True)



```python
# 모델의 개요 표시 1

print(net)

# 모델의 개요 표시 2
print("="*50)
summary(net, (2,), device = "cpu") # device default = "cuda"
```

    Net(
      (l1): Linear(in_features=2, out_features=1, bias=True)
      (sigmoid): Sigmoid()
    )
    ==================================================





    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [1]                       --
    ├─Linear: 1-1                            [1]                       3
    ├─Sigmoid: 1-2                           [1]                       --
    ==========================================================================================
    Total params: 3
    Trainable params: 3
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 0.00
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.00
    Estimated Total Size (MB): 0.00
    ==========================================================================================



### 최적화 알고리즘과 손실 함수의 정의


```python
for parameter in net.parameters():
    print(parameter)
```

    Parameter containing:
    tensor([[1., 1.]], requires_grad=True)
    Parameter containing:
    tensor([1.], requires_grad=True)



```python
# 손실 함수： 교차 엔트로피 함수
loss = nn.BCELoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)
```

### 경사 하강법


```python
# 입력 데이터 x_train과 정답 데이터 y_train의 텐서화

inputs = torch.tensor(x_train).float()
labels = torch.tensor(y_train).float()

# 정답 데이터는 N행 1열 행렬로 변환
labels1 = labels.view((-1,1))
print("labels1 shape = ", labels1.shape)

# 검증 데이터의 텐서화
inputs_test = torch.tensor(x_test).float()
labels_test = torch.tensor(y_test).float()

# 검증용 정답 데이터도 N행 1열 행렬로 변환
labels1_test = labels_test.view((-1,1))
```

    labels1 shape =  torch.Size([70, 1])



```python
# 예측 계산
outputs = net(inputs) # outputs.shape = torch.Size([70, 1])

# 손실 계산
cost = loss(outputs, labels1)

# 손실을 계산 그래프로 출력
g = make_dot(cost, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__29_0.svg)
    


### 반복 계산 (Iterative learning)


```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수
criterion = nn.BCELoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 기록용 리스트 초기화
history = np.zeros((0,5))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):
    # 훈련 페이즈

    # 경삿값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels1)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 손실 저장(스칼라 값 취득)
    train_loss = loss.item()

    # 예측 라벨(1 또는 0) 계산
    predicted = torch.where(outputs < 0.5, 0, 1)

    # 정확도 계산
    train_acc = (predicted == labels1).sum() / len(y_train)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 손실 계산
    loss_test = criterion(outputs_test, labels1_test)

    # 손실 저장(스칼라 값 취득)
    val_loss =  loss_test.item()

    # 예측 라벨(1 또는 0) 계산
    predicted_test = torch.where(outputs_test < 0.5, 0, 1)

    # 정확도 계산
    val_acc = (predicted_test == labels1_test).sum() / len(y_test)

    if ( epoch % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch, train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```

    Epoch [0/10000], loss: 4.77289 acc: 0.50000 val_loss: 4.49384, val_acc: 0.50000
    Epoch [10/10000], loss: 3.80546 acc: 0.50000 val_loss: 3.56537, val_acc: 0.50000
    Epoch [20/10000], loss: 2.84329 acc: 0.50000 val_loss: 2.64328, val_acc: 0.50000
    Epoch [30/10000], loss: 1.91613 acc: 0.50000 val_loss: 1.76244, val_acc: 0.50000
    Epoch [40/10000], loss: 1.17137 acc: 0.50000 val_loss: 1.08537, val_acc: 0.50000
    Epoch [50/10000], loss: 0.84140 acc: 0.50000 val_loss: 0.81872, val_acc: 0.50000
    Epoch [60/10000], loss: 0.77087 acc: 0.50000 val_loss: 0.77093, val_acc: 0.50000
    Epoch [70/10000], loss: 0.75450 acc: 0.34286 val_loss: 0.76105, val_acc: 0.33333
    Epoch [80/10000], loss: 0.74542 acc: 0.25714 val_loss: 0.75447, val_acc: 0.20000
    Epoch [90/10000], loss: 0.73734 acc: 0.24286 val_loss: 0.74778, val_acc: 0.16667
    Epoch [100/10000], loss: 0.72949 acc: 0.24286 val_loss: 0.74098, val_acc: 0.13333
    Epoch [110/10000], loss: 0.72180 acc: 0.27143 val_loss: 0.73419, val_acc: 0.16667
    Epoch [120/10000], loss: 0.71423 acc: 0.31429 val_loss: 0.72749, val_acc: 0.20000
    Epoch [130/10000], loss: 0.70680 acc: 0.41429 val_loss: 0.72087, val_acc: 0.20000
    Epoch [140/10000], loss: 0.69949 acc: 0.47143 val_loss: 0.71437, val_acc: 0.26667
    Epoch [150/10000], loss: 0.69230 acc: 0.52857 val_loss: 0.70797, val_acc: 0.30000
    Epoch [160/10000], loss: 0.68524 acc: 0.60000 val_loss: 0.70167, val_acc: 0.36667
    Epoch [170/10000], loss: 0.67829 acc: 0.62857 val_loss: 0.69548, val_acc: 0.43333
    Epoch [180/10000], loss: 0.67147 acc: 0.68571 val_loss: 0.68938, val_acc: 0.50000
    Epoch [190/10000], loss: 0.66476 acc: 0.75714 val_loss: 0.68339, val_acc: 0.56667
    Epoch [200/10000], loss: 0.65816 acc: 0.81429 val_loss: 0.67749, val_acc: 0.70000
    Epoch [210/10000], loss: 0.65168 acc: 0.84286 val_loss: 0.67169, val_acc: 0.70000
    Epoch [220/10000], loss: 0.64531 acc: 0.85714 val_loss: 0.66599, val_acc: 0.73333
    Epoch [230/10000], loss: 0.63904 acc: 0.85714 val_loss: 0.66037, val_acc: 0.76667
    Epoch [240/10000], loss: 0.63288 acc: 0.88571 val_loss: 0.65485, val_acc: 0.80000
    Epoch [250/10000], loss: 0.62682 acc: 0.88571 val_loss: 0.64942, val_acc: 0.83333
    Epoch [260/10000], loss: 0.62087 acc: 0.90000 val_loss: 0.64408, val_acc: 0.83333
    Epoch [270/10000], loss: 0.61501 acc: 0.91429 val_loss: 0.63882, val_acc: 0.83333
    Epoch [280/10000], loss: 0.60925 acc: 0.92857 val_loss: 0.63364, val_acc: 0.86667
    Epoch [290/10000], loss: 0.60359 acc: 0.94286 val_loss: 0.62855, val_acc: 0.90000
    Epoch [300/10000], loss: 0.59803 acc: 0.94286 val_loss: 0.62354, val_acc: 0.90000
    Epoch [310/10000], loss: 0.59255 acc: 0.94286 val_loss: 0.61861, val_acc: 0.90000
    Epoch [320/10000], loss: 0.58717 acc: 0.94286 val_loss: 0.61376, val_acc: 0.93333
    Epoch [330/10000], loss: 0.58187 acc: 0.94286 val_loss: 0.60899, val_acc: 0.93333
    Epoch [340/10000], loss: 0.57667 acc: 0.97143 val_loss: 0.60429, val_acc: 0.93333
    Epoch [350/10000], loss: 0.57154 acc: 0.97143 val_loss: 0.59967, val_acc: 0.93333
    Epoch [360/10000], loss: 0.56650 acc: 0.97143 val_loss: 0.59512, val_acc: 0.93333
    Epoch [370/10000], loss: 0.56155 acc: 0.98571 val_loss: 0.59064, val_acc: 0.93333
    Epoch [380/10000], loss: 0.55667 acc: 0.98571 val_loss: 0.58623, val_acc: 0.93333
    Epoch [390/10000], loss: 0.55188 acc: 0.98571 val_loss: 0.58189, val_acc: 0.93333
    Epoch [400/10000], loss: 0.54716 acc: 0.98571 val_loss: 0.57762, val_acc: 0.93333
    Epoch [410/10000], loss: 0.54251 acc: 0.98571 val_loss: 0.57341, val_acc: 0.93333
    Epoch [420/10000], loss: 0.53795 acc: 0.98571 val_loss: 0.56927, val_acc: 0.93333
    Epoch [430/10000], loss: 0.53345 acc: 1.00000 val_loss: 0.56519, val_acc: 0.93333
    Epoch [440/10000], loss: 0.52902 acc: 1.00000 val_loss: 0.56117, val_acc: 0.93333
    Epoch [450/10000], loss: 0.52467 acc: 1.00000 val_loss: 0.55722, val_acc: 0.93333
    Epoch [460/10000], loss: 0.52038 acc: 1.00000 val_loss: 0.55333, val_acc: 0.93333
    Epoch [470/10000], loss: 0.51617 acc: 1.00000 val_loss: 0.54949, val_acc: 0.93333
    Epoch [480/10000], loss: 0.51201 acc: 1.00000 val_loss: 0.54571, val_acc: 0.93333
    Epoch [490/10000], loss: 0.50793 acc: 1.00000 val_loss: 0.54199, val_acc: 0.93333
    Epoch [500/10000], loss: 0.50390 acc: 1.00000 val_loss: 0.53833, val_acc: 0.93333
    Epoch [510/10000], loss: 0.49994 acc: 1.00000 val_loss: 0.53472, val_acc: 0.93333
    Epoch [520/10000], loss: 0.49604 acc: 1.00000 val_loss: 0.53116, val_acc: 0.93333
    Epoch [530/10000], loss: 0.49219 acc: 1.00000 val_loss: 0.52766, val_acc: 0.93333
    Epoch [540/10000], loss: 0.48841 acc: 1.00000 val_loss: 0.52421, val_acc: 0.93333
    Epoch [550/10000], loss: 0.48468 acc: 1.00000 val_loss: 0.52080, val_acc: 0.93333
    Epoch [560/10000], loss: 0.48101 acc: 1.00000 val_loss: 0.51745, val_acc: 0.93333
    Epoch [570/10000], loss: 0.47740 acc: 1.00000 val_loss: 0.51415, val_acc: 0.93333
    Epoch [580/10000], loss: 0.47384 acc: 1.00000 val_loss: 0.51089, val_acc: 0.93333
    Epoch [590/10000], loss: 0.47033 acc: 1.00000 val_loss: 0.50769, val_acc: 0.93333
    Epoch [600/10000], loss: 0.46687 acc: 1.00000 val_loss: 0.50452, val_acc: 0.93333
    Epoch [610/10000], loss: 0.46347 acc: 1.00000 val_loss: 0.50141, val_acc: 0.93333
    Epoch [620/10000], loss: 0.46011 acc: 1.00000 val_loss: 0.49833, val_acc: 0.93333
    Epoch [630/10000], loss: 0.45680 acc: 1.00000 val_loss: 0.49530, val_acc: 0.93333
    Epoch [640/10000], loss: 0.45355 acc: 1.00000 val_loss: 0.49232, val_acc: 0.93333
    Epoch [650/10000], loss: 0.45033 acc: 1.00000 val_loss: 0.48937, val_acc: 0.93333
    Epoch [660/10000], loss: 0.44717 acc: 1.00000 val_loss: 0.48647, val_acc: 0.93333
    Epoch [670/10000], loss: 0.44405 acc: 1.00000 val_loss: 0.48360, val_acc: 0.93333
    Epoch [680/10000], loss: 0.44097 acc: 1.00000 val_loss: 0.48078, val_acc: 0.93333
    Epoch [690/10000], loss: 0.43794 acc: 1.00000 val_loss: 0.47800, val_acc: 0.93333
    Epoch [700/10000], loss: 0.43495 acc: 1.00000 val_loss: 0.47525, val_acc: 0.93333
    Epoch [710/10000], loss: 0.43200 acc: 1.00000 val_loss: 0.47254, val_acc: 0.93333
    Epoch [720/10000], loss: 0.42909 acc: 1.00000 val_loss: 0.46987, val_acc: 0.93333
    Epoch [730/10000], loss: 0.42623 acc: 1.00000 val_loss: 0.46723, val_acc: 0.93333
    Epoch [740/10000], loss: 0.42340 acc: 1.00000 val_loss: 0.46463, val_acc: 0.93333
    Epoch [750/10000], loss: 0.42061 acc: 1.00000 val_loss: 0.46206, val_acc: 0.93333
    Epoch [760/10000], loss: 0.41786 acc: 1.00000 val_loss: 0.45953, val_acc: 0.93333
    Epoch [770/10000], loss: 0.41515 acc: 1.00000 val_loss: 0.45703, val_acc: 0.93333
    Epoch [780/10000], loss: 0.41247 acc: 1.00000 val_loss: 0.45457, val_acc: 0.93333
    Epoch [790/10000], loss: 0.40983 acc: 1.00000 val_loss: 0.45213, val_acc: 0.93333
    Epoch [800/10000], loss: 0.40722 acc: 1.00000 val_loss: 0.44973, val_acc: 0.93333
    Epoch [810/10000], loss: 0.40465 acc: 1.00000 val_loss: 0.44736, val_acc: 0.93333
    Epoch [820/10000], loss: 0.40211 acc: 1.00000 val_loss: 0.44502, val_acc: 0.93333
    Epoch [830/10000], loss: 0.39961 acc: 1.00000 val_loss: 0.44271, val_acc: 0.93333
    Epoch [840/10000], loss: 0.39714 acc: 1.00000 val_loss: 0.44043, val_acc: 0.93333
    Epoch [850/10000], loss: 0.39470 acc: 1.00000 val_loss: 0.43818, val_acc: 0.93333
    Epoch [860/10000], loss: 0.39229 acc: 1.00000 val_loss: 0.43596, val_acc: 0.93333
    Epoch [870/10000], loss: 0.38992 acc: 1.00000 val_loss: 0.43377, val_acc: 0.93333
    Epoch [880/10000], loss: 0.38757 acc: 1.00000 val_loss: 0.43160, val_acc: 0.93333
    Epoch [890/10000], loss: 0.38525 acc: 1.00000 val_loss: 0.42946, val_acc: 0.96667
    Epoch [900/10000], loss: 0.38297 acc: 1.00000 val_loss: 0.42735, val_acc: 0.96667
    Epoch [910/10000], loss: 0.38071 acc: 1.00000 val_loss: 0.42526, val_acc: 0.96667
    Epoch [920/10000], loss: 0.37848 acc: 1.00000 val_loss: 0.42320, val_acc: 0.96667
    Epoch [930/10000], loss: 0.37628 acc: 1.00000 val_loss: 0.42116, val_acc: 0.96667
    Epoch [940/10000], loss: 0.37410 acc: 1.00000 val_loss: 0.41915, val_acc: 0.96667
    Epoch [950/10000], loss: 0.37196 acc: 1.00000 val_loss: 0.41717, val_acc: 0.96667
    Epoch [960/10000], loss: 0.36983 acc: 1.00000 val_loss: 0.41520, val_acc: 0.96667
    Epoch [970/10000], loss: 0.36774 acc: 1.00000 val_loss: 0.41327, val_acc: 0.96667
    Epoch [980/10000], loss: 0.36567 acc: 1.00000 val_loss: 0.41135, val_acc: 0.96667
    Epoch [990/10000], loss: 0.36362 acc: 1.00000 val_loss: 0.40946, val_acc: 0.96667
    Epoch [1000/10000], loss: 0.36160 acc: 1.00000 val_loss: 0.40759, val_acc: 0.96667
    Epoch [1010/10000], loss: 0.35961 acc: 1.00000 val_loss: 0.40574, val_acc: 0.96667
    Epoch [1020/10000], loss: 0.35763 acc: 1.00000 val_loss: 0.40391, val_acc: 0.96667
    Epoch [1030/10000], loss: 0.35568 acc: 1.00000 val_loss: 0.40211, val_acc: 0.96667
    Epoch [1040/10000], loss: 0.35376 acc: 1.00000 val_loss: 0.40032, val_acc: 0.96667
    Epoch [1050/10000], loss: 0.35186 acc: 1.00000 val_loss: 0.39856, val_acc: 0.96667
    Epoch [1060/10000], loss: 0.34997 acc: 1.00000 val_loss: 0.39682, val_acc: 0.96667
    Epoch [1070/10000], loss: 0.34811 acc: 1.00000 val_loss: 0.39509, val_acc: 0.96667
    Epoch [1080/10000], loss: 0.34628 acc: 1.00000 val_loss: 0.39339, val_acc: 0.96667
    Epoch [1090/10000], loss: 0.34446 acc: 1.00000 val_loss: 0.39171, val_acc: 0.96667
    Epoch [1100/10000], loss: 0.34266 acc: 1.00000 val_loss: 0.39004, val_acc: 0.96667
    Epoch [1110/10000], loss: 0.34089 acc: 1.00000 val_loss: 0.38839, val_acc: 0.96667
    Epoch [1120/10000], loss: 0.33913 acc: 1.00000 val_loss: 0.38677, val_acc: 0.96667
    Epoch [1130/10000], loss: 0.33739 acc: 1.00000 val_loss: 0.38516, val_acc: 0.96667
    Epoch [1140/10000], loss: 0.33568 acc: 1.00000 val_loss: 0.38357, val_acc: 0.96667
    Epoch [1150/10000], loss: 0.33398 acc: 1.00000 val_loss: 0.38199, val_acc: 0.96667
    Epoch [1160/10000], loss: 0.33230 acc: 1.00000 val_loss: 0.38043, val_acc: 0.96667
    Epoch [1170/10000], loss: 0.33064 acc: 1.00000 val_loss: 0.37889, val_acc: 0.96667
    Epoch [1180/10000], loss: 0.32900 acc: 1.00000 val_loss: 0.37737, val_acc: 0.96667
    Epoch [1190/10000], loss: 0.32737 acc: 1.00000 val_loss: 0.37586, val_acc: 0.96667
    Epoch [1200/10000], loss: 0.32577 acc: 1.00000 val_loss: 0.37437, val_acc: 0.96667
    Epoch [1210/10000], loss: 0.32418 acc: 1.00000 val_loss: 0.37290, val_acc: 0.96667
    Epoch [1220/10000], loss: 0.32260 acc: 1.00000 val_loss: 0.37144, val_acc: 0.96667
    Epoch [1230/10000], loss: 0.32105 acc: 1.00000 val_loss: 0.37000, val_acc: 0.96667
    Epoch [1240/10000], loss: 0.31951 acc: 1.00000 val_loss: 0.36857, val_acc: 0.96667
    Epoch [1250/10000], loss: 0.31799 acc: 1.00000 val_loss: 0.36716, val_acc: 0.96667
    Epoch [1260/10000], loss: 0.31648 acc: 1.00000 val_loss: 0.36576, val_acc: 0.96667
    Epoch [1270/10000], loss: 0.31499 acc: 1.00000 val_loss: 0.36437, val_acc: 0.96667
    Epoch [1280/10000], loss: 0.31351 acc: 1.00000 val_loss: 0.36301, val_acc: 0.96667
    Epoch [1290/10000], loss: 0.31205 acc: 1.00000 val_loss: 0.36165, val_acc: 0.96667
    Epoch [1300/10000], loss: 0.31061 acc: 1.00000 val_loss: 0.36031, val_acc: 0.96667
    Epoch [1310/10000], loss: 0.30918 acc: 1.00000 val_loss: 0.35898, val_acc: 0.96667
    Epoch [1320/10000], loss: 0.30776 acc: 1.00000 val_loss: 0.35767, val_acc: 0.96667
    Epoch [1330/10000], loss: 0.30636 acc: 1.00000 val_loss: 0.35637, val_acc: 0.96667
    Epoch [1340/10000], loss: 0.30498 acc: 1.00000 val_loss: 0.35508, val_acc: 0.96667
    Epoch [1350/10000], loss: 0.30360 acc: 1.00000 val_loss: 0.35381, val_acc: 0.96667
    Epoch [1360/10000], loss: 0.30224 acc: 1.00000 val_loss: 0.35255, val_acc: 0.96667
    Epoch [1370/10000], loss: 0.30090 acc: 1.00000 val_loss: 0.35130, val_acc: 0.96667
    Epoch [1380/10000], loss: 0.29957 acc: 1.00000 val_loss: 0.35006, val_acc: 0.96667
    Epoch [1390/10000], loss: 0.29825 acc: 1.00000 val_loss: 0.34884, val_acc: 0.96667
    Epoch [1400/10000], loss: 0.29694 acc: 1.00000 val_loss: 0.34763, val_acc: 0.96667
    Epoch [1410/10000], loss: 0.29565 acc: 1.00000 val_loss: 0.34643, val_acc: 0.96667
    Epoch [1420/10000], loss: 0.29437 acc: 1.00000 val_loss: 0.34524, val_acc: 0.96667
    Epoch [1430/10000], loss: 0.29310 acc: 1.00000 val_loss: 0.34406, val_acc: 0.96667
    Epoch [1440/10000], loss: 0.29184 acc: 1.00000 val_loss: 0.34290, val_acc: 0.96667
    Epoch [1450/10000], loss: 0.29060 acc: 1.00000 val_loss: 0.34174, val_acc: 0.96667
    Epoch [1460/10000], loss: 0.28937 acc: 1.00000 val_loss: 0.34060, val_acc: 0.96667
    Epoch [1470/10000], loss: 0.28815 acc: 1.00000 val_loss: 0.33947, val_acc: 0.96667
    Epoch [1480/10000], loss: 0.28694 acc: 1.00000 val_loss: 0.33834, val_acc: 0.96667
    Epoch [1490/10000], loss: 0.28574 acc: 1.00000 val_loss: 0.33723, val_acc: 0.96667
    Epoch [1500/10000], loss: 0.28456 acc: 1.00000 val_loss: 0.33613, val_acc: 0.96667
    Epoch [1510/10000], loss: 0.28338 acc: 1.00000 val_loss: 0.33504, val_acc: 0.96667
    Epoch [1520/10000], loss: 0.28222 acc: 1.00000 val_loss: 0.33396, val_acc: 0.96667
    Epoch [1530/10000], loss: 0.28106 acc: 1.00000 val_loss: 0.33289, val_acc: 0.96667
    Epoch [1540/10000], loss: 0.27992 acc: 1.00000 val_loss: 0.33183, val_acc: 0.96667
    Epoch [1550/10000], loss: 0.27879 acc: 1.00000 val_loss: 0.33078, val_acc: 0.96667
    Epoch [1560/10000], loss: 0.27767 acc: 1.00000 val_loss: 0.32974, val_acc: 0.96667
    Epoch [1570/10000], loss: 0.27656 acc: 1.00000 val_loss: 0.32871, val_acc: 0.96667
    Epoch [1580/10000], loss: 0.27545 acc: 1.00000 val_loss: 0.32769, val_acc: 0.96667
    Epoch [1590/10000], loss: 0.27436 acc: 1.00000 val_loss: 0.32668, val_acc: 0.96667
    Epoch [1600/10000], loss: 0.27328 acc: 1.00000 val_loss: 0.32568, val_acc: 0.96667
    Epoch [1610/10000], loss: 0.27221 acc: 1.00000 val_loss: 0.32468, val_acc: 0.96667
    Epoch [1620/10000], loss: 0.27115 acc: 1.00000 val_loss: 0.32370, val_acc: 0.96667
    Epoch [1630/10000], loss: 0.27009 acc: 1.00000 val_loss: 0.32272, val_acc: 0.96667
    Epoch [1640/10000], loss: 0.26905 acc: 1.00000 val_loss: 0.32175, val_acc: 0.96667
    Epoch [1650/10000], loss: 0.26802 acc: 1.00000 val_loss: 0.32080, val_acc: 0.96667
    Epoch [1660/10000], loss: 0.26699 acc: 1.00000 val_loss: 0.31985, val_acc: 0.96667
    Epoch [1670/10000], loss: 0.26597 acc: 1.00000 val_loss: 0.31890, val_acc: 0.96667
    Epoch [1680/10000], loss: 0.26497 acc: 1.00000 val_loss: 0.31797, val_acc: 0.96667
    Epoch [1690/10000], loss: 0.26397 acc: 1.00000 val_loss: 0.31704, val_acc: 0.96667
    Epoch [1700/10000], loss: 0.26298 acc: 1.00000 val_loss: 0.31613, val_acc: 0.96667
    Epoch [1710/10000], loss: 0.26199 acc: 1.00000 val_loss: 0.31522, val_acc: 0.96667
    Epoch [1720/10000], loss: 0.26102 acc: 1.00000 val_loss: 0.31431, val_acc: 0.96667
    Epoch [1730/10000], loss: 0.26005 acc: 1.00000 val_loss: 0.31342, val_acc: 0.96667
    Epoch [1740/10000], loss: 0.25910 acc: 1.00000 val_loss: 0.31253, val_acc: 0.96667
    Epoch [1750/10000], loss: 0.25815 acc: 1.00000 val_loss: 0.31165, val_acc: 0.96667
    Epoch [1760/10000], loss: 0.25721 acc: 1.00000 val_loss: 0.31078, val_acc: 0.96667
    Epoch [1770/10000], loss: 0.25627 acc: 1.00000 val_loss: 0.30992, val_acc: 0.96667
    Epoch [1780/10000], loss: 0.25535 acc: 1.00000 val_loss: 0.30906, val_acc: 0.96667
    Epoch [1790/10000], loss: 0.25443 acc: 1.00000 val_loss: 0.30821, val_acc: 0.96667
    Epoch [1800/10000], loss: 0.25352 acc: 1.00000 val_loss: 0.30737, val_acc: 0.96667
    Epoch [1810/10000], loss: 0.25262 acc: 1.00000 val_loss: 0.30653, val_acc: 0.96667
    Epoch [1820/10000], loss: 0.25172 acc: 1.00000 val_loss: 0.30571, val_acc: 0.96667
    Epoch [1830/10000], loss: 0.25083 acc: 1.00000 val_loss: 0.30488, val_acc: 0.96667
    Epoch [1840/10000], loss: 0.24995 acc: 1.00000 val_loss: 0.30407, val_acc: 0.96667
    Epoch [1850/10000], loss: 0.24908 acc: 1.00000 val_loss: 0.30326, val_acc: 0.96667
    Epoch [1860/10000], loss: 0.24821 acc: 1.00000 val_loss: 0.30246, val_acc: 0.96667
    Epoch [1870/10000], loss: 0.24735 acc: 1.00000 val_loss: 0.30166, val_acc: 0.96667
    Epoch [1880/10000], loss: 0.24650 acc: 1.00000 val_loss: 0.30088, val_acc: 0.96667
    Epoch [1890/10000], loss: 0.24565 acc: 1.00000 val_loss: 0.30009, val_acc: 0.96667
    Epoch [1900/10000], loss: 0.24481 acc: 1.00000 val_loss: 0.29932, val_acc: 0.96667
    Epoch [1910/10000], loss: 0.24398 acc: 1.00000 val_loss: 0.29855, val_acc: 0.96667
    Epoch [1920/10000], loss: 0.24315 acc: 1.00000 val_loss: 0.29778, val_acc: 0.96667
    Epoch [1930/10000], loss: 0.24233 acc: 1.00000 val_loss: 0.29702, val_acc: 0.96667
    Epoch [1940/10000], loss: 0.24152 acc: 1.00000 val_loss: 0.29627, val_acc: 0.96667
    Epoch [1950/10000], loss: 0.24071 acc: 1.00000 val_loss: 0.29553, val_acc: 0.96667
    Epoch [1960/10000], loss: 0.23991 acc: 1.00000 val_loss: 0.29479, val_acc: 0.96667
    Epoch [1970/10000], loss: 0.23911 acc: 1.00000 val_loss: 0.29405, val_acc: 0.96667
    Epoch [1980/10000], loss: 0.23833 acc: 1.00000 val_loss: 0.29332, val_acc: 0.96667
    Epoch [1990/10000], loss: 0.23754 acc: 1.00000 val_loss: 0.29260, val_acc: 0.96667
    Epoch [2000/10000], loss: 0.23677 acc: 1.00000 val_loss: 0.29188, val_acc: 0.96667
    Epoch [2010/10000], loss: 0.23599 acc: 1.00000 val_loss: 0.29117, val_acc: 0.96667
    Epoch [2020/10000], loss: 0.23523 acc: 1.00000 val_loss: 0.29047, val_acc: 0.96667
    Epoch [2030/10000], loss: 0.23447 acc: 1.00000 val_loss: 0.28977, val_acc: 0.96667
    Epoch [2040/10000], loss: 0.23372 acc: 1.00000 val_loss: 0.28907, val_acc: 0.96667
    Epoch [2050/10000], loss: 0.23297 acc: 1.00000 val_loss: 0.28838, val_acc: 0.96667
    Epoch [2060/10000], loss: 0.23223 acc: 1.00000 val_loss: 0.28770, val_acc: 0.96667
    Epoch [2070/10000], loss: 0.23149 acc: 1.00000 val_loss: 0.28702, val_acc: 0.96667
    Epoch [2080/10000], loss: 0.23076 acc: 1.00000 val_loss: 0.28634, val_acc: 0.96667
    Epoch [2090/10000], loss: 0.23003 acc: 1.00000 val_loss: 0.28567, val_acc: 0.96667
    Epoch [2100/10000], loss: 0.22931 acc: 1.00000 val_loss: 0.28501, val_acc: 0.96667
    Epoch [2110/10000], loss: 0.22859 acc: 1.00000 val_loss: 0.28435, val_acc: 0.96667
    Epoch [2120/10000], loss: 0.22788 acc: 1.00000 val_loss: 0.28369, val_acc: 0.96667
    Epoch [2130/10000], loss: 0.22718 acc: 1.00000 val_loss: 0.28304, val_acc: 0.96667
    Epoch [2140/10000], loss: 0.22648 acc: 1.00000 val_loss: 0.28240, val_acc: 0.96667
    Epoch [2150/10000], loss: 0.22578 acc: 1.00000 val_loss: 0.28176, val_acc: 0.96667
    Epoch [2160/10000], loss: 0.22509 acc: 1.00000 val_loss: 0.28112, val_acc: 0.96667
    Epoch [2170/10000], loss: 0.22441 acc: 1.00000 val_loss: 0.28049, val_acc: 0.96667
    Epoch [2180/10000], loss: 0.22373 acc: 1.00000 val_loss: 0.27986, val_acc: 0.96667
    Epoch [2190/10000], loss: 0.22305 acc: 1.00000 val_loss: 0.27924, val_acc: 0.96667
    Epoch [2200/10000], loss: 0.22238 acc: 1.00000 val_loss: 0.27862, val_acc: 0.96667
    Epoch [2210/10000], loss: 0.22171 acc: 1.00000 val_loss: 0.27801, val_acc: 0.96667
    Epoch [2220/10000], loss: 0.22105 acc: 1.00000 val_loss: 0.27740, val_acc: 0.96667
    Epoch [2230/10000], loss: 0.22039 acc: 1.00000 val_loss: 0.27680, val_acc: 0.96667
    Epoch [2240/10000], loss: 0.21974 acc: 1.00000 val_loss: 0.27620, val_acc: 0.96667
    Epoch [2250/10000], loss: 0.21909 acc: 1.00000 val_loss: 0.27560, val_acc: 0.96667
    Epoch [2260/10000], loss: 0.21845 acc: 1.00000 val_loss: 0.27501, val_acc: 0.96667
    Epoch [2270/10000], loss: 0.21781 acc: 1.00000 val_loss: 0.27442, val_acc: 0.96667
    Epoch [2280/10000], loss: 0.21718 acc: 1.00000 val_loss: 0.27384, val_acc: 0.96667
    Epoch [2290/10000], loss: 0.21655 acc: 1.00000 val_loss: 0.27326, val_acc: 0.96667
    Epoch [2300/10000], loss: 0.21592 acc: 1.00000 val_loss: 0.27269, val_acc: 0.96667
    Epoch [2310/10000], loss: 0.21530 acc: 1.00000 val_loss: 0.27211, val_acc: 0.96667
    Epoch [2320/10000], loss: 0.21468 acc: 1.00000 val_loss: 0.27155, val_acc: 0.96667
    Epoch [2330/10000], loss: 0.21407 acc: 1.00000 val_loss: 0.27098, val_acc: 0.96667
    Epoch [2340/10000], loss: 0.21346 acc: 1.00000 val_loss: 0.27042, val_acc: 0.96667
    Epoch [2350/10000], loss: 0.21285 acc: 1.00000 val_loss: 0.26987, val_acc: 0.96667
    Epoch [2360/10000], loss: 0.21225 acc: 1.00000 val_loss: 0.26932, val_acc: 0.96667
    Epoch [2370/10000], loss: 0.21165 acc: 1.00000 val_loss: 0.26877, val_acc: 0.96667
    Epoch [2380/10000], loss: 0.21106 acc: 1.00000 val_loss: 0.26822, val_acc: 0.96667
    Epoch [2390/10000], loss: 0.21047 acc: 1.00000 val_loss: 0.26768, val_acc: 0.96667
    Epoch [2400/10000], loss: 0.20988 acc: 1.00000 val_loss: 0.26715, val_acc: 0.96667
    Epoch [2410/10000], loss: 0.20930 acc: 1.00000 val_loss: 0.26661, val_acc: 0.96667
    Epoch [2420/10000], loss: 0.20872 acc: 1.00000 val_loss: 0.26608, val_acc: 0.96667
    Epoch [2430/10000], loss: 0.20815 acc: 1.00000 val_loss: 0.26556, val_acc: 0.96667
    Epoch [2440/10000], loss: 0.20758 acc: 1.00000 val_loss: 0.26503, val_acc: 0.96667
    Epoch [2450/10000], loss: 0.20701 acc: 1.00000 val_loss: 0.26451, val_acc: 0.96667
    Epoch [2460/10000], loss: 0.20645 acc: 1.00000 val_loss: 0.26400, val_acc: 0.96667
    Epoch [2470/10000], loss: 0.20589 acc: 1.00000 val_loss: 0.26349, val_acc: 0.96667
    Epoch [2480/10000], loss: 0.20533 acc: 1.00000 val_loss: 0.26298, val_acc: 0.96667
    Epoch [2490/10000], loss: 0.20478 acc: 1.00000 val_loss: 0.26247, val_acc: 0.96667
    Epoch [2500/10000], loss: 0.20423 acc: 1.00000 val_loss: 0.26197, val_acc: 0.96667
    Epoch [2510/10000], loss: 0.20369 acc: 1.00000 val_loss: 0.26147, val_acc: 0.96667
    Epoch [2520/10000], loss: 0.20314 acc: 1.00000 val_loss: 0.26097, val_acc: 0.96667
    Epoch [2530/10000], loss: 0.20261 acc: 1.00000 val_loss: 0.26048, val_acc: 0.96667
    Epoch [2540/10000], loss: 0.20207 acc: 1.00000 val_loss: 0.25999, val_acc: 0.96667
    Epoch [2550/10000], loss: 0.20154 acc: 1.00000 val_loss: 0.25950, val_acc: 0.96667
    Epoch [2560/10000], loss: 0.20101 acc: 1.00000 val_loss: 0.25902, val_acc: 0.96667
    Epoch [2570/10000], loss: 0.20048 acc: 1.00000 val_loss: 0.25854, val_acc: 0.96667
    Epoch [2580/10000], loss: 0.19996 acc: 1.00000 val_loss: 0.25806, val_acc: 0.96667
    Epoch [2590/10000], loss: 0.19944 acc: 1.00000 val_loss: 0.25759, val_acc: 0.96667
    Epoch [2600/10000], loss: 0.19893 acc: 1.00000 val_loss: 0.25712, val_acc: 0.96667
    Epoch [2610/10000], loss: 0.19841 acc: 1.00000 val_loss: 0.25665, val_acc: 0.96667
    Epoch [2620/10000], loss: 0.19791 acc: 1.00000 val_loss: 0.25618, val_acc: 0.96667
    Epoch [2630/10000], loss: 0.19740 acc: 1.00000 val_loss: 0.25572, val_acc: 0.96667
    Epoch [2640/10000], loss: 0.19690 acc: 1.00000 val_loss: 0.25526, val_acc: 0.96667
    Epoch [2650/10000], loss: 0.19640 acc: 1.00000 val_loss: 0.25481, val_acc: 0.96667
    Epoch [2660/10000], loss: 0.19590 acc: 1.00000 val_loss: 0.25435, val_acc: 0.96667
    Epoch [2670/10000], loss: 0.19540 acc: 1.00000 val_loss: 0.25390, val_acc: 0.96667
    Epoch [2680/10000], loss: 0.19491 acc: 1.00000 val_loss: 0.25345, val_acc: 0.96667
    Epoch [2690/10000], loss: 0.19442 acc: 1.00000 val_loss: 0.25301, val_acc: 0.96667
    Epoch [2700/10000], loss: 0.19394 acc: 1.00000 val_loss: 0.25257, val_acc: 0.96667
    Epoch [2710/10000], loss: 0.19346 acc: 1.00000 val_loss: 0.25213, val_acc: 0.96667
    Epoch [2720/10000], loss: 0.19298 acc: 1.00000 val_loss: 0.25169, val_acc: 0.96667
    Epoch [2730/10000], loss: 0.19250 acc: 1.00000 val_loss: 0.25125, val_acc: 0.96667
    Epoch [2740/10000], loss: 0.19202 acc: 1.00000 val_loss: 0.25082, val_acc: 0.96667
    Epoch [2750/10000], loss: 0.19155 acc: 1.00000 val_loss: 0.25039, val_acc: 0.96667
    Epoch [2760/10000], loss: 0.19108 acc: 1.00000 val_loss: 0.24997, val_acc: 0.96667
    Epoch [2770/10000], loss: 0.19062 acc: 1.00000 val_loss: 0.24954, val_acc: 0.96667
    Epoch [2780/10000], loss: 0.19016 acc: 1.00000 val_loss: 0.24912, val_acc: 0.96667
    Epoch [2790/10000], loss: 0.18970 acc: 1.00000 val_loss: 0.24870, val_acc: 0.96667
    Epoch [2800/10000], loss: 0.18924 acc: 1.00000 val_loss: 0.24828, val_acc: 0.96667
    Epoch [2810/10000], loss: 0.18878 acc: 1.00000 val_loss: 0.24787, val_acc: 0.96667
    Epoch [2820/10000], loss: 0.18833 acc: 1.00000 val_loss: 0.24746, val_acc: 0.96667
    Epoch [2830/10000], loss: 0.18788 acc: 1.00000 val_loss: 0.24705, val_acc: 0.96667
    Epoch [2840/10000], loss: 0.18743 acc: 1.00000 val_loss: 0.24664, val_acc: 0.96667
    Epoch [2850/10000], loss: 0.18699 acc: 1.00000 val_loss: 0.24624, val_acc: 0.96667
    Epoch [2860/10000], loss: 0.18654 acc: 1.00000 val_loss: 0.24584, val_acc: 0.96667
    Epoch [2870/10000], loss: 0.18610 acc: 1.00000 val_loss: 0.24544, val_acc: 0.96667
    Epoch [2880/10000], loss: 0.18567 acc: 1.00000 val_loss: 0.24504, val_acc: 0.96667
    Epoch [2890/10000], loss: 0.18523 acc: 1.00000 val_loss: 0.24464, val_acc: 0.96667
    Epoch [2900/10000], loss: 0.18480 acc: 1.00000 val_loss: 0.24425, val_acc: 0.96667
    Epoch [2910/10000], loss: 0.18437 acc: 1.00000 val_loss: 0.24386, val_acc: 0.96667
    Epoch [2920/10000], loss: 0.18394 acc: 1.00000 val_loss: 0.24347, val_acc: 0.96667
    Epoch [2930/10000], loss: 0.18352 acc: 1.00000 val_loss: 0.24309, val_acc: 0.96667
    Epoch [2940/10000], loss: 0.18309 acc: 1.00000 val_loss: 0.24270, val_acc: 0.96667
    Epoch [2950/10000], loss: 0.18267 acc: 1.00000 val_loss: 0.24232, val_acc: 0.96667
    Epoch [2960/10000], loss: 0.18225 acc: 1.00000 val_loss: 0.24194, val_acc: 0.96667
    Epoch [2970/10000], loss: 0.18184 acc: 1.00000 val_loss: 0.24156, val_acc: 0.96667
    Epoch [2980/10000], loss: 0.18142 acc: 1.00000 val_loss: 0.24119, val_acc: 0.96667
    Epoch [2990/10000], loss: 0.18101 acc: 1.00000 val_loss: 0.24081, val_acc: 0.96667
    Epoch [3000/10000], loss: 0.18060 acc: 1.00000 val_loss: 0.24044, val_acc: 0.96667
    Epoch [3010/10000], loss: 0.18019 acc: 1.00000 val_loss: 0.24008, val_acc: 0.96667
    Epoch [3020/10000], loss: 0.17979 acc: 1.00000 val_loss: 0.23971, val_acc: 0.96667
    Epoch [3030/10000], loss: 0.17939 acc: 1.00000 val_loss: 0.23934, val_acc: 0.96667
    Epoch [3040/10000], loss: 0.17899 acc: 1.00000 val_loss: 0.23898, val_acc: 0.96667
    Epoch [3050/10000], loss: 0.17859 acc: 1.00000 val_loss: 0.23862, val_acc: 0.96667
    Epoch [3060/10000], loss: 0.17819 acc: 1.00000 val_loss: 0.23826, val_acc: 0.96667
    Epoch [3070/10000], loss: 0.17780 acc: 1.00000 val_loss: 0.23790, val_acc: 0.96667
    Epoch [3080/10000], loss: 0.17740 acc: 1.00000 val_loss: 0.23755, val_acc: 0.96667
    Epoch [3090/10000], loss: 0.17701 acc: 1.00000 val_loss: 0.23720, val_acc: 0.96667
    Epoch [3100/10000], loss: 0.17662 acc: 1.00000 val_loss: 0.23685, val_acc: 0.96667
    Epoch [3110/10000], loss: 0.17624 acc: 1.00000 val_loss: 0.23650, val_acc: 0.96667
    Epoch [3120/10000], loss: 0.17585 acc: 1.00000 val_loss: 0.23615, val_acc: 0.96667
    Epoch [3130/10000], loss: 0.17547 acc: 1.00000 val_loss: 0.23580, val_acc: 0.96667
    Epoch [3140/10000], loss: 0.17509 acc: 1.00000 val_loss: 0.23546, val_acc: 0.96667
    Epoch [3150/10000], loss: 0.17471 acc: 1.00000 val_loss: 0.23512, val_acc: 0.96667
    Epoch [3160/10000], loss: 0.17434 acc: 1.00000 val_loss: 0.23478, val_acc: 0.96667
    Epoch [3170/10000], loss: 0.17396 acc: 1.00000 val_loss: 0.23444, val_acc: 0.96667
    Epoch [3180/10000], loss: 0.17359 acc: 1.00000 val_loss: 0.23411, val_acc: 0.96667
    Epoch [3190/10000], loss: 0.17322 acc: 1.00000 val_loss: 0.23377, val_acc: 0.96667
    Epoch [3200/10000], loss: 0.17285 acc: 1.00000 val_loss: 0.23344, val_acc: 0.96667
    Epoch [3210/10000], loss: 0.17249 acc: 1.00000 val_loss: 0.23311, val_acc: 0.96667
    Epoch [3220/10000], loss: 0.17212 acc: 1.00000 val_loss: 0.23278, val_acc: 0.96667
    Epoch [3230/10000], loss: 0.17176 acc: 1.00000 val_loss: 0.23245, val_acc: 0.96667
    Epoch [3240/10000], loss: 0.17140 acc: 1.00000 val_loss: 0.23213, val_acc: 0.96667
    Epoch [3250/10000], loss: 0.17104 acc: 1.00000 val_loss: 0.23180, val_acc: 0.96667
    Epoch [3260/10000], loss: 0.17068 acc: 1.00000 val_loss: 0.23148, val_acc: 0.96667
    Epoch [3270/10000], loss: 0.17032 acc: 1.00000 val_loss: 0.23116, val_acc: 0.96667
    Epoch [3280/10000], loss: 0.16997 acc: 1.00000 val_loss: 0.23084, val_acc: 0.96667
    Epoch [3290/10000], loss: 0.16962 acc: 1.00000 val_loss: 0.23053, val_acc: 0.96667
    Epoch [3300/10000], loss: 0.16927 acc: 1.00000 val_loss: 0.23021, val_acc: 0.96667
    Epoch [3310/10000], loss: 0.16892 acc: 1.00000 val_loss: 0.22990, val_acc: 0.96667
    Epoch [3320/10000], loss: 0.16857 acc: 1.00000 val_loss: 0.22959, val_acc: 0.96667
    Epoch [3330/10000], loss: 0.16823 acc: 1.00000 val_loss: 0.22928, val_acc: 0.96667
    Epoch [3340/10000], loss: 0.16788 acc: 1.00000 val_loss: 0.22897, val_acc: 0.96667
    Epoch [3350/10000], loss: 0.16754 acc: 1.00000 val_loss: 0.22866, val_acc: 0.96667
    Epoch [3360/10000], loss: 0.16720 acc: 1.00000 val_loss: 0.22835, val_acc: 0.96667
    Epoch [3370/10000], loss: 0.16686 acc: 1.00000 val_loss: 0.22805, val_acc: 0.96667
    Epoch [3380/10000], loss: 0.16653 acc: 1.00000 val_loss: 0.22775, val_acc: 0.96667
    Epoch [3390/10000], loss: 0.16619 acc: 1.00000 val_loss: 0.22745, val_acc: 0.96667
    Epoch [3400/10000], loss: 0.16586 acc: 1.00000 val_loss: 0.22715, val_acc: 0.96667
    Epoch [3410/10000], loss: 0.16553 acc: 1.00000 val_loss: 0.22685, val_acc: 0.96667
    Epoch [3420/10000], loss: 0.16520 acc: 1.00000 val_loss: 0.22655, val_acc: 0.96667
    Epoch [3430/10000], loss: 0.16487 acc: 1.00000 val_loss: 0.22626, val_acc: 0.96667
    Epoch [3440/10000], loss: 0.16454 acc: 1.00000 val_loss: 0.22596, val_acc: 0.96667
    Epoch [3450/10000], loss: 0.16421 acc: 1.00000 val_loss: 0.22567, val_acc: 0.96667
    Epoch [3460/10000], loss: 0.16389 acc: 1.00000 val_loss: 0.22538, val_acc: 0.96667
    Epoch [3470/10000], loss: 0.16357 acc: 1.00000 val_loss: 0.22509, val_acc: 0.96667
    Epoch [3480/10000], loss: 0.16325 acc: 1.00000 val_loss: 0.22480, val_acc: 0.96667
    Epoch [3490/10000], loss: 0.16293 acc: 1.00000 val_loss: 0.22452, val_acc: 0.96667
    Epoch [3500/10000], loss: 0.16261 acc: 1.00000 val_loss: 0.22423, val_acc: 0.96667
    Epoch [3510/10000], loss: 0.16229 acc: 1.00000 val_loss: 0.22395, val_acc: 0.96667
    Epoch [3520/10000], loss: 0.16198 acc: 1.00000 val_loss: 0.22367, val_acc: 0.96667
    Epoch [3530/10000], loss: 0.16166 acc: 1.00000 val_loss: 0.22339, val_acc: 0.96667
    Epoch [3540/10000], loss: 0.16135 acc: 1.00000 val_loss: 0.22311, val_acc: 0.96667
    Epoch [3550/10000], loss: 0.16104 acc: 1.00000 val_loss: 0.22283, val_acc: 0.96667
    Epoch [3560/10000], loss: 0.16073 acc: 1.00000 val_loss: 0.22255, val_acc: 0.96667
    Epoch [3570/10000], loss: 0.16043 acc: 1.00000 val_loss: 0.22228, val_acc: 0.96667
    Epoch [3580/10000], loss: 0.16012 acc: 1.00000 val_loss: 0.22200, val_acc: 0.96667
    Epoch [3590/10000], loss: 0.15981 acc: 1.00000 val_loss: 0.22173, val_acc: 0.96667
    Epoch [3600/10000], loss: 0.15951 acc: 1.00000 val_loss: 0.22146, val_acc: 0.96667
    Epoch [3610/10000], loss: 0.15921 acc: 1.00000 val_loss: 0.22119, val_acc: 0.96667
    Epoch [3620/10000], loss: 0.15891 acc: 1.00000 val_loss: 0.22092, val_acc: 0.96667
    Epoch [3630/10000], loss: 0.15861 acc: 1.00000 val_loss: 0.22065, val_acc: 0.96667
    Epoch [3640/10000], loss: 0.15831 acc: 1.00000 val_loss: 0.22039, val_acc: 0.96667
    Epoch [3650/10000], loss: 0.15801 acc: 1.00000 val_loss: 0.22012, val_acc: 0.96667
    Epoch [3660/10000], loss: 0.15772 acc: 1.00000 val_loss: 0.21986, val_acc: 0.96667
    Epoch [3670/10000], loss: 0.15743 acc: 1.00000 val_loss: 0.21960, val_acc: 0.96667
    Epoch [3680/10000], loss: 0.15713 acc: 1.00000 val_loss: 0.21934, val_acc: 0.96667
    Epoch [3690/10000], loss: 0.15684 acc: 1.00000 val_loss: 0.21908, val_acc: 0.96667
    Epoch [3700/10000], loss: 0.15655 acc: 1.00000 val_loss: 0.21882, val_acc: 0.96667
    Epoch [3710/10000], loss: 0.15626 acc: 1.00000 val_loss: 0.21856, val_acc: 0.96667
    Epoch [3720/10000], loss: 0.15598 acc: 1.00000 val_loss: 0.21830, val_acc: 0.96667
    Epoch [3730/10000], loss: 0.15569 acc: 1.00000 val_loss: 0.21805, val_acc: 0.96667
    Epoch [3740/10000], loss: 0.15540 acc: 1.00000 val_loss: 0.21780, val_acc: 0.96667
    Epoch [3750/10000], loss: 0.15512 acc: 1.00000 val_loss: 0.21754, val_acc: 0.96667
    Epoch [3760/10000], loss: 0.15484 acc: 1.00000 val_loss: 0.21729, val_acc: 0.96667
    Epoch [3770/10000], loss: 0.15456 acc: 1.00000 val_loss: 0.21704, val_acc: 0.96667
    Epoch [3780/10000], loss: 0.15428 acc: 1.00000 val_loss: 0.21679, val_acc: 0.96667
    Epoch [3790/10000], loss: 0.15400 acc: 1.00000 val_loss: 0.21655, val_acc: 0.96667
    Epoch [3800/10000], loss: 0.15372 acc: 1.00000 val_loss: 0.21630, val_acc: 0.96667
    Epoch [3810/10000], loss: 0.15345 acc: 1.00000 val_loss: 0.21605, val_acc: 0.96667
    Epoch [3820/10000], loss: 0.15317 acc: 1.00000 val_loss: 0.21581, val_acc: 0.96667
    Epoch [3830/10000], loss: 0.15290 acc: 1.00000 val_loss: 0.21557, val_acc: 0.96667
    Epoch [3840/10000], loss: 0.15262 acc: 1.00000 val_loss: 0.21532, val_acc: 0.96667
    Epoch [3850/10000], loss: 0.15235 acc: 1.00000 val_loss: 0.21508, val_acc: 0.96667
    Epoch [3860/10000], loss: 0.15208 acc: 1.00000 val_loss: 0.21484, val_acc: 0.96667
    Epoch [3870/10000], loss: 0.15181 acc: 1.00000 val_loss: 0.21460, val_acc: 0.96667
    Epoch [3880/10000], loss: 0.15155 acc: 1.00000 val_loss: 0.21436, val_acc: 0.96667
    Epoch [3890/10000], loss: 0.15128 acc: 1.00000 val_loss: 0.21413, val_acc: 0.96667
    Epoch [3900/10000], loss: 0.15101 acc: 1.00000 val_loss: 0.21389, val_acc: 0.96667
    Epoch [3910/10000], loss: 0.15075 acc: 1.00000 val_loss: 0.21366, val_acc: 0.96667
    Epoch [3920/10000], loss: 0.15049 acc: 1.00000 val_loss: 0.21342, val_acc: 0.96667
    Epoch [3930/10000], loss: 0.15022 acc: 1.00000 val_loss: 0.21319, val_acc: 0.96667
    Epoch [3940/10000], loss: 0.14996 acc: 1.00000 val_loss: 0.21296, val_acc: 0.96667
    Epoch [3950/10000], loss: 0.14970 acc: 1.00000 val_loss: 0.21273, val_acc: 0.96667
    Epoch [3960/10000], loss: 0.14944 acc: 1.00000 val_loss: 0.21250, val_acc: 0.96667
    Epoch [3970/10000], loss: 0.14919 acc: 1.00000 val_loss: 0.21227, val_acc: 0.96667
    Epoch [3980/10000], loss: 0.14893 acc: 1.00000 val_loss: 0.21204, val_acc: 0.96667
    Epoch [3990/10000], loss: 0.14867 acc: 1.00000 val_loss: 0.21182, val_acc: 0.96667
    Epoch [4000/10000], loss: 0.14842 acc: 1.00000 val_loss: 0.21159, val_acc: 0.96667
    Epoch [4010/10000], loss: 0.14816 acc: 1.00000 val_loss: 0.21137, val_acc: 0.96667
    Epoch [4020/10000], loss: 0.14791 acc: 1.00000 val_loss: 0.21114, val_acc: 0.96667
    Epoch [4030/10000], loss: 0.14766 acc: 1.00000 val_loss: 0.21092, val_acc: 0.96667
    Epoch [4040/10000], loss: 0.14741 acc: 1.00000 val_loss: 0.21070, val_acc: 0.96667
    Epoch [4050/10000], loss: 0.14716 acc: 1.00000 val_loss: 0.21048, val_acc: 0.96667
    Epoch [4060/10000], loss: 0.14691 acc: 1.00000 val_loss: 0.21026, val_acc: 0.96667
    Epoch [4070/10000], loss: 0.14667 acc: 1.00000 val_loss: 0.21004, val_acc: 0.96667
    Epoch [4080/10000], loss: 0.14642 acc: 1.00000 val_loss: 0.20982, val_acc: 0.96667
    Epoch [4090/10000], loss: 0.14617 acc: 1.00000 val_loss: 0.20961, val_acc: 0.96667
    Epoch [4100/10000], loss: 0.14593 acc: 1.00000 val_loss: 0.20939, val_acc: 0.96667
    Epoch [4110/10000], loss: 0.14569 acc: 1.00000 val_loss: 0.20918, val_acc: 0.96667
    Epoch [4120/10000], loss: 0.14544 acc: 1.00000 val_loss: 0.20896, val_acc: 0.96667
    Epoch [4130/10000], loss: 0.14520 acc: 1.00000 val_loss: 0.20875, val_acc: 0.96667
    Epoch [4140/10000], loss: 0.14496 acc: 1.00000 val_loss: 0.20854, val_acc: 0.96667
    Epoch [4150/10000], loss: 0.14472 acc: 1.00000 val_loss: 0.20833, val_acc: 0.96667
    Epoch [4160/10000], loss: 0.14448 acc: 1.00000 val_loss: 0.20812, val_acc: 0.96667
    Epoch [4170/10000], loss: 0.14425 acc: 1.00000 val_loss: 0.20791, val_acc: 0.96667
    Epoch [4180/10000], loss: 0.14401 acc: 1.00000 val_loss: 0.20770, val_acc: 0.96667
    Epoch [4190/10000], loss: 0.14377 acc: 1.00000 val_loss: 0.20749, val_acc: 0.96667
    Epoch [4200/10000], loss: 0.14354 acc: 1.00000 val_loss: 0.20728, val_acc: 0.96667
    Epoch [4210/10000], loss: 0.14331 acc: 1.00000 val_loss: 0.20708, val_acc: 0.96667
    Epoch [4220/10000], loss: 0.14307 acc: 1.00000 val_loss: 0.20687, val_acc: 0.96667
    Epoch [4230/10000], loss: 0.14284 acc: 1.00000 val_loss: 0.20667, val_acc: 0.96667
    Epoch [4240/10000], loss: 0.14261 acc: 1.00000 val_loss: 0.20647, val_acc: 0.96667
    Epoch [4250/10000], loss: 0.14238 acc: 1.00000 val_loss: 0.20626, val_acc: 0.96667
    Epoch [4260/10000], loss: 0.14215 acc: 1.00000 val_loss: 0.20606, val_acc: 0.96667
    Epoch [4270/10000], loss: 0.14192 acc: 1.00000 val_loss: 0.20586, val_acc: 0.96667
    Epoch [4280/10000], loss: 0.14170 acc: 1.00000 val_loss: 0.20566, val_acc: 0.96667
    Epoch [4290/10000], loss: 0.14147 acc: 1.00000 val_loss: 0.20546, val_acc: 0.96667
    Epoch [4300/10000], loss: 0.14124 acc: 1.00000 val_loss: 0.20526, val_acc: 0.96667
    Epoch [4310/10000], loss: 0.14102 acc: 1.00000 val_loss: 0.20507, val_acc: 0.96667
    Epoch [4320/10000], loss: 0.14080 acc: 1.00000 val_loss: 0.20487, val_acc: 0.96667
    Epoch [4330/10000], loss: 0.14057 acc: 1.00000 val_loss: 0.20467, val_acc: 0.96667
    Epoch [4340/10000], loss: 0.14035 acc: 1.00000 val_loss: 0.20448, val_acc: 0.96667
    Epoch [4350/10000], loss: 0.14013 acc: 1.00000 val_loss: 0.20429, val_acc: 0.96667
    Epoch [4360/10000], loss: 0.13991 acc: 1.00000 val_loss: 0.20409, val_acc: 0.96667
    Epoch [4370/10000], loss: 0.13969 acc: 1.00000 val_loss: 0.20390, val_acc: 0.96667
    Epoch [4380/10000], loss: 0.13947 acc: 1.00000 val_loss: 0.20371, val_acc: 0.96667
    Epoch [4390/10000], loss: 0.13925 acc: 1.00000 val_loss: 0.20352, val_acc: 0.96667
    Epoch [4400/10000], loss: 0.13904 acc: 1.00000 val_loss: 0.20333, val_acc: 0.96667
    Epoch [4410/10000], loss: 0.13882 acc: 1.00000 val_loss: 0.20314, val_acc: 0.96667
    Epoch [4420/10000], loss: 0.13860 acc: 1.00000 val_loss: 0.20295, val_acc: 0.96667
    Epoch [4430/10000], loss: 0.13839 acc: 1.00000 val_loss: 0.20276, val_acc: 0.96667
    Epoch [4440/10000], loss: 0.13818 acc: 1.00000 val_loss: 0.20257, val_acc: 0.96667
    Epoch [4450/10000], loss: 0.13796 acc: 1.00000 val_loss: 0.20239, val_acc: 0.96667
    Epoch [4460/10000], loss: 0.13775 acc: 1.00000 val_loss: 0.20220, val_acc: 0.96667
    Epoch [4470/10000], loss: 0.13754 acc: 1.00000 val_loss: 0.20202, val_acc: 0.96667
    Epoch [4480/10000], loss: 0.13733 acc: 1.00000 val_loss: 0.20183, val_acc: 0.96667
    Epoch [4490/10000], loss: 0.13712 acc: 1.00000 val_loss: 0.20165, val_acc: 0.96667
    Epoch [4500/10000], loss: 0.13691 acc: 1.00000 val_loss: 0.20147, val_acc: 0.96667
    Epoch [4510/10000], loss: 0.13670 acc: 1.00000 val_loss: 0.20128, val_acc: 0.96667
    Epoch [4520/10000], loss: 0.13650 acc: 1.00000 val_loss: 0.20110, val_acc: 0.96667
    Epoch [4530/10000], loss: 0.13629 acc: 1.00000 val_loss: 0.20092, val_acc: 0.96667
    Epoch [4540/10000], loss: 0.13608 acc: 1.00000 val_loss: 0.20074, val_acc: 0.96667
    Epoch [4550/10000], loss: 0.13588 acc: 1.00000 val_loss: 0.20056, val_acc: 0.96667
    Epoch [4560/10000], loss: 0.13567 acc: 1.00000 val_loss: 0.20038, val_acc: 0.96667
    Epoch [4570/10000], loss: 0.13547 acc: 1.00000 val_loss: 0.20021, val_acc: 0.96667
    Epoch [4580/10000], loss: 0.13527 acc: 1.00000 val_loss: 0.20003, val_acc: 0.96667
    Epoch [4590/10000], loss: 0.13507 acc: 1.00000 val_loss: 0.19985, val_acc: 0.96667
    Epoch [4600/10000], loss: 0.13486 acc: 1.00000 val_loss: 0.19968, val_acc: 0.96667
    Epoch [4610/10000], loss: 0.13466 acc: 1.00000 val_loss: 0.19950, val_acc: 0.96667
    Epoch [4620/10000], loss: 0.13446 acc: 1.00000 val_loss: 0.19933, val_acc: 0.96667
    Epoch [4630/10000], loss: 0.13426 acc: 1.00000 val_loss: 0.19916, val_acc: 0.96667
    Epoch [4640/10000], loss: 0.13407 acc: 1.00000 val_loss: 0.19898, val_acc: 0.96667
    Epoch [4650/10000], loss: 0.13387 acc: 1.00000 val_loss: 0.19881, val_acc: 0.96667
    Epoch [4660/10000], loss: 0.13367 acc: 1.00000 val_loss: 0.19864, val_acc: 0.96667
    Epoch [4670/10000], loss: 0.13348 acc: 1.00000 val_loss: 0.19847, val_acc: 0.96667
    Epoch [4680/10000], loss: 0.13328 acc: 1.00000 val_loss: 0.19830, val_acc: 0.96667
    Epoch [4690/10000], loss: 0.13308 acc: 1.00000 val_loss: 0.19813, val_acc: 0.96667
    Epoch [4700/10000], loss: 0.13289 acc: 1.00000 val_loss: 0.19796, val_acc: 0.96667
    Epoch [4710/10000], loss: 0.13270 acc: 1.00000 val_loss: 0.19779, val_acc: 0.96667
    Epoch [4720/10000], loss: 0.13250 acc: 1.00000 val_loss: 0.19762, val_acc: 0.96667
    Epoch [4730/10000], loss: 0.13231 acc: 1.00000 val_loss: 0.19746, val_acc: 0.96667
    Epoch [4740/10000], loss: 0.13212 acc: 1.00000 val_loss: 0.19729, val_acc: 0.96667
    Epoch [4750/10000], loss: 0.13193 acc: 1.00000 val_loss: 0.19712, val_acc: 0.96667
    Epoch [4760/10000], loss: 0.13174 acc: 1.00000 val_loss: 0.19696, val_acc: 0.96667
    Epoch [4770/10000], loss: 0.13155 acc: 1.00000 val_loss: 0.19679, val_acc: 0.96667
    Epoch [4780/10000], loss: 0.13136 acc: 1.00000 val_loss: 0.19663, val_acc: 0.96667
    Epoch [4790/10000], loss: 0.13117 acc: 1.00000 val_loss: 0.19647, val_acc: 0.96667
    Epoch [4800/10000], loss: 0.13099 acc: 1.00000 val_loss: 0.19630, val_acc: 0.96667
    Epoch [4810/10000], loss: 0.13080 acc: 1.00000 val_loss: 0.19614, val_acc: 0.96667
    Epoch [4820/10000], loss: 0.13061 acc: 1.00000 val_loss: 0.19598, val_acc: 0.96667
    Epoch [4830/10000], loss: 0.13043 acc: 1.00000 val_loss: 0.19582, val_acc: 0.96667
    Epoch [4840/10000], loss: 0.13024 acc: 1.00000 val_loss: 0.19566, val_acc: 0.96667
    Epoch [4850/10000], loss: 0.13006 acc: 1.00000 val_loss: 0.19550, val_acc: 0.96667
    Epoch [4860/10000], loss: 0.12988 acc: 1.00000 val_loss: 0.19534, val_acc: 0.96667
    Epoch [4870/10000], loss: 0.12969 acc: 1.00000 val_loss: 0.19518, val_acc: 0.96667
    Epoch [4880/10000], loss: 0.12951 acc: 1.00000 val_loss: 0.19502, val_acc: 0.96667
    Epoch [4890/10000], loss: 0.12933 acc: 1.00000 val_loss: 0.19487, val_acc: 0.96667
    Epoch [4900/10000], loss: 0.12915 acc: 1.00000 val_loss: 0.19471, val_acc: 0.96667
    Epoch [4910/10000], loss: 0.12897 acc: 1.00000 val_loss: 0.19455, val_acc: 0.96667
    Epoch [4920/10000], loss: 0.12879 acc: 1.00000 val_loss: 0.19440, val_acc: 0.96667
    Epoch [4930/10000], loss: 0.12861 acc: 1.00000 val_loss: 0.19424, val_acc: 0.96667
    Epoch [4940/10000], loss: 0.12843 acc: 1.00000 val_loss: 0.19409, val_acc: 0.96667
    Epoch [4950/10000], loss: 0.12825 acc: 1.00000 val_loss: 0.19394, val_acc: 0.96667
    Epoch [4960/10000], loss: 0.12808 acc: 1.00000 val_loss: 0.19378, val_acc: 0.96667
    Epoch [4970/10000], loss: 0.12790 acc: 1.00000 val_loss: 0.19363, val_acc: 0.96667
    Epoch [4980/10000], loss: 0.12772 acc: 1.00000 val_loss: 0.19348, val_acc: 0.96667
    Epoch [4990/10000], loss: 0.12755 acc: 1.00000 val_loss: 0.19333, val_acc: 0.96667
    Epoch [5000/10000], loss: 0.12737 acc: 1.00000 val_loss: 0.19318, val_acc: 0.96667
    Epoch [5010/10000], loss: 0.12720 acc: 1.00000 val_loss: 0.19302, val_acc: 0.96667
    Epoch [5020/10000], loss: 0.12703 acc: 1.00000 val_loss: 0.19287, val_acc: 0.96667
    Epoch [5030/10000], loss: 0.12685 acc: 1.00000 val_loss: 0.19273, val_acc: 0.96667
    Epoch [5040/10000], loss: 0.12668 acc: 1.00000 val_loss: 0.19258, val_acc: 0.96667
    Epoch [5050/10000], loss: 0.12651 acc: 1.00000 val_loss: 0.19243, val_acc: 0.96667
    Epoch [5060/10000], loss: 0.12634 acc: 1.00000 val_loss: 0.19228, val_acc: 0.96667
    Epoch [5070/10000], loss: 0.12617 acc: 1.00000 val_loss: 0.19213, val_acc: 0.96667
    Epoch [5080/10000], loss: 0.12600 acc: 1.00000 val_loss: 0.19199, val_acc: 0.96667
    Epoch [5090/10000], loss: 0.12583 acc: 1.00000 val_loss: 0.19184, val_acc: 0.96667
    Epoch [5100/10000], loss: 0.12566 acc: 1.00000 val_loss: 0.19169, val_acc: 0.96667
    Epoch [5110/10000], loss: 0.12549 acc: 1.00000 val_loss: 0.19155, val_acc: 0.96667
    Epoch [5120/10000], loss: 0.12532 acc: 1.00000 val_loss: 0.19140, val_acc: 0.96667
    Epoch [5130/10000], loss: 0.12515 acc: 1.00000 val_loss: 0.19126, val_acc: 0.96667
    Epoch [5140/10000], loss: 0.12499 acc: 1.00000 val_loss: 0.19112, val_acc: 0.96667
    Epoch [5150/10000], loss: 0.12482 acc: 1.00000 val_loss: 0.19097, val_acc: 0.96667
    Epoch [5160/10000], loss: 0.12465 acc: 1.00000 val_loss: 0.19083, val_acc: 0.96667
    Epoch [5170/10000], loss: 0.12449 acc: 1.00000 val_loss: 0.19069, val_acc: 0.96667
    Epoch [5180/10000], loss: 0.12432 acc: 1.00000 val_loss: 0.19055, val_acc: 0.96667
    Epoch [5190/10000], loss: 0.12416 acc: 1.00000 val_loss: 0.19041, val_acc: 0.96667
    Epoch [5200/10000], loss: 0.12400 acc: 1.00000 val_loss: 0.19027, val_acc: 0.96667
    Epoch [5210/10000], loss: 0.12383 acc: 1.00000 val_loss: 0.19013, val_acc: 0.96667
    Epoch [5220/10000], loss: 0.12367 acc: 1.00000 val_loss: 0.18999, val_acc: 0.96667
    Epoch [5230/10000], loss: 0.12351 acc: 1.00000 val_loss: 0.18985, val_acc: 0.96667
    Epoch [5240/10000], loss: 0.12335 acc: 1.00000 val_loss: 0.18971, val_acc: 0.96667
    Epoch [5250/10000], loss: 0.12319 acc: 1.00000 val_loss: 0.18957, val_acc: 0.96667
    Epoch [5260/10000], loss: 0.12303 acc: 1.00000 val_loss: 0.18943, val_acc: 0.96667
    Epoch [5270/10000], loss: 0.12287 acc: 1.00000 val_loss: 0.18930, val_acc: 0.96667
    Epoch [5280/10000], loss: 0.12271 acc: 1.00000 val_loss: 0.18916, val_acc: 0.96667
    Epoch [5290/10000], loss: 0.12255 acc: 1.00000 val_loss: 0.18902, val_acc: 0.96667
    Epoch [5300/10000], loss: 0.12239 acc: 1.00000 val_loss: 0.18889, val_acc: 0.96667
    Epoch [5310/10000], loss: 0.12223 acc: 1.00000 val_loss: 0.18875, val_acc: 0.96667
    Epoch [5320/10000], loss: 0.12207 acc: 1.00000 val_loss: 0.18862, val_acc: 0.96667
    Epoch [5330/10000], loss: 0.12192 acc: 1.00000 val_loss: 0.18848, val_acc: 0.96667
    Epoch [5340/10000], loss: 0.12176 acc: 1.00000 val_loss: 0.18835, val_acc: 0.96667
    Epoch [5350/10000], loss: 0.12160 acc: 1.00000 val_loss: 0.18821, val_acc: 0.96667
    Epoch [5360/10000], loss: 0.12145 acc: 1.00000 val_loss: 0.18808, val_acc: 0.96667
    Epoch [5370/10000], loss: 0.12129 acc: 1.00000 val_loss: 0.18795, val_acc: 0.96667
    Epoch [5380/10000], loss: 0.12114 acc: 1.00000 val_loss: 0.18782, val_acc: 0.96667
    Epoch [5390/10000], loss: 0.12099 acc: 1.00000 val_loss: 0.18768, val_acc: 0.96667
    Epoch [5400/10000], loss: 0.12083 acc: 1.00000 val_loss: 0.18755, val_acc: 0.96667
    Epoch [5410/10000], loss: 0.12068 acc: 1.00000 val_loss: 0.18742, val_acc: 0.96667
    Epoch [5420/10000], loss: 0.12053 acc: 1.00000 val_loss: 0.18729, val_acc: 0.96667
    Epoch [5430/10000], loss: 0.12037 acc: 1.00000 val_loss: 0.18716, val_acc: 0.96667
    Epoch [5440/10000], loss: 0.12022 acc: 1.00000 val_loss: 0.18703, val_acc: 0.96667
    Epoch [5450/10000], loss: 0.12007 acc: 1.00000 val_loss: 0.18690, val_acc: 0.96667
    Epoch [5460/10000], loss: 0.11992 acc: 1.00000 val_loss: 0.18678, val_acc: 0.96667
    Epoch [5470/10000], loss: 0.11977 acc: 1.00000 val_loss: 0.18665, val_acc: 0.96667
    Epoch [5480/10000], loss: 0.11962 acc: 1.00000 val_loss: 0.18652, val_acc: 0.96667
    Epoch [5490/10000], loss: 0.11947 acc: 1.00000 val_loss: 0.18639, val_acc: 0.96667
    Epoch [5500/10000], loss: 0.11932 acc: 1.00000 val_loss: 0.18627, val_acc: 0.96667
    Epoch [5510/10000], loss: 0.11918 acc: 1.00000 val_loss: 0.18614, val_acc: 0.96667
    Epoch [5520/10000], loss: 0.11903 acc: 1.00000 val_loss: 0.18601, val_acc: 0.96667
    Epoch [5530/10000], loss: 0.11888 acc: 1.00000 val_loss: 0.18589, val_acc: 0.96667
    Epoch [5540/10000], loss: 0.11873 acc: 1.00000 val_loss: 0.18576, val_acc: 0.96667
    Epoch [5550/10000], loss: 0.11859 acc: 1.00000 val_loss: 0.18564, val_acc: 0.96667
    Epoch [5560/10000], loss: 0.11844 acc: 1.00000 val_loss: 0.18551, val_acc: 0.96667
    Epoch [5570/10000], loss: 0.11830 acc: 1.00000 val_loss: 0.18539, val_acc: 0.96667
    Epoch [5580/10000], loss: 0.11815 acc: 1.00000 val_loss: 0.18527, val_acc: 0.96667
    Epoch [5590/10000], loss: 0.11801 acc: 1.00000 val_loss: 0.18514, val_acc: 0.96667
    Epoch [5600/10000], loss: 0.11786 acc: 1.00000 val_loss: 0.18502, val_acc: 0.96667
    Epoch [5610/10000], loss: 0.11772 acc: 1.00000 val_loss: 0.18490, val_acc: 0.96667
    Epoch [5620/10000], loss: 0.11757 acc: 1.00000 val_loss: 0.18478, val_acc: 0.96667
    Epoch [5630/10000], loss: 0.11743 acc: 1.00000 val_loss: 0.18465, val_acc: 0.96667
    Epoch [5640/10000], loss: 0.11729 acc: 1.00000 val_loss: 0.18453, val_acc: 0.96667
    Epoch [5650/10000], loss: 0.11715 acc: 1.00000 val_loss: 0.18441, val_acc: 0.96667
    Epoch [5660/10000], loss: 0.11701 acc: 1.00000 val_loss: 0.18429, val_acc: 0.96667
    Epoch [5670/10000], loss: 0.11686 acc: 1.00000 val_loss: 0.18417, val_acc: 0.96667
    Epoch [5680/10000], loss: 0.11672 acc: 1.00000 val_loss: 0.18405, val_acc: 0.96667
    Epoch [5690/10000], loss: 0.11658 acc: 1.00000 val_loss: 0.18393, val_acc: 0.96667
    Epoch [5700/10000], loss: 0.11644 acc: 1.00000 val_loss: 0.18381, val_acc: 0.96667
    Epoch [5710/10000], loss: 0.11630 acc: 1.00000 val_loss: 0.18370, val_acc: 0.96667
    Epoch [5720/10000], loss: 0.11616 acc: 1.00000 val_loss: 0.18358, val_acc: 0.96667
    Epoch [5730/10000], loss: 0.11603 acc: 1.00000 val_loss: 0.18346, val_acc: 0.96667
    Epoch [5740/10000], loss: 0.11589 acc: 1.00000 val_loss: 0.18334, val_acc: 0.96667
    Epoch [5750/10000], loss: 0.11575 acc: 1.00000 val_loss: 0.18323, val_acc: 0.96667
    Epoch [5760/10000], loss: 0.11561 acc: 1.00000 val_loss: 0.18311, val_acc: 0.96667
    Epoch [5770/10000], loss: 0.11547 acc: 1.00000 val_loss: 0.18299, val_acc: 0.96667
    Epoch [5780/10000], loss: 0.11534 acc: 1.00000 val_loss: 0.18288, val_acc: 0.96667
    Epoch [5790/10000], loss: 0.11520 acc: 1.00000 val_loss: 0.18276, val_acc: 0.96667
    Epoch [5800/10000], loss: 0.11507 acc: 1.00000 val_loss: 0.18265, val_acc: 0.96667
    Epoch [5810/10000], loss: 0.11493 acc: 1.00000 val_loss: 0.18253, val_acc: 0.96667
    Epoch [5820/10000], loss: 0.11480 acc: 1.00000 val_loss: 0.18242, val_acc: 0.96667
    Epoch [5830/10000], loss: 0.11466 acc: 1.00000 val_loss: 0.18231, val_acc: 0.96667
    Epoch [5840/10000], loss: 0.11453 acc: 1.00000 val_loss: 0.18219, val_acc: 0.96667
    Epoch [5850/10000], loss: 0.11439 acc: 1.00000 val_loss: 0.18208, val_acc: 0.96667
    Epoch [5860/10000], loss: 0.11426 acc: 1.00000 val_loss: 0.18197, val_acc: 0.96667
    Epoch [5870/10000], loss: 0.11413 acc: 1.00000 val_loss: 0.18185, val_acc: 0.96667
    Epoch [5880/10000], loss: 0.11399 acc: 1.00000 val_loss: 0.18174, val_acc: 0.96667
    Epoch [5890/10000], loss: 0.11386 acc: 1.00000 val_loss: 0.18163, val_acc: 0.96667
    Epoch [5900/10000], loss: 0.11373 acc: 1.00000 val_loss: 0.18152, val_acc: 0.96667
    Epoch [5910/10000], loss: 0.11360 acc: 1.00000 val_loss: 0.18141, val_acc: 0.96667
    Epoch [5920/10000], loss: 0.11347 acc: 1.00000 val_loss: 0.18130, val_acc: 0.96667
    Epoch [5930/10000], loss: 0.11333 acc: 1.00000 val_loss: 0.18119, val_acc: 0.96667
    Epoch [5940/10000], loss: 0.11320 acc: 1.00000 val_loss: 0.18108, val_acc: 0.96667
    Epoch [5950/10000], loss: 0.11307 acc: 1.00000 val_loss: 0.18097, val_acc: 0.96667
    Epoch [5960/10000], loss: 0.11294 acc: 1.00000 val_loss: 0.18086, val_acc: 0.96667
    Epoch [5970/10000], loss: 0.11282 acc: 1.00000 val_loss: 0.18075, val_acc: 0.96667
    Epoch [5980/10000], loss: 0.11269 acc: 1.00000 val_loss: 0.18064, val_acc: 0.96667
    Epoch [5990/10000], loss: 0.11256 acc: 1.00000 val_loss: 0.18053, val_acc: 0.96667
    Epoch [6000/10000], loss: 0.11243 acc: 1.00000 val_loss: 0.18042, val_acc: 0.96667
    Epoch [6010/10000], loss: 0.11230 acc: 1.00000 val_loss: 0.18031, val_acc: 0.96667
    Epoch [6020/10000], loss: 0.11217 acc: 1.00000 val_loss: 0.18021, val_acc: 0.96667
    Epoch [6030/10000], loss: 0.11205 acc: 1.00000 val_loss: 0.18010, val_acc: 0.96667
    Epoch [6040/10000], loss: 0.11192 acc: 1.00000 val_loss: 0.17999, val_acc: 0.96667
    Epoch [6050/10000], loss: 0.11179 acc: 1.00000 val_loss: 0.17989, val_acc: 0.96667
    Epoch [6060/10000], loss: 0.11167 acc: 1.00000 val_loss: 0.17978, val_acc: 0.96667
    Epoch [6070/10000], loss: 0.11154 acc: 1.00000 val_loss: 0.17968, val_acc: 0.96667
    Epoch [6080/10000], loss: 0.11142 acc: 1.00000 val_loss: 0.17957, val_acc: 0.96667
    Epoch [6090/10000], loss: 0.11129 acc: 1.00000 val_loss: 0.17947, val_acc: 0.96667
    Epoch [6100/10000], loss: 0.11117 acc: 1.00000 val_loss: 0.17936, val_acc: 0.96667
    Epoch [6110/10000], loss: 0.11104 acc: 1.00000 val_loss: 0.17926, val_acc: 0.96667
    Epoch [6120/10000], loss: 0.11092 acc: 1.00000 val_loss: 0.17915, val_acc: 0.96667
    Epoch [6130/10000], loss: 0.11079 acc: 1.00000 val_loss: 0.17905, val_acc: 0.96667
    Epoch [6140/10000], loss: 0.11067 acc: 1.00000 val_loss: 0.17894, val_acc: 0.96667
    Epoch [6150/10000], loss: 0.11055 acc: 1.00000 val_loss: 0.17884, val_acc: 0.96667
    Epoch [6160/10000], loss: 0.11043 acc: 1.00000 val_loss: 0.17874, val_acc: 0.96667
    Epoch [6170/10000], loss: 0.11030 acc: 1.00000 val_loss: 0.17864, val_acc: 0.96667
    Epoch [6180/10000], loss: 0.11018 acc: 1.00000 val_loss: 0.17853, val_acc: 0.96667
    Epoch [6190/10000], loss: 0.11006 acc: 1.00000 val_loss: 0.17843, val_acc: 0.96667
    Epoch [6200/10000], loss: 0.10994 acc: 1.00000 val_loss: 0.17833, val_acc: 0.96667
    Epoch [6210/10000], loss: 0.10982 acc: 1.00000 val_loss: 0.17823, val_acc: 0.96667
    Epoch [6220/10000], loss: 0.10970 acc: 1.00000 val_loss: 0.17813, val_acc: 0.96667
    Epoch [6230/10000], loss: 0.10958 acc: 1.00000 val_loss: 0.17803, val_acc: 0.96667
    Epoch [6240/10000], loss: 0.10946 acc: 1.00000 val_loss: 0.17793, val_acc: 0.96667
    Epoch [6250/10000], loss: 0.10934 acc: 1.00000 val_loss: 0.17783, val_acc: 0.96667
    Epoch [6260/10000], loss: 0.10922 acc: 1.00000 val_loss: 0.17773, val_acc: 0.96667
    Epoch [6270/10000], loss: 0.10910 acc: 1.00000 val_loss: 0.17763, val_acc: 0.96667
    Epoch [6280/10000], loss: 0.10898 acc: 1.00000 val_loss: 0.17753, val_acc: 0.96667
    Epoch [6290/10000], loss: 0.10886 acc: 1.00000 val_loss: 0.17743, val_acc: 0.96667
    Epoch [6300/10000], loss: 0.10874 acc: 1.00000 val_loss: 0.17733, val_acc: 0.96667
    Epoch [6310/10000], loss: 0.10863 acc: 1.00000 val_loss: 0.17723, val_acc: 0.96667
    Epoch [6320/10000], loss: 0.10851 acc: 1.00000 val_loss: 0.17713, val_acc: 0.96667
    Epoch [6330/10000], loss: 0.10839 acc: 1.00000 val_loss: 0.17704, val_acc: 0.96667
    Epoch [6340/10000], loss: 0.10828 acc: 1.00000 val_loss: 0.17694, val_acc: 0.96667
    Epoch [6350/10000], loss: 0.10816 acc: 1.00000 val_loss: 0.17684, val_acc: 0.96667
    Epoch [6360/10000], loss: 0.10804 acc: 1.00000 val_loss: 0.17675, val_acc: 0.96667
    Epoch [6370/10000], loss: 0.10793 acc: 1.00000 val_loss: 0.17665, val_acc: 0.96667
    Epoch [6380/10000], loss: 0.10781 acc: 1.00000 val_loss: 0.17655, val_acc: 0.96667
    Epoch [6390/10000], loss: 0.10770 acc: 1.00000 val_loss: 0.17646, val_acc: 0.96667
    Epoch [6400/10000], loss: 0.10758 acc: 1.00000 val_loss: 0.17636, val_acc: 0.96667
    Epoch [6410/10000], loss: 0.10747 acc: 1.00000 val_loss: 0.17627, val_acc: 0.96667
    Epoch [6420/10000], loss: 0.10735 acc: 1.00000 val_loss: 0.17617, val_acc: 0.96667
    Epoch [6430/10000], loss: 0.10724 acc: 1.00000 val_loss: 0.17608, val_acc: 0.96667
    Epoch [6440/10000], loss: 0.10713 acc: 1.00000 val_loss: 0.17598, val_acc: 0.96667
    Epoch [6450/10000], loss: 0.10701 acc: 1.00000 val_loss: 0.17589, val_acc: 0.96667
    Epoch [6460/10000], loss: 0.10690 acc: 1.00000 val_loss: 0.17579, val_acc: 0.96667
    Epoch [6470/10000], loss: 0.10679 acc: 1.00000 val_loss: 0.17570, val_acc: 0.96667
    Epoch [6480/10000], loss: 0.10667 acc: 1.00000 val_loss: 0.17561, val_acc: 0.96667
    Epoch [6490/10000], loss: 0.10656 acc: 1.00000 val_loss: 0.17551, val_acc: 0.96667
    Epoch [6500/10000], loss: 0.10645 acc: 1.00000 val_loss: 0.17542, val_acc: 0.96667
    Epoch [6510/10000], loss: 0.10634 acc: 1.00000 val_loss: 0.17533, val_acc: 0.96667
    Epoch [6520/10000], loss: 0.10623 acc: 1.00000 val_loss: 0.17523, val_acc: 0.96667
    Epoch [6530/10000], loss: 0.10612 acc: 1.00000 val_loss: 0.17514, val_acc: 0.96667
    Epoch [6540/10000], loss: 0.10600 acc: 1.00000 val_loss: 0.17505, val_acc: 0.96667
    Epoch [6550/10000], loss: 0.10589 acc: 1.00000 val_loss: 0.17496, val_acc: 0.96667
    Epoch [6560/10000], loss: 0.10578 acc: 1.00000 val_loss: 0.17487, val_acc: 0.96667
    Epoch [6570/10000], loss: 0.10567 acc: 1.00000 val_loss: 0.17478, val_acc: 0.96667
    Epoch [6580/10000], loss: 0.10556 acc: 1.00000 val_loss: 0.17468, val_acc: 0.96667
    Epoch [6590/10000], loss: 0.10546 acc: 1.00000 val_loss: 0.17459, val_acc: 0.96667
    Epoch [6600/10000], loss: 0.10535 acc: 1.00000 val_loss: 0.17450, val_acc: 0.96667
    Epoch [6610/10000], loss: 0.10524 acc: 1.00000 val_loss: 0.17441, val_acc: 0.96667
    Epoch [6620/10000], loss: 0.10513 acc: 1.00000 val_loss: 0.17432, val_acc: 0.96667
    Epoch [6630/10000], loss: 0.10502 acc: 1.00000 val_loss: 0.17423, val_acc: 0.96667
    Epoch [6640/10000], loss: 0.10491 acc: 1.00000 val_loss: 0.17414, val_acc: 0.96667
    Epoch [6650/10000], loss: 0.10481 acc: 1.00000 val_loss: 0.17406, val_acc: 0.96667
    Epoch [6660/10000], loss: 0.10470 acc: 1.00000 val_loss: 0.17397, val_acc: 0.96667
    Epoch [6670/10000], loss: 0.10459 acc: 1.00000 val_loss: 0.17388, val_acc: 0.96667
    Epoch [6680/10000], loss: 0.10448 acc: 1.00000 val_loss: 0.17379, val_acc: 0.96667
    Epoch [6690/10000], loss: 0.10438 acc: 1.00000 val_loss: 0.17370, val_acc: 0.96667
    Epoch [6700/10000], loss: 0.10427 acc: 1.00000 val_loss: 0.17361, val_acc: 0.96667
    Epoch [6710/10000], loss: 0.10417 acc: 1.00000 val_loss: 0.17353, val_acc: 0.96667
    Epoch [6720/10000], loss: 0.10406 acc: 1.00000 val_loss: 0.17344, val_acc: 0.96667
    Epoch [6730/10000], loss: 0.10395 acc: 1.00000 val_loss: 0.17335, val_acc: 0.96667
    Epoch [6740/10000], loss: 0.10385 acc: 1.00000 val_loss: 0.17326, val_acc: 0.96667
    Epoch [6750/10000], loss: 0.10374 acc: 1.00000 val_loss: 0.17318, val_acc: 0.96667
    Epoch [6760/10000], loss: 0.10364 acc: 1.00000 val_loss: 0.17309, val_acc: 0.96667
    Epoch [6770/10000], loss: 0.10354 acc: 1.00000 val_loss: 0.17301, val_acc: 0.96667
    Epoch [6780/10000], loss: 0.10343 acc: 1.00000 val_loss: 0.17292, val_acc: 0.96667
    Epoch [6790/10000], loss: 0.10333 acc: 1.00000 val_loss: 0.17283, val_acc: 0.96667
    Epoch [6800/10000], loss: 0.10322 acc: 1.00000 val_loss: 0.17275, val_acc: 0.96667
    Epoch [6810/10000], loss: 0.10312 acc: 1.00000 val_loss: 0.17266, val_acc: 0.96667
    Epoch [6820/10000], loss: 0.10302 acc: 1.00000 val_loss: 0.17258, val_acc: 0.96667
    Epoch [6830/10000], loss: 0.10292 acc: 1.00000 val_loss: 0.17249, val_acc: 0.96667
    Epoch [6840/10000], loss: 0.10281 acc: 1.00000 val_loss: 0.17241, val_acc: 0.96667
    Epoch [6850/10000], loss: 0.10271 acc: 1.00000 val_loss: 0.17233, val_acc: 0.96667
    Epoch [6860/10000], loss: 0.10261 acc: 1.00000 val_loss: 0.17224, val_acc: 0.96667
    Epoch [6870/10000], loss: 0.10251 acc: 1.00000 val_loss: 0.17216, val_acc: 0.96667
    Epoch [6880/10000], loss: 0.10241 acc: 1.00000 val_loss: 0.17207, val_acc: 0.96667
    Epoch [6890/10000], loss: 0.10230 acc: 1.00000 val_loss: 0.17199, val_acc: 0.96667
    Epoch [6900/10000], loss: 0.10220 acc: 1.00000 val_loss: 0.17191, val_acc: 0.96667
    Epoch [6910/10000], loss: 0.10210 acc: 1.00000 val_loss: 0.17182, val_acc: 0.96667
    Epoch [6920/10000], loss: 0.10200 acc: 1.00000 val_loss: 0.17174, val_acc: 0.96667
    Epoch [6930/10000], loss: 0.10190 acc: 1.00000 val_loss: 0.17166, val_acc: 0.96667
    Epoch [6940/10000], loss: 0.10180 acc: 1.00000 val_loss: 0.17158, val_acc: 0.96667
    Epoch [6950/10000], loss: 0.10170 acc: 1.00000 val_loss: 0.17150, val_acc: 0.96667
    Epoch [6960/10000], loss: 0.10160 acc: 1.00000 val_loss: 0.17141, val_acc: 0.96667
    Epoch [6970/10000], loss: 0.10150 acc: 1.00000 val_loss: 0.17133, val_acc: 0.96667
    Epoch [6980/10000], loss: 0.10140 acc: 1.00000 val_loss: 0.17125, val_acc: 0.96667
    Epoch [6990/10000], loss: 0.10130 acc: 1.00000 val_loss: 0.17117, val_acc: 0.96667
    Epoch [7000/10000], loss: 0.10121 acc: 1.00000 val_loss: 0.17109, val_acc: 0.96667
    Epoch [7010/10000], loss: 0.10111 acc: 1.00000 val_loss: 0.17101, val_acc: 0.96667
    Epoch [7020/10000], loss: 0.10101 acc: 1.00000 val_loss: 0.17093, val_acc: 0.96667
    Epoch [7030/10000], loss: 0.10091 acc: 1.00000 val_loss: 0.17085, val_acc: 0.96667
    Epoch [7040/10000], loss: 0.10081 acc: 1.00000 val_loss: 0.17077, val_acc: 0.96667
    Epoch [7050/10000], loss: 0.10072 acc: 1.00000 val_loss: 0.17069, val_acc: 0.96667
    Epoch [7060/10000], loss: 0.10062 acc: 1.00000 val_loss: 0.17061, val_acc: 0.96667
    Epoch [7070/10000], loss: 0.10052 acc: 1.00000 val_loss: 0.17053, val_acc: 0.96667
    Epoch [7080/10000], loss: 0.10043 acc: 1.00000 val_loss: 0.17045, val_acc: 0.96667
    Epoch [7090/10000], loss: 0.10033 acc: 1.00000 val_loss: 0.17037, val_acc: 0.96667
    Epoch [7100/10000], loss: 0.10023 acc: 1.00000 val_loss: 0.17029, val_acc: 0.96667
    Epoch [7110/10000], loss: 0.10014 acc: 1.00000 val_loss: 0.17021, val_acc: 0.96667
    Epoch [7120/10000], loss: 0.10004 acc: 1.00000 val_loss: 0.17014, val_acc: 0.96667
    Epoch [7130/10000], loss: 0.09995 acc: 1.00000 val_loss: 0.17006, val_acc: 0.96667
    Epoch [7140/10000], loss: 0.09985 acc: 1.00000 val_loss: 0.16998, val_acc: 0.96667
    Epoch [7150/10000], loss: 0.09976 acc: 1.00000 val_loss: 0.16990, val_acc: 0.96667
    Epoch [7160/10000], loss: 0.09966 acc: 1.00000 val_loss: 0.16982, val_acc: 0.96667
    Epoch [7170/10000], loss: 0.09957 acc: 1.00000 val_loss: 0.16975, val_acc: 0.96667
    Epoch [7180/10000], loss: 0.09947 acc: 1.00000 val_loss: 0.16967, val_acc: 0.96667
    Epoch [7190/10000], loss: 0.09938 acc: 1.00000 val_loss: 0.16959, val_acc: 0.96667
    Epoch [7200/10000], loss: 0.09928 acc: 1.00000 val_loss: 0.16952, val_acc: 0.96667
    Epoch [7210/10000], loss: 0.09919 acc: 1.00000 val_loss: 0.16944, val_acc: 0.96667
    Epoch [7220/10000], loss: 0.09910 acc: 1.00000 val_loss: 0.16936, val_acc: 0.96667
    Epoch [7230/10000], loss: 0.09900 acc: 1.00000 val_loss: 0.16929, val_acc: 0.96667
    Epoch [7240/10000], loss: 0.09891 acc: 1.00000 val_loss: 0.16921, val_acc: 0.96667
    Epoch [7250/10000], loss: 0.09882 acc: 1.00000 val_loss: 0.16914, val_acc: 0.96667
    Epoch [7260/10000], loss: 0.09873 acc: 1.00000 val_loss: 0.16906, val_acc: 0.96667
    Epoch [7270/10000], loss: 0.09863 acc: 1.00000 val_loss: 0.16899, val_acc: 0.96667
    Epoch [7280/10000], loss: 0.09854 acc: 1.00000 val_loss: 0.16891, val_acc: 0.96667
    Epoch [7290/10000], loss: 0.09845 acc: 1.00000 val_loss: 0.16884, val_acc: 0.96667
    Epoch [7300/10000], loss: 0.09836 acc: 1.00000 val_loss: 0.16876, val_acc: 0.96667
    Epoch [7310/10000], loss: 0.09827 acc: 1.00000 val_loss: 0.16869, val_acc: 0.96667
    Epoch [7320/10000], loss: 0.09817 acc: 1.00000 val_loss: 0.16861, val_acc: 0.96667
    Epoch [7330/10000], loss: 0.09808 acc: 1.00000 val_loss: 0.16854, val_acc: 0.96667
    Epoch [7340/10000], loss: 0.09799 acc: 1.00000 val_loss: 0.16846, val_acc: 0.96667
    Epoch [7350/10000], loss: 0.09790 acc: 1.00000 val_loss: 0.16839, val_acc: 0.96667
    Epoch [7360/10000], loss: 0.09781 acc: 1.00000 val_loss: 0.16832, val_acc: 0.96667
    Epoch [7370/10000], loss: 0.09772 acc: 1.00000 val_loss: 0.16824, val_acc: 0.96667
    Epoch [7380/10000], loss: 0.09763 acc: 1.00000 val_loss: 0.16817, val_acc: 0.96667
    Epoch [7390/10000], loss: 0.09754 acc: 1.00000 val_loss: 0.16810, val_acc: 0.96667
    Epoch [7400/10000], loss: 0.09745 acc: 1.00000 val_loss: 0.16802, val_acc: 0.96667
    Epoch [7410/10000], loss: 0.09736 acc: 1.00000 val_loss: 0.16795, val_acc: 0.96667
    Epoch [7420/10000], loss: 0.09727 acc: 1.00000 val_loss: 0.16788, val_acc: 0.96667
    Epoch [7430/10000], loss: 0.09718 acc: 1.00000 val_loss: 0.16781, val_acc: 0.96667
    Epoch [7440/10000], loss: 0.09710 acc: 1.00000 val_loss: 0.16774, val_acc: 0.96667
    Epoch [7450/10000], loss: 0.09701 acc: 1.00000 val_loss: 0.16766, val_acc: 0.96667
    Epoch [7460/10000], loss: 0.09692 acc: 1.00000 val_loss: 0.16759, val_acc: 0.96667
    Epoch [7470/10000], loss: 0.09683 acc: 1.00000 val_loss: 0.16752, val_acc: 0.96667
    Epoch [7480/10000], loss: 0.09674 acc: 1.00000 val_loss: 0.16745, val_acc: 0.96667
    Epoch [7490/10000], loss: 0.09665 acc: 1.00000 val_loss: 0.16738, val_acc: 0.96667
    Epoch [7500/10000], loss: 0.09657 acc: 1.00000 val_loss: 0.16731, val_acc: 0.96667
    Epoch [7510/10000], loss: 0.09648 acc: 1.00000 val_loss: 0.16724, val_acc: 0.96667
    Epoch [7520/10000], loss: 0.09639 acc: 1.00000 val_loss: 0.16717, val_acc: 0.96667
    Epoch [7530/10000], loss: 0.09631 acc: 1.00000 val_loss: 0.16710, val_acc: 0.96667
    Epoch [7540/10000], loss: 0.09622 acc: 1.00000 val_loss: 0.16703, val_acc: 0.96667
    Epoch [7550/10000], loss: 0.09613 acc: 1.00000 val_loss: 0.16696, val_acc: 0.96667
    Epoch [7560/10000], loss: 0.09605 acc: 1.00000 val_loss: 0.16689, val_acc: 0.96667
    Epoch [7570/10000], loss: 0.09596 acc: 1.00000 val_loss: 0.16682, val_acc: 0.96667
    Epoch [7580/10000], loss: 0.09587 acc: 1.00000 val_loss: 0.16675, val_acc: 0.96667
    Epoch [7590/10000], loss: 0.09579 acc: 1.00000 val_loss: 0.16668, val_acc: 0.96667
    Epoch [7600/10000], loss: 0.09570 acc: 1.00000 val_loss: 0.16661, val_acc: 0.96667
    Epoch [7610/10000], loss: 0.09562 acc: 1.00000 val_loss: 0.16654, val_acc: 0.96667
    Epoch [7620/10000], loss: 0.09553 acc: 1.00000 val_loss: 0.16647, val_acc: 0.96667
    Epoch [7630/10000], loss: 0.09545 acc: 1.00000 val_loss: 0.16640, val_acc: 0.96667
    Epoch [7640/10000], loss: 0.09536 acc: 1.00000 val_loss: 0.16633, val_acc: 0.96667
    Epoch [7650/10000], loss: 0.09528 acc: 1.00000 val_loss: 0.16626, val_acc: 0.96667
    Epoch [7660/10000], loss: 0.09519 acc: 1.00000 val_loss: 0.16620, val_acc: 0.96667
    Epoch [7670/10000], loss: 0.09511 acc: 1.00000 val_loss: 0.16613, val_acc: 0.96667
    Epoch [7680/10000], loss: 0.09502 acc: 1.00000 val_loss: 0.16606, val_acc: 0.96667
    Epoch [7690/10000], loss: 0.09494 acc: 1.00000 val_loss: 0.16599, val_acc: 0.96667
    Epoch [7700/10000], loss: 0.09486 acc: 1.00000 val_loss: 0.16593, val_acc: 0.96667
    Epoch [7710/10000], loss: 0.09477 acc: 1.00000 val_loss: 0.16586, val_acc: 0.96667
    Epoch [7720/10000], loss: 0.09469 acc: 1.00000 val_loss: 0.16579, val_acc: 0.96667
    Epoch [7730/10000], loss: 0.09461 acc: 1.00000 val_loss: 0.16572, val_acc: 0.96667
    Epoch [7740/10000], loss: 0.09452 acc: 1.00000 val_loss: 0.16566, val_acc: 0.96667
    Epoch [7750/10000], loss: 0.09444 acc: 1.00000 val_loss: 0.16559, val_acc: 0.96667
    Epoch [7760/10000], loss: 0.09436 acc: 1.00000 val_loss: 0.16552, val_acc: 0.96667
    Epoch [7770/10000], loss: 0.09428 acc: 1.00000 val_loss: 0.16546, val_acc: 0.96667
    Epoch [7780/10000], loss: 0.09419 acc: 1.00000 val_loss: 0.16539, val_acc: 0.96667
    Epoch [7790/10000], loss: 0.09411 acc: 1.00000 val_loss: 0.16533, val_acc: 0.96667
    Epoch [7800/10000], loss: 0.09403 acc: 1.00000 val_loss: 0.16526, val_acc: 0.96667
    Epoch [7810/10000], loss: 0.09395 acc: 1.00000 val_loss: 0.16519, val_acc: 0.96667
    Epoch [7820/10000], loss: 0.09387 acc: 1.00000 val_loss: 0.16513, val_acc: 0.96667
    Epoch [7830/10000], loss: 0.09378 acc: 1.00000 val_loss: 0.16506, val_acc: 0.96667
    Epoch [7840/10000], loss: 0.09370 acc: 1.00000 val_loss: 0.16500, val_acc: 0.96667
    Epoch [7850/10000], loss: 0.09362 acc: 1.00000 val_loss: 0.16493, val_acc: 0.96667
    Epoch [7860/10000], loss: 0.09354 acc: 1.00000 val_loss: 0.16487, val_acc: 0.96667
    Epoch [7870/10000], loss: 0.09346 acc: 1.00000 val_loss: 0.16480, val_acc: 0.96667
    Epoch [7880/10000], loss: 0.09338 acc: 1.00000 val_loss: 0.16474, val_acc: 0.96667
    Epoch [7890/10000], loss: 0.09330 acc: 1.00000 val_loss: 0.16468, val_acc: 0.96667
    Epoch [7900/10000], loss: 0.09322 acc: 1.00000 val_loss: 0.16461, val_acc: 0.96667
    Epoch [7910/10000], loss: 0.09314 acc: 1.00000 val_loss: 0.16455, val_acc: 0.96667
    Epoch [7920/10000], loss: 0.09306 acc: 1.00000 val_loss: 0.16448, val_acc: 0.96667
    Epoch [7930/10000], loss: 0.09298 acc: 1.00000 val_loss: 0.16442, val_acc: 0.96667
    Epoch [7940/10000], loss: 0.09290 acc: 1.00000 val_loss: 0.16436, val_acc: 0.96667
    Epoch [7950/10000], loss: 0.09282 acc: 1.00000 val_loss: 0.16429, val_acc: 0.96667
    Epoch [7960/10000], loss: 0.09274 acc: 1.00000 val_loss: 0.16423, val_acc: 0.96667
    Epoch [7970/10000], loss: 0.09266 acc: 1.00000 val_loss: 0.16417, val_acc: 0.96667
    Epoch [7980/10000], loss: 0.09259 acc: 1.00000 val_loss: 0.16410, val_acc: 0.96667
    Epoch [7990/10000], loss: 0.09251 acc: 1.00000 val_loss: 0.16404, val_acc: 0.96667
    Epoch [8000/10000], loss: 0.09243 acc: 1.00000 val_loss: 0.16398, val_acc: 0.96667
    Epoch [8010/10000], loss: 0.09235 acc: 1.00000 val_loss: 0.16392, val_acc: 0.96667
    Epoch [8020/10000], loss: 0.09227 acc: 1.00000 val_loss: 0.16385, val_acc: 0.96667
    Epoch [8030/10000], loss: 0.09219 acc: 1.00000 val_loss: 0.16379, val_acc: 0.96667
    Epoch [8040/10000], loss: 0.09212 acc: 1.00000 val_loss: 0.16373, val_acc: 0.96667
    Epoch [8050/10000], loss: 0.09204 acc: 1.00000 val_loss: 0.16367, val_acc: 0.96667
    Epoch [8060/10000], loss: 0.09196 acc: 1.00000 val_loss: 0.16361, val_acc: 0.96667
    Epoch [8070/10000], loss: 0.09188 acc: 1.00000 val_loss: 0.16354, val_acc: 0.96667
    Epoch [8080/10000], loss: 0.09181 acc: 1.00000 val_loss: 0.16348, val_acc: 0.96667
    Epoch [8090/10000], loss: 0.09173 acc: 1.00000 val_loss: 0.16342, val_acc: 0.96667
    Epoch [8100/10000], loss: 0.09165 acc: 1.00000 val_loss: 0.16336, val_acc: 0.96667
    Epoch [8110/10000], loss: 0.09158 acc: 1.00000 val_loss: 0.16330, val_acc: 0.96667
    Epoch [8120/10000], loss: 0.09150 acc: 1.00000 val_loss: 0.16324, val_acc: 0.96667
    Epoch [8130/10000], loss: 0.09142 acc: 1.00000 val_loss: 0.16318, val_acc: 0.96667
    Epoch [8140/10000], loss: 0.09135 acc: 1.00000 val_loss: 0.16312, val_acc: 0.96667
    Epoch [8150/10000], loss: 0.09127 acc: 1.00000 val_loss: 0.16306, val_acc: 0.96667
    Epoch [8160/10000], loss: 0.09120 acc: 1.00000 val_loss: 0.16300, val_acc: 0.96667
    Epoch [8170/10000], loss: 0.09112 acc: 1.00000 val_loss: 0.16294, val_acc: 0.96667
    Epoch [8180/10000], loss: 0.09105 acc: 1.00000 val_loss: 0.16288, val_acc: 0.96667
    Epoch [8190/10000], loss: 0.09097 acc: 1.00000 val_loss: 0.16282, val_acc: 0.96667
    Epoch [8200/10000], loss: 0.09089 acc: 1.00000 val_loss: 0.16276, val_acc: 0.96667
    Epoch [8210/10000], loss: 0.09082 acc: 1.00000 val_loss: 0.16270, val_acc: 0.96667
    Epoch [8220/10000], loss: 0.09074 acc: 1.00000 val_loss: 0.16264, val_acc: 0.96667
    Epoch [8230/10000], loss: 0.09067 acc: 1.00000 val_loss: 0.16258, val_acc: 0.96667
    Epoch [8240/10000], loss: 0.09060 acc: 1.00000 val_loss: 0.16252, val_acc: 0.96667
    Epoch [8250/10000], loss: 0.09052 acc: 1.00000 val_loss: 0.16246, val_acc: 0.96667
    Epoch [8260/10000], loss: 0.09045 acc: 1.00000 val_loss: 0.16240, val_acc: 0.96667
    Epoch [8270/10000], loss: 0.09037 acc: 1.00000 val_loss: 0.16234, val_acc: 0.96667
    Epoch [8280/10000], loss: 0.09030 acc: 1.00000 val_loss: 0.16228, val_acc: 0.96667
    Epoch [8290/10000], loss: 0.09023 acc: 1.00000 val_loss: 0.16222, val_acc: 0.96667
    Epoch [8300/10000], loss: 0.09015 acc: 1.00000 val_loss: 0.16217, val_acc: 0.96667
    Epoch [8310/10000], loss: 0.09008 acc: 1.00000 val_loss: 0.16211, val_acc: 0.96667
    Epoch [8320/10000], loss: 0.09000 acc: 1.00000 val_loss: 0.16205, val_acc: 0.96667
    Epoch [8330/10000], loss: 0.08993 acc: 1.00000 val_loss: 0.16199, val_acc: 0.96667
    Epoch [8340/10000], loss: 0.08986 acc: 1.00000 val_loss: 0.16193, val_acc: 0.96667
    Epoch [8350/10000], loss: 0.08979 acc: 1.00000 val_loss: 0.16188, val_acc: 0.96667
    Epoch [8360/10000], loss: 0.08971 acc: 1.00000 val_loss: 0.16182, val_acc: 0.96667
    Epoch [8370/10000], loss: 0.08964 acc: 1.00000 val_loss: 0.16176, val_acc: 0.96667
    Epoch [8380/10000], loss: 0.08957 acc: 1.00000 val_loss: 0.16170, val_acc: 0.96667
    Epoch [8390/10000], loss: 0.08950 acc: 1.00000 val_loss: 0.16165, val_acc: 0.96667
    Epoch [8400/10000], loss: 0.08942 acc: 1.00000 val_loss: 0.16159, val_acc: 0.96667
    Epoch [8410/10000], loss: 0.08935 acc: 1.00000 val_loss: 0.16153, val_acc: 0.96667
    Epoch [8420/10000], loss: 0.08928 acc: 1.00000 val_loss: 0.16148, val_acc: 0.96667
    Epoch [8430/10000], loss: 0.08921 acc: 1.00000 val_loss: 0.16142, val_acc: 0.96667
    Epoch [8440/10000], loss: 0.08914 acc: 1.00000 val_loss: 0.16136, val_acc: 0.96667
    Epoch [8450/10000], loss: 0.08907 acc: 1.00000 val_loss: 0.16131, val_acc: 0.96667
    Epoch [8460/10000], loss: 0.08899 acc: 1.00000 val_loss: 0.16125, val_acc: 0.96667
    Epoch [8470/10000], loss: 0.08892 acc: 1.00000 val_loss: 0.16119, val_acc: 0.96667
    Epoch [8480/10000], loss: 0.08885 acc: 1.00000 val_loss: 0.16114, val_acc: 0.96667
    Epoch [8490/10000], loss: 0.08878 acc: 1.00000 val_loss: 0.16108, val_acc: 0.96667
    Epoch [8500/10000], loss: 0.08871 acc: 1.00000 val_loss: 0.16103, val_acc: 0.96667
    Epoch [8510/10000], loss: 0.08864 acc: 1.00000 val_loss: 0.16097, val_acc: 0.96667
    Epoch [8520/10000], loss: 0.08857 acc: 1.00000 val_loss: 0.16092, val_acc: 0.96667
    Epoch [8530/10000], loss: 0.08850 acc: 1.00000 val_loss: 0.16086, val_acc: 0.96667
    Epoch [8540/10000], loss: 0.08843 acc: 1.00000 val_loss: 0.16081, val_acc: 0.96667
    Epoch [8550/10000], loss: 0.08836 acc: 1.00000 val_loss: 0.16075, val_acc: 0.96667
    Epoch [8560/10000], loss: 0.08829 acc: 1.00000 val_loss: 0.16070, val_acc: 0.96667
    Epoch [8570/10000], loss: 0.08822 acc: 1.00000 val_loss: 0.16064, val_acc: 0.96667
    Epoch [8580/10000], loss: 0.08815 acc: 1.00000 val_loss: 0.16059, val_acc: 0.96667
    Epoch [8590/10000], loss: 0.08808 acc: 1.00000 val_loss: 0.16053, val_acc: 0.96667
    Epoch [8600/10000], loss: 0.08801 acc: 1.00000 val_loss: 0.16048, val_acc: 0.96667
    Epoch [8610/10000], loss: 0.08794 acc: 1.00000 val_loss: 0.16042, val_acc: 0.96667
    Epoch [8620/10000], loss: 0.08787 acc: 1.00000 val_loss: 0.16037, val_acc: 0.96667
    Epoch [8630/10000], loss: 0.08780 acc: 1.00000 val_loss: 0.16031, val_acc: 0.96667
    Epoch [8640/10000], loss: 0.08774 acc: 1.00000 val_loss: 0.16026, val_acc: 0.96667
    Epoch [8650/10000], loss: 0.08767 acc: 1.00000 val_loss: 0.16021, val_acc: 0.96667
    Epoch [8660/10000], loss: 0.08760 acc: 1.00000 val_loss: 0.16015, val_acc: 0.96667
    Epoch [8670/10000], loss: 0.08753 acc: 1.00000 val_loss: 0.16010, val_acc: 0.96667
    Epoch [8680/10000], loss: 0.08746 acc: 1.00000 val_loss: 0.16005, val_acc: 0.96667
    Epoch [8690/10000], loss: 0.08739 acc: 1.00000 val_loss: 0.15999, val_acc: 0.96667
    Epoch [8700/10000], loss: 0.08733 acc: 1.00000 val_loss: 0.15994, val_acc: 0.96667
    Epoch [8710/10000], loss: 0.08726 acc: 1.00000 val_loss: 0.15989, val_acc: 0.96667
    Epoch [8720/10000], loss: 0.08719 acc: 1.00000 val_loss: 0.15983, val_acc: 0.96667
    Epoch [8730/10000], loss: 0.08712 acc: 1.00000 val_loss: 0.15978, val_acc: 0.96667
    Epoch [8740/10000], loss: 0.08706 acc: 1.00000 val_loss: 0.15973, val_acc: 0.96667
    Epoch [8750/10000], loss: 0.08699 acc: 1.00000 val_loss: 0.15967, val_acc: 0.96667
    Epoch [8760/10000], loss: 0.08692 acc: 1.00000 val_loss: 0.15962, val_acc: 0.96667
    Epoch [8770/10000], loss: 0.08685 acc: 1.00000 val_loss: 0.15957, val_acc: 0.96667
    Epoch [8780/10000], loss: 0.08679 acc: 1.00000 val_loss: 0.15952, val_acc: 0.96667
    Epoch [8790/10000], loss: 0.08672 acc: 1.00000 val_loss: 0.15946, val_acc: 0.96667
    Epoch [8800/10000], loss: 0.08665 acc: 1.00000 val_loss: 0.15941, val_acc: 0.96667
    Epoch [8810/10000], loss: 0.08659 acc: 1.00000 val_loss: 0.15936, val_acc: 0.96667
    Epoch [8820/10000], loss: 0.08652 acc: 1.00000 val_loss: 0.15931, val_acc: 0.96667
    Epoch [8830/10000], loss: 0.08646 acc: 1.00000 val_loss: 0.15926, val_acc: 0.96667
    Epoch [8840/10000], loss: 0.08639 acc: 1.00000 val_loss: 0.15921, val_acc: 0.96667
    Epoch [8850/10000], loss: 0.08632 acc: 1.00000 val_loss: 0.15915, val_acc: 0.96667
    Epoch [8860/10000], loss: 0.08626 acc: 1.00000 val_loss: 0.15910, val_acc: 0.96667
    Epoch [8870/10000], loss: 0.08619 acc: 1.00000 val_loss: 0.15905, val_acc: 0.96667
    Epoch [8880/10000], loss: 0.08613 acc: 1.00000 val_loss: 0.15900, val_acc: 0.96667
    Epoch [8890/10000], loss: 0.08606 acc: 1.00000 val_loss: 0.15895, val_acc: 0.96667
    Epoch [8900/10000], loss: 0.08600 acc: 1.00000 val_loss: 0.15890, val_acc: 0.96667
    Epoch [8910/10000], loss: 0.08593 acc: 1.00000 val_loss: 0.15885, val_acc: 0.96667
    Epoch [8920/10000], loss: 0.08587 acc: 1.00000 val_loss: 0.15880, val_acc: 0.96667
    Epoch [8930/10000], loss: 0.08580 acc: 1.00000 val_loss: 0.15875, val_acc: 0.96667
    Epoch [8940/10000], loss: 0.08574 acc: 1.00000 val_loss: 0.15870, val_acc: 0.96667
    Epoch [8950/10000], loss: 0.08567 acc: 1.00000 val_loss: 0.15865, val_acc: 0.96667
    Epoch [8960/10000], loss: 0.08561 acc: 1.00000 val_loss: 0.15859, val_acc: 0.96667
    Epoch [8970/10000], loss: 0.08554 acc: 1.00000 val_loss: 0.15854, val_acc: 0.96667
    Epoch [8980/10000], loss: 0.08548 acc: 1.00000 val_loss: 0.15849, val_acc: 0.96667
    Epoch [8990/10000], loss: 0.08541 acc: 1.00000 val_loss: 0.15844, val_acc: 0.96667
    Epoch [9000/10000], loss: 0.08535 acc: 1.00000 val_loss: 0.15839, val_acc: 0.96667
    Epoch [9010/10000], loss: 0.08529 acc: 1.00000 val_loss: 0.15834, val_acc: 0.96667
    Epoch [9020/10000], loss: 0.08522 acc: 1.00000 val_loss: 0.15830, val_acc: 0.96667
    Epoch [9030/10000], loss: 0.08516 acc: 1.00000 val_loss: 0.15825, val_acc: 0.96667
    Epoch [9040/10000], loss: 0.08509 acc: 1.00000 val_loss: 0.15820, val_acc: 0.96667
    Epoch [9050/10000], loss: 0.08503 acc: 1.00000 val_loss: 0.15815, val_acc: 0.96667
    Epoch [9060/10000], loss: 0.08497 acc: 1.00000 val_loss: 0.15810, val_acc: 0.96667
    Epoch [9070/10000], loss: 0.08490 acc: 1.00000 val_loss: 0.15805, val_acc: 0.96667
    Epoch [9080/10000], loss: 0.08484 acc: 1.00000 val_loss: 0.15800, val_acc: 0.96667
    Epoch [9090/10000], loss: 0.08478 acc: 1.00000 val_loss: 0.15795, val_acc: 0.96667
    Epoch [9100/10000], loss: 0.08472 acc: 1.00000 val_loss: 0.15790, val_acc: 0.96667
    Epoch [9110/10000], loss: 0.08465 acc: 1.00000 val_loss: 0.15785, val_acc: 0.96667
    Epoch [9120/10000], loss: 0.08459 acc: 1.00000 val_loss: 0.15781, val_acc: 0.96667
    Epoch [9130/10000], loss: 0.08453 acc: 1.00000 val_loss: 0.15776, val_acc: 0.96667
    Epoch [9140/10000], loss: 0.08446 acc: 1.00000 val_loss: 0.15771, val_acc: 0.96667
    Epoch [9150/10000], loss: 0.08440 acc: 1.00000 val_loss: 0.15766, val_acc: 0.96667
    Epoch [9160/10000], loss: 0.08434 acc: 1.00000 val_loss: 0.15761, val_acc: 0.96667
    Epoch [9170/10000], loss: 0.08428 acc: 1.00000 val_loss: 0.15756, val_acc: 0.96667
    Epoch [9180/10000], loss: 0.08422 acc: 1.00000 val_loss: 0.15752, val_acc: 0.96667
    Epoch [9190/10000], loss: 0.08415 acc: 1.00000 val_loss: 0.15747, val_acc: 0.96667
    Epoch [9200/10000], loss: 0.08409 acc: 1.00000 val_loss: 0.15742, val_acc: 0.96667
    Epoch [9210/10000], loss: 0.08403 acc: 1.00000 val_loss: 0.15737, val_acc: 0.96667
    Epoch [9220/10000], loss: 0.08397 acc: 1.00000 val_loss: 0.15733, val_acc: 0.96667
    Epoch [9230/10000], loss: 0.08391 acc: 1.00000 val_loss: 0.15728, val_acc: 0.96667
    Epoch [9240/10000], loss: 0.08385 acc: 1.00000 val_loss: 0.15723, val_acc: 0.96667
    Epoch [9250/10000], loss: 0.08379 acc: 1.00000 val_loss: 0.15718, val_acc: 0.96667
    Epoch [9260/10000], loss: 0.08372 acc: 1.00000 val_loss: 0.15714, val_acc: 0.96667
    Epoch [9270/10000], loss: 0.08366 acc: 1.00000 val_loss: 0.15709, val_acc: 0.96667
    Epoch [9280/10000], loss: 0.08360 acc: 1.00000 val_loss: 0.15704, val_acc: 0.96667
    Epoch [9290/10000], loss: 0.08354 acc: 1.00000 val_loss: 0.15700, val_acc: 0.96667
    Epoch [9300/10000], loss: 0.08348 acc: 1.00000 val_loss: 0.15695, val_acc: 0.96667
    Epoch [9310/10000], loss: 0.08342 acc: 1.00000 val_loss: 0.15690, val_acc: 0.96667
    Epoch [9320/10000], loss: 0.08336 acc: 1.00000 val_loss: 0.15686, val_acc: 0.96667
    Epoch [9330/10000], loss: 0.08330 acc: 1.00000 val_loss: 0.15681, val_acc: 0.96667
    Epoch [9340/10000], loss: 0.08324 acc: 1.00000 val_loss: 0.15676, val_acc: 0.96667
    Epoch [9350/10000], loss: 0.08318 acc: 1.00000 val_loss: 0.15672, val_acc: 0.96667
    Epoch [9360/10000], loss: 0.08312 acc: 1.00000 val_loss: 0.15667, val_acc: 0.96667
    Epoch [9370/10000], loss: 0.08306 acc: 1.00000 val_loss: 0.15662, val_acc: 0.96667
    Epoch [9380/10000], loss: 0.08300 acc: 1.00000 val_loss: 0.15658, val_acc: 0.96667
    Epoch [9390/10000], loss: 0.08294 acc: 1.00000 val_loss: 0.15653, val_acc: 0.96667
    Epoch [9400/10000], loss: 0.08288 acc: 1.00000 val_loss: 0.15649, val_acc: 0.96667
    Epoch [9410/10000], loss: 0.08282 acc: 1.00000 val_loss: 0.15644, val_acc: 0.96667
    Epoch [9420/10000], loss: 0.08276 acc: 1.00000 val_loss: 0.15640, val_acc: 0.96667
    Epoch [9430/10000], loss: 0.08270 acc: 1.00000 val_loss: 0.15635, val_acc: 0.96667
    Epoch [9440/10000], loss: 0.08265 acc: 1.00000 val_loss: 0.15630, val_acc: 0.96667
    Epoch [9450/10000], loss: 0.08259 acc: 1.00000 val_loss: 0.15626, val_acc: 0.96667
    Epoch [9460/10000], loss: 0.08253 acc: 1.00000 val_loss: 0.15621, val_acc: 0.96667
    Epoch [9470/10000], loss: 0.08247 acc: 1.00000 val_loss: 0.15617, val_acc: 0.96667
    Epoch [9480/10000], loss: 0.08241 acc: 1.00000 val_loss: 0.15612, val_acc: 0.96667
    Epoch [9490/10000], loss: 0.08235 acc: 1.00000 val_loss: 0.15608, val_acc: 0.96667
    Epoch [9500/10000], loss: 0.08229 acc: 1.00000 val_loss: 0.15603, val_acc: 0.96667
    Epoch [9510/10000], loss: 0.08224 acc: 1.00000 val_loss: 0.15599, val_acc: 0.96667
    Epoch [9520/10000], loss: 0.08218 acc: 1.00000 val_loss: 0.15594, val_acc: 0.96667
    Epoch [9530/10000], loss: 0.08212 acc: 1.00000 val_loss: 0.15590, val_acc: 0.96667
    Epoch [9540/10000], loss: 0.08206 acc: 1.00000 val_loss: 0.15586, val_acc: 0.96667
    Epoch [9550/10000], loss: 0.08200 acc: 1.00000 val_loss: 0.15581, val_acc: 0.96667
    Epoch [9560/10000], loss: 0.08195 acc: 1.00000 val_loss: 0.15577, val_acc: 0.96667
    Epoch [9570/10000], loss: 0.08189 acc: 1.00000 val_loss: 0.15572, val_acc: 0.96667
    Epoch [9580/10000], loss: 0.08183 acc: 1.00000 val_loss: 0.15568, val_acc: 0.96667
    Epoch [9590/10000], loss: 0.08177 acc: 1.00000 val_loss: 0.15563, val_acc: 0.96667
    Epoch [9600/10000], loss: 0.08172 acc: 1.00000 val_loss: 0.15559, val_acc: 0.96667
    Epoch [9610/10000], loss: 0.08166 acc: 1.00000 val_loss: 0.15555, val_acc: 0.96667
    Epoch [9620/10000], loss: 0.08160 acc: 1.00000 val_loss: 0.15550, val_acc: 0.96667
    Epoch [9630/10000], loss: 0.08154 acc: 1.00000 val_loss: 0.15546, val_acc: 0.96667
    Epoch [9640/10000], loss: 0.08149 acc: 1.00000 val_loss: 0.15542, val_acc: 0.96667
    Epoch [9650/10000], loss: 0.08143 acc: 1.00000 val_loss: 0.15537, val_acc: 0.96667
    Epoch [9660/10000], loss: 0.08137 acc: 1.00000 val_loss: 0.15533, val_acc: 0.96667
    Epoch [9670/10000], loss: 0.08132 acc: 1.00000 val_loss: 0.15529, val_acc: 0.96667
    Epoch [9680/10000], loss: 0.08126 acc: 1.00000 val_loss: 0.15524, val_acc: 0.96667
    Epoch [9690/10000], loss: 0.08120 acc: 1.00000 val_loss: 0.15520, val_acc: 0.96667
    Epoch [9700/10000], loss: 0.08115 acc: 1.00000 val_loss: 0.15516, val_acc: 0.96667
    Epoch [9710/10000], loss: 0.08109 acc: 1.00000 val_loss: 0.15511, val_acc: 0.96667
    Epoch [9720/10000], loss: 0.08103 acc: 1.00000 val_loss: 0.15507, val_acc: 0.96667
    Epoch [9730/10000], loss: 0.08098 acc: 1.00000 val_loss: 0.15503, val_acc: 0.96667
    Epoch [9740/10000], loss: 0.08092 acc: 1.00000 val_loss: 0.15499, val_acc: 0.96667
    Epoch [9750/10000], loss: 0.08087 acc: 1.00000 val_loss: 0.15494, val_acc: 0.96667
    Epoch [9760/10000], loss: 0.08081 acc: 1.00000 val_loss: 0.15490, val_acc: 0.96667
    Epoch [9770/10000], loss: 0.08076 acc: 1.00000 val_loss: 0.15486, val_acc: 0.96667
    Epoch [9780/10000], loss: 0.08070 acc: 1.00000 val_loss: 0.15482, val_acc: 0.96667
    Epoch [9790/10000], loss: 0.08064 acc: 1.00000 val_loss: 0.15477, val_acc: 0.96667
    Epoch [9800/10000], loss: 0.08059 acc: 1.00000 val_loss: 0.15473, val_acc: 0.96667
    Epoch [9810/10000], loss: 0.08053 acc: 1.00000 val_loss: 0.15469, val_acc: 0.96667
    Epoch [9820/10000], loss: 0.08048 acc: 1.00000 val_loss: 0.15465, val_acc: 0.96667
    Epoch [9830/10000], loss: 0.08042 acc: 1.00000 val_loss: 0.15461, val_acc: 0.96667
    Epoch [9840/10000], loss: 0.08037 acc: 1.00000 val_loss: 0.15456, val_acc: 0.96667
    Epoch [9850/10000], loss: 0.08031 acc: 1.00000 val_loss: 0.15452, val_acc: 0.96667
    Epoch [9860/10000], loss: 0.08026 acc: 1.00000 val_loss: 0.15448, val_acc: 0.96667
    Epoch [9870/10000], loss: 0.08020 acc: 1.00000 val_loss: 0.15444, val_acc: 0.96667
    Epoch [9880/10000], loss: 0.08015 acc: 1.00000 val_loss: 0.15440, val_acc: 0.96667
    Epoch [9890/10000], loss: 0.08009 acc: 1.00000 val_loss: 0.15436, val_acc: 0.96667
    Epoch [9900/10000], loss: 0.08004 acc: 1.00000 val_loss: 0.15432, val_acc: 0.96667
    Epoch [9910/10000], loss: 0.07999 acc: 1.00000 val_loss: 0.15427, val_acc: 0.96667
    Epoch [9920/10000], loss: 0.07993 acc: 1.00000 val_loss: 0.15423, val_acc: 0.96667
    Epoch [9930/10000], loss: 0.07988 acc: 1.00000 val_loss: 0.15419, val_acc: 0.96667
    Epoch [9940/10000], loss: 0.07982 acc: 1.00000 val_loss: 0.15415, val_acc: 0.96667
    Epoch [9950/10000], loss: 0.07977 acc: 1.00000 val_loss: 0.15411, val_acc: 0.96667
    Epoch [9960/10000], loss: 0.07972 acc: 1.00000 val_loss: 0.15407, val_acc: 0.96667
    Epoch [9970/10000], loss: 0.07966 acc: 1.00000 val_loss: 0.15403, val_acc: 0.96667
    Epoch [9980/10000], loss: 0.07961 acc: 1.00000 val_loss: 0.15399, val_acc: 0.96667
    Epoch [9990/10000], loss: 0.07955 acc: 1.00000 val_loss: 0.15395, val_acc: 0.96667


### 결과 확인


```python
# 손실과 정확도 확인

print(f'초기 상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종 상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기 상태 : 손실 : 4.49384  정확도 : 0.50000
    최종 상태 : 손실 : 0.15395  정확도 : 0.96667



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b', label='훈련')
plt.plot(history[:,0], history[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_8%EC%B0%A8%EC%8B%9C__Binary__35_0.webp)
    



```python
# 학습 곡선 출력(정확도)

plt.plot(history[:,0], history[:,2], 'b', label='훈련')
plt.plot(history[:,0], history[:,4], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```

### 결정  경계 그래프 출력



```python
# 검증 데이터 준비

x_t0 = x_test[y_test==0]
x_t1 = x_test[y_test==1]
```


```python
# 파라미터 취득
bias = net.l1.bias.data.numpy()
weight = net.l1.weight.data.numpy()
print(f'BIAS = {bias}, WEIGHT = {weight}')

# 결정 경계를 그리기 위해 x1로부터 x2를 계산
def decision(x):
    return(-(bias + weight[0,0] * x)/ weight[0,1])

# 산포도의 x1의 최솟값과 최댓값
xl = np.array([x_test[:,0].min(), x_test[:,0].max()])
yl = decision(xl)

# 결과 확인
print(f'xl = {xl}  yl = {yl}')
```


```python
# 산포도 출력
plt.scatter(x_t0[:,0], x_t0[:,1], marker='x',
        c='b', s=50, label='class 0')
plt.scatter(x_t1[:,0], x_t1[:,1], marker='o',
        c='k', s=50, label='class 1')

# 결정 경계 직선
plt.plot(xl, yl, c='r')
plt.xlabel('sepal_length')
plt.ylabel('sepal_width')
plt.legend()
plt.show()
```

## 칼럼 BCELoss 함수와 BCEWithLogitsLoss 함수의 차이


```python
# 모델 정의
# 2입력 1출력 로지스틱 회귀 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        super().__init__()
        self.l1 = nn.Linear(n_input, n_output)

        # 초깃값을 모두 1로 함
        # "딥러닝을 위한 수학"과 조건을 맞추기 위한 목적
        self.l1.weight.data.fill_(1.0)
        self.l1.bias.data.fill_(1.0)

    # 예측 함수 정의
    def forward(self, x):
        # 입력 값과 행렬 곱을 계산
        x1 = self.l1(x)
        return x1
```


```python
# 기록용 리스트 초기화
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수 ： logits가 붙은 교차 엔트로피 함수
criterion = nn.BCEWithLogitsLoss()

# 최적화 함수 : 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 기록용 리스트 초기화
history = np.zeros((0,5))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):
    # 훈련 페이즈


    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels1)

       # 경삿값 초기화
    optimizer.zero_grad()

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 손실값 스칼라화
    train_loss = loss.item()

    # 예측 라벨(1 또는 0) 계산
    predicted = torch.where(outputs < 0.0, 0, 1)

    # 정확도 계산
    train_acc = (predicted == labels1).sum() / len(y_train)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 손실 계산
    loss_test = criterion(outputs_test, labels1_test)

    # 손실값 스칼라화
    val_loss =  loss_test.item()

    # 예측 라벨(1 또는 0) 계산
    predicted_test = torch.where(outputs_test < 0.0, 0, 1)

    # 정확도 계산
    val_acc = (predicted_test == labels1_test).sum() / len(y_test)

    if ( epoch % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch, train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```


```python
# 손실과 정확도 확인

print(f'초기 상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종 상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```


```python
# 학습 곡선 표시(손실)

plt.plot(history[:,0], history[:,1], 'b', label='훈련')
plt.plot(history[:,0], history[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


```python
# 학습 곡선 출력(정확도)

plt.plot(history[:,0], history[:,2], 'b', label='훈련')
plt.plot(history[:,0], history[:,4], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```


```python
# 파라미터 취득

bias = net.l1.bias.data.numpy()
weight = net.l1.weight.data.numpy()
print(f'BIAS = {bias}, WEIGHT = {weight}')

# 결정 경계를 그리기 위해 x1로부터 x2를 계산
def decision(x):
    return(-(bias + weight[0,0] * x)/ weight[0,1])

# 산포도의 x1의 최솟값과 최댓값
xl = np.array([x_test[:,0].min(), x_test[:,0].max()])
yl = decision(xl)

# 결과 확인
print(f'xl = {xl}  yl = {yl}')
```


```python
# 산포도 출력
plt.scatter(x_t0[:,0], x_t0[:,1], marker='x',
        c='b', s=50, label='class 0')
plt.scatter(x_t1[:,0], x_t1[:,1], marker='o',
        c='k', s=50, label='class 1')

# 결정 경계 직선
plt.plot(xl, yl, c='r')
plt.xlabel('sepal_length')
plt.ylabel('sepal_width')
plt.legend()
plt.show()
```


## 강의_3기_AI개론_9차시__Multinomial_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_9차시__Multinomial_.ipynb)

# 9장 다중 분류 (Mulitnomial classification)

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
# 한글 폰트 설치

!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    0 upgraded, 0 newly installed, 0 to remove and 19 not upgraded.
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 39 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /usr/share/fonts/truetype: skipping, looped directory detected
    /usr/share/fonts/truetype/humor-sans: skipping, looped directory detected
    /usr/share/fonts/truetype/liberation: skipping, looped directory detected
    /usr/share/fonts/truetype/nanum: skipping, looped directory detected
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
```

    Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->torchviz) (3.0.2)
    Requirement already satisfied: torchinfo in /usr/local/lib/python3.11/dist-packages (1.8.0)


* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 폰트 관련 용도
import matplotlib.font_manager as fm

# Colab, Linux
# 나눔 고딕 폰트의 경로 명시
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```


```python
# 파이토치 관련 라이브러리
import torch
from torch import nn, optim
import torch.nn.functional as F
from torchviz import make_dot
from torchinfo import summary

# Iris dataset
import pandas  as pd
# from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
```


```python
# 기본 폰트 설정
plt.rcParams['font.family'] = font_name

# 기본 폰트 사이즈 변경
plt.rcParams['font.size'] = 14

# 기본 그래프 사이즈 변경
plt.rcParams['figure.figsize'] = (6,6)

# 기본 그리드 표시
# 필요에 따라 설정할 때는, plt.grid()
plt.rcParams['axes.grid'] = True
plt.rcParams["grid.linestyle"] = ":"

# 마이너스 기호 정상 출력
plt.rcParams['axes.unicode_minus'] = False

# 넘파이 부동소수점 자릿수 표시
np.set_printoptions(suppress=True, precision=4)
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')
```

## Iris data

### 데이터 불러오기


```python
# 학습용 데이터 준비

# 라이브러리 임포트
# from sklearn.datasets import load_iris

# 데이터 불러오기
iris = load_iris()
print("iris = \n", iris)
print('iris keys = \n', iris.keys())
print("target_names = \n", iris["target_names"])
```

    iris = 
     {'data': array([[5.1, 3.5, 1.4, 0.2],
           [4.9, 3. , 1.4, 0.2],
           [4.7, 3.2, 1.3, 0.2],
           [4.6, 3.1, 1.5, 0.2],
           [5. , 3.6, 1.4, 0.2],
           [5.4, 3.9, 1.7, 0.4],
           [4.6, 3.4, 1.4, 0.3],
           [5. , 3.4, 1.5, 0.2],
           [4.4, 2.9, 1.4, 0.2],
           [4.9, 3.1, 1.5, 0.1],
           [5.4, 3.7, 1.5, 0.2],
           [4.8, 3.4, 1.6, 0.2],
           [4.8, 3. , 1.4, 0.1],
           [4.3, 3. , 1.1, 0.1],
           [5.8, 4. , 1.2, 0.2],
           [5.7, 4.4, 1.5, 0.4],
           [5.4, 3.9, 1.3, 0.4],
           [5.1, 3.5, 1.4, 0.3],
           [5.7, 3.8, 1.7, 0.3],
           [5.1, 3.8, 1.5, 0.3],
           [5.4, 3.4, 1.7, 0.2],
           [5.1, 3.7, 1.5, 0.4],
           [4.6, 3.6, 1. , 0.2],
           [5.1, 3.3, 1.7, 0.5],
           [4.8, 3.4, 1.9, 0.2],
           [5. , 3. , 1.6, 0.2],
           [5. , 3.4, 1.6, 0.4],
           [5.2, 3.5, 1.5, 0.2],
           [5.2, 3.4, 1.4, 0.2],
           [4.7, 3.2, 1.6, 0.2],
           [4.8, 3.1, 1.6, 0.2],
           [5.4, 3.4, 1.5, 0.4],
           [5.2, 4.1, 1.5, 0.1],
           [5.5, 4.2, 1.4, 0.2],
           [4.9, 3.1, 1.5, 0.2],
           [5. , 3.2, 1.2, 0.2],
           [5.5, 3.5, 1.3, 0.2],
           [4.9, 3.6, 1.4, 0.1],
           [4.4, 3. , 1.3, 0.2],
           [5.1, 3.4, 1.5, 0.2],
           [5. , 3.5, 1.3, 0.3],
           [4.5, 2.3, 1.3, 0.3],
           [4.4, 3.2, 1.3, 0.2],
           [5. , 3.5, 1.6, 0.6],
           [5.1, 3.8, 1.9, 0.4],
           [4.8, 3. , 1.4, 0.3],
           [5.1, 3.8, 1.6, 0.2],
           [4.6, 3.2, 1.4, 0.2],
           [5.3, 3.7, 1.5, 0.2],
           [5. , 3.3, 1.4, 0.2],
           [7. , 3.2, 4.7, 1.4],
           [6.4, 3.2, 4.5, 1.5],
           [6.9, 3.1, 4.9, 1.5],
           [5.5, 2.3, 4. , 1.3],
           [6.5, 2.8, 4.6, 1.5],
           [5.7, 2.8, 4.5, 1.3],
           [6.3, 3.3, 4.7, 1.6],
           [4.9, 2.4, 3.3, 1. ],
           [6.6, 2.9, 4.6, 1.3],
           [5.2, 2.7, 3.9, 1.4],
           [5. , 2. , 3.5, 1. ],
           [5.9, 3. , 4.2, 1.5],
           [6. , 2.2, 4. , 1. ],
           [6.1, 2.9, 4.7, 1.4],
           [5.6, 2.9, 3.6, 1.3],
           [6.7, 3.1, 4.4, 1.4],
           [5.6, 3. , 4.5, 1.5],
           [5.8, 2.7, 4.1, 1. ],
           [6.2, 2.2, 4.5, 1.5],
           [5.6, 2.5, 3.9, 1.1],
           [5.9, 3.2, 4.8, 1.8],
           [6.1, 2.8, 4. , 1.3],
           [6.3, 2.5, 4.9, 1.5],
           [6.1, 2.8, 4.7, 1.2],
           [6.4, 2.9, 4.3, 1.3],
           [6.6, 3. , 4.4, 1.4],
           [6.8, 2.8, 4.8, 1.4],
           [6.7, 3. , 5. , 1.7],
           [6. , 2.9, 4.5, 1.5],
           [5.7, 2.6, 3.5, 1. ],
           [5.5, 2.4, 3.8, 1.1],
           [5.5, 2.4, 3.7, 1. ],
           [5.8, 2.7, 3.9, 1.2],
           [6. , 2.7, 5.1, 1.6],
           [5.4, 3. , 4.5, 1.5],
           [6. , 3.4, 4.5, 1.6],
           [6.7, 3.1, 4.7, 1.5],
           [6.3, 2.3, 4.4, 1.3],
           [5.6, 3. , 4.1, 1.3],
           [5.5, 2.5, 4. , 1.3],
           [5.5, 2.6, 4.4, 1.2],
           [6.1, 3. , 4.6, 1.4],
           [5.8, 2.6, 4. , 1.2],
           [5. , 2.3, 3.3, 1. ],
           [5.6, 2.7, 4.2, 1.3],
           [5.7, 3. , 4.2, 1.2],
           [5.7, 2.9, 4.2, 1.3],
           [6.2, 2.9, 4.3, 1.3],
           [5.1, 2.5, 3. , 1.1],
           [5.7, 2.8, 4.1, 1.3],
           [6.3, 3.3, 6. , 2.5],
           [5.8, 2.7, 5.1, 1.9],
           [7.1, 3. , 5.9, 2.1],
           [6.3, 2.9, 5.6, 1.8],
           [6.5, 3. , 5.8, 2.2],
           [7.6, 3. , 6.6, 2.1],
           [4.9, 2.5, 4.5, 1.7],
           [7.3, 2.9, 6.3, 1.8],
           [6.7, 2.5, 5.8, 1.8],
           [7.2, 3.6, 6.1, 2.5],
           [6.5, 3.2, 5.1, 2. ],
           [6.4, 2.7, 5.3, 1.9],
           [6.8, 3. , 5.5, 2.1],
           [5.7, 2.5, 5. , 2. ],
           [5.8, 2.8, 5.1, 2.4],
           [6.4, 3.2, 5.3, 2.3],
           [6.5, 3. , 5.5, 1.8],
           [7.7, 3.8, 6.7, 2.2],
           [7.7, 2.6, 6.9, 2.3],
           [6. , 2.2, 5. , 1.5],
           [6.9, 3.2, 5.7, 2.3],
           [5.6, 2.8, 4.9, 2. ],
           [7.7, 2.8, 6.7, 2. ],
           [6.3, 2.7, 4.9, 1.8],
           [6.7, 3.3, 5.7, 2.1],
           [7.2, 3.2, 6. , 1.8],
           [6.2, 2.8, 4.8, 1.8],
           [6.1, 3. , 4.9, 1.8],
           [6.4, 2.8, 5.6, 2.1],
           [7.2, 3. , 5.8, 1.6],
           [7.4, 2.8, 6.1, 1.9],
           [7.9, 3.8, 6.4, 2. ],
           [6.4, 2.8, 5.6, 2.2],
           [6.3, 2.8, 5.1, 1.5],
           [6.1, 2.6, 5.6, 1.4],
           [7.7, 3. , 6.1, 2.3],
           [6.3, 3.4, 5.6, 2.4],
           [6.4, 3.1, 5.5, 1.8],
           [6. , 3. , 4.8, 1.8],
           [6.9, 3.1, 5.4, 2.1],
           [6.7, 3.1, 5.6, 2.4],
           [6.9, 3.1, 5.1, 2.3],
           [5.8, 2.7, 5.1, 1.9],
           [6.8, 3.2, 5.9, 2.3],
           [6.7, 3.3, 5.7, 2.5],
           [6.7, 3. , 5.2, 2.3],
           [6.3, 2.5, 5. , 1.9],
           [6.5, 3. , 5.2, 2. ],
           [6.2, 3.4, 5.4, 2.3],
           [5.9, 3. , 5.1, 1.8]]), 'target': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]), 'frame': None, 'target_names': array(['setosa', 'versicolor', 'virginica'], dtype='<U10'), 'DESCR': '.. _iris_dataset:\n\nIris plants dataset\n--------------------\n\n**Data Set Characteristics:**\n\n:Number of Instances: 150 (50 in each of three classes)\n:Number of Attributes: 4 numeric, predictive attributes and the class\n:Attribute Information:\n    - sepal length in cm\n    - sepal width in cm\n    - petal length in cm\n    - petal width in cm\n    - class:\n            - Iris-Setosa\n            - Iris-Versicolour\n            - Iris-Virginica\n\n:Summary Statistics:\n\n============== ==== ==== ======= ===== ====================\n                Min  Max   Mean    SD   Class Correlation\n============== ==== ==== ======= ===== ====================\nsepal length:   4.3  7.9   5.84   0.83    0.7826\nsepal width:    2.0  4.4   3.05   0.43   -0.4194\npetal length:   1.0  6.9   3.76   1.76    0.9490  (high!)\npetal width:    0.1  2.5   1.20   0.76    0.9565  (high!)\n============== ==== ==== ======= ===== ====================\n\n:Missing Attribute Values: None\n:Class Distribution: 33.3% for each of 3 classes.\n:Creator: R.A. Fisher\n:Donor: Michael Marshall (MARSHALL%PLU@io.arc.nasa.gov)\n:Date: July, 1988\n\nThe famous Iris database, first used by Sir R.A. Fisher. The dataset is taken\nfrom Fisher\'s paper. Note that it\'s the same as in R, but not as in the UCI\nMachine Learning Repository, which has two wrong data points.\n\nThis is perhaps the best known database to be found in the\npattern recognition literature.  Fisher\'s paper is a classic in the field and\nis referenced frequently to this day.  (See Duda & Hart, for example.)  The\ndata set contains 3 classes of 50 instances each, where each class refers to a\ntype of iris plant.  One class is linearly separable from the other 2; the\nlatter are NOT linearly separable from each other.\n\n.. dropdown:: References\n\n  - Fisher, R.A. "The use of multiple measurements in taxonomic problems"\n    Annual Eugenics, 7, Part II, 179-188 (1936); also in "Contributions to\n    Mathematical Statistics" (John Wiley, NY, 1950).\n  - Duda, R.O., & Hart, P.E. (1973) Pattern Classification and Scene Analysis.\n    (Q327.D83) John Wiley & Sons.  ISBN 0-471-22361-1.  See page 218.\n  - Dasarathy, B.V. (1980) "Nosing Around the Neighborhood: A New System\n    Structure and Classification Rule for Recognition in Partially Exposed\n    Environments".  IEEE Transactions on Pattern Analysis and Machine\n    Intelligence, Vol. PAMI-2, No. 1, 67-71.\n  - Gates, G.W. (1972) "The Reduced Nearest Neighbor Rule".  IEEE Transactions\n    on Information Theory, May 1972, 431-433.\n  - See also: 1988 MLC Proceedings, 54-64.  Cheeseman et al"s AUTOCLASS II\n    conceptual clustering system finds 3 classes in the data.\n  - Many, many more ...\n', 'feature_names': ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'], 'filename': 'iris.csv', 'data_module': 'sklearn.datasets.data'}
    iris keys = 
     dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
    target_names = 
     ['setosa' 'versicolor' 'virginica']



```python
# 입력 데이터와 정답 데이터
x_org, y_org = iris.data, iris.target

# 결과 확인
print('원본 데이터 타입 :', type(x_org), type(y_org))
print('원본 데이터 크기 :', x_org.shape, y_org.shape)
```

    원본 데이터 타입 : <class 'numpy.ndarray'> <class 'numpy.ndarray'>
    원본 데이터 크기 : (150, 4) (150,)


### 데이터 추출


```python
# 입력 데이터로 sepal(꽃받침) length(0)와 petal(꽃잎) length(2)를 추출
x_select = x_org[:,[0,2]]

# 결과 확인
print('원본 데이터', x_select.shape, y_org.shape)
```

    원본 데이터 (150, 2) (150,)


### 훈련 데이터와 검증 데이터 분할


```python
# 훈련 데이터와 검증 데이터로 분할(셔플도 동시에 실시함)
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    x_select, y_org, train_size=75, test_size=75,
    random_state=123)

print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
```

    (75, 2) (75, 2) (75,) (75,)


### 훈련 데이터의 산포도 출력


```python
# 데이터를 정답별로 분할

x_t0 = x_train[y_train == 0]
x_t1 = x_train[y_train == 1]
x_t2 = x_train[y_train == 2]
```


```python
# 산포도 출력

plt.scatter(x_t0[:,0], x_t0[:,1], marker='x', c='k', s=50, label='0 (setosa)')
plt.scatter(x_t1[:,0], x_t1[:,1], marker='o', c='b', s=50, label='1 (versicolor)')
plt.scatter(x_t2[:,0], x_t2[:,1], marker='^', c='r', s=50, label='2 (virginica)')
plt.xlabel('sepal_length')
plt.ylabel('petal_length')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__19_0.webp)
    


### 모델 정의


```python
# 학습용 파라미터 설정

# 입력 차원수
n_input = x_train.shape[1]

# 출력 차원수
# 분류 클래스 수, 여기서는 3
n_output = len(list(set(y_train)))

# 결과 확인
print(f'n_input: {n_input}  n_output: {n_output}')
```

    n_input: 2  n_output: 3



```python
# 모델 정의
# 2입력 3출력 로지스틱 회귀 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        super().__init__()
        self.l1 = nn.Linear(n_input, n_output)

        # 초깃값을 모두 1로 함
        # "딥러닝을 위한 수학"과 조건을 맞추기 위한 목적
        self.l1.weight.data.fill_(1.0)
        self.l1.bias.data.fill_(1.0)

    def forward(self, x):
        x1 = self.l1(x)
        return x1

# 인스턴스 생성
net = Net(n_input, n_output)
# list(net.parameters())
```

### 모델 확인


```python
# 모델 내부 파라미터 확인
# l1.weight는 행렬, l1.bias는 벡터

for parameter in net.named_parameters():
    print(parameter)

```

    ('l1.weight', Parameter containing:
    tensor([[1., 1.],
            [1., 1.],
            [1., 1.]], requires_grad=True))
    ('l1.bias', Parameter containing:
    tensor([1., 1., 1.], requires_grad=True))



```python
# 모델 개요 표시 1

print(net)
```

    Net(
      (l1): Linear(in_features=2, out_features=3, bias=True)
    )



```python
# 모델 개요 표시 2

summary(net, (2,), device = 'cpu')
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [3]                       --
    ├─Linear: 1-1                            [3]                       9
    ==========================================================================================
    Total params: 9
    Trainable params: 9
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 0.00
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.00
    Estimated Total Size (MB): 0.00
    ==========================================================================================



### 최적화 알고리즘과 손실 함수의 정의


```python
# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)
```

### 경사 하강법


```python
# 입력 데이터 x_train과 정답 데이터 y_train의 텐서 변수화

inputs = torch.tensor(x_train).float()
labels = torch.tensor(y_train).long()

# 검증 데이터의 텐서 변수화

inputs_test = torch.tensor(x_test).float()
labels_test = torch.tensor(y_test).long()
```

### 손실의 계산 그래프 시각화


```python
# 예측 계산
outputs = net(inputs)

# 손실 계산
loss = criterion(outputs, labels)

# 손실의 계산 그래프 시각화
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__32_0.svg)
    


### 예측 라벨을 얻는 방법


```python
# torch.max 함수 호출
# 2번째 인수는 축을 의미함. 1이면 행별로 집계
print(torch.max(outputs, 1))
# print(torch.argmax(outputs, 1))

# 예측 라벨 리스트를 취득
torch.max(outputs, 1)[1]
```

    torch.return_types.max(
    values=tensor([12.0000, 12.7000,  7.6000, 13.0000, 12.3000,  7.6000,  7.3000, 11.1000,
            12.1000, 13.3000,  8.0000,  7.0000, 10.3000,  7.6000, 11.7000, 13.3000,
             7.4000, 13.5000,  8.2000,  8.4000, 12.7000,  6.6000,  7.9000, 12.2000,
            14.6000, 12.0000, 10.2000, 10.5000,  7.1000,  7.3000, 12.6000, 12.7000,
             7.4000,  7.7000, 10.8000, 11.5000, 11.5000, 14.0000, 12.8000, 10.8000,
            10.8000, 15.2000,  7.5000,  7.8000, 11.1000, 13.6000, 12.9000, 14.2000,
            12.7000,  7.6000, 10.9000,  7.0000, 10.9000, 11.2000,  7.4000, 11.7000,
            13.3000, 11.5000, 13.4000, 12.7000,  7.7000, 11.8000,  7.0000, 12.6000,
            11.7000, 10.9000,  9.2000, 12.2000, 10.4000, 12.1000,  7.5000,  9.1000,
            11.1000, 12.0000, 14.3000], grad_fn=<MaxBackward0>),
    indices=tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0]))





    tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0])



### 반복 계산


```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 평가 결과 기록
history = np.zeros((0,5))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 훈련 페이즈

    # 경사 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 예측 라벨 산출
    predicted = torch.max(outputs, 1)[1]

    # 손실과 정확도 계산
    train_loss = loss.item()
    train_acc = (predicted == labels).sum()  / len(labels)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 손실 계산
    loss_test = criterion(outputs_test, labels_test)

    # 예측 라벨 산출
    predicted_test = torch.max(outputs_test, 1)[1]

    # 손실과 정확도 계산
    val_loss =  loss_test.item()
    val_acc =  (predicted_test == labels_test).sum() / len(labels_test)

    if ((epoch) % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch, train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```

    Epoch [0/10000], loss: 1.09861 acc: 0.30667 val_loss: 1.09263, val_acc: 0.26667
    Epoch [10/10000], loss: 1.03580 acc: 0.40000 val_loss: 1.06403, val_acc: 0.26667
    Epoch [20/10000], loss: 1.00477 acc: 0.40000 val_loss: 1.03347, val_acc: 0.26667
    Epoch [30/10000], loss: 0.97672 acc: 0.40000 val_loss: 1.00264, val_acc: 0.26667
    Epoch [40/10000], loss: 0.95057 acc: 0.41333 val_loss: 0.97351, val_acc: 0.26667
    Epoch [50/10000], loss: 0.92616 acc: 0.48000 val_loss: 0.94631, val_acc: 0.38667
    Epoch [60/10000], loss: 0.90338 acc: 0.69333 val_loss: 0.92098, val_acc: 0.56000
    Epoch [70/10000], loss: 0.88212 acc: 0.70667 val_loss: 0.89740, val_acc: 0.60000
    Epoch [80/10000], loss: 0.86227 acc: 0.70667 val_loss: 0.87545, val_acc: 0.61333
    Epoch [90/10000], loss: 0.84373 acc: 0.70667 val_loss: 0.85500, val_acc: 0.62667
    Epoch [100/10000], loss: 0.82640 acc: 0.70667 val_loss: 0.83594, val_acc: 0.62667
    Epoch [110/10000], loss: 0.81019 acc: 0.72000 val_loss: 0.81815, val_acc: 0.62667
    Epoch [120/10000], loss: 0.79500 acc: 0.72000 val_loss: 0.80153, val_acc: 0.62667
    Epoch [130/10000], loss: 0.78077 acc: 0.73333 val_loss: 0.78599, val_acc: 0.62667
    Epoch [140/10000], loss: 0.76741 acc: 0.74667 val_loss: 0.77142, val_acc: 0.64000
    Epoch [150/10000], loss: 0.75485 acc: 0.74667 val_loss: 0.75777, val_acc: 0.65333
    Epoch [160/10000], loss: 0.74303 acc: 0.74667 val_loss: 0.74494, val_acc: 0.68000
    Epoch [170/10000], loss: 0.73189 acc: 0.76000 val_loss: 0.73288, val_acc: 0.70667
    Epoch [180/10000], loss: 0.72138 acc: 0.77333 val_loss: 0.72151, val_acc: 0.76000
    Epoch [190/10000], loss: 0.71145 acc: 0.82667 val_loss: 0.71079, val_acc: 0.78667
    Epoch [200/10000], loss: 0.70205 acc: 0.82667 val_loss: 0.70067, val_acc: 0.78667
    Epoch [210/10000], loss: 0.69315 acc: 0.84000 val_loss: 0.69109, val_acc: 0.80000
    Epoch [220/10000], loss: 0.68470 acc: 0.84000 val_loss: 0.68202, val_acc: 0.80000
    Epoch [230/10000], loss: 0.67667 acc: 0.86667 val_loss: 0.67341, val_acc: 0.81333
    Epoch [240/10000], loss: 0.66904 acc: 0.86667 val_loss: 0.66524, val_acc: 0.81333
    Epoch [250/10000], loss: 0.66176 acc: 0.86667 val_loss: 0.65746, val_acc: 0.82667
    Epoch [260/10000], loss: 0.65483 acc: 0.85333 val_loss: 0.65005, val_acc: 0.82667
    Epoch [270/10000], loss: 0.64820 acc: 0.85333 val_loss: 0.64299, val_acc: 0.82667
    Epoch [280/10000], loss: 0.64187 acc: 0.85333 val_loss: 0.63625, val_acc: 0.82667
    Epoch [290/10000], loss: 0.63581 acc: 0.86667 val_loss: 0.62980, val_acc: 0.82667
    Epoch [300/10000], loss: 0.63000 acc: 0.88000 val_loss: 0.62363, val_acc: 0.82667
    Epoch [310/10000], loss: 0.62443 acc: 0.89333 val_loss: 0.61772, val_acc: 0.82667
    Epoch [320/10000], loss: 0.61909 acc: 0.89333 val_loss: 0.61205, val_acc: 0.82667
    Epoch [330/10000], loss: 0.61394 acc: 0.89333 val_loss: 0.60661, val_acc: 0.82667
    Epoch [340/10000], loss: 0.60900 acc: 0.89333 val_loss: 0.60138, val_acc: 0.84000
    Epoch [350/10000], loss: 0.60423 acc: 0.89333 val_loss: 0.59635, val_acc: 0.84000
    Epoch [360/10000], loss: 0.59964 acc: 0.90667 val_loss: 0.59150, val_acc: 0.85333
    Epoch [370/10000], loss: 0.59521 acc: 0.92000 val_loss: 0.58683, val_acc: 0.86667
    Epoch [380/10000], loss: 0.59093 acc: 0.92000 val_loss: 0.58232, val_acc: 0.86667
    Epoch [390/10000], loss: 0.58679 acc: 0.92000 val_loss: 0.57797, val_acc: 0.86667
    Epoch [400/10000], loss: 0.58279 acc: 0.92000 val_loss: 0.57377, val_acc: 0.86667
    Epoch [410/10000], loss: 0.57891 acc: 0.92000 val_loss: 0.56970, val_acc: 0.86667
    Epoch [420/10000], loss: 0.57516 acc: 0.92000 val_loss: 0.56576, val_acc: 0.86667
    Epoch [430/10000], loss: 0.57152 acc: 0.90667 val_loss: 0.56195, val_acc: 0.86667
    Epoch [440/10000], loss: 0.56799 acc: 0.90667 val_loss: 0.55825, val_acc: 0.86667
    Epoch [450/10000], loss: 0.56456 acc: 0.90667 val_loss: 0.55466, val_acc: 0.86667
    Epoch [460/10000], loss: 0.56123 acc: 0.90667 val_loss: 0.55118, val_acc: 0.86667
    Epoch [470/10000], loss: 0.55799 acc: 0.90667 val_loss: 0.54779, val_acc: 0.88000
    Epoch [480/10000], loss: 0.55484 acc: 0.90667 val_loss: 0.54451, val_acc: 0.88000
    Epoch [490/10000], loss: 0.55177 acc: 0.90667 val_loss: 0.54131, val_acc: 0.88000
    Epoch [500/10000], loss: 0.54878 acc: 0.90667 val_loss: 0.53819, val_acc: 0.88000
    Epoch [510/10000], loss: 0.54587 acc: 0.90667 val_loss: 0.53516, val_acc: 0.88000
    Epoch [520/10000], loss: 0.54303 acc: 0.90667 val_loss: 0.53221, val_acc: 0.88000
    Epoch [530/10000], loss: 0.54026 acc: 0.90667 val_loss: 0.52933, val_acc: 0.88000
    Epoch [540/10000], loss: 0.53755 acc: 0.90667 val_loss: 0.52652, val_acc: 0.88000
    Epoch [550/10000], loss: 0.53491 acc: 0.90667 val_loss: 0.52377, val_acc: 0.88000
    Epoch [560/10000], loss: 0.53233 acc: 0.90667 val_loss: 0.52110, val_acc: 0.88000
    Epoch [570/10000], loss: 0.52981 acc: 0.90667 val_loss: 0.51848, val_acc: 0.88000
    Epoch [580/10000], loss: 0.52734 acc: 0.90667 val_loss: 0.51592, val_acc: 0.88000
    Epoch [590/10000], loss: 0.52493 acc: 0.90667 val_loss: 0.51342, val_acc: 0.88000
    Epoch [600/10000], loss: 0.52256 acc: 0.90667 val_loss: 0.51098, val_acc: 0.88000
    Epoch [610/10000], loss: 0.52025 acc: 0.90667 val_loss: 0.50859, val_acc: 0.88000
    Epoch [620/10000], loss: 0.51798 acc: 0.90667 val_loss: 0.50624, val_acc: 0.88000
    Epoch [630/10000], loss: 0.51576 acc: 0.90667 val_loss: 0.50395, val_acc: 0.88000
    Epoch [640/10000], loss: 0.51358 acc: 0.90667 val_loss: 0.50170, val_acc: 0.88000
    Epoch [650/10000], loss: 0.51144 acc: 0.90667 val_loss: 0.49949, val_acc: 0.88000
    Epoch [660/10000], loss: 0.50934 acc: 0.90667 val_loss: 0.49733, val_acc: 0.89333
    Epoch [670/10000], loss: 0.50728 acc: 0.90667 val_loss: 0.49521, val_acc: 0.90667
    Epoch [680/10000], loss: 0.50526 acc: 0.90667 val_loss: 0.49313, val_acc: 0.90667
    Epoch [690/10000], loss: 0.50328 acc: 0.90667 val_loss: 0.49109, val_acc: 0.90667
    Epoch [700/10000], loss: 0.50133 acc: 0.90667 val_loss: 0.48908, val_acc: 0.90667
    Epoch [710/10000], loss: 0.49941 acc: 0.90667 val_loss: 0.48711, val_acc: 0.90667
    Epoch [720/10000], loss: 0.49752 acc: 0.90667 val_loss: 0.48517, val_acc: 0.90667
    Epoch [730/10000], loss: 0.49567 acc: 0.90667 val_loss: 0.48327, val_acc: 0.90667
    Epoch [740/10000], loss: 0.49385 acc: 0.90667 val_loss: 0.48140, val_acc: 0.90667
    Epoch [750/10000], loss: 0.49205 acc: 0.90667 val_loss: 0.47956, val_acc: 0.90667
    Epoch [760/10000], loss: 0.49029 acc: 0.90667 val_loss: 0.47775, val_acc: 0.90667
    Epoch [770/10000], loss: 0.48855 acc: 0.90667 val_loss: 0.47597, val_acc: 0.90667
    Epoch [780/10000], loss: 0.48684 acc: 0.90667 val_loss: 0.47422, val_acc: 0.90667
    Epoch [790/10000], loss: 0.48515 acc: 0.89333 val_loss: 0.47249, val_acc: 0.92000
    Epoch [800/10000], loss: 0.48349 acc: 0.89333 val_loss: 0.47079, val_acc: 0.92000
    Epoch [810/10000], loss: 0.48186 acc: 0.89333 val_loss: 0.46912, val_acc: 0.92000
    Epoch [820/10000], loss: 0.48024 acc: 0.89333 val_loss: 0.46747, val_acc: 0.92000
    Epoch [830/10000], loss: 0.47865 acc: 0.89333 val_loss: 0.46585, val_acc: 0.92000
    Epoch [840/10000], loss: 0.47709 acc: 0.89333 val_loss: 0.46425, val_acc: 0.92000
    Epoch [850/10000], loss: 0.47554 acc: 0.89333 val_loss: 0.46267, val_acc: 0.92000
    Epoch [860/10000], loss: 0.47402 acc: 0.89333 val_loss: 0.46111, val_acc: 0.92000
    Epoch [870/10000], loss: 0.47251 acc: 0.89333 val_loss: 0.45958, val_acc: 0.92000
    Epoch [880/10000], loss: 0.47103 acc: 0.89333 val_loss: 0.45806, val_acc: 0.92000
    Epoch [890/10000], loss: 0.46956 acc: 0.89333 val_loss: 0.45657, val_acc: 0.92000
    Epoch [900/10000], loss: 0.46811 acc: 0.89333 val_loss: 0.45509, val_acc: 0.92000
    Epoch [910/10000], loss: 0.46668 acc: 0.89333 val_loss: 0.45364, val_acc: 0.92000
    Epoch [920/10000], loss: 0.46527 acc: 0.89333 val_loss: 0.45220, val_acc: 0.92000
    Epoch [930/10000], loss: 0.46388 acc: 0.89333 val_loss: 0.45078, val_acc: 0.92000
    Epoch [940/10000], loss: 0.46250 acc: 0.89333 val_loss: 0.44938, val_acc: 0.92000
    Epoch [950/10000], loss: 0.46114 acc: 0.89333 val_loss: 0.44800, val_acc: 0.92000
    Epoch [960/10000], loss: 0.45980 acc: 0.89333 val_loss: 0.44663, val_acc: 0.92000
    Epoch [970/10000], loss: 0.45847 acc: 0.89333 val_loss: 0.44528, val_acc: 0.92000
    Epoch [980/10000], loss: 0.45716 acc: 0.89333 val_loss: 0.44395, val_acc: 0.92000
    Epoch [990/10000], loss: 0.45586 acc: 0.89333 val_loss: 0.44263, val_acc: 0.92000
    Epoch [1000/10000], loss: 0.45458 acc: 0.89333 val_loss: 0.44133, val_acc: 0.92000
    Epoch [1010/10000], loss: 0.45331 acc: 0.89333 val_loss: 0.44004, val_acc: 0.92000
    Epoch [1020/10000], loss: 0.45205 acc: 0.89333 val_loss: 0.43877, val_acc: 0.92000
    Epoch [1030/10000], loss: 0.45081 acc: 0.89333 val_loss: 0.43751, val_acc: 0.92000
    Epoch [1040/10000], loss: 0.44958 acc: 0.89333 val_loss: 0.43626, val_acc: 0.92000
    Epoch [1050/10000], loss: 0.44836 acc: 0.89333 val_loss: 0.43503, val_acc: 0.92000
    Epoch [1060/10000], loss: 0.44716 acc: 0.89333 val_loss: 0.43381, val_acc: 0.92000
    Epoch [1070/10000], loss: 0.44597 acc: 0.89333 val_loss: 0.43260, val_acc: 0.92000
    Epoch [1080/10000], loss: 0.44479 acc: 0.89333 val_loss: 0.43141, val_acc: 0.92000
    Epoch [1090/10000], loss: 0.44363 acc: 0.89333 val_loss: 0.43023, val_acc: 0.92000
    Epoch [1100/10000], loss: 0.44247 acc: 0.89333 val_loss: 0.42906, val_acc: 0.92000
    Epoch [1110/10000], loss: 0.44133 acc: 0.89333 val_loss: 0.42790, val_acc: 0.92000
    Epoch [1120/10000], loss: 0.44020 acc: 0.89333 val_loss: 0.42676, val_acc: 0.92000
    Epoch [1130/10000], loss: 0.43908 acc: 0.89333 val_loss: 0.42562, val_acc: 0.92000
    Epoch [1140/10000], loss: 0.43797 acc: 0.89333 val_loss: 0.42450, val_acc: 0.92000
    Epoch [1150/10000], loss: 0.43687 acc: 0.89333 val_loss: 0.42339, val_acc: 0.92000
    Epoch [1160/10000], loss: 0.43578 acc: 0.89333 val_loss: 0.42229, val_acc: 0.92000
    Epoch [1170/10000], loss: 0.43470 acc: 0.89333 val_loss: 0.42120, val_acc: 0.92000
    Epoch [1180/10000], loss: 0.43363 acc: 0.89333 val_loss: 0.42012, val_acc: 0.92000
    Epoch [1190/10000], loss: 0.43257 acc: 0.89333 val_loss: 0.41905, val_acc: 0.92000
    Epoch [1200/10000], loss: 0.43152 acc: 0.89333 val_loss: 0.41799, val_acc: 0.92000
    Epoch [1210/10000], loss: 0.43048 acc: 0.89333 val_loss: 0.41694, val_acc: 0.92000
    Epoch [1220/10000], loss: 0.42945 acc: 0.89333 val_loss: 0.41590, val_acc: 0.92000
    Epoch [1230/10000], loss: 0.42843 acc: 0.89333 val_loss: 0.41487, val_acc: 0.92000
    Epoch [1240/10000], loss: 0.42742 acc: 0.89333 val_loss: 0.41384, val_acc: 0.92000
    Epoch [1250/10000], loss: 0.42641 acc: 0.89333 val_loss: 0.41283, val_acc: 0.92000
    Epoch [1260/10000], loss: 0.42542 acc: 0.89333 val_loss: 0.41182, val_acc: 0.92000
    Epoch [1270/10000], loss: 0.42443 acc: 0.89333 val_loss: 0.41083, val_acc: 0.92000
    Epoch [1280/10000], loss: 0.42345 acc: 0.89333 val_loss: 0.40984, val_acc: 0.92000
    Epoch [1290/10000], loss: 0.42248 acc: 0.89333 val_loss: 0.40886, val_acc: 0.92000
    Epoch [1300/10000], loss: 0.42152 acc: 0.89333 val_loss: 0.40789, val_acc: 0.92000
    Epoch [1310/10000], loss: 0.42056 acc: 0.89333 val_loss: 0.40693, val_acc: 0.92000
    Epoch [1320/10000], loss: 0.41962 acc: 0.89333 val_loss: 0.40598, val_acc: 0.92000
    Epoch [1330/10000], loss: 0.41868 acc: 0.89333 val_loss: 0.40503, val_acc: 0.93333
    Epoch [1340/10000], loss: 0.41775 acc: 0.89333 val_loss: 0.40409, val_acc: 0.93333
    Epoch [1350/10000], loss: 0.41682 acc: 0.89333 val_loss: 0.40316, val_acc: 0.93333
    Epoch [1360/10000], loss: 0.41590 acc: 0.89333 val_loss: 0.40224, val_acc: 0.93333
    Epoch [1370/10000], loss: 0.41499 acc: 0.89333 val_loss: 0.40132, val_acc: 0.93333
    Epoch [1380/10000], loss: 0.41409 acc: 0.89333 val_loss: 0.40041, val_acc: 0.93333
    Epoch [1390/10000], loss: 0.41320 acc: 0.89333 val_loss: 0.39951, val_acc: 0.93333
    Epoch [1400/10000], loss: 0.41231 acc: 0.89333 val_loss: 0.39861, val_acc: 0.93333
    Epoch [1410/10000], loss: 0.41143 acc: 0.89333 val_loss: 0.39773, val_acc: 0.93333
    Epoch [1420/10000], loss: 0.41055 acc: 0.89333 val_loss: 0.39685, val_acc: 0.93333
    Epoch [1430/10000], loss: 0.40968 acc: 0.89333 val_loss: 0.39597, val_acc: 0.93333
    Epoch [1440/10000], loss: 0.40882 acc: 0.89333 val_loss: 0.39510, val_acc: 0.93333
    Epoch [1450/10000], loss: 0.40796 acc: 0.89333 val_loss: 0.39424, val_acc: 0.93333
    Epoch [1460/10000], loss: 0.40711 acc: 0.89333 val_loss: 0.39339, val_acc: 0.93333
    Epoch [1470/10000], loss: 0.40627 acc: 0.89333 val_loss: 0.39254, val_acc: 0.93333
    Epoch [1480/10000], loss: 0.40543 acc: 0.90667 val_loss: 0.39170, val_acc: 0.93333
    Epoch [1490/10000], loss: 0.40460 acc: 0.90667 val_loss: 0.39086, val_acc: 0.93333
    Epoch [1500/10000], loss: 0.40378 acc: 0.90667 val_loss: 0.39003, val_acc: 0.93333
    Epoch [1510/10000], loss: 0.40296 acc: 0.90667 val_loss: 0.38921, val_acc: 0.93333
    Epoch [1520/10000], loss: 0.40214 acc: 0.90667 val_loss: 0.38839, val_acc: 0.93333
    Epoch [1530/10000], loss: 0.40134 acc: 0.90667 val_loss: 0.38758, val_acc: 0.93333
    Epoch [1540/10000], loss: 0.40053 acc: 0.90667 val_loss: 0.38677, val_acc: 0.93333
    Epoch [1550/10000], loss: 0.39974 acc: 0.90667 val_loss: 0.38597, val_acc: 0.93333
    Epoch [1560/10000], loss: 0.39894 acc: 0.90667 val_loss: 0.38517, val_acc: 0.94667
    Epoch [1570/10000], loss: 0.39816 acc: 0.90667 val_loss: 0.38438, val_acc: 0.94667
    Epoch [1580/10000], loss: 0.39738 acc: 0.90667 val_loss: 0.38360, val_acc: 0.94667
    Epoch [1590/10000], loss: 0.39660 acc: 0.90667 val_loss: 0.38282, val_acc: 0.94667
    Epoch [1600/10000], loss: 0.39583 acc: 0.90667 val_loss: 0.38204, val_acc: 0.94667
    Epoch [1610/10000], loss: 0.39507 acc: 0.90667 val_loss: 0.38128, val_acc: 0.94667
    Epoch [1620/10000], loss: 0.39431 acc: 0.90667 val_loss: 0.38051, val_acc: 0.94667
    Epoch [1630/10000], loss: 0.39355 acc: 0.90667 val_loss: 0.37975, val_acc: 0.94667
    Epoch [1640/10000], loss: 0.39280 acc: 0.90667 val_loss: 0.37900, val_acc: 0.94667
    Epoch [1650/10000], loss: 0.39206 acc: 0.90667 val_loss: 0.37825, val_acc: 0.94667
    Epoch [1660/10000], loss: 0.39132 acc: 0.90667 val_loss: 0.37751, val_acc: 0.94667
    Epoch [1670/10000], loss: 0.39058 acc: 0.90667 val_loss: 0.37677, val_acc: 0.94667
    Epoch [1680/10000], loss: 0.38985 acc: 0.90667 val_loss: 0.37604, val_acc: 0.94667
    Epoch [1690/10000], loss: 0.38913 acc: 0.90667 val_loss: 0.37531, val_acc: 0.94667
    Epoch [1700/10000], loss: 0.38841 acc: 0.90667 val_loss: 0.37458, val_acc: 0.94667
    Epoch [1710/10000], loss: 0.38769 acc: 0.90667 val_loss: 0.37386, val_acc: 0.94667
    Epoch [1720/10000], loss: 0.38698 acc: 0.90667 val_loss: 0.37315, val_acc: 0.94667
    Epoch [1730/10000], loss: 0.38627 acc: 0.90667 val_loss: 0.37244, val_acc: 0.94667
    Epoch [1740/10000], loss: 0.38557 acc: 0.90667 val_loss: 0.37173, val_acc: 0.94667
    Epoch [1750/10000], loss: 0.38487 acc: 0.90667 val_loss: 0.37103, val_acc: 0.94667
    Epoch [1760/10000], loss: 0.38417 acc: 0.90667 val_loss: 0.37033, val_acc: 0.94667
    Epoch [1770/10000], loss: 0.38348 acc: 0.90667 val_loss: 0.36964, val_acc: 0.94667
    Epoch [1780/10000], loss: 0.38280 acc: 0.90667 val_loss: 0.36895, val_acc: 0.94667
    Epoch [1790/10000], loss: 0.38212 acc: 0.90667 val_loss: 0.36826, val_acc: 0.94667
    Epoch [1800/10000], loss: 0.38144 acc: 0.90667 val_loss: 0.36758, val_acc: 0.94667
    Epoch [1810/10000], loss: 0.38076 acc: 0.90667 val_loss: 0.36690, val_acc: 0.94667
    Epoch [1820/10000], loss: 0.38009 acc: 0.90667 val_loss: 0.36623, val_acc: 0.94667
    Epoch [1830/10000], loss: 0.37943 acc: 0.90667 val_loss: 0.36556, val_acc: 0.94667
    Epoch [1840/10000], loss: 0.37877 acc: 0.90667 val_loss: 0.36490, val_acc: 0.94667
    Epoch [1850/10000], loss: 0.37811 acc: 0.90667 val_loss: 0.36424, val_acc: 0.94667
    Epoch [1860/10000], loss: 0.37746 acc: 0.90667 val_loss: 0.36358, val_acc: 0.94667
    Epoch [1870/10000], loss: 0.37681 acc: 0.90667 val_loss: 0.36293, val_acc: 0.94667
    Epoch [1880/10000], loss: 0.37616 acc: 0.90667 val_loss: 0.36228, val_acc: 0.94667
    Epoch [1890/10000], loss: 0.37552 acc: 0.90667 val_loss: 0.36163, val_acc: 0.94667
    Epoch [1900/10000], loss: 0.37488 acc: 0.90667 val_loss: 0.36099, val_acc: 0.94667
    Epoch [1910/10000], loss: 0.37424 acc: 0.90667 val_loss: 0.36035, val_acc: 0.94667
    Epoch [1920/10000], loss: 0.37361 acc: 0.90667 val_loss: 0.35972, val_acc: 0.94667
    Epoch [1930/10000], loss: 0.37298 acc: 0.90667 val_loss: 0.35909, val_acc: 0.94667
    Epoch [1940/10000], loss: 0.37236 acc: 0.90667 val_loss: 0.35846, val_acc: 0.94667
    Epoch [1950/10000], loss: 0.37174 acc: 0.90667 val_loss: 0.35784, val_acc: 0.94667
    Epoch [1960/10000], loss: 0.37112 acc: 0.90667 val_loss: 0.35722, val_acc: 0.94667
    Epoch [1970/10000], loss: 0.37051 acc: 0.90667 val_loss: 0.35660, val_acc: 0.94667
    Epoch [1980/10000], loss: 0.36990 acc: 0.90667 val_loss: 0.35599, val_acc: 0.94667
    Epoch [1990/10000], loss: 0.36929 acc: 0.90667 val_loss: 0.35538, val_acc: 0.94667
    Epoch [2000/10000], loss: 0.36869 acc: 0.90667 val_loss: 0.35477, val_acc: 0.94667
    Epoch [2010/10000], loss: 0.36809 acc: 0.90667 val_loss: 0.35417, val_acc: 0.94667
    Epoch [2020/10000], loss: 0.36749 acc: 0.90667 val_loss: 0.35357, val_acc: 0.94667
    Epoch [2030/10000], loss: 0.36690 acc: 0.90667 val_loss: 0.35298, val_acc: 0.94667
    Epoch [2040/10000], loss: 0.36631 acc: 0.90667 val_loss: 0.35238, val_acc: 0.94667
    Epoch [2050/10000], loss: 0.36572 acc: 0.90667 val_loss: 0.35179, val_acc: 0.94667
    Epoch [2060/10000], loss: 0.36514 acc: 0.90667 val_loss: 0.35121, val_acc: 0.94667
    Epoch [2070/10000], loss: 0.36455 acc: 0.90667 val_loss: 0.35062, val_acc: 0.94667
    Epoch [2080/10000], loss: 0.36398 acc: 0.90667 val_loss: 0.35004, val_acc: 0.94667
    Epoch [2090/10000], loss: 0.36340 acc: 0.90667 val_loss: 0.34947, val_acc: 0.94667
    Epoch [2100/10000], loss: 0.36283 acc: 0.90667 val_loss: 0.34889, val_acc: 0.94667
    Epoch [2110/10000], loss: 0.36226 acc: 0.90667 val_loss: 0.34832, val_acc: 0.94667
    Epoch [2120/10000], loss: 0.36170 acc: 0.90667 val_loss: 0.34775, val_acc: 0.94667
    Epoch [2130/10000], loss: 0.36114 acc: 0.90667 val_loss: 0.34719, val_acc: 0.94667
    Epoch [2140/10000], loss: 0.36058 acc: 0.90667 val_loss: 0.34663, val_acc: 0.94667
    Epoch [2150/10000], loss: 0.36002 acc: 0.90667 val_loss: 0.34607, val_acc: 0.94667
    Epoch [2160/10000], loss: 0.35947 acc: 0.90667 val_loss: 0.34551, val_acc: 0.94667
    Epoch [2170/10000], loss: 0.35892 acc: 0.90667 val_loss: 0.34496, val_acc: 0.94667
    Epoch [2180/10000], loss: 0.35837 acc: 0.90667 val_loss: 0.34441, val_acc: 0.94667
    Epoch [2190/10000], loss: 0.35782 acc: 0.90667 val_loss: 0.34386, val_acc: 0.94667
    Epoch [2200/10000], loss: 0.35728 acc: 0.90667 val_loss: 0.34331, val_acc: 0.94667
    Epoch [2210/10000], loss: 0.35674 acc: 0.90667 val_loss: 0.34277, val_acc: 0.94667
    Epoch [2220/10000], loss: 0.35621 acc: 0.90667 val_loss: 0.34223, val_acc: 0.94667
    Epoch [2230/10000], loss: 0.35567 acc: 0.90667 val_loss: 0.34170, val_acc: 0.94667
    Epoch [2240/10000], loss: 0.35514 acc: 0.90667 val_loss: 0.34116, val_acc: 0.94667
    Epoch [2250/10000], loss: 0.35461 acc: 0.90667 val_loss: 0.34063, val_acc: 0.94667
    Epoch [2260/10000], loss: 0.35409 acc: 0.90667 val_loss: 0.34010, val_acc: 0.94667
    Epoch [2270/10000], loss: 0.35356 acc: 0.90667 val_loss: 0.33958, val_acc: 0.94667
    Epoch [2280/10000], loss: 0.35304 acc: 0.90667 val_loss: 0.33905, val_acc: 0.94667
    Epoch [2290/10000], loss: 0.35253 acc: 0.90667 val_loss: 0.33853, val_acc: 0.94667
    Epoch [2300/10000], loss: 0.35201 acc: 0.90667 val_loss: 0.33802, val_acc: 0.94667
    Epoch [2310/10000], loss: 0.35150 acc: 0.90667 val_loss: 0.33750, val_acc: 0.94667
    Epoch [2320/10000], loss: 0.35099 acc: 0.90667 val_loss: 0.33699, val_acc: 0.94667
    Epoch [2330/10000], loss: 0.35048 acc: 0.90667 val_loss: 0.33648, val_acc: 0.94667
    Epoch [2340/10000], loss: 0.34998 acc: 0.90667 val_loss: 0.33597, val_acc: 0.94667
    Epoch [2350/10000], loss: 0.34947 acc: 0.90667 val_loss: 0.33546, val_acc: 0.94667
    Epoch [2360/10000], loss: 0.34897 acc: 0.90667 val_loss: 0.33496, val_acc: 0.94667
    Epoch [2370/10000], loss: 0.34848 acc: 0.90667 val_loss: 0.33446, val_acc: 0.94667
    Epoch [2380/10000], loss: 0.34798 acc: 0.90667 val_loss: 0.33396, val_acc: 0.94667
    Epoch [2390/10000], loss: 0.34749 acc: 0.90667 val_loss: 0.33347, val_acc: 0.94667
    Epoch [2400/10000], loss: 0.34700 acc: 0.90667 val_loss: 0.33297, val_acc: 0.94667
    Epoch [2410/10000], loss: 0.34651 acc: 0.90667 val_loss: 0.33248, val_acc: 0.94667
    Epoch [2420/10000], loss: 0.34602 acc: 0.90667 val_loss: 0.33199, val_acc: 0.94667
    Epoch [2430/10000], loss: 0.34554 acc: 0.90667 val_loss: 0.33151, val_acc: 0.94667
    Epoch [2440/10000], loss: 0.34506 acc: 0.90667 val_loss: 0.33102, val_acc: 0.94667
    Epoch [2450/10000], loss: 0.34458 acc: 0.90667 val_loss: 0.33054, val_acc: 0.94667
    Epoch [2460/10000], loss: 0.34411 acc: 0.90667 val_loss: 0.33006, val_acc: 0.94667
    Epoch [2470/10000], loss: 0.34363 acc: 0.90667 val_loss: 0.32959, val_acc: 0.94667
    Epoch [2480/10000], loss: 0.34316 acc: 0.90667 val_loss: 0.32911, val_acc: 0.94667
    Epoch [2490/10000], loss: 0.34269 acc: 0.90667 val_loss: 0.32864, val_acc: 0.94667
    Epoch [2500/10000], loss: 0.34222 acc: 0.90667 val_loss: 0.32817, val_acc: 0.94667
    Epoch [2510/10000], loss: 0.34176 acc: 0.90667 val_loss: 0.32770, val_acc: 0.94667
    Epoch [2520/10000], loss: 0.34130 acc: 0.90667 val_loss: 0.32723, val_acc: 0.94667
    Epoch [2530/10000], loss: 0.34083 acc: 0.90667 val_loss: 0.32677, val_acc: 0.94667
    Epoch [2540/10000], loss: 0.34038 acc: 0.90667 val_loss: 0.32631, val_acc: 0.94667
    Epoch [2550/10000], loss: 0.33992 acc: 0.90667 val_loss: 0.32585, val_acc: 0.94667
    Epoch [2560/10000], loss: 0.33947 acc: 0.90667 val_loss: 0.32539, val_acc: 0.94667
    Epoch [2570/10000], loss: 0.33901 acc: 0.90667 val_loss: 0.32493, val_acc: 0.94667
    Epoch [2580/10000], loss: 0.33856 acc: 0.90667 val_loss: 0.32448, val_acc: 0.94667
    Epoch [2590/10000], loss: 0.33812 acc: 0.90667 val_loss: 0.32403, val_acc: 0.94667
    Epoch [2600/10000], loss: 0.33767 acc: 0.90667 val_loss: 0.32358, val_acc: 0.94667
    Epoch [2610/10000], loss: 0.33723 acc: 0.90667 val_loss: 0.32313, val_acc: 0.94667
    Epoch [2620/10000], loss: 0.33678 acc: 0.90667 val_loss: 0.32269, val_acc: 0.94667
    Epoch [2630/10000], loss: 0.33634 acc: 0.90667 val_loss: 0.32225, val_acc: 0.94667
    Epoch [2640/10000], loss: 0.33591 acc: 0.90667 val_loss: 0.32180, val_acc: 0.94667
    Epoch [2650/10000], loss: 0.33547 acc: 0.90667 val_loss: 0.32136, val_acc: 0.94667
    Epoch [2660/10000], loss: 0.33504 acc: 0.90667 val_loss: 0.32093, val_acc: 0.94667
    Epoch [2670/10000], loss: 0.33460 acc: 0.90667 val_loss: 0.32049, val_acc: 0.94667
    Epoch [2680/10000], loss: 0.33417 acc: 0.90667 val_loss: 0.32006, val_acc: 0.94667
    Epoch [2690/10000], loss: 0.33375 acc: 0.90667 val_loss: 0.31963, val_acc: 0.94667
    Epoch [2700/10000], loss: 0.33332 acc: 0.90667 val_loss: 0.31920, val_acc: 0.94667
    Epoch [2710/10000], loss: 0.33290 acc: 0.90667 val_loss: 0.31877, val_acc: 0.94667
    Epoch [2720/10000], loss: 0.33247 acc: 0.90667 val_loss: 0.31834, val_acc: 0.94667
    Epoch [2730/10000], loss: 0.33205 acc: 0.90667 val_loss: 0.31792, val_acc: 0.94667
    Epoch [2740/10000], loss: 0.33164 acc: 0.90667 val_loss: 0.31750, val_acc: 0.94667
    Epoch [2750/10000], loss: 0.33122 acc: 0.90667 val_loss: 0.31708, val_acc: 0.94667
    Epoch [2760/10000], loss: 0.33080 acc: 0.90667 val_loss: 0.31666, val_acc: 0.94667
    Epoch [2770/10000], loss: 0.33039 acc: 0.90667 val_loss: 0.31624, val_acc: 0.94667
    Epoch [2780/10000], loss: 0.32998 acc: 0.90667 val_loss: 0.31583, val_acc: 0.94667
    Epoch [2790/10000], loss: 0.32957 acc: 0.90667 val_loss: 0.31542, val_acc: 0.94667
    Epoch [2800/10000], loss: 0.32916 acc: 0.90667 val_loss: 0.31500, val_acc: 0.94667
    Epoch [2810/10000], loss: 0.32876 acc: 0.90667 val_loss: 0.31460, val_acc: 0.94667
    Epoch [2820/10000], loss: 0.32835 acc: 0.90667 val_loss: 0.31419, val_acc: 0.94667
    Epoch [2830/10000], loss: 0.32795 acc: 0.90667 val_loss: 0.31378, val_acc: 0.94667
    Epoch [2840/10000], loss: 0.32755 acc: 0.90667 val_loss: 0.31338, val_acc: 0.94667
    Epoch [2850/10000], loss: 0.32715 acc: 0.90667 val_loss: 0.31297, val_acc: 0.94667
    Epoch [2860/10000], loss: 0.32675 acc: 0.90667 val_loss: 0.31257, val_acc: 0.94667
    Epoch [2870/10000], loss: 0.32636 acc: 0.90667 val_loss: 0.31217, val_acc: 0.94667
    Epoch [2880/10000], loss: 0.32597 acc: 0.90667 val_loss: 0.31178, val_acc: 0.94667
    Epoch [2890/10000], loss: 0.32557 acc: 0.90667 val_loss: 0.31138, val_acc: 0.94667
    Epoch [2900/10000], loss: 0.32518 acc: 0.90667 val_loss: 0.31099, val_acc: 0.94667
    Epoch [2910/10000], loss: 0.32480 acc: 0.90667 val_loss: 0.31060, val_acc: 0.94667
    Epoch [2920/10000], loss: 0.32441 acc: 0.90667 val_loss: 0.31020, val_acc: 0.94667
    Epoch [2930/10000], loss: 0.32402 acc: 0.90667 val_loss: 0.30982, val_acc: 0.94667
    Epoch [2940/10000], loss: 0.32364 acc: 0.90667 val_loss: 0.30943, val_acc: 0.94667
    Epoch [2950/10000], loss: 0.32326 acc: 0.90667 val_loss: 0.30904, val_acc: 0.94667
    Epoch [2960/10000], loss: 0.32288 acc: 0.90667 val_loss: 0.30866, val_acc: 0.94667
    Epoch [2970/10000], loss: 0.32250 acc: 0.90667 val_loss: 0.30827, val_acc: 0.94667
    Epoch [2980/10000], loss: 0.32212 acc: 0.90667 val_loss: 0.30789, val_acc: 0.94667
    Epoch [2990/10000], loss: 0.32175 acc: 0.90667 val_loss: 0.30751, val_acc: 0.94667
    Epoch [3000/10000], loss: 0.32137 acc: 0.90667 val_loss: 0.30714, val_acc: 0.94667
    Epoch [3010/10000], loss: 0.32100 acc: 0.90667 val_loss: 0.30676, val_acc: 0.94667
    Epoch [3020/10000], loss: 0.32063 acc: 0.90667 val_loss: 0.30638, val_acc: 0.94667
    Epoch [3030/10000], loss: 0.32026 acc: 0.90667 val_loss: 0.30601, val_acc: 0.94667
    Epoch [3040/10000], loss: 0.31989 acc: 0.90667 val_loss: 0.30564, val_acc: 0.94667
    Epoch [3050/10000], loss: 0.31952 acc: 0.90667 val_loss: 0.30527, val_acc: 0.94667
    Epoch [3060/10000], loss: 0.31916 acc: 0.90667 val_loss: 0.30490, val_acc: 0.94667
    Epoch [3070/10000], loss: 0.31880 acc: 0.90667 val_loss: 0.30453, val_acc: 0.94667
    Epoch [3080/10000], loss: 0.31844 acc: 0.90667 val_loss: 0.30417, val_acc: 0.94667
    Epoch [3090/10000], loss: 0.31807 acc: 0.90667 val_loss: 0.30380, val_acc: 0.94667
    Epoch [3100/10000], loss: 0.31772 acc: 0.90667 val_loss: 0.30344, val_acc: 0.94667
    Epoch [3110/10000], loss: 0.31736 acc: 0.90667 val_loss: 0.30308, val_acc: 0.94667
    Epoch [3120/10000], loss: 0.31700 acc: 0.90667 val_loss: 0.30272, val_acc: 0.94667
    Epoch [3130/10000], loss: 0.31665 acc: 0.90667 val_loss: 0.30236, val_acc: 0.94667
    Epoch [3140/10000], loss: 0.31630 acc: 0.90667 val_loss: 0.30200, val_acc: 0.94667
    Epoch [3150/10000], loss: 0.31594 acc: 0.90667 val_loss: 0.30165, val_acc: 0.94667
    Epoch [3160/10000], loss: 0.31559 acc: 0.90667 val_loss: 0.30129, val_acc: 0.94667
    Epoch [3170/10000], loss: 0.31525 acc: 0.90667 val_loss: 0.30094, val_acc: 0.94667
    Epoch [3180/10000], loss: 0.31490 acc: 0.90667 val_loss: 0.30059, val_acc: 0.94667
    Epoch [3190/10000], loss: 0.31455 acc: 0.90667 val_loss: 0.30024, val_acc: 0.94667
    Epoch [3200/10000], loss: 0.31421 acc: 0.90667 val_loss: 0.29989, val_acc: 0.94667
    Epoch [3210/10000], loss: 0.31386 acc: 0.90667 val_loss: 0.29954, val_acc: 0.94667
    Epoch [3220/10000], loss: 0.31352 acc: 0.90667 val_loss: 0.29919, val_acc: 0.94667
    Epoch [3230/10000], loss: 0.31318 acc: 0.90667 val_loss: 0.29885, val_acc: 0.94667
    Epoch [3240/10000], loss: 0.31284 acc: 0.90667 val_loss: 0.29851, val_acc: 0.94667
    Epoch [3250/10000], loss: 0.31251 acc: 0.90667 val_loss: 0.29816, val_acc: 0.94667
    Epoch [3260/10000], loss: 0.31217 acc: 0.90667 val_loss: 0.29782, val_acc: 0.94667
    Epoch [3270/10000], loss: 0.31183 acc: 0.90667 val_loss: 0.29748, val_acc: 0.94667
    Epoch [3280/10000], loss: 0.31150 acc: 0.90667 val_loss: 0.29715, val_acc: 0.94667
    Epoch [3290/10000], loss: 0.31117 acc: 0.90667 val_loss: 0.29681, val_acc: 0.94667
    Epoch [3300/10000], loss: 0.31084 acc: 0.90667 val_loss: 0.29647, val_acc: 0.94667
    Epoch [3310/10000], loss: 0.31051 acc: 0.90667 val_loss: 0.29614, val_acc: 0.94667
    Epoch [3320/10000], loss: 0.31018 acc: 0.90667 val_loss: 0.29581, val_acc: 0.94667
    Epoch [3330/10000], loss: 0.30985 acc: 0.90667 val_loss: 0.29548, val_acc: 0.94667
    Epoch [3340/10000], loss: 0.30953 acc: 0.90667 val_loss: 0.29515, val_acc: 0.94667
    Epoch [3350/10000], loss: 0.30920 acc: 0.90667 val_loss: 0.29482, val_acc: 0.94667
    Epoch [3360/10000], loss: 0.30888 acc: 0.90667 val_loss: 0.29449, val_acc: 0.94667
    Epoch [3370/10000], loss: 0.30856 acc: 0.90667 val_loss: 0.29416, val_acc: 0.94667
    Epoch [3380/10000], loss: 0.30824 acc: 0.90667 val_loss: 0.29384, val_acc: 0.94667
    Epoch [3390/10000], loss: 0.30792 acc: 0.90667 val_loss: 0.29351, val_acc: 0.94667
    Epoch [3400/10000], loss: 0.30760 acc: 0.90667 val_loss: 0.29319, val_acc: 0.94667
    Epoch [3410/10000], loss: 0.30728 acc: 0.90667 val_loss: 0.29287, val_acc: 0.94667
    Epoch [3420/10000], loss: 0.30696 acc: 0.90667 val_loss: 0.29255, val_acc: 0.94667
    Epoch [3430/10000], loss: 0.30665 acc: 0.90667 val_loss: 0.29223, val_acc: 0.94667
    Epoch [3440/10000], loss: 0.30634 acc: 0.90667 val_loss: 0.29191, val_acc: 0.94667
    Epoch [3450/10000], loss: 0.30602 acc: 0.90667 val_loss: 0.29159, val_acc: 0.94667
    Epoch [3460/10000], loss: 0.30571 acc: 0.90667 val_loss: 0.29128, val_acc: 0.94667
    Epoch [3470/10000], loss: 0.30540 acc: 0.90667 val_loss: 0.29096, val_acc: 0.94667
    Epoch [3480/10000], loss: 0.30509 acc: 0.90667 val_loss: 0.29065, val_acc: 0.94667
    Epoch [3490/10000], loss: 0.30479 acc: 0.90667 val_loss: 0.29034, val_acc: 0.94667
    Epoch [3500/10000], loss: 0.30448 acc: 0.90667 val_loss: 0.29003, val_acc: 0.94667
    Epoch [3510/10000], loss: 0.30417 acc: 0.90667 val_loss: 0.28972, val_acc: 0.94667
    Epoch [3520/10000], loss: 0.30387 acc: 0.90667 val_loss: 0.28941, val_acc: 0.94667
    Epoch [3530/10000], loss: 0.30357 acc: 0.90667 val_loss: 0.28910, val_acc: 0.94667
    Epoch [3540/10000], loss: 0.30327 acc: 0.90667 val_loss: 0.28879, val_acc: 0.94667
    Epoch [3550/10000], loss: 0.30297 acc: 0.90667 val_loss: 0.28849, val_acc: 0.94667
    Epoch [3560/10000], loss: 0.30267 acc: 0.90667 val_loss: 0.28818, val_acc: 0.94667
    Epoch [3570/10000], loss: 0.30237 acc: 0.90667 val_loss: 0.28788, val_acc: 0.94667
    Epoch [3580/10000], loss: 0.30207 acc: 0.90667 val_loss: 0.28758, val_acc: 0.94667
    Epoch [3590/10000], loss: 0.30177 acc: 0.90667 val_loss: 0.28728, val_acc: 0.94667
    Epoch [3600/10000], loss: 0.30148 acc: 0.90667 val_loss: 0.28698, val_acc: 0.94667
    Epoch [3610/10000], loss: 0.30119 acc: 0.90667 val_loss: 0.28668, val_acc: 0.94667
    Epoch [3620/10000], loss: 0.30089 acc: 0.90667 val_loss: 0.28638, val_acc: 0.96000
    Epoch [3630/10000], loss: 0.30060 acc: 0.90667 val_loss: 0.28608, val_acc: 0.96000
    Epoch [3640/10000], loss: 0.30031 acc: 0.90667 val_loss: 0.28579, val_acc: 0.96000
    Epoch [3650/10000], loss: 0.30002 acc: 0.90667 val_loss: 0.28549, val_acc: 0.96000
    Epoch [3660/10000], loss: 0.29973 acc: 0.90667 val_loss: 0.28520, val_acc: 0.96000
    Epoch [3670/10000], loss: 0.29944 acc: 0.90667 val_loss: 0.28491, val_acc: 0.96000
    Epoch [3680/10000], loss: 0.29916 acc: 0.90667 val_loss: 0.28462, val_acc: 0.96000
    Epoch [3690/10000], loss: 0.29887 acc: 0.90667 val_loss: 0.28433, val_acc: 0.96000
    Epoch [3700/10000], loss: 0.29859 acc: 0.90667 val_loss: 0.28404, val_acc: 0.96000
    Epoch [3710/10000], loss: 0.29830 acc: 0.90667 val_loss: 0.28375, val_acc: 0.96000
    Epoch [3720/10000], loss: 0.29802 acc: 0.90667 val_loss: 0.28346, val_acc: 0.96000
    Epoch [3730/10000], loss: 0.29774 acc: 0.90667 val_loss: 0.28318, val_acc: 0.96000
    Epoch [3740/10000], loss: 0.29746 acc: 0.90667 val_loss: 0.28289, val_acc: 0.96000
    Epoch [3750/10000], loss: 0.29718 acc: 0.90667 val_loss: 0.28261, val_acc: 0.96000
    Epoch [3760/10000], loss: 0.29690 acc: 0.90667 val_loss: 0.28232, val_acc: 0.96000
    Epoch [3770/10000], loss: 0.29663 acc: 0.90667 val_loss: 0.28204, val_acc: 0.96000
    Epoch [3780/10000], loss: 0.29635 acc: 0.90667 val_loss: 0.28176, val_acc: 0.96000
    Epoch [3790/10000], loss: 0.29607 acc: 0.90667 val_loss: 0.28148, val_acc: 0.96000
    Epoch [3800/10000], loss: 0.29580 acc: 0.90667 val_loss: 0.28120, val_acc: 0.96000
    Epoch [3810/10000], loss: 0.29553 acc: 0.90667 val_loss: 0.28092, val_acc: 0.96000
    Epoch [3820/10000], loss: 0.29525 acc: 0.90667 val_loss: 0.28064, val_acc: 0.96000
    Epoch [3830/10000], loss: 0.29498 acc: 0.90667 val_loss: 0.28037, val_acc: 0.96000
    Epoch [3840/10000], loss: 0.29471 acc: 0.90667 val_loss: 0.28009, val_acc: 0.96000
    Epoch [3850/10000], loss: 0.29444 acc: 0.90667 val_loss: 0.27982, val_acc: 0.96000
    Epoch [3860/10000], loss: 0.29418 acc: 0.90667 val_loss: 0.27954, val_acc: 0.96000
    Epoch [3870/10000], loss: 0.29391 acc: 0.90667 val_loss: 0.27927, val_acc: 0.96000
    Epoch [3880/10000], loss: 0.29364 acc: 0.90667 val_loss: 0.27900, val_acc: 0.96000
    Epoch [3890/10000], loss: 0.29338 acc: 0.90667 val_loss: 0.27873, val_acc: 0.96000
    Epoch [3900/10000], loss: 0.29311 acc: 0.90667 val_loss: 0.27846, val_acc: 0.96000
    Epoch [3910/10000], loss: 0.29285 acc: 0.90667 val_loss: 0.27819, val_acc: 0.96000
    Epoch [3920/10000], loss: 0.29258 acc: 0.90667 val_loss: 0.27792, val_acc: 0.96000
    Epoch [3930/10000], loss: 0.29232 acc: 0.90667 val_loss: 0.27766, val_acc: 0.96000
    Epoch [3940/10000], loss: 0.29206 acc: 0.90667 val_loss: 0.27739, val_acc: 0.96000
    Epoch [3950/10000], loss: 0.29180 acc: 0.90667 val_loss: 0.27712, val_acc: 0.96000
    Epoch [3960/10000], loss: 0.29154 acc: 0.90667 val_loss: 0.27686, val_acc: 0.96000
    Epoch [3970/10000], loss: 0.29128 acc: 0.90667 val_loss: 0.27660, val_acc: 0.96000
    Epoch [3980/10000], loss: 0.29103 acc: 0.90667 val_loss: 0.27633, val_acc: 0.96000
    Epoch [3990/10000], loss: 0.29077 acc: 0.90667 val_loss: 0.27607, val_acc: 0.96000
    Epoch [4000/10000], loss: 0.29052 acc: 0.90667 val_loss: 0.27581, val_acc: 0.96000
    Epoch [4010/10000], loss: 0.29026 acc: 0.90667 val_loss: 0.27555, val_acc: 0.96000
    Epoch [4020/10000], loss: 0.29001 acc: 0.90667 val_loss: 0.27529, val_acc: 0.96000
    Epoch [4030/10000], loss: 0.28975 acc: 0.90667 val_loss: 0.27504, val_acc: 0.96000
    Epoch [4040/10000], loss: 0.28950 acc: 0.90667 val_loss: 0.27478, val_acc: 0.96000
    Epoch [4050/10000], loss: 0.28925 acc: 0.90667 val_loss: 0.27452, val_acc: 0.96000
    Epoch [4060/10000], loss: 0.28900 acc: 0.90667 val_loss: 0.27427, val_acc: 0.96000
    Epoch [4070/10000], loss: 0.28875 acc: 0.90667 val_loss: 0.27401, val_acc: 0.96000
    Epoch [4080/10000], loss: 0.28850 acc: 0.90667 val_loss: 0.27376, val_acc: 0.96000
    Epoch [4090/10000], loss: 0.28826 acc: 0.90667 val_loss: 0.27351, val_acc: 0.96000
    Epoch [4100/10000], loss: 0.28801 acc: 0.90667 val_loss: 0.27325, val_acc: 0.96000
    Epoch [4110/10000], loss: 0.28776 acc: 0.90667 val_loss: 0.27300, val_acc: 0.96000
    Epoch [4120/10000], loss: 0.28752 acc: 0.90667 val_loss: 0.27275, val_acc: 0.96000
    Epoch [4130/10000], loss: 0.28727 acc: 0.90667 val_loss: 0.27250, val_acc: 0.96000
    Epoch [4140/10000], loss: 0.28703 acc: 0.90667 val_loss: 0.27225, val_acc: 0.96000
    Epoch [4150/10000], loss: 0.28679 acc: 0.90667 val_loss: 0.27200, val_acc: 0.96000
    Epoch [4160/10000], loss: 0.28654 acc: 0.90667 val_loss: 0.27176, val_acc: 0.96000
    Epoch [4170/10000], loss: 0.28630 acc: 0.90667 val_loss: 0.27151, val_acc: 0.96000
    Epoch [4180/10000], loss: 0.28606 acc: 0.90667 val_loss: 0.27127, val_acc: 0.96000
    Epoch [4190/10000], loss: 0.28582 acc: 0.90667 val_loss: 0.27102, val_acc: 0.96000
    Epoch [4200/10000], loss: 0.28559 acc: 0.90667 val_loss: 0.27078, val_acc: 0.96000
    Epoch [4210/10000], loss: 0.28535 acc: 0.90667 val_loss: 0.27053, val_acc: 0.96000
    Epoch [4220/10000], loss: 0.28511 acc: 0.90667 val_loss: 0.27029, val_acc: 0.96000
    Epoch [4230/10000], loss: 0.28487 acc: 0.90667 val_loss: 0.27005, val_acc: 0.96000
    Epoch [4240/10000], loss: 0.28464 acc: 0.90667 val_loss: 0.26981, val_acc: 0.96000
    Epoch [4250/10000], loss: 0.28440 acc: 0.90667 val_loss: 0.26957, val_acc: 0.96000
    Epoch [4260/10000], loss: 0.28417 acc: 0.90667 val_loss: 0.26933, val_acc: 0.96000
    Epoch [4270/10000], loss: 0.28394 acc: 0.90667 val_loss: 0.26909, val_acc: 0.96000
    Epoch [4280/10000], loss: 0.28370 acc: 0.90667 val_loss: 0.26885, val_acc: 0.96000
    Epoch [4290/10000], loss: 0.28347 acc: 0.90667 val_loss: 0.26862, val_acc: 0.96000
    Epoch [4300/10000], loss: 0.28324 acc: 0.90667 val_loss: 0.26838, val_acc: 0.96000
    Epoch [4310/10000], loss: 0.28301 acc: 0.90667 val_loss: 0.26815, val_acc: 0.96000
    Epoch [4320/10000], loss: 0.28278 acc: 0.90667 val_loss: 0.26791, val_acc: 0.96000
    Epoch [4330/10000], loss: 0.28255 acc: 0.90667 val_loss: 0.26768, val_acc: 0.96000
    Epoch [4340/10000], loss: 0.28233 acc: 0.90667 val_loss: 0.26744, val_acc: 0.96000
    Epoch [4350/10000], loss: 0.28210 acc: 0.90667 val_loss: 0.26721, val_acc: 0.96000
    Epoch [4360/10000], loss: 0.28187 acc: 0.90667 val_loss: 0.26698, val_acc: 0.96000
    Epoch [4370/10000], loss: 0.28165 acc: 0.90667 val_loss: 0.26675, val_acc: 0.96000
    Epoch [4380/10000], loss: 0.28142 acc: 0.90667 val_loss: 0.26652, val_acc: 0.96000
    Epoch [4390/10000], loss: 0.28120 acc: 0.90667 val_loss: 0.26629, val_acc: 0.96000
    Epoch [4400/10000], loss: 0.28098 acc: 0.90667 val_loss: 0.26606, val_acc: 0.96000
    Epoch [4410/10000], loss: 0.28075 acc: 0.90667 val_loss: 0.26583, val_acc: 0.96000
    Epoch [4420/10000], loss: 0.28053 acc: 0.90667 val_loss: 0.26560, val_acc: 0.96000
    Epoch [4430/10000], loss: 0.28031 acc: 0.90667 val_loss: 0.26538, val_acc: 0.96000
    Epoch [4440/10000], loss: 0.28009 acc: 0.90667 val_loss: 0.26515, val_acc: 0.96000
    Epoch [4450/10000], loss: 0.27987 acc: 0.90667 val_loss: 0.26493, val_acc: 0.96000
    Epoch [4460/10000], loss: 0.27965 acc: 0.90667 val_loss: 0.26470, val_acc: 0.96000
    Epoch [4470/10000], loss: 0.27943 acc: 0.90667 val_loss: 0.26448, val_acc: 0.96000
    Epoch [4480/10000], loss: 0.27922 acc: 0.90667 val_loss: 0.26425, val_acc: 0.96000
    Epoch [4490/10000], loss: 0.27900 acc: 0.90667 val_loss: 0.26403, val_acc: 0.96000
    Epoch [4500/10000], loss: 0.27878 acc: 0.90667 val_loss: 0.26381, val_acc: 0.96000
    Epoch [4510/10000], loss: 0.27857 acc: 0.90667 val_loss: 0.26359, val_acc: 0.96000
    Epoch [4520/10000], loss: 0.27835 acc: 0.90667 val_loss: 0.26337, val_acc: 0.96000
    Epoch [4530/10000], loss: 0.27814 acc: 0.90667 val_loss: 0.26315, val_acc: 0.96000
    Epoch [4540/10000], loss: 0.27792 acc: 0.90667 val_loss: 0.26293, val_acc: 0.96000
    Epoch [4550/10000], loss: 0.27771 acc: 0.90667 val_loss: 0.26271, val_acc: 0.96000
    Epoch [4560/10000], loss: 0.27750 acc: 0.90667 val_loss: 0.26249, val_acc: 0.96000
    Epoch [4570/10000], loss: 0.27729 acc: 0.90667 val_loss: 0.26228, val_acc: 0.96000
    Epoch [4580/10000], loss: 0.27708 acc: 0.90667 val_loss: 0.26206, val_acc: 0.96000
    Epoch [4590/10000], loss: 0.27687 acc: 0.90667 val_loss: 0.26185, val_acc: 0.96000
    Epoch [4600/10000], loss: 0.27666 acc: 0.90667 val_loss: 0.26163, val_acc: 0.96000
    Epoch [4610/10000], loss: 0.27645 acc: 0.90667 val_loss: 0.26142, val_acc: 0.96000
    Epoch [4620/10000], loss: 0.27624 acc: 0.90667 val_loss: 0.26120, val_acc: 0.96000
    Epoch [4630/10000], loss: 0.27603 acc: 0.90667 val_loss: 0.26099, val_acc: 0.96000
    Epoch [4640/10000], loss: 0.27583 acc: 0.90667 val_loss: 0.26078, val_acc: 0.96000
    Epoch [4650/10000], loss: 0.27562 acc: 0.90667 val_loss: 0.26057, val_acc: 0.96000
    Epoch [4660/10000], loss: 0.27541 acc: 0.90667 val_loss: 0.26035, val_acc: 0.96000
    Epoch [4670/10000], loss: 0.27521 acc: 0.90667 val_loss: 0.26014, val_acc: 0.96000
    Epoch [4680/10000], loss: 0.27500 acc: 0.90667 val_loss: 0.25993, val_acc: 0.96000
    Epoch [4690/10000], loss: 0.27480 acc: 0.90667 val_loss: 0.25973, val_acc: 0.96000
    Epoch [4700/10000], loss: 0.27460 acc: 0.90667 val_loss: 0.25952, val_acc: 0.96000
    Epoch [4710/10000], loss: 0.27440 acc: 0.90667 val_loss: 0.25931, val_acc: 0.96000
    Epoch [4720/10000], loss: 0.27419 acc: 0.90667 val_loss: 0.25910, val_acc: 0.96000
    Epoch [4730/10000], loss: 0.27399 acc: 0.90667 val_loss: 0.25889, val_acc: 0.96000
    Epoch [4740/10000], loss: 0.27379 acc: 0.90667 val_loss: 0.25869, val_acc: 0.96000
    Epoch [4750/10000], loss: 0.27359 acc: 0.90667 val_loss: 0.25848, val_acc: 0.96000
    Epoch [4760/10000], loss: 0.27339 acc: 0.90667 val_loss: 0.25828, val_acc: 0.96000
    Epoch [4770/10000], loss: 0.27319 acc: 0.90667 val_loss: 0.25807, val_acc: 0.96000
    Epoch [4780/10000], loss: 0.27300 acc: 0.90667 val_loss: 0.25787, val_acc: 0.96000
    Epoch [4790/10000], loss: 0.27280 acc: 0.90667 val_loss: 0.25767, val_acc: 0.96000
    Epoch [4800/10000], loss: 0.27260 acc: 0.90667 val_loss: 0.25746, val_acc: 0.96000
    Epoch [4810/10000], loss: 0.27241 acc: 0.90667 val_loss: 0.25726, val_acc: 0.96000
    Epoch [4820/10000], loss: 0.27221 acc: 0.90667 val_loss: 0.25706, val_acc: 0.96000
    Epoch [4830/10000], loss: 0.27202 acc: 0.90667 val_loss: 0.25686, val_acc: 0.96000
    Epoch [4840/10000], loss: 0.27182 acc: 0.90667 val_loss: 0.25666, val_acc: 0.96000
    Epoch [4850/10000], loss: 0.27163 acc: 0.90667 val_loss: 0.25646, val_acc: 0.96000
    Epoch [4860/10000], loss: 0.27143 acc: 0.90667 val_loss: 0.25626, val_acc: 0.96000
    Epoch [4870/10000], loss: 0.27124 acc: 0.90667 val_loss: 0.25606, val_acc: 0.96000
    Epoch [4880/10000], loss: 0.27105 acc: 0.90667 val_loss: 0.25587, val_acc: 0.96000
    Epoch [4890/10000], loss: 0.27086 acc: 0.90667 val_loss: 0.25567, val_acc: 0.96000
    Epoch [4900/10000], loss: 0.27067 acc: 0.90667 val_loss: 0.25547, val_acc: 0.96000
    Epoch [4910/10000], loss: 0.27048 acc: 0.90667 val_loss: 0.25528, val_acc: 0.96000
    Epoch [4920/10000], loss: 0.27029 acc: 0.90667 val_loss: 0.25508, val_acc: 0.96000
    Epoch [4930/10000], loss: 0.27010 acc: 0.90667 val_loss: 0.25489, val_acc: 0.96000
    Epoch [4940/10000], loss: 0.26991 acc: 0.90667 val_loss: 0.25469, val_acc: 0.96000
    Epoch [4950/10000], loss: 0.26972 acc: 0.90667 val_loss: 0.25450, val_acc: 0.96000
    Epoch [4960/10000], loss: 0.26953 acc: 0.90667 val_loss: 0.25431, val_acc: 0.96000
    Epoch [4970/10000], loss: 0.26935 acc: 0.90667 val_loss: 0.25411, val_acc: 0.96000
    Epoch [4980/10000], loss: 0.26916 acc: 0.90667 val_loss: 0.25392, val_acc: 0.96000
    Epoch [4990/10000], loss: 0.26897 acc: 0.90667 val_loss: 0.25373, val_acc: 0.96000
    Epoch [5000/10000], loss: 0.26879 acc: 0.90667 val_loss: 0.25354, val_acc: 0.96000
    Epoch [5010/10000], loss: 0.26860 acc: 0.90667 val_loss: 0.25335, val_acc: 0.96000
    Epoch [5020/10000], loss: 0.26842 acc: 0.90667 val_loss: 0.25316, val_acc: 0.96000
    Epoch [5030/10000], loss: 0.26824 acc: 0.90667 val_loss: 0.25297, val_acc: 0.96000
    Epoch [5040/10000], loss: 0.26805 acc: 0.90667 val_loss: 0.25278, val_acc: 0.96000
    Epoch [5050/10000], loss: 0.26787 acc: 0.90667 val_loss: 0.25259, val_acc: 0.96000
    Epoch [5060/10000], loss: 0.26769 acc: 0.90667 val_loss: 0.25240, val_acc: 0.96000
    Epoch [5070/10000], loss: 0.26751 acc: 0.90667 val_loss: 0.25222, val_acc: 0.96000
    Epoch [5080/10000], loss: 0.26733 acc: 0.90667 val_loss: 0.25203, val_acc: 0.96000
    Epoch [5090/10000], loss: 0.26715 acc: 0.90667 val_loss: 0.25184, val_acc: 0.96000
    Epoch [5100/10000], loss: 0.26697 acc: 0.90667 val_loss: 0.25166, val_acc: 0.96000
    Epoch [5110/10000], loss: 0.26679 acc: 0.90667 val_loss: 0.25147, val_acc: 0.96000
    Epoch [5120/10000], loss: 0.26661 acc: 0.90667 val_loss: 0.25129, val_acc: 0.96000
    Epoch [5130/10000], loss: 0.26643 acc: 0.90667 val_loss: 0.25111, val_acc: 0.96000
    Epoch [5140/10000], loss: 0.26625 acc: 0.90667 val_loss: 0.25092, val_acc: 0.96000
    Epoch [5150/10000], loss: 0.26608 acc: 0.90667 val_loss: 0.25074, val_acc: 0.96000
    Epoch [5160/10000], loss: 0.26590 acc: 0.90667 val_loss: 0.25056, val_acc: 0.96000
    Epoch [5170/10000], loss: 0.26572 acc: 0.90667 val_loss: 0.25037, val_acc: 0.96000
    Epoch [5180/10000], loss: 0.26555 acc: 0.90667 val_loss: 0.25019, val_acc: 0.96000
    Epoch [5190/10000], loss: 0.26537 acc: 0.90667 val_loss: 0.25001, val_acc: 0.96000
    Epoch [5200/10000], loss: 0.26520 acc: 0.90667 val_loss: 0.24983, val_acc: 0.96000
    Epoch [5210/10000], loss: 0.26502 acc: 0.90667 val_loss: 0.24965, val_acc: 0.96000
    Epoch [5220/10000], loss: 0.26485 acc: 0.90667 val_loss: 0.24947, val_acc: 0.96000
    Epoch [5230/10000], loss: 0.26468 acc: 0.90667 val_loss: 0.24929, val_acc: 0.96000
    Epoch [5240/10000], loss: 0.26450 acc: 0.90667 val_loss: 0.24912, val_acc: 0.96000
    Epoch [5250/10000], loss: 0.26433 acc: 0.90667 val_loss: 0.24894, val_acc: 0.96000
    Epoch [5260/10000], loss: 0.26416 acc: 0.90667 val_loss: 0.24876, val_acc: 0.96000
    Epoch [5270/10000], loss: 0.26399 acc: 0.90667 val_loss: 0.24858, val_acc: 0.96000
    Epoch [5280/10000], loss: 0.26382 acc: 0.90667 val_loss: 0.24841, val_acc: 0.96000
    Epoch [5290/10000], loss: 0.26365 acc: 0.90667 val_loss: 0.24823, val_acc: 0.96000
    Epoch [5300/10000], loss: 0.26348 acc: 0.90667 val_loss: 0.24806, val_acc: 0.96000
    Epoch [5310/10000], loss: 0.26331 acc: 0.90667 val_loss: 0.24788, val_acc: 0.96000
    Epoch [5320/10000], loss: 0.26314 acc: 0.90667 val_loss: 0.24771, val_acc: 0.96000
    Epoch [5330/10000], loss: 0.26297 acc: 0.90667 val_loss: 0.24753, val_acc: 0.96000
    Epoch [5340/10000], loss: 0.26280 acc: 0.90667 val_loss: 0.24736, val_acc: 0.96000
    Epoch [5350/10000], loss: 0.26264 acc: 0.90667 val_loss: 0.24719, val_acc: 0.96000
    Epoch [5360/10000], loss: 0.26247 acc: 0.90667 val_loss: 0.24701, val_acc: 0.96000
    Epoch [5370/10000], loss: 0.26230 acc: 0.90667 val_loss: 0.24684, val_acc: 0.96000
    Epoch [5380/10000], loss: 0.26214 acc: 0.90667 val_loss: 0.24667, val_acc: 0.96000
    Epoch [5390/10000], loss: 0.26197 acc: 0.90667 val_loss: 0.24650, val_acc: 0.96000
    Epoch [5400/10000], loss: 0.26181 acc: 0.90667 val_loss: 0.24633, val_acc: 0.96000
    Epoch [5410/10000], loss: 0.26164 acc: 0.90667 val_loss: 0.24616, val_acc: 0.96000
    Epoch [5420/10000], loss: 0.26148 acc: 0.90667 val_loss: 0.24599, val_acc: 0.96000
    Epoch [5430/10000], loss: 0.26131 acc: 0.90667 val_loss: 0.24582, val_acc: 0.96000
    Epoch [5440/10000], loss: 0.26115 acc: 0.90667 val_loss: 0.24565, val_acc: 0.96000
    Epoch [5450/10000], loss: 0.26099 acc: 0.90667 val_loss: 0.24548, val_acc: 0.96000
    Epoch [5460/10000], loss: 0.26083 acc: 0.90667 val_loss: 0.24531, val_acc: 0.96000
    Epoch [5470/10000], loss: 0.26066 acc: 0.90667 val_loss: 0.24514, val_acc: 0.96000
    Epoch [5480/10000], loss: 0.26050 acc: 0.90667 val_loss: 0.24498, val_acc: 0.96000
    Epoch [5490/10000], loss: 0.26034 acc: 0.90667 val_loss: 0.24481, val_acc: 0.96000
    Epoch [5500/10000], loss: 0.26018 acc: 0.90667 val_loss: 0.24464, val_acc: 0.96000
    Epoch [5510/10000], loss: 0.26002 acc: 0.90667 val_loss: 0.24448, val_acc: 0.96000
    Epoch [5520/10000], loss: 0.25986 acc: 0.90667 val_loss: 0.24431, val_acc: 0.96000
    Epoch [5530/10000], loss: 0.25970 acc: 0.90667 val_loss: 0.24415, val_acc: 0.96000
    Epoch [5540/10000], loss: 0.25954 acc: 0.90667 val_loss: 0.24398, val_acc: 0.96000
    Epoch [5550/10000], loss: 0.25939 acc: 0.90667 val_loss: 0.24382, val_acc: 0.96000
    Epoch [5560/10000], loss: 0.25923 acc: 0.90667 val_loss: 0.24366, val_acc: 0.96000
    Epoch [5570/10000], loss: 0.25907 acc: 0.90667 val_loss: 0.24349, val_acc: 0.96000
    Epoch [5580/10000], loss: 0.25891 acc: 0.90667 val_loss: 0.24333, val_acc: 0.96000
    Epoch [5590/10000], loss: 0.25876 acc: 0.90667 val_loss: 0.24317, val_acc: 0.96000
    Epoch [5600/10000], loss: 0.25860 acc: 0.90667 val_loss: 0.24301, val_acc: 0.96000
    Epoch [5610/10000], loss: 0.25845 acc: 0.90667 val_loss: 0.24285, val_acc: 0.96000
    Epoch [5620/10000], loss: 0.25829 acc: 0.90667 val_loss: 0.24268, val_acc: 0.96000
    Epoch [5630/10000], loss: 0.25814 acc: 0.90667 val_loss: 0.24252, val_acc: 0.96000
    Epoch [5640/10000], loss: 0.25798 acc: 0.90667 val_loss: 0.24236, val_acc: 0.96000
    Epoch [5650/10000], loss: 0.25783 acc: 0.90667 val_loss: 0.24220, val_acc: 0.96000
    Epoch [5660/10000], loss: 0.25767 acc: 0.90667 val_loss: 0.24205, val_acc: 0.96000
    Epoch [5670/10000], loss: 0.25752 acc: 0.90667 val_loss: 0.24189, val_acc: 0.96000
    Epoch [5680/10000], loss: 0.25737 acc: 0.90667 val_loss: 0.24173, val_acc: 0.96000
    Epoch [5690/10000], loss: 0.25722 acc: 0.90667 val_loss: 0.24157, val_acc: 0.96000
    Epoch [5700/10000], loss: 0.25706 acc: 0.90667 val_loss: 0.24141, val_acc: 0.96000
    Epoch [5710/10000], loss: 0.25691 acc: 0.90667 val_loss: 0.24126, val_acc: 0.96000
    Epoch [5720/10000], loss: 0.25676 acc: 0.90667 val_loss: 0.24110, val_acc: 0.96000
    Epoch [5730/10000], loss: 0.25661 acc: 0.90667 val_loss: 0.24094, val_acc: 0.96000
    Epoch [5740/10000], loss: 0.25646 acc: 0.90667 val_loss: 0.24079, val_acc: 0.96000
    Epoch [5750/10000], loss: 0.25631 acc: 0.90667 val_loss: 0.24063, val_acc: 0.96000
    Epoch [5760/10000], loss: 0.25616 acc: 0.90667 val_loss: 0.24048, val_acc: 0.96000
    Epoch [5770/10000], loss: 0.25601 acc: 0.90667 val_loss: 0.24032, val_acc: 0.96000
    Epoch [5780/10000], loss: 0.25586 acc: 0.90667 val_loss: 0.24017, val_acc: 0.96000
    Epoch [5790/10000], loss: 0.25571 acc: 0.90667 val_loss: 0.24001, val_acc: 0.96000
    Epoch [5800/10000], loss: 0.25557 acc: 0.90667 val_loss: 0.23986, val_acc: 0.96000
    Epoch [5810/10000], loss: 0.25542 acc: 0.90667 val_loss: 0.23971, val_acc: 0.96000
    Epoch [5820/10000], loss: 0.25527 acc: 0.90667 val_loss: 0.23955, val_acc: 0.96000
    Epoch [5830/10000], loss: 0.25513 acc: 0.90667 val_loss: 0.23940, val_acc: 0.96000
    Epoch [5840/10000], loss: 0.25498 acc: 0.90667 val_loss: 0.23925, val_acc: 0.96000
    Epoch [5850/10000], loss: 0.25483 acc: 0.90667 val_loss: 0.23910, val_acc: 0.96000
    Epoch [5860/10000], loss: 0.25469 acc: 0.90667 val_loss: 0.23895, val_acc: 0.96000
    Epoch [5870/10000], loss: 0.25454 acc: 0.90667 val_loss: 0.23879, val_acc: 0.96000
    Epoch [5880/10000], loss: 0.25440 acc: 0.90667 val_loss: 0.23864, val_acc: 0.96000
    Epoch [5890/10000], loss: 0.25425 acc: 0.90667 val_loss: 0.23849, val_acc: 0.96000
    Epoch [5900/10000], loss: 0.25411 acc: 0.90667 val_loss: 0.23834, val_acc: 0.96000
    Epoch [5910/10000], loss: 0.25397 acc: 0.90667 val_loss: 0.23819, val_acc: 0.96000
    Epoch [5920/10000], loss: 0.25382 acc: 0.90667 val_loss: 0.23805, val_acc: 0.96000
    Epoch [5930/10000], loss: 0.25368 acc: 0.90667 val_loss: 0.23790, val_acc: 0.96000
    Epoch [5940/10000], loss: 0.25354 acc: 0.90667 val_loss: 0.23775, val_acc: 0.96000
    Epoch [5950/10000], loss: 0.25340 acc: 0.90667 val_loss: 0.23760, val_acc: 0.96000
    Epoch [5960/10000], loss: 0.25325 acc: 0.90667 val_loss: 0.23745, val_acc: 0.96000
    Epoch [5970/10000], loss: 0.25311 acc: 0.90667 val_loss: 0.23731, val_acc: 0.96000
    Epoch [5980/10000], loss: 0.25297 acc: 0.90667 val_loss: 0.23716, val_acc: 0.96000
    Epoch [5990/10000], loss: 0.25283 acc: 0.90667 val_loss: 0.23701, val_acc: 0.96000
    Epoch [6000/10000], loss: 0.25269 acc: 0.90667 val_loss: 0.23687, val_acc: 0.96000
    Epoch [6010/10000], loss: 0.25255 acc: 0.90667 val_loss: 0.23672, val_acc: 0.96000
    Epoch [6020/10000], loss: 0.25241 acc: 0.90667 val_loss: 0.23658, val_acc: 0.96000
    Epoch [6030/10000], loss: 0.25227 acc: 0.90667 val_loss: 0.23643, val_acc: 0.96000
    Epoch [6040/10000], loss: 0.25213 acc: 0.90667 val_loss: 0.23629, val_acc: 0.96000
    Epoch [6050/10000], loss: 0.25199 acc: 0.90667 val_loss: 0.23614, val_acc: 0.96000
    Epoch [6060/10000], loss: 0.25186 acc: 0.90667 val_loss: 0.23600, val_acc: 0.96000
    Epoch [6070/10000], loss: 0.25172 acc: 0.90667 val_loss: 0.23586, val_acc: 0.96000
    Epoch [6080/10000], loss: 0.25158 acc: 0.90667 val_loss: 0.23571, val_acc: 0.96000
    Epoch [6090/10000], loss: 0.25144 acc: 0.90667 val_loss: 0.23557, val_acc: 0.96000
    Epoch [6100/10000], loss: 0.25131 acc: 0.90667 val_loss: 0.23543, val_acc: 0.96000
    Epoch [6110/10000], loss: 0.25117 acc: 0.90667 val_loss: 0.23529, val_acc: 0.96000
    Epoch [6120/10000], loss: 0.25104 acc: 0.90667 val_loss: 0.23514, val_acc: 0.96000
    Epoch [6130/10000], loss: 0.25090 acc: 0.90667 val_loss: 0.23500, val_acc: 0.96000
    Epoch [6140/10000], loss: 0.25076 acc: 0.90667 val_loss: 0.23486, val_acc: 0.96000
    Epoch [6150/10000], loss: 0.25063 acc: 0.90667 val_loss: 0.23472, val_acc: 0.96000
    Epoch [6160/10000], loss: 0.25049 acc: 0.90667 val_loss: 0.23458, val_acc: 0.96000
    Epoch [6170/10000], loss: 0.25036 acc: 0.90667 val_loss: 0.23444, val_acc: 0.96000
    Epoch [6180/10000], loss: 0.25023 acc: 0.90667 val_loss: 0.23430, val_acc: 0.96000
    Epoch [6190/10000], loss: 0.25009 acc: 0.90667 val_loss: 0.23416, val_acc: 0.96000
    Epoch [6200/10000], loss: 0.24996 acc: 0.90667 val_loss: 0.23402, val_acc: 0.96000
    Epoch [6210/10000], loss: 0.24983 acc: 0.90667 val_loss: 0.23388, val_acc: 0.96000
    Epoch [6220/10000], loss: 0.24969 acc: 0.90667 val_loss: 0.23375, val_acc: 0.96000
    Epoch [6230/10000], loss: 0.24956 acc: 0.90667 val_loss: 0.23361, val_acc: 0.96000
    Epoch [6240/10000], loss: 0.24943 acc: 0.90667 val_loss: 0.23347, val_acc: 0.96000
    Epoch [6250/10000], loss: 0.24930 acc: 0.90667 val_loss: 0.23333, val_acc: 0.96000
    Epoch [6260/10000], loss: 0.24917 acc: 0.90667 val_loss: 0.23320, val_acc: 0.96000
    Epoch [6270/10000], loss: 0.24904 acc: 0.90667 val_loss: 0.23306, val_acc: 0.96000
    Epoch [6280/10000], loss: 0.24891 acc: 0.90667 val_loss: 0.23292, val_acc: 0.96000
    Epoch [6290/10000], loss: 0.24878 acc: 0.90667 val_loss: 0.23279, val_acc: 0.96000
    Epoch [6300/10000], loss: 0.24865 acc: 0.90667 val_loss: 0.23265, val_acc: 0.96000
    Epoch [6310/10000], loss: 0.24852 acc: 0.90667 val_loss: 0.23252, val_acc: 0.96000
    Epoch [6320/10000], loss: 0.24839 acc: 0.90667 val_loss: 0.23238, val_acc: 0.96000
    Epoch [6330/10000], loss: 0.24826 acc: 0.90667 val_loss: 0.23225, val_acc: 0.96000
    Epoch [6340/10000], loss: 0.24813 acc: 0.90667 val_loss: 0.23211, val_acc: 0.96000
    Epoch [6350/10000], loss: 0.24800 acc: 0.90667 val_loss: 0.23198, val_acc: 0.96000
    Epoch [6360/10000], loss: 0.24787 acc: 0.90667 val_loss: 0.23184, val_acc: 0.96000
    Epoch [6370/10000], loss: 0.24775 acc: 0.90667 val_loss: 0.23171, val_acc: 0.96000
    Epoch [6380/10000], loss: 0.24762 acc: 0.90667 val_loss: 0.23158, val_acc: 0.96000
    Epoch [6390/10000], loss: 0.24749 acc: 0.90667 val_loss: 0.23145, val_acc: 0.96000
    Epoch [6400/10000], loss: 0.24736 acc: 0.90667 val_loss: 0.23131, val_acc: 0.96000
    Epoch [6410/10000], loss: 0.24724 acc: 0.90667 val_loss: 0.23118, val_acc: 0.96000
    Epoch [6420/10000], loss: 0.24711 acc: 0.90667 val_loss: 0.23105, val_acc: 0.96000
    Epoch [6430/10000], loss: 0.24699 acc: 0.90667 val_loss: 0.23092, val_acc: 0.96000
    Epoch [6440/10000], loss: 0.24686 acc: 0.90667 val_loss: 0.23079, val_acc: 0.96000
    Epoch [6450/10000], loss: 0.24674 acc: 0.90667 val_loss: 0.23066, val_acc: 0.96000
    Epoch [6460/10000], loss: 0.24661 acc: 0.90667 val_loss: 0.23053, val_acc: 0.96000
    Epoch [6470/10000], loss: 0.24649 acc: 0.90667 val_loss: 0.23040, val_acc: 0.96000
    Epoch [6480/10000], loss: 0.24636 acc: 0.90667 val_loss: 0.23027, val_acc: 0.96000
    Epoch [6490/10000], loss: 0.24624 acc: 0.90667 val_loss: 0.23014, val_acc: 0.96000
    Epoch [6500/10000], loss: 0.24611 acc: 0.90667 val_loss: 0.23001, val_acc: 0.96000
    Epoch [6510/10000], loss: 0.24599 acc: 0.90667 val_loss: 0.22988, val_acc: 0.96000
    Epoch [6520/10000], loss: 0.24587 acc: 0.90667 val_loss: 0.22975, val_acc: 0.96000
    Epoch [6530/10000], loss: 0.24575 acc: 0.90667 val_loss: 0.22962, val_acc: 0.96000
    Epoch [6540/10000], loss: 0.24562 acc: 0.90667 val_loss: 0.22949, val_acc: 0.96000
    Epoch [6550/10000], loss: 0.24550 acc: 0.90667 val_loss: 0.22936, val_acc: 0.96000
    Epoch [6560/10000], loss: 0.24538 acc: 0.90667 val_loss: 0.22924, val_acc: 0.96000
    Epoch [6570/10000], loss: 0.24526 acc: 0.90667 val_loss: 0.22911, val_acc: 0.96000
    Epoch [6580/10000], loss: 0.24514 acc: 0.90667 val_loss: 0.22898, val_acc: 0.96000
    Epoch [6590/10000], loss: 0.24502 acc: 0.90667 val_loss: 0.22886, val_acc: 0.96000
    Epoch [6600/10000], loss: 0.24489 acc: 0.90667 val_loss: 0.22873, val_acc: 0.96000
    Epoch [6610/10000], loss: 0.24477 acc: 0.90667 val_loss: 0.22860, val_acc: 0.96000
    Epoch [6620/10000], loss: 0.24465 acc: 0.90667 val_loss: 0.22848, val_acc: 0.96000
    Epoch [6630/10000], loss: 0.24453 acc: 0.90667 val_loss: 0.22835, val_acc: 0.96000
    Epoch [6640/10000], loss: 0.24441 acc: 0.90667 val_loss: 0.22823, val_acc: 0.96000
    Epoch [6650/10000], loss: 0.24430 acc: 0.90667 val_loss: 0.22810, val_acc: 0.96000
    Epoch [6660/10000], loss: 0.24418 acc: 0.90667 val_loss: 0.22798, val_acc: 0.96000
    Epoch [6670/10000], loss: 0.24406 acc: 0.90667 val_loss: 0.22785, val_acc: 0.96000
    Epoch [6680/10000], loss: 0.24394 acc: 0.90667 val_loss: 0.22773, val_acc: 0.96000
    Epoch [6690/10000], loss: 0.24382 acc: 0.90667 val_loss: 0.22761, val_acc: 0.96000
    Epoch [6700/10000], loss: 0.24370 acc: 0.90667 val_loss: 0.22748, val_acc: 0.96000
    Epoch [6710/10000], loss: 0.24359 acc: 0.90667 val_loss: 0.22736, val_acc: 0.96000
    Epoch [6720/10000], loss: 0.24347 acc: 0.90667 val_loss: 0.22724, val_acc: 0.96000
    Epoch [6730/10000], loss: 0.24335 acc: 0.90667 val_loss: 0.22711, val_acc: 0.96000
    Epoch [6740/10000], loss: 0.24324 acc: 0.90667 val_loss: 0.22699, val_acc: 0.96000
    Epoch [6750/10000], loss: 0.24312 acc: 0.90667 val_loss: 0.22687, val_acc: 0.96000
    Epoch [6760/10000], loss: 0.24300 acc: 0.90667 val_loss: 0.22675, val_acc: 0.96000
    Epoch [6770/10000], loss: 0.24289 acc: 0.90667 val_loss: 0.22663, val_acc: 0.96000
    Epoch [6780/10000], loss: 0.24277 acc: 0.90667 val_loss: 0.22651, val_acc: 0.96000
    Epoch [6790/10000], loss: 0.24266 acc: 0.90667 val_loss: 0.22638, val_acc: 0.96000
    Epoch [6800/10000], loss: 0.24254 acc: 0.90667 val_loss: 0.22626, val_acc: 0.96000
    Epoch [6810/10000], loss: 0.24243 acc: 0.90667 val_loss: 0.22614, val_acc: 0.96000
    Epoch [6820/10000], loss: 0.24231 acc: 0.90667 val_loss: 0.22602, val_acc: 0.96000
    Epoch [6830/10000], loss: 0.24220 acc: 0.90667 val_loss: 0.22590, val_acc: 0.96000
    Epoch [6840/10000], loss: 0.24208 acc: 0.90667 val_loss: 0.22578, val_acc: 0.96000
    Epoch [6850/10000], loss: 0.24197 acc: 0.90667 val_loss: 0.22566, val_acc: 0.96000
    Epoch [6860/10000], loss: 0.24186 acc: 0.90667 val_loss: 0.22555, val_acc: 0.96000
    Epoch [6870/10000], loss: 0.24174 acc: 0.90667 val_loss: 0.22543, val_acc: 0.96000
    Epoch [6880/10000], loss: 0.24163 acc: 0.90667 val_loss: 0.22531, val_acc: 0.96000
    Epoch [6890/10000], loss: 0.24152 acc: 0.90667 val_loss: 0.22519, val_acc: 0.96000
    Epoch [6900/10000], loss: 0.24141 acc: 0.90667 val_loss: 0.22507, val_acc: 0.96000
    Epoch [6910/10000], loss: 0.24129 acc: 0.90667 val_loss: 0.22495, val_acc: 0.96000
    Epoch [6920/10000], loss: 0.24118 acc: 0.90667 val_loss: 0.22484, val_acc: 0.96000
    Epoch [6930/10000], loss: 0.24107 acc: 0.90667 val_loss: 0.22472, val_acc: 0.96000
    Epoch [6940/10000], loss: 0.24096 acc: 0.90667 val_loss: 0.22460, val_acc: 0.96000
    Epoch [6950/10000], loss: 0.24085 acc: 0.90667 val_loss: 0.22449, val_acc: 0.96000
    Epoch [6960/10000], loss: 0.24074 acc: 0.90667 val_loss: 0.22437, val_acc: 0.96000
    Epoch [6970/10000], loss: 0.24063 acc: 0.90667 val_loss: 0.22425, val_acc: 0.96000
    Epoch [6980/10000], loss: 0.24052 acc: 0.90667 val_loss: 0.22414, val_acc: 0.96000
    Epoch [6990/10000], loss: 0.24041 acc: 0.90667 val_loss: 0.22402, val_acc: 0.96000
    Epoch [7000/10000], loss: 0.24030 acc: 0.90667 val_loss: 0.22391, val_acc: 0.96000
    Epoch [7010/10000], loss: 0.24019 acc: 0.90667 val_loss: 0.22379, val_acc: 0.96000
    Epoch [7020/10000], loss: 0.24008 acc: 0.90667 val_loss: 0.22368, val_acc: 0.96000
    Epoch [7030/10000], loss: 0.23997 acc: 0.90667 val_loss: 0.22356, val_acc: 0.96000
    Epoch [7040/10000], loss: 0.23986 acc: 0.90667 val_loss: 0.22345, val_acc: 0.96000
    Epoch [7050/10000], loss: 0.23975 acc: 0.90667 val_loss: 0.22333, val_acc: 0.96000
    Epoch [7060/10000], loss: 0.23964 acc: 0.90667 val_loss: 0.22322, val_acc: 0.96000
    Epoch [7070/10000], loss: 0.23953 acc: 0.90667 val_loss: 0.22311, val_acc: 0.96000
    Epoch [7080/10000], loss: 0.23943 acc: 0.90667 val_loss: 0.22299, val_acc: 0.96000
    Epoch [7090/10000], loss: 0.23932 acc: 0.90667 val_loss: 0.22288, val_acc: 0.96000
    Epoch [7100/10000], loss: 0.23921 acc: 0.90667 val_loss: 0.22277, val_acc: 0.96000
    Epoch [7110/10000], loss: 0.23910 acc: 0.90667 val_loss: 0.22265, val_acc: 0.96000
    Epoch [7120/10000], loss: 0.23900 acc: 0.90667 val_loss: 0.22254, val_acc: 0.96000
    Epoch [7130/10000], loss: 0.23889 acc: 0.90667 val_loss: 0.22243, val_acc: 0.96000
    Epoch [7140/10000], loss: 0.23879 acc: 0.90667 val_loss: 0.22232, val_acc: 0.96000
    Epoch [7150/10000], loss: 0.23868 acc: 0.90667 val_loss: 0.22221, val_acc: 0.96000
    Epoch [7160/10000], loss: 0.23857 acc: 0.90667 val_loss: 0.22209, val_acc: 0.96000
    Epoch [7170/10000], loss: 0.23847 acc: 0.90667 val_loss: 0.22198, val_acc: 0.96000
    Epoch [7180/10000], loss: 0.23836 acc: 0.90667 val_loss: 0.22187, val_acc: 0.96000
    Epoch [7190/10000], loss: 0.23826 acc: 0.90667 val_loss: 0.22176, val_acc: 0.96000
    Epoch [7200/10000], loss: 0.23815 acc: 0.90667 val_loss: 0.22165, val_acc: 0.96000
    Epoch [7210/10000], loss: 0.23805 acc: 0.90667 val_loss: 0.22154, val_acc: 0.96000
    Epoch [7220/10000], loss: 0.23794 acc: 0.90667 val_loss: 0.22143, val_acc: 0.96000
    Epoch [7230/10000], loss: 0.23784 acc: 0.90667 val_loss: 0.22132, val_acc: 0.96000
    Epoch [7240/10000], loss: 0.23774 acc: 0.90667 val_loss: 0.22121, val_acc: 0.96000
    Epoch [7250/10000], loss: 0.23763 acc: 0.90667 val_loss: 0.22110, val_acc: 0.96000
    Epoch [7260/10000], loss: 0.23753 acc: 0.90667 val_loss: 0.22099, val_acc: 0.96000
    Epoch [7270/10000], loss: 0.23742 acc: 0.90667 val_loss: 0.22088, val_acc: 0.96000
    Epoch [7280/10000], loss: 0.23732 acc: 0.90667 val_loss: 0.22078, val_acc: 0.96000
    Epoch [7290/10000], loss: 0.23722 acc: 0.90667 val_loss: 0.22067, val_acc: 0.96000
    Epoch [7300/10000], loss: 0.23712 acc: 0.90667 val_loss: 0.22056, val_acc: 0.96000
    Epoch [7310/10000], loss: 0.23701 acc: 0.90667 val_loss: 0.22045, val_acc: 0.96000
    Epoch [7320/10000], loss: 0.23691 acc: 0.90667 val_loss: 0.22034, val_acc: 0.96000
    Epoch [7330/10000], loss: 0.23681 acc: 0.90667 val_loss: 0.22024, val_acc: 0.96000
    Epoch [7340/10000], loss: 0.23671 acc: 0.90667 val_loss: 0.22013, val_acc: 0.96000
    Epoch [7350/10000], loss: 0.23661 acc: 0.90667 val_loss: 0.22002, val_acc: 0.96000
    Epoch [7360/10000], loss: 0.23651 acc: 0.90667 val_loss: 0.21992, val_acc: 0.96000
    Epoch [7370/10000], loss: 0.23640 acc: 0.90667 val_loss: 0.21981, val_acc: 0.96000
    Epoch [7380/10000], loss: 0.23630 acc: 0.90667 val_loss: 0.21970, val_acc: 0.96000
    Epoch [7390/10000], loss: 0.23620 acc: 0.90667 val_loss: 0.21960, val_acc: 0.96000
    Epoch [7400/10000], loss: 0.23610 acc: 0.90667 val_loss: 0.21949, val_acc: 0.96000
    Epoch [7410/10000], loss: 0.23600 acc: 0.90667 val_loss: 0.21939, val_acc: 0.96000
    Epoch [7420/10000], loss: 0.23590 acc: 0.90667 val_loss: 0.21928, val_acc: 0.96000
    Epoch [7430/10000], loss: 0.23580 acc: 0.90667 val_loss: 0.21918, val_acc: 0.96000
    Epoch [7440/10000], loss: 0.23570 acc: 0.90667 val_loss: 0.21907, val_acc: 0.96000
    Epoch [7450/10000], loss: 0.23560 acc: 0.90667 val_loss: 0.21897, val_acc: 0.96000
    Epoch [7460/10000], loss: 0.23551 acc: 0.90667 val_loss: 0.21886, val_acc: 0.96000
    Epoch [7470/10000], loss: 0.23541 acc: 0.90667 val_loss: 0.21876, val_acc: 0.96000
    Epoch [7480/10000], loss: 0.23531 acc: 0.90667 val_loss: 0.21865, val_acc: 0.96000
    Epoch [7490/10000], loss: 0.23521 acc: 0.90667 val_loss: 0.21855, val_acc: 0.96000
    Epoch [7500/10000], loss: 0.23511 acc: 0.90667 val_loss: 0.21845, val_acc: 0.96000
    Epoch [7510/10000], loss: 0.23501 acc: 0.90667 val_loss: 0.21834, val_acc: 0.96000
    Epoch [7520/10000], loss: 0.23492 acc: 0.90667 val_loss: 0.21824, val_acc: 0.96000
    Epoch [7530/10000], loss: 0.23482 acc: 0.90667 val_loss: 0.21814, val_acc: 0.96000
    Epoch [7540/10000], loss: 0.23472 acc: 0.90667 val_loss: 0.21803, val_acc: 0.96000
    Epoch [7550/10000], loss: 0.23462 acc: 0.90667 val_loss: 0.21793, val_acc: 0.96000
    Epoch [7560/10000], loss: 0.23453 acc: 0.90667 val_loss: 0.21783, val_acc: 0.96000
    Epoch [7570/10000], loss: 0.23443 acc: 0.90667 val_loss: 0.21773, val_acc: 0.96000
    Epoch [7580/10000], loss: 0.23433 acc: 0.90667 val_loss: 0.21762, val_acc: 0.96000
    Epoch [7590/10000], loss: 0.23424 acc: 0.90667 val_loss: 0.21752, val_acc: 0.96000
    Epoch [7600/10000], loss: 0.23414 acc: 0.90667 val_loss: 0.21742, val_acc: 0.96000
    Epoch [7610/10000], loss: 0.23405 acc: 0.90667 val_loss: 0.21732, val_acc: 0.96000
    Epoch [7620/10000], loss: 0.23395 acc: 0.90667 val_loss: 0.21722, val_acc: 0.96000
    Epoch [7630/10000], loss: 0.23385 acc: 0.90667 val_loss: 0.21712, val_acc: 0.96000
    Epoch [7640/10000], loss: 0.23376 acc: 0.90667 val_loss: 0.21702, val_acc: 0.96000
    Epoch [7650/10000], loss: 0.23366 acc: 0.90667 val_loss: 0.21692, val_acc: 0.96000
    Epoch [7660/10000], loss: 0.23357 acc: 0.90667 val_loss: 0.21682, val_acc: 0.96000
    Epoch [7670/10000], loss: 0.23348 acc: 0.90667 val_loss: 0.21672, val_acc: 0.96000
    Epoch [7680/10000], loss: 0.23338 acc: 0.90667 val_loss: 0.21662, val_acc: 0.96000
    Epoch [7690/10000], loss: 0.23329 acc: 0.90667 val_loss: 0.21652, val_acc: 0.96000
    Epoch [7700/10000], loss: 0.23319 acc: 0.90667 val_loss: 0.21642, val_acc: 0.96000
    Epoch [7710/10000], loss: 0.23310 acc: 0.90667 val_loss: 0.21632, val_acc: 0.96000
    Epoch [7720/10000], loss: 0.23301 acc: 0.90667 val_loss: 0.21622, val_acc: 0.96000
    Epoch [7730/10000], loss: 0.23291 acc: 0.90667 val_loss: 0.21612, val_acc: 0.96000
    Epoch [7740/10000], loss: 0.23282 acc: 0.90667 val_loss: 0.21602, val_acc: 0.96000
    Epoch [7750/10000], loss: 0.23273 acc: 0.90667 val_loss: 0.21592, val_acc: 0.96000
    Epoch [7760/10000], loss: 0.23263 acc: 0.90667 val_loss: 0.21582, val_acc: 0.96000
    Epoch [7770/10000], loss: 0.23254 acc: 0.90667 val_loss: 0.21573, val_acc: 0.96000
    Epoch [7780/10000], loss: 0.23245 acc: 0.90667 val_loss: 0.21563, val_acc: 0.96000
    Epoch [7790/10000], loss: 0.23236 acc: 0.90667 val_loss: 0.21553, val_acc: 0.96000
    Epoch [7800/10000], loss: 0.23226 acc: 0.90667 val_loss: 0.21543, val_acc: 0.96000
    Epoch [7810/10000], loss: 0.23217 acc: 0.90667 val_loss: 0.21534, val_acc: 0.96000
    Epoch [7820/10000], loss: 0.23208 acc: 0.90667 val_loss: 0.21524, val_acc: 0.96000
    Epoch [7830/10000], loss: 0.23199 acc: 0.90667 val_loss: 0.21514, val_acc: 0.96000
    Epoch [7840/10000], loss: 0.23190 acc: 0.90667 val_loss: 0.21505, val_acc: 0.96000
    Epoch [7850/10000], loss: 0.23181 acc: 0.90667 val_loss: 0.21495, val_acc: 0.96000
    Epoch [7860/10000], loss: 0.23172 acc: 0.90667 val_loss: 0.21485, val_acc: 0.96000
    Epoch [7870/10000], loss: 0.23162 acc: 0.90667 val_loss: 0.21476, val_acc: 0.96000
    Epoch [7880/10000], loss: 0.23153 acc: 0.90667 val_loss: 0.21466, val_acc: 0.96000
    Epoch [7890/10000], loss: 0.23144 acc: 0.90667 val_loss: 0.21457, val_acc: 0.96000
    Epoch [7900/10000], loss: 0.23135 acc: 0.90667 val_loss: 0.21447, val_acc: 0.96000
    Epoch [7910/10000], loss: 0.23126 acc: 0.90667 val_loss: 0.21437, val_acc: 0.96000
    Epoch [7920/10000], loss: 0.23117 acc: 0.90667 val_loss: 0.21428, val_acc: 0.96000
    Epoch [7930/10000], loss: 0.23108 acc: 0.90667 val_loss: 0.21418, val_acc: 0.96000
    Epoch [7940/10000], loss: 0.23099 acc: 0.90667 val_loss: 0.21409, val_acc: 0.96000
    Epoch [7950/10000], loss: 0.23091 acc: 0.90667 val_loss: 0.21400, val_acc: 0.96000
    Epoch [7960/10000], loss: 0.23082 acc: 0.90667 val_loss: 0.21390, val_acc: 0.96000
    Epoch [7970/10000], loss: 0.23073 acc: 0.90667 val_loss: 0.21381, val_acc: 0.96000
    Epoch [7980/10000], loss: 0.23064 acc: 0.90667 val_loss: 0.21371, val_acc: 0.96000
    Epoch [7990/10000], loss: 0.23055 acc: 0.90667 val_loss: 0.21362, val_acc: 0.96000
    Epoch [8000/10000], loss: 0.23046 acc: 0.90667 val_loss: 0.21353, val_acc: 0.96000
    Epoch [8010/10000], loss: 0.23037 acc: 0.90667 val_loss: 0.21343, val_acc: 0.96000
    Epoch [8020/10000], loss: 0.23029 acc: 0.90667 val_loss: 0.21334, val_acc: 0.96000
    Epoch [8030/10000], loss: 0.23020 acc: 0.90667 val_loss: 0.21325, val_acc: 0.96000
    Epoch [8040/10000], loss: 0.23011 acc: 0.90667 val_loss: 0.21315, val_acc: 0.96000
    Epoch [8050/10000], loss: 0.23002 acc: 0.90667 val_loss: 0.21306, val_acc: 0.96000
    Epoch [8060/10000], loss: 0.22994 acc: 0.90667 val_loss: 0.21297, val_acc: 0.96000
    Epoch [8070/10000], loss: 0.22985 acc: 0.90667 val_loss: 0.21288, val_acc: 0.96000
    Epoch [8080/10000], loss: 0.22976 acc: 0.90667 val_loss: 0.21278, val_acc: 0.96000
    Epoch [8090/10000], loss: 0.22968 acc: 0.90667 val_loss: 0.21269, val_acc: 0.96000
    Epoch [8100/10000], loss: 0.22959 acc: 0.90667 val_loss: 0.21260, val_acc: 0.96000
    Epoch [8110/10000], loss: 0.22950 acc: 0.90667 val_loss: 0.21251, val_acc: 0.96000
    Epoch [8120/10000], loss: 0.22942 acc: 0.90667 val_loss: 0.21242, val_acc: 0.96000
    Epoch [8130/10000], loss: 0.22933 acc: 0.90667 val_loss: 0.21233, val_acc: 0.96000
    Epoch [8140/10000], loss: 0.22925 acc: 0.90667 val_loss: 0.21223, val_acc: 0.96000
    Epoch [8150/10000], loss: 0.22916 acc: 0.90667 val_loss: 0.21214, val_acc: 0.96000
    Epoch [8160/10000], loss: 0.22907 acc: 0.90667 val_loss: 0.21205, val_acc: 0.96000
    Epoch [8170/10000], loss: 0.22899 acc: 0.90667 val_loss: 0.21196, val_acc: 0.96000
    Epoch [8180/10000], loss: 0.22890 acc: 0.90667 val_loss: 0.21187, val_acc: 0.96000
    Epoch [8190/10000], loss: 0.22882 acc: 0.90667 val_loss: 0.21178, val_acc: 0.96000
    Epoch [8200/10000], loss: 0.22873 acc: 0.90667 val_loss: 0.21169, val_acc: 0.96000
    Epoch [8210/10000], loss: 0.22865 acc: 0.90667 val_loss: 0.21160, val_acc: 0.96000
    Epoch [8220/10000], loss: 0.22857 acc: 0.90667 val_loss: 0.21151, val_acc: 0.96000
    Epoch [8230/10000], loss: 0.22848 acc: 0.90667 val_loss: 0.21142, val_acc: 0.96000
    Epoch [8240/10000], loss: 0.22840 acc: 0.90667 val_loss: 0.21133, val_acc: 0.96000
    Epoch [8250/10000], loss: 0.22831 acc: 0.90667 val_loss: 0.21124, val_acc: 0.96000
    Epoch [8260/10000], loss: 0.22823 acc: 0.90667 val_loss: 0.21115, val_acc: 0.96000
    Epoch [8270/10000], loss: 0.22815 acc: 0.90667 val_loss: 0.21107, val_acc: 0.96000
    Epoch [8280/10000], loss: 0.22806 acc: 0.90667 val_loss: 0.21098, val_acc: 0.96000
    Epoch [8290/10000], loss: 0.22798 acc: 0.90667 val_loss: 0.21089, val_acc: 0.96000
    Epoch [8300/10000], loss: 0.22790 acc: 0.90667 val_loss: 0.21080, val_acc: 0.96000
    Epoch [8310/10000], loss: 0.22781 acc: 0.90667 val_loss: 0.21071, val_acc: 0.96000
    Epoch [8320/10000], loss: 0.22773 acc: 0.90667 val_loss: 0.21062, val_acc: 0.96000
    Epoch [8330/10000], loss: 0.22765 acc: 0.90667 val_loss: 0.21054, val_acc: 0.96000
    Epoch [8340/10000], loss: 0.22757 acc: 0.90667 val_loss: 0.21045, val_acc: 0.96000
    Epoch [8350/10000], loss: 0.22748 acc: 0.90667 val_loss: 0.21036, val_acc: 0.96000
    Epoch [8360/10000], loss: 0.22740 acc: 0.90667 val_loss: 0.21027, val_acc: 0.96000
    Epoch [8370/10000], loss: 0.22732 acc: 0.90667 val_loss: 0.21019, val_acc: 0.96000
    Epoch [8380/10000], loss: 0.22724 acc: 0.90667 val_loss: 0.21010, val_acc: 0.96000
    Epoch [8390/10000], loss: 0.22716 acc: 0.90667 val_loss: 0.21001, val_acc: 0.96000
    Epoch [8400/10000], loss: 0.22708 acc: 0.90667 val_loss: 0.20993, val_acc: 0.96000
    Epoch [8410/10000], loss: 0.22699 acc: 0.90667 val_loss: 0.20984, val_acc: 0.96000
    Epoch [8420/10000], loss: 0.22691 acc: 0.90667 val_loss: 0.20975, val_acc: 0.96000
    Epoch [8430/10000], loss: 0.22683 acc: 0.90667 val_loss: 0.20967, val_acc: 0.96000
    Epoch [8440/10000], loss: 0.22675 acc: 0.90667 val_loss: 0.20958, val_acc: 0.96000
    Epoch [8450/10000], loss: 0.22667 acc: 0.90667 val_loss: 0.20949, val_acc: 0.96000
    Epoch [8460/10000], loss: 0.22659 acc: 0.90667 val_loss: 0.20941, val_acc: 0.96000
    Epoch [8470/10000], loss: 0.22651 acc: 0.90667 val_loss: 0.20932, val_acc: 0.96000
    Epoch [8480/10000], loss: 0.22643 acc: 0.90667 val_loss: 0.20924, val_acc: 0.96000
    Epoch [8490/10000], loss: 0.22635 acc: 0.90667 val_loss: 0.20915, val_acc: 0.96000
    Epoch [8500/10000], loss: 0.22627 acc: 0.90667 val_loss: 0.20907, val_acc: 0.96000
    Epoch [8510/10000], loss: 0.22619 acc: 0.90667 val_loss: 0.20898, val_acc: 0.96000
    Epoch [8520/10000], loss: 0.22611 acc: 0.90667 val_loss: 0.20890, val_acc: 0.96000
    Epoch [8530/10000], loss: 0.22603 acc: 0.90667 val_loss: 0.20881, val_acc: 0.96000
    Epoch [8540/10000], loss: 0.22595 acc: 0.90667 val_loss: 0.20873, val_acc: 0.96000
    Epoch [8550/10000], loss: 0.22587 acc: 0.90667 val_loss: 0.20865, val_acc: 0.96000
    Epoch [8560/10000], loss: 0.22579 acc: 0.90667 val_loss: 0.20856, val_acc: 0.96000
    Epoch [8570/10000], loss: 0.22572 acc: 0.90667 val_loss: 0.20848, val_acc: 0.96000
    Epoch [8580/10000], loss: 0.22564 acc: 0.90667 val_loss: 0.20839, val_acc: 0.96000
    Epoch [8590/10000], loss: 0.22556 acc: 0.90667 val_loss: 0.20831, val_acc: 0.96000
    Epoch [8600/10000], loss: 0.22548 acc: 0.90667 val_loss: 0.20823, val_acc: 0.96000
    Epoch [8610/10000], loss: 0.22540 acc: 0.90667 val_loss: 0.20814, val_acc: 0.96000
    Epoch [8620/10000], loss: 0.22532 acc: 0.90667 val_loss: 0.20806, val_acc: 0.96000
    Epoch [8630/10000], loss: 0.22525 acc: 0.90667 val_loss: 0.20798, val_acc: 0.96000
    Epoch [8640/10000], loss: 0.22517 acc: 0.90667 val_loss: 0.20789, val_acc: 0.96000
    Epoch [8650/10000], loss: 0.22509 acc: 0.90667 val_loss: 0.20781, val_acc: 0.96000
    Epoch [8660/10000], loss: 0.22501 acc: 0.90667 val_loss: 0.20773, val_acc: 0.96000
    Epoch [8670/10000], loss: 0.22494 acc: 0.90667 val_loss: 0.20765, val_acc: 0.96000
    Epoch [8680/10000], loss: 0.22486 acc: 0.90667 val_loss: 0.20756, val_acc: 0.96000
    Epoch [8690/10000], loss: 0.22478 acc: 0.90667 val_loss: 0.20748, val_acc: 0.96000
    Epoch [8700/10000], loss: 0.22471 acc: 0.90667 val_loss: 0.20740, val_acc: 0.96000
    Epoch [8710/10000], loss: 0.22463 acc: 0.90667 val_loss: 0.20732, val_acc: 0.96000
    Epoch [8720/10000], loss: 0.22455 acc: 0.90667 val_loss: 0.20724, val_acc: 0.96000
    Epoch [8730/10000], loss: 0.22448 acc: 0.90667 val_loss: 0.20716, val_acc: 0.96000
    Epoch [8740/10000], loss: 0.22440 acc: 0.90667 val_loss: 0.20707, val_acc: 0.96000
    Epoch [8750/10000], loss: 0.22432 acc: 0.90667 val_loss: 0.20699, val_acc: 0.96000
    Epoch [8760/10000], loss: 0.22425 acc: 0.90667 val_loss: 0.20691, val_acc: 0.96000
    Epoch [8770/10000], loss: 0.22417 acc: 0.90667 val_loss: 0.20683, val_acc: 0.96000
    Epoch [8780/10000], loss: 0.22410 acc: 0.90667 val_loss: 0.20675, val_acc: 0.96000
    Epoch [8790/10000], loss: 0.22402 acc: 0.90667 val_loss: 0.20667, val_acc: 0.96000
    Epoch [8800/10000], loss: 0.22395 acc: 0.90667 val_loss: 0.20659, val_acc: 0.96000
    Epoch [8810/10000], loss: 0.22387 acc: 0.90667 val_loss: 0.20651, val_acc: 0.96000
    Epoch [8820/10000], loss: 0.22380 acc: 0.90667 val_loss: 0.20643, val_acc: 0.96000
    Epoch [8830/10000], loss: 0.22372 acc: 0.90667 val_loss: 0.20635, val_acc: 0.96000
    Epoch [8840/10000], loss: 0.22365 acc: 0.90667 val_loss: 0.20627, val_acc: 0.96000
    Epoch [8850/10000], loss: 0.22357 acc: 0.90667 val_loss: 0.20619, val_acc: 0.96000
    Epoch [8860/10000], loss: 0.22350 acc: 0.90667 val_loss: 0.20611, val_acc: 0.96000
    Epoch [8870/10000], loss: 0.22342 acc: 0.90667 val_loss: 0.20603, val_acc: 0.96000
    Epoch [8880/10000], loss: 0.22335 acc: 0.90667 val_loss: 0.20595, val_acc: 0.96000
    Epoch [8890/10000], loss: 0.22327 acc: 0.90667 val_loss: 0.20587, val_acc: 0.96000
    Epoch [8900/10000], loss: 0.22320 acc: 0.90667 val_loss: 0.20579, val_acc: 0.96000
    Epoch [8910/10000], loss: 0.22313 acc: 0.90667 val_loss: 0.20571, val_acc: 0.96000
    Epoch [8920/10000], loss: 0.22305 acc: 0.90667 val_loss: 0.20563, val_acc: 0.96000
    Epoch [8930/10000], loss: 0.22298 acc: 0.90667 val_loss: 0.20556, val_acc: 0.96000
    Epoch [8940/10000], loss: 0.22291 acc: 0.90667 val_loss: 0.20548, val_acc: 0.96000
    Epoch [8950/10000], loss: 0.22283 acc: 0.90667 val_loss: 0.20540, val_acc: 0.96000
    Epoch [8960/10000], loss: 0.22276 acc: 0.90667 val_loss: 0.20532, val_acc: 0.96000
    Epoch [8970/10000], loss: 0.22269 acc: 0.90667 val_loss: 0.20524, val_acc: 0.96000
    Epoch [8980/10000], loss: 0.22261 acc: 0.90667 val_loss: 0.20517, val_acc: 0.96000
    Epoch [8990/10000], loss: 0.22254 acc: 0.90667 val_loss: 0.20509, val_acc: 0.96000
    Epoch [9000/10000], loss: 0.22247 acc: 0.90667 val_loss: 0.20501, val_acc: 0.96000
    Epoch [9010/10000], loss: 0.22240 acc: 0.90667 val_loss: 0.20493, val_acc: 0.96000
    Epoch [9020/10000], loss: 0.22232 acc: 0.90667 val_loss: 0.20485, val_acc: 0.96000
    Epoch [9030/10000], loss: 0.22225 acc: 0.90667 val_loss: 0.20478, val_acc: 0.96000
    Epoch [9040/10000], loss: 0.22218 acc: 0.90667 val_loss: 0.20470, val_acc: 0.96000
    Epoch [9050/10000], loss: 0.22211 acc: 0.90667 val_loss: 0.20462, val_acc: 0.96000
    Epoch [9060/10000], loss: 0.22204 acc: 0.90667 val_loss: 0.20455, val_acc: 0.96000
    Epoch [9070/10000], loss: 0.22196 acc: 0.90667 val_loss: 0.20447, val_acc: 0.96000
    Epoch [9080/10000], loss: 0.22189 acc: 0.90667 val_loss: 0.20439, val_acc: 0.96000
    Epoch [9090/10000], loss: 0.22182 acc: 0.90667 val_loss: 0.20432, val_acc: 0.96000
    Epoch [9100/10000], loss: 0.22175 acc: 0.90667 val_loss: 0.20424, val_acc: 0.96000
    Epoch [9110/10000], loss: 0.22168 acc: 0.90667 val_loss: 0.20416, val_acc: 0.96000
    Epoch [9120/10000], loss: 0.22161 acc: 0.90667 val_loss: 0.20409, val_acc: 0.96000
    Epoch [9130/10000], loss: 0.22154 acc: 0.90667 val_loss: 0.20401, val_acc: 0.96000
    Epoch [9140/10000], loss: 0.22147 acc: 0.90667 val_loss: 0.20394, val_acc: 0.96000
    Epoch [9150/10000], loss: 0.22140 acc: 0.90667 val_loss: 0.20386, val_acc: 0.96000
    Epoch [9160/10000], loss: 0.22133 acc: 0.90667 val_loss: 0.20379, val_acc: 0.96000
    Epoch [9170/10000], loss: 0.22126 acc: 0.90667 val_loss: 0.20371, val_acc: 0.96000
    Epoch [9180/10000], loss: 0.22118 acc: 0.90667 val_loss: 0.20364, val_acc: 0.96000
    Epoch [9190/10000], loss: 0.22111 acc: 0.90667 val_loss: 0.20356, val_acc: 0.96000
    Epoch [9200/10000], loss: 0.22105 acc: 0.90667 val_loss: 0.20349, val_acc: 0.96000
    Epoch [9210/10000], loss: 0.22098 acc: 0.90667 val_loss: 0.20341, val_acc: 0.96000
    Epoch [9220/10000], loss: 0.22091 acc: 0.90667 val_loss: 0.20334, val_acc: 0.96000
    Epoch [9230/10000], loss: 0.22084 acc: 0.90667 val_loss: 0.20326, val_acc: 0.96000
    Epoch [9240/10000], loss: 0.22077 acc: 0.90667 val_loss: 0.20319, val_acc: 0.96000
    Epoch [9250/10000], loss: 0.22070 acc: 0.90667 val_loss: 0.20311, val_acc: 0.96000
    Epoch [9260/10000], loss: 0.22063 acc: 0.90667 val_loss: 0.20304, val_acc: 0.96000
    Epoch [9270/10000], loss: 0.22056 acc: 0.90667 val_loss: 0.20296, val_acc: 0.96000
    Epoch [9280/10000], loss: 0.22049 acc: 0.90667 val_loss: 0.20289, val_acc: 0.96000
    Epoch [9290/10000], loss: 0.22042 acc: 0.90667 val_loss: 0.20282, val_acc: 0.96000
    Epoch [9300/10000], loss: 0.22035 acc: 0.90667 val_loss: 0.20274, val_acc: 0.96000
    Epoch [9310/10000], loss: 0.22028 acc: 0.90667 val_loss: 0.20267, val_acc: 0.96000
    Epoch [9320/10000], loss: 0.22022 acc: 0.90667 val_loss: 0.20260, val_acc: 0.96000
    Epoch [9330/10000], loss: 0.22015 acc: 0.90667 val_loss: 0.20252, val_acc: 0.96000
    Epoch [9340/10000], loss: 0.22008 acc: 0.90667 val_loss: 0.20245, val_acc: 0.96000
    Epoch [9350/10000], loss: 0.22001 acc: 0.90667 val_loss: 0.20238, val_acc: 0.96000
    Epoch [9360/10000], loss: 0.21994 acc: 0.90667 val_loss: 0.20230, val_acc: 0.96000
    Epoch [9370/10000], loss: 0.21988 acc: 0.90667 val_loss: 0.20223, val_acc: 0.96000
    Epoch [9380/10000], loss: 0.21981 acc: 0.90667 val_loss: 0.20216, val_acc: 0.96000
    Epoch [9390/10000], loss: 0.21974 acc: 0.90667 val_loss: 0.20209, val_acc: 0.96000
    Epoch [9400/10000], loss: 0.21967 acc: 0.90667 val_loss: 0.20201, val_acc: 0.96000
    Epoch [9410/10000], loss: 0.21961 acc: 0.90667 val_loss: 0.20194, val_acc: 0.96000
    Epoch [9420/10000], loss: 0.21954 acc: 0.90667 val_loss: 0.20187, val_acc: 0.96000
    Epoch [9430/10000], loss: 0.21947 acc: 0.90667 val_loss: 0.20180, val_acc: 0.96000
    Epoch [9440/10000], loss: 0.21940 acc: 0.90667 val_loss: 0.20173, val_acc: 0.96000
    Epoch [9450/10000], loss: 0.21934 acc: 0.90667 val_loss: 0.20165, val_acc: 0.96000
    Epoch [9460/10000], loss: 0.21927 acc: 0.90667 val_loss: 0.20158, val_acc: 0.96000
    Epoch [9470/10000], loss: 0.21920 acc: 0.90667 val_loss: 0.20151, val_acc: 0.96000
    Epoch [9480/10000], loss: 0.21914 acc: 0.90667 val_loss: 0.20144, val_acc: 0.96000
    Epoch [9490/10000], loss: 0.21907 acc: 0.90667 val_loss: 0.20137, val_acc: 0.96000
    Epoch [9500/10000], loss: 0.21901 acc: 0.90667 val_loss: 0.20130, val_acc: 0.96000
    Epoch [9510/10000], loss: 0.21894 acc: 0.90667 val_loss: 0.20123, val_acc: 0.96000
    Epoch [9520/10000], loss: 0.21887 acc: 0.90667 val_loss: 0.20115, val_acc: 0.96000
    Epoch [9530/10000], loss: 0.21881 acc: 0.90667 val_loss: 0.20108, val_acc: 0.96000
    Epoch [9540/10000], loss: 0.21874 acc: 0.90667 val_loss: 0.20101, val_acc: 0.96000
    Epoch [9550/10000], loss: 0.21868 acc: 0.90667 val_loss: 0.20094, val_acc: 0.96000
    Epoch [9560/10000], loss: 0.21861 acc: 0.90667 val_loss: 0.20087, val_acc: 0.96000
    Epoch [9570/10000], loss: 0.21854 acc: 0.90667 val_loss: 0.20080, val_acc: 0.96000
    Epoch [9580/10000], loss: 0.21848 acc: 0.90667 val_loss: 0.20073, val_acc: 0.96000
    Epoch [9590/10000], loss: 0.21841 acc: 0.90667 val_loss: 0.20066, val_acc: 0.96000
    Epoch [9600/10000], loss: 0.21835 acc: 0.90667 val_loss: 0.20059, val_acc: 0.96000
    Epoch [9610/10000], loss: 0.21828 acc: 0.90667 val_loss: 0.20052, val_acc: 0.96000
    Epoch [9620/10000], loss: 0.21822 acc: 0.90667 val_loss: 0.20045, val_acc: 0.96000
    Epoch [9630/10000], loss: 0.21815 acc: 0.90667 val_loss: 0.20038, val_acc: 0.96000
    Epoch [9640/10000], loss: 0.21809 acc: 0.90667 val_loss: 0.20031, val_acc: 0.96000
    Epoch [9650/10000], loss: 0.21803 acc: 0.90667 val_loss: 0.20024, val_acc: 0.96000
    Epoch [9660/10000], loss: 0.21796 acc: 0.90667 val_loss: 0.20017, val_acc: 0.96000
    Epoch [9670/10000], loss: 0.21790 acc: 0.90667 val_loss: 0.20010, val_acc: 0.96000
    Epoch [9680/10000], loss: 0.21783 acc: 0.90667 val_loss: 0.20004, val_acc: 0.96000
    Epoch [9690/10000], loss: 0.21777 acc: 0.90667 val_loss: 0.19997, val_acc: 0.96000
    Epoch [9700/10000], loss: 0.21770 acc: 0.90667 val_loss: 0.19990, val_acc: 0.96000
    Epoch [9710/10000], loss: 0.21764 acc: 0.90667 val_loss: 0.19983, val_acc: 0.96000
    Epoch [9720/10000], loss: 0.21758 acc: 0.90667 val_loss: 0.19976, val_acc: 0.96000
    Epoch [9730/10000], loss: 0.21751 acc: 0.90667 val_loss: 0.19969, val_acc: 0.96000
    Epoch [9740/10000], loss: 0.21745 acc: 0.90667 val_loss: 0.19962, val_acc: 0.96000
    Epoch [9750/10000], loss: 0.21739 acc: 0.90667 val_loss: 0.19956, val_acc: 0.96000
    Epoch [9760/10000], loss: 0.21732 acc: 0.90667 val_loss: 0.19949, val_acc: 0.96000
    Epoch [9770/10000], loss: 0.21726 acc: 0.90667 val_loss: 0.19942, val_acc: 0.96000
    Epoch [9780/10000], loss: 0.21720 acc: 0.90667 val_loss: 0.19935, val_acc: 0.96000
    Epoch [9790/10000], loss: 0.21713 acc: 0.90667 val_loss: 0.19928, val_acc: 0.96000
    Epoch [9800/10000], loss: 0.21707 acc: 0.90667 val_loss: 0.19922, val_acc: 0.96000
    Epoch [9810/10000], loss: 0.21701 acc: 0.90667 val_loss: 0.19915, val_acc: 0.96000
    Epoch [9820/10000], loss: 0.21695 acc: 0.90667 val_loss: 0.19908, val_acc: 0.96000
    Epoch [9830/10000], loss: 0.21688 acc: 0.90667 val_loss: 0.19901, val_acc: 0.96000
    Epoch [9840/10000], loss: 0.21682 acc: 0.90667 val_loss: 0.19895, val_acc: 0.96000
    Epoch [9850/10000], loss: 0.21676 acc: 0.90667 val_loss: 0.19888, val_acc: 0.96000
    Epoch [9860/10000], loss: 0.21670 acc: 0.90667 val_loss: 0.19881, val_acc: 0.96000
    Epoch [9870/10000], loss: 0.21663 acc: 0.90667 val_loss: 0.19874, val_acc: 0.96000
    Epoch [9880/10000], loss: 0.21657 acc: 0.90667 val_loss: 0.19868, val_acc: 0.96000
    Epoch [9890/10000], loss: 0.21651 acc: 0.90667 val_loss: 0.19861, val_acc: 0.96000
    Epoch [9900/10000], loss: 0.21645 acc: 0.90667 val_loss: 0.19854, val_acc: 0.96000
    Epoch [9910/10000], loss: 0.21639 acc: 0.90667 val_loss: 0.19848, val_acc: 0.96000
    Epoch [9920/10000], loss: 0.21633 acc: 0.90667 val_loss: 0.19841, val_acc: 0.96000
    Epoch [9930/10000], loss: 0.21626 acc: 0.90667 val_loss: 0.19835, val_acc: 0.96000
    Epoch [9940/10000], loss: 0.21620 acc: 0.90667 val_loss: 0.19828, val_acc: 0.96000
    Epoch [9950/10000], loss: 0.21614 acc: 0.90667 val_loss: 0.19821, val_acc: 0.96000
    Epoch [9960/10000], loss: 0.21608 acc: 0.90667 val_loss: 0.19815, val_acc: 0.96000
    Epoch [9970/10000], loss: 0.21602 acc: 0.90667 val_loss: 0.19808, val_acc: 0.96000
    Epoch [9980/10000], loss: 0.21596 acc: 0.90667 val_loss: 0.19802, val_acc: 0.96000
    Epoch [9990/10000], loss: 0.21590 acc: 0.90667 val_loss: 0.19795, val_acc: 0.96000


### 결과 확인


```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기상태 : 손실 : 1.09263  정확도 : 0.26667
    최종상태 : 손실 : 0.19795  정확도 : 0.96000



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b', label='훈련')
plt.plot(history[:,0], history[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__40_0.webp)
    


### 모델 출력 확인


```python
# 정답 데이터의 0번째, 2번째, 3번째를 추출

print(labels[[0,2,3]])

# 이에 해당하는 입력값을 추출
print("="*50)
i3 = inputs[[0,2,3],:]
print(i3.data.numpy())
```

    tensor([1, 0, 2])
    ==================================================
    [[6.3 4.7]
     [5.  1.6]
     [6.4 5.6]]



```python
# 출력값에 소프트맥스 함수를 적용한 결과를 취득

softmax = torch.nn.Softmax(dim=1)
o3 = net(i3)
k3 = softmax(o3)
print(o3.data.numpy())
print(k3.data.numpy())
```

    [[ 8.8071 14.1937 12.9986]
     [12.8262  9.8     0.1734]
     [ 6.7954 15.0928 17.1111]]
    [[0.0035 0.765  0.2315]
     [0.9537 0.0463 0.    ]
     [0.     0.1173 0.8827]]


### 가중치 행렬과 바이어스 값


```python
# 가중치 행렬
print(net.l1.weight.data)

# 바이어스
print(net.l1.bias.data)
```

    tensor([[ 3.0452, -2.5735],
            [ 1.3573,  0.8481],
            [-1.4026,  4.7253]])
    tensor([ 1.7178,  1.6563, -0.3741])


### 입력 변수 4개 사용하기


```python
# 훈련 데이터와 검증 데이터로 분할(셔플도 동시에 실시함)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x_org, y_org, train_size=75, test_size=75,
    random_state=123)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# 입력 차원수
n_input = x_train.shape[1]
```

    (75, 4) (75, 4) (75,) (75,)



```python
print('입력 데이터(x)')
print(x_train[:5,:])
print(f'입력 차원수: {n_input}')
```

    입력 데이터(x)
    [[6.3 3.3 4.7 1.6]
     [7.  3.2 4.7 1.4]
     [5.  3.  1.6 0.2]
     [6.4 2.8 5.6 2.1]
     [6.3 2.5 5.  1.9]]
    입력 차원수: 4



```python
# 입력 데이터 x_train과 정답 데이터 y_train의 텐서 변수화
inputs = torch.tensor(x_train).float()
labels = torch.tensor(y_train).long()

# 검증용 데이터의 텐서 변수화
inputs_test = torch.tensor(x_test).float()
labels_test = torch.tensor(y_test).long()
```


```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 알고리즘: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 평가 결과 기록
history = np.zeros((0,5))
```


```python
for epoch in range(num_epochs):

    # 훈련 페이즈

    # 경사 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 예측 라벨 산출
    predicted = torch.max(outputs, 1)[1]

    # 손실과 정확도 계산
    train_loss = loss.item()
    train_acc = (predicted == labels).sum()  / len(labels)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 손실 계산
    loss_test = criterion(outputs_test, labels_test)

    # 예측 라벨 산출
    predicted_test = torch.max(outputs_test, 1)[1]

    # 손실과 정확도 계산
    val_loss =  loss_test.item()
    val_acc =  (predicted_test == labels_test).sum() / len(labels_test)

    if ( epoch % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch , train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```

    Epoch [0/10000], loss: 1.09861 acc: 0.30667 val_loss: 1.09158, val_acc: 0.26667
    Epoch [10/10000], loss: 1.01848 acc: 0.40000 val_loss: 1.04171, val_acc: 0.26667
    Epoch [20/10000], loss: 0.96854 acc: 0.40000 val_loss: 0.98850, val_acc: 0.26667
    Epoch [30/10000], loss: 0.92459 acc: 0.65333 val_loss: 0.93996, val_acc: 0.57333
    Epoch [40/10000], loss: 0.88568 acc: 0.70667 val_loss: 0.89704, val_acc: 0.62667
    Epoch [50/10000], loss: 0.85120 acc: 0.70667 val_loss: 0.85918, val_acc: 0.62667
    Epoch [60/10000], loss: 0.82059 acc: 0.70667 val_loss: 0.82572, val_acc: 0.62667
    Epoch [70/10000], loss: 0.79335 acc: 0.72000 val_loss: 0.79607, val_acc: 0.62667
    Epoch [80/10000], loss: 0.76900 acc: 0.72000 val_loss: 0.76968, val_acc: 0.65333
    Epoch [90/10000], loss: 0.74717 acc: 0.72000 val_loss: 0.74610, val_acc: 0.65333
    Epoch [100/10000], loss: 0.72750 acc: 0.76000 val_loss: 0.72494, val_acc: 0.69333
    Epoch [110/10000], loss: 0.70970 acc: 0.77333 val_loss: 0.70585, val_acc: 0.74667
    Epoch [120/10000], loss: 0.69354 acc: 0.81333 val_loss: 0.68856, val_acc: 0.76000
    Epoch [130/10000], loss: 0.67878 acc: 0.84000 val_loss: 0.67283, val_acc: 0.76000
    Epoch [140/10000], loss: 0.66526 acc: 0.84000 val_loss: 0.65846, val_acc: 0.78667
    Epoch [150/10000], loss: 0.65283 acc: 0.86667 val_loss: 0.64528, val_acc: 0.78667
    Epoch [160/10000], loss: 0.64135 acc: 0.88000 val_loss: 0.63313, val_acc: 0.78667
    Epoch [170/10000], loss: 0.63070 acc: 0.89333 val_loss: 0.62190, val_acc: 0.81333
    Epoch [180/10000], loss: 0.62081 acc: 0.90667 val_loss: 0.61149, val_acc: 0.81333
    Epoch [190/10000], loss: 0.61157 acc: 0.90667 val_loss: 0.60179, val_acc: 0.84000
    Epoch [200/10000], loss: 0.60292 acc: 0.90667 val_loss: 0.59273, val_acc: 0.84000
    Epoch [210/10000], loss: 0.59481 acc: 0.90667 val_loss: 0.58425, val_acc: 0.88000
    Epoch [220/10000], loss: 0.58717 acc: 0.93333 val_loss: 0.57628, val_acc: 0.88000
    Epoch [230/10000], loss: 0.57996 acc: 0.93333 val_loss: 0.56877, val_acc: 0.89333
    Epoch [240/10000], loss: 0.57313 acc: 0.93333 val_loss: 0.56169, val_acc: 0.90667
    Epoch [250/10000], loss: 0.56666 acc: 0.93333 val_loss: 0.55498, val_acc: 0.90667
    Epoch [260/10000], loss: 0.56051 acc: 0.92000 val_loss: 0.54862, val_acc: 0.90667
    Epoch [270/10000], loss: 0.55465 acc: 0.92000 val_loss: 0.54257, val_acc: 0.90667
    Epoch [280/10000], loss: 0.54906 acc: 0.92000 val_loss: 0.53681, val_acc: 0.90667
    Epoch [290/10000], loss: 0.54371 acc: 0.92000 val_loss: 0.53131, val_acc: 0.90667
    Epoch [300/10000], loss: 0.53859 acc: 0.93333 val_loss: 0.52605, val_acc: 0.90667
    Epoch [310/10000], loss: 0.53368 acc: 0.93333 val_loss: 0.52102, val_acc: 0.90667
    Epoch [320/10000], loss: 0.52896 acc: 0.93333 val_loss: 0.51619, val_acc: 0.90667
    Epoch [330/10000], loss: 0.52442 acc: 0.93333 val_loss: 0.51155, val_acc: 0.90667
    Epoch [340/10000], loss: 0.52004 acc: 0.93333 val_loss: 0.50709, val_acc: 0.90667
    Epoch [350/10000], loss: 0.51582 acc: 0.93333 val_loss: 0.50280, val_acc: 0.90667
    Epoch [360/10000], loss: 0.51173 acc: 0.93333 val_loss: 0.49865, val_acc: 0.90667
    Epoch [370/10000], loss: 0.50779 acc: 0.93333 val_loss: 0.49465, val_acc: 0.90667
    Epoch [380/10000], loss: 0.50397 acc: 0.93333 val_loss: 0.49078, val_acc: 0.90667
    Epoch [390/10000], loss: 0.50026 acc: 0.93333 val_loss: 0.48703, val_acc: 0.90667
    Epoch [400/10000], loss: 0.49666 acc: 0.94667 val_loss: 0.48340, val_acc: 0.90667
    Epoch [410/10000], loss: 0.49317 acc: 0.94667 val_loss: 0.47988, val_acc: 0.90667
    Epoch [420/10000], loss: 0.48978 acc: 0.94667 val_loss: 0.47647, val_acc: 0.90667
    Epoch [430/10000], loss: 0.48647 acc: 0.96000 val_loss: 0.47315, val_acc: 0.90667
    Epoch [440/10000], loss: 0.48326 acc: 0.96000 val_loss: 0.46992, val_acc: 0.90667
    Epoch [450/10000], loss: 0.48012 acc: 0.96000 val_loss: 0.46678, val_acc: 0.90667
    Epoch [460/10000], loss: 0.47706 acc: 0.96000 val_loss: 0.46372, val_acc: 0.90667
    Epoch [470/10000], loss: 0.47408 acc: 0.96000 val_loss: 0.46073, val_acc: 0.90667
    Epoch [480/10000], loss: 0.47116 acc: 0.96000 val_loss: 0.45783, val_acc: 0.90667
    Epoch [490/10000], loss: 0.46831 acc: 0.96000 val_loss: 0.45499, val_acc: 0.90667
    Epoch [500/10000], loss: 0.46553 acc: 0.96000 val_loss: 0.45221, val_acc: 0.90667
    Epoch [510/10000], loss: 0.46280 acc: 0.96000 val_loss: 0.44951, val_acc: 0.90667
    Epoch [520/10000], loss: 0.46013 acc: 0.96000 val_loss: 0.44686, val_acc: 0.90667
    Epoch [530/10000], loss: 0.45752 acc: 0.96000 val_loss: 0.44426, val_acc: 0.90667
    Epoch [540/10000], loss: 0.45496 acc: 0.96000 val_loss: 0.44173, val_acc: 0.90667
    Epoch [550/10000], loss: 0.45245 acc: 0.96000 val_loss: 0.43924, val_acc: 0.90667
    Epoch [560/10000], loss: 0.44998 acc: 0.96000 val_loss: 0.43681, val_acc: 0.90667
    Epoch [570/10000], loss: 0.44757 acc: 0.96000 val_loss: 0.43442, val_acc: 0.90667
    Epoch [580/10000], loss: 0.44519 acc: 0.96000 val_loss: 0.43208, val_acc: 0.90667
    Epoch [590/10000], loss: 0.44286 acc: 0.96000 val_loss: 0.42979, val_acc: 0.92000
    Epoch [600/10000], loss: 0.44057 acc: 0.96000 val_loss: 0.42753, val_acc: 0.92000
    Epoch [610/10000], loss: 0.43832 acc: 0.96000 val_loss: 0.42532, val_acc: 0.92000
    Epoch [620/10000], loss: 0.43611 acc: 0.96000 val_loss: 0.42315, val_acc: 0.92000
    Epoch [630/10000], loss: 0.43393 acc: 0.96000 val_loss: 0.42101, val_acc: 0.92000
    Epoch [640/10000], loss: 0.43179 acc: 0.96000 val_loss: 0.41891, val_acc: 0.92000
    Epoch [650/10000], loss: 0.42968 acc: 0.96000 val_loss: 0.41685, val_acc: 0.92000
    Epoch [660/10000], loss: 0.42761 acc: 0.96000 val_loss: 0.41482, val_acc: 0.92000
    Epoch [670/10000], loss: 0.42556 acc: 0.96000 val_loss: 0.41282, val_acc: 0.92000
    Epoch [680/10000], loss: 0.42355 acc: 0.96000 val_loss: 0.41085, val_acc: 0.92000
    Epoch [690/10000], loss: 0.42157 acc: 0.96000 val_loss: 0.40892, val_acc: 0.92000
    Epoch [700/10000], loss: 0.41961 acc: 0.96000 val_loss: 0.40701, val_acc: 0.92000
    Epoch [710/10000], loss: 0.41768 acc: 0.96000 val_loss: 0.40513, val_acc: 0.92000
    Epoch [720/10000], loss: 0.41578 acc: 0.96000 val_loss: 0.40329, val_acc: 0.92000
    Epoch [730/10000], loss: 0.41391 acc: 0.96000 val_loss: 0.40146, val_acc: 0.92000
    Epoch [740/10000], loss: 0.41206 acc: 0.96000 val_loss: 0.39967, val_acc: 0.92000
    Epoch [750/10000], loss: 0.41024 acc: 0.96000 val_loss: 0.39789, val_acc: 0.92000
    Epoch [760/10000], loss: 0.40844 acc: 0.96000 val_loss: 0.39615, val_acc: 0.92000
    Epoch [770/10000], loss: 0.40666 acc: 0.96000 val_loss: 0.39443, val_acc: 0.93333
    Epoch [780/10000], loss: 0.40491 acc: 0.96000 val_loss: 0.39273, val_acc: 0.93333
    Epoch [790/10000], loss: 0.40317 acc: 0.96000 val_loss: 0.39105, val_acc: 0.93333
    Epoch [800/10000], loss: 0.40146 acc: 0.96000 val_loss: 0.38939, val_acc: 0.93333
    Epoch [810/10000], loss: 0.39977 acc: 0.96000 val_loss: 0.38776, val_acc: 0.93333
    Epoch [820/10000], loss: 0.39810 acc: 0.96000 val_loss: 0.38615, val_acc: 0.93333
    Epoch [830/10000], loss: 0.39646 acc: 0.96000 val_loss: 0.38456, val_acc: 0.93333
    Epoch [840/10000], loss: 0.39483 acc: 0.96000 val_loss: 0.38298, val_acc: 0.93333
    Epoch [850/10000], loss: 0.39321 acc: 0.97333 val_loss: 0.38143, val_acc: 0.94667
    Epoch [860/10000], loss: 0.39162 acc: 0.97333 val_loss: 0.37990, val_acc: 0.94667
    Epoch [870/10000], loss: 0.39005 acc: 0.97333 val_loss: 0.37838, val_acc: 0.94667
    Epoch [880/10000], loss: 0.38849 acc: 0.97333 val_loss: 0.37688, val_acc: 0.94667
    Epoch [890/10000], loss: 0.38695 acc: 0.97333 val_loss: 0.37540, val_acc: 0.94667
    Epoch [900/10000], loss: 0.38543 acc: 0.97333 val_loss: 0.37394, val_acc: 0.94667
    Epoch [910/10000], loss: 0.38392 acc: 0.97333 val_loss: 0.37249, val_acc: 0.94667
    Epoch [920/10000], loss: 0.38243 acc: 0.97333 val_loss: 0.37106, val_acc: 0.94667
    Epoch [930/10000], loss: 0.38096 acc: 0.97333 val_loss: 0.36965, val_acc: 0.94667
    Epoch [940/10000], loss: 0.37950 acc: 0.97333 val_loss: 0.36825, val_acc: 0.94667
    Epoch [950/10000], loss: 0.37806 acc: 0.97333 val_loss: 0.36686, val_acc: 0.94667
    Epoch [960/10000], loss: 0.37663 acc: 0.97333 val_loss: 0.36550, val_acc: 0.96000
    Epoch [970/10000], loss: 0.37522 acc: 0.97333 val_loss: 0.36414, val_acc: 0.96000
    Epoch [980/10000], loss: 0.37382 acc: 0.97333 val_loss: 0.36280, val_acc: 0.96000
    Epoch [990/10000], loss: 0.37243 acc: 0.97333 val_loss: 0.36148, val_acc: 0.96000
    Epoch [1000/10000], loss: 0.37106 acc: 0.97333 val_loss: 0.36017, val_acc: 0.96000
    Epoch [1010/10000], loss: 0.36970 acc: 0.97333 val_loss: 0.35887, val_acc: 0.96000
    Epoch [1020/10000], loss: 0.36836 acc: 0.97333 val_loss: 0.35758, val_acc: 0.96000
    Epoch [1030/10000], loss: 0.36703 acc: 0.97333 val_loss: 0.35631, val_acc: 0.96000
    Epoch [1040/10000], loss: 0.36571 acc: 0.97333 val_loss: 0.35505, val_acc: 0.96000
    Epoch [1050/10000], loss: 0.36440 acc: 0.97333 val_loss: 0.35381, val_acc: 0.96000
    Epoch [1060/10000], loss: 0.36311 acc: 0.97333 val_loss: 0.35258, val_acc: 0.96000
    Epoch [1070/10000], loss: 0.36183 acc: 0.97333 val_loss: 0.35135, val_acc: 0.96000
    Epoch [1080/10000], loss: 0.36056 acc: 0.97333 val_loss: 0.35014, val_acc: 0.96000
    Epoch [1090/10000], loss: 0.35930 acc: 0.97333 val_loss: 0.34895, val_acc: 0.96000
    Epoch [1100/10000], loss: 0.35805 acc: 0.97333 val_loss: 0.34776, val_acc: 0.96000
    Epoch [1110/10000], loss: 0.35682 acc: 0.97333 val_loss: 0.34659, val_acc: 0.96000
    Epoch [1120/10000], loss: 0.35559 acc: 0.97333 val_loss: 0.34542, val_acc: 0.96000
    Epoch [1130/10000], loss: 0.35438 acc: 0.97333 val_loss: 0.34427, val_acc: 0.96000
    Epoch [1140/10000], loss: 0.35318 acc: 0.97333 val_loss: 0.34313, val_acc: 0.96000
    Epoch [1150/10000], loss: 0.35199 acc: 0.97333 val_loss: 0.34199, val_acc: 0.96000
    Epoch [1160/10000], loss: 0.35081 acc: 0.97333 val_loss: 0.34087, val_acc: 0.96000
    Epoch [1170/10000], loss: 0.34964 acc: 0.97333 val_loss: 0.33976, val_acc: 0.96000
    Epoch [1180/10000], loss: 0.34848 acc: 0.97333 val_loss: 0.33866, val_acc: 0.96000
    Epoch [1190/10000], loss: 0.34732 acc: 0.97333 val_loss: 0.33757, val_acc: 0.96000
    Epoch [1200/10000], loss: 0.34618 acc: 0.97333 val_loss: 0.33649, val_acc: 0.96000
    Epoch [1210/10000], loss: 0.34505 acc: 0.97333 val_loss: 0.33542, val_acc: 0.96000
    Epoch [1220/10000], loss: 0.34393 acc: 0.97333 val_loss: 0.33435, val_acc: 0.96000
    Epoch [1230/10000], loss: 0.34282 acc: 0.97333 val_loss: 0.33330, val_acc: 0.96000
    Epoch [1240/10000], loss: 0.34172 acc: 0.97333 val_loss: 0.33226, val_acc: 0.96000
    Epoch [1250/10000], loss: 0.34062 acc: 0.97333 val_loss: 0.33122, val_acc: 0.96000
    Epoch [1260/10000], loss: 0.33954 acc: 0.97333 val_loss: 0.33020, val_acc: 0.96000
    Epoch [1270/10000], loss: 0.33846 acc: 0.97333 val_loss: 0.32918, val_acc: 0.96000
    Epoch [1280/10000], loss: 0.33740 acc: 0.97333 val_loss: 0.32817, val_acc: 0.96000
    Epoch [1290/10000], loss: 0.33634 acc: 0.97333 val_loss: 0.32717, val_acc: 0.96000
    Epoch [1300/10000], loss: 0.33529 acc: 0.97333 val_loss: 0.32618, val_acc: 0.96000
    Epoch [1310/10000], loss: 0.33425 acc: 0.97333 val_loss: 0.32520, val_acc: 0.96000
    Epoch [1320/10000], loss: 0.33321 acc: 0.97333 val_loss: 0.32422, val_acc: 0.96000
    Epoch [1330/10000], loss: 0.33219 acc: 0.97333 val_loss: 0.32325, val_acc: 0.96000
    Epoch [1340/10000], loss: 0.33117 acc: 0.97333 val_loss: 0.32229, val_acc: 0.96000
    Epoch [1350/10000], loss: 0.33016 acc: 0.97333 val_loss: 0.32134, val_acc: 0.96000
    Epoch [1360/10000], loss: 0.32916 acc: 0.97333 val_loss: 0.32040, val_acc: 0.96000
    Epoch [1370/10000], loss: 0.32817 acc: 0.97333 val_loss: 0.31946, val_acc: 0.96000
    Epoch [1380/10000], loss: 0.32719 acc: 0.97333 val_loss: 0.31853, val_acc: 0.96000
    Epoch [1390/10000], loss: 0.32621 acc: 0.97333 val_loss: 0.31761, val_acc: 0.96000
    Epoch [1400/10000], loss: 0.32524 acc: 0.97333 val_loss: 0.31670, val_acc: 0.96000
    Epoch [1410/10000], loss: 0.32428 acc: 0.97333 val_loss: 0.31579, val_acc: 0.96000
    Epoch [1420/10000], loss: 0.32332 acc: 0.97333 val_loss: 0.31490, val_acc: 0.96000
    Epoch [1430/10000], loss: 0.32237 acc: 0.97333 val_loss: 0.31400, val_acc: 0.96000
    Epoch [1440/10000], loss: 0.32143 acc: 0.97333 val_loss: 0.31312, val_acc: 0.96000
    Epoch [1450/10000], loss: 0.32050 acc: 0.97333 val_loss: 0.31224, val_acc: 0.96000
    Epoch [1460/10000], loss: 0.31957 acc: 0.97333 val_loss: 0.31137, val_acc: 0.96000
    Epoch [1470/10000], loss: 0.31865 acc: 0.97333 val_loss: 0.31050, val_acc: 0.96000
    Epoch [1480/10000], loss: 0.31774 acc: 0.97333 val_loss: 0.30964, val_acc: 0.96000
    Epoch [1490/10000], loss: 0.31683 acc: 0.97333 val_loss: 0.30879, val_acc: 0.96000
    Epoch [1500/10000], loss: 0.31593 acc: 0.97333 val_loss: 0.30795, val_acc: 0.96000
    Epoch [1510/10000], loss: 0.31504 acc: 0.97333 val_loss: 0.30711, val_acc: 0.96000
    Epoch [1520/10000], loss: 0.31415 acc: 0.97333 val_loss: 0.30628, val_acc: 0.96000
    Epoch [1530/10000], loss: 0.31327 acc: 0.97333 val_loss: 0.30545, val_acc: 0.96000
    Epoch [1540/10000], loss: 0.31240 acc: 0.97333 val_loss: 0.30463, val_acc: 0.96000
    Epoch [1550/10000], loss: 0.31153 acc: 0.97333 val_loss: 0.30382, val_acc: 0.96000
    Epoch [1560/10000], loss: 0.31067 acc: 0.97333 val_loss: 0.30301, val_acc: 0.96000
    Epoch [1570/10000], loss: 0.30981 acc: 0.97333 val_loss: 0.30221, val_acc: 0.96000
    Epoch [1580/10000], loss: 0.30896 acc: 0.97333 val_loss: 0.30141, val_acc: 0.96000
    Epoch [1590/10000], loss: 0.30812 acc: 0.97333 val_loss: 0.30062, val_acc: 0.96000
    Epoch [1600/10000], loss: 0.30728 acc: 0.97333 val_loss: 0.29984, val_acc: 0.96000
    Epoch [1610/10000], loss: 0.30645 acc: 0.97333 val_loss: 0.29906, val_acc: 0.96000
    Epoch [1620/10000], loss: 0.30562 acc: 0.97333 val_loss: 0.29828, val_acc: 0.96000
    Epoch [1630/10000], loss: 0.30480 acc: 0.97333 val_loss: 0.29752, val_acc: 0.96000
    Epoch [1640/10000], loss: 0.30399 acc: 0.97333 val_loss: 0.29675, val_acc: 0.96000
    Epoch [1650/10000], loss: 0.30318 acc: 0.97333 val_loss: 0.29600, val_acc: 0.96000
    Epoch [1660/10000], loss: 0.30237 acc: 0.97333 val_loss: 0.29525, val_acc: 0.96000
    Epoch [1670/10000], loss: 0.30158 acc: 0.97333 val_loss: 0.29450, val_acc: 0.96000
    Epoch [1680/10000], loss: 0.30078 acc: 0.97333 val_loss: 0.29376, val_acc: 0.96000
    Epoch [1690/10000], loss: 0.30000 acc: 0.97333 val_loss: 0.29302, val_acc: 0.96000
    Epoch [1700/10000], loss: 0.29922 acc: 0.97333 val_loss: 0.29229, val_acc: 0.96000
    Epoch [1710/10000], loss: 0.29844 acc: 0.97333 val_loss: 0.29157, val_acc: 0.96000
    Epoch [1720/10000], loss: 0.29767 acc: 0.97333 val_loss: 0.29085, val_acc: 0.96000
    Epoch [1730/10000], loss: 0.29690 acc: 0.97333 val_loss: 0.29013, val_acc: 0.96000
    Epoch [1740/10000], loss: 0.29614 acc: 0.97333 val_loss: 0.28942, val_acc: 0.96000
    Epoch [1750/10000], loss: 0.29538 acc: 0.97333 val_loss: 0.28872, val_acc: 0.96000
    Epoch [1760/10000], loss: 0.29463 acc: 0.97333 val_loss: 0.28801, val_acc: 0.96000
    Epoch [1770/10000], loss: 0.29389 acc: 0.97333 val_loss: 0.28732, val_acc: 0.96000
    Epoch [1780/10000], loss: 0.29315 acc: 0.97333 val_loss: 0.28663, val_acc: 0.96000
    Epoch [1790/10000], loss: 0.29241 acc: 0.97333 val_loss: 0.28594, val_acc: 0.96000
    Epoch [1800/10000], loss: 0.29168 acc: 0.97333 val_loss: 0.28526, val_acc: 0.96000
    Epoch [1810/10000], loss: 0.29095 acc: 0.97333 val_loss: 0.28458, val_acc: 0.96000
    Epoch [1820/10000], loss: 0.29023 acc: 0.97333 val_loss: 0.28391, val_acc: 0.96000
    Epoch [1830/10000], loss: 0.28951 acc: 0.97333 val_loss: 0.28324, val_acc: 0.96000
    Epoch [1840/10000], loss: 0.28880 acc: 0.97333 val_loss: 0.28258, val_acc: 0.96000
    Epoch [1850/10000], loss: 0.28809 acc: 0.97333 val_loss: 0.28192, val_acc: 0.96000
    Epoch [1860/10000], loss: 0.28739 acc: 0.97333 val_loss: 0.28126, val_acc: 0.96000
    Epoch [1870/10000], loss: 0.28669 acc: 0.97333 val_loss: 0.28061, val_acc: 0.96000
    Epoch [1880/10000], loss: 0.28599 acc: 0.97333 val_loss: 0.27996, val_acc: 0.96000
    Epoch [1890/10000], loss: 0.28530 acc: 0.97333 val_loss: 0.27932, val_acc: 0.96000
    Epoch [1900/10000], loss: 0.28462 acc: 0.97333 val_loss: 0.27868, val_acc: 0.96000
    Epoch [1910/10000], loss: 0.28394 acc: 0.97333 val_loss: 0.27805, val_acc: 0.96000
    Epoch [1920/10000], loss: 0.28326 acc: 0.97333 val_loss: 0.27742, val_acc: 0.96000
    Epoch [1930/10000], loss: 0.28258 acc: 0.97333 val_loss: 0.27679, val_acc: 0.96000
    Epoch [1940/10000], loss: 0.28192 acc: 0.97333 val_loss: 0.27617, val_acc: 0.96000
    Epoch [1950/10000], loss: 0.28125 acc: 0.97333 val_loss: 0.27555, val_acc: 0.96000
    Epoch [1960/10000], loss: 0.28059 acc: 0.97333 val_loss: 0.27494, val_acc: 0.96000
    Epoch [1970/10000], loss: 0.27993 acc: 0.97333 val_loss: 0.27433, val_acc: 0.96000
    Epoch [1980/10000], loss: 0.27928 acc: 0.97333 val_loss: 0.27372, val_acc: 0.96000
    Epoch [1990/10000], loss: 0.27863 acc: 0.97333 val_loss: 0.27312, val_acc: 0.96000
    Epoch [2000/10000], loss: 0.27799 acc: 0.97333 val_loss: 0.27252, val_acc: 0.96000
    Epoch [2010/10000], loss: 0.27735 acc: 0.97333 val_loss: 0.27193, val_acc: 0.96000
    Epoch [2020/10000], loss: 0.27671 acc: 0.97333 val_loss: 0.27134, val_acc: 0.96000
    Epoch [2030/10000], loss: 0.27608 acc: 0.97333 val_loss: 0.27075, val_acc: 0.96000
    Epoch [2040/10000], loss: 0.27545 acc: 0.97333 val_loss: 0.27016, val_acc: 0.96000
    Epoch [2050/10000], loss: 0.27482 acc: 0.97333 val_loss: 0.26958, val_acc: 0.96000
    Epoch [2060/10000], loss: 0.27420 acc: 0.97333 val_loss: 0.26901, val_acc: 0.96000
    Epoch [2070/10000], loss: 0.27358 acc: 0.97333 val_loss: 0.26843, val_acc: 0.96000
    Epoch [2080/10000], loss: 0.27297 acc: 0.97333 val_loss: 0.26786, val_acc: 0.96000
    Epoch [2090/10000], loss: 0.27236 acc: 0.97333 val_loss: 0.26730, val_acc: 0.96000
    Epoch [2100/10000], loss: 0.27175 acc: 0.97333 val_loss: 0.26674, val_acc: 0.96000
    Epoch [2110/10000], loss: 0.27115 acc: 0.97333 val_loss: 0.26618, val_acc: 0.96000
    Epoch [2120/10000], loss: 0.27055 acc: 0.97333 val_loss: 0.26562, val_acc: 0.96000
    Epoch [2130/10000], loss: 0.26995 acc: 0.97333 val_loss: 0.26507, val_acc: 0.96000
    Epoch [2140/10000], loss: 0.26936 acc: 0.97333 val_loss: 0.26452, val_acc: 0.96000
    Epoch [2150/10000], loss: 0.26877 acc: 0.97333 val_loss: 0.26397, val_acc: 0.96000
    Epoch [2160/10000], loss: 0.26818 acc: 0.97333 val_loss: 0.26343, val_acc: 0.96000
    Epoch [2170/10000], loss: 0.26760 acc: 0.97333 val_loss: 0.26289, val_acc: 0.96000
    Epoch [2180/10000], loss: 0.26702 acc: 0.97333 val_loss: 0.26236, val_acc: 0.96000
    Epoch [2190/10000], loss: 0.26644 acc: 0.97333 val_loss: 0.26182, val_acc: 0.96000
    Epoch [2200/10000], loss: 0.26587 acc: 0.97333 val_loss: 0.26129, val_acc: 0.96000
    Epoch [2210/10000], loss: 0.26530 acc: 0.97333 val_loss: 0.26077, val_acc: 0.96000
    Epoch [2220/10000], loss: 0.26473 acc: 0.97333 val_loss: 0.26024, val_acc: 0.96000
    Epoch [2230/10000], loss: 0.26417 acc: 0.97333 val_loss: 0.25972, val_acc: 0.96000
    Epoch [2240/10000], loss: 0.26361 acc: 0.97333 val_loss: 0.25921, val_acc: 0.96000
    Epoch [2250/10000], loss: 0.26305 acc: 0.97333 val_loss: 0.25869, val_acc: 0.96000
    Epoch [2260/10000], loss: 0.26250 acc: 0.97333 val_loss: 0.25818, val_acc: 0.96000
    Epoch [2270/10000], loss: 0.26195 acc: 0.97333 val_loss: 0.25767, val_acc: 0.96000
    Epoch [2280/10000], loss: 0.26140 acc: 0.97333 val_loss: 0.25717, val_acc: 0.96000
    Epoch [2290/10000], loss: 0.26086 acc: 0.97333 val_loss: 0.25666, val_acc: 0.96000
    Epoch [2300/10000], loss: 0.26032 acc: 0.97333 val_loss: 0.25616, val_acc: 0.96000
    Epoch [2310/10000], loss: 0.25978 acc: 0.97333 val_loss: 0.25567, val_acc: 0.96000
    Epoch [2320/10000], loss: 0.25924 acc: 0.97333 val_loss: 0.25517, val_acc: 0.96000
    Epoch [2330/10000], loss: 0.25871 acc: 0.97333 val_loss: 0.25468, val_acc: 0.96000
    Epoch [2340/10000], loss: 0.25818 acc: 0.97333 val_loss: 0.25419, val_acc: 0.96000
    Epoch [2350/10000], loss: 0.25766 acc: 0.97333 val_loss: 0.25371, val_acc: 0.96000
    Epoch [2360/10000], loss: 0.25713 acc: 0.97333 val_loss: 0.25322, val_acc: 0.96000
    Epoch [2370/10000], loss: 0.25661 acc: 0.97333 val_loss: 0.25274, val_acc: 0.96000
    Epoch [2380/10000], loss: 0.25609 acc: 0.97333 val_loss: 0.25227, val_acc: 0.96000
    Epoch [2390/10000], loss: 0.25558 acc: 0.97333 val_loss: 0.25179, val_acc: 0.96000
    Epoch [2400/10000], loss: 0.25507 acc: 0.97333 val_loss: 0.25132, val_acc: 0.96000
    Epoch [2410/10000], loss: 0.25456 acc: 0.97333 val_loss: 0.25085, val_acc: 0.96000
    Epoch [2420/10000], loss: 0.25405 acc: 0.97333 val_loss: 0.25038, val_acc: 0.96000
    Epoch [2430/10000], loss: 0.25355 acc: 0.97333 val_loss: 0.24992, val_acc: 0.96000
    Epoch [2440/10000], loss: 0.25304 acc: 0.97333 val_loss: 0.24946, val_acc: 0.96000
    Epoch [2450/10000], loss: 0.25255 acc: 0.97333 val_loss: 0.24900, val_acc: 0.96000
    Epoch [2460/10000], loss: 0.25205 acc: 0.97333 val_loss: 0.24854, val_acc: 0.96000
    Epoch [2470/10000], loss: 0.25156 acc: 0.97333 val_loss: 0.24809, val_acc: 0.96000
    Epoch [2480/10000], loss: 0.25107 acc: 0.97333 val_loss: 0.24764, val_acc: 0.96000
    Epoch [2490/10000], loss: 0.25058 acc: 0.97333 val_loss: 0.24719, val_acc: 0.96000
    Epoch [2500/10000], loss: 0.25009 acc: 0.97333 val_loss: 0.24674, val_acc: 0.96000
    Epoch [2510/10000], loss: 0.24961 acc: 0.97333 val_loss: 0.24630, val_acc: 0.96000
    Epoch [2520/10000], loss: 0.24913 acc: 0.97333 val_loss: 0.24585, val_acc: 0.96000
    Epoch [2530/10000], loss: 0.24865 acc: 0.97333 val_loss: 0.24541, val_acc: 0.96000
    Epoch [2540/10000], loss: 0.24818 acc: 0.97333 val_loss: 0.24498, val_acc: 0.96000
    Epoch [2550/10000], loss: 0.24770 acc: 0.97333 val_loss: 0.24454, val_acc: 0.96000
    Epoch [2560/10000], loss: 0.24723 acc: 0.97333 val_loss: 0.24411, val_acc: 0.96000
    Epoch [2570/10000], loss: 0.24676 acc: 0.97333 val_loss: 0.24368, val_acc: 0.96000
    Epoch [2580/10000], loss: 0.24630 acc: 0.98667 val_loss: 0.24325, val_acc: 0.96000
    Epoch [2590/10000], loss: 0.24584 acc: 0.98667 val_loss: 0.24283, val_acc: 0.96000
    Epoch [2600/10000], loss: 0.24537 acc: 0.98667 val_loss: 0.24240, val_acc: 0.96000
    Epoch [2610/10000], loss: 0.24492 acc: 0.98667 val_loss: 0.24198, val_acc: 0.96000
    Epoch [2620/10000], loss: 0.24446 acc: 0.98667 val_loss: 0.24156, val_acc: 0.96000
    Epoch [2630/10000], loss: 0.24401 acc: 0.98667 val_loss: 0.24115, val_acc: 0.96000
    Epoch [2640/10000], loss: 0.24355 acc: 0.98667 val_loss: 0.24073, val_acc: 0.96000
    Epoch [2650/10000], loss: 0.24311 acc: 0.98667 val_loss: 0.24032, val_acc: 0.96000
    Epoch [2660/10000], loss: 0.24266 acc: 0.98667 val_loss: 0.23991, val_acc: 0.96000
    Epoch [2670/10000], loss: 0.24221 acc: 0.98667 val_loss: 0.23950, val_acc: 0.96000
    Epoch [2680/10000], loss: 0.24177 acc: 0.98667 val_loss: 0.23909, val_acc: 0.96000
    Epoch [2690/10000], loss: 0.24133 acc: 0.98667 val_loss: 0.23869, val_acc: 0.96000
    Epoch [2700/10000], loss: 0.24089 acc: 0.98667 val_loss: 0.23829, val_acc: 0.96000
    Epoch [2710/10000], loss: 0.24046 acc: 0.98667 val_loss: 0.23789, val_acc: 0.96000
    Epoch [2720/10000], loss: 0.24002 acc: 0.98667 val_loss: 0.23749, val_acc: 0.96000
    Epoch [2730/10000], loss: 0.23959 acc: 0.98667 val_loss: 0.23710, val_acc: 0.96000
    Epoch [2740/10000], loss: 0.23916 acc: 0.98667 val_loss: 0.23670, val_acc: 0.96000
    Epoch [2750/10000], loss: 0.23874 acc: 0.98667 val_loss: 0.23631, val_acc: 0.96000
    Epoch [2760/10000], loss: 0.23831 acc: 0.98667 val_loss: 0.23592, val_acc: 0.96000
    Epoch [2770/10000], loss: 0.23789 acc: 0.98667 val_loss: 0.23553, val_acc: 0.96000
    Epoch [2780/10000], loss: 0.23747 acc: 0.98667 val_loss: 0.23515, val_acc: 0.96000
    Epoch [2790/10000], loss: 0.23705 acc: 0.98667 val_loss: 0.23476, val_acc: 0.96000
    Epoch [2800/10000], loss: 0.23663 acc: 0.98667 val_loss: 0.23438, val_acc: 0.96000
    Epoch [2810/10000], loss: 0.23622 acc: 0.98667 val_loss: 0.23400, val_acc: 0.96000
    Epoch [2820/10000], loss: 0.23580 acc: 0.98667 val_loss: 0.23363, val_acc: 0.96000
    Epoch [2830/10000], loss: 0.23539 acc: 0.98667 val_loss: 0.23325, val_acc: 0.96000
    Epoch [2840/10000], loss: 0.23498 acc: 0.98667 val_loss: 0.23287, val_acc: 0.96000
    Epoch [2850/10000], loss: 0.23458 acc: 0.98667 val_loss: 0.23250, val_acc: 0.96000
    Epoch [2860/10000], loss: 0.23417 acc: 0.98667 val_loss: 0.23213, val_acc: 0.96000
    Epoch [2870/10000], loss: 0.23377 acc: 0.98667 val_loss: 0.23176, val_acc: 0.96000
    Epoch [2880/10000], loss: 0.23337 acc: 0.98667 val_loss: 0.23140, val_acc: 0.96000
    Epoch [2890/10000], loss: 0.23297 acc: 0.98667 val_loss: 0.23103, val_acc: 0.96000
    Epoch [2900/10000], loss: 0.23257 acc: 0.98667 val_loss: 0.23067, val_acc: 0.96000
    Epoch [2910/10000], loss: 0.23218 acc: 0.98667 val_loss: 0.23031, val_acc: 0.96000
    Epoch [2920/10000], loss: 0.23178 acc: 0.98667 val_loss: 0.22995, val_acc: 0.96000
    Epoch [2930/10000], loss: 0.23139 acc: 0.98667 val_loss: 0.22959, val_acc: 0.96000
    Epoch [2940/10000], loss: 0.23100 acc: 0.98667 val_loss: 0.22923, val_acc: 0.96000
    Epoch [2950/10000], loss: 0.23061 acc: 0.98667 val_loss: 0.22888, val_acc: 0.96000
    Epoch [2960/10000], loss: 0.23023 acc: 0.98667 val_loss: 0.22853, val_acc: 0.96000
    Epoch [2970/10000], loss: 0.22984 acc: 0.98667 val_loss: 0.22818, val_acc: 0.96000
    Epoch [2980/10000], loss: 0.22946 acc: 0.98667 val_loss: 0.22783, val_acc: 0.96000
    Epoch [2990/10000], loss: 0.22908 acc: 0.98667 val_loss: 0.22748, val_acc: 0.96000
    Epoch [3000/10000], loss: 0.22870 acc: 0.98667 val_loss: 0.22713, val_acc: 0.96000
    Epoch [3010/10000], loss: 0.22832 acc: 0.98667 val_loss: 0.22679, val_acc: 0.96000
    Epoch [3020/10000], loss: 0.22795 acc: 0.98667 val_loss: 0.22645, val_acc: 0.96000
    Epoch [3030/10000], loss: 0.22757 acc: 0.98667 val_loss: 0.22610, val_acc: 0.96000
    Epoch [3040/10000], loss: 0.22720 acc: 0.98667 val_loss: 0.22577, val_acc: 0.96000
    Epoch [3050/10000], loss: 0.22683 acc: 0.98667 val_loss: 0.22543, val_acc: 0.96000
    Epoch [3060/10000], loss: 0.22646 acc: 0.98667 val_loss: 0.22509, val_acc: 0.96000
    Epoch [3070/10000], loss: 0.22610 acc: 0.98667 val_loss: 0.22476, val_acc: 0.96000
    Epoch [3080/10000], loss: 0.22573 acc: 0.98667 val_loss: 0.22442, val_acc: 0.96000
    Epoch [3090/10000], loss: 0.22537 acc: 0.98667 val_loss: 0.22409, val_acc: 0.96000
    Epoch [3100/10000], loss: 0.22501 acc: 0.98667 val_loss: 0.22376, val_acc: 0.96000
    Epoch [3110/10000], loss: 0.22465 acc: 0.98667 val_loss: 0.22343, val_acc: 0.96000
    Epoch [3120/10000], loss: 0.22429 acc: 0.98667 val_loss: 0.22311, val_acc: 0.96000
    Epoch [3130/10000], loss: 0.22393 acc: 0.98667 val_loss: 0.22278, val_acc: 0.96000
    Epoch [3140/10000], loss: 0.22358 acc: 0.98667 val_loss: 0.22246, val_acc: 0.96000
    Epoch [3150/10000], loss: 0.22322 acc: 0.98667 val_loss: 0.22214, val_acc: 0.96000
    Epoch [3160/10000], loss: 0.22287 acc: 0.98667 val_loss: 0.22181, val_acc: 0.96000
    Epoch [3170/10000], loss: 0.22252 acc: 0.98667 val_loss: 0.22150, val_acc: 0.96000
    Epoch [3180/10000], loss: 0.22217 acc: 0.98667 val_loss: 0.22118, val_acc: 0.96000
    Epoch [3190/10000], loss: 0.22182 acc: 0.98667 val_loss: 0.22086, val_acc: 0.96000
    Epoch [3200/10000], loss: 0.22148 acc: 0.98667 val_loss: 0.22055, val_acc: 0.96000
    Epoch [3210/10000], loss: 0.22113 acc: 0.98667 val_loss: 0.22023, val_acc: 0.96000
    Epoch [3220/10000], loss: 0.22079 acc: 0.98667 val_loss: 0.21992, val_acc: 0.96000
    Epoch [3230/10000], loss: 0.22045 acc: 0.98667 val_loss: 0.21961, val_acc: 0.96000
    Epoch [3240/10000], loss: 0.22011 acc: 0.98667 val_loss: 0.21930, val_acc: 0.96000
    Epoch [3250/10000], loss: 0.21977 acc: 0.98667 val_loss: 0.21899, val_acc: 0.96000
    Epoch [3260/10000], loss: 0.21943 acc: 0.98667 val_loss: 0.21869, val_acc: 0.96000
    Epoch [3270/10000], loss: 0.21910 acc: 0.98667 val_loss: 0.21838, val_acc: 0.96000
    Epoch [3280/10000], loss: 0.21876 acc: 0.98667 val_loss: 0.21808, val_acc: 0.96000
    Epoch [3290/10000], loss: 0.21843 acc: 0.98667 val_loss: 0.21778, val_acc: 0.96000
    Epoch [3300/10000], loss: 0.21810 acc: 0.98667 val_loss: 0.21747, val_acc: 0.96000
    Epoch [3310/10000], loss: 0.21777 acc: 0.98667 val_loss: 0.21717, val_acc: 0.96000
    Epoch [3320/10000], loss: 0.21744 acc: 0.98667 val_loss: 0.21688, val_acc: 0.96000
    Epoch [3330/10000], loss: 0.21711 acc: 0.98667 val_loss: 0.21658, val_acc: 0.96000
    Epoch [3340/10000], loss: 0.21679 acc: 0.98667 val_loss: 0.21628, val_acc: 0.96000
    Epoch [3350/10000], loss: 0.21646 acc: 0.98667 val_loss: 0.21599, val_acc: 0.96000
    Epoch [3360/10000], loss: 0.21614 acc: 0.98667 val_loss: 0.21570, val_acc: 0.96000
    Epoch [3370/10000], loss: 0.21582 acc: 0.98667 val_loss: 0.21540, val_acc: 0.96000
    Epoch [3380/10000], loss: 0.21550 acc: 0.98667 val_loss: 0.21511, val_acc: 0.96000
    Epoch [3390/10000], loss: 0.21518 acc: 0.98667 val_loss: 0.21483, val_acc: 0.96000
    Epoch [3400/10000], loss: 0.21487 acc: 0.98667 val_loss: 0.21454, val_acc: 0.96000
    Epoch [3410/10000], loss: 0.21455 acc: 0.98667 val_loss: 0.21425, val_acc: 0.96000
    Epoch [3420/10000], loss: 0.21424 acc: 0.98667 val_loss: 0.21396, val_acc: 0.96000
    Epoch [3430/10000], loss: 0.21392 acc: 0.98667 val_loss: 0.21368, val_acc: 0.96000
    Epoch [3440/10000], loss: 0.21361 acc: 0.98667 val_loss: 0.21340, val_acc: 0.96000
    Epoch [3450/10000], loss: 0.21330 acc: 0.98667 val_loss: 0.21312, val_acc: 0.96000
    Epoch [3460/10000], loss: 0.21299 acc: 0.98667 val_loss: 0.21284, val_acc: 0.96000
    Epoch [3470/10000], loss: 0.21268 acc: 0.98667 val_loss: 0.21256, val_acc: 0.96000
    Epoch [3480/10000], loss: 0.21238 acc: 0.98667 val_loss: 0.21228, val_acc: 0.96000
    Epoch [3490/10000], loss: 0.21207 acc: 0.98667 val_loss: 0.21200, val_acc: 0.96000
    Epoch [3500/10000], loss: 0.21177 acc: 0.98667 val_loss: 0.21173, val_acc: 0.96000
    Epoch [3510/10000], loss: 0.21146 acc: 0.98667 val_loss: 0.21145, val_acc: 0.96000
    Epoch [3520/10000], loss: 0.21116 acc: 0.98667 val_loss: 0.21118, val_acc: 0.96000
    Epoch [3530/10000], loss: 0.21086 acc: 0.98667 val_loss: 0.21091, val_acc: 0.96000
    Epoch [3540/10000], loss: 0.21056 acc: 0.98667 val_loss: 0.21064, val_acc: 0.96000
    Epoch [3550/10000], loss: 0.21026 acc: 0.98667 val_loss: 0.21037, val_acc: 0.96000
    Epoch [3560/10000], loss: 0.20997 acc: 0.98667 val_loss: 0.21010, val_acc: 0.96000
    Epoch [3570/10000], loss: 0.20967 acc: 0.98667 val_loss: 0.20983, val_acc: 0.96000
    Epoch [3580/10000], loss: 0.20938 acc: 0.98667 val_loss: 0.20956, val_acc: 0.96000
    Epoch [3590/10000], loss: 0.20909 acc: 0.98667 val_loss: 0.20930, val_acc: 0.96000
    Epoch [3600/10000], loss: 0.20879 acc: 0.98667 val_loss: 0.20903, val_acc: 0.96000
    Epoch [3610/10000], loss: 0.20850 acc: 0.98667 val_loss: 0.20877, val_acc: 0.96000
    Epoch [3620/10000], loss: 0.20821 acc: 0.98667 val_loss: 0.20851, val_acc: 0.96000
    Epoch [3630/10000], loss: 0.20793 acc: 0.98667 val_loss: 0.20825, val_acc: 0.96000
    Epoch [3640/10000], loss: 0.20764 acc: 0.98667 val_loss: 0.20799, val_acc: 0.96000
    Epoch [3650/10000], loss: 0.20735 acc: 0.98667 val_loss: 0.20773, val_acc: 0.96000
    Epoch [3660/10000], loss: 0.20707 acc: 0.98667 val_loss: 0.20747, val_acc: 0.96000
    Epoch [3670/10000], loss: 0.20678 acc: 0.98667 val_loss: 0.20721, val_acc: 0.96000
    Epoch [3680/10000], loss: 0.20650 acc: 0.98667 val_loss: 0.20696, val_acc: 0.96000
    Epoch [3690/10000], loss: 0.20622 acc: 0.98667 val_loss: 0.20670, val_acc: 0.96000
    Epoch [3700/10000], loss: 0.20594 acc: 0.98667 val_loss: 0.20645, val_acc: 0.96000
    Epoch [3710/10000], loss: 0.20566 acc: 0.98667 val_loss: 0.20620, val_acc: 0.96000
    Epoch [3720/10000], loss: 0.20538 acc: 0.98667 val_loss: 0.20595, val_acc: 0.96000
    Epoch [3730/10000], loss: 0.20511 acc: 0.98667 val_loss: 0.20570, val_acc: 0.96000
    Epoch [3740/10000], loss: 0.20483 acc: 0.98667 val_loss: 0.20545, val_acc: 0.96000
    Epoch [3750/10000], loss: 0.20455 acc: 0.98667 val_loss: 0.20520, val_acc: 0.96000
    Epoch [3760/10000], loss: 0.20428 acc: 0.98667 val_loss: 0.20495, val_acc: 0.96000
    Epoch [3770/10000], loss: 0.20401 acc: 0.98667 val_loss: 0.20471, val_acc: 0.96000
    Epoch [3780/10000], loss: 0.20374 acc: 0.98667 val_loss: 0.20446, val_acc: 0.96000
    Epoch [3790/10000], loss: 0.20347 acc: 0.98667 val_loss: 0.20422, val_acc: 0.96000
    Epoch [3800/10000], loss: 0.20320 acc: 0.98667 val_loss: 0.20397, val_acc: 0.96000
    Epoch [3810/10000], loss: 0.20293 acc: 0.98667 val_loss: 0.20373, val_acc: 0.96000
    Epoch [3820/10000], loss: 0.20266 acc: 0.98667 val_loss: 0.20349, val_acc: 0.96000
    Epoch [3830/10000], loss: 0.20239 acc: 0.98667 val_loss: 0.20325, val_acc: 0.96000
    Epoch [3840/10000], loss: 0.20213 acc: 0.98667 val_loss: 0.20301, val_acc: 0.96000
    Epoch [3850/10000], loss: 0.20186 acc: 0.98667 val_loss: 0.20277, val_acc: 0.96000
    Epoch [3860/10000], loss: 0.20160 acc: 0.98667 val_loss: 0.20253, val_acc: 0.96000
    Epoch [3870/10000], loss: 0.20134 acc: 0.98667 val_loss: 0.20230, val_acc: 0.96000
    Epoch [3880/10000], loss: 0.20108 acc: 0.98667 val_loss: 0.20206, val_acc: 0.96000
    Epoch [3890/10000], loss: 0.20082 acc: 0.98667 val_loss: 0.20183, val_acc: 0.96000
    Epoch [3900/10000], loss: 0.20056 acc: 0.98667 val_loss: 0.20159, val_acc: 0.96000
    Epoch [3910/10000], loss: 0.20030 acc: 0.98667 val_loss: 0.20136, val_acc: 0.96000
    Epoch [3920/10000], loss: 0.20004 acc: 0.98667 val_loss: 0.20113, val_acc: 0.96000
    Epoch [3930/10000], loss: 0.19979 acc: 0.98667 val_loss: 0.20090, val_acc: 0.96000
    Epoch [3940/10000], loss: 0.19953 acc: 0.98667 val_loss: 0.20067, val_acc: 0.96000
    Epoch [3950/10000], loss: 0.19928 acc: 0.98667 val_loss: 0.20044, val_acc: 0.96000
    Epoch [3960/10000], loss: 0.19902 acc: 0.98667 val_loss: 0.20021, val_acc: 0.96000
    Epoch [3970/10000], loss: 0.19877 acc: 0.98667 val_loss: 0.19998, val_acc: 0.96000
    Epoch [3980/10000], loss: 0.19852 acc: 0.98667 val_loss: 0.19976, val_acc: 0.96000
    Epoch [3990/10000], loss: 0.19827 acc: 0.98667 val_loss: 0.19953, val_acc: 0.96000
    Epoch [4000/10000], loss: 0.19802 acc: 0.98667 val_loss: 0.19931, val_acc: 0.96000
    Epoch [4010/10000], loss: 0.19777 acc: 0.98667 val_loss: 0.19908, val_acc: 0.96000
    Epoch [4020/10000], loss: 0.19752 acc: 0.98667 val_loss: 0.19886, val_acc: 0.96000
    Epoch [4030/10000], loss: 0.19728 acc: 0.98667 val_loss: 0.19864, val_acc: 0.96000
    Epoch [4040/10000], loss: 0.19703 acc: 0.98667 val_loss: 0.19842, val_acc: 0.96000
    Epoch [4050/10000], loss: 0.19679 acc: 0.98667 val_loss: 0.19820, val_acc: 0.96000
    Epoch [4060/10000], loss: 0.19654 acc: 0.98667 val_loss: 0.19798, val_acc: 0.96000
    Epoch [4070/10000], loss: 0.19630 acc: 0.98667 val_loss: 0.19776, val_acc: 0.96000
    Epoch [4080/10000], loss: 0.19606 acc: 0.98667 val_loss: 0.19754, val_acc: 0.96000
    Epoch [4090/10000], loss: 0.19582 acc: 0.98667 val_loss: 0.19732, val_acc: 0.96000
    Epoch [4100/10000], loss: 0.19557 acc: 0.98667 val_loss: 0.19711, val_acc: 0.96000
    Epoch [4110/10000], loss: 0.19534 acc: 0.98667 val_loss: 0.19689, val_acc: 0.96000
    Epoch [4120/10000], loss: 0.19510 acc: 0.98667 val_loss: 0.19668, val_acc: 0.96000
    Epoch [4130/10000], loss: 0.19486 acc: 0.98667 val_loss: 0.19646, val_acc: 0.96000
    Epoch [4140/10000], loss: 0.19462 acc: 0.98667 val_loss: 0.19625, val_acc: 0.96000
    Epoch [4150/10000], loss: 0.19439 acc: 0.98667 val_loss: 0.19604, val_acc: 0.96000
    Epoch [4160/10000], loss: 0.19415 acc: 0.98667 val_loss: 0.19583, val_acc: 0.96000
    Epoch [4170/10000], loss: 0.19392 acc: 0.98667 val_loss: 0.19562, val_acc: 0.96000
    Epoch [4180/10000], loss: 0.19368 acc: 0.98667 val_loss: 0.19541, val_acc: 0.96000
    Epoch [4190/10000], loss: 0.19345 acc: 0.98667 val_loss: 0.19520, val_acc: 0.96000
    Epoch [4200/10000], loss: 0.19322 acc: 0.98667 val_loss: 0.19499, val_acc: 0.96000
    Epoch [4210/10000], loss: 0.19299 acc: 0.98667 val_loss: 0.19478, val_acc: 0.96000
    Epoch [4220/10000], loss: 0.19276 acc: 0.98667 val_loss: 0.19457, val_acc: 0.96000
    Epoch [4230/10000], loss: 0.19253 acc: 0.98667 val_loss: 0.19437, val_acc: 0.96000
    Epoch [4240/10000], loss: 0.19230 acc: 0.98667 val_loss: 0.19416, val_acc: 0.96000
    Epoch [4250/10000], loss: 0.19207 acc: 0.98667 val_loss: 0.19396, val_acc: 0.96000
    Epoch [4260/10000], loss: 0.19184 acc: 0.98667 val_loss: 0.19376, val_acc: 0.96000
    Epoch [4270/10000], loss: 0.19162 acc: 0.98667 val_loss: 0.19355, val_acc: 0.96000
    Epoch [4280/10000], loss: 0.19139 acc: 0.98667 val_loss: 0.19335, val_acc: 0.96000
    Epoch [4290/10000], loss: 0.19117 acc: 0.98667 val_loss: 0.19315, val_acc: 0.96000
    Epoch [4300/10000], loss: 0.19094 acc: 0.98667 val_loss: 0.19295, val_acc: 0.96000
    Epoch [4310/10000], loss: 0.19072 acc: 0.98667 val_loss: 0.19275, val_acc: 0.96000
    Epoch [4320/10000], loss: 0.19050 acc: 0.98667 val_loss: 0.19255, val_acc: 0.96000
    Epoch [4330/10000], loss: 0.19028 acc: 0.98667 val_loss: 0.19235, val_acc: 0.96000
    Epoch [4340/10000], loss: 0.19006 acc: 0.98667 val_loss: 0.19215, val_acc: 0.96000
    Epoch [4350/10000], loss: 0.18984 acc: 0.98667 val_loss: 0.19196, val_acc: 0.96000
    Epoch [4360/10000], loss: 0.18962 acc: 0.98667 val_loss: 0.19176, val_acc: 0.96000
    Epoch [4370/10000], loss: 0.18940 acc: 0.98667 val_loss: 0.19156, val_acc: 0.96000
    Epoch [4380/10000], loss: 0.18918 acc: 0.98667 val_loss: 0.19137, val_acc: 0.96000
    Epoch [4390/10000], loss: 0.18897 acc: 0.98667 val_loss: 0.19118, val_acc: 0.96000
    Epoch [4400/10000], loss: 0.18875 acc: 0.98667 val_loss: 0.19098, val_acc: 0.96000
    Epoch [4410/10000], loss: 0.18853 acc: 0.98667 val_loss: 0.19079, val_acc: 0.96000
    Epoch [4420/10000], loss: 0.18832 acc: 0.98667 val_loss: 0.19060, val_acc: 0.96000
    Epoch [4430/10000], loss: 0.18811 acc: 0.98667 val_loss: 0.19041, val_acc: 0.96000
    Epoch [4440/10000], loss: 0.18789 acc: 0.98667 val_loss: 0.19021, val_acc: 0.96000
    Epoch [4450/10000], loss: 0.18768 acc: 0.98667 val_loss: 0.19002, val_acc: 0.96000
    Epoch [4460/10000], loss: 0.18747 acc: 0.98667 val_loss: 0.18984, val_acc: 0.96000
    Epoch [4470/10000], loss: 0.18726 acc: 0.98667 val_loss: 0.18965, val_acc: 0.96000
    Epoch [4480/10000], loss: 0.18705 acc: 0.98667 val_loss: 0.18946, val_acc: 0.96000
    Epoch [4490/10000], loss: 0.18684 acc: 0.98667 val_loss: 0.18927, val_acc: 0.96000
    Epoch [4500/10000], loss: 0.18663 acc: 0.98667 val_loss: 0.18908, val_acc: 0.96000
    Epoch [4510/10000], loss: 0.18642 acc: 0.98667 val_loss: 0.18890, val_acc: 0.96000
    Epoch [4520/10000], loss: 0.18622 acc: 0.98667 val_loss: 0.18871, val_acc: 0.96000
    Epoch [4530/10000], loss: 0.18601 acc: 0.98667 val_loss: 0.18853, val_acc: 0.96000
    Epoch [4540/10000], loss: 0.18580 acc: 0.98667 val_loss: 0.18834, val_acc: 0.96000
    Epoch [4550/10000], loss: 0.18560 acc: 0.98667 val_loss: 0.18816, val_acc: 0.96000
    Epoch [4560/10000], loss: 0.18539 acc: 0.98667 val_loss: 0.18798, val_acc: 0.96000
    Epoch [4570/10000], loss: 0.18519 acc: 0.98667 val_loss: 0.18780, val_acc: 0.96000
    Epoch [4580/10000], loss: 0.18499 acc: 0.98667 val_loss: 0.18762, val_acc: 0.96000
    Epoch [4590/10000], loss: 0.18478 acc: 0.98667 val_loss: 0.18743, val_acc: 0.96000
    Epoch [4600/10000], loss: 0.18458 acc: 0.98667 val_loss: 0.18725, val_acc: 0.96000
    Epoch [4610/10000], loss: 0.18438 acc: 0.98667 val_loss: 0.18707, val_acc: 0.96000
    Epoch [4620/10000], loss: 0.18418 acc: 0.98667 val_loss: 0.18690, val_acc: 0.96000
    Epoch [4630/10000], loss: 0.18398 acc: 0.98667 val_loss: 0.18672, val_acc: 0.96000
    Epoch [4640/10000], loss: 0.18378 acc: 0.98667 val_loss: 0.18654, val_acc: 0.96000
    Epoch [4650/10000], loss: 0.18358 acc: 0.98667 val_loss: 0.18636, val_acc: 0.96000
    Epoch [4660/10000], loss: 0.18339 acc: 0.98667 val_loss: 0.18619, val_acc: 0.96000
    Epoch [4670/10000], loss: 0.18319 acc: 0.98667 val_loss: 0.18601, val_acc: 0.96000
    Epoch [4680/10000], loss: 0.18299 acc: 0.98667 val_loss: 0.18583, val_acc: 0.96000
    Epoch [4690/10000], loss: 0.18280 acc: 0.98667 val_loss: 0.18566, val_acc: 0.96000
    Epoch [4700/10000], loss: 0.18260 acc: 0.98667 val_loss: 0.18549, val_acc: 0.96000
    Epoch [4710/10000], loss: 0.18241 acc: 0.98667 val_loss: 0.18531, val_acc: 0.96000
    Epoch [4720/10000], loss: 0.18221 acc: 0.98667 val_loss: 0.18514, val_acc: 0.96000
    Epoch [4730/10000], loss: 0.18202 acc: 0.98667 val_loss: 0.18497, val_acc: 0.96000
    Epoch [4740/10000], loss: 0.18183 acc: 0.98667 val_loss: 0.18479, val_acc: 0.96000
    Epoch [4750/10000], loss: 0.18164 acc: 0.98667 val_loss: 0.18462, val_acc: 0.96000
    Epoch [4760/10000], loss: 0.18144 acc: 0.98667 val_loss: 0.18445, val_acc: 0.96000
    Epoch [4770/10000], loss: 0.18125 acc: 0.98667 val_loss: 0.18428, val_acc: 0.96000
    Epoch [4780/10000], loss: 0.18106 acc: 0.98667 val_loss: 0.18411, val_acc: 0.96000
    Epoch [4790/10000], loss: 0.18087 acc: 0.98667 val_loss: 0.18395, val_acc: 0.96000
    Epoch [4800/10000], loss: 0.18068 acc: 0.98667 val_loss: 0.18378, val_acc: 0.96000
    Epoch [4810/10000], loss: 0.18050 acc: 0.98667 val_loss: 0.18361, val_acc: 0.96000
    Epoch [4820/10000], loss: 0.18031 acc: 0.98667 val_loss: 0.18344, val_acc: 0.96000
    Epoch [4830/10000], loss: 0.18012 acc: 0.98667 val_loss: 0.18328, val_acc: 0.96000
    Epoch [4840/10000], loss: 0.17994 acc: 0.98667 val_loss: 0.18311, val_acc: 0.96000
    Epoch [4850/10000], loss: 0.17975 acc: 0.98667 val_loss: 0.18294, val_acc: 0.96000
    Epoch [4860/10000], loss: 0.17956 acc: 0.98667 val_loss: 0.18278, val_acc: 0.96000
    Epoch [4870/10000], loss: 0.17938 acc: 0.98667 val_loss: 0.18261, val_acc: 0.96000
    Epoch [4880/10000], loss: 0.17920 acc: 0.98667 val_loss: 0.18245, val_acc: 0.96000
    Epoch [4890/10000], loss: 0.17901 acc: 0.98667 val_loss: 0.18229, val_acc: 0.96000
    Epoch [4900/10000], loss: 0.17883 acc: 0.98667 val_loss: 0.18212, val_acc: 0.96000
    Epoch [4910/10000], loss: 0.17865 acc: 0.98667 val_loss: 0.18196, val_acc: 0.96000
    Epoch [4920/10000], loss: 0.17846 acc: 0.98667 val_loss: 0.18180, val_acc: 0.96000
    Epoch [4930/10000], loss: 0.17828 acc: 0.98667 val_loss: 0.18164, val_acc: 0.96000
    Epoch [4940/10000], loss: 0.17810 acc: 0.98667 val_loss: 0.18148, val_acc: 0.96000
    Epoch [4950/10000], loss: 0.17792 acc: 0.98667 val_loss: 0.18132, val_acc: 0.96000
    Epoch [4960/10000], loss: 0.17774 acc: 0.98667 val_loss: 0.18116, val_acc: 0.96000
    Epoch [4970/10000], loss: 0.17756 acc: 0.98667 val_loss: 0.18100, val_acc: 0.96000
    Epoch [4980/10000], loss: 0.17739 acc: 0.98667 val_loss: 0.18084, val_acc: 0.96000
    Epoch [4990/10000], loss: 0.17721 acc: 0.98667 val_loss: 0.18068, val_acc: 0.96000
    Epoch [5000/10000], loss: 0.17703 acc: 0.98667 val_loss: 0.18053, val_acc: 0.96000
    Epoch [5010/10000], loss: 0.17685 acc: 0.98667 val_loss: 0.18037, val_acc: 0.96000
    Epoch [5020/10000], loss: 0.17668 acc: 0.98667 val_loss: 0.18021, val_acc: 0.96000
    Epoch [5030/10000], loss: 0.17650 acc: 0.98667 val_loss: 0.18006, val_acc: 0.96000
    Epoch [5040/10000], loss: 0.17633 acc: 0.98667 val_loss: 0.17990, val_acc: 0.96000
    Epoch [5050/10000], loss: 0.17615 acc: 0.98667 val_loss: 0.17975, val_acc: 0.96000
    Epoch [5060/10000], loss: 0.17598 acc: 0.98667 val_loss: 0.17959, val_acc: 0.96000
    Epoch [5070/10000], loss: 0.17581 acc: 0.98667 val_loss: 0.17944, val_acc: 0.96000
    Epoch [5080/10000], loss: 0.17563 acc: 0.98667 val_loss: 0.17928, val_acc: 0.96000
    Epoch [5090/10000], loss: 0.17546 acc: 0.98667 val_loss: 0.17913, val_acc: 0.96000
    Epoch [5100/10000], loss: 0.17529 acc: 0.98667 val_loss: 0.17898, val_acc: 0.96000
    Epoch [5110/10000], loss: 0.17512 acc: 0.98667 val_loss: 0.17883, val_acc: 0.96000
    Epoch [5120/10000], loss: 0.17495 acc: 0.98667 val_loss: 0.17867, val_acc: 0.96000
    Epoch [5130/10000], loss: 0.17478 acc: 0.98667 val_loss: 0.17852, val_acc: 0.96000
    Epoch [5140/10000], loss: 0.17461 acc: 0.98667 val_loss: 0.17837, val_acc: 0.96000
    Epoch [5150/10000], loss: 0.17444 acc: 0.98667 val_loss: 0.17822, val_acc: 0.96000
    Epoch [5160/10000], loss: 0.17427 acc: 0.98667 val_loss: 0.17807, val_acc: 0.96000
    Epoch [5170/10000], loss: 0.17410 acc: 0.98667 val_loss: 0.17792, val_acc: 0.96000
    Epoch [5180/10000], loss: 0.17393 acc: 0.98667 val_loss: 0.17778, val_acc: 0.96000
    Epoch [5190/10000], loss: 0.17377 acc: 0.98667 val_loss: 0.17763, val_acc: 0.96000
    Epoch [5200/10000], loss: 0.17360 acc: 0.98667 val_loss: 0.17748, val_acc: 0.96000
    Epoch [5210/10000], loss: 0.17343 acc: 0.98667 val_loss: 0.17733, val_acc: 0.96000
    Epoch [5220/10000], loss: 0.17327 acc: 0.98667 val_loss: 0.17719, val_acc: 0.96000
    Epoch [5230/10000], loss: 0.17310 acc: 0.98667 val_loss: 0.17704, val_acc: 0.96000
    Epoch [5240/10000], loss: 0.17294 acc: 0.98667 val_loss: 0.17689, val_acc: 0.96000
    Epoch [5250/10000], loss: 0.17277 acc: 0.98667 val_loss: 0.17675, val_acc: 0.96000
    Epoch [5260/10000], loss: 0.17261 acc: 0.98667 val_loss: 0.17660, val_acc: 0.96000
    Epoch [5270/10000], loss: 0.17245 acc: 0.98667 val_loss: 0.17646, val_acc: 0.96000
    Epoch [5280/10000], loss: 0.17229 acc: 0.98667 val_loss: 0.17631, val_acc: 0.96000
    Epoch [5290/10000], loss: 0.17212 acc: 0.98667 val_loss: 0.17617, val_acc: 0.96000
    Epoch [5300/10000], loss: 0.17196 acc: 0.98667 val_loss: 0.17603, val_acc: 0.96000
    Epoch [5310/10000], loss: 0.17180 acc: 0.98667 val_loss: 0.17589, val_acc: 0.96000
    Epoch [5320/10000], loss: 0.17164 acc: 0.98667 val_loss: 0.17574, val_acc: 0.96000
    Epoch [5330/10000], loss: 0.17148 acc: 0.98667 val_loss: 0.17560, val_acc: 0.96000
    Epoch [5340/10000], loss: 0.17132 acc: 0.98667 val_loss: 0.17546, val_acc: 0.96000
    Epoch [5350/10000], loss: 0.17116 acc: 0.98667 val_loss: 0.17532, val_acc: 0.96000
    Epoch [5360/10000], loss: 0.17100 acc: 0.98667 val_loss: 0.17518, val_acc: 0.96000
    Epoch [5370/10000], loss: 0.17084 acc: 0.98667 val_loss: 0.17504, val_acc: 0.96000
    Epoch [5380/10000], loss: 0.17068 acc: 0.98667 val_loss: 0.17490, val_acc: 0.96000
    Epoch [5390/10000], loss: 0.17053 acc: 0.98667 val_loss: 0.17476, val_acc: 0.96000
    Epoch [5400/10000], loss: 0.17037 acc: 0.98667 val_loss: 0.17462, val_acc: 0.96000
    Epoch [5410/10000], loss: 0.17021 acc: 0.98667 val_loss: 0.17448, val_acc: 0.96000
    Epoch [5420/10000], loss: 0.17006 acc: 0.98667 val_loss: 0.17434, val_acc: 0.96000
    Epoch [5430/10000], loss: 0.16990 acc: 0.98667 val_loss: 0.17421, val_acc: 0.96000
    Epoch [5440/10000], loss: 0.16975 acc: 0.98667 val_loss: 0.17407, val_acc: 0.96000
    Epoch [5450/10000], loss: 0.16959 acc: 0.98667 val_loss: 0.17393, val_acc: 0.96000
    Epoch [5460/10000], loss: 0.16944 acc: 0.98667 val_loss: 0.17380, val_acc: 0.96000
    Epoch [5470/10000], loss: 0.16928 acc: 0.98667 val_loss: 0.17366, val_acc: 0.96000
    Epoch [5480/10000], loss: 0.16913 acc: 0.98667 val_loss: 0.17352, val_acc: 0.96000
    Epoch [5490/10000], loss: 0.16898 acc: 0.98667 val_loss: 0.17339, val_acc: 0.96000
    Epoch [5500/10000], loss: 0.16883 acc: 0.98667 val_loss: 0.17325, val_acc: 0.96000
    Epoch [5510/10000], loss: 0.16867 acc: 0.98667 val_loss: 0.17312, val_acc: 0.96000
    Epoch [5520/10000], loss: 0.16852 acc: 0.98667 val_loss: 0.17299, val_acc: 0.96000
    Epoch [5530/10000], loss: 0.16837 acc: 0.98667 val_loss: 0.17285, val_acc: 0.96000
    Epoch [5540/10000], loss: 0.16822 acc: 0.98667 val_loss: 0.17272, val_acc: 0.96000
    Epoch [5550/10000], loss: 0.16807 acc: 0.98667 val_loss: 0.17259, val_acc: 0.96000
    Epoch [5560/10000], loss: 0.16792 acc: 0.98667 val_loss: 0.17246, val_acc: 0.96000
    Epoch [5570/10000], loss: 0.16777 acc: 0.98667 val_loss: 0.17232, val_acc: 0.96000
    Epoch [5580/10000], loss: 0.16762 acc: 0.98667 val_loss: 0.17219, val_acc: 0.96000
    Epoch [5590/10000], loss: 0.16747 acc: 0.98667 val_loss: 0.17206, val_acc: 0.96000
    Epoch [5600/10000], loss: 0.16732 acc: 0.98667 val_loss: 0.17193, val_acc: 0.96000
    Epoch [5610/10000], loss: 0.16718 acc: 0.98667 val_loss: 0.17180, val_acc: 0.96000
    Epoch [5620/10000], loss: 0.16703 acc: 0.98667 val_loss: 0.17167, val_acc: 0.96000
    Epoch [5630/10000], loss: 0.16688 acc: 0.98667 val_loss: 0.17154, val_acc: 0.96000
    Epoch [5640/10000], loss: 0.16674 acc: 0.98667 val_loss: 0.17141, val_acc: 0.96000
    Epoch [5650/10000], loss: 0.16659 acc: 0.98667 val_loss: 0.17128, val_acc: 0.96000
    Epoch [5660/10000], loss: 0.16644 acc: 0.98667 val_loss: 0.17115, val_acc: 0.96000
    Epoch [5670/10000], loss: 0.16630 acc: 0.98667 val_loss: 0.17103, val_acc: 0.96000
    Epoch [5680/10000], loss: 0.16615 acc: 0.98667 val_loss: 0.17090, val_acc: 0.96000
    Epoch [5690/10000], loss: 0.16601 acc: 0.98667 val_loss: 0.17077, val_acc: 0.96000
    Epoch [5700/10000], loss: 0.16587 acc: 0.98667 val_loss: 0.17064, val_acc: 0.96000
    Epoch [5710/10000], loss: 0.16572 acc: 0.98667 val_loss: 0.17052, val_acc: 0.96000
    Epoch [5720/10000], loss: 0.16558 acc: 0.98667 val_loss: 0.17039, val_acc: 0.96000
    Epoch [5730/10000], loss: 0.16544 acc: 0.98667 val_loss: 0.17027, val_acc: 0.96000
    Epoch [5740/10000], loss: 0.16529 acc: 0.98667 val_loss: 0.17014, val_acc: 0.96000
    Epoch [5750/10000], loss: 0.16515 acc: 0.98667 val_loss: 0.17001, val_acc: 0.96000
    Epoch [5760/10000], loss: 0.16501 acc: 0.98667 val_loss: 0.16989, val_acc: 0.96000
    Epoch [5770/10000], loss: 0.16487 acc: 0.98667 val_loss: 0.16977, val_acc: 0.96000
    Epoch [5780/10000], loss: 0.16473 acc: 0.98667 val_loss: 0.16964, val_acc: 0.96000
    Epoch [5790/10000], loss: 0.16459 acc: 0.98667 val_loss: 0.16952, val_acc: 0.96000
    Epoch [5800/10000], loss: 0.16445 acc: 0.98667 val_loss: 0.16939, val_acc: 0.96000
    Epoch [5810/10000], loss: 0.16431 acc: 0.98667 val_loss: 0.16927, val_acc: 0.96000
    Epoch [5820/10000], loss: 0.16417 acc: 0.98667 val_loss: 0.16915, val_acc: 0.96000
    Epoch [5830/10000], loss: 0.16403 acc: 0.98667 val_loss: 0.16903, val_acc: 0.96000
    Epoch [5840/10000], loss: 0.16389 acc: 0.98667 val_loss: 0.16891, val_acc: 0.96000
    Epoch [5850/10000], loss: 0.16375 acc: 0.98667 val_loss: 0.16878, val_acc: 0.96000
    Epoch [5860/10000], loss: 0.16361 acc: 0.98667 val_loss: 0.16866, val_acc: 0.96000
    Epoch [5870/10000], loss: 0.16348 acc: 0.98667 val_loss: 0.16854, val_acc: 0.96000
    Epoch [5880/10000], loss: 0.16334 acc: 0.98667 val_loss: 0.16842, val_acc: 0.96000
    Epoch [5890/10000], loss: 0.16320 acc: 0.98667 val_loss: 0.16830, val_acc: 0.96000
    Epoch [5900/10000], loss: 0.16307 acc: 0.98667 val_loss: 0.16818, val_acc: 0.96000
    Epoch [5910/10000], loss: 0.16293 acc: 0.98667 val_loss: 0.16806, val_acc: 0.96000
    Epoch [5920/10000], loss: 0.16280 acc: 0.98667 val_loss: 0.16794, val_acc: 0.96000
    Epoch [5930/10000], loss: 0.16266 acc: 0.98667 val_loss: 0.16782, val_acc: 0.96000
    Epoch [5940/10000], loss: 0.16253 acc: 0.98667 val_loss: 0.16771, val_acc: 0.96000
    Epoch [5950/10000], loss: 0.16239 acc: 0.98667 val_loss: 0.16759, val_acc: 0.96000
    Epoch [5960/10000], loss: 0.16226 acc: 0.98667 val_loss: 0.16747, val_acc: 0.96000
    Epoch [5970/10000], loss: 0.16212 acc: 0.98667 val_loss: 0.16735, val_acc: 0.96000
    Epoch [5980/10000], loss: 0.16199 acc: 0.98667 val_loss: 0.16724, val_acc: 0.96000
    Epoch [5990/10000], loss: 0.16186 acc: 0.98667 val_loss: 0.16712, val_acc: 0.96000
    Epoch [6000/10000], loss: 0.16172 acc: 0.98667 val_loss: 0.16700, val_acc: 0.96000
    Epoch [6010/10000], loss: 0.16159 acc: 0.98667 val_loss: 0.16689, val_acc: 0.96000
    Epoch [6020/10000], loss: 0.16146 acc: 0.98667 val_loss: 0.16677, val_acc: 0.96000
    Epoch [6030/10000], loss: 0.16133 acc: 0.98667 val_loss: 0.16665, val_acc: 0.96000
    Epoch [6040/10000], loss: 0.16120 acc: 0.98667 val_loss: 0.16654, val_acc: 0.96000
    Epoch [6050/10000], loss: 0.16107 acc: 0.98667 val_loss: 0.16642, val_acc: 0.96000
    Epoch [6060/10000], loss: 0.16094 acc: 0.98667 val_loss: 0.16631, val_acc: 0.96000
    Epoch [6070/10000], loss: 0.16080 acc: 0.98667 val_loss: 0.16620, val_acc: 0.96000
    Epoch [6080/10000], loss: 0.16067 acc: 0.98667 val_loss: 0.16608, val_acc: 0.96000
    Epoch [6090/10000], loss: 0.16055 acc: 0.98667 val_loss: 0.16597, val_acc: 0.96000
    Epoch [6100/10000], loss: 0.16042 acc: 0.98667 val_loss: 0.16585, val_acc: 0.96000
    Epoch [6110/10000], loss: 0.16029 acc: 0.98667 val_loss: 0.16574, val_acc: 0.96000
    Epoch [6120/10000], loss: 0.16016 acc: 0.98667 val_loss: 0.16563, val_acc: 0.96000
    Epoch [6130/10000], loss: 0.16003 acc: 0.98667 val_loss: 0.16552, val_acc: 0.96000
    Epoch [6140/10000], loss: 0.15990 acc: 0.98667 val_loss: 0.16540, val_acc: 0.96000
    Epoch [6150/10000], loss: 0.15978 acc: 0.98667 val_loss: 0.16529, val_acc: 0.96000
    Epoch [6160/10000], loss: 0.15965 acc: 0.98667 val_loss: 0.16518, val_acc: 0.96000
    Epoch [6170/10000], loss: 0.15952 acc: 0.98667 val_loss: 0.16507, val_acc: 0.96000
    Epoch [6180/10000], loss: 0.15939 acc: 0.98667 val_loss: 0.16496, val_acc: 0.96000
    Epoch [6190/10000], loss: 0.15927 acc: 0.98667 val_loss: 0.16485, val_acc: 0.96000
    Epoch [6200/10000], loss: 0.15914 acc: 0.98667 val_loss: 0.16474, val_acc: 0.96000
    Epoch [6210/10000], loss: 0.15902 acc: 0.98667 val_loss: 0.16463, val_acc: 0.96000
    Epoch [6220/10000], loss: 0.15889 acc: 0.98667 val_loss: 0.16452, val_acc: 0.96000
    Epoch [6230/10000], loss: 0.15877 acc: 0.98667 val_loss: 0.16441, val_acc: 0.96000
    Epoch [6240/10000], loss: 0.15864 acc: 0.98667 val_loss: 0.16430, val_acc: 0.96000
    Epoch [6250/10000], loss: 0.15852 acc: 0.98667 val_loss: 0.16419, val_acc: 0.96000
    Epoch [6260/10000], loss: 0.15839 acc: 0.98667 val_loss: 0.16408, val_acc: 0.96000
    Epoch [6270/10000], loss: 0.15827 acc: 0.98667 val_loss: 0.16398, val_acc: 0.96000
    Epoch [6280/10000], loss: 0.15815 acc: 0.98667 val_loss: 0.16387, val_acc: 0.96000
    Epoch [6290/10000], loss: 0.15802 acc: 0.98667 val_loss: 0.16376, val_acc: 0.96000
    Epoch [6300/10000], loss: 0.15790 acc: 0.98667 val_loss: 0.16365, val_acc: 0.96000
    Epoch [6310/10000], loss: 0.15778 acc: 0.98667 val_loss: 0.16355, val_acc: 0.96000
    Epoch [6320/10000], loss: 0.15766 acc: 0.98667 val_loss: 0.16344, val_acc: 0.96000
    Epoch [6330/10000], loss: 0.15754 acc: 0.98667 val_loss: 0.16333, val_acc: 0.96000
    Epoch [6340/10000], loss: 0.15741 acc: 0.98667 val_loss: 0.16323, val_acc: 0.96000
    Epoch [6350/10000], loss: 0.15729 acc: 0.98667 val_loss: 0.16312, val_acc: 0.96000
    Epoch [6360/10000], loss: 0.15717 acc: 0.98667 val_loss: 0.16302, val_acc: 0.96000
    Epoch [6370/10000], loss: 0.15705 acc: 0.98667 val_loss: 0.16291, val_acc: 0.96000
    Epoch [6380/10000], loss: 0.15693 acc: 0.98667 val_loss: 0.16281, val_acc: 0.96000
    Epoch [6390/10000], loss: 0.15681 acc: 0.98667 val_loss: 0.16270, val_acc: 0.96000
    Epoch [6400/10000], loss: 0.15669 acc: 0.98667 val_loss: 0.16260, val_acc: 0.96000
    Epoch [6410/10000], loss: 0.15657 acc: 0.98667 val_loss: 0.16249, val_acc: 0.96000
    Epoch [6420/10000], loss: 0.15645 acc: 0.98667 val_loss: 0.16239, val_acc: 0.96000
    Epoch [6430/10000], loss: 0.15634 acc: 0.98667 val_loss: 0.16228, val_acc: 0.96000
    Epoch [6440/10000], loss: 0.15622 acc: 0.98667 val_loss: 0.16218, val_acc: 0.96000
    Epoch [6450/10000], loss: 0.15610 acc: 0.98667 val_loss: 0.16208, val_acc: 0.96000
    Epoch [6460/10000], loss: 0.15598 acc: 0.98667 val_loss: 0.16198, val_acc: 0.96000
    Epoch [6470/10000], loss: 0.15586 acc: 0.98667 val_loss: 0.16187, val_acc: 0.96000
    Epoch [6480/10000], loss: 0.15575 acc: 0.98667 val_loss: 0.16177, val_acc: 0.96000
    Epoch [6490/10000], loss: 0.15563 acc: 0.98667 val_loss: 0.16167, val_acc: 0.96000
    Epoch [6500/10000], loss: 0.15551 acc: 0.98667 val_loss: 0.16157, val_acc: 0.96000
    Epoch [6510/10000], loss: 0.15540 acc: 0.98667 val_loss: 0.16147, val_acc: 0.96000
    Epoch [6520/10000], loss: 0.15528 acc: 0.98667 val_loss: 0.16136, val_acc: 0.96000
    Epoch [6530/10000], loss: 0.15516 acc: 0.98667 val_loss: 0.16126, val_acc: 0.96000
    Epoch [6540/10000], loss: 0.15505 acc: 0.98667 val_loss: 0.16116, val_acc: 0.96000
    Epoch [6550/10000], loss: 0.15493 acc: 0.98667 val_loss: 0.16106, val_acc: 0.96000
    Epoch [6560/10000], loss: 0.15482 acc: 0.98667 val_loss: 0.16096, val_acc: 0.96000
    Epoch [6570/10000], loss: 0.15470 acc: 0.98667 val_loss: 0.16086, val_acc: 0.96000
    Epoch [6580/10000], loss: 0.15459 acc: 0.98667 val_loss: 0.16076, val_acc: 0.96000
    Epoch [6590/10000], loss: 0.15448 acc: 0.98667 val_loss: 0.16066, val_acc: 0.96000
    Epoch [6600/10000], loss: 0.15436 acc: 0.98667 val_loss: 0.16056, val_acc: 0.96000
    Epoch [6610/10000], loss: 0.15425 acc: 0.98667 val_loss: 0.16047, val_acc: 0.96000
    Epoch [6620/10000], loss: 0.15414 acc: 0.98667 val_loss: 0.16037, val_acc: 0.96000
    Epoch [6630/10000], loss: 0.15402 acc: 0.98667 val_loss: 0.16027, val_acc: 0.96000
    Epoch [6640/10000], loss: 0.15391 acc: 0.98667 val_loss: 0.16017, val_acc: 0.96000
    Epoch [6650/10000], loss: 0.15380 acc: 0.98667 val_loss: 0.16007, val_acc: 0.96000
    Epoch [6660/10000], loss: 0.15369 acc: 0.98667 val_loss: 0.15998, val_acc: 0.96000
    Epoch [6670/10000], loss: 0.15357 acc: 0.98667 val_loss: 0.15988, val_acc: 0.96000
    Epoch [6680/10000], loss: 0.15346 acc: 0.98667 val_loss: 0.15978, val_acc: 0.96000
    Epoch [6690/10000], loss: 0.15335 acc: 0.98667 val_loss: 0.15968, val_acc: 0.96000
    Epoch [6700/10000], loss: 0.15324 acc: 0.98667 val_loss: 0.15959, val_acc: 0.96000
    Epoch [6710/10000], loss: 0.15313 acc: 0.98667 val_loss: 0.15949, val_acc: 0.96000
    Epoch [6720/10000], loss: 0.15302 acc: 0.98667 val_loss: 0.15939, val_acc: 0.96000
    Epoch [6730/10000], loss: 0.15291 acc: 0.98667 val_loss: 0.15930, val_acc: 0.96000
    Epoch [6740/10000], loss: 0.15280 acc: 0.98667 val_loss: 0.15920, val_acc: 0.96000
    Epoch [6750/10000], loss: 0.15269 acc: 0.98667 val_loss: 0.15911, val_acc: 0.96000
    Epoch [6760/10000], loss: 0.15258 acc: 0.98667 val_loss: 0.15901, val_acc: 0.96000
    Epoch [6770/10000], loss: 0.15247 acc: 0.98667 val_loss: 0.15892, val_acc: 0.96000
    Epoch [6780/10000], loss: 0.15236 acc: 0.98667 val_loss: 0.15882, val_acc: 0.96000
    Epoch [6790/10000], loss: 0.15225 acc: 0.98667 val_loss: 0.15873, val_acc: 0.96000
    Epoch [6800/10000], loss: 0.15215 acc: 0.98667 val_loss: 0.15863, val_acc: 0.96000
    Epoch [6810/10000], loss: 0.15204 acc: 0.98667 val_loss: 0.15854, val_acc: 0.96000
    Epoch [6820/10000], loss: 0.15193 acc: 0.98667 val_loss: 0.15845, val_acc: 0.96000
    Epoch [6830/10000], loss: 0.15182 acc: 0.98667 val_loss: 0.15835, val_acc: 0.96000
    Epoch [6840/10000], loss: 0.15171 acc: 0.98667 val_loss: 0.15826, val_acc: 0.96000
    Epoch [6850/10000], loss: 0.15161 acc: 0.98667 val_loss: 0.15817, val_acc: 0.96000
    Epoch [6860/10000], loss: 0.15150 acc: 0.98667 val_loss: 0.15807, val_acc: 0.96000
    Epoch [6870/10000], loss: 0.15139 acc: 0.98667 val_loss: 0.15798, val_acc: 0.96000
    Epoch [6880/10000], loss: 0.15129 acc: 0.98667 val_loss: 0.15789, val_acc: 0.96000
    Epoch [6890/10000], loss: 0.15118 acc: 0.98667 val_loss: 0.15780, val_acc: 0.96000
    Epoch [6900/10000], loss: 0.15108 acc: 0.98667 val_loss: 0.15771, val_acc: 0.96000
    Epoch [6910/10000], loss: 0.15097 acc: 0.98667 val_loss: 0.15761, val_acc: 0.96000
    Epoch [6920/10000], loss: 0.15086 acc: 0.98667 val_loss: 0.15752, val_acc: 0.96000
    Epoch [6930/10000], loss: 0.15076 acc: 0.98667 val_loss: 0.15743, val_acc: 0.96000
    Epoch [6940/10000], loss: 0.15065 acc: 0.98667 val_loss: 0.15734, val_acc: 0.96000
    Epoch [6950/10000], loss: 0.15055 acc: 0.98667 val_loss: 0.15725, val_acc: 0.96000
    Epoch [6960/10000], loss: 0.15045 acc: 0.98667 val_loss: 0.15716, val_acc: 0.96000
    Epoch [6970/10000], loss: 0.15034 acc: 0.98667 val_loss: 0.15707, val_acc: 0.96000
    Epoch [6980/10000], loss: 0.15024 acc: 0.98667 val_loss: 0.15698, val_acc: 0.96000
    Epoch [6990/10000], loss: 0.15013 acc: 0.98667 val_loss: 0.15689, val_acc: 0.96000
    Epoch [7000/10000], loss: 0.15003 acc: 0.98667 val_loss: 0.15680, val_acc: 0.96000
    Epoch [7010/10000], loss: 0.14993 acc: 0.98667 val_loss: 0.15671, val_acc: 0.96000
    Epoch [7020/10000], loss: 0.14983 acc: 0.98667 val_loss: 0.15662, val_acc: 0.96000
    Epoch [7030/10000], loss: 0.14972 acc: 0.98667 val_loss: 0.15653, val_acc: 0.96000
    Epoch [7040/10000], loss: 0.14962 acc: 0.98667 val_loss: 0.15644, val_acc: 0.96000
    Epoch [7050/10000], loss: 0.14952 acc: 0.98667 val_loss: 0.15636, val_acc: 0.96000
    Epoch [7060/10000], loss: 0.14942 acc: 0.98667 val_loss: 0.15627, val_acc: 0.96000
    Epoch [7070/10000], loss: 0.14931 acc: 0.98667 val_loss: 0.15618, val_acc: 0.96000
    Epoch [7080/10000], loss: 0.14921 acc: 0.98667 val_loss: 0.15609, val_acc: 0.96000
    Epoch [7090/10000], loss: 0.14911 acc: 0.98667 val_loss: 0.15600, val_acc: 0.96000
    Epoch [7100/10000], loss: 0.14901 acc: 0.98667 val_loss: 0.15592, val_acc: 0.96000
    Epoch [7110/10000], loss: 0.14891 acc: 0.98667 val_loss: 0.15583, val_acc: 0.96000
    Epoch [7120/10000], loss: 0.14881 acc: 0.98667 val_loss: 0.15574, val_acc: 0.96000
    Epoch [7130/10000], loss: 0.14871 acc: 0.98667 val_loss: 0.15565, val_acc: 0.96000
    Epoch [7140/10000], loss: 0.14861 acc: 0.98667 val_loss: 0.15557, val_acc: 0.96000
    Epoch [7150/10000], loss: 0.14851 acc: 0.98667 val_loss: 0.15548, val_acc: 0.96000
    Epoch [7160/10000], loss: 0.14841 acc: 0.98667 val_loss: 0.15540, val_acc: 0.96000
    Epoch [7170/10000], loss: 0.14831 acc: 0.98667 val_loss: 0.15531, val_acc: 0.96000
    Epoch [7180/10000], loss: 0.14821 acc: 0.98667 val_loss: 0.15522, val_acc: 0.96000
    Epoch [7190/10000], loss: 0.14811 acc: 0.98667 val_loss: 0.15514, val_acc: 0.96000
    Epoch [7200/10000], loss: 0.14801 acc: 0.98667 val_loss: 0.15505, val_acc: 0.96000
    Epoch [7210/10000], loss: 0.14792 acc: 0.98667 val_loss: 0.15497, val_acc: 0.96000
    Epoch [7220/10000], loss: 0.14782 acc: 0.98667 val_loss: 0.15488, val_acc: 0.96000
    Epoch [7230/10000], loss: 0.14772 acc: 0.98667 val_loss: 0.15480, val_acc: 0.96000
    Epoch [7240/10000], loss: 0.14762 acc: 0.98667 val_loss: 0.15471, val_acc: 0.96000
    Epoch [7250/10000], loss: 0.14752 acc: 0.98667 val_loss: 0.15463, val_acc: 0.96000
    Epoch [7260/10000], loss: 0.14743 acc: 0.98667 val_loss: 0.15455, val_acc: 0.96000
    Epoch [7270/10000], loss: 0.14733 acc: 0.98667 val_loss: 0.15446, val_acc: 0.96000
    Epoch [7280/10000], loss: 0.14723 acc: 0.98667 val_loss: 0.15438, val_acc: 0.96000
    Epoch [7290/10000], loss: 0.14714 acc: 0.98667 val_loss: 0.15429, val_acc: 0.96000
    Epoch [7300/10000], loss: 0.14704 acc: 0.98667 val_loss: 0.15421, val_acc: 0.96000
    Epoch [7310/10000], loss: 0.14694 acc: 0.98667 val_loss: 0.15413, val_acc: 0.96000
    Epoch [7320/10000], loss: 0.14685 acc: 0.98667 val_loss: 0.15404, val_acc: 0.96000
    Epoch [7330/10000], loss: 0.14675 acc: 0.98667 val_loss: 0.15396, val_acc: 0.96000
    Epoch [7340/10000], loss: 0.14666 acc: 0.98667 val_loss: 0.15388, val_acc: 0.96000
    Epoch [7350/10000], loss: 0.14656 acc: 0.98667 val_loss: 0.15380, val_acc: 0.96000
    Epoch [7360/10000], loss: 0.14646 acc: 0.98667 val_loss: 0.15371, val_acc: 0.96000
    Epoch [7370/10000], loss: 0.14637 acc: 0.98667 val_loss: 0.15363, val_acc: 0.96000
    Epoch [7380/10000], loss: 0.14627 acc: 0.98667 val_loss: 0.15355, val_acc: 0.96000
    Epoch [7390/10000], loss: 0.14618 acc: 0.98667 val_loss: 0.15347, val_acc: 0.96000
    Epoch [7400/10000], loss: 0.14609 acc: 0.98667 val_loss: 0.15339, val_acc: 0.96000
    Epoch [7410/10000], loss: 0.14599 acc: 0.98667 val_loss: 0.15331, val_acc: 0.96000
    Epoch [7420/10000], loss: 0.14590 acc: 0.98667 val_loss: 0.15323, val_acc: 0.96000
    Epoch [7430/10000], loss: 0.14580 acc: 0.98667 val_loss: 0.15314, val_acc: 0.96000
    Epoch [7440/10000], loss: 0.14571 acc: 0.98667 val_loss: 0.15306, val_acc: 0.96000
    Epoch [7450/10000], loss: 0.14562 acc: 0.98667 val_loss: 0.15298, val_acc: 0.96000
    Epoch [7460/10000], loss: 0.14552 acc: 0.98667 val_loss: 0.15290, val_acc: 0.96000
    Epoch [7470/10000], loss: 0.14543 acc: 0.98667 val_loss: 0.15282, val_acc: 0.96000
    Epoch [7480/10000], loss: 0.14534 acc: 0.98667 val_loss: 0.15274, val_acc: 0.96000
    Epoch [7490/10000], loss: 0.14525 acc: 0.98667 val_loss: 0.15266, val_acc: 0.96000
    Epoch [7500/10000], loss: 0.14515 acc: 0.98667 val_loss: 0.15258, val_acc: 0.96000
    Epoch [7510/10000], loss: 0.14506 acc: 0.98667 val_loss: 0.15250, val_acc: 0.96000
    Epoch [7520/10000], loss: 0.14497 acc: 0.98667 val_loss: 0.15243, val_acc: 0.96000
    Epoch [7530/10000], loss: 0.14488 acc: 0.98667 val_loss: 0.15235, val_acc: 0.96000
    Epoch [7540/10000], loss: 0.14479 acc: 0.98667 val_loss: 0.15227, val_acc: 0.96000
    Epoch [7550/10000], loss: 0.14470 acc: 0.98667 val_loss: 0.15219, val_acc: 0.96000
    Epoch [7560/10000], loss: 0.14460 acc: 0.98667 val_loss: 0.15211, val_acc: 0.96000
    Epoch [7570/10000], loss: 0.14451 acc: 0.98667 val_loss: 0.15203, val_acc: 0.96000
    Epoch [7580/10000], loss: 0.14442 acc: 0.98667 val_loss: 0.15195, val_acc: 0.96000
    Epoch [7590/10000], loss: 0.14433 acc: 0.98667 val_loss: 0.15188, val_acc: 0.96000
    Epoch [7600/10000], loss: 0.14424 acc: 0.98667 val_loss: 0.15180, val_acc: 0.96000
    Epoch [7610/10000], loss: 0.14415 acc: 0.98667 val_loss: 0.15172, val_acc: 0.96000
    Epoch [7620/10000], loss: 0.14406 acc: 0.98667 val_loss: 0.15164, val_acc: 0.96000
    Epoch [7630/10000], loss: 0.14397 acc: 0.98667 val_loss: 0.15157, val_acc: 0.96000
    Epoch [7640/10000], loss: 0.14388 acc: 0.98667 val_loss: 0.15149, val_acc: 0.96000
    Epoch [7650/10000], loss: 0.14379 acc: 0.98667 val_loss: 0.15141, val_acc: 0.96000
    Epoch [7660/10000], loss: 0.14370 acc: 0.98667 val_loss: 0.15134, val_acc: 0.96000
    Epoch [7670/10000], loss: 0.14362 acc: 0.98667 val_loss: 0.15126, val_acc: 0.96000
    Epoch [7680/10000], loss: 0.14353 acc: 0.98667 val_loss: 0.15118, val_acc: 0.96000
    Epoch [7690/10000], loss: 0.14344 acc: 0.98667 val_loss: 0.15111, val_acc: 0.96000
    Epoch [7700/10000], loss: 0.14335 acc: 0.98667 val_loss: 0.15103, val_acc: 0.96000
    Epoch [7710/10000], loss: 0.14326 acc: 0.98667 val_loss: 0.15096, val_acc: 0.96000
    Epoch [7720/10000], loss: 0.14317 acc: 0.98667 val_loss: 0.15088, val_acc: 0.96000
    Epoch [7730/10000], loss: 0.14309 acc: 0.98667 val_loss: 0.15080, val_acc: 0.96000
    Epoch [7740/10000], loss: 0.14300 acc: 0.98667 val_loss: 0.15073, val_acc: 0.96000
    Epoch [7750/10000], loss: 0.14291 acc: 0.98667 val_loss: 0.15065, val_acc: 0.96000
    Epoch [7760/10000], loss: 0.14282 acc: 0.98667 val_loss: 0.15058, val_acc: 0.96000
    Epoch [7770/10000], loss: 0.14274 acc: 0.98667 val_loss: 0.15050, val_acc: 0.96000
    Epoch [7780/10000], loss: 0.14265 acc: 0.98667 val_loss: 0.15043, val_acc: 0.96000
    Epoch [7790/10000], loss: 0.14256 acc: 0.98667 val_loss: 0.15036, val_acc: 0.96000
    Epoch [7800/10000], loss: 0.14248 acc: 0.98667 val_loss: 0.15028, val_acc: 0.96000
    Epoch [7810/10000], loss: 0.14239 acc: 0.98667 val_loss: 0.15021, val_acc: 0.96000
    Epoch [7820/10000], loss: 0.14230 acc: 0.98667 val_loss: 0.15013, val_acc: 0.96000
    Epoch [7830/10000], loss: 0.14222 acc: 0.98667 val_loss: 0.15006, val_acc: 0.96000
    Epoch [7840/10000], loss: 0.14213 acc: 0.98667 val_loss: 0.14999, val_acc: 0.96000
    Epoch [7850/10000], loss: 0.14205 acc: 0.98667 val_loss: 0.14991, val_acc: 0.96000
    Epoch [7860/10000], loss: 0.14196 acc: 0.98667 val_loss: 0.14984, val_acc: 0.96000
    Epoch [7870/10000], loss: 0.14188 acc: 0.98667 val_loss: 0.14977, val_acc: 0.96000
    Epoch [7880/10000], loss: 0.14179 acc: 0.98667 val_loss: 0.14969, val_acc: 0.96000
    Epoch [7890/10000], loss: 0.14171 acc: 0.98667 val_loss: 0.14962, val_acc: 0.96000
    Epoch [7900/10000], loss: 0.14162 acc: 0.98667 val_loss: 0.14955, val_acc: 0.96000
    Epoch [7910/10000], loss: 0.14154 acc: 0.98667 val_loss: 0.14948, val_acc: 0.96000
    Epoch [7920/10000], loss: 0.14145 acc: 0.98667 val_loss: 0.14940, val_acc: 0.96000
    Epoch [7930/10000], loss: 0.14137 acc: 0.98667 val_loss: 0.14933, val_acc: 0.96000
    Epoch [7940/10000], loss: 0.14128 acc: 0.98667 val_loss: 0.14926, val_acc: 0.96000
    Epoch [7950/10000], loss: 0.14120 acc: 0.98667 val_loss: 0.14919, val_acc: 0.96000
    Epoch [7960/10000], loss: 0.14112 acc: 0.98667 val_loss: 0.14912, val_acc: 0.96000
    Epoch [7970/10000], loss: 0.14103 acc: 0.98667 val_loss: 0.14904, val_acc: 0.96000
    Epoch [7980/10000], loss: 0.14095 acc: 0.98667 val_loss: 0.14897, val_acc: 0.96000
    Epoch [7990/10000], loss: 0.14087 acc: 0.98667 val_loss: 0.14890, val_acc: 0.96000
    Epoch [8000/10000], loss: 0.14078 acc: 0.98667 val_loss: 0.14883, val_acc: 0.96000
    Epoch [8010/10000], loss: 0.14070 acc: 0.98667 val_loss: 0.14876, val_acc: 0.96000
    Epoch [8020/10000], loss: 0.14062 acc: 0.98667 val_loss: 0.14869, val_acc: 0.96000
    Epoch [8030/10000], loss: 0.14054 acc: 0.98667 val_loss: 0.14862, val_acc: 0.96000
    Epoch [8040/10000], loss: 0.14045 acc: 0.98667 val_loss: 0.14855, val_acc: 0.96000
    Epoch [8050/10000], loss: 0.14037 acc: 0.98667 val_loss: 0.14848, val_acc: 0.96000
    Epoch [8060/10000], loss: 0.14029 acc: 0.98667 val_loss: 0.14841, val_acc: 0.96000
    Epoch [8070/10000], loss: 0.14021 acc: 0.98667 val_loss: 0.14834, val_acc: 0.96000
    Epoch [8080/10000], loss: 0.14013 acc: 0.98667 val_loss: 0.14827, val_acc: 0.96000
    Epoch [8090/10000], loss: 0.14004 acc: 0.98667 val_loss: 0.14820, val_acc: 0.96000
    Epoch [8100/10000], loss: 0.13996 acc: 0.98667 val_loss: 0.14813, val_acc: 0.96000
    Epoch [8110/10000], loss: 0.13988 acc: 0.98667 val_loss: 0.14806, val_acc: 0.96000
    Epoch [8120/10000], loss: 0.13980 acc: 0.98667 val_loss: 0.14799, val_acc: 0.96000
    Epoch [8130/10000], loss: 0.13972 acc: 0.98667 val_loss: 0.14792, val_acc: 0.96000
    Epoch [8140/10000], loss: 0.13964 acc: 0.98667 val_loss: 0.14785, val_acc: 0.96000
    Epoch [8150/10000], loss: 0.13956 acc: 0.98667 val_loss: 0.14778, val_acc: 0.96000
    Epoch [8160/10000], loss: 0.13948 acc: 0.98667 val_loss: 0.14771, val_acc: 0.96000
    Epoch [8170/10000], loss: 0.13940 acc: 0.98667 val_loss: 0.14765, val_acc: 0.96000
    Epoch [8180/10000], loss: 0.13932 acc: 0.98667 val_loss: 0.14758, val_acc: 0.96000
    Epoch [8190/10000], loss: 0.13924 acc: 0.98667 val_loss: 0.14751, val_acc: 0.96000
    Epoch [8200/10000], loss: 0.13916 acc: 0.98667 val_loss: 0.14744, val_acc: 0.96000
    Epoch [8210/10000], loss: 0.13908 acc: 0.98667 val_loss: 0.14737, val_acc: 0.96000
    Epoch [8220/10000], loss: 0.13900 acc: 0.98667 val_loss: 0.14731, val_acc: 0.96000
    Epoch [8230/10000], loss: 0.13892 acc: 0.98667 val_loss: 0.14724, val_acc: 0.96000
    Epoch [8240/10000], loss: 0.13884 acc: 0.98667 val_loss: 0.14717, val_acc: 0.96000
    Epoch [8250/10000], loss: 0.13876 acc: 0.98667 val_loss: 0.14710, val_acc: 0.96000
    Epoch [8260/10000], loss: 0.13869 acc: 0.98667 val_loss: 0.14704, val_acc: 0.96000
    Epoch [8270/10000], loss: 0.13861 acc: 0.98667 val_loss: 0.14697, val_acc: 0.96000
    Epoch [8280/10000], loss: 0.13853 acc: 0.98667 val_loss: 0.14690, val_acc: 0.96000
    Epoch [8290/10000], loss: 0.13845 acc: 0.98667 val_loss: 0.14684, val_acc: 0.96000
    Epoch [8300/10000], loss: 0.13837 acc: 0.98667 val_loss: 0.14677, val_acc: 0.96000
    Epoch [8310/10000], loss: 0.13829 acc: 0.98667 val_loss: 0.14670, val_acc: 0.96000
    Epoch [8320/10000], loss: 0.13822 acc: 0.98667 val_loss: 0.14664, val_acc: 0.96000
    Epoch [8330/10000], loss: 0.13814 acc: 0.98667 val_loss: 0.14657, val_acc: 0.96000
    Epoch [8340/10000], loss: 0.13806 acc: 0.98667 val_loss: 0.14650, val_acc: 0.96000
    Epoch [8350/10000], loss: 0.13798 acc: 0.98667 val_loss: 0.14644, val_acc: 0.96000
    Epoch [8360/10000], loss: 0.13791 acc: 0.98667 val_loss: 0.14637, val_acc: 0.96000
    Epoch [8370/10000], loss: 0.13783 acc: 0.98667 val_loss: 0.14631, val_acc: 0.96000
    Epoch [8380/10000], loss: 0.13775 acc: 0.98667 val_loss: 0.14624, val_acc: 0.96000
    Epoch [8390/10000], loss: 0.13768 acc: 0.98667 val_loss: 0.14618, val_acc: 0.96000
    Epoch [8400/10000], loss: 0.13760 acc: 0.98667 val_loss: 0.14611, val_acc: 0.96000
    Epoch [8410/10000], loss: 0.13752 acc: 0.98667 val_loss: 0.14605, val_acc: 0.96000
    Epoch [8420/10000], loss: 0.13745 acc: 0.98667 val_loss: 0.14598, val_acc: 0.96000
    Epoch [8430/10000], loss: 0.13737 acc: 0.98667 val_loss: 0.14592, val_acc: 0.96000
    Epoch [8440/10000], loss: 0.13730 acc: 0.98667 val_loss: 0.14585, val_acc: 0.96000
    Epoch [8450/10000], loss: 0.13722 acc: 0.98667 val_loss: 0.14579, val_acc: 0.96000
    Epoch [8460/10000], loss: 0.13714 acc: 0.98667 val_loss: 0.14572, val_acc: 0.96000
    Epoch [8470/10000], loss: 0.13707 acc: 0.98667 val_loss: 0.14566, val_acc: 0.96000
    Epoch [8480/10000], loss: 0.13699 acc: 0.98667 val_loss: 0.14559, val_acc: 0.96000
    Epoch [8490/10000], loss: 0.13692 acc: 0.98667 val_loss: 0.14553, val_acc: 0.96000
    Epoch [8500/10000], loss: 0.13684 acc: 0.98667 val_loss: 0.14547, val_acc: 0.96000
    Epoch [8510/10000], loss: 0.13677 acc: 0.98667 val_loss: 0.14540, val_acc: 0.96000
    Epoch [8520/10000], loss: 0.13669 acc: 0.98667 val_loss: 0.14534, val_acc: 0.96000
    Epoch [8530/10000], loss: 0.13662 acc: 0.98667 val_loss: 0.14528, val_acc: 0.96000
    Epoch [8540/10000], loss: 0.13654 acc: 0.98667 val_loss: 0.14521, val_acc: 0.96000
    Epoch [8550/10000], loss: 0.13647 acc: 0.98667 val_loss: 0.14515, val_acc: 0.96000
    Epoch [8560/10000], loss: 0.13640 acc: 0.98667 val_loss: 0.14509, val_acc: 0.96000
    Epoch [8570/10000], loss: 0.13632 acc: 0.98667 val_loss: 0.14502, val_acc: 0.96000
    Epoch [8580/10000], loss: 0.13625 acc: 0.98667 val_loss: 0.14496, val_acc: 0.96000
    Epoch [8590/10000], loss: 0.13617 acc: 0.98667 val_loss: 0.14490, val_acc: 0.96000
    Epoch [8600/10000], loss: 0.13610 acc: 0.98667 val_loss: 0.14483, val_acc: 0.96000
    Epoch [8610/10000], loss: 0.13603 acc: 0.98667 val_loss: 0.14477, val_acc: 0.96000
    Epoch [8620/10000], loss: 0.13595 acc: 0.98667 val_loss: 0.14471, val_acc: 0.96000
    Epoch [8630/10000], loss: 0.13588 acc: 0.98667 val_loss: 0.14465, val_acc: 0.96000
    Epoch [8640/10000], loss: 0.13581 acc: 0.98667 val_loss: 0.14459, val_acc: 0.96000
    Epoch [8650/10000], loss: 0.13574 acc: 0.98667 val_loss: 0.14452, val_acc: 0.96000
    Epoch [8660/10000], loss: 0.13566 acc: 0.98667 val_loss: 0.14446, val_acc: 0.96000
    Epoch [8670/10000], loss: 0.13559 acc: 0.98667 val_loss: 0.14440, val_acc: 0.96000
    Epoch [8680/10000], loss: 0.13552 acc: 0.98667 val_loss: 0.14434, val_acc: 0.96000
    Epoch [8690/10000], loss: 0.13545 acc: 0.98667 val_loss: 0.14428, val_acc: 0.96000
    Epoch [8700/10000], loss: 0.13537 acc: 0.98667 val_loss: 0.14422, val_acc: 0.96000
    Epoch [8710/10000], loss: 0.13530 acc: 0.98667 val_loss: 0.14415, val_acc: 0.96000
    Epoch [8720/10000], loss: 0.13523 acc: 0.98667 val_loss: 0.14409, val_acc: 0.96000
    Epoch [8730/10000], loss: 0.13516 acc: 0.98667 val_loss: 0.14403, val_acc: 0.96000
    Epoch [8740/10000], loss: 0.13509 acc: 0.98667 val_loss: 0.14397, val_acc: 0.96000
    Epoch [8750/10000], loss: 0.13501 acc: 0.98667 val_loss: 0.14391, val_acc: 0.96000
    Epoch [8760/10000], loss: 0.13494 acc: 0.98667 val_loss: 0.14385, val_acc: 0.96000
    Epoch [8770/10000], loss: 0.13487 acc: 0.98667 val_loss: 0.14379, val_acc: 0.96000
    Epoch [8780/10000], loss: 0.13480 acc: 0.98667 val_loss: 0.14373, val_acc: 0.96000
    Epoch [8790/10000], loss: 0.13473 acc: 0.98667 val_loss: 0.14367, val_acc: 0.96000
    Epoch [8800/10000], loss: 0.13466 acc: 0.98667 val_loss: 0.14361, val_acc: 0.96000
    Epoch [8810/10000], loss: 0.13459 acc: 0.98667 val_loss: 0.14355, val_acc: 0.96000
    Epoch [8820/10000], loss: 0.13452 acc: 0.98667 val_loss: 0.14349, val_acc: 0.96000
    Epoch [8830/10000], loss: 0.13445 acc: 0.98667 val_loss: 0.14343, val_acc: 0.96000
    Epoch [8840/10000], loss: 0.13438 acc: 0.98667 val_loss: 0.14337, val_acc: 0.96000
    Epoch [8850/10000], loss: 0.13431 acc: 0.98667 val_loss: 0.14331, val_acc: 0.96000
    Epoch [8860/10000], loss: 0.13424 acc: 0.98667 val_loss: 0.14325, val_acc: 0.96000
    Epoch [8870/10000], loss: 0.13417 acc: 0.98667 val_loss: 0.14319, val_acc: 0.96000
    Epoch [8880/10000], loss: 0.13410 acc: 0.98667 val_loss: 0.14313, val_acc: 0.96000
    Epoch [8890/10000], loss: 0.13403 acc: 0.98667 val_loss: 0.14308, val_acc: 0.96000
    Epoch [8900/10000], loss: 0.13396 acc: 0.98667 val_loss: 0.14302, val_acc: 0.96000
    Epoch [8910/10000], loss: 0.13389 acc: 0.98667 val_loss: 0.14296, val_acc: 0.96000
    Epoch [8920/10000], loss: 0.13382 acc: 0.98667 val_loss: 0.14290, val_acc: 0.96000
    Epoch [8930/10000], loss: 0.13375 acc: 0.98667 val_loss: 0.14284, val_acc: 0.96000
    Epoch [8940/10000], loss: 0.13368 acc: 0.98667 val_loss: 0.14278, val_acc: 0.96000
    Epoch [8950/10000], loss: 0.13361 acc: 0.98667 val_loss: 0.14272, val_acc: 0.96000
    Epoch [8960/10000], loss: 0.13354 acc: 0.98667 val_loss: 0.14266, val_acc: 0.96000
    Epoch [8970/10000], loss: 0.13347 acc: 0.98667 val_loss: 0.14261, val_acc: 0.96000
    Epoch [8980/10000], loss: 0.13341 acc: 0.98667 val_loss: 0.14255, val_acc: 0.96000
    Epoch [8990/10000], loss: 0.13334 acc: 0.98667 val_loss: 0.14249, val_acc: 0.96000
    Epoch [9000/10000], loss: 0.13327 acc: 0.98667 val_loss: 0.14243, val_acc: 0.96000
    Epoch [9010/10000], loss: 0.13320 acc: 0.98667 val_loss: 0.14238, val_acc: 0.96000
    Epoch [9020/10000], loss: 0.13313 acc: 0.98667 val_loss: 0.14232, val_acc: 0.96000
    Epoch [9030/10000], loss: 0.13307 acc: 0.98667 val_loss: 0.14226, val_acc: 0.96000
    Epoch [9040/10000], loss: 0.13300 acc: 0.98667 val_loss: 0.14220, val_acc: 0.96000
    Epoch [9050/10000], loss: 0.13293 acc: 0.98667 val_loss: 0.14215, val_acc: 0.96000
    Epoch [9060/10000], loss: 0.13286 acc: 0.98667 val_loss: 0.14209, val_acc: 0.96000
    Epoch [9070/10000], loss: 0.13280 acc: 0.98667 val_loss: 0.14203, val_acc: 0.96000
    Epoch [9080/10000], loss: 0.13273 acc: 0.98667 val_loss: 0.14198, val_acc: 0.96000
    Epoch [9090/10000], loss: 0.13266 acc: 0.98667 val_loss: 0.14192, val_acc: 0.96000
    Epoch [9100/10000], loss: 0.13259 acc: 0.98667 val_loss: 0.14186, val_acc: 0.96000
    Epoch [9110/10000], loss: 0.13253 acc: 0.98667 val_loss: 0.14181, val_acc: 0.96000
    Epoch [9120/10000], loss: 0.13246 acc: 0.98667 val_loss: 0.14175, val_acc: 0.96000
    Epoch [9130/10000], loss: 0.13239 acc: 0.98667 val_loss: 0.14169, val_acc: 0.96000
    Epoch [9140/10000], loss: 0.13233 acc: 0.98667 val_loss: 0.14164, val_acc: 0.96000
    Epoch [9150/10000], loss: 0.13226 acc: 0.98667 val_loss: 0.14158, val_acc: 0.96000
    Epoch [9160/10000], loss: 0.13220 acc: 0.98667 val_loss: 0.14153, val_acc: 0.96000
    Epoch [9170/10000], loss: 0.13213 acc: 0.98667 val_loss: 0.14147, val_acc: 0.96000
    Epoch [9180/10000], loss: 0.13206 acc: 0.98667 val_loss: 0.14141, val_acc: 0.96000
    Epoch [9190/10000], loss: 0.13200 acc: 0.98667 val_loss: 0.14136, val_acc: 0.96000
    Epoch [9200/10000], loss: 0.13193 acc: 0.98667 val_loss: 0.14130, val_acc: 0.96000
    Epoch [9210/10000], loss: 0.13187 acc: 0.98667 val_loss: 0.14125, val_acc: 0.96000
    Epoch [9220/10000], loss: 0.13180 acc: 0.98667 val_loss: 0.14119, val_acc: 0.96000
    Epoch [9230/10000], loss: 0.13174 acc: 0.98667 val_loss: 0.14114, val_acc: 0.96000
    Epoch [9240/10000], loss: 0.13167 acc: 0.98667 val_loss: 0.14108, val_acc: 0.96000
    Epoch [9250/10000], loss: 0.13160 acc: 0.98667 val_loss: 0.14103, val_acc: 0.96000
    Epoch [9260/10000], loss: 0.13154 acc: 0.98667 val_loss: 0.14097, val_acc: 0.96000
    Epoch [9270/10000], loss: 0.13147 acc: 0.98667 val_loss: 0.14092, val_acc: 0.96000
    Epoch [9280/10000], loss: 0.13141 acc: 0.98667 val_loss: 0.14086, val_acc: 0.96000
    Epoch [9290/10000], loss: 0.13135 acc: 0.98667 val_loss: 0.14081, val_acc: 0.96000
    Epoch [9300/10000], loss: 0.13128 acc: 0.98667 val_loss: 0.14075, val_acc: 0.96000
    Epoch [9310/10000], loss: 0.13122 acc: 0.98667 val_loss: 0.14070, val_acc: 0.96000
    Epoch [9320/10000], loss: 0.13115 acc: 0.98667 val_loss: 0.14065, val_acc: 0.96000
    Epoch [9330/10000], loss: 0.13109 acc: 0.98667 val_loss: 0.14059, val_acc: 0.96000
    Epoch [9340/10000], loss: 0.13102 acc: 0.98667 val_loss: 0.14054, val_acc: 0.96000
    Epoch [9350/10000], loss: 0.13096 acc: 0.98667 val_loss: 0.14048, val_acc: 0.96000
    Epoch [9360/10000], loss: 0.13090 acc: 0.98667 val_loss: 0.14043, val_acc: 0.96000
    Epoch [9370/10000], loss: 0.13083 acc: 0.98667 val_loss: 0.14038, val_acc: 0.96000
    Epoch [9380/10000], loss: 0.13077 acc: 0.98667 val_loss: 0.14032, val_acc: 0.96000
    Epoch [9390/10000], loss: 0.13070 acc: 0.98667 val_loss: 0.14027, val_acc: 0.96000
    Epoch [9400/10000], loss: 0.13064 acc: 0.98667 val_loss: 0.14022, val_acc: 0.96000
    Epoch [9410/10000], loss: 0.13058 acc: 0.98667 val_loss: 0.14016, val_acc: 0.96000
    Epoch [9420/10000], loss: 0.13051 acc: 0.98667 val_loss: 0.14011, val_acc: 0.96000
    Epoch [9430/10000], loss: 0.13045 acc: 0.98667 val_loss: 0.14006, val_acc: 0.96000
    Epoch [9440/10000], loss: 0.13039 acc: 0.98667 val_loss: 0.14000, val_acc: 0.96000
    Epoch [9450/10000], loss: 0.13033 acc: 0.98667 val_loss: 0.13995, val_acc: 0.96000
    Epoch [9460/10000], loss: 0.13026 acc: 0.98667 val_loss: 0.13990, val_acc: 0.96000
    Epoch [9470/10000], loss: 0.13020 acc: 0.98667 val_loss: 0.13984, val_acc: 0.96000
    Epoch [9480/10000], loss: 0.13014 acc: 0.98667 val_loss: 0.13979, val_acc: 0.96000
    Epoch [9490/10000], loss: 0.13008 acc: 0.98667 val_loss: 0.13974, val_acc: 0.96000
    Epoch [9500/10000], loss: 0.13001 acc: 0.98667 val_loss: 0.13969, val_acc: 0.96000
    Epoch [9510/10000], loss: 0.12995 acc: 0.98667 val_loss: 0.13963, val_acc: 0.96000
    Epoch [9520/10000], loss: 0.12989 acc: 0.98667 val_loss: 0.13958, val_acc: 0.96000
    Epoch [9530/10000], loss: 0.12983 acc: 0.98667 val_loss: 0.13953, val_acc: 0.96000
    Epoch [9540/10000], loss: 0.12976 acc: 0.98667 val_loss: 0.13948, val_acc: 0.96000
    Epoch [9550/10000], loss: 0.12970 acc: 0.98667 val_loss: 0.13943, val_acc: 0.96000
    Epoch [9560/10000], loss: 0.12964 acc: 0.98667 val_loss: 0.13937, val_acc: 0.96000
    Epoch [9570/10000], loss: 0.12958 acc: 0.98667 val_loss: 0.13932, val_acc: 0.96000
    Epoch [9580/10000], loss: 0.12952 acc: 0.98667 val_loss: 0.13927, val_acc: 0.96000
    Epoch [9590/10000], loss: 0.12946 acc: 0.98667 val_loss: 0.13922, val_acc: 0.96000
    Epoch [9600/10000], loss: 0.12940 acc: 0.98667 val_loss: 0.13917, val_acc: 0.96000
    Epoch [9610/10000], loss: 0.12933 acc: 0.98667 val_loss: 0.13912, val_acc: 0.96000
    Epoch [9620/10000], loss: 0.12927 acc: 0.98667 val_loss: 0.13907, val_acc: 0.96000
    Epoch [9630/10000], loss: 0.12921 acc: 0.98667 val_loss: 0.13901, val_acc: 0.96000
    Epoch [9640/10000], loss: 0.12915 acc: 0.98667 val_loss: 0.13896, val_acc: 0.96000
    Epoch [9650/10000], loss: 0.12909 acc: 0.98667 val_loss: 0.13891, val_acc: 0.96000
    Epoch [9660/10000], loss: 0.12903 acc: 0.98667 val_loss: 0.13886, val_acc: 0.96000
    Epoch [9670/10000], loss: 0.12897 acc: 0.98667 val_loss: 0.13881, val_acc: 0.96000
    Epoch [9680/10000], loss: 0.12891 acc: 0.98667 val_loss: 0.13876, val_acc: 0.96000
    Epoch [9690/10000], loss: 0.12885 acc: 0.98667 val_loss: 0.13871, val_acc: 0.96000
    Epoch [9700/10000], loss: 0.12879 acc: 0.98667 val_loss: 0.13866, val_acc: 0.96000
    Epoch [9710/10000], loss: 0.12873 acc: 0.98667 val_loss: 0.13861, val_acc: 0.96000
    Epoch [9720/10000], loss: 0.12867 acc: 0.98667 val_loss: 0.13856, val_acc: 0.96000
    Epoch [9730/10000], loss: 0.12861 acc: 0.98667 val_loss: 0.13851, val_acc: 0.96000
    Epoch [9740/10000], loss: 0.12855 acc: 0.98667 val_loss: 0.13846, val_acc: 0.96000
    Epoch [9750/10000], loss: 0.12849 acc: 0.98667 val_loss: 0.13841, val_acc: 0.96000
    Epoch [9760/10000], loss: 0.12843 acc: 0.98667 val_loss: 0.13836, val_acc: 0.96000
    Epoch [9770/10000], loss: 0.12837 acc: 0.98667 val_loss: 0.13831, val_acc: 0.96000
    Epoch [9780/10000], loss: 0.12831 acc: 0.98667 val_loss: 0.13826, val_acc: 0.96000
    Epoch [9790/10000], loss: 0.12825 acc: 0.98667 val_loss: 0.13821, val_acc: 0.96000
    Epoch [9800/10000], loss: 0.12819 acc: 0.98667 val_loss: 0.13816, val_acc: 0.96000
    Epoch [9810/10000], loss: 0.12813 acc: 0.98667 val_loss: 0.13811, val_acc: 0.96000
    Epoch [9820/10000], loss: 0.12808 acc: 0.98667 val_loss: 0.13806, val_acc: 0.96000
    Epoch [9830/10000], loss: 0.12802 acc: 0.98667 val_loss: 0.13801, val_acc: 0.96000
    Epoch [9840/10000], loss: 0.12796 acc: 0.98667 val_loss: 0.13796, val_acc: 0.96000
    Epoch [9850/10000], loss: 0.12790 acc: 0.98667 val_loss: 0.13791, val_acc: 0.96000
    Epoch [9860/10000], loss: 0.12784 acc: 0.98667 val_loss: 0.13786, val_acc: 0.96000
    Epoch [9870/10000], loss: 0.12778 acc: 0.98667 val_loss: 0.13782, val_acc: 0.96000
    Epoch [9880/10000], loss: 0.12772 acc: 0.98667 val_loss: 0.13777, val_acc: 0.96000
    Epoch [9890/10000], loss: 0.12767 acc: 0.98667 val_loss: 0.13772, val_acc: 0.96000
    Epoch [9900/10000], loss: 0.12761 acc: 0.98667 val_loss: 0.13767, val_acc: 0.96000
    Epoch [9910/10000], loss: 0.12755 acc: 0.98667 val_loss: 0.13762, val_acc: 0.96000
    Epoch [9920/10000], loss: 0.12749 acc: 0.98667 val_loss: 0.13757, val_acc: 0.96000
    Epoch [9930/10000], loss: 0.12743 acc: 0.98667 val_loss: 0.13752, val_acc: 0.96000
    Epoch [9940/10000], loss: 0.12738 acc: 0.98667 val_loss: 0.13748, val_acc: 0.96000
    Epoch [9950/10000], loss: 0.12732 acc: 0.98667 val_loss: 0.13743, val_acc: 0.96000
    Epoch [9960/10000], loss: 0.12726 acc: 0.98667 val_loss: 0.13738, val_acc: 0.96000
    Epoch [9970/10000], loss: 0.12720 acc: 0.98667 val_loss: 0.13733, val_acc: 0.96000
    Epoch [9980/10000], loss: 0.12715 acc: 0.98667 val_loss: 0.13728, val_acc: 0.96000
    Epoch [9990/10000], loss: 0.12709 acc: 0.98667 val_loss: 0.13724, val_acc: 0.96000



```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기상태 : 손실 : 1.09158  정확도 : 0.26667
    최종상태 : 손실 : 0.13724  정확도 : 0.96000



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b', label='훈련')
plt.plot(history[:,0], history[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__53_0.webp)
    



```python
# 학습 곡선 출력(정확도)

plt.plot(history[:,0], history[:,2], 'b', label='훈련')
plt.plot(history[:,0], history[:,4], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__54_0.webp)
    


### NLLLoss 함수 이해 하기


```python
# 입력 변수 준비

# 더미 출력 데이터
outputs_np = np.array(range(1, 13)).reshape((4,3))
# 더미 정답 데이터
labels_np = np.array([0, 1, 2, 0])

# 텐서화
outputs_dummy = torch.tensor(outputs_np).float()
labels_dummy = torch.tensor(labels_np).long()

# 결과 확인
print(outputs_dummy.data)
print(labels_dummy.data)
```

    tensor([[ 1.,  2.,  3.],
            [ 4.,  5.,  6.],
            [ 7.,  8.,  9.],
            [10., 11., 12.]])
    tensor([0, 1, 2, 0])



```python
# NLLLoss 함수 호출

nllloss = nn.NLLLoss()
loss = nllloss(outputs_dummy, labels_dummy) # -(1 + 5 + 9 + 10)/4 = -6.25
print(loss.item())
```

    -6.25


### 모델 클래스측에 LogSoftmax 함수를 포함


```python
# 모델 정의
# 2입력 3출력 로지스틱 회귀 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        super().__init__()
        self.l1 = nn.Linear(n_input, n_output)
        # logsoftmax 함수 정의
        self.logsoftmax = nn.LogSoftmax(dim=1)

        # 초깃값을 모두 1로 함
        # "딥러닝을 위한 수학"과 조건을 맞추기 위한 목적
        # self.l1.weight.data.fill_(1.0)
        # self.l1.bias.data.fill_(1.0)

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.logsoftmax(x1)
        return x2
```


```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수： NLLLoss 함수
criterion = nn.NLLLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)
```


```python
# 예측 계산
outputs = net(inputs)

# 손실 계산
loss = criterion(outputs, labels)

# 손실의 계산 그래프 시각화
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_9%EC%B0%A8%EC%8B%9C__Multinomial__61_0.svg)
    



```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수： NLLLoss 함수
criterion = nn.NLLLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 평가 결과 기록
history = np.zeros((0,5))
```


```python
for epoch in range(num_epochs):

    # 훈련 페이즈

    # 경사 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 예측 라벨 산출
    predicted = torch.max(outputs, 1)[1]

    # 손실과 정확도 계산
    train_loss = loss.item()
    train_acc = (predicted == labels).sum()  / len(labels)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 손실 계산
    loss_test = criterion(outputs_test, labels_test)

    # 예측 라벨 산출
    predicted_test = torch.max(outputs_test, 1)[1]

    # 손실과 정확도 계산
    val_loss =  loss_test.item()
    val_acc =  (predicted_test == labels_test).sum() / len(labels_test)

    if ( epoch % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch , train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```

    Epoch [0/10000], loss: 4.88003 acc: 0.30667 val_loss: 3.70707, val_acc: 0.36000
    Epoch [10/10000], loss: 1.80466 acc: 0.00000 val_loss: 1.44230, val_acc: 0.00000
    Epoch [20/10000], loss: 1.18552 acc: 0.09333 val_loss: 1.19227, val_acc: 0.29333
    Epoch [30/10000], loss: 1.10535 acc: 0.40000 val_loss: 1.13996, val_acc: 0.26667
    Epoch [40/10000], loss: 1.04555 acc: 0.40000 val_loss: 1.07464, val_acc: 0.26667
    Epoch [50/10000], loss: 0.99253 acc: 0.44000 val_loss: 1.01507, val_acc: 0.36000
    Epoch [60/10000], loss: 0.94560 acc: 0.60000 val_loss: 0.96248, val_acc: 0.48000
    Epoch [70/10000], loss: 0.90413 acc: 0.70667 val_loss: 0.91625, val_acc: 0.61333
    Epoch [80/10000], loss: 0.86747 acc: 0.73333 val_loss: 0.87559, val_acc: 0.62667
    Epoch [90/10000], loss: 0.83500 acc: 0.74667 val_loss: 0.83976, val_acc: 0.65333
    Epoch [100/10000], loss: 0.80617 acc: 0.76000 val_loss: 0.80809, val_acc: 0.66667
    Epoch [110/10000], loss: 0.78049 acc: 0.74667 val_loss: 0.78000, val_acc: 0.68000
    Epoch [120/10000], loss: 0.75752 acc: 0.74667 val_loss: 0.75497, val_acc: 0.70667
    Epoch [130/10000], loss: 0.73688 acc: 0.73333 val_loss: 0.73256, val_acc: 0.74667
    Epoch [140/10000], loss: 0.71825 acc: 0.73333 val_loss: 0.71242, val_acc: 0.76000
    Epoch [150/10000], loss: 0.70138 acc: 0.74667 val_loss: 0.69422, val_acc: 0.77333
    Epoch [160/10000], loss: 0.68601 acc: 0.74667 val_loss: 0.67771, val_acc: 0.78667
    Epoch [170/10000], loss: 0.67197 acc: 0.77333 val_loss: 0.66267, val_acc: 0.80000
    Epoch [180/10000], loss: 0.65907 acc: 0.78667 val_loss: 0.64890, val_acc: 0.80000
    Epoch [190/10000], loss: 0.64719 acc: 0.80000 val_loss: 0.63624, val_acc: 0.80000
    Epoch [200/10000], loss: 0.63621 acc: 0.80000 val_loss: 0.62457, val_acc: 0.81333
    Epoch [210/10000], loss: 0.62601 acc: 0.80000 val_loss: 0.61376, val_acc: 0.84000
    Epoch [220/10000], loss: 0.61650 acc: 0.82667 val_loss: 0.60372, val_acc: 0.84000
    Epoch [230/10000], loss: 0.60763 acc: 0.84000 val_loss: 0.59437, val_acc: 0.84000
    Epoch [240/10000], loss: 0.59930 acc: 0.84000 val_loss: 0.58562, val_acc: 0.84000
    Epoch [250/10000], loss: 0.59148 acc: 0.85333 val_loss: 0.57741, val_acc: 0.84000
    Epoch [260/10000], loss: 0.58411 acc: 0.85333 val_loss: 0.56970, val_acc: 0.84000
    Epoch [270/10000], loss: 0.57714 acc: 0.85333 val_loss: 0.56243, val_acc: 0.84000
    Epoch [280/10000], loss: 0.57055 acc: 0.86667 val_loss: 0.55555, val_acc: 0.84000
    Epoch [290/10000], loss: 0.56428 acc: 0.88000 val_loss: 0.54904, val_acc: 0.84000
    Epoch [300/10000], loss: 0.55832 acc: 0.88000 val_loss: 0.54286, val_acc: 0.84000
    Epoch [310/10000], loss: 0.55264 acc: 0.89333 val_loss: 0.53699, val_acc: 0.84000
    Epoch [320/10000], loss: 0.54722 acc: 0.89333 val_loss: 0.53138, val_acc: 0.84000
    Epoch [330/10000], loss: 0.54203 acc: 0.89333 val_loss: 0.52603, val_acc: 0.84000
    Epoch [340/10000], loss: 0.53705 acc: 0.89333 val_loss: 0.52092, val_acc: 0.84000
    Epoch [350/10000], loss: 0.53227 acc: 0.89333 val_loss: 0.51601, val_acc: 0.84000
    Epoch [360/10000], loss: 0.52768 acc: 0.89333 val_loss: 0.51131, val_acc: 0.84000
    Epoch [370/10000], loss: 0.52326 acc: 0.89333 val_loss: 0.50679, val_acc: 0.84000
    Epoch [380/10000], loss: 0.51900 acc: 0.89333 val_loss: 0.50244, val_acc: 0.84000
    Epoch [390/10000], loss: 0.51488 acc: 0.89333 val_loss: 0.49824, val_acc: 0.84000
    Epoch [400/10000], loss: 0.51090 acc: 0.89333 val_loss: 0.49420, val_acc: 0.85333
    Epoch [410/10000], loss: 0.50705 acc: 0.89333 val_loss: 0.49029, val_acc: 0.85333
    Epoch [420/10000], loss: 0.50333 acc: 0.89333 val_loss: 0.48651, val_acc: 0.85333
    Epoch [430/10000], loss: 0.49971 acc: 0.89333 val_loss: 0.48285, val_acc: 0.88000
    Epoch [440/10000], loss: 0.49620 acc: 0.89333 val_loss: 0.47931, val_acc: 0.88000
    Epoch [450/10000], loss: 0.49279 acc: 0.89333 val_loss: 0.47587, val_acc: 0.88000
    Epoch [460/10000], loss: 0.48947 acc: 0.89333 val_loss: 0.47253, val_acc: 0.88000
    Epoch [470/10000], loss: 0.48624 acc: 0.89333 val_loss: 0.46928, val_acc: 0.88000
    Epoch [480/10000], loss: 0.48310 acc: 0.90667 val_loss: 0.46613, val_acc: 0.88000
    Epoch [490/10000], loss: 0.48003 acc: 0.90667 val_loss: 0.46305, val_acc: 0.88000
    Epoch [500/10000], loss: 0.47704 acc: 0.90667 val_loss: 0.46006, val_acc: 0.89333
    Epoch [510/10000], loss: 0.47412 acc: 0.90667 val_loss: 0.45714, val_acc: 0.89333
    Epoch [520/10000], loss: 0.47127 acc: 0.90667 val_loss: 0.45430, val_acc: 0.89333
    Epoch [530/10000], loss: 0.46848 acc: 0.90667 val_loss: 0.45152, val_acc: 0.89333
    Epoch [540/10000], loss: 0.46576 acc: 0.90667 val_loss: 0.44881, val_acc: 0.89333
    Epoch [550/10000], loss: 0.46309 acc: 0.90667 val_loss: 0.44616, val_acc: 0.89333
    Epoch [560/10000], loss: 0.46048 acc: 0.90667 val_loss: 0.44356, val_acc: 0.89333
    Epoch [570/10000], loss: 0.45792 acc: 0.90667 val_loss: 0.44103, val_acc: 0.90667
    Epoch [580/10000], loss: 0.45541 acc: 0.90667 val_loss: 0.43854, val_acc: 0.90667
    Epoch [590/10000], loss: 0.45295 acc: 0.90667 val_loss: 0.43611, val_acc: 0.92000
    Epoch [600/10000], loss: 0.45053 acc: 0.90667 val_loss: 0.43373, val_acc: 0.93333
    Epoch [610/10000], loss: 0.44816 acc: 0.90667 val_loss: 0.43139, val_acc: 0.93333
    Epoch [620/10000], loss: 0.44584 acc: 0.90667 val_loss: 0.42910, val_acc: 0.93333
    Epoch [630/10000], loss: 0.44355 acc: 0.90667 val_loss: 0.42685, val_acc: 0.93333
    Epoch [640/10000], loss: 0.44131 acc: 0.92000 val_loss: 0.42464, val_acc: 0.93333
    Epoch [650/10000], loss: 0.43910 acc: 0.92000 val_loss: 0.42247, val_acc: 0.93333
    Epoch [660/10000], loss: 0.43693 acc: 0.92000 val_loss: 0.42035, val_acc: 0.93333
    Epoch [670/10000], loss: 0.43479 acc: 0.92000 val_loss: 0.41825, val_acc: 0.93333
    Epoch [680/10000], loss: 0.43269 acc: 0.92000 val_loss: 0.41620, val_acc: 0.93333
    Epoch [690/10000], loss: 0.43062 acc: 0.92000 val_loss: 0.41417, val_acc: 0.93333
    Epoch [700/10000], loss: 0.42859 acc: 0.92000 val_loss: 0.41218, val_acc: 0.93333
    Epoch [710/10000], loss: 0.42658 acc: 0.92000 val_loss: 0.41023, val_acc: 0.93333
    Epoch [720/10000], loss: 0.42460 acc: 0.92000 val_loss: 0.40830, val_acc: 0.93333
    Epoch [730/10000], loss: 0.42266 acc: 0.92000 val_loss: 0.40640, val_acc: 0.93333
    Epoch [740/10000], loss: 0.42074 acc: 0.92000 val_loss: 0.40454, val_acc: 0.93333
    Epoch [750/10000], loss: 0.41884 acc: 0.92000 val_loss: 0.40270, val_acc: 0.93333
    Epoch [760/10000], loss: 0.41698 acc: 0.92000 val_loss: 0.40088, val_acc: 0.93333
    Epoch [770/10000], loss: 0.41514 acc: 0.92000 val_loss: 0.39910, val_acc: 0.93333
    Epoch [780/10000], loss: 0.41332 acc: 0.92000 val_loss: 0.39734, val_acc: 0.93333
    Epoch [790/10000], loss: 0.41153 acc: 0.92000 val_loss: 0.39560, val_acc: 0.93333
    Epoch [800/10000], loss: 0.40976 acc: 0.92000 val_loss: 0.39389, val_acc: 0.93333
    Epoch [810/10000], loss: 0.40801 acc: 0.92000 val_loss: 0.39220, val_acc: 0.93333
    Epoch [820/10000], loss: 0.40629 acc: 0.93333 val_loss: 0.39053, val_acc: 0.93333
    Epoch [830/10000], loss: 0.40459 acc: 0.93333 val_loss: 0.38889, val_acc: 0.93333
    Epoch [840/10000], loss: 0.40291 acc: 0.93333 val_loss: 0.38726, val_acc: 0.93333
    Epoch [850/10000], loss: 0.40124 acc: 0.93333 val_loss: 0.38566, val_acc: 0.93333
    Epoch [860/10000], loss: 0.39960 acc: 0.93333 val_loss: 0.38408, val_acc: 0.93333
    Epoch [870/10000], loss: 0.39798 acc: 0.93333 val_loss: 0.38252, val_acc: 0.93333
    Epoch [880/10000], loss: 0.39638 acc: 0.93333 val_loss: 0.38097, val_acc: 0.93333
    Epoch [890/10000], loss: 0.39479 acc: 0.93333 val_loss: 0.37945, val_acc: 0.93333
    Epoch [900/10000], loss: 0.39323 acc: 0.93333 val_loss: 0.37795, val_acc: 0.93333
    Epoch [910/10000], loss: 0.39168 acc: 0.93333 val_loss: 0.37646, val_acc: 0.93333
    Epoch [920/10000], loss: 0.39015 acc: 0.93333 val_loss: 0.37499, val_acc: 0.93333
    Epoch [930/10000], loss: 0.38863 acc: 0.93333 val_loss: 0.37354, val_acc: 0.93333
    Epoch [940/10000], loss: 0.38713 acc: 0.93333 val_loss: 0.37210, val_acc: 0.93333
    Epoch [950/10000], loss: 0.38565 acc: 0.93333 val_loss: 0.37068, val_acc: 0.93333
    Epoch [960/10000], loss: 0.38418 acc: 0.93333 val_loss: 0.36928, val_acc: 0.93333
    Epoch [970/10000], loss: 0.38273 acc: 0.93333 val_loss: 0.36789, val_acc: 0.93333
    Epoch [980/10000], loss: 0.38130 acc: 0.93333 val_loss: 0.36651, val_acc: 0.93333
    Epoch [990/10000], loss: 0.37988 acc: 0.93333 val_loss: 0.36516, val_acc: 0.93333
    Epoch [1000/10000], loss: 0.37847 acc: 0.93333 val_loss: 0.36381, val_acc: 0.93333
    Epoch [1010/10000], loss: 0.37708 acc: 0.93333 val_loss: 0.36248, val_acc: 0.93333
    Epoch [1020/10000], loss: 0.37570 acc: 0.93333 val_loss: 0.36117, val_acc: 0.93333
    Epoch [1030/10000], loss: 0.37433 acc: 0.93333 val_loss: 0.35987, val_acc: 0.93333
    Epoch [1040/10000], loss: 0.37298 acc: 0.93333 val_loss: 0.35858, val_acc: 0.93333
    Epoch [1050/10000], loss: 0.37164 acc: 0.93333 val_loss: 0.35730, val_acc: 0.93333
    Epoch [1060/10000], loss: 0.37032 acc: 0.93333 val_loss: 0.35604, val_acc: 0.93333
    Epoch [1070/10000], loss: 0.36900 acc: 0.93333 val_loss: 0.35479, val_acc: 0.93333
    Epoch [1080/10000], loss: 0.36770 acc: 0.93333 val_loss: 0.35356, val_acc: 0.93333
    Epoch [1090/10000], loss: 0.36642 acc: 0.93333 val_loss: 0.35233, val_acc: 0.94667
    Epoch [1100/10000], loss: 0.36514 acc: 0.93333 val_loss: 0.35112, val_acc: 0.94667
    Epoch [1110/10000], loss: 0.36388 acc: 0.93333 val_loss: 0.34992, val_acc: 0.94667
    Epoch [1120/10000], loss: 0.36262 acc: 0.93333 val_loss: 0.34873, val_acc: 0.94667
    Epoch [1130/10000], loss: 0.36138 acc: 0.93333 val_loss: 0.34756, val_acc: 0.94667
    Epoch [1140/10000], loss: 0.36015 acc: 0.93333 val_loss: 0.34639, val_acc: 0.94667
    Epoch [1150/10000], loss: 0.35893 acc: 0.93333 val_loss: 0.34524, val_acc: 0.94667
    Epoch [1160/10000], loss: 0.35773 acc: 0.93333 val_loss: 0.34409, val_acc: 0.94667
    Epoch [1170/10000], loss: 0.35653 acc: 0.93333 val_loss: 0.34296, val_acc: 0.94667
    Epoch [1180/10000], loss: 0.35534 acc: 0.93333 val_loss: 0.34183, val_acc: 0.94667
    Epoch [1190/10000], loss: 0.35416 acc: 0.93333 val_loss: 0.34072, val_acc: 0.94667
    Epoch [1200/10000], loss: 0.35300 acc: 0.93333 val_loss: 0.33962, val_acc: 0.94667
    Epoch [1210/10000], loss: 0.35184 acc: 0.93333 val_loss: 0.33853, val_acc: 0.94667
    Epoch [1220/10000], loss: 0.35070 acc: 0.93333 val_loss: 0.33744, val_acc: 0.94667
    Epoch [1230/10000], loss: 0.34956 acc: 0.93333 val_loss: 0.33637, val_acc: 0.94667
    Epoch [1240/10000], loss: 0.34843 acc: 0.93333 val_loss: 0.33531, val_acc: 0.94667
    Epoch [1250/10000], loss: 0.34731 acc: 0.93333 val_loss: 0.33425, val_acc: 0.94667
    Epoch [1260/10000], loss: 0.34621 acc: 0.93333 val_loss: 0.33321, val_acc: 0.94667
    Epoch [1270/10000], loss: 0.34511 acc: 0.93333 val_loss: 0.33217, val_acc: 0.94667
    Epoch [1280/10000], loss: 0.34402 acc: 0.93333 val_loss: 0.33115, val_acc: 0.94667
    Epoch [1290/10000], loss: 0.34294 acc: 0.93333 val_loss: 0.33013, val_acc: 0.94667
    Epoch [1300/10000], loss: 0.34186 acc: 0.93333 val_loss: 0.32912, val_acc: 0.94667
    Epoch [1310/10000], loss: 0.34080 acc: 0.93333 val_loss: 0.32812, val_acc: 0.94667
    Epoch [1320/10000], loss: 0.33975 acc: 0.93333 val_loss: 0.32712, val_acc: 0.94667
    Epoch [1330/10000], loss: 0.33870 acc: 0.93333 val_loss: 0.32614, val_acc: 0.94667
    Epoch [1340/10000], loss: 0.33766 acc: 0.93333 val_loss: 0.32516, val_acc: 0.94667
    Epoch [1350/10000], loss: 0.33663 acc: 0.93333 val_loss: 0.32420, val_acc: 0.94667
    Epoch [1360/10000], loss: 0.33561 acc: 0.93333 val_loss: 0.32324, val_acc: 0.94667
    Epoch [1370/10000], loss: 0.33459 acc: 0.93333 val_loss: 0.32228, val_acc: 0.94667
    Epoch [1380/10000], loss: 0.33359 acc: 0.93333 val_loss: 0.32134, val_acc: 0.94667
    Epoch [1390/10000], loss: 0.33259 acc: 0.93333 val_loss: 0.32040, val_acc: 0.94667
    Epoch [1400/10000], loss: 0.33160 acc: 0.93333 val_loss: 0.31947, val_acc: 0.94667
    Epoch [1410/10000], loss: 0.33062 acc: 0.93333 val_loss: 0.31855, val_acc: 0.94667
    Epoch [1420/10000], loss: 0.32964 acc: 0.93333 val_loss: 0.31764, val_acc: 0.94667
    Epoch [1430/10000], loss: 0.32867 acc: 0.93333 val_loss: 0.31673, val_acc: 0.94667
    Epoch [1440/10000], loss: 0.32771 acc: 0.93333 val_loss: 0.31583, val_acc: 0.94667
    Epoch [1450/10000], loss: 0.32676 acc: 0.93333 val_loss: 0.31494, val_acc: 0.94667
    Epoch [1460/10000], loss: 0.32581 acc: 0.93333 val_loss: 0.31405, val_acc: 0.94667
    Epoch [1470/10000], loss: 0.32487 acc: 0.93333 val_loss: 0.31317, val_acc: 0.94667
    Epoch [1480/10000], loss: 0.32394 acc: 0.93333 val_loss: 0.31230, val_acc: 0.94667
    Epoch [1490/10000], loss: 0.32301 acc: 0.93333 val_loss: 0.31144, val_acc: 0.94667
    Epoch [1500/10000], loss: 0.32210 acc: 0.93333 val_loss: 0.31058, val_acc: 0.94667
    Epoch [1510/10000], loss: 0.32118 acc: 0.93333 val_loss: 0.30973, val_acc: 0.94667
    Epoch [1520/10000], loss: 0.32028 acc: 0.93333 val_loss: 0.30888, val_acc: 0.94667
    Epoch [1530/10000], loss: 0.31938 acc: 0.93333 val_loss: 0.30804, val_acc: 0.94667
    Epoch [1540/10000], loss: 0.31849 acc: 0.93333 val_loss: 0.30721, val_acc: 0.94667
    Epoch [1550/10000], loss: 0.31760 acc: 0.93333 val_loss: 0.30638, val_acc: 0.94667
    Epoch [1560/10000], loss: 0.31672 acc: 0.93333 val_loss: 0.30556, val_acc: 0.94667
    Epoch [1570/10000], loss: 0.31585 acc: 0.94667 val_loss: 0.30474, val_acc: 0.94667
    Epoch [1580/10000], loss: 0.31498 acc: 0.94667 val_loss: 0.30394, val_acc: 0.94667
    Epoch [1590/10000], loss: 0.31412 acc: 0.94667 val_loss: 0.30313, val_acc: 0.94667
    Epoch [1600/10000], loss: 0.31326 acc: 0.94667 val_loss: 0.30234, val_acc: 0.94667
    Epoch [1610/10000], loss: 0.31241 acc: 0.94667 val_loss: 0.30155, val_acc: 0.94667
    Epoch [1620/10000], loss: 0.31157 acc: 0.94667 val_loss: 0.30076, val_acc: 0.94667
    Epoch [1630/10000], loss: 0.31073 acc: 0.94667 val_loss: 0.29998, val_acc: 0.94667
    Epoch [1640/10000], loss: 0.30990 acc: 0.94667 val_loss: 0.29921, val_acc: 0.94667
    Epoch [1650/10000], loss: 0.30908 acc: 0.94667 val_loss: 0.29844, val_acc: 0.94667
    Epoch [1660/10000], loss: 0.30826 acc: 0.94667 val_loss: 0.29768, val_acc: 0.94667
    Epoch [1670/10000], loss: 0.30744 acc: 0.94667 val_loss: 0.29692, val_acc: 0.94667
    Epoch [1680/10000], loss: 0.30663 acc: 0.94667 val_loss: 0.29617, val_acc: 0.94667
    Epoch [1690/10000], loss: 0.30583 acc: 0.94667 val_loss: 0.29542, val_acc: 0.94667
    Epoch [1700/10000], loss: 0.30503 acc: 0.94667 val_loss: 0.29468, val_acc: 0.94667
    Epoch [1710/10000], loss: 0.30424 acc: 0.94667 val_loss: 0.29394, val_acc: 0.94667
    Epoch [1720/10000], loss: 0.30345 acc: 0.94667 val_loss: 0.29321, val_acc: 0.94667
    Epoch [1730/10000], loss: 0.30267 acc: 0.94667 val_loss: 0.29248, val_acc: 0.94667
    Epoch [1740/10000], loss: 0.30189 acc: 0.94667 val_loss: 0.29176, val_acc: 0.94667
    Epoch [1750/10000], loss: 0.30112 acc: 0.94667 val_loss: 0.29105, val_acc: 0.94667
    Epoch [1760/10000], loss: 0.30035 acc: 0.94667 val_loss: 0.29033, val_acc: 0.94667
    Epoch [1770/10000], loss: 0.29959 acc: 0.94667 val_loss: 0.28963, val_acc: 0.94667
    Epoch [1780/10000], loss: 0.29883 acc: 0.94667 val_loss: 0.28893, val_acc: 0.94667
    Epoch [1790/10000], loss: 0.29808 acc: 0.94667 val_loss: 0.28823, val_acc: 0.94667
    Epoch [1800/10000], loss: 0.29734 acc: 0.96000 val_loss: 0.28754, val_acc: 0.94667
    Epoch [1810/10000], loss: 0.29659 acc: 0.96000 val_loss: 0.28685, val_acc: 0.94667
    Epoch [1820/10000], loss: 0.29586 acc: 0.96000 val_loss: 0.28617, val_acc: 0.94667
    Epoch [1830/10000], loss: 0.29512 acc: 0.96000 val_loss: 0.28549, val_acc: 0.94667
    Epoch [1840/10000], loss: 0.29440 acc: 0.96000 val_loss: 0.28482, val_acc: 0.94667
    Epoch [1850/10000], loss: 0.29367 acc: 0.96000 val_loss: 0.28415, val_acc: 0.94667
    Epoch [1860/10000], loss: 0.29295 acc: 0.96000 val_loss: 0.28348, val_acc: 0.94667
    Epoch [1870/10000], loss: 0.29224 acc: 0.96000 val_loss: 0.28282, val_acc: 0.94667
    Epoch [1880/10000], loss: 0.29153 acc: 0.96000 val_loss: 0.28216, val_acc: 0.94667
    Epoch [1890/10000], loss: 0.29083 acc: 0.96000 val_loss: 0.28151, val_acc: 0.94667
    Epoch [1900/10000], loss: 0.29013 acc: 0.96000 val_loss: 0.28087, val_acc: 0.94667
    Epoch [1910/10000], loss: 0.28943 acc: 0.96000 val_loss: 0.28022, val_acc: 0.94667
    Epoch [1920/10000], loss: 0.28874 acc: 0.96000 val_loss: 0.27958, val_acc: 0.94667
    Epoch [1930/10000], loss: 0.28805 acc: 0.96000 val_loss: 0.27895, val_acc: 0.94667
    Epoch [1940/10000], loss: 0.28737 acc: 0.96000 val_loss: 0.27832, val_acc: 0.94667
    Epoch [1950/10000], loss: 0.28669 acc: 0.96000 val_loss: 0.27769, val_acc: 0.94667
    Epoch [1960/10000], loss: 0.28601 acc: 0.96000 val_loss: 0.27707, val_acc: 0.94667
    Epoch [1970/10000], loss: 0.28534 acc: 0.96000 val_loss: 0.27645, val_acc: 0.94667
    Epoch [1980/10000], loss: 0.28467 acc: 0.96000 val_loss: 0.27583, val_acc: 0.94667
    Epoch [1990/10000], loss: 0.28401 acc: 0.96000 val_loss: 0.27522, val_acc: 0.94667
    Epoch [2000/10000], loss: 0.28335 acc: 0.96000 val_loss: 0.27461, val_acc: 0.94667
    Epoch [2010/10000], loss: 0.28270 acc: 0.96000 val_loss: 0.27401, val_acc: 0.94667
    Epoch [2020/10000], loss: 0.28205 acc: 0.96000 val_loss: 0.27341, val_acc: 0.94667
    Epoch [2030/10000], loss: 0.28140 acc: 0.96000 val_loss: 0.27282, val_acc: 0.94667
    Epoch [2040/10000], loss: 0.28076 acc: 0.96000 val_loss: 0.27222, val_acc: 0.94667
    Epoch [2050/10000], loss: 0.28012 acc: 0.96000 val_loss: 0.27163, val_acc: 0.94667
    Epoch [2060/10000], loss: 0.27948 acc: 0.96000 val_loss: 0.27105, val_acc: 0.94667
    Epoch [2070/10000], loss: 0.27885 acc: 0.96000 val_loss: 0.27047, val_acc: 0.94667
    Epoch [2080/10000], loss: 0.27823 acc: 0.96000 val_loss: 0.26989, val_acc: 0.94667
    Epoch [2090/10000], loss: 0.27760 acc: 0.96000 val_loss: 0.26932, val_acc: 0.94667
    Epoch [2100/10000], loss: 0.27698 acc: 0.96000 val_loss: 0.26875, val_acc: 0.94667
    Epoch [2110/10000], loss: 0.27636 acc: 0.96000 val_loss: 0.26818, val_acc: 0.94667
    Epoch [2120/10000], loss: 0.27575 acc: 0.96000 val_loss: 0.26761, val_acc: 0.94667
    Epoch [2130/10000], loss: 0.27514 acc: 0.96000 val_loss: 0.26705, val_acc: 0.96000
    Epoch [2140/10000], loss: 0.27454 acc: 0.96000 val_loss: 0.26650, val_acc: 0.96000
    Epoch [2150/10000], loss: 0.27393 acc: 0.96000 val_loss: 0.26594, val_acc: 0.96000
    Epoch [2160/10000], loss: 0.27333 acc: 0.96000 val_loss: 0.26539, val_acc: 0.96000
    Epoch [2170/10000], loss: 0.27274 acc: 0.96000 val_loss: 0.26485, val_acc: 0.96000
    Epoch [2180/10000], loss: 0.27215 acc: 0.96000 val_loss: 0.26430, val_acc: 0.96000
    Epoch [2190/10000], loss: 0.27156 acc: 0.96000 val_loss: 0.26376, val_acc: 0.96000
    Epoch [2200/10000], loss: 0.27097 acc: 0.96000 val_loss: 0.26323, val_acc: 0.96000
    Epoch [2210/10000], loss: 0.27039 acc: 0.96000 val_loss: 0.26269, val_acc: 0.96000
    Epoch [2220/10000], loss: 0.26981 acc: 0.96000 val_loss: 0.26216, val_acc: 0.96000
    Epoch [2230/10000], loss: 0.26924 acc: 0.96000 val_loss: 0.26163, val_acc: 0.96000
    Epoch [2240/10000], loss: 0.26866 acc: 0.96000 val_loss: 0.26111, val_acc: 0.96000
    Epoch [2250/10000], loss: 0.26810 acc: 0.96000 val_loss: 0.26059, val_acc: 0.96000
    Epoch [2260/10000], loss: 0.26753 acc: 0.96000 val_loss: 0.26007, val_acc: 0.96000
    Epoch [2270/10000], loss: 0.26697 acc: 0.96000 val_loss: 0.25955, val_acc: 0.96000
    Epoch [2280/10000], loss: 0.26641 acc: 0.96000 val_loss: 0.25904, val_acc: 0.96000
    Epoch [2290/10000], loss: 0.26585 acc: 0.96000 val_loss: 0.25853, val_acc: 0.96000
    Epoch [2300/10000], loss: 0.26530 acc: 0.96000 val_loss: 0.25802, val_acc: 0.96000
    Epoch [2310/10000], loss: 0.26475 acc: 0.96000 val_loss: 0.25752, val_acc: 0.96000
    Epoch [2320/10000], loss: 0.26420 acc: 0.96000 val_loss: 0.25702, val_acc: 0.96000
    Epoch [2330/10000], loss: 0.26366 acc: 0.96000 val_loss: 0.25652, val_acc: 0.96000
    Epoch [2340/10000], loss: 0.26311 acc: 0.96000 val_loss: 0.25602, val_acc: 0.96000
    Epoch [2350/10000], loss: 0.26258 acc: 0.96000 val_loss: 0.25553, val_acc: 0.96000
    Epoch [2360/10000], loss: 0.26204 acc: 0.96000 val_loss: 0.25504, val_acc: 0.96000
    Epoch [2370/10000], loss: 0.26151 acc: 0.96000 val_loss: 0.25456, val_acc: 0.96000
    Epoch [2380/10000], loss: 0.26098 acc: 0.96000 val_loss: 0.25407, val_acc: 0.96000
    Epoch [2390/10000], loss: 0.26045 acc: 0.96000 val_loss: 0.25359, val_acc: 0.96000
    Epoch [2400/10000], loss: 0.25993 acc: 0.96000 val_loss: 0.25311, val_acc: 0.96000
    Epoch [2410/10000], loss: 0.25941 acc: 0.96000 val_loss: 0.25263, val_acc: 0.96000
    Epoch [2420/10000], loss: 0.25889 acc: 0.96000 val_loss: 0.25216, val_acc: 0.96000
    Epoch [2430/10000], loss: 0.25837 acc: 0.96000 val_loss: 0.25169, val_acc: 0.96000
    Epoch [2440/10000], loss: 0.25786 acc: 0.96000 val_loss: 0.25122, val_acc: 0.96000
    Epoch [2450/10000], loss: 0.25735 acc: 0.96000 val_loss: 0.25076, val_acc: 0.96000
    Epoch [2460/10000], loss: 0.25685 acc: 0.96000 val_loss: 0.25029, val_acc: 0.96000
    Epoch [2470/10000], loss: 0.25634 acc: 0.96000 val_loss: 0.24983, val_acc: 0.96000
    Epoch [2480/10000], loss: 0.25584 acc: 0.96000 val_loss: 0.24937, val_acc: 0.96000
    Epoch [2490/10000], loss: 0.25534 acc: 0.96000 val_loss: 0.24892, val_acc: 0.96000
    Epoch [2500/10000], loss: 0.25484 acc: 0.96000 val_loss: 0.24847, val_acc: 0.96000
    Epoch [2510/10000], loss: 0.25435 acc: 0.96000 val_loss: 0.24802, val_acc: 0.96000
    Epoch [2520/10000], loss: 0.25386 acc: 0.96000 val_loss: 0.24757, val_acc: 0.96000
    Epoch [2530/10000], loss: 0.25337 acc: 0.96000 val_loss: 0.24712, val_acc: 0.96000
    Epoch [2540/10000], loss: 0.25288 acc: 0.96000 val_loss: 0.24668, val_acc: 0.96000
    Epoch [2550/10000], loss: 0.25240 acc: 0.96000 val_loss: 0.24624, val_acc: 0.96000
    Epoch [2560/10000], loss: 0.25192 acc: 0.96000 val_loss: 0.24580, val_acc: 0.96000
    Epoch [2570/10000], loss: 0.25144 acc: 0.96000 val_loss: 0.24536, val_acc: 0.96000
    Epoch [2580/10000], loss: 0.25096 acc: 0.96000 val_loss: 0.24493, val_acc: 0.96000
    Epoch [2590/10000], loss: 0.25049 acc: 0.96000 val_loss: 0.24450, val_acc: 0.96000
    Epoch [2600/10000], loss: 0.25002 acc: 0.96000 val_loss: 0.24407, val_acc: 0.96000
    Epoch [2610/10000], loss: 0.24955 acc: 0.96000 val_loss: 0.24364, val_acc: 0.96000
    Epoch [2620/10000], loss: 0.24908 acc: 0.96000 val_loss: 0.24322, val_acc: 0.96000
    Epoch [2630/10000], loss: 0.24862 acc: 0.96000 val_loss: 0.24279, val_acc: 0.96000
    Epoch [2640/10000], loss: 0.24815 acc: 0.96000 val_loss: 0.24237, val_acc: 0.96000
    Epoch [2650/10000], loss: 0.24770 acc: 0.96000 val_loss: 0.24196, val_acc: 0.96000
    Epoch [2660/10000], loss: 0.24724 acc: 0.96000 val_loss: 0.24154, val_acc: 0.96000
    Epoch [2670/10000], loss: 0.24678 acc: 0.96000 val_loss: 0.24113, val_acc: 0.96000
    Epoch [2680/10000], loss: 0.24633 acc: 0.96000 val_loss: 0.24071, val_acc: 0.96000
    Epoch [2690/10000], loss: 0.24588 acc: 0.96000 val_loss: 0.24030, val_acc: 0.96000
    Epoch [2700/10000], loss: 0.24543 acc: 0.96000 val_loss: 0.23990, val_acc: 0.96000
    Epoch [2710/10000], loss: 0.24499 acc: 0.96000 val_loss: 0.23949, val_acc: 0.96000
    Epoch [2720/10000], loss: 0.24454 acc: 0.96000 val_loss: 0.23909, val_acc: 0.96000
    Epoch [2730/10000], loss: 0.24410 acc: 0.96000 val_loss: 0.23869, val_acc: 0.96000
    Epoch [2740/10000], loss: 0.24366 acc: 0.96000 val_loss: 0.23829, val_acc: 0.96000
    Epoch [2750/10000], loss: 0.24322 acc: 0.96000 val_loss: 0.23789, val_acc: 0.96000
    Epoch [2760/10000], loss: 0.24279 acc: 0.96000 val_loss: 0.23750, val_acc: 0.96000
    Epoch [2770/10000], loss: 0.24236 acc: 0.96000 val_loss: 0.23710, val_acc: 0.96000
    Epoch [2780/10000], loss: 0.24192 acc: 0.96000 val_loss: 0.23671, val_acc: 0.96000
    Epoch [2790/10000], loss: 0.24150 acc: 0.96000 val_loss: 0.23632, val_acc: 0.96000
    Epoch [2800/10000], loss: 0.24107 acc: 0.96000 val_loss: 0.23594, val_acc: 0.96000
    Epoch [2810/10000], loss: 0.24064 acc: 0.96000 val_loss: 0.23555, val_acc: 0.96000
    Epoch [2820/10000], loss: 0.24022 acc: 0.96000 val_loss: 0.23517, val_acc: 0.96000
    Epoch [2830/10000], loss: 0.23980 acc: 0.96000 val_loss: 0.23479, val_acc: 0.96000
    Epoch [2840/10000], loss: 0.23938 acc: 0.96000 val_loss: 0.23441, val_acc: 0.96000
    Epoch [2850/10000], loss: 0.23897 acc: 0.96000 val_loss: 0.23403, val_acc: 0.96000
    Epoch [2860/10000], loss: 0.23855 acc: 0.96000 val_loss: 0.23365, val_acc: 0.96000
    Epoch [2870/10000], loss: 0.23814 acc: 0.96000 val_loss: 0.23328, val_acc: 0.96000
    Epoch [2880/10000], loss: 0.23773 acc: 0.96000 val_loss: 0.23291, val_acc: 0.96000
    Epoch [2890/10000], loss: 0.23732 acc: 0.96000 val_loss: 0.23254, val_acc: 0.96000
    Epoch [2900/10000], loss: 0.23691 acc: 0.96000 val_loss: 0.23217, val_acc: 0.96000
    Epoch [2910/10000], loss: 0.23651 acc: 0.96000 val_loss: 0.23180, val_acc: 0.96000
    Epoch [2920/10000], loss: 0.23611 acc: 0.96000 val_loss: 0.23144, val_acc: 0.96000
    Epoch [2930/10000], loss: 0.23570 acc: 0.96000 val_loss: 0.23108, val_acc: 0.96000
    Epoch [2940/10000], loss: 0.23531 acc: 0.96000 val_loss: 0.23071, val_acc: 0.96000
    Epoch [2950/10000], loss: 0.23491 acc: 0.96000 val_loss: 0.23035, val_acc: 0.96000
    Epoch [2960/10000], loss: 0.23451 acc: 0.96000 val_loss: 0.23000, val_acc: 0.96000
    Epoch [2970/10000], loss: 0.23412 acc: 0.96000 val_loss: 0.22964, val_acc: 0.96000
    Epoch [2980/10000], loss: 0.23373 acc: 0.96000 val_loss: 0.22929, val_acc: 0.96000
    Epoch [2990/10000], loss: 0.23334 acc: 0.96000 val_loss: 0.22893, val_acc: 0.96000
    Epoch [3000/10000], loss: 0.23295 acc: 0.96000 val_loss: 0.22858, val_acc: 0.96000
    Epoch [3010/10000], loss: 0.23256 acc: 0.96000 val_loss: 0.22823, val_acc: 0.96000
    Epoch [3020/10000], loss: 0.23218 acc: 0.96000 val_loss: 0.22789, val_acc: 0.96000
    Epoch [3030/10000], loss: 0.23180 acc: 0.96000 val_loss: 0.22754, val_acc: 0.96000
    Epoch [3040/10000], loss: 0.23142 acc: 0.96000 val_loss: 0.22720, val_acc: 0.96000
    Epoch [3050/10000], loss: 0.23104 acc: 0.96000 val_loss: 0.22685, val_acc: 0.96000
    Epoch [3060/10000], loss: 0.23066 acc: 0.96000 val_loss: 0.22651, val_acc: 0.96000
    Epoch [3070/10000], loss: 0.23028 acc: 0.96000 val_loss: 0.22617, val_acc: 0.96000
    Epoch [3080/10000], loss: 0.22991 acc: 0.96000 val_loss: 0.22584, val_acc: 0.96000
    Epoch [3090/10000], loss: 0.22954 acc: 0.96000 val_loss: 0.22550, val_acc: 0.96000
    Epoch [3100/10000], loss: 0.22917 acc: 0.96000 val_loss: 0.22517, val_acc: 0.96000
    Epoch [3110/10000], loss: 0.22880 acc: 0.96000 val_loss: 0.22483, val_acc: 0.96000
    Epoch [3120/10000], loss: 0.22843 acc: 0.96000 val_loss: 0.22450, val_acc: 0.96000
    Epoch [3130/10000], loss: 0.22806 acc: 0.96000 val_loss: 0.22417, val_acc: 0.96000
    Epoch [3140/10000], loss: 0.22770 acc: 0.96000 val_loss: 0.22384, val_acc: 0.96000
    Epoch [3150/10000], loss: 0.22734 acc: 0.96000 val_loss: 0.22352, val_acc: 0.96000
    Epoch [3160/10000], loss: 0.22698 acc: 0.96000 val_loss: 0.22319, val_acc: 0.96000
    Epoch [3170/10000], loss: 0.22662 acc: 0.96000 val_loss: 0.22287, val_acc: 0.96000
    Epoch [3180/10000], loss: 0.22626 acc: 0.96000 val_loss: 0.22255, val_acc: 0.96000
    Epoch [3190/10000], loss: 0.22590 acc: 0.96000 val_loss: 0.22222, val_acc: 0.96000
    Epoch [3200/10000], loss: 0.22555 acc: 0.96000 val_loss: 0.22190, val_acc: 0.96000
    Epoch [3210/10000], loss: 0.22520 acc: 0.96000 val_loss: 0.22159, val_acc: 0.96000
    Epoch [3220/10000], loss: 0.22485 acc: 0.96000 val_loss: 0.22127, val_acc: 0.96000
    Epoch [3230/10000], loss: 0.22450 acc: 0.96000 val_loss: 0.22096, val_acc: 0.96000
    Epoch [3240/10000], loss: 0.22415 acc: 0.96000 val_loss: 0.22064, val_acc: 0.96000
    Epoch [3250/10000], loss: 0.22380 acc: 0.96000 val_loss: 0.22033, val_acc: 0.96000
    Epoch [3260/10000], loss: 0.22346 acc: 0.96000 val_loss: 0.22002, val_acc: 0.96000
    Epoch [3270/10000], loss: 0.22311 acc: 0.96000 val_loss: 0.21971, val_acc: 0.96000
    Epoch [3280/10000], loss: 0.22277 acc: 0.96000 val_loss: 0.21940, val_acc: 0.96000
    Epoch [3290/10000], loss: 0.22243 acc: 0.96000 val_loss: 0.21910, val_acc: 0.96000
    Epoch [3300/10000], loss: 0.22209 acc: 0.96000 val_loss: 0.21879, val_acc: 0.96000
    Epoch [3310/10000], loss: 0.22175 acc: 0.96000 val_loss: 0.21849, val_acc: 0.96000
    Epoch [3320/10000], loss: 0.22142 acc: 0.96000 val_loss: 0.21818, val_acc: 0.96000
    Epoch [3330/10000], loss: 0.22108 acc: 0.96000 val_loss: 0.21788, val_acc: 0.96000
    Epoch [3340/10000], loss: 0.22075 acc: 0.96000 val_loss: 0.21758, val_acc: 0.96000
    Epoch [3350/10000], loss: 0.22042 acc: 0.96000 val_loss: 0.21728, val_acc: 0.96000
    Epoch [3360/10000], loss: 0.22009 acc: 0.96000 val_loss: 0.21699, val_acc: 0.96000
    Epoch [3370/10000], loss: 0.21976 acc: 0.96000 val_loss: 0.21669, val_acc: 0.96000
    Epoch [3380/10000], loss: 0.21943 acc: 0.96000 val_loss: 0.21640, val_acc: 0.96000
    Epoch [3390/10000], loss: 0.21910 acc: 0.96000 val_loss: 0.21610, val_acc: 0.96000
    Epoch [3400/10000], loss: 0.21878 acc: 0.96000 val_loss: 0.21581, val_acc: 0.96000
    Epoch [3410/10000], loss: 0.21845 acc: 0.96000 val_loss: 0.21552, val_acc: 0.96000
    Epoch [3420/10000], loss: 0.21813 acc: 0.96000 val_loss: 0.21523, val_acc: 0.96000
    Epoch [3430/10000], loss: 0.21781 acc: 0.96000 val_loss: 0.21494, val_acc: 0.96000
    Epoch [3440/10000], loss: 0.21749 acc: 0.96000 val_loss: 0.21466, val_acc: 0.96000
    Epoch [3450/10000], loss: 0.21717 acc: 0.96000 val_loss: 0.21437, val_acc: 0.96000
    Epoch [3460/10000], loss: 0.21685 acc: 0.96000 val_loss: 0.21409, val_acc: 0.96000
    Epoch [3470/10000], loss: 0.21654 acc: 0.96000 val_loss: 0.21380, val_acc: 0.96000
    Epoch [3480/10000], loss: 0.21622 acc: 0.96000 val_loss: 0.21352, val_acc: 0.96000
    Epoch [3490/10000], loss: 0.21591 acc: 0.96000 val_loss: 0.21324, val_acc: 0.96000
    Epoch [3500/10000], loss: 0.21560 acc: 0.96000 val_loss: 0.21296, val_acc: 0.96000
    Epoch [3510/10000], loss: 0.21529 acc: 0.96000 val_loss: 0.21268, val_acc: 0.96000
    Epoch [3520/10000], loss: 0.21498 acc: 0.96000 val_loss: 0.21241, val_acc: 0.96000
    Epoch [3530/10000], loss: 0.21467 acc: 0.96000 val_loss: 0.21213, val_acc: 0.96000
    Epoch [3540/10000], loss: 0.21437 acc: 0.96000 val_loss: 0.21185, val_acc: 0.96000
    Epoch [3550/10000], loss: 0.21406 acc: 0.96000 val_loss: 0.21158, val_acc: 0.96000
    Epoch [3560/10000], loss: 0.21376 acc: 0.96000 val_loss: 0.21131, val_acc: 0.96000
    Epoch [3570/10000], loss: 0.21345 acc: 0.96000 val_loss: 0.21104, val_acc: 0.96000
    Epoch [3580/10000], loss: 0.21315 acc: 0.96000 val_loss: 0.21077, val_acc: 0.96000
    Epoch [3590/10000], loss: 0.21285 acc: 0.96000 val_loss: 0.21050, val_acc: 0.96000
    Epoch [3600/10000], loss: 0.21255 acc: 0.96000 val_loss: 0.21023, val_acc: 0.96000
    Epoch [3610/10000], loss: 0.21225 acc: 0.96000 val_loss: 0.20996, val_acc: 0.96000
    Epoch [3620/10000], loss: 0.21196 acc: 0.96000 val_loss: 0.20970, val_acc: 0.96000
    Epoch [3630/10000], loss: 0.21166 acc: 0.96000 val_loss: 0.20943, val_acc: 0.96000
    Epoch [3640/10000], loss: 0.21137 acc: 0.96000 val_loss: 0.20917, val_acc: 0.96000
    Epoch [3650/10000], loss: 0.21107 acc: 0.96000 val_loss: 0.20891, val_acc: 0.96000
    Epoch [3660/10000], loss: 0.21078 acc: 0.96000 val_loss: 0.20865, val_acc: 0.96000
    Epoch [3670/10000], loss: 0.21049 acc: 0.96000 val_loss: 0.20839, val_acc: 0.96000
    Epoch [3680/10000], loss: 0.21020 acc: 0.96000 val_loss: 0.20813, val_acc: 0.96000
    Epoch [3690/10000], loss: 0.20991 acc: 0.96000 val_loss: 0.20787, val_acc: 0.96000
    Epoch [3700/10000], loss: 0.20963 acc: 0.96000 val_loss: 0.20761, val_acc: 0.96000
    Epoch [3710/10000], loss: 0.20934 acc: 0.96000 val_loss: 0.20736, val_acc: 0.96000
    Epoch [3720/10000], loss: 0.20905 acc: 0.96000 val_loss: 0.20710, val_acc: 0.96000
    Epoch [3730/10000], loss: 0.20877 acc: 0.96000 val_loss: 0.20685, val_acc: 0.96000
    Epoch [3740/10000], loss: 0.20849 acc: 0.96000 val_loss: 0.20659, val_acc: 0.96000
    Epoch [3750/10000], loss: 0.20821 acc: 0.96000 val_loss: 0.20634, val_acc: 0.96000
    Epoch [3760/10000], loss: 0.20792 acc: 0.96000 val_loss: 0.20609, val_acc: 0.96000
    Epoch [3770/10000], loss: 0.20765 acc: 0.96000 val_loss: 0.20584, val_acc: 0.96000
    Epoch [3780/10000], loss: 0.20737 acc: 0.96000 val_loss: 0.20559, val_acc: 0.96000
    Epoch [3790/10000], loss: 0.20709 acc: 0.96000 val_loss: 0.20535, val_acc: 0.96000
    Epoch [3800/10000], loss: 0.20681 acc: 0.96000 val_loss: 0.20510, val_acc: 0.96000
    Epoch [3810/10000], loss: 0.20654 acc: 0.96000 val_loss: 0.20485, val_acc: 0.96000
    Epoch [3820/10000], loss: 0.20626 acc: 0.96000 val_loss: 0.20461, val_acc: 0.96000
    Epoch [3830/10000], loss: 0.20599 acc: 0.96000 val_loss: 0.20437, val_acc: 0.96000
    Epoch [3840/10000], loss: 0.20572 acc: 0.96000 val_loss: 0.20412, val_acc: 0.96000
    Epoch [3850/10000], loss: 0.20545 acc: 0.96000 val_loss: 0.20388, val_acc: 0.96000
    Epoch [3860/10000], loss: 0.20518 acc: 0.96000 val_loss: 0.20364, val_acc: 0.96000
    Epoch [3870/10000], loss: 0.20491 acc: 0.96000 val_loss: 0.20340, val_acc: 0.96000
    Epoch [3880/10000], loss: 0.20464 acc: 0.96000 val_loss: 0.20316, val_acc: 0.96000
    Epoch [3890/10000], loss: 0.20437 acc: 0.96000 val_loss: 0.20292, val_acc: 0.96000
    Epoch [3900/10000], loss: 0.20411 acc: 0.96000 val_loss: 0.20269, val_acc: 0.96000
    Epoch [3910/10000], loss: 0.20384 acc: 0.96000 val_loss: 0.20245, val_acc: 0.96000
    Epoch [3920/10000], loss: 0.20358 acc: 0.96000 val_loss: 0.20222, val_acc: 0.96000
    Epoch [3930/10000], loss: 0.20332 acc: 0.96000 val_loss: 0.20198, val_acc: 0.96000
    Epoch [3940/10000], loss: 0.20305 acc: 0.96000 val_loss: 0.20175, val_acc: 0.96000
    Epoch [3950/10000], loss: 0.20279 acc: 0.96000 val_loss: 0.20152, val_acc: 0.96000
    Epoch [3960/10000], loss: 0.20253 acc: 0.96000 val_loss: 0.20128, val_acc: 0.96000
    Epoch [3970/10000], loss: 0.20227 acc: 0.96000 val_loss: 0.20105, val_acc: 0.96000
    Epoch [3980/10000], loss: 0.20202 acc: 0.96000 val_loss: 0.20082, val_acc: 0.96000
    Epoch [3990/10000], loss: 0.20176 acc: 0.96000 val_loss: 0.20059, val_acc: 0.96000
    Epoch [4000/10000], loss: 0.20150 acc: 0.96000 val_loss: 0.20037, val_acc: 0.96000
    Epoch [4010/10000], loss: 0.20125 acc: 0.96000 val_loss: 0.20014, val_acc: 0.96000
    Epoch [4020/10000], loss: 0.20099 acc: 0.97333 val_loss: 0.19991, val_acc: 0.96000
    Epoch [4030/10000], loss: 0.20074 acc: 0.97333 val_loss: 0.19969, val_acc: 0.96000
    Epoch [4040/10000], loss: 0.20049 acc: 0.97333 val_loss: 0.19946, val_acc: 0.96000
    Epoch [4050/10000], loss: 0.20024 acc: 0.97333 val_loss: 0.19924, val_acc: 0.96000
    Epoch [4060/10000], loss: 0.19999 acc: 0.97333 val_loss: 0.19902, val_acc: 0.96000
    Epoch [4070/10000], loss: 0.19974 acc: 0.97333 val_loss: 0.19880, val_acc: 0.96000
    Epoch [4080/10000], loss: 0.19949 acc: 0.97333 val_loss: 0.19858, val_acc: 0.96000
    Epoch [4090/10000], loss: 0.19924 acc: 0.97333 val_loss: 0.19835, val_acc: 0.96000
    Epoch [4100/10000], loss: 0.19899 acc: 0.97333 val_loss: 0.19814, val_acc: 0.96000
    Epoch [4110/10000], loss: 0.19875 acc: 0.97333 val_loss: 0.19792, val_acc: 0.96000
    Epoch [4120/10000], loss: 0.19850 acc: 0.97333 val_loss: 0.19770, val_acc: 0.96000
    Epoch [4130/10000], loss: 0.19826 acc: 0.97333 val_loss: 0.19748, val_acc: 0.96000
    Epoch [4140/10000], loss: 0.19802 acc: 0.97333 val_loss: 0.19727, val_acc: 0.96000
    Epoch [4150/10000], loss: 0.19777 acc: 0.97333 val_loss: 0.19705, val_acc: 0.96000
    Epoch [4160/10000], loss: 0.19753 acc: 0.97333 val_loss: 0.19684, val_acc: 0.96000
    Epoch [4170/10000], loss: 0.19729 acc: 0.97333 val_loss: 0.19662, val_acc: 0.96000
    Epoch [4180/10000], loss: 0.19705 acc: 0.97333 val_loss: 0.19641, val_acc: 0.96000
    Epoch [4190/10000], loss: 0.19681 acc: 0.97333 val_loss: 0.19620, val_acc: 0.96000
    Epoch [4200/10000], loss: 0.19658 acc: 0.97333 val_loss: 0.19599, val_acc: 0.96000
    Epoch [4210/10000], loss: 0.19634 acc: 0.97333 val_loss: 0.19578, val_acc: 0.96000
    Epoch [4220/10000], loss: 0.19610 acc: 0.97333 val_loss: 0.19557, val_acc: 0.96000
    Epoch [4230/10000], loss: 0.19587 acc: 0.97333 val_loss: 0.19536, val_acc: 0.96000
    Epoch [4240/10000], loss: 0.19563 acc: 0.97333 val_loss: 0.19515, val_acc: 0.96000
    Epoch [4250/10000], loss: 0.19540 acc: 0.97333 val_loss: 0.19494, val_acc: 0.96000
    Epoch [4260/10000], loss: 0.19517 acc: 0.97333 val_loss: 0.19474, val_acc: 0.96000
    Epoch [4270/10000], loss: 0.19493 acc: 0.97333 val_loss: 0.19453, val_acc: 0.96000
    Epoch [4280/10000], loss: 0.19470 acc: 0.97333 val_loss: 0.19433, val_acc: 0.96000
    Epoch [4290/10000], loss: 0.19447 acc: 0.97333 val_loss: 0.19412, val_acc: 0.96000
    Epoch [4300/10000], loss: 0.19424 acc: 0.97333 val_loss: 0.19392, val_acc: 0.96000
    Epoch [4310/10000], loss: 0.19401 acc: 0.97333 val_loss: 0.19372, val_acc: 0.96000
    Epoch [4320/10000], loss: 0.19379 acc: 0.97333 val_loss: 0.19351, val_acc: 0.96000
    Epoch [4330/10000], loss: 0.19356 acc: 0.97333 val_loss: 0.19331, val_acc: 0.96000
    Epoch [4340/10000], loss: 0.19333 acc: 0.97333 val_loss: 0.19311, val_acc: 0.96000
    Epoch [4350/10000], loss: 0.19311 acc: 0.97333 val_loss: 0.19291, val_acc: 0.96000
    Epoch [4360/10000], loss: 0.19288 acc: 0.97333 val_loss: 0.19271, val_acc: 0.96000
    Epoch [4370/10000], loss: 0.19266 acc: 0.97333 val_loss: 0.19252, val_acc: 0.96000
    Epoch [4380/10000], loss: 0.19243 acc: 0.97333 val_loss: 0.19232, val_acc: 0.96000
    Epoch [4390/10000], loss: 0.19221 acc: 0.97333 val_loss: 0.19212, val_acc: 0.96000
    Epoch [4400/10000], loss: 0.19199 acc: 0.97333 val_loss: 0.19192, val_acc: 0.96000
    Epoch [4410/10000], loss: 0.19177 acc: 0.97333 val_loss: 0.19173, val_acc: 0.96000
    Epoch [4420/10000], loss: 0.19155 acc: 0.97333 val_loss: 0.19153, val_acc: 0.96000
    Epoch [4430/10000], loss: 0.19133 acc: 0.97333 val_loss: 0.19134, val_acc: 0.96000
    Epoch [4440/10000], loss: 0.19111 acc: 0.97333 val_loss: 0.19115, val_acc: 0.96000
    Epoch [4450/10000], loss: 0.19089 acc: 0.97333 val_loss: 0.19095, val_acc: 0.96000
    Epoch [4460/10000], loss: 0.19068 acc: 0.97333 val_loss: 0.19076, val_acc: 0.96000
    Epoch [4470/10000], loss: 0.19046 acc: 0.97333 val_loss: 0.19057, val_acc: 0.96000
    Epoch [4480/10000], loss: 0.19024 acc: 0.97333 val_loss: 0.19038, val_acc: 0.96000
    Epoch [4490/10000], loss: 0.19003 acc: 0.97333 val_loss: 0.19019, val_acc: 0.96000
    Epoch [4500/10000], loss: 0.18981 acc: 0.97333 val_loss: 0.19000, val_acc: 0.96000
    Epoch [4510/10000], loss: 0.18960 acc: 0.97333 val_loss: 0.18981, val_acc: 0.96000
    Epoch [4520/10000], loss: 0.18939 acc: 0.97333 val_loss: 0.18962, val_acc: 0.96000
    Epoch [4530/10000], loss: 0.18918 acc: 0.97333 val_loss: 0.18944, val_acc: 0.96000
    Epoch [4540/10000], loss: 0.18896 acc: 0.97333 val_loss: 0.18925, val_acc: 0.96000
    Epoch [4550/10000], loss: 0.18875 acc: 0.97333 val_loss: 0.18906, val_acc: 0.96000
    Epoch [4560/10000], loss: 0.18854 acc: 0.97333 val_loss: 0.18888, val_acc: 0.96000
    Epoch [4570/10000], loss: 0.18833 acc: 0.97333 val_loss: 0.18869, val_acc: 0.96000
    Epoch [4580/10000], loss: 0.18813 acc: 0.97333 val_loss: 0.18851, val_acc: 0.96000
    Epoch [4590/10000], loss: 0.18792 acc: 0.97333 val_loss: 0.18833, val_acc: 0.96000
    Epoch [4600/10000], loss: 0.18771 acc: 0.97333 val_loss: 0.18814, val_acc: 0.96000
    Epoch [4610/10000], loss: 0.18750 acc: 0.97333 val_loss: 0.18796, val_acc: 0.96000
    Epoch [4620/10000], loss: 0.18730 acc: 0.97333 val_loss: 0.18778, val_acc: 0.96000
    Epoch [4630/10000], loss: 0.18709 acc: 0.97333 val_loss: 0.18760, val_acc: 0.96000
    Epoch [4640/10000], loss: 0.18689 acc: 0.97333 val_loss: 0.18742, val_acc: 0.96000
    Epoch [4650/10000], loss: 0.18669 acc: 0.97333 val_loss: 0.18724, val_acc: 0.96000
    Epoch [4660/10000], loss: 0.18648 acc: 0.97333 val_loss: 0.18706, val_acc: 0.96000
    Epoch [4670/10000], loss: 0.18628 acc: 0.97333 val_loss: 0.18688, val_acc: 0.96000
    Epoch [4680/10000], loss: 0.18608 acc: 0.97333 val_loss: 0.18670, val_acc: 0.96000
    Epoch [4690/10000], loss: 0.18588 acc: 0.97333 val_loss: 0.18653, val_acc: 0.96000
    Epoch [4700/10000], loss: 0.18568 acc: 0.97333 val_loss: 0.18635, val_acc: 0.96000
    Epoch [4710/10000], loss: 0.18548 acc: 0.97333 val_loss: 0.18617, val_acc: 0.96000
    Epoch [4720/10000], loss: 0.18528 acc: 0.97333 val_loss: 0.18600, val_acc: 0.96000
    Epoch [4730/10000], loss: 0.18508 acc: 0.97333 val_loss: 0.18582, val_acc: 0.96000
    Epoch [4740/10000], loss: 0.18488 acc: 0.97333 val_loss: 0.18565, val_acc: 0.96000
    Epoch [4750/10000], loss: 0.18468 acc: 0.97333 val_loss: 0.18548, val_acc: 0.96000
    Epoch [4760/10000], loss: 0.18449 acc: 0.97333 val_loss: 0.18530, val_acc: 0.96000
    Epoch [4770/10000], loss: 0.18429 acc: 0.97333 val_loss: 0.18513, val_acc: 0.96000
    Epoch [4780/10000], loss: 0.18410 acc: 0.97333 val_loss: 0.18496, val_acc: 0.96000
    Epoch [4790/10000], loss: 0.18390 acc: 0.97333 val_loss: 0.18479, val_acc: 0.96000
    Epoch [4800/10000], loss: 0.18371 acc: 0.97333 val_loss: 0.18462, val_acc: 0.96000
    Epoch [4810/10000], loss: 0.18352 acc: 0.97333 val_loss: 0.18445, val_acc: 0.96000
    Epoch [4820/10000], loss: 0.18332 acc: 0.97333 val_loss: 0.18428, val_acc: 0.96000
    Epoch [4830/10000], loss: 0.18313 acc: 0.97333 val_loss: 0.18411, val_acc: 0.96000
    Epoch [4840/10000], loss: 0.18294 acc: 0.97333 val_loss: 0.18394, val_acc: 0.96000
    Epoch [4850/10000], loss: 0.18275 acc: 0.97333 val_loss: 0.18377, val_acc: 0.96000
    Epoch [4860/10000], loss: 0.18256 acc: 0.97333 val_loss: 0.18361, val_acc: 0.96000
    Epoch [4870/10000], loss: 0.18237 acc: 0.97333 val_loss: 0.18344, val_acc: 0.96000
    Epoch [4880/10000], loss: 0.18218 acc: 0.97333 val_loss: 0.18327, val_acc: 0.96000
    Epoch [4890/10000], loss: 0.18199 acc: 0.97333 val_loss: 0.18311, val_acc: 0.96000
    Epoch [4900/10000], loss: 0.18180 acc: 0.97333 val_loss: 0.18294, val_acc: 0.96000
    Epoch [4910/10000], loss: 0.18162 acc: 0.97333 val_loss: 0.18278, val_acc: 0.96000
    Epoch [4920/10000], loss: 0.18143 acc: 0.97333 val_loss: 0.18261, val_acc: 0.96000
    Epoch [4930/10000], loss: 0.18124 acc: 0.97333 val_loss: 0.18245, val_acc: 0.96000
    Epoch [4940/10000], loss: 0.18106 acc: 0.97333 val_loss: 0.18229, val_acc: 0.96000
    Epoch [4950/10000], loss: 0.18087 acc: 0.97333 val_loss: 0.18212, val_acc: 0.96000
    Epoch [4960/10000], loss: 0.18069 acc: 0.97333 val_loss: 0.18196, val_acc: 0.96000
    Epoch [4970/10000], loss: 0.18050 acc: 0.97333 val_loss: 0.18180, val_acc: 0.96000
    Epoch [4980/10000], loss: 0.18032 acc: 0.97333 val_loss: 0.18164, val_acc: 0.96000
    Epoch [4990/10000], loss: 0.18014 acc: 0.97333 val_loss: 0.18148, val_acc: 0.96000
    Epoch [5000/10000], loss: 0.17996 acc: 0.97333 val_loss: 0.18132, val_acc: 0.96000
    Epoch [5010/10000], loss: 0.17978 acc: 0.97333 val_loss: 0.18116, val_acc: 0.96000
    Epoch [5020/10000], loss: 0.17959 acc: 0.97333 val_loss: 0.18100, val_acc: 0.96000
    Epoch [5030/10000], loss: 0.17941 acc: 0.97333 val_loss: 0.18084, val_acc: 0.96000
    Epoch [5040/10000], loss: 0.17923 acc: 0.97333 val_loss: 0.18069, val_acc: 0.96000
    Epoch [5050/10000], loss: 0.17906 acc: 0.97333 val_loss: 0.18053, val_acc: 0.96000
    Epoch [5060/10000], loss: 0.17888 acc: 0.97333 val_loss: 0.18037, val_acc: 0.96000
    Epoch [5070/10000], loss: 0.17870 acc: 0.97333 val_loss: 0.18022, val_acc: 0.96000
    Epoch [5080/10000], loss: 0.17852 acc: 0.97333 val_loss: 0.18006, val_acc: 0.96000
    Epoch [5090/10000], loss: 0.17834 acc: 0.97333 val_loss: 0.17991, val_acc: 0.96000
    Epoch [5100/10000], loss: 0.17817 acc: 0.97333 val_loss: 0.17975, val_acc: 0.96000
    Epoch [5110/10000], loss: 0.17799 acc: 0.97333 val_loss: 0.17960, val_acc: 0.96000
    Epoch [5120/10000], loss: 0.17782 acc: 0.97333 val_loss: 0.17944, val_acc: 0.96000
    Epoch [5130/10000], loss: 0.17764 acc: 0.97333 val_loss: 0.17929, val_acc: 0.96000
    Epoch [5140/10000], loss: 0.17747 acc: 0.97333 val_loss: 0.17914, val_acc: 0.96000
    Epoch [5150/10000], loss: 0.17729 acc: 0.97333 val_loss: 0.17899, val_acc: 0.96000
    Epoch [5160/10000], loss: 0.17712 acc: 0.97333 val_loss: 0.17883, val_acc: 0.96000
    Epoch [5170/10000], loss: 0.17695 acc: 0.97333 val_loss: 0.17868, val_acc: 0.96000
    Epoch [5180/10000], loss: 0.17677 acc: 0.97333 val_loss: 0.17853, val_acc: 0.96000
    Epoch [5190/10000], loss: 0.17660 acc: 0.97333 val_loss: 0.17838, val_acc: 0.96000
    Epoch [5200/10000], loss: 0.17643 acc: 0.97333 val_loss: 0.17823, val_acc: 0.96000
    Epoch [5210/10000], loss: 0.17626 acc: 0.97333 val_loss: 0.17808, val_acc: 0.96000
    Epoch [5220/10000], loss: 0.17609 acc: 0.97333 val_loss: 0.17793, val_acc: 0.96000
    Epoch [5230/10000], loss: 0.17592 acc: 0.97333 val_loss: 0.17779, val_acc: 0.96000
    Epoch [5240/10000], loss: 0.17575 acc: 0.97333 val_loss: 0.17764, val_acc: 0.96000
    Epoch [5250/10000], loss: 0.17558 acc: 0.97333 val_loss: 0.17749, val_acc: 0.96000
    Epoch [5260/10000], loss: 0.17542 acc: 0.97333 val_loss: 0.17734, val_acc: 0.96000
    Epoch [5270/10000], loss: 0.17525 acc: 0.97333 val_loss: 0.17720, val_acc: 0.96000
    Epoch [5280/10000], loss: 0.17508 acc: 0.97333 val_loss: 0.17705, val_acc: 0.96000
    Epoch [5290/10000], loss: 0.17491 acc: 0.97333 val_loss: 0.17690, val_acc: 0.96000
    Epoch [5300/10000], loss: 0.17475 acc: 0.97333 val_loss: 0.17676, val_acc: 0.96000
    Epoch [5310/10000], loss: 0.17458 acc: 0.97333 val_loss: 0.17661, val_acc: 0.96000
    Epoch [5320/10000], loss: 0.17442 acc: 0.97333 val_loss: 0.17647, val_acc: 0.96000
    Epoch [5330/10000], loss: 0.17425 acc: 0.97333 val_loss: 0.17633, val_acc: 0.96000
    Epoch [5340/10000], loss: 0.17409 acc: 0.97333 val_loss: 0.17618, val_acc: 0.96000
    Epoch [5350/10000], loss: 0.17392 acc: 0.97333 val_loss: 0.17604, val_acc: 0.96000
    Epoch [5360/10000], loss: 0.17376 acc: 0.97333 val_loss: 0.17590, val_acc: 0.96000
    Epoch [5370/10000], loss: 0.17360 acc: 0.97333 val_loss: 0.17576, val_acc: 0.96000
    Epoch [5380/10000], loss: 0.17344 acc: 0.97333 val_loss: 0.17561, val_acc: 0.96000
    Epoch [5390/10000], loss: 0.17327 acc: 0.97333 val_loss: 0.17547, val_acc: 0.96000
    Epoch [5400/10000], loss: 0.17311 acc: 0.97333 val_loss: 0.17533, val_acc: 0.96000
    Epoch [5410/10000], loss: 0.17295 acc: 0.97333 val_loss: 0.17519, val_acc: 0.96000
    Epoch [5420/10000], loss: 0.17279 acc: 0.97333 val_loss: 0.17505, val_acc: 0.96000
    Epoch [5430/10000], loss: 0.17263 acc: 0.97333 val_loss: 0.17491, val_acc: 0.96000
    Epoch [5440/10000], loss: 0.17247 acc: 0.97333 val_loss: 0.17477, val_acc: 0.96000
    Epoch [5450/10000], loss: 0.17231 acc: 0.97333 val_loss: 0.17463, val_acc: 0.96000
    Epoch [5460/10000], loss: 0.17216 acc: 0.97333 val_loss: 0.17450, val_acc: 0.96000
    Epoch [5470/10000], loss: 0.17200 acc: 0.97333 val_loss: 0.17436, val_acc: 0.96000
    Epoch [5480/10000], loss: 0.17184 acc: 0.97333 val_loss: 0.17422, val_acc: 0.96000
    Epoch [5490/10000], loss: 0.17168 acc: 0.97333 val_loss: 0.17408, val_acc: 0.96000
    Epoch [5500/10000], loss: 0.17153 acc: 0.97333 val_loss: 0.17395, val_acc: 0.96000
    Epoch [5510/10000], loss: 0.17137 acc: 0.97333 val_loss: 0.17381, val_acc: 0.96000
    Epoch [5520/10000], loss: 0.17121 acc: 0.97333 val_loss: 0.17368, val_acc: 0.96000
    Epoch [5530/10000], loss: 0.17106 acc: 0.97333 val_loss: 0.17354, val_acc: 0.96000
    Epoch [5540/10000], loss: 0.17090 acc: 0.97333 val_loss: 0.17340, val_acc: 0.96000
    Epoch [5550/10000], loss: 0.17075 acc: 0.97333 val_loss: 0.17327, val_acc: 0.96000
    Epoch [5560/10000], loss: 0.17059 acc: 0.97333 val_loss: 0.17314, val_acc: 0.96000
    Epoch [5570/10000], loss: 0.17044 acc: 0.97333 val_loss: 0.17300, val_acc: 0.96000
    Epoch [5580/10000], loss: 0.17029 acc: 0.98667 val_loss: 0.17287, val_acc: 0.96000
    Epoch [5590/10000], loss: 0.17014 acc: 0.98667 val_loss: 0.17274, val_acc: 0.96000
    Epoch [5600/10000], loss: 0.16998 acc: 0.98667 val_loss: 0.17260, val_acc: 0.96000
    Epoch [5610/10000], loss: 0.16983 acc: 0.98667 val_loss: 0.17247, val_acc: 0.96000
    Epoch [5620/10000], loss: 0.16968 acc: 0.98667 val_loss: 0.17234, val_acc: 0.96000
    Epoch [5630/10000], loss: 0.16953 acc: 0.98667 val_loss: 0.17221, val_acc: 0.96000
    Epoch [5640/10000], loss: 0.16938 acc: 0.98667 val_loss: 0.17208, val_acc: 0.96000
    Epoch [5650/10000], loss: 0.16923 acc: 0.98667 val_loss: 0.17195, val_acc: 0.96000
    Epoch [5660/10000], loss: 0.16908 acc: 0.98667 val_loss: 0.17182, val_acc: 0.96000
    Epoch [5670/10000], loss: 0.16893 acc: 0.98667 val_loss: 0.17169, val_acc: 0.96000
    Epoch [5680/10000], loss: 0.16878 acc: 0.98667 val_loss: 0.17156, val_acc: 0.96000
    Epoch [5690/10000], loss: 0.16863 acc: 0.98667 val_loss: 0.17143, val_acc: 0.96000
    Epoch [5700/10000], loss: 0.16848 acc: 0.98667 val_loss: 0.17130, val_acc: 0.96000
    Epoch [5710/10000], loss: 0.16834 acc: 0.98667 val_loss: 0.17117, val_acc: 0.96000
    Epoch [5720/10000], loss: 0.16819 acc: 0.98667 val_loss: 0.17104, val_acc: 0.96000
    Epoch [5730/10000], loss: 0.16804 acc: 0.98667 val_loss: 0.17092, val_acc: 0.96000
    Epoch [5740/10000], loss: 0.16790 acc: 0.98667 val_loss: 0.17079, val_acc: 0.96000
    Epoch [5750/10000], loss: 0.16775 acc: 0.98667 val_loss: 0.17066, val_acc: 0.96000
    Epoch [5760/10000], loss: 0.16760 acc: 0.98667 val_loss: 0.17054, val_acc: 0.96000
    Epoch [5770/10000], loss: 0.16746 acc: 0.98667 val_loss: 0.17041, val_acc: 0.96000
    Epoch [5780/10000], loss: 0.16731 acc: 0.98667 val_loss: 0.17028, val_acc: 0.96000
    Epoch [5790/10000], loss: 0.16717 acc: 0.98667 val_loss: 0.17016, val_acc: 0.96000
    Epoch [5800/10000], loss: 0.16703 acc: 0.98667 val_loss: 0.17003, val_acc: 0.96000
    Epoch [5810/10000], loss: 0.16688 acc: 0.98667 val_loss: 0.16991, val_acc: 0.96000
    Epoch [5820/10000], loss: 0.16674 acc: 0.98667 val_loss: 0.16978, val_acc: 0.96000
    Epoch [5830/10000], loss: 0.16660 acc: 0.98667 val_loss: 0.16966, val_acc: 0.96000
    Epoch [5840/10000], loss: 0.16645 acc: 0.98667 val_loss: 0.16954, val_acc: 0.96000
    Epoch [5850/10000], loss: 0.16631 acc: 0.98667 val_loss: 0.16941, val_acc: 0.96000
    Epoch [5860/10000], loss: 0.16617 acc: 0.98667 val_loss: 0.16929, val_acc: 0.96000
    Epoch [5870/10000], loss: 0.16603 acc: 0.98667 val_loss: 0.16917, val_acc: 0.96000
    Epoch [5880/10000], loss: 0.16589 acc: 0.98667 val_loss: 0.16905, val_acc: 0.96000
    Epoch [5890/10000], loss: 0.16575 acc: 0.98667 val_loss: 0.16892, val_acc: 0.96000
    Epoch [5900/10000], loss: 0.16561 acc: 0.98667 val_loss: 0.16880, val_acc: 0.96000
    Epoch [5910/10000], loss: 0.16547 acc: 0.98667 val_loss: 0.16868, val_acc: 0.96000
    Epoch [5920/10000], loss: 0.16533 acc: 0.98667 val_loss: 0.16856, val_acc: 0.96000
    Epoch [5930/10000], loss: 0.16519 acc: 0.98667 val_loss: 0.16844, val_acc: 0.96000
    Epoch [5940/10000], loss: 0.16505 acc: 0.98667 val_loss: 0.16832, val_acc: 0.96000
    Epoch [5950/10000], loss: 0.16491 acc: 0.98667 val_loss: 0.16820, val_acc: 0.96000
    Epoch [5960/10000], loss: 0.16477 acc: 0.98667 val_loss: 0.16808, val_acc: 0.96000
    Epoch [5970/10000], loss: 0.16464 acc: 0.98667 val_loss: 0.16796, val_acc: 0.96000
    Epoch [5980/10000], loss: 0.16450 acc: 0.98667 val_loss: 0.16784, val_acc: 0.96000
    Epoch [5990/10000], loss: 0.16436 acc: 0.98667 val_loss: 0.16772, val_acc: 0.96000
    Epoch [6000/10000], loss: 0.16423 acc: 0.98667 val_loss: 0.16761, val_acc: 0.96000
    Epoch [6010/10000], loss: 0.16409 acc: 0.98667 val_loss: 0.16749, val_acc: 0.96000
    Epoch [6020/10000], loss: 0.16396 acc: 0.98667 val_loss: 0.16737, val_acc: 0.96000
    Epoch [6030/10000], loss: 0.16382 acc: 0.98667 val_loss: 0.16725, val_acc: 0.96000
    Epoch [6040/10000], loss: 0.16368 acc: 0.98667 val_loss: 0.16714, val_acc: 0.96000
    Epoch [6050/10000], loss: 0.16355 acc: 0.98667 val_loss: 0.16702, val_acc: 0.96000
    Epoch [6060/10000], loss: 0.16342 acc: 0.98667 val_loss: 0.16690, val_acc: 0.96000
    Epoch [6070/10000], loss: 0.16328 acc: 0.98667 val_loss: 0.16679, val_acc: 0.96000
    Epoch [6080/10000], loss: 0.16315 acc: 0.98667 val_loss: 0.16667, val_acc: 0.96000
    Epoch [6090/10000], loss: 0.16302 acc: 0.98667 val_loss: 0.16656, val_acc: 0.96000
    Epoch [6100/10000], loss: 0.16288 acc: 0.98667 val_loss: 0.16644, val_acc: 0.96000
    Epoch [6110/10000], loss: 0.16275 acc: 0.98667 val_loss: 0.16633, val_acc: 0.96000
    Epoch [6120/10000], loss: 0.16262 acc: 0.98667 val_loss: 0.16621, val_acc: 0.96000
    Epoch [6130/10000], loss: 0.16249 acc: 0.98667 val_loss: 0.16610, val_acc: 0.96000
    Epoch [6140/10000], loss: 0.16235 acc: 0.98667 val_loss: 0.16599, val_acc: 0.96000
    Epoch [6150/10000], loss: 0.16222 acc: 0.98667 val_loss: 0.16587, val_acc: 0.96000
    Epoch [6160/10000], loss: 0.16209 acc: 0.98667 val_loss: 0.16576, val_acc: 0.96000
    Epoch [6170/10000], loss: 0.16196 acc: 0.98667 val_loss: 0.16565, val_acc: 0.96000
    Epoch [6180/10000], loss: 0.16183 acc: 0.98667 val_loss: 0.16554, val_acc: 0.96000
    Epoch [6190/10000], loss: 0.16170 acc: 0.98667 val_loss: 0.16542, val_acc: 0.96000
    Epoch [6200/10000], loss: 0.16157 acc: 0.98667 val_loss: 0.16531, val_acc: 0.96000
    Epoch [6210/10000], loss: 0.16144 acc: 0.98667 val_loss: 0.16520, val_acc: 0.96000
    Epoch [6220/10000], loss: 0.16132 acc: 0.98667 val_loss: 0.16509, val_acc: 0.96000
    Epoch [6230/10000], loss: 0.16119 acc: 0.98667 val_loss: 0.16498, val_acc: 0.96000
    Epoch [6240/10000], loss: 0.16106 acc: 0.98667 val_loss: 0.16487, val_acc: 0.96000
    Epoch [6250/10000], loss: 0.16093 acc: 0.98667 val_loss: 0.16476, val_acc: 0.96000
    Epoch [6260/10000], loss: 0.16080 acc: 0.98667 val_loss: 0.16465, val_acc: 0.96000
    Epoch [6270/10000], loss: 0.16068 acc: 0.98667 val_loss: 0.16454, val_acc: 0.96000
    Epoch [6280/10000], loss: 0.16055 acc: 0.98667 val_loss: 0.16443, val_acc: 0.96000
    Epoch [6290/10000], loss: 0.16042 acc: 0.98667 val_loss: 0.16432, val_acc: 0.96000
    Epoch [6300/10000], loss: 0.16030 acc: 0.98667 val_loss: 0.16421, val_acc: 0.96000
    Epoch [6310/10000], loss: 0.16017 acc: 0.98667 val_loss: 0.16410, val_acc: 0.96000
    Epoch [6320/10000], loss: 0.16005 acc: 0.98667 val_loss: 0.16399, val_acc: 0.96000
    Epoch [6330/10000], loss: 0.15992 acc: 0.98667 val_loss: 0.16389, val_acc: 0.96000
    Epoch [6340/10000], loss: 0.15980 acc: 0.98667 val_loss: 0.16378, val_acc: 0.96000
    Epoch [6350/10000], loss: 0.15967 acc: 0.98667 val_loss: 0.16367, val_acc: 0.96000
    Epoch [6360/10000], loss: 0.15955 acc: 0.98667 val_loss: 0.16356, val_acc: 0.96000
    Epoch [6370/10000], loss: 0.15942 acc: 0.98667 val_loss: 0.16346, val_acc: 0.96000
    Epoch [6380/10000], loss: 0.15930 acc: 0.98667 val_loss: 0.16335, val_acc: 0.96000
    Epoch [6390/10000], loss: 0.15918 acc: 0.98667 val_loss: 0.16325, val_acc: 0.96000
    Epoch [6400/10000], loss: 0.15905 acc: 0.98667 val_loss: 0.16314, val_acc: 0.96000
    Epoch [6410/10000], loss: 0.15893 acc: 0.98667 val_loss: 0.16303, val_acc: 0.96000
    Epoch [6420/10000], loss: 0.15881 acc: 0.98667 val_loss: 0.16293, val_acc: 0.96000
    Epoch [6430/10000], loss: 0.15869 acc: 0.98667 val_loss: 0.16282, val_acc: 0.96000
    Epoch [6440/10000], loss: 0.15857 acc: 0.98667 val_loss: 0.16272, val_acc: 0.96000
    Epoch [6450/10000], loss: 0.15844 acc: 0.98667 val_loss: 0.16261, val_acc: 0.96000
    Epoch [6460/10000], loss: 0.15832 acc: 0.98667 val_loss: 0.16251, val_acc: 0.96000
    Epoch [6470/10000], loss: 0.15820 acc: 0.98667 val_loss: 0.16241, val_acc: 0.96000
    Epoch [6480/10000], loss: 0.15808 acc: 0.98667 val_loss: 0.16230, val_acc: 0.96000
    Epoch [6490/10000], loss: 0.15796 acc: 0.98667 val_loss: 0.16220, val_acc: 0.96000
    Epoch [6500/10000], loss: 0.15784 acc: 0.98667 val_loss: 0.16210, val_acc: 0.96000
    Epoch [6510/10000], loss: 0.15772 acc: 0.98667 val_loss: 0.16199, val_acc: 0.96000
    Epoch [6520/10000], loss: 0.15760 acc: 0.98667 val_loss: 0.16189, val_acc: 0.96000
    Epoch [6530/10000], loss: 0.15748 acc: 0.98667 val_loss: 0.16179, val_acc: 0.96000
    Epoch [6540/10000], loss: 0.15736 acc: 0.98667 val_loss: 0.16169, val_acc: 0.96000
    Epoch [6550/10000], loss: 0.15725 acc: 0.98667 val_loss: 0.16158, val_acc: 0.96000
    Epoch [6560/10000], loss: 0.15713 acc: 0.98667 val_loss: 0.16148, val_acc: 0.96000
    Epoch [6570/10000], loss: 0.15701 acc: 0.98667 val_loss: 0.16138, val_acc: 0.96000
    Epoch [6580/10000], loss: 0.15689 acc: 0.98667 val_loss: 0.16128, val_acc: 0.96000
    Epoch [6590/10000], loss: 0.15678 acc: 0.98667 val_loss: 0.16118, val_acc: 0.96000
    Epoch [6600/10000], loss: 0.15666 acc: 0.98667 val_loss: 0.16108, val_acc: 0.96000
    Epoch [6610/10000], loss: 0.15654 acc: 0.98667 val_loss: 0.16098, val_acc: 0.96000
    Epoch [6620/10000], loss: 0.15643 acc: 0.98667 val_loss: 0.16088, val_acc: 0.96000
    Epoch [6630/10000], loss: 0.15631 acc: 0.98667 val_loss: 0.16078, val_acc: 0.96000
    Epoch [6640/10000], loss: 0.15619 acc: 0.98667 val_loss: 0.16068, val_acc: 0.96000
    Epoch [6650/10000], loss: 0.15608 acc: 0.98667 val_loss: 0.16058, val_acc: 0.96000
    Epoch [6660/10000], loss: 0.15596 acc: 0.98667 val_loss: 0.16048, val_acc: 0.96000
    Epoch [6670/10000], loss: 0.15585 acc: 0.98667 val_loss: 0.16038, val_acc: 0.96000
    Epoch [6680/10000], loss: 0.15573 acc: 0.98667 val_loss: 0.16028, val_acc: 0.96000
    Epoch [6690/10000], loss: 0.15562 acc: 0.98667 val_loss: 0.16019, val_acc: 0.96000
    Epoch [6700/10000], loss: 0.15550 acc: 0.98667 val_loss: 0.16009, val_acc: 0.96000
    Epoch [6710/10000], loss: 0.15539 acc: 0.98667 val_loss: 0.15999, val_acc: 0.96000
    Epoch [6720/10000], loss: 0.15528 acc: 0.98667 val_loss: 0.15989, val_acc: 0.96000
    Epoch [6730/10000], loss: 0.15516 acc: 0.98667 val_loss: 0.15980, val_acc: 0.96000
    Epoch [6740/10000], loss: 0.15505 acc: 0.98667 val_loss: 0.15970, val_acc: 0.96000
    Epoch [6750/10000], loss: 0.15494 acc: 0.98667 val_loss: 0.15960, val_acc: 0.96000
    Epoch [6760/10000], loss: 0.15483 acc: 0.98667 val_loss: 0.15951, val_acc: 0.96000
    Epoch [6770/10000], loss: 0.15471 acc: 0.98667 val_loss: 0.15941, val_acc: 0.96000
    Epoch [6780/10000], loss: 0.15460 acc: 0.98667 val_loss: 0.15931, val_acc: 0.96000
    Epoch [6790/10000], loss: 0.15449 acc: 0.98667 val_loss: 0.15922, val_acc: 0.96000
    Epoch [6800/10000], loss: 0.15438 acc: 0.98667 val_loss: 0.15912, val_acc: 0.96000
    Epoch [6810/10000], loss: 0.15427 acc: 0.98667 val_loss: 0.15903, val_acc: 0.96000
    Epoch [6820/10000], loss: 0.15416 acc: 0.98667 val_loss: 0.15893, val_acc: 0.96000
    Epoch [6830/10000], loss: 0.15405 acc: 0.98667 val_loss: 0.15884, val_acc: 0.96000
    Epoch [6840/10000], loss: 0.15394 acc: 0.98667 val_loss: 0.15874, val_acc: 0.96000
    Epoch [6850/10000], loss: 0.15383 acc: 0.98667 val_loss: 0.15865, val_acc: 0.96000
    Epoch [6860/10000], loss: 0.15372 acc: 0.98667 val_loss: 0.15855, val_acc: 0.96000
    Epoch [6870/10000], loss: 0.15361 acc: 0.98667 val_loss: 0.15846, val_acc: 0.96000
    Epoch [6880/10000], loss: 0.15350 acc: 0.98667 val_loss: 0.15837, val_acc: 0.96000
    Epoch [6890/10000], loss: 0.15339 acc: 0.98667 val_loss: 0.15827, val_acc: 0.96000
    Epoch [6900/10000], loss: 0.15328 acc: 0.98667 val_loss: 0.15818, val_acc: 0.96000
    Epoch [6910/10000], loss: 0.15317 acc: 0.98667 val_loss: 0.15809, val_acc: 0.96000
    Epoch [6920/10000], loss: 0.15306 acc: 0.98667 val_loss: 0.15800, val_acc: 0.96000
    Epoch [6930/10000], loss: 0.15295 acc: 0.98667 val_loss: 0.15790, val_acc: 0.96000
    Epoch [6940/10000], loss: 0.15285 acc: 0.98667 val_loss: 0.15781, val_acc: 0.96000
    Epoch [6950/10000], loss: 0.15274 acc: 0.98667 val_loss: 0.15772, val_acc: 0.96000
    Epoch [6960/10000], loss: 0.15263 acc: 0.98667 val_loss: 0.15763, val_acc: 0.96000
    Epoch [6970/10000], loss: 0.15252 acc: 0.98667 val_loss: 0.15754, val_acc: 0.96000
    Epoch [6980/10000], loss: 0.15242 acc: 0.98667 val_loss: 0.15744, val_acc: 0.96000
    Epoch [6990/10000], loss: 0.15231 acc: 0.98667 val_loss: 0.15735, val_acc: 0.96000
    Epoch [7000/10000], loss: 0.15220 acc: 0.98667 val_loss: 0.15726, val_acc: 0.96000
    Epoch [7010/10000], loss: 0.15210 acc: 0.98667 val_loss: 0.15717, val_acc: 0.96000
    Epoch [7020/10000], loss: 0.15199 acc: 0.98667 val_loss: 0.15708, val_acc: 0.96000
    Epoch [7030/10000], loss: 0.15189 acc: 0.98667 val_loss: 0.15699, val_acc: 0.96000
    Epoch [7040/10000], loss: 0.15178 acc: 0.98667 val_loss: 0.15690, val_acc: 0.96000
    Epoch [7050/10000], loss: 0.15168 acc: 0.98667 val_loss: 0.15681, val_acc: 0.96000
    Epoch [7060/10000], loss: 0.15157 acc: 0.98667 val_loss: 0.15672, val_acc: 0.96000
    Epoch [7070/10000], loss: 0.15147 acc: 0.98667 val_loss: 0.15663, val_acc: 0.96000
    Epoch [7080/10000], loss: 0.15136 acc: 0.98667 val_loss: 0.15654, val_acc: 0.96000
    Epoch [7090/10000], loss: 0.15126 acc: 0.98667 val_loss: 0.15645, val_acc: 0.96000
    Epoch [7100/10000], loss: 0.15116 acc: 0.98667 val_loss: 0.15637, val_acc: 0.96000
    Epoch [7110/10000], loss: 0.15105 acc: 0.98667 val_loss: 0.15628, val_acc: 0.96000
    Epoch [7120/10000], loss: 0.15095 acc: 0.98667 val_loss: 0.15619, val_acc: 0.96000
    Epoch [7130/10000], loss: 0.15085 acc: 0.98667 val_loss: 0.15610, val_acc: 0.96000
    Epoch [7140/10000], loss: 0.15074 acc: 0.98667 val_loss: 0.15601, val_acc: 0.96000
    Epoch [7150/10000], loss: 0.15064 acc: 0.98667 val_loss: 0.15593, val_acc: 0.96000
    Epoch [7160/10000], loss: 0.15054 acc: 0.98667 val_loss: 0.15584, val_acc: 0.96000
    Epoch [7170/10000], loss: 0.15044 acc: 0.98667 val_loss: 0.15575, val_acc: 0.96000
    Epoch [7180/10000], loss: 0.15033 acc: 0.98667 val_loss: 0.15566, val_acc: 0.96000
    Epoch [7190/10000], loss: 0.15023 acc: 0.98667 val_loss: 0.15558, val_acc: 0.96000
    Epoch [7200/10000], loss: 0.15013 acc: 0.98667 val_loss: 0.15549, val_acc: 0.96000
    Epoch [7210/10000], loss: 0.15003 acc: 0.98667 val_loss: 0.15541, val_acc: 0.96000
    Epoch [7220/10000], loss: 0.14993 acc: 0.98667 val_loss: 0.15532, val_acc: 0.96000
    Epoch [7230/10000], loss: 0.14983 acc: 0.98667 val_loss: 0.15523, val_acc: 0.96000
    Epoch [7240/10000], loss: 0.14973 acc: 0.98667 val_loss: 0.15515, val_acc: 0.96000
    Epoch [7250/10000], loss: 0.14963 acc: 0.98667 val_loss: 0.15506, val_acc: 0.96000
    Epoch [7260/10000], loss: 0.14953 acc: 0.98667 val_loss: 0.15498, val_acc: 0.96000
    Epoch [7270/10000], loss: 0.14943 acc: 0.98667 val_loss: 0.15489, val_acc: 0.96000
    Epoch [7280/10000], loss: 0.14933 acc: 0.98667 val_loss: 0.15481, val_acc: 0.96000
    Epoch [7290/10000], loss: 0.14923 acc: 0.98667 val_loss: 0.15472, val_acc: 0.96000
    Epoch [7300/10000], loss: 0.14913 acc: 0.98667 val_loss: 0.15464, val_acc: 0.96000
    Epoch [7310/10000], loss: 0.14903 acc: 0.98667 val_loss: 0.15455, val_acc: 0.96000
    Epoch [7320/10000], loss: 0.14893 acc: 0.98667 val_loss: 0.15447, val_acc: 0.96000
    Epoch [7330/10000], loss: 0.14883 acc: 0.98667 val_loss: 0.15439, val_acc: 0.96000
    Epoch [7340/10000], loss: 0.14873 acc: 0.98667 val_loss: 0.15430, val_acc: 0.96000
    Epoch [7350/10000], loss: 0.14863 acc: 0.98667 val_loss: 0.15422, val_acc: 0.96000
    Epoch [7360/10000], loss: 0.14854 acc: 0.98667 val_loss: 0.15413, val_acc: 0.96000
    Epoch [7370/10000], loss: 0.14844 acc: 0.98667 val_loss: 0.15405, val_acc: 0.96000
    Epoch [7380/10000], loss: 0.14834 acc: 0.98667 val_loss: 0.15397, val_acc: 0.96000
    Epoch [7390/10000], loss: 0.14824 acc: 0.98667 val_loss: 0.15389, val_acc: 0.96000
    Epoch [7400/10000], loss: 0.14815 acc: 0.98667 val_loss: 0.15380, val_acc: 0.96000
    Epoch [7410/10000], loss: 0.14805 acc: 0.98667 val_loss: 0.15372, val_acc: 0.96000
    Epoch [7420/10000], loss: 0.14795 acc: 0.98667 val_loss: 0.15364, val_acc: 0.96000
    Epoch [7430/10000], loss: 0.14786 acc: 0.98667 val_loss: 0.15356, val_acc: 0.96000
    Epoch [7440/10000], loss: 0.14776 acc: 0.98667 val_loss: 0.15348, val_acc: 0.96000
    Epoch [7450/10000], loss: 0.14767 acc: 0.98667 val_loss: 0.15339, val_acc: 0.96000
    Epoch [7460/10000], loss: 0.14757 acc: 0.98667 val_loss: 0.15331, val_acc: 0.96000
    Epoch [7470/10000], loss: 0.14747 acc: 0.98667 val_loss: 0.15323, val_acc: 0.96000
    Epoch [7480/10000], loss: 0.14738 acc: 0.98667 val_loss: 0.15315, val_acc: 0.96000
    Epoch [7490/10000], loss: 0.14728 acc: 0.98667 val_loss: 0.15307, val_acc: 0.96000
    Epoch [7500/10000], loss: 0.14719 acc: 0.98667 val_loss: 0.15299, val_acc: 0.96000
    Epoch [7510/10000], loss: 0.14709 acc: 0.98667 val_loss: 0.15291, val_acc: 0.96000
    Epoch [7520/10000], loss: 0.14700 acc: 0.98667 val_loss: 0.15283, val_acc: 0.96000
    Epoch [7530/10000], loss: 0.14691 acc: 0.98667 val_loss: 0.15275, val_acc: 0.96000
    Epoch [7540/10000], loss: 0.14681 acc: 0.98667 val_loss: 0.15267, val_acc: 0.96000
    Epoch [7550/10000], loss: 0.14672 acc: 0.98667 val_loss: 0.15259, val_acc: 0.96000
    Epoch [7560/10000], loss: 0.14662 acc: 0.98667 val_loss: 0.15251, val_acc: 0.96000
    Epoch [7570/10000], loss: 0.14653 acc: 0.98667 val_loss: 0.15243, val_acc: 0.96000
    Epoch [7580/10000], loss: 0.14644 acc: 0.98667 val_loss: 0.15235, val_acc: 0.96000
    Epoch [7590/10000], loss: 0.14634 acc: 0.98667 val_loss: 0.15227, val_acc: 0.96000
    Epoch [7600/10000], loss: 0.14625 acc: 0.98667 val_loss: 0.15219, val_acc: 0.96000
    Epoch [7610/10000], loss: 0.14616 acc: 0.98667 val_loss: 0.15211, val_acc: 0.96000
    Epoch [7620/10000], loss: 0.14607 acc: 0.98667 val_loss: 0.15204, val_acc: 0.96000
    Epoch [7630/10000], loss: 0.14597 acc: 0.98667 val_loss: 0.15196, val_acc: 0.96000
    Epoch [7640/10000], loss: 0.14588 acc: 0.98667 val_loss: 0.15188, val_acc: 0.96000
    Epoch [7650/10000], loss: 0.14579 acc: 0.98667 val_loss: 0.15180, val_acc: 0.96000
    Epoch [7660/10000], loss: 0.14570 acc: 0.98667 val_loss: 0.15172, val_acc: 0.96000
    Epoch [7670/10000], loss: 0.14561 acc: 0.98667 val_loss: 0.15165, val_acc: 0.96000
    Epoch [7680/10000], loss: 0.14552 acc: 0.98667 val_loss: 0.15157, val_acc: 0.96000
    Epoch [7690/10000], loss: 0.14542 acc: 0.98667 val_loss: 0.15149, val_acc: 0.96000
    Epoch [7700/10000], loss: 0.14533 acc: 0.98667 val_loss: 0.15142, val_acc: 0.96000
    Epoch [7710/10000], loss: 0.14524 acc: 0.98667 val_loss: 0.15134, val_acc: 0.96000
    Epoch [7720/10000], loss: 0.14515 acc: 0.98667 val_loss: 0.15126, val_acc: 0.96000
    Epoch [7730/10000], loss: 0.14506 acc: 0.98667 val_loss: 0.15119, val_acc: 0.96000
    Epoch [7740/10000], loss: 0.14497 acc: 0.98667 val_loss: 0.15111, val_acc: 0.96000
    Epoch [7750/10000], loss: 0.14488 acc: 0.98667 val_loss: 0.15103, val_acc: 0.96000
    Epoch [7760/10000], loss: 0.14479 acc: 0.98667 val_loss: 0.15096, val_acc: 0.96000
    Epoch [7770/10000], loss: 0.14470 acc: 0.98667 val_loss: 0.15088, val_acc: 0.96000
    Epoch [7780/10000], loss: 0.14461 acc: 0.98667 val_loss: 0.15081, val_acc: 0.96000
    Epoch [7790/10000], loss: 0.14452 acc: 0.98667 val_loss: 0.15073, val_acc: 0.96000
    Epoch [7800/10000], loss: 0.14444 acc: 0.98667 val_loss: 0.15066, val_acc: 0.96000
    Epoch [7810/10000], loss: 0.14435 acc: 0.98667 val_loss: 0.15058, val_acc: 0.96000
    Epoch [7820/10000], loss: 0.14426 acc: 0.98667 val_loss: 0.15051, val_acc: 0.96000
    Epoch [7830/10000], loss: 0.14417 acc: 0.98667 val_loss: 0.15043, val_acc: 0.96000
    Epoch [7840/10000], loss: 0.14408 acc: 0.98667 val_loss: 0.15036, val_acc: 0.96000
    Epoch [7850/10000], loss: 0.14399 acc: 0.98667 val_loss: 0.15028, val_acc: 0.96000
    Epoch [7860/10000], loss: 0.14391 acc: 0.98667 val_loss: 0.15021, val_acc: 0.96000
    Epoch [7870/10000], loss: 0.14382 acc: 0.98667 val_loss: 0.15013, val_acc: 0.96000
    Epoch [7880/10000], loss: 0.14373 acc: 0.98667 val_loss: 0.15006, val_acc: 0.96000
    Epoch [7890/10000], loss: 0.14364 acc: 0.98667 val_loss: 0.14999, val_acc: 0.96000
    Epoch [7900/10000], loss: 0.14356 acc: 0.98667 val_loss: 0.14991, val_acc: 0.96000
    Epoch [7910/10000], loss: 0.14347 acc: 0.98667 val_loss: 0.14984, val_acc: 0.96000
    Epoch [7920/10000], loss: 0.14338 acc: 0.98667 val_loss: 0.14976, val_acc: 0.96000
    Epoch [7930/10000], loss: 0.14330 acc: 0.98667 val_loss: 0.14969, val_acc: 0.96000
    Epoch [7940/10000], loss: 0.14321 acc: 0.98667 val_loss: 0.14962, val_acc: 0.96000
    Epoch [7950/10000], loss: 0.14312 acc: 0.98667 val_loss: 0.14955, val_acc: 0.96000
    Epoch [7960/10000], loss: 0.14304 acc: 0.98667 val_loss: 0.14947, val_acc: 0.96000
    Epoch [7970/10000], loss: 0.14295 acc: 0.98667 val_loss: 0.14940, val_acc: 0.96000
    Epoch [7980/10000], loss: 0.14287 acc: 0.98667 val_loss: 0.14933, val_acc: 0.96000
    Epoch [7990/10000], loss: 0.14278 acc: 0.98667 val_loss: 0.14926, val_acc: 0.96000
    Epoch [8000/10000], loss: 0.14269 acc: 0.98667 val_loss: 0.14918, val_acc: 0.96000
    Epoch [8010/10000], loss: 0.14261 acc: 0.98667 val_loss: 0.14911, val_acc: 0.96000
    Epoch [8020/10000], loss: 0.14252 acc: 0.98667 val_loss: 0.14904, val_acc: 0.96000
    Epoch [8030/10000], loss: 0.14244 acc: 0.98667 val_loss: 0.14897, val_acc: 0.96000
    Epoch [8040/10000], loss: 0.14235 acc: 0.98667 val_loss: 0.14890, val_acc: 0.96000
    Epoch [8050/10000], loss: 0.14227 acc: 0.98667 val_loss: 0.14883, val_acc: 0.96000
    Epoch [8060/10000], loss: 0.14219 acc: 0.98667 val_loss: 0.14876, val_acc: 0.96000
    Epoch [8070/10000], loss: 0.14210 acc: 0.98667 val_loss: 0.14868, val_acc: 0.96000
    Epoch [8080/10000], loss: 0.14202 acc: 0.98667 val_loss: 0.14861, val_acc: 0.96000
    Epoch [8090/10000], loss: 0.14193 acc: 0.98667 val_loss: 0.14854, val_acc: 0.96000
    Epoch [8100/10000], loss: 0.14185 acc: 0.98667 val_loss: 0.14847, val_acc: 0.96000
    Epoch [8110/10000], loss: 0.14177 acc: 0.98667 val_loss: 0.14840, val_acc: 0.96000
    Epoch [8120/10000], loss: 0.14168 acc: 0.98667 val_loss: 0.14833, val_acc: 0.96000
    Epoch [8130/10000], loss: 0.14160 acc: 0.98667 val_loss: 0.14826, val_acc: 0.96000
    Epoch [8140/10000], loss: 0.14152 acc: 0.98667 val_loss: 0.14819, val_acc: 0.96000
    Epoch [8150/10000], loss: 0.14144 acc: 0.98667 val_loss: 0.14812, val_acc: 0.96000
    Epoch [8160/10000], loss: 0.14135 acc: 0.98667 val_loss: 0.14805, val_acc: 0.96000
    Epoch [8170/10000], loss: 0.14127 acc: 0.98667 val_loss: 0.14798, val_acc: 0.96000
    Epoch [8180/10000], loss: 0.14119 acc: 0.98667 val_loss: 0.14791, val_acc: 0.96000
    Epoch [8190/10000], loss: 0.14111 acc: 0.98667 val_loss: 0.14785, val_acc: 0.96000
    Epoch [8200/10000], loss: 0.14102 acc: 0.98667 val_loss: 0.14778, val_acc: 0.96000
    Epoch [8210/10000], loss: 0.14094 acc: 0.98667 val_loss: 0.14771, val_acc: 0.96000
    Epoch [8220/10000], loss: 0.14086 acc: 0.98667 val_loss: 0.14764, val_acc: 0.96000
    Epoch [8230/10000], loss: 0.14078 acc: 0.98667 val_loss: 0.14757, val_acc: 0.96000
    Epoch [8240/10000], loss: 0.14070 acc: 0.98667 val_loss: 0.14750, val_acc: 0.96000
    Epoch [8250/10000], loss: 0.14062 acc: 0.98667 val_loss: 0.14743, val_acc: 0.96000
    Epoch [8260/10000], loss: 0.14054 acc: 0.98667 val_loss: 0.14737, val_acc: 0.96000
    Epoch [8270/10000], loss: 0.14046 acc: 0.98667 val_loss: 0.14730, val_acc: 0.96000
    Epoch [8280/10000], loss: 0.14037 acc: 0.98667 val_loss: 0.14723, val_acc: 0.96000
    Epoch [8290/10000], loss: 0.14029 acc: 0.98667 val_loss: 0.14716, val_acc: 0.96000
    Epoch [8300/10000], loss: 0.14021 acc: 0.98667 val_loss: 0.14710, val_acc: 0.96000
    Epoch [8310/10000], loss: 0.14013 acc: 0.98667 val_loss: 0.14703, val_acc: 0.96000
    Epoch [8320/10000], loss: 0.14005 acc: 0.98667 val_loss: 0.14696, val_acc: 0.96000
    Epoch [8330/10000], loss: 0.13997 acc: 0.98667 val_loss: 0.14689, val_acc: 0.96000
    Epoch [8340/10000], loss: 0.13989 acc: 0.98667 val_loss: 0.14683, val_acc: 0.96000
    Epoch [8350/10000], loss: 0.13981 acc: 0.98667 val_loss: 0.14676, val_acc: 0.96000
    Epoch [8360/10000], loss: 0.13974 acc: 0.98667 val_loss: 0.14669, val_acc: 0.96000
    Epoch [8370/10000], loss: 0.13966 acc: 0.98667 val_loss: 0.14663, val_acc: 0.96000
    Epoch [8380/10000], loss: 0.13958 acc: 0.98667 val_loss: 0.14656, val_acc: 0.96000
    Epoch [8390/10000], loss: 0.13950 acc: 0.98667 val_loss: 0.14649, val_acc: 0.96000
    Epoch [8400/10000], loss: 0.13942 acc: 0.98667 val_loss: 0.14643, val_acc: 0.96000
    Epoch [8410/10000], loss: 0.13934 acc: 0.98667 val_loss: 0.14636, val_acc: 0.96000
    Epoch [8420/10000], loss: 0.13926 acc: 0.98667 val_loss: 0.14630, val_acc: 0.96000
    Epoch [8430/10000], loss: 0.13918 acc: 0.98667 val_loss: 0.14623, val_acc: 0.96000
    Epoch [8440/10000], loss: 0.13911 acc: 0.98667 val_loss: 0.14617, val_acc: 0.96000
    Epoch [8450/10000], loss: 0.13903 acc: 0.98667 val_loss: 0.14610, val_acc: 0.96000
    Epoch [8460/10000], loss: 0.13895 acc: 0.98667 val_loss: 0.14603, val_acc: 0.96000
    Epoch [8470/10000], loss: 0.13887 acc: 0.98667 val_loss: 0.14597, val_acc: 0.96000
    Epoch [8480/10000], loss: 0.13880 acc: 0.98667 val_loss: 0.14590, val_acc: 0.96000
    Epoch [8490/10000], loss: 0.13872 acc: 0.98667 val_loss: 0.14584, val_acc: 0.96000
    Epoch [8500/10000], loss: 0.13864 acc: 0.98667 val_loss: 0.14578, val_acc: 0.96000
    Epoch [8510/10000], loss: 0.13856 acc: 0.98667 val_loss: 0.14571, val_acc: 0.96000
    Epoch [8520/10000], loss: 0.13849 acc: 0.98667 val_loss: 0.14565, val_acc: 0.96000
    Epoch [8530/10000], loss: 0.13841 acc: 0.98667 val_loss: 0.14558, val_acc: 0.96000
    Epoch [8540/10000], loss: 0.13833 acc: 0.98667 val_loss: 0.14552, val_acc: 0.96000
    Epoch [8550/10000], loss: 0.13826 acc: 0.98667 val_loss: 0.14545, val_acc: 0.96000
    Epoch [8560/10000], loss: 0.13818 acc: 0.98667 val_loss: 0.14539, val_acc: 0.96000
    Epoch [8570/10000], loss: 0.13811 acc: 0.98667 val_loss: 0.14533, val_acc: 0.96000
    Epoch [8580/10000], loss: 0.13803 acc: 0.98667 val_loss: 0.14526, val_acc: 0.96000
    Epoch [8590/10000], loss: 0.13795 acc: 0.98667 val_loss: 0.14520, val_acc: 0.96000
    Epoch [8600/10000], loss: 0.13788 acc: 0.98667 val_loss: 0.14514, val_acc: 0.96000
    Epoch [8610/10000], loss: 0.13780 acc: 0.98667 val_loss: 0.14507, val_acc: 0.96000
    Epoch [8620/10000], loss: 0.13773 acc: 0.98667 val_loss: 0.14501, val_acc: 0.96000
    Epoch [8630/10000], loss: 0.13765 acc: 0.98667 val_loss: 0.14495, val_acc: 0.96000
    Epoch [8640/10000], loss: 0.13758 acc: 0.98667 val_loss: 0.14488, val_acc: 0.96000
    Epoch [8650/10000], loss: 0.13750 acc: 0.98667 val_loss: 0.14482, val_acc: 0.96000
    Epoch [8660/10000], loss: 0.13743 acc: 0.98667 val_loss: 0.14476, val_acc: 0.96000
    Epoch [8670/10000], loss: 0.13735 acc: 0.98667 val_loss: 0.14470, val_acc: 0.96000
    Epoch [8680/10000], loss: 0.13728 acc: 0.98667 val_loss: 0.14463, val_acc: 0.96000
    Epoch [8690/10000], loss: 0.13720 acc: 0.98667 val_loss: 0.14457, val_acc: 0.96000
    Epoch [8700/10000], loss: 0.13713 acc: 0.98667 val_loss: 0.14451, val_acc: 0.96000
    Epoch [8710/10000], loss: 0.13705 acc: 0.98667 val_loss: 0.14445, val_acc: 0.96000
    Epoch [8720/10000], loss: 0.13698 acc: 0.98667 val_loss: 0.14438, val_acc: 0.96000
    Epoch [8730/10000], loss: 0.13691 acc: 0.98667 val_loss: 0.14432, val_acc: 0.96000
    Epoch [8740/10000], loss: 0.13683 acc: 0.98667 val_loss: 0.14426, val_acc: 0.96000
    Epoch [8750/10000], loss: 0.13676 acc: 0.98667 val_loss: 0.14420, val_acc: 0.96000
    Epoch [8760/10000], loss: 0.13669 acc: 0.98667 val_loss: 0.14414, val_acc: 0.96000
    Epoch [8770/10000], loss: 0.13661 acc: 0.98667 val_loss: 0.14408, val_acc: 0.96000
    Epoch [8780/10000], loss: 0.13654 acc: 0.98667 val_loss: 0.14402, val_acc: 0.96000
    Epoch [8790/10000], loss: 0.13647 acc: 0.98667 val_loss: 0.14396, val_acc: 0.96000
    Epoch [8800/10000], loss: 0.13639 acc: 0.98667 val_loss: 0.14389, val_acc: 0.96000
    Epoch [8810/10000], loss: 0.13632 acc: 0.98667 val_loss: 0.14383, val_acc: 0.96000
    Epoch [8820/10000], loss: 0.13625 acc: 0.98667 val_loss: 0.14377, val_acc: 0.96000
    Epoch [8830/10000], loss: 0.13618 acc: 0.98667 val_loss: 0.14371, val_acc: 0.96000
    Epoch [8840/10000], loss: 0.13610 acc: 0.98667 val_loss: 0.14365, val_acc: 0.96000
    Epoch [8850/10000], loss: 0.13603 acc: 0.98667 val_loss: 0.14359, val_acc: 0.96000
    Epoch [8860/10000], loss: 0.13596 acc: 0.98667 val_loss: 0.14353, val_acc: 0.96000
    Epoch [8870/10000], loss: 0.13589 acc: 0.98667 val_loss: 0.14347, val_acc: 0.96000
    Epoch [8880/10000], loss: 0.13582 acc: 0.98667 val_loss: 0.14341, val_acc: 0.96000
    Epoch [8890/10000], loss: 0.13574 acc: 0.98667 val_loss: 0.14335, val_acc: 0.96000
    Epoch [8900/10000], loss: 0.13567 acc: 0.98667 val_loss: 0.14329, val_acc: 0.96000
    Epoch [8910/10000], loss: 0.13560 acc: 0.98667 val_loss: 0.14323, val_acc: 0.96000
    Epoch [8920/10000], loss: 0.13553 acc: 0.98667 val_loss: 0.14317, val_acc: 0.96000
    Epoch [8930/10000], loss: 0.13546 acc: 0.98667 val_loss: 0.14311, val_acc: 0.96000
    Epoch [8940/10000], loss: 0.13539 acc: 0.98667 val_loss: 0.14306, val_acc: 0.96000
    Epoch [8950/10000], loss: 0.13532 acc: 0.98667 val_loss: 0.14300, val_acc: 0.96000
    Epoch [8960/10000], loss: 0.13525 acc: 0.98667 val_loss: 0.14294, val_acc: 0.96000
    Epoch [8970/10000], loss: 0.13518 acc: 0.98667 val_loss: 0.14288, val_acc: 0.96000
    Epoch [8980/10000], loss: 0.13511 acc: 0.98667 val_loss: 0.14282, val_acc: 0.96000
    Epoch [8990/10000], loss: 0.13504 acc: 0.98667 val_loss: 0.14276, val_acc: 0.96000
    Epoch [9000/10000], loss: 0.13497 acc: 0.98667 val_loss: 0.14270, val_acc: 0.96000
    Epoch [9010/10000], loss: 0.13490 acc: 0.98667 val_loss: 0.14264, val_acc: 0.96000
    Epoch [9020/10000], loss: 0.13483 acc: 0.98667 val_loss: 0.14259, val_acc: 0.96000
    Epoch [9030/10000], loss: 0.13476 acc: 0.98667 val_loss: 0.14253, val_acc: 0.96000
    Epoch [9040/10000], loss: 0.13469 acc: 0.98667 val_loss: 0.14247, val_acc: 0.96000
    Epoch [9050/10000], loss: 0.13462 acc: 0.98667 val_loss: 0.14241, val_acc: 0.96000
    Epoch [9060/10000], loss: 0.13455 acc: 0.98667 val_loss: 0.14236, val_acc: 0.96000
    Epoch [9070/10000], loss: 0.13448 acc: 0.98667 val_loss: 0.14230, val_acc: 0.96000
    Epoch [9080/10000], loss: 0.13441 acc: 0.98667 val_loss: 0.14224, val_acc: 0.96000
    Epoch [9090/10000], loss: 0.13434 acc: 0.98667 val_loss: 0.14218, val_acc: 0.96000
    Epoch [9100/10000], loss: 0.13427 acc: 0.98667 val_loss: 0.14213, val_acc: 0.96000
    Epoch [9110/10000], loss: 0.13420 acc: 0.98667 val_loss: 0.14207, val_acc: 0.96000
    Epoch [9120/10000], loss: 0.13413 acc: 0.98667 val_loss: 0.14201, val_acc: 0.96000
    Epoch [9130/10000], loss: 0.13407 acc: 0.98667 val_loss: 0.14195, val_acc: 0.96000
    Epoch [9140/10000], loss: 0.13400 acc: 0.98667 val_loss: 0.14190, val_acc: 0.96000
    Epoch [9150/10000], loss: 0.13393 acc: 0.98667 val_loss: 0.14184, val_acc: 0.96000
    Epoch [9160/10000], loss: 0.13386 acc: 0.98667 val_loss: 0.14178, val_acc: 0.96000
    Epoch [9170/10000], loss: 0.13379 acc: 0.98667 val_loss: 0.14173, val_acc: 0.96000
    Epoch [9180/10000], loss: 0.13373 acc: 0.98667 val_loss: 0.14167, val_acc: 0.96000
    Epoch [9190/10000], loss: 0.13366 acc: 0.98667 val_loss: 0.14161, val_acc: 0.96000
    Epoch [9200/10000], loss: 0.13359 acc: 0.98667 val_loss: 0.14156, val_acc: 0.96000
    Epoch [9210/10000], loss: 0.13352 acc: 0.98667 val_loss: 0.14150, val_acc: 0.96000
    Epoch [9220/10000], loss: 0.13345 acc: 0.98667 val_loss: 0.14145, val_acc: 0.96000
    Epoch [9230/10000], loss: 0.13339 acc: 0.98667 val_loss: 0.14139, val_acc: 0.96000
    Epoch [9240/10000], loss: 0.13332 acc: 0.98667 val_loss: 0.14133, val_acc: 0.96000
    Epoch [9250/10000], loss: 0.13325 acc: 0.98667 val_loss: 0.14128, val_acc: 0.96000
    Epoch [9260/10000], loss: 0.13319 acc: 0.98667 val_loss: 0.14122, val_acc: 0.96000
    Epoch [9270/10000], loss: 0.13312 acc: 0.98667 val_loss: 0.14117, val_acc: 0.96000
    Epoch [9280/10000], loss: 0.13305 acc: 0.98667 val_loss: 0.14111, val_acc: 0.96000
    Epoch [9290/10000], loss: 0.13299 acc: 0.98667 val_loss: 0.14106, val_acc: 0.96000
    Epoch [9300/10000], loss: 0.13292 acc: 0.98667 val_loss: 0.14100, val_acc: 0.96000
    Epoch [9310/10000], loss: 0.13285 acc: 0.98667 val_loss: 0.14095, val_acc: 0.96000
    Epoch [9320/10000], loss: 0.13279 acc: 0.98667 val_loss: 0.14089, val_acc: 0.96000
    Epoch [9330/10000], loss: 0.13272 acc: 0.98667 val_loss: 0.14084, val_acc: 0.96000
    Epoch [9340/10000], loss: 0.13266 acc: 0.98667 val_loss: 0.14078, val_acc: 0.96000
    Epoch [9350/10000], loss: 0.13259 acc: 0.98667 val_loss: 0.14073, val_acc: 0.96000
    Epoch [9360/10000], loss: 0.13252 acc: 0.98667 val_loss: 0.14067, val_acc: 0.96000
    Epoch [9370/10000], loss: 0.13246 acc: 0.98667 val_loss: 0.14062, val_acc: 0.96000
    Epoch [9380/10000], loss: 0.13239 acc: 0.98667 val_loss: 0.14056, val_acc: 0.96000
    Epoch [9390/10000], loss: 0.13233 acc: 0.98667 val_loss: 0.14051, val_acc: 0.96000
    Epoch [9400/10000], loss: 0.13226 acc: 0.98667 val_loss: 0.14046, val_acc: 0.96000
    Epoch [9410/10000], loss: 0.13220 acc: 0.98667 val_loss: 0.14040, val_acc: 0.96000
    Epoch [9420/10000], loss: 0.13213 acc: 0.98667 val_loss: 0.14035, val_acc: 0.96000
    Epoch [9430/10000], loss: 0.13207 acc: 0.98667 val_loss: 0.14029, val_acc: 0.96000
    Epoch [9440/10000], loss: 0.13200 acc: 0.98667 val_loss: 0.14024, val_acc: 0.96000
    Epoch [9450/10000], loss: 0.13194 acc: 0.98667 val_loss: 0.14019, val_acc: 0.96000
    Epoch [9460/10000], loss: 0.13187 acc: 0.98667 val_loss: 0.14013, val_acc: 0.96000
    Epoch [9470/10000], loss: 0.13181 acc: 0.98667 val_loss: 0.14008, val_acc: 0.96000
    Epoch [9480/10000], loss: 0.13174 acc: 0.98667 val_loss: 0.14003, val_acc: 0.96000
    Epoch [9490/10000], loss: 0.13168 acc: 0.98667 val_loss: 0.13997, val_acc: 0.96000
    Epoch [9500/10000], loss: 0.13162 acc: 0.98667 val_loss: 0.13992, val_acc: 0.96000
    Epoch [9510/10000], loss: 0.13155 acc: 0.98667 val_loss: 0.13987, val_acc: 0.96000
    Epoch [9520/10000], loss: 0.13149 acc: 0.98667 val_loss: 0.13982, val_acc: 0.96000
    Epoch [9530/10000], loss: 0.13142 acc: 0.98667 val_loss: 0.13976, val_acc: 0.96000
    Epoch [9540/10000], loss: 0.13136 acc: 0.98667 val_loss: 0.13971, val_acc: 0.96000
    Epoch [9550/10000], loss: 0.13130 acc: 0.98667 val_loss: 0.13966, val_acc: 0.96000
    Epoch [9560/10000], loss: 0.13123 acc: 0.98667 val_loss: 0.13960, val_acc: 0.96000
    Epoch [9570/10000], loss: 0.13117 acc: 0.98667 val_loss: 0.13955, val_acc: 0.96000
    Epoch [9580/10000], loss: 0.13111 acc: 0.98667 val_loss: 0.13950, val_acc: 0.96000
    Epoch [9590/10000], loss: 0.13104 acc: 0.98667 val_loss: 0.13945, val_acc: 0.96000
    Epoch [9600/10000], loss: 0.13098 acc: 0.98667 val_loss: 0.13940, val_acc: 0.96000
    Epoch [9610/10000], loss: 0.13092 acc: 0.98667 val_loss: 0.13934, val_acc: 0.96000
    Epoch [9620/10000], loss: 0.13086 acc: 0.98667 val_loss: 0.13929, val_acc: 0.96000
    Epoch [9630/10000], loss: 0.13079 acc: 0.98667 val_loss: 0.13924, val_acc: 0.96000
    Epoch [9640/10000], loss: 0.13073 acc: 0.98667 val_loss: 0.13919, val_acc: 0.96000
    Epoch [9650/10000], loss: 0.13067 acc: 0.98667 val_loss: 0.13914, val_acc: 0.96000
    Epoch [9660/10000], loss: 0.13061 acc: 0.98667 val_loss: 0.13909, val_acc: 0.96000
    Epoch [9670/10000], loss: 0.13054 acc: 0.98667 val_loss: 0.13903, val_acc: 0.96000
    Epoch [9680/10000], loss: 0.13048 acc: 0.98667 val_loss: 0.13898, val_acc: 0.96000
    Epoch [9690/10000], loss: 0.13042 acc: 0.98667 val_loss: 0.13893, val_acc: 0.96000
    Epoch [9700/10000], loss: 0.13036 acc: 0.98667 val_loss: 0.13888, val_acc: 0.96000
    Epoch [9710/10000], loss: 0.13030 acc: 0.98667 val_loss: 0.13883, val_acc: 0.96000
    Epoch [9720/10000], loss: 0.13023 acc: 0.98667 val_loss: 0.13878, val_acc: 0.96000
    Epoch [9730/10000], loss: 0.13017 acc: 0.98667 val_loss: 0.13873, val_acc: 0.96000
    Epoch [9740/10000], loss: 0.13011 acc: 0.98667 val_loss: 0.13868, val_acc: 0.96000
    Epoch [9750/10000], loss: 0.13005 acc: 0.98667 val_loss: 0.13863, val_acc: 0.96000
    Epoch [9760/10000], loss: 0.12999 acc: 0.98667 val_loss: 0.13858, val_acc: 0.96000
    Epoch [9770/10000], loss: 0.12993 acc: 0.98667 val_loss: 0.13853, val_acc: 0.96000
    Epoch [9780/10000], loss: 0.12987 acc: 0.98667 val_loss: 0.13847, val_acc: 0.96000
    Epoch [9790/10000], loss: 0.12981 acc: 0.98667 val_loss: 0.13842, val_acc: 0.96000
    Epoch [9800/10000], loss: 0.12974 acc: 0.98667 val_loss: 0.13837, val_acc: 0.96000
    Epoch [9810/10000], loss: 0.12968 acc: 0.98667 val_loss: 0.13832, val_acc: 0.96000
    Epoch [9820/10000], loss: 0.12962 acc: 0.98667 val_loss: 0.13827, val_acc: 0.96000
    Epoch [9830/10000], loss: 0.12956 acc: 0.98667 val_loss: 0.13822, val_acc: 0.96000
    Epoch [9840/10000], loss: 0.12950 acc: 0.98667 val_loss: 0.13817, val_acc: 0.96000
    Epoch [9850/10000], loss: 0.12944 acc: 0.98667 val_loss: 0.13812, val_acc: 0.96000
    Epoch [9860/10000], loss: 0.12938 acc: 0.98667 val_loss: 0.13808, val_acc: 0.96000
    Epoch [9870/10000], loss: 0.12932 acc: 0.98667 val_loss: 0.13803, val_acc: 0.96000
    Epoch [9880/10000], loss: 0.12926 acc: 0.98667 val_loss: 0.13798, val_acc: 0.96000
    Epoch [9890/10000], loss: 0.12920 acc: 0.98667 val_loss: 0.13793, val_acc: 0.96000
    Epoch [9900/10000], loss: 0.12914 acc: 0.98667 val_loss: 0.13788, val_acc: 0.96000
    Epoch [9910/10000], loss: 0.12908 acc: 0.98667 val_loss: 0.13783, val_acc: 0.96000
    Epoch [9920/10000], loss: 0.12902 acc: 0.98667 val_loss: 0.13778, val_acc: 0.96000
    Epoch [9930/10000], loss: 0.12896 acc: 0.98667 val_loss: 0.13773, val_acc: 0.96000
    Epoch [9940/10000], loss: 0.12890 acc: 0.98667 val_loss: 0.13768, val_acc: 0.96000
    Epoch [9950/10000], loss: 0.12884 acc: 0.98667 val_loss: 0.13763, val_acc: 0.96000
    Epoch [9960/10000], loss: 0.12879 acc: 0.98667 val_loss: 0.13758, val_acc: 0.96000
    Epoch [9970/10000], loss: 0.12873 acc: 0.98667 val_loss: 0.13754, val_acc: 0.96000
    Epoch [9980/10000], loss: 0.12867 acc: 0.98667 val_loss: 0.13749, val_acc: 0.96000
    Epoch [9990/10000], loss: 0.12861 acc: 0.98667 val_loss: 0.13744, val_acc: 0.96000



```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기상태 : 손실 : 3.70707  정확도 : 0.36000
    최종상태 : 손실 : 0.13744  정확도 : 0.96000



```python
# 패턴 2 모델의 출력 결과
w = outputs[:5,:].data
print(w.numpy())

# 확률값을 얻고 싶은 경우
print(torch.exp(w).numpy())
```

    [[ -5.0138  -0.1021  -2.403 ]
     [ -5.0423  -0.0205  -4.2822]
     [ -0.0609  -2.8283 -16.1468]
     [-11.6712  -3.1905  -0.042 ]
     [ -9.2089  -1.6898  -0.2041]]
    [[0.0066 0.9029 0.0905]
     [0.0065 0.9797 0.0138]
     [0.9409 0.0591 0.    ]
     [0.     0.0412 0.9588]
     [0.0001 0.1846 0.8153]]


### 모델 클래스측에 소프트맥스 함수 만 포함된 경우


```python
# 모델 정의
# 2입력 3출력 로지스틱 회귀 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output):
        super().__init__()
        self.l1 = nn.Linear(n_input, n_output)
        # 소프트맥스 함수 정의
        self.softmax = nn.Softmax(dim=1)

        # 초깃값을 모두 1로 함
        # "딥러닝을 위한 수학"과 조건을 맞추기 위한 목적
        self.l1.weight.data.fill_(1.0)
        self.l1.bias.data.fill_(1.0)

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.softmax(x1)
        return x2
```


```python
# 학습률
lr = 0.01

# 초기화
net = Net(n_input, n_output)

# 손실 함수： NLLLoss 함수
criterion = nn.NLLLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10000

# 평가 결과 기록
history = np.zeros((0,5))
```


```python
for epoch in range(num_epochs):

    # 훈련 페이즈

    # 경사 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 여기서 로그 함수를 적용함
    outputs2 = torch.log(outputs)

    # 손실 계산
    loss = criterion(outputs2, labels)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 예측 라벨 산출
    predicted = torch.max(outputs, 1)[1]

    # 손실과 정확도 계산
    train_loss = loss.item()
    train_acc = (predicted == labels).sum()  / len(labels)

    # 예측 페이즈

    # 예측 계산
    outputs_test = net(inputs_test)

    # 여기서 로그 함수를 적용함
    outputs2_test = torch.log(outputs_test)

    # 손실 계산
    loss_test = criterion(outputs2_test, labels_test)

    # 예측 라벨 산출
    predicted_test = torch.max(outputs_test, 1)[1]

    # 손실과 정확도 계산
    val_loss =  loss_test.item()
    val_acc =  (predicted_test == labels_test).sum() / len(labels_test)

    if ( epoch % 10 == 0):
        print (f'Epoch [{epoch}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
        item = np.array([epoch , train_loss, train_acc, val_loss, val_acc])
        history = np.vstack((history, item))
```

    Epoch [0/10000], loss: 1.09861 acc: 0.30667 val_loss: 1.09158, val_acc: 0.26667
    Epoch [10/10000], loss: 1.01848 acc: 0.40000 val_loss: 1.04171, val_acc: 0.26667
    Epoch [20/10000], loss: 0.96854 acc: 0.40000 val_loss: 0.98850, val_acc: 0.26667
    Epoch [30/10000], loss: 0.92459 acc: 0.65333 val_loss: 0.93996, val_acc: 0.57333
    Epoch [40/10000], loss: 0.88568 acc: 0.70667 val_loss: 0.89704, val_acc: 0.62667
    Epoch [50/10000], loss: 0.85120 acc: 0.70667 val_loss: 0.85918, val_acc: 0.62667
    Epoch [60/10000], loss: 0.82059 acc: 0.70667 val_loss: 0.82572, val_acc: 0.62667
    Epoch [70/10000], loss: 0.79335 acc: 0.72000 val_loss: 0.79607, val_acc: 0.62667
    Epoch [80/10000], loss: 0.76900 acc: 0.72000 val_loss: 0.76968, val_acc: 0.65333
    Epoch [90/10000], loss: 0.74717 acc: 0.72000 val_loss: 0.74610, val_acc: 0.65333
    Epoch [100/10000], loss: 0.72750 acc: 0.76000 val_loss: 0.72494, val_acc: 0.69333
    Epoch [110/10000], loss: 0.70970 acc: 0.77333 val_loss: 0.70585, val_acc: 0.74667
    Epoch [120/10000], loss: 0.69354 acc: 0.81333 val_loss: 0.68856, val_acc: 0.76000
    Epoch [130/10000], loss: 0.67878 acc: 0.84000 val_loss: 0.67283, val_acc: 0.76000
    Epoch [140/10000], loss: 0.66526 acc: 0.84000 val_loss: 0.65846, val_acc: 0.78667
    Epoch [150/10000], loss: 0.65283 acc: 0.86667 val_loss: 0.64528, val_acc: 0.78667
    Epoch [160/10000], loss: 0.64135 acc: 0.88000 val_loss: 0.63313, val_acc: 0.78667
    Epoch [170/10000], loss: 0.63070 acc: 0.89333 val_loss: 0.62190, val_acc: 0.81333
    Epoch [180/10000], loss: 0.62080 acc: 0.90667 val_loss: 0.61149, val_acc: 0.81333
    Epoch [190/10000], loss: 0.61157 acc: 0.90667 val_loss: 0.60179, val_acc: 0.84000
    Epoch [200/10000], loss: 0.60292 acc: 0.90667 val_loss: 0.59273, val_acc: 0.84000
    Epoch [210/10000], loss: 0.59481 acc: 0.90667 val_loss: 0.58425, val_acc: 0.88000
    Epoch [220/10000], loss: 0.58717 acc: 0.93333 val_loss: 0.57628, val_acc: 0.88000
    Epoch [230/10000], loss: 0.57996 acc: 0.93333 val_loss: 0.56877, val_acc: 0.89333
    Epoch [240/10000], loss: 0.57313 acc: 0.93333 val_loss: 0.56169, val_acc: 0.90667
    Epoch [250/10000], loss: 0.56666 acc: 0.93333 val_loss: 0.55498, val_acc: 0.90667
    Epoch [260/10000], loss: 0.56051 acc: 0.92000 val_loss: 0.54862, val_acc: 0.90667
    Epoch [270/10000], loss: 0.55465 acc: 0.92000 val_loss: 0.54257, val_acc: 0.90667
    Epoch [280/10000], loss: 0.54906 acc: 0.92000 val_loss: 0.53681, val_acc: 0.90667
    Epoch [290/10000], loss: 0.54371 acc: 0.92000 val_loss: 0.53131, val_acc: 0.90667
    Epoch [300/10000], loss: 0.53859 acc: 0.93333 val_loss: 0.52605, val_acc: 0.90667
    Epoch [310/10000], loss: 0.53368 acc: 0.93333 val_loss: 0.52102, val_acc: 0.90667
    Epoch [320/10000], loss: 0.52896 acc: 0.93333 val_loss: 0.51619, val_acc: 0.90667
    Epoch [330/10000], loss: 0.52442 acc: 0.93333 val_loss: 0.51155, val_acc: 0.90667
    Epoch [340/10000], loss: 0.52004 acc: 0.93333 val_loss: 0.50709, val_acc: 0.90667
    Epoch [350/10000], loss: 0.51582 acc: 0.93333 val_loss: 0.50280, val_acc: 0.90667
    Epoch [360/10000], loss: 0.51173 acc: 0.93333 val_loss: 0.49865, val_acc: 0.90667
    Epoch [370/10000], loss: 0.50779 acc: 0.93333 val_loss: 0.49465, val_acc: 0.90667
    Epoch [380/10000], loss: 0.50397 acc: 0.93333 val_loss: 0.49078, val_acc: 0.90667
    Epoch [390/10000], loss: 0.50026 acc: 0.93333 val_loss: 0.48703, val_acc: 0.90667
    Epoch [400/10000], loss: 0.49666 acc: 0.94667 val_loss: 0.48340, val_acc: 0.90667
    Epoch [410/10000], loss: 0.49317 acc: 0.94667 val_loss: 0.47988, val_acc: 0.90667
    Epoch [420/10000], loss: 0.48978 acc: 0.94667 val_loss: 0.47647, val_acc: 0.90667
    Epoch [430/10000], loss: 0.48647 acc: 0.96000 val_loss: 0.47315, val_acc: 0.90667
    Epoch [440/10000], loss: 0.48326 acc: 0.96000 val_loss: 0.46992, val_acc: 0.90667
    Epoch [450/10000], loss: 0.48012 acc: 0.96000 val_loss: 0.46678, val_acc: 0.90667
    Epoch [460/10000], loss: 0.47706 acc: 0.96000 val_loss: 0.46372, val_acc: 0.90667
    Epoch [470/10000], loss: 0.47408 acc: 0.96000 val_loss: 0.46073, val_acc: 0.90667
    Epoch [480/10000], loss: 0.47116 acc: 0.96000 val_loss: 0.45783, val_acc: 0.90667
    Epoch [490/10000], loss: 0.46831 acc: 0.96000 val_loss: 0.45499, val_acc: 0.90667
    Epoch [500/10000], loss: 0.46553 acc: 0.96000 val_loss: 0.45221, val_acc: 0.90667
    Epoch [510/10000], loss: 0.46280 acc: 0.96000 val_loss: 0.44951, val_acc: 0.90667
    Epoch [520/10000], loss: 0.46013 acc: 0.96000 val_loss: 0.44686, val_acc: 0.90667
    Epoch [530/10000], loss: 0.45752 acc: 0.96000 val_loss: 0.44426, val_acc: 0.90667
    Epoch [540/10000], loss: 0.45496 acc: 0.96000 val_loss: 0.44173, val_acc: 0.90667
    Epoch [550/10000], loss: 0.45245 acc: 0.96000 val_loss: 0.43924, val_acc: 0.90667
    Epoch [560/10000], loss: 0.44998 acc: 0.96000 val_loss: 0.43681, val_acc: 0.90667
    Epoch [570/10000], loss: 0.44757 acc: 0.96000 val_loss: 0.43442, val_acc: 0.90667
    Epoch [580/10000], loss: 0.44519 acc: 0.96000 val_loss: 0.43208, val_acc: 0.90667
    Epoch [590/10000], loss: 0.44286 acc: 0.96000 val_loss: 0.42979, val_acc: 0.92000
    Epoch [600/10000], loss: 0.44057 acc: 0.96000 val_loss: 0.42753, val_acc: 0.92000
    Epoch [610/10000], loss: 0.43832 acc: 0.96000 val_loss: 0.42532, val_acc: 0.92000
    Epoch [620/10000], loss: 0.43611 acc: 0.96000 val_loss: 0.42315, val_acc: 0.92000
    Epoch [630/10000], loss: 0.43393 acc: 0.96000 val_loss: 0.42101, val_acc: 0.92000
    Epoch [640/10000], loss: 0.43179 acc: 0.96000 val_loss: 0.41891, val_acc: 0.92000
    Epoch [650/10000], loss: 0.42968 acc: 0.96000 val_loss: 0.41685, val_acc: 0.92000
    Epoch [660/10000], loss: 0.42761 acc: 0.96000 val_loss: 0.41482, val_acc: 0.92000
    Epoch [670/10000], loss: 0.42556 acc: 0.96000 val_loss: 0.41282, val_acc: 0.92000
    Epoch [680/10000], loss: 0.42355 acc: 0.96000 val_loss: 0.41085, val_acc: 0.92000
    Epoch [690/10000], loss: 0.42157 acc: 0.96000 val_loss: 0.40892, val_acc: 0.92000
    Epoch [700/10000], loss: 0.41961 acc: 0.96000 val_loss: 0.40701, val_acc: 0.92000
    Epoch [710/10000], loss: 0.41768 acc: 0.96000 val_loss: 0.40513, val_acc: 0.92000
    Epoch [720/10000], loss: 0.41578 acc: 0.96000 val_loss: 0.40329, val_acc: 0.92000
    Epoch [730/10000], loss: 0.41391 acc: 0.96000 val_loss: 0.40146, val_acc: 0.92000
    Epoch [740/10000], loss: 0.41206 acc: 0.96000 val_loss: 0.39967, val_acc: 0.92000
    Epoch [750/10000], loss: 0.41024 acc: 0.96000 val_loss: 0.39789, val_acc: 0.92000
    Epoch [760/10000], loss: 0.40844 acc: 0.96000 val_loss: 0.39615, val_acc: 0.92000
    Epoch [770/10000], loss: 0.40666 acc: 0.96000 val_loss: 0.39443, val_acc: 0.93333
    Epoch [780/10000], loss: 0.40491 acc: 0.96000 val_loss: 0.39273, val_acc: 0.93333
    Epoch [790/10000], loss: 0.40317 acc: 0.96000 val_loss: 0.39105, val_acc: 0.93333
    Epoch [800/10000], loss: 0.40146 acc: 0.96000 val_loss: 0.38939, val_acc: 0.93333
    Epoch [810/10000], loss: 0.39977 acc: 0.96000 val_loss: 0.38776, val_acc: 0.93333
    Epoch [820/10000], loss: 0.39810 acc: 0.96000 val_loss: 0.38615, val_acc: 0.93333
    Epoch [830/10000], loss: 0.39646 acc: 0.96000 val_loss: 0.38456, val_acc: 0.93333
    Epoch [840/10000], loss: 0.39483 acc: 0.96000 val_loss: 0.38298, val_acc: 0.93333
    Epoch [850/10000], loss: 0.39321 acc: 0.97333 val_loss: 0.38143, val_acc: 0.94667
    Epoch [860/10000], loss: 0.39162 acc: 0.97333 val_loss: 0.37990, val_acc: 0.94667
    Epoch [870/10000], loss: 0.39005 acc: 0.97333 val_loss: 0.37838, val_acc: 0.94667
    Epoch [880/10000], loss: 0.38849 acc: 0.97333 val_loss: 0.37688, val_acc: 0.94667
    Epoch [890/10000], loss: 0.38695 acc: 0.97333 val_loss: 0.37540, val_acc: 0.94667
    Epoch [900/10000], loss: 0.38543 acc: 0.97333 val_loss: 0.37394, val_acc: 0.94667
    Epoch [910/10000], loss: 0.38392 acc: 0.97333 val_loss: 0.37249, val_acc: 0.94667
    Epoch [920/10000], loss: 0.38243 acc: 0.97333 val_loss: 0.37106, val_acc: 0.94667
    Epoch [930/10000], loss: 0.38096 acc: 0.97333 val_loss: 0.36965, val_acc: 0.94667
    Epoch [940/10000], loss: 0.37950 acc: 0.97333 val_loss: 0.36825, val_acc: 0.94667
    Epoch [950/10000], loss: 0.37806 acc: 0.97333 val_loss: 0.36686, val_acc: 0.94667
    Epoch [960/10000], loss: 0.37663 acc: 0.97333 val_loss: 0.36550, val_acc: 0.96000
    Epoch [970/10000], loss: 0.37522 acc: 0.97333 val_loss: 0.36414, val_acc: 0.96000
    Epoch [980/10000], loss: 0.37382 acc: 0.97333 val_loss: 0.36280, val_acc: 0.96000
    Epoch [990/10000], loss: 0.37243 acc: 0.97333 val_loss: 0.36148, val_acc: 0.96000
    Epoch [1000/10000], loss: 0.37106 acc: 0.97333 val_loss: 0.36017, val_acc: 0.96000
    Epoch [1010/10000], loss: 0.36970 acc: 0.97333 val_loss: 0.35887, val_acc: 0.96000
    Epoch [1020/10000], loss: 0.36836 acc: 0.97333 val_loss: 0.35758, val_acc: 0.96000
    Epoch [1030/10000], loss: 0.36703 acc: 0.97333 val_loss: 0.35631, val_acc: 0.96000
    Epoch [1040/10000], loss: 0.36571 acc: 0.97333 val_loss: 0.35505, val_acc: 0.96000
    Epoch [1050/10000], loss: 0.36440 acc: 0.97333 val_loss: 0.35381, val_acc: 0.96000
    Epoch [1060/10000], loss: 0.36311 acc: 0.97333 val_loss: 0.35258, val_acc: 0.96000
    Epoch [1070/10000], loss: 0.36183 acc: 0.97333 val_loss: 0.35135, val_acc: 0.96000
    Epoch [1080/10000], loss: 0.36056 acc: 0.97333 val_loss: 0.35014, val_acc: 0.96000
    Epoch [1090/10000], loss: 0.35930 acc: 0.97333 val_loss: 0.34895, val_acc: 0.96000
    Epoch [1100/10000], loss: 0.35805 acc: 0.97333 val_loss: 0.34776, val_acc: 0.96000
    Epoch [1110/10000], loss: 0.35682 acc: 0.97333 val_loss: 0.34659, val_acc: 0.96000
    Epoch [1120/10000], loss: 0.35559 acc: 0.97333 val_loss: 0.34542, val_acc: 0.96000
    Epoch [1130/10000], loss: 0.35438 acc: 0.97333 val_loss: 0.34427, val_acc: 0.96000
    Epoch [1140/10000], loss: 0.35318 acc: 0.97333 val_loss: 0.34313, val_acc: 0.96000
    Epoch [1150/10000], loss: 0.35199 acc: 0.97333 val_loss: 0.34199, val_acc: 0.96000
    Epoch [1160/10000], loss: 0.35081 acc: 0.97333 val_loss: 0.34087, val_acc: 0.96000
    Epoch [1170/10000], loss: 0.34964 acc: 0.97333 val_loss: 0.33976, val_acc: 0.96000
    Epoch [1180/10000], loss: 0.34848 acc: 0.97333 val_loss: 0.33866, val_acc: 0.96000
    Epoch [1190/10000], loss: 0.34732 acc: 0.97333 val_loss: 0.33757, val_acc: 0.96000
    Epoch [1200/10000], loss: 0.34618 acc: 0.97333 val_loss: 0.33649, val_acc: 0.96000
    Epoch [1210/10000], loss: 0.34505 acc: 0.97333 val_loss: 0.33542, val_acc: 0.96000
    Epoch [1220/10000], loss: 0.34393 acc: 0.97333 val_loss: 0.33435, val_acc: 0.96000
    Epoch [1230/10000], loss: 0.34282 acc: 0.97333 val_loss: 0.33330, val_acc: 0.96000
    Epoch [1240/10000], loss: 0.34172 acc: 0.97333 val_loss: 0.33226, val_acc: 0.96000
    Epoch [1250/10000], loss: 0.34062 acc: 0.97333 val_loss: 0.33122, val_acc: 0.96000
    Epoch [1260/10000], loss: 0.33954 acc: 0.97333 val_loss: 0.33020, val_acc: 0.96000
    Epoch [1270/10000], loss: 0.33846 acc: 0.97333 val_loss: 0.32918, val_acc: 0.96000
    Epoch [1280/10000], loss: 0.33740 acc: 0.97333 val_loss: 0.32817, val_acc: 0.96000
    Epoch [1290/10000], loss: 0.33634 acc: 0.97333 val_loss: 0.32717, val_acc: 0.96000
    Epoch [1300/10000], loss: 0.33529 acc: 0.97333 val_loss: 0.32618, val_acc: 0.96000
    Epoch [1310/10000], loss: 0.33425 acc: 0.97333 val_loss: 0.32520, val_acc: 0.96000
    Epoch [1320/10000], loss: 0.33321 acc: 0.97333 val_loss: 0.32422, val_acc: 0.96000
    Epoch [1330/10000], loss: 0.33219 acc: 0.97333 val_loss: 0.32325, val_acc: 0.96000
    Epoch [1340/10000], loss: 0.33117 acc: 0.97333 val_loss: 0.32229, val_acc: 0.96000
    Epoch [1350/10000], loss: 0.33016 acc: 0.97333 val_loss: 0.32134, val_acc: 0.96000
    Epoch [1360/10000], loss: 0.32916 acc: 0.97333 val_loss: 0.32040, val_acc: 0.96000
    Epoch [1370/10000], loss: 0.32817 acc: 0.97333 val_loss: 0.31946, val_acc: 0.96000
    Epoch [1380/10000], loss: 0.32719 acc: 0.97333 val_loss: 0.31853, val_acc: 0.96000
    Epoch [1390/10000], loss: 0.32621 acc: 0.97333 val_loss: 0.31761, val_acc: 0.96000
    Epoch [1400/10000], loss: 0.32524 acc: 0.97333 val_loss: 0.31670, val_acc: 0.96000
    Epoch [1410/10000], loss: 0.32428 acc: 0.97333 val_loss: 0.31579, val_acc: 0.96000
    Epoch [1420/10000], loss: 0.32332 acc: 0.97333 val_loss: 0.31489, val_acc: 0.96000
    Epoch [1430/10000], loss: 0.32237 acc: 0.97333 val_loss: 0.31400, val_acc: 0.96000
    Epoch [1440/10000], loss: 0.32143 acc: 0.97333 val_loss: 0.31312, val_acc: 0.96000
    Epoch [1450/10000], loss: 0.32050 acc: 0.97333 val_loss: 0.31224, val_acc: 0.96000
    Epoch [1460/10000], loss: 0.31957 acc: 0.97333 val_loss: 0.31137, val_acc: 0.96000
    Epoch [1470/10000], loss: 0.31865 acc: 0.97333 val_loss: 0.31050, val_acc: 0.96000
    Epoch [1480/10000], loss: 0.31774 acc: 0.97333 val_loss: 0.30964, val_acc: 0.96000
    Epoch [1490/10000], loss: 0.31683 acc: 0.97333 val_loss: 0.30879, val_acc: 0.96000
    Epoch [1500/10000], loss: 0.31593 acc: 0.97333 val_loss: 0.30795, val_acc: 0.96000
    Epoch [1510/10000], loss: 0.31504 acc: 0.97333 val_loss: 0.30711, val_acc: 0.96000
    Epoch [1520/10000], loss: 0.31415 acc: 0.97333 val_loss: 0.30628, val_acc: 0.96000
    Epoch [1530/10000], loss: 0.31327 acc: 0.97333 val_loss: 0.30545, val_acc: 0.96000
    Epoch [1540/10000], loss: 0.31240 acc: 0.97333 val_loss: 0.30463, val_acc: 0.96000
    Epoch [1550/10000], loss: 0.31153 acc: 0.97333 val_loss: 0.30382, val_acc: 0.96000
    Epoch [1560/10000], loss: 0.31067 acc: 0.97333 val_loss: 0.30301, val_acc: 0.96000
    Epoch [1570/10000], loss: 0.30981 acc: 0.97333 val_loss: 0.30221, val_acc: 0.96000
    Epoch [1580/10000], loss: 0.30896 acc: 0.97333 val_loss: 0.30141, val_acc: 0.96000
    Epoch [1590/10000], loss: 0.30812 acc: 0.97333 val_loss: 0.30062, val_acc: 0.96000
    Epoch [1600/10000], loss: 0.30728 acc: 0.97333 val_loss: 0.29984, val_acc: 0.96000
    Epoch [1610/10000], loss: 0.30645 acc: 0.97333 val_loss: 0.29906, val_acc: 0.96000
    Epoch [1620/10000], loss: 0.30562 acc: 0.97333 val_loss: 0.29828, val_acc: 0.96000
    Epoch [1630/10000], loss: 0.30480 acc: 0.97333 val_loss: 0.29752, val_acc: 0.96000
    Epoch [1640/10000], loss: 0.30399 acc: 0.97333 val_loss: 0.29675, val_acc: 0.96000
    Epoch [1650/10000], loss: 0.30318 acc: 0.97333 val_loss: 0.29600, val_acc: 0.96000
    Epoch [1660/10000], loss: 0.30237 acc: 0.97333 val_loss: 0.29525, val_acc: 0.96000
    Epoch [1670/10000], loss: 0.30158 acc: 0.97333 val_loss: 0.29450, val_acc: 0.96000
    Epoch [1680/10000], loss: 0.30078 acc: 0.97333 val_loss: 0.29376, val_acc: 0.96000
    Epoch [1690/10000], loss: 0.30000 acc: 0.97333 val_loss: 0.29302, val_acc: 0.96000
    Epoch [1700/10000], loss: 0.29922 acc: 0.97333 val_loss: 0.29229, val_acc: 0.96000
    Epoch [1710/10000], loss: 0.29844 acc: 0.97333 val_loss: 0.29157, val_acc: 0.96000
    Epoch [1720/10000], loss: 0.29767 acc: 0.97333 val_loss: 0.29085, val_acc: 0.96000
    Epoch [1730/10000], loss: 0.29690 acc: 0.97333 val_loss: 0.29013, val_acc: 0.96000
    Epoch [1740/10000], loss: 0.29614 acc: 0.97333 val_loss: 0.28942, val_acc: 0.96000
    Epoch [1750/10000], loss: 0.29538 acc: 0.97333 val_loss: 0.28872, val_acc: 0.96000
    Epoch [1760/10000], loss: 0.29463 acc: 0.97333 val_loss: 0.28801, val_acc: 0.96000
    Epoch [1770/10000], loss: 0.29389 acc: 0.97333 val_loss: 0.28732, val_acc: 0.96000
    Epoch [1780/10000], loss: 0.29315 acc: 0.97333 val_loss: 0.28663, val_acc: 0.96000
    Epoch [1790/10000], loss: 0.29241 acc: 0.97333 val_loss: 0.28594, val_acc: 0.96000
    Epoch [1800/10000], loss: 0.29168 acc: 0.97333 val_loss: 0.28526, val_acc: 0.96000
    Epoch [1810/10000], loss: 0.29095 acc: 0.97333 val_loss: 0.28458, val_acc: 0.96000
    Epoch [1820/10000], loss: 0.29023 acc: 0.97333 val_loss: 0.28391, val_acc: 0.96000
    Epoch [1830/10000], loss: 0.28951 acc: 0.97333 val_loss: 0.28324, val_acc: 0.96000
    Epoch [1840/10000], loss: 0.28880 acc: 0.97333 val_loss: 0.28258, val_acc: 0.96000
    Epoch [1850/10000], loss: 0.28809 acc: 0.97333 val_loss: 0.28192, val_acc: 0.96000
    Epoch [1860/10000], loss: 0.28739 acc: 0.97333 val_loss: 0.28126, val_acc: 0.96000
    Epoch [1870/10000], loss: 0.28669 acc: 0.97333 val_loss: 0.28061, val_acc: 0.96000
    Epoch [1880/10000], loss: 0.28599 acc: 0.97333 val_loss: 0.27996, val_acc: 0.96000
    Epoch [1890/10000], loss: 0.28530 acc: 0.97333 val_loss: 0.27932, val_acc: 0.96000
    Epoch [1900/10000], loss: 0.28462 acc: 0.97333 val_loss: 0.27868, val_acc: 0.96000
    Epoch [1910/10000], loss: 0.28394 acc: 0.97333 val_loss: 0.27805, val_acc: 0.96000
    Epoch [1920/10000], loss: 0.28326 acc: 0.97333 val_loss: 0.27742, val_acc: 0.96000
    Epoch [1930/10000], loss: 0.28258 acc: 0.97333 val_loss: 0.27679, val_acc: 0.96000
    Epoch [1940/10000], loss: 0.28192 acc: 0.97333 val_loss: 0.27617, val_acc: 0.96000
    Epoch [1950/10000], loss: 0.28125 acc: 0.97333 val_loss: 0.27555, val_acc: 0.96000
    Epoch [1960/10000], loss: 0.28059 acc: 0.97333 val_loss: 0.27494, val_acc: 0.96000
    Epoch [1970/10000], loss: 0.27993 acc: 0.97333 val_loss: 0.27433, val_acc: 0.96000
    Epoch [1980/10000], loss: 0.27928 acc: 0.97333 val_loss: 0.27372, val_acc: 0.96000
    Epoch [1990/10000], loss: 0.27863 acc: 0.97333 val_loss: 0.27312, val_acc: 0.96000
    Epoch [2000/10000], loss: 0.27799 acc: 0.97333 val_loss: 0.27252, val_acc: 0.96000
    Epoch [2010/10000], loss: 0.27735 acc: 0.97333 val_loss: 0.27193, val_acc: 0.96000
    Epoch [2020/10000], loss: 0.27671 acc: 0.97333 val_loss: 0.27134, val_acc: 0.96000
    Epoch [2030/10000], loss: 0.27608 acc: 0.97333 val_loss: 0.27075, val_acc: 0.96000
    Epoch [2040/10000], loss: 0.27545 acc: 0.97333 val_loss: 0.27016, val_acc: 0.96000
    Epoch [2050/10000], loss: 0.27482 acc: 0.97333 val_loss: 0.26958, val_acc: 0.96000
    Epoch [2060/10000], loss: 0.27420 acc: 0.97333 val_loss: 0.26901, val_acc: 0.96000
    Epoch [2070/10000], loss: 0.27358 acc: 0.97333 val_loss: 0.26843, val_acc: 0.96000
    Epoch [2080/10000], loss: 0.27297 acc: 0.97333 val_loss: 0.26786, val_acc: 0.96000
    Epoch [2090/10000], loss: 0.27236 acc: 0.97333 val_loss: 0.26730, val_acc: 0.96000
    Epoch [2100/10000], loss: 0.27175 acc: 0.97333 val_loss: 0.26674, val_acc: 0.96000
    Epoch [2110/10000], loss: 0.27115 acc: 0.97333 val_loss: 0.26618, val_acc: 0.96000
    Epoch [2120/10000], loss: 0.27055 acc: 0.97333 val_loss: 0.26562, val_acc: 0.96000
    Epoch [2130/10000], loss: 0.26995 acc: 0.97333 val_loss: 0.26507, val_acc: 0.96000
    Epoch [2140/10000], loss: 0.26936 acc: 0.97333 val_loss: 0.26452, val_acc: 0.96000
    Epoch [2150/10000], loss: 0.26877 acc: 0.97333 val_loss: 0.26397, val_acc: 0.96000
    Epoch [2160/10000], loss: 0.26818 acc: 0.97333 val_loss: 0.26343, val_acc: 0.96000
    Epoch [2170/10000], loss: 0.26760 acc: 0.97333 val_loss: 0.26289, val_acc: 0.96000
    Epoch [2180/10000], loss: 0.26702 acc: 0.97333 val_loss: 0.26236, val_acc: 0.96000
    Epoch [2190/10000], loss: 0.26644 acc: 0.97333 val_loss: 0.26182, val_acc: 0.96000
    Epoch [2200/10000], loss: 0.26587 acc: 0.97333 val_loss: 0.26129, val_acc: 0.96000
    Epoch [2210/10000], loss: 0.26530 acc: 0.97333 val_loss: 0.26077, val_acc: 0.96000
    Epoch [2220/10000], loss: 0.26473 acc: 0.97333 val_loss: 0.26024, val_acc: 0.96000
    Epoch [2230/10000], loss: 0.26417 acc: 0.97333 val_loss: 0.25972, val_acc: 0.96000
    Epoch [2240/10000], loss: 0.26361 acc: 0.97333 val_loss: 0.25921, val_acc: 0.96000
    Epoch [2250/10000], loss: 0.26305 acc: 0.97333 val_loss: 0.25869, val_acc: 0.96000
    Epoch [2260/10000], loss: 0.26250 acc: 0.97333 val_loss: 0.25818, val_acc: 0.96000
    Epoch [2270/10000], loss: 0.26195 acc: 0.97333 val_loss: 0.25767, val_acc: 0.96000
    Epoch [2280/10000], loss: 0.26140 acc: 0.97333 val_loss: 0.25717, val_acc: 0.96000
    Epoch [2290/10000], loss: 0.26086 acc: 0.97333 val_loss: 0.25666, val_acc: 0.96000
    Epoch [2300/10000], loss: 0.26032 acc: 0.97333 val_loss: 0.25616, val_acc: 0.96000
    Epoch [2310/10000], loss: 0.25978 acc: 0.97333 val_loss: 0.25567, val_acc: 0.96000
    Epoch [2320/10000], loss: 0.25924 acc: 0.97333 val_loss: 0.25517, val_acc: 0.96000
    Epoch [2330/10000], loss: 0.25871 acc: 0.97333 val_loss: 0.25468, val_acc: 0.96000
    Epoch [2340/10000], loss: 0.25818 acc: 0.97333 val_loss: 0.25419, val_acc: 0.96000
    Epoch [2350/10000], loss: 0.25766 acc: 0.97333 val_loss: 0.25371, val_acc: 0.96000
    Epoch [2360/10000], loss: 0.25713 acc: 0.97333 val_loss: 0.25322, val_acc: 0.96000
    Epoch [2370/10000], loss: 0.25661 acc: 0.97333 val_loss: 0.25274, val_acc: 0.96000
    Epoch [2380/10000], loss: 0.25609 acc: 0.97333 val_loss: 0.25227, val_acc: 0.96000
    Epoch [2390/10000], loss: 0.25558 acc: 0.97333 val_loss: 0.25179, val_acc: 0.96000
    Epoch [2400/10000], loss: 0.25507 acc: 0.97333 val_loss: 0.25132, val_acc: 0.96000
    Epoch [2410/10000], loss: 0.25456 acc: 0.97333 val_loss: 0.25085, val_acc: 0.96000
    Epoch [2420/10000], loss: 0.25405 acc: 0.97333 val_loss: 0.25038, val_acc: 0.96000
    Epoch [2430/10000], loss: 0.25355 acc: 0.97333 val_loss: 0.24992, val_acc: 0.96000
    Epoch [2440/10000], loss: 0.25304 acc: 0.97333 val_loss: 0.24946, val_acc: 0.96000
    Epoch [2450/10000], loss: 0.25255 acc: 0.97333 val_loss: 0.24900, val_acc: 0.96000
    Epoch [2460/10000], loss: 0.25205 acc: 0.97333 val_loss: 0.24854, val_acc: 0.96000
    Epoch [2470/10000], loss: 0.25156 acc: 0.97333 val_loss: 0.24809, val_acc: 0.96000
    Epoch [2480/10000], loss: 0.25107 acc: 0.97333 val_loss: 0.24764, val_acc: 0.96000
    Epoch [2490/10000], loss: 0.25058 acc: 0.97333 val_loss: 0.24719, val_acc: 0.96000
    Epoch [2500/10000], loss: 0.25009 acc: 0.97333 val_loss: 0.24674, val_acc: 0.96000
    Epoch [2510/10000], loss: 0.24961 acc: 0.97333 val_loss: 0.24630, val_acc: 0.96000
    Epoch [2520/10000], loss: 0.24913 acc: 0.97333 val_loss: 0.24585, val_acc: 0.96000
    Epoch [2530/10000], loss: 0.24865 acc: 0.97333 val_loss: 0.24541, val_acc: 0.96000
    Epoch [2540/10000], loss: 0.24818 acc: 0.97333 val_loss: 0.24498, val_acc: 0.96000
    Epoch [2550/10000], loss: 0.24770 acc: 0.97333 val_loss: 0.24454, val_acc: 0.96000
    Epoch [2560/10000], loss: 0.24723 acc: 0.97333 val_loss: 0.24411, val_acc: 0.96000
    Epoch [2570/10000], loss: 0.24676 acc: 0.97333 val_loss: 0.24368, val_acc: 0.96000
    Epoch [2580/10000], loss: 0.24630 acc: 0.98667 val_loss: 0.24325, val_acc: 0.96000
    Epoch [2590/10000], loss: 0.24584 acc: 0.98667 val_loss: 0.24283, val_acc: 0.96000
    Epoch [2600/10000], loss: 0.24537 acc: 0.98667 val_loss: 0.24240, val_acc: 0.96000
    Epoch [2610/10000], loss: 0.24492 acc: 0.98667 val_loss: 0.24198, val_acc: 0.96000
    Epoch [2620/10000], loss: 0.24446 acc: 0.98667 val_loss: 0.24156, val_acc: 0.96000
    Epoch [2630/10000], loss: 0.24401 acc: 0.98667 val_loss: 0.24115, val_acc: 0.96000
    Epoch [2640/10000], loss: 0.24355 acc: 0.98667 val_loss: 0.24073, val_acc: 0.96000
    Epoch [2650/10000], loss: 0.24311 acc: 0.98667 val_loss: 0.24032, val_acc: 0.96000
    Epoch [2660/10000], loss: 0.24266 acc: 0.98667 val_loss: 0.23991, val_acc: 0.96000
    Epoch [2670/10000], loss: 0.24221 acc: 0.98667 val_loss: 0.23950, val_acc: 0.96000
    Epoch [2680/10000], loss: 0.24177 acc: 0.98667 val_loss: 0.23909, val_acc: 0.96000
    Epoch [2690/10000], loss: 0.24133 acc: 0.98667 val_loss: 0.23869, val_acc: 0.96000
    Epoch [2700/10000], loss: 0.24089 acc: 0.98667 val_loss: 0.23829, val_acc: 0.96000
    Epoch [2710/10000], loss: 0.24046 acc: 0.98667 val_loss: 0.23789, val_acc: 0.96000
    Epoch [2720/10000], loss: 0.24002 acc: 0.98667 val_loss: 0.23749, val_acc: 0.96000
    Epoch [2730/10000], loss: 0.23959 acc: 0.98667 val_loss: 0.23710, val_acc: 0.96000
    Epoch [2740/10000], loss: 0.23916 acc: 0.98667 val_loss: 0.23670, val_acc: 0.96000
    Epoch [2750/10000], loss: 0.23874 acc: 0.98667 val_loss: 0.23631, val_acc: 0.96000
    Epoch [2760/10000], loss: 0.23831 acc: 0.98667 val_loss: 0.23592, val_acc: 0.96000
    Epoch [2770/10000], loss: 0.23789 acc: 0.98667 val_loss: 0.23553, val_acc: 0.96000
    Epoch [2780/10000], loss: 0.23747 acc: 0.98667 val_loss: 0.23515, val_acc: 0.96000
    Epoch [2790/10000], loss: 0.23705 acc: 0.98667 val_loss: 0.23476, val_acc: 0.96000
    Epoch [2800/10000], loss: 0.23663 acc: 0.98667 val_loss: 0.23438, val_acc: 0.96000
    Epoch [2810/10000], loss: 0.23622 acc: 0.98667 val_loss: 0.23400, val_acc: 0.96000
    Epoch [2820/10000], loss: 0.23580 acc: 0.98667 val_loss: 0.23363, val_acc: 0.96000
    Epoch [2830/10000], loss: 0.23539 acc: 0.98667 val_loss: 0.23325, val_acc: 0.96000
    Epoch [2840/10000], loss: 0.23498 acc: 0.98667 val_loss: 0.23287, val_acc: 0.96000
    Epoch [2850/10000], loss: 0.23458 acc: 0.98667 val_loss: 0.23250, val_acc: 0.96000
    Epoch [2860/10000], loss: 0.23417 acc: 0.98667 val_loss: 0.23213, val_acc: 0.96000
    Epoch [2870/10000], loss: 0.23377 acc: 0.98667 val_loss: 0.23176, val_acc: 0.96000
    Epoch [2880/10000], loss: 0.23337 acc: 0.98667 val_loss: 0.23140, val_acc: 0.96000
    Epoch [2890/10000], loss: 0.23297 acc: 0.98667 val_loss: 0.23103, val_acc: 0.96000
    Epoch [2900/10000], loss: 0.23257 acc: 0.98667 val_loss: 0.23067, val_acc: 0.96000
    Epoch [2910/10000], loss: 0.23218 acc: 0.98667 val_loss: 0.23031, val_acc: 0.96000
    Epoch [2920/10000], loss: 0.23178 acc: 0.98667 val_loss: 0.22995, val_acc: 0.96000
    Epoch [2930/10000], loss: 0.23139 acc: 0.98667 val_loss: 0.22959, val_acc: 0.96000
    Epoch [2940/10000], loss: 0.23100 acc: 0.98667 val_loss: 0.22923, val_acc: 0.96000
    Epoch [2950/10000], loss: 0.23061 acc: 0.98667 val_loss: 0.22888, val_acc: 0.96000
    Epoch [2960/10000], loss: 0.23023 acc: 0.98667 val_loss: 0.22853, val_acc: 0.96000
    Epoch [2970/10000], loss: 0.22984 acc: 0.98667 val_loss: 0.22818, val_acc: 0.96000
    Epoch [2980/10000], loss: 0.22946 acc: 0.98667 val_loss: 0.22783, val_acc: 0.96000
    Epoch [2990/10000], loss: 0.22908 acc: 0.98667 val_loss: 0.22748, val_acc: 0.96000
    Epoch [3000/10000], loss: 0.22870 acc: 0.98667 val_loss: 0.22713, val_acc: 0.96000
    Epoch [3010/10000], loss: 0.22832 acc: 0.98667 val_loss: 0.22679, val_acc: 0.96000
    Epoch [3020/10000], loss: 0.22795 acc: 0.98667 val_loss: 0.22645, val_acc: 0.96000
    Epoch [3030/10000], loss: 0.22757 acc: 0.98667 val_loss: 0.22610, val_acc: 0.96000
    Epoch [3040/10000], loss: 0.22720 acc: 0.98667 val_loss: 0.22577, val_acc: 0.96000
    Epoch [3050/10000], loss: 0.22683 acc: 0.98667 val_loss: 0.22543, val_acc: 0.96000
    Epoch [3060/10000], loss: 0.22646 acc: 0.98667 val_loss: 0.22509, val_acc: 0.96000
    Epoch [3070/10000], loss: 0.22610 acc: 0.98667 val_loss: 0.22476, val_acc: 0.96000
    Epoch [3080/10000], loss: 0.22573 acc: 0.98667 val_loss: 0.22442, val_acc: 0.96000
    Epoch [3090/10000], loss: 0.22537 acc: 0.98667 val_loss: 0.22409, val_acc: 0.96000
    Epoch [3100/10000], loss: 0.22501 acc: 0.98667 val_loss: 0.22376, val_acc: 0.96000
    Epoch [3110/10000], loss: 0.22465 acc: 0.98667 val_loss: 0.22343, val_acc: 0.96000
    Epoch [3120/10000], loss: 0.22429 acc: 0.98667 val_loss: 0.22311, val_acc: 0.96000
    Epoch [3130/10000], loss: 0.22393 acc: 0.98667 val_loss: 0.22278, val_acc: 0.96000
    Epoch [3140/10000], loss: 0.22357 acc: 0.98667 val_loss: 0.22246, val_acc: 0.96000
    Epoch [3150/10000], loss: 0.22322 acc: 0.98667 val_loss: 0.22214, val_acc: 0.96000
    Epoch [3160/10000], loss: 0.22287 acc: 0.98667 val_loss: 0.22181, val_acc: 0.96000
    Epoch [3170/10000], loss: 0.22252 acc: 0.98667 val_loss: 0.22150, val_acc: 0.96000
    Epoch [3180/10000], loss: 0.22217 acc: 0.98667 val_loss: 0.22118, val_acc: 0.96000
    Epoch [3190/10000], loss: 0.22182 acc: 0.98667 val_loss: 0.22086, val_acc: 0.96000
    Epoch [3200/10000], loss: 0.22148 acc: 0.98667 val_loss: 0.22055, val_acc: 0.96000
    Epoch [3210/10000], loss: 0.22113 acc: 0.98667 val_loss: 0.22023, val_acc: 0.96000
    Epoch [3220/10000], loss: 0.22079 acc: 0.98667 val_loss: 0.21992, val_acc: 0.96000
    Epoch [3230/10000], loss: 0.22045 acc: 0.98667 val_loss: 0.21961, val_acc: 0.96000
    Epoch [3240/10000], loss: 0.22011 acc: 0.98667 val_loss: 0.21930, val_acc: 0.96000
    Epoch [3250/10000], loss: 0.21977 acc: 0.98667 val_loss: 0.21899, val_acc: 0.96000
    Epoch [3260/10000], loss: 0.21943 acc: 0.98667 val_loss: 0.21869, val_acc: 0.96000
    Epoch [3270/10000], loss: 0.21910 acc: 0.98667 val_loss: 0.21838, val_acc: 0.96000
    Epoch [3280/10000], loss: 0.21876 acc: 0.98667 val_loss: 0.21808, val_acc: 0.96000
    Epoch [3290/10000], loss: 0.21843 acc: 0.98667 val_loss: 0.21778, val_acc: 0.96000
    Epoch [3300/10000], loss: 0.21810 acc: 0.98667 val_loss: 0.21747, val_acc: 0.96000
    Epoch [3310/10000], loss: 0.21777 acc: 0.98667 val_loss: 0.21717, val_acc: 0.96000
    Epoch [3320/10000], loss: 0.21744 acc: 0.98667 val_loss: 0.21688, val_acc: 0.96000
    Epoch [3330/10000], loss: 0.21711 acc: 0.98667 val_loss: 0.21658, val_acc: 0.96000
    Epoch [3340/10000], loss: 0.21679 acc: 0.98667 val_loss: 0.21628, val_acc: 0.96000
    Epoch [3350/10000], loss: 0.21646 acc: 0.98667 val_loss: 0.21599, val_acc: 0.96000
    Epoch [3360/10000], loss: 0.21614 acc: 0.98667 val_loss: 0.21570, val_acc: 0.96000
    Epoch [3370/10000], loss: 0.21582 acc: 0.98667 val_loss: 0.21540, val_acc: 0.96000
    Epoch [3380/10000], loss: 0.21550 acc: 0.98667 val_loss: 0.21511, val_acc: 0.96000
    Epoch [3390/10000], loss: 0.21518 acc: 0.98667 val_loss: 0.21483, val_acc: 0.96000
    Epoch [3400/10000], loss: 0.21487 acc: 0.98667 val_loss: 0.21454, val_acc: 0.96000
    Epoch [3410/10000], loss: 0.21455 acc: 0.98667 val_loss: 0.21425, val_acc: 0.96000
    Epoch [3420/10000], loss: 0.21424 acc: 0.98667 val_loss: 0.21396, val_acc: 0.96000
    Epoch [3430/10000], loss: 0.21392 acc: 0.98667 val_loss: 0.21368, val_acc: 0.96000
    Epoch [3440/10000], loss: 0.21361 acc: 0.98667 val_loss: 0.21340, val_acc: 0.96000
    Epoch [3450/10000], loss: 0.21330 acc: 0.98667 val_loss: 0.21312, val_acc: 0.96000
    Epoch [3460/10000], loss: 0.21299 acc: 0.98667 val_loss: 0.21284, val_acc: 0.96000
    Epoch [3470/10000], loss: 0.21268 acc: 0.98667 val_loss: 0.21256, val_acc: 0.96000
    Epoch [3480/10000], loss: 0.21238 acc: 0.98667 val_loss: 0.21228, val_acc: 0.96000
    Epoch [3490/10000], loss: 0.21207 acc: 0.98667 val_loss: 0.21200, val_acc: 0.96000
    Epoch [3500/10000], loss: 0.21177 acc: 0.98667 val_loss: 0.21173, val_acc: 0.96000
    Epoch [3510/10000], loss: 0.21146 acc: 0.98667 val_loss: 0.21145, val_acc: 0.96000
    Epoch [3520/10000], loss: 0.21116 acc: 0.98667 val_loss: 0.21118, val_acc: 0.96000
    Epoch [3530/10000], loss: 0.21086 acc: 0.98667 val_loss: 0.21091, val_acc: 0.96000
    Epoch [3540/10000], loss: 0.21056 acc: 0.98667 val_loss: 0.21064, val_acc: 0.96000
    Epoch [3550/10000], loss: 0.21026 acc: 0.98667 val_loss: 0.21037, val_acc: 0.96000
    Epoch [3560/10000], loss: 0.20997 acc: 0.98667 val_loss: 0.21010, val_acc: 0.96000
    Epoch [3570/10000], loss: 0.20967 acc: 0.98667 val_loss: 0.20983, val_acc: 0.96000
    Epoch [3580/10000], loss: 0.20938 acc: 0.98667 val_loss: 0.20956, val_acc: 0.96000
    Epoch [3590/10000], loss: 0.20909 acc: 0.98667 val_loss: 0.20930, val_acc: 0.96000
    Epoch [3600/10000], loss: 0.20879 acc: 0.98667 val_loss: 0.20903, val_acc: 0.96000
    Epoch [3610/10000], loss: 0.20850 acc: 0.98667 val_loss: 0.20877, val_acc: 0.96000
    Epoch [3620/10000], loss: 0.20821 acc: 0.98667 val_loss: 0.20851, val_acc: 0.96000
    Epoch [3630/10000], loss: 0.20793 acc: 0.98667 val_loss: 0.20825, val_acc: 0.96000
    Epoch [3640/10000], loss: 0.20764 acc: 0.98667 val_loss: 0.20799, val_acc: 0.96000
    Epoch [3650/10000], loss: 0.20735 acc: 0.98667 val_loss: 0.20773, val_acc: 0.96000
    Epoch [3660/10000], loss: 0.20707 acc: 0.98667 val_loss: 0.20747, val_acc: 0.96000
    Epoch [3670/10000], loss: 0.20678 acc: 0.98667 val_loss: 0.20721, val_acc: 0.96000
    Epoch [3680/10000], loss: 0.20650 acc: 0.98667 val_loss: 0.20696, val_acc: 0.96000
    Epoch [3690/10000], loss: 0.20622 acc: 0.98667 val_loss: 0.20670, val_acc: 0.96000
    Epoch [3700/10000], loss: 0.20594 acc: 0.98667 val_loss: 0.20645, val_acc: 0.96000
    Epoch [3710/10000], loss: 0.20566 acc: 0.98667 val_loss: 0.20620, val_acc: 0.96000
    Epoch [3720/10000], loss: 0.20538 acc: 0.98667 val_loss: 0.20595, val_acc: 0.96000
    Epoch [3730/10000], loss: 0.20511 acc: 0.98667 val_loss: 0.20570, val_acc: 0.96000
    Epoch [3740/10000], loss: 0.20483 acc: 0.98667 val_loss: 0.20545, val_acc: 0.96000
    Epoch [3750/10000], loss: 0.20455 acc: 0.98667 val_loss: 0.20520, val_acc: 0.96000
    Epoch [3760/10000], loss: 0.20428 acc: 0.98667 val_loss: 0.20495, val_acc: 0.96000
    Epoch [3770/10000], loss: 0.20401 acc: 0.98667 val_loss: 0.20471, val_acc: 0.96000
    Epoch [3780/10000], loss: 0.20374 acc: 0.98667 val_loss: 0.20446, val_acc: 0.96000
    Epoch [3790/10000], loss: 0.20347 acc: 0.98667 val_loss: 0.20422, val_acc: 0.96000
    Epoch [3800/10000], loss: 0.20320 acc: 0.98667 val_loss: 0.20397, val_acc: 0.96000
    Epoch [3810/10000], loss: 0.20293 acc: 0.98667 val_loss: 0.20373, val_acc: 0.96000
    Epoch [3820/10000], loss: 0.20266 acc: 0.98667 val_loss: 0.20349, val_acc: 0.96000
    Epoch [3830/10000], loss: 0.20239 acc: 0.98667 val_loss: 0.20325, val_acc: 0.96000
    Epoch [3840/10000], loss: 0.20213 acc: 0.98667 val_loss: 0.20301, val_acc: 0.96000
    Epoch [3850/10000], loss: 0.20186 acc: 0.98667 val_loss: 0.20277, val_acc: 0.96000
    Epoch [3860/10000], loss: 0.20160 acc: 0.98667 val_loss: 0.20253, val_acc: 0.96000
    Epoch [3870/10000], loss: 0.20134 acc: 0.98667 val_loss: 0.20230, val_acc: 0.96000
    Epoch [3880/10000], loss: 0.20108 acc: 0.98667 val_loss: 0.20206, val_acc: 0.96000
    Epoch [3890/10000], loss: 0.20082 acc: 0.98667 val_loss: 0.20183, val_acc: 0.96000
    Epoch [3900/10000], loss: 0.20056 acc: 0.98667 val_loss: 0.20159, val_acc: 0.96000
    Epoch [3910/10000], loss: 0.20030 acc: 0.98667 val_loss: 0.20136, val_acc: 0.96000
    Epoch [3920/10000], loss: 0.20004 acc: 0.98667 val_loss: 0.20113, val_acc: 0.96000
    Epoch [3930/10000], loss: 0.19979 acc: 0.98667 val_loss: 0.20090, val_acc: 0.96000
    Epoch [3940/10000], loss: 0.19953 acc: 0.98667 val_loss: 0.20067, val_acc: 0.96000
    Epoch [3950/10000], loss: 0.19928 acc: 0.98667 val_loss: 0.20044, val_acc: 0.96000
    Epoch [3960/10000], loss: 0.19902 acc: 0.98667 val_loss: 0.20021, val_acc: 0.96000
    Epoch [3970/10000], loss: 0.19877 acc: 0.98667 val_loss: 0.19998, val_acc: 0.96000
    Epoch [3980/10000], loss: 0.19852 acc: 0.98667 val_loss: 0.19976, val_acc: 0.96000
    Epoch [3990/10000], loss: 0.19827 acc: 0.98667 val_loss: 0.19953, val_acc: 0.96000
    Epoch [4000/10000], loss: 0.19802 acc: 0.98667 val_loss: 0.19931, val_acc: 0.96000
    Epoch [4010/10000], loss: 0.19777 acc: 0.98667 val_loss: 0.19908, val_acc: 0.96000
    Epoch [4020/10000], loss: 0.19752 acc: 0.98667 val_loss: 0.19886, val_acc: 0.96000
    Epoch [4030/10000], loss: 0.19728 acc: 0.98667 val_loss: 0.19864, val_acc: 0.96000
    Epoch [4040/10000], loss: 0.19703 acc: 0.98667 val_loss: 0.19842, val_acc: 0.96000
    Epoch [4050/10000], loss: 0.19679 acc: 0.98667 val_loss: 0.19820, val_acc: 0.96000
    Epoch [4060/10000], loss: 0.19654 acc: 0.98667 val_loss: 0.19798, val_acc: 0.96000
    Epoch [4070/10000], loss: 0.19630 acc: 0.98667 val_loss: 0.19776, val_acc: 0.96000
    Epoch [4080/10000], loss: 0.19606 acc: 0.98667 val_loss: 0.19754, val_acc: 0.96000
    Epoch [4090/10000], loss: 0.19582 acc: 0.98667 val_loss: 0.19732, val_acc: 0.96000
    Epoch [4100/10000], loss: 0.19557 acc: 0.98667 val_loss: 0.19711, val_acc: 0.96000
    Epoch [4110/10000], loss: 0.19534 acc: 0.98667 val_loss: 0.19689, val_acc: 0.96000
    Epoch [4120/10000], loss: 0.19510 acc: 0.98667 val_loss: 0.19668, val_acc: 0.96000
    Epoch [4130/10000], loss: 0.19486 acc: 0.98667 val_loss: 0.19646, val_acc: 0.96000
    Epoch [4140/10000], loss: 0.19462 acc: 0.98667 val_loss: 0.19625, val_acc: 0.96000
    Epoch [4150/10000], loss: 0.19439 acc: 0.98667 val_loss: 0.19604, val_acc: 0.96000
    Epoch [4160/10000], loss: 0.19415 acc: 0.98667 val_loss: 0.19583, val_acc: 0.96000
    Epoch [4170/10000], loss: 0.19392 acc: 0.98667 val_loss: 0.19562, val_acc: 0.96000
    Epoch [4180/10000], loss: 0.19368 acc: 0.98667 val_loss: 0.19541, val_acc: 0.96000
    Epoch [4190/10000], loss: 0.19345 acc: 0.98667 val_loss: 0.19520, val_acc: 0.96000
    Epoch [4200/10000], loss: 0.19322 acc: 0.98667 val_loss: 0.19499, val_acc: 0.96000
    Epoch [4210/10000], loss: 0.19299 acc: 0.98667 val_loss: 0.19478, val_acc: 0.96000
    Epoch [4220/10000], loss: 0.19276 acc: 0.98667 val_loss: 0.19457, val_acc: 0.96000
    Epoch [4230/10000], loss: 0.19253 acc: 0.98667 val_loss: 0.19437, val_acc: 0.96000
    Epoch [4240/10000], loss: 0.19230 acc: 0.98667 val_loss: 0.19416, val_acc: 0.96000
    Epoch [4250/10000], loss: 0.19207 acc: 0.98667 val_loss: 0.19396, val_acc: 0.96000
    Epoch [4260/10000], loss: 0.19184 acc: 0.98667 val_loss: 0.19376, val_acc: 0.96000
    Epoch [4270/10000], loss: 0.19162 acc: 0.98667 val_loss: 0.19355, val_acc: 0.96000
    Epoch [4280/10000], loss: 0.19139 acc: 0.98667 val_loss: 0.19335, val_acc: 0.96000
    Epoch [4290/10000], loss: 0.19117 acc: 0.98667 val_loss: 0.19315, val_acc: 0.96000
    Epoch [4300/10000], loss: 0.19094 acc: 0.98667 val_loss: 0.19295, val_acc: 0.96000
    Epoch [4310/10000], loss: 0.19072 acc: 0.98667 val_loss: 0.19275, val_acc: 0.96000
    Epoch [4320/10000], loss: 0.19050 acc: 0.98667 val_loss: 0.19255, val_acc: 0.96000
    Epoch [4330/10000], loss: 0.19028 acc: 0.98667 val_loss: 0.19235, val_acc: 0.96000
    Epoch [4340/10000], loss: 0.19006 acc: 0.98667 val_loss: 0.19215, val_acc: 0.96000
    Epoch [4350/10000], loss: 0.18984 acc: 0.98667 val_loss: 0.19196, val_acc: 0.96000
    Epoch [4360/10000], loss: 0.18962 acc: 0.98667 val_loss: 0.19176, val_acc: 0.96000
    Epoch [4370/10000], loss: 0.18940 acc: 0.98667 val_loss: 0.19156, val_acc: 0.96000
    Epoch [4380/10000], loss: 0.18918 acc: 0.98667 val_loss: 0.19137, val_acc: 0.96000
    Epoch [4390/10000], loss: 0.18897 acc: 0.98667 val_loss: 0.19118, val_acc: 0.96000
    Epoch [4400/10000], loss: 0.18875 acc: 0.98667 val_loss: 0.19098, val_acc: 0.96000
    Epoch [4410/10000], loss: 0.18853 acc: 0.98667 val_loss: 0.19079, val_acc: 0.96000
    Epoch [4420/10000], loss: 0.18832 acc: 0.98667 val_loss: 0.19060, val_acc: 0.96000
    Epoch [4430/10000], loss: 0.18811 acc: 0.98667 val_loss: 0.19041, val_acc: 0.96000
    Epoch [4440/10000], loss: 0.18789 acc: 0.98667 val_loss: 0.19021, val_acc: 0.96000
    Epoch [4450/10000], loss: 0.18768 acc: 0.98667 val_loss: 0.19002, val_acc: 0.96000
    Epoch [4460/10000], loss: 0.18747 acc: 0.98667 val_loss: 0.18984, val_acc: 0.96000
    Epoch [4470/10000], loss: 0.18726 acc: 0.98667 val_loss: 0.18965, val_acc: 0.96000
    Epoch [4480/10000], loss: 0.18705 acc: 0.98667 val_loss: 0.18946, val_acc: 0.96000
    Epoch [4490/10000], loss: 0.18684 acc: 0.98667 val_loss: 0.18927, val_acc: 0.96000
    Epoch [4500/10000], loss: 0.18663 acc: 0.98667 val_loss: 0.18908, val_acc: 0.96000
    Epoch [4510/10000], loss: 0.18642 acc: 0.98667 val_loss: 0.18890, val_acc: 0.96000
    Epoch [4520/10000], loss: 0.18622 acc: 0.98667 val_loss: 0.18871, val_acc: 0.96000
    Epoch [4530/10000], loss: 0.18601 acc: 0.98667 val_loss: 0.18853, val_acc: 0.96000
    Epoch [4540/10000], loss: 0.18580 acc: 0.98667 val_loss: 0.18834, val_acc: 0.96000
    Epoch [4550/10000], loss: 0.18560 acc: 0.98667 val_loss: 0.18816, val_acc: 0.96000
    Epoch [4560/10000], loss: 0.18539 acc: 0.98667 val_loss: 0.18798, val_acc: 0.96000
    Epoch [4570/10000], loss: 0.18519 acc: 0.98667 val_loss: 0.18780, val_acc: 0.96000
    Epoch [4580/10000], loss: 0.18499 acc: 0.98667 val_loss: 0.18762, val_acc: 0.96000
    Epoch [4590/10000], loss: 0.18478 acc: 0.98667 val_loss: 0.18743, val_acc: 0.96000
    Epoch [4600/10000], loss: 0.18458 acc: 0.98667 val_loss: 0.18725, val_acc: 0.96000
    Epoch [4610/10000], loss: 0.18438 acc: 0.98667 val_loss: 0.18707, val_acc: 0.96000
    Epoch [4620/10000], loss: 0.18418 acc: 0.98667 val_loss: 0.18690, val_acc: 0.96000
    Epoch [4630/10000], loss: 0.18398 acc: 0.98667 val_loss: 0.18672, val_acc: 0.96000
    Epoch [4640/10000], loss: 0.18378 acc: 0.98667 val_loss: 0.18654, val_acc: 0.96000
    Epoch [4650/10000], loss: 0.18358 acc: 0.98667 val_loss: 0.18636, val_acc: 0.96000
    Epoch [4660/10000], loss: 0.18339 acc: 0.98667 val_loss: 0.18619, val_acc: 0.96000
    Epoch [4670/10000], loss: 0.18319 acc: 0.98667 val_loss: 0.18601, val_acc: 0.96000
    Epoch [4680/10000], loss: 0.18299 acc: 0.98667 val_loss: 0.18583, val_acc: 0.96000
    Epoch [4690/10000], loss: 0.18280 acc: 0.98667 val_loss: 0.18566, val_acc: 0.96000
    Epoch [4700/10000], loss: 0.18260 acc: 0.98667 val_loss: 0.18549, val_acc: 0.96000
    Epoch [4710/10000], loss: 0.18241 acc: 0.98667 val_loss: 0.18531, val_acc: 0.96000
    Epoch [4720/10000], loss: 0.18221 acc: 0.98667 val_loss: 0.18514, val_acc: 0.96000
    Epoch [4730/10000], loss: 0.18202 acc: 0.98667 val_loss: 0.18497, val_acc: 0.96000
    Epoch [4740/10000], loss: 0.18183 acc: 0.98667 val_loss: 0.18479, val_acc: 0.96000
    Epoch [4750/10000], loss: 0.18164 acc: 0.98667 val_loss: 0.18462, val_acc: 0.96000
    Epoch [4760/10000], loss: 0.18144 acc: 0.98667 val_loss: 0.18445, val_acc: 0.96000
    Epoch [4770/10000], loss: 0.18125 acc: 0.98667 val_loss: 0.18428, val_acc: 0.96000
    Epoch [4780/10000], loss: 0.18106 acc: 0.98667 val_loss: 0.18411, val_acc: 0.96000
    Epoch [4790/10000], loss: 0.18087 acc: 0.98667 val_loss: 0.18395, val_acc: 0.96000
    Epoch [4800/10000], loss: 0.18068 acc: 0.98667 val_loss: 0.18378, val_acc: 0.96000
    Epoch [4810/10000], loss: 0.18050 acc: 0.98667 val_loss: 0.18361, val_acc: 0.96000
    Epoch [4820/10000], loss: 0.18031 acc: 0.98667 val_loss: 0.18344, val_acc: 0.96000
    Epoch [4830/10000], loss: 0.18012 acc: 0.98667 val_loss: 0.18328, val_acc: 0.96000
    Epoch [4840/10000], loss: 0.17994 acc: 0.98667 val_loss: 0.18311, val_acc: 0.96000
    Epoch [4850/10000], loss: 0.17975 acc: 0.98667 val_loss: 0.18294, val_acc: 0.96000
    Epoch [4860/10000], loss: 0.17956 acc: 0.98667 val_loss: 0.18278, val_acc: 0.96000
    Epoch [4870/10000], loss: 0.17938 acc: 0.98667 val_loss: 0.18261, val_acc: 0.96000
    Epoch [4880/10000], loss: 0.17920 acc: 0.98667 val_loss: 0.18245, val_acc: 0.96000
    Epoch [4890/10000], loss: 0.17901 acc: 0.98667 val_loss: 0.18229, val_acc: 0.96000
    Epoch [4900/10000], loss: 0.17883 acc: 0.98667 val_loss: 0.18212, val_acc: 0.96000
    Epoch [4910/10000], loss: 0.17865 acc: 0.98667 val_loss: 0.18196, val_acc: 0.96000
    Epoch [4920/10000], loss: 0.17846 acc: 0.98667 val_loss: 0.18180, val_acc: 0.96000
    Epoch [4930/10000], loss: 0.17828 acc: 0.98667 val_loss: 0.18164, val_acc: 0.96000
    Epoch [4940/10000], loss: 0.17810 acc: 0.98667 val_loss: 0.18148, val_acc: 0.96000
    Epoch [4950/10000], loss: 0.17792 acc: 0.98667 val_loss: 0.18132, val_acc: 0.96000
    Epoch [4960/10000], loss: 0.17774 acc: 0.98667 val_loss: 0.18116, val_acc: 0.96000
    Epoch [4970/10000], loss: 0.17756 acc: 0.98667 val_loss: 0.18100, val_acc: 0.96000
    Epoch [4980/10000], loss: 0.17739 acc: 0.98667 val_loss: 0.18084, val_acc: 0.96000
    Epoch [4990/10000], loss: 0.17721 acc: 0.98667 val_loss: 0.18068, val_acc: 0.96000
    Epoch [5000/10000], loss: 0.17703 acc: 0.98667 val_loss: 0.18053, val_acc: 0.96000
    Epoch [5010/10000], loss: 0.17685 acc: 0.98667 val_loss: 0.18037, val_acc: 0.96000
    Epoch [5020/10000], loss: 0.17668 acc: 0.98667 val_loss: 0.18021, val_acc: 0.96000
    Epoch [5030/10000], loss: 0.17650 acc: 0.98667 val_loss: 0.18006, val_acc: 0.96000
    Epoch [5040/10000], loss: 0.17633 acc: 0.98667 val_loss: 0.17990, val_acc: 0.96000
    Epoch [5050/10000], loss: 0.17615 acc: 0.98667 val_loss: 0.17975, val_acc: 0.96000
    Epoch [5060/10000], loss: 0.17598 acc: 0.98667 val_loss: 0.17959, val_acc: 0.96000
    Epoch [5070/10000], loss: 0.17581 acc: 0.98667 val_loss: 0.17944, val_acc: 0.96000
    Epoch [5080/10000], loss: 0.17563 acc: 0.98667 val_loss: 0.17928, val_acc: 0.96000
    Epoch [5090/10000], loss: 0.17546 acc: 0.98667 val_loss: 0.17913, val_acc: 0.96000
    Epoch [5100/10000], loss: 0.17529 acc: 0.98667 val_loss: 0.17898, val_acc: 0.96000
    Epoch [5110/10000], loss: 0.17512 acc: 0.98667 val_loss: 0.17883, val_acc: 0.96000
    Epoch [5120/10000], loss: 0.17495 acc: 0.98667 val_loss: 0.17867, val_acc: 0.96000
    Epoch [5130/10000], loss: 0.17478 acc: 0.98667 val_loss: 0.17852, val_acc: 0.96000
    Epoch [5140/10000], loss: 0.17461 acc: 0.98667 val_loss: 0.17837, val_acc: 0.96000
    Epoch [5150/10000], loss: 0.17444 acc: 0.98667 val_loss: 0.17822, val_acc: 0.96000
    Epoch [5160/10000], loss: 0.17427 acc: 0.98667 val_loss: 0.17807, val_acc: 0.96000
    Epoch [5170/10000], loss: 0.17410 acc: 0.98667 val_loss: 0.17792, val_acc: 0.96000
    Epoch [5180/10000], loss: 0.17393 acc: 0.98667 val_loss: 0.17778, val_acc: 0.96000
    Epoch [5190/10000], loss: 0.17377 acc: 0.98667 val_loss: 0.17763, val_acc: 0.96000
    Epoch [5200/10000], loss: 0.17360 acc: 0.98667 val_loss: 0.17748, val_acc: 0.96000
    Epoch [5210/10000], loss: 0.17343 acc: 0.98667 val_loss: 0.17733, val_acc: 0.96000
    Epoch [5220/10000], loss: 0.17327 acc: 0.98667 val_loss: 0.17719, val_acc: 0.96000
    Epoch [5230/10000], loss: 0.17310 acc: 0.98667 val_loss: 0.17704, val_acc: 0.96000
    Epoch [5240/10000], loss: 0.17294 acc: 0.98667 val_loss: 0.17689, val_acc: 0.96000
    Epoch [5250/10000], loss: 0.17277 acc: 0.98667 val_loss: 0.17675, val_acc: 0.96000
    Epoch [5260/10000], loss: 0.17261 acc: 0.98667 val_loss: 0.17660, val_acc: 0.96000
    Epoch [5270/10000], loss: 0.17245 acc: 0.98667 val_loss: 0.17646, val_acc: 0.96000
    Epoch [5280/10000], loss: 0.17229 acc: 0.98667 val_loss: 0.17631, val_acc: 0.96000
    Epoch [5290/10000], loss: 0.17212 acc: 0.98667 val_loss: 0.17617, val_acc: 0.96000
    Epoch [5300/10000], loss: 0.17196 acc: 0.98667 val_loss: 0.17603, val_acc: 0.96000
    Epoch [5310/10000], loss: 0.17180 acc: 0.98667 val_loss: 0.17589, val_acc: 0.96000
    Epoch [5320/10000], loss: 0.17164 acc: 0.98667 val_loss: 0.17574, val_acc: 0.96000
    Epoch [5330/10000], loss: 0.17148 acc: 0.98667 val_loss: 0.17560, val_acc: 0.96000
    Epoch [5340/10000], loss: 0.17132 acc: 0.98667 val_loss: 0.17546, val_acc: 0.96000
    Epoch [5350/10000], loss: 0.17116 acc: 0.98667 val_loss: 0.17532, val_acc: 0.96000
    Epoch [5360/10000], loss: 0.17100 acc: 0.98667 val_loss: 0.17518, val_acc: 0.96000
    Epoch [5370/10000], loss: 0.17084 acc: 0.98667 val_loss: 0.17504, val_acc: 0.96000
    Epoch [5380/10000], loss: 0.17068 acc: 0.98667 val_loss: 0.17490, val_acc: 0.96000
    Epoch [5390/10000], loss: 0.17053 acc: 0.98667 val_loss: 0.17476, val_acc: 0.96000
    Epoch [5400/10000], loss: 0.17037 acc: 0.98667 val_loss: 0.17462, val_acc: 0.96000
    Epoch [5410/10000], loss: 0.17021 acc: 0.98667 val_loss: 0.17448, val_acc: 0.96000
    Epoch [5420/10000], loss: 0.17006 acc: 0.98667 val_loss: 0.17434, val_acc: 0.96000
    Epoch [5430/10000], loss: 0.16990 acc: 0.98667 val_loss: 0.17421, val_acc: 0.96000
    Epoch [5440/10000], loss: 0.16975 acc: 0.98667 val_loss: 0.17407, val_acc: 0.96000
    Epoch [5450/10000], loss: 0.16959 acc: 0.98667 val_loss: 0.17393, val_acc: 0.96000
    Epoch [5460/10000], loss: 0.16944 acc: 0.98667 val_loss: 0.17380, val_acc: 0.96000
    Epoch [5470/10000], loss: 0.16928 acc: 0.98667 val_loss: 0.17366, val_acc: 0.96000
    Epoch [5480/10000], loss: 0.16913 acc: 0.98667 val_loss: 0.17352, val_acc: 0.96000
    Epoch [5490/10000], loss: 0.16898 acc: 0.98667 val_loss: 0.17339, val_acc: 0.96000
    Epoch [5500/10000], loss: 0.16883 acc: 0.98667 val_loss: 0.17325, val_acc: 0.96000
    Epoch [5510/10000], loss: 0.16867 acc: 0.98667 val_loss: 0.17312, val_acc: 0.96000
    Epoch [5520/10000], loss: 0.16852 acc: 0.98667 val_loss: 0.17299, val_acc: 0.96000
    Epoch [5530/10000], loss: 0.16837 acc: 0.98667 val_loss: 0.17285, val_acc: 0.96000
    Epoch [5540/10000], loss: 0.16822 acc: 0.98667 val_loss: 0.17272, val_acc: 0.96000
    Epoch [5550/10000], loss: 0.16807 acc: 0.98667 val_loss: 0.17259, val_acc: 0.96000
    Epoch [5560/10000], loss: 0.16792 acc: 0.98667 val_loss: 0.17246, val_acc: 0.96000
    Epoch [5570/10000], loss: 0.16777 acc: 0.98667 val_loss: 0.17232, val_acc: 0.96000
    Epoch [5580/10000], loss: 0.16762 acc: 0.98667 val_loss: 0.17219, val_acc: 0.96000
    Epoch [5590/10000], loss: 0.16747 acc: 0.98667 val_loss: 0.17206, val_acc: 0.96000
    Epoch [5600/10000], loss: 0.16732 acc: 0.98667 val_loss: 0.17193, val_acc: 0.96000
    Epoch [5610/10000], loss: 0.16718 acc: 0.98667 val_loss: 0.17180, val_acc: 0.96000
    Epoch [5620/10000], loss: 0.16703 acc: 0.98667 val_loss: 0.17167, val_acc: 0.96000
    Epoch [5630/10000], loss: 0.16688 acc: 0.98667 val_loss: 0.17154, val_acc: 0.96000
    Epoch [5640/10000], loss: 0.16674 acc: 0.98667 val_loss: 0.17141, val_acc: 0.96000
    Epoch [5650/10000], loss: 0.16659 acc: 0.98667 val_loss: 0.17128, val_acc: 0.96000
    Epoch [5660/10000], loss: 0.16644 acc: 0.98667 val_loss: 0.17115, val_acc: 0.96000
    Epoch [5670/10000], loss: 0.16630 acc: 0.98667 val_loss: 0.17103, val_acc: 0.96000
    Epoch [5680/10000], loss: 0.16615 acc: 0.98667 val_loss: 0.17090, val_acc: 0.96000
    Epoch [5690/10000], loss: 0.16601 acc: 0.98667 val_loss: 0.17077, val_acc: 0.96000
    Epoch [5700/10000], loss: 0.16587 acc: 0.98667 val_loss: 0.17064, val_acc: 0.96000
    Epoch [5710/10000], loss: 0.16572 acc: 0.98667 val_loss: 0.17052, val_acc: 0.96000
    Epoch [5720/10000], loss: 0.16558 acc: 0.98667 val_loss: 0.17039, val_acc: 0.96000
    Epoch [5730/10000], loss: 0.16544 acc: 0.98667 val_loss: 0.17027, val_acc: 0.96000
    Epoch [5740/10000], loss: 0.16529 acc: 0.98667 val_loss: 0.17014, val_acc: 0.96000
    Epoch [5750/10000], loss: 0.16515 acc: 0.98667 val_loss: 0.17001, val_acc: 0.96000
    Epoch [5760/10000], loss: 0.16501 acc: 0.98667 val_loss: 0.16989, val_acc: 0.96000
    Epoch [5770/10000], loss: 0.16487 acc: 0.98667 val_loss: 0.16977, val_acc: 0.96000
    Epoch [5780/10000], loss: 0.16473 acc: 0.98667 val_loss: 0.16964, val_acc: 0.96000
    Epoch [5790/10000], loss: 0.16459 acc: 0.98667 val_loss: 0.16952, val_acc: 0.96000
    Epoch [5800/10000], loss: 0.16445 acc: 0.98667 val_loss: 0.16939, val_acc: 0.96000
    Epoch [5810/10000], loss: 0.16431 acc: 0.98667 val_loss: 0.16927, val_acc: 0.96000
    Epoch [5820/10000], loss: 0.16417 acc: 0.98667 val_loss: 0.16915, val_acc: 0.96000
    Epoch [5830/10000], loss: 0.16403 acc: 0.98667 val_loss: 0.16903, val_acc: 0.96000
    Epoch [5840/10000], loss: 0.16389 acc: 0.98667 val_loss: 0.16891, val_acc: 0.96000
    Epoch [5850/10000], loss: 0.16375 acc: 0.98667 val_loss: 0.16878, val_acc: 0.96000
    Epoch [5860/10000], loss: 0.16361 acc: 0.98667 val_loss: 0.16866, val_acc: 0.96000
    Epoch [5870/10000], loss: 0.16348 acc: 0.98667 val_loss: 0.16854, val_acc: 0.96000
    Epoch [5880/10000], loss: 0.16334 acc: 0.98667 val_loss: 0.16842, val_acc: 0.96000
    Epoch [5890/10000], loss: 0.16320 acc: 0.98667 val_loss: 0.16830, val_acc: 0.96000
    Epoch [5900/10000], loss: 0.16307 acc: 0.98667 val_loss: 0.16818, val_acc: 0.96000
    Epoch [5910/10000], loss: 0.16293 acc: 0.98667 val_loss: 0.16806, val_acc: 0.96000
    Epoch [5920/10000], loss: 0.16280 acc: 0.98667 val_loss: 0.16794, val_acc: 0.96000
    Epoch [5930/10000], loss: 0.16266 acc: 0.98667 val_loss: 0.16782, val_acc: 0.96000
    Epoch [5940/10000], loss: 0.16253 acc: 0.98667 val_loss: 0.16771, val_acc: 0.96000
    Epoch [5950/10000], loss: 0.16239 acc: 0.98667 val_loss: 0.16759, val_acc: 0.96000
    Epoch [5960/10000], loss: 0.16226 acc: 0.98667 val_loss: 0.16747, val_acc: 0.96000
    Epoch [5970/10000], loss: 0.16212 acc: 0.98667 val_loss: 0.16735, val_acc: 0.96000
    Epoch [5980/10000], loss: 0.16199 acc: 0.98667 val_loss: 0.16724, val_acc: 0.96000
    Epoch [5990/10000], loss: 0.16186 acc: 0.98667 val_loss: 0.16712, val_acc: 0.96000
    Epoch [6000/10000], loss: 0.16172 acc: 0.98667 val_loss: 0.16700, val_acc: 0.96000
    Epoch [6010/10000], loss: 0.16159 acc: 0.98667 val_loss: 0.16689, val_acc: 0.96000
    Epoch [6020/10000], loss: 0.16146 acc: 0.98667 val_loss: 0.16677, val_acc: 0.96000
    Epoch [6030/10000], loss: 0.16133 acc: 0.98667 val_loss: 0.16665, val_acc: 0.96000
    Epoch [6040/10000], loss: 0.16120 acc: 0.98667 val_loss: 0.16654, val_acc: 0.96000
    Epoch [6050/10000], loss: 0.16107 acc: 0.98667 val_loss: 0.16642, val_acc: 0.96000
    Epoch [6060/10000], loss: 0.16093 acc: 0.98667 val_loss: 0.16631, val_acc: 0.96000
    Epoch [6070/10000], loss: 0.16080 acc: 0.98667 val_loss: 0.16620, val_acc: 0.96000
    Epoch [6080/10000], loss: 0.16067 acc: 0.98667 val_loss: 0.16608, val_acc: 0.96000
    Epoch [6090/10000], loss: 0.16055 acc: 0.98667 val_loss: 0.16597, val_acc: 0.96000
    Epoch [6100/10000], loss: 0.16042 acc: 0.98667 val_loss: 0.16585, val_acc: 0.96000
    Epoch [6110/10000], loss: 0.16029 acc: 0.98667 val_loss: 0.16574, val_acc: 0.96000
    Epoch [6120/10000], loss: 0.16016 acc: 0.98667 val_loss: 0.16563, val_acc: 0.96000
    Epoch [6130/10000], loss: 0.16003 acc: 0.98667 val_loss: 0.16552, val_acc: 0.96000
    Epoch [6140/10000], loss: 0.15990 acc: 0.98667 val_loss: 0.16540, val_acc: 0.96000
    Epoch [6150/10000], loss: 0.15978 acc: 0.98667 val_loss: 0.16529, val_acc: 0.96000
    Epoch [6160/10000], loss: 0.15965 acc: 0.98667 val_loss: 0.16518, val_acc: 0.96000
    Epoch [6170/10000], loss: 0.15952 acc: 0.98667 val_loss: 0.16507, val_acc: 0.96000
    Epoch [6180/10000], loss: 0.15939 acc: 0.98667 val_loss: 0.16496, val_acc: 0.96000
    Epoch [6190/10000], loss: 0.15927 acc: 0.98667 val_loss: 0.16485, val_acc: 0.96000
    Epoch [6200/10000], loss: 0.15914 acc: 0.98667 val_loss: 0.16474, val_acc: 0.96000
    Epoch [6210/10000], loss: 0.15902 acc: 0.98667 val_loss: 0.16463, val_acc: 0.96000
    Epoch [6220/10000], loss: 0.15889 acc: 0.98667 val_loss: 0.16452, val_acc: 0.96000
    Epoch [6230/10000], loss: 0.15877 acc: 0.98667 val_loss: 0.16441, val_acc: 0.96000
    Epoch [6240/10000], loss: 0.15864 acc: 0.98667 val_loss: 0.16430, val_acc: 0.96000
    Epoch [6250/10000], loss: 0.15852 acc: 0.98667 val_loss: 0.16419, val_acc: 0.96000
    Epoch [6260/10000], loss: 0.15839 acc: 0.98667 val_loss: 0.16408, val_acc: 0.96000
    Epoch [6270/10000], loss: 0.15827 acc: 0.98667 val_loss: 0.16398, val_acc: 0.96000
    Epoch [6280/10000], loss: 0.15815 acc: 0.98667 val_loss: 0.16387, val_acc: 0.96000
    Epoch [6290/10000], loss: 0.15802 acc: 0.98667 val_loss: 0.16376, val_acc: 0.96000
    Epoch [6300/10000], loss: 0.15790 acc: 0.98667 val_loss: 0.16365, val_acc: 0.96000
    Epoch [6310/10000], loss: 0.15778 acc: 0.98667 val_loss: 0.16355, val_acc: 0.96000
    Epoch [6320/10000], loss: 0.15766 acc: 0.98667 val_loss: 0.16344, val_acc: 0.96000
    Epoch [6330/10000], loss: 0.15754 acc: 0.98667 val_loss: 0.16333, val_acc: 0.96000
    Epoch [6340/10000], loss: 0.15741 acc: 0.98667 val_loss: 0.16323, val_acc: 0.96000
    Epoch [6350/10000], loss: 0.15729 acc: 0.98667 val_loss: 0.16312, val_acc: 0.96000
    Epoch [6360/10000], loss: 0.15717 acc: 0.98667 val_loss: 0.16302, val_acc: 0.96000
    Epoch [6370/10000], loss: 0.15705 acc: 0.98667 val_loss: 0.16291, val_acc: 0.96000
    Epoch [6380/10000], loss: 0.15693 acc: 0.98667 val_loss: 0.16281, val_acc: 0.96000
    Epoch [6390/10000], loss: 0.15681 acc: 0.98667 val_loss: 0.16270, val_acc: 0.96000
    Epoch [6400/10000], loss: 0.15669 acc: 0.98667 val_loss: 0.16260, val_acc: 0.96000
    Epoch [6410/10000], loss: 0.15657 acc: 0.98667 val_loss: 0.16249, val_acc: 0.96000
    Epoch [6420/10000], loss: 0.15645 acc: 0.98667 val_loss: 0.16239, val_acc: 0.96000
    Epoch [6430/10000], loss: 0.15634 acc: 0.98667 val_loss: 0.16228, val_acc: 0.96000
    Epoch [6440/10000], loss: 0.15622 acc: 0.98667 val_loss: 0.16218, val_acc: 0.96000
    Epoch [6450/10000], loss: 0.15610 acc: 0.98667 val_loss: 0.16208, val_acc: 0.96000
    Epoch [6460/10000], loss: 0.15598 acc: 0.98667 val_loss: 0.16198, val_acc: 0.96000
    Epoch [6470/10000], loss: 0.15586 acc: 0.98667 val_loss: 0.16187, val_acc: 0.96000
    Epoch [6480/10000], loss: 0.15575 acc: 0.98667 val_loss: 0.16177, val_acc: 0.96000
    Epoch [6490/10000], loss: 0.15563 acc: 0.98667 val_loss: 0.16167, val_acc: 0.96000
    Epoch [6500/10000], loss: 0.15551 acc: 0.98667 val_loss: 0.16157, val_acc: 0.96000
    Epoch [6510/10000], loss: 0.15540 acc: 0.98667 val_loss: 0.16147, val_acc: 0.96000
    Epoch [6520/10000], loss: 0.15528 acc: 0.98667 val_loss: 0.16136, val_acc: 0.96000
    Epoch [6530/10000], loss: 0.15516 acc: 0.98667 val_loss: 0.16126, val_acc: 0.96000
    Epoch [6540/10000], loss: 0.15505 acc: 0.98667 val_loss: 0.16116, val_acc: 0.96000
    Epoch [6550/10000], loss: 0.15493 acc: 0.98667 val_loss: 0.16106, val_acc: 0.96000
    Epoch [6560/10000], loss: 0.15482 acc: 0.98667 val_loss: 0.16096, val_acc: 0.96000
    Epoch [6570/10000], loss: 0.15470 acc: 0.98667 val_loss: 0.16086, val_acc: 0.96000
    Epoch [6580/10000], loss: 0.15459 acc: 0.98667 val_loss: 0.16076, val_acc: 0.96000
    Epoch [6590/10000], loss: 0.15448 acc: 0.98667 val_loss: 0.16066, val_acc: 0.96000
    Epoch [6600/10000], loss: 0.15436 acc: 0.98667 val_loss: 0.16056, val_acc: 0.96000
    Epoch [6610/10000], loss: 0.15425 acc: 0.98667 val_loss: 0.16047, val_acc: 0.96000
    Epoch [6620/10000], loss: 0.15414 acc: 0.98667 val_loss: 0.16037, val_acc: 0.96000
    Epoch [6630/10000], loss: 0.15402 acc: 0.98667 val_loss: 0.16027, val_acc: 0.96000
    Epoch [6640/10000], loss: 0.15391 acc: 0.98667 val_loss: 0.16017, val_acc: 0.96000
    Epoch [6650/10000], loss: 0.15380 acc: 0.98667 val_loss: 0.16007, val_acc: 0.96000
    Epoch [6660/10000], loss: 0.15369 acc: 0.98667 val_loss: 0.15997, val_acc: 0.96000
    Epoch [6670/10000], loss: 0.15357 acc: 0.98667 val_loss: 0.15988, val_acc: 0.96000
    Epoch [6680/10000], loss: 0.15346 acc: 0.98667 val_loss: 0.15978, val_acc: 0.96000
    Epoch [6690/10000], loss: 0.15335 acc: 0.98667 val_loss: 0.15968, val_acc: 0.96000
    Epoch [6700/10000], loss: 0.15324 acc: 0.98667 val_loss: 0.15959, val_acc: 0.96000
    Epoch [6710/10000], loss: 0.15313 acc: 0.98667 val_loss: 0.15949, val_acc: 0.96000
    Epoch [6720/10000], loss: 0.15302 acc: 0.98667 val_loss: 0.15939, val_acc: 0.96000
    Epoch [6730/10000], loss: 0.15291 acc: 0.98667 val_loss: 0.15930, val_acc: 0.96000
    Epoch [6740/10000], loss: 0.15280 acc: 0.98667 val_loss: 0.15920, val_acc: 0.96000
    Epoch [6750/10000], loss: 0.15269 acc: 0.98667 val_loss: 0.15911, val_acc: 0.96000
    Epoch [6760/10000], loss: 0.15258 acc: 0.98667 val_loss: 0.15901, val_acc: 0.96000
    Epoch [6770/10000], loss: 0.15247 acc: 0.98667 val_loss: 0.15892, val_acc: 0.96000
    Epoch [6780/10000], loss: 0.15236 acc: 0.98667 val_loss: 0.15882, val_acc: 0.96000
    Epoch [6790/10000], loss: 0.15225 acc: 0.98667 val_loss: 0.15873, val_acc: 0.96000
    Epoch [6800/10000], loss: 0.15214 acc: 0.98667 val_loss: 0.15863, val_acc: 0.96000
    Epoch [6810/10000], loss: 0.15204 acc: 0.98667 val_loss: 0.15854, val_acc: 0.96000
    Epoch [6820/10000], loss: 0.15193 acc: 0.98667 val_loss: 0.15845, val_acc: 0.96000
    Epoch [6830/10000], loss: 0.15182 acc: 0.98667 val_loss: 0.15835, val_acc: 0.96000
    Epoch [6840/10000], loss: 0.15171 acc: 0.98667 val_loss: 0.15826, val_acc: 0.96000
    Epoch [6850/10000], loss: 0.15161 acc: 0.98667 val_loss: 0.15817, val_acc: 0.96000
    Epoch [6860/10000], loss: 0.15150 acc: 0.98667 val_loss: 0.15807, val_acc: 0.96000
    Epoch [6870/10000], loss: 0.15139 acc: 0.98667 val_loss: 0.15798, val_acc: 0.96000
    Epoch [6880/10000], loss: 0.15129 acc: 0.98667 val_loss: 0.15789, val_acc: 0.96000
    Epoch [6890/10000], loss: 0.15118 acc: 0.98667 val_loss: 0.15780, val_acc: 0.96000
    Epoch [6900/10000], loss: 0.15108 acc: 0.98667 val_loss: 0.15771, val_acc: 0.96000
    Epoch [6910/10000], loss: 0.15097 acc: 0.98667 val_loss: 0.15761, val_acc: 0.96000
    Epoch [6920/10000], loss: 0.15086 acc: 0.98667 val_loss: 0.15752, val_acc: 0.96000
    Epoch [6930/10000], loss: 0.15076 acc: 0.98667 val_loss: 0.15743, val_acc: 0.96000
    Epoch [6940/10000], loss: 0.15065 acc: 0.98667 val_loss: 0.15734, val_acc: 0.96000
    Epoch [6950/10000], loss: 0.15055 acc: 0.98667 val_loss: 0.15725, val_acc: 0.96000
    Epoch [6960/10000], loss: 0.15045 acc: 0.98667 val_loss: 0.15716, val_acc: 0.96000
    Epoch [6970/10000], loss: 0.15034 acc: 0.98667 val_loss: 0.15707, val_acc: 0.96000
    Epoch [6980/10000], loss: 0.15024 acc: 0.98667 val_loss: 0.15698, val_acc: 0.96000
    Epoch [6990/10000], loss: 0.15013 acc: 0.98667 val_loss: 0.15689, val_acc: 0.96000
    Epoch [7000/10000], loss: 0.15003 acc: 0.98667 val_loss: 0.15680, val_acc: 0.96000
    Epoch [7010/10000], loss: 0.14993 acc: 0.98667 val_loss: 0.15671, val_acc: 0.96000
    Epoch [7020/10000], loss: 0.14983 acc: 0.98667 val_loss: 0.15662, val_acc: 0.96000
    Epoch [7030/10000], loss: 0.14972 acc: 0.98667 val_loss: 0.15653, val_acc: 0.96000
    Epoch [7040/10000], loss: 0.14962 acc: 0.98667 val_loss: 0.15644, val_acc: 0.96000
    Epoch [7050/10000], loss: 0.14952 acc: 0.98667 val_loss: 0.15636, val_acc: 0.96000
    Epoch [7060/10000], loss: 0.14942 acc: 0.98667 val_loss: 0.15627, val_acc: 0.96000
    Epoch [7070/10000], loss: 0.14931 acc: 0.98667 val_loss: 0.15618, val_acc: 0.96000
    Epoch [7080/10000], loss: 0.14921 acc: 0.98667 val_loss: 0.15609, val_acc: 0.96000
    Epoch [7090/10000], loss: 0.14911 acc: 0.98667 val_loss: 0.15600, val_acc: 0.96000
    Epoch [7100/10000], loss: 0.14901 acc: 0.98667 val_loss: 0.15592, val_acc: 0.96000
    Epoch [7110/10000], loss: 0.14891 acc: 0.98667 val_loss: 0.15583, val_acc: 0.96000
    Epoch [7120/10000], loss: 0.14881 acc: 0.98667 val_loss: 0.15574, val_acc: 0.96000
    Epoch [7130/10000], loss: 0.14871 acc: 0.98667 val_loss: 0.15565, val_acc: 0.96000
    Epoch [7140/10000], loss: 0.14861 acc: 0.98667 val_loss: 0.15557, val_acc: 0.96000
    Epoch [7150/10000], loss: 0.14851 acc: 0.98667 val_loss: 0.15548, val_acc: 0.96000
    Epoch [7160/10000], loss: 0.14841 acc: 0.98667 val_loss: 0.15540, val_acc: 0.96000
    Epoch [7170/10000], loss: 0.14831 acc: 0.98667 val_loss: 0.15531, val_acc: 0.96000
    Epoch [7180/10000], loss: 0.14821 acc: 0.98667 val_loss: 0.15522, val_acc: 0.96000
    Epoch [7190/10000], loss: 0.14811 acc: 0.98667 val_loss: 0.15514, val_acc: 0.96000
    Epoch [7200/10000], loss: 0.14801 acc: 0.98667 val_loss: 0.15505, val_acc: 0.96000
    Epoch [7210/10000], loss: 0.14792 acc: 0.98667 val_loss: 0.15497, val_acc: 0.96000
    Epoch [7220/10000], loss: 0.14782 acc: 0.98667 val_loss: 0.15488, val_acc: 0.96000
    Epoch [7230/10000], loss: 0.14772 acc: 0.98667 val_loss: 0.15480, val_acc: 0.96000
    Epoch [7240/10000], loss: 0.14762 acc: 0.98667 val_loss: 0.15471, val_acc: 0.96000
    Epoch [7250/10000], loss: 0.14752 acc: 0.98667 val_loss: 0.15463, val_acc: 0.96000
    Epoch [7260/10000], loss: 0.14743 acc: 0.98667 val_loss: 0.15455, val_acc: 0.96000
    Epoch [7270/10000], loss: 0.14733 acc: 0.98667 val_loss: 0.15446, val_acc: 0.96000
    Epoch [7280/10000], loss: 0.14723 acc: 0.98667 val_loss: 0.15438, val_acc: 0.96000
    Epoch [7290/10000], loss: 0.14714 acc: 0.98667 val_loss: 0.15429, val_acc: 0.96000
    Epoch [7300/10000], loss: 0.14704 acc: 0.98667 val_loss: 0.15421, val_acc: 0.96000
    Epoch [7310/10000], loss: 0.14694 acc: 0.98667 val_loss: 0.15413, val_acc: 0.96000
    Epoch [7320/10000], loss: 0.14685 acc: 0.98667 val_loss: 0.15404, val_acc: 0.96000
    Epoch [7330/10000], loss: 0.14675 acc: 0.98667 val_loss: 0.15396, val_acc: 0.96000
    Epoch [7340/10000], loss: 0.14666 acc: 0.98667 val_loss: 0.15388, val_acc: 0.96000
    Epoch [7350/10000], loss: 0.14656 acc: 0.98667 val_loss: 0.15380, val_acc: 0.96000
    Epoch [7360/10000], loss: 0.14646 acc: 0.98667 val_loss: 0.15371, val_acc: 0.96000
    Epoch [7370/10000], loss: 0.14637 acc: 0.98667 val_loss: 0.15363, val_acc: 0.96000
    Epoch [7380/10000], loss: 0.14627 acc: 0.98667 val_loss: 0.15355, val_acc: 0.96000
    Epoch [7390/10000], loss: 0.14618 acc: 0.98667 val_loss: 0.15347, val_acc: 0.96000
    Epoch [7400/10000], loss: 0.14609 acc: 0.98667 val_loss: 0.15339, val_acc: 0.96000
    Epoch [7410/10000], loss: 0.14599 acc: 0.98667 val_loss: 0.15331, val_acc: 0.96000
    Epoch [7420/10000], loss: 0.14590 acc: 0.98667 val_loss: 0.15323, val_acc: 0.96000
    Epoch [7430/10000], loss: 0.14580 acc: 0.98667 val_loss: 0.15314, val_acc: 0.96000
    Epoch [7440/10000], loss: 0.14571 acc: 0.98667 val_loss: 0.15306, val_acc: 0.96000
    Epoch [7450/10000], loss: 0.14562 acc: 0.98667 val_loss: 0.15298, val_acc: 0.96000
    Epoch [7460/10000], loss: 0.14552 acc: 0.98667 val_loss: 0.15290, val_acc: 0.96000
    Epoch [7470/10000], loss: 0.14543 acc: 0.98667 val_loss: 0.15282, val_acc: 0.96000
    Epoch [7480/10000], loss: 0.14534 acc: 0.98667 val_loss: 0.15274, val_acc: 0.96000
    Epoch [7490/10000], loss: 0.14525 acc: 0.98667 val_loss: 0.15266, val_acc: 0.96000
    Epoch [7500/10000], loss: 0.14515 acc: 0.98667 val_loss: 0.15258, val_acc: 0.96000
    Epoch [7510/10000], loss: 0.14506 acc: 0.98667 val_loss: 0.15250, val_acc: 0.96000
    Epoch [7520/10000], loss: 0.14497 acc: 0.98667 val_loss: 0.15243, val_acc: 0.96000
    Epoch [7530/10000], loss: 0.14488 acc: 0.98667 val_loss: 0.15235, val_acc: 0.96000
    Epoch [7540/10000], loss: 0.14479 acc: 0.98667 val_loss: 0.15227, val_acc: 0.96000
    Epoch [7550/10000], loss: 0.14470 acc: 0.98667 val_loss: 0.15219, val_acc: 0.96000
    Epoch [7560/10000], loss: 0.14460 acc: 0.98667 val_loss: 0.15211, val_acc: 0.96000
    Epoch [7570/10000], loss: 0.14451 acc: 0.98667 val_loss: 0.15203, val_acc: 0.96000
    Epoch [7580/10000], loss: 0.14442 acc: 0.98667 val_loss: 0.15195, val_acc: 0.96000
    Epoch [7590/10000], loss: 0.14433 acc: 0.98667 val_loss: 0.15188, val_acc: 0.96000
    Epoch [7600/10000], loss: 0.14424 acc: 0.98667 val_loss: 0.15180, val_acc: 0.96000
    Epoch [7610/10000], loss: 0.14415 acc: 0.98667 val_loss: 0.15172, val_acc: 0.96000
    Epoch [7620/10000], loss: 0.14406 acc: 0.98667 val_loss: 0.15164, val_acc: 0.96000
    Epoch [7630/10000], loss: 0.14397 acc: 0.98667 val_loss: 0.15157, val_acc: 0.96000
    Epoch [7640/10000], loss: 0.14388 acc: 0.98667 val_loss: 0.15149, val_acc: 0.96000
    Epoch [7650/10000], loss: 0.14379 acc: 0.98667 val_loss: 0.15141, val_acc: 0.96000
    Epoch [7660/10000], loss: 0.14370 acc: 0.98667 val_loss: 0.15134, val_acc: 0.96000
    Epoch [7670/10000], loss: 0.14362 acc: 0.98667 val_loss: 0.15126, val_acc: 0.96000
    Epoch [7680/10000], loss: 0.14353 acc: 0.98667 val_loss: 0.15118, val_acc: 0.96000
    Epoch [7690/10000], loss: 0.14344 acc: 0.98667 val_loss: 0.15111, val_acc: 0.96000
    Epoch [7700/10000], loss: 0.14335 acc: 0.98667 val_loss: 0.15103, val_acc: 0.96000
    Epoch [7710/10000], loss: 0.14326 acc: 0.98667 val_loss: 0.15096, val_acc: 0.96000
    Epoch [7720/10000], loss: 0.14317 acc: 0.98667 val_loss: 0.15088, val_acc: 0.96000
    Epoch [7730/10000], loss: 0.14309 acc: 0.98667 val_loss: 0.15080, val_acc: 0.96000
    Epoch [7740/10000], loss: 0.14300 acc: 0.98667 val_loss: 0.15073, val_acc: 0.96000
    Epoch [7750/10000], loss: 0.14291 acc: 0.98667 val_loss: 0.15065, val_acc: 0.96000
    Epoch [7760/10000], loss: 0.14282 acc: 0.98667 val_loss: 0.15058, val_acc: 0.96000
    Epoch [7770/10000], loss: 0.14274 acc: 0.98667 val_loss: 0.15050, val_acc: 0.96000
    Epoch [7780/10000], loss: 0.14265 acc: 0.98667 val_loss: 0.15043, val_acc: 0.96000
    Epoch [7790/10000], loss: 0.14256 acc: 0.98667 val_loss: 0.15036, val_acc: 0.96000
    Epoch [7800/10000], loss: 0.14248 acc: 0.98667 val_loss: 0.15028, val_acc: 0.96000
    Epoch [7810/10000], loss: 0.14239 acc: 0.98667 val_loss: 0.15021, val_acc: 0.96000
    Epoch [7820/10000], loss: 0.14230 acc: 0.98667 val_loss: 0.15013, val_acc: 0.96000
    Epoch [7830/10000], loss: 0.14222 acc: 0.98667 val_loss: 0.15006, val_acc: 0.96000
    Epoch [7840/10000], loss: 0.14213 acc: 0.98667 val_loss: 0.14999, val_acc: 0.96000
    Epoch [7850/10000], loss: 0.14205 acc: 0.98667 val_loss: 0.14991, val_acc: 0.96000
    Epoch [7860/10000], loss: 0.14196 acc: 0.98667 val_loss: 0.14984, val_acc: 0.96000
    Epoch [7870/10000], loss: 0.14188 acc: 0.98667 val_loss: 0.14977, val_acc: 0.96000
    Epoch [7880/10000], loss: 0.14179 acc: 0.98667 val_loss: 0.14969, val_acc: 0.96000
    Epoch [7890/10000], loss: 0.14171 acc: 0.98667 val_loss: 0.14962, val_acc: 0.96000
    Epoch [7900/10000], loss: 0.14162 acc: 0.98667 val_loss: 0.14955, val_acc: 0.96000
    Epoch [7910/10000], loss: 0.14154 acc: 0.98667 val_loss: 0.14948, val_acc: 0.96000
    Epoch [7920/10000], loss: 0.14145 acc: 0.98667 val_loss: 0.14940, val_acc: 0.96000
    Epoch [7930/10000], loss: 0.14137 acc: 0.98667 val_loss: 0.14933, val_acc: 0.96000
    Epoch [7940/10000], loss: 0.14128 acc: 0.98667 val_loss: 0.14926, val_acc: 0.96000
    Epoch [7950/10000], loss: 0.14120 acc: 0.98667 val_loss: 0.14919, val_acc: 0.96000
    Epoch [7960/10000], loss: 0.14112 acc: 0.98667 val_loss: 0.14912, val_acc: 0.96000
    Epoch [7970/10000], loss: 0.14103 acc: 0.98667 val_loss: 0.14904, val_acc: 0.96000
    Epoch [7980/10000], loss: 0.14095 acc: 0.98667 val_loss: 0.14897, val_acc: 0.96000
    Epoch [7990/10000], loss: 0.14087 acc: 0.98667 val_loss: 0.14890, val_acc: 0.96000
    Epoch [8000/10000], loss: 0.14078 acc: 0.98667 val_loss: 0.14883, val_acc: 0.96000
    Epoch [8010/10000], loss: 0.14070 acc: 0.98667 val_loss: 0.14876, val_acc: 0.96000
    Epoch [8020/10000], loss: 0.14062 acc: 0.98667 val_loss: 0.14869, val_acc: 0.96000
    Epoch [8030/10000], loss: 0.14054 acc: 0.98667 val_loss: 0.14862, val_acc: 0.96000
    Epoch [8040/10000], loss: 0.14045 acc: 0.98667 val_loss: 0.14855, val_acc: 0.96000
    Epoch [8050/10000], loss: 0.14037 acc: 0.98667 val_loss: 0.14848, val_acc: 0.96000
    Epoch [8060/10000], loss: 0.14029 acc: 0.98667 val_loss: 0.14841, val_acc: 0.96000
    Epoch [8070/10000], loss: 0.14021 acc: 0.98667 val_loss: 0.14834, val_acc: 0.96000
    Epoch [8080/10000], loss: 0.14013 acc: 0.98667 val_loss: 0.14827, val_acc: 0.96000
    Epoch [8090/10000], loss: 0.14004 acc: 0.98667 val_loss: 0.14820, val_acc: 0.96000
    Epoch [8100/10000], loss: 0.13996 acc: 0.98667 val_loss: 0.14813, val_acc: 0.96000
    Epoch [8110/10000], loss: 0.13988 acc: 0.98667 val_loss: 0.14806, val_acc: 0.96000
    Epoch [8120/10000], loss: 0.13980 acc: 0.98667 val_loss: 0.14799, val_acc: 0.96000
    Epoch [8130/10000], loss: 0.13972 acc: 0.98667 val_loss: 0.14792, val_acc: 0.96000
    Epoch [8140/10000], loss: 0.13964 acc: 0.98667 val_loss: 0.14785, val_acc: 0.96000
    Epoch [8150/10000], loss: 0.13956 acc: 0.98667 val_loss: 0.14778, val_acc: 0.96000
    Epoch [8160/10000], loss: 0.13948 acc: 0.98667 val_loss: 0.14771, val_acc: 0.96000
    Epoch [8170/10000], loss: 0.13940 acc: 0.98667 val_loss: 0.14765, val_acc: 0.96000
    Epoch [8180/10000], loss: 0.13932 acc: 0.98667 val_loss: 0.14758, val_acc: 0.96000
    Epoch [8190/10000], loss: 0.13924 acc: 0.98667 val_loss: 0.14751, val_acc: 0.96000
    Epoch [8200/10000], loss: 0.13916 acc: 0.98667 val_loss: 0.14744, val_acc: 0.96000
    Epoch [8210/10000], loss: 0.13908 acc: 0.98667 val_loss: 0.14737, val_acc: 0.96000
    Epoch [8220/10000], loss: 0.13900 acc: 0.98667 val_loss: 0.14731, val_acc: 0.96000
    Epoch [8230/10000], loss: 0.13892 acc: 0.98667 val_loss: 0.14724, val_acc: 0.96000
    Epoch [8240/10000], loss: 0.13884 acc: 0.98667 val_loss: 0.14717, val_acc: 0.96000
    Epoch [8250/10000], loss: 0.13876 acc: 0.98667 val_loss: 0.14710, val_acc: 0.96000
    Epoch [8260/10000], loss: 0.13869 acc: 0.98667 val_loss: 0.14704, val_acc: 0.96000
    Epoch [8270/10000], loss: 0.13861 acc: 0.98667 val_loss: 0.14697, val_acc: 0.96000
    Epoch [8280/10000], loss: 0.13853 acc: 0.98667 val_loss: 0.14690, val_acc: 0.96000
    Epoch [8290/10000], loss: 0.13845 acc: 0.98667 val_loss: 0.14684, val_acc: 0.96000
    Epoch [8300/10000], loss: 0.13837 acc: 0.98667 val_loss: 0.14677, val_acc: 0.96000
    Epoch [8310/10000], loss: 0.13829 acc: 0.98667 val_loss: 0.14670, val_acc: 0.96000
    Epoch [8320/10000], loss: 0.13822 acc: 0.98667 val_loss: 0.14664, val_acc: 0.96000
    Epoch [8330/10000], loss: 0.13814 acc: 0.98667 val_loss: 0.14657, val_acc: 0.96000
    Epoch [8340/10000], loss: 0.13806 acc: 0.98667 val_loss: 0.14650, val_acc: 0.96000
    Epoch [8350/10000], loss: 0.13798 acc: 0.98667 val_loss: 0.14644, val_acc: 0.96000
    Epoch [8360/10000], loss: 0.13791 acc: 0.98667 val_loss: 0.14637, val_acc: 0.96000
    Epoch [8370/10000], loss: 0.13783 acc: 0.98667 val_loss: 0.14631, val_acc: 0.96000
    Epoch [8380/10000], loss: 0.13775 acc: 0.98667 val_loss: 0.14624, val_acc: 0.96000
    Epoch [8390/10000], loss: 0.13768 acc: 0.98667 val_loss: 0.14618, val_acc: 0.96000
    Epoch [8400/10000], loss: 0.13760 acc: 0.98667 val_loss: 0.14611, val_acc: 0.96000
    Epoch [8410/10000], loss: 0.13752 acc: 0.98667 val_loss: 0.14605, val_acc: 0.96000
    Epoch [8420/10000], loss: 0.13745 acc: 0.98667 val_loss: 0.14598, val_acc: 0.96000
    Epoch [8430/10000], loss: 0.13737 acc: 0.98667 val_loss: 0.14592, val_acc: 0.96000
    Epoch [8440/10000], loss: 0.13730 acc: 0.98667 val_loss: 0.14585, val_acc: 0.96000
    Epoch [8450/10000], loss: 0.13722 acc: 0.98667 val_loss: 0.14579, val_acc: 0.96000
    Epoch [8460/10000], loss: 0.13714 acc: 0.98667 val_loss: 0.14572, val_acc: 0.96000
    Epoch [8470/10000], loss: 0.13707 acc: 0.98667 val_loss: 0.14566, val_acc: 0.96000
    Epoch [8480/10000], loss: 0.13699 acc: 0.98667 val_loss: 0.14559, val_acc: 0.96000
    Epoch [8490/10000], loss: 0.13692 acc: 0.98667 val_loss: 0.14553, val_acc: 0.96000
    Epoch [8500/10000], loss: 0.13684 acc: 0.98667 val_loss: 0.14547, val_acc: 0.96000
    Epoch [8510/10000], loss: 0.13677 acc: 0.98667 val_loss: 0.14540, val_acc: 0.96000
    Epoch [8520/10000], loss: 0.13669 acc: 0.98667 val_loss: 0.14534, val_acc: 0.96000
    Epoch [8530/10000], loss: 0.13662 acc: 0.98667 val_loss: 0.14528, val_acc: 0.96000
    Epoch [8540/10000], loss: 0.13654 acc: 0.98667 val_loss: 0.14521, val_acc: 0.96000
    Epoch [8550/10000], loss: 0.13647 acc: 0.98667 val_loss: 0.14515, val_acc: 0.96000
    Epoch [8560/10000], loss: 0.13640 acc: 0.98667 val_loss: 0.14509, val_acc: 0.96000
    Epoch [8570/10000], loss: 0.13632 acc: 0.98667 val_loss: 0.14502, val_acc: 0.96000
    Epoch [8580/10000], loss: 0.13625 acc: 0.98667 val_loss: 0.14496, val_acc: 0.96000
    Epoch [8590/10000], loss: 0.13617 acc: 0.98667 val_loss: 0.14490, val_acc: 0.96000
    Epoch [8600/10000], loss: 0.13610 acc: 0.98667 val_loss: 0.14483, val_acc: 0.96000
    Epoch [8610/10000], loss: 0.13603 acc: 0.98667 val_loss: 0.14477, val_acc: 0.96000
    Epoch [8620/10000], loss: 0.13595 acc: 0.98667 val_loss: 0.14471, val_acc: 0.96000
    Epoch [8630/10000], loss: 0.13588 acc: 0.98667 val_loss: 0.14465, val_acc: 0.96000
    Epoch [8640/10000], loss: 0.13581 acc: 0.98667 val_loss: 0.14459, val_acc: 0.96000
    Epoch [8650/10000], loss: 0.13574 acc: 0.98667 val_loss: 0.14452, val_acc: 0.96000
    Epoch [8660/10000], loss: 0.13566 acc: 0.98667 val_loss: 0.14446, val_acc: 0.96000
    Epoch [8670/10000], loss: 0.13559 acc: 0.98667 val_loss: 0.14440, val_acc: 0.96000
    Epoch [8680/10000], loss: 0.13552 acc: 0.98667 val_loss: 0.14434, val_acc: 0.96000
    Epoch [8690/10000], loss: 0.13545 acc: 0.98667 val_loss: 0.14428, val_acc: 0.96000
    Epoch [8700/10000], loss: 0.13537 acc: 0.98667 val_loss: 0.14422, val_acc: 0.96000
    Epoch [8710/10000], loss: 0.13530 acc: 0.98667 val_loss: 0.14415, val_acc: 0.96000
    Epoch [8720/10000], loss: 0.13523 acc: 0.98667 val_loss: 0.14409, val_acc: 0.96000
    Epoch [8730/10000], loss: 0.13516 acc: 0.98667 val_loss: 0.14403, val_acc: 0.96000
    Epoch [8740/10000], loss: 0.13509 acc: 0.98667 val_loss: 0.14397, val_acc: 0.96000
    Epoch [8750/10000], loss: 0.13501 acc: 0.98667 val_loss: 0.14391, val_acc: 0.96000
    Epoch [8760/10000], loss: 0.13494 acc: 0.98667 val_loss: 0.14385, val_acc: 0.96000
    Epoch [8770/10000], loss: 0.13487 acc: 0.98667 val_loss: 0.14379, val_acc: 0.96000
    Epoch [8780/10000], loss: 0.13480 acc: 0.98667 val_loss: 0.14373, val_acc: 0.96000
    Epoch [8790/10000], loss: 0.13473 acc: 0.98667 val_loss: 0.14367, val_acc: 0.96000
    Epoch [8800/10000], loss: 0.13466 acc: 0.98667 val_loss: 0.14361, val_acc: 0.96000
    Epoch [8810/10000], loss: 0.13459 acc: 0.98667 val_loss: 0.14355, val_acc: 0.96000
    Epoch [8820/10000], loss: 0.13452 acc: 0.98667 val_loss: 0.14349, val_acc: 0.96000
    Epoch [8830/10000], loss: 0.13445 acc: 0.98667 val_loss: 0.14343, val_acc: 0.96000
    Epoch [8840/10000], loss: 0.13438 acc: 0.98667 val_loss: 0.14337, val_acc: 0.96000
    Epoch [8850/10000], loss: 0.13431 acc: 0.98667 val_loss: 0.14331, val_acc: 0.96000
    Epoch [8860/10000], loss: 0.13424 acc: 0.98667 val_loss: 0.14325, val_acc: 0.96000
    Epoch [8870/10000], loss: 0.13417 acc: 0.98667 val_loss: 0.14319, val_acc: 0.96000
    Epoch [8880/10000], loss: 0.13410 acc: 0.98667 val_loss: 0.14313, val_acc: 0.96000
    Epoch [8890/10000], loss: 0.13403 acc: 0.98667 val_loss: 0.14308, val_acc: 0.96000
    Epoch [8900/10000], loss: 0.13396 acc: 0.98667 val_loss: 0.14302, val_acc: 0.96000
    Epoch [8910/10000], loss: 0.13389 acc: 0.98667 val_loss: 0.14296, val_acc: 0.96000
    Epoch [8920/10000], loss: 0.13382 acc: 0.98667 val_loss: 0.14290, val_acc: 0.96000
    Epoch [8930/10000], loss: 0.13375 acc: 0.98667 val_loss: 0.14284, val_acc: 0.96000
    Epoch [8940/10000], loss: 0.13368 acc: 0.98667 val_loss: 0.14278, val_acc: 0.96000
    Epoch [8950/10000], loss: 0.13361 acc: 0.98667 val_loss: 0.14272, val_acc: 0.96000
    Epoch [8960/10000], loss: 0.13354 acc: 0.98667 val_loss: 0.14266, val_acc: 0.96000
    Epoch [8970/10000], loss: 0.13347 acc: 0.98667 val_loss: 0.14261, val_acc: 0.96000
    Epoch [8980/10000], loss: 0.13341 acc: 0.98667 val_loss: 0.14255, val_acc: 0.96000
    Epoch [8990/10000], loss: 0.13334 acc: 0.98667 val_loss: 0.14249, val_acc: 0.96000
    Epoch [9000/10000], loss: 0.13327 acc: 0.98667 val_loss: 0.14243, val_acc: 0.96000
    Epoch [9010/10000], loss: 0.13320 acc: 0.98667 val_loss: 0.14238, val_acc: 0.96000
    Epoch [9020/10000], loss: 0.13313 acc: 0.98667 val_loss: 0.14232, val_acc: 0.96000
    Epoch [9030/10000], loss: 0.13307 acc: 0.98667 val_loss: 0.14226, val_acc: 0.96000
    Epoch [9040/10000], loss: 0.13300 acc: 0.98667 val_loss: 0.14220, val_acc: 0.96000
    Epoch [9050/10000], loss: 0.13293 acc: 0.98667 val_loss: 0.14215, val_acc: 0.96000
    Epoch [9060/10000], loss: 0.13286 acc: 0.98667 val_loss: 0.14209, val_acc: 0.96000
    Epoch [9070/10000], loss: 0.13280 acc: 0.98667 val_loss: 0.14203, val_acc: 0.96000
    Epoch [9080/10000], loss: 0.13273 acc: 0.98667 val_loss: 0.14198, val_acc: 0.96000
    Epoch [9090/10000], loss: 0.13266 acc: 0.98667 val_loss: 0.14192, val_acc: 0.96000
    Epoch [9100/10000], loss: 0.13259 acc: 0.98667 val_loss: 0.14186, val_acc: 0.96000
    Epoch [9110/10000], loss: 0.13253 acc: 0.98667 val_loss: 0.14181, val_acc: 0.96000
    Epoch [9120/10000], loss: 0.13246 acc: 0.98667 val_loss: 0.14175, val_acc: 0.96000
    Epoch [9130/10000], loss: 0.13239 acc: 0.98667 val_loss: 0.14169, val_acc: 0.96000
    Epoch [9140/10000], loss: 0.13233 acc: 0.98667 val_loss: 0.14164, val_acc: 0.96000
    Epoch [9150/10000], loss: 0.13226 acc: 0.98667 val_loss: 0.14158, val_acc: 0.96000
    Epoch [9160/10000], loss: 0.13220 acc: 0.98667 val_loss: 0.14153, val_acc: 0.96000
    Epoch [9170/10000], loss: 0.13213 acc: 0.98667 val_loss: 0.14147, val_acc: 0.96000
    Epoch [9180/10000], loss: 0.13206 acc: 0.98667 val_loss: 0.14141, val_acc: 0.96000
    Epoch [9190/10000], loss: 0.13200 acc: 0.98667 val_loss: 0.14136, val_acc: 0.96000
    Epoch [9200/10000], loss: 0.13193 acc: 0.98667 val_loss: 0.14130, val_acc: 0.96000
    Epoch [9210/10000], loss: 0.13187 acc: 0.98667 val_loss: 0.14125, val_acc: 0.96000
    Epoch [9220/10000], loss: 0.13180 acc: 0.98667 val_loss: 0.14119, val_acc: 0.96000
    Epoch [9230/10000], loss: 0.13174 acc: 0.98667 val_loss: 0.14114, val_acc: 0.96000
    Epoch [9240/10000], loss: 0.13167 acc: 0.98667 val_loss: 0.14108, val_acc: 0.96000
    Epoch [9250/10000], loss: 0.13160 acc: 0.98667 val_loss: 0.14103, val_acc: 0.96000
    Epoch [9260/10000], loss: 0.13154 acc: 0.98667 val_loss: 0.14097, val_acc: 0.96000
    Epoch [9270/10000], loss: 0.13147 acc: 0.98667 val_loss: 0.14092, val_acc: 0.96000
    Epoch [9280/10000], loss: 0.13141 acc: 0.98667 val_loss: 0.14086, val_acc: 0.96000
    Epoch [9290/10000], loss: 0.13135 acc: 0.98667 val_loss: 0.14081, val_acc: 0.96000
    Epoch [9300/10000], loss: 0.13128 acc: 0.98667 val_loss: 0.14075, val_acc: 0.96000
    Epoch [9310/10000], loss: 0.13122 acc: 0.98667 val_loss: 0.14070, val_acc: 0.96000
    Epoch [9320/10000], loss: 0.13115 acc: 0.98667 val_loss: 0.14065, val_acc: 0.96000
    Epoch [9330/10000], loss: 0.13109 acc: 0.98667 val_loss: 0.14059, val_acc: 0.96000
    Epoch [9340/10000], loss: 0.13102 acc: 0.98667 val_loss: 0.14054, val_acc: 0.96000
    Epoch [9350/10000], loss: 0.13096 acc: 0.98667 val_loss: 0.14048, val_acc: 0.96000
    Epoch [9360/10000], loss: 0.13090 acc: 0.98667 val_loss: 0.14043, val_acc: 0.96000
    Epoch [9370/10000], loss: 0.13083 acc: 0.98667 val_loss: 0.14038, val_acc: 0.96000
    Epoch [9380/10000], loss: 0.13077 acc: 0.98667 val_loss: 0.14032, val_acc: 0.96000
    Epoch [9390/10000], loss: 0.13070 acc: 0.98667 val_loss: 0.14027, val_acc: 0.96000
    Epoch [9400/10000], loss: 0.13064 acc: 0.98667 val_loss: 0.14022, val_acc: 0.96000
    Epoch [9410/10000], loss: 0.13058 acc: 0.98667 val_loss: 0.14016, val_acc: 0.96000
    Epoch [9420/10000], loss: 0.13051 acc: 0.98667 val_loss: 0.14011, val_acc: 0.96000
    Epoch [9430/10000], loss: 0.13045 acc: 0.98667 val_loss: 0.14006, val_acc: 0.96000
    Epoch [9440/10000], loss: 0.13039 acc: 0.98667 val_loss: 0.14000, val_acc: 0.96000
    Epoch [9450/10000], loss: 0.13033 acc: 0.98667 val_loss: 0.13995, val_acc: 0.96000
    Epoch [9460/10000], loss: 0.13026 acc: 0.98667 val_loss: 0.13990, val_acc: 0.96000
    Epoch [9470/10000], loss: 0.13020 acc: 0.98667 val_loss: 0.13984, val_acc: 0.96000
    Epoch [9480/10000], loss: 0.13014 acc: 0.98667 val_loss: 0.13979, val_acc: 0.96000
    Epoch [9490/10000], loss: 0.13008 acc: 0.98667 val_loss: 0.13974, val_acc: 0.96000
    Epoch [9500/10000], loss: 0.13001 acc: 0.98667 val_loss: 0.13969, val_acc: 0.96000
    Epoch [9510/10000], loss: 0.12995 acc: 0.98667 val_loss: 0.13963, val_acc: 0.96000
    Epoch [9520/10000], loss: 0.12989 acc: 0.98667 val_loss: 0.13958, val_acc: 0.96000
    Epoch [9530/10000], loss: 0.12983 acc: 0.98667 val_loss: 0.13953, val_acc: 0.96000
    Epoch [9540/10000], loss: 0.12976 acc: 0.98667 val_loss: 0.13948, val_acc: 0.96000
    Epoch [9550/10000], loss: 0.12970 acc: 0.98667 val_loss: 0.13943, val_acc: 0.96000
    Epoch [9560/10000], loss: 0.12964 acc: 0.98667 val_loss: 0.13937, val_acc: 0.96000
    Epoch [9570/10000], loss: 0.12958 acc: 0.98667 val_loss: 0.13932, val_acc: 0.96000
    Epoch [9580/10000], loss: 0.12952 acc: 0.98667 val_loss: 0.13927, val_acc: 0.96000
    Epoch [9590/10000], loss: 0.12946 acc: 0.98667 val_loss: 0.13922, val_acc: 0.96000
    Epoch [9600/10000], loss: 0.12940 acc: 0.98667 val_loss: 0.13917, val_acc: 0.96000
    Epoch [9610/10000], loss: 0.12933 acc: 0.98667 val_loss: 0.13912, val_acc: 0.96000
    Epoch [9620/10000], loss: 0.12927 acc: 0.98667 val_loss: 0.13907, val_acc: 0.96000
    Epoch [9630/10000], loss: 0.12921 acc: 0.98667 val_loss: 0.13901, val_acc: 0.96000
    Epoch [9640/10000], loss: 0.12915 acc: 0.98667 val_loss: 0.13896, val_acc: 0.96000
    Epoch [9650/10000], loss: 0.12909 acc: 0.98667 val_loss: 0.13891, val_acc: 0.96000
    Epoch [9660/10000], loss: 0.12903 acc: 0.98667 val_loss: 0.13886, val_acc: 0.96000
    Epoch [9670/10000], loss: 0.12897 acc: 0.98667 val_loss: 0.13881, val_acc: 0.96000
    Epoch [9680/10000], loss: 0.12891 acc: 0.98667 val_loss: 0.13876, val_acc: 0.96000
    Epoch [9690/10000], loss: 0.12885 acc: 0.98667 val_loss: 0.13871, val_acc: 0.96000
    Epoch [9700/10000], loss: 0.12879 acc: 0.98667 val_loss: 0.13866, val_acc: 0.96000
    Epoch [9710/10000], loss: 0.12873 acc: 0.98667 val_loss: 0.13861, val_acc: 0.96000
    Epoch [9720/10000], loss: 0.12867 acc: 0.98667 val_loss: 0.13856, val_acc: 0.96000
    Epoch [9730/10000], loss: 0.12861 acc: 0.98667 val_loss: 0.13851, val_acc: 0.96000
    Epoch [9740/10000], loss: 0.12855 acc: 0.98667 val_loss: 0.13846, val_acc: 0.96000
    Epoch [9750/10000], loss: 0.12849 acc: 0.98667 val_loss: 0.13841, val_acc: 0.96000
    Epoch [9760/10000], loss: 0.12843 acc: 0.98667 val_loss: 0.13836, val_acc: 0.96000
    Epoch [9770/10000], loss: 0.12837 acc: 0.98667 val_loss: 0.13831, val_acc: 0.96000
    Epoch [9780/10000], loss: 0.12831 acc: 0.98667 val_loss: 0.13826, val_acc: 0.96000
    Epoch [9790/10000], loss: 0.12825 acc: 0.98667 val_loss: 0.13821, val_acc: 0.96000
    Epoch [9800/10000], loss: 0.12819 acc: 0.98667 val_loss: 0.13816, val_acc: 0.96000
    Epoch [9810/10000], loss: 0.12813 acc: 0.98667 val_loss: 0.13811, val_acc: 0.96000
    Epoch [9820/10000], loss: 0.12808 acc: 0.98667 val_loss: 0.13806, val_acc: 0.96000
    Epoch [9830/10000], loss: 0.12802 acc: 0.98667 val_loss: 0.13801, val_acc: 0.96000
    Epoch [9840/10000], loss: 0.12796 acc: 0.98667 val_loss: 0.13796, val_acc: 0.96000
    Epoch [9850/10000], loss: 0.12790 acc: 0.98667 val_loss: 0.13791, val_acc: 0.96000
    Epoch [9860/10000], loss: 0.12784 acc: 0.98667 val_loss: 0.13786, val_acc: 0.96000
    Epoch [9870/10000], loss: 0.12778 acc: 0.98667 val_loss: 0.13782, val_acc: 0.96000
    Epoch [9880/10000], loss: 0.12772 acc: 0.98667 val_loss: 0.13777, val_acc: 0.96000
    Epoch [9890/10000], loss: 0.12767 acc: 0.98667 val_loss: 0.13772, val_acc: 0.96000
    Epoch [9900/10000], loss: 0.12761 acc: 0.98667 val_loss: 0.13767, val_acc: 0.96000
    Epoch [9910/10000], loss: 0.12755 acc: 0.98667 val_loss: 0.13762, val_acc: 0.96000
    Epoch [9920/10000], loss: 0.12749 acc: 0.98667 val_loss: 0.13757, val_acc: 0.96000
    Epoch [9930/10000], loss: 0.12743 acc: 0.98667 val_loss: 0.13752, val_acc: 0.96000
    Epoch [9940/10000], loss: 0.12738 acc: 0.98667 val_loss: 0.13748, val_acc: 0.96000
    Epoch [9950/10000], loss: 0.12732 acc: 0.98667 val_loss: 0.13743, val_acc: 0.96000
    Epoch [9960/10000], loss: 0.12726 acc: 0.98667 val_loss: 0.13738, val_acc: 0.96000
    Epoch [9970/10000], loss: 0.12720 acc: 0.98667 val_loss: 0.13733, val_acc: 0.96000
    Epoch [9980/10000], loss: 0.12715 acc: 0.98667 val_loss: 0.13728, val_acc: 0.96000
    Epoch [9990/10000], loss: 0.12709 acc: 0.98667 val_loss: 0.13724, val_acc: 0.96000



```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기상태 : 손실 : 1.09158  정확도 : 0.26667
    최종상태 : 손실 : 0.13724  정확도 : 0.96000



```python
# 패턴 3 모델의 출력값
w = outputs[:5,:].data.numpy()
print(w)
```

    [[0.0059 0.9056 0.0885]
     [0.0069 0.9792 0.0139]
     [0.9452 0.0548 0.    ]
     [0.     0.0404 0.9596]
     [0.0001 0.1743 0.8256]]



## 강의_3기_AI개론_10차시__MNIST_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_10차시__MNIST_.ipynb)

# 10장 MNIST를 활용한 숫자 인식

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
# 한글 폰트 설치

!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    debconf: unable to initialize frontend: Dialog
    debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 78, <> line 4.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Processing triggers for fontconfig (2.13.1-4.2ubuntu5) ...
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 39 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /usr/share/fonts/truetype: skipping, looped directory detected
    /usr/share/fonts/truetype/humor-sans: skipping, looped directory detected
    /usr/share/fonts/truetype/liberation: skipping, looped directory detected
    /usr/share/fonts/truetype/nanum: skipping, looped directory detected
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3
    Successfully installed torchinfo-1.8.0


* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 폰트 관련 용도
import matplotlib.font_manager as fm

# Colab, Linux
# 나눔 고딕 폰트의 경로 명시
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```


```python
# 파이토치 관련 라이브러리
import torch
from torch import nn, optim
import torch.nn.functional as F
from torchviz import make_dot
from torchinfo import summary
from tqdm.notebook import tqdm

import torchvision.transforms as transforms
import torchvision.datasets as datasets
```


```python
# 기본 폰트 설정
# 윈도우에서는 "malgun.ttf" 혹은 "NanumBarunGothic.ttf" 등을 사용할 수 있다. 맥에서는 "AppleGothic.ttf"
plt.rcParams['font.family'] = font_name

# 기본 폰트 사이즈 변경
plt.rcParams['font.size'] = 14

# 기본 그래프 사이즈 변경
plt.rcParams['figure.figsize'] = (6,6)

# 기본 그리드 표시
# 필요에 따라 설정할 때는, plt.grid()
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = ':'


# 마이너스 기호 정상 출력
plt.rcParams['axes.unicode_minus'] = False

# 넘파이 부동소수점 자릿수 표시
np.set_printoptions(suppress=True, precision=4)
```

## MNIST 숫자 인식

### 활성화 함수와 ReLU 함수


```python
# ReLU 함수의 그래프

relu = nn.ReLU()
x_np = np.arange(-2, 2.1, 0.25)
x = torch.tensor(x_np).float()
y = relu(x)

plt.plot(x.data, y.data)
plt.title('ReLU 함수')
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__10_0.webp)
    


### GPU 디바이스 확인


```python
# 디바이스 할당
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
```

    cpu



```python
# 텐서 변수 x, y
x_np = np.arange(-2.0, 2.1, 0.25)
y_np = np.arange(-1.0, 3.1, 0.25)
x = torch.tensor(x_np).float()
y = torch.tensor(y_np).float()

# x와 y 사이의 연산
z = x * y
print(z)
```

    tensor([ 2.0000,  1.3125,  0.7500,  0.3125, -0.0000, -0.1875, -0.2500, -0.1875,
             0.0000,  0.3125,  0.7500,  1.3125,  2.0000,  2.8125,  3.7500,  4.8125,
             6.0000])



```python
# 변수 x를 GPU로 보냄
x = x.to(device)

# 변수 x와 y의 디바이스 속성 확인
print('x: ', x.device)
print('y: ', y.device)
```

    x:  cpu
    y:  cpu



```python
# 이 상태에서 x와 y의 연산을 수행하면...

z = x * y
```


```python
# y도 GPU로 보냄
y = y.to(device)

# 연산이 가능해짐
z = x * y
print(z)
print("z.device = ", z.device)
```

    tensor([ 2.0000,  1.3125,  0.7500,  0.3125, -0.0000, -0.1875, -0.2500, -0.1875,
             0.0000,  0.3125,  0.7500,  1.3125,  2.0000,  2.8125,  3.7500,  4.8125,
             6.0000])
    z.device =  cpu


### MNIST Dataset을 활용해 불러오기


```python
# 라이브러리 임포트
import torchvision.datasets as datasets

# 다운로드받을 디렉터리명
data_root = './data'

train_set0 = datasets.MNIST(
    # 원본 데이터를 다운로드받을 디렉터리 지정
    root = data_root,
    # 훈련 데이터인지 또는 검증 데이터인지
    train = True,
    # 원본 데이터가 없는 경우, 다운로드를 실행하는지 여부
    download = True)
```

    Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz to ./data/MNIST/raw/train-images-idx3-ubyte.gz


    100%|██████████| 9.91M/9.91M [00:00<00:00, 91.8MB/s]

    Extracting ./data/MNIST/raw/train-images-idx3-ubyte.gz to ./data/MNIST/raw


    


    
    Downloading http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz to ./data/MNIST/raw/train-labels-idx1-ubyte.gz


    100%|██████████| 28.9k/28.9k [00:00<00:00, 35.9MB/s]


    Extracting ./data/MNIST/raw/train-labels-idx1-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw/t10k-images-idx3-ubyte.gz


    100%|██████████| 1.65M/1.65M [00:00<00:00, 63.8MB/s]


    Extracting ./data/MNIST/raw/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz


    100%|██████████| 4.54k/4.54k [00:00<00:00, 2.99MB/s]


    Extracting ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw
    



```python
# 다운로드한 파일 확인
# 리눅스 명령어
!ls -lR ./data/MNIST

# Window 명령어
# !dir /s data\MNIST
```

    ./data/MNIST:
    total 4
    drwxr-xr-x 2 root root 4096 Feb 10 03:14 raw
    
    ./data/MNIST/raw:
    total 65008
    -rw-r--r-- 1 root root  7840016 Feb 10 03:14 t10k-images-idx3-ubyte
    -rw-r--r-- 1 root root  1648877 Feb 10 03:14 t10k-images-idx3-ubyte.gz
    -rw-r--r-- 1 root root    10008 Feb 10 03:14 t10k-labels-idx1-ubyte
    -rw-r--r-- 1 root root     4542 Feb 10 03:14 t10k-labels-idx1-ubyte.gz
    -rw-r--r-- 1 root root 47040016 Feb 10 03:14 train-images-idx3-ubyte
    -rw-r--r-- 1 root root  9912422 Feb 10 03:14 train-images-idx3-ubyte.gz
    -rw-r--r-- 1 root root    60008 Feb 10 03:14 train-labels-idx1-ubyte
    -rw-r--r-- 1 root root    28881 Feb 10 03:14 train-labels-idx1-ubyte.gz



```python
# 데이터 건수 확인
print("train_set0 타입:", type(train_set0))
print("train_set0 : \n", train_set0)
print('데이터 건수: ', len(train_set0))


# 첫번째 요소 가져오기
image, label = train_set0[0]

# 데이터 타입 확인
print("="*50)
print('입력 데이터 타입 : ', type(image)) # <class 'PIL.Image.Image'>
print('정답 데이터 타입 : ', type(label)) # <class 'int'>

print("max = ", np.array(image).max())
print("min = ", np.array(image).min())

```

    train_set0 타입: <class 'torchvision.datasets.mnist.MNIST'>
    train_set0 : 
     Dataset MNIST
        Number of datapoints: 60000
        Root location: ./data
        Split: Train
    데이터 건수:  60000
    ==================================================
    입력 데이터 타입 :  <class 'PIL.Image.Image'>
    정답 데이터 타입 :  <class 'int'>
    max =  255
    min =  0



```python
# 입력 데이터를 이미지로 출력

plt.figure(figsize=(1,1))
plt.title(f'{label}')
plt.imshow(image, cmap='gray_r')
plt.axis('off')
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__21_0.webp)
    



```python
## plt.subplot

plt.figure(figsize=(4, 2))
plt.subplot(1,2,1), plt.imshow(image, cmap = 'gray_r')
plt.subplot(1,2,2), plt.imshow(image, cmap = 'gray_r')
plt.show()

```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__22_0.webp)
    



```python
# 정답 데이터와 함께 처음 20개 데이터를 이미지로 출력

plt.figure(figsize=(10, 3))
for i in range(20):
    ax = plt.subplot(2, 10, i + 1)

    # image와 label 취득
    image, label = train_set0[i]

    # 이미지 출력
    plt.imshow(image, cmap='gray_r')
    ax.set_title(f'{label}')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__23_0.webp)
    


### Transforms를 활용한 데이터 전처리


```python
# 라이브러리 임포트
# import torchvision.transforms as transforms

transform1 = transforms.Compose([
    # 데이터를 텐서로 변환
    transforms.ToTensor(),
])

train_set1 = datasets.MNIST(
    root=data_root,
    train=True,
    download=True,
    transform = transform1)
```


```python
# 변환 결과 확인

image, label = train_set1[0]
print('입력 데이터 타입 : ', type(image)) # <class 'torch.Tensor'>
print('입력 데이터 shape : ', image.shape)
print('최솟값 : ', image.data.min())
print('최댓값 : ', image.data.max())
```

    입력 데이터 타입 :  <class 'torch.Tensor'>
    입력 데이터 shape :  torch.Size([1, 28, 28])
    최솟값 :  tensor(0.)
    최댓값 :  tensor(1.)


### Normalize 사용 하기


```python
## 순서 중요
transform2 = transforms.Compose([
    # 데이터를 텐서로 변환
    transforms.ToTensor(),

    # 데이터 정규화
    transforms.Normalize(mean = 0.5,  std = 0.5), # z-transform
])

train_set2 = datasets.MNIST(
    root = data_root,
    train = True,
    download = True,
    transform = transform2)
```


```python
# 변환 결과 확인

image, label = train_set2[0]
print('shape : ', image.shape)
print('최솟값 : ', image.data.min())
print('최댓값 : ', image.data.max())
```

    shape :  torch.Size([1, 28, 28])
    최솟값 :  tensor(-1.)
    최댓값 :  tensor(1.)


### 람다 표현식을 활용한 함수 정의


```python
def f(x):
    return 1/np.exp(-10*x)


lambda x: 1/np.exp(-10*x)
```




    <function __main__.<lambda>(x)>




```python
# 일반적인 함수의 정의

def f(x):
    return (2 * x**2 + 2)

x = np.arange(-2, 2.1, 0.25)
y = f(x)
print(y)


# 람다 표현식으로 함수 정의
print("="*50)
g = lambda x: 2 * x**2 + 2

y = g(x)
print(y)
```

    [10.     8.125  6.5    5.125  4.     3.125  2.5    2.125  2.     2.125
      2.5    3.125  4.     5.125  6.5    8.125 10.   ]
    ==================================================
    [10.     8.125  6.5    5.125  4.     3.125  2.5    2.125  2.     2.125
      2.5    3.125  4.     5.125  6.5    8.125 10.   ]


### Lambda 클래스를 사용해 1차원으로 텐서 변환하기


```python
transform = transforms.Compose([
    # 데이터를 텐서로 변환
    transforms.ToTensor(),

    # 데이터 정규화
    transforms.Normalize(0.5, 0.5),

    # 현재 텐서를 1계 텐서로 변환
    transforms.Lambda(lambda x: x.view(-1))

])

train_set = datasets.MNIST(
    root = data_root,
    train = True,
    download=True,
    transform = transform)
```


```python
transform3 = transforms.Compose([
    # 데이터를 텐서로 변환
    transforms.ToTensor(),

    # 데이터 정규화
    transforms.Normalize(0.5, 0.5),

    # 현재 텐서를 1계 텐서로 변환
    transforms.Lambda(lambda x: x.view(-1)),
])

train_set3 = datasets.MNIST(
    root = data_root,
    train = True,
    download=True,
    transform = transform3)
```


```python
# 변환 결과 확인

image, label = train_set3[0]
print('shape : ', image.shape)
print('최솟값 : ', image.data.min())
print('최댓값 : ', image.data.max())
```

    shape :  torch.Size([784])
    최솟값 :  tensor(-1.)
    최댓값 :  tensor(1.)


### 최종 구현 형태


```python
# 데이터 변환용 함수 Transforms
# (1) Image를 텐서화
# (2) [0, 1] 범위의 값을 [-1, 1] 범위로 조정
# (3) 데이터의 shape을 [1, 28, 28] 에서 [784] 로 변환

transform = transforms.Compose([
    # (1) 데이터를 텐서로 변환
    transforms.ToTensor(),

    # (2) 데이터 정규화
    transforms.Normalize(0.5, 0.5),

    # (3) 1계 텐서로 변환
    transforms.Lambda(lambda x: x.view(-1)),
])
```


```python
# 데이터 입수를 위한 Dataset 함수

# 훈련용 데이터셋 정의
train_set = datasets.MNIST(
    root = data_root,
    train = True,
    download = True,
    transform = transform)

# 검증용 데이터셋 정의
test_set = datasets.MNIST(
    root = data_root,
    train = False,
    download = True,
    transform = transform)
```

### 데이터로더를 활용한 미니 배치 데이터 생성


```python
# 라이브러리 임포트
from torch.utils.data import DataLoader

# 미니 배치 사이즈 지정
batch_size = 500

# 훈련용 데이터로더
# 훈련용이므로, 셔플을 적용함
train_loader = DataLoader(
    dataset = train_set,
    batch_size = batch_size,
    shuffle = True)

# 검증용 데이터로더
# 검증시에는 셔플을 필요로하지 않음
test_loader = DataLoader(
    dataset = test_set,
    batch_size = batch_size,
    shuffle = False)
```


```python
# 몇 개의 그룹으로 데이터를 가져올 수 있는가
# images, labels = next(iter(train_loader))

print(len(train_loader))

# 데이터로더로부터 가장 처음 한 세트를 가져옴
for images, labels in train_loader:
    break

print(images.shape)
print(labels.shape)

# print("max value = ", images.max())
```

    120
    torch.Size([500, 784])
    torch.Size([500])



```python
# 이미지 출력
plt.figure(figsize=(10, 3))
# fig, axs = plt.subplots(2, 10, figsize = (10, 3))

for i in range(20):
    ax = plt.subplot(2, 10, i + 1)

    # row = i//10
    # col = i % 10

    # 넘파이로 배열로 변환
    image = images[i].numpy()
    label = labels[i]

    # 이미지의 범위를 [0, 1] 로 되돌림
    image2 = (image + 1)/ 2

    # 이미지 출력
    plt.imshow(image2.reshape(28, 28), cmap='gray_r')
    # ax.set_title(str(label.item()))
    ax.set_title(f'{label}')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # axs[row, col].imshow(image2.reshape(28, 28), cmap='gray_r')
    # axs[row, col].set_title(f'{label}')
    # axs[row, col].get_xaxis().set_visible(False)
    # axs[row, col].get_yaxis().set_visible(False)
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__43_0.webp)
    


### 모델 정의


```python
# 입력 차원수
n_input = image.shape[0]

# 출력 차원수
# 분류 클래스 수는 10
n_output = len(set(list(labels.data.numpy())))

# 은닉층의 노드 수
n_hidden = 128

# 결과 확인
print(f'n_input: {n_input}  n_hidden: {n_hidden} n_output: {n_output}')
```

    n_input: 784  n_hidden: 128 n_output: 10



```python
# 모델 정의
# 784입력 10출력 1은닉층의 신경망 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super().__init__()

        # 은닉층 정의(은닉층 노드 수 : n_hidden)
        self.l1 = nn.Linear(n_input, n_hidden)

        # 출력층 정의
        self.l2 = nn.Linear(n_hidden, n_output)

        # ReLU 함수 정의
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.relu(x1)
        x3 = self.l2(x2)
        return x3
```


```python
# 난수 고정
torch.manual_seed(123)
torch.cuda.manual_seed(123)
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms = True

# 모델 인스턴스 생성
net = Net(n_input, n_output, n_hidden)

# 모델을 GPU로 전송
net = net.to(device)
# next(net.parameters()).is_cuda
```


```python
# 학습률
lr = 0.01

# 최적화 알고리즘: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()
```


```python
# 모델 내부 파라미터 확인
# l1.weight, l1.bias, l2.weight, l2.bias를 확인할 수 있음

for parameter in net.named_parameters():
    print(parameter)

# list(net.named_parameters())[0][1].data.cpu().numpy()
```

    ('l1.weight', Parameter containing:
    tensor([[-0.0146,  0.0012, -0.0177,  ...,  0.0277,  0.0200,  0.0315],
            [ 0.0184, -0.0322,  0.0175,  ...,  0.0089, -0.0028, -0.0033],
            [ 0.0092,  0.0261,  0.0075,  ...,  0.0061,  0.0267, -0.0258],
            ...,
            [ 0.0235, -0.0026, -0.0129,  ...,  0.0322, -0.0059, -0.0169],
            [-0.0328, -0.0258,  0.0124,  ..., -0.0049,  0.0006,  0.0334],
            [ 0.0187, -0.0076, -0.0202,  ...,  0.0325, -0.0159, -0.0240]],
           requires_grad=True))
    ('l1.bias', Parameter containing:
    tensor([ 0.0325, -0.0298,  0.0013,  0.0199,  0.0268, -0.0248, -0.0172, -0.0355,
             0.0122, -0.0048,  0.0214,  0.0202, -0.0243,  0.0015, -0.0276,  0.0296,
             0.0341, -0.0228,  0.0230,  0.0347, -0.0091, -0.0346,  0.0206, -0.0060,
             0.0329,  0.0047,  0.0180,  0.0101,  0.0177, -0.0309,  0.0228, -0.0224,
             0.0321,  0.0179,  0.0321,  0.0184,  0.0219, -0.0089,  0.0310, -0.0039,
            -0.0074, -0.0317,  0.0192, -0.0021,  0.0190,  0.0038,  0.0334, -0.0027,
            -0.0127,  0.0229, -0.0265,  0.0023, -0.0162, -0.0134, -0.0027,  0.0212,
            -0.0205, -0.0144,  0.0121,  0.0001,  0.0086,  0.0033,  0.0123,  0.0213,
            -0.0177,  0.0247, -0.0109, -0.0222,  0.0228, -0.0110, -0.0074, -0.0089,
            -0.0205,  0.0323, -0.0207, -0.0205, -0.0028, -0.0341, -0.0304,  0.0144,
             0.0072,  0.0326, -0.0342, -0.0329, -0.0032, -0.0200, -0.0029, -0.0098,
             0.0220, -0.0160,  0.0099,  0.0033, -0.0289,  0.0110,  0.0199,  0.0131,
            -0.0279,  0.0122,  0.0237,  0.0126, -0.0055, -0.0088, -0.0057, -0.0048,
             0.0007, -0.0017, -0.0324,  0.0048, -0.0134,  0.0334,  0.0298, -0.0060,
             0.0263,  0.0113, -0.0113,  0.0150,  0.0091, -0.0311, -0.0079,  0.0002,
            -0.0282, -0.0016,  0.0304, -0.0237, -0.0157, -0.0255,  0.0006,  0.0100],
           requires_grad=True))
    ('l2.weight', Parameter containing:
    tensor([[ 0.0107,  0.0714,  0.0153,  ...,  0.0704,  0.0505, -0.0382],
            [-0.0066,  0.0348,  0.0143,  ..., -0.0039, -0.0141,  0.0130],
            [-0.0251, -0.0654,  0.0567,  ..., -0.0435,  0.0154,  0.0256],
            ...,
            [-0.0131,  0.0147, -0.0452,  ...,  0.0344, -0.0539,  0.0466],
            [ 0.0771, -0.0510,  0.0769,  ..., -0.0257, -0.0351,  0.0670],
            [ 0.0456,  0.0628, -0.0649,  ..., -0.0804,  0.0707,  0.0119]],
           requires_grad=True))
    ('l2.bias', Parameter containing:
    tensor([-0.0787, -0.0282, -0.0108,  0.0021, -0.0330, -0.0162, -0.0825,  0.0590,
             0.0566, -0.0631], requires_grad=True))



```python
# 모델 개요 표시 1

print(net)
```

    Net(
      (l1): Linear(in_features=784, out_features=128, bias=True)
      (l2): Linear(in_features=128, out_features=10, bias=True)
      (relu): ReLU(inplace=True)
    )



```python
# 모델 개요 표시 2

summary(net, (784,))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [10]                      --
    ├─Linear: 1-1                            [128]                     100,480
    ├─ReLU: 1-2                              [128]                     --
    ├─Linear: 1-3                            [10]                      1,290
    ==========================================================================================
    Total params: 101,770
    Trainable params: 101,770
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 12.87
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.41
    Estimated Total Size (MB): 0.41
    ==========================================================================================



### 경사 하강법


```python
# 훈련 데이터셋의 가장 처음 항목을 취득
# 데이터로더에서 가장 처음 항목을 취득
for images, labels in train_loader:
    break
```


```python
# 데이터로더에서 취득한 데이터를 GPU로 보냄
inputs = images.to(device)
labels = labels.to(device)
```


```python
# 예측 계산
outputs = net(inputs)

# 결과 확인
print(outputs)

```

    tensor([[-0.3622, -0.1927, -0.0179,  ...,  0.1073,  0.1025, -0.0615],
            [-0.4072, -0.1814,  0.0716,  ...,  0.1866,  0.1975,  0.1161],
            [-0.3221, -0.0547, -0.2868,  ...,  0.1967, -0.0103,  0.1591],
            ...,
            [-0.2091, -0.1058,  0.2365,  ...,  0.1360,  0.0665,  0.0987],
            [-0.2756, -0.2012,  0.1703,  ...,  0.1223,  0.2388,  0.0233],
            [-0.3045, -0.2458,  0.1416,  ...,  0.1012,  0.0820, -0.1457]],
           grad_fn=<AddmmBackward0>)



```python
#  손실 계산
loss = criterion(outputs, labels)

# 손실값 가져오기
print(loss)

# 손실 계산 그래프 시각화
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```

    tensor(2.3329, grad_fn=<NllLossBackward0>)



    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__56_1.svg)
    


### 경사 계산


```python
next(net.parameters()).is_cuda
```




    False




```python
# 경사 계산 실행
loss.backward()
```


```python
# 경사 계산 결과
w = net.to('cpu')
print(w.l1.weight.grad.numpy())
print(w.l1.bias.grad.numpy())
print(w.l2.weight.grad.numpy())
print(w.l2.bias.grad.numpy())
```

    [[-0.0007 -0.0007 -0.0007 ... -0.0007 -0.0007 -0.0007]
     [ 0.0077  0.0077  0.0077 ...  0.0077  0.0077  0.0077]
     [-0.0018 -0.0018 -0.0018 ... -0.0018 -0.0018 -0.0018]
     ...
     [-0.0008 -0.0008 -0.0008 ... -0.0008 -0.0008 -0.0008]
     [ 0.0011  0.0011  0.0011 ...  0.0011  0.0011  0.0011]
     [-0.0001 -0.0001 -0.0001 ... -0.0001 -0.0001 -0.0001]]
    [ 0.0007 -0.0077  0.0018  0.0008 -0.      0.      0.0014 -0.0008  0.0025
     -0.0016  0.0009 -0.002   0.0006  0.0025 -0.0026  0.0008  0.0061 -0.0011
     -0.0018  0.008   0.0063  0.0026 -0.0036  0.0056 -0.0006 -0.0038  0.0034
      0.     -0.0026 -0.0032 -0.0006  0.0034  0.0018  0.      0.0001  0.0002
      0.0047 -0.0012  0.0022  0.0018  0.0037 -0.0061  0.0011  0.0097 -0.0017
     -0.0012 -0.0004 -0.001  -0.0031 -0.0003 -0.0008  0.0004  0.0001 -0.0016
     -0.002  -0.0001 -0.0006 -0.0024 -0.0004  0.0029  0.0013 -0.0085  0.0013
      0.0015  0.     -0.0006  0.004  -0.0016 -0.0052  0.0003 -0.0031  0.0001
      0.0009 -0.0017 -0.0069 -0.0028  0.0017 -0.003   0.0012  0.0024  0.0011
     -0.002   0.0053 -0.0001  0.007   0.0024  0.003   0.0038 -0.0001 -0.0017
     -0.0006 -0.0021  0.0026  0.      0.0045  0.0037  0.0058 -0.0032 -0.
     -0.0003 -0.0006  0.      0.0029  0.0017  0.0022 -0.0034 -0.0001  0.0006
     -0.0015 -0.0035  0.0017 -0.0021 -0.0022  0.0013 -0.0002  0.0035 -0.0027
      0.0006 -0.002   0.002  -0.0036  0.0004  0.0006  0.0006 -0.0011  0.0008
     -0.0011  0.0001]
    [[-0.0198 -0.0018 -0.02   ... -0.0068 -0.0056 -0.0021]
     [ 0.0061 -0.0106  0.0044 ... -0.0123  0.0017  0.0009]
     [-0.0059  0.0061  0.0035 ...  0.002   0.0012 -0.0008]
     ...
     [ 0.0067 -0.0137  0.0041 ...  0.0053 -0.0006  0.0019]
     [-0.0066 -0.0007  0.0034 ...  0.0073 -0.0021 -0.0036]
     [ 0.0088  0.0024 -0.0002 ... -0.0002  0.0019  0.0012]]
    [-0.053  -0.033   0.0125 -0.005   0.0229  0.0163  0.0168  0.0102  0.0214
     -0.0091]


### 파라미터 수정


```python
# 경사 하강법 적용
optimizer.step()
```


```python
# 파라미터 값 출력
print(net.l1.weight)
print(net.l1.bias)
```

    Parameter containing:
    tensor([[-0.0146,  0.0012, -0.0177,  ...,  0.0278,  0.0200,  0.0316],
            [ 0.0183, -0.0322,  0.0174,  ...,  0.0088, -0.0029, -0.0034],
            [ 0.0092,  0.0261,  0.0075,  ...,  0.0061,  0.0267, -0.0258],
            ...,
            [ 0.0235, -0.0026, -0.0129,  ...,  0.0323, -0.0059, -0.0169],
            [-0.0329, -0.0258,  0.0124,  ..., -0.0049,  0.0006,  0.0334],
            [ 0.0187, -0.0076, -0.0202,  ...,  0.0325, -0.0159, -0.0240]],
           requires_grad=True)
    Parameter containing:
    tensor([ 3.2475e-02, -2.9682e-02,  1.2742e-03,  1.9874e-02,  2.6836e-02,
            -2.4759e-02, -1.7201e-02, -3.5517e-02,  1.2199e-02, -4.7449e-03,
             2.1379e-02,  2.0187e-02, -2.4297e-02,  1.4928e-03, -2.7613e-02,
             2.9618e-02,  3.4051e-02, -2.2777e-02,  2.2983e-02,  3.4580e-02,
            -9.1870e-03, -3.4619e-02,  2.0599e-02, -6.0632e-03,  3.2937e-02,
             4.7784e-03,  1.7949e-02,  1.0102e-02,  1.7700e-02, -3.0853e-02,
             2.2817e-02, -2.2391e-02,  3.2049e-02,  1.7890e-02,  3.2113e-02,
             1.8418e-02,  2.1852e-02, -8.8597e-03,  3.0939e-02, -3.9572e-03,
            -7.4435e-03, -3.1608e-02,  1.9150e-02, -2.2176e-03,  1.9040e-02,
             3.7815e-03,  3.3376e-02, -2.7366e-03, -1.2678e-02,  2.2926e-02,
            -2.6499e-02,  2.2708e-03, -1.6189e-02, -1.3415e-02, -2.7006e-03,
             2.1242e-02, -2.0511e-02, -1.4376e-02,  1.2089e-02,  9.8037e-05,
             8.5776e-03,  3.3507e-03,  1.2323e-02,  2.1314e-02, -1.7690e-02,
             2.4736e-02, -1.0986e-02, -2.2139e-02,  2.2898e-02, -1.1038e-02,
            -7.4188e-03, -8.9315e-03, -2.0528e-02,  3.2279e-02, -2.0665e-02,
            -2.0434e-02, -2.7932e-03, -3.4027e-02, -3.0392e-02,  1.4364e-02,
             7.1700e-03,  3.2612e-02, -3.4299e-02, -3.2920e-02, -3.2781e-03,
            -2.0019e-02, -2.9709e-03, -9.8261e-03,  2.1964e-02, -1.5987e-02,
             9.8720e-03,  3.2919e-03, -2.8945e-02,  1.0965e-02,  1.9866e-02,
             1.3074e-02, -2.7974e-02,  1.2213e-02,  2.3668e-02,  1.2602e-02,
            -5.4937e-03, -8.7514e-03, -5.7194e-03, -4.8619e-03,  6.6892e-04,
            -1.7088e-03, -3.2382e-02,  4.8306e-03, -1.3428e-02,  3.3444e-02,
             2.9813e-02, -5.9374e-03,  2.6309e-02,  1.1309e-02, -1.1252e-02,
             1.4970e-02,  9.1236e-03, -3.1057e-02, -7.8487e-03,  1.3641e-04,
            -2.8135e-02, -1.6511e-03,  3.0365e-02, -2.3754e-02, -1.5655e-02,
            -2.5556e-02,  6.5686e-04,  9.9645e-03], requires_grad=True)


### 반복 계산


```python
# 난수 고정
torch.manual_seed(123)
torch.cuda.manual_seed(123)


# 학습률
lr = 0.01

# 모델 초기화
net = Net(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
# num_epochs = 100
num_epochs = 10


# 평가 결과 기록
history = np.zeros((0,5))
```


```python
# tqdm 라이브러리 임포트
from tqdm.notebook import tqdm

# 반복 계산 메인 루프
for epoch in range(num_epochs):
    train_acc, train_loss = 0, 0
    val_acc, val_loss = 0, 0
    n_train, n_test = 0, 0

    # 훈련 페이즈
    for inputs, labels in tqdm(train_loader):
        n_train += len(labels)

        # GPU로 전송
        inputs = inputs.to(device)
        labels = labels.to(device)

        # 경사 초기화
        optimizer.zero_grad()

        # 예측 계산
        outputs = net(inputs)

        # 손실 계산
        loss = criterion(outputs, labels)

        # 경사 계산
        loss.backward()

        # 파라미터 수정
        optimizer.step()

        # 예측 라벨 산출
        predicted = torch.max(outputs, 1)[1]

        # 손실과 정확도 계산
        train_loss += loss.item()
        train_acc += (predicted == labels).sum().item()

    # 예측 페이즈
    for inputs_test, labels_test in test_loader:
        n_test += len(labels_test)

        inputs_test = inputs_test.to(device)
        labels_test = labels_test.to(device)


        # 예측 계산
        outputs_test = net(inputs_test)

        # 손실 계산
        loss_test = criterion(outputs_test, labels_test)

        # 예측 라벨 산출
        predicted_test = torch.max(outputs_test, 1)[1]

        # 손실과 정확도 계산
        val_loss +=  loss_test.item()
        val_acc +=  (predicted_test == labels_test).sum().item()

    # 평가 결과 산출, 기록
    train_acc = train_acc / n_train
    val_acc = val_acc / n_test
    train_loss = train_loss * batch_size / n_train
    val_loss = val_loss * batch_size / n_test
    print (f'Epoch [{epoch+1}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
    item = np.array([epoch+1 , train_loss, train_acc, val_loss, val_acc])
    history = np.vstack((history, item))
```


      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [1/10], loss: 1.82932 acc: 0.56960 val_loss: 1.32629, val_acc: 0.74660



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [2/10], loss: 1.03889 acc: 0.79537 val_loss: 0.79661, val_acc: 0.83180



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.70809 acc: 0.84110 val_loss: 0.60256, val_acc: 0.85850



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.57300 acc: 0.86057 val_loss: 0.51192, val_acc: 0.87140



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.50223 acc: 0.87102 val_loss: 0.45827, val_acc: 0.87930



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.45883 acc: 0.87877 val_loss: 0.42422, val_acc: 0.88650



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.42938 acc: 0.88327 val_loss: 0.40076, val_acc: 0.88970



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.40813 acc: 0.88743 val_loss: 0.38285, val_acc: 0.89370



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.39176 acc: 0.89065 val_loss: 0.36857, val_acc: 0.89680



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.37875 acc: 0.89313 val_loss: 0.35741, val_acc: 0.89930


### 결과 확인


```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )
```

    초기상태 : 손실 : 1.32629  정확도 : 0.74660
    최종상태 : 손실 : 0.35741  정확도 : 0.89930



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b', label='훈련')
plt.plot(history[:,0], history[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__69_0.webp)
    



```python
# 학습 곡선 출력(정확도)

plt.plot(history[:,0], history[:,2], 'b', label='훈련')
plt.plot(history[:,0], history[:,4], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__70_0.webp)
    


### 이미지 출력 확인


```python
# 데이터로더에서 처음 한 세트 가져오기
for images, labels in test_loader:
    break

# 예측 결과 가져오기
inputs = images.to(device)
labels = labels.to(device)
outputs = net(inputs)
predicted = torch.max(outputs, 1)[1]
```


```python
# 처음 50건의 이미지에 대해 "정답:예측"으로 출력

plt.figure(figsize=(10, 8))
for i in range(50):
  ax = plt.subplot(5, 10, i + 1)

  # 넘파이 배열로 변환
  image = images[i]
  label = labels[i]
  pred = predicted[i]
  if (pred == label):
    c = 'k'
  else:
    c = 'b'

  # 이미지의 범위를 [0, 1] 로 되돌림
  image2 = (image + 1)/ 2

  # 이미지 출력
  plt.imshow(image2.reshape(28, 28),cmap='gray_r')
  ax.set_title(f'{label}:{pred}', c=c)
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__73_0.webp)
    


### 은닉층 추가하기


```python
# 모델 정의
# 784입력 10출력을 갖는 2개의 은닉층을 포함한 신경망

class Net2(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super().__init__()

        # 첫번째 은닉층 정의(은닉층 노드 수: n_hidden)
        self.l1 = nn.Linear(n_input, n_hidden)

        # 두번째 은닉층 정의(은닉층 노드 수: n_hidden)
        self.l2 = nn.Linear(n_hidden, n_hidden)

        # 출력층 정의
        self.l3 = nn.Linear(n_hidden, n_output)

        # ReLU 함수 정의
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.relu(x1)
        x3 = self.l2(x2)
        x4 = self.relu(x3)
        x5 = self.l3(x4)
        return x5
```


```python
# 난수 고정
torch.manual_seed(123)
torch.cuda.manual_seed(123)

# 모델 초기화
net = Net2(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 함수: 경사 하강법
optimizer = torch.optim.SGD(net.parameters(), lr=lr)
```


```python
print(net)
```

    Net2(
      (l1): Linear(in_features=784, out_features=128, bias=True)
      (l2): Linear(in_features=128, out_features=128, bias=True)
      (l3): Linear(in_features=128, out_features=10, bias=True)
      (relu): ReLU(inplace=True)
    )



```python
# 모델 개요 표시 2

summary(net, (784,))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net2                                     [10]                      --
    ├─Linear: 1-1                            [128]                     100,480
    ├─ReLU: 1-2                              [128]                     --
    ├─Linear: 1-3                            [128]                     16,512
    ├─ReLU: 1-4                              [128]                     --
    ├─Linear: 1-5                            [10]                      1,290
    ==========================================================================================
    Total params: 118,282
    Trainable params: 118,282
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 14.99
    ==========================================================================================
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.00
    Params size (MB): 0.47
    Estimated Total Size (MB): 0.48
    ==========================================================================================




```python
# 데이터로더에서 처음 한 세트 가져오기
for images, labels in test_loader:
    break

# 예측 결과 가져오기
inputs = images.to(device)
labels = labels.to(device)
```


```python
# 예측 계산
outputs = net(inputs)

# 손실 계산
loss = criterion(outputs, labels)

# 손실 계산 그래프 시각화
make_dot(loss, params=dict(net.named_parameters()))
```




    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__80_0.svg)
    



### 경사 계산


```python
# 경사 계산
loss.backward()

# 경사 계산 결과 일부
w = net.to('cpu').l1.weight.grad.numpy()
print("w = ", w)

# 각 요소의 절댓값 평균
print(np.abs(w).mean())
```

    w =  [[-0.0007 -0.0007 -0.0007 ... -0.0007 -0.0007 -0.0007]
     [-0.0001 -0.0001 -0.0001 ... -0.0001 -0.0001 -0.0001]
     [-0.0005 -0.0005 -0.0005 ... -0.0005 -0.0005 -0.0005]
     ...
     [ 0.0015  0.0015  0.0015 ...  0.0015  0.0015  0.0015]
     [ 0.0002  0.0002  0.0002 ...  0.0002  0.0002  0.0002]
     [ 0.0003  0.0003  0.0003 ...  0.0003  0.0003  0.0003]]
    0.0008487979


### 반복 계산


```python
# 난수 고정
torch.manual_seed(123)
torch.cuda.manual_seed(123)


# 모델 초기화
net = Net2(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history2 = np.zeros((0,5))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):
    train_acc = 0
    train_loss = 0
    val_acc = 0
    val_loss = 0
    n_train = 0
    n_test = 0

    # 훈련 페이즈
    for inputs, labels in tqdm(train_loader):
        n_train += len(labels)

        # GPU로 전송
        inputs = inputs.to(device)
        labels = labels.to(device)

        # 경사 초기화
        optimizer.zero_grad()

        # 예측 계산
        outputs = net(inputs)

        # 손실 계산
        loss = criterion(outputs, labels)

        # 경사 계산
        loss.backward()

        # 파라미터 수정
        optimizer.step()

        # 예측 라벨 산출
        predicted = torch.max(outputs, 1)[1]

        # 손실과 정확도 계산
        train_loss += loss.item()
        train_acc += (predicted == labels).sum().item()

    # 예측 페이즈
    for inputs_test, labels_test in test_loader:
        n_test += len(labels_test)

        inputs_test = inputs_test.to(device)
        labels_test = labels_test.to(device)

        # 예측 계산
        outputs_test = net(inputs_test)

        # 손실 계산
        loss_test = criterion(outputs_test, labels_test)

        # 예측 라벨 산출
        predicted_test = torch.max(outputs_test, 1)[1]

        # 손실과 정확도 계산
        val_loss +=  loss_test.item()
        val_acc +=  (predicted_test == labels_test).sum().item()

    # 평가 결과 산출, 기록
    train_acc = train_acc / n_train
    val_acc = val_acc / n_test
    train_loss = train_loss * batch_size / n_train
    val_loss = val_loss * batch_size / n_test
    print (f'Epoch [{epoch+1}/{num_epochs}], loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {val_loss:.5f}, val_acc: {val_acc:.5f}')
    item = np.array([epoch+1 , train_loss, train_acc, val_loss, val_acc])
    history2 = np.vstack((history2, item))
```


      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [1/10], loss: 2.20163 acc: 0.25380 val_loss: 2.04576, val_acc: 0.49800



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [2/10], loss: 1.75820 acc: 0.60442 val_loss: 1.39272, val_acc: 0.68680



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [3/10], loss: 1.11285 acc: 0.75652 val_loss: 0.86511, val_acc: 0.80820



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.75171 acc: 0.82292 val_loss: 0.63478, val_acc: 0.84390



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.59030 acc: 0.84978 val_loss: 0.52463, val_acc: 0.86360



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.50672 acc: 0.86653 val_loss: 0.46401, val_acc: 0.87430



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.45680 acc: 0.87543 val_loss: 0.42149, val_acc: 0.88570



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.42336 acc: 0.88188 val_loss: 0.39552, val_acc: 0.89020



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.39965 acc: 0.88770 val_loss: 0.37600, val_acc: 0.89360



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.38195 acc: 0.89187 val_loss: 0.35886, val_acc: 0.89880



```python
# 손실과 정확도 확인

print(f'초기상태 : 손실 : {history2[0,3]:.5f}  정확도 : {history2[0,4]:.5f}' )
print(f'최종상태 : 손실 : {history2[-1,3]:.5f}  정확도 : {history2[-1,4]:.5f}' )
```

    초기상태 : 손실 : 2.04576  정확도 : 0.49800
    최종상태 : 손실 : 0.35886  정확도 : 0.89880



```python
# 학습 곡선 출력(손실)
plt.plot(history2[:,0], history2[:,1], 'b', label='훈련')
plt.plot(history2[:,0], history2[:,3], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__87_0.webp)
    



```python
# 학습 곡선 출력(정확도)

plt.plot(history2[:,0], history2[:,2], 'b', label='훈련')
plt.plot(history2[:,0], history2[:,4], 'k', label='검증')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__88_0.webp)
    


### 경사 소실과 ReLU 함수


```python
# 모델 정의 -　시그모이드 함수 버전
# 784입력 10출력을 갖는 2개의 은닉층을 포함한 신경망

class Net3(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super().__init__()

        # 첫번째 은닉층 정의(은닉층 노드 수: n_hidden)
        self.l1 = nn.Linear(n_input, n_hidden)

        # 두번째 은닉층 정의(은닉층 노드 수: n_hidden)
        self.l2 = nn.Linear(n_hidden, n_hidden)

        # 출력층 정의
        self.l3 = nn.Linear(n_hidden, n_output)

        # 시그모이드 함수 정의
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.sigmoid(x1)
        x3 = self.l2(x2)
        x4 = self.sigmoid(x3)
        x5 = self.l3(x4)
        return x5
```


```python
# 난수 고정
torch.manual_seed(123)
torch.cuda.manual_seed(123)

# 모델 초기화
net = Net3(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 최적화 함수: 경사 하강법
optimizer = torch.optim.SGD(net.parameters(), lr=lr)
```


```python
# 데이터로더에서 처음 한 세트 가져오기
for images, labels in test_loader:
    break

# 예측 결과 가져오기
inputs = images.to(device)
labels = labels.to(device)
```


```python
# 예측 계산
outputs = net(inputs)

# 손실 계산
loss = criterion(outputs, labels)

# 손실 계산 그래프 시각화
make_dot(loss, params=dict(net.named_parameters()))
```




    
![svg](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__93_0.svg)
    




```python
# 경사 계산
loss.backward()

# 경사 계산 결과의 일부
w = net.to('cpu').l1.weight.grad.numpy()
print(w)

# 각 요소의 절댓값 평균
print(np.abs(w).mean())
```

    [[ 0.0001  0.0001  0.0001 ...  0.0001  0.0001  0.0001]
     [ 0.0001  0.0001  0.0001 ...  0.0001  0.0001  0.0001]
     [-0.0001 -0.0001 -0.0001 ... -0.0001 -0.0001 -0.0001]
     ...
     [-0.0001 -0.0001 -0.0001 ... -0.0001 -0.0001 -0.0001]
     [ 0.0002  0.0002  0.0002 ...  0.0002  0.0002  0.0002]
     [-0.0001 -0.0001 -0.0001 ... -0.0001 -0.0001 -0.0001]]
    0.00017514593


### 배치 사이즈와 정확도의 관계


```python
# 학습용 함수
def fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history):
    base_epochs = len(history)
    batch_size_train = len(train_loader)
    batch_size_test = len(test_loader)


    for epoch in range(base_epochs, num_epochs+base_epochs):
        train_loss = 0
        train_acc = 0
        val_loss = 0
        val_acc = 0

        # 훈련 페이즈
        # count = 0

        for inputs, labels in tqdm(train_loader):

            # count += len(labels)
            inputs = inputs.to(device)
            labels = labels.to(device)

            # 경사 초기화
            optimizer.zero_grad()

            # 예측 계산
            outputs = net(inputs)

            # 손실 계산
            loss = criterion(outputs, labels)
            train_loss += loss.item()

            # 경사 계산
            loss.backward()

            # 파라미터 수정
            optimizer.step()

            # 예측 라벨 산출
            predicted = torch.max(outputs, 1)[1]

            # 정답 건수 산출
            train_acc += (predicted == labels).sum().item() /len(labels)

            # 훈련 데이터에 대해 손실과 정확도 계산
        avg_train_loss = train_loss / batch_size_train
        avg_train_acc = train_acc / batch_size_train

        # 예측 페이즈
        # count = 0

        for inputs, labels in test_loader:
            # count += len(labels)

            inputs = inputs.to(device)
            labels = labels.to(device)

            # 예측 계산
            outputs = net(inputs)

            # 손실 계산
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            # 예측 라벨 산출
            predicted = torch.max(outputs, 1)[1]

            # 정답 건수 산출
            val_acc += (predicted == labels).sum().item() /len(labels)

            # 검증 데이터에 대해 손실과 정확도 계산
        avg_val_loss = val_loss / batch_size_test
        avg_val_acc = val_acc / batch_size_test

        print (f'Epoch [{(epoch+1)}/{num_epochs+base_epochs}], loss: {avg_train_loss:.5f} acc: {avg_train_acc:.5f} val_loss: {avg_val_loss:.5f}, val_acc: {avg_val_acc:.5f}')
        item = np.array([epoch+1, avg_train_loss, avg_train_acc, avg_val_loss, avg_val_acc])
        history = np.vstack((history, item))
    return history
```


```python
# 파이토치 난수 고정

def torch_seed(seed=123):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # torch.backends.cudnn.deterministic = True
    # torch.use_deterministic_algorithms(True)
```

### Batch size  500


```python
# 미니 배치 사이즈 지정
batch_size_train = 500

# 훈련용 데이터로더
# 훈련용이므로 셔플을 적용함
train_loader = DataLoader(
    train_set,
    batch_size = batch_size_train,
    shuffle = True)

# 난수 고정
torch_seed()

# 학습률
lr = 0.01

# 모델 초기화
net = Net(n_input, n_output, n_hidden).to(device)

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history = np.zeros((0,5))
```


```python
history = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history)
```


      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [1/10], loss: 1.82932 acc: 0.56960 val_loss: 1.32629, val_acc: 0.74660



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [2/10], loss: 1.03889 acc: 0.79537 val_loss: 0.79661, val_acc: 0.83180



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.70809 acc: 0.84110 val_loss: 0.60256, val_acc: 0.85850



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.57300 acc: 0.86057 val_loss: 0.51192, val_acc: 0.87140



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.50223 acc: 0.87102 val_loss: 0.45827, val_acc: 0.87930



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.45883 acc: 0.87877 val_loss: 0.42422, val_acc: 0.88650



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.42938 acc: 0.88327 val_loss: 0.40076, val_acc: 0.88970



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.40813 acc: 0.88743 val_loss: 0.38285, val_acc: 0.89370



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.39176 acc: 0.89065 val_loss: 0.36857, val_acc: 0.89680



      0%|          | 0/120 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.37875 acc: 0.89313 val_loss: 0.35741, val_acc: 0.89930


### batch_size=200


```python
# 미니 배치 사이즈 지정
batch_size_train = 200

# 훈련용 데이터로더
# 훈련용이므로 셔플을 적용함
train_loader = DataLoader(
    train_set, batch_size = batch_size_train,
    shuffle = True)

# 난수 고정
torch_seed()

# 학습률
lr = 0.01

# 모델 초기화
net = Net(n_input, n_output, n_hidden).to(device)

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history3 = np.zeros((0,5))
```


```python
history3 = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history3)
```


      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [1/10], loss: 1.30017 acc: 0.71105 val_loss: 0.68051, val_acc: 0.84730



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [2/10], loss: 0.56331 acc: 0.86208 val_loss: 0.45811, val_acc: 0.87970



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.43948 acc: 0.88183 val_loss: 0.39073, val_acc: 0.89210



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.39051 acc: 0.89073 val_loss: 0.36061, val_acc: 0.89740



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.36304 acc: 0.89678 val_loss: 0.33796, val_acc: 0.90370



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.34487 acc: 0.90107 val_loss: 0.32460, val_acc: 0.90620



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.33107 acc: 0.90442 val_loss: 0.31342, val_acc: 0.91130



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.32004 acc: 0.90785 val_loss: 0.30469, val_acc: 0.91430



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.31084 acc: 0.91033 val_loss: 0.29686, val_acc: 0.91330



      0%|          | 0/300 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.30229 acc: 0.91278 val_loss: 0.28928, val_acc: 0.91760


### batch_size=100


```python
# 미니 배치 사이즈 지정
batch_size_train = 100

# 훈련용 데이터로더
# 훈련용이므로 셔플을 적용함
train_loader = DataLoader(
    train_set, batch_size = batch_size_train,
    shuffle = True)

# 난수 고정
torch_seed()

# 학습률
lr = 0.01

# 모델 초기화
net = Net(n_input, n_output, n_hidden).to(device)

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history4 = np.zeros((0,5))
```


```python
history4 = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history4)
```


      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [1/10], loss: 0.93449 acc: 0.78320 val_loss: 0.46005, val_acc: 0.87920



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [2/10], loss: 0.41716 acc: 0.88513 val_loss: 0.35982, val_acc: 0.89870



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.35608 acc: 0.89830 val_loss: 0.32409, val_acc: 0.90800



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.32769 acc: 0.90545 val_loss: 0.30662, val_acc: 0.91020



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.30828 acc: 0.91092 val_loss: 0.29081, val_acc: 0.91770



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.29329 acc: 0.91597 val_loss: 0.28169, val_acc: 0.91810



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.28022 acc: 0.91935 val_loss: 0.26869, val_acc: 0.92430



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.26842 acc: 0.92298 val_loss: 0.25890, val_acc: 0.92690



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.25724 acc: 0.92583 val_loss: 0.25020, val_acc: 0.92730



      0%|          | 0/600 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.24618 acc: 0.92952 val_loss: 0.23854, val_acc: 0.93200


### batch_size=50


```python
# 미니 배치 사이즈 지정
batch_size_train = 50

# 훈련용 데이터로더
# 훈련용이므로 셔플을 적용함
train_loader = DataLoader(
    train_set, batch_size = batch_size_train,
    shuffle = True)

# 난수 고정
torch_seed()

# 학습률
lr = 0.01

# 모델 초기화
net = Net(n_input, n_output, n_hidden).to(device)

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history5 = np.zeros((0,5))
```


```python
history5 = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history5)
```


      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [1/10], loss: 0.68133 acc: 0.82922 val_loss: 0.36122, val_acc: 0.89640



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [2/10], loss: 0.34658 acc: 0.89972 val_loss: 0.31089, val_acc: 0.91170



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.30507 acc: 0.91165 val_loss: 0.28181, val_acc: 0.91760



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.27770 acc: 0.91998 val_loss: 0.26108, val_acc: 0.92370



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.25497 acc: 0.92593 val_loss: 0.24184, val_acc: 0.93190



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.23419 acc: 0.93302 val_loss: 0.22800, val_acc: 0.93360



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.21595 acc: 0.93800 val_loss: 0.20686, val_acc: 0.94190



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.19983 acc: 0.94313 val_loss: 0.19247, val_acc: 0.94300



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.18607 acc: 0.94723 val_loss: 0.18570, val_acc: 0.94650



      0%|          | 0/1200 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.17366 acc: 0.95130 val_loss: 0.17183, val_acc: 0.94890



```python
# 학습 곡선 출력(정확도)

plt.plot(history[:,0], history[:,4], label='batch_size=500', c='k', linestyle='-.')
plt.plot(history3[:,0], history3[:,4], label='batch_size=200', c='b', linestyle='-.')
plt.plot(history4[:,0], history4[:,4], label='batch_size=100', c='k')
plt.plot(history5[:,0], history5[:,4], label='batch_size=50', c='b')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.title('학습 곡선(정확도)')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/deep-learning/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_10%EC%B0%A8%EC%8B%9C__MNIST__110_0.webp)
    

