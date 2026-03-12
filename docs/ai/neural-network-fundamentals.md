# 신경망 기초


## 강의_3기_AI개론_4차시__Perceptron_BP_ActivationF_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_4차시__Perceptron_BP_ActivationF_.ipynb)

# 4장 인공지능 개론

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
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3


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

## 퍼셉트론 (Perceptron)


```python
import torch
from torch import nn
import torch.nn.functional as F
```

### 선형 퍼셉트론 구현


```python
## 선형 퍼셉트론 구현

def perceptron(x, w, b = 0):
    if not isinstance(x, np.ndarray) or not isinstance(x, np.ndarray):
        x = np.array(x)
        w = np.array(w)
    y = np.sum(x*w) + b
    return y

x = [1, 2, 3]
w = [1, 2, 3]
# x = np.array([1, 2, 3])
# w = np.array([1, 2, 3])

y = perceptron(x, w)
print("result =", y)
```

    result = 14



```python
## 선형 퍼셉트론 구현: 랜텀 initial weights

def perceptron(x):
    w = np.random.rand(len(x))
    b = np.random.rand()
    y = np.sum(x*w) + b
    return y, w, b

x = np.array([1, 2, 3])
w = np.array([1, 2, 3])

y, w, b = perceptron(x)
print("result =", y.round(3))
print("weight = ", w)
print("b = ", round(b, 3))

```

    result = 3.872
    weight =  [0.6354 0.9663 0.1028]
    b =  0.996


### Pytorch 를 이용한 perceptron


```python
## Pytorch 를 이용한 perceptron
# torch.manual_seed(0)

input_size = 10
output_size = 1
y = nn.Linear(input_size, output_size)

print("weights = \n", y.weight)
print("bias = \n", y.bias)
print("="*50)

# 난수 생성
x = torch.rand(input_size)
print("x input = \n", x)
print("output = ", y(x))
```

    weights = 
     Parameter containing:
    tensor([[-0.2100, -0.1679, -0.2891,  0.2916,  0.1475,  0.0402, -0.2919, -0.1315,
             -0.0679,  0.0026]], requires_grad=True)
    bias = 
     Parameter containing:
    tensor([-0.0885], requires_grad=True)
    ==================================================
    x input = 
     tensor([0.6266, 0.7196, 0.6680, 0.5833, 0.0691, 0.9878, 0.5864, 0.4230, 0.2783,
            0.4751])
    output =  tensor([-0.5584], grad_fn=<ViewBackward0>)


## 오류 순전파 (Forward propagation)


```python
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sse(y, x):
    return (y-x)**2

def perceptron(x, w, b = 0):
    if not isinstance(x, np.ndarray) or not isinstance(x, np.ndarray):
        x = np.array(x)
        w = np.array(w)
    y = np.sum(x*w) + b
    return y
```

## 활성화 함수 (Activation function)


```python
## 시그모이드 (sigmoid)
def activation_plot(x, y, title:str):
    plt.plot(x, y)
    plt.title(title)
    # plt.grid(linestyle = ":")
    plt.show()
```


```python
# numpy
x = np.linspace(-5, 5, 100)
def sigmoid(x):
    y = 1/(1 + np.exp(-x))
    return y
y = sigmoid(x)

# torch class
# torch_simoid = nn.Sigmoid()
# y = torch_simoid(torch.tensor(x))
# y = F.sigmoid(torch.tensor(x))

activation_plot(x, y, "Sigmoid")
```

    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__18_1.webp)
    



```python
## Tanh (Hyperbolic Tangent)
def tanh(x):
    y = np.tanh(x)
        # y = (np.exp(x) - np.exp(-x))/ (np.exp(x) + np.exp(-x))
    return y
y = tanh(x)

# torch
torch_tanh = nn.Tanh()
y = torch_tanh(torch.tensor(x))
y = F.tanh(torch.tensor(x))

activation_plot(x, y, "Tanh")
```

    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__19_1.webp)
    



```python
## ReLU (Rectified Linear Unit)
def relu(x):
    y = np.maximum(0, x)
    return y

# torch
# torch_relu = nn.ReLU()
# y = torch_relu(torch.tensor(x))
# y = F.relu(torch.tensor(x))

# y = relu(x)
activation_plot(x, y, "ReLU")
```

    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__20_1.webp)
    



```python
## Leaky ReLU
def leakyRelu(x, alpha:float):
    y = np.maximum(alpha*x, x)
    return y
y = leakyRelu(x, 0.1)

# torch
# torch_lrelu = nn.LeakyReLU(0.1)
# y = torch_lrelu(torch.tensor(x))
# y = F.leaky_relu(torch.tensor(x), 0.1)


activation_plot(x, y, "Leaky ReLU")
```

    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__21_1.webp)
    



```python
## Exponential ReLU
def eRelu(x, alpha):
    y = (x>0)*x + (x <= 0)*(alpha*(np.exp(x) - 1))
    return y

y = eRelu(x, 1.)

# torch
# torch_lrelu = nn.GELU(0.1)
# y = torch_lrelu(torch.tensor(x))
# y = F.leaky_relu(torch.tensor(x), 0.1)

activation_plot(x, y, "Exponential ReLU")
```

    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.
    WARNING:matplotlib.font_manager:findfont: Font family 'NanumGothic' not found.



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_4%EC%B0%A8%EC%8B%9C__Perceptron_BP_ActivationF__22_1.webp)
    



## 강의_3기_AI개론_5차시__GD_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_5차시__GD_.ipynb)

# 5장 인공지능 학습

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
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3


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
# path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
# font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```


```python
# 파이토치 관련 라이브러리
import torch
from torchviz import make_dot
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

## 경사 하강법  (Gradient descent, GD) 구현

### GD 3D plot


```python
def L(u, v):
    return 3 * u**2 + 3 * v**2 - u*v + 7*u - 7*v + 10
def Lu(u, v):
    return 6* u - v + 7
def Lv(u, v):
    return 6* v - u - 7

u = np.linspace(-5, 5, 501)
v = np.linspace(-5, 5, 501)
U, V = np.meshgrid(u, v)
Z = L(U, V)
```


```python
# 경사 하강법 시뮬레이션
W = np.array([4.0, 4.0])
W1 = [W[0]]
W2 = [W[1]]
N = 21
alpha = 0.05
for i in range(N):
    W = W - alpha *np.array([Lu(W[0], W[1]), Lv(W[0], W[1])])
    W1.append(W[0])
    W2.append(W[1])
```


```python
n_loop=11

WW1 = np.array(W1[:n_loop])
WW2 = np.array(W2[:n_loop])
ZZ = L(WW1, WW2)
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax.set_zlim(0,250)
ax.set_xlabel('W')
ax.set_ylabel('B')
ax.set_zlabel('loss')
ax.view_init(30, 240)
ax.xaxis._axinfo["grid"]['linewidth'] = 2.
ax.yaxis._axinfo["grid"]['linewidth'] = 2.
ax.zaxis._axinfo["grid"]['linewidth'] = 2.
ax.contour3D(U, V, Z, 100, cmap='Blues', alpha=0.7)
ax.plot3D(WW1, WW2, ZZ, 'o-', c='r', alpha=1, markersize=7)
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__13_0.webp)
    


### 데이터 전처리
다섯명의 신장과 체중 데이터를 사용한다.  
1차 함수를 사용해 신장으로 체중을 예측하는 경우, 최적 직선을 구하는 것이 목적이다.


```python
# 샘플 데이터 선언
sampleData1 = np.array([
    [166, 58.7],
    [176.0, 75.7],
    [171.0, 62.1],
    [173.0, 70.4],
    [169.0,60.1]
])
print(sampleData1)
```

    [[166.   58.7]
     [176.   75.7]
     [171.   62.1]
     [173.   70.4]
     [169.   60.1]]



```python
# 머신러닝 모델에서 사용하기 위해, 신장을 변수 x로,
# 체중을 변수 y로 함

x = sampleData1[:,0]
y = sampleData1[:,1]
```


```python
# 산포도 출력 확인

plt.scatter(x,  y,  c='k',  s=50)
# plt.plot([166, 176], [60, 75], 'r:')
plt.xlabel('$x$: 신장 (cm) ')
plt.ylabel('$y$: 체중 (kg)')
plt.title('신장과 체중의 관계')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__17_0.webp)
    


### 데이터 변환
머신러닝 모델에서 데이터는 0에 가까운 값을 갖는 것이 바람직하다.
따라서, x, y 모두 평균값이 0이 되도록 평행이동시켜서 새로운 좌표계를 X, Y로 한다.


```python
X = x - x.mean()
Y = y - y.mean()
```


```python
# 산포도를 통해 결과 확인

plt.scatter(X,  Y,  c='k',  s=50)
plt.xlabel('$X$')
plt.ylabel('$Y$')
plt.title('데이터 가공 후 신장과 체중의 관계')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__20_0.webp)
    


### 예측 계산


```python
# X와 Y를 텐서 변수로 변환

X = torch.tensor(X).float()
Y = torch.tensor(Y).float()

# 결과 확인

print(X)
print(Y)
```

    tensor([-5.,  5.,  0.,  2., -2.])
    tensor([-6.7000, 10.3000, -3.3000,  5.0000, -5.3000])



```python
# 파라미터 정의
# W와 B는 경사 계산을 위해, requires_grad=True 로 설정함

W = torch.tensor(1.0, requires_grad=True).float()
B = torch.tensor(1.0, requires_grad=True).float()
```


```python
# 예측 함수는 1차 함수

def pred(X):
    return W * X + B
```


```python
# 예측 값 계산

Yp =  pred(X)

# 결과 확인

print(Yp)
```

    tensor([-4.,  6.,  1.,  3., -1.], grad_fn=<AddBackward0>)



```python
# 예측 값의 계산 그래프 표시

params = {'W': W, 'B': B}
g = make_dot(Yp, params=params)
display(g)
```


    
![svg](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__26_0.svg)
    


### 손실 계산


```python
# 평균 제곱 오차 손실함수

def mse(Yp, Y):
    loss = ((Yp - Y) ** 2).mean()
    return loss
```


```python
# 손실 계산

loss = mse(Yp, Y)

# 결과 표시

print(loss)
```

    tensor(13.3520, grad_fn=<MeanBackward0>)



```python
# 손실 계산 그래프 출력

params = {'W': W, 'B': B}
g = make_dot(loss, params=params)
display(g)
```


    
![svg](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__30_0.svg)
    


### 경사 계산


```python
# 경사 계산

loss.backward()
# loss.backward(retain_graph=True)

```


```python
# 경삿값 확인

print(W.grad)
print(B.grad)
```

    tensor(-19.0400)
    tensor(2.0000)


### 파라미터 수정


```python
# 학습률 정의

lr = 0.001
```

W와 B는 한번 계산이 끝났기 때문에, 이 상태로 값의 갱신은 불가능하다.
따라서, 다음과 같이 수정해야 한다.


```python
#  경사를 기반으로 파라미터 수정

# W -= lr * W.grad
# B -= lr * B.grad ## Error

with torch.no_grad():
    W -= lr * W.grad
    B -= lr * B.grad

    # 계산이 끝난 경삿값을 초기화함
    W.grad.zero_()
    B.grad.zero_()

```


```python
# 파라미터 경삿값 확인

print(W)
print(B)
print(W.grad)
print(B.grad)
```

    tensor(1.0190, requires_grad=True)
    tensor(0.9980, requires_grad=True)
    tensor(0.)
    tensor(0.)


### 반복 계산


```python
# 초기화

# W와 B를 변수로 사용
W = torch.tensor(1.0, requires_grad=True).float()
B = torch.tensor(1.0, requires_grad=True).float()

# 반복 횟수
num_epochs = 500

# 학습률
lr = 0.001

# history 기록을 위한 배열 초기화
history = np.zeros((0, 2))
```


```python
# 루프 처리

for epoch in range(num_epochs):

    # 예측 계산
    Yp = pred(X)

    # 손실 계산
    loss = mse(Yp, Y)

    # 경사 계산
    loss.backward()

    with torch.no_grad():
        # 파라미터 수정
        W -= lr * W.grad
        B -= lr * B.grad

        # 경삿값 초기화
        W.grad.zero_()
        B.grad.zero_()

    # 손실 기록
    if (epoch %10 == 0):
        item = np.array([epoch, loss.item()])
        history = np.vstack((history, item))
        print(f'epoch = {epoch}  loss = {loss:.4f}')
```

    epoch = 0  loss = 13.3520
    epoch = 10  loss = 10.3855
    epoch = 20  loss = 8.5173
    epoch = 30  loss = 7.3364
    epoch = 40  loss = 6.5858
    epoch = 50  loss = 6.1047
    epoch = 60  loss = 5.7927
    epoch = 70  loss = 5.5868
    epoch = 80  loss = 5.4476
    epoch = 90  loss = 5.3507
    epoch = 100  loss = 5.2805
    epoch = 110  loss = 5.2275
    epoch = 120  loss = 5.1855
    epoch = 130  loss = 5.1507
    epoch = 140  loss = 5.1208
    epoch = 150  loss = 5.0943
    epoch = 160  loss = 5.0703
    epoch = 170  loss = 5.0480
    epoch = 180  loss = 5.0271
    epoch = 190  loss = 5.0074
    epoch = 200  loss = 4.9887
    epoch = 210  loss = 4.9708
    epoch = 220  loss = 4.9537
    epoch = 230  loss = 4.9373
    epoch = 240  loss = 4.9217
    epoch = 250  loss = 4.9066
    epoch = 260  loss = 4.8922
    epoch = 270  loss = 4.8783
    epoch = 280  loss = 4.8650
    epoch = 290  loss = 4.8522
    epoch = 300  loss = 4.8399
    epoch = 310  loss = 4.8281
    epoch = 320  loss = 4.8167
    epoch = 330  loss = 4.8058
    epoch = 340  loss = 4.7953
    epoch = 350  loss = 4.7853
    epoch = 360  loss = 4.7756
    epoch = 370  loss = 4.7663
    epoch = 380  loss = 4.7574
    epoch = 390  loss = 4.7488
    epoch = 400  loss = 4.7406
    epoch = 410  loss = 4.7327
    epoch = 420  loss = 4.7251
    epoch = 430  loss = 4.7178
    epoch = 440  loss = 4.7108
    epoch = 450  loss = 4.7040
    epoch = 460  loss = 4.6976
    epoch = 470  loss = 4.6913
    epoch = 480  loss = 4.6854
    epoch = 490  loss = 4.6796


### 결과 평가


```python
# 최종 파라미터 값
print('W = ', W.data.numpy())
print('B = ', B.data.numpy())

# 손실 확인
print(f'초기상태 : 손실:{history[0,1]:.4f}')
print(f'최종상태 : 손실:{history[-1,1]:.4f}')
```

    W =  1.820683
    B =  0.3675114
    초기상태 : 손실:13.3520
    최종상태 : 손실:4.6796



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__44_0.webp)
    


### 산포도에 회귀 직선을 동시에 출력함


```python
# x의 범위를 구함(Xrange)
X_max = X.max()
X_min = X.min()
X_range = np.array((X_min, X_max))
X_range = torch.from_numpy(X_range).float()
print(X_range)

# 이와 대응하는 예측값 y를 구함
Y_range = pred(X_range)
print(Y_range.data)
```

    tensor([-5.,  5.])
    tensor([-8.7359,  9.4709])



```python
# 그래프 출력

plt.scatter(X,  Y,  c='k',  s=50)
plt.xlabel('$X$')
plt.ylabel('$Y$')
plt.plot(X_range.data, Y_range.data, lw=2, c='b')
plt.title('신장과 체중의 상관 직선(가공 후)')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__47_0.webp)
    


### 가공 전 데이터로 회귀 직선 출력


```python
# y좌표와 x좌표 값 계산

x_range = X_range + x.mean()
yp_range = Y_range + y.mean()
```


```python
# 그래프 출력

plt.scatter(x,  y,  c='k',  s=50)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.plot(x_range, yp_range.data, lw=2, c='b')
plt.title('신장과 체중의 상관 직선(가공 전)')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__50_0.webp)
    


### 최적화 함수와 step 함수 이용하기


```python
# 초기화

# W와 B를 변수로 사용
W = torch.tensor(1.0, requires_grad=True).float()
B = torch.tensor(1.0, requires_grad=True).float()

# 반복 횟수
num_epochs = 500

# 학습률
lr = 0.001

# optimizer 로 SGD(확률적 경사 하강법)을 사용
import torch.optim as optim
optimizer = optim.SGD([W, B], lr=lr)

# history 기록을 위한 배열 초기화
history = np.zeros((0, 2))
```


```python
# 루프 처리

for epoch in range(num_epochs):

    # 예측 계산
    Yp = pred(X)

    # 손실 계산
    loss = mse(Yp, Y)

    # 경삿값 초기화
    optimizer.zero_grad()

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()


    # 손실 기록
    if (epoch %10 == 0):
        item = np.array([epoch, loss.item()])
        history = np.vstack((history, item))
        print(f'epoch = {epoch}  loss = {loss:.4f}')
```

    epoch = 0  loss = 13.3520
    epoch = 10  loss = 10.3855
    epoch = 20  loss = 8.5173
    epoch = 30  loss = 7.3364
    epoch = 40  loss = 6.5858
    epoch = 50  loss = 6.1047
    epoch = 60  loss = 5.7927
    epoch = 70  loss = 5.5868
    epoch = 80  loss = 5.4476
    epoch = 90  loss = 5.3507
    epoch = 100  loss = 5.2805
    epoch = 110  loss = 5.2275
    epoch = 120  loss = 5.1855
    epoch = 130  loss = 5.1507
    epoch = 140  loss = 5.1208
    epoch = 150  loss = 5.0943
    epoch = 160  loss = 5.0703
    epoch = 170  loss = 5.0480
    epoch = 180  loss = 5.0271
    epoch = 190  loss = 5.0074
    epoch = 200  loss = 4.9887
    epoch = 210  loss = 4.9708
    epoch = 220  loss = 4.9537
    epoch = 230  loss = 4.9373
    epoch = 240  loss = 4.9217
    epoch = 250  loss = 4.9066
    epoch = 260  loss = 4.8922
    epoch = 270  loss = 4.8783
    epoch = 280  loss = 4.8650
    epoch = 290  loss = 4.8522
    epoch = 300  loss = 4.8399
    epoch = 310  loss = 4.8281
    epoch = 320  loss = 4.8167
    epoch = 330  loss = 4.8058
    epoch = 340  loss = 4.7953
    epoch = 350  loss = 4.7853
    epoch = 360  loss = 4.7756
    epoch = 370  loss = 4.7663
    epoch = 380  loss = 4.7574
    epoch = 390  loss = 4.7488
    epoch = 400  loss = 4.7406
    epoch = 410  loss = 4.7327
    epoch = 420  loss = 4.7251
    epoch = 430  loss = 4.7178
    epoch = 440  loss = 4.7108
    epoch = 450  loss = 4.7040
    epoch = 460  loss = 4.6976
    epoch = 470  loss = 4.6913
    epoch = 480  loss = 4.6854
    epoch = 490  loss = 4.6796



```python
# 최종 파라미터 값
print('W = ', W.data.numpy())
print('B = ', B.data.numpy())

# 손실 확인
print(f'초기상태 : 손실:{history[0,1]:.4f}')
print(f'최종상태 : 손실:{history[-1,1]:.4f}')
```

    W =  1.820683
    B =  0.3675114
    초기상태 : 손실:13.3520
    최종상태 : 손실:4.6796



```python
# 학습 곡선 출력(손실)

plt.plot(history[:,0], history[:,1], 'b')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.title('학습 곡선(손실)')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__55_0.webp)
    


3.7의 결과와 비교해보면 동일한 것을 알 수 있다.
따라서, step 함수는 다음의 코드와 같은 로직을 수행하고 있다.

```py3

 with torch.no_grad():
        # 파라미터 수정
        # 프레임워크를 사용하는 경우는 step 함수가 이를 대신함
        W -= lr * W.grad
        B -= lr * B.grad
```

### 최적화 함수 튜닝


```python
# 초기화

# W와 B를 변수로 사용
W = torch.tensor(1.0, requires_grad=True).float()
B = torch.tensor(1.0, requires_grad=True).float()

# 반복 횟수
num_epochs = 500

# 학습률
lr = 0.001

# optimizer로 SGD(확률적 경사 하강법)을 사용
import torch.optim as optim
optimizer = optim.SGD([W, B], lr=lr, momentum=0.9)

# history 기록을 위한 배열 초기화
history2 = np.zeros((0, 2))
```


```python
# 루프 처리

for epoch in range(num_epochs):

    # 예측 계산
    Yp = pred(X)

    # 손실 계산
    loss = mse(Yp, Y)

    # 경사 계산
    loss.backward()

    # 파라미터 수정
    optimizer.step()

    # 경삿값 초기화
    optimizer.zero_grad()

    # 손실 기록
    if (epoch %10 == 0):
        item = np.array([epoch, loss.item()])
        history2 = np.vstack((history2, item))
        print(f'epoch = {epoch}  loss = {loss:.4f}')
```

    epoch = 0  loss = 13.3520
    epoch = 10  loss = 5.7585
    epoch = 20  loss = 5.9541
    epoch = 30  loss = 5.0276
    epoch = 40  loss = 4.8578
    epoch = 50  loss = 4.7052
    epoch = 60  loss = 4.6327
    epoch = 70  loss = 4.5940
    epoch = 80  loss = 4.5698
    epoch = 90  loss = 4.5574
    epoch = 100  loss = 4.5495
    epoch = 110  loss = 4.5452
    epoch = 120  loss = 4.5426
    epoch = 130  loss = 4.5411
    epoch = 140  loss = 4.5403
    epoch = 150  loss = 4.5398
    epoch = 160  loss = 4.5395
    epoch = 170  loss = 4.5393
    epoch = 180  loss = 4.5392
    epoch = 190  loss = 4.5391
    epoch = 200  loss = 4.5391
    epoch = 210  loss = 4.5391
    epoch = 220  loss = 4.5391
    epoch = 230  loss = 4.5390
    epoch = 240  loss = 4.5390
    epoch = 250  loss = 4.5390
    epoch = 260  loss = 4.5390
    epoch = 270  loss = 4.5390
    epoch = 280  loss = 4.5390
    epoch = 290  loss = 4.5390
    epoch = 300  loss = 4.5390
    epoch = 310  loss = 4.5390
    epoch = 320  loss = 4.5390
    epoch = 330  loss = 4.5390
    epoch = 340  loss = 4.5390
    epoch = 350  loss = 4.5390
    epoch = 360  loss = 4.5390
    epoch = 370  loss = 4.5390
    epoch = 380  loss = 4.5390
    epoch = 390  loss = 4.5390
    epoch = 400  loss = 4.5390
    epoch = 410  loss = 4.5390
    epoch = 420  loss = 4.5390
    epoch = 430  loss = 4.5390
    epoch = 440  loss = 4.5390
    epoch = 450  loss = 4.5390
    epoch = 460  loss = 4.5390
    epoch = 470  loss = 4.5390
    epoch = 480  loss = 4.5390
    epoch = 490  loss = 4.5390



```python
# 학습 곡선(손실) 출력

plt.plot(history[:,0], history[:,1], 'b', label='기본값 설정')
plt.plot(history2[:,0], history2[:,1], 'k', label='momentum=0.9')
plt.xlabel('반복 횟수')
plt.ylabel('손실')
plt.legend()
plt.title('학습 곡선(손실)')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__60_0.webp)
    


### y = x**2 함수의 경사하강 (GD)


```python
x = np.arange(-4, 4.1, 0.1)
y = x**2

plt.figure(figsize = (6, 4))
plt.grid(linestyle = ":")
plt.plot(x, y)

## 초기값 (initial value)
x_ = 4
y_ = 16
lr = 0.1

iter = 10
# for _ in range(iter):

#     plt.scatter(x_, y_, s = 80,  c = "r")
#     dy_dx = 2*x_

#     x_ = x_ - lr*dy_dx
#     y_ = x_**2

plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__62_0.webp)
    


### Regression GD


```python
## X, Y data
x = np.arange(2, 10, step = 2, dtype=np.float16)
y = np.array([81, 93, 91, 97], dtype=np.float16)

plt.scatter(x, y, s = 80)
plt.show()

## 최소제곱법을 이용한 회귀계수 추정
a = 0
b = 0

## learning rate
lr = 0.02
iter = 501


fig, ax = plt.subplots(1, 6, figsize = (12,4))
x_fit = np.arange(2, 10)

j = 0
for i in range(iter):
    y_hat = a*x + b
    error = (y - y_hat)

    a_diff = -(2/len(x))*sum(error*x)
    b_diff = -(2/len(x))*sum(error)

    a = a - lr*a_diff
    b = b - lr*b_diff

    if i % 100 == 0:
        print(f'iter = {i}, slope = {a:.4f}, intercept = {b:.4f}')

        ax[j].scatter(x, y)
        ax[j].plot(x_fit, b + a*x_fit, 'r')
        ax[j].set_title(f'iteration = {i}')
        ax[j].set_ylim(70, 100)

        j += 1

plt.show()


```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__64_0.webp)
    


    iter = 0, slope = 18.5600, intercept = 3.6200
    iter = 100, slope = 8.9456, intercept = 39.3669
    iter = 200, slope = 5.7656, intercept = 58.3238
    iter = 300, slope = 4.1119, intercept = 68.2131
    iter = 400, slope = 3.2519, intercept = 73.3725
    iter = 500, slope = 2.7869, intercept = 76.0619



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__64_2.webp)
    


### 복잡한 함수의 GD


```python
# From calculation, we expect that the local minimum occurs at x=9/4
x_old = 0
x_new = 6 # The algorithm starts at x=6
eps = 0.01 # step size
precision = 0.00001

def f(x):
    return x**4 + 3*x**3 + 1

def f_prime(x):
    return 4 * x**3 - 9 * x**2

while abs(x_new - x_old) > precision:
    x_old = x_new
    x_new = x_old - eps * f_prime(x_old)

print(f"Local minimum occurs at: {x_new}")

x = np.arange(-4, 2, 0.1)

plt.plot(x, f(x))
plt.grid(linestyle = ":")
plt.show()
```

    Local minimum occurs at: 2.2499646074278457



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_5%EC%B0%A8%EC%8B%9C__GD__66_1.webp)
    



## 강의_3기_AI개론_6차시__Object_function_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_6차시__Object_function_.ipynb)

# 6장 예측 함수 정의 하기

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
```

    Successfully installed nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-nvjitlink-cu12-12.4.127 torchviz-0.0.3


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

## 선형 회귀 (Linear regression) 손실 함수

### Linear hidden layers


```python
def linear(x, w, b):
  y = torch.matmul(x, w) + b
  return y

x = torch.FloatTensor([[1, 2, 3],
                       [2, 4, 6]])
print("Initial value", "="*50)
print("x: \n", x)

w1 = torch.rand(3, 4)
b1 = torch.ones(1, 4)
print("w1: \n", w1)
print("b1: \n", b1)

```

    Initial value ==================================================
    x: 
     tensor([[1., 2., 3.],
            [2., 4., 6.]])
    w1: 
     tensor([[0.1561, 0.8231, 0.7018, 0.2547],
            [0.0762, 0.3104, 0.7260, 0.5712],
            [0.3995, 0.0515, 0.5970, 0.3863]])
    b1: 
     tensor([[1., 1., 1., 1.]])



```python
## Hidden layer 1
print("Hidden layer 1", "="*50)
h1 = linear(x, w1, b1)
print("linear(x, w1, b1): \n")
print(h1)
# b = torch.tensor([3])

# Hidden layer 2
print("Hidden layer 2", "="*50)
w2 = torch.rand(4, 3)
print("w2: \n", w2)
b2 = torch.ones(1, 3)
print("b2: \n", b2)

print()
h2 = linear(h1, w2, b2)
print("linear(w1, w2, b): \n", "="*50)
print(h2)
```

    Hidden layer 1 ==================================================
    linear(x, w1, b1): 
    
    tensor([[2.5070, 2.5984, 4.9449, 3.5558],
            [4.0141, 4.1967, 8.8898, 6.1117]])
    Hidden layer 2 ==================================================
    w2: 
     tensor([[0.3832, 0.9377, 0.8449],
            [0.5708, 0.0678, 0.6028],
            [0.8122, 0.1830, 0.8957],
            [0.6924, 0.1640, 0.2347]])
    b2: 
     tensor([[1., 1., 1.]])
    
    linear(w1, w2, b): 
     ==================================================
    tensor([[ 9.9220,  5.0146,  9.9480],
            [16.3854,  7.6768, 16.3179]])


### 회귀 분석: Single data


```python
# torch.manual_seed(1)
input = torch.randn(1, requires_grad=True)
target = torch.randn(1)

print("Before SDG","="*50)
print("input: ", input)
print("target: ", target)

loss = nn.MSELoss() # class
optimizer = optim.SGD([input], lr=0.02) # params argument given to the optimizer should be an iterable of Tensors or dicts

for epoch in range(100):

  loss_result = loss(input, target)
  # loss_result = (input - target)**2
  # print("loss_result: ", loss_result)
  optimizer.zero_grad() # Sets the gradients of all optimized torch.Tensors to zero.
  loss_result.backward() # Computes the gradient of current tensor wrt graph leaves
  optimizer.step()

print("After SDG", "="*50)
print("input: ", input)
print("target: ", target)
```

    Before SDG ==================================================
    input:  tensor([-2.2794], requires_grad=True)
    target:  tensor([0.8761])
    After SDG ==================================================
    input:  tensor([0.8228], requires_grad=True)
    target:  tensor([0.8761])


### 회귀 분석: Batch data


```python
x = torch.arange(-3, 3, 0.1)
y = 2 * x + 1
y1 = 2 * x + 1 + torch.randn(x.shape)
print("x = \n", x)
print("y = \n", y1)

plt.plot(x.numpy(), y.numpy())
plt.plot(x.numpy(), y1.numpy(), "o")
plt.show()
```

    x = 
     tensor([-3.0000e+00, -2.9000e+00, -2.8000e+00, -2.7000e+00, -2.6000e+00,
            -2.5000e+00, -2.4000e+00, -2.3000e+00, -2.2000e+00, -2.1000e+00,
            -2.0000e+00, -1.9000e+00, -1.8000e+00, -1.7000e+00, -1.6000e+00,
            -1.5000e+00, -1.4000e+00, -1.3000e+00, -1.2000e+00, -1.1000e+00,
            -1.0000e+00, -9.0000e-01, -8.0000e-01, -7.0000e-01, -6.0000e-01,
            -5.0000e-01, -4.0000e-01, -3.0000e-01, -2.0000e-01, -1.0000e-01,
            -2.3842e-08,  1.0000e-01,  2.0000e-01,  3.0000e-01,  4.0000e-01,
             5.0000e-01,  6.0000e-01,  7.0000e-01,  8.0000e-01,  9.0000e-01,
             1.0000e+00,  1.1000e+00,  1.2000e+00,  1.3000e+00,  1.4000e+00,
             1.5000e+00,  1.6000e+00,  1.7000e+00,  1.8000e+00,  1.9000e+00,
             2.0000e+00,  2.1000e+00,  2.2000e+00,  2.3000e+00,  2.4000e+00,
             2.5000e+00,  2.6000e+00,  2.7000e+00,  2.8000e+00,  2.9000e+00])
    y = 
     tensor([-5.6562, -4.6821, -4.5692, -5.3380, -4.2822, -3.6094, -3.4296, -4.3626,
            -3.4961, -1.8547, -2.4206, -1.5669, -2.2308, -3.1217, -1.5268, -1.1674,
            -1.7885, -0.6554, -0.5419, -1.6530, -1.6600,  0.0740, -0.8599, -1.7846,
            -1.0413, -0.1855,  0.7463, -0.5915,  1.6027,  2.2478,  1.2890, -0.2717,
             1.6807,  1.2525,  0.8120,  2.6701,  0.3058,  3.3220,  1.8301,  2.5123,
             3.9486,  1.9211,  5.9662,  3.7459,  3.6962,  3.2712,  3.6519,  4.3499,
             5.7666,  3.9812,  5.7902,  5.2615,  7.1498,  4.2552,  6.4119,  6.3046,
             5.0495,  5.3742,  6.8492,  7.4082])



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__16_1.webp)
    


### 회귀 분석: batch data


```python
## Simulate data
x = torch.arange(-3, 3, 0.1)
y = 2 * x + 1
y1 = 2 * x + 1 + torch.randn(x.shape)
print("x = \n", x)
print("y = \n", y1)

plt.plot(x, y)
plt.plot(x, y1, "o")
plt.show()
```

    x = 
     tensor([-3.0000e+00, -2.9000e+00, -2.8000e+00, -2.7000e+00, -2.6000e+00,
            -2.5000e+00, -2.4000e+00, -2.3000e+00, -2.2000e+00, -2.1000e+00,
            -2.0000e+00, -1.9000e+00, -1.8000e+00, -1.7000e+00, -1.6000e+00,
            -1.5000e+00, -1.4000e+00, -1.3000e+00, -1.2000e+00, -1.1000e+00,
            -1.0000e+00, -9.0000e-01, -8.0000e-01, -7.0000e-01, -6.0000e-01,
            -5.0000e-01, -4.0000e-01, -3.0000e-01, -2.0000e-01, -1.0000e-01,
            -2.3842e-08,  1.0000e-01,  2.0000e-01,  3.0000e-01,  4.0000e-01,
             5.0000e-01,  6.0000e-01,  7.0000e-01,  8.0000e-01,  9.0000e-01,
             1.0000e+00,  1.1000e+00,  1.2000e+00,  1.3000e+00,  1.4000e+00,
             1.5000e+00,  1.6000e+00,  1.7000e+00,  1.8000e+00,  1.9000e+00,
             2.0000e+00,  2.1000e+00,  2.2000e+00,  2.3000e+00,  2.4000e+00,
             2.5000e+00,  2.6000e+00,  2.7000e+00,  2.8000e+00,  2.9000e+00])
    y = 
     tensor([-5.9167, -3.9447, -5.6223, -4.0863, -4.5880, -5.0063, -3.9763, -2.4459,
            -3.5088, -3.8868, -2.1705, -2.7506, -1.4298, -4.2381, -2.3589, -0.1983,
            -2.0479, -1.8499, -0.9510, -0.8186,  0.7749, -0.9127, -2.3240,  0.5426,
             0.3100, -1.0177, -1.0024,  0.4696, -0.6133,  1.4404,  1.8807,  0.6990,
             1.2501,  2.3735,  2.0950,  1.3549,  1.2450,  2.1464,  2.4091,  3.8207,
             2.1393,  2.6143,  3.0969,  3.2183,  3.5943,  3.1596,  2.0317,  4.2764,
             4.3305,  5.2369,  5.2304,  5.0597,  4.8653,  4.8217,  5.8014,  4.6964,
             5.1506,  6.5247,  6.1717,  5.7490])



    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__18_1.webp)
    



```python
# Initial weight and bias
a = torch.randn(1, requires_grad=True)
b = torch.randn(1, requires_grad=True)
print("Initial value = \n", "="*50)
print("a: ", a)
print("b: ", b)

# Define loss and optimizer
lr = 0.01
loss = nn.MSELoss()
optimizer = optim.SGD([a, b], lr=lr)

n_epochs = 100

for epoch in range(n_epochs):
    yhat = a*x + b
    loss_result = loss(yhat, y1)
    if epoch % 10 == 0:
      print("epoch: ", epoch, "a: ", a.item(), "b: ",
            b.item(), "loss: ", loss_result.item())
    optimizer.zero_grad()
    loss_result.backward()
    optimizer.step()

print("After SGD", "="*50)
print(a, b)
```

    Initial value = 
     ==================================================
    a:  tensor([-0.4390], requires_grad=True)
    b:  tensor([0.0206], requires_grad=True)
    epoch:  0 a:  -0.4390020966529846 b:  0.02057533524930477 loss:  17.44143295288086
    epoch:  10 a:  0.6328509449958801 b:  0.14871202409267426 loss:  5.784862041473389
    epoch:  20 a:  1.2108873128890991 b:  0.26087409257888794 loss:  2.317333936691284
    epoch:  30 a:  1.5229146480560303 b:  0.35654592514038086 loss:  1.252461552619934
    epoch:  40 a:  1.6915931701660156 b:  0.43689200282096863 loss:  0.9037297368049622
    epoch:  50 a:  1.7829780578613281 b:  0.5037174224853516 loss:  0.7758422493934631
    epoch:  60 a:  1.8326499462127686 b:  0.558957040309906 loss:  0.7208566665649414
    epoch:  70 a:  1.8597805500030518 b:  0.6044394969940186 loss:  0.6929482817649841
    epoch:  80 a:  1.8747056722640991 b:  0.6417922377586365 loss:  0.6768621802330017
    epoch:  90 a:  1.8830021619796753 b:  0.672417402267456 loss:  0.6668579578399658
    After SGD ==================================================
    tensor([1.8877], requires_grad=True) tensor([0.6975], requires_grad=True)


## 예측 함수의 내부 구조


```python
# 레이어 함수 정의

# 첫번째 선형 함수
# 784 입력 수
# 128 출력 수
l1 = nn.Linear(784, 128)

# 두번째 선형 함수
# 128 입력 수
# 10 출력 수
l2 = nn.Linear(128, 10)

# 활성화 함수
relu = nn.ReLU(inplace=True)
```


```python
# 입력 텐서로부터 출력 텐서를 계산

# 더미 입력 데이터 작성
inputs = torch.randn(100, 784)

# 중간 텐서 1 계산
m1 = l1(inputs)

# 중간 텐서 2 계산
m2 = relu(m1)

# 출력 텐서 계산
outputs = l2(m2)

# 입력 텐서와 출력 텐서 shape 확인
print('입력 텐서', inputs.shape)
print('출력 텐서', outputs.shape)
```

    입력 텐서 torch.Size([100, 784])
    출력 텐서 torch.Size([100, 10])



```python
# nn.Sequential을 사용해 전체를 합성 함수로 정의

net2 = nn.Sequential(
    l1,
    relu,
    l2
)

outputs2 = net2(inputs)

# 입력 텐서와 출력 텐서의 shape 확인
print('입력 텐서', inputs.shape)
print('출력 텐서', outputs2.shape)
```

    입력 텐서 torch.Size([100, 784])
    출력 텐서 torch.Size([100, 10])


###  활성화 함수의 목적
이 절에서는 예측 결과 그래프(그림 4-9에서 그림 4-11까지)가 중요하며, 따라서 지금 시점에서 구현 코드의 의미를 이해하지 못하더라도 상관없다. 아래의 코드는 어디까지나 참고를 위해 작성되었다.


```python
# 훈련 데이터, 검증 데이터 계산
np.random.seed(123)
x = np.random.randn(100,1)

# y는 x^2에 난수를 1/10만큼 더한 값
y = x**2 + np.random.randn(100,1) * 0.2

# 데이터를 50건씩 훈련용과 검증용으로 나눔
x_train = x[:50,:]
x_test = x[50:,:]
y_train = y[:50,:]
y_test = y[50:,:]
```


```python
# 산포도 출력
plt.scatter(x_train, y_train, c='b', label='훈련 데이터')
plt.scatter(x_test, y_test, c='k', marker='x', label='검증 데이터')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__26_0.webp)
    



```python
# 입력 변수 x와 정답 yt의 텐서화

inputs = torch.tensor(x_train).float()
labels = torch.tensor(y_train).float()

inputs_test = torch.tensor(x_test).float()
labels_test = torch.tensor(y_test).float()
```

### 선형 회귀 모델의 경우


```python
# 모델 정의

class Net(nn.Module):
    def __init__(self):
        #  부모 클래스 nn.Modules 의 초기화
        super().__init__()

        # 출력층 정의
        self.l1 = nn.Linear(1, 1)

    # 예측 함수 정의
    def forward(self, x):
        x1 = self.l1(x) # 선형 회귀
        return x1
```


```python
# 학습률
lr = 0.01

# 인스턴스 생성(파라미터 초기화)
net = Net()

# 최적화 알고리즘 : 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 손실 함수： 평균 제곱 오차
criterion = nn.MSELoss()

# 반복 횟수
num_epochs = 10000

#  history 기록을 위한 배열 초기화(손실 함수 값 만을 기록)
history = np.zeros((0,2))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 경사 값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net(inputs)

    # 오차 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 경사 하강법 적용
    optimizer.step()

    # 100회 마다 도중 경과를 기록
    if ( epoch % 100 == 0):
        history = np.vstack((history, np.array([epoch, loss.item()])))
        print(f'Epoch {epoch} loss: {loss.item():.5f}')
```

    Epoch 0 loss: 4.07665
    Epoch 100 loss: 3.21111
    Epoch 200 loss: 3.19657
    Epoch 300 loss: 3.19632
    Epoch 400 loss: 3.19631
    Epoch 500 loss: 3.19631
    Epoch 600 loss: 3.19631
    Epoch 700 loss: 3.19631
    Epoch 800 loss: 3.19631
    Epoch 900 loss: 3.19631
    Epoch 1000 loss: 3.19631
    Epoch 1100 loss: 3.19631
    Epoch 1200 loss: 3.19631
    Epoch 1300 loss: 3.19631
    Epoch 1400 loss: 3.19631
    Epoch 1500 loss: 3.19631
    Epoch 1600 loss: 3.19631
    Epoch 1700 loss: 3.19631
    Epoch 1800 loss: 3.19631
    Epoch 1900 loss: 3.19631
    Epoch 2000 loss: 3.19631
    Epoch 2100 loss: 3.19631
    Epoch 2200 loss: 3.19631
    Epoch 2300 loss: 3.19631
    Epoch 2400 loss: 3.19631
    Epoch 2500 loss: 3.19631
    Epoch 2600 loss: 3.19631
    Epoch 2700 loss: 3.19631
    Epoch 2800 loss: 3.19631
    Epoch 2900 loss: 3.19631
    Epoch 3000 loss: 3.19631
    Epoch 3100 loss: 3.19631
    Epoch 3200 loss: 3.19631
    Epoch 3300 loss: 3.19631
    Epoch 3400 loss: 3.19631
    Epoch 3500 loss: 3.19631
    Epoch 3600 loss: 3.19631
    Epoch 3700 loss: 3.19631
    Epoch 3800 loss: 3.19631
    Epoch 3900 loss: 3.19631
    Epoch 4000 loss: 3.19631
    Epoch 4100 loss: 3.19631
    Epoch 4200 loss: 3.19631
    Epoch 4300 loss: 3.19631
    Epoch 4400 loss: 3.19631
    Epoch 4500 loss: 3.19631
    Epoch 4600 loss: 3.19631
    Epoch 4700 loss: 3.19631
    Epoch 4800 loss: 3.19631
    Epoch 4900 loss: 3.19631
    Epoch 5000 loss: 3.19631
    Epoch 5100 loss: 3.19631
    Epoch 5200 loss: 3.19631
    Epoch 5300 loss: 3.19631
    Epoch 5400 loss: 3.19631
    Epoch 5500 loss: 3.19631
    Epoch 5600 loss: 3.19631
    Epoch 5700 loss: 3.19631
    Epoch 5800 loss: 3.19631
    Epoch 5900 loss: 3.19631
    Epoch 6000 loss: 3.19631
    Epoch 6100 loss: 3.19631
    Epoch 6200 loss: 3.19631
    Epoch 6300 loss: 3.19631
    Epoch 6400 loss: 3.19631
    Epoch 6500 loss: 3.19631
    Epoch 6600 loss: 3.19631
    Epoch 6700 loss: 3.19631
    Epoch 6800 loss: 3.19631
    Epoch 6900 loss: 3.19631
    Epoch 7000 loss: 3.19631
    Epoch 7100 loss: 3.19631
    Epoch 7200 loss: 3.19631
    Epoch 7300 loss: 3.19631
    Epoch 7400 loss: 3.19631
    Epoch 7500 loss: 3.19631
    Epoch 7600 loss: 3.19631
    Epoch 7700 loss: 3.19631
    Epoch 7800 loss: 3.19631
    Epoch 7900 loss: 3.19631
    Epoch 8000 loss: 3.19631
    Epoch 8100 loss: 3.19631
    Epoch 8200 loss: 3.19631
    Epoch 8300 loss: 3.19631
    Epoch 8400 loss: 3.19631
    Epoch 8500 loss: 3.19631
    Epoch 8600 loss: 3.19631
    Epoch 8700 loss: 3.19631
    Epoch 8800 loss: 3.19631
    Epoch 8900 loss: 3.19631
    Epoch 9000 loss: 3.19631
    Epoch 9100 loss: 3.19631
    Epoch 9200 loss: 3.19631
    Epoch 9300 loss: 3.19631
    Epoch 9400 loss: 3.19631
    Epoch 9500 loss: 3.19631
    Epoch 9600 loss: 3.19631
    Epoch 9700 loss: 3.19631
    Epoch 9800 loss: 3.19631
    Epoch 9900 loss: 3.19631



```python
# 결과 그래프
labels_pred = net(inputs_test)

plt.title('은닉층 없음,활성화 함수 없음')
plt.scatter(inputs_test[:,0].data, labels_pred[:,0].data, c='b', label='예측값')
plt.scatter(inputs_test[:,0].data, labels_test[:,0].data, c='k', marker='x',label='정답')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__32_0.webp)
    


### 활성화 함수가 없는 딥러닝 모델의 경우


```python
# 모델 정의

class Net2(nn.Module):
    def __init__(self):
        #  부모 클래스 nn.Modules 초기화
        super().__init__()

        # 출력층 정의
        self.l1 = nn.Linear(1, 10)
        self.l2 = nn.Linear(10, 10)
        self.l3 = nn.Linear(10,1)

    # 예측 함수 정의
    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.l2(x1)
        x3 = self.l3(x2)
        return x3
```


```python
# 학습률
lr = 0.01

# 인스턴스 생성(파라미터 초기화)
net2 = Net2()

# 최적화 알고리즘 : 경사 하강법
optimizer = optim.SGD(net2.parameters(), lr=lr)

# 손실 함수 : 평균 제곱 오차
criterion = nn.MSELoss()

# 반복 횟수
num_epochs = 10000

# history 기록을 위한 배열 초기화(손실 함수 값 만을 기록)
history = np.zeros((0,2))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 경사 값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net2(inputs)

    # 오차 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 경사 하강법 적용
    optimizer.step()

    # 100회 마다 도중 경과를 기록
    if ( epoch % 100 == 0):
        history = np.vstack((history, np.array([epoch, loss.item()])))
        print(f'Epoch {epoch} loss: {loss.item():.5f}')
```

    Epoch 0 loss: 6.10382
    Epoch 100 loss: 3.19631
    Epoch 200 loss: 3.19631
    Epoch 300 loss: 3.19631
    Epoch 400 loss: 3.19631
    Epoch 500 loss: 3.19631
    Epoch 600 loss: 3.19631
    Epoch 700 loss: 3.19631
    Epoch 800 loss: 3.19631
    Epoch 900 loss: 3.19631
    Epoch 1000 loss: 3.19631
    Epoch 1100 loss: 3.19631
    Epoch 1200 loss: 3.19631
    Epoch 1300 loss: 3.19631
    Epoch 1400 loss: 3.19631
    Epoch 1500 loss: 3.19631
    Epoch 1600 loss: 3.19631
    Epoch 1700 loss: 3.19631
    Epoch 1800 loss: 3.19631
    Epoch 1900 loss: 3.19631
    Epoch 2000 loss: 3.19631
    Epoch 2100 loss: 3.19631
    Epoch 2200 loss: 3.19631
    Epoch 2300 loss: 3.19631
    Epoch 2400 loss: 3.19631
    Epoch 2500 loss: 3.19631
    Epoch 2600 loss: 3.19631
    Epoch 2700 loss: 3.19631
    Epoch 2800 loss: 3.19631
    Epoch 2900 loss: 3.19631
    Epoch 3000 loss: 3.19631
    Epoch 3100 loss: 3.19631
    Epoch 3200 loss: 3.19631
    Epoch 3300 loss: 3.19631
    Epoch 3400 loss: 3.19631
    Epoch 3500 loss: 3.19631
    Epoch 3600 loss: 3.19631
    Epoch 3700 loss: 3.19631
    Epoch 3800 loss: 3.19631
    Epoch 3900 loss: 3.19631
    Epoch 4000 loss: 3.19631
    Epoch 4100 loss: 3.19631
    Epoch 4200 loss: 3.19631
    Epoch 4300 loss: 3.19631
    Epoch 4400 loss: 3.19631
    Epoch 4500 loss: 3.19631
    Epoch 4600 loss: 3.19631
    Epoch 4700 loss: 3.19631
    Epoch 4800 loss: 3.19631
    Epoch 4900 loss: 3.19631
    Epoch 5000 loss: 3.19631
    Epoch 5100 loss: 3.19631
    Epoch 5200 loss: 3.19631
    Epoch 5300 loss: 3.19631
    Epoch 5400 loss: 3.19631
    Epoch 5500 loss: 3.19631
    Epoch 5600 loss: 3.19631
    Epoch 5700 loss: 3.19631
    Epoch 5800 loss: 3.19631
    Epoch 5900 loss: 3.19631
    Epoch 6000 loss: 3.19631
    Epoch 6100 loss: 3.19631
    Epoch 6200 loss: 3.19631
    Epoch 6300 loss: 3.19631
    Epoch 6400 loss: 3.19631
    Epoch 6500 loss: 3.19631
    Epoch 6600 loss: 3.19631
    Epoch 6700 loss: 3.19631
    Epoch 6800 loss: 3.19631
    Epoch 6900 loss: 3.19631
    Epoch 7000 loss: 3.19631
    Epoch 7100 loss: 3.19631
    Epoch 7200 loss: 3.19631
    Epoch 7300 loss: 3.19631
    Epoch 7400 loss: 3.19631
    Epoch 7500 loss: 3.19631
    Epoch 7600 loss: 3.19631
    Epoch 7700 loss: 3.19631
    Epoch 7800 loss: 3.19631
    Epoch 7900 loss: 3.19631
    Epoch 8000 loss: 3.19631
    Epoch 8100 loss: 3.19631
    Epoch 8200 loss: 3.19631
    Epoch 8300 loss: 3.19631
    Epoch 8400 loss: 3.19631
    Epoch 8500 loss: 3.19631
    Epoch 8600 loss: 3.19631
    Epoch 8700 loss: 3.19631
    Epoch 8800 loss: 3.19631
    Epoch 8900 loss: 3.19631
    Epoch 9000 loss: 3.19631
    Epoch 9100 loss: 3.19631
    Epoch 9200 loss: 3.19631
    Epoch 9300 loss: 3.19631
    Epoch 9400 loss: 3.19631
    Epoch 9500 loss: 3.19631
    Epoch 9600 loss: 3.19631
    Epoch 9700 loss: 3.19631
    Epoch 9800 loss: 3.19631
    Epoch 9900 loss: 3.19631



```python
# 결과 그래프
labels_pred2 = net2(inputs_test)

plt.title('은닉층 2개, 활성화 함수 사용하지 않음')
plt.scatter(inputs_test[:,0].data, labels_pred2[:,0].data, c='b', label='예측값')
plt.scatter(inputs_test[:,0].data, labels_test[:,0].data, c='k', marker='x',label='정답')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__37_0.webp)
    


### 활성화 함수 사용가 있는 딥러닝 모델의 경우


```python
# 모델 정의

class Net3(nn.Module):
    def __init__(self):
        #  부모 클래스 nn.Modules 초기화
        super().__init__()

        # 출력층 정의
        self.l1 = nn.Linear(1, 10)
        self.l2 = nn.Linear(10, 10)
        self.l3 = nn.Linear(10,1)
        self.relu = nn.ReLU(inplace=True)

    # 예측 함수 정의
    def forward(self, x):
        x1 = self.relu(self.l1(x))
        x2 = self.relu(self.l2(x1))
        x3 = self.l3(x2)
        return x3
```


```python
# 학습률
lr = 0.01

# 인스턴스 생성(파라미터 초기화)
net3 = Net3()

# 최적화 알고리즘 : 경사 하강법
optimizer = optim.SGD(net3.parameters(), lr=lr)

# 손실 함수： 평균 제곱 오차
criterion = nn.MSELoss()

# 반복 횟수
num_epochs = 10000

# history 기록을 위한 배열 초기화(손실 함수 값 만을 기록)
history = np.zeros((0,2))
```


```python
# 반복 계산 메인 루프

for epoch in range(num_epochs):

    # 경사 값 초기화
    optimizer.zero_grad()

    # 예측 계산
    outputs = net3(inputs)

    # 오차 계산
    loss = criterion(outputs, labels)

    # 경사 계산
    loss.backward()

    # 경사 하강법 적용
    optimizer.step()

    # 100회 마다 도중 경과를 기록
    if ( epoch % 100 == 0):
        history = np.vstack((history, np.array([epoch, loss.item()])))
        print(f'Epoch {epoch} loss: {loss.item():.5f}')
```

    Epoch 0 loss: 4.68561
    Epoch 100 loss: 0.93972
    Epoch 200 loss: 0.15431
    Epoch 300 loss: 0.09376
    Epoch 400 loss: 0.07852
    Epoch 500 loss: 0.07051
    Epoch 600 loss: 0.06508
    Epoch 700 loss: 0.06159
    Epoch 800 loss: 0.05960
    Epoch 900 loss: 0.05824
    Epoch 1000 loss: 0.05723
    Epoch 1100 loss: 0.05644
    Epoch 1200 loss: 0.05582
    Epoch 1300 loss: 0.05494
    Epoch 1400 loss: 0.05419
    Epoch 1500 loss: 0.05365
    Epoch 1600 loss: 0.05321
    Epoch 1700 loss: 0.05285
    Epoch 1800 loss: 0.05252
    Epoch 1900 loss: 0.05205
    Epoch 2000 loss: 0.05155
    Epoch 2100 loss: 0.05114
    Epoch 2200 loss: 0.05079
    Epoch 2300 loss: 0.05048
    Epoch 2400 loss: 0.05020
    Epoch 2500 loss: 0.04995
    Epoch 2600 loss: 0.04972
    Epoch 2700 loss: 0.04947
    Epoch 2800 loss: 0.04925
    Epoch 2900 loss: 0.04905
    Epoch 3000 loss: 0.04888
    Epoch 3100 loss: 0.04874
    Epoch 3200 loss: 0.04860
    Epoch 3300 loss: 0.04848
    Epoch 3400 loss: 0.04837
    Epoch 3500 loss: 0.04826
    Epoch 3600 loss: 0.04817
    Epoch 3700 loss: 0.04809
    Epoch 3800 loss: 0.04802
    Epoch 3900 loss: 0.04795
    Epoch 4000 loss: 0.04788
    Epoch 4100 loss: 0.04782
    Epoch 4200 loss: 0.04777
    Epoch 4300 loss: 0.04772
    Epoch 4400 loss: 0.04767
    Epoch 4500 loss: 0.04762
    Epoch 4600 loss: 0.04758
    Epoch 4700 loss: 0.04754
    Epoch 4800 loss: 0.04750
    Epoch 4900 loss: 0.04741
    Epoch 5000 loss: 0.04730
    Epoch 5100 loss: 0.04720
    Epoch 5200 loss: 0.04713
    Epoch 5300 loss: 0.04704
    Epoch 5400 loss: 0.04694
    Epoch 5500 loss: 0.04686
    Epoch 5600 loss: 0.04678
    Epoch 5700 loss: 0.04670
    Epoch 5800 loss: 0.04662
    Epoch 5900 loss: 0.04654
    Epoch 6000 loss: 0.04647
    Epoch 6100 loss: 0.04640
    Epoch 6200 loss: 0.04634
    Epoch 6300 loss: 0.04628
    Epoch 6400 loss: 0.04622
    Epoch 6500 loss: 0.04616
    Epoch 6600 loss: 0.04611
    Epoch 6700 loss: 0.04606
    Epoch 6800 loss: 0.04601
    Epoch 6900 loss: 0.04597
    Epoch 7000 loss: 0.04593
    Epoch 7100 loss: 0.04590
    Epoch 7200 loss: 0.04587
    Epoch 7300 loss: 0.04584
    Epoch 7400 loss: 0.04581
    Epoch 7500 loss: 0.04579
    Epoch 7600 loss: 0.04577
    Epoch 7700 loss: 0.04575
    Epoch 7800 loss: 0.04574
    Epoch 7900 loss: 0.04573
    Epoch 8000 loss: 0.04572
    Epoch 8100 loss: 0.04571
    Epoch 8200 loss: 0.04570
    Epoch 8300 loss: 0.04569
    Epoch 8400 loss: 0.04568
    Epoch 8500 loss: 0.04568
    Epoch 8600 loss: 0.04567
    Epoch 8700 loss: 0.04567
    Epoch 8800 loss: 0.04566
    Epoch 8900 loss: 0.04566
    Epoch 9000 loss: 0.04565
    Epoch 9100 loss: 0.04565
    Epoch 9200 loss: 0.04564
    Epoch 9300 loss: 0.04564
    Epoch 9400 loss: 0.04564
    Epoch 9500 loss: 0.04563
    Epoch 9600 loss: 0.04563
    Epoch 9700 loss: 0.04563
    Epoch 9800 loss: 0.04562
    Epoch 9900 loss: 0.04562



```python
# 결과 그래프
labels_pred3 = net3(inputs_test)

plt.title('은닉층 2개, 활성화 함수 사용')
plt.scatter(inputs_test[:,0].data, labels_pred3[:,0].data, c='b', label='예측값')
plt.scatter(inputs_test[:,0].data, labels_test[:,0].data, c='k', marker='x',label='정답')
plt.legend()
plt.show()

```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__42_0.webp)
    


## 이진 분류 (Binary classification) 비용 함수

### 시그모이드 (Sigmoid) 함수


```python
##
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.arange(-5.0, 5.0, 0.1)
y = sigmoid(x)

fig, axes = plt.subplots(figsize=(4, 4))
plt.plot(x, y)
plt.grid(linestyle = ":")
plt.hlines(0.5, -5, 5, colors="r", linestyles="dashed")
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__45_0.webp)
    



```python
x = np.arange(-5.0, 5.0, 0.1)
y1 = sigmoid(0.5*x)
y2 = sigmoid(x)
y3 = sigmoid(2*x)

fig, axes = plt.subplots(figsize=(4, 4))
plt.plot(x, y1, 'r', linestyle='--') # W의 값이 0.5일때
plt.plot(x, y2, 'g') # W의 값이 1일때
plt.plot(x, y3, 'b', linestyle='--') # W의 값이 2일때
plt.plot([0,0],[1.0,0.0], ':') # 가운데 점선 추가
plt.title('Sigmoid Function')
plt.show()
```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__46_0.webp)
    


### 이진 분류 함수의 손실 함수와 비용 함수


```python
# torch.manual_seed(1)
x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]
x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

print("Data shape", "="*50)
print(x_train.shape)
print(y_train.shape)

# Parameter initialize
W = torch.zeros((2, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

print("W: \n", W)
print("b: \n", b)

# sigmoid function
def prob(x, w, b):
    y = 1/(1 + torch.exp(-(torch.matmul(x, w) + b)))
    return y

prob = prob(x_train, W, b)
# prob = torch.sigmoid(x_train.matmul(W) + b)

print("Prob: \n", prob)

# cost function
losses = -(y_train*torch.log(prob) + (1 - y_train)*torch.log(1 - prob))
cost = losses.mean()
print("cost: \n", cost)
```

    Data shape ==================================================
    torch.Size([6, 2])
    torch.Size([6, 1])
    W: 
     tensor([[0.],
            [0.]], requires_grad=True)
    b: 
     tensor([0.], requires_grad=True)
    Prob: 
     tensor([[0.5000],
            [0.5000],
            [0.5000],
            [0.5000],
            [0.5000],
            [0.5000]], grad_fn=<MulBackward0>)
    cost: 
     tensor(0.6931, grad_fn=<MeanBackward0>)



```python
#
x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]
x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

loss = nn.BCELoss()
sigmoid = nn.Sigmoid()
W = torch.zeros((2, 1), requires_grad=True) #
b = torch.zeros(1, requires_grad=True)

lr = 1
optimizer = optim.SGD([W, b], lr=1)
# print("optimizer: \n", optimizer)

nb_epochs = 1000
for epoch in range(nb_epochs + 1):

    prediction = sigmoid(x_train.matmul(W) + b)
    # prediction = torch.sigmoid(x_train.matmul(W) + b) # method
    cost = loss(prediction, y_train)
    # cost = F.binary_cross_entropy(prediction, y_train)

    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print('Epoch {:4d}/{} Cost: {:.6f}'.format(
            epoch, nb_epochs, cost.item()
        ))
```

    Epoch    0/1000 Cost: 0.693147
    Epoch  100/1000 Cost: 0.134722
    Epoch  200/1000 Cost: 0.080643
    Epoch  300/1000 Cost: 0.057900
    Epoch  400/1000 Cost: 0.045300
    Epoch  500/1000 Cost: 0.037261
    Epoch  600/1000 Cost: 0.031672
    Epoch  700/1000 Cost: 0.027556
    Epoch  800/1000 Cost: 0.024394
    Epoch  900/1000 Cost: 0.021888
    Epoch 1000/1000 Cost: 0.019852


## 다중 분류 (Multinomial classification) 비용 함수

### Pytorch 소프트맥스 함수


```python
def softmax(x):
    y = np.exp(x)/np.sum(np.exp(x))
    return y


x = torch.rand(1, 4)
print('Tensor x = \n', x)

prob = softmax(x.numpy())
# prob = torch.softmax(x, dim = 1) # dim 0, 1
# prob = F.softmax(x, dim = 1)

print("Softmax = \n", prob)
```

    Tensor x = 
     tensor([[0.5389, 0.7376, 0.4636, 0.6481]])
    Softmax = 
     [[0.2346 0.2862 0.2176 0.2617]]


### Pytorch로 softmax 의 cost 함수 구현하기


```python
### One-hot vector 만들기

x = torch.rand(3, 5, requires_grad=True)
print("x: \n", x)
prob = F.softmax(x, dim = 1)
print("prob: \n", prob)

y = torch.randint(5, (3,)) # torch.int64
print("target y = ", y)

# 모든 원소가 0의 값을 가진 3 × 5 텐서 생성
y_one_hot = torch.zeros_like(x)
print(y_one_hot)
y_one_hot.scatter_(dim = 1, index = y.unsqueeze(dim = 1), value = 1) # Tensor.scatter_(dim, index, src, *, reduce=None)
print("one hot vector = \n", y_one_hot)


# 비용함수
print("Crossentroy cost function = ")
(-y_one_hot * torch.log(F.softmax(x, dim=1))).sum(dim=1).mean()
```

    x: 
     tensor([[0.7282, 0.0839, 0.4163, 0.9972, 0.7081],
            [0.5378, 0.7255, 0.6014, 0.9830, 0.2230],
            [0.8833, 0.5953, 0.5312, 0.8071, 0.5571]], requires_grad=True)
    prob: 
     tensor([[0.2200, 0.1155, 0.1610, 0.2879, 0.2156],
            [0.1798, 0.2169, 0.1916, 0.2806, 0.1312],
            [0.2438, 0.1828, 0.1715, 0.2259, 0.1760]], grad_fn=<SoftmaxBackward0>)
    target y =  tensor([0, 4, 3])
    tensor([[0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0.]])
    one hot vector = 
     tensor([[1., 0., 0., 0., 0.],
            [0., 0., 0., 0., 1.],
            [0., 0., 0., 1., 0.]])
    Crossentroy cost function = 





    tensor(1.6776, grad_fn=<MeanBackward0>)




```python
### Crossentropy 비용함수
# Low level
torch.log(F.softmax(x, dim=1))

# High level
F.log_softmax(x, dim=1)

# cost function
(y_one_hot * - F.log_softmax(x, dim=1)).sum(dim=1).mean()

 # High level
# 세번째 수식
F.nll_loss(F.log_softmax(x, dim=1), y) # y =  tensor([1, 1, 3])

# 네번째 수식
F.cross_entropy(x, y) # z = torch.rand(3, 5, requires_grad=True), y = torch.randint(5, (3,))
```




    tensor(1.6776, grad_fn=<NllLossBackward0>)




```python
x_train = [[1, 2, 1, 1],
           [2, 1, 3, 2],
           [3, 1, 3, 4],
           [4, 1, 5, 5],
           [1, 7, 5, 5],
           [1, 2, 5, 6],
           [1, 6, 6, 6],
           [1, 7, 7, 7]]
y_train = [2, 2, 2, 1, 1, 1, 0, 0]
x_train = torch.FloatTensor(x_train)
y_train = torch.LongTensor(y_train)

print(x_train.shape)
print(y_train.shape)

#
y_one_hot = torch.zeros(8, 3)
y_one_hot.scatter_(1, y_train.unsqueeze(1), 1)


# 모델 초기화
W = torch.zeros((4, 3), requires_grad=True)
b = torch.zeros((1, 3), requires_grad=True)
# optimizer 설정
lr = 0.1
optimizer = optim.SGD([W, b], lr=lr)

nb_epochs = 100

for epoch in range(nb_epochs + 1):

    # H(x) 계산
    hypothesis = F.softmax(x_train.matmul(W) + b, dim=1)
    cost = (y_one_hot * -torch.log(hypothesis)).sum(dim=1).mean()

    # cost로 H(x) 개선
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print('Epoch {:4d}/{} Cost: {:.6f}'.format(
            epoch, nb_epochs, cost.item()
        ))
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[1], line 10
          1 x_train = [[1, 2, 1, 1],
          2            [2, 1, 3, 2],
          3            [3, 1, 3, 4],
       (...)
          7            [1, 6, 6, 6],
          8            [1, 7, 7, 7]]
          9 y_train = [2, 2, 2, 1, 1, 1, 0, 0]
    ---> 10 x_train = torch.FloatTensor(x_train)
         11 y_train = torch.LongTensor(y_train)
         13 print(x_train.shape)


    NameError: name 'torch' is not defined



```python
import numpy as np
import matplotlib.pyplot as plt

# 예제 3D 포인트 클라우드 데이터 (X, Y, Z)
point_cloud = np.array([
    [1, 2, 0.5], [2, 3, 1.0], [3, 4, 1.5], [4, 5, 2.0], 
    [2, 2, 0.3], [3, 3, 1.2], [5, 5, 2.5], [6, 7, 3.0]
])

# X, Y 좌표만 가져와서 Top-Down Projection 수행
x = point_cloud[:, 0]
y = point_cloud[:, 1]

# 2D Top-Down View 시각화
plt.figure(figsize=(6, 6))
plt.scatter(x, y, c='blue', marker='o', label="Projected Points")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Top-Down Projection of 3D Point Cloud")
plt.grid(True)
plt.legend()
plt.show()

```


    
![png](../assets/images/ai/neural-network-fundamentals/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_6%EC%B0%A8%EC%8B%9C__Object_function__57_0.webp)
    



```python

```
