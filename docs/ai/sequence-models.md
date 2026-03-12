# 시퀀스 모델 (RNN/LSTM)


## 강의_3기_AI개론_19차시__RNN_LSTM_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_19차시__RNN_LSTM_.ipynb)

# 19장 순환 신경망 (Recurrent neural network)
- Vanilla RNN, LSTM

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```


```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
```


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
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

import os
import torch
from torch import nn, optim
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
# GPU 디바이스 할당

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
```

    cuda:0


# **Vanillla RNN**

### RNN 모델 구조


```python
def torch_seed(seed=123, deter = False):
  
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = deter
    torch.use_deterministic_algorithms = deter
```


```python
## parameter 
input_size = 2
hidden_size = 4

# (batch_size, time_steps, input_size)
inputs = torch.rand((1, 5, input_size)) # U(0, 1)
print(inputs)
print(inputs.dtype)
```

    tensor([[[0.1241, 0.4324],
             [0.2235, 0.2961],
             [0.9725, 0.1091],
             [0.7995, 0.5880],
             [0.7150, 0.0430]]])
    torch.float32



```python
input_size = 2
hidden_size = 4
rnn = nn.RNN(input_size, hidden_size, batch_first=True)
```


```python
torch_seed()

## parameter 
input_size = 2
hidden_size = 4
rnn = nn.RNN(input_size, hidden_size, batch_first=True) # 맨 앞이 batch
print('hidden weights = \n')
list(rnn.parameters())
```

    hidden weights = 
    





    [Parameter containing:
     tensor([[-0.2039,  0.0166],
             [-0.2483,  0.1886],
             [-0.4260,  0.3665],
             [-0.3634, -0.3975]], requires_grad=True),
     Parameter containing:
     tensor([[-0.3159,  0.2264, -0.1847,  0.1871],
             [-0.4244, -0.3034, -0.1836, -0.0983],
             [-0.3814,  0.3274, -0.1179,  0.1605],
             [ 0.3536,  0.0932,  0.1367,  0.4826]], requires_grad=True),
     Parameter containing:
     tensor([-0.2255,  0.1584, -0.2225,  0.3573], requires_grad=True),
     Parameter containing:
     tensor([ 0.3993, -0.4610,  0.4268,  0.2388], requires_grad=True)]




```python
outputs, _status = rnn(inputs) # inputs = (1, 5, 2)
print("hiddens = \n", outputs)  ## 모든 노드
print("terminal = \n", _status)  ## 마지막 노드
```

    hiddens = 
     tensor([[[ 0.1544, -0.2467,  0.3004,  0.3619],
             [ 0.0407, -0.3659,  0.1003,  0.5680],
             [-0.0306, -0.4653, -0.2222,  0.4361],
             [ 0.0475, -0.2338,  0.0348,  0.1952],
             [-0.0091, -0.4193, -0.1508,  0.3911]]], grad_fn=<TransposeBackward1>)
    terminal = 
     tensor([[[-0.0091, -0.4193, -0.1508,  0.3911]]], grad_fn=<StackBackward0>)


### 2개 이상의 RNN layer


```python
inputs = torch.Tensor(1, 5, 2)
# (batch_size, time_steps, input_size)
cell = nn.RNN(input_size = 2, hidden_size = 6, num_layers = 2, 
              batch_first=True)

outputs, _status = cell(inputs)
print("hidden shape = \n", outputs)  ## 모든 노드
print()
print("terminal = \n",_status)  ## 마지막 노드

print("_status[0] = \n", _status[0])  ## first layer 마지막 노드
print("_status[1] = \n", _status[1])  ## second layer 마지막 노드
```

    hidden shape = 
     tensor([[[-0.0987, -0.6732, -0.4266,  0.0146, -0.0286,  0.3485],
             [-0.2571, -0.7404, -0.3544,  0.1276, -0.0586,  0.5508],
             [-0.1535, -0.6743, -0.2998, -0.0404, -0.1162,  0.5495],
             [-0.1249, -0.7686, -0.3432,  0.0732, -0.0550,  0.5247],
             [-0.1860, -0.7401, -0.3549,  0.0213, -0.0958,  0.5711]]],
           grad_fn=<TransposeBackward1>)
    
    terminal = 
     tensor([[[ 0.6543, -0.5262,  0.0933, -0.8319,  0.3218, -0.0678]],
    
            [[-0.1860, -0.7401, -0.3549,  0.0213, -0.0958,  0.5711]]],
           grad_fn=<StackBackward0>)
    _status[0] = 
     tensor([[ 0.6543, -0.5262,  0.0933, -0.8319,  0.3218, -0.0678]],
           grad_fn=<SelectBackward0>)
    _status[1] = 
     tensor([[-0.1860, -0.7401, -0.3549,  0.0213, -0.0958,  0.5711]],
           grad_fn=<SelectBackward0>)


# **문자단위 RNN**


```python
input_str = 'apple'
label_str = 'pple!'
```

### Vocab set


```python
# 1. Vocab set
char_vocab = sorted(list(set(input_str+label_str)))
vocab_size = len(char_vocab)
print ('문자 집합의 크기 : {}'.format(vocab_size))
print(char_vocab)
```

    문자 집합의 크기 : 5
    ['!', 'a', 'e', 'l', 'p']


### 문자 집합에 고유한 정수를 부여


```python
# 2. 문자 집합에 고유한 정수를 부여
char_to_index = dict((c, i) for i, c in enumerate(char_vocab)) # 문자에 고유한 정수 인덱스 부여
print(char_to_index)

index_to_char = dict((i, c) for i, c in enumerate(char_vocab)) # 문자에 고유한 정수 인덱스 부여
print(index_to_char)
```

    {'!': 0, 'a': 1, 'e': 2, 'l': 3, 'p': 4}
    {0: '!', 1: 'a', 2: 'e', 3: 'l', 4: 'p'}


### Label encoding 만들기


```python
# 3. Label encoding 
x_data = [char_to_index[c] for c in input_str]
y_data = [char_to_index[c] for c in label_str]
print(x_data)
print(y_data)

```

    [1, 4, 4, 3, 2]
    [4, 4, 3, 2, 0]



```python
# 배치 차원 추가
x_data = [x_data]
y_data = [y_data]
print(x_data)
print(y_data)
```

    [[1, 4, 4, 3, 2]]
    [[4, 4, 3, 2, 0]]


### Onehot encoding


```python
# 4. Onehot encoding 
# x_one_hot = [np.eye(vocab_size)[x] for x in x_data]
x_one_hot = np.eye(vocab_size)[x_data]
print(x_one_hot)
```

    [[[0. 1. 0. 0. 0.]
      [0. 0. 0. 0. 1.]
      [0. 0. 0. 0. 1.]
      [0. 0. 0. 1. 0.]
      [0. 0. 1. 0. 0.]]]


### Tensor input 만들기


```python
X = torch.FloatTensor(x_one_hot)
Y = torch.LongTensor(y_data)
print('훈련 데이터의 크기 : {}'.format(X.shape))
print('레이블의 크기 : {}'.format(Y.shape))
print("X = \n", X)
print("Y = \n", Y)
```

    훈련 데이터의 크기 : torch.Size([1, 5, 5])
    레이블의 크기 : torch.Size([1, 5])
    X = 
     tensor([[[0., 1., 0., 0., 0.],
             [0., 0., 0., 0., 1.],
             [0., 0., 0., 0., 1.],
             [0., 0., 0., 1., 0.],
             [0., 0., 1., 0., 0.]]])
    Y = 
     tensor([[4, 4, 3, 2, 0]])


### RNN 모델 만들기


```python
input_size = vocab_size # 입력의 크기는 문자 집합의 크기
hidden_size = 6
output_size = 5
learning_rate = 0.1
```


```python
class VanillaRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(VanillaRNN, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True) # RNN 셀 구현
        self.fc = nn.Linear(hidden_size, output_size, bias=True) # 출력층 구현

    def forward(self, x): # 구현한 RNN 셀과 출력층을 연결
        x, _status = self.rnn(x)
        x = self.fc(x)
        return x
```


```python
net = VanillaRNN(input_size, hidden_size, output_size)
```

### Output 크기


```python
outputs = net(X) # X.shape = torch.Size([1, 5, 5])
print(outputs.shape) # 3차원 텐서
print(outputs)
```

    torch.Size([1, 5, 5])
    tensor([[[ 0.1416, -0.0020,  0.1332,  0.0077, -0.0202],
             [-0.3027, -0.1178,  0.1346, -0.0147,  0.0964],
             [-0.2770, -0.0168,  0.1117, -0.2443,  0.1217],
             [ 0.0175,  0.0066,  0.0873, -0.0874,  0.0303],
             [-0.0669,  0.2396,  0.1866,  0.0601,  0.2300]]],
           grad_fn=<ViewBackward0>)



```python
print(outputs)
print(Y)

```

    tensor([[[ 0.3650,  0.7164, -0.0127,  0.1906, -0.3810],
             [ 0.3215,  0.6482, -0.0727,  0.2921, -0.0229],
             [ 0.4450,  0.6361, -0.2579,  0.3304,  0.0214],
             [ 0.5763,  0.4344, -0.1728,  0.3319, -0.4698],
             [ 0.2496,  0.8205,  0.1673,  0.0787, -0.2713]]],
           grad_fn=<ViewBackward0>)
    tensor([[4, 4, 3, 2, 0]])



```python
print(outputs.view(-1, input_size)) # 2차원 텐서로 변환
print(Y.view(-1))

```

    tensor([[ 0.1416, -0.0020,  0.1332,  0.0077, -0.0202],
            [-0.3027, -0.1178,  0.1346, -0.0147,  0.0964],
            [-0.2770, -0.0168,  0.1117, -0.2443,  0.1217],
            [ 0.0175,  0.0066,  0.0873, -0.0874,  0.0303],
            [-0.0669,  0.2396,  0.1866,  0.0601,  0.2300]],
           grad_fn=<ViewBackward0>)
    tensor([4, 4, 3, 2, 0])


### Loss function, optimizer 정의


```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), learning_rate)
```

### RNN 모델 학습


```python
# output shape = (1, 5, 5)
# Y shape = (1, 5)

for i in range(100):
    
    outputs = net(X)
    loss = criterion(outputs.view(-1, output_size), Y.view(-1)) # view를 하는 이유는 Batch 차원 제거를 위해, CrossEntropyLoss: outputs should be (N, C), and Y should be (N, )

    optimizer.zero_grad()
    loss.backward() # 기울기 계산
    optimizer.step() # 아까 optimizer 선언 시 넣어둔 파라미터 업데이트

    # 아래 세 줄은 모델이 실제 어떻게 예측했는지를 확인하기 위한 코드.
    result = outputs.argmax(axis=2) # 최종 예측값인 각 time-step 별 5차원 벡터에 대해서 가장 높은 값의 인덱스를 선택
    result_str = ''.join([index_to_char[c] for c in np.squeeze(result.numpy())]) # np.squeeze(result.numpy()) : 1d vector
    print(i, "loss: ", round(loss.item(), 3), "prediction: ", result, "true Y: ", y_data, "prediction str: ", result_str)
```

    0 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    1 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    2 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    3 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    4 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    5 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    6 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    7 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    8 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    9 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    10 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    11 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    12 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    13 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    14 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    15 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    16 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    17 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    18 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    19 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    20 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    21 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    22 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    23 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    24 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    25 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    26 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    27 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    28 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    29 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    30 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    31 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    32 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    33 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    34 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    35 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    36 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    37 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    38 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    39 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    40 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    41 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    42 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    43 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    44 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    45 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    46 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    47 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    48 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    49 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    50 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    51 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    52 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    53 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    54 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    55 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    56 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    57 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    58 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    59 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    60 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    61 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    62 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    63 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    64 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    65 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    66 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    67 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    68 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    69 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    70 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    71 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    72 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    73 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    74 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    75 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    76 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    77 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    78 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    79 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    80 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    81 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    82 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    83 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    84 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    85 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    86 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    87 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    88 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    89 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    90 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    91 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    92 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    93 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    94 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    95 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    96 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    97 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    98 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!
    99 loss:  0.0 prediction:  tensor([[4, 4, 3, 2, 0]]) true Y:  [[4, 4, 3, 2, 0]] prediction str:  pple!


### 한글을 이용한 RNN


```python
# text = "공복에 드셔야 흡수가 잘되기 때문입니다. 공복에 드셨을 때 소화가 잘 되지 않는 분들은 식후에 드시는 것이 좋아요. 생들기름은 성인 기준으로 하루 5g정도 드시면 충분합니다. 숟가락에 따랐을 때 반절이면 5g이에요."
text = "안녕하세요 여러분"
input_str_kr = text
label_str_kr = text[1:] + "!"

print(input_str_kr)
print(label_str_kr)

# input_str_kr = '안녕하세요 여러분'
# label_str_kr = '녕하세요 여러분!'

```

    안녕하세요 여러분
    녕하세요 여러분!



```python

## 1. Vocabulary set
voc_set = set(input_str_kr+label_str_kr)
char_vocab = sorted(list(voc_set))
vocab_size = len(char_vocab)
print ('문자 집합의 크기 : {}'.format(vocab_size))
print("Vocabulary set = ", voc_set)
print("="*50)

```

    문자 집합의 크기 : 10
    Vocabulary set =  {'요', '러', '분', '녕', '여', '세', ' ', '!', '하', '안'}
    ==================================================



```python

# 2. 문자 집합에 고유한 정수를 부여
char_to_index = dict((c, i) for i, c in enumerate(char_vocab)) # 문자에 고유한 정수 인덱스 부여
print("Char to index = \n", char_to_index)

index_to_char = dict((i, c) for i, c in enumerate(char_vocab)) # 문자에 고유한 정수 인덱스 부여
print("Idx to char = \n",index_to_char)
print("="*50)

```

    Char to index = 
     {' ': 0, '!': 1, '녕': 2, '러': 3, '분': 4, '세': 5, '안': 6, '여': 7, '요': 8, '하': 9}
    Idx to char = 
     {0: ' ', 1: '!', 2: '녕', 3: '러', 4: '분', 5: '세', 6: '안', 7: '여', 8: '요', 9: '하'}
    ==================================================



```python

# 3. Label encoding
x_data = [char_to_index[c] for c in input_str_kr]
y_data = [char_to_index[c] for c in label_str_kr]

# 배치 차원 추가
x_data = [x_data]
y_data = [y_data]

print("Label encoding = \n")
print("input_str = \n", x_data)
print("output_str = \n",y_data)
print("="*50)

```

    Label encoding = 
    
    input_str = 
     [[6, 2, 9, 5, 8, 0, 7, 3, 4]]
    output_str = 
     [[2, 9, 5, 8, 0, 7, 3, 4, 1]]
    ==================================================



```python

# 4. Onehot encoding 
print('input_str One hot encoding =')
# x_one_hot = [np.eye(vocab_size)[x] for x in x_data]
x_one_hot = np.eye(vocab_size)[x_data]
print(x_one_hot)

```

    input_str One hot encoding =
    [[[0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
      [0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
      [0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
      [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]
      [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
      [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
      [0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]
      [0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
      [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]]]



```python

# 5. Tensor vector
X = torch.FloatTensor(x_one_hot)
Y = torch.LongTensor(y_data)
print('훈련 데이터의 크기 : {}'.format(X.shape))
print('레이블의 크기 : {}'.format(Y.shape))
print(X)
print(Y)
```

    훈련 데이터의 크기 : torch.Size([1, 9, 10])
    레이블의 크기 : torch.Size([1, 9])
    tensor([[[0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
             [0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
             [0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
             [0., 0., 0., 0., 0., 1., 0., 0., 0., 0.],
             [0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
             [1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
             [0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
             [0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
             [0., 0., 0., 0., 1., 0., 0., 0., 0., 0.]]])
    tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]])



```python
# 5. Model
vocab_size = len(char_vocab)
input_size = vocab_size # 입력의 크기는 문자 집합의 크기
hidden_size = 20
output_size = vocab_size
learning_rate = 0.1

class VanillaRNN_Kor(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(VanillaRNN_Kor, self).__init__()
        self.rnn = torch.nn.RNN(input_size, hidden_size, batch_first=True) # RNN 셀 구현
        self.fc = torch.nn.Linear(hidden_size, output_size, bias=True) # 출력층 구현

    def forward(self, x): # 구현한 RNN 셀과 출력층을 연결
        x, _status = self.rnn(x)
        x = self.fc(x)
        return x

net = VanillaRNN_Kor(input_size, hidden_size, output_size)
print("RNN parameters = \n", net.parameters)
# list(net.parameters())

outputs = net(X)
print(outputs.shape) # 3차원 텐서
# print(outputs)
criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), learning_rate)

for i in range(100):
    
    outputs = net(X)
    loss = criterion(outputs.view(-1, input_size), Y.view(-1)) # view를 하는 이유는 Batch 차원 제거를 위해
    # loss = criterion(outputs, Y) # view를 하는 이유는 Batch 차원 제거를 위해, doesnot work

    optimizer.zero_grad()
    loss.backward() # 기울기 계산
    optimizer.step() # 아까 optimizer 선언 시 넣어둔 파라미터 업데이트

    # 아래 세 줄은 모델이 실제 어떻게 예측했는지를 확인하기 위한 코드.
    result = outputs.argmax(axis=2) # 최종 예측값인 각 time-step 별 5차원 벡터에 대해서 가장 높은 값의 인덱스를 선택
    result_str = ''.join([index_to_char[c] for c in np.squeeze(result.numpy())]) # np.squeeze(result.numpy()) : 1d vector
    print(i, "loss: ", loss.item(), "prediction: ", result, "true Y: ", y_data, "prediction str: ", result_str)
```

    RNN parameters = 
     <bound method Module.parameters of VanillaRNN_Kor(
      (rnn): RNN(10, 20, batch_first=True)
      (fc): Linear(in_features=20, out_features=10, bias=True)
    )>
    torch.Size([1, 9, 10])
    0 loss:  2.2905445098876953 prediction:  tensor([[8, 1, 1, 1, 8, 7, 8, 8, 8]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  요!!!요여요요요
    1 loss:  1.9417288303375244 prediction:  tensor([[3, 9, 7, 7, 0, 7, 7, 7, 7]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  러하여여 여여여여
    2 loss:  1.3427523374557495 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 9, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러하!
    3 loss:  0.6551940441131592 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    4 loss:  0.22501195967197418 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    5 loss:  0.07384788990020752 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    6 loss:  0.027078425511717796 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    7 loss:  0.011597594246268272 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    8 loss:  0.005739525426179171 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    9 loss:  0.0031857499852776527 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    10 loss:  0.0019389488734304905 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    11 loss:  0.00127002177760005 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    12 loss:  0.0008811643347144127 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    13 loss:  0.0006393386283889413 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    14 loss:  0.000480061920825392 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    15 loss:  0.000370307156117633 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    16 loss:  0.00029168950277380645 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    17 loss:  0.00023355244775302708 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    18 loss:  0.00018953466496896 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    19 loss:  0.00015568113303743303 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    20 loss:  0.00012931933451909572 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    21 loss:  0.00010866307275136933 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    22 loss:  9.233588934876025e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    23 loss:  7.954380271257833e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    24 loss:  6.945282802917063e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    25 loss:  6.140103505458683e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    26 loss:  5.499126564245671e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    27 loss:  4.982627433491871e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    28 loss:  4.558827276923694e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    29 loss:  4.206539233564399e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    30 loss:  3.913846376235597e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    31 loss:  3.655584805528633e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    32 loss:  3.442351953708567e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    33 loss:  3.255607225582935e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    34 loss:  3.0900522688170895e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    35 loss:  2.9443626772263087e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    36 loss:  2.8158912755316123e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    37 loss:  2.69933880190365e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    38 loss:  2.5907327653840184e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    39 loss:  2.4980205125757493e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    40 loss:  2.4092809326248243e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    41 loss:  2.3258391593117267e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    42 loss:  2.2543175873579457e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    43 loss:  2.1854448277736083e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    44 loss:  2.1218695110292174e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    45 loss:  2.0675659470725805e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    46 loss:  2.0159110135864466e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    47 loss:  1.9642558982013725e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    48 loss:  1.917898771353066e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    49 loss:  1.874191002571024e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    50 loss:  1.8357806766289286e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    51 loss:  1.800019344955217e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    52 loss:  1.7616090190131217e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    53 loss:  1.729821269691456e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    54 loss:  1.6967089322861284e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    55 loss:  1.6675699953339063e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    56 loss:  1.6410798707511276e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    57 loss:  1.6119409337989055e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    58 loss:  1.589424573467113e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    59 loss:  1.565583261253778e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    60 loss:  1.5430669009219855e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    61 loss:  1.520550449640723e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    62 loss:  1.500682901678374e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    63 loss:  1.4834644389338791e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    64 loss:  1.4635967090725899e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    65 loss:  1.4477027434622869e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    66 loss:  1.430484280717792e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    67 loss:  1.4172393093758728e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    68 loss:  1.4013450709171593e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    69 loss:  1.3828020200890023e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    70 loss:  1.3682325516128913e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    71 loss:  1.3496893188857939e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    72 loss:  1.3377688446780667e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    73 loss:  1.3231991943030152e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    74 loss:  1.31260321722948e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    75 loss:  1.3020072401559446e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    76 loss:  1.2887620869150851e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    77 loss:  1.2781661098415498e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    78 loss:  1.2649209566006903e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    79 loss:  1.2543248885776848e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    80 loss:  1.2437288205546793e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    81 loss:  1.2344572496658657e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    82 loss:  1.2238611816428602e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    83 loss:  1.2159141078882385e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    84 loss:  1.2092917131667491e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    85 loss:  1.1960464689764194e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    86 loss:  1.1880993952217977e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    87 loss:  1.1801524124166463e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    88 loss:  1.1708808415278327e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    89 loss:  1.1642581739579327e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    90 loss:  1.1549866030691192e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    91 loss:  1.1483642083476298e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    92 loss:  1.1404171345930081e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    93 loss:  1.1324700608383864e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    94 loss:  1.1258475751674268e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    95 loss:  1.1192250894964673e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    96 loss:  1.1112779247923754e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    97 loss:  1.1073044333897997e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    98 loss:  1.1006819477188401e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!
    99 loss:  1.0940592801489402e-05 prediction:  tensor([[2, 9, 5, 8, 0, 7, 3, 4, 1]]) true Y:  [[2, 9, 5, 8, 0, 7, 3, 4, 1]] prediction str:  녕하세요 여러분!


# LSTM을 이용한 네이버 영화 리뷰 분류


```python
import pandas as pd
from urllib import request
```

### LSTM 모델 확인하기


```python
## parameter 
input_dim = 5
hidden_size = 3

# (batch_size, time_steps, input_size)
inputs = torch.rand(1, 3, 5)
print(inputs)
print(inputs.dtype)
```

    tensor([[[0.7100, 0.9957, 0.4907, 0.9389, 0.7806],
             [0.3214, 0.4088, 0.0813, 0.1504, 0.1035],
             [0.4708, 0.6658, 0.8689, 0.5481, 0.7580]]])
    torch.float32



```python

input_dim = 5
hidden_size = 3
lstm = nn.LSTM(input_dim, hidden_size, batch_first=True)
```


```python
lstm = nn.LSTM(input_dim, hidden_size, batch_first=True)
print(list(lstm.parameters()))
```

    [Parameter containing:
    tensor([[ 0.5397,  0.5626,  0.3286,  0.3228,  0.2959],
            [ 0.0164, -0.2817, -0.3701, -0.3762,  0.5716],
            [ 0.2709, -0.1316, -0.2345,  0.3070, -0.0737],
            [-0.5672,  0.5385,  0.0761, -0.2042,  0.1676],
            [ 0.0562, -0.2714,  0.2077,  0.3398, -0.0219],
            [-0.1687,  0.1323, -0.2917,  0.5124,  0.2712],
            [-0.2456, -0.2141,  0.5528,  0.5555,  0.1807],
            [-0.5257, -0.1093,  0.0794,  0.4418,  0.4990],
            [ 0.1540,  0.5476,  0.5192,  0.3305,  0.3985],
            [-0.4080,  0.1440, -0.2368,  0.4245, -0.5680],
            [-0.1213, -0.3567,  0.1859,  0.3139,  0.2983],
            [ 0.5680, -0.4044,  0.0663, -0.1984,  0.2319]], requires_grad=True), Parameter containing:
    tensor([[-0.0327, -0.2666, -0.3233],
            [ 0.0801, -0.3055, -0.4298],
            [ 0.4196, -0.4396, -0.5388],
            [-0.4854, -0.3523, -0.5207],
            [-0.0070, -0.3771, -0.0437],
            [-0.4638,  0.0256, -0.3320],
            [ 0.2137,  0.5540, -0.2854],
            [-0.1279,  0.5377,  0.1945],
            [-0.3493, -0.1414, -0.4543],
            [ 0.4033, -0.0952,  0.2715],
            [ 0.5465, -0.2416, -0.4925],
            [ 0.4804,  0.4602,  0.5591]], requires_grad=True), Parameter containing:
    tensor([ 0.3275, -0.1922,  0.4263,  0.3348,  0.0428,  0.4898,  0.2103, -0.4981,
             0.3870, -0.2937, -0.3315, -0.3669], requires_grad=True), Parameter containing:
    tensor([ 0.0531,  0.0546, -0.1629, -0.4639,  0.2123,  0.3096,  0.0634, -0.1233,
             0.2790, -0.3386,  0.3839,  0.5220], requires_grad=True)]


### 데이터 다운 로드


```python
# 데이터 로드하기
# 각 각 ratings_train.txt, ratings_test.txt 저장
request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", 
                    filename="ratings_train.txt")
request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", 
                    filename="ratings_test.txt")
```




    ('ratings_test.txt', <http.client.HTTPMessage at 0x2c0172d5550>)




```python
train_data = pd.read_table('ratings_train.txt', sep = "\t", nrows = 10000)
test_data = pd.read_table('ratings_test.txt', sep = "\t", nrows = 10000)
print('총 샘플의 수 :',len(train_data))
train_data.head()
```

    총 샘플의 수 : 10000





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>document</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9976970</td>
      <td>아 더빙.. 진짜 짜증나네요 목소리</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3819312</td>
      <td>흠...포스터보고 초딩영화줄....오버연기조차 가볍지 않구나</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10265843</td>
      <td>너무재밓었다그래서보는것을추천한다</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9045019</td>
      <td>교도소 이야기구먼 ..솔직히 재미는 없다..평점 조정</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6483659</td>
      <td>사이몬페그의 익살스런 연기가 돋보였던 영화!스파이더맨에서 늙어보이기만 했던 커스틴 ...</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### 데이터 전처리


```python
train_data.dropna(inplace=True, how = "any")
train_data.drop_duplicates(subset=['document'], inplace=True)
print('총 샘플의 수 :',len(train_data)) 
train_data.head()
```

    총 샘플의 수 : 9918





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>document</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9976970</td>
      <td>아 더빙.. 진짜 짜증나네요 목소리</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3819312</td>
      <td>흠...포스터보고 초딩영화줄....오버연기조차 가볍지 않구나</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10265843</td>
      <td>너무재밓었다그래서보는것을추천한다</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9045019</td>
      <td>교도소 이야기구먼 ..솔직히 재미는 없다..평점 조정</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6483659</td>
      <td>사이몬페그의 익살스런 연기가 돋보였던 영화!스파이더맨에서 늙어보이기만 했던 커스틴 ...</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
### 한글과 공백을 제외하고 모두 제거
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]"," ",
                                                             regex=True)
train_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>document</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9976970</td>
      <td>아 더빙   진짜 짜증나네요 목소리</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3819312</td>
      <td>흠   포스터보고 초딩영화줄    오버연기조차 가볍지 않구나</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10265843</td>
      <td>너무재밓었다그래서보는것을추천한다</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9045019</td>
      <td>교도소 이야기구먼   솔직히 재미는 없다  평점 조정</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6483659</td>
      <td>사이몬페그의 익살스런 연기가 돋보였던 영화 스파이더맨에서 늙어보이기만 했던 커스틴 ...</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
### 빈자료 제거
train_data['document'] = train_data['document'].str.strip()
train_data['document'] = train_data['document'].replace('', np.nan)
train_data.dropna(how = 'any', inplace=True)
print(train_data.isnull().sum())
print(train_data.shape) # (145393, 3)
```

    id          0
    document    0
    label       0
    dtype: int64
    (9858, 3)


### 토큰화 (Tokenizing)


```python
!pip install konlpy
```


```python
from konlpy.tag import Okt
from tqdm import tqdm
```


```python
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
okt = Okt()
okt.morphs("교도소 이야기구먼 솔직히 재미는 없다평점 조정")
```




    ['교도소', '이야기', '구먼', '솔직히', '재미', '는', '없다', '평점', '조정']




```python
X_data = []
for sentence in tqdm(train_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_data.append(stopwords_removed_sentence)
```

    100%|██████████| 9858/9858 [00:46<00:00, 211.89it/s]



```python
y_data = train_data['label']

print(len(X_data))
print(len(y_data))

print(X_data[:5])
print(y_data[:5])
```

    9858
    9858
    [['아', '더빙', '진짜', '짜증나다', '목소리'], ['흠', '포스터', '보고', '초딩', '영화', '줄', '오버', '연기', '조차', '가볍다', '않다'], ['너', '무재', '밓었', '다그', '래서', '보다', '추천'], ['교도소', '이야기', '구먼', '솔직하다', '재미', '없다', '평점', '조정'], ['사이', '몬페', '그', '익살스럽다', '연기', '돋보이다', '영화', '스파이더맨', '에서', '늙다', '보이다', '하다', '커스틴', '던스트', '너무나도', '이쁘다', '보이다']]
    0    0
    1    1
    2    0
    3    0
    4    1
    Name: label, dtype: int64


### 학습데이터, 검증데이터


```python
from sklearn.model_selection import train_test_split

X_train, X_valid, y_train, y_valid = train_test_split(X_data, y_data, test_size=0.2, 
                                                      random_state=0, stratify=y_data)
print("X_train shape = ", len(X_train))
print("X_valid shape = ", len(X_valid))
print("y_train shape = ", len(y_train))
print("y_valid shape = ", len(y_valid))

```

    X_train shape =  7886
    X_valid shape =  1972
    y_train shape =  7886
    y_valid shape =  1972


### 단어 집합 만들기


```python
from collections import Counter

word_list = []
for sent in X_train:
    for word in sent:
      word_list.append(word)

word_counts = Counter(word_list) # == len(set(word_list))
print('총 단어수 :', len(word_counts))
display(word_counts)

```

    총 단어수 : 10876



    Counter({'영화': 2678,
             '보다': 2244,
             '하다': 2241,
             '없다': 858,
             '이다': 733,
             '있다': 675,
             '좋다': 579,
             '정말': 537,
             '너무': 526,
             '만': 497,
             '재밌다': 477,
             '같다': 471,
             '점': 466,
             '되다': 461,
             '적': 456,
             '진짜': 440,
             '아니다': 420,
             '으로': 416,
             '로': 406,
             '않다': 385,
             '나오다': 364,
             '연기': 363,
             '에서': 362,
             '만들다': 335,
             '평점': 334,
             '나': 323,
             '최고': 322,
             '것': 322,
             '내': 318,
             '안': 317,
             '그': 310,
             '못': 293,
             '사람': 280,
             '스토리': 274,
             '드라마': 273,
             '왜': 271,
             '보고': 265,
             '감동': 258,
             '생각': 255,
             '감독': 249,
             '말': 248,
             '이렇다': 247,
             '때': 246,
             'ㅋㅋ': 238,
             '그냥': 237,
             '아깝다': 236,
             '아': 234,
             '거': 229,
             '재미없다': 224,
             '시간': 223,
             '배우': 217,
             '더': 215,
             '내용': 213,
             '중': 213,
             '재미': 211,
             '요': 211,
             '자다': 204,
             '지루하다': 200,
             '가다': 196,
             '까지': 194,
             '재미있다': 192,
             '하고': 191,
             '뭐': 187,
             '들다': 185,
             '모르다': 183,
             '주다': 182,
             '작품': 181,
             '쓰레기': 179,
             '수': 175,
             '좀': 171,
             '알다': 166,
             '사랑': 158,
             '하나': 158,
             '볼': 157,
             '싶다': 157,
             '이건': 152,
             'ㅋ': 150,
             '잘': 149,
             '마지막': 146,
             '정도': 146,
             '그렇다': 146,
             '개': 145,
             '차다': 139,
             '액션': 138,
             '연출': 138,
             '돈': 138,
             '이렇게': 135,
             '저': 134,
             '다시': 134,
             '걸': 132,
             '주인공': 131,
             '최악': 130,
             '안되다': 130,
             '지금': 128,
             '완전': 127,
             '기': 127,
             '많다': 124,
             '나다': 124,
             '받다': 123,
             '느낌': 123,
             '오다': 122,
             '처음': 121,
             '장면': 120,
             'ㅠㅠ': 120,
             '역시': 119,
             'ㅋㅋㅋ': 117,
             '별': 116,
             '명작': 116,
             '이야기': 114,
             '인데': 112,
             '라': 112,
             '넘다': 110,
             '별로': 110,
             '부터': 110,
             '일': 109,
             'ㅡㅡ': 108,
             '면': 106,
             '먹다': 106,
             '남다': 105,
             '이나': 105,
             '좋아하다': 101,
             '꼭': 101,
             '괜찮다': 100,
             '년': 100,
             '버리다': 99,
             '또': 99,
             '아름답다': 98,
             '인생': 97,
             '이해': 97,
             '끝': 97,
             '난': 95,
             '느끼다': 95,
             '라고': 95,
             '이영화': 95,
             '이런': 94,
             '무슨': 92,
             '그리고': 92,
             '멋지다': 92,
             '해주다': 91,
             '야': 90,
             '서': 90,
             '전': 90,
             '줄': 89,
             '많이': 89,
             '마음': 88,
             '대': 87,
             '한번': 87,
             '여': 87,
             '때문': 87,
             '결말': 87,
             '허다': 86,
             '알': 86,
             '가슴': 86,
             '어떻다': 85,
             '편': 85,
             '분': 85,
             '소재': 85,
             '에게': 85,
             '뻔하다': 85,
             '엔': 84,
             '두': 84,
             '어리다': 84,
             '없이': 81,
             '영': 81,
             '라는': 81,
             '이고': 81,
             '성': 80,
             '속': 80,
             '되어다': 80,
             '씨': 80,
             '인간': 79,
             '모든': 79,
             '가장': 79,
             '아쉽다': 79,
             '죽다': 78,
             '냐': 78,
             '랑': 78,
             '지만': 76,
             '기억': 76,
             '끝나다': 76,
             'ㅠ': 76,
             '짱': 75,
             '보기': 75,
             '끄다': 74,
             '뿐': 74,
             '웃기다': 74,
             '님': 74,
             '남자': 74,
             '유치하다': 74,
             '크다': 74,
             '솔직하다': 73,
             'ㅎㅎ': 73,
             '매력': 73,
             '하지만': 73,
             '보여주다': 72,
             '쓰다': 72,
             '늘다': 71,
             '니': 71,
             '높다': 70,
             '자체': 70,
             '애': 69,
             '실망': 69,
             '여자': 69,
             '캐릭터': 69,
             '수준': 69,
             '번': 69,
             '반전': 68,
             '전개': 68,
             '화': 68,
             '무섭다': 68,
             '제': 67,
             '본': 67,
             '우리': 67,
             '살다': 66,
             '찍다': 66,
             '지다': 65,
             '현실': 65,
             '급': 65,
             '추천': 64,
             '공감': 63,
             '낮다': 63,
             '대한': 63,
             '맞다': 63,
             '재다': 62,
             '이상': 62,
             'ㅋㅋㅋㅋ': 61,
             '함': 61,
             '개봉': 61,
             '뭔가': 60,
             '눈물': 60,
             '인지': 60,
             '대단하다': 59,
             '계속': 59,
             '코미디': 59,
             '음악': 59,
             '눈': 58,
             '슬프다': 58,
             '전혀': 58,
             '이라': 58,
             '근데': 58,
             '다른': 58,
             '짜증나다': 58,
             '움': 58,
             '돼다': 58,
             '빠지다': 58,
             '말다': 57,
             '제목': 57,
             '밖에': 57,
             '처럼': 57,
             '기대하다': 57,
             '건지다': 57,
             '인가': 56,
             '미치다': 56,
             'ㅜㅜ': 56,
             '욕': 56,
             '중간': 55,
             '기분': 55,
             '여운': 55,
             '시리즈': 54,
             '이란': 53,
             '표현': 53,
             '야하다': 53,
             '연기력': 53,
             '이네': 52,
             '감': 52,
             '내내': 52,
             '잇다': 52,
             '뭔': 52,
             '내다': 52,
             '굿': 52,
             '모두': 51,
             '믿다': 51,
             '이제': 51,
             '보이다': 51,
             '이라는': 51,
             '자': 50,
             '일본': 50,
             '작가': 50,
             '잼': 49,
             '이쁘다': 49,
             '원작': 49,
             '몰입': 49,
             '아이': 48,
             '영상': 48,
             '연': 48,
             '에는': 48,
             '이유': 48,
             'ㅡ': 48,
             '오랜': 48,
             '막장': 48,
             '걍': 48,
             '위': 48,
             '가족': 47,
             '작': 47,
             '아주': 47,
             '한국': 47,
             '나름': 47,
             '노잼': 47,
             '아직도': 47,
             '절대': 47,
             '력': 47,
             '특히': 47,
             '점도': 47,
             '요즘': 47,
             '후': 47,
             '스릴러': 46,
             '이딴': 46,
             '긴장감': 46,
             '웃다': 46,
             '수작': 46,
             '딱': 46,
             '이랑': 46,
             '대박': 46,
             '졸작': 45,
             '시키다': 45,
             '어': 45,
             '그래도': 45,
             '치다': 45,
             '애니': 45,
             '잔잔하다': 45,
             '너': 45,
             '친구': 45,
             '기대': 45,
             '깊다': 45,
             '귀엽다': 45,
             'ㅎ': 45,
             '짜다': 45,
             '찾다': 44,
             '느껴지다': 44,
             '물': 44,
             '진심': 44,
             '이라고': 44,
             '아프다': 44,
             '설정': 44,
             '접': 43,
             '모습': 43,
             '떨어지다': 43,
             '건': 43,
             '삶': 43,
             '보지': 43,
             '앞': 43,
             '부분': 43,
             '인상': 42,
             '문제': 42,
             '조금': 42,
             '용': 42,
             '당시': 42,
             '개인': 42,
             '놈': 42,
             '스럽다': 42,
             '빼다': 42,
             '포스터': 41,
             '한국영': 41,
             '따뜻하다': 41,
             '자신': 41,
             '몇': 41,
             '울다': 41,
             '멋있다': 41,
             '알바': 40,
             '년대': 40,
             '배경': 40,
             '추억': 40,
             '점수': 39,
             '초반': 39,
             '해보다': 39,
             '무엇': 39,
             '정신': 39,
             '필요없다': 39,
             '나가다': 39,
             '써다': 39,
             '데': 39,
             '류': 38,
             '에도': 38,
             '의미': 38,
             '신선하다': 38,
             '가지': 38,
             '예쁘다': 38,
             '제대로': 38,
             '세': 37,
             '식': 37,
             '시': 37,
             '우리나라': 37,
             '같이': 37,
             '웃음': 37,
             '제일': 37,
             '더럽다': 37,
             '안타깝다': 37,
             '극장': 37,
             '노래': 37,
             '영화로': 36,
             '쓸다': 36,
             '시나리오': 36,
             '한테': 36,
             '대사': 36,
             '캐스팅': 36,
             '질': 36,
             '결국': 36,
             '라면': 35,
             '반': 35,
             '공포': 35,
             '이지': 35,
             '티비': 35,
             '보단': 35,
             '따다': 35,
             '이상하다': 35,
             '나이': 35,
             '세상': 35,
             '기다': 35,
             '웃기': 35,
             '대다': 35,
             '도대체': 35,
             '책': 35,
             '사실': 35,
             '시작': 35,
             '시대': 35,
             '엄청': 35,
             '장난': 35,
             '원': 35,
             '부족하다': 34,
             '마다': 34,
             '이지만': 34,
             '대해': 34,
             '최고다': 34,
             '맘': 33,
             '기도': 33,
             '봄': 33,
             '평가': 33,
             '상': 33,
             '엄마': 33,
             '충분하다': 33,
             '훌륭하다': 33,
             '뭘': 33,
             '함께': 33,
             '이후': 33,
             '죽이다': 33,
             '두다': 33,
             '첨': 33,
             '완벽하다': 33,
             '음': 33,
             '그저': 32,
             '이야': 32,
             '몰입도': 32,
             '아무': 32,
             '답답하다': 32,
             '쯤': 32,
             '배우다': 32,
             '공포영화': 32,
             '엉': 32,
             '영화관': 32,
             '오': 32,
             '비다': 31,
             '집': 31,
             '망하다': 31,
             '살리다': 31,
             '극': 31,
             '놀라다': 31,
             '매우': 31,
             '누구': 31,
             '전쟁': 31,
             '남': 31,
             '얼마나': 31,
             '낫다': 31,
             '드리다': 31,
             '그리다': 30,
             '해': 30,
             '돌리다': 30,
             '씬': 30,
             '차라리': 30,
             '이라도': 30,
             '어설프다': 30,
             '누가': 30,
             '실화': 30,
             '관객': 30,
             '팬': 30,
             '간': 30,
             '억': 30,
             '엔딩': 30,
             '새롭다': 29,
             '한마디': 29,
             '꽤': 29,
             '영화인': 29,
             '필요하다': 29,
             '미국': 29,
             '읽다': 29,
             '힘들다': 29,
             '어색하다': 29,
             '위해': 29,
             '등': 29,
             '출연': 29,
             '후회': 29,
             '어디': 29,
             '아직': 29,
             '코믹': 29,
             '어울리다': 29,
             '건가': 29,
             '유쾌하다': 29,
             '그렇게': 28,
             '싫다': 28,
             '킬링타임': 28,
             '서다': 28,
             '소리': 28,
             '구': 28,
             '그대로': 28,
             '분위기': 28,
             '만큼': 28,
             '이르다': 28,
             '분들': 28,
             '밉다': 28,
             '코': 28,
             '오늘': 28,
             '생기다': 28,
             '그나마': 28,
             '대체': 27,
             '스릴': 27,
             '전부': 27,
             '그것': 27,
             '장르': 27,
             '충격': 27,
             '소름': 27,
             '갈수록': 27,
             '역사': 27,
             '구성': 27,
             '탄탄하다': 27,
             '잔인하다': 27,
             '심하다': 27,
             '회': 27,
             '애니메이션': 27,
             '명': 27,
             '놓다': 27,
             '살': 27,
             '부': 26,
             '바라다': 26,
             '생각나다': 26,
             '훨씬': 26,
             '옛날': 26,
             '여기': 26,
             '준': 26,
             '흥행': 26,
             '년도': 26,
             '여배우': 26,
             '로맨스': 26,
             '중국': 26,
             '뒤': 26,
             '시절': 26,
             '행복하다': 26,
             '좀비': 26,
             '라니': 26,
             '해도': 26,
             '화려하다': 26,
             '어이없다': 26,
             '주연': 25,
             '떠나다': 25,
             '머리': 25,
             '예술': 25,
             '쉬다': 25,
             '작다': 25,
             '날': 25,
             '오글거리다': 25,
             '만점': 25,
             '멀다': 25,
             '돋다': 25,
             '어느': 25,
             '총': 25,
             '강추': 25,
             '다큐': 25,
             '순간': 25,
             '엄청나다': 25,
             '답': 25,
             '제발': 25,
             '나쁘다': 25,
             '비디오': 25,
             '확실하다': 24,
             '지루함': 24,
             '약간': 24,
             '인물': 24,
             '비슷하다': 24,
             '복수': 24,
             '들이다': 24,
             '따르다': 24,
             '이름': 24,
             '즐겁다': 24,
             '편이': 24,
             '당하다': 24,
             '존재': 24,
             '상당하다': 24,
             '얼굴': 24,
             '달다': 24,
             '언제': 24,
             '걸리다': 24,
             '선택': 24,
             '걸작': 23,
             '개연': 23,
             '네이버': 23,
             'ㅉㅉ': 23,
             '머': 23,
             '당신': 23,
             '어디서': 23,
             '자기': 23,
             '소설': 23,
             '감정': 23,
             '짜증': 23,
             '년전': 23,
             '빨리': 23,
             '초딩': 23,
             '이리': 23,
             '그래서': 23,
             '발': 23,
             '얘기': 23,
             '죠': 23,
             '너무나': 23,
             '잊다': 23,
             '아무리': 23,
             '주제': 23,
             '만화': 22,
             '흠': 22,
             '갑자기': 22,
             '발연기': 22,
             '그만': 22,
             '사랑스럽다': 22,
             '타다': 22,
             '미화': 22,
             '최근': 22,
             '산': 22,
             '말고': 22,
             '아들': 22,
             '극장판': 22,
             '비추다': 22,
             '터지다': 22,
             '점주': 22,
             '그러나': 22,
             '다니다': 22,
             '장': 22,
             '맛': 22,
             '진': 22,
             '진부하다': 22,
             '흐르다': 22,
             '보내다': 22,
             '감사하다': 22,
             '판': 22,
             '불편하다': 22,
             '에선': 22,
             '상황': 22,
             '방송': 22,
             '순수하다': 21,
             '안보': 21,
             '곳': 21,
             '싸우다': 21,
             'ㅜ': 21,
             '만들어지다': 21,
             '울': 21,
             '완성': 21,
             '니까': 21,
             '전작': 21,
             '다운': 21,
             '어렵다': 21,
             '질질': 21,
             '에서도': 21,
             '맨': 21,
             '다르다': 21,
             '시즌': 21,
             '참고': 21,
             '휴': 21,
             '여주': 21,
             '졸라': 21,
             '진정하다': 20,
             '그런': 20,
             '라서': 20,
             '힘드다': 20,
             '에요': 20,
             '화이팅': 20,
             '화면': 20,
             '든': 20,
             '성룡': 20,
             '제작': 20,
             '비교': 20,
             '한편': 20,
             '수가': 20,
             '며': 20,
             '동안': 20,
             '끌다': 20,
             '꿈': 20,
             '사건': 20,
             '또한': 20,
             '래': 20,
             '몇번': 20,
             '궁금하다': 20,
             '원래': 20,
             '풀다': 20,
             '편집': 20,
             '막': 20,
             '뻔': 20,
             '왠만하다': 20,
             '엉망': 19,
             '단': 19,
             '가보다': 19,
             '께': 19,
             '담다': 19,
             '라도': 19,
             '존나': 19,
             '요소': 19,
             '게임': 19,
             '주': 19,
             '각본': 19,
             '선': 19,
             '거의': 19,
             '집중': 19,
             '똑같다': 19,
             '으로도': 19,
             '괜히': 19,
             '소중하다': 19,
             '평생': 19,
             '가볍다': 19,
             '뭐라다': 19,
             '간만': 19,
             '보다는': 19,
             '느와르': 19,
             '먼저': 19,
             '술': 19,
             '노력': 19,
             '재': 19,
             '무조건': 19,
             '만의': 19,
             '더빙': 19,
             '넘치다': 18,
             '굉장하다': 18,
             '물론': 18,
             '비': 18,
             '들어가다': 18,
             '재밋': 18,
             '힘': 18,
             '아버지': 18,
             '만으로도': 18,
             '케이블': 18,
             '살인': 18,
             '거리': 18,
             '몰다': 18,
             '혼자': 18,
             '약하다': 18,
             '키': 18,
             '얻다': 18,
             '무': 18,
             '흔하다': 18,
             '짧다': 18,
             '성하다': 18,
             '전체': 18,
             '상처': 18,
             '모': 18,
             'ㅇ': 18,
             '화가': 18,
             '피': 18,
             '사회': 18,
             '시청률': 18,
             '만나다': 18,
             '끼다': 18,
             '멜로': 18,
             '그녀': 18,
             '상미': 18,
             '남기다': 18,
             '적다': 18,
             '낭비': 18,
             '전편': 17,
             '만하': 17,
             '씩': 17,
             '아저씨': 17,
             '살아가다': 17,
             '상영': 17,
             '뛰어나다': 17,
             '보': 17,
             '점점': 17,
             '어른': 17,
             '소녀': 17,
             '새끼': 17,
             '한심하다': 17,
             '도저히': 17,
             '으리': 17,
             '취향': 17,
             '똥': 17,
             '인거': 17,
             '손': 17,
             '이기다': 17,
             '여성': 17,
             '황당하다': 17,
             '평': 17,
             '형': 17,
             '거지': 17,
             '흥미': 17,
             '강하다': 17,
             '열': 17,
             '묻다': 17,
             '통해': 17,
             '예전': 17,
             '세계': 17,
             '실제': 17,
             '동화': 17,
             '흥미롭다': 17,
             '몸': 16,
             '예상': 16,
             '후반': 16,
             '으로는': 16,
             '특유': 16,
             '땐': 16,
             '잡다': 16,
             '빨': 16,
             '항상': 16,
             '감성': 16,
             '생': 16,
             '바꾸다': 16,
             '위대하다': 16,
             '아빠': 16,
             '온': 16,
             '그때': 16,
             '차': 16,
             '조': 16,
             '찾아보다': 16,
             '개그': 16,
             '평론가': 16,
             '이하': 16,
             '언': 16,
             '암': 16,
             '란': 16,
             '즐기다': 16,
             '참신하다': 16,
             '중반': 16,
             '개다': 16,
             '안나': 16,
             '에겐': 16,
             '잃다': 16,
             '기다리다': 16,
             '간다': 16,
             '지나다': 16,
             '기억나다': 16,
             '까진': 16,
             '허무하다': 16,
             '배': 16,
             '꿀잼': 16,
             '자극': 16,
             '히': 16,
             '법': 16,
             '돌아가다': 16,
             '지키다': 16,
             '현재': 16,
             '계': 15,
             '진정': 15,
             '이번': 15,
             '하하': 15,
             '산만하다': 15,
             '삼류': 15,
             '억지': 15,
             '동': 15,
             '쩔다': 15,
             '독특하다': 15,
             '그게': 15,
             '걸다': 15,
             '딸': 15,
             '채널': 15,
             '노답': 15,
             '역겹다': 15,
             '깊이': 15,
             '성도': 15,
             '불쾌하다': 15,
             '굳이': 15,
             '끝내다': 15,
             '즈': 15,
             '의도': 15,
             '다루다': 15,
             '실망하다': 15,
             '목소리': 15,
             '안좋다': 15,
             '청춘': 15,
             '섬세하다': 15,
             '햇': 15,
             '나서다': 15,
             '헐다': 15,
             '범죄': 15,
             '에서는': 15,
             'ㅋㅋㅋㅋㅋ': 15,
             '가지다': 15,
             '올해': 15,
             '귀신': 15,
             '밑': 15,
             '역대': 15,
             '심심하다': 15,
             '예요': 15,
             '억지스럽다': 15,
             '다만': 15,
             '당': 15,
             '흥미진진': 15,
             '오빠': 15,
             '신': 15,
             '늦다': 15,
             '열심히': 15,
             '시도': 15,
             '빵점': 15,
             '돋보이다': 15,
             '조차': 15,
             '치고': 15,
             '죽음': 15,
             '싫어하다': 15,
             '설레다': 15,
             '일이': 15,
             '이에요': 15,
             '액션영화': 15,
             '반개': 15,
             '다시다': 15,
             '방법': 15,
             '죽': 15,
             '삼': 15,
             '자식': 15,
             '부르다': 14,
             '때리다': 14,
             '거기': 14,
             '리뷰': 14,
             '그래픽': 14,
             '귀': 14,
             '정서': 14,
             '표정': 14,
             '다행': 14,
             '어쩔': 14,
             '순': 14,
             '철학': 14,
             '글': 14,
             '미안하다': 14,
             '공': 14,
             '그닥': 14,
             '볼때': 14,
             '에게는': 14,
             'ㅈ': 14,
             '교훈': 14,
             '일단': 14,
             '이라니': 14,
             '바': 14,
             '더욱': 14,
             '갖다': 14,
             '필요': 14,
             'ㅠㅠㅠ': 14,
             '엿': 14,
             '결과': 14,
             '사극': 14,
             '흘리다': 14,
             '으': 14,
             '퀄리티': 14,
             '너무나도': 14,
             '나머지': 14,
             '기회': 14,
             '떼다': 14,
             '가면': 14,
             '결혼': 14,
             '티': 14,
             '챙기다': 14,
             '댓글': 14,
             '뛰다': 14,
             '겁나다': 14,
             '이며': 14,
             '학교': 14,
             '중요하다': 14,
             '군': 14,
             '견자단': 14,
             '전설': 14,
             '심': 14,
             '비극': 14,
             '바보': 14,
             '홍콩': 14,
             '만이': 14,
             '짓': 14,
             '가요': 14,
             '감다': 14,
             '일어나다': 14,
             '잊혀지다': 14,
             '손발': 14,
             '메세지': 14,
             '마무리': 14,
             '촬영': 14,
             '외': 14,
             '기적': 14,
             '비판': 13,
             '나르다': 13,
             '그런데': 13,
             '너무하다': 13,
             '개뿔': 13,
             '우울하다': 13,
             '쓰래': 13,
             '식상하다': 13,
             '성인': 13,
             '문화': 13,
             '상상': 13,
             '화보': 13,
             '개념': 13,
             '예산': 13,
             '스타일': 13,
             '진지하다': 13,
             '바로': 13,
             '다소': 13,
             '표절': 13,
             '가끔': 13,
             '연인': 13,
             '심리': 13,
             '리얼': 13,
             '희망': 13,
             '자연': 13,
             '로는': 13,
             ...})



```python
print('훈련 데이터에서의 단어 영화의 등장 횟수 :', word_counts['영화']) # class Counter (= dictionary)
print('훈련 데이터에서의 단어 공감의 등장 횟수 :', word_counts['공감'])
```

    훈련 데이터에서의 단어 영화의 등장 횟수 : 2678
    훈련 데이터에서의 단어 공감의 등장 횟수 : 63



```python
vocab = sorted(word_counts, key=word_counts.get, reverse=True)
vocab
```




    ['영화',
     '보다',
     '하다',
     '없다',
     '이다',
     '있다',
     '좋다',
     '정말',
     '너무',
     '만',
     '재밌다',
     '같다',
     '점',
     '되다',
     '적',
     '진짜',
     '아니다',
     '으로',
     '로',
     '않다',
     '나오다',
     '연기',
     '에서',
     '만들다',
     '평점',
     '나',
     '최고',
     '것',
     '내',
     '안',
     '그',
     '못',
     '사람',
     '스토리',
     '드라마',
     '왜',
     '보고',
     '감동',
     '생각',
     '감독',
     '말',
     '이렇다',
     '때',
     'ㅋㅋ',
     '그냥',
     '아깝다',
     '아',
     '거',
     '재미없다',
     '시간',
     '배우',
     '더',
     '내용',
     '중',
     '재미',
     '요',
     '자다',
     '지루하다',
     '가다',
     '까지',
     '재미있다',
     '하고',
     '뭐',
     '들다',
     '모르다',
     '주다',
     '작품',
     '쓰레기',
     '수',
     '좀',
     '알다',
     '사랑',
     '하나',
     '볼',
     '싶다',
     '이건',
     'ㅋ',
     '잘',
     '마지막',
     '정도',
     '그렇다',
     '개',
     '차다',
     '액션',
     '연출',
     '돈',
     '이렇게',
     '저',
     '다시',
     '걸',
     '주인공',
     '최악',
     '안되다',
     '지금',
     '완전',
     '기',
     '많다',
     '나다',
     '받다',
     '느낌',
     '오다',
     '처음',
     '장면',
     'ㅠㅠ',
     '역시',
     'ㅋㅋㅋ',
     '별',
     '명작',
     '이야기',
     '인데',
     '라',
     '넘다',
     '별로',
     '부터',
     '일',
     'ㅡㅡ',
     '면',
     '먹다',
     '남다',
     '이나',
     '좋아하다',
     '꼭',
     '괜찮다',
     '년',
     '버리다',
     '또',
     '아름답다',
     '인생',
     '이해',
     '끝',
     '난',
     '느끼다',
     '라고',
     '이영화',
     '이런',
     '무슨',
     '그리고',
     '멋지다',
     '해주다',
     '야',
     '서',
     '전',
     '줄',
     '많이',
     '마음',
     '대',
     '한번',
     '여',
     '때문',
     '결말',
     '허다',
     '알',
     '가슴',
     '어떻다',
     '편',
     '분',
     '소재',
     '에게',
     '뻔하다',
     '엔',
     '두',
     '어리다',
     '없이',
     '영',
     '라는',
     '이고',
     '성',
     '속',
     '되어다',
     '씨',
     '인간',
     '모든',
     '가장',
     '아쉽다',
     '죽다',
     '냐',
     '랑',
     '지만',
     '기억',
     '끝나다',
     'ㅠ',
     '짱',
     '보기',
     '끄다',
     '뿐',
     '웃기다',
     '님',
     '남자',
     '유치하다',
     '크다',
     '솔직하다',
     'ㅎㅎ',
     '매력',
     '하지만',
     '보여주다',
     '쓰다',
     '늘다',
     '니',
     '높다',
     '자체',
     '애',
     '실망',
     '여자',
     '캐릭터',
     '수준',
     '번',
     '반전',
     '전개',
     '화',
     '무섭다',
     '제',
     '본',
     '우리',
     '살다',
     '찍다',
     '지다',
     '현실',
     '급',
     '추천',
     '공감',
     '낮다',
     '대한',
     '맞다',
     '재다',
     '이상',
     'ㅋㅋㅋㅋ',
     '함',
     '개봉',
     '뭔가',
     '눈물',
     '인지',
     '대단하다',
     '계속',
     '코미디',
     '음악',
     '눈',
     '슬프다',
     '전혀',
     '이라',
     '근데',
     '다른',
     '짜증나다',
     '움',
     '돼다',
     '빠지다',
     '말다',
     '제목',
     '밖에',
     '처럼',
     '기대하다',
     '건지다',
     '인가',
     '미치다',
     'ㅜㅜ',
     '욕',
     '중간',
     '기분',
     '여운',
     '시리즈',
     '이란',
     '표현',
     '야하다',
     '연기력',
     '이네',
     '감',
     '내내',
     '잇다',
     '뭔',
     '내다',
     '굿',
     '모두',
     '믿다',
     '이제',
     '보이다',
     '이라는',
     '자',
     '일본',
     '작가',
     '잼',
     '이쁘다',
     '원작',
     '몰입',
     '아이',
     '영상',
     '연',
     '에는',
     '이유',
     'ㅡ',
     '오랜',
     '막장',
     '걍',
     '위',
     '가족',
     '작',
     '아주',
     '한국',
     '나름',
     '노잼',
     '아직도',
     '절대',
     '력',
     '특히',
     '점도',
     '요즘',
     '후',
     '스릴러',
     '이딴',
     '긴장감',
     '웃다',
     '수작',
     '딱',
     '이랑',
     '대박',
     '졸작',
     '시키다',
     '어',
     '그래도',
     '치다',
     '애니',
     '잔잔하다',
     '너',
     '친구',
     '기대',
     '깊다',
     '귀엽다',
     'ㅎ',
     '짜다',
     '찾다',
     '느껴지다',
     '물',
     '진심',
     '이라고',
     '아프다',
     '설정',
     '접',
     '모습',
     '떨어지다',
     '건',
     '삶',
     '보지',
     '앞',
     '부분',
     '인상',
     '문제',
     '조금',
     '용',
     '당시',
     '개인',
     '놈',
     '스럽다',
     '빼다',
     '포스터',
     '한국영',
     '따뜻하다',
     '자신',
     '몇',
     '울다',
     '멋있다',
     '알바',
     '년대',
     '배경',
     '추억',
     '점수',
     '초반',
     '해보다',
     '무엇',
     '정신',
     '필요없다',
     '나가다',
     '써다',
     '데',
     '류',
     '에도',
     '의미',
     '신선하다',
     '가지',
     '예쁘다',
     '제대로',
     '세',
     '식',
     '시',
     '우리나라',
     '같이',
     '웃음',
     '제일',
     '더럽다',
     '안타깝다',
     '극장',
     '노래',
     '영화로',
     '쓸다',
     '시나리오',
     '한테',
     '대사',
     '캐스팅',
     '질',
     '결국',
     '라면',
     '반',
     '공포',
     '이지',
     '티비',
     '보단',
     '따다',
     '이상하다',
     '나이',
     '세상',
     '기다',
     '웃기',
     '대다',
     '도대체',
     '책',
     '사실',
     '시작',
     '시대',
     '엄청',
     '장난',
     '원',
     '부족하다',
     '마다',
     '이지만',
     '대해',
     '최고다',
     '맘',
     '기도',
     '봄',
     '평가',
     '상',
     '엄마',
     '충분하다',
     '훌륭하다',
     '뭘',
     '함께',
     '이후',
     '죽이다',
     '두다',
     '첨',
     '완벽하다',
     '음',
     '그저',
     '이야',
     '몰입도',
     '아무',
     '답답하다',
     '쯤',
     '배우다',
     '공포영화',
     '엉',
     '영화관',
     '오',
     '비다',
     '집',
     '망하다',
     '살리다',
     '극',
     '놀라다',
     '매우',
     '누구',
     '전쟁',
     '남',
     '얼마나',
     '낫다',
     '드리다',
     '그리다',
     '해',
     '돌리다',
     '씬',
     '차라리',
     '이라도',
     '어설프다',
     '누가',
     '실화',
     '관객',
     '팬',
     '간',
     '억',
     '엔딩',
     '새롭다',
     '한마디',
     '꽤',
     '영화인',
     '필요하다',
     '미국',
     '읽다',
     '힘들다',
     '어색하다',
     '위해',
     '등',
     '출연',
     '후회',
     '어디',
     '아직',
     '코믹',
     '어울리다',
     '건가',
     '유쾌하다',
     '그렇게',
     '싫다',
     '킬링타임',
     '서다',
     '소리',
     '구',
     '그대로',
     '분위기',
     '만큼',
     '이르다',
     '분들',
     '밉다',
     '코',
     '오늘',
     '생기다',
     '그나마',
     '대체',
     '스릴',
     '전부',
     '그것',
     '장르',
     '충격',
     '소름',
     '갈수록',
     '역사',
     '구성',
     '탄탄하다',
     '잔인하다',
     '심하다',
     '회',
     '애니메이션',
     '명',
     '놓다',
     '살',
     '부',
     '바라다',
     '생각나다',
     '훨씬',
     '옛날',
     '여기',
     '준',
     '흥행',
     '년도',
     '여배우',
     '로맨스',
     '중국',
     '뒤',
     '시절',
     '행복하다',
     '좀비',
     '라니',
     '해도',
     '화려하다',
     '어이없다',
     '주연',
     '떠나다',
     '머리',
     '예술',
     '쉬다',
     '작다',
     '날',
     '오글거리다',
     '만점',
     '멀다',
     '돋다',
     '어느',
     '총',
     '강추',
     '다큐',
     '순간',
     '엄청나다',
     '답',
     '제발',
     '나쁘다',
     '비디오',
     '확실하다',
     '지루함',
     '약간',
     '인물',
     '비슷하다',
     '복수',
     '들이다',
     '따르다',
     '이름',
     '즐겁다',
     '편이',
     '당하다',
     '존재',
     '상당하다',
     '얼굴',
     '달다',
     '언제',
     '걸리다',
     '선택',
     '걸작',
     '개연',
     '네이버',
     'ㅉㅉ',
     '머',
     '당신',
     '어디서',
     '자기',
     '소설',
     '감정',
     '짜증',
     '년전',
     '빨리',
     '초딩',
     '이리',
     '그래서',
     '발',
     '얘기',
     '죠',
     '너무나',
     '잊다',
     '아무리',
     '주제',
     '만화',
     '흠',
     '갑자기',
     '발연기',
     '그만',
     '사랑스럽다',
     '타다',
     '미화',
     '최근',
     '산',
     '말고',
     '아들',
     '극장판',
     '비추다',
     '터지다',
     '점주',
     '그러나',
     '다니다',
     '장',
     '맛',
     '진',
     '진부하다',
     '흐르다',
     '보내다',
     '감사하다',
     '판',
     '불편하다',
     '에선',
     '상황',
     '방송',
     '순수하다',
     '안보',
     '곳',
     '싸우다',
     'ㅜ',
     '만들어지다',
     '울',
     '완성',
     '니까',
     '전작',
     '다운',
     '어렵다',
     '질질',
     '에서도',
     '맨',
     '다르다',
     '시즌',
     '참고',
     '휴',
     '여주',
     '졸라',
     '진정하다',
     '그런',
     '라서',
     '힘드다',
     '에요',
     '화이팅',
     '화면',
     '든',
     '성룡',
     '제작',
     '비교',
     '한편',
     '수가',
     '며',
     '동안',
     '끌다',
     '꿈',
     '사건',
     '또한',
     '래',
     '몇번',
     '궁금하다',
     '원래',
     '풀다',
     '편집',
     '막',
     '뻔',
     '왠만하다',
     '엉망',
     '단',
     '가보다',
     '께',
     '담다',
     '라도',
     '존나',
     '요소',
     '게임',
     '주',
     '각본',
     '선',
     '거의',
     '집중',
     '똑같다',
     '으로도',
     '괜히',
     '소중하다',
     '평생',
     '가볍다',
     '뭐라다',
     '간만',
     '보다는',
     '느와르',
     '먼저',
     '술',
     '노력',
     '재',
     '무조건',
     '만의',
     '더빙',
     '넘치다',
     '굉장하다',
     '물론',
     '비',
     '들어가다',
     '재밋',
     '힘',
     '아버지',
     '만으로도',
     '케이블',
     '살인',
     '거리',
     '몰다',
     '혼자',
     '약하다',
     '키',
     '얻다',
     '무',
     '흔하다',
     '짧다',
     '성하다',
     '전체',
     '상처',
     '모',
     'ㅇ',
     '화가',
     '피',
     '사회',
     '시청률',
     '만나다',
     '끼다',
     '멜로',
     '그녀',
     '상미',
     '남기다',
     '적다',
     '낭비',
     '전편',
     '만하',
     '씩',
     '아저씨',
     '살아가다',
     '상영',
     '뛰어나다',
     '보',
     '점점',
     '어른',
     '소녀',
     '새끼',
     '한심하다',
     '도저히',
     '으리',
     '취향',
     '똥',
     '인거',
     '손',
     '이기다',
     '여성',
     '황당하다',
     '평',
     '형',
     '거지',
     '흥미',
     '강하다',
     '열',
     '묻다',
     '통해',
     '예전',
     '세계',
     '실제',
     '동화',
     '흥미롭다',
     '몸',
     '예상',
     '후반',
     '으로는',
     '특유',
     '땐',
     '잡다',
     '빨',
     '항상',
     '감성',
     '생',
     '바꾸다',
     '위대하다',
     '아빠',
     '온',
     '그때',
     '차',
     '조',
     '찾아보다',
     '개그',
     '평론가',
     '이하',
     '언',
     '암',
     '란',
     '즐기다',
     '참신하다',
     '중반',
     '개다',
     '안나',
     '에겐',
     '잃다',
     '기다리다',
     '간다',
     '지나다',
     '기억나다',
     '까진',
     '허무하다',
     '배',
     '꿀잼',
     '자극',
     '히',
     '법',
     '돌아가다',
     '지키다',
     '현재',
     '계',
     '진정',
     '이번',
     '하하',
     '산만하다',
     '삼류',
     '억지',
     '동',
     '쩔다',
     '독특하다',
     '그게',
     '걸다',
     '딸',
     '채널',
     '노답',
     '역겹다',
     '깊이',
     '성도',
     '불쾌하다',
     '굳이',
     '끝내다',
     '즈',
     '의도',
     '다루다',
     '실망하다',
     '목소리',
     '안좋다',
     '청춘',
     '섬세하다',
     '햇',
     '나서다',
     '헐다',
     '범죄',
     '에서는',
     'ㅋㅋㅋㅋㅋ',
     '가지다',
     '올해',
     '귀신',
     '밑',
     '역대',
     '심심하다',
     '예요',
     '억지스럽다',
     '다만',
     '당',
     '흥미진진',
     '오빠',
     '신',
     '늦다',
     '열심히',
     '시도',
     '빵점',
     '돋보이다',
     '조차',
     '치고',
     '죽음',
     '싫어하다',
     '설레다',
     '일이',
     '이에요',
     '액션영화',
     '반개',
     '다시다',
     '방법',
     '죽',
     '삼',
     '자식',
     '부르다',
     '때리다',
     '거기',
     '리뷰',
     '그래픽',
     '귀',
     '정서',
     '표정',
     '다행',
     '어쩔',
     '순',
     '철학',
     '글',
     '미안하다',
     '공',
     '그닥',
     '볼때',
     '에게는',
     'ㅈ',
     '교훈',
     '일단',
     '이라니',
     '바',
     '더욱',
     '갖다',
     '필요',
     'ㅠㅠㅠ',
     '엿',
     '결과',
     '사극',
     '흘리다',
     '으',
     '퀄리티',
     '너무나도',
     '나머지',
     '기회',
     '떼다',
     '가면',
     '결혼',
     '티',
     '챙기다',
     '댓글',
     '뛰다',
     '겁나다',
     '이며',
     '학교',
     '중요하다',
     '군',
     '견자단',
     '전설',
     '심',
     '비극',
     '바보',
     '홍콩',
     '만이',
     '짓',
     '가요',
     '감다',
     '일어나다',
     '잊혀지다',
     '손발',
     '메세지',
     '마무리',
     '촬영',
     '외',
     '기적',
     '비판',
     '나르다',
     '그런데',
     '너무하다',
     '개뿔',
     '우울하다',
     '쓰래',
     '식상하다',
     '성인',
     '문화',
     '상상',
     '화보',
     '개념',
     '예산',
     '스타일',
     '진지하다',
     '바로',
     '다소',
     '표절',
     '가끔',
     '연인',
     '심리',
     '리얼',
     '희망',
     '자연',
     '로는',
     ...]




```python
### 
word_to_index = {}
word_to_index['<PAD>'] = 0
word_to_index['<UNK>'] = 1

for index, word in enumerate(vocab) :
  word_to_index[word] = index + 2

vocab_size = len(word_to_index)
print('패딩 토큰과 UNK 토큰을 고려한 단어 집합의 크기 :', vocab_size)
```

    패딩 토큰과 UNK 토큰을 고려한 단어 집합의 크기 : 10878



```python
print(word_to_index)
print('단어 <PAD>와 맵핑되는 정수 :', word_to_index['<PAD>'])
print('단어 <UNK>와 맵핑되는 정수 :', word_to_index['<UNK>'])
print('단어 영화와 맵핑되는 정수 :', word_to_index['영화'])
```

    {'<PAD>': 0, '<UNK>': 1, '영화': 2, '보다': 3, '하다': 4, '없다': 5, '이다': 6, '있다': 7, '좋다': 8, '정말': 9, '너무': 10, '만': 11, '재밌다': 12, '같다': 13, '점': 14, '되다': 15, '적': 16, '진짜': 17, '아니다': 18, '으로': 19, '로': 20, '않다': 21, '나오다': 22, '연기': 23, '에서': 24, '만들다': 25, '평점': 26, '나': 27, '최고': 28, '것': 29, '내': 30, '안': 31, '그': 32, '못': 33, '사람': 34, '스토리': 35, '드라마': 36, '왜': 37, '보고': 38, '감동': 39, '생각': 40, '감독': 41, '말': 42, '이렇다': 43, '때': 44, 'ㅋㅋ': 45, '그냥': 46, '아깝다': 47, '아': 48, '거': 49, '재미없다': 50, '시간': 51, '배우': 52, '더': 53, '내용': 54, '중': 55, '재미': 56, '요': 57, '자다': 58, '지루하다': 59, '가다': 60, '까지': 61, '재미있다': 62, '하고': 63, '뭐': 64, '들다': 65, '모르다': 66, '주다': 67, '작품': 68, '쓰레기': 69, '수': 70, '좀': 71, '알다': 72, '사랑': 73, '하나': 74, '볼': 75, '싶다': 76, '이건': 77, 'ㅋ': 78, '잘': 79, '마지막': 80, '정도': 81, '그렇다': 82, '개': 83, '차다': 84, '액션': 85, '연출': 86, '돈': 87, '이렇게': 88, '저': 89, '다시': 90, '걸': 91, '주인공': 92, '최악': 93, '안되다': 94, '지금': 95, '완전': 96, '기': 97, '많다': 98, '나다': 99, '받다': 100, '느낌': 101, '오다': 102, '처음': 103, '장면': 104, 'ㅠㅠ': 105, '역시': 106, 'ㅋㅋㅋ': 107, '별': 108, '명작': 109, '이야기': 110, '인데': 111, '라': 112, '넘다': 113, '별로': 114, '부터': 115, '일': 116, 'ㅡㅡ': 117, '면': 118, '먹다': 119, '남다': 120, '이나': 121, '좋아하다': 122, '꼭': 123, '괜찮다': 124, '년': 125, '버리다': 126, '또': 127, '아름답다': 128, '인생': 129, '이해': 130, '끝': 131, '난': 132, '느끼다': 133, '라고': 134, '이영화': 135, '이런': 136, '무슨': 137, '그리고': 138, '멋지다': 139, '해주다': 140, '야': 141, '서': 142, '전': 143, '줄': 144, '많이': 145, '마음': 146, '대': 147, '한번': 148, '여': 149, '때문': 150, '결말': 151, '허다': 152, '알': 153, '가슴': 154, '어떻다': 155, '편': 156, '분': 157, '소재': 158, '에게': 159, '뻔하다': 160, '엔': 161, '두': 162, '어리다': 163, '없이': 164, '영': 165, '라는': 166, '이고': 167, '성': 168, '속': 169, '되어다': 170, '씨': 171, '인간': 172, '모든': 173, '가장': 174, '아쉽다': 175, '죽다': 176, '냐': 177, '랑': 178, '지만': 179, '기억': 180, '끝나다': 181, 'ㅠ': 182, '짱': 183, '보기': 184, '끄다': 185, '뿐': 186, '웃기다': 187, '님': 188, '남자': 189, '유치하다': 190, '크다': 191, '솔직하다': 192, 'ㅎㅎ': 193, '매력': 194, '하지만': 195, '보여주다': 196, '쓰다': 197, '늘다': 198, '니': 199, '높다': 200, '자체': 201, '애': 202, '실망': 203, '여자': 204, '캐릭터': 205, '수준': 206, '번': 207, '반전': 208, '전개': 209, '화': 210, '무섭다': 211, '제': 212, '본': 213, '우리': 214, '살다': 215, '찍다': 216, '지다': 217, '현실': 218, '급': 219, '추천': 220, '공감': 221, '낮다': 222, '대한': 223, '맞다': 224, '재다': 225, '이상': 226, 'ㅋㅋㅋㅋ': 227, '함': 228, '개봉': 229, '뭔가': 230, '눈물': 231, '인지': 232, '대단하다': 233, '계속': 234, '코미디': 235, '음악': 236, '눈': 237, '슬프다': 238, '전혀': 239, '이라': 240, '근데': 241, '다른': 242, '짜증나다': 243, '움': 244, '돼다': 245, '빠지다': 246, '말다': 247, '제목': 248, '밖에': 249, '처럼': 250, '기대하다': 251, '건지다': 252, '인가': 253, '미치다': 254, 'ㅜㅜ': 255, '욕': 256, '중간': 257, '기분': 258, '여운': 259, '시리즈': 260, '이란': 261, '표현': 262, '야하다': 263, '연기력': 264, '이네': 265, '감': 266, '내내': 267, '잇다': 268, '뭔': 269, '내다': 270, '굿': 271, '모두': 272, '믿다': 273, '이제': 274, '보이다': 275, '이라는': 276, '자': 277, '일본': 278, '작가': 279, '잼': 280, '이쁘다': 281, '원작': 282, '몰입': 283, '아이': 284, '영상': 285, '연': 286, '에는': 287, '이유': 288, 'ㅡ': 289, '오랜': 290, '막장': 291, '걍': 292, '위': 293, '가족': 294, '작': 295, '아주': 296, '한국': 297, '나름': 298, '노잼': 299, '아직도': 300, '절대': 301, '력': 302, '특히': 303, '점도': 304, '요즘': 305, '후': 306, '스릴러': 307, '이딴': 308, '긴장감': 309, '웃다': 310, '수작': 311, '딱': 312, '이랑': 313, '대박': 314, '졸작': 315, '시키다': 316, '어': 317, '그래도': 318, '치다': 319, '애니': 320, '잔잔하다': 321, '너': 322, '친구': 323, '기대': 324, '깊다': 325, '귀엽다': 326, 'ㅎ': 327, '짜다': 328, '찾다': 329, '느껴지다': 330, '물': 331, '진심': 332, '이라고': 333, '아프다': 334, '설정': 335, '접': 336, '모습': 337, '떨어지다': 338, '건': 339, '삶': 340, '보지': 341, '앞': 342, '부분': 343, '인상': 344, '문제': 345, '조금': 346, '용': 347, '당시': 348, '개인': 349, '놈': 350, '스럽다': 351, '빼다': 352, '포스터': 353, '한국영': 354, '따뜻하다': 355, '자신': 356, '몇': 357, '울다': 358, '멋있다': 359, '알바': 360, '년대': 361, '배경': 362, '추억': 363, '점수': 364, '초반': 365, '해보다': 366, '무엇': 367, '정신': 368, '필요없다': 369, '나가다': 370, '써다': 371, '데': 372, '류': 373, '에도': 374, '의미': 375, '신선하다': 376, '가지': 377, '예쁘다': 378, '제대로': 379, '세': 380, '식': 381, '시': 382, '우리나라': 383, '같이': 384, '웃음': 385, '제일': 386, '더럽다': 387, '안타깝다': 388, '극장': 389, '노래': 390, '영화로': 391, '쓸다': 392, '시나리오': 393, '한테': 394, '대사': 395, '캐스팅': 396, '질': 397, '결국': 398, '라면': 399, '반': 400, '공포': 401, '이지': 402, '티비': 403, '보단': 404, '따다': 405, '이상하다': 406, '나이': 407, '세상': 408, '기다': 409, '웃기': 410, '대다': 411, '도대체': 412, '책': 413, '사실': 414, '시작': 415, '시대': 416, '엄청': 417, '장난': 418, '원': 419, '부족하다': 420, '마다': 421, '이지만': 422, '대해': 423, '최고다': 424, '맘': 425, '기도': 426, '봄': 427, '평가': 428, '상': 429, '엄마': 430, '충분하다': 431, '훌륭하다': 432, '뭘': 433, '함께': 434, '이후': 435, '죽이다': 436, '두다': 437, '첨': 438, '완벽하다': 439, '음': 440, '그저': 441, '이야': 442, '몰입도': 443, '아무': 444, '답답하다': 445, '쯤': 446, '배우다': 447, '공포영화': 448, '엉': 449, '영화관': 450, '오': 451, '비다': 452, '집': 453, '망하다': 454, '살리다': 455, '극': 456, '놀라다': 457, '매우': 458, '누구': 459, '전쟁': 460, '남': 461, '얼마나': 462, '낫다': 463, '드리다': 464, '그리다': 465, '해': 466, '돌리다': 467, '씬': 468, '차라리': 469, '이라도': 470, '어설프다': 471, '누가': 472, '실화': 473, '관객': 474, '팬': 475, '간': 476, '억': 477, '엔딩': 478, '새롭다': 479, '한마디': 480, '꽤': 481, '영화인': 482, '필요하다': 483, '미국': 484, '읽다': 485, '힘들다': 486, '어색하다': 487, '위해': 488, '등': 489, '출연': 490, '후회': 491, '어디': 492, '아직': 493, '코믹': 494, '어울리다': 495, '건가': 496, '유쾌하다': 497, '그렇게': 498, '싫다': 499, '킬링타임': 500, '서다': 501, '소리': 502, '구': 503, '그대로': 504, '분위기': 505, '만큼': 506, '이르다': 507, '분들': 508, '밉다': 509, '코': 510, '오늘': 511, '생기다': 512, '그나마': 513, '대체': 514, '스릴': 515, '전부': 516, '그것': 517, '장르': 518, '충격': 519, '소름': 520, '갈수록': 521, '역사': 522, '구성': 523, '탄탄하다': 524, '잔인하다': 525, '심하다': 526, '회': 527, '애니메이션': 528, '명': 529, '놓다': 530, '살': 531, '부': 532, '바라다': 533, '생각나다': 534, '훨씬': 535, '옛날': 536, '여기': 537, '준': 538, '흥행': 539, '년도': 540, '여배우': 541, '로맨스': 542, '중국': 543, '뒤': 544, '시절': 545, '행복하다': 546, '좀비': 547, '라니': 548, '해도': 549, '화려하다': 550, '어이없다': 551, '주연': 552, '떠나다': 553, '머리': 554, '예술': 555, '쉬다': 556, '작다': 557, '날': 558, '오글거리다': 559, '만점': 560, '멀다': 561, '돋다': 562, '어느': 563, '총': 564, '강추': 565, '다큐': 566, '순간': 567, '엄청나다': 568, '답': 569, '제발': 570, '나쁘다': 571, '비디오': 572, '확실하다': 573, '지루함': 574, '약간': 575, '인물': 576, '비슷하다': 577, '복수': 578, '들이다': 579, '따르다': 580, '이름': 581, '즐겁다': 582, '편이': 583, '당하다': 584, '존재': 585, '상당하다': 586, '얼굴': 587, '달다': 588, '언제': 589, '걸리다': 590, '선택': 591, '걸작': 592, '개연': 593, '네이버': 594, 'ㅉㅉ': 595, '머': 596, '당신': 597, '어디서': 598, '자기': 599, '소설': 600, '감정': 601, '짜증': 602, '년전': 603, '빨리': 604, '초딩': 605, '이리': 606, '그래서': 607, '발': 608, '얘기': 609, '죠': 610, '너무나': 611, '잊다': 612, '아무리': 613, '주제': 614, '만화': 615, '흠': 616, '갑자기': 617, '발연기': 618, '그만': 619, '사랑스럽다': 620, '타다': 621, '미화': 622, '최근': 623, '산': 624, '말고': 625, '아들': 626, '극장판': 627, '비추다': 628, '터지다': 629, '점주': 630, '그러나': 631, '다니다': 632, '장': 633, '맛': 634, '진': 635, '진부하다': 636, '흐르다': 637, '보내다': 638, '감사하다': 639, '판': 640, '불편하다': 641, '에선': 642, '상황': 643, '방송': 644, '순수하다': 645, '안보': 646, '곳': 647, '싸우다': 648, 'ㅜ': 649, '만들어지다': 650, '울': 651, '완성': 652, '니까': 653, '전작': 654, '다운': 655, '어렵다': 656, '질질': 657, '에서도': 658, '맨': 659, '다르다': 660, '시즌': 661, '참고': 662, '휴': 663, '여주': 664, '졸라': 665, '진정하다': 666, '그런': 667, '라서': 668, '힘드다': 669, '에요': 670, '화이팅': 671, '화면': 672, '든': 673, '성룡': 674, '제작': 675, '비교': 676, '한편': 677, '수가': 678, '며': 679, '동안': 680, '끌다': 681, '꿈': 682, '사건': 683, '또한': 684, '래': 685, '몇번': 686, '궁금하다': 687, '원래': 688, '풀다': 689, '편집': 690, '막': 691, '뻔': 692, '왠만하다': 693, '엉망': 694, '단': 695, '가보다': 696, '께': 697, '담다': 698, '라도': 699, '존나': 700, '요소': 701, '게임': 702, '주': 703, '각본': 704, '선': 705, '거의': 706, '집중': 707, '똑같다': 708, '으로도': 709, '괜히': 710, '소중하다': 711, '평생': 712, '가볍다': 713, '뭐라다': 714, '간만': 715, '보다는': 716, '느와르': 717, '먼저': 718, '술': 719, '노력': 720, '재': 721, '무조건': 722, '만의': 723, '더빙': 724, '넘치다': 725, '굉장하다': 726, '물론': 727, '비': 728, '들어가다': 729, '재밋': 730, '힘': 731, '아버지': 732, '만으로도': 733, '케이블': 734, '살인': 735, '거리': 736, '몰다': 737, '혼자': 738, '약하다': 739, '키': 740, '얻다': 741, '무': 742, '흔하다': 743, '짧다': 744, '성하다': 745, '전체': 746, '상처': 747, '모': 748, 'ㅇ': 749, '화가': 750, '피': 751, '사회': 752, '시청률': 753, '만나다': 754, '끼다': 755, '멜로': 756, '그녀': 757, '상미': 758, '남기다': 759, '적다': 760, '낭비': 761, '전편': 762, '만하': 763, '씩': 764, '아저씨': 765, '살아가다': 766, '상영': 767, '뛰어나다': 768, '보': 769, '점점': 770, '어른': 771, '소녀': 772, '새끼': 773, '한심하다': 774, '도저히': 775, '으리': 776, '취향': 777, '똥': 778, '인거': 779, '손': 780, '이기다': 781, '여성': 782, '황당하다': 783, '평': 784, '형': 785, '거지': 786, '흥미': 787, '강하다': 788, '열': 789, '묻다': 790, '통해': 791, '예전': 792, '세계': 793, '실제': 794, '동화': 795, '흥미롭다': 796, '몸': 797, '예상': 798, '후반': 799, '으로는': 800, '특유': 801, '땐': 802, '잡다': 803, '빨': 804, '항상': 805, '감성': 806, '생': 807, '바꾸다': 808, '위대하다': 809, '아빠': 810, '온': 811, '그때': 812, '차': 813, '조': 814, '찾아보다': 815, '개그': 816, '평론가': 817, '이하': 818, '언': 819, '암': 820, '란': 821, '즐기다': 822, '참신하다': 823, '중반': 824, '개다': 825, '안나': 826, '에겐': 827, '잃다': 828, '기다리다': 829, '간다': 830, '지나다': 831, '기억나다': 832, '까진': 833, '허무하다': 834, '배': 835, '꿀잼': 836, '자극': 837, '히': 838, '법': 839, '돌아가다': 840, '지키다': 841, '현재': 842, '계': 843, '진정': 844, '이번': 845, '하하': 846, '산만하다': 847, '삼류': 848, '억지': 849, '동': 850, '쩔다': 851, '독특하다': 852, '그게': 853, '걸다': 854, '딸': 855, '채널': 856, '노답': 857, '역겹다': 858, '깊이': 859, '성도': 860, '불쾌하다': 861, '굳이': 862, '끝내다': 863, '즈': 864, '의도': 865, '다루다': 866, '실망하다': 867, '목소리': 868, '안좋다': 869, '청춘': 870, '섬세하다': 871, '햇': 872, '나서다': 873, '헐다': 874, '범죄': 875, '에서는': 876, 'ㅋㅋㅋㅋㅋ': 877, '가지다': 878, '올해': 879, '귀신': 880, '밑': 881, '역대': 882, '심심하다': 883, '예요': 884, '억지스럽다': 885, '다만': 886, '당': 887, '흥미진진': 888, '오빠': 889, '신': 890, '늦다': 891, '열심히': 892, '시도': 893, '빵점': 894, '돋보이다': 895, '조차': 896, '치고': 897, '죽음': 898, '싫어하다': 899, '설레다': 900, '일이': 901, '이에요': 902, '액션영화': 903, '반개': 904, '다시다': 905, '방법': 906, '죽': 907, '삼': 908, '자식': 909, '부르다': 910, '때리다': 911, '거기': 912, '리뷰': 913, '그래픽': 914, '귀': 915, '정서': 916, '표정': 917, '다행': 918, '어쩔': 919, '순': 920, '철학': 921, '글': 922, '미안하다': 923, '공': 924, '그닥': 925, '볼때': 926, '에게는': 927, 'ㅈ': 928, '교훈': 929, '일단': 930, '이라니': 931, '바': 932, '더욱': 933, '갖다': 934, '필요': 935, 'ㅠㅠㅠ': 936, '엿': 937, '결과': 938, '사극': 939, '흘리다': 940, '으': 941, '퀄리티': 942, '너무나도': 943, '나머지': 944, '기회': 945, '떼다': 946, '가면': 947, '결혼': 948, '티': 949, '챙기다': 950, '댓글': 951, '뛰다': 952, '겁나다': 953, '이며': 954, '학교': 955, '중요하다': 956, '군': 957, '견자단': 958, '전설': 959, '심': 960, '비극': 961, '바보': 962, '홍콩': 963, '만이': 964, '짓': 965, '가요': 966, '감다': 967, '일어나다': 968, '잊혀지다': 969, '손발': 970, '메세지': 971, '마무리': 972, '촬영': 973, '외': 974, '기적': 975, '비판': 976, '나르다': 977, '그런데': 978, '너무하다': 979, '개뿔': 980, '우울하다': 981, '쓰래': 982, '식상하다': 983, '성인': 984, '문화': 985, '상상': 986, '화보': 987, '개념': 988, '예산': 989, '스타일': 990, '진지하다': 991, '바로': 992, '다소': 993, '표절': 994, '가끔': 995, '연인': 996, '심리': 997, '리얼': 998, '희망': 999, '자연': 1000, '로는': 1001, '왠지': 1002, '기술': 1003, '어이': 1004, '바뀌다': 1005, '초': 1006, '우연히': 1007, '과거': 1008, '만족하다': 1009, '짐': 1010, '터': 1011, '다음': 1012, '예고편': 1013, '조연': 1014, '주기도': 1015, '스파이더맨': 1016, '맞추다': 1017, '희다': 1018, '눈물나다': 1019, '프로': 1020, '불쌍하다': 1021, '리메이크': 1022, '역': 1023, '우': 1024, '수도': 1025, '지루': 1026, '빠져들다': 1027, '과연': 1028, '스러운': 1029, '제작비': 1030, '속편': 1031, '신기하다': 1032, '둘': 1033, '제로': 1034, '자막': 1035, '쏘다': 1036, '현': 1037, '졸리다': 1038, '춤': 1039, '가치': 1040, '고민': 1041, '푹': 1042, '프로그램': 1043, '단순하다': 1044, '종교': 1045, '넣다': 1046, 'ㅎㅎㅎ': 1047, '영환': 1048, '나중': 1049, '인정': 1050, '부끄럽다': 1051, '소': 1052, '외계인': 1053, '이든': 1054, '강': 1055, '선생님': 1056, '학생': 1057, '존경': 1058, '레알': 1059, '여전하다': 1060, '호러': 1061, '반복': 1062, '연기자': 1063, '판타지': 1064, '관': 1065, '사': 1066, '런가': 1067, '여서': 1068, '쫌': 1069, '흐름': 1070, '이제야': 1071, '보이': 1072, '조절': 1073, '접다': 1074, '망작': 1075, '악역': 1076, '원하다': 1077, '혹은': 1078, '적당하다': 1079, '라인': 1080, '죄': 1081, '훈훈하다': 1082, '마르다': 1083, '노': 1084, '지난': 1085, '마': 1086, '까지도': 1087, '대의': 1088, '사라지다': 1089, '가깝다': 1090, '이연걸': 1091, '살짝': 1092, '창': 1093, '아쉬움': 1094, '갈다': 1095, '메다': 1096, '드': 1097, '스': 1098, '컷': 1099, '달': 1100, '따라가다': 1101, '뜨다': 1102, '에서의': 1103, '후속작': 1104, '게이': 1105, '전달': 1106, '늘': 1107, '스타': 1108, '특별하다': 1109, '썩다': 1110, '팔': 1111, '유': 1112, '방': 1113, '어찌': 1114, '유치': 1115, '관심': 1116, '낚': 1117, '드럽다': 1118, '서로': 1119, '오락': 1120, '쵝오': 1121, '병맛': 1122, '고양이': 1123, 'ㅇㅇ': 1124, '한다는': 1125, '올': 1126, '인하다': 1127, '핵': 1128, '변하다': 1129, '북한': 1130, '첫': 1131, '슬픔': 1132, '색다르다': 1133, '착하다': 1134, '숨다': 1135, '패러디': 1136, '다가오다': 1137, '아오': 1138, '돌아오다': 1139, '겠다': 1140, '남녀': 1141, 'ㅋㅋㅋㅋㅋㅋ': 1142, '면서': 1143, '줄거리': 1144, '묘사': 1145, '스케일': 1146, '독립영화': 1147, '고생': 1148, '망치다': 1149, '심장': 1150, '유일하다': 1151, '빌리다': 1152, '영원하다': 1153, '천재': 1154, '폭력': 1155, '새': 1156, '연결': 1157, '깔다': 1158, '관계': 1159, '무비': 1160, '로봇': 1161, '응원': 1162, '불가': 1163, '되게': 1164, '아침': 1165, '이미': 1166, '밋밋하다': 1167, '열정': 1168, '프랑스': 1169, '울리다': 1170, '커플': 1171, '보라': 1172, '날다': 1173, '에피소드': 1174, '밥': 1175, '양심': 1176, '강렬하다': 1177, '환상': 1178, '앞서': 1179, '실감': 1180, '과정': 1181, '허세': 1182, '타임': 1183, '여러': 1184, '말로': 1185, '교육': 1186, '긴장': 1187, '한계': 1188, '악당': 1189, '화나다': 1190, '자살': 1191, '조폭': 1192, '완전하다': 1193, '어머니': 1194, '송강호': 1195, '잘못': 1196, '행동': 1197, '닿다': 1198, '암튼': 1199, '잘만': 1200, '학년': 1201, 'ㅉㅉㅉ': 1202, '이정': 1203, '개판': 1204, '입': 1205, '주기': 1206, '이면': 1207, '틀다': 1208, '짜지다': 1209, '화끈하다': 1210, '볼거리': 1211, '안다': 1212, '줄다': 1213, '기본': 1214, '오히려': 1215, '성우': 1216, '지나치다': 1217, '평이': 1218, '양': 1219, '토나오다': 1220, '왕': 1221, '예능': 1222, '영국': 1223, '자주': 1224, '저렇게': 1225, '누군가': 1226, '심형래': 1227, '초등학교': 1228, '대로': 1229, '불다': 1230, '싸구려': 1231, '대작': 1232, '끌': 1233, '실력': 1234, '유명하다': 1235, '밤': 1236, '전형': 1237, '신분': 1238, '혹시': 1239, '이냐': 1240, '길다': 1241, '신나다': 1242, '트': 1243, '채우다': 1244, '탈': 1245, '줍다': 1246, '잠': 1247, '소름끼치다': 1248, '그럭저럭': 1249, '보시': 1250, '진행': 1251, '태어나다': 1252, '카메라': 1253, '변태': 1254, '빛': 1255, '대한민국': 1256, '시점': 1257, '펑펑': 1258, '정': 1259, '언제나': 1260, '보이지': 1261, '오그라들다': 1262, '사다': 1263, '생애': 1264, '꺼': 1265, '어떤': 1266, '깔끔하다': 1267, '분노': 1268, '자동차': 1269, '그린': 1270, '포기': 1271, '말아먹다': 1272, '영화계': 1273, '연예인': 1274, '길': 1275, '쇼': 1276, '영웅': 1277, '아픔': 1278, '바라보다': 1279, '랄': 1280, '파': 1281, '전반': 1282, '타': 1283, '터미네이터': 1284, '이따위': 1285, '시원하다': 1286, '등등': 1287, '잘생기다': 1288, '씁쓸하다': 1289, '녹다': 1290, '난해하다': 1291, '보다도': 1292, '만해': 1293, '스럽게': 1294, '무겁다': 1295, '왜케': 1296, '저러다': 1297, '옛': 1298, '저런': 1299, '과는': 1300, '딱하다': 1301, '쓸데없이': 1302, '체': 1303, '존': 1304, '특이하다': 1305, '편하다': 1306, 'ㅅㅂ': 1307, '아줌마': 1308, '아래': 1309, '전율': 1310, '형님': 1311, '달리': 1312, '명화': 1313, '신의': 1314, '외국': 1315, '졸다': 1316, '세기': 1317, '사고': 1318, '필름': 1319, '어린이': 1320, '찝찝하다': 1321, '대놓고': 1322, '넘어가다': 1323, '늘어지다': 1324, '역할': 1325, '영화제': 1326, '국민': 1327, '제니퍼': 1328, '밋': 1329, '이여': 1330, '짝퉁': 1331, '등장인물': 1332, '러브': 1333, '불륜': 1334, '의외로': 1335, '좋아지다': 1336, '오래되다': 1337, '굳다': 1338, '섹스': 1339, '가득하다': 1340, '히어로': 1341, '상태': 1342, '더하다': 1343, '진창': 1344, '로써': 1345, '참다': 1346, '매니아': 1347, '시기': 1348, '용서': 1349, '동영상': 1350, '홍콩영화': 1351, 'ㅁ': 1352, '아역': 1353, '지겹다': 1354, '통쾌하다': 1355, '감상': 1356, '월': 1357, '땜': 1358, '거슬리다': 1359, '편의': 1360, '젤': 1361, '덕분': 1362, '로만': 1363, '감각': 1364, '끌리다': 1365, '평범하다': 1366, '동생': 1367, '레전드': 1368, '능력': 1369, '관람': 1370, '약': 1371, '아끼다': 1372, '싸움': 1373, '뽑다': 1374, '이기': 1375, '사투리': 1376, '무재': 1377, '는걸': 1378, '평균': 1379, '그동안': 1380, '도전': 1381, '기준': 1382, '재밋어': 1383, '은근': 1384, '미소': 1385, '어제': 1386, '포르노': 1387, '천': 1388, '공간': 1389, '괴물': 1390, '흑': 1391, '에나': 1392, '입다': 1393, '몇몇': 1394, '나라': 1395, '해오다': 1396, '따위': 1397, '잠시': 1398, '러닝': 1399, '자르다': 1400, '유머': 1401, '애기': 1402, '듣다': 1403, '기세': 1404, '여자애': 1405, '째': 1406, '까지는': 1407, 'ㅜㅠ': 1408, '치고는': 1409, '덥다': 1410, '짠하다': 1411, '멋': 1412, '분명하다': 1413, 'ㄱ': 1414, '무지': 1415, '토록': 1416, '블록버스터': 1417, '무시': 1418, '구나': 1419, '앤': 1420, '부터가': 1421, '보신': 1422, '봣': 1423, '하이': 1424, '희생': 1425, '운': 1426, '용도': 1427, '꽝': 1428, '노출': 1429, '망': 1430, '보아': 1431, '남성': 1432, '동시': 1433, '레옹': 1434, '으로서': 1435, '마치': 1436, '그다지': 1437, '연애': 1438, '신다': 1439, '걱정': 1440, '만에': 1441, '다리': 1442, 'ㅋㅋㅋㅋㅋㅋㅋㅋ': 1443, '형편': 1444, '아련하다': 1445, '들어서다': 1446, '기르다': 1447, '그림': 1448, '줌': 1449, '일상': 1450, '진실': 1451, '형제': 1452, '그만하다': 1453, '지는': 1454, '전개도': 1455, '한데': 1456, '다큐멘터리': 1457, '개도': 1458, '누군지': 1459, '구리': 1460, '문': 1461, '이래': 1462, '공부': 1463, '키우다': 1464, '마리': 1465, '정작': 1466, '픽션': 1467, '재난영화': 1468, '주의': 1469, '쪽': 1470, '과장': 1471, '감명': 1472, '라이언': 1473, '우정': 1474, '기만': 1475, '등장': 1476, '크게': 1477, '싸이코': 1478, '광고': 1479, '성격': 1480, '명연기': 1481, '처절하다': 1482, '멍청하다': 1483, '재밋다': 1484, '아무나': 1485, '게다가': 1486, '거나': 1487, '설명': 1488, '목적': 1489, '적임': 1490, '관점': 1491, '의식': 1492, '옆': 1493, '타짜': 1494, '홍보': 1495, '테러': 1496, '짝': 1497, '꾸다': 1498, '글쎄': 1499, '녀': 1500, '최소한': 1501, 'ㄷㄷ': 1502, '당황': 1503, '비중': 1504, '벌써': 1505, '부족': 1506, '추다': 1507, '관련': 1508, '달리다': 1509, '발견': 1510, '좀더': 1511, '우뢰매': 1512, '울컥': 1513, '플롯': 1514, '돌다': 1515, '적절하다': 1516, '막장드라마': 1517, '중심': 1518, '린다': 1519, '심각하다': 1520, '십': 1521, '지리다': 1522, '예': 1523, '국내': 1524, '갈등': 1525, '별루': 1526, '치유': 1527, '세련되다': 1528, '극단': 1529, '사이': 1530, '초등학생': 1531, '뇌': 1532, '박수': 1533, '언니': 1534, '올리다': 1535, '경찰': 1536, '떨다': 1537, '쪽팔리다': 1538, '압권': 1539, '마냥': 1540, '하라': 1541, '수입': 1542, '헐리우드': 1543, '스트레스': 1544, '에서만': 1545, '가능하다': 1546, '투': 1547, '슈렉': 1548, '군대': 1549, '공짜': 1550, '평소': 1551, '뭉클하다': 1552, '내놓다': 1553, '단지': 1554, '지르다': 1555, '오래': 1556, '적어도': 1557, '기대다': 1558, '반하다': 1559, '아예': 1560, '공포물': 1561, '청소년': 1562, '경': 1563, '코난': 1564, '오우삼': 1565, '겨': 1566, '직업': 1567, '하자': 1568, '담기다': 1569, '화란': 1570, '안감': 1571, '성장': 1572, '았': 1573, '소소하다': 1574, '로그인': 1575, '느리다': 1576, '와우': 1577, '틴': 1578, '그립다': 1579, '최수종': 1580, '예수': 1581, '미학': 1582, '없애다': 1583, '분만': 1584, '바람': 1585, '디즈니': 1586, '도안': 1587, '최고봉': 1588, '하늘': 1589, '형식': 1590, '주지': 1591, '레이': 1592, '정신병': 1593, '싸다': 1594, '바르다': 1595, '질리': 1596, '도움': 1597, '추리': 1598, '로버트': 1599, '드니': 1600, '지구': 1601, '민망하다': 1602, '나타나다': 1603, '권': 1604, '만으로': 1605, '진하다': 1606, '검색': 1607, '찌다': 1608, '앞뒤': 1609, '이보': 1610, '겪다': 1611, '물이': 1612, '무협': 1613, '왕조현': 1614, '롭고': 1615, '비밀': 1616, '무한': 1617, '뜬금': 1618, '자리': 1619, '치': 1620, '끼우다': 1621, '호': 1622, '이라서': 1623, '에로': 1624, '우주': 1625, '소년': 1626, '한개': 1627, '영어': 1628, '시시하다': 1629, '대안': 1630, '종영': 1631, '생생하다': 1632, '효과': 1633, '베스트': 1634, '세다': 1635, '끼리': 1636, '탄생': 1637, '기법': 1638, '감안': 1639, '들어오다': 1640, '피다': 1641, '근': 1642, '추하다': 1643, '본방': 1644, '결정': 1645, '아우': 1646, '당연하다': 1647, '상상력': 1648, '웃': 1649, '무의미하다': 1650, '거장': 1651, '쓸데없다': 1652, '김': 1653, '버전': 1654, '고딩': 1655, '탓': 1656, '막판': 1657, '해내다': 1658, '연관': 1659, '움직이다': 1660, '부턴': 1661, '실패': 1662, '스스로': 1663, '국산': 1664, '반갑다': 1665, '빠르다': 1666, '뮤지컬': 1667, '인게': 1668, '담배': 1669, '방식': 1670, '세계관': 1671, '조합': 1672, '난리': 1673, '에게도': 1674, '용기': 1675, '섹시하다': 1676, '정체': 1677, '반도': 1678, '범인': 1679, '하나로': 1680, '해피엔딩': 1681, '스런': 1682, '홍상수': 1683, '에다': 1684, '어디가': 1685, '뒷': 1686, '수고': 1687, '고르다': 1688, '명성': 1689, '이루다': 1690, '갖추다': 1691, '새다': 1692, '깨닫다': 1693, '옴': 1694, '점줌': 1695, '뿐이다': 1696, '옳다': 1697, '아이돌': 1698, '미모': 1699, '던지다': 1700, '마저': 1701, '모자라다': 1702, 'ㅅ': 1703, '돌아보다': 1704, '외모': 1705, '낼': 1706, '외화': 1707, '포인트': 1708, '향': 1709, '리': 1710, '백': 1711, '부자': 1712, '불': 1713, '이만': 1714, '부부': 1715, '지우다': 1716, '신경': 1717, '방향': 1718, '쥐다': 1719, '감탄': 1720, '살이': 1721, '고뇌': 1722, 'ㅠㅜ': 1723, '딴': 1724, '확인': 1725, '행복': 1726, '색감': 1727, '무료': 1728, '안습': 1729, '께서': 1730, '배역': 1731, '거부': 1732, '목숨': 1733, '라스트': 1734, '호감': 1735, '사무라이': 1736, '지저분하다': 1737, '워': 1738, '우와': 1739, '충실하다': 1740, '코드': 1741, '만세': 1742, '늙다': 1743, 'ㄴ': 1744, '마이': 1745, '감정이입': 1746, '옷': 1747, '지나가다': 1748, '수록': 1749, '짬뽕': 1750, '김기덕': 1751, '버': 1752, '여행': 1753, '후기': 1754, '명장': 1755, '이자': 1756, '대가': 1757, '일주일': 1758, '살인마': 1759, '잖다': 1760, '악': 1761, '과도': 1762, '굿굿': 1763, '세번': 1764, '커서': 1765, '확': 1766, '일으키다': 1767, '동물': 1768, '만큼은': 1769, '곳곳': 1770, '복선': 1771, '입장': 1772, '잭': 1773, '이전': 1774, '꼬': 1775, '에만': 1776, '이니까': 1777, '이구': 1778, '시종일관': 1779, '본인': 1780, '자꾸': 1781, '패': 1782, '방영': 1783, '으론': 1784, '토마스': 1785, '매': 1786, '의리': 1787, '그지같다': 1788, '액션씬': 1789, '첨으로': 1790, '냥': 1791, '태국': 1792, '한참': 1793, '단연': 1794, '뺏다': 1795, '낳다': 1796, '캐리': 1797, '지상파': 1798, '인터스텔라': 1799, '젠': 1800, '시청': 1801, '연극': 1802, '껏': 1803, '학살': 1804, '쩐다': 1805, '투자': 1806, '부럽다': 1807, '역량': 1808, '이니': 1809, '억지로': 1810, '절제': 1811, '높이다': 1812, '장혁': 1813, '지도': 1814, '성공': 1815, '광구': 1816, '주성치': 1817, '든지': 1818, '흡입': 1819, '긴박': 1820, '애절하다': 1821, '죄다': 1822, '쉬': 1823, '데리': 1824, '척': 1825, '수많다': 1826, '인터넷': 1827, '돼지': 1828, '흘러가다': 1829, '미드': 1830, '집착': 1831, '사수': 1832, '진리': 1833, '배신': 1834, '개성': 1835, '납득': 1836, '붙이다': 1837, '과의': 1838, '와의': 1839, '일찍': 1840, '끔찍하다': 1841, '맥': 1842, '해결': 1843, '성은': 1844, '막히다': 1845, '유럽': 1846, '단순': 1847, '갠': 1848, '메시지': 1849, '부작': 1850, '으로써': 1851, '설득': 1852, '엇': 1853, '이어서': 1854, '고맙다': 1855, '번은': 1856, '국어': 1857, '그걸': 1858, '겉': 1859, '내면': 1860, '놀랍다': 1861, '깎다': 1862, '여인': 1863, '조작': 1864, '촌스럽다': 1865, '가리다': 1866, '꼴': 1867, '헤어지다': 1868, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 1869, '색깔': 1870, '분동': 1871, '겁니다': 1872, '엑소시스트': 1873, '올라가다': 1874, '값': 1875, '주제가': 1876, '인가요': 1877, '와는': 1878, '오는': 1879, '오버': 1880, '마이너스': 1881, '이도': 1882, '표': 1883, '기발하다': 1884, '발상': 1885, '이끌다': 1886, '만들기': 1887, '봣는데': 1888, '영웅본색': 1889, '영구': 1890, '니깐': 1891, '힘내다': 1892, '얘': 1893, '무술': 1894, '칼': 1895, '영향': 1896, '의상': 1897, '태도': 1898, '가시': 1899, '찬': 1900, '성의': 1901, '화일': 1902, '한가지': 1903, '우베': 1904, '가난하다': 1905, '리지': 1906, '고독': 1907, '향연': 1908, '편도': 1909, '어휴': 1910, '빡치다': 1911, '마을': 1912, '따로': 1913, '졸리': 1914, '최': 1915, '로우': 1916, '맺다': 1917, '나와라': 1918, '이민기': 1919, '만남': 1920, '휴머니즘': 1921, '탑': 1922, '즐거움': 1923, '일품': 1924, '김희선': 1925, '만족': 1926, '던데': 1927, '들어주다': 1928, '이별': 1929, '도르다': 1930, '디': 1931, '달달': 1932, '없어지다': 1933, '쥐': 1934, '넘어서다': 1935, '조용하다': 1936, '전문가': 1937, '쩌': 1938, '풍': 1939, '길이': 1940, '펭귄': 1941, '오브': 1942, '박보영': 1943, '티나': 1944, '유리': 1945, '왠': 1946, '극치': 1947, '깜짝': 1948, '거야': 1949, '한국인': 1950, '골': 1951, '넹': 1952, '블레이드': 1953, '실': 1954, '웬': 1955, '일부러': 1956, '정의': 1957, '루즈': 1958, '헐리웃': 1959, '박하다': 1960, '하루': 1961, '금': 1962, '젊다': 1963, '홀로': 1964, '새삼': 1965, '앉다': 1966, '만화책': 1967, '신인': 1968, '대학교': 1969, '애쓰다': 1970, 'ㄷㄷㄷ': 1971, '의문': 1972, '많아지다': 1973, '여기다': 1974, '단어': 1975, '맡다': 1976, '뛰어넘다': 1977, '마이클': 1978, '내일': 1979, '극본': 1980, '중학교': 1981, '어차피': 1982, '무리': 1983, '짱짱맨': 1984, '유발': 1985, '풍경': 1986, '용이': 1987, '겁': 1988, '참나': 1989, '아기': 1990, '화답': 1991, '영활': 1992, '킹': 1993, '거품': 1994, '전투': 1995, '적당': 1996, '인권': 1997, '각자': 1998, '묻히다': 1999, '한결같다': 2000, '날리다': 2001, '무기': 2002, '보임': 2003, '사진': 2004, '심지어': 2005, '삭제': 2006, '분량': 2007, '션': 2008, '양반': 2009, '꾼': 2010, '시선': 2011, '틀리다': 2012, '포': 2013, '조여정': 2014, '한지': 2015, '기차': 2016, '힐링': 2017, '신데렐라': 2018, '객관': 2019, '혹평': 2020, '재밋음': 2021, '몸매': 2022, '부모': 2023, '벗다': 2024, '낮추다': 2025, '정재영': 2026, '한정': 2027, '곧': 2028, '러시아': 2029, '자연스럽다': 2030, '웅장': 2031, '배경음악': 2032, '카리스마': 2033, '대신': 2034, '로움': 2035, '애니매이션': 2036, '으로만': 2037, '생활': 2038, '넘기다': 2039, '명불허전': 2040, '뜻': 2041, '시청자': 2042, '호구': 2043, '누': 2044, '환장하다': 2045, '토': 2046, '잠깐': 2047, '누나': 2048, '스텝': 2049, '기존': 2050, '전이': 2051, '열자': 2052, '선사': 2053, '고전': 2054, '우선': 2055, '빈': 2056, '졸잼': 2057, '잡': 2058, '혼란': 2059, '송혜교': 2060, '젠장': 2061, '파괴': 2062, '사기': 2063, '맨날': 2064, '빠순이': 2065, '찬사': 2066, '장애인': 2067, '나소': 2068, '뜬금없이': 2069, '놀다': 2070, '전락': 2071, '의하다': 2072, '통': 2073, '지지': 2074, '특수': 2075, '민': 2076, '자라': 2077, '울면': 2078, '세월': 2079, '임권택': 2080, '금보': 2081, '등록': 2082, '둘째': 2083, '지대': 2084, '보통': 2085, '기자': 2086, '조카': 2087, '컬트': 2088, '국가': 2089, 'ㅋㅋㅋㅋㅋㅋㅋ': 2090, '바다': 2091, '절정': 2092, '근래': 2093, '캐': 2094, '아누': 2095, '떨리다': 2096, '신고': 2097, '절대로': 2098, '성적': 2099, '신념': 2100, '화질': 2101, '웬만하다': 2102, '새벽': 2103, '완벽': 2104, '붙다': 2105, '풋풋하다': 2106, '리들리': 2107, '스콧': 2108, '그렇다고': 2109, '허허': 2110, '정선': 2111, '찌질하다': 2112, '영화사': 2113, '선물': 2114, '세트': 2115, '틱': 2116, '틀어주다': 2117, '그야말로': 2118, '원표': 2119, '닮다': 2120, '흑백': 2121, '임팩트': 2122, '포스': 2123, '본성': 2124, '탈출': 2125, '쌍': 2126, '발전': 2127, '흉내': 2128, '김치': 2129, '승리': 2130, '번역': 2131, '금발': 2132, '용의': 2133, '월드': 2134, '멍': 2135, '처': 2136, '선동': 2137, '제외': 2138, '하고는': 2139, '반드시': 2140, '로서': 2141, '보고오다': 2142, '제작자': 2143, '장점': 2144, '묘': 2145, '정말로': 2146, '회사': 2147, '차이': 2148, '사운드': 2149, '분장': 2150, '혹': 2151, '롱': 2152, '유덕화': 2153, '생기': 2154, '상관': 2155, '낫': 2156, '한텐': 2157, '인형': 2158, '반감': 2159, '어린시절': 2160, '지옥': 2161, '지하철': 2162, '어거지': 2163, '아자': 2164, '영화감독': 2165, '으으': 2166, '포장': 2167, '하드': 2168, '순수': 2169, '지고': 2170, '뉴스': 2171, '하니': 2172, '슈퍼맨': 2173, '뭥미': 2174, '시골': 2175, '스틱': 2176, '미녀': 2177, '효': 2178, '원숭이': 2179, '일부': 2180, '눈치': 2181, '후회되다': 2182, '쩝': 2183, '으로나': 2184, '견디다': 2185, '병': 2186, '고추': 2187, '교수': 2188, '김수현': 2189, '몽환': 2190, '사용': 2191, '쌈': 2192, '훨': 2193, '경험': 2194, '만도': 2195, '빨다': 2196, '최강': 2197, '시사회': 2198, '흑역사': 2199, '참으로': 2200, '감히': 2201, '절반': 2202, '구로': 2203, '깨': 2204, '그만큼': 2205, '재주': 2206, '데이': 2207, '칠': 2208, '시트콤': 2209, '성찰': 2210, '너무도': 2211, '박평': 2212, '방금': 2213, '도시': 2214, '풀': 2215, '새록새록': 2216, '꽃': 2217, '알파': 2218, '치노': 2219, '다섯': 2220, '똑바로': 2221, '로나': 2222, '검사': 2223, '퍼즐': 2224, '왕자': 2225, '인들': 2226, '소장': 2227, '이래서': 2228, '야동': 2229, '밀려오다': 2230, '때우다': 2231, '베일': 2232, '마약': 2233, '다크나이트': 2234, '일드': 2235, '파다': 2236, '링': 2237, '이의': 2238, '요리': 2239, '풋': 2240, '초적': 2241, '떠오르다': 2242, '주윤발': 2243, '징그럽다': 2244, '저희': 2245, '불구': 2246, '깡패': 2247, '계시다': 2248, '악마': 2249, '무난': 2250, '주위': 2251, '깨알': 2252, '주변': 2253, '망치': 2254, '강제': 2255, '이혼': 2256, '어색': 2257, '아마추어': 2258, '실험': 2259, '무언가': 2260, '직전': 2261, '공주': 2262, '재수없다': 2263, 'ㅠㅠㅠㅠ': 2264, '나비': 2265, '지드래곤': 2266, '덕': 2267, '로맨틱': 2268, '포함': 2269, '정리': 2270, '남아': 2271, '줄알': 2272, '패턴': 2273, '개그맨': 2274, '꼬마': 2275, '센스': 2276, '인기': 2277, '케로로': 2278, '및': 2279, '셋': 2280, '미스': 2281, '컨셉': 2282, '출발': 2283, '의사': 2284, '얼마': 2285, '오로라': 2286, '녀석': 2287, '파리': 2288, '최후': 2289, '욬': 2290, '잠들다': 2291, '점준': 2292, '불러일으키다': 2293, '안성기': 2294, '드림': 2295, '천사': 2296, '짜이다': 2297, '여러가지': 2298, '멍하다': 2299, '몇개': 2300, '양조위': 2301, '차원': 2302, '비슷': 2303, '대통령': 2304, '철': 2305, '청': 2306, '단체': 2307, '교양': 2308, '박찬욱': 2309, '잔혹': 2310, '각색': 2311, '작위': 2312, '용가리': 2313, '씨발': 2314, '토끼': 2315, '음식': 2316, '한국말': 2317, '가관': 2318, '정유미': 2319, '채': 2320, '로맨틱코미디': 2321, '보호': 2322, '찬양': 2323, '위원회': 2324, '기획': 2325, '집단': 2326, '욕망': 2327, '흔': 2328, '프레데터': 2329, '대표': 2330, '품': 2331, '저리': 2332, '찡': 2333, '재방': 2334, '워낙': 2335, '고로': 2336, '논': 2337, '동호': 2338, '사상': 2339, '아치': 2340, '현상': 2341, '치밀하다': 2342, '중년': 2343, '본적': 2344, '하아': 2345, '고본': 2346, '어깨': 2347, '뎀': 2348, '의심': 2349, '퍼펙트': 2350, '다이하드': 2351, '메이': 2352, '어쩜': 2353, '에혀': 2354, '아놀드': 2355, '합치다': 2356, '기독교': 2357, '하나님': 2358, '태양': 2359, '인내심': 2360, '속지': 2361, '삼다': 2362, '재미나': 2363, '피해자': 2364, '대부': 2365, '매번': 2366, '어마어마하다': 2367, '색': 2368, '만족스럽다': 2369, '디스': 2370, '옥': 2371, '꿈꾸다': 2372, '여정': 2373, '박': 2374, '아기자기하다': 2375, '소방관': 2376, '범': 2377, '어쩌면': 2378, '톰': 2379, '언젠가': 2380, '부다': 2381, '오랫': 2382, '나오니': 2383, '물들다': 2384, '성폭행': 2385, '한석규': 2386, '공중파': 2387, '그거': 2388, '서극': 2389, '어쩌라고': 2390, '깨우다': 2391, '너희': 2392, '진수': 2393, '다해': 2394, '린': 2395, '윤계상': 2396, '엽문': 2397, '별하나': 2398, '놀이': 2399, '실소': 2400, '꾸미다': 2401, '따분하다': 2402, '천녀유혼': 2403, '외설': 2404, '진짜진짜': 2405, '설마': 2406, '시험': 2407, '사장': 2408, '스페인': 2409, '잔뜩': 2410, '상투': 2411, '에반게리온': 2412, '눈빛': 2413, '구라': 2414, '신기': 2415, '전성기': 2416, '파격': 2417, '웨스턴': 2418, '덜하다': 2419, '베다': 2420, '벗어나다': 2421, '허준': 2422, '만큼도': 2423, '하고도': 2424, '목사': 2425, '모순': 2426, '마동석': 2427, '최초': 2428, '뒤늦다': 2429, '자유롭다': 2430, '주더': 2431, '직접': 2432, '대부분': 2433, '질주': 2434, '구석': 2435, '려고': 2436, '감사': 2437, '게뭐': 2438, '들보': 2439, '넌': 2440, '보장': 2441, '정우성': 2442, '오르다': 2443, '배트맨': 2444, '판단': 2445, '맙시': 2446, '호기심': 2447, '현대': 2448, '에이': 2449, '싹': 2450, '모범': 2451, '웰': 2452, '리브': 2453, '쭉': 2454, '여기저기': 2455, '매끄럽다': 2456, '인지도': 2457, '바닥': 2458, '뜯다': 2459, '뒤지다': 2460, '이군': 2461, '도입': 2462, '존내': 2463, '볼걸': 2464, '기사': 2465, '심오하다': 2466, '탄압': 2467, '계기': 2468, '겉멋': 2469, '정당하다': 2470, '마련': 2471, '늘리다': 2472, 'ㅂㅅ': 2473, '어떡하다': 2474, '부로': 2475, '총알': 2476, '무게': 2477, '전라도': 2478, '나뉘다': 2479, 'ㅅㅅ': 2480, '할아버지': 2481, '화구': 2482, '고수': 2483, '찌': 2484, '할리우드': 2485, '압축': 2486, '가득': 2487, '서기': 2488, '허구': 2489, '도통': 2490, '밴드': 2491, '이외': 2492, '스릴러물': 2493, '이어지다': 2494, '극복': 2495, '론': 2496, '간첩': 2497, '대면': 2498, '솔': 2499, '끼': 2500, '조정': 2501, '메인': 2502, '조각': 2503, '천만': 2504, '짐승': 2505, '우기다': 2506, '로렌스': 2507, '하락': 2508, '할머니': 2509, '열리다': 2510, '강력': 2511, '지독하다': 2512, '장동건': 2513, '짓다': 2514, '상대': 2515, '클라라': 2516, '두번째': 2517, '만큼이나': 2518, '한국판': 2519, '임요환': 2520, '역작': 2521, '엽기': 2522, '두렵다': 2523, '자매': 2524, '에서나': 2525, '부디': 2526, '내공': 2527, '이상은': 2528, '조니뎁': 2529, '달콤하다': 2530, '빼놓다': 2531, '죄송하다': 2532, '쯧쯧': 2533, '영화배우': 2534, '얼': 2535, '버킷리스트': 2536, '어떻': 2537, '어딘가': 2538, '초기': 2539, '일만': 2540, '오오': 2541, '능가': 2542, '깨끗하다': 2543, '유지태': 2544, '비현실적': 2545, '납치': 2546, '초점': 2547, '후지': 2548, '로코': 2549, '캬': 2550, '타고': 2551, '차승원': 2552, '스티븐': 2553, '레': 2554, '곡': 2555, '서서히': 2556, '찾기': 2557, '어우러지다': 2558, '케': 2559, '시사': 2560, 'ㅎㄷㄷ': 2561, '섹시': 2562, '달려들다': 2563, '부자연스럽다': 2564, '탁월하다': 2565, '김구라': 2566, '신동엽': 2567, '냄새': 2568, '엉뚱하다': 2569, '어쩌': 2570, '대하': 2571, '축구': 2572, '명품': 2573, '슈퍼': 2574, '앤드류': 2575, '깜놀': 2576, '보나': 2577, '혀': 2578, '으로가': 2579, '베': 2580, '접근': 2581, '비정상': 2582, '린즈링': 2583, '겨우': 2584, '해석': 2585, '승부': 2586, '종': 2587, '말고는': 2588, '깨다': 2589, '가을': 2590, '아마': 2591, '빅': 2592, '잘알다': 2593, '차마': 2594, '한수': 2595, '요구': 2596, '초월': 2597, '빵': 2598, '어처구니': 2599, '가능': 2600, '당대': 2601, '지경': 2602, '생명': 2603, '용암': 2604, '콜린': 2605, '모으다': 2606, '벌어지다': 2607, '땀': 2608, '케미': 2609, '연속': 2610, '고프다': 2611, '에야': 2612, '선정': 2613, '닥': 2614, '서부': 2615, '평화': 2616, '달인': 2617, '가야': 2618, '장나라': 2619, '옮기다': 2620, '타란티노': 2621, '역쉬': 2622, '중독': 2623, '주말': 2624, '널': 2625, '홍': 2626, '놓치다': 2627, '만원': 2628, '에게나': 2629, '고등학교': 2630, '살인자': 2631, '리기': 2632, '우연': 2633, '복잡하다': 2634, '이승환': 2635, '소박하다': 2636, '더불다': 2637, '농담': 2638, '자유': 2639, '살아오다': 2640, '본질': 2641, '스크린': 2642, '엄정화': 2643, '듬': 2644, '환경': 2645, '원피스': 2646, '파라': 2647, '노말': 2648, '장선우': 2649, '부실하다': 2650, '꺼지다': 2651, '간직': 2652, '한장': 2653, '이러니': 2654, '흐지부지': 2655, '심정': 2656, '남지': 2657, '개콘': 2658, '요새': 2659, '쨋': 2660, '시각': 2661, '노인': 2662, '구경': 2663, '이병헌': 2664, '미도': 2665, '예체능': 2666, '옴니버스': 2667, '불행하다': 2668, '에드워드': 2669, '은은하다': 2670, '팀': 2671, '벌': 2672, '고해': 2673, '한동안': 2674, '주목': 2675, '여왕': 2676, '친': 2677, '틈': 2678, '장만옥': 2679, '려': 2680, '코끼리': 2681, '강시': 2682, '모음': 2683, '님들': 2684, '매다': 2685, '용감하다': 2686, '모험': 2687, '담': 2688, '능': 2689, '프레디': 2690, '하든': 2691, '감흥': 2692, '햇음': 2693, '습': 2694, '편안하다': 2695, '숨기다': 2696, '크리스틴': 2697, '쓴다': 2698, '명확하다': 2699, '하고프다': 2700, '일반인': 2701, '결코': 2702, '남발': 2703, '조커': 2704, '무어': 2705, '전투씬': 2706, '딸리다': 2707, '강동원': 2708, '예측': 2709, '대본': 2710, '투표': 2711, '본능': 2712, '지네': 2713, '떄': 2714, '살아나다': 2715, '단조롭다': 2716, '이웃': 2717, '유대인': 2718, '대상': 2719, '팍': 2720, '그건': 2721, '덜': 2722, '박진': 2723, '아바타': 2724, '성공하다': 2725, '서인국': 2726, '때매': 2727, '맥스': 2728, '빅뱅': 2729, '불필요하다': 2730, '밝다': 2731, '아내': 2732, '베리': 2733, '사귀다': 2734, '쓸쓸하다': 2735, '키드': 2736, '기용': 2737, '절절': 2738, '반성': 2739, '열다': 2740, '설': 2741, '각': 2742, '무대': 2743, '업': 2744, '목': 2745, '형사': 2746, '바디': 2747, '로마': 2748, '오프닝': 2749, '여러분': 2750, '컴퓨터': 2751, '기키': 2752, '애틋하다': 2753, '전쟁영화': 2754, '뽕': 2755, '부터는': 2756, '샘': 2757, '땅': 2758, '키스': 2759, '뱀파이어': 2760, '의지': 2761, '응': 2762, '편견': 2763, '상관없다': 2764, '불법': 2765, '세뇌': 2766, '밝혀지다': 2767, '지원': 2768, '빛나다': 2769, '당당하다': 2770, '손대다': 2771, '개신교': 2772, '복제': 2773, '솜씨': 2774, '화의': 2775, '아아': 2776, '입사': 2777, '킬링': 2778, '연상': 2779, '괴롭다': 2780, '모니카': 2781, '브루스': 2782, '착각': 2783, '퍼포먼스': 2784, '권력': 2785, '짐작': 2786, '가게': 2787, '군더더기': 2788, '비노': 2789, '내리다': 2790, '삼국지': 2791, '듭니': 2792, '난뒤': 2793, '놀람': 2794, '밖': 2795, '좆': 2796, '잡고': 2797, '엑스트라': 2798, 'ㅄ': 2799, '드디어': 2800, '온몸': 2801, '감싸다': 2802, '졸업': 2803, '구분': 2804, '필드': 2805, '궁금': 2806, '일반': 2807, '비정하다': 2808, '맑다': 2809, '그리움': 2810, '제임스': 2811, '완': 2812, '도데': 2813, '와이프': 2814, '잃어버리다': 2815, '어지럽다': 2816, '교회': 2817, '먹음': 2818, '헛웃음': 2819, '참패': 2820, '다우니': 2821, '출신': 2822, '태': 2823, '인격': 2824, '오글오글': 2825, '나루토': 2826, '섞이다': 2827, '여동생': 2828, '였음': 2829, '어째': 2830, '나은': 2831, '안목': 2832, '거울': 2833, '리차드': 2834, '무리수': 2835, '오싹하다': 2836, '뻥': 2837, '머리스타일': 2838, '판치다': 2839, '몸짓': 2840, '미국인': 2841, '하디': 2842, '간지': 2843, '완젼': 2844, '실상': 2845, '스타워즈': 2846, '닷': 2847, '머릿속': 2848, '폭발': 2849, '격': 2850, '단점': 2851, '가짜': 2852, '비참하다': 2853, '근본': 2854, '가운데': 2855, '인류': 2856, '치르다': 2857, '백배': 2858, '가르치다': 2859, '달라': 2860, '널다': 2861, '막상': 2862, '별거': 2863, '유선': 2864, '정치인': 2865, '판이': 2866, '무너지다': 2867, '이용': 2868, '황': 2869, '최대': 2870, '불안하다': 2871, '루이스': 2872, '신하균': 2873, '배급사': 2874, '라기': 2875, '수능': 2876, '완죤': 2877, '각각': 2878, '먼지': 2879, '횡설수설': 2880, '게스트': 2881, '싱어': 2882, '싸이코패스': 2883, '별개': 2884, '에서야': 2885, '야경': 2886, '즉': 2887, '엑소': 2888, '이이이': 2889, '가나': 2890, '고도': 2891, '상승': 2892, '태안': 2893, '업그레이드': 2894, '댓글알바': 2895, '영화평론가': 2896, '가해자': 2897, '이겠다': 2898, '일지': 2899, '일일': 2900, '불후': 2901, '절망': 2902, '펴다': 2903, '스포': 2904, '공연': 2905, '드물다': 2906, '건데': 2907, '활동': 2908, '독립': 2909, '시리': 2910, '신뢰': 2911, '이정재': 2912, '상어': 2913, '택': 2914, '미션임파서블': 2915, '만치': 2916, '짝사랑': 2917, '설레임': 2918, '미가': 2919, '압도': 2920, '압': 2921, '민중': 2922, '소매치기': 2923, '실수': 2924, '김래원': 2925, '여유': 2926, '푸다': 2927, '띄우다': 2928, '지기': 2929, '니콜라스': 2930, '케이': 2931, '도망가다': 2932, '소품': 2933, '비행기': 2934, '인셉션': 2935, '잉': 2936, '시간여행': 2937, '랑은': 2938, '두뇌': 2939, '곤': 2940, '이틀': 2941, '애니스톤': 2942, '렌트': 2943, '안내': 2944, '전기': 2945, '여름': 2946, '조롱': 2947, '전통': 2948, '호러영화': 2949, '부드럽다': 2950, '나오미': 2951, '찍': 2952, '따지다': 2953, '장난감': 2954, '아이언맨': 2955, '댄서': 2956, '공개': 2957, '멜로영화': 2958, '담백하다': 2959, '예술가': 2960, '권상우': 2961, '평타': 2962, '기간': 2963, '라이': 2964, '비호감': 2965, '캐릭': 2966, '오씨': 2967, '베드': 2968, '신세경': 2969, '파워': 2970, '공유': 2971, '김민종': 2972, '참여': 2973, '녹화': 2974, '테이프': 2975, '치우다': 2976, '가수': 2977, '상업': 2978, '총장': 2979, '대학': 2980, '밖엔': 2981, '물의': 2982, '일본인': 2983, '멋대로': 2984, '배려': 2985, '눈꼽': 2986, '켜다': 2987, '민주주의': 2988, '마틴': 2989, '인종차별': 2990, '지역': 2991, '밟다': 2992, '도가니': 2993, '빙빙': 2994, '평작': 2995, '신세계': 2996, '도구로': 2997, '층': 2998, '뉴': 2999, '학': 3000, '라곤': 3001, '팍팍': 3002, '비롯': 3003, '또는': 3004, '경이': 3005, '민간인': 3006, '변명': 3007, '떠돌다': 3008, '루비': 3009, '포드': 3010, '표본': 3011, '대원': 3012, '소수': 3013, '요란하다': 3014, '짜임새': 3015, '난잡하다': 3016, '기전': 3017, '불교': 3018, '제왕': 3019, '박중훈': 3020, '오늘날': 3021, '임청하': 3022, '마녀': 3023, '재난': 3024, '답지': 3025, '나아지다': 3026, '버금': 3027, '테스트': 3028, '한적': 3029, '케빈': 3030, '메리': 3031, '파커': 3032, '형태': 3033, '오지': 3034, '놀래다': 3035, '휴가': 3036, '개선': 3037, '걸왜': 3038, '분명': 3039, '짱구': 3040, '히나타': 3041, '급전': 3042, '우아하다': 3043, '첩보': 3044, '메이드': 3045, '콘스탄틴': 3046, '낙': 3047, '일요일': 3048, '낭만': 3049, '분신': 3050, '개막': 3051, '히치콕': 3052, '함부로': 3053, '기계': 3054, '바쁘다': 3055, '찾아가다': 3056, '측면': 3057, '토미': 3058, '래야': 3059, '광기': 3060, '권위': 3061, '정책': 3062, '구림': 3063, '택시': 3064, '정확하다': 3065, '고증': 3066, '어딨다': 3067, '아르': 3068, '관객수': 3069, '알아차리다': 3070, '달라지다': 3071, '튀다': 3072, '애초': 3073, '킁': 3074, '내려가다': 3075, '주관': 3076, '부진': 3077, '혐오': 3078, '신곡': 3079, '샤이니': 3080, '에이핑크': 3081, '정은지': 3082, '수지': 3083, '첫사랑': 3084, '생략': 3085, '바치다': 3086, '적도': 3087, '똑같이': 3088, '삼성': 3089, '이던': 3090, '런닝타임': 3091, '성동일': 3092, '앞서다': 3093, '드러나다': 3094, '삶다': 3095, '룩': 3096, '황금': 3097, '동성애': 3098, '휼륭하다': 3099, '제이슨': 3100, '람보': 3101, '록키': 3102, '해봤다': 3103, '커녕': 3104, '추가': 3105, '잡스': 3106, '범벅': 3107, '야구': 3108, '질감': 3109, '홍금보': 3110, '강요': 3111, '독일': 3112, '다수': 3113, '사만': 3114, '의견': 3115, '소유': 3116, '위트': 3117, '인척': 3118, '아리다': 3119, '여고괴담': 3120, '밀': 3121, '박히다': 3122, '얼음': 3123, '배꼽': 3124, '아이디어': 3125, '아동': 3126, '장가': 3127, '공각기동대': 3128, '타르': 3129, '주인': 3130, '다크': 3131, '풍자': 3132, '와도': 3133, '아무렇다': 3134, '잔': 3135, '첨부': 3136, '라고는': 3137, '군인': 3138, '주장': 3139, '서른': 3140, '주님': 3141, '막다': 3142, '단막극': 3143, '년작': 3144, '장이': 3145, '조승우': 3146, '수애': 3147, '큐브': 3148, '장화홍련': 3149, '변화': 3150, '떨어뜨리다': 3151, '은퇴': 3152, '투척': 3153, '증거': 3154, '산이': 3155, '말리': 3156, '전지현': 3157, '달러': 3158, '쿵푸허슬': 3159, '조명': 3160, '비록': 3161, '지라': 3162, '안쓰럽다': 3163, '마찬가지': 3164, '스톤': 3165, '잘리다': 3166, '사촌동생': 3167, '알바생': 3168, '린치': 3169, '무간도': 3170, '흠잡다': 3171, '법정': 3172, '팬텀': 3173, '울음': 3174, '제라드': 3175, '버틀러': 3176, '취해': 3177, '장애': 3178, '대비': 3179, '커피': 3180, '끼치다': 3181, '설리': 3182, '미래': 3183, '리가': 3184, '죄책감': 3185, '낯선': 3186, '국적': 3187, '운동': 3188, '훈남': 3189, '게살': 3190, '화장실': 3191, '걸레': 3192, '정신병원': 3193, '망가지다': 3194, '수습': 3195, '엠마': 3196, '로버츠': 3197, '찜찜하다': 3198, '적나라하다': 3199, '고치다': 3200, '예고': 3201, '버그': 3202, '필립': 3203, '깡': 3204, '정치': 3205, '뎅': 3206, '팝콘': 3207, '가도': 3208, '성과': 3209, '대화': 3210, '천국': 3211, '진보': 3212, '건조하다': 3213, '그랬는데': 3214, '제적': 3215, '피아노': 3216, '피로': 3217, '도의': 3218, '이해도': 3219, '이미지': 3220, '뚝뚝': 3221, '끊기다': 3222, '라지': 3223, '제시카': 3224, '차리다': 3225, '삽질': 3226, '도망치다': 3227, '해대': 3228, '물건': 3229, '안이': 3230, '올레': 3231, '원주고': 3232, '센터': 3233, '케릭': 3234, '스텝업': 3235, '카피': 3236, '나타내다': 3237, '잡히다': 3238, '서스펜스': 3239, '료코': 3240, '차인표': 3241, '가기': 3242, '신화': 3243, '에릭': 3244, '호화': 3245, '재판': 3246, '짜깁다': 3247, '김지수': 3248, '회장': 3249, '한글': 3250, '거짓말': 3251, '어번': 3252, '가하다': 3253, '역활': 3254, '부탁드리다': 3255, '붉다': 3256, '합': 3257, '금지': 3258, '찔리다': 3259, '가슴속': 3260, '기승': 3261, '마마': 3262, '그나저나': 3263, '발음': 3264, '겨울': 3265, '손오공': 3266, '여명': 3267, '여신': 3268, '설치다': 3269, '정무문': 3270, '버티다': 3271, '교감': 3272, '존트라볼타': 3273, '외면': 3274, '거절': 3275, '헤어스타일': 3276, '잔혹하다': 3277, '여지': 3278, '킴': 3279, '퍼스': 3280, '박자': 3281, '프리': 3282, '자본': 3283, '이따': 3284, '알려지다': 3285, '스탤론': 3286, '셈': 3287, '서정': 3288, '세르게이': 3289, '보드': 3290, '행': 3291, '집안': 3292, '나니': 3293, '저주': 3294, '승': 3295, '떡밥': 3296, '욕먹다': 3297, '향수': 3298, '백인': 3299, '질투': 3300, '디카프리오': 3301, '대책': 3302, '깨달음': 3303, '후딱': 3304, '배다': 3305, '에플렉': 3306, '애정': 3307, '타이': 3308, '쉐리던': 3309, '영혼': 3310, '현대인': 3311, '남겨지다': 3312, '다세포': 3313, '안남': 3314, '대구': 3315, '일수': 3316, '뵈다': 3317, '담담하다': 3318, '해설': 3319, '모니터링': 3320, '집합': 3321, '빈약하다': 3322, '외로움': 3323, '허니': 3324, '예스': 3325, '어긋나다': 3326, '말르다': 3327, '다그': 3328, '출연료': 3329, '도둑': 3330, '가보': 3331, '광주': 3332, '즐': 3333, '명절': 3334, '김혜선': 3335, '극적': 3336, '기괴하다': 3337, '오유': 3338, '부대': 3339, '높아지다': 3340, '두근거리다': 3341, '요약': 3342, '통틀어': 3343, '결론': 3344, '이은주': 3345, '문학': 3346, '선전': 3347, '물다': 3348, '박정희': 3349, '나머진': 3350, '의학': 3351, '공리': 3352, '유지': 3353, '조잡하다': 3354, '폴': 3355, '순위': 3356, '조진웅': 3357, '자랑': 3358, '심다': 3359, '상징': 3360, '시청율': 3361, '흐뭇하다': 3362, '식이': 3363, '색채': 3364, '여태': 3365, '쓰러지다': 3366, '눈부시다': 3367, '만드': 3368, '당장': 3369, '중국산': 3370, '논란': 3371, '홍어': 3372, '이라고는': 3373, '경쾌하다': 3374, '면모': 3375, '크리스찬': 3376, '경악': 3377, '크리스': 3378, '미스캐스팅': 3379, '우리네': 3380, '죄인': 3381, '과대': 3382, '채플린': 3383, '벅차다': 3384, '구역': 3385, '후의': 3386, '호흡': 3387, '이승기': 3388, '써로게이트': 3389, '장편': 3390, '블랙코미디': 3391, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 3392, '벨라': 3393, '삼각관계': 3394, '놀란': 3395, '파트': 3396, '일리': 3397, '무당': 3398, '콩': 3399, '연습': 3400, '매일': 3401, '피하': 3402, '해피': 3403, '대변': 3404, '흥분': 3405, '바토리': 3406, '이종석': 3407, '누님': 3408, '미니': 3409, '크루즈': 3410, '장치': 3411, '떡': 3412, '재회': 3413, '출현': 3414, '대충': 3415, '야말로': 3416, '끊다': 3417, '오현경': 3418, 'ㅜㅜㅜ': 3419, '영호': 3420, '하트넷': 3421, '끝내주다': 3422, '다양하다': 3423, '지게': 3424, '틀': 3425, '잘나다': 3426, '러브스토리': 3427, '정상': 3428, '일본애니': 3429, '로드': 3430, '뜨겁다': 3431, '헤어': 3432, '벨': 3433, '커버': 3434, '개그콘서트': 3435, '도아': 3436, '박스오피스': 3437, '마저도': 3438, 'ㄷ': 3439, '올려주다': 3440, '존멋': 3441, '관계도': 3442, '접영': 3443, '행진': 3444, '시보': 3445, '민들레': 3446, '돌': 3447, '정보': 3448, '종이': 3449, '막심': 3450, '해달라다': 3451, '카': 3452, '황당': 3453, '톱': 3454, '이념': 3455, '몰락': 3456, '정돈': 3457, '낚이': 3458, '주온': 3459, '매주': 3460, '재탕': 3461, '주변인': 3462, '까지만': 3463, '스나이퍼': 3464, '절로': 3465, '장사': 3466, '느': 3467, '아담': 3468, '지나': 3469, '투성이': 3470, '재수': 3471, '크크': 3472, '괜': 3473, '강력하다': 3474, '일제': 3475, '사망': 3476, '갑': 3477, '아시아': 3478, '톤': 3479, '작화': 3480, '라퓨타': 3481, '은혜': 3482, '어지간하다': 3483, 'ㅏ': 3484, '그림자': 3485, '획': 3486, '핳': 3487, '인연': 3488, '클린트': 3489, '쉽다': 3490, '사르다': 3491, '스럽지': 3492, '트릭': 3493, '흑인': 3494, '발톱': 3495, '완존': 3496, '토니': 3497, '어루만지다': 3498, '직설': 3499, '슴': 3500, '거치다': 3501, '애매하다': 3502, '거지같다': 3503, '왜곡': 3504, '닌': 3505, '본드': 3506, '매드': 3507, '떠들다': 3508, '조장': 3509, '유명': 3510, '호강': 3511, '못자다': 3512, 'ㅜㅡ': 3513, '밧다': 3514, '용다': 3515, '겨울왕국': 3516, '대고': 3517, '준비': 3518, '화류': 3519, '낚임': 3520, '에여': 3521, '흥': 3522, '외다': 3523, '이소룡': 3524, '던': 3525, '훌쩍': 3526, '사로자다': 3527, '남자친구': 3528, '우드': 3529, '질린다': 3530, '번째': 3531, '성욕': 3532, '하품': 3533, '인도': 3534, '원주율': 3535, '찬란하다': 3536, '이정현': 3537, '정권': 3538, '코메디': 3539, '추': 3540, '연주': 3541, '거대하다': 3542, '저그': 3543, '자료': 3544, '볼땐': 3545, '감점': 3546, '반대': 3547, '비난': 3548, '안해': 3549, '예수님': 3550, '번개': 3551, '중후': 3552, '러셀': 3553, '크로우': 3554, '여부': 3555, '검술': 3556, '도쿄': 3557, '해리포터': 3558, '대중': 3559, '실패하다': 3560, '이서진': 3561, '가족영화': 3562, '패스': 3563, '대감': 3564, '하나같이': 3565, '주옥': 3566, '프레': 3567, '한경직': 3568, '나발': 3569, '기한': 3570, '킬러': 3571, '미스터리': 3572, '누르다': 3573, '도로': 3574, '디테': 3575, '언급': 3576, '퍼': 3577, '사람과': 3578, '로운': 3579, '분석': 3580, '맷': 3581, '데이먼': 3582, '은기': 3583, '마루': 3584, '글자': 3585, '가가': 3586, '자녀': 3587, '이안': 3588, '지치다': 3589, '소통': 3590, '반응': 3591, '김동완': 3592, '모야': 3593, '수없이': 3594, '해적': 3595, '텐데': 3596, '본격': 3597, '정화': 3598, '흥겹다': 3599, '읭': 3600, '박다': 3601, '말투': 3602, '꺾다': 3603, '깔리다': 3604, '초능력': 3605, '올라오다': 3606, '지내다': 3607, '아리': 3608, '혁명': 3609, '와사비': 3610, '손색': 3611, '이계인': 3612, '마음속': 3613, '마스터피스': 3614, '김태희': 3615, '에로영화': 3616, '악플': 3617, '리더': 3618, '참혹하다': 3619, '미묘하다': 3620, '자위': 3621, '영차': 3622, '무서움': 3623, '알맞다': 3624, '되돌리다': 3625, '디워': 3626, '토요명화': 3627, '차갑다': 3628, '심야식당': 3629, '복': 3630, '중국영화': 3631, '학원': 3632, '과학': 3633, '늑대': 3634, '유익하다': 3635, '안기다': 3636, '경지': 3637, '작렬': 3638, '클래식': 3639, '클레멘타인': 3640, '해명': 3641, '가정': 3642, '이드': 3643, '오로지': 3644, '아햏햏': 3645, '굿굿굿': 3646, '묵주': 3647, '에바': 3648, '인성': 3649, '헤': 3650, '어정쩡하다': 3651, '허풍': 3652, '짝짓기': 3653, '경쟁': 3654, '역사왜곡': 3655, '장군': 3656, '마돈나': 3657, '엄': 3658, '보삼': 3659, '모방': 3660, '엮': 3661, '풀리다': 3662, '민폐': 3663, '사도': 3664, '경우': 3665, '감독판': 3666, '빵터지다': 3667, '순도': 3668, '구혜선': 3669, '장근석': 3670, '멀리': 3671, '포뇨': 3672, '스키': 3673, '노트북': 3674, '장수': 3675, '용구성': 3676, '난후': 3677, '서프라이즈': 3678, '르': 3679, '발킬머': 3680, '실사': 3681, '감격': 3682, '성해': 3683, '해드리다': 3684, '정형': 3685, '로지': 3686, '장국영': 3687, '재탕하다': 3688, '고든': 3689, '마술': 3690, '쩌는듯': 3691, '동성': 3692, '히키코모리': 3693, '무관': 3694, '시민': 3695, '구해': 3696, '이구나': 3697, '군사': 3698, '주군': 3699, '빨갱이': 3700, '몬초': 3701, '이무영': 3702, '냉소': 3703, '치가': 3704, '잘봣습니': 3705, '고급스럽다': 3706, '세얼간이': 3707, '임신': 3708, '베이': 3709, '롯': 3710, '풍기다': 3711, 'ㄹㅇ': 3712, '가물가물': 3713, '재현': 3714, '저절로': 3715, '시르다': 3716, '박신혜': 3717, '봉하': 3718, '제법': 3719, '바베트': 3720, '만찬': 3721, '두근두근': 3722, '소유자': 3723, '정사': 3724, '긔': 3725, '이요원': 3726, '덩어리': 3727, '하숙집': 3728, '가왜': 3729, '불과': 3730, '볼일': 3731, '록': 3732, '스탁': 3733, '스모': 3734, '배럴': 3735, '교묘하다': 3736, '주시': 3737, '훨낫다': 3738, '기어': 3739, '알리': 3740, '등골': 3741, '고스트': 3742, '뚫리다': 3743, '메이크업': 3744, '스완': 3745, '따라서': 3746, 'ㅠㅠㅠㅠㅠ': 3747, '캄캄하다': 3748, '오줌': 3749, '오늘이': 3750, '여균동': 3751, '중국인': 3752, '조차도': 3753, '숭고하다': 3754, '상도': 3755, '닥터진': 3756, '힐러리': 3757, '파티': 3758, '춤추다': 3759, '뒷이야기': 3760, '뽀로로': 3761, '은평': 3762, '헷갈리다': 3763, '덜다': 3764, '나레이션': 3765, '아나운서': 3766, '작성': 3767, '대형': 3768, '강혜정': 3769, '흐': 3770, '숨막히다': 3771, '추잡하다': 3772, '이세영': 3773, '성숙하다': 3774, '흉내내': 3775, '피곤하다': 3776, '지능': 3777, '성숙': 3778, '책임감': 3779, '복싱': 3780, '사의': 3781, '때메': 3782, '상실': 3783, '그러하다': 3784, '공자': 3785, '속이다': 3786, '수위': 3787, '쏠리다': 3788, '봣음': 3789, '보고서': 3790, '나약하다': 3791, '성유리': 3792, '사주다': 3793, '변신': 3794, '예나': 3795, '젊음': 3796, '널리': 3797, '긴박하다': 3798, '강대국': 3799, '남일': 3800, '네티즌': 3801, '인식': 3802, '전인': 3803, '비치': 3804, 'ㅂ': 3805, '이기도': 3806, '불꽃': 3807, '홍진호': 3808, '자제': 3809, '무방': 3810, '대가리': 3811, '탄탄': 3812, '이런저런': 3813, '사업': 3814, '지침': 3815, '전도연': 3816, '삼만리': 3817, '뱉다': 3818, '방화': 3819, '실종': 3820, '욕심': 3821, '요정': 3822, '비장': 3823, '미사일': 3824, '근대': 3825, '기리': 3826, '염치': 3827, '주원': 3828, '나인': 3829, '억이': 3830, '다가': 3831, '정말루': 3832, '줄리': 3833, '런': 3834, '이랑은': 3835, '집기': 3836, '치아': 3837, '조선': 3838, '장영': 3839, '소개': 3840, '표기': 3841, '알아보다': 3842, '대판': 3843, '폐지': 3844, '으헝': 3845, '해지': 3846, '충': 3847, '투자자': 3848, '다듬어지다': 3849, '복습': 3850, '뒷받침': 3851, '부탁': 3852, '고급': 3853, '장병': 3854, '작자': 3855, '진솔하다': 3856, '최곤데': 3857, '다가가다': 3858, '몬': 3859, '쩌네': 3860, '찰리채플린': 3861, '해바라기': 3862, '의아': 3863, '생가': 3864, '필요성': 3865, '볼타': 3866, '대요': 3867, '구심': 3868, '한두': 3869, '결승전': 3870, '탈피': 3871, '지니어스': 3872, '퇴색': 3873, '지껄이다': 3874, '공효진': 3875, '콧대': 3876, '왼쪽': 3877, '옹': 3878, '흡사하다': 3879, '복녀': 3880, '균': 3881, '접함': 3882, '그러니까': 3883, '자화상': 3884, '식스센스': 3885, '류작': 3886, '망설이다': 3887, '금성무': 3888, '동의': 3889, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 3890, '벌이다': 3891, '탁': 3892, '송승헌': 3893, '믿어지다': 3894, '이기광': 3895, '유투브': 3896, '우수하다': 3897, '금은': 3898, '예진': 3899, '난감하다': 3900, '어어': 3901, '애국': 3902, '오랫동안': 3903, '도와주다': 3904, '우울증': 3905, '타락': 3906, '감옥': 3907, '꼴다': 3908, '존슨': 3909, '충청도': 3910, '고요': 3911, '광해': 3912, '치킨': 3913, '구식': 3914, '애니메': 3915, '재방송': 3916, '전함': 3917, '미취': 3918, '초등': 3919, '데이빗': 3920, '에러': 3921, '어르신': 3922, '주민': 3923, '주자': 3924, '그치다': 3925, '꼽': 3926, '아이고': 3927, '콱': 3928, '어딜': 3929, '본영': 3930, '빠': 3931, 'ㅣ': 3932, '파치노': 3933, '브라이언': 3934, '창피하다': 3935, 'ㅍ': 3936, '테크노': 3937, '그토록': 3938, '현빈': 3939, '사랑과전쟁': 3940, '장판': 3941, '최하': 3942, '갱': 3943, '리좀': 3944, '로다': 3945, '왕가위': 3946, '건축': 3947, '건축가': 3948, '한몫': 3949, '모니터': 3950, '미리': 3951, '찍어내다': 3952, '가부장': 3953, '제프': 3954, '브리': 3955, '놀': 3956, '영양가': 3957, '뭐임': 3958, '드래곤볼': 3959, '가져오다': 3960, '반지의제왕': 3961, '왤케': 3962, '허영': 3963, '조건': 3964, '노동': 3965, '주요': 3966, '전용': 3967, '사나이': 3968, '지리': 3969, '디자인': 3970, '육': 3971, '황홀하다': 3972, '경향': 3973, '우디': 3974, '조센징': 3975, '절때': 3976, '녹이다': 3977, '퇴보하다': 3978, '유치원': 3979, '주체': 3980, '또다시': 3981, '바랬는데': 3982, '신사': 3983, '꼬맹이': 3984, '마는': 3985, '접해': 3986, '출생': 3987, '적히다': 3988, '마디': 3989, '일그러지다': 3990, '희극': 3991, '말초신경': 3992, '김서형': 3993, '발생': 3994, '축소': 3995, '처리': 3996, '전차': 3997, '임창정': 3998, '칭송': 3999, '장통': 4000, '판도': 4001, '제기': 4002, '호러물': 4003, '주류': 4004, '무색': 4005, '소스': 4006, '큐': 4007, '쫄깃쫄깃': 4008, '하수': 4009, '구가': 4010, '주신': 4011, '봣던': 4012, '김민준': 4013, '김수로': 4014, '데이트': 4015, '멸망': 4016, '자세하다': 4017, '뭘말': 4018, '투철': 4019, '어필': 4020, '못만드': 4021, '김승우': 4022, '일정': 4023, '성취': 4024, '만들엇네': 4025, '엠비씨': 4026, '조기': 4027, '무척': 4028, '하얗다': 4029, '유령': 4030, '알리시아': 4031, '럭': 4032, '에든': 4033, '쏘우': 4034, '로또': 4035, '습작': 4036, '함축': 4037, '히스': 4038, '스킬': 4039, '별루임': 4040, '중딩': 4041, '욕구': 4042, '나날이': 4043, '밸런스': 4044, '가시다': 4045, '블랙': 4046, '인걸': 4047, '용두사미': 4048, '옹호': 4049, '유대': 4050, '이러하다': 4051, '부가': 4052, '몫': 4053, '전국': 4054, '이편': 4055, '명대사': 4056, '레고': 4057, '위장': 4058, '복장': 4059, '걸이': 4060, '로더': 4061, '렉': 4062, '폰': 4063, '차지': 4064, '산업': 4065, '팔다': 4066, '반면': 4067, '트렌드': 4068, '소화': 4069, '시련': 4070, '홍경인': 4071, '돌려주다': 4072, '바램': 4073, '특징': 4074, '미장센': 4075, '한바탕': 4076, '절': 4077, '존중': 4078, '밨습니': 4079, '중단': 4080, '매트릭스': 4081, '비명': 4082, '애도': 4083, '콩가루': 4084, '박사': 4085, '온통': 4086, '이상형': 4087, '눈요기': 4088, '안개': 4089, '성인영화': 4090, '수의': 4091, '아따': 4092, '임은경': 4093, '데드': 4094, '해선': 4095, '가문': 4096, '섞다': 4097, '펼치다': 4098, '밤새': 4099, '주행': 4100, '활': 4101, '소린': 4102, '스크림': 4103, '정신차리다': 4104, '오락가락': 4105, '시종': 4106, '리스': 4107, '가르다': 4108, '니스': 4109, '팔이': 4110, '사토시': 4111, '엘리트': 4112, '명복': 4113, '일어나서': 4114, '남경': 4115, '거짓': 4116, '축복': 4117, '의료': 4118, '이종혁': 4119, '퀼리티': 4120, '년뒤': 4121, '긍정': 4122, '에다가': 4123, '블럭버스터': 4124, '히죽': 4125, '전무후무': 4126, '이소연': 4127, '집다': 4128, '퍼지다': 4129, '징': 4130, '차분하다': 4131, '계절': 4132, '건강': 4133, '국민학교': 4134, '빚': 4135, '삼촌': 4136, '격인': 4137, '데니스': 4138, '퀸': 4139, '홀': 4140, '사기꾼': 4141, '망상': 4142, '갑갑하다': 4143, '녹음': 4144, '뮤지컬영화': 4145, '헉': 4146, '슬로우': 4147, '모션': 4148, '학창시절': 4149, '의존': 4150, '조종': 4151, '쉣': 4152, '하찮다': 4153, '겸비': 4154, '값지다': 4155, '도발': 4156, '제제': 4157, '범죄자': 4158, '테이크': 4159, '개방': 4160, '이함': 4161, '산드라': 4162, '브라운': 4163, '에미': 4164, '증명': 4165, '즐감': 4166, '위로': 4167, '지모': 4168, '민주당': 4169, '쏟다': 4170, '라그': 4171, '특출나다': 4172, '니나': 4173, '오디션': 4174, '유감': 4175, '게왜': 4176, '금물': 4177, '책임': 4178, '모성애': 4179, '멀쩡하다': 4180, '진행중': 4181, '과제': 4182, '화중': 4183, '스토': 4184, '인생관': 4185, '쑤시다': 4186, '트라우마': 4187, '식탁': 4188, '정적': 4189, '움직임': 4190, '각성': 4191, '흔들리다': 4192, '걸음': 4193, '맛있다': 4194, '상자': 4195, '바꿔치다': 4196, '잡탕': 4197, '환': 4198, '처키': 4199, '해군': 4200, '유도': 4201, '이중': 4202, '알고싶다': 4203, '소문나다': 4204, '잔치': 4205, '이브': 4206, '앙증맞다': 4207, '이크': 4208, '제압': 4209, '사살': 4210, '어둡다': 4211, '꼴리다': 4212, '털다': 4213, '짜장면': 4214, '공룡': 4215, '넨': 4216, '빼앗다': 4217, '오해': 4218, '우스': 4219, '협박': 4220, '타임슬립': 4221, 'ㅎㅎㅎㅎ': 4222, '불법체류자': 4223, '병원': 4224, '설마설마': 4225, '바이러스': 4226, '습격': 4227, '에서부터': 4228, '이라기': 4229, '컬': 4230, '미흡하다': 4231, '환타': 4232, '자비': 4233, '날로': 4234, '실컷': 4235, '이신': 4236, '졸': 4237, '타고나다': 4238, '할로윈': 4239, '억배': 4240, '절묘하다': 4241, '농구': 4242, '잠자다': 4243, '오만': 4244, '랩': 4245, '첩혈쌍웅': 4246, '주가': 4247, '저만': 4248, '으루': 4249, '활짝': 4250, '비번': 4251, '환불': 4252, '생동감': 4253, '박물관': 4254, '딱지': 4255, '틀어놓다': 4256, '가라': 4257, '어후': 4258, '죽여주다': 4259, '아따맘마': 4260, '뿜었다': 4261, '미루다': 4262, '왓츠': 4263, '이모': 4264, '방가': 4265, '바가지': 4266, '사신': 4267, '죽도': 4268, '성함': 4269, '품다': 4270, '판사': 4271, '합의': 4272, '처벌': 4273, '동기': 4274, '번만': 4275, '스탠': 4276, '오멘': 4277, '이하나': 4278, '정겨운': 4279, '우수': 4280, '화하다': 4281, '교과서': 4282, '옹박': 4283, '신파': 4284, '병구': 4285, '따오다': 4286, '지적': 4287, '레드': 4288, '타인': 4289, '듣기': 4290, '와일드': 4291, '재앙': 4292, '가능성': 4293, '헌': 4294, '정신건강': 4295, '어도': 4296, '다케시': 4297, '어물': 4298, '구토': 4299, '공기': 4300, '전해지다': 4301, '어서': 4302, '줄리엣': 4303, '세영': 4304, 'ㅇㅅㅇ': 4305, '본답': 4306, '앵': 4307, '서민': 4308, '으악': 4309, '아역배우': 4310, '작년': 4311, '가나다': 4312, '라마': 4313, '바사': 4314, '앙': 4315, '왜캐': 4316, '외치': 4317, '스탈린그라드': 4318, '병사': 4319, '며칠': 4320, '이지나': 4321, '허무': 4322, '된장': 4323, '성형': 4324, '미로': 4325, '악몽': 4326, '덕후': 4327, '오래간만': 4328, '뽕짝': 4329, '만약': 4330, '부류': 4331, '떄문': 4332, '무도': 4333, '싸이': 4334, '꺼내다': 4335, '저렇다': 4336, '도그빌': 4337, '임성한': 4338, '지식인': 4339, '숨쉬다': 4340, '유작': 4341, '루크': 4342, '매혹': 4343, '맘껏': 4344, '썻': 4345, '일본도': 4346, '아만다': 4347, '바티스타': 4348, '전격': 4349, '적극': 4350, '레이싱': 4351, '카이': 4352, '시네마': 4353, '재밋습': 4354, '역사상': 4355, '독보': 4356, '개척': 4357, '뿌리': 4358, '반영': 4359, '빗대다': 4360, '고질': 4361, '분노하다': 4362, '야곱': 4363, '제보': 4364, '엘리자베스': 4365, '쿵': 4366, '데이즈': 4367, '배드': 4368, '패자부활전': 4369, '리얼리티': 4370, '민족': 4371, '하이킥': 4372, '지현우': 4373, '황비홍': 4374, '부영': 4375, '장화': 4376, '석': 4377, '지식': 4378, '고요하다': 4379, '서글프다': 4380, '사색': 4381, '정철': 4382, '애잔하다': 4383, '자질': 4384, '의심스럽다': 4385, '호화롭다': 4386, '통한': 4387, '끓다': 4388, '숲': 4389, '매달리다': 4390, '너리': 4391, '곽지민': 4392, '똥폼': 4393, '전두환': 4394, '고통': 4395, '미이라': 4396, '자아': 4397, '성향': 4398, '고스': 4399, '짱개': 4400, '통쾌': 4401, '하우스': 4402, '이유리': 4403, '만주': 4404, '폭탄': 4405, '스필버그': 4406, '탐정': 4407, '상담': 4408, '가히': 4409, '덤': 4410, '저건': 4411, '저지르다': 4412, '단편': 4413, '구조': 4414, '질문': 4415, '땅크': 4416, '부릉부릉': 4417, '깜찍하다': 4418, '로부터': 4419, '수녀': 4420, '장용': 4421, '주진모': 4422, '스펙': 4423, '굿바이': 4424, '년후': 4425, '간단하다': 4426, '은희': 4427, '방만': 4428, '일베': 4429, '주니어': 4430, '운명': 4431, '해독': 4432, '일어나고': 4433, '낚시꾼': 4434, '별다르다': 4435, '계시': 4436, '상반': 4437, '허황': 4438, '식인': 4439, '얽히다': 4440, '지켜보다': 4441, '그땐': 4442, '주걸륜': 4443, '철권': 4444, '만은': 4445, '이성재': 4446, '안젤리나': 4447, '이물': 4448, '살때': 4449, '장진': 4450, '에의': 4451, '내지': 4452, '끝내': 4453, '멘탈': 4454, '통찰': 4455, '부족함': 4456, '팔리다': 4457, '기원': 4458, '현지': 4459, '미달': 4460, '개떡': 4461, '비유': 4462, '연예계': 4463, '리리': 4464, '프렌즈': 4465, '어쩐지': 4466, '스토킹': 4467, '이프': 4468, '다음주': 4469, '엑스': 4470, '방이': 4471, '이집트': 4472, '갇히다': 4473, '교사': 4474, '부도': 4475, '치졸하다': 4476, '운지': 4477, '놔두다': 4478, '듬뿍': 4479, '이어진': 4480, '밀리다': 4481, '유행어': 4482, '상급': 4483, '라스베가스': 4484, '모름': 4485, '수다': 4486, '서양': 4487, '불문': 4488, '요원': 4489, '스티브': 4490, '이중성': 4491, '스태프': 4492, '우웩': 4493, '진과': 4494, '매료': 4495, '지니': 4496, 'ㅈㄴ': 4497, '티브이': 4498, '신도': 4499, '패션': 4500, '뭣': 4501, '파트너': 4502, '러시아어': 4503, '누리': 4504, '권리': 4505, '컴플렉스': 4506, '만화가': 4507, '리그': 4508, '단독': 4509, '김민희': 4510, '류승룡': 4511, '남편': 4512, '햐': 4513, '트릴로지': 4514, '들것': 4515, '난이': 4516, '진자': 4517, '디비디': 4518, '모녀': 4519, '살해': 4520, '뱃김': 4521, '펀치': 4522, '플': 4523, '증말': 4524, '착오': 4525, '아마도': 4526, '재치': 4527, '어의': 4528, '로맨스영화': 4529, '이야말로': 4530, '다녀오다': 4531, '범작': 4532, '후루룩': 4533, '유오성': 4534, '톰크루즈': 4535, '젛': 4536, '어우': 4537, '웟음': 4538, '하여금': 4539, '근접하다': 4540, '빙의': 4541, '노땅': 4542, '크리스토퍼': 4543, '썩': 4544, '레슬링': 4545, '좌파': 4546, '쫓아가다': 4547, 'ㄹ': 4548, '멈추다': 4549, '도배': 4550, '드네': 4551, '자격': 4552, '성장하다': 4553, '열차': 4554, '평정': 4555, '의젖': 4556, '멍청': 4557, '토요일': 4558, '황정민': 4559, '김소현': 4560, '그라드': 4561, '귀요미': 4562, '키스신': 4563, '사춘기': 4564, '감추다': 4565, '칼라': 4566, '낚였다': 4567, '돌싱': 4568, '향기': 4569, '정지훈': 4570, '지존파': 4571, '정당화': 4572, '자이언트': 4573, '어떻든': 4574, '왓': 4575, '인간미': 4576, '제공': 4577, '친절하다': 4578, '이득': 4579, '찌르다': 4580, '임수정': 4581, '거창하다': 4582, '아무튼': 4583, '특집': 4584, '얼다': 4585, '가치관': 4586, '귀여니': 4587, '미미': 4588, '공존': 4589, '예뻣다': 4590, '인공': 4591, '구역질': 4592, '스님': 4593, '만큼의': 4594, '것임': 4595, '로이': 4596, '장끌': 4597, '복귀': 4598, '참가자': 4599, '파악': 4600, '즘': 4601, '소문': 4602, '미성년': 4603, '바치': 4604, '데인': 4605, '게리': 4606, '존론': 4607, '재키': 4608, '포근하다': 4609, '경의': 4610, '벌다': 4611, '정녕': 4612, '세대': 4613, '도현': 4614, '윤찬': 4615, '어수선하다': 4616, '홈': 4617, '나누다': 4618, '논리': 4619, '잊어버리다': 4620, '김범': 4621, '냉혹하다': 4622, '상치': 4623, '장동민': 4624, '라운드': 4625, '소라': 4626, '아오이': 4627, '우승자': 4628, '페이스': 4629, '간절하다': 4630, '다시금': 4631, '김해': 4632, '묵': 4633, '오페라': 4634, '주제곡': 4635, '근육': 4636, '니당다': 4637, '갈래': 4638, '돌아다니다': 4639, '미스터': 4640, '드림웍스': 4641, '주석': 4642, '도끼': 4643, '사정봉': 4644, '사정': 4645, '거임': 4646, '가안': 4647, '영화상': 4648, '고개': 4649, '꼽히다': 4650, '고현정': 4651, '수년': 4652, '찰나': 4653, '앵글': 4654, '극한': 4655, '달고나': 4656, '김보성': 4657, '구리다': 4658, '하차': 4659, '비수': 4660, '헬기': 4661, '마구': 4662, '미군': 4663, '업햄': 4664, '인터뷰': 4665, '고발': 4666, '명언': 4667, '무고': 4668, '손예진': 4669, '에이미': 4670, '숀펜': 4671, '놀랏다': 4672, 'ㅓ': 4673, '모티브': 4674, '오래오래': 4675, '안녕하다': 4676, '대학생': 4677, '효민': 4678, '스피드': 4679, '권하다': 4680, '고백': 4681, '임지연': 4682, '유이': 4683, '비주': 4684, '달려가다': 4685, '곁': 4686, '외롭다': 4687, '무려': 4688, '수용': 4689, '빙': 4690, '불과하다': 4691, '오류': 4692, '주된': 4693, '사할린': 4694, '상당수': 4695, '노역': 4696, '우기': 4697, '케이트': 4698, '넉': 4699, '일대기': 4700, '스포일러': 4701, '떼': 4702, '긋다': 4703, '남아돌다': 4704, '죽지': 4705, '천공': 4706, '의성': 4707, '훑다': 4708, '헐크': 4709, '익숙하다': 4710, '후속': 4711, '기해': 4712, '메이퀸': 4713, '건담': 4714, '시드': 4715, '트리스탄': 4716, '터키': 4717, '스킵': 4718, '기타': 4719, '아일랜드': 4720, '실속': 4721, '단면': 4722, '가오': 4723, '지인': 4724, '저급하다': 4725, '썰렁하다': 4726, '번봄': 4727, '었': 4728, '도덕': 4729, '고조': 4730, '뿜': 4731, '불가능': 4732, '꺅': 4733, '인색하다': 4734, '스트레이트': 4735, '검다': 4736, '나무': 4737, '치기': 4738, '쳐다보다': 4739, '소원': 4740, '유태인': 4741, '서커스': 4742, '베토벤': 4743, '폐륜': 4744, '겉도': 4745, '단단하다': 4746, '솜': 4747, '가두다': 4748, '띠띠': 4749, '흘러나오다': 4750, '맨인블랙': 4751, '난무': 4752, '문득': 4753, '트로트': 4754, '진퉁': 4755, '감수성': 4756, '고만': 4757, '손자': 4758, '쫙': 4759, '무성영화': 4760, '방해': 4761, '진영': 4762, '알리다': 4763, '아시': 4764, '핀': 4765, '남친': 4766, '힙합': 4767, '가구': 4768, '몬스터왕국': 4769, '김준호': 4770, '인칭': 4771, '약점': 4772, '펙': 4773, '가드': 4774, '다나': 4775, '관해': 4776, '짱짱하다': 4777, '답답': 4778, '숙면': 4779, '취하': 4780, '다다': 4781, '내기': 4782, '대치': 4783, '무한도전': 4784, '그럴듯하다': 4785, '낌': 4786, '엿보다': 4787, '절도': 4788, '빵빵': 4789, '엉덩이': 4790, '찢다': 4791, '데넘': 4792, '연민': 4793, '안녕': 4794, '용인': 4795, '라푼젤': 4796, '심은하': 4797, '닼': 4798, '내생': 4799, '떤다': 4800, '해안': 4801, '된거': 4802, '엉터리': 4803, '무심코': 4804, '퓨': 4805, '다이아나': 4806, '에일리언': 4807, '자랑스럽다': 4808, '지니다': 4809, '싱겁다': 4810, '재희': 4811, '복제인간': 4812, '따분함': 4813, '재밋습니': 4814, '대역': 4815, '기부': 4816, '자하': 4817, '스무': 4818, '턴': 4819, '에게로': 4820, '인턴': 4821, '랜턴': 4822, '보디가드': 4823, '슬랩': 4824, '맵다': 4825, '사나': 4826, '묵직하다': 4827, '창작': 4828, '어중간하다': 4829, '합리화': 4830, '루': 4831, '애란': 4832, '채다': 4833, '타령': 4834, '파이팅': 4835, '믄': 4836, '뭉클': 4837, '내심': 4838, '나열하다': 4839, '부담': 4840, '대도': 4841, '만화영화': 4842, '멜깁슨': 4843, '페이': 4844, '인사': 4845, '찬란': 4846, '장하나': 4847, '어처구니없다': 4848, '대들다': 4849, '슬래셔': 4850, '마음껏': 4851, '강물': 4852, '진국': 4853, '브레이크': 4854, '꼽으': 4855, '마리나': 4856, '마린': 4857, '귀염': 4858, '자도': 4859, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 4860, '간지나다': 4861, '신부': 4862, '기황후': 4863, '소이현': 4864, '상쾌하다': 4865, '반지': 4866, '경찰서': 4867, '빠삐용': 4868, '분도': 4869, '지영': 4870, '주지훈': 4871, '토리': 4872, '쌤': 4873, '관리': 4874, '이스트': 4875, '방향성': 4876, '비상구': 4877, '저녁': 4878, '티켓': 4879, '로망': 4880, '작전': 4881, '코스프레': 4882, '할배': 4883, '어줍다': 4884, '짱짱': 4885, '취지': 4886, '어케': 4887, '갓': 4888, '매칭': 4889, '안대': 4890, '결혼식': 4891, '요괴': 4892, '뒤죽박죽': 4893, '질리다': 4894, '또다른': 4895, '칭찬': 4896, '펼쳐지다': 4897, '세우다': 4898, '얄팍하다': 4899, '다주': 4900, '닥치고': 4901, '하지원': 4902, '거듭': 4903, '에가': 4904, '휘': 4905, '포켓몬스터': 4906, '염병': 4907, '관계자': 4908, '러시': 4909, '곤란하다': 4910, '은커녕': 4911, '질색': 4912, '거가': 4913, '무적자': 4914, '짜임': 4915, '후유증': 4916, '마케마케': 4917, '음모론': 4918, '아영': 4919, '볼껄': 4920, '찔끔': 4921, '아날로그': 4922, '쫌더': 4923, '러브레터': 4924, '벨루치': 4925, '문채원': 4926, '배출': 4927, '뚜렷하다': 4928, '드라큘라': 4929, '나영': 4930, '머싯': 4931, '북받치다': 4932, '막강': 4933, '고어영화': 4934, '강철중': 4935, '영화니': 4936, '탑기어': 4937, '강예빈': 4938, '따름': 4939, '다기': 4940, '철저하다': 4941, '그로': 4942, '꾸역꾸역': 4943, '샤론스톤': 4944, '만듭시': 4945, '상콤': 4946, '스머프': 4947, '봣으': 4948, '갈리다': 4949, '계획': 4950, '중앙': 4951, '패착': 4952, '생겨나다': 4953, '예민하다': 4954, '흡수': 4955, '유년기': 4956, '바스코': 4957, '강용석': 4958, '영감': 4959, '리모컨': 4960, '나대다': 4961, '도하': 4962, '히로스에': 4963, '다듬다': 4964, '숨소리': 4965, '이재용': 4966, '잔인함': 4967, '두운': 4968, '가버리다': 4969, '쇼킹': 4970, '푸른': 4971, '위험하다': 4972, '기이하다': 4973, '쟁이': 4974, '정사씬': 4975, '올려놓다': 4976, '특': 4977, '유의': 4978, '룸메이트': 4979, '아낌없다': 4980, '유니크': 4981, '기수': 4982, '예지원': 4983, '끼들': 4984, '터널': 4985, '재료': 4986, '피식': 4987, '어떠하다': 4988, '흔적': 4989, '조니': 4990, '괴짜': 4991, '타이틀': 4992, '발랄하다': 4993, '환자': 4994, '마법': 4995, '우린': 4996, '성기': 4997, '체적': 4998, '부실': 4999, '부모님': 5000, '공공': 5001, '고어': 5002, '기광': 5003, '숀': 5004, '분안': 5005, '어기다': 5006, '론데': 5007, '소말리아': 5008, '차태현': 5009, '히로인': 5010, '두리반': 5011, '존엄성': 5012, '숨죽': 5013, '유일': 5014, '활약': 5015, '짜릿하다': 5016, '무분별': 5017, '봉준호': 5018, '년생': 5019, '드라마정': 5020, '무시무시하다': 5021, '유리창': 5022, '어째서': 5023, '쿵푸팬더': 5024, '입력': 5025, '빠져나오다': 5026, '갈수': 5027, '이형': 5028, '탁재훈': 5029, '멜로디': 5030, '내다보다': 5031, '괜츈': 5032, '거만': 5033, '편성': 5034, '광희': 5035, '쫓겨나다': 5036, '매니': 5037, '이완': 5038, '맥그리거': 5039, '조반': 5040, '은지원': 5041, '화만': 5042, '김영호': 5043, '흥분하다': 5044, '수사물': 5045, '퀴즈': 5046, '류덕환': 5047, '언능': 5048, '지아': 5049, '막간': 5050, '시내': 5051, '따스하다': 5052, '모처럼': 5053, '우에노': 5054, '주리': 5055, '피의자': 5056, '드릴': 5057, '한결': 5058, '꼬옥': 5059, '제이': 5060, '아키라': 5061, '의외': 5062, '암울하다': 5063, '쩔어요': 5064, '시끄럽다': 5065, '껀들': 5066, '통제': 5067, '봣네': 5068, '천하다': 5069, '능청': 5070, '시퀀스': 5071, 'ㅗ': 5072, '총각': 5073, '훔치다': 5074, '온갖': 5075, '프레드': 5076, '소리치다': 5077, '줄리아': 5078, '우산': 5079, '그딴': 5080, '랫': 5081, '진작': 5082, '한예슬': 5083, '슬슬': 5084, '부어': 5085, 'ㅎㅡㅎ': 5086, '강아지': 5087, '가져가다': 5088, '명도': 5089, '가상하다': 5090, '중이병': 5091, '넘어지다': 5092, '만인': 5093, '야만': 5094, '빨갛다': 5095, '동아리': 5096, '김하늘': 5097, '기초': 5098, '일케': 5099, '심취': 5100, '산다': 5101, '스며들다': 5102, '힝': 5103, '맘에안듬': 5104, '놨다': 5105, '전의': 5106, '패러독스': 5107, '애가': 5108, '인간극장': 5109, '계단': 5110, '무덤': 5111, '구멍': 5112, '클로이': 5113, '디테일': 5114, '곱다': 5115, '펜싱': 5116, '땡': 5117, '칠이': 5118, '뒈지다': 5119, '감상문': 5120, '끊임없다': 5121, '함정': 5122, '끈': 5123, '웬디': 5124, '는바': 5125, '쥬산': 5126, '대갈': 5127, '공상': 5128, '다프네': 5129, '후자': 5130, '상이': 5131, '샷': 5132, '신라': 5133, '에스트로겐': 5134, '하이퍼': 5135, '크리': 5136, '쓰이다': 5137, '조르다': 5138, '진도': 5139, '뻔햇': 5140, '엑': 5141, '팜므파탈': 5142, '추격': 5143, '화비': 5144, '정비': 5145, '단속': 5146, '투모로우': 5147, '프로젝트': 5148, '거래': 5149, '양자경': 5150, '글구': 5151, '사족': 5152, '졷': 5153, '조화': 5154, '어쩌다': 5155, '모기': 5156, '희망이': 5157, '전하': 5158, 'ㅕ': 5159, '희롱': 5160, '강철': 5161, '저학년': 5162, '크리스마스': 5163, '세명': 5164, '미국영화': 5165, '존예': 5166, '꾸준하다': 5167, '대리': 5168, '여친': 5169, '수호': 5170, '믹스': 5171, '전세계': 5172, '생선': 5173, '눈알': 5174, '폴라': 5175, '안티': 5176, '비평가': 5177, '이자벨': 5178, '모로': 5179, '젊은이': 5180, '에드': 5181, '김유미': 5182, '꽉': 5183, '정글': 5184, '아이유': 5185, '화해': 5186, '기독교인': 5187, 'ㅐ': 5188, '쎄다': 5189, '그중': 5190, '장진영': 5191, '해외': 5192, '뿌리다': 5193, '노동자': 5194, '망각': 5195, '둥이': 5196, '부활': 5197, '잼남': 5198, '몹시': 5199, '서영희': 5200, '주년': 5201, '궁금증': 5202, '부산': 5203, '노리다': 5204, '쏙': 5205, '툭하면': 5206, '불쌍타': 5207, '하편': 5208, '고기': 5209, '자평': 5210, '별명': 5211, '똑똑하다': 5212, '불가능하다': 5213, '연봉': 5214, '키이라': 5215, '윤후': 5216, '르완다': 5217, '난민': 5218, '배두나': 5219, '타이타닉': 5220, '전환': 5221, '멘토': 5222, '보구': 5223, 'ㅁㅇ': 5224, '토비': 5225, '작정': 5226, '정석': 5227, '토토': 5228, '김청기': 5229, '모양': 5230, '힐러': 5231, '프': 5232, '업다': 5233, '거여': 5234, '연속극': 5235, '고딕': 5236, '버튼': 5237, '부동산': 5238, '탈세': 5239, '고난': 5240, '공통점': 5241, '사생활': 5242, '웨슬리': 5243, '다문화': 5244, '비약': 5245, '시바': 5246, '항체': 5247, '동료': 5248, '리부트': 5249, '역류': 5250, '음향': 5251, '레이미': 5252, '남매': 5253, '직장인': 5254, '출연자': 5255, '최다니엘': 5256, '때로는': 5257, '독립영화관': 5258, '불호': 5259, '인정받다': 5260, '점차': 5261, '겔겔': 5262, '크레딧': 5263, '일방': 5264, '초라하다': 5265, '호기': 5266, '가만히': 5267, '철수': 5268, '캐치미': 5269, '유아': 5270, '잠기다': 5271, '첩보물': 5272, '탕': 5273, '보심': 5274, '밋었': 5275, '물폭탄': 5276, '중국사람': 5277, '입원': 5278, '저렴하다': 5279, '뻑': 5280, '장쯔이': 5281, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 5282, '동포': 5283, '글귀': 5284, '필': 5285, '소지섭': 5286, '공식': 5287, '룰': 5288, '절실': 5289, '혐': 5290, '최민수': 5291, '쪽바리': 5292, '씹다': 5293, '귀가': 5294, '총기': 5295, '다치다': 5296, '최대한': 5297, '반점': 5298, '외국인': 5299, '성립': 5300, '농락': 5301, '청리': 5302, '샤론': 5303, '강간': 5304, '순환선': 5305, '인굿': 5306, '컴퍼니': 5307, '순정': 5308, '히트': 5309, '만지다': 5310, '어마': 5311, '컴퓨터그래픽': 5312, '피아니스트': 5313, '브로디': 5314, '송하윤': 5315, '빅피쉬': 5316, '이상기': 5317, '트리': 5318, '최시원': 5319, '루시': 5320, '극영화': 5321, '서방': 5322, '숭배': 5323, '수컷': 5324, '파국': 5325, '짜내다': 5326, '벗겨지다': 5327, '인종': 5328, '이순신': 5329, '여우주연상': 5330, '옥수수': 5331, '밭': 5332, '체스': 5333, '우아': 5334, '아유': 5335, '생소하다': 5336, '십중팔구': 5337, '임용': 5338, '이제껏': 5339, '타레가': 5340, '뭍': 5341, '생전': 5342, '액트오브밸러': 5343, '론서바이버': 5344, '네이비씰': 5345, '스티븐시걸': 5346, '콘서트': 5347, '더니': 5348, '동반': 5349, '더보': 5350, '단번': 5351, '백프로': 5352, '힘없다': 5353, '어김없이': 5354, '우정은': 5355, '소스케': 5356, '윰': 5357, '상회': 5358, '낯': 5359, '추석': 5360, '재연': 5361, '미라': 5362, '스케이트장': 5363, '폐가': 5364, '감고': 5365, '운율': 5366, '공격': 5367, '유순하다': 5368, '여성성': 5369, '일기토': 5370, '지략': 5371, '맞짱': 5372, '오메': 5373, '깃털': 5374, '흑백영화': 5375, '진영화': 5376, '쿡': 5377, '사교': 5378, '셋트': 5379, '허세쩌': 5380, '수식어': 5381, '평가절하': 5382, '레빗': 5383, '중동': 5384, '나볼': 5385, '수나': 5386, '보증': 5387, '이성': 5388, '보셧어': 5389, '타겟': 5390, '따윈': 5391, '안중': 5392, '더군다나': 5393, '눈앞': 5394, '구출': 5395, '커스틴': 5396, '추연': 5397, '기력': 5398, '빅맨': 5399, '공이': 5400, '친일파': 5401, '충성': 5402, '부업': 5403, '모이다': 5404, '울먹이다': 5405, '무미건조': 5406, '쌩뚱맞고': 5407, '휴머니스트': 5408, '역설': 5409, '잇엇으': 5410, '테드': 5411, '야유': 5412, '하나라': 5413, '더러': 5414, '나비효과': 5415, '트루먼쇼': 5416, '엠버': 5417, '허드': 5418, '카펜터': 5419, '필수': 5420, '메간폭스': 5421, '미식축구': 5422, '둘일때': 5423, '샤를': 5424, '아우라': 5425, '개엿': 5426, '생뚱맞': 5427, '트란안훙꺼': 5428, '되드라구': 5429, '아름': 5430, '재계': 5431, '실실': 5432, '아이돌가수': 5433, '마에다': 5434, '아츠코': 5435, '차이나다': 5436, '핀란드': 5437, '할랫': 5438, '고은님': 5439, '아시안': 5440, '굴렁쇠': 5441, '벗기다': 5442, '갑날': 5443, '밖에는': 5444, '껄끄랏': 5445, '박한별': 5446, '샴푸': 5447, '변비': 5448, '버시': 5449, '닫다': 5450, '선희': 5451, '하숙': 5452, '사궈': 5453, '일상다반사': 5454, '다르덴': 5455, '차이밍량': 5456, '그릇': 5457, '재밋는데': 5458, '우습다': 5459, '버켓': 5460, '리스트': 5461, '트루': 5462, '스내치': 5463, '무리다': 5464, '정두홍': 5465, '액숀': 5466, '그늘': 5467, '간수': 5468, '적재적소': 5469, '일본자위대': 5470, '호모': 5471, '빼기': 5472, 'ㅎㅎㅎㅎㅎㅎㅎㅎ': 5473, '상품': 5474, '라이더': 5475, '느작없어': 5476, '슬펏음': 5477, '이맘': 5478, '수술': 5479, '컨저링': 5480, '브루노': 5481, '개독': 5482, '흐느적': 5483, '사인방': 5484, '울프': 5485, '스카': 5486, '삐리뽕': 5487, '애니메이션영화': 5488, '재활용': 5489, '왕가네': 5490, '지우개': 5491, '끝냇': 5492, '꼳': 5493, '짝짝': 5494, '종합': 5495, '볼떄': 5496, '그이': 5497, '황신혜': 5498, '티남': 5499, '무라카미': 5500, '정욕': 5501, '악한': 5502, '원도': 5503, '졸렬하다': 5504, '속물': 5505, '그리스도': 5506, '무릎': 5507, '꿇다': 5508, '야인시대': 5509, '똘볼수': 5510, '한희정': 5511, '가주': 5512, '천연색': 5513, '좌절': 5514, '선덕여왕': 5515, '일편단심': 5516, '최종': 5517, '모시': 5518, '관리자': 5519, '예원': 5520, '건졌넹': 5521, '가울': 5522, '싶넹': 5523, '스페셜': 5524, '윤시윤': 5525, '봣엇': 5526, '음량': 5527, '존쿠삭나온': 5528, '존쿠삭연기': 5529, '이쯤': 5530, '폼': 5531, '씬시티': 5532, '더도': 5533, '김리나': 5534, '유키스': 5535, '세계대전': 5536, '피고': 5537, '지휘': 5538, '고위': 5539, '장교': 5540, '하드코어': 5541, '부각시키다': 5542, '갈라티아': 5543, '이수경': 5544, '효리': 5545, '외도': 5546, '통채': 5547, '건물': 5548, '지하가': 5549, '편찮다': 5550, '낭': 5551, '이상훈': 5552, '트림': 5553, '김영애': 5554, '벡터맨': 5555, '프로도': 5556, '영관': 5557, '리플릿': 5558, '이영': 5559, '짊': 5560, '어진': 5561, '여담': 5562, '프시': 5563, '황금기': 5564, '춘추전국': 5565, '베이비': 5566, '아포칼립토': 5567, '초입': 5568, '찌그러지다': 5569, '완죤반했엇': 5570, '팡': 5571, '지엔': 5572, '평민': 5573, '동원': 5574, '대군': 5575, '제나라': 5576, '드라마틱하다': 5577, '쩌는구': 5578, '배분': 5579, '음정': 5580, '이하늬': 5581, '개솔': 5582, '혼잡하다': 5583, '카톨릭': 5584, '그리스도교': 5585, '유일신': 5586, '하느님': 5587, '애국가': 5588, '퀴어': 5589, '재및음': 5590, '통과': 5591, '질왜': 5592, '달이': 5593, '훅': 5594, '지존': 5595, '황추생': 5596, '오진우': 5597, '메릴': 5598, '스트립': 5599, '시우민': 5600, '얼른': 5601, '것좀': 5602, '이취': 5603, '집합소': 5604, '습관': 5605, '수면제': 5606, '어쩌자': 5607, '깇체': 5608, '병태': 5609, '널린': 5610, '테레비': 5611, '고향': 5612, '주무': 5613, '꽃게': 5614, '존쿠삭': 5615, '언론': 5616, '개입': 5617, '일부분': 5618, '가다가': 5619, '탈선': 5620, '엎어지다': 5621, '해서웨이': 5622, '망첬': 5623, '다재': 5624, '얼버무리다': 5625, 'ㅆ': 5626, '박용우': 5627, '봫': 5628, '맥클레인': 5629, '보실': 5630, '낰였다': 5631, '프리미엄': 5632, '이선균': 5633, '김상중': 5634, '계쇠': 5635, '홍진영': 5636, '애교': 5637, '서예': 5638, '손꼽다': 5639, '패트레이버': 5640, '퍼시픽': 5641, '림': 5642, '벗': 5643, '닭': 5644, '원빈': 5645, '마리오': 5646, '돈벌': 5647, '장소': 5648, '창업': 5649, '아이템': 5650, '험하다': 5651, '스승': 5652, '단념': 5653, '대소': 5654, '사운트': 5655, '트랙': 5656, '텔레비전': 5657, '화재': 5658, '맘속': 5659, '둘째딸': 5660, '지하실': 5661, '고사': 5662, '없슴': 5663, '그러면': 5664, '우즈': 5665, '홧팅': 5666, '미그기': 5667, '발사': 5668, '전투기': 5669, '격추': 5670, '글래스톤베리': 5671, '부패하다': 5672, '로마노프': 5673, '왕조': 5674, '뭣같': 5675, '항거': 5676, '폭도': 5677, '김아중': 5678, '화두': 5679, '식민지': 5680, '건설': 5681, '관광객': 5682, '룬드': 5683, '렌': 5684, '토니쟈': 5685, '인디언': 5686, '소리내다': 5687, '넘사벽': 5688, '년씨짘': 5689, '나올때마닼': 5690, '으헠': 5691, '레버': 5692, '델피': 5693, '측은하다': 5694, '직장': 5695, '미생': 5696, '딴판': 5697, '게속': 5698, '얼렁뚱땅': 5699, '발란스': 5700, '데이라잇': 5701, '프럼': 5702, '어스': 5703, '아이슬란드': 5704, '아일럔드': 5705, '샤워씬': 5706, '동창회': 5707, '노근리': 5708, '선글라스': 5709, '축': 5710, '니뽄류': 5711, '도시괴담': 5712, '쌈질': 5713, '하하호호': 5714, '낚시질': 5715, '플스': 5716, '로멘틱': 5717, '급식': 5718, '미스테리영화': 5719, '저스트': 5720, '위드': 5721, '년임': 5722, '에어컨': 5723, '모해': 5724, '원조교제': 5725, '유민': 5726, '찌이잉': 5727, '제리': 5728, '개보': 5729, '퀜틴영화': 5730, '댐': 5731, '희극배우': 5732, '같잖다': 5733, '무자': 5734, '격자': 5735, '월급': 5736, '와츠': 5737, '강석': 5738, '어렷을때': 5739, '강우석': 5740, '아사': 5741, '버터': 5742, '마시기': 5743, '프랑': 5744, '사강': 5745, '급박하다': 5746, '미술': 5747, '무극': 5748, '망극': 5749, '기념': 5750, '퀭': 5751, '앨고어': 5752, '평수': 5753, '화산고': 5754, '팔자': 5755, '야웅': 5756, '스퀘어': 5757, '닉스': 5758, '합병': 5759, '크리처': 5760, '가원': 5761, '혜결': 5762, '기여': 5763, '닥본할끙': 5764, '미란': 5765, '연대': 5766, '김진수': 5767, '강간범': 5768, '마가렛': 5769, '없엇으': 5770, '더재밋엇을듯': 5771, '나이트': 5772, '랬': 5773, '전당포': 5774, '스무살': 5775, '유로': 5776, '정원': 5777, '유토피아': 5778, '부시': 5779, '이역': 5780, '이수만': 5781, '미천하다': 5782, '빙점': 5783, '이레': 5784, '이상인': 5785, '뮬란': 5786, '전쟁씬': 5787, '맴도': 5788, '단것': 5789, '이이경': 5790, '기타등등': 5791, '시간대': 5792, '처가': 5793, '궁': 5794, '홀딱': 5795, 'ㅈㄷㄹ': 5796, '마이티': 5797, '껀': 5798, '한거자': 5799, '이라곤': 5800, '격거봣': 5801, '왕따': 5802, '화병': 5803, '혼하': 5804, '루터': 5805, '평등하다': 5806, '백제': 5807, '털': 5808, '홍길동전': 5809, '힐줄': 5810, '어머나': 5811, '황폐': 5812, '각심': 5813, '급작': 5814, '의의': 5815, '바로바로': 5816, '씨부리다': 5817, '의정': 5818, '심혈': 5819, '기울이다': 5820, '슈퍼로봇': 5821, '화로': 5822, '빙자': 5823, '노틸러스호': 5824, '공중': 5825, '격침': 5826, '버지니아': 5827, '클레어': 5828, '역사드라마': 5829, '주접': 5830, '이나라': 5831, '촌빨': 5832, '달기지': 5833, '미니어쳐': 5834, '우뢔매': 5835, '한하유': 5836, '얘길': 5837, '로간': 5838, '주로': 5839, '하층': 5840, '복수심': 5841, '빨치산': 5842, '약탈': 5843, '외로이': 5844, '마카로니': 5845, '선두': 5846, '에리오': 5847, '모리': 5848, '최루성': 5849, '디젤': 5850, '열뻐치': 5851, '타입': 5852, '차암': 5853, '그대': 5854, '피해망상': 5855, '틀림없다': 5856, '해리슨': 5857, '글렌': 5858, '클로즈': 5859, '출시': 5860, '디게': 5861, '화산': 5862, '범한': 5863, '나로': 5864, '올킬': 5865, '아랫': 5866, '반신반의': 5867, '가톨릭': 5868, '등급': 5869, '가야로': 5870, 'ㅡㅡㅋ': 5871, '쟁장': 5872, '팔마': 5873, '인스피릿': 5874, '비스트': 5875, '핑도네': 5876, '배필': 5877, '피어스': 5878, '브로스': 5879, '맹탕': 5880, '홀트': 5881, '일류': 5882, '곽부성': 5883, '고소영': 5884, '비트': 5885, '사뭇': 5886, '백발': 5887, '웄던': 5888, '염정': 5889, '변탠': 5890, '이연서': 5891, '뵙다': 5892, '추잡': 5893, '연산군': 5894, '샤시': 5895, '친딸': 5896, '인혜힘들': 5897, '어브': 5898, '어릴떄': 5899, '울고불고': 5900, '정기용': 5901, '차기': 5902, '돌려차기': 5903, '매치': 5904, '컴터': 5905, '마스다': 5906, '버러지': 5907, '년돈': 5908, '고학년': 5909, '덜덜': 5910, '인내력': 5911, '강하늘': 5912, '추락': 5913, '자본주의': 5914, '베이컨': 5915, '지스': 5916, '영화장르': 5917, '천은': 5918, '누규': 5919, '판박이': 5920, '꾀': 5921, '월스트리트': 5922, '평론': 5923, '오정희': 5924, '섹': 5925, '전태일': 5926, '헛되': 5927, 'ㅎㅅㅎ': 5928, '일본드라마': 5929, '한눈': 5930, '이응': 5931, '스타트랙': 5932, '시설': 5933, '불면증': 5934, '재밋쎠': 5935, '집년': 5936, '참낰': 5937, '보세욬': 5938, '윤회사상': 5939, '단순화': 5940, '계절풍': 5941, '고려': 5942, '목도리': 5943, '백화': 5944, '외로': 5945, '내보내다': 5946, '잘빠지다': 5947, '에스': 5948, '피오': 5949, '박진영': 5950, '비밀결혼': 5951, '사기죄': 5952, '고소': 5953, '기반': 5954, '럴슨': 5955, '왜놈': 5956, '뜻대로': 5957, '김영민': 5958, '유능하다': 5959, '커트': 5960, '콕스였군': 5961, '문츠': 5962, '무진': 5963, '스키장': 5964, '빠리': 5965, '모자라': 5966, '살살': 5967, '간지럽다': 5968, '힌': 5969, '전화선': 5970, '고결하다': 5971, '하셧을까': 5972, '림프비즈킷': 5973, '쥑': 5974, '난널': 5975, '펑샤': 5976, '오강': 5977, '헛소리': 5978, '연도': 5979, '국물': 5980, '빈도': 5981, '종결': 5982, '레베카': 5983, '변치': 5984, '생뚱': 5985, '엉뚱': 5986, '갸우뚱': 5987, '랜드': 5988, '재정': 5989, '스탈린': 5990, '각도': 5991, '라든지': 5992, '이라든지': 5993, '잘살다': 5994, 'ㄲㅈ': 5995, '워킹데드': 5996, '훔': 5997, '컨디션': 5998, '이러니까': 5999, '가격': 6000, '흥정': 6001, '럴': 6002, '똥망': 6003, '물소': 6004, '얕다': 6005, '젠도': 6006, '안착': 6007, '배척': 6008, '국': 6009, '셨': 6010, '백만조': 6011, '송해성': 6012, '루비반지': 6013, '도무지': 6014, '진전': 6015, '경민이': 6016, '퍼붓다': 6017, '나이스': 6018, '연출자': 6019, '채용': 6020, '시스템': 6021, '외주': 6022, '잼슴': 6023, 'ㅇㅎ': 6024, '나야': 6025, '먹어주다': 6026, '옼': 6027, '앟': 6028, '드르륵': 6029, '톰크로즈': 6030, '실재': 6031, '뱅뱅': 6032, '허비하다': 6033, '노출하다': 6034, '장벽': 6035, '족족': 6036, '동무': 6037, '실연': 6038, '일본여행': 6039, '분과': 6040, '동일': 6041, '김민지': 6042, '이수혁': 6043, '남고': 6044, '김예림': 6045, '엘': 6046, '연결하다': 6047, '남용': 6048, '태민': 6049, '멤버': 6050, 'ㅈㄹ': 6051, '덴젤와싱턴': 6052, '모레쯔': 6053, '후덕': 6054, '슥': 6055, '뗼': 6056, '보상': 6057, '결실': 6058, '거두다': 6059, '멘트': 6060, '죄송': 6061, '드랍': 6062, '김태균': 6063, '재능': 6064, '분대': 6065, '맥주': 6066, '마시다': 6067, '적기가': 6068, '까비': 6069, '나잇스탠드': 6070, '사고방식': 6071, '밌다': 6072, '좁다': 6073, '의욕': 6074, '리프': 6075, '의젓하다': 6076, '터미널': 6077, '데드풀': 6078, '김용': 6079, '재밍': 6080, '프라': 6081, '병희': 6082, '촤근': 6083, '만만하다': 6084, '게이고': 6085, '수꼴': 6086, '좌빨': 6087, '인민재판': 6088, '김정은': 6089, '제국': 6090, '질의': 6091, '표상': 6092, '냉철하다': 6093, '철심': 6094, '어으어엉': 6095, '떼거지': 6096, '보편': 6097, '파시즘': 6098, '견지되': 6099, '독특': 6100, '마땅하다': 6101, '단역': 6102, '섯다': 6103, '열풍': 6104, '고온': 6105, '고니': 6106, '아귀': 6107, '설전': 6108, '외우다': 6109, '주근': 6110, '두기': 6111, '쌀': 6112, '시한': 6113, '욧': 6114, '윤석': 6115, '무위자연': 6116, '주몽': 6117, '총셋팅': 6118, '군생활': 6119, '크림': 6120, '열중': 6121, '수업': 6122, '안소니': 6123, '앨빈': 6124, '이러케': 6125, '파일량': 6126, '인간성': 6127, '앱스토어': 6128, '애플': 6129, '안드로이드': 6130, '시시': 6131, '껄렁하다': 6132, '육신': 6133, '핥다': 6134, '패틴슨': 6135, '무뇌충일': 6136, '파라다이스목장': 6137, '양면': 6138, '정준': 6139, '여현수': 6140, '이원종': 6141, '김사랑': 6142, '건너': 6143, '쪽나': 6144, '정이': 6145, '뛰어다니다': 6146, '커다랗다': 6147, '금욕': 6148, '음탕하다': 6149, '리눅스': 6150, '과유': 6151, '불급': 6152, '어울림': 6153, '살맛': 6154, '안듬': 6155, '서울': 6156, '쎼뇨리따': 6157, '무소유': 6158, '가트': 6159, '바콜': 6160, '멘스': 6161, '감미': 6162, '포레스트검프': 6163, 'ㅠㅜㅠ': 6164, '한국어': 6165, '민망': 6166, '정시': 6167, '폐허': 6168, '핵전쟁': 6169, '삿다': 6170, '최진혁': 6171, '꺄악': 6172, '삼장': 6173, '앙탈': 6174, '재밋는뎅': 6175, '점임': 6176, '맞먹다': 6177, '헤니': 6178, '억압': 6179, '소시민': 6180, '과감': 6181, '신춘': 6182, '과욕': 6183, '리도': 6184, '강지환': 6185, '쟁쟁': 6186, '격투': 6187, '경전': 6188, '어간': 6189, '넘흐': 6190, '아수라': 6191, '헨젤': 6192, '그레텔': 6193, '캠프': 6194, '오기': 6195, '웨이': 6196, '지밀': 6197, '명량해전': 6198, '마파도': 6199, '뼈대': 6200, '박정아': 6201, '취학': 6202, '안경': 6203, '영화음악': 6204, '번뜩이다': 6205, '괜챦음': 6206, '작곡': 6207, '파스': 6208, '쌕시': 6209, '시샘': 6210, '근친상간': 6211, '메': 6212, '드래곤': 6213, '토르': 6214, '잡수다': 6215, '선방': 6216, '산삼': 6217, '무림': 6218, '씻다': 6219, '대회': 6220, '가차': 6221, '와인': 6222, '부르짖다': 6223, '문법': 6224, '잘끝냇구': 6225, '터끝': 6226, '멍하니': 6227, '무표정': 6228, '쟤': 6229, '저력': 6230, '금융': 6231, '삼가다': 6232, '고인': 6233, '볼라': 6234, '화신': 6235, '미련': 6236, '모라': 6237, '날조': 6238, 'ㅋㅋㅋㄱ': 6239, '선교': 6240, '민영화': 6241, '데빌': 6242, '대강': 6243, '막만드': 6244, '구지': 6245, '친분': 6246, '특별출연': 6247, '천하': 6248, '양녕대군': 6249, '김재철': 6250, '전사': 6251, '발치': 6252, '색소폰': 6253, '청아': 6254, '곽재용': 6255, '강변': 6256, '발판': 6257, '갠차다': 6258, '재밋는듯': 6259, '별루더': 6260, '김순옥': 6261, '배수빈': 6262, '한상진': 6263, '김태현': 6264, '농간': 6265, '엄연하다': 6266, '재력': 6267, '오만해': 6268, '앞바다': 6269, '오염시키다': 6270, '생계': 6271, '상대로': 6272, '새마을운동': 6273, '노욕': 6274, '똥례': 6275, '레슬리': 6276, '닐슨': 6277, '찰리': 6278, '쉰': 6279, '멜라': 6280, '앤더슨': 6281, '라티': 6282, '파가': 6283, '레지나': 6284, '줄어들다': 6285, '훨배낫다': 6286, '상업성': 6287, '자세': 6288, '작업': 6289, 'ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ': 6290, '맘마미아': 6291, '시월애': 6292, '드라이빙': 6293, '롤': 6294, '몽롱': 6295, '넋': 6296, '먹거리': 6297, '허슬': 6298, '음울하다': 6299, '조여': 6300, '밤임': 6301, '라라피포': 6302, '부러': 6303, '오묘하다': 6304, '카타르': 6305, '시스': 6306, '버겁다': 6307, '카페': 6308, '발싸개': 6309, '빼어나다': 6310, '목표': 6311, '수도승': 6312, '떠내려가다': 6313, '폭스라이프': 6314, '실버': 6315, '이뿌다': 6316, '똥파리': 6317, '물어': 6318, '신랄하다': 6319, '윤여정': 6320, '진술': 6321, '금액': 6322, '유명배우': 6323, '정이안': 6324, '물체': 6325, '빠르기': 6326, '까먹다': 6327, '주앙': 6328, '큐브릭': 6329, '수목장': 6330, '지장': 6331, '우승': 6332, '송민호': 6333, '송윤아': 6334, '불운': 6335, '기득권': 6336, '백야': 6337, '샤말란': 6338, '박아': 6339, '정신분열증': 6340, '류승': 6341, '해주': 6342, '것땜': 6343, '담날': 6344, '윤한': 6345, '소연': 6346, '수역': 6347, '대관': 6348, '이경실': 6349, '안거': 6350, '범죄예방': 6351, '그릇되다': 6352, '결제': 6353, '판타지영화': 6354, '가벼워지다': 6355, '번지르르하다': 6356, '사라예보': 6357, '반대편': 6358, '심층': 6359, '시각장애인': 6360, 'ㄵ': 6361, '이준': 6362, '음청': 6363, '쓸엑': 6364, '바라지': 6365, '기상': 6366, '외한': 6367, '묶다': 6368, '알란': 6369, '옥죄': 6370, '강정원': 6371, '정연': 6372, '자리다': 6373, '인용': 6374, '비율': 6375, '익숙': 6376, '안정감': 6377, '풍취': 6378, '폴란드': 6379, '투영': 6380, '밑에님보': 6381, '뿜음': 6382, 'ㄱㄱ': 6383, '리더십': 6384, '천박': 6385, '게맛살': 6386, '덩달아': 6387, '점때': 6388, '케이크': 6389, '짝패': 6390, '샐러리맨': 6391, '초한지': 6392, '찌개': 6393, '벌리다': 6394, '영계': 6395, '노땅녀': 6396, '베베': 6397, '정기': 6398, '볼날': 6399, '셋별': 6400, '으잌': 6401, '사관학교': 6402, '부서': 6403, '책임자': 6404, '법인': 6405, '국방부': 6406, '소속': 6407, '기관': 6408, '책임지다': 6409, '척머슬러': 6410, '증언': 6411, '머임': 6412, '꼭두각시': 6413, '자고로': 6414, '땅속': 6415, '뭍혀': 6416, '부자간': 6417, '원망': 6418, '김현정': 6419, '겜블러': 6420, '게이물': 6421, '하반신': 6422, '아빠어디가': 6423, '보물': 6424, '형역': 6425, '올드보이': 6426, '성장기': 6427, '탈탈': 6428, '배알': 6429, '육식': 6430, '빌딩': 6431, '딧노': 6432, '부임': 6433, '여분': 6434, '가상현실': 6435, '딕': 6436, '해악': 6437, '대우': 6438, '여장': 6439, '화장': 6440, '여론': 6441, '상관관계': 6442, '숀팬': 6443, '강수연': 6444, '최정원': 6445, '신음': 6446, '넢어': 6447, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 6448, '그림판': 6449, '손손': 6450, '심리상담': 6451, '우상화': 6452, '망국': 6453, '멍청이': 6454, '배배꼬았다': 6455, '김명민': 6456, '연쇄살인범': 6457, '폐쇄된': 6458, '거죽': 6459, '입히다': 6460, '꼽는': 6461, '유해진': 6462, '구수하다': 6463, '맛깔나다': 6464, '이장님': 6465, '쩍': 6466, '눈살': 6467, '찌푸리다': 6468, '앓이': 6469, '유아인': 6470, '소윤': 6471, '바랬던': 6472, '단언컨대': 6473, '외치다': 6474, '원조': 6475, '우리동네': 6476, '언떤놈': 6477, '빡센': 6478, 'ㅋㄱ': 6479, '쌓이다': 6480, '정점': 6481, '빈스': 6482, '김수미': 6483, '계곡': 6484, '아무래도': 6485, '선하다': 6486, '이천원': 6487, '재밋는': 6488, '태희': 6489, '차승민': 6490, '숲속': 6491, '눈의여왕': 6492, '쓰뤠긔': 6493, '쌩뚱맞': 6494, '관좀': 6495, '복고': 6496, '건아': 6497, '쩌비': 6498, '낄낄대다': 6499, '풋함': 6500, '돈크라이마미': 6501, '스파르타': 6502, '필수요소': 6503, '선셋': 6504, '삼거리': 6505, '코스트': 6506, '나리': 6507, '찌릿': 6508, '짜릿': 6509, '쿠바': 6510, '토로': 6511, '박선영': 6512, '남장': 6513, '수트': 6514, '미남': 6515, '권유': 6516, '창조': 6517, '중복': 6518, 'ㅋㄲㅈㅁ': 6519, '드립': 6520, '낮': 6521, '수바': 6522, '문자': 6523, '썰전': 6524, '인맥': 6525, '레벨': 6526, '위인': 6527, '상영작': 6528, '현혹': 6529, '고객': 6530, '낚시': 6531, '콤': 6532, '엄기준': 6533, '매너': 6534, '블': 6535, '대적': 6536, '조달환': 6537, '이지혜': 6538, '인강': 6539, '요하': 6540, '유독': 6541, '장강': 6542, '육상': 6543, '첫걸음': 6544, '유학생': 6545, '교포': 6546, '스위프트': 6547, '쪙': 6548, '떡실신': 6549, '되돌아보다': 6550, '니미': 6551, '링컨': 6552, '바이올린': 6553, '쌍둥이': 6554, '줄라': 6555, '심판': 6556, '결선': 6557, '고시': 6558, '촌극': 6559, '야박하다': 6560, '이위': 6561, '공군': 6562, '군수': 6563, '멸망하다': 6564, '말껄': 6565, '국비': 6566, '종범': 6567, '이상자': 6568, '강심장': 6569, '뽱': 6570, '말빨': 6571, '한재석': 6572, '최정희': 6573, '태문': 6574, 'ㅣㅆ': 6575, '느덕': 6576, '조만간': 6577, '초록': 6578, '남자배우': 6579, '젤로': 6580, '배짱': 6581, '인구': 6582, '이기만': 6583, '중박': 6584, '프라챠': 6585, '핀카엡': 6586, '빈자리': 6587, '패닉': 6588, '경극': 6589, '컨': 6590, '주사': 6591, '락': 6592, '맨몸': 6593, '순전하다': 6594, '정조': 6595, '흠뻑': 6596, '부인': 6597, '가엾다': 6598, '로보트': 6599, '비원에이포': 6600, '멋진날': 6601, '섬': 6602, '까지의': 6603, '질병': 6604, '다이빙벨': 6605, '침몰': 6606, '매회': 6607, '수혁': 6608, '장철': 6609, '하규': 6610, '매니저': 6611, '카드': 6612, '잏': 6613, '무산': 6614, '오리진': 6615, '어쨋': 6616, '도기': 6617, '박제': 6618, '풍속': 6619, '학적': 6620, '가치나': 6621, '자의식': 6622, '꿈틀': 6623, '서투르다': 6624, '게으르다': 6625, '똥통': 6626, '해프닝': 6627, '헌재': 6628, '판결': 6629, '교복': 6630, '적대': 6631, '걸륜': 6632, '걸륜팬': 6633, '야마카시': 6634, '야수': 6635, '명곡': 6636, '줸좡': 6637, '채드': 6638, '머레이': 6639, '찾아다니다': 6640, '날카롭다': 6641, '형이상학적': 6642, '지각': 6643, '이뻣다': 6644, '진구': 6645, '됫음': 6646, '살기': 6647, '배구': 6648, '뻘짓': 6649, '멘붕': 6650, '페러다임': 6651, '헤집다': 6652, '이입': 6653, '일해': 6654, '중고생': 6655, '추어': 6656, '팽팽': 6657, '조율': 6658, '브이': 6659, '헤더': 6660, '이엄': 6661, '북경어': 6662, '이종수': 6663, '잛': 6664, '엊그제': 6665, '사계절': 6666, '파란색': 6667, '이세창': 6668, '공연장': 6669, '탕웨이': 6670, '옥보단': 6671, '데스노트': 6672, '테이큰': 6673, '마법천자문': 6674, '쩌구': 6675, '저쩌구': 6676, '김슬기': 6677, '아악': 6678, '맨앤': 6679, '퍼뜩': 6680, '최전선': 6681, '데려가다': 6682, '독일어': 6683, '백봉기': 6684, '레젼드': 6685, '미인': 6686, '골빈': 6687, '사라졋으': 6688, '발라': 6689, '처참하다': 6690, '잠기': 6691, '조이스틱': 6692, '장악': 6693, '지그': 6694, '빅매치': 6695, '컴텨': 6696, '비쥬': 6697, '흐리다': 6698, '레몬이': 6699, '진장': 6700, '소울메이트': 6701, '사운드트랙': 6702, '로섬': 6703, '헤드윅': 6704, '극우': 6705, '축하': 6706, '질적': 6707, '정준호': 6708, '종잡': 6709, '비밥': 6710, '쏫': 6711, '아지': 6712, '임꺽정': 6713, '극악': 6714, '외계': 6715, '코같다': 6716, '핫': 6717, '우엉': 6718, '건축학개론': 6719, '제겐': 6720, '이영애': 6721, '노찌': 6722, '쯔': 6723, '오만하다': 6724, '수뤠기': 6725, '알반': 6726, '환희': 6727, '물어보다': 6728, '프리즌브레이크': 6729, '갈구다': 6730, '깨어나다': 6731, '제자리': 6732, '미키': 6733, '셰릴': 6734, '린펜': 6735, '조안': 6736, '버런': 6737, '부리다': 6738, '지명도': 6739, '몰락하다': 6740, '닌자': 6741, '어쌔씬': 6742, '아라': 6743, '고래': 6744, '호들갑': 6745, '환복': 6746, '안전모': 6747, '전철': 6748, '멉': 6749, '일편': 6750, '쪼': 6751, '그랜트': 6752, '한자리': 6753, '삼박자': 6754, '절묘': 6755, '말장난': 6756, '르르': 6757, '모건': 6758, '뼈': 6759, '독': 6760, '고문': 6761, '자라다': 6762, '무리하다': 6763, '방학기': 6764, '동명': 6765, '읅': 6766, '포에버': 6767, '졸도': 6768, '로얄': 6769, '댄스': 6770, '들썩들썩': 6771, '구도': 6772, '사바세계': 6773, '중생': 6774, '받아들이다': 6775, '블랙리스트': 6776, '이어트': 6777, '어프': 6778, '할리데이': 6779, '광활하다': 6780, '로프': 6781, '인디펜던스': 6782, '전말': 6783, '이듭': 6784, '한공주': 6785, '바이오맨': 6786, '신상옥': 6787, '유학': 6788, '공채': 6789, '텔런튼데': 6790, '이구만': 6791, '학예회': 6792, '회사원': 6793, '부라': 6794, '워드': 6795, '응어리': 6796, '안속': 6797, '싱그럽다': 6798, '브라운관': 6799, '악하다': 6800, '무책임': 6801, '서인영': 6802, '김옥빈': 6803, '벙': 6804, '렌느': 6805, '회수': 6806, '로드리게즈': 6807, '용일': 6808, '암만': 6809, '사하나': 6810, '원더풀': 6811, '욕정': 6812, '불타다': 6813, '학위': 6814, '위조': 6815, '성범죄자': 6816, '제자': 6817, '허진호': 6818, '밨는데': 6819, '전설의고향': 6820, '의천도룡기': 6821, '난도': 6822, '댄싱': 6823, '안방': 6824, '만날': 6825, '맙소사': 6826, '모욕': 6827, '효시': 6828, '임정은': 6829, '빵꾸똥꾸': 6830, '앞세우다': 6831, '왕정': 6832, '무능하다': 6833, '하여튼': 6834, '은석': 6835, '치밀다': 6836, '선속': 6837, '머물다': 6838, '셀카': 6839, '거참': 6840, '친자': 6841, '겜블': 6842, '형사물': 6843, '펜': 6844, '영수': 6845, '병장': 6846, '해감': 6847, '밤벌레': 6848, '하룻밤': 6849, '신고식': 6850, '승연이': 6851, '사냥꾼': 6852, '스팅': 6853, '홧병': 6854, '당기다': 6855, '굿닥터': 6856, '갈아타다': 6857, '난간': 6858, '펙트': 6859, '한순간': 6860, '올랜도': 6861, '블룸': 6862, '다운로드': 6863, '개요': 6864, '것멋': 6865, '개폼': 6866, '선인장': 6867, '이상현': 6868, '몸소': 6869, '부녀': 6870, '조엘': 6871, '슈마허': 6872, '로빈': 6873, '어럈을때': 6874, '마스크': 6875, '련': 6876, '모터사이클': 6877, '제보자': 6878, '주소': 6879, '교육영화': 6880, '미덕': 6881, '유쾌': 6882, 'ㅈㅐ': 6883, '밌었다': 6884, '확확': 6885, '꽂히다': 6886, '역린': 6887, '아트': 6888, '무뇌충': 6889, '무식하다': 6890, '피드백': 6891, '보영': 6892, '걸치다': 6893, '소임': 6894, '오시': 6895, '마모루': 6896, '민정': 6897, '제시카알바': 6898, '윌슨': 6899, '느꼇다': 6900, '귀족': 6901, '사구조': 6902, '미결': 6903, '소오강호': 6904, '해전': 6905, '광신도': 6906, '암세포': 6907, '핫챠': 6908, '수법': 6909, '지롱': 6910, '깔깔': 6911, '볼케이노': 6912, '잼잼': 6913, '엑스맨': 6914, '증': 6915, '영희': 6916, '느님': 6917, 'ㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜㅜ': 6918, '단추': 6919, '에로물': 6920, '심리학자': 6921, '직소': 6922, '절댜': 6923, '가당': 6924, '기절': 6925, 'ㅜㅜㅜㅜ': 6926, '정준하': 6927, '을해': 6928, '마담': 6929, '프루스트': 6930, '견줄만': 6931, '유애': 6932, '엄지': 6933, '사악하다': 6934, '원인': 6935, '월리스': 6936, '그루밋때': 6937, '기기': 6938, '군상': 6939, '히든싱어': 6940, '쏙쏙': 6941, '이태준': 6942, '김민정': 6943, '나열': 6944, '저예산영화': 6945, '다크호스': 6946, '아이콘': 6947, '에이즈': 6948, '운동화': 6949, '프렌드': 6950, '복희': 6951, '쭉빵녀': 6952, '삐용': 6953, '리브스': 6954, '불록': 6955, '대만': 6956, '망측하다': 6957, '채팅': 6958, '퍼센트': 6959, '한없이': 6960, '라이오넬': 6961, '영홥': 6962, '시궁창': 6963, '신들리다': 6964, '충만': 6965, '카스': 6966, '어지럽히다': 6967, '암호': 6968, '모스부호': 6969, '텐션': 6970, '순식간': 6971, '니노': 6972, '이중인격': 6973, '정장': 6974, '땡땡': 6975, '질풍': 6976, '흑암': 6977, '천일': 6978, '유혹': 6979, '가감': 6980, '있엇으리': 6981, '처녀': 6982, '플랜카드': 6983, '환영': 6984, '자시다': 6985, '깨금': 6986, '죠스': 6987, '단계': 6988, '난날': 6989, '즈음': 6990, '녹음기': 6991, '베스트셀러': 6992, '태조': 6993, '왕건': 6994, '분노의질주': 6995, '세븐': 6996, '준애': 6997, '소양': 6998, '솔까말': 6999, '불행중': 7000, '최헌': 7001, '관대하다': 7002, '찰지다': 7003, '아메리칸': 7004, '녀놈': 7005, '뻣': 7006, '틸리': 7007, '깜찍': 7008, '그레이': 7009, '테마': 7010, '몰두': 7011, '리셋': 7012, '설키': 7013, '인간관계': 7014, '헬': 7015, '할머님': 7016, '이준기': 7017, '그다음': 7018, '단발머리': 7019, '점밑': 7020, '숨졸': 7021, 'ㅋㄷㅋㄷ': 7022, '킬킬': 7023, '봤늡데': 7024, '망햇': 7025, '신민아': 7026, '구상': 7027, '노자': 7028, '끼리끼리': 7029, '액': 7030, '이또': 7031, '오월': 7032, '야릇하다': 7033, '라디오헤드': 7034, '삽입곡': 7035, '화룡': 7036, '점정': 7037, '주룩': 7038, '김성균': 7039, '꼬부라지다': 7040, '혓소리': 7041, '김태연': 7042, '할숭': 7043, '괜찬': 7044, '차별성': 7045, '자지러지다': 7046, '알콜': 7047, '종착역': 7048, '대유': 7049, '트레비스': 7050, '밀양': 7051, '깊숙하다': 7052, '뛰어내리다': 7053, '이마트': 7054, '샷따': 7055, '소화기': 7056, '재밓당': 7057, '행여': 7058, '여름방학': 7059, '특선': 7060, '이루어지다': 7061, '면도': 7062, '독살': 7063, '안되겠니': 7064, '황금시간대': 7065, '수신료': 7066, '펜대': 7067, '맹승지': 7068, '돌진': 7069, '별룹니': 7070, '겐': 7071, '아찔하다': 7072, '간분': 7073, '킨': 7074, '중독증': 7075, '미워하다': 7076, '광장': 7077, '소유진': 7078, '스럽지도': 7079, '질소': 7080, '과자': 7081, '스킨헤드': 7082, '좀해': 7083, '그따위': 7084, '봉달': 7085, '화려': 7086, '옌': 7087, '사랑받다': 7088, '허전하다': 7089, '루퍼트': 7090, '편안함': 7091, 'ㅡㅜ': 7092, '애사': 7093, '갈겨쓰다': 7094, '화난': 7095, '루피': 7096, '명과': 7097, '아드레날린': 7098, '과다복용': 7099, '깡통': 7100, '구만': 7101, '에너지': 7102, '포토': 7103, '원어민': 7104, '오그': 7105, '보증수표': 7106, '불변': 7107, '주제넘다': 7108, '감별': 7109, '이태임': 7110, '엘리베이터': 7111, '터틀': 7112, '주크박스': 7113, '직선': 7114, '획기': 7115, '특권': 7116, '행위': 7117, '남지현': 7118, '정향': 7119, '하유미': 7120, '밤바': 7121, '웃찿사': 7122, '서수민': 7123, '자책': 7124, '시달리다': 7125, '갖가지': 7126, '승전': 7127, '결': 7128, '식임': 7129, '피겨': 7130, '월남': 7131, '절말': 7132, '휴대폰': 7133, '빠뜨리다': 7134, 'ㅉㅉㅉㅉ': 7135, '아이리스': 7136, '수치': 7137, '자시': 7138, '접합': 7139, '파이다': 7140, '환대': 7141, '런닝': 7142, '임도': 7143, '센치하다': 7144, '직업여성': 7145, '끝없이': 7146, '정명석': 7147, '군침': 7148, '기립박수': 7149, '여교사': 7150, '개잼': 7151, '부셰미': 7152, '시에나': 7153, '밀러': 7154, '으이': 7155, '걸스데이': 7156, '이혜리': 7157, '자잘하다': 7158, '숏컷': 7159, '관계성': 7160, '냉정': 7161, '배우진': 7162, '굿잡': 7163, '라이브': 7164, '전결': 7165, '후세': 7166, '김유정': 7167, '주임': 7168, '은밀': 7169, '나위': 7170, '음성': 7171, '스토커': 7172, '미져리': 7173, '칭한다': 7174, '자스민': 7175, '슴돠': 7176, '싸하다': 7177, '윈': 7178, '투어': 7179, '악평': 7180, '스피디함': 7181, '돌발': 7182, '황보라': 7183, '잘맞다': 7184, '그만두다': 7185, '리액션': 7186, '불닭': 7187, '무얼': 7188, '켈리': 7189, '쇄골': 7190, '님꺼': 7191, '다예': 7192, '감자별': 7193, '부작용': 7194, '뺒': 7195, '식물': 7196, '정윤희': 7197, '아기자기': 7198, '격파': 7199, '여호와': 7200, '증인': 7201, '본분': 7202, '조성하': 7203, '구체': 7204, '경선': 7205, '티프': 7206, '월터': 7207, '힐': 7208, '비장하다': 7209, '윌리스': 7210, '찰흙': 7211, '게바라': 7212, '예루살렘': 7213, '팔로우': 7214, '뿌리치다': 7215, '표지': 7216, '제이콥': 7217, '팔뚝': 7218, '성스럽다': 7219, '작작': 7220, '독도': 7221, '피리': 7222, '불면': 7223, '까딱까딱': 7224, '적꿈': 7225, '므흣': 7226, '두부': 7227, '빈스본': 7228, '사병': 7229, '호주': 7230, '로보캅': 7231, '자극시키다': 7232, '완주': 7233, '마라톤': 7234, '일석이조': 7235, '토막': 7236, '오마주': 7237, '특수분장': 7238, '울트라맨': 7239, '후짐': 7240, '끝장': 7241, '뒤뚱뒤뚱': 7242, '지은': 7243, '휴잭맨': 7244, '복수혈전': 7245, '까지와': 7246, '난뭐': 7247, '화이자': 7248, '옥소리': 7249, '프로필': 7250, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 7251, '대못': 7252, '내려오다': 7253, '예언': 7254, '새롭웠': 7255, '활보': 7256, '고나은': 7257, '두서': 7258, '오그리다': 7259, '짤랐을꺼': 7260, '독재자': 7261, '괴수영화': 7262, '도랏': 7263, '어언': 7264, '히히히': 7265, '햇살': 7266, '부엌': 7267, '신년': 7268, '베를릴': 7269, '만으로는': 7270, '화백': 7271, '명탐정코난': 7272, '남도일': 7273, '미비하다': 7274, '아젛': 7275, '짬봉': 7276, '난왜릏': 7277, '끝판': 7278, '애쉬': 7279, '요호': 7280, '투캇': 7281, '에르': 7282, '체베트': 7283, '왕족': 7284, '희생양': 7285, '비운': 7286, '이아쉬': 7287, '찿': 7288, '빠담빠담': 7289, '빠져듬': 7290, '생명력': 7291, '뿜어대': 7292, '목도': 7293, '현란하다': 7294, '드라이버': 7295, '갓파더': 7296, '과장하다': 7297, '태고': 7298, '머리털': 7299, '워스트': 7300, '거꾸로': 7301, '폭소': 7302, '신비': 7303, '개대': 7304, '룸바': 7305, '치코': 7306, '나우': 7307, '재생': 7308, '왈츠': 7309, '톱스타': 7310, '양영희': 7311, '할로우': 7312, '뽐내다': 7313, '수배': 7314, '야스쿠니': 7315, '카메런': 7316, '방조명': 7317, '펠레': 7318, '베른': 7319, '라이어': 7320, '스티치': 7321, '튿': 7322, '불만족': 7323, '자위대': 7324, '영화떄문': 7325, '측정': 7326, '여리다': 7327, '인문학': 7328, '분야': 7329, '해체': 7330, '수갑': 7331, '이인기': 7332, '생강빵': 7333, '군요': 7334, '문장': 7335, '송지효': 7336, '개구': 7337, '부정': 7338, '엇음': 7339, '확신': 7340, '수학': 7341, '알러뷰': 7342, '중국드라마': 7343, '준정': 7344, '다물어지다': 7345, '구지성': 7346, '백내장': 7347, '와오라니': 7348, '족장': 7349, '허벅지': 7350, '쓰다듬다': 7351, '트레': 7352, '헌터': 7353, '군국': 7354, '묵념': 7355, '페제': 7356, '저조하다': 7357, '뽀뽀': 7358, '질임': 7359, '담론': 7360, '효율': 7361, '가성': 7362, '반타작': 7363, '입가': 7364, '방사': 7365, '수합': 7366, '수정': 7367, '핑계': 7368, '정부': 7369, '서구': 7370, '하나요': 7371, '외상': 7372, '속임수': 7373, '인런글': 7374, '자서': 7375, '올바르다': 7376, '흐믓하': 7377, '리바이': 7378, '줄곧': 7379, '짤': 7380, '갈비': 7381, '잭맨': 7382, '기독교도': 7383, '아저씬': 7384, '최양일': 7385, '얍얍': 7386, '뚝딱': 7387, '연상연하': 7388, '취조': 7389, '통편집': 7390, '좆망': 7391, '리뉴': 7392, '산이면': 7393, '푸르다': 7394, '과민': 7395, '망우': 7396, '묘소': 7397, '아사카': 7398, '쿠': 7399, '완점잼': 7400, '섹히들': 7401, '뎌': 7402, '슌': 7403, '주귀': 7404, '오케이': 7405, '천진하다': 7406, '밥값': 7407, '룻': 7408, '애뜻함': 7409, '기아': 7410, '금치': 7411, '몸서리': 7412, '다물다': 7413, '지쯔': 7414, '윤종신': 7415, '이하늘': 7416, '뽑히다': 7417, '심사': 7418, '위원': 7419, '쌓다': 7420, '어허': 7421, '무성': 7422, '똥꼬': 7423, '아워스': 7424, '계승': 7425, '순결': 7426, '명문': 7427, '식겁하다': 7428, '소신': 7429, '호비다': 7430, '손가락': 7431, '짤림': 7432, '츤데레': 7433, '스노우': 7434, '깜짝깜짝': 7435, '단발': 7436, '스티플러': 7437, '법적': 7438, '날므': 7439, '시범': 7440, '대희': 7441, '전화': 7442, '끊음': 7443, '전역': 7444, '생활관': 7445, '통일': 7446, '중요시': 7447, '은성': 7448, '명민하다': 7449, '띠': 7450, '띠디띠': 7451, '맥락': 7452, '터프': 7453, '전진': 7454, '당돌하다': 7455, '은별': 7456, '움속': 7457, '나후': 7458, '아스카': 7459, '읽히다': 7460, '저리다': 7461, '공정하다': 7462, '결과물': 7463, '오현민': 7464, '봉만대': 7465, '이해력': 7466, '도시락': 7467, '씩씩하다': 7468, '국회의원': 7469, '오즈의마법사': 7470, '철통': 7471, '젬슴': 7472, '퀼리티쩌': 7473, '입술': 7474, '라시오': 7475, '마이애미': 7476, '서준영': 7477, '쿵쿵': 7478, '자연재해': 7479, '클라스': 7480, '출가': 7481, '은하사': 7482, '피좀': 7483, '가방': 7484, '압꿘': 7485, '뺑소니': 7486, '눈감다': 7487, '점심': 7488, '부러지다': 7489, '이착': 7490, '척움': 7491, '흉하다': 7492, '도개': 7493, '운치': 7494, '이식': 7495, '먹방': 7496, '클로즈업': 7497, '고귀하다': 7498, '뭉': 7499, '묵고': 7500, '댕기': 7501, '슈퍼스타': 7502, '짏': 7503, '윤숙': 7504, '파파야': 7505, '작작하다': 7506, '올리버': 7507, '무뇌': 7508, '족': 7509, '터테': 7510, '이닝': 7511, '반칙왕': 7512, '홍련같': 7513, '김지운': 7514, '가을로': 7515, '쫓기다': 7516, '아오뽁쳐': 7517, '미세': 7518, '스미스': 7519, '됫으': 7520, '스피릿': 7521, '봉테일': 7522, '형무소': 7523, '족구': 7524, '김연아': 7525, '에리': 7526, '소파': 7527, '뚱땡이': 7528, '왕년': 7529, '박노식': 7530, '박준규': 7531, '주머니': 7532, '루카스': 7533, '천천히': 7534, '물대포': 7535, '쏠때': 7536, '웃겻다': 7537, '테니스': 7538, '종목': 7539, '난생': 7540, '늙어감': 7541, '끄덕이다': 7542, '으로써는': 7543, '느꼇': 7544, '아울리다': 7545, '형용': 7546, '카니발': 7547, '사이드': 7548, '미러': 7549, '상대성': 7550, '이론': 7551, '끙': 7552, '지조': 7553, '베키': 7554, '반대말': 7555, '왜냐하면': 7556, '의료인': 7557, '교육인': 7558, '숙명': 7559, '만드심': 7560, '스토리텔링': 7561, '어내스트': 7562, '셀레스틴': 7563, '돌림': 7564, '이훨': 7565, '문성우': 7566, '써주다': 7567, '살타': 7568, '갈현': 7569, '두루': 7570, '고창': 7571, '따분': 7572, '베트공': 7573, '일병': 7574, '피해': 7575, '데미무어': 7576, '젖통': 7577, '화전': 7578, '오도': 7579, '넬': 7580, '곰탱이': 7581, '겸손': 7582, '무수': 7583, '들썩이다': 7584, '정상인': 7585, '감옥살이': 7586, '김갑수': 7587, '폭락': 7588, '졸료': 7589, '소모': 7590, '느거': 7591, '인관': 7592, '고거': 7593, 'ㅏㄱ': 7594, '김우빈': 7595, '좔좔': 7596, '최소': 7597, '양도': 7598, '헝편없어': 7599, '라우': 7600, '문서': 7601, '리허설': 7602, '인천': 7603, '뚬': 7604, '학부모': 7605, '여진구': 7606, '정진': 7607, '김규리': 7608, '킄': 7609, '전병': 7610, '인간드': 7611, '욱': 7612, '게봣습': 7613, '다시없다': 7614, '고집쟁이': 7615, '여야': 7616, '헛점많': 7617, '꼼꼼하다': 7618, '특정': 7619, '박형식': 7620, '선생': 7621, '다라': 7622, '이기심': 7623, '윤아': 7624, '웹툰': 7625, '독신': 7626, '포유': 7627, '부담스럽다': 7628, '깐느': 7629, '백만불': 7630, '급하다': 7631, '길들이다': 7632, '종료': 7633, '수정과': 7634, '마마마': 7635, '우측': 7636, 'ㅜㅜㅜㅜㅜㅜㅜ': 7637, '강점': 7638, '징용': 7639, '한인': 7640, '천명': 7641, '패전': 7642, '마감': 7643, '조상': 7644, '반공': 7645, '윤두준': 7646, '친해지다': 7647, '안도': 7648, '파일': 7649, '더구나': 7650, '애고': 7651, '헛봤다': 7652, '허드슨': 7653, '넌센스': 7654, '사시': 7655, '인과관계': 7656, '순대볶음': 7657, '자칭': 7658, '인심': 7659, '승려': 7660, '국교': 7661, '세균': 7662, '걔': 7663, '중화사상': 7664, '정통하다': 7665, '족도': 7666, '글치': 7667, '오죽힌': 7668, '뭘루': 7669, '깜바테': 7670, '디센트': 7671, '파스텔': 7672, '단원': 7673, '궤': 7674, '개운하다': 7675, '침울하다': 7676, '찮': 7677, '밑천': 7678, '현영': 7679, '덕의': 7680, '무녀': 7681, '쇼생': 7682, '애비': 7683, '아크엔젤': 7684, '졸데': 7685, '차븟': 7686, 'ㅇㄱ': 7687, '디시': 7688, '그리스': 7689, '감탄사': 7690, '뉴완다': 7691, '샬라샬': 7692, '즁': 7693, '쥬': 7694, '시베리아': 7695, '훈련': 7696, '작살': 7697, '일찐': 7698, '개제': 7699, '손현': 7700, '오룡': 7701, '썻다': 7702, '트이다': 7703, '이민': 7704, '약소국': 7705, '드리우다': 7706, '취했을뿐': 7707, '컴': 7708, '요로': 7709, '나본': 7710, '삼계탕': 7711, '후라이드': 7712, '삼겹살': 7713, '그랫쪄': 7714, '왜케많음': 7715, '핵꿀잼졸잼': 7716, '썪는줄': 7717, '비둘기': 7718, '성애자': 7719, 'ㅘ': 7720, 'ㅏㅏㅏ': 7721, '왜남': 7722, '보석같다': 7723, '노예': 7724, '마약상': 7725, '모조리': 7726, '답니': 7727, '벚꽃': 7728, '밀다': 7729, '치료': 7730, '썸머': 7731, '전수진': 7732, '이은우': 7733, '성수': 7734, '으로서의': 7735, '관계씬': 7736, '일삼': 7737, '말년': 7738, '고하': 7739, '노병': 7740, '싯달': 7741, '못때': 7742, '가식': 7743, '긴왤케': 7744, '향상': 7745, '악물다': 7746, '용의자': 7747, '뫼비우스': 7748, '환타지': 7749, '매장': 7750, '제시': 7751, '아이젠': 7752, '스마트': 7753, '김지석': 7754, '송새벽': 7755, '본전': 7756, '손호영': 7757, '오죽하다': 7758, '엔딩크레딧': 7759, '무지하다': 7760, '느끼하다': 7761, '스웨': 7762, '엇갈리다': 7763, '섭렵': 7764, '샤워': 7765, '말고도': 7766, '중공군': 7767, '각하': 7768, '참전용사': 7769, '호국': 7770, '영령': 7771, '죄송스럽다': 7772, '아바': 7773, '온라인': 7774, '경제': 7775, '갉다': 7776, '억울': 7777, 'ㅊ': 7778, '중주': 7779, '이끼': 7780, '폐쇄성': 7781, '익히다': 7782, '는고': 7783, '분열': 7784, '어법': 7785, '디디': 7786, '개간': 7787, '텝': 7788, '바퀴벌레': 7789, '국밥': 7790, '이명박': 7791, '사대강': 7792, '이대로': 7793, '큰일': 7794, '폐해': 7795, '막연하다': 7796, '문단속': 7797, '중요성': 7798, '불사': 7799, '숨바꼭질': 7800, '마지막방송': 7801, '신성록': 7802, '이율': 7803, 'ㅇㅇㅇ': 7804, '싸움판': 7805, '독일인': 7806, '강렬': 7807, '파도': 7808, '수반': 7809, '육중': 7810, '해병': 7811, '년놈': 7812, '만화챡': 7813, '읊어': 7814, '삭카': 7815, '로제': 7816, '주문': 7817, '어찌나': 7818, '무신': 7819, '때론': 7820, '낚곃네': 7821, '공지': 7822, '김여정': 7823, '출품': 7824, '박경원': 7825, '조수정': 7826, '이빨': 7827, '영물': 7828, '왜꼭': 7829, '완득이': 7830, '찌랭': 7831, '찮음': 7832, '상사': 7833, '생인': 7834, '윤호': 7835, '호탄': 7836, '정여립': 7837, '기축옥사': 7838, '연장': 7839, '어보': 7840, '명치': 7841, '깨달': 7842, '서류': 7843, '봉투': 7844, '상남자': 7845, '파고들다': 7846, '웟': 7847, '파이어': 7848, '질퍽': 7849, '산뜻하다': 7850, '버무러진': 7851, '이자나': 7852, '꾸리': 7853, '시외': 7854, '싱황': 7855, '꿈햇': 7856, '마물': 7857, '아숩다': 7858, '러': 7859, '중량': 7860, '세기말': 7861, '구슬': 7862, '꿰어': 7863, '보배': 7864, '가인': 7865, '정정은': 7866, '어케된거': 7867, '완표': 7868, '재영': 7869, '학기': 7870, '좃': 7871, '전방': 7872, '급속': 7873, '무제한': 7874, '반담횽': 7875, '디바이드': 7876, '읍니': 7877, '금방': 7878, '득템': 7879, '영화롭다': 7880, '케니지': 7881, '다잉영': 7882, '추악하다': 7883, '국방': 7884, '족속': 7885, '핸드': 7886, '사납다': 7887, '괴물영화': 7888, '박빙': 7889, '진부': 7890, '잠입': 7891, '양산': 7892, '스타크': 7893, '눕다': 7894, '무릅쏴': 7895, '사격': 7896, '알렉스': 7897, '오로린': 7898, '심심': 7899, '미묘': 7900, '가나다라': 7901, '알콜중독자': 7902, '전범': 7903, '서영': 7904, '유흥': 7905, '유명인사': 7906, '비싸다': 7907, '구두': 7908, '허울': 7909, '스키니진': 7910, '지드': 7911, '갈피': 7912, '넋두리': 7913, '훼': 7914, '여자아이': 7915, '청순하다': 7916, '응사': 7917, '한혜진': 7918, '지진희': 7919, '열연': 7920, '교도소': 7921, '구먼': 7922, '지아이조': 7923, '일본제국': 7924, '영점': 7925, '청국장': 7926, '잔악하다': 7927, '대길': 7928, '덕햇': 7929, '페이크': 7930, '이민정': 7931, '수천': 7932, '찌잉': 7933, '머릿': 7934, '아리땁다': 7935, '다케우치': 7936, '기모노': 7937, '그랜드': 7938, '부다페스트': 7939, '호텔': 7940, '김병조': 7941, '안과': 7942, '죽는겈': 7943, '딸도': 7944, '아비': 7945, '홀리랜드': 7946, '호야': 7947, '후끈': 7948, '후끈하다': 7949, '지당': 7950, '개이득': 7951, '이양': 7952, '금도': 7953, '속단': 7954, '할리': 7955, '아작': 7956, '소개팅': 7957, '박차다': 7958, '견우': 7959, '거린': 7960, '우물': 7961, '킹오파': 7962, '배틀로얄': 7963, '이영하': 7964, '아부지': 7965, '직시': 7966, '뺴': 7967, '극혐': 7968, '쫓아오다': 7969, '조문탁': 7970, '척도': 7971, '하울': 7972, '팥': 7973, '붕어빵': 7974, '해피앤드': 7975, '뭐시기': 7976, '페테': 7977, '그루지': 7978, '지잔': 7979, '노트': 7980, '불능': 7981, '박규리': 7982, '한승연': 7983, '정니콜': 7984, '구하라': 7985, '강지영': 7986, '카라': 7987, '카밀리아': 7988, '민감하다': 7989, '혐한': 7990, '호크': 7991, '팬심': 7992, '호평': 7993, '충무로': 7994, '막대': 7995, '출산': 7996, '오지랖': 7997, '아싸': 7998, '진입': 7999, '드넹': 8000, '유니세프': 8001, '리암': 8002, '슨': 8003, '잼없드': 8004, '개봉일': 8005, '먹이사슬': 8006, '기두': 8007, '윤설희': 8008, '주마': 8009, '지상': 8010, '통렬': 8011, '퀴': 8012, '릿카': 8013, '박은혜': 8014, '동양': 8015, '쩌러': 8016, '라거': 8017, '운영': 8018, '모퉁이': 8019, '더듬다': 8020, '에헤헹': 8021, '목격': 8022, '유턴': 8023, '착지': 8024, '어설품': 8025, '이펙트': 8026, '마침': 8027, '요일': 8028, '금토': 8029, '캡': 8030, '안당': 8031, '함속': 8032, '엉엉': 8033, '이혜영': 8034, '강남': 8035, '은색': 8036, '재규어': 8037, '외제차': 8038, '캡슐': 8039, '갸차폰': 8040, '완구': 8041, '답안': 8042, '국가대표': 8043, '똥쿠소': 8044, '찌끄레기들': 8045, '꿈나라': 8046, '진주': 8047, '이말년': 8048, '유물': 8049, '차이다': 8050, '진임': 8051, '거쫌': 8052, '도중': 8053, '베데스다': 8054, '작부': 8055, '나눔': 8056, '테스': 8057, '김조한': 8058, '쏭': 8059, '현태': 8060, '짜리몽땅': 8061, '여가': 8062, '깨물다': 8063, '리오': 8064, '모리꼬': 8065, '킥': 8066, '오컬트': 8067, '전문직': 8068, '호령': 8069, '루저': 8070, '다스베이더': 8071, '레이어': 8072, '정신없이': 8073, '곳도': 8074, '육감': 8075, '호호': 8076, '쨩': 8077, '녹': 8078, '독선': 8079, 'ㅠㅡㅠ': 8080, '콜라보': 8081, '썰다': 8082, '영리하다': 8083, '트렌디': 8084, '타계': 8085, '브래드': 8086, '역정': 8087, '리즈중': 8088, '도나': 8089, '설경구': 8090, '발산': 8091, '최적화': 8092, '마스터': 8093, '취권': 8094, '장엄하다': 8095, '엄숙하다': 8096, '은유': 8097, '봉': 8098, '위주': 8099, '이슈': 8100, '료': 8101, '칠하다': 8102, '천배': 8103, '뎃': 8104, '알렉산더': 8105, '비단': 8106, '네러티브': 8107, '취미': 8108, '올인': 8109, '천식': 8110, '창백하다': 8111, '볼껄그': 8112, '괴리감': 8113, '떨치다': 8114, '버무린': 8115, '시에라리온': 8116, '자이몬': 8117, '훈수': 8118, '존큐': 8119, '안젤라베이비': 8120, '꼴릿': 8121, '큰코다치다': 8122, '켄드릭': 8123, '김희로': 8124, '노골': 8125, '방한': 8126, '왜욕해': 8127, '더락': 8128, '존시나': 8129, '셧': 8130, '감당': 8131, '환포': 8132, '지라치': 8133, '다크라이': 8134, '디안시': 8135, '과잉': 8136, '이화여고': 8137, '지구과학': 8138, '숨': 8139, '셀프': 8140, '추강': 8141, '시중': 8142, '수만': 8143, '밋음': 8144, '머나멀다': 8145, 'ㅠㅠㅠㅠㅠㅠㅠㅠ': 8146, '미췬': 8147, '처먹어랔': 8148, '종일': 8149, '대니': 8150, '스티브유': 8151, '그린호넷': 8152, '기쁨': 8153, '섭리': 8154, '성미': 8155, '자애': 8156, '야심': 8157, '다방면': 8158, '보더': 8159, '진실되다': 8160, '대결': 8161, '라이드': 8162, '외쿡': 8163, '다수결': 8164, '운석': 8165, '다큐맨': 8166, '터리': 8167, '맑음': 8168, '파문': 8169, '격하': 8170, '다정하다': 8171, '점단': 8172, '샛기들': 8173, '잘봣으': 8174, '봣다': 8175, '소용': 8176, '넼': 8177, '서러움': 8178, '슷비슷비하': 8179, '이나마': 8180, '템포': 8181, '두드러지다': 8182, '오스먼트': 8183, '낯설다': 8184, '껀줄': 8185, '조미': 8186, '막문위': 8187, '쩡': 8188, '재밋게봐': 8189, '밋엇움': 8190, '네버엔딩': 8191, '간략하다': 8192, '불편': 8193, '서울시장': 8194, '후보': 8195, '착': 8196, '달라붙다': 8197, '이경영': 8198, '윤은혜': 8199, '무조': 8200, '장첸': 8201, '퀵이유': 8202, '차차': 8203, '레파': 8204, '벨아미': 8205, '로버트패틴슨': 8206, '지워지다': 8207, '보수': 8208, '패륜': 8209, '쌉싸름하다': 8210, '석가탄신일': 8211, '석탄일': 8212, '살피다': 8213, '전주': 8214, '국제': 8215, '김영하': 8216, '순서': 8217, '고등학생': 8218, '맹신': 8219, '시정': 8220, '이햐': 8221, '광관': 8222, '학자': 8223, '로마인': 8224, '주해': 8225, '근거': 8226, '전무하다': 8227, '씐': 8228, '부적': 8229, '소질': 8230, '무마': 8231, '대재앙': 8232, '무례하다': 8233, '황은정': 8234, '캡틴': 8235, '보때': 8236, '동민': 8237, '아더': 8238, '원탁': 8239, '랜슬롯': 8240, '란슬롯': 8241, '기네': 8242, '비어': 8243, '역도': 8244, '김강우': 8245, '깽': 8246, '옥택연': 8247, '마누라': 8248, '초능력자': 8249, '한효주': 8250, '처넌': 8251, '보너스': 8252, '픽사': 8253, '전라': 8254, '동키': 8255, '성실하다': 8256, '기적처럼': 8257, '늦가을': 8258, '산책': 8259, '우여곡절': 8260, '교섭': 8261, '가늠': 8262, '매경': 8263, '어학': 8264, '신기하': 8265, '헬로': 8266, '굼뜨': 8267, '느릿느릿': 8268, '익스펜더블': 8269, '백터': 8270, '이소재': 8271, '정신과': 8272, '신경질': 8273, '떽땍거리': 8274, '술함': 8275, '훈련소': 8276, '크': 8277, '민권': 8278, '손꾸락': 8279, '거열': 8280, '다모': 8281, '이원규': 8282, '대학로': 8283, '방송국': 8284, '박대동': 8285, '홍도': 8286, '쾌': 8287, '준면': 8288, '나잘하다': 8289, '궁합': 8290, '그해': 8291, '김현숙': 8292, '옥빈': 8293, '김소연': 8294, '꼽아': 8295, '부각': 8296, '걷다': 8297, '그렇지만': 8298, '채밌네': 8299, '로마시대': 8300, '대다수': 8301, '에린': 8302, '프레스토': 8303, '네요': 8304, '트라이앵글': 8305, '볼랫더': 8306, '라던가': 8307, '훌륭햇음': 8308, '기억상실증': 8309, 'ㅔㅔ': 8310, '나잇': 8311, '데드캠프': 8312, '생존': 8313, '좀재밋다': 8314, '개드립': 8315, '클릭': 8316, '완젼히': 8317, '가지가지': 8318, '더티': 8319, '로맨스코미디': 8320, '남궁민': 8321, '화잇팅': 8322, '조그만': 8323, '치열하다': 8324, '이돈': 8325, '몰랑몰랑': 8326, '자명하다': 8327, '스렉': 8328, '친일': 8329, '페넬로페': 8330, '노출씬': 8331, '장학우': 8332, '드뷔시': 8333, '달빛': 8334, '로티': 8335, '관능': 8336, '이민호': 8337, '대장': 8338, '핟러': 8339, '우주기지': 8340, '튼실하다': 8341, '갈갈': 8342, '세코': 8343, '부문': 8344, '회복': 8345, '본연': 8346, '무니': 8347, '인증': 8348, '바랬어': 8349, '즌': 8350, '만난': 8351, '신사참배': 8352, '케드': 8353, '칠흑': 8354, '추적자': 8355, '셜록홈즈': 8356, '권태기': 8357, '비일': 8358, '반적': 8359, '피트': 8360, '발동': 8361, '특공대': 8362, '장날': 8363, '겁내': 8364, '토크쇼': 8365, '구별': 8366, '발끝': 8367, '소환': 8368, '자새': 8369, '안재욱': 8370, '개새': 8371, '루쿠': 8372, '에반스': 8373, '비즐러': 8374, '엿들으': 8375, '왜색': 8376, '작고': 8377, '교활하다': 8378, '파렐': 8379, '제레미': 8380, '레너': 8381, '왕창': 8382, '브로드밴드': 8383, '낚였네': 8384, '공룡대탐험': 8385, '내버리다': 8386, '카밀라': 8387, '개봉관': 8388, '확보': 8389, '드뎌': 8390, '종말': 8391, '하인': 8392, '욱겨': 8393, '디지다': 8394, '건전하다': 8395, '대풍수': 8396, '교체': 8397, '헛짓임': 8398, '점말': 8399, '고결': 8400, '혼다': 8401, '메이저': 8402, '장담': 8403, '컨데': 8404, '리얼리즘': 8405, '네네': 8406, '먹히다': 8407, '편리': 8408, '오점': 8409, '노노': 8410, '살림': 8411, '리모콘': 8412, '펀집': 8413, '카톡': 8414, '트와일라잇': 8415, '뚝': 8416, '디질레': 8417, '각인': 8418, '진흙': 8419, '찍지마라': 8420, '오연': 8421, '서사시': 8422, '로빈스': 8423, '리포트': 8424, '모튼': 8425, '심즈': 8426, '재미엄': 8427, '유식': 8428, '마키': 8429, '궁극': 8430, '지점': 8431, '만듬': 8432, '잭키': 8433, '바운': 8434, '운스': 8435, '믿음직하다': 8436, '날카로워지다': 8437, '끙끙': 8438, '음침하다': 8439, '영화리뷰': 8440, '제곱': 8441, '까지를': 8442, '교차': 8443, '시방': 8444, '하윤': 8445, '나니아': 8446, '연대기': 8447, '크랭크': 8448, '울렁거리다': 8449, '호모포비아': 8450, '성현': 8451, '구사': 8452, '회보': 8453, '진찌': 8454, '잘라먹다': 8455, '싫어지다': 8456, '오랜만': 8457, '조은경': 8458, '입맞춤': 8459, '황진': 8460, '미씨': 8461, '탱': 8462, '침대': 8463, '옷벗다': 8464, '분잡': 8465, '에두': 8466, '신궁': 8467, '사담': 8468, '사십': 8469, '잘못짚다': 8470, '사들이다': 8471, '우레': 8472, '시가전': 8473, '낸시': 8474, '알렌': 8475, '기선': 8476, '뭉치': 8477, '싸대기': 8478, '멋졋음': 8479, '인철': 8480, '각기': 8481, '안정': 8482, '헥헥거리': 8483, '구니스': 8484, '구디넙': 8485, '감기': 8486, '신선': 8487, '핵꿀잼': 8488, '위태': 8489, '마지노선': 8490, '달마': 8491, '두사부일체': 8492, '주유소': 8493, '시리다': 8494, '넘버': 8495, '니키타': 8496, '뤽': 8497, '배송': 8498, '민요': 8499, '파랑새': 8500, '잡아넣다': 8501, '그룹': 8502, '더럽히다': 8503, '모자이크': 8504, '얙션': 8505, '토토가': 8506, '유플러스': 8507, '헛된': 8508, '코리안': 8509, '얼티': 8510, '텀': 8511, '굿윌헌팅도쩐당': 8512, '아씨': 8513, '신세': 8514, '와아아': 8515, '개편': 8516, '지상렬': 8517, '역주행': 8518, '차로': 8519, '희미하다': 8520, '일명': 8521, '닥치다': 8522, '무력하다': 8523, '앨리': 8524, '클레이': 8525, '더욱이': 8526, '다임': 8527, '미스코리아': 8528, '거젆': 8529, '이대': 8530, '사이코': 8531, '현기증': 8532, '목록': 8533, '베타': 8534, '황홀경': 8535, '속상하다': 8536, '뻑뻑': 8537, '얇다': 8538, '대전': 8539, '네덜란드인': 8540, '일제시대': 8541, '외세': 8542, '침입': 8543, '종류': 8544, '애완견': 8545, '복종': 8546, '배신자': 8547, '척결': 8548, '한창': 8549, '남북': 8550, '평화로': 8551, '서태지': 8552, '이연희': 8553, '하와': 8554, '우연찮': 8555, '이영은': 8556, '최성국': 8557, '윖': 8558, '별루란걸': 8559, '조심하다': 8560, '뎁': 8561, '스패': 8562, '고고': 8563, '서두르다': 8564, '숫자': 8565, '문지기': 8566, '규칙': 8567, '슬링': 8568, '접때': 8569, '상쾌': 8570, '껄끄런': 8571, '드라큐라': 8572, '이육사만': 8573, '딴사람': 8574, '이육사': 8575, '유나': 8576, '이남': 8577, 'ㅠㅂㅠ': 8578, '스톱모션': 8579, '정성': 8580, '못지않다': 8581, '미숙': 8582, '여실히': 8583, '장터': 8584, '정감': 8585, '문근영': 8586, '케보키언': 8587, '만을': 8588, '분신사바': 8589, '박재정': 8590, '윤소이': 8591, '메가박스': 8592, '죄악': 8593, '박하사탕': 8594, '으아아': 8595, '어그': 8596, '공백': 8597, '위안': 8598, '장정초': 8599, '빛깔': 8600, '시초': 8601, '논산': 8602, '마중가': 8603, '허락': 8604, '격은': 8605, '연하다': 8606, '많앗곸': 8607, '스타크래프트': 8608, '질럿들': 8609, '브래드피트': 8610, '동명이인': 8611, '초대': 8612, '승화': 8613, '전투력': 8614, '인어': 8615, '꼬리': 8616, '신비롭다': 8617, '노드': 8618, '해짐': 8619, '내려지다': 8620, '노개런티': 8621, '김우수': 8622, '유괴': 8623, '불협화음': 8624, '코네': 8625, '조앙': 8626, '연소자': 8627, '그랫': 8628, '어떨': 8629, '물고기': 8630, '어부': 8631, '초래': 8632, '소동': 8633, '음미': 8634, '스마일리': 8635, '머피': 8636, '일침': 8637, '가사': 8638, '실었는진': 8639, '인디밴드': 8640, '춥다': 8641, '한겨울': 8642, '안산': 8643, '예술의전당': 8644, '연합': 8645, '화남': 8646, '지자': 8647, '일진': 8648, '잠자코': 8649, '엠페러': 8650, '종결자': 8651, '장고': 8652, '우월': 8653, '남우': 8654, '가만있다': 8655, '불똥': 8656, '성냥': 8657, '재림': 8658, '제빵': 8659, '김탁구': 8660, '해롭다': 8661, '고의': 8662, '정연식': 8663, '파장': 8664, '은테': 8665, '드럼': 8666, '왓으': 8667, '다코타': 8668, '패닝': 8669, '간신히': 8670, '머시': 8671, '염': 8672, '화합': 8673, '왜만듬': 8674, '마리옹': 8675, '꼬띠': 8676, '부딪치다': 8677, '여하튼': 8678, '진의': 8679, '틴토': 8680, '잘만드': 8681, '닳다': 8682, '빈틈': 8683, '권선': 8684, '징악': 8685, '무용': 8686, '멕': 8687, '스파이': 8688, '어덜트': 8689, '어벤져스': 8690, '물결': 8691, '휩쓸다': 8692, '린듯': 8693, '미녀삼총사': 8694, '낭만자객': 8695, '시장': 8696, '사향': 8697, '남의껄': 8698, '못만듬': 8699, '이래도': 8700, '해밋': 8701, '수확': 8702, '셰인': 8703, '성지': 8704, '몬스터': 8705, '주식회사': 8706, '쪽지': 8707, '평땜': 8708, '자음': 8709, '엄태구': 8710, '혜영': 8711, '천만이': 8712, '동근': 8713, '종훈': 8714, '상하': 8715, '신현준': 8716, '셋트메뉴': 8717, '동양인': 8718, '서양인': 8719, '사죄': 8720, '잡기': 8721, '보도': 8722, '연맹': 8723, '명백하다': 8724, '불만제로': 8725, '가량': 8726, '국영': 8727, '사고뭉치': 8728, '눌물': 8729, '유후': 8730, '고등': 8731, '비디오카메라': 8732, '리턴': 8733, '참신': 8734, '허망': 8735, '학력': 8736, '중졸': 8737, '큰소리치다': 8738, '몽골': 8739, '인양': 8740, '젖': 8741, '매기': 8742, '큐땜': 8743, '올밴': 8744, '유세윤': 8745, '음주운전': 8746, '가이무': 8747, '오역': 8748, '에그': 8749, '리즈시절': 8750, '미쉘': 8751, '김정훈': 8752, '구스': 8753, '산트': 8754, '흐미': 8755, '헐겁다': 8756, '사사롭다': 8757, '친하다': 8758, '천원': 8759, '푸념': 8760, 'ㅆㅆㅆㅆㅆㅆ': 8761, '응답': 8762, '연령': 8763, '대별': 8764, '공산당': 8765, '위화': 8766, '북': 8767, 'ㅏㄷ': 8768, '될껀데': 8769, '둥둥': 8770, '떠다니다': 8771, '애마부인': 8772, '입맛': 8773, '나이트워치': 8774, '박얘쁜': 8775, '빠수니': 8776, '누명': 8777, '아웃': 8778, '입단': 8779, '곡예사': 8780, '줄타기': 8781, '사자': 8782, '윤주': 8783, '정호': 8784, '연씨': 8785, '에스팀': 8786, '유래': 8787, '탈락': 8788, '청탁': 8789, '국판': 8790, '브라더스': 8791, '지표': 8792, '관용': 8793, '바질': 8794, '리스크': 8795, 'ㄹㅏ': 8796, '체벌': 8797, '심금': 8798, '몸빵': 8799, '괜춘함': 8800, '겹': 8801, '빡': 8802, '꾸밈': 8803, '빈번': 8804, '여경': 8805, '경첨': 8806, '띄다': 8807, '신애': 8808, '휠씬잼밌': 8809, '노희경': 8810, '나수윤': 8811, '침묵': 8812, '이준익': 8813, '광': 8814, '코프': 8815, '드라만데': 8816, '이선': 8817, '민지': 8818, '라만': 8819, '핑': 8820, '한평생': 8821, '서서': 8822, '명예': 8823, '파렴치하다': 8824, '리자': 8825, '개멋': 8826, '홀홀': 8827, '교향곡': 8828, '저급': 8829, '긴지': 8830, '캐치온': 8831, '말리다': 8832, '한자': 8833, '비로소': 8834, '사대': 8835, '지못미': 8836, '은데': 8837, '원씨': 8838, '드러내다': 8839, '화통': 8840, '거돈': 8841, '어캐봐': 8842, '이두용': 8843, '렸': 8844, '간질': 8845, '긁다': 8846, '김해숙': 8847, '일장춘몽': 8848, '아론': 8849, '레논': 8850, '살수': 8851, '발암': 8852, '깝깝': 8853, '컷팅': 8854, '혼나다': 8855, '칙칙하다': 8856, '수긍': 8857, '밑바닥': 8858, '김혜리': 8859, '보물찾기': 8860, '미지': 8861, '판빙빙': 8862, '황효명': 8863, '광경': 8864, '밥말': 8865, '더블린': 8866, '남극': 8867, '휴먼': 8868, '췌밌는데': 8869, '어머님께': 8870, '외할아버지': 8871, '외할머니': 8872, '부여': 8873, '촌티': 8874, '유희': 8875, '오지명': 8876, '명의': 8877, '데뷰': 8878, '내적': 8879, '외적인': 8880, '정답': 8881, '랄거': 8882, '날짜': 8883, '왜정': 8884, '한지민': 8885, '세라': 8886, '저기': 8887, '박정철': 8888, '고릴라': 8889, '거도': 8890, '레즈비언': 8891, '배렸다': 8892, '후퇴': 8893, '퓨티드': 8894, '수두': 8895, '투신': 8896, '덴마': 8897, '박정민': 8898, '미만': 8899, '추접': 8900, '무모하다': 8901, '알앗슴': 8902, '으로만은': 8903, '마라천': 8904, '옆집': 8905, '괴기': 8906, '서울대': 8907, '굴려': 8908, '직종': 8909, '아팟': 8910, '분투': 8911, '옹졸하다': 8912, '뭐함': 8913, '홍수아': 8914, '커트코베인': 8915, '시원시원하다': 8916, '애인': 8917, '방공': 8918, '딱좋다': 8919, '세르': 8920, '지오': 8921, '구티': 8922, '레스': 8923, '슬레': 8924, '셔물': 8925, '들어맞다': 8926, '희귀': 8927, '웨딩싱어': 8928, '배심원': 8929, '는단': 8930, '조정석': 8931, '불평등': 8932, '미사여구': 8933, '루프': 8934, '사가다': 8935, '콜라': 8936, '에이스': 8937, '폭': 8938, '협동': 8939, '개인주의': 8940, '케르디오': 8941, '메로엣타': 8942, '맞서다': 8943, '뒤집어지다': 8944, '포럼': 8945, '윌': 8946, '에너미': 8947, '앳': 8948, '게이트': 8949, '전도': 8950, '소련군': 8951, '진격': 8952, '탈영병': 8953, '재밋는거': 8954, '동행': 8955, '가족사진': 8956, '사슴': 8957, '므': 8958, '최민식': 8959, '히스레져': 8960, '비견': 8961, '괜차늠': 8962, '딱지왕': 8963, '볼륨': 8964, '나른하다': 8965, '아메리칸파이': 8966, '괜시리': 8967, '공항': 8968, '딱딱하다': 8969, '조리': 8970, '스크립트': 8971, '글러': 8972, '바랬다': 8973, '열도': 8974, '대중화': 8975, '나물': 8976, '하등': 8977, '무섭딘': 8978, '잘나가다': 8979, '치히로': 8980, '행방불명': 8981, '겟썸': 8982, '삐': 8983, '알맹이': 8984, '치장': 8985, '자만': 8986, '특성': 8987, '출하': 8988, '오직': 8989, '강호': 8990, '흑전사': 8991, '매달': 8992, '아가': 8993, '할인': 8994, '평인': 8995, '블레어': 8996, '시프트': 8997, '정통': 8998, '메뚜기': 8999, '미미하다': 9000, '도신': 9001, '뉴욕': 9002, '직': 9003, '주사위': 9004, '엇네': 9005, '사리': 9006, '맛보다': 9007, '퀵': 9008, '그래비티': 9009, '영화제작사': 9010, '비강': 9011, '도박': 9012, '절친': 9013, '관여': 9014, '중견': 9015, '술사': 9016, '헛': 9017, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 9018, '구제불': 9019, '능이': 9020, '에드먼드': 9021, '젤리': 9022, '거들다': 9023, '하여간': 9024, '쥐뿔': 9025, '어머님': 9026, '삼십분': 9027, '왜나왓는': 9028, '불친절하다': 9029, '내해': 9030, '놈놈놈': 9031, '화살': 9032, '허리': 9033, '여군': 9034, '금단비': 9035, '까지라도': 9036, '성질': 9037, '이이해': 9038, '막내': 9039, '신발': 9040, '응응': 9041, '광팬': 9042, '일과': 9043, '취업': 9044, '안전': 9045, '바규': 9046, '실무': 9047, '플레이': 9048, '김경석': 9049, '쓰레길': 9050, '볼보': 9051, '밑밥': 9052, '끝낼떄': 9053, '실질': 9054, '공중전': 9055, '인크레더블': 9056, '대중성': 9057, '왜르케': 9058, '스메': 9059, '소드': 9060, '코스모폴리스': 9061, '퇴물': 9062, '죽어뿌': 9063, '일관': 9064, '헤드': 9065, '펑점': 9066, '무자비하다': 9067, '엥': 9068, '바론': 9069, '삽': 9070, '파내다': 9071, '탐구': 9072, '토익': 9073, '스리': 9074, '킵': 9075, '무빙': 9076, '포워드': 9077, '호킨스': 9078, '샘슨': 9079, '게일': 9080, '랜디': 9081, '우디알렌': 9082, '탱고': 9083, '배비장전': 9084, '격려': 9085, '방지법': 9086, '합성': 9087, '비틀어지다': 9088, '토대': 9089, '퀵실버': 9090, '유튜브': 9091, '학교괴담': 9092, '퀸틴': 9093, '포룸': 9094, '나카타': 9095, '유전자': 9096, '샌드맨': 9097, '왜안됫': 9098, '웅': 9099, '빠다': 9100, '더프': 9101, '난또': 9102, '원한': 9103, '디아나': 9104, '암프': 9105, '랄프': 9106, '들여다보다': 9107, '챔프': 9108, '허탈': 9109, '이미테이션': 9110, '쯧': 9111, '기인': 9112, '시아란': 9113, '힌즈': 9114, '걸즈': 9115, '창문': 9116, '캠프락': 9117, '버레스크등': 9118, '부수': 9119, '불사신': 9120, '꼬이다': 9121, '풀림': 9122, '계몽영화': 9123, '답습': 9124, '스트라이커': 9125, '몇대': 9126, '날고기': 9127, '코스': 9128, '르노': 9129, '라르': 9130, '브': 9131, '지크': 9132, '미처': 9133, '노도': 9134, '전직': 9135, '브라보': 9136, '느슨하다': 9137, '콧물': 9138, '드라마스페셜': 9139, '만년': 9140, '지망': 9141, '애환': 9142, '경력': 9143, '스웨덴': 9144, '흐헬': 9145, '횡단보도': 9146, '건너다': 9147, '이범수': 9148, '추상': 9149, '사토미': 9150, '이건모': 9151, '치매': 9152, '영화대본': 9153, '가위바위보': 9154, '말좀해': 9155, '기관사': 9156, '자수': 9157, '낙태': 9158, '한고은': 9159, '인적': 9160, '이탈리아': 9161, '세현': 9162, '비아': 9163, '눈길': 9164, '편지': 9165, '넴': 9166, '무책임하다': 9167, '다른사람': 9168, '쓰기': 9169, '마샬': 9170, '헛슨': 9171, '까지나': 9172, '라디오': 9173, '기숙': 9174, '전원': 9175, '에타': 9176, '숨지다': 9177, '우마': 9178, '동해': 9179, '호소': 9180, '요시히코': 9181, '엄따': 9182, '믕지': 9183, '방학': 9184, '뉴코아': 9185, '지배': 9186, '개월': 9187, '스카이': 9188, '쇼와시대': 9189, '대략': 9190, '웜홀': 9191, '친숙하다': 9192, '노트르담': 9193, '카사노바': 9194, '난대': 9195, '어가': 9196, '셀': 9197, '리아나': 9198, '애린': 9199, '는가': 9200, '에손': 9201, '얹다': 9202, 'ㅅㅂㅡㅡ': 9203, '아보': 9204, '포도': 9205, '딸기': 9206, '쭝쿠러': 9207, '로드무비': 9208, '눈뜨다': 9209, '샬로': 9210, '맹목': 9211, '샬': 9212, '살길': 9213, '꼬박': 9214, '추월': 9215, '가넷': 9216, '태우다': 9217, '사이더': 9218, '투입': 9219, '쒸레기': 9220, '옥주현': 9221, '진배': 9222, '이예': 9223, '킌': 9224, '아이맥스': 9225, '조우': 9226, '윤하': 9227, '논스톱': 9228, '자락': 9229, '순응': 9230, '세밀': 9231, '건일': 9232, '꼭보': 9233, '이즈': 9234, '구야': 9235, '쓰나미': 9236, '기겁': 9237, '대나무': 9238, '에서가': 9239, '미디어': 9240, '미지근하다': 9241, '뿜는': 9242, '서도': 9243, '코엑스': 9244, '아랫쪽': 9245, '배치': 9246, '충돌': 9247, '거룩하다': 9248, '구려': 9249, '이블데드': 9250, '정은': 9251, '암살': 9252, '껌': 9253, '김선빈': 9254, '달밤': 9255, '푸근하다': 9256, '매너리즘': 9257, '이노센스': 9258, '간접': 9259, '거북하다': 9260, '거처': 9261, '새끼고양이': 9262, '전선': 9263, '들이밀다': 9264, '투니버스': 9265, '열쇠': 9266, '겄': 9267, '꾹': 9268, 'ㅃㅋ': 9269, '눈을땔수': 9270, '일박이일': 9271, '멘타리': 9272, '제자리걸음': 9273, '퇴화': 9274, '유료': 9275, '사천원': 9276, '다니엘헤니': 9277, '기량': 9278, '본진': 9279, '헤드셋': 9280, '찌릴뻔': 9281, '눈밭': 9282, '꼬맹일때': 9283, '진좀': 9284, '이주': 9285, '꽁': 9286, '막바지': 9287, '순풍': 9288, '낚였': 9289, '남아도': 9290, '적월': 9291, '율': 9292, '이백만원': 9293, '벌금': 9294, '붕법': 9295, '설렁설렁': 9296, '혼': 9297, '이치': 9298, '닌교': 9299, '츠가이': 9300, '인형사': 9301, '연쇄': 9302, '당계례': 9303, '발차기': 9304, '독재정': 9305, '지시': 9306, '자알': 9307, '강풀': 9308, '벼': 9309, '지역감정': 9310, '공인': 9311, '민국이': 9312, '데뷔': 9313, '비속어': 9314, '이시영': 9315, '뚝심': 9316, '모욕감': 9317, '당하': 9318, '봤슴당': 9319, '위만': 9320, '김남길': 9321, 'ㅈㅈ': 9322, '미셸': 9323, '레오': 9324, '락스': 9325, '홀리모터스': 9326, '적지': 9327, '톡톡하다': 9328, '박쥐': 9329, '백미': 9330, '어슬픔': 9331, '영국영화': 9332, '서고': 9333, '강도': 9334, '인질': 9335, '하다못해': 9336, '덩': 9337, '비폭력': 9338, '딜레마': 9339, '남진': 9340, '코닌': 9341, '거짓말쟁이': 9342, '김영광': 9343, '경수진': 9344, '초로': 9345, '재밋네': 9346, '달팽이': 9347, '김프': 9348, '리맨': 9349, '균형': 9350, '용하다': 9351, '통일한국': 9352, '그리스도인': 9353, '블라인드': 9354, '탄식': 9355, '살며시': 9356, '박지수': 9357, '엣지': 9358, '초집': 9359, '습니': 9360, '햇습': 9361, '볼론': 9362, '점준새': 9363, '소시지': 9364, '박혓': 9365, '타락하다': 9366, '예비': 9367, '마르': 9368, '바벨': 9369, '강정': 9370, '그램': 9371, '고안': 9372, '정안': 9373, '느꼇는데': 9374, '트레일러': 9375, '분간': 9376, '에잉': 9377, '크리에이터': 9378, '압시': 9379, '비행': 9380, '화학': 9381, '봣습니닼': 9382, '잼잇엇숩니': 9383, '본가': 9384, '따먹다': 9385, '팔이만': 9386, '룸싸롱': 9387, '찌라시': 9388, '소비자': 9389, '상호': 9390, '만이라도': 9391, '그루': 9392, '가정은': 9393, '파탄': 9394, '꽁꽁': 9395, '싸': 9396, '조악하다': 9397, '주술': 9398, '그림형제': 9399, '버치': 9400, '크로이처': 9401, '소나타': 9402, '극명하다': 9403, '대론': 9404, '더라도': 9405, '퍼트': 9406, '오드리햅번': 9407, '플래닛': 9408, '비보': 9409, '이를': 9410, '나마': 9411, '일자리': 9412, '포탈': 9413, '아이로봇': 9414, '산낙지': 9415, '재기': 9416, '식당': 9417, '차세대': 9418, '언밸러스': 9419, '뚱뚱하다': 9420, '고역': 9421, '간간히': 9422, '계명': 9423, '병동': 9424, '로뎅': 9425, '아릅답': 9426, '까미유': 9427, '뇌리': 9428, '앨런': 9429, '알프레드': 9430, '투비': 9431, '임마': 9432, '쩌내': 9433, '비디오테잎': 9434, '좍좍': 9435, '패럴': 9436, '극도': 9437, '저해': 9438, '유년': 9439, '태운': 9440, '법칙': 9441, '주네': 9442, '워낭소리': 9443, '진개': 9444, '천카이거': 9445, '효느': 9446, '생명체': 9447, '진화': 9448, '한채영': 9449, '무식': 9450, '로디': 9451, '쉽죠잉': 9452, '지송': 9453, '강압': 9454, '주입': 9455, '실태': 9456, '평화롭다': 9457, '숙청': 9458, '강행': 9459, '뼈채': 9460, '덴젤': 9461, '청순': 9462, '번더': 9463, '신영화': 9464, '브는중': 9465, '익숙해지다': 9466, '가박': 9467, '장대': 9468, '소하': 9469, '이기주의': 9470, '이불': 9471, '덮다': 9472, '십대': 9473, '테크닉': 9474, 'ㅝ': 9475, '맛깔': 9476, '답임': 9477, '벡실': 9478, '츽오': 9479, '나늬겟': 9480, '솟아오르다': 9481, '샘물': 9482, '양파': 9483, '수염': 9484, '복잡': 9485, '진진': 9486, '스틴던스트': 9487, '예외': 9488, '오래도록': 9489, '석호': 9490, '올라서다': 9491, '할리우드영화': 9492, '읔': 9493, '읭스러움': 9494, '태클': 9495, '거때메': 9496, '어쩌실꺼': 9497, '속출': 9498, '시갈영홪우': 9499, '에게서': 9500, '자동': 9501, '응답기': 9502, '듯이': 9503, '과소': 9504, '가레스': 9505, '아주아주': 9506, '관조': 9507, '나부랭이': 9508, '진짴': 9509, '도시공학': 9510, '월리': 9511, '애견': 9512, 'ㅠㅅㅠ': 9513, '장서희': 9514, '못구': 9515, '다각': 9516, '보수파': 9517, '한판': 9518, '분나': 9519, '묘기': 9520, '썻는': 9521, '주저': 9522, '저수지': 9523, '펄프픽션': 9524, '꼽는다': 9525, '방귀만': 9526, '잔뜩뀌': 9527, '팬티': 9528, '클러버': 9529, '아늠': 9530, '돔': 9531, '때때로': 9532, '아이구': 9533, '왜썻을까': 9534, '티켓파워': 9535, '씨네프': 9536, '내뿜': 9537, '영홬': 9538, '루고': 9539, '멎다': 9540, '약자': 9541, '마야': 9542, '불안감': 9543, '이암': 9544, '부전': 9545, '워터': 9546, '마스코트': 9547, '희재': 9548, '빈번히': 9549, '블리치': 9550, '반올림': 9551, '막말': 9552, '오태식': 9553, '송시': 9554, '쉴드치다': 9555, '김대호': 9556, '병풍': 9557, '모시다': 9558, '태현': 9559, '경계': 9560, '산화': 9561, '웹': 9562, '까맣다': 9563, '쓸모없다': 9564, '뻣뻣하다': 9565, '퇴보': 9566, '아프리카': 9567, '사치': 9568, '서언': 9569, '서준이': 9570, '볼맛': 9571, '붙이': 9572, '심빠들': 9573, '도서관': 9574, '이하고': 9575, '퀸카': 9576, '쓰레기통': 9577, '물벼락': 9578, '낚인건': 9579, '허각': 9580, '노무': 9581, '엿같다': 9582, '배추': 9583, '월트디즈니': 9584, '도리': 9585, '가까이': 9586, '채시라': 9587, '한가인': 9588, '말입': 9589, '소블': 9590, '공블리': 9591, '미션': 9592, '난도질': 9593, '곤충': 9594, '딱이다': 9595, '실현': 9596, '이씨': 9597, '뮤직': 9598, '비됴': 9599, '실습': 9600, '시미즈': 9601, '어따': 9602, '욥': 9603, '제본': 9604, '미도리': 9605, '과다르': 9606, '솔직': 9607, '더블': 9608, '도일': 9609, '최상급': 9610, '조선시대': 9611, '난국': 9612, '밍': 9613, '우와한녀': 9614, '재개': 9615, '스러웟음': 9616, '비주류': 9617, '불가피하다': 9618, '지지다': 9619, '유유': 9620, '증폭': 9621, '코렌': 9622, '부의': 9623, '차예련': 9624, '으로서는': 9625, '오창석': 9626, '중도하차': 9627, '쯪쯔': 9628, '선언': 9629, '섥혀': 9630, '연줄': 9631, '빌어': 9632, '먹고살다': 9633, '야비하다': 9634, '촌철': 9635, '만듭': 9636, '망신': 9637, '프렌치': 9638, '캉캉': 9639, '불어': 9640, '관념': 9641, '이기대': 9642, '창희': 9643, '강산': 9644, '스탭': 9645, '오사카': 9646, '말함': 9647, '암툰': 9648, '무명': 9649, '권인지': 9650, '싸이다': 9651, '마이클잭슨': 9652, '비칭할때': 9653, '피크타임': 9654, '우스꽝스럽다': 9655, '씌우다': 9656, '카메오': 9657, '짙다': 9658, '라일': 9659, '골목': 9660, '상권': 9661, '슈퍼마켓': 9662, '후휘': 9663, '립': 9664, '도란': 9665, '세종대왕': 9666, '이승연': 9667, '계세': 9668, '안타': 9669, '여행가': 9670, '찬송': 9671, '성경책': 9672, '교인': 9673, '그렉': 9674, '박정학': 9675, '패널': 9676, '서운하다': 9677, '벅스라이프': 9678, '관광': 9679, '쿵푸': 9680, '자유분방하다': 9681, '집시': 9682, '정신의학': 9683, '분노조절': 9684, '증상': 9685, '파손': 9686, '선샤인': 9687, '금요일': 9688, '활력소': 9689, '보듬다': 9690, '고레': 9691, '히로': 9692, '아나킨': 9693, '쪽국': 9694, '퀼': 9695, '욕함': 9696, '민초': 9697, '나누어지다': 9698, '꽃봉오리': 9699, '분별': 9700, '정은채': 9701, '우울': 9702, '비용': 9703, '생산': 9704, '먹고다': 9705, '일이구': 9706, '대세': 9707, '배급': 9708, '한나': 9709, '넘겨보다': 9710, '요요': 9711, '무뚝뚝하다': 9712, '스탭들': 9713, '압삘럽': 9714, '안간힘': 9715, '거북': 9716, '한단': 9717, '정신승리': 9718, '곁들이다': 9719, '설계': 9720, '요런': 9721, '골드미스': 9722, '세바퀴': 9723, '봣드': 9724, '나이틀리': 9725, '정신장애': 9726, '틱장애': 9727, '해파리': 9728, '현수': 9729, '내사': 9730, '우먼': 9731, '이지현': 9732, '육체': 9733, '뿅': 9734, '힌국': 9735, '머좀': 9736, '무착': 9737, '지정학적': 9738, '패왕별희': 9739, '리멤버': 9740, '흐접': 9741, '어어어어': 9742, '관장': 9743, '뱃가이': 9744, '불리다': 9745, '교코': 9746, '케이코': 9747, '세이': 9748, '규': 9749, '우우': 9750, '귀찮다': 9751, '이정우': 9752, '다미': 9753, '김푸른': 9754, '봉사활동': 9755, '이인상': 9756, '그로테스크': 9757, '나제': 9758, '흘렷다': 9759, '파헤치다': 9760, '크리스티나': 9761, '나래': 9762, '가난': 9763, '최무룡': 9764, '맞장구': 9765, '부탄가스': 9766, '터뜨리다': 9767, '실사영화': 9768, 'ㅏㅋㅋ': 9769, '원보': 9770, '웃스': 9771, '정식': 9772, '왜왜왜': 9773, '미궁': 9774, '못하겄내': 9775, '하문': 9776, '미제': 9777, '느그': 9778, '중거': 9779, '따리': 9780, '낚었어': 9781, '왜케많': 9782, '후진국': 9783, '환가': 9784, '퀄': 9785, '써머': 9786, '관성': 9787, '걸핏하면': 9788, '깨지다': 9789, '재혼': 9790, '조울증': 9791, '웩': 9792, '기름': 9793, '갚다': 9794, '소감': 9795, '새미': 9796, '어드벤쳐': 9797, '용검': 9798, '위워회': 9799, '라닥': 9800, '복용': 9801, '유효하다': 9802, '디스크': 9803, '낯가림': 9804, 'ㅇㄴ': 9805, 'ㅁㅊ': 9806, '악의': 9807, '트집': 9808, '대접': 9809, '개차반': 9810, '저스틴': 9811, '팀버': 9812, '레이크': 9813, '연애소설': 9814, '드레곤': 9815, '기형': 9816, '찬성': 9817, '시온': 9818, '테라': 9819, '감임': 9820, '살색': 9821, '하늘나라': 9822, '레저': 9823, '재탄생': 9824, '서요': 9825, '통속': 9826, '개구리': 9827, '극찬': 9828, '재미나다': 9829, '굶주리다': 9830, '얻어맞다': 9831, '여우': 9832, '챠크라': 9833, '장례식': 9834, '엘레나': 9835, '드라이': 9836, '하이힐': 9837, '전기톱': 9838, '무쌍': 9839, '개똥': 9840, '망고': 9841, '위기': 9842, '매그놀리아': 9843, '년차': 9844, '최효종': 9845, '김원효': 9846, '꼬꼬': 9847, '스탠리': 9848, '효과음': 9849, '언더월드': 9850, '동굴': 9851, '없슴다': 9852, '들리다': 9853, '고집': 9854, '참사': 9855, '중이': 9856, '인어공주': 9857, '아웅': 9858, '도자기': 9859, '글쎼': 9860, '프랑스인': 9861, '회고': 9862, '라오스': 9863, '해빙': 9864, '사릉': 9865, '흡': 9866, '명량': 9867, '쩍발': 9868, '차도': 9869, '다니엘': 9870, '스콜': 9871, '세지': 9872, '쫭': 9873, '낮아지다': 9874, '맑은': 9875, '세탁기': 9876, '경화': 9877, '쿠엔틴': 9878, '광대하다': 9879, 'ㄴㅅ': 9880, '십분': 9881, '월드컵': 9882, '재밋게본': 9883, '에스프레소': 9884, '땡기다': 9885, '집대성': 9886, '힛걸': 9887, '모레츠': 9888, '맞춤': 9889, '면알': 9890, '가증': 9891, '짜증스럽다': 9892, '쑈할때': 9893, '행각': 9894, '뻔뻔': 9895, '메우다': 9896, '빈센트': 9897, '발작': 9898, '추기경': 9899, '교황': 9900, '격었': 9901, '동감': 9902, '니시다': 9903, '김현주': 9904, '활발하다': 9905, '드하': 9906, '김민': 9907, '에네스': 9908, '카야': 9909, '꺼리다': 9910, '개무시': 9911, '경기': 9912, '독사': 9913, '진저리': 9914, '스나입스': 9915, '똑': 9916, '미국드라마': 9917, '소담': 9918, '제대': 9919, '권력자': 9920, '산물': 9921, '부처': 9922, '사과': 9923, '신동': 9924, '뿌듯하다': 9925, '행간': 9926, '순진하다': 9927, '특선영화': 9928, '으이구': 9929, '여덟': 9930, '도라에몽': 9931, '애매': 9932, '헬스장': 9933, '사키': 9934, '부추기다': 9935, '추격씬': 9936, '한풀': 9937, '영도': 9938, '조선소': 9939, '지난해': 9940, '선박': 9941, '수주': 9942, '아웃사이더': 9943, '구급대원': 9944, '시킴': 9945, '비범하다': 9946, '부러워하다': 9947, '공작': 9948, '참새': 9949, '날아가다': 9950, '만끽': 9951, '양대': 9952, '산맥': 9953, '이보희': 9954, '에이브': 9955, '릴': 9956, '라빈': 9957, '낚였눼': 9958, '워리어': 9959, '고립': 9960, '혈육': 9961, '펌프': 9962, '노파': 9963, '김은형': 9964, '문명': 9965, '불알': 9966, '밋게봣': 9967, '딘': 9968, '몰래': 9969, '금기': 9970, '유사': 9971, '거북이': 9972, '모터': 9973, '최첨단': 9974, '그러기에': 9975, '날림': 9976, '살인씬': 9977, '친절': 9978, '오른': 9979, '뻐기다': 9980, '훨배': 9981, '쇼생크탈출': 9982, '요따위': 9983, '포르코': 9984, '저음': 9985, '욱일승천기': 9986, '일장기': 9987, '일맥상통': 9988, '택배': 9989, '머랄': 9990, '이삼': 9991, '아하': 9992, '롯데': 9993, '왜인': 9994, '업체': 9995, '유람선': 9996, '잠도': 9997, '체험': 9998, '퉁': 9999, '궈': 10000, '먹기': 10001, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 10002, '합격': 10003, '봉작': 10004, '자꾸만': 10005, '계집': 10006, '초상': 10007, '사빠': 10008, '순결하다': 10009, '곧다': 10010, '수원': 10011, '규모': 10012, '징징대다': 10013, '이탈리아인': 10014, '일어': 10015, '식객': 10016, '안토니오': 10017, '모티프': 10018, '작별인사': 10019, '토이스토리': 10020, '고시원': 10021, '마주치다': 10022, '심승보': 10023, '종북주의자': 10024, '판명': 10025, '국보법': 10026, '엄중하다': 10027, '다스리다': 10028, '이적': 10029, '빠아님': 10030, '와나': 10031, '럼': 10032, '골빈뇬들': 10033, '신기다': 10034, '수행': 10035, '조가': 10036, '리키': 10037, '슈러더': 10038, '주근깨': 10039, '울부짖다': 10040, '드릅': 10041, '훠': 10042, '얼씬': 10043, '최동훈': 10044, '전우치': 10045, '주심': 10046, '탁구': 10047, '질때': 10048, '술술': 10049, '흠결': 10050, '일뚱': 10051, '박지성': 10052, '얼리다': 10053, '나오넥': 10054, '밋엇다': 10055, '랭킹': 10056, '일텐데': 10057, '바지': 10058, '헐헐': 10059, '기능': 10060, '샤샤': 10061, '티라노': 10062, '뭐햇': 10063, '침팬지': 10064, '통행': 10065, '직진': 10066, '로큰롤': 10067, '여자도': 10068, '원수': 10069, '코코몽': 10070, '막일': 10071, '캐나다': 10072, '영화제작': 10073, '브라질': 10074, '관망': 10075, 'ㄹㅋ': 10076, '월러스': 10077, '처형': 10078, '울림': 10079, '제주도': 10080, '힘알': 10081, '로마군': 10082, '레어템': 10083, '템': 10084, '호박': 10085, '오죽': 10086, '잔대': 10087, '유캔': 10088, '퀀시': 10089, '시네마천국': 10090, '코러스': 10091, '찡끗': 10092, '강하': 10093, '기운': 10094, '꿋꿋하다': 10095, '왈가': 10096, '왈부': 10097, 'ㅎㅌㅊ': 10098, '최선': 10099, '최상': 10100, '낚일순': 10101, '랍니다': 10102, '확장': 10103, '맥과이어': 10104, '에어': 10105, '리언': 10106, '한일': 10107, '신카이': 10108, '마코토': 10109, '카나': 10110, '결여': 10111, '선입견': 10112, '꼴통': 10113, '페미니즘': 10114, '페미나치': 10115, '마인드': 10116, '존못': 10117, '나사': 10118, '고양': 10119, '웨폰': 10120, '어뜨케': 10121, '시꺼멓다': 10122, '뻔헸': 10123, '다지다': 10124, '따': 10125, '재발': 10126, '갓말띤줄알았': 10127, '렛': 10128, '아이디': 10129, '걸끝': 10130, '닮음': 10131, '골든': 10132, '라즈': 10133, '상식': 10134, '양키': 10135, '풍족하다': 10136, '팬픽': 10137, '배속': 10138, '고자': 10139, '제한': 10140, '유속': 10141, '이문식': 10142, '쇠발개쉐기': 10143, '파워레인저': 10144, '편리하다': 10145, '한가운데': 10146, '헤매다': 10147, '소림축구': 10148, '김두영': 10149, '보존': 10150, '분에이': 10151, '걸짝': 10152, '일도': 10153, '제하': 10154, '화재현장': 10155, '상반기': 10156, '날수': 10157, '와리': 10158, '색휘': 10159, '사로잡히다': 10160, '완젼빠': 10161, '장백지': 10162, '자부': 10163, '달성': 10164, '혈팬': 10165, '혜람이죽엇네': 10166, '사골': 10167, '우려': 10168, '먹듯': 10169, '썰매': 10170, '목적지': 10171, '데몰리션맨': 10172, '이퀄리브리엄': 10173, '가져다주다': 10174, '개살구': 10175, '맟춰': 10176, '메뉴': 10177, '드삼': 10178, '박스': 10179, '오피스': 10180, '재밌': 10181, '와이': 10182, '무치다': 10183, '쫙깔렷': 10184, '뒤쪽': 10185, '폭포': 10186, '비키다': 10187, '예의': 10188, '모호하다': 10189, '갸웃': 10190, '자위행위': 10191, '화평': 10192, '진화론': 10193, '깍지': 10194, '천안함프로젝트': 10195, '골깜': 10196, '부라리다': 10197, '마직': 10198, '막부': 10199, '구숙정': 10200, '가라앉다': 10201, '비열하다': 10202, '가스펠': 10203, '편곡': 10204, '브리짓스': 10205, '가래': 10206, '헤일': 10207, '테': 10208, '벨트': 10209, '거만하다': 10210, '사형수': 10211, '갈증': 10212, '해소': 10213, '수박도': 10214, '케토': 10215, '펠릭스': 10216, '라이터': 10217, '역행': 10218, '헤어지자': 10219, '가세': 10220, '욯': 10221, '어케되는': 10222, '순이': 10223, '다투다': 10224, '무표': 10225, '홍혜정': 10226, '이그': 10227, '마도': 10228, '후련': 10229, '나머': 10230, '월요일': 10231, '채탁연': 10232, '황우슬혜': 10233, '도가니탕': 10234, '상중하': 10235, '제어': 10236, '퀘': 10237, '뜻밖': 10238, '성추행': 10239, '공갈': 10240, '성매매': 10241, '알선': 10242, '포주': 10243, '소녀시대': 10244, '경쟁자': 10245, '뚜껑': 10246, '폐기물': 10247, '투닥': 10248, '기린': 10249, '이광수': 10250, '능력자': 10251, '비고': 10252, '모텐슨': 10253, '이스턴': 10254, '헛짓': 10255, '이상향': 10256, '스탈': 10257, '대국민': 10258, '박시환': 10259, '난입': 10260, '침': 10261, '쿨하다': 10262, '캄탄할': 10263, '보고따': 10264, '말이얌': 10265, '재밋내': 10266, '리버': 10267, '피닉스': 10268, '공동체': 10269, '포퐁': 10270, '진호': 10271, '하겟네별': 10272, '어나': 10273, '종방': 10274, '방도': 10275, '수백향': 10276, '바른': 10277, '아스': 10278, '트랄': 10279, '놨': 10280, '민세': 10281, '박영린': 10282, '결집': 10283, '개발': 10284, '자빠지다': 10285, '찡하다': 10286, '씨익': 10287, '윽수': 10288, '마법사': 10289, '실비': 10290, '재일동포': 10291, '분단': 10292, '조총련': 10293, '소외': 10294, '차별': 10295, '에이리언': 10296, '욕설': 10297, '엄지원': 10298, '이지아': 10299, '가누다': 10300, '멍멍': 10301, '실습생': 10302, '큰작가되셩': 10303, '문소리': 10304, '톨스토이': 10305, '사상가': 10306, '소로': 10307, '농부': 10308, '일본군': 10309, '나스': 10310, '타샤': 10311, '킨스키': 10312, '델마와루이스': 10313, '케이스': 10314, '너덜너덜': 10315, '누더기': 10316, '리본': 10317, '하고만': 10318, '모독': 10319, '구관': 10320, '명관': 10321, '닭목': 10322, '브금': 10323, '가만': 10324, '정치사': 10325, '회상': 10326, '금성': 10327, '샘플': 10328, '재밋구': 10329, '대규모': 10330, '해상전': 10331, '터너': 10332, '잭스': 10333, '호홉': 10334, '토닥토닥': 10335, '로라': 10336, '이글': 10337, '젖다': 10338, '블렉코메디': 10339, '메딘': 10340, '스마트폰': 10341, '볼바': 10342, '덤덤하다': 10343, '천정명': 10344, '온주완': 10345, '마란': 10346, '존잼': 10347, '벌로': 10348, '죨': 10349, '김조광수': 10350, '보셩': 10351, '휴그랜트': 10352, '제데로': 10353, '고이': 10354, '라이즈': 10355, '여학생': 10356, '백마': 10357, '뮤비': 10358, '압박': 10359, '폴라로이드': 10360, '사진기': 10361, '대조': 10362, '전우': 10363, '몸값': 10364, '소심하다': 10365, '파쿠르': 10366, '레닌': 10367, '시숙': 10368, '숙': 10369, '강시선생': 10370, '노다메': 10371, '아슬아슬하다': 10372, '무궁무진': 10373, '길래': 10374, '뚱보흑': 10375, '피디': 10376, '가타카': 10377, '이다윗': 10378, '어리석다': 10379, '황정음': 10380, '정경호': 10381, '류수영': 10382, '지미': 10383, '매튜': 10384, '맥커너히': 10385, '두고두고': 10386, '아닐런지': 10387, '토의': 10388, '부터의': 10389, '일어서다': 10390, '마당': 10391, '줫': 10392, '십이': 10393, '카운트': 10394, '한일월드컵': 10395, '고루': 10396, '지향': 10397, '이정국': 10398, '짚다': 10399, '비치다': 10400, '년안': 10401, '작품하나': 10402, '결심': 10403, '조성은': 10404, '팔레스타인': 10405, '암도': 10406, '유영': 10407, '어메이징': 10408, '가제': 10409, '총사': 10410, '충동': 10411, '인도영화': 10412, '요기': 10413, '최지우': 10414, '위안부': 10415, '예매': 10416, '허둥대다': 10417, '어둠': 10418, '신밧드': 10419, '험담': 10420, '오한': 10421, '쯔무시': 10422, '구원': 10423, '이듬': 10424, '유동근': 10425, '의형제': 10426, '창의': 10427, '학원물': 10428, '활용': 10429, '줫다': 10430, '원호': 10431, '선출': 10432, '쟁탈전': 10433, '쇼핑': 10434, '보석': 10435, '다이아몬드': 10436, '돌아이': 10437, '얼릉': 10438, 'ㅅㅋ': 10439, '엘지': 10440, '똑바루': 10441, '도도': 10442, '지리멸렬하다': 10443, '세아': 10444, '스포츠영화': 10445, '혼합': 10446, '티브': 10447, '류승범': 10448, '만일': 10449, '시프': 10450, '웨버': 10451, '곰': 10452, '사이버': 10453, '뮬러': 10454, '고명환': 10455, '호프만': 10456, '잡아내다': 10457, '두세': 10458, '지수': 10459, '갈팡질팡': 10460, '아베': 10461, '히로시': 10462, '타무라': 10463, '키도': 10464, '온돌': 10465, '어쩌나': 10466, '불쾌감': 10467, '애둘맘': 10468, '애둘': 10469, '재우다': 10470, '낚으시네': 10471, '오늘밤': 10472, '악몸': 10473, '풀이': 10474, '더기': 10475, '이랬는데': 10476, '미스터빈': 10477, '삼사': 10478, '커피숍': 10479, '의논': 10480, '범학': 10481, '입학': 10482, '훼손': 10483, '웃낌': 10484, '날줄': 10485, '애뜻': 10486, '선수': 10487, '전략': 10488, '줄기': 10489, '국민성': 10490, '충족': 10491, '정신대': 10492, '방구': 10493, '청춘영화': 10494, '브래들리': 10495, '쿠퍼': 10496, '이오': 10497, '걸리버': 10498, '여행기': 10499, '비평': 10500, '승격': 10501, '성악가': 10502, '바탕': 10503, '아리아': 10504, '오달수': 10505, '애매모호하다': 10506, '확실': 10507, '한선': 10508, '먹이': 10509, '폭동': 10510, '울버린': 10511, '랑드': 10512, '토키': 10513, '다카': 10514, '오자룡': 10515, '저하': 10516, '재밋게봣는데': 10517, '평범': 10518, '최강희': 10519, '팅기다': 10520, '마왕': 10521, '겨버령': 10522, '밥상': 10523, '엎음': 10524, '한쪽': 10525, '다이나믹': 10526, '현충일': 10527, '형수': 10528, '관우': 10529, '말씀': 10530, '피부': 10531, '뚫다': 10532, 'ㅋㄱㅋ': 10533, 'ㅜㅜㅠ': 10534, '피우다': 10535, '초늑녁': 10536, '기언': 10537, '못느꼇': 10538, '아노하나': 10539, '슈타게': 10540, '탄피': 10541, '법부': 10542, '엎': 10543, 'ㄱㄱㄱ': 10544, '이현우': 10545, '민호': 10546, '사소하다': 10547, '유주얼서스펙트': 10548, '후배': 10549, '대지': 10550, '버릇': 10551, '모도': 10552, '이롭다': 10553, '류시시': 10554, '시계수리공': 10555, '장효전': 10556, '약혼자': 10557, '뻗다': 10558, '챙': 10559, '붙잡다': 10560, '에잇': 10561, '나무라다': 10562, '분한': 10563, '콩쾌': 10564, '원폭': 10565, '조의': 10566, '꿀': 10567, '실물': 10568, '어유': 10569, '어런': 10570, '참내': 10571, '이진': 10572, '해장국': 10573, '건강하다': 10574, '명필름': 10575, '심재명': 10576, '디스코': 10577, '공찬': 10578, '일색': 10579, '기묘하다': 10580, '대게': 10581, '정해지다': 10582, '마침표': 10583, '낭랑하다': 10584, '리딩': 10585, '레드라이트': 10586, '과찬': 10587, '황제': 10588, '황후': 10589, '불화': 10590, '껄욕': 10591, '유덕': 10592, '더글러스': 10593, '흐트러뜨리': 10594, '윤발': 10595, '자마자': 10596, '여보세요': 10597, '커지다': 10598, '특유의슬': 10599, '상통': 10600, '일치': 10601, '퍼스트': 10602, '달기': 10603, '괴로움': 10604, '랴': 10605, '리슨': 10606, '껄': 10607, '고스트라이더': 10608, '스치다': 10609, '모욕죄': 10610, '더록': 10611, '메타': 10612, '쇼타': 10613, '스시': 10614, '야구모': 10615, '엔티티': 10616, '이수정': 10617, '젓통': 10618, '김혜수': 10619, '어딘': 10620, '붕뜬': 10621, '닫히다': 10622, '박희': 10623, '쇼핑몰': 10624, '이도영': 10625, '상응': 10626, '쒯': 10627, '캔슬': 10628, '거물': 10629, '필추': 10630, '심장마비': 10631, '급사': 10632, '과언': 10633, '사상충': 10634, '코지': 10635, '논픽션': 10636, '총을드': 10637, '포르노그라피': 10638, '이나영': 10639, '임의': 10640, '자각': 10641, '원망하다': 10642, '미군정': 10643, '이승': 10644, '행적': 10645, '규명': 10646, '에로의': 10647, '변모': 10648, '갑작스레': 10649, '한시': 10650, '늦추다': 10651, '가비': 10652, '의향': 10653, '장윤현': 10654, '쓰시': 10655, '번성': 10656, '보조': 10657, '마크': 10658, '진우': 10659, '진혼': 10660, '상술': 10661, '선거': 10662, '세심': 10663, '작업실': 10664, '잠그다': 10665, '도난': 10666, '망청': 10667, '쥐약': 10668, '김혜성': 10669, '이현진': 10670, '카체이싱': 10671, '바둑': 10672, '급수': 10673, '바둑용어': 10674, '자처': 10675, '오른쪽': 10676, '화살표': 10677, '조성': 10678, '내려놓다': 10679, '설국열차': 10680, '가루지기': 10681, '벌레': 10682, '여사': 10683, '낭비하다': 10684, '불현듯이': 10685, '정독': 10686, '천년': 10687, '유혼': 10688, '마니마니': 10689, '잡다하다': 10690, '샛길': 10691, '와아': 10692, '익스트림': 10693, '미요': 10694, '왜세': 10695, '드넒': 10696, '당나라': 10697, '역적': 10698, '김춘추': 10699, '겨짐': 10700, '년반': 10701, '연락': 10702, '덱스터': 10703, '사례': 10704, '나왓으': 10705, '괴뢰': 10706, '왘': 10707, '자고': 10708, '왓음': 10709, '어쨌든': 10710, '에게만': 10711, '헤롱헤롱': 10712, '술처': 10713, '어쩜이리': 10714, '징글': 10715, '딸아이': 10716, '눈시울': 10717, '꿀벌': 10718, '코트': 10719, '반즈': 10720, '생생': 10721, '모나리자': 10722, '어요': 10723, '회볼때': 10724, '후레쉬맨': 10725, '경상도': 10726, '정직하다': 10727, '한숨': 10728, '초이스': 10729, '임밸류': 10730, '껄끄러웠다': 10731, '사가': 10732, '범죄영화': 10733, '허위': 10734, '브라': 10735, '고통스럽다': 10736, '박카스': 10737, '낚지마': 10738, '속수무책': 10739, '김남주': 10740, '표나': 10741, '관상': 10742, '정선경': 10743, '절벽': 10744, '얼꽝': 10745, '어려움': 10746, '테론': 10747, '여겨지다': 10748, '서사': 10749, '서안': 10750, '우쭐': 10751, '주물럭거리다': 10752, '앓다': 10753, '엘리샤': 10754, '커스버트': 10755, '로비': 10756, '컨트롤': 10757, '협회': 10758, '리플': 10759, '헸을것': 10760, '괞찮네': 10761, '제우스': 10762, '박살': 10763, '시나리오작가': 10764, '신파극': 10765, '퍼시픽림': 10766, '어밴져스등': 10767, '근처': 10768, '에라도': 10769, '공임': 10770, '퀸즈': 10771, '김준': 10772, '살육': 10773, '흩어지다': 10774, '밀리': 10775, '식인종': 10776, '어쩌잔거': 10777, '말살': 10778, '해고': 10779, '백만': 10780, '장미': 10781, '엠마뉴엘': 10782, '능동': 10783, '팩트': 10784, '박력': 10785, '스턴': 10786, '상전': 10787, '감우성': 10788, '처분': 10789, '돌팔매': 10790, '나영석': 10791, '학대': 10792, '장애자': 10793, '보이콧': 10794, '이응경': 10795, '길용우': 10796, '감금': 10797, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ': 10798, '충분': 10799, '뉘': 10800, '적요': 10801, '주정뱅이': 10802, '리안': 10803, '소피아': 10804, '흑연': 10805, '합기도': 10806, '갠찮': 10807, '징징거리다': 10808, '머꼬': 10809, '좇': 10810, '상큼': 10811, '무렵': 10812, '띵하다': 10813, '음원': 10814, '햐하핯': 10815, '밓었': 10816, '래서': 10817, '빅팬': 10818, '멀미': 10819, '아이즈': 10820, '강츄': 10821, '한주': 10822, '감정씬': 10823, '또해': 10824, '달리기': 10825, '이민자': 10826, '라스': 10827, '봣어': 10828, '이러다가': 10829, '회태': 10830, '방터': 10831, '게모': 10832, '중국어': 10833, '유승준': 10834, '순박하다': 10835, '등록금': 10836, '거고': 10837, '늘어놓다': 10838, '들르다': 10839, '쮸쮸': 10840, '사서': 10841, '살사': 10842, '히피': 10843, '드럼통': 10844, '비긴': 10845, '어게인': 10846, '견줄': 10847, '마가리타': 10848, '때쌩': 10849, '시들시들하다': 10850, '로세': 10851, '되살리다': 10852, '약물': 10853, '세월호': 10854, '선진': 10855, '하물며': 10856, '우왕': 10857, '현정': 10858, '결재': 10859, '유승호': 10860, '인제': 10861, '한물가다': 10862, '패션쇼': 10863, '다음팟': 10864, '장창': 10865, '저작권': 10866, '카라스': 10867, '트롤': 10868, '파이널판타지': 10869, '요나': 10870, '로무': 10871, '구입': 10872, '사면': 10873, '얏타맨': 10874, '젬': 10875, '양요섭': 10876, '표절논란': 10877}
    단어 <PAD>와 맵핑되는 정수 : 0
    단어 <UNK>와 맵핑되는 정수 : 1
    단어 영화와 맵핑되는 정수 : 2


### 단어 인코딩 (label)


```python
def texts_to_sequences(tokenized_X_data, word_to_index):
  encoded_X_data = []
  for sent in tokenized_X_data:
    index_sequences = []
    for word in sent:
      try:
          index_sequences.append(word_to_index[word])
      except KeyError:
          index_sequences.append(word_to_index['<UNK>'])
    encoded_X_data.append(index_sequences)
  return encoded_X_data
```


```python
encoded_X_train = texts_to_sequences(X_train, word_to_index)
encoded_X_valid = texts_to_sequences(X_valid, word_to_index)
```




    [[39,
      1186,
      843,
      976,
      73,
      2771,
      1718,
      272,
      24,
      573,
      49,
      164,
      3651,
      2,
      1279,
      11,
      4,
      49,
      399,
      514,
      5321,
      20,
      37,
      25,
      1949],
     [62, 3652, 1537, 247],
     [136,
      373,
      2,
      192,
      5322,
      202,
      155,
      75,
      1538,
      1950,
      666,
      2772,
      18,
      479,
      1045,
      25,
      5323,
      4],
     [5324,
      3653,
      3654,
      910,
      5325,
      1280,
      185,
      977,
      2773,
      4,
      91,
      113,
      74,
      797,
      74,
      294,
      1046,
      1187,
      1719,
      5326,
      41,
      2774,
      441,
      1720,
      4,
      186,
      80,
      172,
      1721,
      5327,
      2288,
      15,
      104,
      844,
      1539],
     [56,
      74,
      5,
      1951,
      911,
      3655,
      5328,
      452,
      16,
      54,
      798,
      63,
      3,
      912,
      1407,
      124,
      978,
      54,
      165,
      762,
      62,
      1120,
      16,
      85,
      54,
      425,
      65,
      845,
      156,
      92,
      217,
      137,
      5329,
      3656,
      1540,
      1722,
      4,
      7],
     [46, 480, 20, 1121, 227, 89, 353, 11, 3, 187, 176, 1952],
     [64, 273, 70, 164, 200, 26],
     [132, 114, 280, 5],
     [3657, 552, 846, 1047, 391, 3657, 93, 5330, 100, 2, 315, 261, 91, 72],
     [9, 515, 725, 5331, 5332, 5333, 138],
     [47, 56, 3658],
     [183, 442],
     [354, 2775, 1188, 30, 237, 1281, 126, 76],
     [70, 188, 1408, 5334, 2776, 5335, 1723],
     [847, 50, 284, 498, 122, 21],
     [31, 3, 15, 2, 1724, 2, 3659],
     [257, 81, 115, 3, 481, 27, 233],
     [5336,
      2,
      76,
      70,
      2777,
      1725,
      1541,
      5337,
      848,
      295,
      1542,
      4,
      165,
      380,
      70,
      2777],
     [799,
      532,
      1189,
      3,
      1282,
      532,
      1189,
      344,
      16,
      615,
      1409,
      296,
      124,
      2778,
      1283,
      5338,
      800,
      28,
      80,
      1189,
      2289,
      1284,
      2779,
      316,
      616,
      3660],
     [96, 93, 55, 93, 1953, 1285, 20],
     [75, 763, 179, 592, 18],
     [3, 2780],
     [80, 5339, 3661, 1954, 5340, 1286, 3662, 13, 101],
     [9, 124, 2, 1726, 5341, 317, 27],
     [75, 11, 152, 62],
     [48, 1955, 14, 147, 1190, 5342, 103, 26, 913, 2290, 78],
     [5343,
      27,
      5344,
      1287,
      5345,
      22,
      2,
      726,
      122,
      1956,
      329,
      3,
      17,
      83,
      203,
      6,
      1543,
      381,
      849,
      39,
      667,
      91,
      553,
      593,
      168,
      10,
      420,
      3663,
      2781,
      617,
      1957,
      3664,
      15,
      2782,
      45],
     [96,
      152,
      336,
      63,
      56,
      5,
      132,
      127,
      230,
      12,
      153,
      3,
      9,
      51,
      3,
      2291,
      68,
      212,
      26,
      2292,
      3665,
      9,
      5,
      77,
      979],
     [125, 2, 668, 14, 5346, 22, 1048, 144, 72],
     [285, 111, 257, 257, 5347, 2783, 2293, 105],
     [248, 850, 400, 1191, 5348, 260, 5349, 1191],
     [914, 8, 56, 5, 35, 1958, 426, 63, 39, 85, 5],
     [95, 148, 764, 427, 727, 3666],
     [10, 39, 16, 2, 57, 1049, 148, 5350, 76],
     [208, 980, 46, 208, 3, 3, 482],
     [981,
      6,
      5351,
      3667,
      4,
      3668,
      5352,
      1122,
      2,
      192,
      2784,
      2,
      111,
      2784,
      382,
      1410,
      21,
      35,
      209,
      533,
      18,
      81,
      20,
      694,
      10,
      4,
      40,
      228],
     [17, 10, 8, 2],
     [89, 157, 401],
     [2294, 129, 93, 391, 120, 45],
     [3669, 618, 851, 36],
     [284, 401, 177, 50, 318, 3670, 1288, 14, 2295],
     [73, 4],
     [9, 93],
     [127,
      32,
      89,
      667,
      54,
      265,
      5353,
      204,
      2785,
      7,
      189,
      294,
      138,
      5354,
      284,
      345,
      248,
      11,
      3,
      54,
      2786,
      15,
      3,
      34,
      1544,
      100,
      4,
      274,
      36,
      3671,
      3671,
      4],
     [1289, 1050, 4, 70, 249, 5, 218, 666, 5355, 554, 169, 1545, 1546],
     [3672, 5356, 3673, 193, 3672, 915, 149, 5357],
     [84, 128, 330, 2296, 20, 180, 15, 2],
     [1959,
      3674,
      7,
      274,
      297,
      161,
      3675,
      5358,
      7,
      383,
      801,
      916,
      1290,
      65,
      7,
      53,
      238,
      1411,
      23,
      162,
      42,
      4,
      164,
      28,
      6],
     [1291, 516, 555, 253, 46, 982, 97, 373, 1192, 331, 3, 33, 2, 13],
     [233,
      239,
      221,
      4,
      33,
      4,
      54,
      1193,
      221,
      2787,
      25,
      2,
      443,
      1727,
      30,
      3676,
      52,
      173,
      29,
      852,
      194,
      16,
      6,
      38,
      3677,
      374,
      234,
      534,
      82,
      2],
     [12, 298, 124],
     [332, 29, 360, 392, 83, 299, 227],
     [5359, 1051, 2, 77, 64, 5360, 421, 229, 71, 619],
     [46, 319, 3, 15, 81, 556, 2788, 164, 79, 2297, 2, 225],
     [17, 152, 336, 63, 97, 2, 3678, 5361, 1292, 535, 33, 4, 137, 2, 141],
     [9, 402, 28, 2, 6, 30, 129, 28, 2],
     [5362,
      1052,
      3679,
      2789,
      3680,
      5363,
      24,
      2298,
      917,
      217,
      275,
      44,
      10,
      281,
      620,
      35,
      209,
      346,
      1547,
      1960,
      101,
      422,
      103,
      728,
      2790,
      44,
      557,
      5364,
      31,
      729,
      384,
      237,
      5365,
      728,
      5366,
      133,
      124,
      2,
      153,
      170,
      10,
      8,
      1961,
      6],
     [5367, 16, 56, 5368, 5369, 5370, 5371, 2791, 517, 5372],
     [730, 127, 3, 107],
     [75, 1293],
     [28],
     [5373,
      91,
      155,
      428,
      4,
      918,
      1294,
      594,
      24,
      1728,
      20,
      196,
      3,
      332,
      914,
      919,
      185,
      3681,
      250,
      262,
      4,
      853,
      53,
      184,
      499,
      54,
      1729,
      364,
      37,
      222,
      72,
      1548,
      1123,
      251,
      3,
      105],
     [1295, 158, 1962, 5374, 695, 555, 2, 731, 5375, 121, 574, 5],
     [12],
     [130, 195, 919, 70, 5, 59],
     [1412, 5376, 621, 1963, 558, 240],
     [27, 1964, 453, 27, 3],
     [95, 732, 1194, 44, 645, 128, 73, 4, 1965, 133, 15],
     [726, 146, 2792],
     [54, 575, 981, 920, 7, 285, 128, 75, 11, 4],
     [1549,
      24,
      120,
      51,
      5377,
      403,
      20,
      1550,
      2,
      329,
      3,
      15,
      2,
      300,
      2,
      181,
      2793,
      444,
      42,
      33,
      63,
      2299,
      1966,
      534,
      204,
      404,
      189,
      53,
      98,
      133,
      2],
     [40, 3, 9, 12, 2794, 78, 798, 2795, 111, 78],
     [28, 2, 31, 3, 34, 301, 130, 33, 4, 3682],
     [536, 3, 2, 179, 71, 130, 4, 669, 482, 29, 573],
     [41, 5378, 302, 233, 696, 43, 2, 25, 429, 621, 802],
     [2796, 2797, 400, 3683, 112],
     [1194, 1730, 9, 122, 518, 670, 123, 430, 697, 220, 3684, 193],
     [71, 983, 307, 2],
     [3685, 210, 15, 307, 500, 347],
     [320, 1967, 3, 1731, 5379, 2798, 8, 552, 2799, 595],
     [1195,
      23,
      1968,
      144,
      72,
      241,
      537,
      501,
      17,
      1296,
      559,
      286,
      97,
      108,
      3686,
      5380,
      23,
      1195,
      68,
      2300,
      31,
      3,
      68,
      11,
      13,
      23,
      17,
      147,
      203,
      107,
      18,
      46,
      205,
      345,
      253],
     [576, 74, 74, 62, 2],
     [3,
      3,
      4,
      2800,
      3,
      2,
      1963,
      2301,
      300,
      215,
      29,
      11,
      13,
      3687,
      2,
      22,
      29,
      733,
      431,
      2,
      242,
      5381,
      483],
     [726, 519, 16, 6, 95, 130, 94, 1732, 266, 2801, 2802, 2],
     [851],
     [321, 385, 39, 538, 62, 2],
     [734, 24, 619, 71, 3688],
     [285, 1969, 2803, 68, 13, 82, 481, 27, 98, 698, 2, 287, 1413],
     [2, 10, 5382, 15, 1551, 3689, 5383, 122, 26, 646, 3, 14, 147, 365, 1407, 18],
     [14, 147],
     [984, 18, 184, 287, 92, 484, 765, 465],
     [109, 315, 2804, 4, 1970, 647, 322, 2805],
     [102, 466, 3, 2, 55, 386, 425, 65],
     [5384, 985, 423, 142, 479, 153, 4, 2],
     [596, 3690, 276, 49, 141, 27, 176, 1053, 11, 5385, 5386, 7],
     [539, 5387, 52, 20, 454, 2],
     [69, 374, 2302, 7, 597, 986, 4, 32, 173, 29],
     [3691, 1124],
     [560, 520, 1971, 136, 2, 103, 6],
     [596, 308, 14, 113],
     [3692, 1054, 5388, 1054, 172, 73, 63, 648, 766, 337, 2303, 577],
     [403, 24, 4, 1951, 911, 1297, 99, 25, 65, 598, 3, 2806],
     [28, 36],
     [598, 5389, 57, 767, 647, 31, 22],
     [5390, 1196, 803, 578, 4, 54, 3693, 63, 239, 3694, 2],
     [2807,
      3695,
      1733,
      5391,
      5392,
      5,
      2304,
      405,
      1733,
      854,
      3696,
      263,
      252,
      223,
      1972,
      165,
      987,
      267,
      445,
      5393,
      599,
      5394,
      24,
      1733,
      126,
      4,
      5395,
      4,
      32,
      855,
      1414,
      2305,
      5,
      988,
      5,
      1197,
      11,
      4,
      243,
      856,
      467],
     [83, 299, 230, 35, 420, 406, 17],
     [282, 58, 33, 455, 144, 72, 18],
     [125, 143, 446, 103, 3, 2, 344, 16, 1734, 468],
     [5396, 150, 8],
     [9, 12, 1055, 5397, 5398, 768, 5399, 671],
     [112, 5400, 23, 10, 33, 4, 56, 338],
     [280, 268, 51, 60, 66, 427],
     [163,
      802,
      1192,
      391,
      72,
      407,
      65,
      129,
      3697,
      4,
      1552,
      2,
      408,
      766,
      521,
      102,
      1198,
      1973,
      408,
      2808,
      2808,
      217,
      355,
      323,
      134],
     [537,
      1735,
      920,
      769,
      118,
      920,
      5401,
      72,
      33,
      4,
      1736,
      522,
      42,
      4,
      2,
      1298,
      1736,
      387,
      29,
      622,
      316,
      1553,
      2,
      6,
      3698,
      921,
      5,
      1554,
      3699,
      5402,
      735,
      2306,
      5403,
      277,
      579,
      5404,
      2307,
      6,
      922,
      485,
      72,
      34,
      114,
      5,
      4],
     [54,
      66,
      672,
      523,
      57,
      429,
      89,
      409,
      452,
      1974,
      2809,
      4,
      89,
      989,
      2,
      253,
      1199,
      1299,
      91,
      37,
      25],
     [37, 229, 348, 75, 40, 31, 4, 388, 244, 120],
     [2308,
      51,
      38,
      71,
      519,
      119,
      2,
      80,
      10,
      238,
      3700,
      112,
      502,
      1555,
      3701,
      617,
      242,
      1975,
      42,
      339,
      1056,
      223,
      2810,
      923,
      238,
      3701,
      80,
      71,
      5405,
      13,
      4],
     [3702,
      2309,
      168,
      924,
      804,
      1556,
      60,
      4,
      113,
      50,
      3702,
      2309,
      2310,
      5406,
      3703,
      346,
      5407,
      1737,
      667,
      990,
      539,
      1300,
      736,
      561,
      198,
      3704,
      15,
      21,
      456,
      55,
      54,
      5408,
      166,
      5409,
      16,
      248,
      1301,
      925,
      233,
      102,
      1198,
      21],
     [27, 1415, 12, 430, 171, 185, 1738, 142, 486],
     [1739, 151, 1720, 4, 107],
     [123, 43, 1057, 1056, 145, 65, 5410, 118, 4, 3705],
     [573, 2811, 2812, 41, 1976, 15],
     [805,
      991,
      3706,
      1200,
      673,
      2,
      15,
      29,
      18,
      1557,
      2,
      356,
      518,
      1740,
      40,
      4,
      349,
      16,
      800,
      5411,
      3,
      535,
      12],
     [1416, 59, 86, 302, 275, 41, 159, 5412],
     [30,
      340,
      174,
      375,
      7,
      116,
      55,
      5413,
      118,
      992,
      2,
      3,
      29,
      6,
      215,
      176,
      143,
      148,
      123,
      3,
      4,
      2],
     [43, 2, 114, 1741, 224, 21],
     [993, 175, 14, 7, 318, 28],
     [2, 254, 2],
     [674, 1058, 4, 674, 1742],
     [3, 1059, 258, 5414, 244],
     [387, 2],
     [212, 295, 540, 287, 376, 66, 5415, 535, 1977],
     [59, 410, 97, 27, 4],
     [857, 6, 17],
     [107, 50],
     [192,
      540,
      2,
      112,
      925,
      1558,
      31,
      4,
      17,
      102,
      129,
      2,
      74,
      53,
      198,
      3707,
      138,
      5416],
     [26, 1302, 200, 2813, 1303, 2814, 3708, 288, 737, 57],
     [1060, 281, 5417, 5418, 1061, 266, 2815, 1304, 5419],
     [2, 13, 309, 806, 16, 36, 28, 393, 28, 52],
     [1978,
      3709,
      623,
      295,
      926,
      421,
      133,
      1417,
      85,
      518,
      699,
      524,
      393,
      2,
      5420,
      166,
      29,
      138,
      597,
      251,
      5421,
      1743],
     [127, 38, 76, 598, 3],
     [1979, 324, 15],
     [54, 770, 624, 19, 60, 672, 467, 411, 2816, 847],
     [89, 927, 174, 344, 325, 297, 2, 303, 1062, 4, 3, 432],
     [5422, 2, 17, 122, 2817, 150, 31, 3],
     [74, 18, 5423],
     [1980, 52, 23, 272, 424],
     [5424, 3710, 917, 74, 733, 5425, 3711, 2, 1559, 126],
     [46,
      700,
      858,
      499,
      1981,
      1201,
      802,
      3,
      3712,
      519,
      2818,
      46,
      49,
      3,
      258,
      5426,
      13,
      17],
     [180, 3713, 4],
     [1982,
      1983,
      600,
      282,
      3714,
      4,
      40,
      625,
      469,
      2,
      298,
      2311,
      4,
      53,
      99,
      77,
      64,
      46,
      5427,
      205,
      859,
      5,
      443,
      94,
      41,
      738,
      142,
      11,
      601,
      803,
      285,
      2312,
      16,
      1560,
      2819,
      11,
      22,
      5428,
      274,
      31,
      3],
     [2313, 17, 1984, 6, 78],
     [1202],
     [1189, 739, 85, 5, 928, 1744, 445, 2, 303, 626, 380, 740, 445, 3, 602, 1985],
     [2314],
     [575,
      175,
      5,
      21,
      212,
      97,
      147,
      226,
      6,
      52,
      23,
      10,
      8,
      303,
      1745,
      394,
      1746,
      3715,
      5429,
      57,
      79,
      3],
     [43, 381, 1561, 114],
     [1203, 3716],
     [43, 1204, 2, 38, 1562, 929, 741, 18, 580, 1125, 91, 771, 66],
     [2315,
      27,
      1126,
      44,
      115,
      857,
      6,
      412,
      12,
      701,
      269,
      66,
      1747,
      276,
      1305,
      701,
      377,
      433,
      366,
      4,
      930,
      299,
      6,
      308,
      539,
      2820,
      56,
      929,
      5,
      2,
      3717,
      378,
      1747,
      5430,
      2821,
      4,
      34,
      412,
      2,
      379,
      213,
      339,
      66],
     [32, 44, 163, 62, 3, 95, 3, 78],
     [64, 177, 49, 289],
     [2, 37, 5431, 3718, 252, 412, 130, 94],
     [5432,
      310,
      3,
      233,
      35,
      5,
      672,
      321,
      88,
      12,
      339,
      106,
      116,
      213,
      2,
      194,
      5433,
      2822,
      333,
      1418,
      4,
      5434,
      5435,
      3719,
      1063,
      2823,
      99],
     [56, 7, 68, 860, 7, 78],
     [50,
      59,
      13,
      2316,
      2,
      111,
      3720,
      3721,
      63,
      113,
      5436,
      3720,
      3721,
      110,
      7,
      2316,
      3,
      56,
      7,
      77,
      75,
      5,
      2316,
      114,
      31,
      22,
      5437,
      1986,
      470,
      503,
      1563,
      5438,
      198,
      517,
      114,
      31,
      22,
      117],
     [136, 2, 17, 103, 3],
     [2, 144, 70, 7, 39, 136, 29, 6, 3722, 30, 129, 41, 38, 7],
     [1564, 64, 21, 3, 6],
     [41, 188, 65, 5439, 197, 2, 31, 3],
     [1299,
      2824,
      3723,
      5440,
      702,
      41,
      931,
      1748,
      83,
      310,
      37,
      5441,
      772,
      5442,
      3724,
      468,
      25,
      555,
      111,
      5443,
      7],
     [471, 2317, 4, 932, 161, 46, 4, 3725],
     [10,
      525,
      3,
      525,
      2,
      134,
      5444,
      69,
      134,
      4,
      8,
      29,
      18,
      30,
      1987,
      50,
      525,
      1293,
      258,
      48,
      703,
      5445],
     [1565, 773, 162, 1566, 224, 15],
     [99, 1205, 19, 140, 53, 8],
     [28, 2, 134, 4, 70, 249],
     [5446, 23, 10, 33, 4, 2825, 255],
     [5447, 11, 8],
     [552, 541, 23, 3, 1988, 119, 252, 46, 444, 40, 5, 252],
     [994, 69],
     [2826, 627, 5448, 55, 74],
     [117, 846, 1989, 596, 112, 262, 466, 263],
     [3726, 23, 2318, 265, 52, 166, 1567, 60, 157, 87, 84, 556, 5449],
     [68,
      103,
      22,
      44,
      115,
      3,
      357,
      125,
      1206,
      20,
      995,
      90,
      341,
      11,
      109,
      55,
      109,
      6,
      407,
      119,
      75,
      1749,
      933,
      53,
      129,
      16,
      19,
      102,
      5450],
     [1549, 43, 4, 383, 189, 17, 1306],
     [41, 581, 728, 4, 71, 82],
     [48, 1307],
     [42, 504, 214, 5451, 2319, 194, 3727],
     [3728, 1308, 32, 1308, 855, 996, 5452, 807, 5453, 142, 1990, 934, 861, 2],
     [9,
      40,
      145,
      4,
      15,
      2,
      57,
      623,
      2,
      55,
      174,
      165,
      1991,
      1280,
      185,
      46,
      5454,
      57],
     [122, 34, 1207, 114, 628, 862, 1957, 1568, 118, 921, 16, 1064, 542, 81],
     [5455, 6, 1547, 5456, 74, 31, 2827, 2320, 1750, 5457, 1569],
     [46, 1122, 227],
     [5458, 37, 26, 6],
     [2,
      3,
      1992,
      30,
      3729,
      3,
      30,
      356,
      774,
      330,
      2,
      86,
      23,
      775,
      3730,
      603,
      165,
      1570,
      273,
      21,
      2,
      1751,
      41,
      391,
      1127,
      5459,
      275,
      2,
      594,
      26,
      273,
      33,
      15,
      1419,
      72,
      538,
      2],
     [151, 465, 130, 4, 5, 863, 130, 1571],
     [776],
     [304, 47, 447, 41, 130, 94],
     [582, 3, 1572, 2, 671],
     [847, 108, 3731, 5, 2321],
     [472, 127, 43, 2828, 15, 70, 7],
     [64, 141, 49],
     [395,
      230,
      487,
      413,
      485,
      101,
      742,
      1208,
      96,
      1128,
      114,
      2829,
      305,
      354,
      210,
      17,
      3,
      5],
     [145, 59],
     [5460, 5461, 176, 123, 4, 29, 176, 123, 3, 263, 2],
     [5462,
      542,
      3732,
      3733,
      1420,
      1547,
      3734,
      1993,
      3735,
      864,
      5463,
      380,
      156,
      3736,
      1752,
      5464,
      13,
      2830,
      1209,
      393,
      983,
      5465,
      381,
      5466,
      14,
      67],
     [367, 3, 214, 41, 581, 3737, 4, 935, 7],
     [408, 732, 166, 5467, 447, 2322, 100],
     [471,
      354,
      210,
      3,
      2831,
      311,
      303,
      204,
      797,
      5468,
      58,
      4,
      533,
      41,
      865,
      275,
      45],
     [192, 361, 2, 95, 3, 3738, 2832, 8, 5469, 312, 1046],
     [234, 358, 255],
     [110, 10, 160],
     [1210, 4, 735, 11],
     [1309, 26, 169, 1573],
     [5470, 2323, 2],
     [2, 38, 132, 306, 2833, 3, 80, 104, 2834, 3739, 917, 13, 21, 76],
     [1574, 5471, 3, 8, 2, 594, 26, 1994, 5472, 2324],
     [59, 3740, 97, 488, 862, 1575, 4, 48, 27, 5473],
     [321, 4, 726, 929, 16, 54, 98, 2],
     [2835, 170, 126, 235, 2325, 5474],
     [3741, 2836, 172, 2326, 2327],
     [1753, 276, 158, 174, 505, 7, 866, 41],
     [214, 408, 808, 4, 978, 214, 1129],
     [23, 520, 236, 520, 649, 649],
     [80, 3742, 5475, 15, 5476, 57],
     [181, 414, 10, 238, 154, 2837, 3743, 126, 13],
     [1754,
      38,
      4,
      5,
      3,
      80,
      446,
      5477,
      241,
      80,
      468,
      5,
      99,
      2838,
      313,
      3744,
      5478,
      31,
      65,
      4,
      138,
      189,
      92,
      326,
      409,
      264,
      71,
      1199,
      75,
      11,
      4,
      204,
      154,
      5479,
      31,
      4,
      174,
      8],
     [1310, 133],
     [5480,
      287,
      993,
      33,
      254,
      106,
      309,
      7,
      12,
      212,
      3745,
      41,
      573,
      448,
      1755,
      1756,
      997,
      401,
      675,
      1757],
     [9, 56, 5, 469, 5481, 53, 99, 138, 484, 5482, 2839],
     [5483, 736, 1576, 629, 2840, 2841, 457, 4, 3746, 630, 172],
     [396, 562, 936, 58, 1962, 5484, 3747],
     [403, 36, 347, 2, 2328, 2842, 743, 158, 160, 151],
     [2329,
      55,
      5485,
      2329,
      2843,
      134,
      4,
      3,
      5486,
      2329,
      506,
      344,
      16,
      1995,
      196,
      33,
      4,
      18,
      672,
      1421,
      3748,
      48,
      31,
      275],
     [2844, 12],
     [473, 362, 19, 998, 56],
     [37, 88, 26, 200],
     [260, 28, 539, 1211],
     [50, 5487],
     [190, 33, 3],
     [9, 37, 507, 66, 425, 1212],
     [26,
      14,
      1996,
      1130,
      2845,
      1997,
      345,
      866,
      29,
      375,
      7,
      1045,
      16,
      29,
      1732,
      266,
      65],
     [282, 2, 2846, 9, 28, 937, 11, 5488, 458, 867],
     [311, 26, 29, 249, 94, 1723],
     [132, 136, 2, 486, 128, 330, 21, 349, 777],
     [69, 5489, 470, 4, 5490, 778, 3749, 2847],
     [486, 184],
     [52, 704, 86, 563, 29, 27, 79, 4, 33, 4],
     [39,
      122,
      123,
      3,
      136,
      2,
      113,
      8,
      767,
      1065,
      79,
      5,
      182,
      182,
      18,
      1758,
      63,
      270,
      126,
      33,
      1422,
      508,
      123,
      3],
     [284, 434, 184, 8, 46, 82],
     [102,
      105,
      30,
      2848,
      5491,
      435,
      17,
      238,
      2,
      6,
      105,
      80,
      231,
      2849,
      255,
      3750,
      306,
      374,
      127,
      3],
     [17,
      28,
      2,
      274,
      501,
      1423,
      198,
      37,
      88,
      604,
      767,
      5492,
      198,
      130,
      94,
      176,
      5493,
      3,
      263,
      2,
      779,
      13],
     [85, 5494, 195, 5495, 16, 701, 5496, 500, 32, 226, 5497, 4],
     [1577, 382, 91, 1311, 183],
     [1424, 1578, 1561, 2330, 2850, 2851, 399, 1759, 74, 31, 211],
     [5498, 2852, 154, 113, 5499, 138, 3751, 41, 188, 69, 18],
     [298, 12],
     [125, 143, 650, 68, 152, 5500, 373, 1760],
     [380,
      626,
      2853,
      938,
      2854,
      732,
      1761,
      5501,
      489,
      19,
      1127,
      631,
      380,
      626,
      3752,
      3753,
      1998,
      421,
      5502,
      408,
      2855,
      556,
      741,
      70,
      7,
      430,
      2331,
      174,
      1579,
      4,
      29,
      6],
     [583, 10, 8, 583, 10, 1999],
     [1580, 36, 31, 3, 46, 630, 632, 78],
     [5503,
      780,
      366,
      4,
      21,
      5504,
      172,
      1312,
      143,
      2856,
      488,
      356,
      147,
      5505,
      20,
      1425,
      3754,
      73,
      32,
      367,
      1762,
      676,
      15,
      70,
      5,
      2856,
      1581,
      5506,
      342,
      5507,
      5508,
      4,
      288,
      459,
      4,
      70,
      5,
      809,
      1425,
      2857,
      150,
      6],
     [290, 11, 3, 39, 16, 167, 128, 1313],
     [415, 115, 59, 36, 5509, 2858, 222],
     [183, 6, 127, 38, 76, 5510, 7, 472, 71, 2859, 1213],
     [5511, 6],
     [30, 5512, 14, 301, 14, 18, 14, 67, 76, 146, 6],
     [564, 5513, 129, 1066, 999, 5514, 128, 244, 1582, 129, 58, 262, 2],
     [988, 5, 731, 164, 605, 159, 584, 189, 84, 341, 247, 243],
     [12, 3],
     [28],
     [939, 3755, 5515, 3756, 6, 12, 3, 1314, 404, 2858, 99, 630, 350, 360, 177],
     [1131,
      343,
      108,
      83,
      257,
      343,
      108,
      83,
      131,
      343,
      108,
      83,
      78,
      3757,
      3758,
      633,
      24,
      3689,
      313,
      3759,
      38,
      108,
      83,
      15,
      1315,
      985,
      2860,
      142,
      32,
      1067,
      5516,
      420,
      606,
      60,
      2332,
      60,
      136,
      91,
      73,
      240,
      42,
      4,
      7,
      5517,
      16,
      19,
      108,
      83],
     [430, 810, 5518, 3, 811, 294, 39, 2, 39, 56],
     [930, 518, 235, 115, 1583, 5519, 141],
     [105, 1132],
     [5520, 2333, 619, 651, 317],
     [3, 75, 1749, 127, 3, 68],
     [156, 24, 454],
     [1763, 12, 3],
     [543, 290, 11, 5521, 5522, 229, 1952, 812, 3, 1133, 634, 7, 5523],
     [95,
      61,
      1426,
      2861,
      677,
      470,
      31,
      1422,
      157,
      123,
      3,
      105,
      1214,
      162,
      1764,
      3,
      15,
      1426,
      2861,
      96,
      12,
      3,
      5,
      1000,
      1294,
      1426,
      2861,
      2334,
      3,
      15,
      45],
     [89, 397, 351, 849, 6],
     [62, 3, 2862, 181, 175, 5524, 121, 3760, 13, 30, 1427, 7, 8],
     [104, 104, 555, 6],
     [930, 5525, 150, 5526, 179, 40, 3, 652, 200, 36, 1068, 8],
     [54,
      225,
      2335,
      3761,
      122,
      79,
      3,
      1215,
      10,
      744,
      241,
      5527,
      10,
      1765,
      202,
      915,
      1983,
      15,
      21,
      76,
      517,
      11,
      352,
      8],
     [5528,
      2,
      2000,
      3762,
      2,
      1428,
      111,
      5529,
      455,
      5530,
      15,
      23,
      455,
      252,
      436,
      252,
      3763],
     [781, 350, 1957, 5531, 27, 350, 1134, 350, 2336, 5532, 92, 301, 705],
     [1429, 2863, 5, 2, 201, 1001, 10, 50, 51, 11, 2001],
     [39, 7, 32, 169, 161, 921, 16, 375, 1135, 2, 148, 38, 2337, 4],
     [10, 225, 565],
     [1136, 2, 49, 1002, 89, 397, 6],
     [192, 26, 273, 3, 84, 27, 114, 937, 51, 81, 38, 50, 31, 3, 117],
     [2319, 96, 1746, 45, 1766, 1137, 2, 18, 259, 409, 2],
     [5533, 625, 3764, 219, 2],
     [323, 178, 3, 1316, 345, 437, 1316],
     [5534, 281],
     [17, 5535, 2338, 868, 869, 52, 2864, 188, 868, 3765, 1216, 3766, 13],
     [190,
      56,
      634,
      184,
      287,
      17,
      12,
      3,
      78,
      471,
      286,
      426,
      12,
      21,
      410,
      426,
      63,
      17,
      225,
      3],
     [2, 130, 94],
     [813,
      5536,
      5537,
      635,
      870,
      2002,
      1003,
      302,
      1317,
      460,
      1767,
      2865,
      460,
      5538,
      4,
      5539,
      5540,
      40,
      1317],
     [5541, 16, 701, 11, 1217, 5542],
     [393,
      1430,
      3767,
      17,
      5543,
      231,
      34,
      250,
      231,
      940,
      2866,
      5544,
      618,
      17,
      522,
      461,
      206,
      5545,
      36,
      490,
      5546,
      435,
      2339,
      28,
      206,
      706,
      3768,
      1318,
      32,
      201,
      30,
      41,
      399,
      1319,
      5547,
      20,
      126,
      185,
      3769,
      471,
      17,
      315],
     [537, 142, 42, 94, 104, 60, 2849, 4, 5548, 5549, 31, 2867],
     [607, 436],
     [54, 82, 114, 425, 65, 21],
     [616, 59],
     [1768, 284, 2868, 4, 5550, 741, 270, 231, 155, 375, 7],
     [616, 230, 1069],
     [43, 2, 585, 74],
     [376, 158, 20, 88, 249, 209, 94, 5551],
     [1218, 114, 132, 481, 211, 225, 3],
     [2, 165, 2869, 6, 5552, 1219, 2340, 23, 1769, 28, 6],
     [636,
      35,
      160,
      35,
      449,
      745,
      190,
      86,
      1431,
      618,
      731,
      6,
      618,
      2339,
      2870,
      707,
      3770,
      5553,
      2341,
      1767,
      3,
      267,
      1220],
     [321,
      3771,
      2,
      86,
      233,
      1770,
      1135,
      1771,
      2342,
      76,
      81,
      20,
      871,
      601,
      262,
      912,
      5554,
      23,
      61],
     [13, 872, 941, 653],
     [12, 26, 10, 222, 182],
     [444, 40, 164, 2299, 3, 4],
     [5555, 13, 1320, 5556, 942, 404, 8],
     [3, 1321, 2, 181, 873, 861, 2343, 1432, 88, 61, 3772, 275, 678, 7],
     [3773, 9, 163, 44, 216, 96, 3774, 2003, 1559],
     [307, 3775, 782, 2, 38, 3776, 58],
     [26, 37, 49, 249, 31, 245],
     [209, 160, 51, 47, 373, 2],
     [156, 1433, 429, 5557, 24, 2344, 7, 649, 649],
     [37, 8, 52, 377, 88, 25, 2345],
     [64, 177, 415, 63, 1584, 22, 5558, 2004, 3, 2871],
     [282, 66, 2346, 1772, 24, 8, 26, 10, 526],
     [163,
      44,
      3777,
      544,
      338,
      2,
      746,
      16,
      1070,
      35,
      2005,
      32,
      150,
      208,
      61,
      33,
      133,
      1958,
      4,
      330,
      407,
      65,
      2,
      1070,
      208,
      133,
      81,
      575,
      3778,
      15,
      3777,
      377,
      3,
      2,
      652,
      586,
      200,
      537,
      170],
     [190, 28],
     [5559, 210, 3, 51, 467, 157, 3, 185, 126],
     [28, 36, 91, 1071, 3, 632, 554, 334, 4, 283, 4, 15, 36, 220, 4],
     [1138, 87, 47, 1307, 37, 3, 51, 47, 87, 47, 700, 50],
     [4, 5],
     [12, 59, 21],
     [174,
      2347,
      5560,
      5561,
      3779,
      174,
      998,
      4,
      262,
      2,
      5562,
      19,
      1773,
      2348,
      5563,
      435,
      138,
      814,
      2872,
      1774,
      3780,
      5564,
      943,
      58,
      262,
      4,
      89,
      44,
      17,
      3780,
      3781,
      5565,
      416,
      6],
     [43, 5566, 2, 389, 24, 767, 4, 94],
     [84, 62, 23, 608, 20, 4, 848, 52, 587, 3, 107],
     [2873, 3782, 131, 61, 3],
     [2874, 554, 2349, 15, 155, 1434, 217],
     [5567, 344, 16, 19, 3, 34, 1435, 135, 5568, 115, 181, 44, 61, 344, 5569],
     [1775,
      2875,
      220,
      2,
      3783,
      747,
      491,
      363,
      2810,
      340,
      597,
      20,
      4,
      7,
      18,
      597,
      159,
      340,
      483],
     [62, 193, 582, 79, 3, 327],
     [145, 574, 1124, 3784],
     [654, 452, 338, 414, 422, 69, 354, 210, 14, 147, 114, 5, 874, 199, 979],
     [162, 207, 38, 1764, 3, 12, 376, 36, 2876, 181, 3],
     [264, 35, 93, 151, 53, 93],
     [48, 5570, 92, 5571, 5572, 253, 2877, 139],
     [2878, 340, 169, 637, 51, 223, 554, 1001, 130, 33, 4, 852, 110],
     [90, 38, 76, 2, 28],
     [3785,
      5573,
      5574,
      4,
      2879,
      1585,
      1767,
      1436,
      5575,
      811,
      49,
      250,
      5576,
      1221,
      3698,
      3786,
      104,
      24,
      2,
      2006,
      4,
      126],
     [1586, 1586, 288],
     [9, 5577, 566],
     [748, 1568, 2, 232],
     [655, 100, 38, 76, 492, 100, 44, 5],
     [396, 115, 5578, 11, 45],
     [30,
      696,
      1222,
      55,
      386,
      93,
      6,
      2007,
      5579,
      33,
      63,
      508,
      2880,
      4,
      1072,
      3787,
      1073,
      33,
      63,
      708,
      110,
      11,
      400,
      226,
      63,
      43,
      944,
      2881,
      508,
      37,
      910,
      462,
      445,
      30,
      26,
      197],
     [312, 1223, 351, 941],
     [2350, 2882, 865, 269, 72, 5580, 1776, 811, 368, 3788, 390, 707, 94],
     [84, 160, 59],
     [93, 39, 5, 1322, 875, 117, 42, 1587, 245, 2],
     [37, 2351, 2351, 144, 72],
     [199, 2352, 2008, 1588, 55, 74, 605, 44, 17, 225, 3789, 107],
     [9, 783, 582, 2, 57, 2353, 606, 33, 25],
     [28, 2, 2, 3790, 940, 231, 197, 588],
     [2883, 25, 1048, 144, 72, 136, 2, 14, 764, 121, 874],
     [2354],
     [1224, 329, 129, 2, 109],
     [291, 35, 395, 74, 74, 10, 152, 1074],
     [204, 92, 378, 131, 61, 3],
     [5581, 618, 414, 1777, 360, 134, 5582, 4, 247],
     [2355, 135, 312, 224, 474, 88, 35, 5583, 2, 122, 21],
     [5584,
      2772,
      2356,
      2357,
      5585,
      134,
      4,
      2357,
      876,
      2358,
      5586,
      224,
      5587,
      1589,
      188,
      5588,
      22,
      262,
      1778,
      57],
     [81, 118, 2009, 402, 433, 82, 877],
     [1075, 55, 1075],
     [514, 37, 229, 4, 252, 66],
     [292, 271],
     [106, 674, 42, 369],
     [9,
      251,
      3,
      10,
      203,
      187,
      4,
      9,
      160,
      59,
      35,
      566,
      1590,
      376,
      983,
      330,
      649,
      212,
      777,
      1300,
      9,
      480,
      20,
      410,
      179,
      89,
      927,
      50,
      2,
      6,
      187,
      12,
      9,
      2884,
      166,
      29,
      133,
      140],
     [99, 148, 446, 1225, 79, 621, 3, 134, 40, 4, 2, 749],
     [125, 2885, 2, 638, 8],
     [30, 3, 155, 5589, 2, 3, 218, 16, 6],
     [30, 129, 28, 2],
     [5590],
     [163, 44, 3, 180, 800, 2359, 5591, 1125, 29, 733, 191, 39],
     [323, 467, 3, 263, 2, 163, 44, 6, 812, 1437, 56, 33, 133],
     [77,
      1779,
      397,
      5592,
      248,
      2886,
      2010,
      6,
      95,
      527,
      1323,
      2887,
      5593,
      1323,
      342,
      24,
      1226,
      609,
      4,
      49,
      532,
      557,
      82,
      127,
      4,
      567,
      173,
      91,
      5594,
      17,
      574,
      5595],
     [284, 2011, 19, 3, 460, 3, 267, 154, 119, 119, 4],
     [5596, 313, 5597, 568, 1076, 23, 291, 35, 1999, 126, 175, 68],
     [474, 1077, 269, 66, 13],
     [1438, 1003, 404, 12],
     [5598, 5599, 23, 9, 233, 9, 34, 146, 261, 656, 107],
     [1439,
      2360,
      533,
      44,
      2360,
      1591,
      21,
      517,
      741,
      945,
      67,
      2012,
      437,
      1591,
      21,
      3791,
      34,
      48],
     [12, 26, 2361, 247],
     [1592, 5600, 73, 63, 2888, 671],
     [3792,
      17,
      243,
      64,
      205,
      653,
      1780,
      18,
      1956,
      946,
      243,
      498,
      1440,
      15,
      453,
      3793,
      5601,
      180,
      1139,
      217,
      4,
      1197,
      491,
      4,
      5602,
      22],
     [947, 521, 110, 624, 19],
     [509, 2889, 5603, 2889, 2889, 1140, 1047],
     [438,
      161,
      12,
      257,
      115,
      1593,
      277,
      5604,
      20,
      3794,
      492,
      61,
      2890,
      3,
      4,
      131,
      61,
      3,
      926,
      421,
      1004,
      5,
      938,
      874,
      318,
      5605,
      250,
      815,
      37,
      1225,
      249,
      33,
      25],
     [27, 927, 5606],
     [1227, 816, 3795, 95, 121, 2000, 327],
     [607, 5607, 1949],
     [10,
      218,
      16,
      402,
      21,
      5608,
      1781,
      1005,
      2891,
      357,
      1006,
      1441,
      992,
      2892,
      228],
     [97, 22, 493, 31, 3662, 110, 98, 627, 9, 51, 60, 66, 3, 106, 1594, 1782],
     [5609, 141, 124, 322, 927, 3796, 7],
     [3797, 5610, 2321, 2, 1965, 639],
     [2877, 59, 50],
     [1228, 1201, 44, 1007, 5611, 20, 1783, 4, 49, 181, 358, 105],
     [141, 17, 982, 97],
     [214,
      5612,
      30,
      696,
      647,
      5613,
      1229,
      22,
      39,
      7,
      2893,
      5614,
      1442,
      2362,
      2013,
      80,
      468,
      39],
     [56, 5, 50, 96, 93, 6, 198, 331, 1324, 384, 3, 143, 27, 62],
     [847, 33, 3, 2],
     [208, 481, 27, 376],
     [5615, 13, 189, 948, 63, 76, 45],
     [707,
      4,
      3,
      3798,
      2363,
      5616,
      1325,
      121,
      3799,
      5617,
      37,
      3800,
      13,
      21,
      330,
      214,
      1008,
      346,
      577],
     [96,
      283,
      4,
      3,
      1429,
      609,
      98,
      108,
      324,
      31,
      4,
      1429,
      5618,
      116,
      186,
      167,
      35,
      12,
      2014,
      23,
      79,
      4],
     [674, 188, 77, 18],
     [500, 347, 1784, 586, 311],
     [363, 109, 615],
     [85, 5, 56, 7, 357, 94, 2],
     [84,
      437,
      23,
      863,
      1141,
      92,
      437,
      1225,
      23,
      4,
      486,
      303,
      189,
      92,
      23,
      2015,
      125,
      81,
      15],
     [107, 1785, 5619, 2016, 5620, 4, 5621, 126, 1142],
     [9, 124, 2017, 15, 2],
     [424, 332, 39, 123, 3],
     [2018, 2894, 640, 1420, 5622, 378, 14],
     [868, 44, 1786, 5623, 117],
     [2895,
      71,
      3,
      1326,
      24,
      429,
      61,
      100,
      68,
      111,
      617,
      389,
      24,
      2,
      2790,
      406,
      817,
      108,
      304,
      1225,
      200,
      95,
      3801,
      26,
      88,
      222,
      14,
      33,
      273,
      522,
      423,
      2019,
      16,
      167,
      1595,
      3802,
      878,
      1327,
      399,
      108,
      14,
      304,
      420,
      133],
     [879, 28, 354, 750, 15, 29, 6],
     [229,
      348,
      383,
      2896,
      159,
      2020,
      100,
      391,
      180,
      2,
      3,
      256,
      119,
      2,
      18,
      4,
      3,
      180,
      461,
      817,
      37,
      7,
      66],
     [96, 2021, 1443, 102, 28, 227, 1328, 22, 5624, 1329, 317, 2022, 183],
     [1124, 14, 107, 227],
     [290, 11, 9, 40, 4, 4, 2],
     [776, 1787, 776, 1787, 776],
     [408,
      766,
      272,
      2364,
      1143,
      1078,
      2897,
      18,
      40,
      4,
      3,
      1226,
      927,
      8,
      2023,
      8,
      323,
      1078,
      8,
      34,
      2898,
      563,
      1226,
      927,
      93,
      34,
      2899,
      66,
      40,
      42,
      610,
      947,
      2024,
      126,
      588,
      29,
      462,
      656,
      2900,
      185],
     [125,
      3803,
      125,
      103,
      3,
      812,
      3,
      44,
      519,
      1310,
      300,
      534,
      37,
      34,
      2365,
      1317,
      28,
      2,
      167,
      2901,
      109,
      333,
      4,
      38,
      873,
      130,
      245,
      564,
      207,
      81,
      3,
      13,
      948,
      63,
      732,
      170,
      127,
      148,
      53,
      3],
     [14, 1330, 263],
     [1788],
     [1789, 63, 57, 769, 3804, 11, 3, 263, 2, 914, 1444, 5],
     [999, 2902, 18, 46, 219, 814, 15, 5625, 13, 1734, 468],
     [32, 382, 147, 32, 545, 870, 429, 1445, 358, 1411],
     [5626, 3805, 13, 2],
     [12,
      5627,
      171,
      475,
      3806,
      195,
      36,
      131,
      61,
      33,
      3,
      1790,
      131,
      61,
      5628,
      317,
      57],
     [29, 1304, 5629, 80, 3807, 198, 775, 33, 3, 1140, 195, 28],
     [64, 74, 420, 5, 995, 24, 3, 12],
     [90, 3, 1596, 21, 494, 2],
     [1414, 1791, 2366, 1187, 15, 2021, 105],
     [583, 386, 425, 65, 62, 2903],
     [26, 2367, 200, 604, 2025, 4, 14, 1079, 2],
     [393, 52, 28, 2, 5630, 508, 1144, 341, 247, 45, 2904, 314, 107],
     [5631,
      949,
      5632,
      117,
      172,
      16,
      118,
      1069,
      425,
      1446,
      14,
      67,
      241,
      17,
      5633,
      2026,
      5634,
      286,
      97,
      1281,
      52,
      1230,
      510,
      308,
      69,
      2,
      216,
      117,
      17,
      2,
      3,
      5635,
      59,
      2780,
      117],
     [3808,
      171,
      22,
      53,
      950,
      3,
      53,
      225,
      217,
      193,
      5636,
      171,
      1762,
      5637,
      2368,
      1447,
      71,
      3809,
      4,
      1213,
      184,
      641],
     [2905, 3, 258, 422, 2369],
     [5638, 880, 352, 3, 5, 32, 343, 11, 3, 3810, 228],
     [30, 129, 24, 28, 2, 134, 5639, 2, 439, 2],
     [49, 506, 187, 2, 9, 2906],
     [83, 62, 303, 1984, 187],
     [5640,
      589,
      16,
      115,
      7,
      2907,
      5641,
      5642,
      1331,
      931,
      103,
      3,
      34,
      927,
      739,
      66,
      475,
      927,
      481,
      1009,
      11,
      228],
     [1126,
      2370,
      5643,
      503,
      2370,
      1298,
      29,
      8,
      29,
      274,
      2371,
      949,
      399,
      881,
      5644,
      3811,
      588,
      951],
     [393, 23, 86, 173, 118, 24, 8],
     [106, 1792, 5645, 5646, 113, 1288, 114, 56, 5, 14],
     [199,
      46,
      391,
      5647,
      40,
      4,
      320,
      27,
      465,
      853,
      569,
      6,
      199,
      389,
      642,
      20,
      2908,
      4],
     [158, 12, 309, 113, 5648, 2027, 799, 35, 3812, 168, 175, 195, 143, 12, 3],
     [212,
      3745,
      68,
      240,
      71,
      251,
      71,
      739,
      3813,
      1332,
      11,
      98,
      235,
      232,
      1061,
      232,
      2804,
      1571,
      2028,
      156,
      22,
      124],
     [5649,
      2372,
      8,
      5650,
      7,
      3814,
      4,
      82,
      1447,
      197,
      1992,
      184,
      533,
      32,
      561,
      5651,
      2373,
      5652,
      15,
      3815,
      142,
      60,
      15,
      1078,
      5653,
      1597,
      15,
      84,
      290,
      11,
      2374,
      633,
      5654,
      679,
      3,
      2909,
      1992,
      380],
     [108, 2910, 39, 5, 3816, 493, 378, 40, 186, 45],
     [594, 108, 14, 481, 2911, 200, 14, 818, 31, 3, 8],
     [1448, 84, 2375, 128, 73, 329, 3817],
     [5655, 5656, 2353, 606, 2, 178, 79, 495],
     [202, 3, 370, 82, 438, 6, 484, 320, 18, 2029, 2, 670, 206, 1793, 338],
     [8],
     [39, 39, 255, 9, 28, 57],
     [99, 5657, 3],
     [2912, 2030, 139, 23, 84, 184, 8],
     [27, 568, 1720, 4, 5, 998, 4, 1145, 15, 2913, 751, 3818, 44, 174, 344, 16, 6],
     [540,
      68,
      276,
      29,
      441,
      457,
      186,
      5658,
      2376,
      158,
      2,
      55,
      1794,
      28,
      134,
      3,
      1146,
      2031,
      2032,
      3819,
      2377,
      1598,
      4,
      56,
      61,
      695,
      1333,
      1080,
      1795,
      53,
      8,
      677,
      1599,
      1600,
      20,
      2033,
      106],
     [1228, 44, 115, 30, 5659, 28, 36],
     [3820, 2914, 5660, 137, 1081, 177, 45],
     [5661, 934, 169, 5662, 339, 2378, 214, 2899, 66],
     [2379, 765, 342, 709, 2915, 234, 216],
     [703, 286, 52, 152, 336, 4, 137, 1147, 2916, 443, 5663, 56, 5],
     [60, 59, 7, 5664, 199, 2, 25],
     [3821, 1761, 1796, 1761, 127, 242, 1761, 1796, 301, 16, 705, 1601, 429, 5],
     [99, 3759],
     [26, 120, 426, 1602, 353, 425, 1446, 14, 1449, 46, 1574, 1450, 698, 2],
     [5665, 740, 13, 2917, 366, 34, 221, 4, 29, 13, 1574, 1450, 2918, 611, 378, 2],
     [9, 90, 38, 76, 2, 2380, 30, 342, 1299, 3822, 1603, 72],
     [26, 169, 2, 631, 40, 4, 25, 2],
     [1334, 73, 128, 4, 21, 416, 362, 3823, 2919, 2920, 16, 6],
     [522, 1451, 149, 2381, 553, 154, 1552, 1082, 2382, 11, 39, 538, 36, 5666],
     [290,
      11,
      3,
      305,
      2,
      1292,
      53,
      12,
      80,
      5667,
      3824,
      5668,
      4,
      44,
      2034,
      5669,
      5670,
      584,
      104,
      9,
      2921,
      1604,
      6],
     [9, 730, 3, 68, 6, 37, 274, 501, 3],
     [511, 123, 3],
     [32, 201, 1605, 162, 3825, 581, 5671, 391, 2383, 53, 128],
     [459, 27, 398, 161, 358, 732, 40, 4],
     [46, 3, 22, 857, 1128, 299],
     [29, 47, 153, 476, 982, 97],
     [77, 424, 260, 28],
     [439, 2030, 362, 1606, 2384],
     [5672,
      5673,
      5674,
      3826,
      5675,
      2,
      2801,
      19,
      5676,
      4,
      2029,
      2922,
      441,
      5677,
      177],
     [2923, 158, 1305, 23, 283, 94, 160, 35, 86, 114, 190, 14, 118, 15],
     [307, 475, 422, 77, 64, 18],
     [3827, 5, 1231, 1438, 2908],
     [431, 12, 59, 66, 3],
     [103, 131, 1584, 12, 6, 512, 868, 226, 117],
     [882, 69, 304, 47],
     [942, 3828, 5678, 22, 3761],
     [510, 161, 1452, 569, 4, 70, 7, 82, 2, 17, 2, 1280, 70, 7, 2],
     [1010, 1797, 447, 9, 139],
     [305, 384, 2385, 5679, 15, 752, 123, 483, 2],
     [5680,
      5681,
      293,
      460,
      1011,
      2924,
      20,
      729,
      5682,
      83,
      1148,
      8,
      158,
      111,
      96,
      1149],
     [2925, 308, 2, 22, 42, 402],
     [5683, 32, 5684, 5685, 23, 85, 1050, 179],
     [883, 44, 3, 1335, 187, 2],
     [616, 9, 145, 251, 2, 181, 97, 477, 169, 120, 5686, 390],
     [258, 1336, 36, 846, 5687, 310, 25],
     [132, 8, 124],
     [1306, 3, 2926, 2035, 7, 237, 2],
     [734, 36, 3829, 5688, 173, 1798, 36, 1798, 570, 36, 25, 1083],
     [3830, 27, 67, 25, 517, 733, 457, 514, 87, 492, 3831, 392],
     [3,
      2036,
      55,
      90,
      148,
      3,
      1607,
      4,
      25,
      3,
      30,
      1150,
      952,
      4,
      1151,
      109,
      1799,
      1012,
      19,
      784,
      371,
      3],
     [5689, 1142, 5690, 1142, 5691, 107, 241, 12],
     [39, 884, 255, 3832, 28, 1586, 2927, 5692],
     [2386, 2928, 1231],
     [3833, 5693, 407, 65, 139],
     [657, 54, 243],
     [136, 69, 2, 342, 2037, 65],
     [1800, 5694, 2929, 61, 4, 2930, 2931],
     [214,
      626,
      5695,
      2038,
      4,
      44,
      123,
      196,
      76,
      36,
      884,
      5696,
      1801,
      4,
      680,
      10,
      39,
      16,
      6,
      546,
      127,
      43,
      1232,
      22,
      3834,
      57,
      2387,
      658,
      43,
      36,
      22,
      753,
      198,
      2039,
      13,
      10,
      175,
      255],
     [108, 1084],
     [113, 620, 2, 105, 38, 286, 317, 3, 113, 326, 105],
     [64, 58, 25, 617, 911, 2932, 496, 1085, 627, 3835, 10, 5697],
     [52,
      23,
      14,
      86,
      14,
      35,
      299,
      54,
      328,
      3836,
      94,
      13,
      44,
      92,
      77,
      218,
      18,
      480,
      4,
      5698,
      5699,
      1323,
      101,
      3,
      17,
      1608,
      1608,
      54,
      1609,
      31,
      224,
      64,
      1781,
      77,
      218,
      18,
      1323],
     [1802, 250, 23, 149, 92, 487, 23, 461, 92, 819, 5700, 190, 160],
     [710, 753, 31, 22, 18],
     [209, 885, 86, 346, 847, 2933, 71, 487, 2934, 468, 919, 70, 5],
     [48,
      953,
      657,
      681,
      33,
      3,
      289,
      289,
      3,
      820,
      590,
      37,
      498,
      657,
      185,
      657,
      185,
      81,
      1803,
      402,
      3,
      256,
      22,
      657,
      681],
     [360, 98, 3837, 112, 2332, 3837, 112],
     [362, 3838, 121, 543, 489, 19, 4, 14, 560, 67, 37, 278, 442],
     [953, 50, 292, 341, 1086, 57, 5701, 333, 1337, 2, 7, 2388, 3, 3],
     [659, 5702, 5703, 547, 1581, 53, 12],
     [2040, 2389, 1135, 109],
     [64, 2390, 168, 3839, 210, 141, 2, 3840, 821, 3, 5704, 5705, 134, 3841, 4],
     [315, 6, 117, 297, 785, 2, 668, 251, 203, 6],
     [1610, 783, 920, 5],
     [5706, 300, 612, 33, 4],
     [46, 4, 5, 682, 1065, 2, 2935, 424, 4, 28, 1974, 2936, 78],
     [1338, 1338, 817, 2, 3, 237, 69],
     [125, 421, 754, 5707, 13, 101],
     [294, 711, 116, 2391, 2041, 325, 2, 954, 56, 162, 7],
     [519, 16, 167, 238, 2],
     [955, 24, 1152, 3, 9, 62],
     [460,
      1611,
      21,
      5708,
      1804,
      683,
      367,
      232,
      379,
      3842,
      4,
      21,
      5709,
      755,
      237,
      19,
      1279,
      2392],
     [2937,
      866,
      29,
      1409,
      296,
      124,
      5710,
      65,
      21,
      365,
      435,
      287,
      59,
      21,
      75,
      763,
      886,
      991,
      338,
      1562,
      1612,
      166,
      29,
      175,
      14],
     [10, 656, 68],
     [1147, 569, 376, 21, 5711, 5712, 373, 548],
     [1013,
      37,
      4,
      252,
      66,
      1013,
      22,
      74,
      31,
      22,
      1013,
      3843,
      5713,
      4,
      1540,
      22,
      5714,
      4,
      181,
      1013,
      137,
      2041,
      232,
      66,
      252,
      2042,
      2043,
      20,
      3,
      252,
      5715,
      71,
      1453,
      469,
      753,
      1440,
      15,
      3844,
      4],
     [304, 47, 2, 134, 42, 4, 1051],
     [29, 17, 12, 3],
     [23, 79, 4, 519, 184, 486, 1584, 46, 22],
     [5716, 149, 1153],
     [3845, 50],
     [36,
      215,
      154,
      119,
      119,
      3846,
      2,
      6,
      17,
      424,
      615,
      2938,
      346,
      660,
      10,
      615,
      40,
      4,
      94,
      282,
      1977,
      2,
      6],
     [30, 3, 2, 55, 174, 851, 651, 430, 49, 3, 60, 1316],
     [50],
     [5717, 235, 1409, 1133, 335, 6, 84, 50],
     [332, 17, 9, 1805, 106, 2939, 1154, 41, 188, 1058, 4, 96],
     [5718, 3847, 121, 331, 804, 2],
     [1147, 2393, 196, 296, 39, 16, 2],
     [412, 3848, 433, 38, 1806, 786, 5719],
     [81,
      118,
      14,
      100,
      15,
      52,
      23,
      58,
      3849,
      86,
      64,
      74,
      246,
      5,
      311,
      55,
      311,
      995,
      534,
      44,
      421,
      3850,
      2940,
      4],
     [31, 245, 245, 200, 10, 200],
     [259, 409, 37, 498, 231, 99],
     [844, 19, 109, 6],
     [26,
      10,
      200,
      239,
      62,
      21,
      1302,
      42,
      11,
      98,
      43,
      373,
      2,
      1014,
      3851,
      956,
      1014,
      54,
      201,
      239,
      5,
      684,
      541,
      114,
      194,
      5,
      2941,
      143,
      5720,
      5721,
      268,
      2942,
      38,
      2,
      3,
      32,
      1067,
      867],
     [393, 201, 42, 94, 95, 5722, 374, 2937, 33, 4],
     [570,
      308,
      69,
      2,
      3,
      445,
      254,
      13,
      35,
      328,
      34,
      2044,
      957,
      1454,
      66,
      34,
      2045,
      4,
      436,
      25,
      13,
      570,
      3852,
      442,
      2046,
      2943,
      20,
      87,
      2944,
      213,
      2394,
      77,
      2945,
      47,
      49,
      75,
      2945,
      20,
      46,
      2946,
      5723,
      2047,
      53,
      1208],
     [1613, 756, 592, 42, 4, 5724],
     [5725, 20, 3853, 2038, 822, 78],
     [5726, 2048, 23, 39, 182, 182],
     [5727, 4, 39, 105],
     [2395, 5728, 20, 73, 228],
     [69, 13, 2, 41, 261, 773, 1425, 887, 3854, 2947, 4, 3855],
     [5729, 33, 350, 630, 426, 47, 595],
     [9, 12, 36],
     [17, 83, 50, 204, 281, 1807, 3, 241, 853, 131, 17, 131, 107, 30, 1427, 114],
     [1614, 174, 378, 216, 2],
     [2, 5730, 452, 69, 288, 1155, 1339, 223, 3856, 5, 150],
     [81, 118, 30, 696, 1147, 55, 3857, 26, 694, 265, 45],
     [2948, 2949, 18, 2950, 3858, 1156, 1615, 823, 1061, 156, 1157, 296, 432],
     [18, 2, 37, 454, 130, 31, 60, 207, 764, 121, 3, 109, 111],
     [45, 78, 494],
     [292, 2039, 3, 5731, 308, 2, 3859, 35, 980],
     [1616,
      30,
      31,
      3,
      577,
      66,
      46,
      2359,
      1340,
      10,
      12,
      1455,
      804,
      668,
      96,
      888,
      107,
      303,
      2396,
      171,
      23,
      3860,
      57],
     [3],
     [28, 5732, 3861, 1742],
     [39, 16, 482],
     [58,
      15,
      2,
      372,
      26,
      10,
      222,
      817,
      821,
      29,
      5733,
      3762,
      371,
      5734,
      5735,
      5736,
      47,
      2951,
      5737,
      194,
      14],
     [3862, 5738, 2377, 41, 68, 261, 3863, 4, 186],
     [22, 510, 17, 707, 94],
     [459, 27, 148, 446, 60, 3, 40],
     [17, 163, 44, 73, 66, 5739, 179, 462, 128, 238],
     [958, 31, 22, 2397, 2952, 3864, 4, 31, 3, 454, 192, 2398, 1015, 47, 176],
     [583, 463],
     [9, 541, 359],
     [136, 2, 7, 5740, 569],
     [75, 11, 1456],
     [332, 1128, 299, 41, 1808, 2953, 75, 3865, 133, 2],
     [39, 7, 146, 1082, 2, 111, 26, 37, 43],
     [172, 16, 19, 26, 10, 222, 77, 18],
     [110, 201, 787, 1233, 33, 4],
     [284, 10, 122],
     [417, 707, 4, 3, 2, 62, 58, 3, 78],
     [2, 123, 3, 5741, 5742, 2805, 17, 13, 23, 1617, 39],
     [62, 148, 3, 2954, 303, 62],
     [17, 867, 3, 2, 458, 388, 244],
     [9, 12, 106, 235, 2393],
     [1016, 174, 122, 1016, 96, 73, 4, 1153, 8],
     [412,
      64,
      12,
      252,
      66,
      137,
      2955,
      260,
      816,
      1977,
      4,
      598,
      310,
      263,
      66,
      54,
      269,
      1618,
      5,
      1341,
      2399,
      127,
      269,
      37,
      88,
      26,
      200,
      66],
     [12, 1304, 191, 3866, 106, 139, 241, 576, 581, 98, 3867, 80, 208, 78],
     [403, 20, 3, 2400, 11, 22, 450, 6, 26, 200],
     [661,
      642,
      242,
      2049,
      2401,
      60,
      2956,
      1234,
      504,
      428,
      100,
      1619,
      245,
      675,
      635,
      3868,
      4,
      3869,
      377,
      18,
      37,
      364,
      2957,
      31,
      4,
      252,
      288,
      699,
      72,
      698,
      3870,
      1809,
      506,
      364,
      934,
      418,
      1620,
      5743],
     [50, 144, 72, 62],
     [248, 89, 49, 5744, 1052, 864, 5745, 4, 247, 45],
     [1006,
      824,
      1087,
      9,
      2402,
      176,
      53,
      11,
      513,
      544,
      20,
      521,
      230,
      5746,
      4,
      230,
      1810,
      1621,
      1017,
      209,
      4,
      370,
      101,
      788],
     [26, 1073, 483, 166, 40, 65],
     [30, 712, 88, 50, 2, 103, 6],
     [593, 168, 825],
     [5747, 11, 5748, 944, 5749],
     [2050, 2958, 1590, 3871, 4, 4, 601, 1811, 1217, 10, 2959, 2],
     [3808, 3872, 702, 661, 293, 5750, 19, 14, 464],
     [2, 18, 1457],
     [777, 1737, 41, 373, 69, 2],
     [400, 2051, 83, 851, 1018, 1088, 2],
     [46, 713, 146, 19, 3, 7],
     [30, 712, 88, 445, 2, 438, 6, 117, 48, 243],
     [3873, 170, 126, 31, 436, 15, 34, 862, 436, 288, 367],
     [280, 5, 113],
     [9, 58, 25, 68, 6],
     [2403, 728, 4, 714, 262, 4, 669, 5751, 2],
     [662, 20, 5752, 2865, 6, 2865, 3874, 42, 273],
     [415, 124, 1456, 269, 54, 232],
     [493,
      210,
      61,
      249,
      826,
      811,
      1342,
      179,
      3,
      267,
      237,
      946,
      5,
      25,
      283,
      266,
      138,
      309,
      52,
      264,
      1343,
      125,
      28,
      36,
      134,
      40,
      15],
     [2404, 186, 444, 29, 5, 40, 4, 80, 157, 19, 230, 40, 4, 228],
     [50, 2405, 2052],
     [694, 1344, 2, 396, 47],
     [92, 645, 73, 9, 128, 2],
     [324, 31, 63, 3, 867, 2],
     [9, 378, 128, 34, 351, 39, 16, 42, 369],
     [2960, 1345, 4, 34, 129, 348, 416, 16, 643, 397, 133, 70, 7, 109],
     [603,
      1992,
      90,
      3,
      3875,
      510,
      5753,
      144,
      167,
      3876,
      1812,
      96,
      33,
      512,
      193,
      1622,
      2961,
      5754,
      44,
      3877,
      5755,
      526,
      95,
      1089,
      53,
      1288,
      1813,
      139,
      1743,
      107,
      90,
      3,
      187],
     [573, 56, 2053, 4, 2054, 875, 1120, 2],
     [5756, 225, 3878],
     [2406,
      230,
      7,
      4,
      131,
      61,
      3,
      59,
      49,
      1346,
      241,
      131,
      61,
      59,
      6,
      2,
      42,
      4,
      4,
      269,
      1814,
      66,
      26,
      200,
      538,
      34,
      360,
      13,
      2019,
      16,
      19,
      623,
      3,
      2,
      55,
      174,
      315],
     [135, 11, 1815, 4, 5757, 5758, 178, 5759, 4, 116, 5],
     [162, 1458, 10, 1235, 1755, 118, 1136, 98, 2055, 86, 201, 10, 62],
     [5760,
      1347,
      827,
      1816,
      2962,
      319,
      206,
      6,
      3879,
      158,
      362,
      577,
      1348,
      675,
      15,
      68,
      1816,
      676,
      94,
      173,
      118,
      24,
      69],
     [48,
      27,
      17,
      49,
      183,
      217,
      305,
      2407,
      2963,
      111,
      427,
      30,
      5761,
      685,
      2056,
      889,
      475,
      1623,
      3,
      234,
      3,
      2057,
      257,
      257,
      358,
      310,
      953,
      39,
      16,
      167,
      5762,
      3880,
      188,
      580,
      5763,
      449,
      3880,
      188,
      1459,
      72,
      131,
      1158,
      5764],
     [49, 84, 12, 2, 3881],
     [80, 5765, 1564, 780, 2058, 44, 1019, 105],
     [214, 272, 110, 5766, 221, 483, 408],
     [2964, 368, 11, 2059, 351, 3658, 2408, 5767, 849, 23, 4, 9, 243],
     [327, 4, 828, 2],
     [757, 159, 166, 2409, 2, 434, 127, 5768, 2323, 2, 22, 78],
     [156, 452, 322, 742, 50, 190, 2965, 11, 2410, 22],
     [2060,
      281,
      14,
      41,
      865,
      262,
      4,
      101,
      72,
      607,
      53,
      33,
      25,
      40,
      15,
      1608,
      42,
      4,
      163,
      81,
      20,
      173,
      14,
      694],
     [86,
      302,
      35,
      1204,
      2411,
      16,
      167,
      152,
      3882,
      213,
      260,
      462,
      809,
      90,
      148,
      133,
      727,
      3,
      156,
      352],
     [5769, 13, 2966, 10, 243, 5770, 118, 5771, 436],
     [49, 2967, 161, 24, 1236, 1224, 4, 1624, 452, 5772, 178, 2303],
     [2022, 2968, 890, 184, 8, 34, 2, 31, 213, 34],
     [43, 72, 105, 454, 454, 3883, 2969, 18, 5773, 277, 27],
     [1817, 22, 144, 153, 589, 22, 829, 616, 2061, 289, 289],
     [5774, 31, 4, 1625, 2062, 219, 2970, 765],
     [568, 69],
     [238, 5775, 3884],
     [3885, 1237, 16, 48, 3886, 333, 3, 15],
     [603, 2, 166, 5776, 1349, 15, 21],
     [1337, 5777, 214, 2372, 5778],
     [2971, 3, 3, 2],
     [149, 125, 637, 162, 180, 120, 73, 423, 40, 4, 3, 497, 2],
     [235, 122, 34, 11, 3],
     [42, 369, 2412, 320, 843, 959],
     [95, 3, 17, 515, 7, 62, 2, 646, 1238, 3887, 3],
     [3888, 2413, 1060, 960, 3889, 39, 90, 148],
     [45, 2414, 216, 1020, 107, 700, 2043],
     [1239,
      477,
      2063,
      887,
      2,
      539,
      31,
      245,
      784,
      869,
      2972,
      2,
      55,
      1151,
      212,
      295,
      1806,
      2973,
      4],
     [368, 370, 41, 1021, 2],
     [49, 163, 44, 403, 24, 140, 2974, 2975, 20, 2974, 4, 2064, 3, 45],
     [9, 961, 16, 265, 189, 221, 4],
     [46, 2976, 403, 911, 5779, 1818, 4],
     [2371, 5780, 1976, 323, 212, 323, 149, 3890],
     [280],
     [2065,
      997,
      2868,
      4,
      87,
      3891,
      319,
      119,
      5781,
      32,
      1052,
      169,
      2977,
      3736,
      2978,
      16,
      5782,
      110],
     [2415, 1090, 2, 1091, 2416, 5783, 216, 68],
     [2, 41, 159, 1058, 2066, 638],
     [192,
      2019,
      16,
      19,
      1563,
      3892,
      23,
      114,
      86,
      1460,
      35,
      624,
      19,
      830,
      367,
      1292,
      956,
      92,
      3893,
      23,
      33,
      4,
      117,
      1022,
      418,
      1240,
      258,
      571,
      36],
     [1819, 302, 3894, 21, 81, 20, 9, 233, 36, 631, 71, 18, 13],
     [124, 3],
     [141, 27, 2979, 442, 1461, 789, 317, 492, 2980, 2979, 5784, 45],
     [255, 3895, 188, 23, 10, 79, 4, 17, 28],
     [114, 57],
     [58],
     [318, 92, 111, 208, 164, 92, 126, 2, 478, 11, 8, 14, 5785, 2],
     [528, 5786, 175, 5787, 82, 23, 82, 110, 82, 441, 82],
     [3896, 1350, 87, 270, 3, 463, 40, 65, 2],
     [1820, 266, 725, 209, 231, 163, 208, 715, 252, 481, 139, 1351],
     [941, 846],
     [28, 686, 3],
     [77, 64],
     [51, 831, 234, 2848, 5788, 1626, 587, 2417, 16, 167, 128],
     [214, 2012, 40, 4, 2067, 214, 2012, 21, 5789, 72],
     [714, 42, 4, 5, 441, 28, 2418, 295, 276, 29, 2981],
     [114],
     [259, 417, 1241, 120, 2, 5790, 73, 4, 2],
     [90, 3, 80, 1821, 2419, 365, 104, 3897, 5791, 2054, 109],
     [28, 109, 6, 9, 1337, 2, 111, 113, 39, 16, 6, 182, 2420, 3898, 5],
     [471, 1092, 2421],
     [3899,
      1023,
      862,
      483,
      66,
      294,
      384,
      3,
      5792,
      2900,
      36,
      166,
      14,
      24,
      284,
      2422,
      3899,
      1159,
      2982,
      118,
      714,
      42,
      140,
      4,
      3900,
      2422,
      213,
      5793,
      2422,
      159,
      465,
      79,
      4,
      138,
      5794,
      83,
      2068,
      27,
      2069,
      729,
      116,
      4,
      42,
      94],
     [54, 716, 149, 92, 5795, 1559, 126, 45],
     [438, 427],
     [154, 355, 2],
     [715, 1242, 310],
     [941, 3901, 317, 749, 317, 928, 317, 5796, 3901, 449, 211, 211, 14],
     [163, 44, 17, 62, 3, 227],
     [2782, 1126, 5797, 404, 33, 414, 422, 318, 586, 12],
     [14,
      55,
      29,
      55,
      354,
      210,
      1822,
      630,
      1093,
      7,
      1093,
      354,
      210,
      630,
      118,
      3902,
      1462],
     [2983, 916, 72, 2],
     [346, 891, 22, 4],
     [1069, 18],
     [37, 606, 26, 222, 255, 12],
     [30, 129, 1243, 685, 1823, 1160],
     [2061, 401, 307, 2, 224, 3, 59, 1316],
     [108, 1627, 1244, 1015, 47, 315, 6, 514, 37, 25, 32, 865, 1421, 687],
     [30, 129, 28, 2, 55, 74, 3903, 154, 334],
     [885, 277],
     [1069,
      3904,
      892,
      366,
      138,
      1012,
      207,
      161,
      71,
      12,
      539,
      373,
      893,
      4,
      845,
      5798,
      192,
      597,
      2984,
      5799,
      27,
      2985,
      960,
      5800,
      2986,
      2423,
      5],
     [894,
      265,
      57,
      5801,
      198,
      1628,
      66,
      447,
      5,
      955,
      632,
      44,
      2070,
      4,
      1463,
      499,
      5802,
      11,
      584,
      398,
      3905,
      590,
      5803,
      3905,
      19,
      3906,
      19,
      2071,
      149,
      453,
      24,
      284,
      826,
      102,
      138,
      1191,
      4,
      875,
      507,
      2987,
      3907,
      60,
      138,
      529,
      11,
      948,
      4,
      3908,
      5804,
      34,
      7,
      948,
      2424,
      1191],
     [666,
      2988,
      367,
      232,
      153,
      140,
      2,
      954,
      2989,
      5805,
      1993,
      2425,
      188,
      809,
      484,
      3909,
      2304,
      809,
      342,
      19,
      53,
      226,
      2990,
      5,
      263,
      172,
      173,
      29,
      5806],
     [962, 18, 5807, 3910, 2991, 6, 414, 472, 66],
     [106, 62, 1352],
     [155, 14, 113, 130],
     [1332, 10, 98, 54, 69, 832, 2426, 3881, 1442, 5808, 186],
     [37, 3, 93, 6],
     [145, 203, 3911, 214, 2948, 5809, 88, 69, 384, 2992, 5810, 442, 5811],
     [83, 1464, 1772, 111, 8, 364, 33, 67, 1629, 59],
     [9, 3912, 577],
     [172, 2072, 5812, 4, 1000, 1601, 32, 223, 1563, 5813, 698, 592, 566],
     [5814, 240, 82, 315, 245],
     [2427,
      171,
      552,
      18,
      1353,
      552,
      289,
      289,
      2427,
      1824,
      2,
      88,
      25,
      17,
      519,
      2993,
      46,
      32,
      87,
      19,
      3913,
      1465],
     [10, 3914, 19, 187, 228, 3, 267, 1354, 244],
     [62],
     [1243, 112, 77, 12, 152, 874],
     [1147,
      112,
      97,
      1630,
      63,
      3,
      5815,
      20,
      157,
      267,
      309,
      934,
      3,
      301,
      59,
      21,
      209,
      8],
     [181, 62, 5816, 42, 33, 63, 2994, 467, 44, 1024, 112, 2073, 629],
     [543, 963, 68, 24, 174, 259, 120, 68, 349, 16, 19, 2403, 226],
     [39, 16, 167, 12],
     [46, 2995, 256, 833, 31, 22],
     [49, 435, 20, 3, 36, 5],
     [991, 571, 5817, 411, 172, 5818, 2996, 9, 687, 1239, 3693, 253],
     [656, 2, 179, 104, 27, 74, 5819, 5820, 2],
     [2988, 367, 232, 40, 4, 140],
     [42,
      504,
      959,
      415,
      348,
      1161,
      3915,
      6,
      272,
      5821,
      518,
      6,
      2428,
      20,
      460,
      2997,
      142,
      1161,
      698,
      270,
      68,
      348,
      703,
      2042,
      1320,
      2074,
      420,
      5822,
      814,
      97,
      1631,
      170,
      2429,
      1057,
      984,
      2998,
      2074,
      741,
      207,
      121,
      3916,
      15,
      959,
      68],
     [538, 5823, 116, 1245, 1004, 46, 192, 42, 4, 82],
     [2999, 5824, 5825, 3917, 5826, 316, 44, 32, 1355, 300, 1632],
     [511, 284, 1824, 3, 284, 122, 193, 3918, 3000, 3919, 1320, 159, 220],
     [9, 62],
     [332, 19, 790, 12, 51, 11, 47, 2],
     [5827, 3920, 5828, 2430, 140],
     [848, 543, 5829, 3, 1211, 3001, 460, 890, 447, 124, 41, 3921, 3],
     [547, 2, 18, 9, 114, 57, 51, 47],
     [26,
      3,
      117,
      5830,
      1537,
      7,
      5831,
      474,
      2,
      230,
      7,
      18,
      7,
      1825,
      118,
      26,
      2431,
      112,
      595],
     [5832, 2001, 165, 758, 32, 487, 86],
     [5833, 5834, 949, 3002, 99, 5835, 3, 72, 1239, 2075, 1633, 41, 1227],
     [9, 206, 338, 2, 494, 2, 253, 77, 46, 2],
     [1237, 16],
     [1810, 427, 348, 287, 155, 66, 95, 184, 161, 23, 114, 35, 114],
     [31, 211],
     [734, 856, 24, 207, 53, 22, 13],
     [393, 1094, 7, 195, 5836, 10, 378, 14, 1246],
     [1989, 30, 129, 93, 2, 1356, 1634, 729],
     [425, 530, 62, 75, 70, 7, 2],
     [2432,
      1611,
      3922,
      5837,
      65,
      3,
      32,
      348,
      525,
      1804,
      2433,
      3923,
      142,
      5838,
      5839,
      5840,
      2076,
      5841,
      24,
      3003,
      15,
      3004,
      957,
      3005,
      5842,
      1804,
      4,
      3891,
      735,
      6,
      1466,
      1130,
      957,
      3006,
      394,
      198,
      79,
      140,
      4],
     [5843, 277, 293, 3007, 507, 89, 350, 1134, 350, 301, 18, 91, 57],
     [80, 2434, 917, 2, 746, 42, 4],
     [99, 1225, 1964, 5844, 3008, 1095, 70, 7, 414, 154, 334],
     [5845, 2418, 5846, 3924, 5847, 5848, 1775, 236, 106, 2, 895, 4],
     [1826, 5849, 756, 537, 24],
     [10, 62, 123, 148, 3],
     [26, 451, 932, 526, 17, 50],
     [471, 3925, 2056, 5850],
     [71, 449, 745, 2435, 10, 98, 264, 82, 35, 165],
     [91, 448, 134, 377, 22, 401],
     [30, 3, 2, 55, 780, 3926, 70, 7, 81, 20, 28],
     [52,
      1081,
      5,
      727,
      54,
      1467,
      422,
      3927,
      17,
      425,
      13,
      3009,
      3928,
      17,
      5851,
      25,
      279,
      188,
      37,
      82,
      1635,
      71,
      578,
      4,
      364,
      14],
     [124, 688, 173, 2, 3, 12, 5852, 240, 45],
     [156, 5853, 12],
     [8, 542, 331],
     [5854, 1330, 26, 2361, 247],
     [49,
      998,
      4,
      773,
      5855,
      1593,
      277,
      773,
      5856,
      199,
      129,
      82,
      2,
      218,
      250,
      330,
      595,
      1247,
      121,
      2077],
     [5857, 3010, 1800, 331, 60],
     [3929, 3, 14, 147, 177, 2, 292, 1468, 3011],
     [5858, 5859, 52, 42, 140, 782, 2, 1237],
     [2, 37, 5860, 94, 649, 182],
     [34, 1733, 459, 27, 711, 1733, 854, 116, 4, 503, 814, 3012, 508, 697, 639],
     [1827, 7, 655, 100, 1126, 2436, 4, 951, 38, 992, 2006, 5861, 50, 3, 2437],
     [292, 409, 369, 890, 5862],
     [156, 5863, 1186, 100, 5864, 501, 130, 4, 669, 3013, 964, 130, 4, 7, 2, 253],
     [279, 1469, 20, 246, 3, 1466, 73, 331, 1994, 3730],
     [149, 92, 30, 436, 126, 76, 125],
     [354, 210, 539, 415, 14],
     [3014, 4, 186, 3015, 5, 85, 739],
     [514,
      137,
      54,
      232,
      46,
      1243,
      112,
      3866,
      5865,
      11,
      22,
      208,
      160,
      2,
      746,
      10,
      3016,
      117],
     [231, 114, 5, 27, 159, 1131, 231, 940, 25],
     [309,
      3860,
      57,
      14,
      81,
      111,
      26,
      222,
      346,
      53,
      1246,
      165,
      987,
      3017,
      5866,
      157,
      26,
      1754,
      3790,
      5867,
      4,
      769,
      3,
      491,
      31,
      4],
     [30, 17, 88, 2078, 142, 3930, 750, 5, 13],
     [12, 345, 5868, 2357, 3018, 1287, 4, 98],
     [299, 6, 882, 219, 6, 45],
     [102,
      1357,
      13,
      68,
      313,
      676,
      1125,
      49,
      201,
      187,
      206,
      6,
      17,
      54,
      5,
      305,
      36,
      49,
      404,
      535,
      58,
      25,
      219,
      94,
      5869,
      6],
     [26, 222, 3931, 5870, 130, 33, 4, 2, 424, 28, 107],
     [348, 510, 1096, 3019, 3020, 49, 90, 38, 76, 492, 503, 4, 44, 5],
     [96, 314, 183, 225, 138, 48, 208, 17, 418, 18],
     [477, 99, 1591, 3932, 477, 709, 25, 5871, 48, 27, 182, 47, 5872, 227],
     [696],
     [153, 3933, 139, 23, 3934, 1097, 5873, 139, 86, 726, 139, 806, 16, 717],
     [663, 2438, 177],
     [91, 2, 134, 25, 2024, 64, 4, 252],
     [50],
     [874,
      3935,
      37,
      82,
      5874,
      188,
      5875,
      2,
      3,
      60,
      12,
      13,
      1098,
      3936,
      1636,
      82,
      1086,
      57],
     [80, 104, 24, 231, 5876, 57, 8, 499, 5877, 483],
     [3, 3, 5, 56, 697, 2439, 380, 57],
     [26, 1073],
     [43, 2079, 7, 3021, 2080, 650],
     [5878, 5879, 2440, 205, 3706, 139, 2, 201, 10, 50],
     [1079, 328, 1017, 42, 94, 35],
     [547,
      331,
      542,
      494,
      489,
      544,
      2827,
      563,
      1470,
      709,
      12,
      21,
      5880,
      1637,
      2930,
      5881,
      1358,
      26,
      306,
      60],
     [2081,
      118,
      1471,
      15,
      275,
      60,
      1359,
      229,
      348,
      3937,
      85,
      276,
      479,
      518,
      6,
      195,
      95,
      3,
      1060,
      3937,
      85,
      1638,
      56,
      20,
      1137,
      35,
      524,
      447,
      5882,
      219,
      348,
      5883,
      118,
      539,
      2441,
      702,
      131,
      78],
     [264, 150, 4, 5, 2442, 5884, 37, 3938, 539, 295, 5, 72, 5885, 24, 23, 4, 3],
     [332, 30, 215, 43, 97, 2, 3, 26, 304, 47, 2082, 150],
     [248, 5886, 242, 924, 1639, 60, 757],
     [3022, 5887, 3023, 2051, 2335, 109, 240, 75, 40, 896, 826, 57],
     [458, 1472, 325, 3, 36, 6, 3939, 90, 3, 7, 458, 8],
     [586, 871, 3024, 2],
     [84, 46, 3940, 286, 3941, 265],
     [26, 200, 3, 941, 51, 47, 5888, 2, 103, 115, 131, 61, 59],
     [5889, 210, 1810, 2024, 4, 2, 957, 41, 5890],
     [95, 403, 24, 4, 33, 3],
     [882, 93, 2, 14, 3942, 668, 14, 67, 414, 304, 47],
     [48, 612, 4, 615, 78, 48, 465, 32, 545, 465, 1579, 105],
     [102, 5891, 188, 1968, 3025, 21, 264, 58, 3, 1012, 68, 24, 127, 5892, 533],
     [237, 160, 275, 35, 264, 84, 147, 695, 4],
     [2,
      3,
      256,
      4,
      1640,
      438,
      6,
      9,
      480,
      20,
      5893,
      351,
      2,
      387,
      5894,
      1225,
      254,
      3943,
      6,
      71,
      4],
     [109, 15, 1025, 7, 2],
     [484, 103, 60, 44, 40, 99, 92, 5895, 1162, 4, 3],
     [439, 4, 1360, 2939, 875],
     [1828, 88, 139],
     [242, 49, 2083, 897, 30, 696, 2, 55, 1361, 187, 107],
     [432, 202, 341, 247],
     [36, 5896, 329, 10, 238, 5897, 4, 804, 3944, 329, 708, 209, 10, 681, 445],
     [2, 3, 51, 47, 81, 69, 5898, 69, 2],
     [46, 323, 15, 144, 72, 208, 7, 151],
     [5899, 572, 20, 1152, 3, 45, 363, 2, 327],
     [417, 1026, 46, 441, 498, 1829, 181],
     [2, 292, 857, 227],
     [623, 3, 2, 55, 386, 225],
     [88, 608, 20, 952, 23, 438, 3, 2, 54, 2083, 167, 264, 9, 602, 2084, 3945],
     [9, 363, 169, 1830, 1248],
     [28, 55, 74],
     [3946, 1362, 513, 1203],
     [8, 2, 179, 348, 354, 210, 579, 5900, 4, 29, 919, 70, 5, 1641],
     [3947,
      791,
      340,
      71,
      53,
      3026,
      25,
      5901,
      3948,
      188,
      42,
      4,
      3948,
      791,
      98,
      447],
     [342, 5902, 5903, 3027, 952, 2443],
     [86, 393, 272, 449, 168, 32, 201, 54, 5904, 94, 248, 3949, 4],
     [77, 64, 51, 10, 10, 145, 120, 5905, 3950, 672, 2322, 97, 1427, 226, 18, 93],
     [77, 90, 3, 311],
     [615,
      20,
      718,
      3,
      5906,
      3951,
      948,
      4,
      21,
      124,
      1099,
      615,
      88,
      391,
      3952,
      233,
      278,
      2,
      801,
      321,
      259,
      67,
      2,
      6],
     [305, 123, 950, 3, 1151, 36, 670, 108, 1246],
     [269, 5907, 13, 2, 177],
     [5908, 5909, 605, 44, 501, 38, 408, 88, 211, 7, 4, 5910, 1537],
     [5911, 3028],
     [5912, 23, 79, 4],
     [2444, 1416, 5913, 3029, 7],
     [5914, 976, 115, 254, 3953, 217, 7, 339, 7],
     [3030,
      5915,
      3954,
      3955,
      5916,
      1473,
      1592,
      3956,
      864,
      3031,
      2872,
      3032,
      52,
      47,
      52,
      352,
      894,
      67,
      76,
      81],
     [132, 95, 3, 55, 111, 30, 1027, 29, 733, 2085, 226, 6, 78],
     [387, 50, 155, 3033, 20, 102, 1198, 21, 834, 439, 59, 2, 3957, 74, 5, 2],
     [155, 135, 38, 1299, 26, 121, 3034, 1642, 147, 5917, 3958],
     [73, 1474, 790, 2, 28, 2, 56, 1363, 2445, 4, 2446],
     [782, 16, 1432, 3, 258, 153, 70, 164, 406],
     [90, 3, 62, 955, 10, 12],
     [73, 223, 1831, 2028],
     [43, 2, 166, 49, 610],
     [129, 689, 32, 1364, 9, 432, 106, 1154, 41, 6],
     [1567, 915, 5918, 7],
     [49, 96, 12, 1055, 1643, 152, 1774, 627, 13, 2447, 309, 5],
     [925, 49, 39, 16, 333, 4, 34, 5919, 749],
     [14, 1213, 247, 3959, 96, 504, 5920, 20, 3960, 17, 1538],
     [49, 5921, 12],
     [3961],
     [498, 12, 156, 18, 149],
     [5922, 404, 835, 12],
     [46, 3035, 740, 1475, 4, 186, 46, 861, 2],
     [2086, 817, 26, 3962, 328, 5923, 224, 364, 67, 1989],
     [2, 930, 12, 4, 195, 135, 883, 44, 3, 1249],
     [1007,
      3,
      170,
      527,
      115,
      1644,
      1832,
      4,
      48,
      9,
      1416,
      128,
      73,
      127,
      7,
      9,
      3963,
      1100,
      5924,
      73,
      933,
      53,
      546,
      355,
      8,
      3964,
      5,
      73,
      408,
      184,
      669,
      73,
      6,
      128],
     [332, 30, 2, 129, 156, 213, 29, 55, 93],
     [355, 321, 8],
     [290, 11, 3036, 270, 2087, 1824, 38, 22, 2087, 10, 122, 26, 14, 759],
     [120, 664, 27, 5925, 1098, 2045, 65],
     [117, 137, 2041, 232, 130, 1163, 848, 2, 131, 196],
     [128],
     [1028, 2448, 3965, 218, 5926, 898, 5927, 21, 4, 3037, 170],
     [1250, 118, 72],
     [116, 4, 499, 3, 5928],
     [9, 5929, 194, 5930],
     [5931],
     [5932, 3, 835, 62],
     [26, 1073, 2324],
     [48, 9, 379, 203, 1029, 2, 117, 84, 87, 47, 308, 3038, 3],
     [1629],
     [596, 141, 2, 141, 69, 141],
     [1249, 195, 59, 343, 3039, 7],
     [2088, 1160, 55, 24, 174, 109],
     [136, 381, 19, 806, 2449, 1365, 2089, 3966, 5933, 492, 374, 217, 5],
     [58, 1126, 44, 3, 28, 565, 5934, 2450, 1089],
     [2065, 2, 2090, 1082, 3725, 5935],
     [97, 5936, 3967, 2, 193],
     [26, 10, 200],
     [188,
      48,
      5937,
      227,
      188,
      82,
      3040,
      27,
      5938,
      45,
      137,
      5939,
      199,
      498,
      5940,
      316,
      50,
      41,
      40,
      4,
      1833,
      88,
      432,
      689,
      270,
      7,
      1366,
      690,
      74,
      5,
      81,
      17,
      41,
      188,
      1058,
      4],
     [28, 2, 42, 369],
     [888, 63, 12, 8],
     [3968, 399, 148, 446, 2091, 90, 3, 320],
     [3969, 1065, 391, 5941],
     [2, 767, 267, 1770, 24, 629, 22, 2400, 235, 20, 40, 63, 3, 1335, 124],
     [205, 608, 20, 11, 1640, 239, 474, 5942, 4, 21, 205, 3970, 1421, 93, 6],
     [14, 5],
     [913, 120, 103, 6, 123, 3, 135],
     [3041,
      17,
      899,
      2,
      3042,
      83,
      82,
      53,
      1734,
      18,
      248,
      3041,
      5943,
      54,
      406,
      279,
      3971,
      5944,
      446,
      24,
      2069,
      207,
      5945,
      3041,
      1367,
      5946,
      627,
      150,
      6,
      615,
      181,
      44,
      1087,
      1333,
      1080,
      573,
      21,
      78,
      279,
      953,
      1834,
      266,
      330,
      710,
      3],
     [17, 1472, 325, 3, 2, 23, 520],
     [10,
      89,
      428,
      15,
      2,
      433,
      53,
      533,
      9,
      5947,
      3,
      267,
      3972,
      3043,
      5948,
      5949,
      99,
      2,
      2451],
     [271],
     [1751, 41, 68, 1835, 7, 852, 152, 10, 428, 15, 3973, 7],
     [4, 42, 5],
     [83, 56, 5, 39, 74, 5],
     [1590, 509, 2092],
     [17, 5950, 23, 4, 1083],
     [521, 54, 410, 97, 84, 64, 5951, 187, 21, 1141, 92, 495, 21],
     [93, 55, 93, 9, 1368, 2, 308, 91, 25, 41, 121, 2874, 5952, 20, 5953],
     [39, 32, 201, 565],
     [2075, 1633, 5, 474, 1836, 316, 1369],
     [2093, 3, 28, 542, 2],
     [615, 260, 5954, 19, 4, 1740, 2, 58, 1101, 13],
     [1164, 12, 3, 3974, 4, 5955, 23, 344, 325],
     [5956, 159, 300, 527, 277, 15, 7, 3975, 994, 2330, 295, 48, 1538],
     [1453],
     [1057, 55, 411, 3976, 20, 3, 1803, 163, 626, 2094, 605, 11, 1370, 4, 1803],
     [5957, 58, 94, 44, 7],
     [74, 555, 68],
     [308, 91, 87, 67, 3, 172, 233],
     [114, 6],
     [5958, 1371, 329, 3817],
     [294,
      3044,
      307,
      652,
      200,
      68,
      19,
      172,
      997,
      130,
      138,
      294,
      202,
      58,
      3977,
      309,
      443,
      200,
      2452,
      3045,
      36],
     [135,
      1365,
      740,
      2095,
      2453,
      1098,
      22,
      2,
      1232,
      333,
      4,
      5,
      32,
      264,
      1645,
      4,
      2,
      134,
      3,
      3046,
      276,
      2,
      891,
      3,
      153,
      15,
      14,
      36,
      27,
      242,
      2,
      135,
      1022,
      4,
      388,
      14,
      6],
     [654, 24, 1793, 3978, 41],
     [43, 69, 2, 1030, 357, 156, 1372, 242, 5959, 1968, 41, 159, 67, 94],
     [306, 3047, 6],
     [49,
      30,
      3979,
      632,
      44,
      3048,
      1165,
      24,
      140,
      91,
      20,
      180,
      149,
      92,
      5960,
      199,
      5961,
      163,
      44,
      953,
      281,
      2,
      374,
      552,
      19,
      145,
      1476,
      4,
      40,
      3,
      1477,
      1102,
      33,
      4],
     [5962, 2413, 322, 5963, 63, 17, 13, 1166, 73, 246, 27, 601, 3980, 4, 486],
     [229, 44, 38, 376, 519, 28, 12],
     [9, 565, 9, 12],
     [3981, 3, 327, 327],
     [1131,
      104,
      5964,
      1103,
      900,
      5965,
      3049,
      196,
      29,
      5966,
      61,
      146,
      5967,
      5968,
      5969,
      5970,
      621,
      900,
      146,
      2454,
      6,
      3982,
      257,
      257,
      754,
      29,
      296,
      575,
      175,
      290,
      11,
      154,
      2096,
      2,
      3,
      8],
     [5971, 3983, 1730, 137, 965, 5972],
     [458, 203],
     [95, 3, 12, 17, 836, 193],
     [5973, 11, 14, 229, 348, 389, 24, 3, 2, 267, 1565, 5974, 167, 76, 45],
     [5975, 3, 322, 558, 3, 5, 2917, 82],
     [106, 5976, 5977],
     [487, 23, 919, 49, 141],
     [1189, 137, 3050, 719, 197, 209, 3051, 633, 3, 185],
     [3052, 1478, 2455, 102, 1837, 137, 5978, 141],
     [10, 8, 162, 901, 1311, 715, 38, 3984, 10, 281, 2097],
     [212, 295, 5979, 38, 428, 4, 4, 2098, 3053, 2025, 428, 4, 94, 3985],
     [1104, 324, 15, 2, 762, 38, 3, 53, 62],
     [665, 823, 2, 6, 45, 5980, 119, 1099, 1646, 296, 46],
     [8],
     [540, 650, 966, 18, 792, 25, 90, 229, 496, 57, 182, 10, 152, 3986, 57, 182],
     [156,
      434,
      2,
      522,
      461,
      109,
      306,
      1031,
      250,
      3054,
      3054,
      1373,
      18,
      739,
      172,
      3054,
      1373,
      261,
      14,
      24,
      401,
      309,
      28,
      6,
      2,
      1088,
      1978,
      5981,
      359],
     [148, 3, 938, 153, 90, 3, 56, 7],
     [59, 56, 5],
     [1751,
      580,
      4,
      3055,
      2,
      98,
      29,
      698,
      4,
      279,
      397,
      338,
      1318,
      206,
      11,
      698,
      186,
      367,
      74,
      698,
      33,
      4],
     [304,
      47,
      36,
      117,
      103,
      161,
      298,
      62,
      2023,
      1008,
      3987,
      1616,
      489,
      2456,
      1251,
      316,
      33,
      4,
      291,
      35,
      20,
      60,
      117,
      589,
      5982,
      1240,
      357,
      532,
      295,
      2457,
      31,
      3988],
     [725, 1479, 169, 56, 3001, 5],
     [1152,
      682,
      3056,
      3057,
      1292,
      2,
      169,
      34,
      1838,
      1159,
      933,
      344,
      325,
      1137,
      2,
      732,
      1839,
      1159,
      785,
      1838,
      1159,
      1056,
      1105,
      323,
      138,
      204,
      323,
      61,
      154,
      1552,
      1411,
      2],
     [97],
     [32,
      180,
      363,
      1407,
      2773,
      4,
      70,
      5,
      440,
      2773,
      20,
      1252,
      3058,
      17,
      3058,
      242,
      1480,
      1647,
      1085,
      363,
      2971,
      4,
      5,
      5983,
      146,
      5984,
      21,
      1436,
      73,
      4,
      34,
      180,
      828,
      2394,
      30,
      517,
      612,
      21,
      33,
      440,
      18],
     [5985,
      5986,
      5987,
      1648,
      449,
      745,
      32,
      5,
      209,
      4,
      3989,
      20,
      203,
      32,
      201,
      6,
      248,
      991,
      1649,
      3059,
      1649,
      70,
      5,
      3990,
      3991,
      3,
      29,
      13,
      146,
      355,
      4,
      36,
      1089,
      3992,
      11,
      837,
      4,
      36,
      2839,
      416,
      3990,
      3884],
     [9, 93, 2, 3, 567, 491, 454, 763],
     [80, 3993, 2458, 31, 2459, 783],
     [728,
      2099,
      2100,
      3060,
      3061,
      223,
      1831,
      356,
      1645,
      19,
      1127,
      3994,
      2013,
      191,
      5988,
      683,
      356,
      5989,
      3995,
      3062,
      2460,
      3996,
      4,
      1831,
      1223,
      5990,
      2461],
     ...]




```python
index_to_word = {}
for key, value in word_to_index.items():
    index_to_word[value] = key

decoded_sample = [index_to_word[word] for word in encoded_X_train[0]]
print('기존의 첫번째 샘플 :', X_train[0])
print('복원된 첫번째 샘플 :', decoded_sample)
```

    기존의 첫번째 샘플 : ['감동', '교육', '계', '비판', '사랑', '손대다', '방향', '모두', '에서', '확실하다', '거', '없이', '어정쩡하다', '영화', '바라보다', '만', '하다', '거', '라면', '대체', '극영화', '로', '왜', '만들다', '거야']
    복원된 첫번째 샘플 : ['감동', '교육', '계', '비판', '사랑', '손대다', '방향', '모두', '에서', '확실하다', '거', '없이', '어정쩡하다', '영화', '바라보다', '만', '하다', '거', '라면', '대체', '극영화', '로', '왜', '만들다', '거야']


### Zero 패딩 (Padding)


```python
encoded_X_train[:10]
```




    [[39,
      1186,
      843,
      976,
      73,
      2771,
      1718,
      272,
      24,
      573,
      49,
      164,
      3651,
      2,
      1279,
      11,
      4,
      49,
      399,
      514,
      5321,
      20,
      37,
      25,
      1949],
     [62, 3652, 1537, 247],
     [136,
      373,
      2,
      192,
      5322,
      202,
      155,
      75,
      1538,
      1950,
      666,
      2772,
      18,
      479,
      1045,
      25,
      5323,
      4],
     [5324,
      3653,
      3654,
      910,
      5325,
      1280,
      185,
      977,
      2773,
      4,
      91,
      113,
      74,
      797,
      74,
      294,
      1046,
      1187,
      1719,
      5326,
      41,
      2774,
      441,
      1720,
      4,
      186,
      80,
      172,
      1721,
      5327,
      2288,
      15,
      104,
      844,
      1539],
     [56,
      74,
      5,
      1951,
      911,
      3655,
      5328,
      452,
      16,
      54,
      798,
      63,
      3,
      912,
      1407,
      124,
      978,
      54,
      165,
      762,
      62,
      1120,
      16,
      85,
      54,
      425,
      65,
      845,
      156,
      92,
      217,
      137,
      5329,
      3656,
      1540,
      1722,
      4,
      7],
     [46, 480, 20, 1121, 227, 89, 353, 11, 3, 187, 176, 1952],
     [64, 273, 70, 164, 200, 26],
     [132, 114, 280, 5],
     [3657, 552, 846, 1047, 391, 3657, 93, 5330, 100, 2, 315, 261, 91, 72],
     [9, 515, 725, 5331, 5332, 5333, 138]]




```python
max_len = 30
def pad_sequences(sentences, max_len):
  features = np.zeros((len(sentences), max_len), dtype=int)
  for index, sentence in enumerate(sentences):
    if len(sentence) != 0:
      features[index, :len(sentence)] = np.array(sentence)[:max_len]
  return features

padded_X_train = pad_sequences(encoded_X_train, max_len=max_len)
padded_X_valid = pad_sequences(encoded_X_valid, max_len=max_len)

print('훈련 데이터의 크기 :', padded_X_train.shape)
print('검증 데이터의 크기 :', padded_X_valid.shape)

```

    훈련 데이터의 크기 : (7886, 30)
    검증 데이터의 크기 : (1972, 30)



```python
print('첫번째 샘플의 길이 :', len(padded_X_train[0]))
print('첫번째 샘플 :', padded_X_train[0])
```

    첫번째 샘플의 길이 : 30
    첫번째 샘플 : [  39 1186  843  976   73 2771 1718  272   24  573   49  164 3651    2
     1279   11    4   49  399  514 5321   20   37   25 1949    0    0    0
        0    0]


### LSTM을 이용한 네이버 영화 리뷰 분류 모델


```python
train_label_tensor = torch.tensor(np.array(y_train))
valid_label_tensor = torch.tensor(np.array(y_valid))
```


```python
embedding_dim = 100
hidden_dim = 128
output_dim = 2
learning_rate = 0.1
num_epochs = 10
```


```python
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(TextClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x: (batch_size, seq_length)
        embedded = self.embedding(x)  # (batch_size, seq_length, embedding_dim)

        # LSTM은 (hidden state, cell state)의 튜플을 반환합니다
        lstm_out, (hidden, cell) = self.lstm(embedded)  # lstm_out: (batch_size, seq_length, hidden_dim), hidden: (1, batch_size, hidden_dim)

        last_hidden = hidden.squeeze(0)  # (batch_size, hidden_dim)
        logits = self.fc(last_hidden)  # (batch_size, output_dim)
        
        return logits

```


```python
torch.tensor(padded_X_train)
```




    tensor([[  39, 1186,  843,  ...,    0,    0,    0],
            [  62, 3652, 1537,  ...,    0,    0,    0],
            [ 136,  373,    2,  ...,    0,    0,    0],
            ...,
            [ 221,   60,  459,  ...,    0,    0,    0],
            [ 365,  910,  386,  ...,    0,    0,    0],
            [ 312,  361,  235,  ...,    0,    0,    0]], dtype=torch.int32)




```python
# encoded_train = torch.tensor(padded_X_train).to(torch.int64)
encoded_train = torch.tensor(padded_X_train)
train_dataset = torch.utils.data.TensorDataset(encoded_train,   # 2d
                                               train_label_tensor) # 1d
train_dataloader = torch.utils.data.DataLoader(train_dataset, 
                                               shuffle=True, 
                                               batch_size=32)

# encoded_valid = torch.tensor(padded_X_valid).to(torch.int64)
encoded_valid = torch.tensor(padded_X_valid)
valid_dataset = torch.utils.data.TensorDataset(encoded_valid, 
                                               valid_label_tensor)
valid_dataloader = torch.utils.data.DataLoader(valid_dataset, 
                                               shuffle=True, 
                                               batch_size=1)

```


```python
model = TextClassifier(vocab_size, embedding_dim, hidden_dim, output_dim)
model.to(device)
```




    TextClassifier(
      (embedding): Embedding(10878, 100)
      (lstm): LSTM(100, 128, batch_first=True)
      (fc): Linear(in_features=128, out_features=2, bias=True)
    )




```python
criterion = nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```


```python
def calculate_accuracy(logits, labels):
    # _, predicted = torch.max(logits, 1)
    predicted = torch.argmax(logits, dim=1)
    correct = (predicted == labels).sum().item()
    total = labels.size(0)
    accuracy = correct / total
    return accuracy
```


```python
def evaluate(model, valid_dataloader, criterion, device):
    val_loss = 0
    val_correct = 0
    val_total = 0

    model.eval()
    with torch.no_grad():
        # 데이터로더로부터 배치 크기만큼의 데이터를 연속으로 로드
        for batch_X, batch_y in valid_dataloader:
            batch_X, batch_y = batch_X.to(device), batch_y.long().to(device)

            # 모델의 예측값
            logits = model(batch_X)

            # 손실을 계산
            loss = criterion(logits, batch_y)

            # 정확도와 손실을 계산함
            val_loss += loss.item()
            val_correct += calculate_accuracy(logits, batch_y) * batch_y.size(0)
            val_total += batch_y.size(0)

    val_accuracy = val_correct / val_total
    val_loss /= len(valid_dataloader)

    return val_loss, val_accuracy

```


```python
num_epochs = 20

# Training loop
best_val_loss = float('inf')

# Training loop
for epoch in range(num_epochs):
    # Training
    train_loss = 0
    train_correct = 0
    train_total = 0
    model.train()
    for batch_X, batch_y in tqdm(train_dataloader):
        # Forward pass
        batch_X, batch_y = batch_X.to(device), batch_y.long().to(device)
        # batch_X.shape == (batch_size, max_len)
        # batch_y = batch_y.long()
        logits = model(batch_X)

        # Compute loss
        loss = criterion(logits, batch_y)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Calculate training accuracy and loss
        train_loss += loss.item()
        train_correct += calculate_accuracy(logits, batch_y) * batch_y.size(0)
        train_total += batch_y.size(0)

    train_accuracy = train_correct / train_total
    train_loss /= len(train_dataloader)

    val_loss, val_accuracy = evaluate(model, valid_dataloader, criterion, device)

    print(f'Epoch {epoch+1}/{num_epochs}:')
    print(f'Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}')
    print(f'Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}')

    # 검증 손실이 최소일 때 체크포인트 저장
    if val_loss < best_val_loss:
        print(f'Validation loss improved from {best_val_loss:.4f} to {val_loss:.4f}. 체크포인트를 저장합니다.')
        best_val_loss = val_loss
        torch.save(model.state_dict(), 'best_model_checkpoint.pth')

```

    100%|██████████| 247/247 [00:01<00:00, 225.75it/s]


    Epoch 1/20:
    Train Loss: 0.0097, Train Accuracy: 0.9980
    Validation Loss: 1.2554, Validation Accuracy: 0.7556
    Validation loss improved from inf to 1.2554. 체크포인트를 저장합니다.


    100%|██████████| 247/247 [00:01<00:00, 241.60it/s]


    Epoch 2/20:
    Train Loss: 0.0079, Train Accuracy: 0.9985
    Validation Loss: 1.4400, Validation Accuracy: 0.7581


    100%|██████████| 247/247 [00:01<00:00, 152.97it/s]


    Epoch 3/20:
    Train Loss: 0.0112, Train Accuracy: 0.9970
    Validation Loss: 1.1156, Validation Accuracy: 0.7601
    Validation loss improved from 1.2554 to 1.1156. 체크포인트를 저장합니다.


    100%|██████████| 247/247 [00:01<00:00, 239.18it/s]


    Epoch 4/20:
    Train Loss: 0.0137, Train Accuracy: 0.9963
    Validation Loss: 1.2092, Validation Accuracy: 0.7541


    100%|██████████| 247/247 [00:01<00:00, 167.19it/s]


    Epoch 5/20:
    Train Loss: 0.0295, Train Accuracy: 0.9906
    Validation Loss: 1.0336, Validation Accuracy: 0.7465
    Validation loss improved from 1.1156 to 1.0336. 체크포인트를 저장합니다.


    100%|██████████| 247/247 [00:01<00:00, 238.53it/s]


    Epoch 6/20:
    Train Loss: 0.0132, Train Accuracy: 0.9966
    Validation Loss: 1.3661, Validation Accuracy: 0.7581


    100%|██████████| 247/247 [00:01<00:00, 181.97it/s]


    Epoch 7/20:
    Train Loss: 0.0096, Train Accuracy: 0.9970
    Validation Loss: 1.3687, Validation Accuracy: 0.7612


    100%|██████████| 247/247 [00:01<00:00, 226.56it/s]


    Epoch 8/20:
    Train Loss: 0.0097, Train Accuracy: 0.9968
    Validation Loss: 1.3568, Validation Accuracy: 0.7698


    100%|██████████| 247/247 [00:01<00:00, 238.93it/s]


    Epoch 9/20:
    Train Loss: 0.0130, Train Accuracy: 0.9958
    Validation Loss: 1.2913, Validation Accuracy: 0.7556


    100%|██████████| 247/247 [00:01<00:00, 238.29it/s]


    Epoch 10/20:
    Train Loss: 0.0073, Train Accuracy: 0.9977
    Validation Loss: 1.4615, Validation Accuracy: 0.7520


    100%|██████████| 247/247 [00:00<00:00, 261.97it/s]


    Epoch 11/20:
    Train Loss: 0.0042, Train Accuracy: 0.9989
    Validation Loss: 1.4505, Validation Accuracy: 0.7627


    100%|██████████| 247/247 [00:01<00:00, 232.29it/s]


    Epoch 12/20:
    Train Loss: 0.0042, Train Accuracy: 0.9987
    Validation Loss: 1.4539, Validation Accuracy: 0.7632


    100%|██████████| 247/247 [00:01<00:00, 244.68it/s]


    Epoch 13/20:
    Train Loss: 0.0035, Train Accuracy: 0.9990
    Validation Loss: 1.5447, Validation Accuracy: 0.7667


    100%|██████████| 247/247 [00:00<00:00, 253.20it/s]


    Epoch 14/20:
    Train Loss: 0.0035, Train Accuracy: 0.9987
    Validation Loss: 1.5068, Validation Accuracy: 0.7622


    100%|██████████| 247/247 [00:00<00:00, 248.80it/s]


    Epoch 15/20:
    Train Loss: 0.0031, Train Accuracy: 0.9989
    Validation Loss: 1.8140, Validation Accuracy: 0.7667


    100%|██████████| 247/247 [00:00<00:00, 250.06it/s]


    Epoch 16/20:
    Train Loss: 0.0036, Train Accuracy: 0.9991
    Validation Loss: 1.6003, Validation Accuracy: 0.7612


    100%|██████████| 247/247 [00:00<00:00, 252.45it/s]


    Epoch 17/20:
    Train Loss: 0.0026, Train Accuracy: 0.9991
    Validation Loss: 1.7392, Validation Accuracy: 0.7652


    100%|██████████| 247/247 [00:01<00:00, 242.97it/s]


    Epoch 18/20:
    Train Loss: 0.0038, Train Accuracy: 0.9986
    Validation Loss: 1.6365, Validation Accuracy: 0.7622


    100%|██████████| 247/247 [00:00<00:00, 255.37it/s]


    Epoch 19/20:
    Train Loss: 0.0026, Train Accuracy: 0.9990
    Validation Loss: 1.6332, Validation Accuracy: 0.7586


    100%|██████████| 247/247 [00:00<00:00, 263.38it/s]


    Epoch 20/20:
    Train Loss: 0.0032, Train Accuracy: 0.9989
    Validation Loss: 1.4980, Validation Accuracy: 0.7546


### 모델 로드 및 평가


```python
# 모델 로드
model.load_state_dict(torch.load('best_model_checkpoint.pth'))

# 모델을 device에 올립니다.
model.to(device)

```




    TextClassifier(
      (embedding): Embedding(10878, 100)
      (lstm): LSTM(100, 128, batch_first=True)
      (fc): Linear(in_features=128, out_features=2, bias=True)
    )




```python
# 검증 데이터에 대한 정확도와 손실 계산
val_loss, val_accuracy = evaluate(model, valid_dataloader, criterion, device)

print(f'Best model validation loss: {val_loss:.4f}')
print(f'Best model validation accuracy: {val_accuracy:.4f}')

```

    Best model validation loss: 1.0336
    Best model validation accuracy: 0.7465



## 강의_3기_AI응용_6차시__DeepRNN_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_6차시__DeepRNN_.ipynb)

# 6장 Deep RNN

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
# 한글 폰트 설치

!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
# from IPython.display import display

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
# 기본 폰트 설정
plt.rcParams['font.family'] = font_name  # window font

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
import os
import pandas as pd
import seaborn as sns
import json

# from google.colab import drive
# drive.mount('/content/drive')
```

## Text data 전처리

### 데이터 불러오기


```python
## Data read
# download "word2vecnlptutorial1" from kaggle

train_data = pd.read_csv('./csv/labeledTrainData.tsv',
                         header = 0,
                         delimiter = '\t', 
                         quoting = 3)
print(train_data.shape)
train_data.head()
```

    (25000, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>sentiment</th>
      <th>review</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>"5814_8"</td>
      <td>1</td>
      <td>"With all this stuff going down at the moment ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>"2381_9"</td>
      <td>1</td>
      <td>"\"The Classic War of the Worlds\" by Timothy ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>"7759_3"</td>
      <td>0</td>
      <td>"The film starts with a manager (Nicholas Bell...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>"3630_4"</td>
      <td>0</td>
      <td>"It must be assumed that those who praised thi...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>"9495_8"</td>
      <td>1</td>
      <td>"Superbly trashy and wondrously unpretentious ...</td>
    </tr>
  </tbody>
</table>
</div>



### EDA (Explanatory Data Analysis)


```python
## 데이터 갯수

print('전체 학습데이터의 개수: {}'.format(len(train_data)))
```

    전체 학습데이터의 개수: 25000



```python
## Using python

reviews = train_data['review']
# type(reviews[0]) # string
tokenized_review = [r.split() for r in reviews]
print(tokenized_review[0])

##
len_tokenized_review = [len(t) for t in tokenized_review]
print('단어갯수 = ', len_tokenized_review)

## 음절길이
eumjeol_reviews = [len(s.replace(" ", "")) for s in reviews]
print('음절갯수 = ', eumjeol_reviews)
```

    ['"With', 'all', 'this', 'stuff', 'going', 'down', 'at', 'the', 'moment', 'with', 'MJ', "i've", 'started', 'listening', 'to', 'his', 'music,', 'watching', 'the', 'odd', 'documentary', 'here', 'and', 'there,', 'watched', 'The', 'Wiz', 'and', 'watched', 'Moonwalker', 'again.', 'Maybe', 'i', 'just', 'want', 'to', 'get', 'a', 'certain', 'insight', 'into', 'this', 'guy', 'who', 'i', 'thought', 'was', 'really', 'cool', 'in', 'the', 'eighties', 'just', 'to', 'maybe', 'make', 'up', 'my', 'mind', 'whether', 'he', 'is', 'guilty', 'or', 'innocent.', 'Moonwalker', 'is', 'part', 'biography,', 'part', 'feature', 'film', 'which', 'i', 'remember', 'going', 'to', 'see', 'at', 'the', 'cinema', 'when', 'it', 'was', 'originally', 'released.', 'Some', 'of', 'it', 'has', 'subtle', 'messages', 'about', "MJ's", 'feeling', 'towards', 'the', 'press', 'and', 'also', 'the', 'obvious', 'message', 'of', 'drugs', 'are', 'bad', "m'kay.<br", '/><br', '/>Visually', 'impressive', 'but', 'of', 'course', 'this', 'is', 'all', 'about', 'Michael', 'Jackson', 'so', 'unless', 'you', 'remotely', 'like', 'MJ', 'in', 'anyway', 'then', 'you', 'are', 'going', 'to', 'hate', 'this', 'and', 'find', 'it', 'boring.', 'Some', 'may', 'call', 'MJ', 'an', 'egotist', 'for', 'consenting', 'to', 'the', 'making', 'of', 'this', 'movie', 'BUT', 'MJ', 'and', 'most', 'of', 'his', 'fans', 'would', 'say', 'that', 'he', 'made', 'it', 'for', 'the', 'fans', 'which', 'if', 'true', 'is', 'really', 'nice', 'of', 'him.<br', '/><br', '/>The', 'actual', 'feature', 'film', 'bit', 'when', 'it', 'finally', 'starts', 'is', 'only', 'on', 'for', '20', 'minutes', 'or', 'so', 'excluding', 'the', 'Smooth', 'Criminal', 'sequence', 'and', 'Joe', 'Pesci', 'is', 'convincing', 'as', 'a', 'psychopathic', 'all', 'powerful', 'drug', 'lord.', 'Why', 'he', 'wants', 'MJ', 'dead', 'so', 'bad', 'is', 'beyond', 'me.', 'Because', 'MJ', 'overheard', 'his', 'plans?', 'Nah,', 'Joe', "Pesci's", 'character', 'ranted', 'that', 'he', 'wanted', 'people', 'to', 'know', 'it', 'is', 'he', 'who', 'is', 'supplying', 'drugs', 'etc', 'so', 'i', 'dunno,', 'maybe', 'he', 'just', 'hates', "MJ's", 'music.<br', '/><br', '/>Lots', 'of', 'cool', 'things', 'in', 'this', 'like', 'MJ', 'turning', 'into', 'a', 'car', 'and', 'a', 'robot', 'and', 'the', 'whole', 'Speed', 'Demon', 'sequence.', 'Also,', 'the', 'director', 'must', 'have', 'had', 'the', 'patience', 'of', 'a', 'saint', 'when', 'it', 'came', 'to', 'filming', 'the', 'kiddy', 'Bad', 'sequence', 'as', 'usually', 'directors', 'hate', 'working', 'with', 'one', 'kid', 'let', 'alone', 'a', 'whole', 'bunch', 'of', 'them', 'performing', 'a', 'complex', 'dance', 'scene.<br', '/><br', '/>Bottom', 'line,', 'this', 'movie', 'is', 'for', 'people', 'who', 'like', 'MJ', 'on', 'one', 'level', 'or', 'another', '(which', 'i', 'think', 'is', 'most', 'people).', 'If', 'not,', 'then', 'stay', 'away.', 'It', 'does', 'try', 'and', 'give', 'off', 'a', 'wholesome', 'message', 'and', 'ironically', "MJ's", 'bestest', 'buddy', 'in', 'this', 'movie', 'is', 'a', 'girl!', 'Michael', 'Jackson', 'is', 'truly', 'one', 'of', 'the', 'most', 'talented', 'people', 'ever', 'to', 'grace', 'this', 'planet', 'but', 'is', 'he', 'guilty?', 'Well,', 'with', 'all', 'the', 'attention', "i've", 'gave', 'this', 'subject....hmmm', 'well', 'i', "don't", 'know', 'because', 'people', 'can', 'be', 'different', 'behind', 'closed', 'doors,', 'i', 'know', 'this', 'for', 'a', 'fact.', 'He', 'is', 'either', 'an', 'extremely', 'nice', 'but', 'stupid', 'guy', 'or', 'one', 'of', 'the', 'most', 'sickest', 'liars.', 'I', 'hope', 'he', 'is', 'not', 'the', 'latter."']
    단어갯수 =  [433, 158, 378, 379, 367, 89, 112, 132, 163, 43, 48, 172, 382, 130, 112, 187, 395, 456, 241, 118, 231, 274, 254, 43, 38, 141, 225, 254, 670, 123, 54, 116, 120, 328, 373, 284, 135, 115, 169, 542, 250, 140, 121, 174, 164, 115, 80, 134, 252, 194, 161, 97, 212, 140, 57, 139, 148, 170, 72, 379, 515, 226, 132, 137, 122, 55, 968, 73, 194, 129, 128, 425, 184, 185, 130, 146, 263, 92, 192, 138, 133, 273, 420, 191, 428, 294, 346, 51, 124, 110, 107, 117, 124, 136, 136, 141, 165, 73, 197, 84, 215, 869, 94, 165, 48, 107, 125, 121, 361, 423, 183, 208, 321, 69, 117, 227, 124, 156, 106, 127, 187, 365, 136, 274, 337, 804, 463, 325, 111, 214, 133, 618, 166, 569, 425, 26, 328, 177, 168, 136, 166, 272, 165, 156, 255, 184, 169, 281, 334, 113, 83, 179, 161, 313, 288, 97, 225, 351, 453, 167, 344, 219, 104, 141, 243, 132, 933, 136, 112, 153, 171, 216, 282, 143, 440, 133, 349, 130, 152, 222, 445, 418, 789, 126, 221, 138, 85, 395, 119, 135, 771, 106, 67, 157, 74, 278, 74, 276, 224, 102, 110, 241, 121, 272, 874, 215, 141, 249, 183, 126, 150, 575, 152, 98, 1000, 104, 341, 217, 172, 124, 129, 184, 609, 97, 141, 271, 467, 115, 363, 135, 492, 308, 139, 138, 118, 399, 151, 821, 149, 130, 182, 197, 89, 570, 164, 303, 53, 228, 133, 128, 215, 269, 148, 127, 160, 712, 251, 160, 214, 176, 525, 279, 138, 325, 158, 324, 536, 149, 171, 273, 497, 111, 115, 756, 178, 315, 392, 139, 196, 202, 449, 367, 150, 282, 78, 112, 435, 251, 145, 115, 191, 146, 114, 132, 84, 184, 151, 135, 281, 546, 227, 136, 129, 167, 261, 235, 697, 584, 369, 117, 192, 326, 754, 161, 59, 250, 197, 196, 312, 28, 137, 331, 102, 194, 199, 197, 114, 72, 59, 167, 177, 178, 174, 191, 280, 332, 145, 827, 362, 212, 69, 47, 108, 183, 292, 603, 252, 112, 134, 158, 44, 305, 118, 117, 156, 364, 32, 53, 115, 125, 141, 130, 355, 597, 148, 119, 301, 181, 194, 167, 123, 146, 117, 757, 427, 520, 141, 400, 156, 335, 198, 129, 83, 120, 189, 178, 242, 178, 34, 115, 116, 619, 155, 135, 388, 144, 142, 256, 123, 205, 83, 60, 252, 344, 58, 361, 151, 119, 148, 335, 464, 245, 117, 410, 139, 95, 332, 714, 278, 125, 231, 155, 210, 612, 181, 133, 158, 247, 43, 761, 824, 206, 99, 205, 244, 172, 166, 91, 156, 157, 717, 338, 156, 171, 146, 583, 146, 177, 253, 687, 214, 203, 103, 153, 931, 138, 45, 818, 261, 226, 144, 85, 414, 337, 219, 127, 264, 124, 165, 180, 222, 160, 162, 350, 272, 117, 163, 124, 385, 342, 70, 152, 409, 121, 92, 129, 41, 85, 291, 522, 428, 198, 345, 562, 466, 179, 883, 120, 90, 306, 149, 154, 141, 138, 164, 74, 201, 141, 372, 144, 288, 257, 34, 552, 308, 51, 142, 203, 90, 172, 132, 317, 120, 289, 352, 520, 151, 326, 178, 148, 720, 179, 442, 154, 113, 149, 131, 201, 132, 626, 128, 67, 423, 291, 75, 140, 64, 363, 142, 246, 593, 203, 190, 139, 132, 90, 193, 956, 122, 123, 255, 363, 580, 141, 282, 196, 361, 129, 106, 220, 98, 115, 207, 133, 161, 43, 78, 123, 399, 331, 94, 54, 462, 118, 505, 204, 410, 166, 50, 335, 128, 315, 233, 35, 268, 120, 121, 159, 407, 346, 368, 108, 778, 228, 384, 176, 167, 148, 392, 187, 124, 207, 137, 143, 258, 192, 523, 60, 133, 356, 121, 60, 194, 81, 465, 43, 224, 121, 189, 101, 241, 104, 280, 576, 242, 147, 161, 123, 564, 485, 215, 124, 233, 87, 145, 115, 377, 149, 97, 191, 171, 132, 395, 252, 229, 228, 396, 143, 59, 172, 136, 236, 235, 101, 117, 149, 494, 117, 213, 180, 127, 381, 100, 150, 293, 200, 213, 298, 151, 245, 149, 96, 158, 202, 432, 193, 71, 255, 49, 314, 160, 70, 51, 562, 277, 129, 220, 97, 223, 129, 543, 109, 287, 40, 65, 60, 351, 167, 156, 72, 207, 148, 461, 44, 166, 125, 301, 196, 129, 123, 456, 213, 111, 320, 128, 224, 147, 77, 149, 120, 421, 373, 101, 422, 236, 621, 118, 92, 758, 321, 452, 115, 143, 145, 588, 89, 151, 217, 158, 123, 53, 334, 327, 204, 170, 375, 121, 58, 137, 144, 265, 128, 248, 101, 117, 138, 504, 268, 142, 211, 105, 119, 151, 330, 162, 113, 53, 128, 218, 262, 282, 107, 125, 367, 169, 113, 155, 246, 195, 152, 220, 969, 128, 134, 132, 199, 143, 152, 130, 248, 150, 307, 321, 193, 312, 323, 353, 355, 88, 164, 307, 121, 204, 512, 164, 83, 101, 154, 348, 204, 177, 357, 214, 141, 284, 153, 91, 57, 899, 116, 455, 48, 118, 324, 145, 365, 351, 262, 138, 310, 184, 417, 211, 83, 220, 342, 54, 106, 226, 404, 104, 531, 55, 91, 211, 128, 86, 366, 244, 373, 411, 143, 134, 176, 134, 432, 99, 179, 143, 59, 165, 185, 277, 79, 174, 119, 113, 633, 179, 230, 146, 198, 342, 250, 333, 136, 209, 419, 134, 101, 580, 76, 117, 445, 60, 193, 135, 204, 123, 126, 137, 126, 150, 316, 198, 95, 929, 51, 288, 131, 199, 763, 198, 126, 153, 135, 161, 311, 237, 202, 236, 115, 98, 130, 139, 212, 353, 416, 139, 337, 273, 61, 225, 126, 591, 148, 128, 150, 399, 117, 156, 223, 211, 200, 361, 159, 191, 291, 175, 142, 264, 636, 137, 184, 125, 258, 655, 465, 178, 105, 174, 218, 582, 154, 238, 420, 575, 218, 317, 176, 118, 159, 121, 834, 251, 61, 516, 233, 155, 233, 325, 214, 299, 330, 194, 134, 183, 255, 287, 185, 367, 102, 232, 143, 99, 136, 202, 95, 576, 203, 139, 243, 146, 244, 328, 190, 219, 172, 510, 135, 203, 201, 129, 350, 235, 258, 459, 156, 185, 427, 177, 820, 51, 241, 500, 134, 342, 98, 53, 185, 298, 128, 216, 64, 117, 252, 120, 41, 326, 255, 506, 163, 151, 150, 259, 209, 189, 122, 127, 181, 118, 55, 127, 131, 186, 137, 171, 251, 552, 126, 213, 167, 248, 411, 203, 177, 85, 190, 66, 182, 163, 135, 78, 236, 140, 189, 172, 128, 264, 139, 139, 138, 116, 230, 164, 162, 75, 133, 213, 258, 389, 139, 602, 254, 33, 435, 90, 500, 128, 173, 235, 356, 109, 583, 176, 154, 860, 193, 220, 129, 206, 401, 294, 173, 152, 224, 137, 51, 207, 312, 273, 210, 191, 298, 135, 142, 129, 58, 139, 807, 194, 127, 387, 122, 233, 889, 144, 353, 177, 171, 249, 190, 370, 150, 125, 128, 122, 505, 288, 207, 219, 166, 967, 652, 454, 141, 130, 121, 135, 329, 63, 70, 407, 328, 156, 133, 524, 201, 278, 785, 148, 190, 427, 113, 84, 245, 128, 150, 158, 366, 815, 173, 526, 281, 27, 275, 122, 135, 398, 133, 164, 159, 569, 148, 682, 152, 65, 96, 182, 181, 131, 102, 25, 684, 238, 120, 115, 184, 150, 161, 125, 135, 166, 261, 296, 122, 622, 185, 518, 210, 246, 215, 297, 173, 196, 100, 213, 108, 129, 147, 165, 982, 148, 785, 117, 260, 120, 317, 343, 137, 462, 131, 99, 141, 224, 280, 155, 117, 101, 258, 182, 322, 133, 133, 198, 103, 532, 236, 52, 128, 206, 152, 261, 192, 374, 434, 264, 143, 111, 288, 135, 262, 129, 352, 841, 305, 215, 327, 393, 297, 77, 404, 192, 414, 423, 195, 44, 344, 237, 360, 306, 148, 830, 52, 422, 107, 130, 135, 82, 96, 240, 153, 315, 232, 722, 196, 177, 141, 350, 158, 161, 492, 180, 81, 376, 351, 173, 180, 162, 245, 232, 358, 132, 480, 342, 154, 125, 308, 188, 136, 59, 126, 206, 159, 77, 856, 164, 124, 124, 498, 298, 181, 911, 123, 248, 111, 132, 217, 161, 315, 89, 96, 326, 238, 82, 306, 123, 76, 160, 251, 467, 133, 133, 478, 105, 134, 124, 143, 287, 147, 59, 706, 206, 71, 124, 112, 85, 141, 216, 207, 99, 149, 154, 280, 118, 81, 250, 245, 75, 132, 542, 172, 109, 172, 444, 110, 53, 919, 163, 306, 279, 177, 414, 380, 124, 103, 248, 84, 106, 292, 524, 211, 390, 193, 146, 41, 131, 580, 88, 220, 794, 267, 207, 421, 316, 117, 83, 288, 357, 507, 125, 139, 116, 134, 146, 439, 155, 150, 262, 172, 178, 150, 97, 143, 191, 208, 128, 136, 196, 667, 155, 631, 269, 111, 166, 402, 187, 715, 143, 76, 70, 42, 82, 125, 191, 73, 169, 489, 122, 733, 693, 136, 126, 500, 377, 247, 262, 107, 162, 81, 361, 365, 110, 86, 138, 78, 476, 54, 103, 118, 247, 526, 189, 224, 372, 105, 194, 526, 140, 72, 63, 166, 320, 60, 152, 213, 673, 428, 187, 80, 126, 188, 146, 487, 79, 280, 418, 329, 334, 105, 608, 170, 179, 215, 198, 378, 526, 93, 112, 624, 207, 322, 91, 78, 130, 166, 144, 248, 479, 916, 119, 146, 99, 280, 192, 212, 129, 134, 136, 200, 184, 127, 346, 853, 558, 184, 94, 539, 138, 113, 148, 145, 98, 149, 52, 227, 293, 319, 136, 123, 137, 198, 226, 137, 138, 219, 117, 120, 349, 277, 396, 281, 223, 235, 394, 349, 162, 123, 244, 236, 125, 230, 179, 167, 122, 315, 58, 139, 140, 315, 330, 482, 167, 190, 514, 130, 243, 178, 356, 201, 246, 173, 65, 133, 220, 127, 123, 87, 157, 138, 888, 151, 155, 219, 403, 854, 203, 132, 487, 437, 57, 193, 91, 103, 296, 338, 825, 481, 223, 166, 422, 147, 611, 397, 181, 175, 593, 503, 227, 476, 208, 176, 308, 167, 119, 57, 319, 82, 339, 436, 224, 221, 346, 716, 173, 60, 279, 149, 128, 92, 370, 139, 272, 364, 157, 89, 142, 125, 168, 281, 101, 82, 269, 107, 62, 330, 99, 429, 363, 152, 230, 157, 203, 279, 99, 150, 212, 374, 190, 207, 218, 63, 615, 321, 60, 58, 680, 283, 149, 281, 554, 231, 84, 115, 219, 49, 201, 429, 746, 515, 301, 46, 756, 105, 184, 599, 79, 939, 55, 557, 397, 426, 232, 213, 266, 355, 156, 69, 436, 158, 135, 161, 813, 178, 269, 470, 140, 713, 135, 236, 187, 137, 293, 291, 158, 436, 213, 149, 125, 352, 339, 82, 108, 726, 388, 131, 154, 199, 78, 196, 169, 132, 123, 306, 80, 151, 280, 119, 247, 196, 187, 103, 150, 230, 97, 121, 150, 55, 456, 232, 133, 90, 57, 146, 174, 36, 130, 146, 287, 206, 154, 214, 153, 221, 184, 155, 163, 456, 112, 325, 223, 34, 87, 263, 110, 128, 248, 513, 474, 571, 135, 156, 145, 278, 460, 134, 62, 157, 121, 333, 43, 124, 265, 131, 132, 237, 74, 325, 117, 183, 170, 330, 159, 104, 109, 242, 354, 300, 559, 68, 137, 535, 123, 200, 491, 95, 910, 131, 130, 57, 143, 135, 578, 254, 190, 189, 449, 471, 122, 429, 390, 410, 115, 148, 172, 79, 248, 194, 123, 115, 263, 81, 118, 144, 303, 89, 43, 136, 147, 707, 234, 249, 55, 191, 124, 127, 208, 266, 586, 690, 119, 262, 193, 169, 257, 116, 266, 122, 228, 441, 122, 258, 119, 237, 118, 64, 197, 381, 151, 132, 214, 262, 215, 222, 135, 280, 381, 313, 132, 181, 342, 261, 117, 102, 724, 93, 152, 187, 129, 122, 153, 439, 180, 109, 243, 166, 135, 966, 149, 148, 112, 97, 766, 121, 162, 126, 89, 119, 649, 146, 104, 97, 223, 133, 138, 332, 150, 486, 601, 813, 127, 93, 121, 183, 204, 125, 235, 127, 137, 129, 197, 158, 230, 82, 117, 174, 145, 392, 175, 526, 135, 213, 114, 320, 122, 117, 118, 883, 141, 134, 187, 252, 130, 118, 108, 242, 68, 127, 241, 174, 197, 383, 152, 226, 334, 215, 110, 182, 211, 590, 175, 188, 141, 137, 157, 327, 328, 283, 139, 127, 310, 248, 554, 94, 150, 109, 252, 484, 225, 78, 68, 269, 668, 150, 177, 227, 132, 140, 170, 109, 133, 163, 92, 234, 154, 109, 321, 139, 133, 120, 790, 231, 99, 99, 167, 154, 173, 169, 133, 619, 131, 166, 156, 123, 227, 138, 159, 254, 217, 246, 164, 388, 278, 229, 171, 414, 247, 79, 651, 283, 128, 132, 331, 138, 443, 561, 146, 106, 194, 123, 139, 102, 33, 245, 119, 120, 230, 283, 136, 67, 150, 699, 164, 410, 536, 130, 90, 47, 301, 252, 171, 344, 152, 184, 303, 147, 896, 243, 514, 165, 77, 115, 170, 55, 186, 121, 154, 227, 141, 570, 157, 134, 143, 560, 199, 155, 157, 208, 146, 140, 275, 65, 349, 90, 885, 34, 377, 110, 144, 88, 132, 376, 75, 115, 120, 88, 269, 272, 56, 187, 231, 270, 126, 43, 168, 68, 190, 197, 49, 212, 146, 550, 196, 153, 196, 132, 147, 939, 234, 363, 146, 157, 160, 210, 823, 240, 979, 203, 103, 157, 296, 141, 376, 245, 115, 104, 131, 1296, 496, 277, 634, 700, 56, 93, 251, 779, 50, 213, 252, 351, 403, 95, 101, 182, 145, 70, 103, 622, 124, 512, 248, 138, 117, 119, 163, 291, 370, 147, 159, 140, 115, 120, 158, 165, 77, 715, 771, 189, 167, 61, 211, 133, 635, 138, 189, 466, 162, 234, 146, 138, 169, 264, 244, 306, 167, 56, 140, 128, 81, 106, 86, 49, 455, 163, 73, 131, 174, 117, 253, 119, 297, 429, 176, 244, 82, 514, 374, 192, 128, 375, 605, 123, 784, 237, 633, 115, 114, 440, 428, 25, 108, 398, 70, 821, 390, 174, 92, 134, 139, 155, 75, 318, 202, 233, 179, 567, 450, 190, 283, 650, 152, 246, 269, 197, 385, 458, 443, 123, 178, 122, 250, 54, 342, 313, 155, 146, 103, 177, 200, 247, 46, 149, 318, 569, 308, 175, 762, 320, 113, 114, 511, 160, 124, 181, 87, 129, 383, 288, 138, 140, 429, 118, 113, 173, 314, 194, 298, 95, 339, 177, 278, 140, 160, 198, 756, 341, 220, 109, 404, 217, 443, 515, 120, 802, 56, 117, 348, 348, 131, 138, 705, 132, 125, 241, 534, 35, 287, 313, 400, 401, 538, 144, 104, 302, 107, 139, 262, 155, 119, 124, 91, 251, 131, 200, 77, 476, 148, 225, 249, 109, 287, 364, 75, 53, 131, 414, 487, 152, 126, 157, 62, 302, 373, 130, 148, 171, 174, 136, 194, 160, 169, 226, 191, 119, 56, 233, 171, 217, 173, 217, 201, 64, 475, 46, 836, 176, 208, 152, 138, 184, 467, 116, 246, 386, 193, 185, 198, 438, 587, 95, 86, 351, 138, 283, 188, 79, 113, 765, 214, 163, 128, 49, 126, 375, 110, 99, 621, 137, 142, 503, 355, 195, 141, 278, 78, 225, 121, 370, 115, 183, 244, 164, 226, 302, 101, 113, 406, 211, 152, 316, 138, 148, 84, 195, 90, 634, 277, 127, 239, 216, 134, 311, 308, 495, 632, 142, 299, 56, 122, 619, 312, 99, 332, 131, 548, 181, 340, 112, 235, 51, 115, 114, 276, 228, 42, 168, 124, 111, 459, 128, 356, 90, 358, 298, 271, 133, 112, 190, 44, 223, 199, 136, 147, 227, 342, 141, 309, 500, 177, 146, 47, 121, 115, 174, 57, 218, 410, 365, 313, 158, 307, 96, 196, 123, 116, 289, 174, 209, 274, 353, 561, 170, 127, 145, 679, 127, 286, 129, 221, 94, 160, 245, 85, 508, 64, 69, 180, 145, 329, 112, 124, 736, 201, 252, 120, 151, 255, 120, 168, 121, 100, 120, 97, 105, 114, 307, 132, 358, 130, 113, 66, 59, 970, 106, 252, 121, 365, 120, 168, 196, 126, 294, 572, 83, 404, 442, 208, 44, 377, 241, 164, 142, 119, 161, 504, 151, 279, 127, 198, 49, 442, 427, 187, 468, 115, 264, 181, 139, 100, 111, 251, 52, 146, 180, 77, 104, 916, 312, 140, 351, 234, 108, 206, 117, 334, 186, 214, 138, 135, 283, 269, 291, 126, 55, 40, 178, 119, 239, 222, 210, 139, 121, 236, 174, 98, 135, 213, 175, 359, 198, 243, 362, 114, 311, 382, 460, 122, 177, 124, 77, 144, 193, 119, 146, 370, 523, 114, 161, 366, 60, 733, 217, 161, 164, 144, 140, 215, 308, 178, 154, 130, 105, 165, 124, 201, 133, 334, 338, 731, 84, 347, 153, 163, 154, 451, 320, 52, 565, 96, 49, 180, 93, 199, 369, 587, 310, 134, 191, 376, 592, 55, 450, 337, 66, 196, 95, 197, 130, 136, 162, 129, 328, 144, 171, 480, 123, 324, 241, 52, 243, 645, 142, 121, 188, 286, 159, 184, 151, 199, 357, 122, 138, 146, 76, 246, 163, 220, 183, 458, 112, 217, 136, 132, 146, 139, 99, 135, 121, 257, 240, 81, 458, 470, 129, 142, 234, 299, 423, 334, 937, 433, 164, 118, 757, 134, 147, 187, 520, 181, 283, 123, 164, 532, 664, 253, 497, 303, 88, 189, 120, 180, 419, 108, 85, 217, 120, 172, 128, 97, 221, 815, 961, 131, 220, 161, 369, 713, 140, 132, 198, 238, 94, 108, 180, 112, 245, 324, 180, 140, 510, 89, 44, 231, 184, 659, 197, 99, 348, 41, 202, 81, 135, 150, 164, 204, 163, 149, 155, 689, 40, 116, 231, 112, 108, 203, 81, 108, 469, 246, 253, 146, 332, 122, 320, 311, 135, 341, 197, 190, 230, 444, 179, 126, 134, 161, 123, 163, 219, 435, 120, 303, 148, 290, 88, 265, 184, 382, 216, 112, 606, 416, 44, 234, 139, 370, 121, 143, 231, 825, 129, 302, 124, 147, 289, 299, 347, 123, 139, 110, 116, 287, 76, 123, 110, 1012, 191, 162, 150, 184, 586, 124, 201, 630, 143, 250, 491, 284, 212, 115, 53, 201, 186, 46, 151, 212, 251, 287, 370, 134, 222, 69, 560, 138, 221, 412, 145, 75, 394, 275, 271, 214, 118, 192, 169, 189, 305, 494, 982, 33, 152, 468, 151, 71, 125, 128, 209, 727, 127, 118, 113, 200, 201, 77, 167, 226, 201, 141, 54, 77, 171, 155, 117, 199, 311, 126, 599, 126, 110, 150, 244, 163, 116, 91, 141, 170, 112, 149, 193, 284, 157, 55, 592, 197, 186, 329, 293, 539, 140, 567, 163, 233, 153, 397, 657, 160, 193, 181, 562, 225, 89, 355, 376, 119, 116, 178, 145, 115, 213, 37, 175, 211, 181, 135, 287, 200, 233, 821, 97, 140, 219, 128, 131, 183, 436, 107, 338, 113, 94, 141, 346, 96, 188, 297, 112, 245, 140, 315, 346, 270, 655, 247, 109, 130, 205, 444, 501, 379, 308, 530, 586, 234, 409, 420, 137, 61, 145, 105, 150, 82, 484, 201, 122, 177, 110, 305, 590, 95, 595, 120, 115, 95, 200, 56, 621, 170, 154, 167, 95, 138, 136, 221, 140, 257, 85, 191, 170, 309, 285, 131, 100, 977, 283, 107, 101, 429, 468, 159, 232, 370, 536, 126, 76, 324, 187, 116, 122, 122, 48, 233, 593, 200, 217, 319, 106, 223, 153, 173, 1263, 267, 147, 946, 278, 397, 299, 194, 122, 312, 197, 64, 608, 148, 132, 190, 180, 152, 113, 182, 121, 122, 181, 69, 206, 129, 274, 167, 174, 155, 159, 117, 157, 178, 162, 352, 469, 187, 335, 273, 637, 436, 124, 141, 241, 50, 120, 340, 159, 565, 187, 441, 226, 112, 243, 301, 451, 209, 393, 260, 261, 122, 102, 102, 43, 90, 104, 114, 471, 283, 367, 140, 246, 287, 127, 138, 130, 292, 121, 392, 321, 208, 143, 142, 121, 141, 185, 67, 191, 122, 173, 275, 384, 103, 63, 101, 137, 125, 191, 262, 246, 997, 112, 226, 172, 216, 136, 114, 420, 152, 222, 134, 137, 186, 265, 149, 81, 256, 358, 333, 151, 279, 140, 141, 335, 340, 383, 149, 170, 418, 333, 969, 242, 67, 215, 238, 175, 247, 142, 189, 230, 69, 141, 102, 507, 218, 276, 183, 176, 431, 816, 293, 468, 509, 349, 101, 170, 504, 124, 158, 118, 125, 100, 367, 46, 153, 416, 755, 306, 381, 116, 628, 129, 132, 300, 106, 543, 156, 139, 114, 300, 228, 539, 285, 808, 167, 322, 307, 133, 165, 54, 440, 129, 189, 129, 267, 179, 467, 852, 125, 112, 403, 63, 658, 166, 301, 247, 598, 133, 310, 140, 231, 288, 117, 335, 135, 672, 189, 160, 121, 120, 71, 163, 256, 118, 197, 92, 712, 579, 162, 298, 733, 214, 175, 58, 186, 383, 252, 56, 226, 105, 290, 196, 148, 506, 193, 108, 157, 506, 116, 101, 167, 144, 86, 351, 165, 115, 318, 575, 118, 857, 236, 129, 230, 379, 186, 288, 134, 234, 223, 130, 146, 302, 94, 230, 137, 586, 243, 204, 102, 114, 254, 38, 151, 314, 131, 864, 164, 113, 262, 233, 298, 620, 67, 206, 168, 133, 90, 2470, 187, 235, 145, 162, 437, 219, 227, 215, 572, 142, 204, 350, 138, 140, 62, 149, 153, 60, 878, 558, 31, 158, 146, 216, 254, 993, 130, 238, 479, 124, 127, 482, 340, 341, 169, 356, 117, 241, 203, 127, 268, 142, 203, 67, 304, 207, 130, 122, 137, 172, 114, 131, 145, 168, 82, 301, 136, 177, 232, 349, 123, 484, 99, 320, 205, 286, 272, 733, 61, 114, 196, 177, 166, 94, 414, 152, 145, 154, 236, 131, 126, 110, 85, 532, 161, 664, 246, 246, 161, 209, 84, 406, 281, 111, 244, 755, 116, 201, 294, 508, 154, 142, 553, 424, 159, 308, 119, 240, 155, 115, 936, 159, 97, 147, 217, 215, 264, 399, 339, 81, 158, 334, 108, 146, 229, 401, 269, 60, 320, 125, 117, 71, 361, 144, 384, 129, 66, 130, 135, 584, 507, 56, 358, 44, 124, 83, 128, 103, 340, 320, 128, 223, 79, 258, 303, 143, 144, 119, 88, 565, 138, 470, 205, 40, 189, 1021, 693, 120, 101, 309, 67, 80, 142, 331, 115, 216, 302, 366, 480, 192, 129, 166, 229, 157, 151, 140, 142, 121, 259, 102, 141, 753, 272, 240, 184, 128, 146, 177, 275, 172, 274, 143, 445, 152, 152, 164, 165, 1000, 228, 502, 94, 159, 135, 607, 302, 149, 339, 134, 127, 66, 219, 125, 31, 617, 309, 134, 190, 167, 186, 169, 357, 612, 174, 167, 145, 204, 174, 151, 328, 53, 210, 74, 129, 130, 133, 404, 139, 83, 110, 156, 483, 341, 710, 144, 993, 129, 211, 221, 121, 151, 438, 333, 247, 219, 342, 243, 543, 110, 543, 552, 484, 97, 43, 150, 351, 118, 181, 164, 381, 405, 174, 204, 231, 19, 276, 171, 365, 250, 43, 181, 189, 202, 207, 186, 157, 82, 156, 387, 250, 149, 100, 277, 159, 170, 135, 870, 492, 294, 169, 60, 225, 365, 247, 675, 197, 181, 354, 173, 245, 146, 240, 157, 51, 134, 374, 154, 124, 116, 123, 162, 158, 183, 975, 356, 151, 47, 185, 119, 157, 130, 455, 71, 277, 156, 152, 116, 296, 117, 50, 233, 548, 60, 384, 510, 226, 186, 235, 205, 230, 220, 202, 217, 331, 124, 497, 64, 128, 50, 204, 136, 108, 498, 327, 581, 119, 515, 668, 384, 89, 282, 451, 260, 198, 194, 128, 421, 154, 62, 225, 976, 363, 138, 58, 297, 265, 70, 124, 71, 148, 290, 181, 108, 215, 111, 69, 281, 265, 234, 107, 218, 166, 202, 357, 122, 165, 158, 254, 135, 102, 158, 212, 120, 157, 117, 468, 286, 64, 216, 502, 262, 118, 234, 207, 403, 144, 259, 127, 264, 119, 135, 509, 126, 127, 261, 172, 263, 184, 209, 531, 609, 211, 125, 79, 115, 138, 595, 113, 122, 181, 188, 264, 629, 178, 190, 106, 197, 123, 263, 785, 301, 467, 404, 161, 136, 62, 58, 147, 140, 176, 802, 409, 78, 149, 166, 306, 399, 134, 570, 138, 409, 113, 358, 290, 91, 274, 45, 201, 360, 716, 479, 121, 211, 269, 198, 145, 144, 125, 169, 116, 176, 334, 116, 724, 355, 138, 99, 166, 117, 307, 304, 216, 273, 126, 129, 224, 271, 204, 805, 300, 313, 34, 133, 253, 121, 130, 809, 133, 799, 208, 127, 193, 288, 102, 336, 388, 301, 178, 188, 90, 154, 348, 65, 108, 185, 277, 309, 146, 165, 208, 441, 163, 286, 12, 201, 136, 287, 56, 487, 239, 268, 146, 49, 326, 143, 97, 327, 187, 139, 83, 185, 134, 266, 164, 213, 215, 155, 136, 113, 132, 336, 30, 203, 165, 423, 113, 123, 109, 241, 476, 78, 119, 180, 119, 149, 222, 151, 510, 130, 255, 231, 142, 134, 152, 143, 169, 142, 144, 60, 80, 150, 234, 227, 305, 127, 467, 219, 255, 101, 613, 173, 396, 117, 209, 126, 477, 146, 210, 330, 84, 354, 299, 123, 136, 60, 345, 171, 108, 253, 71, 573, 352, 414, 369, 187, 220, 192, 390, 158, 352, 186, 436, 187, 433, 451, 76, 117, 58, 138, 141, 119, 160, 127, 146, 351, 359, 122, 581, 111, 149, 339, 57, 221, 197, 327, 168, 42, 195, 122, 275, 96, 180, 97, 57, 633, 436, 28, 220, 456, 266, 377, 116, 687, 686, 374, 288, 227, 425, 61, 188, 126, 263, 108, 178, 121, 150, 388, 775, 423, 132, 136, 243, 137, 552, 196, 130, 112, 175, 402, 133, 137, 61, 248, 62, 92, 166, 122, 44, 350, 486, 746, 422, 411, 149, 89, 122, 128, 163, 1601, 154, 194, 945, 78, 425, 218, 222, 443, 503, 129, 324, 273, 143, 160, 172, 107, 385, 531, 503, 200, 59, 149, 206, 131, 85, 315, 249, 142, 165, 135, 121, 152, 131, 150, 170, 185, 40, 236, 99, 124, 140, 153, 103, 177, 340, 504, 266, 165, 116, 158, 211, 258, 620, 239, 118, 555, 129, 335, 340, 186, 446, 183, 150, 169, 371, 283, 340, 176, 172, 321, 117, 581, 300, 559, 60, 52, 168, 330, 222, 62, 87, 78, 632, 335, 90, 670, 919, 131, 405, 133, 114, 623, 360, 445, 51, 415, 215, 142, 90, 126, 132, 76, 36, 118, 79, 478, 135, 108, 307, 264, 168, 146, 209, 133, 385, 129, 195, 149, 158, 232, 251, 284, 529, 338, 418, 145, 120, 76, 120, 119, 208, 234, 164, 49, 123, 310, 117, 50, 230, 121, 155, 47, 133, 158, 47, 417, 176, 199, 137, 210, 382, 273, 154, 140, 189, 112, 128, 960, 945, 588, 217, 195, 341, 217, 556, 136, 311, 425, 68, 253, 125, 1002, 591, 86, 203, 119, 111, 161, 186, 122, 134, 497, 118, 315, 801, 119, 228, 193, 331, 146, 368, 137, 155, 140, 171, 134, 262, 154, 326, 162, 51, 92, 52, 148, 110, 152, 150, 357, 321, 111, 160, 619, 293, 137, 78, 251, 187, 181, 133, 147, 127, 177, 250, 79, 988, 123, 908, 112, 119, 737, 476, 253, 241, 119, 155, 246, 99, 215, 219, 166, 361, 47, 207, 170, 190, 194, 401, 173, 120, 154, 577, 173, 106, 260, 163, 187, 334, 118, 641, 150, 278, 250, 200, 372, 58, 71, 349, 475, 136, 127, 125, 164, 113, 183, 472, 124, 113, 129, 181, 195, 179, 147, 67, 142, 147, 533, 324, 108, 590, 169, 122, 317, 155, 234, 93, 59, 149, 168, 178, 147, 458, 366, 237, 133, 205, 151, 68, 173, 79, 296, 221, 116, 398, 756, 293, 297, 171, 425, 181, 242, 316, 109, 85, 151, 144, 84, 156, 74, 216, 311, 98, 223, 305, 134, 654, 74, 171, 494, 196, 129, 137, 543, 192, 311, 159, 98, 68, 169, 437, 69, 267, 307, 300, 216, 208, 134, 484, 174, 755, 132, 118, 279, 261, 287, 138, 143, 175, 261, 119, 165, 80, 243, 232, 152, 303, 212, 181, 290, 148, 255, 162, 167, 157, 199, 323, 240, 182, 129, 407, 189, 123, 214, 240, 119, 118, 188, 107, 215, 120, 250, 170, 525, 76, 246, 131, 225, 180, 157, 688, 89, 387, 97, 338, 360, 241, 128, 698, 437, 337, 119, 75, 589, 127, 156, 157, 140, 234, 693, 196, 566, 239, 295, 250, 127, 64, 145, 110, 306, 181, 251, 400, 202, 173, 41, 134, 204, 128, 129, 69, 111, 263, 362, 150, 117, 162, 148, 146, 100, 345, 313, 77, 305, 224, 614, 141, 196, 225, 236, 385, 141, 98, 329, 37, 267, 112, 528, 152, 121, 205, 370, 96, 138, 140, 370, 156, 154, 331, 206, 468, 54, 140, 239, 107, 157, 136, 261, 265, 138, 147, 467, 80, 143, 656, 121, 138, 413, 813, 535, 471, 664, 459, 494, 143, 259, 191, 139, 161, 142, 171, 119, 70, 166, 147, 618, 165, 151, 113, 126, 246, 156, 146, 190, 388, 75, 165, 232, 172, 230, 238, 177, 127, 522, 337, 257, 125, 75, 116, 211, 308, 131, 412, 519, 82, 474, 125, 163, 79, 207, 56, 95, 365, 710, 273, 182, 133, 92, 270, 156, 355, 229, 169, 253, 144, 129, 187, 134, 109, 130, 144, 328, 177, 172, 194, 197, 149, 119, 76, 137, 174, 670, 212, 363, 669, 140, 123, 111, 125, 55, 196, 151, 859, 69, 51, 1000, 541, 210, 55, 499, 153, 269, 385, 117, 106, 347, 480, 978, 214, 131, 141, 499, 230, 152, 107, 248, 890, 486, 279, 95, 123, 185, 162, 930, 133, 171, 299, 125, 365, 158, 215, 165, 108, 137, 306, 85, 290, 638, 59, 399, 127, 1000, 116, 145, 137, 264, 179, 120, 226, 573, 232, 176, 192, 353, 73, 74, 237, 131, 160, 161, 75, 111, 258, 60, 145, 252, 210, 347, 158, 309, 373, 170, 147, 155, 195, 553, 127, 270, 264, 152, 323, 410, 132, 136, 143, 153, 213, 215, 219, 288, 70, 1000, 268, 793, 147, 83, 218, 164, 110, 147, 267, 337, 175, 341, 554, 153, 98, 80, 48, 236, 146, 148, 110, 145, 159, 151, 120, 83, 400, 143, 371, 214, 238, 111, 152, 114, 342, 100, 403, 418, 197, 289, 408, 183, 146, 229, 527, 167, 199, 119, 266, 78, 98, 601, 348, 177, 66, 226, 127, 294, 229, 108, 113, 169, 119, 130, 88, 137, 264, 42, 79, 357, 165, 133, 128, 165, 76, 262, 942, 150, 66, 148, 276, 431, 58, 267, 530, 131, 306, 217, 394, 825, 182, 117, 143, 187, 221, 224, 246, 394, 190, 346, 318, 461, 113, 184, 402, 674, 124, 314, 204, 471, 153, 197, 272, 317, 237, 188, 154, 262, 87, 184, 114, 228, 380, 160, 149, 157, 103, 182, 224, 163, 192, 685, 122, 150, 397, 118, 207, 131, 312, 518, 185, 211, 361, 147, 309, 149, 157, 596, 311, 992, 136, 122, 151, 359, 296, 480, 329, 174, 164, 94, 188, 218, 80, 120, 213, 126, 194, 292, 256, 359, 218, 527, 70, 66, 146, 98, 137, 170, 59, 126, 632, 161, 250, 116, 169, 165, 435, 180, 1196, 287, 335, 102, 146, 135, 337, 93, 200, 329, 189, 135, 242, 323, 891, 192, 474, 134, 143, 141, 127, 76, 371, 283, 127, 131, 157, 179, 431, 397, 287, 990, 108, 174, 42, 389, 218, 171, 248, 221, 187, 118, 219, 146, 110, 229, 149, 265, 177, 260, 440, 526, 222, 308, 68, 228, 679, 134, 123, 49, 388, 116, 251, 73, 184, 105, 226, 136, 194, 128, 215, 146, 152, 131, 199, 741, 178, 495, 149, 136, 136, 385, 60, 80, 205, 231, 71, 375, 342, 225, 305, 143, 101, 165, 44, 495, 106, 187, 181, 342, 457, 267, 570, 165, 131, 138, 119, 155, 409, 115, 212, 166, 148, 142, 137, 251, 338, 298, 186, 489, 414, 78, 144, 72, 283, 136, 957, 409, 436, 321, 374, 75, 175, 186, 688, 127, 324, 133, 133, 114, 104, 252, 151, 312, 126, 551, 227, 162, 126, 314, 144, 145, 193, 138, 57, 479, 133, 116, 265, 375, 447, 88, 358, 132, 138, 118, 193, 134, 644, 155, 392, 177, 115, 175, 350, 138, 287, 137, 289, 199, 205, 437, 501, 406, 176, 446, 121, 205, 268, 234, 159, 151, 230, 261, 160, 162, 137, 265, 832, 83, 136, 58, 107, 120, 246, 175, 314, 619, 128, 458, 139, 322, 121, 159, 379, 202, 140, 83, 135, 126, 498, 150, 236, 25, 186, 147, 297, 71, 226, 651, 175, 158, 130, 171, 634, 161, 105, 535, 195, 411, 186, 114, 43, 71, 338, 187, 225, 119, 117, 69, 37, 181, 323, 366, 695, 268, 504, 69, 238, 198, 226, 134, 389, 58, 706, 253, 130, 117, 211, 34, 52, 127, 151, 189, 278, 249, 128, 126, 449, 391, 369, 390, 154, 178, 64, 242, 263, 970, 140, 563, 170, 490, 433, 133, 324, 670, 145, 652, 231, 185, 111, 216, 341, 217, 519, 299, 418, 369, 143, 140, 219, 145, 115, 343, 119, 145, 186, 140, 238, 118, 836, 122, 113, 120, 574, 83, 167, 111, 342, 164, 561, 396, 176, 409, 76, 140, 120, 187, 161, 146, 130, 190, 105, 191, 133, 137, 116, 135, 190, 137, 149, 34, 170, 172, 43, 81, 64, 169, 168, 184, 137, 156, 233, 144, 460, 130, 364, 50, 81, 337, 174, 155, 242, 468, 160, 57, 123, 225, 125, 150, 142, 174, 119, 117, 62, 617, 140, 243, 153, 127, 419, 369, 111, 164, 201, 178, 57, 163, 323, 167, 785, 72, 573, 129, 229, 215, 536, 296, 333, 551, 107, 113, 159, 133, 115, 141, 1001, 266, 355, 212, 130, 110, 362, 176, 577, 235, 202, 134, 204, 107, 109, 124, 370, 114, 67, 177, 515, 179, 108, 117, 113, 291, 414, 212, 700, 147, 131, 329, 72, 568, 328, 126, 47, 998, 111, 234, 105, 141, 367, 121, 293, 131, 241, 240, 228, 135, 152, 53, 141, 44, 163, 130, 170, 135, 302, 131, 604, 145, 116, 129, 112, 241, 261, 120, 141, 497, 181, 517, 139, 221, 570, 139, 173, 322, 390, 183, 169, 116, 146, 123, 211, 82, 149, 135, 193, 62, 236, 166, 90, 128, 94, 131, 859, 168, 591, 73, 398, 310, 243, 224, 157, 117, 144, 377, 171, 132, 63, 145, 205, 147, 83, 51, 140, 124, 233, 191, 131, 165, 107, 164, 158, 38, 285, 103, 99, 637, 168, 124, 136, 384, 1074, 60, 216, 129, 203, 118, 178, 154, 116, 88, 759, 70, 183, 374, 138, 319, 269, 67, 40, 177, 32, 378, 197, 82, 147, 169, 184, 146, 258, 147, 383, 153, 259, 167, 217, 211, 387, 397, 226, 125, 231, 115, 262, 278, 567, 305, 94, 258, 71, 63, 78, 117, 316, 215, 370, 235, 226, 223, 989, 45, 197, 292, 236, 722, 278, 217, 209, 793, 334, 1013, 197, 152, 128, 57, 201, 379, 126, 174, 673, 207, 85, 303, 135, 202, 146, 300, 42, 405, 384, 214, 144, 209, 174, 167, 43, 142, 203, 83, 268, 141, 194, 219, 198, 179, 596, 355, 143, 147, 453, 133, 99, 161, 121, 176, 123, 272, 455, 57, 60, 239, 155, 98, 411, 103, 119, 312, 306, 270, 147, 275, 138, 184, 169, 276, 403, 69, 161, 112, 170, 287, 216, 129, 124, 155, 111, 487, 461, 251, 133, 247, 114, 427, 126, 229, 131, 177, 244, 89, 137, 145, 436, 304, 114, 134, 105, 151, 195, 223, 372, 325, 115, 149, 118, 203, 62, 380, 220, 125, 77, 123, 42, 116, 232, 150, 247, 181, 149, 183, 116, 194, 430, 107, 401, 150, 150, 266, 421, 41, 137, 546, 176, 162, 150, 224, 199, 191, 149, 154, 360, 51, 277, 118, 225, 211, 171, 132, 164, 239, 230, 128, 149, 215, 129, 302, 287, 126, 97, 118, 178, 149, 95, 388, 166, 115, 250, 109, 56, 257, 142, 131, 244, 190, 372, 86, 158, 139, 296, 120, 94, 139, 411, 84, 175, 72, 128, 176, 133, 238, 84, 116, 139, 208, 159, 283, 199, 236, 116, 121, 71, 127, 245, 420, 214, 129, 148, 246, 311, 154, 135, 123, 418, 180, 46, 144, 185, 242, 41, 110, 138, 78, 371, 338, 134, 493, 947, 100, 115, 376, 95, 180, 126, 120, 330, 80, 412, 124, 53, 581, 410, 76, 244, 237, 92, 187, 140, 407, 203, 680, 114, 213, 145, 176, 136, 94, 127, 166, 465, 64, 507, 230, 154, 128, 266, 174, 69, 167, 336, 243, 171, 111, 205, 42, 139, 338, 129, 169, 327, 202, 187, 132, 253, 274, 550, 170, 347, 359, 227, 60, 229, 151, 118, 126, 677, 115, 403, 131, 132, 403, 163, 42, 261, 124, 248, 100, 238, 38, 192, 721, 163, 194, 42, 283, 129, 63, 52, 179, 310, 481, 491, 199, 221, 142, 180, 267, 354, 665, 443, 550, 169, 545, 116, 157, 146, 98, 143, 140, 105, 124, 245, 70, 114, 160, 100, 218, 183, 135, 119, 56, 127, 228, 429, 79, 188, 866, 118, 421, 101, 118, 487, 107, 161, 626, 124, 214, 86, 133, 129, 254, 551, 618, 102, 246, 243, 144, 214, 266, 148, 477, 141, 229, 215, 316, 325, 181, 144, 136, 241, 50, 247, 132, 105, 150, 293, 119, 384, 148, 141, 229, 48, 375, 128, 142, 168, 162, 80, 79, 136, 601, 317, 133, 70, 209, 319, 60, 422, 250, 124, 524, 192, 295, 235, 140, 659, 215, 106, 496, 109, 150, 103, 716, 64, 169, 83, 227, 273, 322, 137, 270, 276, 84, 314, 139, 146, 67, 294, 70, 126, 199, 222, 540, 231, 128, 209, 261, 210, 401, 214, 209, 63, 110, 231, 221, 449, 513, 358, 114, 171, 163, 254, 52, 171, 174, 67, 72, 168, 462, 75, 364, 180, 139, 201, 224, 618, 376, 152, 290, 178, 295, 180, 270, 217, 287, 155, 133, 113, 490, 152, 177, 268, 222, 324, 138, 570, 183, 128, 220, 751, 174, 196, 190, 585, 672, 426, 170, 151, 174, 104, 145, 125, 53, 238, 232, 389, 993, 421, 142, 90, 153, 150, 150, 162, 175, 164, 138, 158, 110, 246, 133, 95, 274, 363, 470, 49, 134, 122, 254, 219, 292, 146, 139, 178, 269, 131, 227, 216, 195, 273, 174, 110, 155, 236, 214, 169, 128, 56, 560, 115, 112, 169, 252, 62, 197, 125, 146, 156, 129, 147, 151, 427, 231, 669, 117, 356, 928, 692, 110, 124, 204, 558, 129, 172, 135, 157, 129, 67, 163, 561, 524, 110, 179, 697, 128, 154, 84, 285, 335, 196, 55, 286, 75, 271, 452, 117, 156, 208, 198, 515, 140, 289, 181, 485, 282, 58, 183, 118, 117, 81, 176, 199, 249, 735, 264, 169, 729, 548, 154, 143, 151, 129, 110, 529, 375, 195, 109, 537, 112, 787, 443, 207, 95, 122, 58, 130, 231, 211, 852, 191, 450, 341, 146, 294, 178, 118, 182, 821, 435, 70, 162, 136, 196, 140, 127, 156, 148, 110, 235, 175, 141, 173, 708, 320, 162, 102, 112, 147, 76, 589, 151, 243, 138, 49, 96, 323, 44, 69, 594, 129, 238, 129, 135, 120, 152, 32, 132, 125, 751, 123, 273, 132, 191, 157, 160, 187, 366, 140, 180, 131, 159, 327, 359, 412, 125, 233, 221, 160, 123, 123, 104, 232, 101, 256, 572, 216, 365, 130, 138, 191, 331, 179, 141, 516, 443, 188, 585, 768, 242, 477, 421, 287, 147, 545, 213, 118, 79, 170, 283, 120, 105, 51, 53, 373, 199, 132, 171, 73, 147, 320, 96, 184, 126, 372, 146, 123, 400, 403, 699, 92, 213, 127, 142, 89, 141, 162, 548, 121, 318, 122, 131, 250, 159, 616, 100, 178, 317, 153, 137, 76, 551, 351, 186, 148, 71, 72, 291, 617, 703, 170, 200, 218, 204, 201, 161, 171, 115, 163, 183, 199, 310, 789, 889, 144, 194, 264, 131, 41, 152, 582, 483, 280, 156, 441, 162, 155, 63, 109, 125, 392, 79, 108, 115, 177, 162, 95, 119, 274, 122, 345, 305, 110, 175, 134, 501, 577, 242, 190, 105, 232, 159, 141, 128, 288, 141, 127, 191, 342, 245, 256, 128, 214, 61, 437, 113, 170, 170, 65, 177, 53, 332, 241, 403, 276, 48, 206, 137, 106, 158, 113, 908, 306, 624, 222, 144, 147, 187, 1316, 228, 159, 999, 122, 136, 202, 152, 113, 162, 109, 419, 33, 92, 196, 168, 183, 240, 204, 171, 128, 781, 466, 209, 130, 209, 64, 117, 499, 260, 151, 271, 235, 559, 328, 44, 150, 333, 133, 570, 115, 169, 128, 242, 154, 166, 44, 140, 184, 267, 151, 119, 766, 198, 188, 685, 159, 68, 132, 356, 79, 125, 800, 270, 184, 259, 281, 158, 101, 83, 160, 33, 253, 156, 189, 438, 311, 69, 90, 143, 392, 354, 172, 352, 314, 205, 50, 187, 94, 497, 341, 221, 61, 652, 126, 343, 181, 843, 112, 95, 94, 139, 167, 282, 750, 157, 171, 289, 398, 295, 47, 109, 223, 115, 123, 36, 153, 50, 153, 124, 357, 139, 174, 135, 123, 373, 505, 128, 211, 174, 308, 474, 170, 72, 149, 358, 441, 135, 145, 276, 303, 164, 333, 425, 142, 236, 177, 127, 123, 649, 294, 73, 143, 242, 129, 170, 142, 148, 169, 95, 93, 248, 65, 556, 217, 213, 121, 311, 356, 161, 635, 102, 305, 310, 217, 207, 447, 122, 415, 115, 133, 197, 132, 45, 128, 360, 258, 629, 164, 508, 458, 684, 150, 56, 366, 128, 179, 448, 111, 204, 803, 194, 174, 124, 410, 285, 455, 329, 161, 259, 374, 42, 118, 195, 248, 350, 204, 208, 271, 65, 233, 44, 182, 183, 356, 169, 186, 132, 1522, 180, 115, 489, 107, 395, 71, 221, 275, 796, 240, 254, 187, 109, 193, 644, 134, 136, 51, 226, 637, 245, 142, 60, 674, 201, 163, 99, 55, 282, 516, 210, 272, 138, 268, 217, 155, 268, 249, 183, 182, 465, 193, 113, 199, 469, 493, 372, 135, 116, 171, 96, 226, 78, 449, 284, 103, 220, 431, 131, 439, 260, 138, 342, 233, 114, 833, 172, 151, 110, 557, 154, 150, 164, 197, 72, 116, 111, 314, 364, 255, 190, 356, 63, 356, 342, 281, 76, 171, 327, 178, 346, 227, 131, 197, 118, 91, 113, 481, 138, 210, 320, 62, 128, 174, 195, 671, 177, 215, 213, 244, 126, 455, 180, 150, 108, 361, 116, 640, 123, 351, 265, 249, 71, 196, 104, 92, 687, 143, 143, 704, 799, 133, 340, 229, 283, 173, 394, 418, 152, 46, 193, 197, 184, 144, 105, 245, 190, 104, 214, 263, 194, 576, 261, 125, 427, 189, 188, 354, 54, 137, 182, 169, 240, 495, 304, 43, 162, 189, 264, 147, 500, 138, 302, 166, 133, 63, 147, 108, 180, 765, 223, 220, 121, 170, 244, 165, 50, 103, 150, 400, 126, 234, 354, 167, 353, 859, 177, 177, 356, 231, 95, 166, 128, 185, 68, 64, 829, 883, 163, 61, 119, 155, 248, 110, 45, 142, 90, 435, 131, 367, 365, 167, 110, 116, 202, 407, 64, 354, 157, 277, 165, 246, 136, 91, 91, 339, 374, 313, 518, 220, 164, 122, 222, 262, 376, 103, 124, 432, 402, 126, 100, 97, 183, 541, 131, 680, 201, 336, 35, 199, 64, 124, 890, 65, 173, 188, 307, 298, 215, 389, 237, 140, 136, 393, 206, 270, 206, 95, 28, 293, 68, 258, 314, 484, 353, 146, 539, 196, 124, 98, 104, 230, 151, 109, 163, 281, 124, 128, 130, 165, 297, 353, 158, 111, 286, 108, 304, 161, 420, 188, 53, 185, 198, 43, 110, 980, 264, 124, 168, 107, 202, 135, 128, 197, 208, 161, 164, 227, 816, 159, 357, 148, 48, 113, 184, 517, 138, 236, 71, 206, 107, 196, 117, 318, 251, 47, 85, 56, 303, 119, 196, 103, 102, 108, 243, 100, 460, 132, 80, 87, 297, 147, 146, 103, 114, 206, 160, 312, 84, 116, 350, 147, 361, 131, 113, 315, 570, 236, 215, 148, 74, 173, 1085, 118, 126, 686, 168, 101, 292, 192, 244, 233, 293, 134, 145, 261, 109, 189, 64, 346, 920, 181, 155, 214, 372, 252, 375, 183, 155, 127, 660, 309, 151, 467, 69, 293, 510, 122, 206, 128, 287, 126, 517, 267, 300, 44, 70, 149, 403, 846, 178, 252, 122, 225, 195, 133, 115, 33, 124, 113, 207, 307, 206, 569, 297, 142, 60, 108, 756, 185, 240, 200, 184, 258, 49, 51, 49, 150, 161, 566, 285, 127, 163, 78, 114, 639, 40, 246, 87, 201, 162, 114, 209, 195, 126, 156, 235, 241, 158, 124, 150, 148, 375, 260, 232, 130, 316, 89, 208, 251, 118, 387, 163, 735, 61, 50, 235, 216, 156, 285, 115, 169, 298, 120, 898, 201, 50, 249, 253, 80, 199, 311, 210, 94, 156, 293, 233, 663, 160, 292, 219, 586, 133, 975, 192, 160, 107, 166, 144, 332, 279, 813, 182, 201, 202, 333, 113, 313, 271, 953, 152, 751, 360, 121, 843, 215, 42, 192, 491, 143, 140, 111, 150, 228, 166, 458, 120, 150, 319, 131, 176, 265, 172, 186, 59, 166, 129, 272, 241, 171, 211, 206, 166, 223, 166, 157, 152, 568, 366, 159, 207, 154, 533, 268, 135, 129, 115, 130, 509, 103, 192, 123, 358, 256, 149, 233, 651, 140, 48, 255, 125, 70, 220, 121, 83, 133, 149, 360, 112, 139, 237, 329, 328, 152, 107, 118, 165, 172, 114, 580, 406, 130, 215, 139, 82, 125, 110, 54, 758, 333, 148, 944, 106, 126, 154, 343, 170, 122, 229, 328, 95, 267, 151, 254, 217, 145, 213, 107, 248, 612, 83, 360, 212, 181, 135, 353, 253, 126, 153, 426, 362, 195, 201, 269, 55, 135, 111, 123, 421, 665, 360, 172, 212, 182, 260, 157, 104, 260, 116, 185, 449, 173, 159, 134, 252, 334, 188, 106, 90, 134, 152, 464, 136, 63, 526, 256, 238, 461, 146, 156, 82, 421, 47, 183, 71, 289, 166, 451, 138, 51, 196, 101, 243, 174, 544, 95, 171, 175, 446, 164, 128, 98, 232, 271, 119, 98, 227, 60, 1070, 399, 136, 457, 220, 506, 228, 648, 192, 165, 208, 169, 303, 196, 58, 151, 158, 183, 376, 178, 164, 194, 66, 160, 48, 121, 253, 265, 228, 52, 247, 147, 389, 206, 534, 123, 82, 338, 271, 238, 144, 364, 488, 344, 207, 368, 185, 226, 425, 204, 746, 184, 344, 285, 251, 500, 238, 292, 377, 142, 161, 243, 124, 179, 275, 174, 297, 168, 162, 88, 111, 108, 158, 144, 534, 159, 91, 521, 520, 137, 65, 382, 54, 649, 151, 178, 428, 182, 170, 187, 197, 109, 124, 287, 165, 483, 153, 984, 112, 347, 119, 336, 264, 276, 427, 267, 38, 120, 154, 164, 582, 237, 139, 64, 546, 119, 278, 164, 131, 113, 45, 275, 180, 126, 271, 128, 158, 177, 166, 121, 122, 273, 412, 246, 131, 237, 154, 81, 152, 76, 418, 136, 272, 801, 183, 288, 159, 206, 144, 149, 49, 144, 71, 464, 131, 30, 299, 76, 149, 165, 208, 55, 41, 125, 94, 96, 721, 130, 161, 110, 167, 100, 118, 150, 106, 46, 34, 132, 88, 443, 165, 248, 108, 489, 56, 192, 89, 128, 124, 569, 76, 236, 137, 118, 275, 304, 265, 195, 115, 255, 107, 83, 37, 499, 200, 64, 218, 292, 78, 111, 254, 142, 321, 334, 403, 349, 234, 272, 322, 83, 119, 306, 177, 73, 109, 120, 134, 72, 170, 155, 118, 171, 131, 124, 114, 257, 172, 142, 172, 616, 232, 254, 48, 130, 139, 140, 249, 345, 514, 139, 170, 389, 316, 149, 85, 36, 397, 213, 237, 131, 78, 37, 186, 62, 127, 191, 94, 101, 94, 480, 291, 213, 46, 313, 242, 191, 431, 598, 139, 119, 329, 354, 558, 201, 122, 140, 298, 43, 635, 137, 166, 200, 188, 143, 132, 118, 154, 121, 172, 172, 163, 187, 131, 22, 170, 452, 280, 218, 190, 70, 595, 91, 198, 336, 188, 221, 482, 102, 147, 199, 924, 417, 118, 289, 143, 734, 315, 48, 106, 434, 180, 196, 337, 355, 89, 126, 873, 138, 219, 144, 95, 147, 133, 174, 278, 278, 353, 58, 1001, 170, 493, 118, 587, 256, 119, 466, 343, 82, 203, 45, 636, 59, 349, 660, 327, 156, 354, 420, 501, 190, 555, 236, 161, 61, 134, 171, 155, 555, 378, 313, 468, 382, 226, 138, 47, 171, 158, 186, 772, 128, 104, 44, 65, 427, 338, 148, 550, 177, 225, 78, 471, 112, 124, 212, 72, 162, 226, 57, 183, 598, 129, 206, 137, 174, 64, 126, 162, 123, 635, 354, 405, 218, 237, 154, 237, 180, 157, 175, 175, 297, 80, 437, 453, 780, 130, 153, 114, 218, 110, 373, 243, 108, 180, 217, 151, 272, 499, 169, 359, 385, 799, 122, 134, 166, 145, 245, 118, 129, 377, 164, 233, 735, 134, 145, 234, 259, 146, 307, 450, 569, 113, 417, 157, 133, 333, 267, 255, 216, 622, 60, 126, 117, 102, 215, 169, 996, 113, 121, 137, 133, 322, 36, 368, 113, 271, 94, 280, 267, 307, 151, 99, 72, 218, 118, 55, 149, 117, 395, 128, 146, 413, 153, 192, 136, 199, 238, 364, 73, 145, 159, 120, 206, 78, 174, 125, 296, 177, 1398, 65, 169, 52, 552, 135, 240, 351, 63, 242, 46, 186, 170, 128, 160, 292, 125, 129, 200, 114, 196, 250, 577, 110, 205, 181, 220, 241, 114, 259, 345, 106, 362, 217, 179, 71, 500, 133, 41, 291, 276, 132, 255, 168, 973, 217, 40, 204, 729, 157, 88, 155, 133, 142, 150, 190, 412, 66, 321, 288, 236, 409, 372, 251, 97, 86, 191, 158, 264, 220, 355, 203, 551, 543, 307, 75, 138, 94, 248, 58, 38, 617, 221, 172, 370, 521, 189, 294, 266, 141, 110, 316, 60, 85, 152, 128, 652, 114, 947, 126, 241, 84, 89, 564, 192, 140, 144, 182, 648, 148, 171, 242, 258, 176, 194, 187, 145, 134, 239, 243, 152, 375, 135, 345, 101, 115, 371, 559, 324, 110, 235, 94, 673, 89, 127, 256, 130, 182, 139, 54, 369, 182, 54, 118, 62, 241, 435, 127, 242, 181, 129, 399, 221, 363, 136, 174, 179, 153, 487, 96, 211, 280, 216, 517, 79, 390, 167, 183, 219, 148, 252, 1001, 98, 207, 114, 248, 76, 308, 135, 133, 404, 385, 344, 754, 102, 47, 262, 130, 73, 277, 307, 148, 66, 178, 992, 142, 991, 104, 130, 158, 150, 171, 189, 278, 219, 213, 107, 117, 221, 209, 119, 160, 173, 131, 138, 42, 220, 57, 423, 223, 145, 153, 133, 209, 266, 91, 61, 380, 157, 172, 297, 171, 538, 230, 68, 290, 135, 594, 53, 142, 163, 207, 184, 94, 235, 155, 144, 169, 346, 53, 109, 151, 160, 469, 124, 229, 181, 94, 116, 882, 472, 274, 538, 56, 183, 306, 130, 326, 329, 135, 408, 132, 123, 92, 187, 149, 244, 394, 293, 144, 184, 173, 120, 540, 102, 78, 168, 159, 435, 730, 102, 152, 187, 82, 492, 57, 395, 182, 149, 213, 203, 147, 230, 86, 328, 58, 394, 521, 456, 75, 315, 127, 144, 125, 116, 394, 74, 237, 44, 141, 170, 36, 160, 157, 146, 237, 359, 152, 64, 346, 552, 151, 388, 111, 953, 170, 154, 582, 136, 49, 119, 133, 99, 806, 136, 526, 481, 63, 187, 191, 108, 467, 131, 300, 160, 320, 51, 505, 183, 407, 158, 703, 253, 245, 125, 266, 455, 176, 127, 552, 113, 255, 138, 67, 204, 117, 96, 132, 266, 212, 278, 623, 315, 148, 195, 99, 262, 245, 316, 457, 123, 143, 67, 129, 143, 309, 151, 43, 125, 69, 120, 764, 195, 258, 243, 127, 228, 204, 253, 156, 120, 112, 356, 116, 114, 178, 28, 39, 420, 242, 307, 138, 471, 388, 273, 63, 343, 107, 330, 198, 336, 131, 137, 192, 137, 120, 165, 456, 184, 636, 226, 98, 174, 740, 157, 167, 203, 152, 837, 305, 142, 145, 187, 124, 154, 269, 135, 121, 152, 202, 80, 155, 269, 134, 525, 182, 85, 659, 56, 257, 239, 353, 364, 78, 127, 219, 76, 416, 251, 96, 661, 187, 164, 306, 140, 566, 138, 132, 185, 110, 278, 256, 227, 528, 57, 144, 141, 202, 173, 448, 178, 69, 263, 151, 117, 151, 178, 315, 235, 472, 111, 130, 257, 118, 546, 103, 234, 129, 109, 258, 238, 71, 422, 62, 45, 112, 126, 202, 283, 279, 156, 84, 89, 164, 217, 308, 267, 486, 490, 359, 765, 172, 122, 1148, 78, 293, 145, 810, 191, 144, 204, 205, 278, 158, 43, 121, 159, 131, 159, 288, 206, 289, 998, 127, 176, 116, 128, 179, 114, 149, 388, 189, 284, 213, 392, 157, 339, 194, 150, 127, 124, 165, 121, 116, 264, 310, 263, 129, 152, 154, 230, 674, 314, 271, 169, 311, 332, 173, 550, 250, 198, 485, 137, 149, 170, 477, 140, 190, 345, 129, 164, 400, 126, 460, 203, 308, 130, 166, 134, 399, 167, 145, 144, 123, 110, 96, 189, 121, 157, 469, 429, 194, 145, 124, 108, 191, 814, 33, 148, 528, 706, 285, 976, 258, 360, 549, 178, 155, 243, 673, 546, 727, 177, 301, 226, 574, 527, 172, 185, 93, 316, 548, 158, 366, 558, 250, 569, 95, 199, 129, 230, 371, 161, 128, 399, 119, 613, 323, 363, 282, 23, 260, 217, 85, 71, 119, 299, 164, 360, 71, 55, 274, 124, 150, 216, 203, 93, 269, 579, 145, 284, 128, 147, 117, 127, 177, 160, 104, 208, 129, 172, 138, 138, 124, 160, 254, 129, 155, 303, 181, 139, 48, 358, 183, 326, 225, 132, 53, 974, 415, 192, 149, 195, 131, 138, 58, 157, 183, 204, 486, 74, 112, 138, 200, 461, 140, 305, 154, 161, 185, 485, 141, 371, 159, 215, 997, 341, 312, 201, 166, 64, 527, 41, 204, 471, 187, 617, 190, 212, 137, 139, 100, 152, 110, 127, 165, 148, 226, 152, 329, 1527, 166, 308, 144, 53, 260, 98, 132, 112, 135, 533, 250, 426, 376, 372, 195, 165, 118, 447, 154, 197, 245, 139, 139, 86, 118, 179, 139, 64, 401, 119, 239, 141, 182, 34, 148, 157, 773, 124, 107, 561, 787, 118, 292, 607, 167, 142, 118, 228, 76, 88, 169, 183, 130, 282, 144, 122, 180, 118, 133, 101, 786, 135, 248, 124, 280, 105, 59, 345, 351, 560, 67, 135, 81, 446, 115, 117, 123, 180, 218, 133, 523, 132, 476, 239, 164, 375, 270, 717, 321, 458, 106, 766, 153, 232, 591, 202, 39, 669, 195, 137, 184, 174, 401, 77, 200, 160, 429, 301, 248, 146, 165, 182, 167, 178, 216, 157, 335, 126, 148, 113, 128, 417, 112, 206, 263, 228, 120, 328, 117, 60, 81, 117, 241, 88, 204, 291, 408, 15, 89, 87, 63, 882, 383, 257, 189, 155, 308, 223, 291, 580, 410, 113, 118, 393, 268, 276, 343, 401, 137, 176, 322, 85, 67, 238, 93, 127, 137, 115, 1003, 164, 142, 931, 144, 117, 343, 62, 105, 88, 465, 358, 112, 259, 292, 135, 165, 284, 174, 329, 177, 268, 148, 113, 416, 522, 211, 428, 145, 332, 309, 501, 108, 366, 311, 166, 407, 162, 142, 177, 187, 258, 71, 176, 156, 366, 128, 344, 127, 185, 155, 209, 154, 233, 377, 148, 109, 303, 115, 131, 248, 122, 218, 535, 257, 84, 127, 113, 47, 175, 83, 70, 866, 66, 83, 218, 157, 324, 137, 951, 455, 148, 180, 377, 635, 787, 143, 105, 313, 148, 227, 359, 203, 272, 336, 93, 657, 143, 414, 246, 199, 140, 223, 416, 317, 135, 128, 140, 923, 351, 430, 221, 125, 125, 630, 297, 212, 259, 108, 120, 64, 123, 285, 440, 71, 129, 617, 148, 223, 254, 170, 267, 344, 91, 135, 183, 156, 141, 103, 128, 272, 120, 109, 22, 665, 248, 122, 461, 42, 626, 150, 106, 584, 121, 157, 50, 890, 52, 141, 88, 346, 68, 286, 68, 194, 162, 141, 139, 124, 288, 66, 119, 135, 115, 63, 124, 11, 177, 126, 166, 124, 137, 266, 225, 245, 178, 130, 169, 27, 136, 126, 53, 322, 289, 122, 168, 231, 136, 179, 124, 223, 185, 454, 210, 123, 146, 47, 382, 399, 404, 618, 252, 123, 291, 151, 186, 283, 144, 114, 237, 101, 285, 331, 139, 102, 105, 110, 197, 84, 193, 290, 160, 220, 145, 433, 398, 125, 150, 137, 153, 36, 153, 560, 181, 129, 153, 63, 244, 84, 125, 259, 126, 712, 135, 88, 145, 127, 287, 144, 109, 144, 150, 195, 160, 58, 135, 123, 486, 135, 284, 103, 834, 128, 184, 128, 276, 243, 282, 123, 352, 219, 410, 135, 115, 122, 250, 202, 142, 162, 53, 244, 154, 173, 211, 178, 275, 409, 50, 218, 123, 732, 721, 79, 133, 130, 73, 237, 180, 145, 153, 534, 117, 513, 136, 284, 126, 162, 223, 194, 49, 216, 292, 877, 463, 195, 139, 309, 120, 500, 49, 339, 147, 118, 120, 159, 137, 471, 84, 72, 74, 128, 428, 239, 54, 507, 131, 287, 209, 174, 147, 40, 215, 133, 184, 112, 136, 158, 314, 91, 125, 134, 121, 173, 369, 371, 162, 113, 50, 30, 38, 72, 88, 504, 310, 409, 166, 246, 145, 89, 28, 60, 185, 236, 229, 73, 134, 629, 129, 79, 221, 46, 129, 118, 169, 128, 126, 959, 122, 179, 109, 124, 113, 356, 130, 516, 130, 99, 190, 120, 242, 181, 408, 154, 126, 680, 237, 541, 439, 135, 433, 1000, 176, 472, 790, 326, 141, 422, 114, 603, 125, 203, 123, 134, 125, 270, 102, 164, 50, 164, 811, 171, 138, 533, 60, 211, 144, 297, 605, 60, 151, 134, 89, 138, 37, 989, 337, 125, 284, 235, 54, 543, 147, 85, 219, 77, 668, 230, 103, 143, 47, 370, 252, 121, 144, 150, 181, 94, 99, 220, 250, 161, 593, 160, 191, 341, 75, 392, 106, 160, 569, 197, 135, 147, 203, 122, 272, 474, 260, 267, 142, 200, 96, 302, 54, 276, 132, 198, 394, 434, 183, 183, 202, 133, 158, 109, 203, 204, 139, 209, 544, 45, 67, 642, 90, 39, 236, 224, 651, 314, 142, 142, 132, 132, 100, 434, 328, 199, 248, 133, 116, 196, 179, 183, 545, 329, 147, 145, 267, 169, 400, 280, 191, 552, 357, 203, 298, 173, 138, 300, 105, 178, 412, 176, 192, 104, 127, 127, 657, 107, 60, 138, 422, 291, 185, 112, 89, 282, 261, 126, 120, 145, 112, 178, 32, 63, 132, 131, 183, 137, 102, 256, 147, 377, 152, 445, 153, 956, 212, 140, 130, 118, 802, 146, 201, 166, 73, 34, 212, 592, 141, 112, 177, 267, 439, 51, 238, 118, 227, 150, 127, 298, 130, 117, 142, 163, 148, 126, 169, 236, 424, 147, 201, 155, 213, 367, 216, 256, 113, 120, 219, 153, 170, 203, 112, 252, 220, 234, 195, 60, 222, 173, 123, 389, 331, 208, 327, 175, 180, 119, 226, 291, 149, 455, 112, 226, 335, 146, 260, 147, 139, 386, 52, 110, 245, 155, 98, 250, 237, 138, 18, 327, 212, 352, 171, 161, 51, 150, 385, 134, 310, 186, 143, 232, 686, 127, 125, 838, 128, 447, 347, 90, 126, 129, 109, 147, 377, 305, 118, 120, 290, 191, 469, 517, 287, 292, 96, 135, 197, 116, 107, 312, 467, 171, 221, 261, 86, 117, 166, 130, 260, 246, 131, 125, 310, 133, 60, 237, 124, 210, 218, 139, 129, 137, 132, 947, 446, 149, 501, 149, 229, 202, 243, 120, 41, 324, 164, 50, 124, 94, 125, 62, 231, 431, 295, 137, 144, 800, 325, 129, 188, 82, 72, 107, 274, 118, 732, 55, 140, 326, 163, 150, 119, 169, 77, 146, 161, 259, 154, 408, 71, 188, 84, 162, 117, 156, 179, 233, 532, 220, 127, 124, 188, 416, 144, 139, 557, 235, 127, 525, 101, 126, 140, 586, 121, 69, 442, 140, 256, 385, 485, 138, 127, 142, 230, 31, 255, 121, 144, 41, 111, 261, 322, 127, 147, 149, 135, 119, 163, 247, 115, 114, 62, 163, 170, 178, 127, 112, 234, 156, 127, 214, 116, 54, 165, 110, 298, 542, 56, 151, 204, 247, 154, 150, 205, 216, 305, 171, 296, 121, 133, 205, 425, 117, 125, 272, 461, 884, 113, 280, 223, 45, 55, 185, 63, 313, 133, 82, 527, 254, 148, 159, 136, 112, 133, 413, 190, 160, 172, 312, 446, 308, 110, 345, 118, 261, 210, 158, 434, 147, 152, 131, 119, 359, 145, 147, 309, 621, 216, 196, 134, 866, 989, 150, 466, 142, 439, 111, 170, 531, 138, 188, 157, 186, 251, 190, 111, 182, 57, 281, 168, 680, 259, 247, 59, 197, 129, 320, 94, 128, 255, 208, 145, 42, 156, 409, 271, 292, 119, 164, 391, 314, 102, 210, 326, 267, 266, 172, 348, 145, 119, 193, 363, 51, 119, 813, 161, 197, 72, 149, 111, 136, 251, 218, 304, 436, 144, 308, 372, 122, 175, 81, 141, 151, 428, 255, 103, 119, 393, 131, 232, 153, 737, 122, 143, 97, 124, 123, 63, 137, 312, 237, 593, 244, 149, 339, 410, 538, 332, 442, 46, 217, 156, 93, 232, 150, 232, 657, 125, 89, 100, 265, 206, 180, 200, 67, 238, 365, 323, 161, 138, 473, 357, 161, 151, 662, 216, 150, 677, 106, 167, 346, 113, 372, 109, 141, 47, 228, 224, 114, 239, 125, 364, 153, 563, 208, 228, 179, 260, 221, 50, 50, 207, 218, 140, 237, 105, 136, 505, 153, 235, 168, 65, 28, 249, 761, 62, 351, 120, 172, 592, 127, 56, 222, 179, 440, 685, 301, 276, 182, 72, 122, 180, 115, 134, 140, 181, 356, 612, 318, 179, 189, 196, 131, 294, 126, 316, 323, 184, 143, 154, 137, 146, 422, 146, 801, 206, 119, 102, 113, 132, 63, 377, 292, 301, 199, 115, 226, 135, 256, 306, 201, 149, 973, 273, 382, 61, 123, 200, 29, 126, 311, 187, 139, 70, 206, 999, 51, 282, 204, 283, 709, 162, 402, 548, 151, 716, 130, 107, 50, 158, 153, 27, 665, 134, 155, 263, 124, 218, 145, 130, 219, 166, 121, 204, 160, 314, 122, 709, 76, 453, 146, 196, 126, 120, 559, 996, 279, 145, 154, 152, 278, 275, 129, 103, 198, 475, 166, 112, 685, 307, 308, 153, 117, 128, 283, 48, 194, 457, 170, 132, 57, 113, 118, 308, 139, 105, 429, 348, 196, 132, 292, 787, 291, 160, 129, 571, 176, 240, 82, 176, 385, 1066, 169, 297, 246, 92, 165, 563, 143, 203, 54, 657, 107, 196, 150, 159, 533, 109, 140, 161, 775, 100, 184, 206, 234, 126, 105, 107, 193, 193, 145, 146, 230, 339, 231, 298, 293, 218, 400, 482, 127, 488, 248, 162, 154, 46, 148, 92, 167, 118, 290, 55, 113, 145, 104, 700, 390, 134, 376, 126, 187, 254, 461, 175, 39, 87, 127, 463, 562, 111, 135, 515, 99, 55, 136, 344, 142, 228, 137, 190, 106, 304, 77, 233, 98, 125, 73, 267, 182, 126, 198, 446, 179, 520, 43, 119, 123, 57, 913, 171, 805, 313, 570, 115, 393, 181, 81, 271, 87, 139, 90, 161, 77, 777, 296, 263, 122, 142, 116, 184, 170, 101, 234, 308, 129, 191, 123, 251, 241, 221, 185, 136, 120, 241, 427, 144, 67, 229, 295, 132, 113, 157, 233, 211, 123, 239, 159, 435, 169, 129, 51, 350, 234, 87, 247, 34, 93, 123, 120, 82, 967, 215, 799, 44, 124, 165, 37, 78, 148, 180, 67, 91, 283, 119, 110, 183, 225, 156, 448, 255, 126, 147, 315, 167, 135, 119, 121, 217, 105, 120, 264, 185, 395, 182, 1723, 156, 100, 124, 144, 207, 303, 49, 127, 127, 77, 163, 201, 82, 39, 291, 299, 590, 322, 123, 690, 525, 111, 36, 147, 85, 276, 101, 121, 223, 180, 83, 53, 124, 91, 137, 390, 143, 495, 228, 134, 292, 272, 199, 266, 195, 430, 72, 55, 41, 103, 276, 316, 402, 81, 287, 260, 660, 169, 199, 137, 110, 96, 39, 201, 169, 139, 355, 261, 321, 118, 84, 283, 66, 112, 120, 75, 154, 231, 937, 95, 123, 241, 195, 125, 545, 256, 130, 606, 63, 412, 280, 138, 148, 192, 191, 147, 135, 139, 211, 399, 900, 351, 1001, 323, 503, 107, 151, 593, 615, 109, 242, 321, 163, 328, 501, 97, 651, 366, 169, 149, 57, 69, 51, 518, 308, 461, 88, 177, 267, 47, 215, 256, 163, 121, 160, 229, 226, 124, 681, 605, 998, 266, 50, 89, 294, 995, 297, 131, 239, 137, 51, 229, 544, 125, 118, 129, 148, 454, 196, 405, 150, 200, 62, 115, 167, 235, 170, 464, 277, 338, 236, 225, 47, 627, 671, 145, 119, 233, 100, 296, 187, 58, 118, 120, 182, 123, 150, 60, 193, 142, 170, 270, 224, 462, 112, 166, 165, 234, 78, 270, 74, 209, 219, 383, 453, 117, 179, 240, 57, 137, 154, 256, 234, 99, 737, 63, 347, 214, 113, 156, 88, 176, 72, 313, 440, 148, 137, 68, 84, 444, 70, 129, 199, 401, 266, 283, 711, 142, 147, 325, 40, 437, 204, 143, 111, 370, 226, 117, 72, 837, 228, 486, 151, 286, 102, 71, 118, 166, 294, 73, 314, 281, 102, 233, 655, 260, 120, 146, 275, 433, 311, 157, 683, 855, 390, 137, 691, 132, 274, 991, 506, 369, 220, 198, 144, 89, 133, 446, 57, 138, 126, 163, 131, 157, 489, 239, 206, 238, 975, 170, 199, 121, 115, 66, 126, 119, 250, 52, 774, 127, 90, 454, 143, 93, 245, 219, 130, 202, 155, 135, 211, 153, 119, 226, 183, 177, 219, 209, 236, 233, 831, 180, 163, 224, 142, 185, 179, 206, 167, 197, 204, 198, 112, 253, 205, 278, 117, 122, 132, 286, 173, 128, 133, 120, 358, 486, 257, 253, 72, 122, 139, 477, 249, 811, 317, 584, 149, 213, 484, 188, 134, 1186, 126, 509, 329, 133, 179, 217, 172, 394, 146, 172, 326, 122, 167, 121, 123, 160, 199, 130, 108, 204, 256, 114, 177, 175, 423, 746, 975, 156, 151, 311, 371, 202, 173, 59, 410, 189, 154, 179, 428, 133, 149, 36, 60, 76, 156, 56, 309, 113, 250, 129, 529, 201, 90, 56, 150, 306, 269, 177, 176, 544, 257, 171, 295, 161, 142, 85, 340, 324, 245, 165, 167, 122, 93, 45, 238, 124, 245, 181, 181, 432, 535, 83, 386, 413, 82, 79, 127, 109, 117, 133, 187, 101, 479, 100, 665, 323, 101, 187, 163, 133, 115, 173, 98, 201, 268, 256, 273, 337, 185, 89, 437, 46, 179, 337, 131, 83, 284, 185, 141, 960, 111, 120, 115, 290, 115, 153, 112, 115, 111, 192, 120, 140, 65, 118, 113, 101, 162, 134, 274, 91, 172, 142, 121, 63, 142, 123, 262, 135, 167, 155, 59, 206, 161, 102, 131, 63, 306, 281, 56, 263, 76, 41, 431, 103, 323, 676, 132, 157, 45, 167, 953, 138, 141, 149, 380, 114, 117, 388, 171, 103, 216, 295, 51, 62, 752, 143, 439, 309, 216, 188, 267, 120, 193, 568, 142, 130, 122, 283, 132, 419, 215, 79, 129, 145, 65, 260, 96, 125, 149, 517, 136, 90, 296, 991, 49, 115, 141, 110, 76, 144, 134, 606, 195, 143, 134, 369, 85, 359, 202, 56, 255, 457, 463, 119, 430, 161, 248, 193, 176, 128, 168, 98, 137, 214, 471, 377, 119, 104, 346, 474, 211, 200, 212, 702, 74, 121, 128, 640, 151, 157, 225, 203, 127, 277, 69, 101, 202, 121, 336, 117, 169, 144, 340, 109, 179, 235, 418, 247, 365, 108, 196, 23, 193, 335, 129, 120, 126, 103, 181, 197, 64, 163, 113, 114, 282, 124, 150, 214, 63, 289, 457, 105, 138, 145, 281, 108, 385, 48, 169, 121, 165, 173, 596, 169, 145, 169, 177, 209, 615, 143, 265, 128, 116, 216, 110, 398, 202, 659, 228, 96, 108, 135, 111, 84, 133, 170, 86, 82, 124, 193, 123, 130, 253, 49, 141, 291, 236, 127, 183, 116, 706, 115, 537, 146, 504, 138, 150, 118, 133, 208, 228, 562, 296, 565, 111, 141, 203, 240, 91, 60, 243, 149, 176, 194, 243, 130, 675, 137, 487, 242, 115, 177, 143, 724, 379, 127, 107, 133, 396, 393, 132, 423, 160, 102, 183, 72, 157, 185, 268, 223, 55, 330, 185, 210, 240, 67, 418, 313, 190, 359, 531, 136, 119, 344, 84, 350, 598, 131, 661, 159, 981, 128, 115, 83, 894, 274, 111, 504, 47, 127, 160, 55, 191, 681, 116, 241, 1001, 686, 51, 161, 123, 240, 161, 321, 148, 242, 654, 435, 121, 184, 629, 283, 110, 107, 163, 110, 119, 407, 366, 170, 69, 61, 165, 305, 275, 179, 389, 242, 309, 124, 215, 212, 248, 225, 835, 147, 136, 119, 176, 161, 367, 168, 103, 302, 141, 238, 71, 158, 268, 176, 222, 228, 210, 179, 152, 154, 225, 303, 266, 129, 364, 34, 195, 139, 94, 917, 147, 193, 337, 131, 58, 216, 109, 188, 291, 343, 312, 603, 160, 131, 408, 137, 568, 127, 122, 123, 330, 205, 167, 329, 340, 346, 220, 122, 58, 166, 144, 293, 174, 245, 413, 315, 46, 306, 231, 135, 352, 202, 164, 115, 73, 243, 136, 290, 295, 119, 232, 608, 38, 863, 75, 70, 197, 318, 173, 234, 446, 569, 44, 144, 330, 627, 104, 219, 117, 917, 331, 518, 116, 204, 120, 63, 247, 160, 121, 383, 165, 242, 92, 236, 436, 365, 133, 440, 183, 146, 110, 455, 115, 111, 160, 250, 130, 138, 122, 123, 44, 332, 136, 370, 409, 293, 80, 132, 107, 72, 366, 301, 92, 39, 59, 248, 173, 171, 408, 122, 157, 122, 266, 161, 134, 570, 106, 185, 43, 286, 40, 158, 236, 137, 513, 114, 74, 160, 168, 1057, 165, 203, 117, 74, 204, 325, 88, 179, 100, 217, 439, 195, 299, 135, 185, 312, 126, 132, 64, 112, 38, 623, 129, 130, 124, 188, 294, 60, 136, 189, 171, 316, 188, 153, 168, 245, 61, 350, 157, 122, 148, 641, 498, 126, 228, 273, 179, 139, 171, 332, 177, 180, 288, 220, 428, 139, 92, 147, 142, 158, 188, 113, 626, 143, 137, 694, 168, 132, 342, 574, 316, 688, 145, 123, 220, 186, 119, 118, 307, 583, 147, 91, 602, 137, 213, 501, 131, 118, 52, 259, 188, 208, 239, 168, 124, 168, 141, 228, 183, 239, 377, 122, 310, 107, 214, 148, 87, 525, 125, 114, 77, 112, 143, 113, 190, 172, 154, 235, 148, 119, 228, 133, 221, 853, 119, 253, 139, 139, 108, 178, 331, 360, 1007, 153, 156, 144, 84, 224, 626, 547, 215, 82, 199, 185, 170, 184, 67, 277, 77, 360, 153, 305, 589, 403, 95, 287, 706, 196, 227, 420, 198, 241, 223, 149, 90, 166, 202, 123, 164, 304, 176, 154, 142, 436, 143, 142, 410, 163, 159, 625, 165, 577, 96, 119, 220, 93, 182, 126, 97, 124, 172, 253, 243, 160, 150, 708, 353, 219, 168, 124, 672, 275, 196, 163, 169, 153, 396, 160, 134, 794, 127, 134, 155, 248, 169, 120, 235, 150, 113, 636, 172, 132, 181, 86, 244, 131, 182, 129, 181, 145, 273, 150, 148, 195, 198, 708, 222, 352, 420, 67, 197, 259, 400, 752, 131, 134, 132, 199, 202, 166, 128, 139, 529, 150, 143, 919, 101, 140, 125, 363, 69, 162, 530, 122, 222, 428, 39, 193, 131, 458, 139, 158, 145, 219, 75, 1006, 114, 100, 417, 124, 303, 166, 523, 591, 307, 209, 109, 125, 211, 173, 273, 142, 96, 44, 390, 44, 176, 349, 113, 479, 110, 106, 196, 178, 172, 293, 219, 363, 175, 188, 278, 243, 78, 234, 117, 362, 176, 165, 131, 599, 155, 158, 94, 143, 105, 402, 164, 126, 54, 56, 79, 392, 130, 147, 481, 180, 165, 113, 157, 83, 163, 148, 52, 88, 469, 113, 210, 1076, 170, 78, 223, 123, 127, 199, 102, 424, 92, 709, 200, 192, 97, 52, 161, 156, 415, 229, 58, 230, 170, 728, 294, 46, 78, 117, 158, 149, 369, 586, 294, 138, 174, 103, 168, 278, 222, 145, 343, 441, 47, 200, 157, 139, 601, 209, 965, 281, 126, 266, 192, 301, 89, 123, 121, 380, 62, 157, 332, 171, 454, 789, 169, 127, 486, 219, 251, 225, 124, 163, 191, 385, 286, 460, 120, 126, 119, 858, 229, 146, 227, 302, 246, 123, 42, 325, 182, 121, 736, 84, 373, 72, 154, 582, 326, 276, 240, 125, 103, 252, 262, 658, 247, 212, 188, 268, 307, 188, 276, 182, 141, 384, 195, 148, 322, 181, 168, 724, 711, 285, 172, 44, 171, 209, 163, 37, 223, 144, 190, 120, 300, 181, 179, 145, 384, 218, 299, 734, 155, 83, 359, 318, 82, 144, 502, 234, 123, 263, 261, 123, 507, 109, 231, 765, 129, 480, 119, 990, 267, 199, 324, 86, 161, 60, 126, 117, 106, 334, 76, 163, 476, 104, 230, 105, 179, 114, 363, 232, 136, 117, 68, 201, 376, 218, 524, 387, 117, 263, 200, 120, 126, 817, 171, 321, 98, 974, 433, 134, 113, 168, 722, 140, 162, 142, 160, 75, 99, 269, 285, 126, 238, 115, 159, 119, 332, 43, 62, 136, 182, 534, 67, 164, 155, 273, 301, 564, 98, 541, 183, 521, 65, 363, 111, 268, 118, 687, 125, 49, 113, 528, 635, 325, 126, 453, 108, 316, 147, 282, 129, 188, 122, 114, 148, 112, 415, 477, 201, 148, 109, 181, 464, 119, 118, 146, 190, 78, 250, 467, 352, 44, 151, 115, 246, 152, 303, 136, 154, 303, 183, 135, 161, 250, 521, 152, 214, 131, 143, 190, 127, 44, 541, 171, 297, 455, 147, 996, 177, 173, 296, 241, 246, 188, 116, 137, 170, 124, 120, 115, 140, 233, 170, 127, 161, 305, 167, 185, 213, 68, 117, 54, 147, 302, 518, 43, 189, 210, 143, 168, 152, 142, 170, 152, 296, 191, 180, 496, 156, 219, 667, 309, 248, 66, 336, 203, 167, 130, 343, 556, 977, 152, 995, 249, 165, 326, 126, 129, 412, 154, 159, 57, 480, 146, 153, 482, 534, 632, 156, 102, 189, 534, 132, 232, 452, 59, 334, 128, 142, 162, 102, 438, 267, 57, 252, 511, 327, 267, 243, 543, 211, 157, 159, 207, 101, 255, 162, 210, 147, 115, 201, 373, 313, 157, 257, 760, 115, 607, 63, 222, 221, 47, 414, 115, 162, 232, 315, 136, 134, 220, 44, 53, 188, 136, 86, 138, 243, 115, 141, 125, 657, 557, 119, 246, 193, 763, 61, 185, 68, 190, 625, 145, 135, 244, 319, 151, 964, 438, 136, 121, 144, 266, 122, 132, 159, 114, 406, 510, 984, 145, 632, 348, 191, 130, 301, 347, 172, 104, 101, 50, 177, 212, 154, 142, 139, 264, 123, 114, 188, 222, 90, 95, 114, 113, 357, 435, 188, 226, 154, 173, 172, 161, 152, 170, 136, 263, 70, 173, 227, 144, 197, 96, 691, 570, 944, 263, 168, 938, 280, 63, 465, 138, 160, 366, 109, 785, 42, 368, 245, 224, 192, 179, 316, 151, 93, 344, 246, 323, 313, 371, 328, 159, 246, 310, 107, 187, 194, 338, 165, 122, 312, 39, 251, 177, 133, 295, 93, 180, 171, 122, 110, 182, 502, 209, 155, 675, 460, 184, 43, 467, 127, 97, 305, 221, 211, 231, 158, 96, 138, 892, 357, 355, 197, 135, 473, 110, 145, 152, 97, 472, 127, 84, 29, 815, 124, 137, 344, 239, 221, 132, 257, 266, 61, 119, 116, 76, 171, 117, 118, 563, 431, 232, 221, 903, 204, 469, 357, 413, 150, 173, 166, 227, 230, 284, 871, 129, 179, 201, 161, 81, 226, 168, 209, 245, 147, 41, 46, 108, 108, 170, 280, 159, 274, 208, 335, 221, 602, 221, 199, 158, 167, 167, 334, 192, 172, 533, 125, 38, 104, 144, 279, 309, 197, 125, 255, 175, 71, 142, 497, 353, 130, 121, 229, 156, 517, 372, 108, 209, 496, 95, 222, 162, 152, 152, 139, 184, 142, 188, 144, 163, 177, 159, 45, 206, 972, 69, 52, 131, 173, 402, 146, 142, 431, 292, 154, 131, 898, 406, 178, 124, 202, 200, 171, 227, 125, 47, 119, 727, 143, 108, 146, 138, 262, 165, 376, 132, 273, 465, 46, 74, 82, 216, 70, 72, 261, 181, 98, 525, 256, 172, 123, 575, 354, 345, 145, 45, 207, 124, 87, 119, 153, 155, 161, 206, 112, 247, 234, 258, 204, 80, 229, 153, 306, 426, 361, 112, 166, 133, 85, 199, 199, 384, 140, 146, 235, 155, 298, 191, 166, 623, 296, 145, 441, 380, 966, 97, 307, 421, 182, 133, 188, 296, 119, 169, 155, 102, 227, 728, 107, 959, 370, 162, 97, 156, 100, 147, 240, 124, 252, 159, 125, 250, 136, 93, 325, 295, 193, 330, 82, 126, 107, 49, 47, 143, 145, 426, 348, 212, 299, 165, 164, 527, 361, 256, 119, 412, 120, 83, 249, 508, 258, 130, 47, 133, 180, 144, 135, 103, 98, 342, 136, 178, 171, 798, 117, 138, 97, 190, 160, 141, 126, 130, 145, 125, 470, 312, 211, 482, 96, 165, 139, 166, 149, 369, 137, 174, 754, 300, 366, 137, 290, 73, 179, 155, 138, 229, 381, 205, 109, 121, 247, 126, 222, 199, 143, 154, 151, 1002, 287, 143, 330, 140, 115, 440, 86, 131, 213, 165, 181, 343, 218, 242, 95, 178, 124, 486, 113, 182, 594, 162, 129, 217, 48, 114, 151, 34, 134, 283, 126, 289, 270, 304, 206, 129, 115, 163, 76, 45, 116, 147, 157, 89, 156, 334, 121, 80, 119, 251, 182, 188, 131, 345, 214, 183, 218, 318, 240, 280, 284, 108, 247, 140, 739, 148, 238, 130, 138, 136, 148, 151, 158, 712, 679, 168, 370, 119, 573, 384, 210, 209, 260, 340, 490, 116, 496, 597, 74, 187, 113, 811, 235, 338, 126, 251, 288, 583, 240, 345, 233, 203, 144, 490, 98, 319, 237, 174, 158, 69, 710, 290, 634, 104, 133, 867, 170, 107, 190, 277, 116, 156, 270, 218, 878, 134, 206, 252, 150, 276, 565, 664, 380, 115, 52, 97, 98, 454, 239, 180, 207, 277, 49, 118, 232, 53, 132, 117, 211, 791, 184, 225, 59, 188, 54, 110, 193, 186, 37, 138, 157, 172, 193, 227, 55, 295, 80, 355, 861, 180, 56, 182, 195, 318, 173, 277, 134, 298, 119, 238, 132, 135, 126, 213, 244, 145, 354, 294, 339, 157, 399, 305, 92, 181, 226, 54, 50, 120, 199, 274, 258, 510, 129, 113, 230, 128, 593, 214, 201, 133, 367, 184, 142, 160, 186, 140, 247, 273, 114, 585, 111, 220, 232, 53, 159, 171, 252, 164, 62, 128, 391, 289, 207, 294, 81, 172, 261, 132, 201, 674, 87, 341, 309, 278, 198, 496, 142, 116, 127, 124, 577, 126, 232, 123, 217, 249, 225, 678, 135, 114, 137, 138, 187, 448, 845, 374, 398, 228, 218, 636, 516, 203, 278, 338, 240, 473, 154, 64, 520, 145, 141, 52, 234, 163, 107, 194, 175, 32, 42, 186, 215, 127, 148, 906, 368, 106, 458, 119, 231, 204, 175, 246, 132, 734, 236, 261, 146, 116, 220, 46, 100, 121, 71, 130, 136, 73, 121, 162, 151, 851, 324, 114, 167, 393, 238, 104, 352, 205, 322, 145, 165, 104, 267, 287, 151, 277, 42, 465, 326, 136, 404, 159, 203, 210, 119, 182, 268, 132, 512, 689, 179, 193, 68, 964, 450, 592, 293, 111, 420, 366, 728, 292, 151, 113, 754, 205, 51, 696, 129, 83, 87, 152, 163, 360, 160, 363, 158, 159, 343, 351, 462, 152, 345, 401, 667, 177, 381, 277, 102, 209, 646, 232, 767, 856, 148, 184, 233, 92, 392, 198, 103, 342, 312, 131, 189, 200, 113, 152, 119, 145, 76, 343, 77, 272, 211, 174, 132, 186, 267, 132, 145, 315, 79, 773, 408, 194, 615, 122, 484, 553, 135, 251, 165, 74, 142, 237, 171, 129, 606, 433, 83, 219, 138, 163, 205, 55, 492, 150, 433, 266, 241, 186, 247, 239, 209, 212, 271, 254, 144, 358, 125, 57, 152, 185, 346, 154, 79, 130, 72, 322, 144, 61, 161, 165, 207, 194, 310, 582, 292, 177, 55, 328, 281, 840, 148, 421, 356, 209, 190, 148, 156, 169, 141, 358, 117, 478, 194, 154, 149, 292, 525, 652, 163, 153, 214, 207, 141, 142, 158, 186, 112, 984, 54, 157, 160, 171, 152, 285, 315, 163, 311, 196, 527, 256, 324, 113, 56, 150, 254, 99, 575, 247, 147, 142, 102, 419, 125, 119, 116, 206, 404, 531, 51, 80, 149, 126, 257, 199, 95, 63, 147, 130, 275, 42, 134, 423, 341, 132, 163, 205, 125, 143, 79, 112, 306, 132, 112, 73, 168, 225, 120, 766, 46, 128, 66, 986, 148, 87, 101, 941, 103, 134, 125, 531, 67, 42, 165, 86, 526, 78, 719, 177, 571, 76, 122, 423, 259, 131, 271, 217, 166, 208, 95, 367, 141, 668, 187, 38, 113, 285, 658, 837, 142, 116, 123, 120, 113, 353, 130, 848, 200, 195, 50, 96, 58, 96, 258, 176, 208, 399, 704, 239, 139, 130, 155, 133, 165, 170, 457, 117, 50, 283, 295, 416, 587, 131, 270, 144, 590, 82, 141, 137, 265, 132, 63, 118, 133, 323, 149, 49, 134, 463, 186, 46, 343, 212, 336, 239, 263, 141, 258, 129, 683, 103, 180, 202, 124, 91, 166, 939, 186, 450, 229, 47, 156, 223, 130, 989, 332, 962, 125, 135, 277, 170, 950, 215, 129, 409, 197, 130, 166, 55, 140, 207, 272, 74, 119, 368, 169, 347, 352, 178, 238, 290, 263, 87, 117, 997, 120, 201, 116, 173, 103, 121, 500, 133, 610, 135, 166, 836, 186, 396, 110, 123, 263, 143, 114, 506, 172, 59, 145, 372, 251, 112, 219, 124, 188, 182, 163, 163, 467, 205, 605, 125, 433, 125, 146, 81, 280, 343, 163, 87, 139, 62, 142, 190, 104, 432, 196, 76, 321, 313, 288, 110, 162, 199, 323, 679, 101, 169, 210, 395, 88, 368, 157, 150, 156, 50, 486, 45, 122, 153, 50, 725, 266, 175, 152, 191, 182, 202, 340, 80, 126, 122, 269, 518, 271, 433, 49, 171, 171, 331, 236, 39, 158, 217, 177, 141, 279, 424, 146, 208, 188, 289, 125, 144, 195, 68, 140, 163, 662, 406, 433, 187, 359, 100, 158, 63, 197, 210, 291, 158, 126, 171, 107, 204, 42, 190, 146, 52, 283, 357, 109, 117, 306, 172, 196, 306, 110, 149, 71, 144, 133, 141, 375, 138, 491, 70, 116, 788, 149, 70, 228, 148, 490, 241, 169, 136, 221, 153, 581, 189, 196, 123, 74, 151, 177, 231, 621, 86, 70, 124, 124, 151, 179, 169, 834, 116, 180, 150, 495, 127, 127, 309, 108, 212, 618, 232, 185, 475, 374, 164, 255, 170, 701, 150, 129, 58, 162, 197, 364, 148, 387, 201, 139, 118, 342, 101, 124, 278, 156, 210, 569, 113, 269, 248, 127, 83, 275, 506, 147, 83, 120, 188, 83, 268, 578, 179, 213, 176, 241, 119, 197, 118, 141, 671, 300, 124, 245, 116, 320, 591, 362, 167, 162, 219, 180, 136, 129, 192, 163, 198, 369, 613, 261, 158, 178, 357, 201, 137, 118, 159, 123, 507, 122, 191, 173, 222, 106, 125, 128, 793, 300, 141, 152, 127, 130, 554, 107, 290, 110, 144, 505, 71, 518, 118, 190, 155, 170, 167, 216, 128, 761, 217, 85, 484, 316, 268, 232, 184, 174, 149, 135, 55, 44, 112, 180, 232, 432, 146, 125, 167, 121, 134, 189, 453, 280, 479, 90, 114, 150, 714, 405, 122, 199, 213, 132, 154, 121, 981, 136, 747, 172, 551, 215, 155, 44, 375, 598, 102, 107, 208, 430, 211, 171, 168, 65, 137, 161, 93, 225, 158, 666, 207, 294, 59, 90, 189, 176, 90, 182, 74, 126, 171, 451, 143, 132, 298, 51, 253, 367, 262, 503, 146, 180, 69, 153, 447, 115, 137, 154, 181, 241, 195, 94, 144, 112, 247, 140, 129, 182, 88, 146, 195, 616, 95, 114, 606, 139, 169, 162, 399, 182, 57, 123, 42, 425, 214, 566, 101, 115, 120, 874, 344, 191, 140, 150, 49, 181, 133, 156, 277, 148, 131, 801, 429, 230, 484, 147, 512, 46, 336, 147, 157, 215, 50, 933, 263, 123, 892, 243, 588, 185, 103, 90, 540, 159, 471, 240, 154, 325, 136, 278, 153, 341, 135, 70, 89, 334, 205, 244, 130, 227, 872, 202, 151, 139, 511, 135, 172, 692, 245, 143, 352, 144, 114, 138, 270, 490, 70, 516, 140, 310, 373, 517, 444, 475, 127, 202, 285, 221, 342, 138, 456, 776, 58, 145, 67, 137, 797, 198, 195, 314, 365, 230, 674, 730, 44, 188, 236, 301, 158, 159, 138, 130, 142, 127, 120, 214, 187, 139, 140, 247, 315, 155, 119, 151, 355, 82, 182, 270, 131, 632, 157, 58, 94, 110, 233, 290, 374, 347, 114, 128, 978, 86, 174, 265, 139, 159, 125, 288, 327, 383, 200, 63, 178, 137, 111, 173, 160, 389, 176, 108, 53, 84, 165, 122, 109, 257, 180, 700, 209, 84, 229, 367, 192, 161, 133, 103, 76, 113, 347, 106, 160, 97, 544, 368, 127, 102, 136, 420, 55, 283, 138, 176, 267, 283, 561, 138, 236, 127, 157, 178, 271, 143, 199, 169, 88, 204, 287, 811, 332, 133, 261, 121, 641, 183, 190, 42, 125, 86, 55, 160, 261, 182, 162, 213, 76, 183, 70, 263, 462, 124, 224, 121, 144, 210, 69, 498, 123, 255, 186, 172, 505, 121, 227, 145, 131, 107, 189, 223, 749, 299, 127, 182, 156, 52, 343, 252, 185, 415, 352, 57, 123, 510, 168, 238, 188, 79, 209, 297, 289, 155, 166, 242, 115, 213, 123, 150, 164, 317, 199, 207, 114, 424, 212, 216, 188, 97, 175, 142, 570, 203, 259, 825, 127, 178, 133, 191, 111, 39, 190, 629, 389, 144, 112, 144, 135, 471, 249, 327, 58, 130, 236, 103, 151, 138, 527, 213, 733, 622, 147, 63, 40, 217, 380, 127, 288, 319, 131, 477, 145, 192, 214, 103, 261, 361, 120, 103, 324, 419, 168, 88, 190, 124, 88, 108, 223, 209, 395, 181, 163, 127, 193, 246, 221, 109, 212, 449, 97, 282, 145, 444, 366, 229, 163, 196, 60, 83, 911, 136, 548, 266, 121, 137, 260, 128, 148, 60, 55, 252, 122, 67, 291, 123, 140, 200, 55, 193, 474, 153, 213, 158, 182, 215, 49, 75, 113, 161, 48, 164, 129, 367, 115, 160, 557, 82, 464, 215, 112, 199, 114, 155, 121, 340, 125, 127, 155, 111, 123, 135, 137, 530, 373, 112, 131, 127, 359, 126, 130, 115, 286, 256, 118, 152, 154, 200, 73, 377, 396, 386, 158, 102, 145, 37, 139, 232, 229, 978, 142, 257, 413, 55, 130, 121, 107, 21, 252, 122, 303, 198, 218, 451, 283, 403, 238, 102, 149, 204, 473, 177, 157, 71, 650, 160, 54, 79, 148, 351, 211, 325, 83, 192, 87, 252, 133, 359, 124, 136, 338, 279, 168, 239, 130, 61, 279, 439, 143, 364, 173, 307, 171, 72, 235, 346, 143, 122, 289, 118, 648, 200, 150, 166, 269, 166, 174, 150, 617, 330, 424, 52, 267, 313, 369, 97, 159, 267, 122, 895, 169, 151, 471, 108, 79, 628, 320, 930, 58, 241, 97, 154, 134, 134, 133, 332, 137, 148, 118, 241, 130, 141, 135, 588, 230, 351, 156, 91, 247, 314, 157, 200, 131, 170, 239, 139, 133, 525, 113, 73, 119, 204, 126, 168, 131, 490, 177, 172, 216, 226, 132, 198, 86, 150, 127, 177, 489, 116, 229, 56, 206, 144, 139, 757, 95, 53, 198, 347, 327, 111, 402, 147, 239, 430, 346, 488, 127, 186, 346, 123, 77, 273, 177, 123, 647, 139, 344, 307, 123, 120, 154, 243, 315, 234, 213, 175, 129, 124, 178, 117, 506, 57, 244, 151, 128, 217, 426, 242, 334, 112, 73, 563, 177, 364, 228, 173, 161, 977, 182, 131, 548, 704, 171, 56, 392, 132, 50, 40, 198, 1475, 295, 52, 291, 53, 215, 250, 130, 765, 258, 271, 112, 192, 111, 822, 168, 191, 154, 149, 207, 140, 174, 203, 326, 301, 136, 48, 145, 146, 164, 73, 94, 192, 316, 203, 286, 144, 245, 143, 132, 395, 947, 448, 219, 129, 43, 142, 127, 123, 105, 518, 134, 198, 144, 123, 121, 339, 244, 701, 149, 52, 723, 224, 287, 116, 152, 135, 222, 155, 111, 196, 450, 216, 190, 647, 133, 284, 67, 112, 120, 277, 234, 110, 136, 296, 314, 99, 53, 217, 146, 293, 198, 402, 141, 143, 129, 671, 209, 436, 285, 49, 174, 418, 172, 203, 254, 61, 50, 55, 526, 193, 138, 296, 95, 143, 165, 591, 472, 671, 738, 175, 330, 238, 146, 178, 238, 993, 658, 117, 436, 100, 483, 496, 202, 145, 226, 135, 141, 62, 315, 100, 151, 100, 203, 53, 170, 199, 163, 436, 117, 294, 76, 156, 201, 87, 103, 142, 68, 96, 213, 135, 56, 32, 204, 245, 199, 413, 179, 130, 114, 109, 118, 143, 408, 300, 124, 426, 152, 140, 150, 125, 179, 214, 145, 132, 129, 140, 315, 173, 589, 128, 88, 106, 110, 147, 109, 96, 58, 249, 179, 163, 688, 407, 404, 125, 57, 140, 279, 111, 148, 134, 244, 142, 173, 140, 837, 110, 120, 337, 169, 151, 54, 127, 156, 130, 142, 843, 451, 59, 362, 145, 90, 206, 170, 46, 253, 154, 265, 105, 109, 450, 50, 153, 54, 509, 134, 165, 130, 187, 316, 780, 137, 209, 166, 148, 203, 100, 147, 499, 320, 513, 157, 78, 145, 180, 257, 133, 476, 184, 104, 228, 874, 147, 175, 167, 196, 57, 183, 170, 205, 653, 237, 571, 109, 124, 225, 261, 258, 214, 170, 100, 233, 108, 374, 113, 167, 293, 373, 253, 240, 427, 159, 41, 262, 185, 168, 340, 147, 146, 169, 82, 110, 349, 190, 132, 236, 614, 125, 260, 137, 279, 289, 216, 59, 112, 213, 137, 353, 180, 432, 669, 258, 112, 203, 131, 646, 173, 542, 154, 129, 218, 264, 84, 527, 60, 205, 174, 522, 212, 991, 82, 253, 50, 127, 186, 59, 56, 112, 365, 161, 112, 131, 126, 137, 540, 117, 195, 174, 208, 520, 106, 377, 166, 114, 246, 168, 855, 136, 285, 600, 67, 398, 105, 273, 117, 107, 225, 146, 446, 187, 67, 374, 251, 300, 88, 196, 225, 125, 366, 122, 100, 198, 145, 231, 144, 114, 201, 86, 285, 168, 278, 232, 108, 193, 317, 124, 143, 255, 122, 174, 82, 985, 296, 474, 103, 784, 170, 45, 81, 435, 264, 267, 67, 87, 529, 407, 357, 173, 186, 295, 201, 50, 314, 172, 523, 721, 151, 177, 252, 168, 122, 104, 293, 278, 74, 634, 144, 198, 406, 151, 139, 495, 338, 113, 166, 71, 240, 231, 179, 160, 159, 135, 196, 224, 329, 364, 508, 142, 141, 121, 53, 153, 200, 130, 65, 219, 140, 316, 454, 285, 169, 121, 116, 58, 192, 230, 144, 271, 122, 132, 827, 229, 127, 151, 303, 364, 154, 310, 242, 249, 234, 245, 189, 130, 131, 127, 257, 119, 344, 84, 145, 132, 82, 314, 255, 140, 132, 184, 248, 60, 127, 190, 54, 147, 117, 475, 188, 75, 316, 117, 106, 152, 305, 140, 194, 203, 264, 74, 171, 799, 209, 119, 152, 179, 78, 110, 80, 451, 130, 547, 107, 111, 212, 50, 223, 82, 381, 198, 740, 227, 193, 108, 171, 213, 478, 139, 158, 183, 131, 154, 155, 372, 28, 342, 178, 455, 94, 161, 127, 184, 87, 160, 168, 192, 146, 75, 182, 187, 175, 369, 148, 140, 50, 158, 214, 131, 84, 412, 284, 108, 111, 164, 152, 126, 441, 113, 117, 804, 189, 344, 70, 290, 412, 114, 188, 154, 664, 132, 67, 242, 167, 138, 267, 51, 70, 140, 273, 132, 268, 318, 140, 650, 432, 330, 336, 104, 153, 196, 162, 537, 208, 211, 56, 137, 419, 154, 879, 157, 345, 173, 110, 247, 160, 199, 118, 70, 164, 450, 191, 154, 77, 117, 130, 181, 157, 154, 241, 883, 285, 141, 369, 113, 352, 41, 120, 458, 138, 711, 163, 732, 145, 61, 301, 140, 128, 213, 422, 264, 151, 152, 132, 38, 108, 106, 449, 218, 69, 57, 217, 249, 588, 144, 128, 150, 140, 123, 644, 150, 131, 270, 144, 130, 212, 123, 134, 900, 137, 211, 54, 145, 213, 117, 803, 305, 165, 385, 356, 184, 130, 615, 360, 386, 178, 420, 47, 182, 38, 153, 199, 468, 449, 136, 83, 120, 114, 125, 230, 159, 294, 223, 357, 556, 131, 412, 127, 86, 129, 187, 271, 365, 142, 102, 60, 191, 115, 166, 156, 182, 715, 95, 155, 352, 94, 216, 259, 333, 435, 233, 104, 296, 232, 153, 292, 85, 79, 112, 240, 610, 304, 134, 335, 475, 237, 212, 185, 131, 189, 79, 212, 113, 207, 112, 207, 26, 165, 186, 152, 237, 43, 125, 484, 180, 111, 668, 539, 143, 115, 200, 905, 256, 184, 284, 262, 538, 269, 790, 392, 214, 502, 385, 128, 130, 92, 249, 105, 162, 133, 149, 138, 340, 117, 53, 92, 174, 36, 121, 400, 491, 586, 124, 206, 97, 116, 115, 127, 294, 246, 95, 123, 381, 184, 179, 123, 112, 317, 127, 104, 199, 136, 184, 360, 79, 196, 208, 229, 423, 134, 195, 98, 118, 307, 63, 427, 130, 337, 168, 833, 126, 44, 417, 46, 268, 254, 162, 122, 121, 82, 56, 76, 306, 164, 149, 141, 129, 435, 105, 147, 149, 47, 110, 169, 96, 127, 147, 128, 114, 336, 354, 133, 89, 202, 117, 229, 484, 119, 129, 130, 70, 87, 109, 50, 672, 388, 114, 364, 220, 245, 105, 222, 135, 146, 129, 214, 66, 38, 376, 334, 99, 856, 148, 204, 149, 166, 75, 273, 86, 215, 309, 191, 125, 171, 338, 108, 141, 119, 145, 187, 110, 387, 137, 163, 125, 133, 257, 276, 182, 192, 101, 168, 127, 121, 759, 308, 49, 463, 309, 74, 150, 452, 63, 188, 169, 182, 144, 150, 419, 325, 125, 121, 285, 126, 197, 296, 105, 424, 179, 577, 649, 224, 119, 138, 714, 333, 306, 268, 111, 315, 310, 255, 64, 80, 264, 124, 209, 255, 405, 807, 140, 157, 340, 145, 206, 135, 241, 118, 160, 902, 154, 172, 271, 177, 160, 358, 755, 91, 356, 674, 333, 194, 110, 172, 275, 136, 75, 135, 566, 123, 108, 250, 128, 58, 357, 294, 161, 181, 376, 150, 192, 301, 139, 438, 361, 211, 385, 454, 109, 554, 187, 155, 259, 159, 341, 228, 143, 314, 128, 123, 554, 258, 220, 234, 145, 188, 197, 273, 164, 111, 106, 393, 249, 113, 146, 130, 150, 747, 413, 116, 352, 290, 395, 105, 155, 231, 366, 125, 357, 372, 85, 387, 264, 174, 201, 186, 156, 429, 77, 124, 171, 304, 187, 268, 140, 344, 49, 307, 270, 247, 177, 114, 254, 275, 142, 68, 193, 437, 330, 108, 859, 142, 227, 221, 241, 342, 211, 128, 345, 95, 293, 147, 131, 151, 178, 209, 87, 107, 81, 161, 142, 97, 84, 107, 124, 170, 118, 105, 260, 701, 93, 178, 125, 160, 91, 83, 405, 348, 83, 137, 328, 194, 166, 115, 295, 216, 472, 183, 309, 133, 98, 137, 161, 417, 331, 228, 342, 183, 127, 426, 220, 233, 176, 198, 125, 106, 79, 77, 340, 338, 123, 625, 58, 281, 229, 114, 112, 186, 481, 97, 239, 53, 531, 387, 274, 89, 334, 141, 43, 123, 206, 130, 132, 125, 557, 42, 169, 179, 199, 157, 863, 439, 122, 151, 71, 132, 167, 138, 258, 256, 173, 611, 62, 507, 159, 127, 233, 555, 148, 29, 51, 203, 268, 170, 126, 122, 234, 75, 476, 266, 131, 215, 1001, 246, 207, 69, 234, 34, 124, 61, 169, 818, 328, 121, 138, 136, 124, 409, 167, 137, 908, 642, 129, 137, 133, 210, 244, 259, 402, 400, 280, 392, 165, 606, 159, 173, 148, 117, 180, 144, 111, 295, 319, 432, 340, 134, 125, 95, 195, 166, 134, 157, 554, 97, 319, 107, 231, 402, 395, 119, 246, 82, 165, 233, 93, 439, 138, 253, 161, 204, 333, 166, 184, 328, 72, 117, 158, 123, 139, 80, 854, 297, 129, 453, 500, 168, 148, 126, 348, 148, 76, 204, 111, 138, 143, 335, 258, 162, 890, 184, 280, 202, 154, 221, 139, 269, 123, 139, 152, 212, 177, 461, 361, 315, 105, 227, 131, 76, 199, 174, 171, 260, 286, 356, 169, 131, 184, 151, 858, 402, 128, 286, 119, 154, 49, 250, 224, 101, 174, 103, 130, 87, 732, 249, 63, 220, 163, 151, 151, 77, 782, 307, 408, 142, 137, 120, 117, 46, 585, 131, 46, 164, 113, 158, 198, 163, 136, 196, 212, 523, 178, 136, 370, 108, 287, 177, 406, 281, 125, 146, 135, 602, 292, 92, 89, 82, 127, 76, 156, 128, 130, 166, 225, 125, 167, 145, 190, 68, 190, 129, 43, 178, 155, 1007, 142, 144, 308, 298, 746, 145, 243, 176, 303, 241, 46, 127, 121, 210, 162, 57, 187, 60, 200, 344, 121, 375, 154, 113, 341, 111, 306, 191, 486, 619, 196, 143, 64, 132, 189, 187, 73, 211, 89, 125, 53, 288, 175, 103, 303, 156, 69, 199, 259, 480, 42, 280, 69, 382, 136, 153, 137, 140, 253, 135, 169, 295, 136, 434, 261, 166, 148, 235, 144, 168, 101, 135, 94, 125, 122, 130, 158, 537, 89, 136, 106, 184, 66, 76, 164, 136, 155, 203, 265, 156, 145, 162, 119, 428, 212, 142, 108, 511, 62, 128, 139, 75, 76, 339, 114, 184, 350, 166, 148, 216, 123, 306, 76, 167, 144, 507, 42, 209, 148, 401, 320, 194, 81, 113, 155, 519, 990, 765, 225, 71, 183, 168, 361, 214, 310, 284, 266, 147, 179, 144, 184, 158, 271, 235, 209, 111, 230, 265, 127, 96, 91, 285, 158, 171, 89, 341, 193, 103, 248, 154, 488, 211, 255, 349, 223, 143, 194, 197, 91, 206, 80, 532, 446, 149, 233, 257, 816, 140, 122, 226, 186, 347, 165, 116, 110, 223, 241, 301, 150, 227, 146, 195, 181, 235, 292, 50, 83, 133, 278, 733, 244, 174, 171, 281, 357, 743, 150, 92, 154, 130, 147, 383, 140, 102, 265, 468, 154, 127, 251, 377, 112, 133, 44, 485, 179, 165, 80, 167, 157, 249, 703, 503, 243, 42, 139, 169, 178, 191, 206, 317, 125, 393, 151, 39, 768, 135, 66, 307, 158, 52, 87, 255, 684, 567, 129, 168, 411, 33, 206, 98, 321, 271, 104, 137, 222, 181, 338, 459, 85, 129, 178, 72, 167, 441, 127, 449, 142, 213, 197, 402, 177, 151, 307, 362, 388, 227, 108, 200, 377, 292, 297, 254, 137, 186, 140, 115, 351, 111, 552, 219, 130, 327, 80, 172, 130, 192, 999, 510, 141, 108, 226, 178, 542, 102, 151, 279, 121, 120, 87, 140, 162, 236, 167, 161, 78, 147, 146, 103, 401, 246, 160, 269, 235, 303, 155, 273, 102, 133, 195, 315, 215, 115, 179, 166, 25, 167, 354, 303, 48, 163, 726, 483, 122, 154, 392, 652, 736, 145, 160, 804, 323, 152, 190, 166, 111, 481, 319, 96, 420, 74, 515, 144, 537, 288, 221, 122, 317, 79, 290, 215, 99, 968, 104, 345, 824, 132, 154, 353, 261, 305, 244, 126, 153, 209, 121, 351, 216, 122, 253, 161, 149, 240, 408, 167, 222, 167, 153, 129, 155, 909, 141, 165, 271, 96, 129, 144, 141, 241, 289, 248, 224, 285, 198, 139, 300, 155, 638, 131, 100, 992, 779, 280, 133, 176, 233, 578, 145, 84, 90, 139, 149, 161, 45, 143, 129, 264, 462, 243, 152, 134, 120, 177, 393, 43, 217, 260, 165, 242, 351, 100, 649, 108, 262, 135, 143, 281, 730, 139, 126, 355, 127, 117, 200, 143, 151, 563, 140, 114, 185, 179, 216, 88, 188, 283, 195, 63, 64, 143, 404, 147, 695, 476, 168, 206, 419, 236, 131, 112, 123, 152, 41, 242, 438, 308, 568, 212, 344, 127, 244, 697, 224, 189, 145, 225, 52, 421, 135, 136, 161, 175, 226, 379, 208, 55, 140, 1010, 70, 128, 100, 236, 147, 96, 270, 126, 125, 264, 477, 138, 132, 146, 378, 615, 75, 359, 251, 185, 132, 129, 146, 163, 76, 521, 116, 291, 210, 213, 194, 149, 61, 144, 117, 154, 910, 313, 129, 190, 325, 368, 42, 329, 213, 353, 195, 489, 96, 795, 119, 221, 311, 366, 119, 373, 154, 87, 247, 466, 215, 149, 123, 111, 817, 266, 213, 309, 69, 164, 292, 100, 233, 70, 495, 103, 236, 177, 121, 1051, 237, 229, 46, 228, 74, 214, 204, 119, 132, 175, 143, 215, 133, 124, 95, 246, 154, 145, 326, 185, 329, 532, 132, 111, 239, 133, 180, 345, 358, 187, 157, 306, 306, 141, 569, 232, 573, 200, 172, 55, 237, 92, 231, 170, 90, 384, 398, 163, 133, 169, 124, 115, 186, 204, 274, 381, 189, 501, 403, 189, 132, 363, 495, 71, 362, 313, 178, 263, 238, 116, 272, 324, 225, 511, 142, 222, 94, 157, 278, 149, 222, 117, 476, 163, 244, 147, 86, 191, 159, 185, 329, 112, 456, 185, 145, 151, 362, 486, 153, 239, 127, 145, 219, 172, 185, 479, 126, 146, 146, 152, 170, 73, 190, 85, 134, 151, 174, 75, 85, 257, 196, 110, 276, 181, 116, 255, 130, 351, 114, 125, 222, 200, 128, 210, 90, 159, 588, 973, 72, 164, 170, 213, 238, 549, 281, 227, 289, 284, 291, 298, 187, 865, 261, 77, 351, 118, 181, 130, 422, 136, 992, 620, 244, 467, 62, 171, 189, 36, 224, 132, 138, 157, 108, 142, 38, 403, 634, 158, 744, 57, 617, 108, 109, 108, 262, 95, 37, 140, 77, 81, 183, 154, 183, 148, 159, 252, 238, 499, 142, 257, 235, 463, 130, 105, 151, 298, 401, 119, 391, 277, 552, 133, 228, 289, 472, 97, 257, 255, 204, 219, 127, 68, 336, 275, 129, 32, 112, 208, 142, 331, 137, 252, 128, 168, 134, 301, 47, 40, 108, 154, 118, 134, 299, 323, 791, 132, 170, 172, 269, 174, 275, 39, 303, 766, 154, 124, 292, 223, 226, 155, 442, 333, 162, 90, 235, 121, 125, 174, 324, 138, 443, 194, 63, 122, 248, 376, 210, 295, 99, 153, 176, 336, 248, 238, 164, 344, 185, 39, 216, 412, 157, 135, 46, 179, 215, 434, 278, 608, 302, 183, 908, 109, 270, 326, 166, 108, 120, 297, 587, 60, 131, 263, 91, 127, 480, 221, 195, 136, 130, 117, 137, 141, 49, 608, 104, 103, 112, 155, 77, 147, 130, 118, 452, 258, 322, 253, 218, 226, 161, 189, 146, 193, 175, 154, 131, 239, 251, 144, 530, 346, 388, 76, 478, 298, 307, 145, 329, 158, 205, 131, 115, 124, 140, 154, 972, 92, 329, 262, 251, 126, 144, 214, 142, 504, 125, 183, 116, 53, 103, 493, 200, 661, 46, 162, 412, 200, 123, 159, 142, 753, 186, 140, 399, 205, 57, 131, 380, 461, 405, 263, 89, 294, 224, 378, 244, 87, 53, 474, 238, 179, 131, 645, 259, 136, 283, 116, 35, 26, 68, 153, 544, 436, 213, 548, 118, 265, 202, 134, 52, 280, 416, 471, 44, 158, 403, 127, 50, 63, 591, 155, 197, 129, 184, 338, 191, 271, 200, 392, 224, 133, 177, 477, 123, 363, 285, 115, 117, 44, 123, 211, 145, 153, 128, 185, 70, 296, 167, 152, 211, 654, 87, 365, 119, 134, 83, 176, 327, 695, 181, 451, 138, 328, 139, 170, 187, 120, 186, 218, 231, 254, 128, 270, 129, 134, 142, 120, 110, 126, 317, 186, 61, 133, 356, 332, 206, 775, 217, 136, 122, 192, 169, 660, 176, 255, 142, 813, 258, 129, 108, 128, 215, 164, 265, 182, 98, 58, 338, 120, 484, 724, 63, 516, 235, 600, 149, 131, 281, 82, 210, 192, 117, 134, 100, 272, 1014, 96, 143, 392, 250, 194, 125, 518, 110, 183, 293, 259, 126, 156, 393, 1376, 218, 748, 157, 245, 331, 42, 125, 104, 243, 687, 379, 204, 97, 116, 381, 85, 117, 146, 214, 376, 256, 154, 114, 581, 292, 771, 267, 365, 64, 313, 232, 283, 130, 77, 161, 121, 295, 85, 111, 101, 158, 330, 296, 119, 153, 224, 299, 213, 137, 239, 420, 519, 183, 164, 139, 279, 46, 367, 200, 175, 306, 219, 163, 75, 148, 119, 113, 167, 242, 112, 122, 175, 100, 412, 457, 313, 259, 127, 175, 349, 308, 88, 186, 97, 507, 143, 241, 139, 275, 344, 163, 153, 83, 618, 361, 161, 119, 137, 160, 316, 145, 169, 200, 96, 324, 189, 272, 169, 164, 140, 133, 108, 181, 291, 57, 263, 135, 572, 381, 129, 185, 278, 123, 702, 427, 138, 115, 30, 262, 486, 262, 460, 179, 37, 221, 234, 1006, 39, 115, 120, 87, 1147, 97, 225, 125, 511, 169, 319, 114, 291, 155, 108, 169, 133, 179, 237, 353, 823, 118, 174, 282, 166, 196, 363, 242, 413, 104, 149, 142, 456, 622, 168, 121, 341, 110, 320, 86, 120, 114, 321, 118, 983, 282, 141, 41, 168, 170, 187, 179, 128, 298, 142, 715, 134, 102, 300, 657, 146, 123, 263, 88, 106, 129, 139, 490, 234, 249, 961, 181, 525, 197, 143, 317, 367, 143, 759, 428, 137, 120, 174, 166, 138, 171, 180, 194, 122, 202, 192, 126, 88, 200, 331, 850, 154, 411, 149, 289, 129, 685, 406, 140, 128, 173, 166, 54, 159, 170, 400, 266, 130, 209, 102, 242, 47, 168, 138, 128, 650, 236, 162, 112, 144, 207, 368, 47, 199, 146, 762, 310, 280, 79, 130, 274, 113, 163, 151, 345, 253, 59, 129, 293, 123, 266, 168, 170, 595, 247, 215, 266, 143, 155, 298, 42, 201, 184, 286, 342, 126, 61, 135, 188, 158, 617, 120, 106, 36, 140, 93, 133, 198, 141, 295, 473, 124, 163, 59, 142, 928, 314, 66, 136, 159, 703, 460, 403, 117, 119, 75, 212, 168, 119, 505, 97, 188, 206, 147, 159, 560, 221, 143, 91, 235, 171, 174, 874, 306, 101, 173, 167, 201, 361, 389, 622, 63, 281, 705, 123, 153, 138, 101, 245, 206, 187, 247, 230, 142, 109, 104, 199, 116, 192, 266, 86, 128, 129, 525, 177, 187, 65, 127, 710, 235, 996, 135, 404, 72, 206, 140, 260, 295, 354, 342, 212, 170, 224, 119, 306, 451, 31, 138, 92, 65, 120, 133, 300, 146, 136, 696, 53, 346, 452, 125, 112, 129, 318, 287, 159, 129, 330, 242, 169, 215, 203, 110, 129, 262, 156, 262, 117, 194, 168, 124, 274, 799, 143, 471, 108, 289, 217, 105, 168, 44, 210, 194, 429, 208, 301, 347, 157, 253, 124, 111, 225, 263, 158, 43, 208, 125, 92, 297, 174, 181, 125, 415, 139, 436, 120, 146, 274, 114, 243, 157, 410, 206, 135, 120, 314, 144, 180, 153, 53, 312, 184, 137, 474, 355, 116, 306, 169, 168, 285, 101, 130, 82, 86, 117, 168, 123, 60, 175, 151, 202, 148, 297, 217, 93, 490, 103, 828, 94, 130, 145, 127, 167, 177, 68, 813, 141, 111, 117, 43, 119, 169, 111, 183, 54, 42, 269, 189, 136, 643, 263, 289, 181, 97, 60, 429, 122, 116, 461, 71, 136, 372, 436, 145, 230, 188, 195, 216, 87, 148, 456, 127, 138, 514, 701, 165, 299, 41, 200, 307, 468, 544, 93, 118, 561, 147, 154, 160, 239, 137, 118, 124, 337, 310, 285, 201, 134, 527, 116, 199, 139, 583, 201, 207, 118, 613, 108, 260, 171, 193, 109, 187, 350, 179, 88, 426, 128, 45, 130, 245, 235, 513, 136, 313, 315, 461, 192, 266, 141, 198, 80, 125, 259, 187, 142, 198, 356, 128, 161, 228, 206, 335, 280, 123, 104, 105, 38, 84, 107, 470, 195, 471, 47, 182, 230, 169, 781, 117, 144, 318, 144, 887, 146, 363, 61, 900, 177, 690, 619, 146, 674, 161, 121, 219, 247, 433, 35, 192, 211, 219, 239, 304, 808, 139, 205, 194, 299, 148, 113, 230, 58, 204, 168, 461, 147, 174, 142, 282, 454, 146, 226, 988, 212, 285, 393, 137, 120, 155, 228, 113, 159, 219, 307, 201, 174, 176, 166, 393, 80, 338, 335, 94, 42, 112, 345, 200, 593, 108, 121, 171, 230, 255, 458, 200, 385, 448, 565, 473, 101, 60, 320, 237, 154, 297, 181, 190, 375, 1192, 121, 430, 160, 156, 67, 50, 320, 40, 438, 562, 130, 152, 59, 35, 138, 149, 659, 974, 124, 154, 331, 130, 277, 229, 110, 268, 398, 396, 122, 124, 234, 114, 325, 269, 140, 296, 68, 209, 109, 58, 607, 100, 79, 45, 44, 119, 121, 348, 438, 122, 97, 300, 208, 251, 66, 50, 173, 108, 129, 128, 117, 132, 169, 170, 485, 185, 193, 170, 108, 61, 308, 108, 115, 102, 48, 126, 163, 160, 129, 153, 164, 181, 290, 122, 98, 151, 44, 229, 401, 51, 844, 188, 152, 123, 314, 186, 167, 65, 131, 27, 130, 133, 197, 124, 129, 184, 56, 79, 268, 149, 131, 289, 61, 161, 212, 116, 177, 590, 140, 93, 139, 367, 230, 126, 340, 338, 408, 373, 546, 176, 250, 182, 143, 143, 332, 172, 544, 285, 251, 408, 156, 193, 275, 90, 144, 111, 340, 325, 170, 141, 189, 267, 213, 119, 86, 275, 140, 471, 130, 1008, 126, 243, 218, 588, 184, 120, 892, 89, 220, 139, 67, 940, 226, 130, 247, 857, 47, 157, 299, 184, 157, 195, 135, 275, 199, 33, 118, 380, 137, 153, 166, 199, 128, 148, 444, 272, 122, 129, 715, 218, 174, 59, 97, 232, 169, 117, 162, 183, 84, 122, 210, 147, 117, 201, 129, 148, 122, 178, 162, 143, 156, 20, 175, 141, 66, 107, 133, 183, 236, 141, 234, 83, 128, 180, 121, 66, 447, 418, 193, 825, 189, 394, 158, 164, 250, 236, 317, 426, 43, 215, 151, 182, 253, 278, 288, 237, 393, 223, 139, 30, 238, 91, 126, 152, 166, 120, 201, 143, 517, 179, 64, 233, 239, 471, 178, 160, 141, 101, 556, 433, 414, 189, 158, 119, 397, 617, 419, 136, 131, 274, 202, 171, 188, 153, 131, 230, 219, 95, 142, 241, 212, 176, 135, 412, 125, 438, 173, 169, 63, 332, 158, 355, 134, 198, 122, 173, 204, 150, 134, 528, 256, 165, 221, 242, 164, 139, 301, 65, 240, 171, 225, 175, 409, 239, 669, 342, 190, 125, 68, 110, 127, 52, 343, 110, 143, 143, 575, 335, 203, 251, 262, 133, 195, 212, 210, 125, 308, 123, 217, 106, 89, 317, 384, 461, 77, 55, 102, 255, 150, 976, 410, 168, 146, 189, 105, 417, 140, 351, 139, 131, 284, 250, 207, 36, 65, 832, 313, 419, 493, 263, 419, 341, 272, 554, 298, 121, 168, 359, 147, 115, 308, 128, 445, 197, 285, 159, 449, 804, 469, 207, 384, 656, 254, 123, 173, 126, 484, 450, 78, 156, 219, 95, 108, 222, 138, 375, 122, 147, 533, 421, 138, 133, 146, 55, 205, 459, 107, 492, 164, 179, 615, 204, 750, 194, 146, 179, 250, 665, 274, 331, 365, 116, 314, 117, 88, 208, 271, 126, 119, 379, 180, 287, 283, 311, 196, 328, 486, 119, 254, 141, 75, 247, 217, 156, 199, 177, 164, 433, 540, 185, 161, 340, 575, 577, 401, 134, 122, 51, 156, 127, 101, 138, 121, 123, 71, 114, 52, 541, 493, 153, 336, 407, 234, 610, 335, 111, 832, 90, 213, 685, 153, 133, 229, 230, 292, 198, 34, 81, 242, 184, 205, 67, 176, 123, 164, 190, 142, 71, 90, 291, 251, 145, 317, 155, 49, 279, 230, 121, 311, 266, 133, 123, 227, 262, 171, 485, 330, 199, 199, 395, 390, 149, 165, 140, 48, 218, 172, 125, 138, 131, 128, 413, 144, 179, 346, 77, 151, 140, 530, 14, 78, 76, 243, 218, 112, 179, 163, 173, 73, 280, 125, 115, 454, 83, 226, 170, 126, 607, 185, 241, 189, 413, 182, 170, 154, 155, 150, 111, 151, 183, 187, 201, 101, 767, 124, 179, 96, 232, 92, 57, 185, 118, 235, 164, 182, 500, 106, 42, 144, 197, 159, 485, 122, 130, 106, 138, 114, 494, 542, 130, 124, 622, 294, 190, 129, 116, 116, 189, 133, 119, 206, 117, 471, 142, 314, 747, 169, 626, 128, 383, 158, 270, 56, 602, 294, 721, 150, 109, 186, 436, 266, 233, 771, 264, 186, 69, 109, 370, 544, 240, 130, 267, 154, 47, 545, 140, 54, 140, 173, 267, 123, 614, 266, 381, 268, 56, 359, 254, 313, 403, 82, 189, 146, 257, 132, 30, 108, 111, 125, 48, 173, 221, 635, 695, 141, 188, 107, 112, 216, 136, 161, 274, 119, 61, 102, 510, 59, 546, 154, 309, 134, 261, 403, 164, 137, 100, 134, 219, 127, 712, 174, 210, 207, 410, 211, 75, 122, 81, 150, 49, 486, 638, 154, 162, 165, 135, 141, 54, 211, 838, 296, 410, 124, 266, 300, 472, 131, 155, 128, 331, 154, 116, 227, 226, 74, 221, 233, 211, 458, 553, 386, 196, 190, 274, 111, 230, 151, 92, 360, 147, 166, 178, 283, 120, 146, 208, 245, 278, 414, 121, 123, 156, 426, 464, 142, 135, 554, 294, 215, 504, 296, 136, 182, 81, 276, 187, 144, 390, 151, 90, 257, 481, 228, 107, 581, 162, 61, 131, 170, 164, 168, 245, 176, 99, 132, 429, 133, 155, 178, 204, 166, 111, 187, 287, 151, 121, 341, 221, 993, 615, 635, 122, 439, 348, 230, 173, 150, 166, 93, 220, 135, 144, 181, 203, 129, 223, 230, 155, 446, 979, 301, 62, 347, 393, 129, 41, 432, 226, 193, 70, 139, 235, 424, 174, 104, 410, 122, 59, 120, 95, 80, 169, 185, 399, 99, 122, 88, 410, 221, 134, 95, 159, 56, 169, 158, 147, 307, 126, 490, 459, 74, 100, 279, 390, 139, 160, 126, 206, 29, 196, 131, 182, 201, 170, 90, 232, 115, 239, 381, 157, 540, 156, 142, 180, 168, 161, 128, 225, 111, 119, 163, 160, 583, 157, 156, 386, 164, 220, 124, 137, 173, 312, 157, 394, 118, 68, 119, 100, 563, 439, 120, 324, 228, 241, 135, 135, 366, 68, 238, 518, 207, 86, 532, 135, 124, 182, 109, 151, 137, 219, 231, 243, 70, 54, 986, 339, 185, 226, 67, 172, 214, 150, 181, 144, 320, 85, 481, 183, 128, 180, 95, 368, 118, 179, 174, 303, 66, 132, 281, 188, 372, 223, 394, 291, 323, 61, 57, 110, 136, 198, 136, 151, 171, 86, 112, 171, 168, 296, 442, 121, 372, 453, 335, 73, 275, 32, 352, 83, 143, 256, 389, 179, 378, 137, 350, 169, 272, 49, 249, 127, 296, 338, 575, 264, 66, 126, 1010, 129, 178, 130, 331, 80, 124, 481, 131, 49, 261, 581, 136, 176, 256, 138, 170, 99, 153, 196, 134, 248, 128, 228, 58, 135, 497, 261, 123, 171, 181, 169, 119, 162, 111, 138, 128, 258, 545, 136, 282, 197, 122, 534, 300, 117, 112, 228, 170, 155, 243, 212, 127, 149, 138, 182, 187, 442, 256, 112, 139, 122, 164, 247, 165, 218, 300, 188, 288, 342, 155, 108, 211, 164, 476, 366, 496, 92, 482, 315, 109, 363, 746, 186, 769, 116, 127, 96, 117, 130, 116, 152, 140, 263, 249, 273, 190, 134, 223, 567, 127, 217, 231, 191, 245, 177, 156, 123, 373, 59, 709, 489, 100, 153, 204, 153, 47, 52, 111, 113, 106, 200, 47, 68, 480, 107, 137, 186, 307, 261, 121, 226, 174, 220, 320, 162, 297, 145, 81, 121, 227, 225, 169, 382, 748, 151, 274, 95, 146, 137, 104, 395, 132, 126, 177, 124, 329, 124, 103, 154, 89, 449, 133, 118, 399, 128, 132, 237, 229, 123, 112, 117, 155, 639, 55, 146, 136, 962, 235, 176, 147, 145, 241, 208, 173, 185, 467, 291, 176, 50, 195, 138, 157, 372, 182, 190, 236, 58, 394, 119, 127, 243, 379, 745, 152, 122, 187, 128, 296, 118, 73, 122, 461, 105, 72, 93, 208, 129, 166, 76, 314, 203, 140, 261, 249, 239, 208, 208, 191, 411, 84, 355, 133, 332, 166, 142, 83, 259, 106, 357, 226, 266, 135, 142, 211, 216, 222, 121, 136, 114, 505, 157, 139, 341, 525, 164, 128, 135, 56, 60, 259, 223, 145, 241, 49, 396, 295, 139, 151, 63, 123, 682, 190, 92, 287, 368, 201, 125, 600, 163, 44, 128, 322, 228, 82, 145, 209, 470, 225, 124, 60, 299, 156, 273, 87, 761, 362, 342, 253, 206, 358, 254, 924, 271, 233, 43, 90, 360, 461, 428, 302, 686, 224, 170, 190, 124, 674, 170, 159, 113, 113, 131, 145, 120, 136, 120, 428, 31, 387, 91, 456, 188, 184, 534, 387, 304, 140, 82, 387, 127, 118, 353, 115, 178, 588, 429, 253, 448, 129, 73, 207, 186, 616, 144, 243, 186, 341, 120, 193, 88, 87, 49, 588, 290, 253, 285, 174, 321, 418, 155, 80, 156, 480, 111, 825, 155, 300, 139, 196, 139, 146, 196, 166, 249, 308, 160, 259, 70, 312, 135, 53, 150, 88, 422, 140, 132, 110, 1015, 284, 104, 187, 162, 849, 137, 278, 194, 170, 167, 340, 94, 611, 104, 226, 332, 132, 200, 154, 114, 64, 554, 333, 156, 441, 251, 140, 253, 90, 385, 179, 120, 266, 28, 110, 77, 52, 193, 115, 300, 271, 121, 474, 81, 120, 143, 298, 159, 136, 117, 190, 273, 194, 206, 552, 191, 121, 307, 122, 215, 131, 231, 230, 253, 194, 262, 130, 610, 750, 43, 311, 218, 411, 109, 122, 164, 134, 200, 306, 124, 913, 40, 147, 452, 123, 249, 128, 199, 188, 234, 180, 323, 57, 323, 310, 75, 144, 139, 232, 115, 183, 187, 315, 67, 64, 301, 188, 189, 790, 335, 43, 114, 193, 32, 408, 377, 70, 389, 197, 158, 309, 317, 169, 977, 49, 188, 283, 218, 134, 69, 138, 700, 339, 131, 116, 279, 195, 156, 39, 104, 123, 111, 271, 160, 173, 186, 122, 291, 248, 205, 150, 423, 360, 212, 157, 244, 202, 140, 236, 201, 164, 212, 117, 302, 124, 98, 202, 184, 158, 145, 139, 71, 927, 222, 284, 303, 217, 160, 202, 114, 473, 112, 98, 253, 114, 445, 331, 200, 215, 171, 66, 323, 118, 786, 49, 129, 385, 200, 187, 193, 94, 79, 71, 156, 789, 99, 199, 107, 733, 152, 116, 121, 113, 625, 205, 111, 223, 607, 547, 805, 165, 43, 151, 173, 216, 211, 197, 130, 125, 62, 191, 530, 138, 210, 377, 214, 185, 139, 138, 559, 262, 146, 118, 60, 174, 204, 156, 295, 152, 114, 65, 156, 119, 119, 128, 173, 175, 146, 65, 180, 269, 201, 150, 77, 144, 186, 719, 107, 154, 154, 516, 282, 130, 409, 103, 161, 331, 332, 157, 269, 179, 164, 439, 185, 230, 59, 331, 123, 692, 70, 205, 154, 320, 111, 552, 84, 272, 285, 170, 210, 48, 205, 459, 400, 123, 71, 281, 321, 126, 167, 190, 481, 109, 246, 87, 207, 119, 707, 119, 246, 120, 136, 391, 246, 133, 154, 123, 136, 152, 181, 143, 98, 182, 436, 67, 122, 91, 99, 102, 195, 319, 917, 261, 273, 160, 197, 149, 229, 170, 191, 113, 440, 154, 735, 304, 126, 50, 424, 175, 263, 289, 239, 262, 58, 908, 230, 140, 433, 234, 119, 79, 159, 125, 153, 122, 993, 122, 173, 159, 430, 160, 146, 120, 232, 372, 89, 166, 180, 85, 133, 93, 220, 343, 149, 120, 602, 156, 160, 352, 60, 100, 101, 146, 143, 549, 219, 618, 139, 260, 114, 137, 131, 172, 142, 114, 143, 202, 121, 164, 233, 208, 162, 142, 323, 227, 249, 267, 257, 255, 172, 107, 208, 269, 44, 78, 188, 188, 235, 143, 361, 193, 249, 325, 147, 212, 702, 329, 333, 128, 144, 235, 132, 229, 154, 244, 97, 148, 268, 122, 172, 95, 373, 133, 137, 139, 641, 78, 132, 114, 120, 177, 353, 372, 115, 185, 97, 174, 137, 76, 57, 357, 45, 297, 256, 148, 192, 605, 138, 215, 188, 139, 111, 446, 191, 162, 138, 117, 157, 127, 149, 57, 145, 122, 113, 421, 199, 81, 314, 101, 138, 123, 103, 97, 154, 348, 143, 681, 308, 131, 177, 174, 247, 103, 171, 65, 151, 144, 158, 134, 179, 122, 137, 309, 363, 201, 376, 225, 135, 113, 565, 217, 129, 404, 168, 200, 442, 138, 156, 156, 69, 152, 169, 994, 190, 194, 131, 143, 57, 196, 169, 161, 201, 259, 110, 207, 149, 116, 143, 302, 54, 556, 163, 998, 137, 259, 145, 322, 148, 307, 313, 117, 150, 165, 123, 179, 305, 153, 435, 222, 79, 164, 506, 191, 90, 91, 56, 228, 216, 265, 442, 179, 311, 149, 186, 49, 147, 228, 112, 162, 121, 481, 166, 366, 107, 603, 111, 146, 142, 137, 273, 184, 73, 167, 152, 120, 180, 258, 167, 337, 520, 141, 108, 116, 122, 73, 473, 135, 376, 138, 42, 286, 118, 119, 104, 111, 119, 109, 119, 131, 188, 307, 135, 175, 141, 308, 104, 693, 220, 495, 317, 141, 849, 117, 122, 484, 108, 243, 389, 209, 425, 122, 342, 128, 169, 17, 457, 158, 145, 931, 94, 289, 201, 304, 353, 108, 179, 392, 105, 191, 138, 416, 55, 300, 142, 142, 224, 158, 97, 78, 119, 461, 124, 278, 466, 142, 70, 130, 148, 378, 150, 121, 221, 198, 166, 154, 76, 49, 67, 226, 138, 219, 467, 167, 151, 320, 169, 182, 49, 79, 128, 175, 152, 328, 261, 56, 489, 177, 599, 108, 212, 1000, 106, 444, 267, 586, 126, 241, 189, 378, 136, 311, 161, 170, 186, 393, 452, 299, 99, 201, 171, 115, 364, 437, 291, 125, 124, 205, 179, 141, 171, 142, 356, 232, 134, 174, 98, 109, 152, 169, 288, 121, 208, 220, 152, 121, 90, 125, 424, 149, 182, 118, 222, 146, 121, 261, 76, 157, 255, 127, 407, 193, 155, 156, 703, 999, 750, 77, 327, 139, 104, 110, 111, 24, 269, 169, 287, 95, 188, 470, 125, 464, 116, 162, 195, 138, 131, 714, 479, 133, 1004, 143, 391, 168, 49, 999, 393, 431, 667, 109, 182, 59, 133, 178, 523, 215, 153, 170, 351, 182, 128, 217, 119, 168, 161, 132, 201, 714, 56, 113, 137, 445, 42, 186, 164, 55, 126, 304, 210, 519, 482, 213, 537, 238, 248, 125, 133, 335, 280, 93, 637, 156, 129, 478, 218, 73, 100, 148, 124, 266, 211, 138, 166, 142, 103, 372, 134, 93, 93, 225, 148, 122, 71, 82, 431, 250, 258, 219, 396, 149, 379, 155, 162, 10, 128, 337, 248, 120, 117, 314, 253, 124, 226, 118, 120, 167, 527, 168, 113, 291, 174, 295, 121, 185, 89, 497, 121, 375, 459, 153, 252, 165, 198, 159, 301, 110, 122, 252, 169, 284, 130, 228, 196, 166, 187, 188, 220, 35, 143, 187, 129, 153, 178, 399, 415, 406, 417, 298, 322, 353, 157, 430, 213, 249, 270, 229, 227, 565, 166, 159, 142, 134, 59, 164, 1830, 145, 151, 197, 110, 80, 148, 154, 117, 249, 111, 258, 128, 398, 140, 167, 141, 291, 132, 82, 48, 576, 143, 471, 179, 127, 741, 189, 124, 222, 133, 169, 527, 251, 223, 175, 122, 105, 171, 416, 191, 70, 165, 155, 625, 193, 92, 513, 154, 132, 108, 155, 137, 121, 348, 338, 132, 136, 122, 136, 67, 249, 241, 443, 420, 209, 145, 630, 995, 359, 582, 448, 253, 130, 713, 407, 128, 156, 168, 459, 177, 264, 132, 205, 270, 483, 324, 192, 567, 172, 178, 134, 448, 482, 197, 83, 44, 239, 173, 555, 120, 150, 449, 133, 145, 198, 157, 127, 50, 686, 282, 330, 194, 903, 597, 163, 578, 370, 113, 145, 239, 154, 169, 201, 140, 957, 175, 175, 128, 413, 203, 432, 312, 101, 36, 170, 585, 124, 169, 267, 358, 181, 149, 532, 326, 180, 192, 315, 125, 333, 155, 112, 495, 122, 127, 117, 482, 217, 217, 378, 199, 158, 194, 347, 90, 880, 1001, 206, 75, 140, 167, 76, 72, 144, 123, 136, 278, 134, 141, 123, 506, 54, 146, 128, 119, 409, 390, 263, 328, 141, 161, 133, 457, 117, 71, 305, 251, 210, 440, 96, 45, 361, 393, 192, 125, 181, 46, 282, 713, 297, 202, 211, 459, 230, 177, 1000, 893, 140, 123, 209, 221, 218, 162, 142, 188, 142, 208, 219, 462, 108, 93, 104, 169, 559, 627, 148, 180, 193, 107, 355, 132, 265, 300, 817, 169, 290, 364, 150, 114, 64, 247, 291, 134, 264, 131, 264, 204, 52, 141, 125, 164, 180, 164, 172, 97, 811, 99, 47, 124, 300, 83, 138, 134, 114, 998, 282, 112, 131, 187, 468, 144, 320, 405, 178, 996, 134, 79, 130, 356, 81, 410, 61, 157, 70, 171, 791, 739, 597, 160, 200, 72, 190, 294, 119, 159, 132, 181, 312, 85, 198, 154, 170, 180, 193, 580, 584, 141, 326, 285, 366, 244, 139, 145, 186, 296, 228, 107, 154, 295, 217, 105, 213, 142, 429, 55, 151, 121, 135, 158, 166, 115, 85, 61, 519, 404, 238, 147, 102, 563, 269, 182, 245, 74, 150, 380, 135, 234, 170, 249, 538, 61, 68, 135, 432, 158, 268, 242, 54, 112, 151, 575, 559, 80, 263, 142, 277, 74, 170, 121, 280, 485, 515, 161, 126, 177, 209, 188, 953, 105, 59, 69, 370, 584, 161, 382, 138, 136, 167, 131, 107, 185, 82, 572, 415, 157, 58, 414, 106, 174, 479, 134, 121, 267, 122, 131, 518, 162, 80, 132, 147, 105, 234, 119, 216, 156, 239, 133, 199, 315, 146, 643, 976, 137, 99, 105, 274, 61, 186, 244, 305, 47, 243, 352, 420, 202, 188, 121, 202, 299, 328, 227, 668, 426, 116, 107, 99, 251, 64, 312, 202, 355, 111, 160, 174, 140, 819, 431, 109, 148, 334, 189, 140, 167, 214, 207, 122, 202, 70, 179, 1000, 212, 113, 124, 129, 383, 142, 127, 161, 104, 234, 140, 119, 191, 405, 626, 751, 586, 269, 140, 130, 250, 228, 123, 388, 47, 361, 405, 188, 361, 155, 370, 127, 315, 91, 172, 155, 200, 109, 298, 441, 57, 102, 396, 88, 157, 117, 486, 153, 141, 157, 183, 303, 133, 269, 168, 412, 330, 171, 37, 244, 276, 180, 138, 138, 289, 131, 91, 349, 112, 76, 344, 375, 642, 150, 199, 744, 395, 274, 292, 154, 231, 229, 124, 110, 43, 113, 378, 177, 92, 300, 55, 468, 110, 130, 39, 97, 158, 87, 120, 248, 184, 140, 163, 191, 170, 144, 256, 133, 123, 264, 70, 127, 363, 79, 60, 196, 525, 549, 384, 164, 178, 141, 236, 233, 180, 64, 176, 114, 440, 189, 371, 150, 285, 73, 141, 279, 111, 160, 612, 724, 102, 377, 153, 244, 211, 78, 258, 636, 240, 631, 556, 301, 314, 410, 221, 1839, 232, 140, 149, 395, 363, 163, 178, 192, 109, 109, 303, 287, 66, 49, 134, 244, 146, 745, 83, 247, 161, 152, 291, 186, 134, 34, 748, 435, 54, 110, 534, 90, 138, 211, 157, 119, 215, 133, 124, 127, 471, 79, 67, 274, 528, 123, 246, 213, 86, 54, 133, 465, 96, 178, 276, 251, 115, 305, 340, 97, 141, 166, 135, 95, 245, 123, 337, 198, 187, 486, 299, 244, 263, 116, 321, 177, 95, 92, 136, 136, 197, 157, 157, 181, 261, 188, 269, 161, 596, 173, 118, 356, 199, 437, 112, 129, 272, 41, 128, 832, 86, 329, 108, 131, 190, 109, 145, 517, 450, 154, 89, 635, 404, 726, 160, 121, 56, 426, 393, 313, 235, 526, 364, 101, 144, 165, 256, 316, 508, 128, 403, 171, 219, 277, 720, 172, 46, 201, 134, 60, 304, 104, 142, 230, 702, 585, 373, 159, 234, 127, 56, 129, 76, 56, 178, 149, 157, 78, 191, 174, 78, 175, 465, 215, 613, 24, 140, 148, 124, 137, 367, 587, 341, 61, 81, 132, 149, 216, 427, 155, 190, 122, 249, 126, 498, 131, 127, 151, 74, 108, 256, 179, 420, 127, 134, 231, 180, 134, 204, 353, 132, 214, 439, 193, 239, 241, 102, 292, 469, 107, 241, 477, 211, 145, 132, 257, 109, 66, 263, 239, 221, 350, 58, 86, 202, 108, 39, 607, 178, 245, 164, 641, 59, 77, 357, 151, 130, 520, 501, 114, 159, 172, 325, 53, 135, 92, 101, 635, 129, 112, 377, 569, 196, 261, 127, 194, 174, 59, 100, 111, 169, 145, 109, 128, 227, 999, 334, 279, 333, 138, 210, 379, 293, 110, 112, 249, 235, 201, 124, 45, 419, 111, 135, 73, 153, 126, 290, 175, 190, 328, 117, 267, 231, 76, 183, 379, 81, 40, 143, 135, 370, 116, 72, 189, 334, 185, 173, 139, 526, 122, 204, 667, 611, 137, 302, 987, 219, 112, 161, 111, 142, 182, 255, 204, 587, 181, 169, 322, 65, 246, 673, 898, 298, 133, 90, 165, 168, 485, 117, 129, 271, 114, 287, 409, 209, 196, 174, 111, 101, 122, 133, 116, 316, 358, 465, 136, 115, 151, 596, 150, 100, 177, 356, 144, 126, 454, 819, 128, 122, 114, 410, 250, 129, 138, 165, 321, 109, 559, 595, 118, 156, 117, 132, 82, 203, 119, 382, 140, 366, 337, 137, 115, 163, 173, 80, 212, 271, 111, 253, 400, 121, 346, 131, 602, 227, 315, 224, 249, 211, 157, 318, 157, 278, 161, 175, 606, 87, 535, 270, 166, 424, 229, 316, 146, 362, 229, 219, 503, 186, 288, 280, 193, 175, 534, 383, 168, 132, 156, 153, 103, 205, 223, 144, 289, 691, 46, 165, 133, 322, 264, 141, 120, 127, 124, 83, 77, 156, 771, 427, 129, 340, 129, 184, 69, 533, 449, 103, 66, 266, 239, 133, 259, 126, 113, 53, 158, 289, 241, 245, 625, 191, 169, 140, 293, 134, 124, 399, 591, 202, 470, 150, 427, 149, 148, 231, 110, 209, 454, 507, 311, 310, 363, 252, 198, 313, 233, 75, 369, 338, 201, 197, 134, 126, 117, 688, 130, 185, 163, 262, 123, 130, 64, 124, 255, 238, 785, 430, 181, 233, 116, 119, 129, 280, 238, 45, 43, 220, 100, 129, 139, 146, 224, 160, 303, 321, 129, 514, 157, 646, 377, 166, 90, 153, 81, 244, 966, 164, 148, 300, 184, 287, 328, 146, 258, 117, 291, 121, 146, 182, 557, 347, 118, 41, 510, 207, 120, 83, 594, 63, 159, 80, 113, 360, 133, 117, 48, 133, 142, 287, 141, 163, 259, 61, 242, 118, 165, 262, 301, 169, 133, 124, 158, 136, 354, 213, 139, 141, 153, 125, 483, 169, 179, 525, 129, 280, 139, 210, 162, 124, 100, 951, 139, 735, 133, 257, 947, 320, 81, 251, 122, 528, 39, 144, 306, 143, 119, 357, 125, 213, 241, 113, 350, 482, 779, 997, 136, 85, 167, 545, 131, 923, 63, 329, 231, 211, 143, 136, 274, 106, 203, 405, 676, 149, 231, 340, 84, 843, 321, 239, 125, 390, 188, 101, 126, 173, 94, 143, 162, 126, 113, 126, 335, 126, 247, 130, 363, 372, 144, 713, 126, 199, 196, 919, 74, 107, 115, 189, 967, 124, 122, 171, 458, 185, 384, 995, 175, 136, 212, 506, 125, 351, 150, 643, 229, 325, 322, 101, 104, 133, 218, 624, 54, 373, 135, 242, 117, 66, 221, 282, 114, 612, 158, 115, 246, 157, 235, 437, 158, 171, 117, 92, 82, 287, 174, 126, 406, 730, 220, 194, 49, 92, 233, 228, 125, 354, 193, 226, 87, 246, 374, 350, 162, 211, 107, 196, 282, 717, 768, 150, 206, 188, 126, 90, 791, 373, 49, 788, 205, 185, 41, 410, 354, 140, 202, 254, 77, 992, 132, 127, 242, 144, 179, 145, 135, 120, 174, 146, 556, 156, 447, 225, 377, 129, 418, 312, 469, 136, 169, 193, 122, 586, 122, 199, 176, 113, 333, 158, 123, 270, 201, 531, 229, 124, 234, 161, 56, 249, 275, 221, 141, 123, 300, 225, 467, 180, 218, 352, 131, 132, 326, 247, 77, 122, 144, 118, 402, 117, 453, 348, 158, 207, 223, 138, 140, 44, 511, 147, 238, 197, 143, 156, 235, 249, 476, 427, 372, 440, 257, 124, 51, 46, 102, 124, 272, 135, 194, 247, 639, 107, 190, 136, 102, 120, 168, 149, 46, 87, 681, 189, 390, 65, 406, 310, 178, 193, 795, 89, 134, 140, 216, 382, 362, 317, 183, 280, 441, 180, 123, 512, 339, 114, 163, 115, 144, 298, 232, 168, 130, 318, 426, 61, 428, 39, 123, 142, 168, 113, 123, 101, 252, 167, 467, 115, 134, 331, 153, 64, 250, 140, 147, 158, 124, 162, 120, 172, 367, 206, 289, 114, 115, 295, 693, 111, 133, 195, 198, 76, 145, 123, 121, 160, 222, 68, 388, 259, 135, 158, 466, 177, 520, 311, 57, 227, 181, 156, 186, 335, 504, 121, 273, 198, 104, 393, 964, 164, 160, 243, 285, 118, 949, 59, 151, 237, 140, 132, 75, 78, 133, 114, 158, 129, 354, 123, 145, 217, 171, 384, 400, 130, 50, 111, 133, 73, 119, 206, 700, 191, 70, 591, 365, 873, 318, 193, 60, 171, 281, 220, 168, 297, 138, 173, 260, 169, 151, 107, 114, 171, 431, 135, 122, 153, 375, 268, 54, 222, 125, 495, 139, 317, 323, 64, 838, 61, 126, 119, 192, 261, 228, 178, 229, 95, 132, 43, 285, 155, 111, 109, 341, 75, 126, 136, 79, 127, 196, 464, 129, 456, 156, 200, 505, 100, 845, 203, 96, 117, 128, 263, 130, 116, 187, 112, 243, 153, 166, 147, 146, 201, 45, 196, 137, 123, 184, 193, 123, 188, 70, 745, 207, 178, 459, 302, 74, 180, 453, 801, 172, 123, 420, 169, 146, 367, 226, 138, 126, 69, 370, 649, 187, 110, 169, 275, 149, 204, 228, 196, 116, 272, 330, 142, 190, 145, 192, 132, 312, 190, 96, 147, 99, 156, 144, 156, 132, 131, 220, 152, 267, 69, 159, 98, 142, 133, 306, 183, 178, 42, 227, 94, 144, 129, 268, 149, 137, 54, 63, 151, 645, 981, 257, 121, 175, 457, 167, 92, 133, 55, 82, 421, 142, 94, 528, 149, 134, 113, 94, 156, 171, 168, 640, 118, 205, 150, 144, 384, 172, 28, 234, 236, 135, 204, 48, 108, 131, 139, 396, 326, 168, 327, 104, 40, 225, 111, 75, 127, 387, 218, 208, 115, 128, 165, 199, 250, 55, 438, 50, 355, 318, 237, 132, 130, 575, 271, 48, 207, 245, 118, 203, 127, 47, 150, 118, 64, 104, 109, 163, 106, 160, 117, 147, 219, 194, 452, 170, 537, 208, 301, 91, 121, 120, 143, 228, 126, 487, 114, 141, 224, 12, 153, 218, 149, 173, 171, 961, 175, 628, 201, 199, 236, 206, 236, 72, 114, 164, 59, 314, 114, 118, 203, 465, 165, 455, 63, 460, 169, 342, 142, 123, 198, 167, 100, 122, 368, 504, 119, 62, 409, 234, 42, 97, 161, 891, 236, 161, 153, 117, 151, 77, 435, 132, 139, 155, 501, 176, 206, 522, 173, 128, 191, 133, 272, 207, 107, 126, 52, 503, 125, 164, 411, 293, 201, 188, 162, 116, 40, 123, 205, 117, 205, 101, 162, 83, 300, 316, 103, 154, 131, 338, 177, 139, 386, 439, 153, 171, 121, 329, 148, 102, 164, 119, 370, 185, 167, 77, 251, 94, 134, 128, 68, 123, 144, 127, 153, 61, 345, 112, 79, 575, 362, 245, 409, 123, 160, 45, 268, 65, 28, 595, 156, 399, 416, 344, 102, 128, 115, 147, 130, 134, 241, 248, 621, 72, 106, 123, 130, 300, 116, 337, 223, 50, 163, 264, 363, 206, 174, 118, 107, 113, 635, 531, 472, 108, 292, 459, 109, 430, 91, 278, 215, 122, 107, 261, 118, 86, 255, 166, 218, 125, 314, 101, 137, 146, 76, 51, 834, 65, 158, 214, 145, 225, 260, 122, 197, 295, 286, 209, 323, 96, 686, 437, 91, 170, 106, 506, 110, 241, 416, 77, 396, 195, 227, 378, 175, 208, 112, 124, 130, 145, 129, 523, 182, 109, 183, 141, 104, 116, 151, 339, 284, 167, 1364, 195, 315, 210, 275, 173, 56, 116, 199, 171, 156, 125, 117, 221, 157, 300, 604, 144, 160, 227, 305, 721, 165, 173, 515, 187, 127, 180, 65, 600, 413, 110, 155, 214, 222, 151, 322, 103, 135, 441, 211, 83, 130, 689, 214, 584, 410, 286, 728, 154, 234, 46, 250, 141, 138, 148, 147, 198, 110, 260, 256, 148, 401, 218, 256, 156, 182, 277, 122, 108, 119, 180, 272, 188, 270, 125, 259, 259, 42, 612, 119, 362, 142, 125, 226, 124, 70, 106, 290, 127, 140, 266, 545, 254, 354, 283, 380, 50, 180, 166, 62, 160, 73, 202, 71, 73, 349, 117, 139, 279, 130, 184, 535, 341, 130, 498, 596, 299, 177, 183, 151, 918, 540, 120, 123, 286, 246, 153, 468, 232, 69, 146, 95, 142, 345, 199, 235, 247, 311, 188, 153, 118, 149, 454, 320, 144, 148, 182, 201, 500, 94, 107, 239, 55, 108, 238, 290, 72, 749, 73, 438, 194, 159, 129, 97, 327, 270, 263, 105, 206, 162, 143, 215, 133, 195, 152, 407, 143, 766, 69, 323, 146, 168, 137, 466, 266, 337, 72, 306, 115, 104, 408, 229, 138, 162, 349, 107, 229, 111, 356, 222, 243, 302, 161, 84, 90, 157, 120, 749, 406, 120, 172, 263, 133, 119, 597, 539, 108, 557, 146, 460, 306, 150, 218, 173, 323, 608, 117, 126, 209, 97, 492, 131, 173, 136, 153, 177, 397, 143, 237, 153, 445, 136, 135, 272, 233, 91, 220, 245, 118, 51, 104, 121, 201, 124, 153, 192, 52, 448, 216, 49, 81, 884, 548, 358, 148, 42, 262, 184, 339, 484, 157, 138, 99, 140, 421, 239, 326, 115, 350, 164, 217, 67, 157, 267, 99, 253, 133, 138, 141, 227, 144, 53, 459, 170, 186, 143, 262, 131, 169, 189, 239, 354, 162, 369, 88, 152, 222, 253, 124, 284, 408, 66, 471, 147, 26, 430, 146, 108, 199, 240, 278, 48, 178, 114, 153, 192, 198, 111, 154, 204, 229, 165, 706, 173, 578, 107, 268, 506, 192, 324, 81, 39, 115, 256, 40, 690, 131, 52, 360, 112, 184, 257, 112, 216, 398, 131, 133, 347, 164, 85, 176, 269, 198, 298, 200, 143, 105, 164, 181, 168, 262, 999, 318, 362, 60, 132, 85, 324, 148, 183, 278, 410, 118, 253, 352, 211, 451, 49, 122, 151, 145, 176, 114, 257, 160, 161, 127, 968, 178, 126, 107, 428, 63, 124, 51, 179, 261, 308, 112, 148, 404, 149, 112, 114, 69, 200, 447, 136, 221, 53, 69, 150, 113, 854, 143, 251, 249, 188, 279, 158, 161, 131, 145, 127, 447, 350, 69, 87, 111, 127, 154, 427, 133, 150, 88, 413, 87, 656, 68, 170, 192, 102, 68, 133, 124, 214, 253, 184, 67, 687, 301, 430, 338, 128, 173, 246, 220, 112, 559, 183, 181, 121, 160, 111, 264, 139, 643, 70, 126, 163, 169, 148, 825, 424, 214, 146, 167, 275, 160, 288, 194, 149, 417, 140, 166, 67, 123, 172, 234, 329, 119, 50, 59, 530, 153, 140, 128, 247, 218, 151, 319, 58, 128, 169, 118, 390, 223, 158, 92, 561, 143, 158, 154, 118, 622, 114, 218, 114, 129, 457, 625, 187, 255, 259, 262, 185, 101, 277, 136, 191, 282, 216, 157, 140, 168, 341, 179, 126, 231, 215, 327, 208, 285, 437, 105, 66, 145, 119, 72, 148, 131, 204, 390, 108, 216, 88, 278, 111, 194, 140, 127, 126, 208, 64, 186, 227, 216, 208, 71, 185, 119, 198, 411, 363, 157, 639, 171, 590, 440, 59, 255, 346, 133, 191, 116, 194, 353, 133, 197, 126, 243, 154, 178, 168, 573, 184, 268, 344, 171, 275, 295, 144, 153, 224, 244, 197, 134, 117, 328, 247, 137, 250, 154, 178, 376, 51, 111, 199, 412, 142, 114, 288, 102, 247, 120, 288, 344, 302, 153, 36, 118, 105, 341, 190, 107, 344, 393, 777, 161, 157, 261, 120, 871, 723, 67, 200, 68, 120, 36, 151, 324, 146, 469, 180, 108, 256, 190, 344, 149, 114, 109, 434, 129, 609, 182, 265, 207, 121, 179, 138, 229, 307, 304, 96, 143, 141, 183, 85, 274, 161, 101, 130, 132, 177, 475, 182, 291, 79, 146, 498, 202, 433, 133, 314, 208, 52, 177, 366, 138, 79, 675, 151, 134, 192, 118, 600, 192, 374, 144, 81, 207, 420, 376, 92, 138, 158, 281, 142, 42, 514, 282, 51, 651, 184, 126, 195, 108, 136, 69, 173, 145, 126, 94, 47, 156, 261, 321, 137, 104, 130, 213, 244, 51, 248, 502, 269, 607, 152, 173, 188, 196, 170, 164, 63, 200, 485, 204, 106, 128, 109, 153, 130, 142, 321, 169, 163, 116, 219, 235, 134, 200, 303, 228, 229, 71, 196, 52, 136, 176, 128, 55, 223, 193, 122, 53, 118, 185, 122, 315, 226, 113, 169, 72, 533, 168, 352, 126, 145, 334, 177, 830, 140, 175, 132, 215, 185, 199, 185, 292, 237, 140, 128, 98, 325, 79, 122, 203, 305, 280, 283, 141, 162, 47, 179, 148, 168, 253, 315, 163, 251, 203, 496, 545, 191, 696, 327, 167, 149, 112, 250, 309, 523, 109, 425, 201, 187, 335, 359, 114, 308, 436, 57, 108, 233, 481, 49, 109, 178, 195, 327, 325, 160, 33, 308, 114, 57, 133, 247, 116, 145, 244, 41, 72, 133, 313, 195, 906, 205, 78, 252, 523, 392, 250, 173, 85, 506, 476, 218, 33, 415, 131, 126, 150, 197, 263, 144, 149, 91, 160, 477, 142, 253, 109, 470, 146, 96, 56, 109, 132, 135, 130, 155, 163, 335, 236, 330, 67, 235, 54, 95, 370, 101, 124, 240, 183, 221, 228, 258, 121, 186, 176, 185, 305, 245, 128, 132, 128, 144, 185, 210, 41, 192, 71, 901, 170, 157, 116, 387, 214, 84, 473, 144, 139, 209, 137, 172, 184, 709, 335, 160, 141, 277, 244, 176, 120, 293, 114, 132, 236, 196, 161, 156, 273, 255, 312, 267, 184, 125, 466, 582, 275, 102, 555, 87, 261, 159, 57, 823, 174, 128, 421, 194, 128, 128, 237, 144, 44, 131, 414, 797, 917, 120, 243, 246, 105, 207, 115, 301, 185, 261, 136, 170, 92, 927, 270, 192, 307, 152, 138, 599, 293, 127, 198, 664, 130, 127, 158, 152, 107, 122, 165, 371, 683, 151, 243, 179, 157, 90, 281, 124, 127, 166, 189, 151, 140, 962, 277, 118, 72, 221, 173, 313, 222, 129, 225, 134, 10, 988, 324, 379, 208, 114, 351, 112, 334, 112, 240, 186, 492, 622, 739, 218, 591, 326, 321, 113, 156, 215, 187, 139, 155, 317, 156, 217, 146, 135, 129, 325, 246, 340, 375, 231, 491, 50, 400, 124, 100, 437, 133, 255, 151, 82, 236, 98, 181, 314, 107, 87, 317, 124, 123, 105, 155, 345, 378, 71, 245, 120, 470, 122, 355, 179, 237, 198, 238, 204, 158, 147, 204, 205, 131, 126, 218, 85, 220, 208, 125, 320, 462, 273, 84, 120, 366, 162, 169, 37, 238, 807, 285, 140, 130, 251, 163, 883, 202, 371, 215, 466, 128, 110, 65, 55, 109, 149, 174, 71, 187, 688, 132, 125, 200, 273, 206, 118, 178, 198, 111, 197, 236, 157, 366, 123, 129, 192, 351, 307, 303, 351, 182, 65, 146, 42, 53, 491, 164, 135, 220, 176, 143, 368, 128, 149, 150, 556, 573, 373, 323, 126, 181, 702, 282, 125, 144, 963, 196, 126, 190, 153, 145, 156, 297, 129, 162, 110, 604, 194, 481, 177, 112, 233, 394, 60, 251, 204, 685, 107, 183, 59, 138, 179, 1277, 128, 272, 38, 75, 428, 75, 136, 258, 288, 107, 62, 181, 134, 169, 328, 43, 213, 138, 863, 431, 312, 472, 168, 124, 158, 331, 154, 155, 173, 120, 132, 58, 130, 153, 146, 133, 207, 125, 115, 576, 541, 103, 180, 71, 135, 260, 131, 144, 140, 128, 177, 933, 121, 569, 116, 95, 227, 61, 129, 151, 406, 255, 83, 691, 273, 137, 82, 464, 384, 476, 120, 60, 199, 509, 465, 194, 103, 251, 225, 117, 120, 151, 446, 124, 217, 105, 182, 189, 124, 192, 109, 525, 193, 475, 140, 405, 402, 122, 152, 324, 132, 268, 156, 206, 170, 123, 101, 87, 139, 165, 560, 376, 116, 120, 418, 209, 148, 152, 77, 117, 123, 145, 474, 101, 153, 127, 129, 118, 547, 200, 544, 485, 74, 378, 413, 213, 242, 160, 141, 128, 198, 132, 375, 135, 46, 135, 176, 139, 974, 154, 125, 320, 94, 313, 226, 215, 242, 60, 191, 460, 122, 125, 129, 442, 74, 75, 167, 129, 101, 103, 128, 142, 152, 125, 217, 72, 77, 411, 503, 115, 217, 347, 427, 504, 149, 485, 291, 236, 138, 310, 328, 375, 173, 188, 131, 806, 123, 75, 147, 88, 178, 827, 23, 482, 663, 27, 84, 117, 206, 396, 72, 54, 246, 176, 289, 670, 127, 138, 235, 163, 58, 126, 107, 101, 162, 237, 208, 201, 142, 348, 51, 228, 628, 176, 201, 696, 978, 106, 244, 46, 239, 166, 773, 114, 144, 132, 326, 139, 185, 100, 253, 126, 109, 274, 213, 961, 51, 280, 563, 124, 415, 147, 69, 376, 688, 69, 180, 151, 213, 137, 445, 816, 220, 288, 876, 93, 261, 302, 134, 72, 183, 150, 187, 264, 287, 232, 238, 304, 570, 158, 223, 179, 341, 108, 61, 201, 800, 357, 252, 24, 546, 142, 46, 141, 522, 181, 173, 128, 131, 157, 204, 160, 203, 194, 251, 106, 704, 229, 457, 103, 360, 128, 45, 125, 176, 379, 103, 81, 196, 180, 760, 152, 310, 110, 282, 150, 109, 138, 221, 83, 223, 110, 140, 386, 162, 267, 181, 201, 395, 122, 126, 160, 78, 48, 157, 136, 321, 163, 147, 125, 184, 138, 151, 191, 57, 54, 128, 111, 595, 44, 159, 632, 373, 71, 120, 165, 388, 130, 49, 119, 124, 213, 117, 133, 233, 154, 154, 112, 989, 131, 334, 440, 152, 145, 103, 150, 165, 385, 130, 214, 216, 129, 95, 114, 167, 187, 160, 225, 391, 98, 150, 714, 109, 142, 365, 177, 217, 366, 106, 187, 112, 506, 264, 59, 441, 314, 130, 133, 398, 90, 155, 61, 406, 473, 195, 235, 125, 459, 194, 120, 295, 877, 143, 148, 194, 231, 82, 996, 356, 276, 88, 471, 56, 131, 470, 302, 112, 296, 427, 133, 201, 105, 209, 207, 158, 204, 446, 272, 136, 133, 154, 178, 112, 165, 256, 169, 153, 105, 119, 18, 144, 303, 151, 124, 128, 251, 125, 157, 210, 137, 267, 124, 187, 92, 213, 149, 231, 78, 108, 199, 418, 89, 300, 100, 74, 104, 52, 259, 373, 103, 140, 115, 165, 230, 380, 520, 172, 87, 534, 216, 113, 148, 601, 148, 701, 361, 308, 117, 144, 546, 162, 58, 260, 77, 185, 253, 296, 355, 293, 38, 329, 59, 54, 186, 196, 334, 302, 216, 145, 294, 264, 917, 122, 160, 142, 134, 123, 188, 152, 164, 444, 213, 122, 121, 107, 54, 179, 518, 149, 163, 479, 48, 387, 516, 134, 116, 291, 546, 130, 312, 146, 115, 181, 122, 293, 109, 171, 154, 458, 353, 351, 432, 213, 140, 246, 309, 138, 105, 179, 116, 431, 152, 198, 152, 57, 609, 108, 113, 61, 138, 107, 207, 371, 331, 151, 111, 469, 189, 333, 51, 340, 163, 119, 177, 155, 549, 222, 61, 51, 161, 130, 118, 274, 179, 151, 249, 113, 184, 120, 296, 105, 165, 264, 104, 409, 155, 53, 232, 249, 121, 158, 168, 783, 477, 138, 306, 645, 236, 161, 128, 136, 641, 320, 187, 130, 247, 423, 325, 398, 317, 134, 212, 286, 40, 193, 139, 70, 520, 43, 110, 334, 443, 193, 270, 290, 161, 133, 316, 115, 166, 251, 159, 88, 182, 175, 280, 92, 209, 132, 101, 171, 646, 1001, 132, 134, 233, 66, 106, 248, 216, 197, 995, 190, 76, 91, 332, 115, 331, 183, 253, 297, 732, 181, 159, 125, 244, 171, 306, 202, 266, 133, 233, 124, 146, 333, 140, 156, 184, 123, 391, 131, 162, 123, 104, 283, 171, 119, 215, 60, 203, 190, 202, 69, 170, 501, 140, 152, 176, 136, 301, 135, 167, 671, 96, 132, 254, 57, 130, 170, 91, 234, 75, 222, 304, 371, 129, 260, 133, 559, 146, 108, 40, 196, 117, 149, 95, 260, 634, 412, 119, 494, 271, 179, 118, 739, 129, 120, 341, 335, 119, 232, 205, 677, 299, 249, 168, 140, 93, 201, 121, 272, 107, 261, 468, 699, 212, 118, 222, 173, 67, 173, 202, 385, 185, 229, 300, 304, 141, 273, 121, 157, 494, 46, 34, 190, 49, 126, 72, 125, 88, 264, 135, 118, 94, 354, 365, 326, 156, 134, 133, 144, 205, 586, 650, 117, 167, 123, 47, 305, 109, 195, 119, 327, 154, 452, 196, 254, 486, 41, 220, 458, 138, 278, 180, 127, 107, 178, 239, 123, 197, 383, 36, 743, 121, 246, 128, 209, 227, 48, 126, 162, 120, 365, 86, 150, 187, 677, 187, 123, 102, 78, 45, 138, 144, 220, 110, 166, 257, 196, 117, 147, 178, 107, 112, 242, 140, 356, 155, 341, 49, 54, 358, 454, 165, 151, 236, 114, 504, 131, 90, 117, 291, 166, 117, 212, 198, 36, 109, 427, 909, 283, 146, 190, 57, 899, 126, 190, 77, 104, 70, 663, 230, 117, 320, 123, 114, 58, 141, 256, 292, 170, 263, 259, 134, 161, 172, 65, 133, 110, 364, 127, 258, 191, 54, 168, 271, 189, 69, 264, 283, 120, 196, 72, 276, 104, 138, 132, 316, 130, 173, 155, 90, 287, 240, 43, 88, 188, 148, 189, 84, 58, 354, 181, 295, 118, 304, 55, 306, 141, 314, 246, 528, 180, 160, 371, 457, 69, 379, 342, 163, 318, 148, 220, 154, 155, 666, 559, 232, 388, 184, 276, 220, 466, 602, 531, 138, 491, 75, 246, 104, 128, 129, 57, 66, 561, 143, 36, 145, 357, 122, 242, 133, 294, 155, 177, 878, 124, 136, 613, 119, 439, 207, 225, 199, 161, 128, 170, 96, 205, 149, 130, 245, 173, 106, 59, 262, 90, 149, 109, 439, 211, 207, 177, 178, 124, 228, 177, 964, 128, 139, 89, 128, 279, 291, 615, 185, 153, 228, 105, 261, 412, 51, 55, 158, 112, 136, 73, 167, 954, 178, 510, 35, 460, 144, 141, 170, 203, 177, 357, 199, 96, 87, 455, 188, 165, 118, 50, 332, 224, 88, 168, 146, 170, 587, 165, 117, 220, 125, 163, 369, 123, 276, 83, 80, 223, 188, 451, 139, 162, 144, 147, 179, 413, 336, 46, 143, 356, 101, 348, 253, 136, 177, 145, 193, 96, 117, 179, 238, 229, 224, 560, 281, 184, 374, 98, 164, 878, 229, 53, 115, 130, 121, 274, 414, 17, 180, 128, 62, 277, 69, 46, 60, 421, 131, 134, 79, 639, 399, 154, 189, 166, 115, 549, 176, 361, 147, 285, 141, 315, 108, 209, 395, 119, 406, 142, 533, 231, 127, 145, 384, 187, 115, 127, 135, 175, 140, 62, 199, 120, 427, 278, 284, 135, 192, 150, 314, 199, 82, 69, 989, 198, 134, 183, 203, 311, 421, 404, 247, 264, 57, 511, 311, 95, 174, 127, 197, 184]
    음절갯수 =  [1872, 791, 2074, 1869, 1867, 355, 496, 599, 803, 202, 268, 725, 1915, 633, 506, 953, 1952, 2052, 1182, 583, 1234, 1369, 1422, 181, 173, 649, 1034, 1132, 2983, 533, 284, 531, 608, 1513, 1774, 1335, 613, 553, 775, 2564, 1182, 646, 705, 794, 730, 577, 378, 629, 1155, 874, 817, 486, 993, 682, 248, 721, 767, 730, 307, 1670, 2403, 1026, 640, 599, 524, 265, 4844, 283, 930, 534, 575, 2002, 874, 849, 678, 639, 1200, 397, 949, 731, 536, 1257, 1981, 880, 1868, 1355, 1715, 234, 537, 533, 536, 613, 492, 613, 609, 737, 787, 359, 977, 325, 990, 3879, 437, 728, 187, 534, 603, 598, 1734, 2089, 771, 984, 1455, 327, 627, 1056, 516, 668, 445, 521, 923, 1566, 590, 1186, 1493, 3646, 2230, 1435, 520, 1051, 619, 2825, 723, 3000, 1913, 104, 1553, 809, 782, 503, 650, 1223, 659, 683, 1158, 799, 714, 1290, 1711, 521, 374, 771, 764, 1617, 1487, 436, 1035, 1588, 2456, 828, 1736, 1013, 512, 673, 1085, 622, 4151, 624, 577, 695, 721, 931, 1608, 639, 2224, 600, 1616, 581, 703, 1199, 1983, 1998, 3638, 613, 1163, 594, 433, 1888, 530, 634, 3519, 496, 292, 767, 334, 1351, 351, 1212, 965, 502, 571, 1130, 540, 1216, 3761, 1037, 648, 1211, 811, 516, 645, 3069, 694, 456, 4675, 465, 1608, 1139, 811, 555, 572, 848, 2908, 384, 573, 1283, 2185, 528, 1299, 612, 2139, 1438, 612, 561, 543, 1796, 682, 4006, 619, 628, 835, 859, 414, 2604, 738, 1466, 264, 1069, 581, 523, 1086, 1382, 722, 579, 742, 3346, 1281, 783, 1022, 887, 2589, 1412, 697, 1567, 768, 1378, 2539, 736, 849, 1276, 2282, 510, 525, 3640, 767, 1375, 1777, 641, 923, 943, 2448, 1691, 651, 1239, 391, 533, 1990, 1186, 577, 522, 772, 698, 516, 556, 370, 920, 615, 565, 1293, 2459, 1011, 592, 591, 737, 1297, 1071, 3193, 2949, 1796, 541, 1012, 1455, 3836, 807, 244, 1243, 939, 891, 1556, 213, 567, 1529, 421, 894, 959, 941, 555, 355, 273, 749, 748, 781, 833, 952, 1383, 1583, 679, 4022, 1951, 970, 324, 241, 565, 885, 1285, 2900, 1063, 561, 673, 757, 199, 1412, 532, 634, 642, 1689, 137, 247, 559, 552, 792, 554, 1974, 2774, 713, 509, 1503, 809, 950, 787, 677, 827, 513, 3552, 2080, 2631, 654, 1846, 703, 1629, 1022, 621, 396, 571, 843, 738, 1082, 804, 188, 516, 544, 3026, 813, 556, 2004, 630, 630, 1102, 509, 889, 373, 280, 1258, 1789, 321, 1594, 711, 582, 710, 1529, 2184, 1208, 530, 1879, 716, 451, 1598, 3412, 1277, 624, 998, 703, 911, 2867, 845, 661, 800, 1267, 240, 3510, 3875, 891, 438, 994, 1256, 860, 687, 429, 719, 794, 3356, 1587, 778, 711, 700, 2797, 783, 885, 1127, 3274, 1004, 943, 546, 700, 4253, 521, 224, 3358, 1253, 974, 651, 425, 2103, 1689, 1109, 622, 1037, 533, 819, 1009, 983, 749, 676, 1490, 1192, 551, 797, 577, 1686, 1574, 296, 681, 1857, 559, 415, 585, 197, 403, 1238, 2468, 1966, 939, 1728, 2556, 2287, 798, 4226, 534, 444, 1294, 686, 679, 654, 616, 806, 297, 971, 677, 1800, 638, 1192, 1237, 140, 2425, 1427, 207, 656, 996, 467, 798, 537, 1688, 485, 1291, 1667, 2480, 744, 1604, 840, 670, 3692, 858, 2399, 788, 555, 636, 706, 933, 617, 2857, 556, 368, 1970, 1293, 381, 655, 263, 1725, 629, 1145, 2915, 908, 832, 638, 576, 391, 861, 4267, 606, 556, 1209, 1730, 2650, 669, 1232, 1001, 1937, 625, 511, 962, 497, 558, 1111, 611, 704, 211, 344, 524, 1841, 1515, 462, 220, 2199, 523, 2438, 867, 1909, 876, 256, 1629, 731, 1508, 1140, 178, 1215, 550, 527, 739, 2159, 1729, 1850, 466, 3892, 1059, 2025, 733, 765, 861, 1891, 858, 517, 1083, 615, 709, 1252, 978, 2375, 295, 630, 1613, 557, 280, 828, 345, 2070, 207, 1194, 521, 921, 500, 1127, 473, 1336, 2960, 1258, 600, 699, 538, 2855, 2363, 1081, 561, 1072, 391, 600, 608, 1827, 708, 396, 831, 723, 554, 1818, 1126, 1152, 1033, 1826, 612, 239, 771, 634, 967, 1014, 466, 590, 700, 2404, 541, 919, 801, 633, 1729, 474, 742, 1228, 920, 1041, 1413, 591, 982, 646, 533, 755, 968, 2175, 836, 335, 1146, 269, 1565, 630, 319, 265, 2654, 1314, 534, 889, 426, 1092, 540, 2612, 466, 1243, 231, 267, 258, 1814, 839, 785, 374, 979, 742, 2091, 193, 807, 572, 1278, 981, 551, 667, 1954, 999, 511, 1416, 715, 1091, 659, 377, 651, 565, 1990, 1967, 500, 1950, 1040, 3088, 565, 414, 3742, 1344, 2222, 566, 666, 779, 2958, 404, 772, 958, 665, 543, 257, 1561, 1450, 966, 879, 1806, 526, 278, 613, 645, 1214, 601, 1078, 506, 559, 563, 2411, 1225, 702, 1065, 467, 577, 654, 1491, 770, 549, 247, 537, 1067, 1222, 1406, 492, 598, 1765, 728, 547, 735, 1143, 973, 708, 1062, 4827, 645, 584, 621, 862, 676, 803, 613, 1139, 610, 1474, 1585, 812, 1475, 1521, 1594, 1700, 405, 870, 1512, 546, 957, 2298, 785, 365, 557, 795, 1527, 1031, 789, 1783, 1022, 641, 1231, 738, 456, 281, 4162, 490, 1878, 226, 622, 1509, 640, 1729, 1563, 1094, 661, 1407, 782, 1920, 1055, 329, 960, 1701, 272, 511, 1216, 2065, 422, 2441, 261, 386, 970, 603, 378, 1734, 1126, 1704, 1920, 596, 625, 758, 644, 2106, 423, 742, 633, 274, 759, 966, 1321, 433, 805, 521, 525, 2893, 909, 1068, 637, 868, 1773, 1188, 1668, 604, 969, 1942, 610, 449, 2948, 405, 541, 2018, 284, 935, 616, 923, 530, 573, 619, 575, 733, 1794, 969, 393, 4544, 217, 1424, 580, 924, 3573, 845, 623, 687, 659, 724, 1475, 1154, 1045, 1121, 514, 433, 570, 606, 1089, 1634, 2094, 597, 1566, 1240, 311, 959, 542, 3094, 712, 562, 731, 2071, 507, 744, 1189, 956, 934, 1826, 710, 902, 1214, 874, 604, 1260, 2885, 679, 912, 547, 1077, 2987, 2232, 813, 547, 851, 1092, 3030, 737, 1129, 1943, 2559, 980, 1459, 772, 509, 686, 543, 3924, 1201, 313, 2541, 1176, 924, 1005, 1643, 909, 1537, 1558, 977, 613, 874, 1253, 1453, 884, 1736, 452, 1028, 701, 465, 620, 860, 490, 3033, 851, 570, 1151, 649, 1083, 1431, 917, 1034, 729, 2378, 609, 937, 888, 560, 1700, 1030, 1216, 2518, 746, 714, 2032, 825, 3616, 216, 1277, 2279, 617, 1618, 498, 245, 811, 1342, 601, 1128, 294, 522, 1104, 599, 179, 1596, 1226, 2481, 683, 690, 634, 1211, 926, 895, 550, 533, 656, 551, 252, 580, 620, 907, 598, 750, 1246, 2586, 548, 1092, 720, 1127, 1852, 976, 952, 350, 814, 281, 841, 681, 640, 348, 1017, 694, 839, 751, 539, 1269, 681, 684, 568, 504, 953, 697, 731, 343, 612, 987, 1106, 1958, 612, 2713, 1116, 144, 1902, 403, 2701, 572, 776, 1064, 1715, 531, 2839, 813, 696, 4166, 986, 1022, 512, 965, 1933, 1338, 794, 700, 964, 685, 251, 932, 1603, 1305, 1126, 932, 1547, 611, 577, 626, 255, 677, 3756, 990, 535, 1805, 529, 1093, 4344, 675, 1605, 812, 887, 1193, 854, 1760, 664, 551, 581, 544, 2373, 1341, 1130, 1016, 763, 4814, 2919, 2185, 641, 646, 542, 546, 1480, 311, 347, 1817, 1530, 802, 601, 2410, 962, 1229, 3822, 687, 855, 2095, 566, 353, 1225, 597, 646, 818, 1693, 4015, 854, 2279, 1259, 136, 1481, 515, 679, 1945, 608, 666, 938, 2552, 725, 3437, 664, 295, 501, 780, 868, 597, 459, 136, 3136, 1181, 553, 568, 881, 827, 724, 638, 570, 731, 1315, 1412, 555, 3198, 909, 2593, 955, 1153, 983, 1195, 873, 919, 435, 1085, 540, 561, 689, 692, 4596, 709, 3923, 536, 1221, 525, 1464, 1623, 651, 2369, 679, 461, 627, 1078, 1290, 687, 458, 505, 1223, 818, 1474, 599, 596, 938, 531, 2676, 1243, 241, 640, 972, 724, 1262, 826, 1789, 2161, 1243, 646, 563, 1279, 600, 1262, 586, 1647, 4070, 1479, 972, 1580, 1947, 1379, 420, 1977, 788, 1993, 2016, 875, 213, 1584, 1010, 1670, 1422, 680, 3663, 248, 2013, 536, 642, 616, 389, 476, 1098, 589, 1539, 1062, 3656, 871, 863, 655, 1663, 652, 802, 2558, 744, 395, 1748, 1660, 817, 801, 779, 1194, 1069, 1640, 567, 2213, 1486, 645, 544, 1383, 926, 647, 303, 636, 913, 747, 343, 4479, 831, 473, 554, 2195, 1484, 852, 4367, 584, 1227, 577, 614, 951, 759, 1348, 361, 486, 1543, 1157, 364, 1422, 552, 361, 678, 1222, 2168, 656, 607, 2212, 582, 563, 559, 549, 1495, 689, 233, 3475, 985, 280, 572, 438, 410, 693, 928, 933, 472, 657, 720, 1191, 572, 390, 1232, 1129, 333, 634, 2353, 834, 518, 827, 2013, 543, 249, 4494, 775, 1434, 1421, 850, 1889, 1593, 527, 528, 1229, 379, 526, 1252, 2459, 1035, 1810, 895, 741, 212, 620, 2758, 415, 1161, 3920, 1234, 1017, 1968, 1422, 566, 461, 1238, 1422, 2324, 578, 608, 597, 581, 606, 2152, 680, 828, 1206, 863, 775, 634, 477, 622, 868, 1042, 512, 598, 1084, 3167, 722, 2869, 1248, 485, 786, 1945, 919, 3153, 621, 366, 308, 205, 430, 686, 888, 346, 762, 2320, 524, 3344, 3334, 625, 537, 2335, 1768, 1230, 1362, 548, 802, 385, 1809, 1774, 589, 435, 694, 316, 2293, 249, 499, 530, 1199, 2781, 858, 1058, 1701, 508, 1010, 2458, 600, 373, 279, 840, 1552, 290, 703, 1101, 3127, 2078, 950, 368, 523, 863, 591, 2383, 403, 1232, 2040, 1490, 1643, 558, 2823, 861, 844, 966, 933, 1840, 2617, 420, 581, 2913, 953, 1535, 536, 356, 523, 755, 678, 1135, 2236, 4337, 528, 645, 529, 1259, 895, 970, 665, 623, 678, 849, 936, 593, 1579, 4061, 2766, 853, 519, 2579, 693, 554, 596, 683, 452, 610, 239, 1056, 1304, 1514, 677, 539, 579, 796, 1194, 523, 642, 987, 621, 541, 1627, 1297, 1942, 1245, 1034, 1120, 2059, 1635, 693, 518, 1149, 1024, 602, 1080, 791, 781, 593, 1523, 244, 729, 589, 1593, 1593, 2239, 772, 859, 2413, 531, 1103, 877, 1645, 1077, 1195, 843, 332, 577, 955, 609, 585, 454, 614, 626, 4260, 782, 660, 1032, 1914, 3980, 1141, 574, 2339, 2059, 245, 784, 467, 534, 1455, 1587, 4115, 2133, 1082, 759, 2044, 611, 2956, 1891, 763, 813, 2854, 2570, 1103, 2027, 1015, 865, 1447, 662, 568, 225, 1310, 382, 1607, 2089, 1044, 1098, 1605, 3335, 887, 280, 1214, 697, 650, 426, 1857, 639, 1298, 1873, 706, 423, 656, 591, 767, 1256, 437, 357, 1123, 449, 261, 1507, 382, 2047, 1698, 761, 982, 607, 917, 1250, 560, 775, 1028, 1719, 859, 892, 1001, 272, 3148, 1626, 297, 245, 3386, 1537, 591, 1417, 2459, 1002, 370, 519, 969, 232, 918, 1914, 3477, 2608, 1330, 234, 3519, 563, 902, 2554, 353, 4270, 306, 2680, 1807, 2124, 1046, 949, 1259, 1601, 704, 340, 1987, 654, 608, 798, 3781, 859, 1269, 2317, 656, 3643, 557, 1120, 922, 654, 1278, 1370, 694, 1911, 951, 652, 691, 1708, 1511, 348, 570, 3420, 1808, 579, 678, 893, 412, 868, 775, 714, 500, 1377, 363, 767, 1253, 525, 1134, 773, 918, 476, 629, 1040, 507, 579, 661, 321, 2233, 1015, 633, 441, 242, 748, 843, 189, 594, 716, 1121, 989, 707, 996, 681, 1239, 714, 742, 720, 2001, 516, 1554, 947, 151, 386, 1239, 503, 675, 1067, 2094, 2296, 2957, 520, 759, 704, 1233, 2045, 623, 264, 693, 581, 1500, 206, 554, 1275, 559, 612, 1106, 288, 1580, 541, 700, 776, 1526, 631, 493, 531, 1009, 1653, 1630, 2903, 338, 633, 2596, 553, 945, 2335, 454, 4185, 655, 618, 255, 628, 687, 2641, 1167, 985, 777, 2062, 2239, 540, 2037, 1894, 1908, 545, 615, 782, 432, 1179, 1016, 551, 537, 1305, 388, 543, 607, 1386, 433, 200, 683, 698, 3623, 1101, 1199, 241, 884, 566, 553, 945, 1310, 2688, 3279, 570, 1149, 920, 748, 1135, 573, 1214, 537, 1023, 2151, 600, 1290, 564, 980, 613, 353, 981, 2050, 725, 623, 968, 1179, 935, 989, 529, 1170, 1641, 1555, 653, 800, 1596, 1366, 543, 499, 3673, 382, 641, 873, 595, 521, 760, 2076, 811, 558, 1099, 770, 713, 4795, 680, 622, 536, 461, 3296, 569, 850, 594, 462, 589, 3009, 669, 556, 431, 1016, 667, 563, 1478, 695, 2375, 2814, 3873, 635, 452, 557, 865, 857, 593, 1144, 567, 540, 555, 946, 662, 1252, 420, 536, 713, 727, 1739, 800, 2533, 630, 990, 499, 1514, 579, 528, 566, 4222, 590, 638, 821, 1163, 591, 548, 467, 1065, 333, 590, 1071, 842, 919, 2064, 710, 1153, 1475, 938, 476, 831, 1002, 2726, 800, 860, 736, 620, 712, 1626, 1645, 1533, 609, 520, 1288, 1128, 2562, 454, 784, 520, 1027, 2015, 1024, 346, 374, 1285, 3293, 734, 878, 1036, 600, 571, 769, 511, 642, 798, 411, 1126, 813, 536, 1508, 599, 862, 551, 3553, 1049, 408, 427, 813, 621, 773, 762, 586, 2848, 612, 696, 687, 569, 1089, 668, 811, 1101, 979, 1110, 715, 1734, 1395, 1029, 874, 1925, 1108, 394, 3165, 1350, 554, 560, 1584, 654, 2012, 2537, 672, 475, 952, 545, 571, 514, 157, 1160, 586, 520, 1055, 1185, 635, 292, 659, 3051, 739, 1961, 2482, 538, 448, 215, 1676, 1107, 846, 1626, 656, 909, 1307, 724, 4274, 1326, 2232, 766, 332, 521, 895, 255, 854, 550, 614, 1056, 728, 2587, 779, 649, 583, 2572, 874, 720, 648, 1042, 708, 631, 1287, 299, 1895, 425, 4067, 130, 1632, 587, 593, 414, 611, 1701, 333, 510, 568, 459, 1312, 1425, 225, 1035, 1000, 1243, 645, 216, 951, 314, 867, 915, 230, 947, 656, 2500, 941, 739, 895, 550, 633, 4469, 1149, 1711, 642, 586, 714, 1004, 3541, 1273, 4704, 898, 512, 607, 1358, 593, 1778, 1161, 546, 578, 599, 5847, 2275, 1656, 3081, 3398, 250, 399, 1256, 3527, 224, 990, 1280, 1756, 2069, 479, 400, 821, 668, 365, 523, 2845, 539, 2467, 1162, 672, 549, 512, 670, 1365, 1626, 663, 656, 660, 528, 648, 851, 825, 314, 3567, 3825, 1005, 824, 279, 988, 560, 3087, 635, 954, 2400, 708, 1159, 620, 575, 832, 1217, 1109, 1367, 738, 256, 625, 549, 342, 552, 416, 176, 2203, 832, 346, 558, 833, 618, 1183, 558, 1179, 1926, 700, 1164, 360, 2515, 1692, 846, 555, 1615, 2945, 594, 3644, 1144, 3089, 637, 553, 2026, 1943, 155, 515, 1751, 365, 3654, 1904, 838, 468, 589, 595, 679, 364, 1579, 976, 1091, 840, 2630, 2234, 812, 1344, 2905, 659, 1190, 1185, 879, 1975, 2110, 2137, 562, 856, 520, 1195, 263, 1691, 1387, 669, 704, 493, 905, 957, 1254, 238, 752, 1688, 2562, 1475, 783, 3610, 1509, 528, 511, 2449, 723, 633, 876, 441, 555, 1670, 1263, 684, 683, 2129, 540, 502, 827, 1516, 866, 1374, 499, 1563, 842, 1385, 698, 702, 892, 3572, 1709, 1018, 517, 2149, 989, 2046, 2491, 552, 3718, 221, 568, 1539, 1658, 729, 605, 3291, 649, 538, 1228, 2476, 180, 1285, 1382, 1960, 1910, 2593, 615, 529, 1332, 501, 571, 1282, 718, 573, 560, 420, 1190, 579, 868, 345, 2357, 697, 1018, 1122, 529, 1389, 1670, 348, 240, 656, 1987, 2401, 707, 543, 720, 272, 1735, 1894, 548, 712, 794, 838, 834, 887, 734, 755, 1050, 903, 508, 259, 1114, 957, 883, 760, 938, 923, 291, 2219, 255, 3824, 850, 903, 632, 612, 855, 2184, 442, 1149, 1977, 921, 784, 896, 1955, 2686, 488, 420, 1642, 604, 1351, 834, 379, 599, 3801, 1116, 719, 544, 204, 524, 1800, 527, 475, 3055, 617, 712, 2487, 1586, 935, 686, 1231, 338, 1038, 603, 1831, 576, 868, 1082, 704, 1121, 1730, 438, 587, 1938, 992, 704, 1538, 664, 685, 359, 845, 400, 2950, 1338, 534, 1123, 1080, 536, 1428, 1797, 2253, 3151, 751, 1347, 273, 562, 2950, 1514, 469, 1520, 627, 2541, 840, 1570, 487, 1023, 204, 613, 587, 1377, 1021, 188, 661, 619, 515, 2070, 557, 1677, 406, 1638, 1353, 1340, 563, 505, 836, 213, 1083, 949, 686, 734, 979, 1630, 672, 1380, 2263, 926, 623, 201, 570, 568, 768, 285, 994, 1928, 1684, 1578, 755, 1390, 419, 902, 547, 505, 1310, 801, 942, 1333, 1755, 2548, 857, 525, 742, 3266, 575, 1273, 672, 1040, 371, 813, 1040, 353, 2760, 283, 333, 800, 656, 1816, 513, 564, 3431, 967, 1257, 573, 713, 1356, 512, 727, 620, 514, 535, 445, 488, 569, 1439, 570, 1597, 578, 477, 357, 287, 4428, 494, 1156, 557, 1812, 538, 810, 958, 504, 1374, 2754, 382, 1970, 2142, 877, 201, 1679, 1152, 804, 684, 515, 674, 2245, 694, 1273, 565, 909, 234, 1832, 1997, 944, 2364, 488, 1198, 755, 568, 494, 563, 1259, 225, 688, 830, 355, 533, 4224, 1373, 684, 1691, 1195, 554, 917, 608, 1647, 883, 1010, 580, 652, 1232, 1208, 1293, 591, 266, 198, 815, 528, 1123, 1009, 891, 596, 612, 1099, 723, 490, 567, 1006, 800, 1627, 896, 1174, 1607, 534, 1669, 1714, 2160, 511, 811, 511, 352, 663, 881, 597, 623, 1776, 2574, 535, 803, 1820, 323, 3451, 914, 761, 782, 683, 607, 901, 1465, 818, 763, 527, 520, 821, 560, 929, 654, 1713, 1526, 3191, 436, 1693, 738, 751, 650, 1988, 1498, 262, 2459, 493, 283, 919, 447, 882, 1826, 2541, 1459, 634, 910, 1647, 2960, 254, 2192, 1821, 274, 903, 407, 836, 613, 547, 831, 588, 1441, 626, 766, 2189, 590, 1572, 1165, 258, 1256, 3122, 679, 561, 847, 1400, 736, 802, 726, 990, 1753, 543, 592, 632, 277, 1143, 774, 1150, 838, 1984, 591, 1014, 584, 770, 734, 654, 460, 622, 552, 1243, 1202, 324, 2077, 2210, 798, 643, 1026, 1468, 1884, 1398, 4720, 2042, 888, 514, 3866, 645, 679, 831, 2598, 1049, 1285, 530, 873, 2412, 3246, 1151, 2305, 1480, 348, 896, 530, 781, 2128, 527, 424, 1038, 601, 757, 530, 451, 975, 3806, 4809, 541, 1134, 741, 1564, 3313, 621, 619, 930, 1156, 441, 547, 866, 496, 1165, 1492, 790, 745, 2552, 393, 216, 989, 945, 3085, 876, 516, 1742, 200, 977, 413, 650, 684, 781, 934, 812, 669, 756, 3129, 194, 494, 1020, 569, 562, 894, 391, 544, 2273, 1104, 1116, 626, 1598, 544, 1586, 1430, 544, 1522, 999, 858, 1096, 2108, 857, 597, 569, 746, 514, 751, 1031, 2245, 541, 1346, 656, 1306, 420, 1295, 810, 2019, 1096, 508, 3051, 1703, 216, 976, 617, 1744, 577, 743, 1048, 3856, 596, 1329, 558, 607, 1409, 1323, 1580, 566, 654, 459, 520, 1289, 352, 565, 546, 4857, 985, 670, 731, 851, 2532, 526, 878, 2908, 632, 1203, 2380, 1298, 1005, 543, 254, 881, 830, 179, 644, 1029, 1121, 1427, 1697, 705, 1089, 295, 2701, 656, 1141, 2309, 615, 300, 1953, 1163, 1264, 1026, 597, 812, 733, 812, 1247, 2572, 5071, 168, 689, 2112, 677, 345, 516, 625, 934, 3525, 557, 498, 555, 956, 1030, 368, 790, 1040, 865, 637, 298, 411, 795, 660, 657, 884, 1443, 594, 2808, 603, 453, 682, 1114, 710, 573, 425, 684, 780, 518, 676, 954, 1235, 681, 241, 2804, 924, 860, 1411, 1258, 2440, 623, 2751, 645, 1109, 632, 2052, 3038, 717, 840, 907, 2643, 1166, 415, 1624, 1738, 571, 566, 752, 657, 553, 1014, 163, 788, 915, 749, 582, 1377, 966, 1024, 3808, 496, 689, 844, 517, 672, 866, 1967, 532, 1507, 544, 436, 601, 1736, 430, 870, 1405, 556, 1214, 598, 1402, 1658, 1350, 2966, 1098, 532, 668, 1066, 2028, 2567, 1796, 1491, 2186, 2841, 978, 1853, 1969, 640, 279, 688, 558, 822, 351, 2175, 881, 561, 923, 527, 1469, 2743, 478, 2616, 550, 552, 456, 867, 266, 2763, 790, 659, 807, 436, 612, 618, 982, 560, 1151, 406, 998, 854, 1382, 1334, 581, 457, 4544, 1291, 519, 526, 2037, 2394, 819, 924, 1930, 2604, 582, 383, 1589, 747, 479, 562, 592, 216, 1025, 2667, 904, 941, 1430, 520, 1100, 609, 763, 6122, 1180, 682, 4569, 1246, 1973, 1222, 926, 594, 1540, 859, 314, 2774, 694, 542, 928, 738, 717, 653, 850, 633, 606, 829, 322, 967, 613, 1238, 768, 888, 706, 715, 528, 758, 822, 845, 1697, 2166, 854, 1315, 1351, 2920, 2010, 571, 576, 1156, 221, 519, 1648, 737, 3016, 908, 2154, 928, 491, 1161, 1481, 2088, 963, 1943, 1140, 1246, 619, 499, 503, 200, 394, 499, 588, 2262, 1438, 1706, 605, 1201, 1257, 591, 602, 648, 1452, 612, 1944, 1491, 1001, 614, 676, 636, 627, 808, 261, 928, 590, 841, 1401, 1787, 505, 249, 509, 585, 541, 821, 1180, 1058, 4706, 541, 1085, 799, 1012, 707, 585, 2082, 681, 1032, 594, 634, 808, 1276, 627, 360, 1109, 1627, 1559, 734, 1438, 638, 577, 1525, 1568, 1711, 720, 747, 1923, 1582, 4772, 1090, 279, 982, 1146, 921, 1311, 585, 939, 1113, 317, 794, 467, 2281, 1004, 1219, 902, 841, 2032, 3682, 1254, 2247, 2597, 1636, 462, 821, 2463, 614, 710, 541, 578, 479, 1723, 211, 772, 1913, 3661, 1549, 1839, 535, 3049, 686, 596, 1338, 549, 2337, 777, 679, 597, 1292, 1062, 2623, 1323, 3925, 723, 1594, 1346, 550, 748, 279, 2037, 637, 898, 579, 1253, 822, 2231, 3952, 540, 530, 1820, 271, 3207, 807, 1405, 1158, 3022, 574, 1276, 594, 1069, 1285, 587, 1628, 599, 3357, 1100, 627, 590, 601, 333, 743, 1185, 570, 866, 394, 3213, 2943, 791, 1289, 3559, 988, 747, 272, 868, 1895, 1275, 338, 1011, 516, 1399, 845, 597, 2325, 894, 531, 690, 2369, 540, 426, 767, 626, 406, 1571, 755, 549, 1539, 2787, 557, 3992, 1139, 566, 1103, 1921, 839, 1584, 544, 1000, 1054, 610, 567, 1487, 406, 953, 611, 2821, 1156, 909, 477, 546, 1242, 198, 761, 1588, 668, 3957, 808, 550, 1231, 1190, 1296, 2688, 290, 938, 788, 544, 381, 11241, 970, 1117, 620, 876, 2016, 1064, 1037, 1063, 2861, 642, 978, 1710, 588, 596, 288, 641, 659, 275, 3725, 2665, 158, 771, 702, 1046, 1236, 4809, 681, 1184, 2200, 574, 654, 2285, 1734, 1575, 783, 1735, 520, 962, 990, 596, 1340, 703, 948, 298, 1463, 1065, 633, 452, 578, 817, 536, 525, 740, 714, 361, 1624, 583, 853, 1041, 1590, 591, 2488, 428, 1497, 950, 1317, 1405, 3487, 320, 532, 1038, 897, 810, 434, 1889, 677, 669, 682, 1032, 568, 602, 499, 434, 2666, 697, 3004, 1233, 1057, 727, 995, 451, 1885, 1381, 533, 1131, 3672, 525, 1072, 1454, 2499, 722, 538, 2546, 2084, 713, 1593, 583, 1192, 788, 549, 4690, 646, 453, 644, 1112, 1038, 1142, 2039, 1527, 337, 677, 1488, 534, 652, 1106, 1988, 1239, 310, 1514, 545, 534, 328, 1725, 647, 1736, 563, 296, 630, 589, 2938, 2357, 277, 1733, 198, 560, 386, 592, 471, 1679, 1552, 529, 915, 353, 1206, 1411, 681, 629, 547, 371, 2553, 589, 2150, 1021, 189, 856, 4974, 3256, 569, 444, 1400, 285, 343, 723, 1525, 493, 1001, 1348, 1951, 2081, 968, 638, 832, 1043, 640, 655, 648, 720, 611, 1337, 426, 679, 3248, 1398, 1214, 879, 557, 618, 868, 1233, 774, 1346, 640, 2305, 741, 759, 773, 732, 4752, 1071, 2458, 389, 690, 591, 2737, 1386, 706, 1586, 540, 629, 338, 1027, 595, 192, 3278, 1379, 629, 898, 658, 909, 848, 1670, 2929, 739, 718, 701, 952, 816, 730, 1485, 299, 927, 331, 507, 622, 593, 1861, 677, 430, 552, 655, 2314, 1453, 3328, 647, 4414, 580, 969, 935, 524, 717, 2343, 1792, 1082, 1144, 1675, 1141, 2430, 540, 2481, 2528, 2440, 532, 206, 753, 1798, 571, 809, 707, 1742, 2437, 818, 1071, 1066, 90, 1425, 684, 1651, 1210, 236, 848, 928, 951, 984, 915, 703, 368, 641, 1816, 1204, 718, 486, 1331, 730, 814, 585, 4322, 2394, 1494, 902, 290, 1041, 1727, 1195, 3026, 886, 815, 1566, 870, 1111, 627, 1106, 776, 256, 599, 1914, 799, 580, 618, 685, 743, 864, 826, 4694, 1645, 695, 211, 822, 554, 799, 588, 2429, 358, 1272, 725, 690, 610, 1319, 577, 224, 1032, 2785, 296, 2009, 2534, 1094, 862, 1001, 1071, 947, 955, 970, 1083, 1600, 571, 2311, 271, 561, 242, 1009, 648, 463, 2385, 1497, 2654, 523, 2500, 3279, 1707, 368, 1263, 2096, 1145, 984, 903, 637, 2047, 649, 267, 1081, 4457, 1665, 586, 302, 1256, 1321, 279, 544, 290, 652, 1340, 882, 543, 930, 524, 304, 1215, 1300, 1349, 585, 966, 799, 1039, 1801, 527, 785, 688, 1301, 617, 420, 663, 965, 563, 682, 535, 2224, 1341, 316, 995, 2504, 1388, 543, 1222, 1035, 1852, 637, 1163, 648, 1198, 551, 558, 2330, 572, 580, 1284, 800, 1261, 842, 1017, 2825, 2809, 920, 639, 367, 509, 671, 2618, 550, 586, 850, 808, 1239, 2967, 742, 861, 493, 937, 566, 1228, 3526, 1413, 2160, 1931, 807, 580, 294, 256, 599, 604, 823, 3551, 2136, 402, 706, 774, 1493, 1767, 669, 2634, 574, 1750, 492, 1650, 1320, 445, 1297, 214, 894, 1629, 3649, 2286, 528, 907, 1365, 989, 684, 684, 651, 817, 540, 830, 1552, 494, 3162, 1574, 642, 490, 771, 541, 1568, 1565, 1030, 1239, 577, 580, 1157, 1260, 977, 3605, 1411, 1599, 195, 605, 1196, 568, 619, 3713, 624, 4100, 936, 590, 919, 1311, 536, 1580, 1801, 1404, 814, 875, 397, 652, 1609, 329, 500, 782, 1168, 1628, 594, 737, 928, 1995, 795, 1286, 61, 926, 542, 1263, 270, 2319, 1224, 1318, 605, 199, 1404, 727, 540, 1513, 932, 596, 421, 914, 683, 1414, 812, 1059, 925, 646, 602, 526, 626, 1632, 116, 956, 767, 1848, 539, 510, 468, 1193, 2313, 417, 556, 898, 500, 692, 1107, 739, 2429, 534, 1187, 1122, 661, 585, 656, 644, 776, 609, 806, 234, 373, 726, 1008, 1129, 1295, 597, 2153, 1005, 1213, 525, 2977, 714, 1720, 536, 1003, 607, 2247, 677, 855, 1744, 421, 1778, 1420, 655, 652, 259, 1672, 838, 543, 1124, 321, 2720, 1649, 2001, 1552, 930, 997, 945, 1735, 673, 1782, 915, 2021, 850, 2220, 1972, 340, 629, 310, 605, 673, 537, 623, 611, 598, 1687, 1790, 580, 2675, 491, 725, 1478, 253, 1001, 863, 1533, 774, 204, 816, 564, 1303, 398, 840, 434, 272, 3063, 1910, 117, 1096, 2000, 1206, 1950, 538, 3394, 3409, 1566, 1313, 1108, 2021, 258, 983, 608, 1275, 524, 776, 593, 781, 1930, 3428, 2100, 541, 635, 1311, 678, 2675, 888, 619, 483, 803, 1734, 654, 728, 245, 1258, 258, 389, 736, 551, 193, 1625, 2304, 3490, 1987, 1866, 668, 419, 620, 549, 714, 7802, 691, 880, 4552, 435, 2065, 938, 974, 2047, 2826, 604, 1667, 1311, 723, 675, 847, 533, 1770, 2510, 2499, 892, 284, 666, 1111, 585, 399, 1564, 1230, 689, 808, 600, 569, 644, 564, 668, 817, 833, 203, 1015, 441, 564, 686, 566, 468, 727, 1688, 2452, 1271, 693, 541, 821, 981, 1351, 3073, 1240, 468, 2538, 611, 1686, 1627, 851, 2173, 787, 660, 751, 1973, 1342, 1563, 804, 828, 1430, 563, 2909, 1349, 3131, 268, 218, 716, 1567, 1023, 314, 378, 331, 2836, 1520, 416, 3118, 4205, 612, 1892, 611, 554, 2969, 1698, 1883, 234, 1968, 1040, 742, 429, 514, 545, 316, 166, 577, 356, 2272, 618, 545, 1518, 1331, 805, 655, 987, 698, 1878, 616, 890, 748, 816, 1034, 1154, 1379, 2619, 1435, 1956, 674, 556, 342, 523, 543, 1011, 1163, 875, 245, 544, 1454, 576, 251, 1017, 616, 680, 181, 531, 762, 176, 2029, 962, 892, 679, 966, 1732, 1348, 699, 659, 868, 545, 552, 5011, 4375, 2882, 991, 808, 1700, 950, 2831, 574, 1656, 1872, 338, 1335, 603, 4588, 2698, 412, 978, 536, 558, 696, 859, 604, 617, 2477, 520, 1428, 3865, 575, 1057, 896, 1496, 711, 1841, 556, 644, 645, 758, 623, 1147, 802, 1687, 781, 269, 492, 259, 693, 524, 658, 723, 1667, 1494, 597, 844, 2923, 1417, 659, 333, 1099, 942, 895, 604, 744, 534, 878, 1231, 321, 4364, 519, 4297, 558, 595, 3842, 2258, 1167, 1110, 585, 817, 1177, 565, 1024, 985, 689, 1870, 194, 966, 785, 850, 839, 1857, 796, 572, 674, 2746, 838, 547, 1214, 802, 832, 1561, 592, 3156, 663, 1310, 1136, 881, 1926, 291, 339, 1683, 2355, 646, 595, 547, 730, 520, 812, 2430, 640, 544, 554, 752, 886, 776, 729, 316, 643, 730, 2690, 1551, 498, 2814, 817, 518, 1312, 713, 1070, 458, 262, 540, 754, 724, 680, 2445, 1708, 1037, 638, 844, 634, 311, 783, 396, 369, 989, 552, 1810, 3433, 1462, 1393, 757, 2182, 905, 1121, 1516, 518, 427, 660, 596, 372, 616, 301, 913, 1576, 426, 1015, 1443, 693, 3087, 332, 896, 2516, 940, 674, 667, 2564, 854, 1367, 777, 405, 306, 817, 2101, 271, 1205, 1418, 1285, 1058, 972, 672, 2408, 781, 3377, 648, 570, 1268, 1104, 1291, 669, 613, 918, 1215, 574, 832, 360, 1175, 1096, 687, 1401, 1047, 875, 1216, 701, 1088, 624, 690, 738, 860, 1382, 1180, 772, 629, 2048, 813, 564, 961, 1221, 565, 520, 885, 453, 1043, 566, 1243, 700, 2560, 399, 1300, 582, 924, 973, 677, 3358, 387, 1904, 504, 1588, 1657, 1124, 607, 3256, 2423, 1620, 502, 328, 2683, 552, 765, 798, 529, 1069, 3596, 812, 2677, 1009, 1349, 1093, 545, 246, 677, 515, 1530, 859, 1168, 1966, 940, 678, 234, 616, 842, 544, 557, 284, 500, 1313, 1710, 724, 527, 756, 695, 637, 462, 1683, 1513, 371, 1469, 990, 2812, 614, 793, 1051, 1010, 1848, 684, 558, 1478, 213, 1176, 524, 2625, 623, 616, 983, 1969, 448, 582, 546, 1706, 667, 667, 1580, 1104, 2140, 262, 766, 1123, 522, 864, 586, 1216, 1179, 656, 633, 2003, 344, 650, 2904, 517, 647, 1842, 4188, 2716, 2461, 3452, 2131, 2370, 585, 1209, 1001, 569, 663, 693, 866, 615, 298, 736, 689, 3067, 743, 788, 513, 605, 1132, 715, 624, 723, 1859, 346, 749, 985, 859, 1040, 1100, 803, 519, 2434, 1584, 1247, 697, 322, 530, 891, 1488, 629, 2049, 2522, 344, 2306, 589, 700, 352, 1005, 250, 448, 1693, 3550, 1245, 729, 561, 441, 1177, 746, 1661, 989, 768, 1129, 704, 591, 840, 662, 535, 540, 638, 1518, 819, 698, 943, 926, 687, 540, 360, 600, 774, 3627, 1009, 1748, 3347, 576, 545, 533, 579, 260, 808, 698, 4089, 332, 237, 4841, 2487, 955, 243, 2325, 775, 1289, 1862, 542, 470, 1668, 2180, 4586, 1063, 557, 648, 2209, 1067, 682, 573, 1197, 4123, 2346, 1273, 426, 565, 782, 736, 4470, 619, 721, 1279, 544, 1686, 691, 898, 833, 549, 567, 1515, 451, 1287, 2869, 258, 1768, 684, 4427, 552, 655, 542, 1190, 858, 638, 1042, 2604, 1119, 844, 878, 1626, 370, 371, 1117, 567, 835, 681, 373, 552, 1351, 268, 801, 1338, 981, 1608, 765, 1341, 1816, 774, 705, 681, 868, 2822, 575, 1400, 1137, 670, 1548, 1995, 522, 599, 583, 636, 1081, 1023, 988, 1397, 319, 4818, 1210, 3510, 664, 393, 1066, 823, 484, 625, 1346, 1636, 814, 1504, 2692, 627, 460, 449, 243, 1140, 721, 613, 542, 701, 745, 732, 533, 395, 1866, 663, 1682, 1087, 1071, 530, 731, 515, 1606, 442, 1943, 2035, 876, 1356, 1926, 779, 746, 1131, 2419, 715, 923, 560, 1261, 389, 479, 2937, 1572, 869, 293, 1072, 543, 1261, 1070, 532, 527, 739, 675, 625, 454, 659, 1168, 213, 346, 1672, 829, 646, 572, 651, 350, 1333, 4599, 633, 391, 550, 1337, 2014, 253, 1356, 2804, 580, 1378, 1013, 1839, 4090, 850, 562, 627, 851, 1040, 1126, 1190, 1983, 888, 1608, 1464, 2332, 587, 811, 2163, 3177, 585, 1496, 1072, 2105, 624, 894, 1316, 1524, 996, 934, 662, 1254, 453, 826, 503, 1107, 1761, 650, 658, 703, 483, 767, 1066, 779, 845, 3347, 611, 716, 1903, 566, 1118, 632, 1366, 2677, 990, 961, 1875, 699, 1317, 821, 658, 2898, 1420, 4536, 585, 526, 673, 1523, 1328, 2170, 1763, 901, 780, 439, 799, 956, 382, 555, 1095, 582, 1004, 1331, 1368, 1826, 999, 2432, 341, 285, 707, 479, 637, 724, 309, 513, 3076, 679, 1057, 551, 842, 805, 1966, 838, 5392, 1204, 1571, 437, 653, 622, 1540, 442, 958, 1531, 875, 601, 1181, 1378, 4327, 878, 1955, 573, 599, 641, 559, 374, 1902, 1243, 575, 689, 762, 802, 2081, 1912, 1411, 4911, 500, 721, 204, 1935, 981, 741, 1105, 1047, 969, 569, 923, 579, 535, 1092, 711, 1197, 866, 1262, 1936, 2537, 985, 1348, 286, 1057, 3159, 598, 543, 240, 1847, 517, 1132, 327, 924, 518, 1120, 594, 836, 617, 1041, 638, 612, 623, 895, 3481, 850, 2593, 678, 609, 576, 1845, 312, 331, 1042, 1146, 390, 1585, 1726, 1009, 1441, 690, 424, 746, 255, 2568, 453, 835, 972, 1524, 2113, 1242, 2908, 805, 584, 587, 474, 641, 1896, 532, 978, 742, 625, 612, 634, 1241, 1625, 1396, 932, 2199, 1879, 362, 684, 362, 1365, 640, 4486, 1905, 2195, 1472, 1833, 381, 761, 895, 3170, 570, 1467, 591, 590, 541, 440, 1172, 632, 1367, 554, 2624, 1019, 697, 514, 1435, 589, 641, 838, 601, 263, 2374, 598, 519, 1304, 1725, 2176, 414, 1741, 645, 614, 626, 850, 581, 3074, 679, 1832, 788, 566, 995, 1681, 561, 1272, 659, 1379, 997, 831, 2085, 2492, 1820, 835, 2246, 556, 848, 1181, 1062, 759, 721, 1043, 1129, 716, 748, 569, 1255, 4036, 392, 614, 211, 493, 534, 1359, 848, 1424, 3015, 555, 2020, 577, 1499, 605, 786, 1874, 936, 663, 426, 643, 549, 2195, 605, 1054, 158, 839, 734, 1479, 373, 1009, 2926, 881, 703, 597, 801, 2898, 719, 433, 2484, 918, 2178, 887, 536, 203, 293, 1569, 832, 1171, 541, 529, 358, 182, 858, 1542, 1553, 3122, 1242, 2560, 326, 1043, 895, 1122, 622, 1717, 250, 3387, 1215, 559, 524, 1061, 162, 245, 609, 743, 832, 1317, 1094, 546, 531, 2063, 1743, 2110, 1906, 648, 656, 290, 1065, 1313, 4777, 633, 2774, 757, 2338, 1988, 635, 1572, 3059, 709, 2896, 1059, 853, 432, 1054, 1599, 1073, 2636, 1280, 2035, 1522, 752, 677, 1047, 613, 583, 1507, 594, 579, 817, 568, 990, 497, 4003, 561, 504, 518, 2898, 382, 674, 525, 1694, 744, 2784, 1971, 827, 1879, 387, 607, 486, 873, 748, 611, 595, 861, 523, 868, 565, 629, 529, 617, 916, 630, 660, 188, 731, 941, 213, 340, 321, 816, 835, 832, 649, 715, 1039, 651, 2253, 518, 1490, 232, 399, 1510, 800, 644, 1149, 2126, 756, 238, 531, 957, 635, 700, 628, 881, 552, 555, 237, 3204, 701, 1244, 735, 543, 2196, 1714, 490, 806, 985, 910, 255, 817, 1486, 845, 3573, 340, 2657, 536, 1143, 1094, 2486, 1497, 1467, 2469, 499, 478, 676, 562, 553, 685, 4747, 1116, 1603, 1014, 578, 555, 1606, 806, 2535, 1169, 1059, 663, 953, 477, 590, 733, 1647, 549, 297, 877, 2506, 880, 532, 510, 584, 1650, 2105, 971, 3287, 558, 628, 1482, 303, 2697, 1564, 651, 177, 5039, 504, 1233, 526, 625, 1903, 575, 1155, 577, 1153, 1025, 1060, 569, 693, 222, 644, 220, 829, 530, 749, 580, 1448, 565, 2887, 641, 536, 593, 612, 1052, 1147, 572, 664, 2316, 771, 2630, 591, 1001, 2617, 677, 728, 1436, 1849, 844, 777, 606, 589, 594, 866, 358, 657, 672, 801, 302, 1060, 753, 417, 557, 400, 539, 4039, 793, 2912, 307, 1750, 1400, 1160, 1029, 739, 562, 670, 1917, 811, 608, 249, 656, 1047, 609, 394, 208, 563, 571, 1113, 864, 549, 703, 551, 785, 744, 192, 1239, 493, 447, 3008, 870, 574, 545, 1799, 5020, 322, 1006, 519, 935, 585, 765, 661, 596, 377, 3653, 317, 816, 1789, 594, 1418, 1165, 262, 191, 816, 177, 2057, 952, 352, 625, 783, 788, 595, 1261, 673, 1692, 719, 1165, 762, 917, 915, 1698, 1901, 1188, 596, 1093, 492, 1116, 1514, 2847, 1350, 445, 1168, 309, 249, 324, 565, 1620, 912, 1733, 1055, 1064, 1089, 4772, 174, 886, 1436, 1216, 3225, 1305, 996, 941, 3874, 1528, 5023, 923, 680, 637, 305, 1122, 1809, 614, 828, 3462, 1062, 349, 1436, 603, 902, 593, 1458, 193, 1787, 1640, 955, 638, 985, 772, 767, 185, 566, 945, 396, 1362, 632, 836, 1003, 907, 808, 2658, 1839, 661, 586, 2087, 559, 478, 763, 536, 775, 505, 1206, 2118, 279, 235, 1182, 710, 448, 1922, 447, 551, 1382, 1395, 1258, 675, 1206, 571, 838, 754, 1243, 1951, 353, 706, 609, 694, 1269, 976, 593, 622, 700, 463, 2396, 2224, 1112, 622, 1122, 647, 1979, 522, 1131, 586, 893, 1114, 398, 708, 672, 2091, 1488, 492, 584, 574, 674, 942, 1117, 1730, 1592, 520, 776, 550, 931, 248, 1790, 1001, 563, 363, 536, 186, 596, 1141, 775, 1195, 837, 642, 759, 561, 861, 2308, 562, 1818, 707, 674, 1207, 1969, 194, 652, 2906, 824, 723, 709, 1122, 881, 872, 662, 632, 1527, 283, 1267, 587, 947, 1060, 775, 697, 841, 1318, 1095, 508, 654, 963, 581, 1336, 1274, 516, 429, 521, 834, 666, 479, 1805, 820, 579, 1189, 537, 279, 1055, 636, 621, 1251, 844, 1642, 417, 723, 637, 1412, 548, 436, 647, 2076, 399, 764, 385, 640, 824, 622, 1074, 380, 550, 597, 933, 778, 1302, 960, 1109, 540, 569, 333, 588, 1284, 2019, 989, 606, 715, 1153, 1683, 703, 779, 539, 1967, 733, 205, 728, 927, 1129, 186, 490, 653, 399, 1792, 1507, 652, 2320, 4530, 480, 540, 1778, 456, 809, 647, 577, 1630, 415, 1928, 528, 265, 2827, 1962, 343, 1191, 1106, 411, 793, 574, 1984, 972, 3214, 502, 879, 604, 837, 635, 389, 605, 749, 2029, 280, 2352, 1160, 793, 655, 1318, 740, 299, 761, 1561, 1149, 762, 553, 907, 205, 568, 1487, 509, 875, 1407, 888, 885, 652, 1213, 1374, 2569, 741, 2061, 1525, 1004, 265, 1078, 562, 558, 615, 3482, 484, 1975, 609, 627, 1761, 727, 208, 1188, 572, 1115, 410, 1113, 196, 896, 3718, 729, 936, 202, 1215, 557, 349, 243, 723, 1555, 2331, 2454, 883, 1043, 636, 872, 1248, 1615, 3307, 2135, 2743, 787, 2490, 588, 742, 594, 449, 661, 620, 501, 590, 1252, 358, 512, 764, 431, 971, 861, 562, 541, 237, 578, 1056, 2086, 325, 892, 4282, 510, 2041, 442, 555, 2288, 500, 691, 2975, 677, 875, 377, 652, 501, 1198, 2723, 3168, 509, 1096, 1096, 695, 879, 1217, 724, 2212, 679, 1088, 1004, 1566, 1532, 782, 642, 588, 1121, 199, 1167, 662, 517, 705, 1384, 518, 1705, 679, 716, 1132, 230, 1604, 606, 595, 823, 716, 335, 365, 642, 2898, 1474, 534, 333, 978, 1456, 265, 2004, 1121, 568, 2333, 894, 1548, 911, 565, 3455, 961, 541, 2417, 562, 714, 537, 3199, 310, 738, 403, 1005, 1361, 1451, 637, 1140, 1302, 312, 1537, 585, 710, 305, 1549, 255, 604, 933, 964, 2566, 1219, 622, 1029, 1120, 924, 1834, 1075, 970, 327, 557, 1067, 915, 2045, 2402, 1670, 501, 757, 657, 1199, 216, 845, 755, 322, 299, 809, 2188, 315, 1509, 842, 676, 928, 1178, 2851, 1761, 693, 1376, 891, 1430, 851, 1252, 917, 1390, 805, 585, 481, 2482, 733, 811, 1226, 1020, 1442, 572, 2698, 868, 551, 1029, 3275, 810, 974, 865, 2692, 3531, 1859, 870, 751, 809, 514, 605, 528, 213, 1153, 1215, 1908, 4741, 1911, 676, 447, 688, 675, 744, 706, 764, 834, 652, 698, 480, 1088, 612, 404, 1261, 1714, 2155, 230, 638, 599, 1319, 1019, 1339, 689, 636, 798, 1238, 611, 1077, 1016, 880, 1293, 820, 496, 796, 1066, 951, 861, 626, 280, 3189, 555, 547, 756, 1279, 281, 956, 513, 634, 696, 565, 715, 688, 2134, 996, 3256, 521, 1683, 4262, 3458, 479, 561, 905, 2583, 572, 756, 593, 698, 543, 334, 883, 2829, 2579, 529, 857, 3330, 576, 737, 382, 1335, 1565, 889, 267, 1338, 404, 1270, 1980, 561, 769, 865, 889, 2460, 565, 1332, 821, 2251, 1266, 254, 810, 574, 509, 409, 822, 927, 1269, 3506, 1177, 831, 3507, 2433, 713, 694, 591, 611, 474, 2428, 1927, 863, 490, 2504, 569, 3438, 2017, 1074, 433, 596, 268, 616, 1030, 1002, 4131, 867, 1998, 1606, 651, 1352, 801, 518, 897, 3789, 1832, 301, 690, 597, 810, 729, 530, 673, 604, 513, 1008, 806, 602, 746, 3256, 1524, 776, 469, 561, 613, 378, 2369, 768, 1125, 697, 196, 499, 1569, 226, 319, 2780, 557, 1043, 569, 673, 531, 687, 148, 628, 579, 3465, 548, 1206, 549, 864, 779, 803, 920, 2055, 585, 777, 551, 790, 1440, 1630, 1923, 588, 956, 1068, 854, 579, 574, 483, 1048, 465, 1242, 2765, 954, 1789, 581, 616, 907, 1451, 799, 637, 2378, 2068, 946, 2724, 3557, 1022, 2133, 2025, 1266, 676, 2779, 1109, 500, 326, 767, 1238, 538, 514, 214, 235, 1883, 978, 579, 818, 336, 662, 1596, 461, 778, 596, 1645, 601, 500, 1881, 1915, 3183, 473, 1029, 493, 644, 373, 647, 705, 2739, 532, 1320, 612, 554, 1245, 708, 3227, 480, 857, 1658, 707, 613, 323, 2478, 1851, 886, 648, 409, 310, 1367, 3115, 3345, 853, 990, 1218, 915, 929, 749, 783, 564, 702, 837, 869, 1383, 3634, 4566, 643, 945, 1234, 661, 184, 733, 2886, 2201, 1307, 778, 2167, 735, 694, 268, 543, 529, 1994, 344, 473, 482, 875, 749, 459, 598, 1258, 596, 1753, 1292, 512, 985, 540, 2405, 2534, 1037, 859, 554, 1051, 773, 516, 614, 1412, 613, 560, 866, 1503, 1194, 1130, 572, 1034, 236, 2199, 495, 762, 737, 260, 799, 235, 1806, 1129, 1806, 1392, 210, 1019, 725, 616, 829, 536, 4368, 1302, 3049, 1129, 684, 790, 860, 5851, 1032, 678, 4891, 508, 698, 902, 758, 568, 856, 517, 1907, 161, 430, 1030, 746, 840, 1183, 861, 971, 595, 3718, 2216, 968, 549, 911, 277, 574, 2319, 1189, 760, 1263, 1190, 2424, 1597, 179, 630, 1690, 629, 2493, 580, 815, 638, 1176, 632, 725, 197, 656, 827, 1193, 617, 556, 3658, 915, 966, 3347, 750, 338, 589, 1746, 424, 566, 3644, 1297, 896, 1236, 1284, 732, 489, 427, 711, 170, 1173, 750, 901, 1991, 1593, 277, 406, 663, 1820, 1605, 761, 1567, 1605, 890, 230, 907, 383, 2409, 1540, 1188, 287, 3087, 598, 1790, 756, 4137, 545, 427, 505, 595, 766, 1250, 3870, 738, 872, 1371, 1987, 1337, 218, 509, 971, 540, 585, 172, 674, 223, 715, 574, 1743, 685, 840, 635, 601, 1739, 2447, 619, 1103, 752, 1462, 2295, 718, 316, 750, 1566, 1891, 607, 661, 1246, 1374, 741, 1630, 2240, 634, 1086, 747, 525, 562, 2985, 1425, 346, 676, 1101, 580, 714, 629, 656, 684, 451, 436, 1072, 314, 2667, 1077, 828, 552, 1518, 1654, 689, 2832, 502, 1617, 1463, 1028, 1060, 2152, 548, 1897, 619, 631, 917, 685, 276, 533, 1724, 1257, 2958, 783, 2861, 2392, 3132, 624, 241, 1570, 648, 773, 2150, 465, 917, 3799, 894, 767, 554, 2031, 1272, 2278, 1558, 690, 1184, 1716, 240, 583, 848, 1167, 1582, 969, 904, 1357, 294, 1153, 224, 803, 896, 1852, 717, 782, 664, 7480, 813, 521, 2397, 531, 1984, 309, 1127, 1206, 3866, 1169, 1274, 877, 523, 948, 3035, 583, 611, 241, 971, 2877, 1199, 602, 262, 3341, 1011, 777, 494, 227, 1352, 2316, 901, 1228, 641, 1263, 948, 680, 1287, 1164, 779, 883, 2085, 882, 537, 916, 2390, 2277, 1680, 644, 467, 860, 560, 1047, 358, 1981, 1267, 502, 1037, 1986, 583, 1855, 1169, 615, 1506, 1040, 465, 4316, 720, 705, 507, 2763, 719, 711, 741, 884, 313, 531, 526, 1395, 1676, 1119, 1007, 1711, 309, 1824, 1633, 1347, 372, 776, 1550, 825, 1671, 1241, 596, 830, 514, 370, 532, 2270, 582, 916, 1524, 315, 611, 794, 842, 3472, 770, 1074, 955, 1265, 514, 2288, 707, 634, 533, 1739, 599, 3083, 542, 1501, 1282, 1151, 323, 1007, 501, 491, 3228, 589, 737, 3215, 3470, 559, 1538, 1070, 1242, 885, 1797, 2363, 695, 223, 830, 881, 887, 614, 479, 1166, 815, 542, 968, 1340, 890, 2782, 1082, 579, 1911, 882, 965, 1696, 212, 643, 811, 794, 1094, 2338, 1523, 186, 756, 805, 1186, 609, 2558, 628, 1520, 728, 659, 281, 749, 536, 838, 3689, 946, 879, 542, 815, 1137, 753, 279, 596, 563, 1747, 594, 1089, 1529, 714, 1717, 4059, 909, 805, 1771, 1058, 455, 682, 634, 799, 293, 338, 3821, 4007, 808, 303, 536, 710, 1133, 528, 218, 658, 461, 2159, 581, 1659, 1799, 742, 570, 550, 861, 2082, 308, 1689, 705, 1354, 754, 1083, 588, 371, 417, 1534, 1787, 1602, 2528, 1068, 715, 589, 931, 1262, 2024, 553, 569, 1854, 1798, 714, 425, 462, 879, 2740, 605, 3135, 925, 1483, 147, 933, 292, 538, 4372, 281, 896, 915, 1477, 1395, 1033, 1885, 1122, 630, 574, 1768, 1004, 1255, 1044, 458, 123, 1487, 313, 1298, 1587, 2243, 1855, 647, 2518, 833, 597, 420, 464, 1115, 728, 480, 794, 1270, 527, 506, 634, 639, 1378, 1705, 814, 530, 1337, 527, 1352, 756, 1932, 891, 293, 875, 902, 194, 523, 4593, 1185, 660, 851, 573, 999, 604, 623, 939, 1008, 806, 818, 1088, 3709, 806, 1708, 756, 228, 495, 847, 2397, 648, 1025, 315, 973, 523, 893, 589, 1433, 1122, 249, 394, 238, 1347, 542, 988, 453, 535, 503, 1085, 488, 2009, 568, 404, 452, 1567, 622, 647, 503, 521, 995, 818, 1476, 406, 551, 1700, 676, 1785, 562, 504, 1501, 2838, 1155, 978, 733, 344, 901, 5217, 526, 597, 2973, 788, 499, 1303, 840, 1128, 1166, 1389, 655, 676, 1182, 506, 869, 307, 1599, 4273, 884, 623, 1038, 1908, 1199, 1731, 805, 701, 586, 3129, 1356, 664, 2049, 339, 1497, 2386, 550, 1046, 564, 1438, 542, 2380, 1258, 1336, 197, 292, 789, 1945, 3990, 860, 1194, 599, 1054, 890, 604, 482, 175, 564, 520, 896, 1496, 1062, 2528, 1436, 621, 304, 511, 3378, 894, 1124, 954, 899, 1141, 193, 270, 222, 670, 716, 2484, 1298, 603, 777, 361, 543, 2947, 192, 1093, 409, 923, 676, 555, 1035, 864, 599, 713, 1110, 1296, 722, 499, 693, 658, 1638, 1179, 1149, 532, 1456, 399, 931, 1165, 529, 1840, 767, 3429, 300, 274, 1121, 992, 764, 1284, 547, 765, 1440, 575, 4851, 941, 221, 1154, 1134, 335, 864, 1532, 994, 374, 696, 1378, 1052, 3138, 730, 1410, 989, 2779, 548, 4486, 923, 654, 413, 794, 572, 1484, 1213, 3870, 802, 881, 902, 1581, 541, 1496, 1294, 4646, 711, 3638, 1606, 561, 3902, 1040, 167, 834, 2216, 689, 643, 544, 668, 1060, 747, 2123, 585, 662, 1518, 540, 815, 1252, 908, 921, 245, 765, 528, 1311, 981, 848, 982, 1055, 741, 1129, 603, 670, 759, 2704, 1686, 794, 931, 670, 2728, 1276, 562, 503, 538, 614, 2292, 479, 841, 585, 1610, 1150, 794, 984, 3239, 607, 231, 1111, 594, 305, 1021, 500, 436, 652, 618, 1819, 532, 714, 1046, 1537, 1736, 585, 512, 517, 674, 764, 584, 2752, 2128, 579, 1057, 635, 330, 539, 517, 254, 3466, 1501, 789, 4503, 496, 557, 724, 1487, 732, 542, 1088, 1502, 453, 1411, 736, 1181, 978, 620, 919, 573, 1202, 2908, 387, 1889, 1025, 866, 599, 1476, 1254, 545, 706, 2102, 1613, 1025, 976, 1260, 217, 549, 503, 533, 1949, 3157, 1650, 725, 859, 779, 1119, 730, 516, 1211, 526, 855, 2124, 788, 779, 570, 1281, 1554, 850, 517, 365, 607, 713, 2107, 568, 291, 2371, 1217, 1013, 2261, 679, 717, 381, 1861, 240, 877, 382, 1402, 796, 1996, 632, 219, 814, 489, 1177, 842, 2460, 498, 787, 859, 2364, 715, 585, 487, 1104, 1320, 638, 613, 1094, 306, 5244, 1985, 618, 2313, 1023, 2424, 1017, 3054, 953, 758, 965, 854, 1447, 865, 259, 818, 719, 779, 1695, 894, 773, 876, 327, 775, 266, 617, 1050, 1270, 1065, 243, 1080, 664, 1842, 998, 2743, 600, 327, 1596, 1126, 1040, 707, 1884, 2355, 1543, 943, 1774, 894, 1086, 1857, 922, 4027, 840, 1724, 1267, 1111, 2120, 1033, 1539, 1800, 558, 759, 1129, 643, 884, 1321, 905, 1324, 703, 732, 391, 514, 531, 836, 597, 2616, 700, 459, 2482, 2525, 616, 309, 1901, 228, 2918, 764, 844, 2071, 850, 1012, 798, 915, 548, 636, 1434, 779, 2167, 685, 4888, 498, 1555, 560, 1616, 1348, 1359, 2021, 1286, 180, 613, 623, 794, 2923, 1102, 625, 296, 2537, 514, 1346, 759, 547, 492, 186, 1368, 791, 520, 1189, 541, 672, 727, 793, 668, 612, 1344, 1945, 1190, 576, 1097, 715, 369, 635, 305, 2110, 729, 1382, 3668, 917, 1413, 726, 907, 697, 721, 278, 650, 323, 2244, 626, 140, 1307, 322, 776, 942, 1053, 237, 217, 582, 523, 405, 3445, 641, 771, 559, 723, 416, 549, 652, 545, 221, 154, 637, 456, 2315, 891, 1093, 443, 2261, 261, 932, 404, 533, 578, 2704, 331, 1206, 607, 503, 1128, 1444, 1236, 957, 529, 1205, 418, 393, 180, 2439, 883, 288, 1146, 1360, 402, 500, 1146, 701, 1406, 1471, 1945, 1896, 1156, 1245, 1588, 368, 569, 1491, 805, 395, 507, 537, 603, 284, 731, 754, 500, 831, 622, 598, 494, 1358, 828, 545, 820, 3010, 1135, 1243, 220, 643, 660, 670, 1096, 1788, 2285, 581, 801, 1747, 1431, 640, 397, 179, 1958, 962, 1216, 634, 342, 191, 898, 292, 599, 851, 402, 563, 448, 2271, 1447, 1127, 246, 1377, 1284, 849, 1832, 3013, 551, 577, 1672, 1645, 2717, 1035, 695, 684, 1336, 219, 2893, 624, 786, 828, 832, 630, 610, 579, 631, 528, 718, 864, 712, 925, 667, 96, 786, 2144, 1364, 928, 927, 342, 3205, 473, 887, 1612, 805, 1118, 2262, 480, 706, 1049, 4356, 1889, 526, 1335, 690, 3339, 1339, 202, 389, 1826, 879, 909, 1615, 1671, 440, 547, 4132, 639, 1002, 592, 437, 690, 582, 801, 1334, 1251, 1635, 231, 4619, 785, 2387, 552, 3094, 1145, 538, 2136, 1861, 371, 1000, 207, 3202, 272, 1583, 3296, 1626, 706, 1599, 2047, 2447, 857, 2568, 1008, 779, 256, 612, 843, 702, 2666, 1808, 1369, 2032, 1751, 1056, 671, 201, 767, 720, 873, 3948, 584, 472, 211, 303, 1910, 1424, 668, 2576, 850, 1027, 392, 2201, 511, 544, 941, 298, 754, 1048, 263, 819, 2796, 569, 850, 557, 775, 299, 563, 706, 563, 2995, 1698, 1821, 993, 1081, 726, 1097, 844, 708, 802, 797, 1532, 338, 1995, 2139, 3686, 525, 683, 550, 1082, 574, 1662, 1152, 518, 813, 963, 731, 1299, 2405, 646, 1569, 1913, 3686, 549, 602, 757, 655, 1211, 552, 655, 1746, 673, 1133, 3509, 610, 714, 1094, 1218, 711, 1641, 1984, 2987, 535, 2465, 702, 575, 1534, 1339, 1127, 948, 2917, 266, 585, 559, 386, 1153, 896, 5069, 553, 616, 581, 554, 1565, 165, 1609, 532, 1230, 431, 1401, 1309, 1515, 632, 525, 350, 1079, 528, 278, 629, 592, 1930, 517, 662, 2001, 687, 902, 648, 904, 1066, 1611, 304, 655, 718, 549, 1049, 391, 808, 555, 1295, 786, 6677, 307, 818, 211, 2545, 628, 1061, 1633, 270, 1246, 209, 810, 721, 524, 864, 1599, 555, 562, 971, 534, 996, 1170, 2728, 558, 889, 791, 1058, 1128, 516, 1326, 1647, 517, 1677, 1027, 862, 345, 2424, 610, 212, 1351, 1405, 559, 1298, 679, 4598, 946, 206, 958, 3683, 604, 449, 721, 531, 732, 720, 836, 1770, 308, 1572, 1357, 1166, 1912, 1721, 1077, 463, 414, 887, 825, 1251, 1109, 1717, 970, 2702, 2660, 1342, 367, 640, 431, 1137, 283, 271, 3010, 1027, 800, 1730, 2647, 951, 1374, 1261, 672, 498, 1382, 253, 421, 637, 629, 2818, 527, 4309, 583, 954, 415, 440, 2845, 981, 586, 612, 812, 3290, 813, 846, 1319, 1292, 869, 865, 791, 765, 579, 1130, 936, 784, 1864, 643, 1552, 505, 533, 1644, 2506, 1684, 493, 1099, 400, 3260, 386, 650, 1176, 597, 909, 630, 294, 1914, 839, 300, 555, 223, 1064, 2204, 591, 1023, 832, 629, 2046, 975, 1600, 665, 837, 783, 814, 2222, 411, 995, 1257, 1119, 2456, 376, 1910, 796, 944, 1084, 679, 1055, 5008, 451, 1039, 575, 1198, 366, 1508, 602, 613, 1759, 1638, 1465, 3502, 497, 207, 1145, 659, 358, 1299, 1494, 704, 299, 920, 4891, 657, 4919, 503, 575, 732, 579, 805, 880, 1579, 1033, 900, 520, 573, 1102, 1006, 588, 650, 818, 653, 564, 234, 1100, 294, 1869, 1066, 666, 637, 612, 954, 1355, 428, 270, 1926, 697, 919, 1368, 700, 2522, 983, 270, 1446, 633, 2498, 247, 636, 726, 1088, 829, 447, 1079, 767, 701, 759, 1589, 194, 585, 685, 781, 2223, 529, 1038, 824, 452, 503, 3827, 2520, 1309, 2558, 270, 854, 1330, 534, 1659, 1624, 692, 2073, 593, 621, 341, 1102, 682, 1213, 1825, 1403, 670, 833, 794, 555, 2508, 457, 384, 862, 652, 2094, 3185, 436, 714, 883, 461, 2225, 271, 1940, 829, 719, 935, 936, 775, 1066, 458, 1745, 262, 1818, 2535, 2137, 343, 1462, 601, 696, 652, 555, 1872, 359, 1052, 210, 613, 795, 174, 729, 671, 751, 1060, 1578, 716, 275, 1596, 2838, 663, 1867, 542, 4475, 832, 738, 2628, 652, 204, 594, 711, 449, 3373, 639, 2780, 2140, 334, 795, 894, 525, 2111, 556, 1395, 682, 1499, 243, 2276, 794, 1855, 793, 3011, 1253, 1124, 606, 1267, 2120, 814, 646, 2659, 528, 1156, 695, 340, 1037, 586, 471, 602, 1458, 980, 1446, 3025, 1426, 756, 888, 484, 1217, 1084, 1509, 2110, 663, 652, 332, 538, 645, 1393, 786, 229, 547, 303, 555, 4331, 955, 1319, 1216, 569, 1006, 935, 1082, 708, 588, 471, 1874, 577, 588, 818, 107, 180, 1933, 1061, 1609, 579, 2245, 1802, 1239, 304, 1582, 438, 1555, 876, 1771, 573, 664, 867, 713, 561, 734, 2135, 889, 3289, 1128, 472, 804, 3443, 637, 717, 1006, 730, 4039, 1510, 670, 622, 935, 550, 774, 1236, 554, 528, 711, 921, 323, 748, 1177, 628, 2285, 937, 392, 3174, 276, 1221, 1172, 1703, 1645, 384, 474, 948, 393, 1929, 1289, 537, 3155, 831, 714, 1345, 619, 2710, 610, 587, 797, 549, 1389, 1126, 1082, 2604, 263, 632, 651, 959, 755, 2137, 769, 287, 1254, 807, 567, 594, 877, 1422, 1064, 2300, 522, 602, 1196, 530, 2687, 549, 1168, 598, 513, 1148, 1081, 314, 2116, 320, 188, 515, 617, 1007, 1267, 1395, 699, 380, 351, 675, 942, 1292, 1382, 2728, 2237, 1667, 3502, 809, 604, 5475, 406, 1457, 706, 4080, 869, 691, 894, 944, 1201, 747, 228, 617, 863, 581, 722, 1689, 856, 1381, 4753, 587, 815, 572, 541, 794, 529, 733, 1640, 912, 1203, 973, 2038, 702, 1741, 893, 751, 530, 551, 742, 542, 517, 1290, 1475, 1211, 646, 710, 754, 1064, 3062, 1485, 1315, 851, 1399, 1500, 906, 2881, 1116, 985, 2448, 739, 683, 759, 2253, 668, 817, 1502, 573, 784, 1864, 588, 2151, 963, 1391, 553, 805, 538, 1853, 716, 649, 697, 605, 534, 460, 847, 540, 748, 2215, 2109, 861, 650, 559, 536, 943, 3700, 183, 622, 2412, 3468, 1207, 4252, 1287, 1722, 2460, 804, 687, 1096, 3201, 2485, 3275, 848, 1452, 1137, 2559, 2408, 738, 902, 394, 1439, 2489, 717, 1625, 2661, 1198, 2788, 465, 849, 619, 1029, 1697, 754, 587, 1898, 587, 2805, 1521, 1751, 1469, 142, 1261, 983, 395, 273, 526, 1476, 658, 1808, 377, 254, 1184, 582, 686, 918, 806, 372, 1176, 2680, 646, 1374, 582, 677, 525, 589, 972, 827, 514, 1016, 577, 782, 582, 682, 552, 713, 1219, 539, 736, 1510, 833, 587, 239, 1636, 822, 1514, 898, 501, 259, 4212, 1875, 907, 803, 979, 558, 643, 246, 719, 834, 1038, 2334, 322, 549, 653, 982, 2054, 646, 1407, 715, 738, 881, 2396, 623, 1690, 890, 947, 4753, 1645, 1539, 952, 778, 353, 2413, 180, 921, 2196, 825, 2737, 877, 1113, 653, 611, 458, 654, 528, 580, 780, 653, 958, 673, 1546, 6662, 718, 1434, 660, 208, 1191, 480, 663, 477, 611, 2459, 1153, 2029, 1764, 1709, 847, 758, 585, 2240, 704, 965, 1172, 601, 598, 387, 542, 873, 645, 327, 1719, 567, 1249, 701, 899, 195, 654, 701, 3526, 545, 548, 2812, 3743, 613, 1507, 2936, 751, 589, 567, 1039, 377, 465, 810, 1012, 524, 1236, 596, 495, 805, 543, 554, 478, 3445, 561, 1133, 589, 1269, 537, 279, 1606, 1666, 2594, 309, 627, 359, 2197, 569, 569, 531, 912, 1035, 574, 2378, 533, 2218, 1111, 742, 1810, 1115, 3327, 1469, 2129, 570, 3586, 666, 986, 2894, 966, 174, 3215, 830, 549, 761, 790, 1893, 301, 852, 681, 2083, 1382, 1192, 733, 705, 858, 731, 772, 1093, 751, 1704, 589, 638, 499, 669, 1891, 580, 1014, 1253, 995, 531, 1404, 606, 259, 343, 501, 1061, 491, 898, 1310, 1982, 97, 371, 426, 271, 4246, 1804, 1057, 932, 679, 1394, 961, 1343, 2698, 1891, 525, 574, 1837, 1444, 1258, 1569, 1872, 615, 810, 1564, 437, 278, 1103, 460, 615, 638, 564, 6068, 788, 628, 4222, 778, 540, 1786, 279, 535, 410, 2001, 1776, 546, 1286, 1404, 575, 745, 1421, 687, 1477, 844, 1301, 731, 557, 2062, 2461, 930, 2000, 701, 1648, 1579, 2424, 501, 2096, 1453, 724, 1872, 751, 678, 939, 862, 1235, 334, 851, 660, 2009, 547, 1635, 542, 898, 712, 972, 670, 1039, 1868, 652, 629, 1367, 546, 541, 1334, 602, 952, 2485, 1301, 436, 628, 558, 232, 807, 397, 283, 4005, 335, 453, 1057, 763, 1715, 597, 5048, 2029, 801, 941, 1670, 3018, 3696, 588, 472, 1278, 781, 947, 1725, 951, 1360, 1653, 396, 3267, 692, 1840, 1153, 875, 565, 1084, 2055, 1392, 569, 515, 668, 4491, 1666, 1940, 1030, 584, 529, 2785, 1594, 915, 1158, 444, 505, 339, 565, 1348, 2001, 314, 649, 2642, 713, 982, 1317, 762, 1327, 1565, 386, 633, 848, 773, 651, 462, 608, 1300, 557, 480, 102, 3252, 1099, 537, 2215, 187, 2869, 694, 543, 2986, 545, 681, 262, 3990, 263, 665, 339, 1733, 303, 1275, 279, 961, 746, 573, 637, 555, 1366, 292, 572, 596, 473, 277, 600, 57, 786, 599, 759, 572, 606, 1237, 1089, 1111, 908, 577, 780, 122, 610, 556, 226, 1374, 1313, 534, 721, 1116, 592, 827, 546, 929, 878, 2257, 1135, 538, 645, 195, 1701, 1844, 1850, 2862, 1113, 549, 1279, 644, 884, 1369, 602, 555, 1090, 491, 1217, 1444, 646, 454, 477, 503, 957, 371, 961, 1408, 673, 1068, 641, 2001, 1927, 537, 599, 591, 726, 191, 787, 2496, 846, 560, 676, 282, 1027, 391, 601, 1185, 539, 3066, 623, 555, 614, 563, 1313, 661, 526, 669, 707, 893, 790, 247, 648, 551, 2388, 577, 1369, 429, 4113, 598, 825, 646, 1171, 1126, 1248, 582, 1647, 999, 1933, 589, 541, 568, 1140, 964, 682, 797, 225, 1186, 688, 837, 982, 792, 1330, 1940, 269, 972, 528, 3486, 3509, 301, 654, 531, 350, 1324, 859, 660, 641, 2449, 571, 2552, 559, 1247, 565, 703, 1092, 878, 225, 1066, 1452, 3947, 2076, 877, 652, 1452, 586, 2444, 224, 1670, 636, 525, 615, 884, 612, 2409, 383, 308, 334, 598, 2158, 1094, 256, 2392, 585, 1340, 870, 721, 642, 169, 982, 562, 943, 540, 632, 704, 1784, 347, 632, 625, 542, 813, 1606, 1764, 728, 490, 204, 130, 161, 342, 429, 2391, 1388, 1774, 632, 1203, 629, 373, 167, 250, 832, 1142, 1148, 363, 632, 3144, 570, 324, 952, 214, 575, 680, 758, 596, 607, 4449, 537, 858, 473, 556, 556, 1645, 585, 2213, 557, 538, 938, 536, 1194, 966, 2005, 709, 587, 2989, 1101, 2409, 2021, 571, 1988, 4283, 775, 2205, 3709, 1493, 608, 1921, 516, 2761, 525, 931, 507, 564, 595, 1200, 498, 793, 234, 747, 4147, 775, 577, 2857, 297, 987, 691, 1260, 2692, 291, 726, 690, 445, 625, 191, 4641, 1481, 623, 1384, 1181, 301, 2551, 682, 327, 1142, 373, 3517, 1062, 444, 619, 243, 1734, 1236, 597, 668, 769, 831, 432, 505, 947, 1136, 850, 2467, 755, 853, 1656, 377, 1928, 497, 742, 2468, 932, 715, 696, 938, 552, 1275, 2180, 1220, 1256, 705, 961, 509, 1378, 261, 1348, 604, 1028, 1956, 2022, 827, 850, 949, 557, 722, 498, 964, 1021, 553, 953, 2529, 206, 281, 2858, 407, 224, 1088, 1066, 2846, 1368, 696, 705, 639, 624, 496, 2062, 1607, 911, 1109, 663, 584, 922, 731, 800, 2711, 1489, 623, 731, 1244, 696, 2078, 1309, 816, 2796, 1838, 943, 1382, 817, 651, 1311, 537, 829, 1934, 880, 840, 508, 610, 739, 3071, 492, 286, 651, 1941, 1344, 781, 545, 460, 1330, 1117, 589, 573, 622, 557, 875, 152, 294, 544, 586, 852, 680, 448, 1295, 648, 1877, 705, 2118, 702, 4291, 839, 710, 620, 525, 3860, 575, 1082, 652, 330, 158, 1023, 2789, 651, 598, 752, 1203, 2161, 255, 1057, 543, 1071, 647, 535, 1393, 582, 612, 782, 814, 699, 548, 778, 1136, 2022, 698, 955, 584, 918, 1847, 950, 1248, 542, 522, 1021, 819, 773, 966, 573, 1188, 1129, 1200, 853, 278, 986, 761, 599, 1664, 1598, 1007, 1518, 745, 730, 537, 1111, 1453, 614, 2422, 509, 1194, 1575, 726, 1263, 631, 574, 1757, 252, 518, 1206, 731, 440, 1029, 1112, 680, 66, 1454, 1048, 1688, 854, 739, 256, 654, 1623, 646, 1422, 943, 684, 1063, 3293, 585, 539, 3884, 577, 2116, 1700, 560, 559, 647, 483, 718, 1789, 1585, 549, 555, 1405, 824, 2213, 2370, 1266, 1495, 472, 613, 934, 535, 498, 1469, 2280, 780, 1039, 1251, 402, 536, 878, 582, 1274, 1325, 634, 629, 1384, 565, 271, 1192, 561, 937, 1045, 637, 517, 570, 562, 4769, 2059, 667, 2486, 679, 1074, 1025, 1198, 609, 237, 1580, 756, 209, 520, 487, 801, 303, 1104, 2049, 1603, 714, 737, 3652, 1802, 574, 794, 355, 326, 525, 1290, 496, 3396, 269, 752, 1506, 844, 689, 648, 709, 345, 626, 761, 1219, 699, 1864, 300, 827, 362, 718, 576, 800, 809, 998, 2450, 1142, 682, 563, 877, 1877, 579, 644, 2310, 1187, 548, 2264, 475, 589, 644, 2649, 567, 299, 2063, 693, 1277, 1928, 2164, 645, 636, 615, 1017, 172, 1165, 622, 693, 231, 449, 1305, 1405, 596, 724, 694, 663, 554, 734, 1030, 561, 510, 286, 672, 829, 800, 680, 535, 1027, 706, 576, 892, 525, 253, 782, 551, 1416, 2485, 266, 729, 935, 1165, 742, 666, 1018, 1018, 1370, 788, 1251, 568, 529, 874, 1839, 541, 510, 1223, 2194, 3979, 537, 1289, 958, 227, 225, 855, 299, 1437, 597, 390, 2596, 1236, 764, 820, 608, 519, 634, 2097, 831, 771, 744, 1434, 2127, 1414, 539, 1665, 585, 1204, 912, 779, 2063, 573, 734, 595, 535, 1838, 636, 727, 1482, 2821, 952, 972, 698, 4183, 4676, 693, 2166, 750, 2277, 509, 695, 2434, 660, 932, 803, 826, 1215, 847, 501, 820, 262, 1349, 798, 3283, 1184, 1096, 229, 1006, 578, 1307, 430, 670, 1179, 924, 666, 169, 674, 1865, 1221, 1320, 549, 699, 1997, 1522, 497, 984, 1520, 1179, 1212, 889, 1603, 653, 502, 859, 1616, 239, 544, 3902, 814, 845, 316, 644, 453, 562, 1255, 1108, 1377, 2015, 711, 1386, 1852, 515, 869, 369, 544, 654, 2023, 1419, 497, 521, 1782, 637, 1102, 697, 3460, 552, 662, 508, 533, 517, 290, 591, 1581, 1133, 2930, 1189, 665, 1653, 2005, 2431, 1553, 2037, 211, 1240, 907, 452, 1097, 737, 1141, 3245, 553, 426, 414, 1282, 924, 785, 807, 307, 1135, 1733, 1693, 732, 627, 2165, 1584, 791, 745, 3027, 973, 691, 3070, 538, 763, 1620, 518, 1845, 602, 700, 210, 1062, 990, 562, 1091, 507, 1738, 698, 2513, 935, 956, 876, 1219, 1037, 214, 203, 955, 1018, 645, 1172, 574, 654, 2442, 779, 1217, 699, 276, 114, 1207, 4022, 283, 1679, 542, 821, 2674, 554, 261, 907, 1025, 2021, 3196, 1761, 1157, 915, 331, 567, 901, 518, 635, 597, 882, 1675, 2808, 1569, 821, 964, 958, 571, 1341, 589, 1690, 1490, 851, 557, 723, 674, 699, 1904, 733, 3866, 1132, 559, 434, 611, 587, 281, 1777, 1309, 1339, 927, 582, 1009, 598, 1109, 1618, 892, 696, 4570, 1134, 1831, 269, 553, 977, 113, 581, 1441, 784, 731, 295, 969, 4860, 246, 1375, 876, 1329, 3563, 718, 2020, 2350, 670, 3466, 623, 556, 220, 613, 843, 146, 2976, 609, 668, 1200, 600, 1139, 713, 540, 1097, 795, 671, 939, 855, 1474, 535, 3428, 382, 1991, 678, 973, 600, 633, 2778, 4591, 1264, 693, 734, 716, 1190, 1319, 551, 439, 861, 2187, 793, 453, 3531, 1567, 1476, 727, 560, 606, 1310, 243, 917, 2125, 756, 643, 259, 578, 474, 1362, 654, 530, 1918, 1832, 911, 571, 1363, 3697, 1317, 648, 654, 2467, 728, 1110, 371, 854, 1864, 5061, 796, 1383, 1105, 374, 797, 2781, 715, 906, 255, 2697, 475, 884, 726, 703, 2538, 489, 653, 679, 3344, 519, 790, 1060, 958, 571, 442, 509, 928, 941, 613, 691, 1153, 1569, 1045, 1421, 1359, 879, 1936, 2272, 546, 2263, 1201, 719, 698, 200, 700, 397, 760, 573, 1358, 248, 589, 664, 544, 3198, 1767, 690, 1882, 604, 771, 1292, 2092, 854, 207, 415, 550, 2134, 2665, 612, 588, 2533, 460, 230, 651, 1640, 680, 1081, 671, 781, 453, 1445, 328, 1098, 437, 651, 338, 1354, 780, 602, 960, 2400, 805, 2555, 204, 535, 534, 266, 4426, 984, 3531, 1489, 2361, 555, 1988, 820, 413, 1230, 370, 599, 397, 819, 370, 3836, 1327, 1224, 572, 592, 507, 816, 780, 461, 1150, 1389, 579, 858, 570, 1135, 1168, 963, 859, 591, 552, 1056, 1984, 669, 281, 1191, 1361, 565, 543, 805, 1113, 877, 607, 1101, 735, 2110, 718, 584, 218, 1669, 1053, 383, 1212, 169, 450, 564, 554, 360, 4496, 1112, 3649, 201, 566, 696, 203, 355, 700, 831, 319, 414, 1306, 582, 562, 887, 1030, 753, 2113, 1263, 611, 688, 1534, 832, 630, 590, 622, 1107, 511, 580, 1299, 946, 1894, 844, 7712, 682, 453, 628, 612, 900, 1373, 285, 570, 578, 377, 676, 899, 378, 183, 1353, 1668, 2901, 1556, 565, 3359, 2447, 479, 215, 742, 390, 1344, 455, 564, 1081, 842, 375, 225, 514, 407, 694, 1990, 643, 2487, 1130, 634, 1313, 1364, 922, 1462, 860, 2144, 346, 262, 209, 473, 1210, 1440, 1990, 356, 1448, 1235, 3163, 693, 974, 620, 485, 495, 203, 950, 789, 668, 1567, 1125, 1451, 557, 357, 1259, 321, 528, 518, 311, 660, 1063, 4374, 437, 575, 1126, 964, 566, 2635, 1246, 576, 2917, 298, 2007, 1323, 631, 756, 851, 855, 776, 680, 691, 931, 1722, 4427, 1650, 4954, 1574, 2339, 485, 641, 3087, 2869, 524, 1177, 1559, 734, 1598, 2392, 455, 2984, 1647, 804, 761, 237, 317, 233, 2700, 1350, 2111, 411, 871, 1348, 220, 910, 1186, 780, 583, 803, 1189, 1015, 539, 2968, 2889, 4670, 1221, 244, 352, 1408, 4750, 1292, 683, 1111, 636, 221, 989, 2573, 547, 520, 603, 645, 2269, 918, 2019, 675, 810, 323, 521, 748, 1108, 877, 1983, 1285, 1592, 1022, 1047, 211, 3094, 3350, 539, 506, 1112, 532, 1360, 801, 300, 558, 621, 813, 583, 642, 315, 778, 657, 771, 1128, 1078, 2475, 527, 621, 701, 1040, 358, 1262, 321, 1055, 1122, 1739, 2651, 559, 843, 1123, 297, 689, 762, 1268, 994, 410, 3151, 309, 1492, 1058, 548, 752, 383, 833, 333, 1565, 1954, 677, 615, 345, 379, 1987, 316, 635, 893, 1838, 1498, 1342, 3308, 700, 696, 1448, 181, 2080, 875, 611, 576, 1658, 1027, 508, 310, 3901, 1141, 2413, 615, 1331, 530, 266, 527, 789, 1402, 334, 1532, 1313, 482, 1060, 3116, 1210, 543, 563, 1401, 2001, 1360, 704, 3279, 4296, 2033, 550, 3389, 589, 1268, 4668, 2363, 1778, 943, 950, 721, 345, 632, 1994, 248, 545, 585, 706, 639, 681, 2243, 1200, 941, 1193, 4934, 797, 956, 610, 510, 356, 560, 529, 1111, 221, 3499, 671, 469, 2351, 639, 423, 1197, 1120, 617, 882, 758, 636, 938, 718, 495, 1134, 797, 766, 1076, 994, 1171, 1197, 4021, 876, 700, 1061, 677, 886, 816, 872, 741, 926, 998, 840, 527, 1230, 929, 1273, 543, 536, 596, 1311, 828, 617, 611, 591, 1584, 2529, 1186, 1083, 419, 586, 737, 2150, 1188, 3964, 1389, 2795, 792, 1062, 2328, 848, 638, 6105, 533, 2389, 1705, 590, 892, 1104, 767, 1861, 691, 907, 1467, 633, 755, 567, 622, 707, 843, 616, 549, 996, 1349, 472, 897, 747, 2298, 3482, 4607, 683, 682, 1415, 1796, 966, 902, 257, 1856, 881, 715, 877, 1971, 657, 590, 172, 282, 315, 718, 258, 1549, 521, 1094, 556, 2583, 871, 462, 279, 640, 1485, 1384, 916, 746, 2880, 1245, 750, 1258, 700, 654, 415, 1583, 1523, 1214, 750, 700, 564, 428, 207, 1050, 538, 1167, 883, 915, 2230, 2687, 362, 1819, 1926, 369, 385, 549, 526, 516, 590, 830, 495, 2259, 449, 2950, 1668, 469, 914, 790, 555, 464, 788, 488, 869, 1374, 1141, 1120, 1619, 946, 338, 2097, 205, 856, 1530, 634, 346, 1223, 867, 646, 4319, 531, 534, 577, 1387, 477, 770, 501, 517, 508, 841, 540, 710, 284, 569, 575, 465, 776, 605, 1235, 409, 842, 618, 520, 299, 672, 609, 1278, 512, 834, 706, 278, 995, 738, 481, 549, 290, 1413, 1248, 275, 1282, 388, 230, 1954, 490, 1406, 3243, 602, 705, 200, 786, 5332, 582, 560, 678, 2046, 533, 582, 1826, 750, 512, 1003, 1238, 238, 232, 3450, 643, 2114, 1381, 1000, 881, 1169, 551, 838, 2596, 698, 582, 529, 1345, 663, 1877, 1135, 343, 569, 569, 278, 1159, 501, 543, 637, 2307, 625, 403, 1529, 4681, 223, 460, 654, 512, 354, 591, 623, 2788, 859, 657, 520, 1616, 312, 1780, 857, 221, 1228, 2240, 2121, 544, 1882, 749, 1332, 926, 842, 592, 769, 458, 672, 887, 2354, 1881, 592, 568, 1713, 2185, 1044, 965, 1097, 3172, 339, 540, 596, 2882, 683, 762, 1031, 915, 545, 1306, 291, 518, 964, 608, 1504, 579, 834, 676, 1675, 478, 1056, 1052, 2125, 1122, 1673, 528, 843, 112, 824, 1535, 545, 528, 522, 475, 992, 993, 302, 792, 485, 553, 1366, 557, 689, 947, 285, 1448, 2221, 514, 542, 610, 1274, 462, 1980, 180, 731, 519, 807, 733, 2704, 894, 566, 879, 797, 906, 3073, 661, 1265, 559, 570, 957, 536, 1771, 923, 3164, 980, 482, 592, 600, 517, 473, 583, 755, 388, 357, 650, 924, 615, 625, 1168, 265, 643, 1511, 1064, 584, 1037, 603, 3258, 538, 2477, 713, 2394, 640, 679, 561, 535, 947, 998, 2614, 1263, 2744, 516, 591, 909, 1135, 453, 265, 1125, 691, 791, 932, 1254, 619, 3022, 574, 2230, 1311, 536, 779, 772, 3381, 1852, 592, 517, 580, 1851, 2192, 569, 2135, 658, 394, 789, 315, 693, 952, 1295, 1009, 241, 1564, 859, 926, 1183, 285, 2076, 1572, 864, 1700, 2262, 607, 590, 1446, 376, 1556, 2911, 547, 3015, 701, 4829, 531, 623, 377, 4141, 1266, 583, 2521, 199, 592, 849, 250, 787, 3106, 502, 1135, 4807, 3286, 219, 789, 560, 1108, 744, 1421, 574, 1130, 3135, 1973, 695, 766, 3334, 1417, 584, 518, 661, 509, 601, 1941, 1603, 684, 298, 244, 755, 1489, 1458, 876, 1723, 1103, 1317, 569, 923, 1050, 1142, 1131, 4199, 635, 684, 604, 798, 805, 1730, 868, 454, 1493, 646, 1117, 365, 791, 1315, 811, 1094, 1097, 1011, 821, 657, 729, 1120, 1491, 1164, 561, 1882, 146, 852, 669, 457, 4203, 649, 857, 1641, 674, 228, 1074, 413, 810, 1419, 1606, 1614, 2705, 703, 593, 2020, 578, 3149, 603, 469, 612, 1515, 924, 810, 1543, 1653, 1692, 1087, 536, 268, 769, 718, 1539, 742, 1037, 1868, 1467, 234, 1391, 1051, 611, 1770, 877, 722, 549, 297, 1097, 646, 1407, 1258, 567, 1065, 2961, 177, 4022, 333, 356, 986, 1468, 743, 1088, 2200, 2695, 175, 627, 1453, 2916, 547, 929, 545, 4278, 1749, 2566, 480, 877, 572, 286, 1061, 714, 525, 1564, 746, 1063, 370, 1101, 1919, 1758, 620, 2113, 742, 688, 545, 2215, 538, 611, 710, 1182, 585, 570, 612, 529, 197, 1570, 573, 1881, 1935, 1325, 359, 636, 563, 344, 1610, 1577, 432, 174, 252, 1075, 711, 872, 1989, 511, 651, 527, 1119, 690, 601, 2845, 483, 857, 185, 1279, 185, 692, 1307, 741, 2455, 526, 355, 725, 756, 4803, 700, 899, 551, 336, 1003, 1602, 417, 814, 440, 975, 1924, 955, 1412, 606, 845, 1596, 659, 577, 292, 557, 189, 2839, 611, 598, 776, 856, 1377, 307, 606, 917, 796, 1498, 774, 698, 692, 1325, 296, 1938, 698, 570, 664, 2850, 2412, 624, 1124, 1249, 875, 581, 792, 1564, 870, 851, 1353, 1000, 1956, 610, 374, 602, 665, 690, 899, 510, 3065, 622, 605, 3287, 757, 599, 1621, 2434, 1625, 3428, 686, 525, 962, 883, 611, 495, 1375, 2819, 682, 504, 2762, 580, 1058, 2244, 611, 583, 237, 1130, 977, 924, 1065, 851, 588, 819, 552, 1212, 866, 1184, 2000, 559, 1422, 502, 1162, 673, 398, 2397, 572, 614, 364, 519, 619, 522, 827, 826, 698, 1058, 540, 535, 1064, 577, 992, 4216, 580, 1288, 584, 576, 499, 872, 1592, 1626, 4964, 698, 703, 648, 439, 1057, 3195, 2707, 981, 354, 1015, 860, 857, 806, 293, 1242, 324, 1698, 689, 1329, 2820, 2037, 392, 1368, 3710, 887, 1128, 1893, 824, 1116, 1116, 711, 415, 645, 913, 557, 832, 1674, 784, 709, 716, 2027, 587, 678, 1949, 851, 718, 2871, 771, 2915, 488, 494, 1047, 381, 841, 542, 415, 562, 819, 1192, 1149, 780, 615, 3597, 1584, 982, 824, 558, 3488, 1306, 918, 751, 766, 676, 1917, 767, 680, 3621, 604, 606, 858, 1100, 830, 579, 1105, 751, 509, 2949, 752, 569, 785, 418, 990, 626, 748, 592, 725, 743, 1209, 703, 614, 822, 889, 3150, 944, 1765, 1940, 286, 865, 1269, 1822, 3658, 602, 639, 685, 1015, 977, 669, 557, 585, 2320, 610, 612, 4613, 463, 712, 559, 1680, 291, 679, 2891, 617, 1283, 1851, 181, 880, 520, 2273, 683, 714, 617, 972, 372, 4570, 543, 497, 1812, 597, 1339, 798, 2314, 2688, 1497, 943, 543, 611, 1045, 830, 1243, 667, 419, 197, 1974, 185, 834, 1551, 540, 2221, 422, 537, 934, 756, 826, 1420, 1148, 1676, 799, 762, 1331, 1071, 398, 986, 560, 1828, 755, 751, 621, 2954, 705, 609, 399, 618, 582, 1716, 768, 527, 257, 204, 352, 1645, 632, 570, 2354, 763, 798, 545, 670, 487, 772, 706, 219, 376, 2274, 511, 1054, 5388, 803, 409, 1038, 545, 645, 1055, 417, 1993, 470, 3584, 913, 893, 491, 223, 629, 701, 1906, 1068, 264, 1076, 728, 3144, 1382, 243, 327, 540, 740, 787, 1759, 2910, 1472, 579, 809, 448, 798, 1721, 994, 633, 1614, 1985, 188, 907, 743, 636, 2676, 882, 4595, 1267, 545, 1295, 777, 1327, 452, 564, 514, 1731, 289, 633, 1659, 708, 2226, 3659, 742, 660, 2253, 1015, 1237, 1034, 537, 686, 990, 1906, 1338, 2270, 558, 608, 589, 3989, 1059, 776, 1103, 1517, 1175, 600, 199, 1607, 886, 544, 3267, 396, 1759, 372, 746, 2759, 1459, 1373, 1167, 578, 507, 1149, 1247, 3077, 1155, 997, 859, 1125, 1377, 804, 1338, 881, 605, 1837, 936, 646, 1464, 850, 794, 3319, 3610, 1309, 741, 195, 805, 977, 736, 156, 1077, 670, 983, 592, 1388, 821, 735, 605, 1798, 933, 1451, 3432, 799, 325, 1699, 1589, 370, 662, 2411, 1068, 604, 1140, 1261, 597, 2635, 538, 1048, 3623, 647, 2205, 556, 4500, 1378, 872, 1439, 394, 734, 318, 630, 553, 474, 1588, 336, 710, 2132, 458, 1092, 500, 830, 534, 1932, 1155, 731, 544, 350, 968, 1762, 1058, 2341, 1906, 610, 1221, 945, 617, 547, 4088, 849, 1402, 451, 4179, 2175, 550, 555, 852, 3541, 657, 640, 569, 722, 357, 443, 1215, 1496, 565, 1038, 544, 695, 522, 1511, 236, 323, 559, 909, 2680, 297, 754, 694, 1229, 1466, 2651, 505, 2610, 803, 2406, 287, 1909, 541, 1310, 571, 3273, 667, 208, 518, 2758, 2822, 1539, 619, 2026, 519, 1330, 698, 1343, 621, 850, 549, 526, 686, 562, 2156, 2312, 899, 637, 553, 808, 2126, 542, 528, 643, 863, 373, 1183, 2438, 1595, 223, 625, 509, 1221, 774, 1396, 612, 837, 1480, 789, 584, 790, 1260, 2683, 662, 1022, 557, 566, 901, 627, 191, 2487, 780, 1434, 2180, 568, 4614, 817, 907, 369, 1198, 1063, 919, 543, 716, 798, 516, 548, 527, 634, 1095, 791, 589, 812, 1382, 770, 769, 991, 303, 540, 297, 646, 1500, 2343, 195, 909, 969, 598, 800, 713, 677, 731, 705, 1426, 957, 815, 2423, 760, 1082, 3092, 1329, 1125, 284, 1634, 1045, 708, 543, 1566, 2651, 4586, 665, 5130, 1128, 703, 1502, 533, 663, 2101, 744, 701, 343, 2306, 608, 686, 2236, 2616, 2760, 717, 465, 864, 2624, 655, 1006, 2196, 266, 1586, 542, 664, 779, 491, 2201, 1226, 236, 1181, 2406, 1485, 1305, 1076, 2637, 998, 734, 652, 1006, 399, 1407, 665, 938, 695, 515, 926, 1710, 1396, 724, 1118, 3708, 525, 2806, 278, 1167, 1073, 224, 2136, 524, 793, 1025, 1466, 596, 719, 1070, 192, 218, 862, 719, 390, 599, 1224, 552, 629, 533, 3021, 2625, 584, 1029, 848, 3430, 239, 885, 301, 922, 3048, 652, 681, 1087, 1446, 676, 4522, 2102, 666, 530, 675, 1426, 524, 675, 725, 546, 1864, 2267, 4811, 695, 2907, 1807, 899, 556, 1378, 1677, 888, 497, 459, 316, 727, 913, 770, 774, 689, 1286, 559, 508, 911, 1095, 399, 392, 534, 527, 1775, 2353, 904, 1133, 644, 792, 874, 720, 745, 726, 552, 1109, 285, 763, 1070, 575, 981, 543, 3325, 2811, 4362, 1225, 764, 4387, 1367, 297, 2150, 736, 737, 1745, 556, 4053, 180, 1727, 1222, 894, 766, 915, 1347, 668, 473, 1522, 1125, 1495, 1545, 1955, 1521, 705, 1162, 1327, 555, 770, 945, 1613, 820, 557, 1314, 173, 1137, 814, 622, 1285, 478, 826, 726, 556, 521, 925, 2166, 883, 730, 3426, 1906, 802, 211, 2180, 617, 481, 1461, 994, 900, 1100, 667, 460, 655, 3974, 1497, 1591, 849, 594, 2172, 484, 692, 740, 489, 2152, 581, 415, 175, 3707, 568, 627, 1788, 1116, 1177, 591, 1131, 1184, 286, 468, 555, 314, 798, 519, 499, 2760, 2098, 1112, 999, 4110, 912, 2254, 1836, 2210, 703, 841, 671, 1102, 1085, 1236, 3911, 665, 820, 940, 730, 360, 1160, 779, 1023, 1112, 701, 194, 226, 538, 534, 791, 1496, 742, 1186, 966, 1602, 909, 2825, 1167, 844, 659, 705, 745, 1684, 971, 712, 2491, 562, 167, 484, 650, 1354, 1595, 949, 543, 1210, 819, 346, 630, 2398, 1633, 593, 538, 985, 724, 2255, 1821, 463, 1006, 2574, 413, 910, 740, 700, 714, 664, 749, 648, 796, 709, 809, 771, 741, 198, 1052, 4456, 336, 261, 605, 702, 1794, 654, 617, 2038, 1427, 714, 637, 4298, 2035, 840, 576, 921, 937, 777, 1085, 560, 186, 527, 3441, 549, 512, 730, 670, 1299, 734, 1706, 684, 1207, 2240, 208, 280, 307, 978, 338, 328, 1155, 819, 471, 2501, 1207, 819, 524, 2940, 1582, 1599, 630, 241, 1021, 572, 377, 647, 612, 654, 770, 1001, 531, 969, 1144, 1156, 916, 376, 1006, 724, 1457, 2029, 1810, 532, 726, 589, 410, 997, 865, 1718, 592, 687, 1183, 776, 1381, 925, 737, 2959, 1220, 695, 2107, 1814, 4354, 408, 1491, 2016, 930, 570, 847, 1336, 549, 857, 708, 447, 1116, 3592, 439, 4379, 1688, 716, 418, 788, 525, 718, 1214, 546, 1190, 682, 571, 1168, 646, 404, 1436, 1243, 903, 1568, 405, 595, 492, 245, 233, 690, 622, 1957, 1638, 1002, 1561, 741, 765, 2630, 1678, 1219, 546, 1905, 564, 396, 1203, 2577, 1304, 616, 275, 553, 785, 646, 650, 484, 470, 1578, 562, 848, 754, 4044, 534, 671, 414, 1011, 778, 672, 724, 652, 641, 543, 2259, 1425, 912, 2362, 431, 821, 648, 766, 664, 1969, 619, 858, 3400, 1344, 1826, 556, 1265, 349, 836, 813, 581, 1047, 1972, 967, 512, 512, 1060, 570, 908, 1033, 651, 701, 707, 4785, 1496, 654, 1803, 654, 536, 2036, 383, 585, 1017, 814, 823, 1755, 1006, 1197, 474, 892, 542, 2235, 552, 802, 2822, 757, 554, 1001, 233, 638, 705, 157, 565, 1249, 537, 1380, 1248, 1309, 921, 633, 482, 821, 318, 214, 556, 641, 746, 433, 757, 1582, 517, 330, 523, 1063, 860, 935, 621, 1617, 1021, 828, 1060, 1562, 1018, 1311, 1443, 586, 1215, 574, 3320, 762, 1107, 680, 689, 677, 669, 669, 711, 3522, 3137, 873, 1624, 555, 2763, 1830, 844, 1060, 1369, 1433, 2402, 598, 2363, 2765, 335, 967, 570, 4002, 1111, 1655, 615, 1124, 1310, 2634, 1021, 1847, 1119, 827, 614, 2139, 492, 1521, 1176, 839, 736, 320, 3429, 1421, 3041, 501, 627, 4127, 908, 471, 912, 1261, 534, 677, 1197, 929, 4004, 663, 917, 1122, 660, 1294, 2815, 3105, 1859, 506, 229, 397, 465, 2313, 1217, 785, 914, 1329, 238, 505, 1016, 249, 580, 550, 1063, 4041, 867, 964, 263, 848, 230, 524, 827, 849, 157, 655, 815, 758, 801, 972, 225, 1350, 354, 1598, 3832, 726, 228, 794, 944, 1476, 886, 1320, 597, 1350, 523, 1030, 610, 581, 561, 995, 1163, 744, 1901, 1508, 1587, 799, 1817, 1411, 392, 835, 1085, 257, 207, 504, 819, 1359, 1221, 2346, 541, 516, 1078, 600, 2733, 945, 913, 763, 1774, 835, 636, 769, 813, 647, 1176, 1229, 522, 2643, 551, 1002, 1094, 219, 796, 813, 1081, 781, 253, 555, 1773, 1289, 905, 1275, 347, 804, 1174, 561, 1029, 3541, 361, 1691, 1288, 1356, 915, 2136, 660, 575, 590, 544, 2539, 596, 1020, 541, 979, 1127, 1067, 3348, 680, 505, 627, 603, 861, 2096, 4062, 1648, 1894, 1042, 1136, 2892, 2512, 893, 1224, 1652, 1071, 2352, 619, 294, 2506, 665, 635, 227, 1164, 713, 460, 866, 867, 179, 217, 779, 1018, 573, 701, 4042, 1692, 581, 2305, 508, 1100, 1046, 696, 1266, 612, 3701, 1082, 1148, 824, 491, 924, 243, 520, 604, 403, 606, 608, 340, 557, 698, 649, 4253, 1452, 494, 716, 1821, 1079, 510, 1763, 884, 1461, 690, 790, 442, 1274, 1283, 637, 1274, 232, 2276, 1608, 565, 1845, 735, 958, 1183, 586, 808, 1295, 653, 2459, 3156, 824, 869, 362, 4375, 2321, 2773, 1333, 588, 1844, 1743, 3460, 1340, 663, 592, 3421, 999, 274, 3544, 593, 371, 395, 697, 715, 1499, 745, 1699, 751, 771, 1617, 1607, 2464, 746, 1681, 1827, 3179, 791, 1921, 1343, 559, 975, 3010, 1173, 3931, 4024, 611, 852, 1164, 468, 1656, 834, 508, 1536, 1493, 667, 874, 936, 551, 654, 542, 635, 402, 1673, 459, 1138, 1010, 849, 590, 851, 1212, 606, 715, 1588, 408, 3717, 2060, 862, 2896, 591, 2344, 2441, 655, 1146, 712, 352, 607, 1050, 801, 649, 3032, 1997, 399, 970, 570, 800, 1006, 286, 2467, 677, 2206, 1209, 1048, 800, 1194, 1154, 837, 996, 1183, 1158, 663, 1802, 591, 231, 697, 872, 1681, 684, 332, 651, 315, 1400, 643, 252, 734, 717, 1090, 818, 1440, 2827, 1628, 806, 261, 1493, 1234, 3988, 695, 1842, 1738, 1003, 895, 683, 784, 767, 678, 1585, 555, 2146, 906, 704, 637, 1378, 2660, 3233, 785, 789, 957, 879, 674, 614, 682, 942, 547, 4375, 290, 677, 733, 910, 586, 1274, 1515, 649, 1484, 945, 2513, 1116, 1616, 486, 235, 721, 1120, 502, 2759, 1185, 692, 600, 528, 2021, 630, 547, 548, 943, 1821, 2744, 287, 341, 713, 567, 1202, 944, 475, 306, 654, 612, 1271, 206, 615, 2002, 1593, 690, 763, 987, 532, 739, 382, 570, 1623, 553, 562, 319, 761, 1082, 606, 3565, 245, 605, 277, 4398, 738, 399, 486, 4319, 489, 655, 611, 2437, 311, 182, 878, 397, 2569, 384, 3318, 841, 2657, 359, 554, 2211, 1175, 614, 1357, 886, 698, 929, 472, 1928, 694, 3037, 905, 175, 513, 1236, 2713, 3819, 726, 543, 622, 655, 493, 1761, 548, 4034, 1009, 987, 218, 480, 226, 420, 1212, 864, 958, 1833, 3489, 1286, 667, 615, 683, 555, 752, 899, 2151, 540, 270, 1329, 1281, 1925, 2863, 576, 1189, 642, 2725, 384, 643, 626, 1225, 676, 299, 539, 607, 1556, 732, 229, 677, 2099, 806, 215, 1581, 1050, 1622, 1165, 1237, 597, 1178, 597, 3401, 503, 773, 897, 622, 505, 776, 4513, 844, 2311, 1203, 223, 682, 1127, 607, 4610, 1602, 4912, 556, 579, 1276, 769, 4462, 1055, 551, 1788, 1009, 605, 806, 231, 647, 1014, 1223, 347, 604, 1695, 716, 1868, 1688, 770, 1125, 1303, 1256, 383, 571, 4877, 549, 937, 625, 747, 434, 507, 2272, 587, 2958, 601, 813, 3831, 817, 1867, 478, 625, 1209, 651, 542, 2513, 698, 322, 660, 1775, 1221, 571, 983, 601, 905, 870, 842, 812, 2098, 831, 2844, 533, 1983, 653, 624, 467, 1318, 1717, 779, 438, 761, 327, 621, 846, 415, 1881, 811, 336, 1569, 1560, 1283, 489, 731, 963, 1613, 3096, 420, 833, 899, 1967, 378, 1603, 695, 769, 710, 234, 2594, 177, 534, 717, 276, 3329, 1309, 810, 738, 881, 939, 932, 1793, 335, 627, 523, 1392, 2503, 1401, 2044, 203, 831, 825, 1574, 1133, 141, 682, 1027, 868, 719, 1218, 1880, 640, 997, 884, 1299, 582, 657, 793, 304, 621, 730, 2965, 1871, 1958, 859, 1621, 516, 615, 258, 837, 972, 1373, 821, 589, 825, 533, 912, 203, 874, 577, 268, 1282, 1685, 523, 568, 1357, 709, 944, 1418, 557, 577, 337, 610, 640, 627, 1623, 596, 2486, 302, 559, 3498, 636, 335, 1138, 670, 2431, 1063, 764, 576, 1113, 632, 2844, 851, 823, 562, 314, 734, 766, 1063, 2755, 402, 314, 554, 582, 676, 927, 752, 3389, 578, 841, 642, 2316, 644, 519, 1276, 459, 991, 3003, 1074, 876, 2220, 1951, 759, 1199, 713, 3578, 629, 610, 221, 709, 899, 1667, 701, 1953, 989, 659, 519, 1602, 497, 503, 1197, 769, 993, 2615, 552, 1397, 1176, 542, 486, 1298, 2431, 612, 373, 542, 851, 444, 1468, 2570, 786, 883, 827, 1120, 544, 936, 603, 585, 3021, 1383, 583, 1221, 573, 1414, 2589, 1533, 738, 685, 970, 784, 598, 609, 947, 685, 923, 1679, 2979, 1336, 742, 712, 1782, 973, 667, 538, 739, 572, 2569, 571, 908, 939, 953, 487, 562, 670, 3786, 1452, 744, 760, 701, 601, 2554, 605, 1367, 465, 658, 2432, 345, 2336, 522, 971, 662, 798, 795, 1056, 567, 3663, 979, 362, 2306, 1635, 1215, 994, 794, 855, 787, 650, 256, 183, 518, 816, 1085, 2172, 628, 514, 790, 580, 583, 913, 1999, 1441, 2149, 386, 529, 662, 3412, 1816, 557, 988, 931, 664, 700, 678, 4745, 684, 3517, 800, 2693, 964, 741, 208, 1693, 3028, 491, 523, 1187, 1863, 860, 861, 847, 280, 604, 735, 428, 1065, 741, 3323, 982, 1396, 270, 482, 824, 784, 375, 884, 292, 581, 770, 2302, 606, 643, 1599, 211, 1055, 2021, 1201, 2233, 683, 804, 315, 666, 2113, 559, 675, 657, 726, 1265, 919, 387, 656, 508, 1141, 693, 594, 717, 399, 707, 927, 3128, 456, 514, 2862, 528, 771, 774, 1893, 809, 308, 509, 179, 1790, 1056, 2934, 547, 489, 591, 4125, 1466, 909, 743, 700, 218, 803, 599, 752, 1359, 687, 551, 3715, 2160, 1158, 2259, 666, 2370, 246, 1425, 764, 737, 858, 247, 4513, 1309, 596, 4382, 970, 3079, 817, 500, 395, 2432, 763, 2303, 1135, 713, 1472, 625, 1273, 731, 1664, 605, 299, 408, 1466, 856, 1147, 529, 1034, 4157, 957, 631, 665, 2394, 569, 748, 3433, 1169, 666, 1546, 606, 515, 694, 1311, 2483, 334, 2589, 673, 1428, 1642, 2378, 2107, 2143, 619, 841, 1385, 1060, 1774, 622, 2477, 3874, 280, 603, 303, 579, 3809, 909, 940, 1586, 1671, 1042, 2838, 3358, 199, 904, 1035, 1314, 702, 766, 729, 540, 688, 558, 570, 1109, 859, 750, 597, 1108, 1415, 811, 525, 662, 1624, 342, 800, 1203, 566, 3128, 725, 254, 399, 563, 1061, 1427, 1803, 1783, 573, 539, 4599, 375, 828, 1283, 721, 670, 569, 1261, 1447, 1871, 957, 275, 831, 631, 526, 820, 740, 1877, 813, 541, 223, 372, 810, 576, 584, 1312, 807, 3311, 900, 350, 1099, 1746, 870, 759, 560, 432, 315, 541, 1598, 443, 639, 473, 2625, 1723, 563, 461, 679, 2036, 278, 1409, 638, 809, 1225, 1270, 2546, 598, 1062, 569, 714, 881, 1346, 741, 883, 750, 472, 884, 1370, 3726, 1579, 598, 1194, 584, 3000, 788, 831, 193, 539, 386, 262, 784, 1095, 820, 671, 1110, 328, 769, 328, 1086, 2257, 555, 1120, 543, 724, 1061, 344, 2450, 570, 1255, 973, 917, 2327, 562, 1049, 738, 631, 461, 867, 1092, 3643, 1630, 607, 802, 756, 230, 1570, 1199, 882, 1837, 1887, 226, 549, 2318, 862, 1055, 821, 332, 1019, 1345, 1369, 830, 744, 1136, 566, 906, 587, 674, 773, 1478, 991, 945, 651, 2140, 1067, 1084, 828, 451, 899, 574, 2525, 900, 1120, 4022, 695, 798, 650, 862, 487, 180, 853, 2992, 1938, 647, 533, 695, 640, 2179, 1238, 1511, 243, 626, 1152, 436, 644, 821, 2378, 875, 3019, 2927, 682, 237, 200, 1080, 1740, 516, 1313, 1572, 708, 2201, 647, 845, 1128, 474, 1327, 1808, 547, 474, 1487, 1846, 669, 455, 833, 605, 404, 577, 1089, 956, 1755, 928, 691, 536, 848, 1197, 1005, 513, 956, 2187, 527, 1266, 664, 2096, 1757, 1187, 848, 956, 281, 357, 4384, 595, 2425, 1164, 617, 603, 1241, 584, 666, 305, 245, 1158, 630, 316, 1251, 602, 617, 907, 225, 861, 2239, 758, 1048, 766, 845, 992, 208, 302, 550, 798, 223, 966, 574, 1779, 514, 798, 2652, 388, 2106, 995, 536, 1079, 538, 723, 511, 1549, 555, 603, 855, 528, 533, 611, 660, 2718, 1812, 555, 617, 557, 1649, 613, 557, 525, 1466, 1174, 606, 771, 727, 906, 378, 1805, 2238, 1919, 682, 536, 748, 183, 662, 1172, 1025, 4620, 644, 1225, 2065, 250, 618, 634, 509, 98, 1206, 559, 1417, 813, 953, 2058, 1334, 1847, 1277, 496, 663, 849, 2626, 809, 702, 304, 2831, 666, 311, 375, 726, 1548, 917, 1488, 426, 861, 404, 1136, 649, 1839, 541, 603, 1491, 1556, 824, 1100, 687, 323, 1422, 2074, 651, 1828, 746, 1481, 774, 290, 1044, 1638, 601, 561, 1270, 538, 3088, 1062, 718, 856, 1300, 766, 895, 680, 2781, 1388, 1966, 256, 1215, 1485, 1753, 382, 744, 1220, 581, 4136, 766, 694, 2211, 517, 352, 3039, 1430, 4069, 244, 1153, 496, 729, 620, 663, 548, 1671, 603, 680, 605, 1039, 622, 655, 661, 2710, 921, 1668, 695, 456, 1174, 1382, 714, 906, 564, 749, 1136, 662, 605, 2414, 558, 341, 521, 1086, 610, 722, 534, 2373, 856, 787, 1074, 1002, 600, 922, 498, 641, 565, 799, 2409, 530, 1247, 261, 907, 663, 610, 3675, 431, 267, 850, 1512, 1507, 548, 2029, 667, 1092, 2166, 1797, 2476, 649, 853, 1637, 587, 455, 1394, 813, 609, 3098, 635, 1607, 1474, 589, 569, 638, 1122, 1563, 1086, 938, 795, 642, 552, 813, 559, 2365, 268, 1137, 660, 577, 1032, 1911, 1072, 1664, 495, 420, 2485, 862, 1709, 1173, 770, 786, 4580, 856, 567, 2599, 3125, 831, 222, 1939, 608, 207, 203, 873, 7312, 1339, 279, 1418, 290, 1013, 1257, 596, 3439, 1275, 1225, 527, 826, 531, 4081, 736, 880, 714, 625, 945, 587, 822, 954, 1589, 1389, 603, 228, 589, 630, 780, 361, 488, 759, 1548, 1073, 1301, 621, 1052, 677, 603, 1746, 4956, 2045, 852, 547, 240, 727, 538, 556, 530, 2549, 597, 954, 675, 599, 532, 1586, 1110, 3317, 747, 252, 3658, 1047, 1289, 519, 748, 637, 1129, 691, 509, 919, 2180, 1033, 1011, 3148, 585, 1483, 320, 586, 578, 1325, 1139, 605, 595, 1512, 1622, 459, 256, 1003, 696, 1566, 854, 1930, 596, 698, 574, 2940, 1031, 1884, 1326, 249, 794, 1894, 856, 1057, 1065, 233, 255, 246, 2429, 869, 549, 1281, 401, 666, 688, 2717, 2264, 3224, 3525, 911, 1505, 985, 795, 731, 1111, 4691, 2959, 536, 2064, 429, 2125, 2348, 1071, 608, 1180, 676, 605, 292, 1636, 398, 708, 457, 1008, 223, 736, 920, 754, 1876, 548, 1462, 400, 739, 1013, 424, 536, 594, 393, 450, 1073, 756, 273, 150, 820, 1135, 950, 1992, 823, 644, 522, 532, 561, 602, 1824, 1412, 566, 1871, 647, 667, 691, 575, 898, 1016, 704, 564, 546, 669, 1434, 740, 2625, 614, 356, 446, 536, 675, 528, 452, 272, 1177, 798, 817, 3273, 1929, 2067, 607, 325, 630, 1361, 538, 606, 573, 1240, 593, 876, 603, 3880, 603, 531, 1540, 716, 660, 234, 529, 686, 566, 649, 4222, 2289, 246, 1600, 702, 409, 990, 797, 243, 1147, 681, 1189, 505, 525, 2285, 199, 724, 237, 2571, 587, 720, 551, 921, 1354, 3968, 615, 967, 766, 690, 975, 523, 697, 2263, 1425, 2575, 716, 347, 669, 864, 1172, 630, 2215, 845, 602, 943, 4185, 629, 738, 787, 918, 267, 800, 734, 929, 3102, 1133, 2747, 523, 537, 1129, 1270, 1154, 1041, 973, 466, 1190, 551, 1733, 500, 659, 1496, 1824, 1140, 1222, 1949, 636, 176, 1241, 867, 726, 1639, 698, 658, 783, 364, 548, 1657, 682, 555, 1056, 3045, 635, 1388, 577, 1250, 1466, 1052, 281, 539, 1002, 617, 1643, 953, 2064, 2858, 1308, 504, 948, 514, 3157, 762, 2498, 708, 544, 1118, 1111, 399, 2503, 249, 852, 857, 2393, 1075, 5017, 417, 1112, 227, 577, 980, 277, 258, 525, 1734, 646, 474, 612, 567, 677, 2338, 546, 812, 807, 937, 2674, 417, 1710, 732, 627, 1126, 858, 3764, 561, 1320, 3020, 298, 1870, 477, 1407, 629, 532, 1075, 682, 2007, 863, 304, 1757, 1126, 1277, 385, 860, 1143, 562, 1696, 515, 485, 902, 708, 1029, 632, 483, 890, 414, 1287, 724, 1380, 1196, 479, 938, 1499, 628, 602, 1150, 602, 792, 294, 4847, 1392, 2237, 514, 4203, 760, 198, 368, 1759, 1246, 1264, 342, 381, 2322, 1928, 1725, 860, 925, 1305, 881, 276, 1493, 807, 2607, 3577, 720, 872, 1222, 728, 594, 564, 1397, 1203, 346, 2949, 648, 932, 1982, 667, 614, 2362, 1664, 547, 729, 343, 1238, 1124, 821, 642, 727, 656, 1025, 988, 1598, 1695, 2337, 663, 657, 527, 237, 758, 1053, 564, 267, 1038, 640, 1348, 2472, 1334, 860, 565, 521, 294, 839, 1009, 676, 1228, 532, 605, 3667, 1142, 546, 649, 1259, 1797, 700, 1419, 1151, 1140, 1059, 1076, 882, 589, 548, 621, 1373, 582, 1585, 346, 639, 544, 403, 1337, 1141, 599, 625, 908, 1040, 281, 529, 929, 221, 760, 643, 2299, 856, 329, 1406, 576, 542, 606, 1280, 753, 945, 1032, 1169, 337, 869, 3607, 1035, 661, 708, 831, 381, 419, 354, 1982, 574, 2320, 469, 521, 941, 194, 975, 352, 1786, 836, 3533, 1171, 960, 538, 809, 898, 2068, 609, 701, 857, 519, 653, 663, 1731, 143, 1746, 816, 2025, 449, 685, 630, 727, 418, 667, 902, 969, 714, 330, 843, 899, 779, 1761, 618, 666, 227, 751, 949, 544, 406, 1918, 1163, 461, 537, 774, 691, 672, 1991, 539, 616, 3986, 944, 1674, 305, 1227, 1784, 521, 887, 585, 3082, 609, 314, 1300, 786, 570, 1192, 201, 295, 720, 1400, 648, 1334, 1513, 670, 3083, 1983, 1565, 1611, 463, 667, 943, 815, 2573, 979, 966, 266, 628, 2003, 698, 4357, 766, 1715, 878, 589, 1161, 802, 953, 522, 347, 856, 2088, 994, 766, 368, 503, 579, 891, 704, 730, 1285, 4204, 1499, 514, 1731, 505, 1739, 187, 586, 2009, 631, 3868, 689, 3084, 669, 294, 1606, 693, 683, 1020, 2020, 1289, 700, 740, 639, 156, 536, 530, 2147, 912, 278, 217, 896, 1076, 2767, 642, 546, 733, 678, 606, 3326, 918, 589, 1398, 709, 535, 996, 582, 535, 4460, 643, 940, 244, 645, 1015, 519, 4107, 1419, 703, 1690, 1545, 816, 574, 2877, 1502, 1887, 797, 2034, 174, 794, 170, 745, 932, 2317, 2290, 568, 385, 595, 530, 536, 1079, 679, 1406, 971, 1764, 2792, 567, 1936, 547, 395, 589, 815, 1268, 1625, 623, 423, 301, 976, 520, 768, 775, 888, 3325, 480, 729, 1670, 417, 1020, 1151, 1531, 1901, 1097, 496, 1436, 1067, 658, 1317, 425, 339, 585, 1108, 2777, 1398, 672, 1669, 2290, 1281, 950, 916, 602, 919, 379, 1027, 555, 990, 551, 929, 138, 767, 780, 700, 1042, 178, 569, 2647, 892, 581, 3384, 2633, 715, 462, 941, 4302, 1228, 794, 1500, 1311, 2522, 1440, 3703, 1943, 958, 2208, 1865, 542, 665, 431, 1194, 471, 712, 603, 734, 646, 1829, 530, 212, 417, 799, 182, 564, 1821, 1997, 2730, 612, 931, 481, 563, 554, 592, 1460, 1148, 486, 549, 1700, 857, 901, 552, 538, 1412, 641, 447, 965, 625, 954, 1611, 364, 977, 901, 1133, 2054, 573, 777, 523, 604, 1468, 254, 2129, 661, 1546, 716, 4056, 562, 209, 1997, 199, 1285, 1379, 744, 586, 543, 384, 262, 361, 1322, 731, 686, 658, 541, 2403, 524, 704, 815, 209, 544, 758, 487, 529, 629, 538, 529, 1514, 1742, 589, 396, 927, 530, 1050, 2615, 536, 548, 594, 296, 384, 506, 273, 3280, 1849, 543, 1601, 952, 1049, 464, 942, 697, 647, 625, 1027, 268, 160, 1724, 1538, 505, 3989, 632, 977, 639, 767, 350, 1127, 400, 1103, 1417, 916, 616, 709, 1607, 547, 578, 529, 621, 846, 566, 1803, 614, 681, 567, 529, 1258, 1337, 928, 886, 540, 745, 537, 538, 3583, 1299, 248, 2072, 1482, 365, 701, 1974, 281, 814, 697, 801, 629, 635, 2116, 1485, 559, 595, 1357, 639, 902, 1350, 491, 1972, 948, 2450, 2944, 987, 506, 690, 3216, 1518, 1467, 1213, 484, 1387, 1343, 1241, 279, 395, 1233, 563, 925, 1167, 2091, 3775, 676, 717, 1591, 613, 999, 687, 1162, 522, 698, 4700, 697, 751, 1226, 833, 737, 1709, 3469, 429, 1680, 2967, 1616, 809, 590, 890, 1304, 646, 355, 630, 2429, 539, 532, 1336, 504, 275, 1558, 1425, 782, 789, 1656, 663, 948, 1522, 597, 2001, 1829, 895, 1823, 2151, 529, 2474, 867, 706, 1127, 774, 1647, 1052, 683, 1430, 672, 608, 2755, 1203, 1072, 1045, 657, 834, 911, 1322, 716, 470, 510, 1717, 1200, 553, 631, 567, 739, 3893, 1935, 524, 1620, 1476, 1789, 528, 678, 1029, 1633, 586, 1629, 1714, 413, 2073, 1173, 727, 885, 797, 806, 2001, 348, 662, 859, 1383, 837, 1160, 626, 1593, 229, 1304, 1248, 1254, 782, 539, 1278, 1275, 685, 270, 976, 2066, 1468, 535, 3978, 660, 1076, 1027, 1139, 1618, 923, 557, 1624, 446, 1477, 771, 617, 699, 788, 976, 429, 590, 378, 696, 688, 445, 387, 563, 537, 780, 571, 513, 1243, 3217, 532, 780, 544, 787, 459, 334, 1822, 1506, 427, 569, 1429, 859, 729, 537, 1365, 1063, 1990, 916, 1483, 570, 519, 683, 796, 1963, 1541, 1062, 1640, 905, 631, 2077, 1034, 1080, 813, 849, 572, 469, 331, 510, 1593, 1544, 536, 2785, 282, 1276, 1069, 528, 585, 922, 2481, 478, 1073, 266, 2366, 1833, 1305, 443, 1398, 621, 217, 602, 990, 633, 585, 566, 2741, 210, 852, 794, 957, 817, 4457, 2036, 583, 679, 375, 748, 788, 703, 1297, 1121, 763, 2955, 224, 2294, 736, 611, 1077, 2583, 661, 129, 252, 1000, 1276, 746, 578, 562, 1118, 351, 2436, 1252, 643, 962, 4811, 1165, 941, 282, 1107, 165, 614, 298, 863, 4080, 1486, 536, 687, 638, 642, 2056, 780, 587, 4166, 3174, 605, 632, 595, 998, 1123, 1123, 1814, 2047, 1300, 1767, 710, 2718, 687, 907, 705, 565, 877, 729, 519, 1374, 1364, 1885, 1541, 593, 531, 459, 1000, 810, 624, 702, 2501, 462, 1540, 524, 1203, 2126, 1712, 550, 1130, 483, 731, 1093, 458, 2057, 655, 1113, 708, 1009, 1517, 797, 833, 1593, 386, 547, 726, 565, 648, 353, 4057, 1345, 645, 2155, 2240, 892, 686, 548, 1704, 718, 326, 935, 564, 626, 543, 1667, 1150, 708, 4031, 886, 1213, 970, 704, 1102, 678, 1324, 557, 649, 613, 918, 772, 2341, 1682, 1552, 473, 1059, 605, 436, 916, 794, 793, 1152, 1382, 1771, 773, 556, 829, 661, 3998, 2067, 561, 1411, 510, 755, 232, 1127, 980, 483, 754, 544, 597, 384, 3856, 1173, 273, 1148, 727, 616, 746, 295, 3819, 1240, 1919, 603, 634, 578, 518, 219, 2765, 642, 212, 699, 467, 777, 1009, 821, 575, 801, 878, 2356, 841, 585, 1928, 567, 1290, 932, 2146, 1431, 557, 710, 584, 2648, 1330, 394, 451, 377, 505, 344, 789, 590, 601, 745, 906, 614, 821, 600, 830, 332, 962, 583, 184, 887, 687, 4813, 587, 603, 1533, 1352, 3490, 546, 1140, 775, 1341, 1091, 216, 661, 648, 911, 797, 223, 883, 296, 939, 1626, 546, 1803, 659, 572, 1583, 518, 1488, 899, 2325, 2671, 1006, 642, 343, 542, 887, 835, 367, 991, 504, 527, 212, 1439, 816, 534, 1417, 722, 337, 822, 1311, 2573, 207, 1405, 312, 1750, 637, 650, 595, 688, 1169, 654, 837, 1509, 605, 2051, 1328, 834, 618, 1043, 683, 741, 452, 710, 445, 566, 517, 617, 724, 2467, 482, 535, 509, 880, 281, 329, 763, 544, 684, 839, 1300, 671, 639, 737, 553, 1774, 1039, 675, 488, 2334, 273, 536, 691, 362, 314, 1361, 525, 773, 1654, 799, 627, 943, 586, 1324, 296, 760, 616, 2380, 204, 1046, 732, 1806, 1762, 948, 391, 570, 683, 2389, 4552, 3673, 985, 317, 780, 827, 1580, 983, 1398, 1490, 1170, 745, 828, 633, 922, 781, 1144, 1126, 1009, 575, 1035, 1073, 582, 434, 348, 1531, 686, 804, 505, 1610, 836, 546, 1187, 629, 2319, 970, 1183, 1505, 983, 708, 913, 989, 432, 1078, 371, 2382, 2138, 693, 1113, 1188, 3827, 653, 576, 1015, 843, 1529, 703, 544, 518, 882, 1046, 1325, 657, 985, 663, 836, 916, 1066, 1350, 238, 401, 604, 1511, 3482, 1110, 748, 826, 1423, 1629, 3707, 658, 465, 686, 627, 637, 1631, 675, 591, 1178, 2022, 731, 528, 1114, 1718, 548, 629, 225, 2305, 779, 693, 420, 876, 755, 1262, 3384, 2630, 1183, 206, 627, 783, 849, 875, 852, 1507, 567, 1919, 743, 209, 3477, 664, 356, 1609, 783, 224, 391, 1272, 3178, 2612, 668, 747, 1843, 187, 951, 436, 1400, 1417, 468, 620, 1006, 871, 1539, 2369, 387, 567, 746, 313, 792, 2127, 757, 2011, 746, 1105, 901, 1855, 860, 569, 1412, 1821, 1703, 1242, 544, 922, 1740, 1345, 1435, 1316, 572, 886, 658, 539, 1720, 609, 2414, 1054, 560, 1533, 412, 707, 560, 977, 5228, 2359, 751, 558, 1205, 812, 2401, 507, 663, 1334, 520, 536, 414, 674, 695, 1229, 833, 717, 345, 688, 688, 523, 1895, 1105, 817, 1261, 1098, 1275, 756, 1178, 564, 584, 896, 1635, 1006, 563, 695, 800, 101, 792, 1812, 1477, 276, 712, 3432, 2435, 623, 756, 1721, 3211, 3447, 663, 693, 3974, 1447, 656, 858, 816, 509, 2316, 1470, 488, 1930, 367, 2326, 599, 2644, 1451, 927, 560, 1547, 333, 1326, 1060, 443, 4790, 540, 1622, 3894, 563, 718, 1599, 1225, 1425, 1239, 536, 734, 926, 533, 1447, 978, 620, 1251, 762, 585, 1118, 2032, 726, 1048, 659, 692, 645, 705, 4062, 608, 779, 1414, 464, 631, 764, 656, 1236, 1325, 1113, 1175, 1324, 924, 593, 1400, 701, 3288, 707, 473, 4639, 3616, 1301, 602, 832, 1143, 2769, 619, 572, 432, 625, 669, 816, 204, 610, 654, 1189, 2213, 1096, 729, 572, 654, 955, 2026, 201, 1086, 1260, 756, 1104, 1688, 456, 3190, 505, 1028, 657, 602, 1246, 3666, 640, 575, 1633, 590, 589, 890, 785, 658, 2611, 560, 616, 882, 790, 928, 379, 822, 1351, 868, 278, 267, 683, 1956, 632, 3110, 2224, 792, 949, 1958, 1052, 689, 512, 573, 681, 218, 1224, 2045, 1326, 2616, 998, 1687, 619, 1027, 3639, 975, 862, 710, 1047, 207, 2099, 540, 642, 737, 939, 1131, 1793, 1073, 259, 569, 5223, 329, 613, 455, 1017, 694, 414, 1158, 605, 516, 1139, 2280, 595, 616, 652, 1870, 2902, 317, 1668, 1072, 833, 607, 646, 715, 735, 325, 2538, 512, 1509, 913, 1069, 862, 650, 255, 628, 585, 754, 4461, 1452, 575, 868, 1556, 1681, 217, 1405, 949, 1669, 1033, 2050, 395, 3540, 588, 1214, 1603, 1791, 547, 1706, 714, 413, 1107, 2202, 1072, 717, 585, 571, 3910, 1156, 998, 1282, 315, 667, 1476, 498, 1099, 315, 2237, 490, 1234, 778, 574, 4786, 1118, 1060, 226, 1098, 343, 936, 901, 590, 560, 815, 745, 1027, 749, 583, 503, 1073, 686, 699, 1644, 861, 1474, 2352, 617, 512, 1029, 571, 809, 1583, 1748, 899, 702, 1403, 1345, 628, 2517, 1009, 2848, 1019, 710, 276, 1247, 423, 1253, 864, 548, 1720, 1822, 714, 565, 802, 565, 531, 846, 982, 1209, 1695, 879, 2306, 1963, 779, 604, 1652, 2450, 307, 1914, 1497, 670, 1269, 1100, 540, 1317, 1499, 1012, 2285, 618, 1115, 470, 637, 1285, 662, 1082, 520, 2275, 766, 1100, 693, 387, 926, 716, 971, 1429, 532, 2138, 876, 672, 668, 1634, 2304, 707, 1079, 613, 648, 1014, 814, 786, 2291, 612, 559, 644, 749, 867, 327, 848, 372, 649, 686, 786, 324, 428, 1175, 971, 643, 1121, 864, 551, 1239, 597, 1698, 520, 525, 1049, 928, 656, 1028, 384, 751, 2646, 4676, 332, 718, 751, 959, 1139, 2459, 1482, 940, 1340, 1226, 1511, 1391, 839, 3904, 1194, 332, 1601, 526, 948, 554, 2169, 563, 4633, 2755, 1125, 2023, 256, 824, 871, 148, 946, 530, 671, 705, 474, 586, 178, 1929, 3233, 728, 3566, 217, 2880, 508, 490, 469, 1115, 420, 162, 579, 384, 390, 768, 626, 870, 664, 795, 1113, 1224, 2365, 590, 1060, 1041, 2231, 583, 528, 698, 1422, 1958, 585, 2038, 1353, 2626, 644, 1100, 1245, 2106, 503, 1172, 1287, 889, 978, 618, 358, 1499, 1241, 559, 148, 516, 919, 697, 1476, 657, 1307, 612, 753, 633, 1483, 192, 204, 530, 774, 584, 721, 1437, 1417, 3600, 566, 796, 781, 1327, 908, 1239, 222, 1358, 3470, 589, 592, 1226, 1143, 1016, 753, 2034, 1757, 644, 433, 1123, 552, 589, 766, 1405, 597, 2010, 959, 328, 582, 1031, 1944, 972, 1347, 529, 743, 744, 1593, 1170, 1068, 730, 1616, 784, 197, 910, 1869, 662, 632, 213, 809, 1015, 2142, 1282, 2602, 1305, 904, 4246, 571, 1226, 1525, 674, 502, 559, 1469, 2502, 268, 585, 1265, 402, 597, 2016, 972, 865, 652, 548, 514, 636, 679, 256, 3157, 512, 496, 480, 671, 398, 682, 550, 591, 1993, 1247, 1520, 1253, 1021, 1202, 733, 869, 684, 962, 840, 755, 670, 1135, 1115, 581, 2620, 1627, 1816, 348, 2109, 1321, 1584, 609, 1558, 808, 946, 667, 504, 676, 675, 707, 4725, 431, 1718, 1198, 1217, 537, 677, 924, 648, 2272, 571, 968, 613, 200, 455, 2373, 808, 3155, 224, 731, 2097, 955, 599, 705, 621, 3705, 813, 557, 1946, 1072, 253, 590, 1653, 2115, 1801, 1161, 401, 1436, 969, 1712, 1133, 383, 300, 2144, 1058, 812, 517, 2871, 1238, 624, 1438, 534, 168, 115, 257, 705, 2731, 1996, 866, 2622, 515, 1219, 909, 588, 257, 1466, 1912, 2345, 223, 694, 1860, 585, 213, 322, 2922, 638, 903, 541, 813, 1685, 885, 1266, 913, 1664, 984, 573, 789, 2089, 510, 1625, 1260, 538, 543, 172, 539, 984, 657, 741, 611, 860, 282, 1410, 792, 686, 960, 2929, 453, 1609, 631, 574, 360, 833, 1502, 3239, 830, 1998, 565, 1595, 660, 880, 796, 575, 883, 1120, 1055, 1110, 532, 1311, 541, 544, 638, 509, 586, 601, 1407, 848, 299, 604, 1659, 1571, 906, 3510, 951, 646, 585, 979, 866, 3262, 765, 1273, 567, 3915, 1216, 627, 483, 538, 876, 738, 1328, 913, 450, 231, 1576, 505, 2343, 3381, 306, 2456, 1181, 2689, 686, 602, 1430, 455, 919, 935, 537, 544, 472, 1142, 5030, 465, 698, 1759, 1274, 947, 565, 2485, 528, 877, 1333, 1120, 601, 652, 2004, 6392, 983, 3871, 698, 1136, 1747, 256, 542, 417, 1071, 3353, 1766, 992, 394, 557, 1737, 356, 568, 662, 1196, 1871, 1228, 707, 553, 2498, 1470, 4019, 1167, 1683, 317, 1509, 1309, 1315, 714, 321, 743, 615, 1292, 329, 492, 495, 808, 1498, 1431, 576, 750, 930, 1209, 1026, 709, 1024, 1950, 2372, 893, 901, 645, 1174, 203, 1747, 981, 822, 1509, 974, 681, 316, 718, 468, 571, 707, 1108, 588, 543, 897, 477, 1927, 2180, 1531, 1199, 640, 746, 1627, 1448, 408, 843, 422, 2340, 638, 1092, 813, 1395, 1592, 748, 700, 366, 2922, 1561, 778, 545, 649, 789, 1250, 628, 732, 878, 404, 1514, 873, 1340, 711, 659, 589, 595, 536, 810, 1384, 277, 1253, 588, 2788, 1865, 533, 979, 1352, 519, 3366, 1933, 598, 494, 137, 1224, 2240, 1200, 2304, 897, 203, 1097, 1075, 4750, 202, 477, 591, 397, 5670, 500, 1162, 551, 2561, 725, 1478, 520, 1234, 694, 520, 857, 633, 911, 1063, 1614, 3891, 613, 749, 1189, 818, 937, 1687, 1093, 1770, 496, 687, 720, 2244, 2911, 748, 551, 1558, 511, 1501, 390, 526, 458, 1445, 529, 4992, 1410, 635, 199, 800, 846, 825, 879, 599, 1342, 643, 3226, 606, 453, 1464, 2940, 629, 529, 1304, 348, 477, 649, 615, 2058, 1158, 1210, 4536, 828, 2489, 918, 656, 1509, 1700, 722, 3887, 2024, 612, 628, 756, 754, 685, 920, 812, 1005, 515, 877, 858, 580, 457, 906, 1629, 3963, 800, 1862, 733, 1346, 576, 3109, 1996, 744, 606, 877, 766, 224, 758, 748, 1842, 1253, 596, 864, 448, 1247, 231, 768, 675, 562, 3416, 1179, 745, 542, 660, 1034, 1651, 251, 857, 612, 3671, 1608, 1314, 324, 607, 1443, 540, 693, 691, 1716, 1168, 281, 598, 1396, 603, 1371, 766, 732, 2764, 1122, 930, 1154, 590, 677, 1508, 180, 986, 831, 1303, 1598, 510, 248, 594, 816, 681, 3144, 523, 542, 184, 634, 369, 557, 918, 638, 1379, 2093, 688, 791, 296, 663, 4290, 1502, 312, 635, 734, 3403, 2103, 2000, 556, 526, 332, 962, 709, 626, 2292, 461, 896, 980, 699, 664, 2669, 1022, 615, 411, 980, 709, 836, 4117, 1410, 486, 784, 801, 1033, 1733, 1826, 3035, 304, 1491, 3540, 559, 678, 701, 487, 1027, 1014, 842, 1149, 996, 602, 553, 420, 882, 516, 1027, 1474, 430, 538, 532, 2561, 967, 943, 280, 570, 3524, 996, 4858, 635, 2002, 320, 1011, 648, 1214, 1267, 1732, 1623, 1154, 856, 1027, 534, 1470, 2120, 154, 606, 354, 324, 565, 592, 1437, 693, 707, 3286, 247, 1516, 2396, 557, 583, 555, 1562, 1348, 663, 561, 1652, 1132, 762, 949, 886, 538, 689, 1232, 807, 1210, 519, 901, 765, 553, 1225, 3653, 735, 2114, 514, 1421, 1139, 462, 763, 206, 1025, 898, 1928, 991, 1404, 1693, 732, 1106, 597, 559, 979, 1442, 800, 211, 965, 562, 393, 1554, 802, 824, 562, 1964, 605, 2172, 537, 599, 1324, 604, 1049, 715, 1795, 897, 626, 536, 1341, 709, 862, 643, 265, 1523, 888, 673, 2209, 1669, 533, 1603, 716, 789, 1517, 460, 596, 364, 380, 560, 856, 541, 295, 838, 642, 927, 682, 1436, 1006, 398, 2459, 573, 3676, 396, 570, 666, 576, 787, 802, 397, 3858, 627, 501, 499, 195, 507, 698, 535, 795, 246, 192, 1304, 861, 590, 3074, 1249, 1456, 853, 482, 260, 1937, 570, 536, 2200, 343, 582, 1745, 2148, 714, 1079, 791, 947, 1005, 422, 670, 2127, 589, 534, 2388, 3564, 748, 1580, 175, 906, 1604, 2173, 2997, 510, 513, 2555, 696, 657, 617, 1047, 586, 558, 554, 1559, 1410, 1297, 1099, 583, 2399, 527, 972, 691, 2817, 879, 922, 533, 3148, 487, 1067, 807, 924, 457, 873, 1597, 857, 377, 1969, 555, 225, 601, 1234, 1135, 2490, 549, 1536, 1629, 2176, 871, 1344, 687, 958, 394, 531, 1210, 921, 652, 930, 1694, 601, 695, 1162, 1021, 1667, 1367, 558, 506, 466, 180, 402, 470, 2547, 985, 2245, 232, 807, 1034, 804, 3616, 544, 703, 1450, 645, 4150, 722, 1493, 289, 4248, 750, 3379, 2757, 590, 3244, 835, 554, 1026, 1122, 2087, 176, 884, 972, 1131, 1223, 1591, 4053, 586, 978, 972, 1448, 775, 541, 1053, 287, 952, 746, 2104, 680, 793, 724, 1348, 2228, 677, 993, 4988, 906, 1324, 1703, 567, 655, 767, 951, 541, 709, 1010, 1576, 972, 834, 815, 841, 1794, 393, 1647, 1631, 415, 185, 553, 1721, 902, 2778, 511, 543, 830, 939, 1139, 2077, 964, 1799, 2071, 2556, 2269, 514, 266, 1359, 1116, 587, 1467, 884, 854, 1794, 5955, 607, 2205, 658, 712, 322, 246, 1547, 217, 2131, 2609, 581, 706, 254, 178, 586, 719, 2703, 4847, 576, 667, 1576, 516, 1239, 1109, 541, 1272, 2028, 1740, 547, 542, 1172, 505, 1471, 1059, 649, 1424, 365, 969, 508, 218, 2870, 469, 336, 191, 232, 531, 552, 1771, 1994, 587, 457, 1371, 815, 1225, 306, 209, 728, 417, 566, 629, 578, 555, 821, 781, 2314, 823, 845, 776, 464, 310, 1458, 485, 550, 477, 223, 571, 720, 669, 563, 753, 741, 844, 1223, 583, 482, 666, 208, 986, 1835, 213, 3949, 866, 677, 563, 1429, 892, 776, 352, 574, 156, 618, 596, 898, 509, 635, 853, 222, 377, 1379, 722, 736, 1488, 295, 700, 970, 492, 883, 2818, 626, 442, 564, 1985, 1079, 609, 1735, 1715, 1905, 1723, 2949, 713, 1157, 811, 635, 638, 1532, 734, 2729, 1227, 1130, 1847, 668, 821, 1198, 500, 628, 528, 1534, 1553, 685, 569, 937, 1362, 1031, 497, 417, 1243, 617, 2078, 619, 4849, 560, 1126, 1130, 2543, 823, 492, 4216, 434, 1005, 638, 361, 4439, 981, 640, 1163, 3846, 183, 735, 1340, 890, 689, 982, 714, 1357, 917, 147, 542, 1830, 744, 724, 778, 912, 576, 659, 2017, 1230, 616, 569, 3383, 1023, 828, 330, 506, 1097, 763, 525, 648, 824, 397, 600, 911, 687, 516, 819, 547, 745, 587, 867, 789, 658, 665, 113, 825, 730, 274, 551, 646, 828, 1043, 682, 1085, 394, 543, 817, 548, 329, 2355, 2058, 859, 3960, 953, 1772, 802, 784, 1241, 967, 1510, 1882, 194, 954, 659, 771, 1137, 1288, 1243, 1315, 1843, 960, 619, 141, 1127, 409, 546, 675, 680, 566, 836, 569, 2437, 824, 307, 1034, 1122, 2375, 848, 748, 673, 542, 2355, 2156, 1858, 957, 693, 532, 1919, 2724, 1973, 597, 621, 1260, 1025, 800, 864, 691, 634, 1069, 1035, 498, 762, 1055, 984, 784, 676, 1978, 614, 2244, 770, 838, 310, 1602, 706, 1665, 537, 935, 567, 826, 1079, 664, 696, 2568, 1126, 725, 1011, 1083, 860, 591, 1349, 355, 1115, 726, 1111, 755, 1782, 1103, 3627, 1555, 996, 614, 303, 473, 563, 243, 1568, 471, 656, 646, 2675, 1535, 909, 1093, 1292, 583, 887, 1094, 1056, 587, 1558, 570, 1135, 463, 480, 1620, 1844, 2192, 341, 236, 489, 1229, 725, 4541, 1864, 719, 658, 847, 560, 1782, 677, 1684, 662, 598, 1337, 1296, 991, 165, 284, 4530, 1439, 1997, 2485, 1280, 1949, 1472, 1304, 2642, 1588, 575, 731, 1640, 723, 502, 1465, 687, 2153, 918, 1237, 740, 2124, 3771, 2321, 973, 1885, 3275, 1147, 593, 799, 593, 2405, 2188, 342, 656, 1087, 471, 490, 879, 596, 1723, 545, 658, 2374, 1960, 603, 625, 640, 279, 1035, 2216, 500, 2400, 789, 838, 2998, 902, 3777, 885, 681, 824, 1130, 3060, 1208, 1484, 1713, 493, 1564, 592, 423, 885, 1317, 543, 634, 1863, 846, 1313, 1590, 1493, 770, 1606, 2460, 507, 1244, 668, 427, 1150, 1048, 697, 876, 799, 714, 2117, 2450, 827, 723, 1532, 2824, 2925, 1881, 622, 564, 216, 763, 597, 459, 624, 546, 600, 315, 597, 235, 2486, 2551, 684, 1520, 1878, 1081, 2850, 1552, 561, 4009, 389, 935, 3085, 698, 597, 1112, 998, 1364, 968, 141, 350, 1177, 962, 908, 234, 802, 554, 686, 873, 566, 305, 430, 1387, 1239, 555, 1515, 759, 222, 1291, 1111, 518, 1572, 1267, 530, 547, 1058, 1178, 950, 2448, 1366, 968, 1004, 1909, 1921, 704, 770, 668, 247, 1034, 770, 585, 649, 575, 587, 1930, 643, 750, 1608, 320, 673, 693, 2398, 69, 300, 347, 1177, 924, 516, 824, 780, 809, 359, 1523, 526, 484, 2131, 421, 996, 786, 611, 2803, 863, 1049, 869, 2112, 836, 787, 778, 702, 652, 588, 750, 943, 810, 964, 467, 3668, 577, 829, 470, 1091, 382, 258, 921, 538, 1049, 747, 851, 2426, 480, 197, 707, 892, 739, 2335, 582, 539, 510, 657, 494, 2290, 2654, 645, 589, 3010, 1366, 860, 605, 519, 533, 834, 540, 555, 822, 564, 2545, 615, 1501, 3529, 798, 3135, 586, 1846, 780, 1364, 238, 2939, 1369, 3485, 689, 521, 834, 1951, 1295, 1192, 3437, 1141, 921, 285, 549, 1901, 2560, 1056, 627, 1374, 737, 213, 2604, 693, 221, 665, 902, 1186, 586, 2836, 1177, 1708, 1166, 271, 1728, 1270, 1284, 1987, 345, 860, 538, 1212, 622, 142, 552, 551, 503, 217, 821, 1012, 2991, 3349, 718, 741, 465, 546, 1064, 566, 758, 1309, 592, 362, 452, 2324, 246, 2422, 761, 1625, 607, 1319, 1789, 775, 706, 473, 628, 995, 705, 3247, 730, 1017, 869, 2084, 1099, 307, 566, 314, 616, 220, 2459, 3101, 815, 677, 848, 600, 666, 250, 1045, 4019, 1411, 2005, 552, 1165, 1349, 2089, 626, 699, 667, 1510, 705, 523, 1115, 869, 310, 1076, 1078, 1012, 2269, 2568, 1797, 891, 817, 1282, 550, 1129, 719, 391, 1778, 644, 804, 850, 1212, 555, 739, 900, 1165, 1343, 1898, 537, 594, 632, 1829, 2313, 684, 664, 2692, 1440, 1020, 2513, 1369, 630, 890, 365, 1170, 899, 651, 1877, 579, 433, 1170, 2173, 978, 540, 2730, 599, 265, 653, 838, 754, 772, 1120, 804, 477, 563, 1882, 611, 688, 826, 1040, 757, 519, 876, 1327, 674, 551, 1596, 1120, 4319, 2724, 2989, 594, 1982, 1731, 1092, 682, 702, 842, 480, 1152, 600, 620, 846, 889, 562, 1083, 1092, 603, 2173, 4748, 1497, 247, 1693, 1851, 546, 191, 1922, 956, 784, 364, 732, 1126, 2120, 780, 550, 1938, 582, 302, 529, 455, 339, 758, 832, 1982, 419, 538, 444, 1797, 1030, 652, 453, 724, 309, 800, 643, 654, 1416, 524, 2276, 2115, 327, 492, 1282, 1960, 666, 682, 652, 965, 149, 899, 552, 803, 903, 755, 425, 1047, 551, 1122, 1920, 743, 2734, 746, 590, 861, 747, 884, 534, 1144, 597, 485, 693, 642, 2908, 627, 755, 1813, 778, 982, 621, 673, 857, 1421, 719, 1815, 480, 320, 630, 450, 2781, 2159, 527, 1532, 1000, 1161, 615, 615, 1636, 340, 1055, 2551, 956, 394, 2575, 594, 593, 917, 531, 763, 686, 1019, 1118, 1248, 342, 275, 4881, 1661, 821, 1034, 327, 801, 1022, 718, 862, 623, 1587, 425, 2344, 799, 589, 801, 402, 1682, 532, 913, 846, 1384, 316, 563, 1581, 948, 1544, 1076, 1913, 1234, 1452, 287, 283, 532, 679, 919, 667, 723, 790, 378, 520, 852, 735, 1370, 2052, 566, 1870, 1956, 1586, 401, 1203, 149, 1665, 391, 632, 1231, 1817, 745, 1703, 603, 1579, 691, 1222, 272, 1323, 578, 1436, 1494, 2787, 1182, 322, 609, 5136, 588, 817, 561, 1506, 370, 660, 2372, 553, 220, 1321, 2644, 654, 686, 1139, 629, 773, 465, 647, 818, 537, 1101, 599, 1121, 295, 652, 2289, 1154, 578, 816, 841, 767, 581, 790, 552, 559, 592, 1224, 2403, 529, 1410, 947, 596, 2542, 1378, 520, 545, 1054, 774, 797, 998, 1170, 583, 762, 585, 769, 836, 2212, 1001, 548, 646, 544, 772, 1103, 715, 1014, 1451, 920, 1422, 1683, 728, 476, 992, 861, 2565, 1690, 2646, 402, 2380, 1431, 520, 1728, 3425, 758, 3463, 505, 536, 461, 500, 589, 549, 716, 655, 1350, 1148, 1298, 892, 556, 1056, 2559, 591, 1106, 1039, 872, 1141, 787, 698, 605, 1525, 265, 3349, 2313, 480, 750, 815, 698, 192, 252, 558, 485, 482, 924, 214, 301, 2362, 515, 621, 866, 1346, 1222, 504, 1057, 805, 1010, 1412, 811, 1396, 640, 344, 596, 1205, 975, 840, 1696, 3487, 649, 1375, 430, 570, 625, 499, 1943, 596, 608, 809, 535, 1475, 516, 495, 785, 421, 2384, 541, 546, 2126, 534, 616, 1170, 1071, 619, 559, 591, 800, 2757, 240, 641, 697, 4745, 995, 848, 640, 578, 1258, 1017, 871, 857, 2083, 1395, 853, 200, 965, 617, 705, 1787, 947, 883, 1141, 253, 1806, 559, 514, 1107, 1870, 3444, 720, 563, 765, 615, 1403, 560, 298, 530, 2164, 507, 306, 452, 924, 635, 766, 367, 1389, 995, 673, 1155, 1236, 1112, 843, 907, 973, 1737, 396, 1899, 568, 1425, 723, 686, 427, 1147, 518, 1627, 1190, 1226, 603, 591, 971, 1091, 1061, 545, 657, 535, 2464, 705, 630, 1595, 2410, 826, 628, 601, 308, 271, 1089, 1086, 632, 1273, 226, 1788, 1425, 626, 741, 345, 587, 3248, 872, 488, 1500, 1637, 929, 583, 2855, 659, 198, 566, 1609, 966, 375, 691, 946, 2076, 1024, 554, 225, 1440, 624, 1271, 387, 3473, 1715, 1589, 1217, 1031, 1566, 1127, 4301, 1286, 1032, 196, 432, 1551, 2251, 2208, 1454, 3446, 1152, 700, 978, 573, 3302, 856, 707, 492, 490, 582, 637, 540, 588, 546, 2142, 146, 1916, 438, 2207, 952, 996, 2419, 1752, 1639, 705, 418, 1796, 587, 562, 1784, 529, 824, 2885, 2016, 1237, 2291, 637, 310, 920, 805, 2998, 708, 1146, 797, 1647, 567, 906, 409, 340, 210, 2681, 1337, 1224, 1409, 751, 1536, 2095, 606, 448, 712, 2351, 517, 4100, 760, 1290, 696, 1041, 641, 658, 848, 742, 1235, 1406, 747, 1310, 366, 1456, 619, 221, 623, 473, 2065, 586, 590, 438, 4473, 1356, 532, 972, 717, 3798, 595, 1439, 987, 757, 727, 1865, 392, 3102, 463, 921, 1440, 596, 904, 597, 615, 342, 2586, 1441, 705, 2150, 1126, 678, 1178, 429, 1887, 912, 508, 1236, 124, 534, 313, 227, 964, 515, 1365, 1174, 523, 2418, 325, 508, 635, 1419, 653, 734, 648, 868, 1299, 874, 961, 2791, 1041, 518, 1593, 581, 920, 709, 1164, 1035, 1068, 815, 1223, 625, 3034, 3484, 201, 1628, 994, 1962, 550, 493, 814, 634, 888, 1555, 576, 4473, 171, 742, 2177, 538, 1177, 581, 900, 791, 1041, 949, 1590, 227, 1501, 1413, 349, 715, 674, 1116, 479, 804, 826, 1385, 323, 324, 1450, 916, 914, 3668, 1588, 203, 622, 938, 152, 1872, 1705, 368, 1935, 886, 723, 1484, 1531, 768, 4575, 229, 974, 1232, 994, 608, 292, 655, 3183, 1380, 558, 640, 1275, 849, 865, 217, 522, 655, 527, 1309, 724, 838, 870, 590, 1444, 1191, 859, 652, 2149, 1588, 1048, 680, 1050, 928, 637, 1016, 956, 720, 1023, 502, 1347, 529, 400, 960, 838, 715, 699, 650, 308, 4325, 923, 1256, 1436, 909, 708, 917, 511, 2206, 543, 458, 1247, 535, 1938, 1390, 1038, 1061, 867, 268, 1450, 594, 3420, 234, 635, 1925, 954, 821, 878, 385, 377, 346, 729, 3598, 436, 915, 515, 3344, 650, 551, 605, 524, 3133, 966, 486, 1006, 2807, 2378, 3948, 860, 183, 601, 843, 1037, 873, 882, 533, 556, 267, 864, 2576, 792, 909, 1731, 949, 901, 649, 664, 2784, 1124, 670, 592, 253, 730, 1041, 739, 1526, 711, 616, 288, 710, 591, 552, 522, 870, 812, 679, 294, 752, 1390, 948, 664, 333, 557, 934, 3427, 478, 716, 719, 2476, 1322, 620, 1821, 523, 756, 1591, 1851, 753, 1264, 766, 759, 2251, 976, 1099, 332, 1526, 530, 3380, 309, 955, 735, 1657, 518, 2775, 399, 1328, 1388, 797, 947, 238, 917, 2344, 1919, 541, 271, 1111, 1362, 560, 743, 853, 2295, 541, 1228, 491, 1017, 552, 3340, 518, 1104, 597, 638, 1892, 1311, 679, 711, 578, 681, 652, 873, 664, 486, 844, 1976, 318, 554, 471, 436, 488, 988, 1615, 4478, 1242, 1246, 804, 883, 741, 1104, 744, 850, 562, 1980, 739, 3339, 1455, 590, 252, 1921, 829, 1244, 1221, 1248, 1258, 248, 4166, 1127, 673, 1961, 1138, 495, 361, 794, 594, 705, 557, 4360, 482, 809, 748, 2090, 712, 771, 631, 978, 1831, 401, 753, 898, 374, 584, 438, 984, 1660, 699, 529, 2797, 716, 771, 1725, 270, 444, 447, 576, 621, 2673, 1035, 2846, 709, 1239, 524, 594, 618, 765, 605, 510, 627, 884, 523, 711, 1070, 916, 682, 609, 1611, 1001, 1191, 1214, 1226, 1220, 816, 594, 829, 1340, 199, 339, 841, 980, 1172, 670, 1703, 832, 1158, 1674, 602, 1103, 3452, 1654, 1428, 558, 711, 1093, 622, 1074, 679, 1027, 497, 675, 1264, 517, 893, 476, 1786, 627, 662, 623, 3150, 370, 611, 561, 594, 702, 1707, 1651, 526, 808, 421, 719, 637, 342, 295, 1655, 181, 1509, 1176, 679, 823, 2783, 587, 1074, 883, 674, 545, 2022, 866, 787, 633, 542, 744, 567, 633, 275, 694, 570, 565, 1876, 791, 369, 1423, 430, 625, 581, 445, 447, 826, 1764, 628, 3734, 1433, 553, 772, 814, 1134, 470, 747, 317, 718, 587, 675, 545, 779, 512, 696, 1379, 1702, 871, 1652, 1005, 627, 551, 2544, 1079, 581, 1902, 816, 1001, 2163, 553, 676, 717, 326, 711, 808, 4601, 992, 922, 549, 622, 250, 1098, 756, 858, 999, 1126, 512, 901, 723, 487, 608, 1374, 217, 2607, 904, 4863, 627, 1325, 642, 1405, 718, 1488, 1548, 551, 712, 694, 565, 912, 1361, 706, 1970, 1158, 370, 790, 2293, 810, 462, 469, 246, 1159, 1045, 1286, 2153, 756, 1551, 627, 878, 238, 704, 1028, 522, 875, 559, 2178, 759, 1705, 514, 2906, 504, 716, 604, 599, 1265, 898, 376, 779, 745, 563, 770, 1182, 729, 1873, 2430, 643, 540, 498, 540, 329, 2345, 604, 1707, 604, 179, 1389, 508, 538, 521, 528, 608, 542, 604, 543, 728, 1383, 607, 715, 675, 1511, 495, 3541, 1039, 2223, 1622, 596, 4257, 528, 604, 2241, 546, 1142, 1937, 989, 2017, 589, 1552, 613, 757, 88, 2260, 765, 647, 4580, 397, 1410, 958, 1432, 1506, 544, 802, 1902, 570, 807, 592, 2151, 284, 1404, 637, 606, 1107, 688, 419, 376, 560, 2202, 561, 1280, 2291, 697, 270, 648, 731, 1748, 774, 577, 993, 858, 781, 713, 351, 213, 238, 983, 569, 1138, 2086, 716, 630, 1597, 762, 830, 236, 343, 574, 844, 727, 1551, 1097, 232, 2246, 789, 2976, 526, 961, 4968, 541, 2163, 1274, 2497, 667, 1050, 956, 1747, 561, 1437, 721, 822, 814, 1789, 2093, 1382, 547, 1089, 690, 527, 1712, 2150, 1282, 583, 544, 977, 851, 643, 782, 624, 1817, 1178, 677, 760, 494, 535, 746, 757, 1380, 547, 955, 1090, 776, 524, 423, 546, 1989, 655, 933, 558, 984, 584, 559, 999, 372, 738, 1319, 521, 1828, 1021, 670, 868, 3156, 4706, 3903, 382, 1435, 616, 508, 545, 529, 121, 1232, 793, 1402, 405, 994, 1976, 618, 2084, 538, 742, 830, 576, 638, 3267, 2237, 547, 5155, 694, 2011, 818, 227, 4844, 1921, 2273, 3359, 470, 852, 262, 620, 849, 2707, 1020, 688, 787, 1585, 798, 598, 989, 537, 748, 804, 648, 909, 3348, 246, 551, 613, 2014, 195, 877, 797, 257, 525, 1438, 942, 2575, 2179, 1030, 2592, 1182, 1129, 624, 567, 1416, 1254, 436, 2695, 745, 566, 2356, 1003, 414, 522, 648, 646, 1408, 938, 625, 833, 646, 522, 1573, 533, 448, 458, 1044, 687, 583, 311, 345, 1903, 1080, 1229, 1252, 1749, 667, 1636, 682, 685, 45, 556, 1668, 980, 528, 544, 1555, 1195, 569, 1003, 572, 518, 780, 2647, 690, 510, 1343, 825, 1337, 646, 912, 400, 2376, 522, 1817, 2034, 694, 1073, 805, 861, 772, 1377, 527, 523, 1222, 955, 1293, 564, 958, 796, 758, 761, 910, 940, 178, 633, 887, 550, 739, 756, 1996, 2022, 2013, 1877, 1409, 1475, 1652, 767, 2015, 1080, 998, 1387, 1104, 1065, 2758, 761, 647, 640, 623, 237, 815, 8628, 685, 668, 971, 572, 378, 642, 712, 567, 1148, 477, 1245, 538, 1805, 635, 827, 681, 1413, 608, 371, 282, 2610, 674, 2227, 762, 603, 3445, 833, 580, 1045, 593, 732, 2430, 1227, 1181, 847, 567, 455, 784, 2077, 809, 325, 725, 659, 2926, 736, 437, 2482, 706, 639, 470, 669, 682, 590, 1700, 1574, 617, 532, 578, 591, 313, 1081, 1024, 2107, 1971, 939, 640, 2655, 4541, 1739, 2709, 2258, 1133, 570, 3431, 2085, 559, 822, 813, 1942, 837, 1240, 621, 930, 1254, 2367, 1591, 844, 2695, 932, 837, 658, 2179, 2350, 969, 365, 210, 1128, 808, 2630, 494, 648, 2219, 604, 663, 810, 750, 533, 192, 3089, 1350, 1497, 817, 4260, 2815, 930, 2543, 1773, 506, 692, 1080, 764, 801, 877, 612, 4132, 769, 751, 565, 1702, 1000, 1920, 1453, 388, 161, 716, 2797, 644, 785, 1259, 1746, 781, 713, 2465, 1512, 842, 896, 1392, 589, 1438, 731, 513, 2512, 519, 614, 560, 2149, 1000, 1005, 1790, 843, 685, 928, 1574, 390, 4195, 4657, 907, 355, 695, 870, 305, 346, 660, 510, 527, 1192, 654, 601, 586, 2328, 246, 619, 630, 547, 1811, 1855, 1139, 1429, 614, 770, 595, 2170, 491, 333, 1353, 1198, 1022, 1954, 434, 190, 1752, 1912, 841, 587, 775, 195, 1268, 3194, 1347, 971, 909, 2197, 971, 849, 4759, 4632, 638, 562, 989, 1030, 1005, 675, 710, 1007, 681, 973, 974, 2186, 577, 483, 501, 723, 2704, 3121, 650, 963, 913, 490, 1493, 590, 1307, 1364, 3806, 772, 1536, 1671, 723, 563, 245, 1113, 1530, 580, 1241, 537, 1110, 988, 249, 658, 627, 721, 834, 804, 726, 444, 3872, 554, 216, 571, 1454, 382, 692, 662, 541, 4920, 1149, 538, 584, 868, 2512, 666, 1421, 1702, 810, 4493, 562, 347, 598, 1567, 398, 1914, 306, 678, 335, 831, 3633, 3671, 3003, 775, 956, 326, 892, 1427, 506, 767, 595, 903, 1449, 366, 888, 703, 794, 805, 922, 2787, 2573, 638, 1725, 1331, 1671, 1089, 674, 576, 860, 1274, 1218, 529, 620, 1500, 943, 530, 988, 695, 2026, 263, 611, 538, 650, 584, 860, 545, 431, 242, 2708, 1786, 989, 671, 521, 2620, 1226, 781, 1100, 331, 660, 1867, 685, 1143, 724, 1117, 2588, 272, 319, 686, 2021, 717, 1202, 1155, 244, 537, 623, 2783, 2684, 315, 1212, 570, 1280, 332, 801, 611, 1285, 2197, 2519, 708, 539, 878, 866, 868, 4379, 515, 289, 344, 1780, 2846, 692, 1885, 665, 620, 795, 607, 530, 799, 355, 2777, 2152, 757, 276, 1948, 460, 804, 2241, 526, 527, 1260, 559, 611, 2415, 704, 340, 610, 646, 509, 1189, 538, 980, 675, 1147, 620, 927, 1540, 706, 3274, 4967, 658, 466, 517, 1467, 296, 965, 1043, 1389, 209, 1072, 1583, 2048, 967, 723, 560, 879, 1382, 1651, 1030, 3236, 2064, 502, 530, 536, 1059, 296, 1541, 910, 1647, 563, 732, 795, 640, 3787, 1988, 556, 651, 1534, 867, 692, 790, 1003, 1031, 562, 941, 335, 882, 4694, 996, 547, 639, 599, 1803, 636, 553, 715, 535, 1207, 598, 547, 917, 1997, 2893, 3719, 2563, 1250, 679, 548, 1057, 989, 598, 1847, 230, 1662, 1943, 834, 1581, 664, 1732, 588, 1629, 429, 705, 728, 888, 470, 1317, 2112, 216, 498, 1983, 397, 843, 531, 2095, 727, 610, 702, 799, 1296, 568, 1282, 638, 2384, 1576, 829, 193, 1054, 1233, 792, 640, 580, 1329, 591, 481, 1775, 403, 380, 1588, 1599, 2999, 719, 913, 3353, 1973, 1143, 1418, 759, 1038, 978, 596, 496, 231, 548, 1866, 839, 410, 1456, 214, 2281, 552, 633, 184, 442, 731, 322, 553, 1163, 799, 613, 696, 917, 747, 630, 1250, 552, 544, 1293, 334, 547, 1698, 323, 270, 865, 2403, 2468, 1747, 781, 825, 626, 1200, 1137, 784, 330, 937, 561, 1978, 821, 1656, 691, 1338, 309, 664, 1066, 559, 605, 2861, 3289, 438, 1895, 673, 1118, 872, 413, 1215, 2949, 1070, 3183, 2683, 1360, 1461, 2034, 1017, 8485, 1019, 559, 641, 1987, 1839, 745, 1012, 854, 505, 511, 1457, 1490, 301, 241, 588, 1172, 614, 3464, 422, 1104, 841, 680, 1322, 957, 633, 168, 3293, 2045, 251, 534, 2370, 526, 568, 924, 790, 556, 1101, 655, 581, 602, 2188, 333, 332, 1281, 2389, 568, 1252, 983, 441, 237, 560, 2300, 432, 842, 1122, 989, 535, 1333, 1641, 519, 685, 794, 623, 410, 1094, 635, 1526, 812, 872, 2322, 1430, 1112, 1179, 556, 1630, 812, 421, 427, 612, 567, 868, 691, 654, 956, 1223, 902, 1247, 829, 2832, 828, 610, 1788, 877, 2131, 553, 666, 1363, 216, 549, 3973, 383, 1669, 448, 628, 836, 512, 629, 2175, 2070, 765, 424, 2963, 2049, 3539, 752, 555, 231, 1926, 1736, 1369, 1084, 2799, 1608, 489, 736, 759, 1211, 1496, 2554, 541, 1935, 802, 929, 1238, 3490, 831, 188, 880, 582, 262, 1496, 567, 672, 1104, 3582, 2605, 1558, 783, 1073, 613, 272, 622, 324, 277, 949, 620, 741, 382, 908, 836, 355, 791, 2493, 1022, 2824, 135, 720, 699, 502, 622, 1760, 2597, 1440, 299, 303, 563, 706, 1054, 2060, 764, 815, 583, 1143, 600, 2539, 588, 531, 650, 331, 520, 1184, 801, 2019, 612, 593, 1113, 769, 676, 966, 1643, 613, 1126, 2223, 890, 1085, 1030, 475, 1395, 2116, 548, 1035, 2474, 1081, 618, 587, 1293, 493, 334, 1234, 1013, 1119, 1588, 269, 409, 901, 438, 182, 2797, 831, 1124, 754, 3207, 267, 364, 1566, 739, 600, 2647, 2443, 499, 705, 836, 1507, 255, 582, 430, 519, 2837, 561, 579, 1790, 2644, 946, 1325, 541, 855, 784, 250, 458, 567, 800, 697, 534, 577, 1119, 5030, 1546, 1201, 1538, 591, 1050, 1676, 1404, 537, 515, 1104, 1029, 947, 544, 215, 1935, 491, 639, 332, 682, 510, 1368, 851, 836, 1614, 513, 1200, 1020, 345, 921, 1703, 329, 206, 654, 562, 1721, 640, 326, 931, 1474, 801, 804, 626, 2450, 530, 936, 3108, 2903, 589, 1583, 4862, 982, 539, 742, 461, 617, 881, 1205, 825, 2699, 748, 755, 1440, 289, 1271, 3383, 4155, 1429, 617, 438, 758, 699, 2228, 570, 558, 1276, 535, 1359, 2031, 1002, 854, 786, 500, 451, 524, 585, 568, 1397, 1763, 2246, 583, 479, 620, 2733, 674, 484, 789, 1728, 670, 544, 2223, 3769, 601, 586, 519, 2090, 1144, 569, 655, 830, 1428, 539, 2553, 2860, 529, 687, 634, 657, 355, 914, 554, 1725, 583, 1647, 1560, 629, 519, 829, 762, 433, 1044, 1217, 548, 1173, 1826, 523, 1613, 614, 2710, 994, 1442, 880, 1141, 932, 844, 1544, 702, 1122, 729, 808, 2866, 398, 2464, 1565, 742, 2055, 1076, 1406, 689, 1709, 1007, 1047, 2625, 951, 1449, 1304, 967, 806, 2535, 1784, 835, 668, 705, 688, 472, 1064, 960, 686, 1368, 3286, 200, 820, 532, 1510, 1282, 642, 568, 586, 567, 360, 338, 618, 3742, 2129, 575, 1552, 566, 811, 345, 2589, 2242, 505, 287, 1274, 1114, 669, 1096, 568, 471, 294, 623, 1213, 1113, 1096, 3125, 953, 846, 718, 1320, 572, 561, 1664, 2771, 859, 2313, 705, 1876, 627, 598, 974, 522, 1045, 2234, 2342, 1382, 1467, 1613, 1408, 1033, 1533, 1103, 344, 1652, 1725, 946, 907, 609, 588, 524, 3280, 576, 960, 712, 1291, 538, 551, 281, 550, 1251, 935, 3731, 2029, 808, 1044, 613, 563, 661, 1303, 1240, 213, 214, 1041, 425, 576, 677, 793, 993, 713, 1386, 1544, 607, 2539, 732, 2742, 1648, 790, 454, 704, 410, 1154, 4493, 767, 676, 1339, 841, 1388, 1454, 634, 1124, 587, 1468, 591, 674, 983, 2492, 1536, 519, 204, 2667, 986, 517, 374, 2774, 351, 678, 431, 548, 1685, 607, 574, 226, 551, 745, 1360, 530, 772, 1054, 385, 1186, 563, 759, 1307, 1354, 831, 531, 599, 765, 691, 1653, 897, 600, 610, 748, 582, 2384, 736, 948, 2386, 517, 1180, 624, 832, 754, 703, 482, 4665, 725, 3458, 560, 1239, 4268, 1448, 378, 1186, 525, 2403, 172, 695, 1388, 688, 541, 1691, 554, 1076, 1179, 616, 1654, 2138, 3440, 5151, 539, 381, 829, 2572, 549, 4000, 294, 1531, 1136, 1025, 660, 760, 1307, 498, 941, 2046, 2917, 754, 1163, 1616, 430, 4274, 1477, 1357, 618, 2027, 842, 450, 527, 922, 389, 629, 648, 598, 530, 568, 1490, 535, 1074, 534, 1606, 1870, 605, 3291, 566, 890, 967, 4578, 331, 425, 558, 793, 4770, 514, 532, 754, 2357, 878, 1886, 4630, 805, 667, 857, 2441, 593, 1499, 764, 3151, 1149, 1476, 1383, 476, 518, 629, 1053, 2892, 254, 1697, 693, 1266, 572, 260, 1058, 1300, 618, 2992, 688, 583, 1090, 687, 1146, 2075, 782, 816, 579, 461, 362, 1125, 824, 604, 1806, 3502, 941, 887, 242, 430, 1142, 1176, 513, 1616, 846, 1073, 377, 1206, 1588, 1670, 677, 1031, 497, 931, 1375, 3452, 3590, 675, 940, 769, 630, 421, 3810, 1538, 199, 3708, 946, 754, 204, 1928, 1868, 661, 952, 1155, 362, 4783, 546, 721, 1082, 583, 939, 662, 554, 625, 787, 722, 2670, 749, 2109, 972, 1773, 602, 1946, 1461, 2363, 600, 693, 950, 607, 2765, 550, 837, 723, 518, 1550, 690, 663, 1175, 938, 2429, 1092, 580, 1047, 754, 294, 1209, 1236, 1024, 728, 544, 1484, 952, 2182, 823, 1004, 1637, 627, 658, 1555, 1191, 301, 526, 607, 535, 1829, 543, 2072, 1781, 716, 1072, 1134, 619, 688, 187, 2360, 673, 1143, 949, 662, 739, 1029, 1081, 2358, 1958, 1688, 2080, 1256, 517, 238, 205, 416, 609, 1367, 652, 835, 1245, 3163, 540, 826, 649, 467, 570, 791, 692, 207, 415, 3183, 861, 1785, 295, 2015, 1475, 822, 890, 3501, 447, 610, 656, 956, 1656, 1650, 1537, 899, 1471, 2034, 746, 545, 2414, 1696, 558, 732, 548, 610, 1425, 1087, 765, 557, 1385, 1991, 265, 1931, 165, 552, 696, 796, 552, 550, 487, 1321, 714, 2007, 507, 696, 1648, 655, 314, 1195, 623, 598, 786, 610, 663, 521, 825, 1827, 976, 1468, 468, 544, 1414, 3169, 512, 628, 922, 923, 412, 630, 545, 502, 688, 934, 328, 1922, 1316, 697, 780, 2211, 924, 2463, 1413, 262, 1083, 900, 795, 776, 1631, 2333, 591, 1314, 940, 496, 1831, 4253, 718, 774, 1198, 1298, 558, 4365, 280, 669, 1143, 667, 596, 339, 372, 511, 496, 745, 620, 1664, 616, 763, 1009, 794, 1911, 1843, 586, 218, 530, 622, 312, 516, 1041, 3333, 913, 273, 2953, 1706, 4369, 1462, 804, 294, 794, 1278, 995, 855, 1372, 677, 847, 1183, 783, 670, 501, 474, 787, 1949, 679, 603, 691, 1794, 1160, 252, 1005, 541, 2235, 584, 1656, 1713, 309, 3958, 272, 658, 542, 903, 1128, 1047, 821, 1026, 432, 614, 223, 1513, 831, 513, 465, 1524, 338, 609, 619, 358, 549, 994, 2248, 637, 2229, 758, 849, 2333, 498, 3802, 936, 437, 570, 532, 1144, 581, 561, 817, 554, 1265, 799, 765, 685, 669, 1001, 208, 989, 664, 536, 912, 897, 594, 794, 288, 3839, 1014, 775, 2152, 1458, 328, 832, 2092, 3696, 864, 553, 2002, 777, 643, 1643, 1038, 572, 595, 282, 1720, 2992, 973, 564, 972, 1262, 645, 835, 1145, 1020, 556, 1369, 1472, 600, 901, 703, 847, 682, 1437, 888, 489, 683, 485, 727, 606, 697, 556, 560, 947, 729, 1499, 293, 757, 511, 635, 593, 1448, 845, 856, 192, 1121, 401, 769, 731, 1351, 677, 612, 259, 307, 692, 2988, 4644, 1150, 522, 777, 2166, 816, 478, 587, 278, 448, 1983, 670, 435, 2371, 677, 577, 549, 409, 731, 790, 665, 3048, 501, 988, 666, 676, 1812, 766, 134, 1082, 1183, 586, 811, 191, 551, 652, 579, 1843, 1581, 804, 1505, 497, 198, 948, 553, 323, 598, 1875, 860, 990, 526, 607, 714, 1027, 1190, 237, 2115, 229, 1890, 1455, 1191, 551, 575, 2767, 1302, 189, 918, 1088, 478, 970, 558, 202, 685, 518, 265, 496, 562, 758, 483, 694, 479, 796, 1037, 963, 2197, 797, 2531, 959, 1357, 463, 544, 590, 679, 1007, 595, 2516, 492, 631, 1049, 55, 734, 1011, 684, 788, 748, 4837, 811, 2807, 1061, 898, 1354, 988, 1052, 310, 526, 802, 310, 1583, 541, 549, 1026, 2175, 784, 2498, 311, 2038, 752, 1648, 638, 567, 884, 747, 544, 602, 1589, 2560, 561, 254, 1951, 1119, 227, 496, 788, 4179, 1307, 821, 751, 586, 696, 320, 2166, 654, 587, 756, 2370, 800, 884, 2553, 727, 621, 867, 645, 1377, 1016, 476, 530, 240, 2236, 604, 786, 1981, 1448, 897, 859, 703, 549, 190, 580, 942, 565, 979, 363, 659, 390, 1242, 1354, 458, 769, 574, 1569, 809, 603, 1883, 2107, 695, 844, 551, 1512, 601, 527, 899, 538, 1809, 841, 797, 379, 1139, 413, 570, 622, 302, 529, 777, 529, 847, 334, 1469, 505, 343, 2921, 1584, 1101, 2113, 551, 748, 223, 1236, 266, 133, 2787, 700, 1994, 1854, 1651, 502, 624, 551, 670, 593, 553, 1124, 1165, 3019, 398, 540, 551, 604, 1575, 595, 1720, 986, 239, 806, 1314, 1690, 1020, 838, 523, 518, 529, 2869, 2585, 2093, 535, 1279, 2106, 548, 1794, 412, 1264, 872, 563, 472, 1239, 546, 375, 1123, 870, 990, 611, 1494, 457, 659, 686, 319, 275, 3881, 274, 695, 929, 649, 1139, 1318, 626, 953, 1551, 1278, 989, 1517, 480, 3225, 1865, 403, 654, 536, 2497, 530, 1167, 2058, 348, 1952, 1009, 971, 1897, 892, 870, 521, 494, 690, 668, 615, 2375, 870, 498, 905, 598, 531, 523, 705, 1612, 1264, 823, 6402, 983, 1529, 950, 1353, 885, 240, 534, 1015, 877, 646, 559, 510, 1071, 695, 1689, 2643, 659, 698, 1111, 1541, 3255, 730, 829, 2602, 850, 532, 772, 305, 2903, 1884, 555, 744, 1026, 991, 760, 1325, 513, 602, 2221, 942, 351, 628, 3334, 1135, 2793, 2033, 1340, 3249, 701, 1066, 201, 1142, 691, 671, 767, 692, 936, 468, 1134, 1134, 643, 2032, 1110, 1223, 662, 967, 1361, 587, 464, 549, 955, 1178, 986, 1358, 618, 1140, 1210, 173, 3147, 530, 1556, 627, 596, 911, 568, 313, 499, 1397, 557, 646, 1298, 2447, 1086, 1433, 1338, 1726, 218, 804, 813, 242, 746, 337, 984, 317, 370, 1505, 488, 594, 1311, 603, 845, 2657, 1563, 547, 2188, 2798, 1298, 789, 788, 745, 4247, 2791, 616, 540, 1264, 1157, 712, 2003, 1086, 307, 654, 441, 671, 1631, 992, 1087, 1129, 1459, 930, 770, 535, 681, 2132, 1621, 643, 704, 748, 866, 2370, 455, 510, 1098, 269, 474, 1053, 1382, 303, 3287, 317, 2031, 1018, 825, 608, 469, 1444, 1247, 1363, 494, 1010, 704, 668, 968, 632, 821, 780, 1764, 667, 3577, 282, 1638, 680, 777, 687, 2209, 1170, 1875, 369, 1388, 534, 482, 1960, 993, 633, 817, 1626, 459, 1093, 516, 1671, 972, 1130, 1516, 783, 336, 412, 751, 532, 3967, 1820, 711, 707, 1191, 614, 544, 2856, 2538, 512, 2805, 715, 2113, 1383, 683, 924, 699, 1592, 2817, 475, 590, 1149, 494, 2470, 569, 780, 706, 657, 771, 1818, 645, 1089, 698, 2243, 638, 590, 1432, 1113, 437, 1008, 1054, 496, 262, 464, 518, 938, 557, 671, 801, 292, 2005, 904, 201, 334, 4247, 2354, 1715, 674, 205, 1255, 762, 1643, 2368, 792, 591, 494, 690, 1987, 1206, 1379, 536, 1659, 751, 1105, 302, 823, 1355, 522, 1170, 668, 693, 574, 1100, 692, 240, 2224, 738, 772, 658, 1138, 557, 736, 839, 1114, 1866, 809, 1809, 377, 657, 1067, 1182, 579, 1377, 1980, 266, 2390, 809, 131, 2175, 645, 493, 785, 1101, 1306, 223, 819, 528, 679, 895, 885, 496, 654, 910, 1133, 702, 3535, 798, 2746, 500, 1215, 2929, 854, 1500, 379, 190, 542, 1096, 193, 3225, 639, 263, 1617, 524, 745, 1281, 533, 933, 1864, 641, 596, 1718, 755, 435, 829, 1205, 893, 1507, 883, 699, 535, 825, 800, 741, 1227, 5065, 1501, 1616, 260, 572, 414, 1545, 656, 878, 1289, 2057, 548, 1102, 1724, 984, 2371, 219, 534, 550, 664, 814, 498, 1223, 764, 707, 567, 5508, 770, 586, 499, 1865, 277, 548, 255, 808, 1216, 1337, 568, 704, 1914, 659, 600, 540, 310, 937, 2217, 716, 1130, 247, 302, 710, 557, 3565, 662, 1149, 1328, 960, 1315, 687, 733, 625, 670, 724, 1911, 1579, 290, 433, 531, 617, 746, 1998, 525, 698, 436, 2052, 459, 3186, 300, 805, 953, 424, 341, 592, 542, 1035, 1172, 954, 316, 3125, 1428, 1913, 1763, 651, 839, 1162, 1032, 527, 2604, 769, 881, 512, 731, 488, 1242, 673, 3150, 314, 588, 704, 764, 731, 3915, 2286, 1141, 667, 798, 1298, 803, 1571, 822, 674, 2030, 679, 768, 319, 536, 730, 1042, 1463, 562, 305, 250, 2542, 765, 677, 630, 1181, 1055, 736, 1443, 282, 607, 750, 576, 1765, 1009, 686, 466, 2674, 673, 661, 625, 521, 3019, 650, 922, 568, 541, 2140, 2950, 799, 1285, 1135, 1273, 890, 518, 1276, 509, 794, 1441, 1026, 697, 620, 937, 1540, 890, 637, 1272, 951, 1616, 993, 1401, 1924, 486, 299, 667, 545, 369, 647, 625, 930, 2121, 475, 1115, 461, 1270, 497, 958, 686, 603, 616, 1004, 316, 944, 1272, 1005, 1019, 316, 823, 566, 891, 2103, 1787, 596, 2819, 831, 2870, 1792, 264, 1242, 1699, 631, 971, 513, 867, 1801, 590, 833, 637, 1082, 739, 793, 845, 2920, 909, 1146, 1546, 842, 1066, 1396, 680, 705, 1005, 1107, 945, 595, 546, 1552, 1289, 561, 1169, 705, 825, 1692, 233, 503, 1056, 1859, 558, 519, 1321, 633, 1116, 540, 1340, 1651, 1453, 559, 194, 543, 494, 1568, 865, 538, 1714, 1779, 3516, 808, 627, 1282, 545, 4530, 3614, 335, 893, 321, 533, 156, 730, 1445, 669, 2167, 820, 480, 1152, 855, 1733, 734, 558, 521, 2074, 652, 2813, 729, 1393, 877, 534, 861, 786, 1127, 1565, 1362, 444, 618, 625, 776, 431, 1286, 752, 450, 656, 532, 859, 2309, 811, 1492, 400, 661, 2321, 968, 1879, 598, 1420, 938, 236, 773, 1771, 690, 342, 3224, 712, 619, 924, 516, 2997, 976, 1787, 616, 338, 999, 1864, 1694, 412, 669, 759, 1284, 644, 170, 2470, 1396, 242, 3114, 763, 513, 853, 489, 637, 315, 775, 571, 564, 497, 283, 750, 1223, 1611, 539, 481, 627, 1136, 1129, 276, 1154, 2420, 1312, 2915, 765, 717, 794, 877, 808, 799, 357, 996, 2516, 1004, 526, 627, 492, 691, 607, 618, 1556, 719, 821, 502, 1013, 1067, 656, 912, 1333, 1079, 1114, 309, 898, 270, 575, 753, 563, 218, 1034, 889, 615, 238, 587, 855, 541, 1494, 939, 570, 824, 297, 2639, 748, 1651, 549, 732, 1688, 788, 3619, 700, 682, 579, 1107, 704, 956, 871, 1409, 1072, 601, 643, 446, 1463, 378, 519, 934, 1437, 1306, 1438, 596, 767, 239, 811, 698, 783, 1178, 1300, 904, 1167, 901, 2073, 2605, 761, 3061, 1436, 760, 708, 550, 1153, 1491, 2356, 548, 1987, 1061, 911, 1378, 1584, 540, 1480, 2053, 283, 477, 1019, 2135, 226, 450, 899, 910, 1485, 1459, 735, 146, 1455, 535, 235, 576, 1231, 547, 692, 1244, 208, 315, 659, 1373, 862, 4317, 964, 365, 1166, 2523, 1791, 1240, 797, 451, 2488, 2118, 936, 163, 1918, 646, 546, 704, 956, 1275, 725, 723, 358, 740, 2332, 638, 1081, 518, 2208, 557, 480, 247, 484, 570, 667, 590, 667, 693, 1601, 1048, 1521, 279, 1014, 252, 410, 1700, 417, 589, 1081, 869, 958, 1071, 1171, 552, 869, 891, 935, 1369, 1089, 580, 598, 644, 663, 938, 1005, 222, 1012, 276, 4310, 783, 777, 536, 1715, 962, 481, 2241, 686, 663, 1173, 631, 853, 812, 3527, 1490, 751, 633, 1189, 1078, 849, 598, 1350, 548, 524, 1215, 869, 724, 733, 1111, 1131, 1543, 1291, 907, 604, 1924, 2517, 1384, 450, 2751, 495, 1123, 684, 305, 4138, 812, 566, 2007, 944, 558, 635, 1068, 690, 216, 634, 1920, 3924, 4610, 531, 1134, 1165, 476, 972, 495, 1234, 877, 1346, 608, 785, 591, 4466, 1323, 884, 1315, 685, 639, 2762, 1442, 539, 970, 3224, 561, 619, 716, 773, 512, 646, 798, 1762, 3136, 643, 1138, 824, 748, 453, 1398, 580, 536, 833, 826, 634, 600, 4069, 1376, 555, 341, 1073, 769, 1375, 1171, 613, 997, 559, 46, 4664, 1408, 1862, 921, 530, 1501, 545, 1568, 549, 1140, 913, 2251, 2980, 3768, 1053, 2394, 1633, 1554, 543, 722, 992, 801, 594, 674, 1351, 609, 1013, 653, 553, 519, 1585, 1131, 1514, 1715, 1132, 2123, 189, 1964, 575, 438, 2083, 567, 1290, 618, 387, 1129, 491, 704, 1342, 538, 454, 1485, 564, 574, 502, 770, 1748, 1794, 334, 1206, 594, 2188, 648, 1625, 813, 1085, 967, 1050, 940, 711, 599, 811, 1024, 544, 515, 957, 329, 975, 1004, 527, 1538, 2055, 1317, 420, 544, 1609, 660, 696, 179, 1223, 3659, 1265, 758, 604, 1374, 736, 4084, 894, 1817, 1028, 2234, 510, 425, 341, 244, 524, 713, 783, 324, 1020, 3071, 563, 600, 1000, 1228, 929, 518, 901, 952, 576, 896, 1116, 667, 1754, 529, 661, 929, 1525, 1452, 1438, 1678, 656, 318, 608, 199, 233, 2180, 769, 586, 1114, 802, 625, 1826, 602, 650, 681, 2722, 2761, 1905, 1552, 571, 805, 3138, 1295, 609, 635, 4589, 1021, 602, 843, 716, 730, 678, 1483, 632, 767, 475, 2957, 885, 2464, 853, 529, 1064, 1911, 300, 1263, 1033, 3433, 484, 786, 279, 556, 891, 5673, 583, 1318, 138, 348, 2148, 360, 655, 1271, 1434, 534, 307, 841, 538, 807, 1665, 190, 852, 573, 4269, 1902, 1227, 2294, 704, 554, 686, 1609, 735, 743, 854, 603, 638, 234, 607, 652, 592, 609, 858, 543, 510, 2866, 2624, 496, 847, 318, 594, 1206, 569, 644, 628, 577, 745, 4449, 630, 2629, 596, 490, 1215, 303, 610, 763, 1838, 1196, 333, 3177, 1274, 624, 366, 2163, 1903, 2450, 585, 310, 931, 2419, 2121, 994, 467, 1192, 983, 528, 615, 631, 1960, 541, 1105, 489, 815, 889, 649, 877, 463, 2636, 973, 2266, 594, 1906, 1993, 517, 628, 1449, 620, 1186, 746, 915, 812, 592, 536, 434, 619, 746, 2476, 1644, 605, 688, 2058, 959, 673, 708, 322, 525, 581, 664, 2316, 471, 758, 569, 534, 527, 2841, 912, 2230, 2252, 358, 1713, 1853, 800, 1103, 740, 643, 640, 882, 560, 1857, 592, 244, 620, 778, 678, 4647, 697, 533, 1602, 421, 1369, 1110, 978, 1210, 297, 871, 2168, 562, 613, 537, 1954, 324, 323, 872, 606, 548, 514, 633, 720, 694, 596, 1029, 342, 393, 1817, 2346, 551, 1039, 1551, 2147, 2544, 629, 2340, 1410, 1095, 576, 1419, 1545, 1926, 845, 802, 583, 3860, 618, 305, 682, 449, 870, 3630, 111, 2347, 3126, 112, 404, 567, 962, 1800, 303, 232, 1139, 851, 1238, 3156, 533, 614, 994, 704, 269, 570, 525, 545, 741, 913, 986, 932, 554, 1713, 232, 1002, 3254, 811, 925, 3606, 4484, 516, 1230, 218, 1038, 866, 3800, 525, 654, 601, 1638, 642, 905, 408, 1292, 577, 549, 1270, 928, 4887, 224, 1294, 2923, 545, 1949, 678, 290, 1720, 3550, 309, 862, 672, 868, 563, 2069, 3752, 1012, 1364, 4430, 426, 1140, 1306, 645, 270, 828, 758, 828, 1270, 1427, 975, 1068, 1514, 2837, 815, 1006, 807, 1533, 541, 288, 926, 3647, 1710, 1278, 99, 2725, 668, 223, 610, 2556, 856, 893, 598, 577, 680, 893, 688, 873, 856, 1211, 543, 3332, 1031, 2148, 569, 1632, 669, 208, 640, 766, 1820, 432, 369, 876, 816, 3527, 816, 1436, 513, 1354, 664, 510, 551, 1078, 379, 1084, 470, 662, 1614, 799, 1208, 807, 1054, 1715, 583, 598, 796, 350, 250, 666, 693, 1609, 838, 575, 628, 940, 639, 714, 1004, 213, 237, 589, 534, 3024, 198, 770, 3074, 1849, 409, 593, 854, 2208, 541, 228, 517, 608, 1018, 533, 527, 1258, 688, 702, 573, 4629, 586, 1543, 2078, 692, 703, 497, 754, 760, 1802, 582, 988, 1001, 634, 438, 485, 766, 796, 809, 941, 1683, 470, 691, 3387, 554, 707, 1651, 830, 984, 1627, 484, 859, 492, 2283, 1240, 271, 2313, 1493, 647, 628, 1950, 458, 624, 273, 1994, 2339, 957, 1162, 584, 1990, 898, 538, 1639, 4121, 677, 650, 874, 1030, 373, 4842, 1822, 1290, 353, 2202, 276, 557, 2173, 1519, 555, 1463, 1949, 600, 839, 536, 931, 959, 674, 997, 1959, 1289, 712, 579, 668, 804, 487, 737, 1285, 785, 630, 484, 559, 85, 616, 1399, 703, 597, 621, 1210, 547, 656, 1081, 625, 1196, 518, 845, 432, 974, 705, 1109, 340, 442, 828, 1984, 400, 1479, 426, 407, 465, 243, 1243, 1794, 546, 617, 592, 751, 1153, 1810, 2507, 818, 377, 2472, 992, 536, 653, 2803, 654, 3456, 1861, 1415, 499, 543, 2511, 770, 230, 1156, 346, 910, 1279, 1358, 1507, 1294, 203, 1473, 287, 242, 794, 816, 1525, 1241, 968, 695, 1381, 1124, 4395, 572, 755, 678, 600, 514, 736, 614, 696, 1950, 1024, 605, 594, 547, 233, 975, 2354, 618, 724, 2247, 236, 1758, 2620, 610, 527, 1412, 2781, 588, 1336, 699, 513, 825, 606, 1433, 528, 753, 686, 2245, 1660, 1741, 2116, 1004, 669, 1113, 1479, 568, 414, 810, 575, 2085, 758, 769, 674, 243, 3005, 532, 507, 283, 665, 567, 923, 1757, 1564, 738, 528, 2241, 802, 1575, 226, 1629, 726, 526, 812, 594, 2323, 959, 259, 246, 766, 580, 585, 1239, 866, 628, 1227, 443, 876, 559, 1217, 500, 777, 1255, 521, 1868, 707, 216, 1082, 1115, 561, 771, 744, 3874, 2252, 567, 1344, 2865, 1289, 741, 548, 688, 2937, 1492, 830, 586, 1108, 2181, 1537, 1758, 1493, 614, 1002, 1352, 171, 1003, 594, 352, 2630, 213, 516, 1695, 2097, 956, 1343, 1351, 831, 598, 1454, 565, 754, 1310, 706, 459, 744, 757, 1219, 414, 1016, 566, 514, 827, 2912, 4995, 585, 575, 1070, 338, 511, 1137, 960, 976, 5258, 775, 310, 447, 1631, 521, 1414, 810, 1160, 1322, 3412, 816, 664, 568, 1092, 806, 1371, 963, 1131, 665, 959, 607, 709, 1527, 623, 727, 949, 544, 1930, 535, 775, 547, 482, 1334, 749, 593, 880, 296, 933, 1001, 986, 290, 764, 2636, 692, 651, 813, 590, 1360, 632, 694, 3173, 419, 540, 1145, 272, 621, 794, 508, 1219, 374, 1037, 1344, 1706, 596, 1230, 542, 2668, 660, 541, 233, 907, 609, 669, 509, 1310, 2927, 1950, 516, 2545, 1227, 760, 545, 3315, 574, 518, 1487, 1654, 498, 976, 976, 3127, 1398, 1229, 845, 682, 483, 1058, 547, 1310, 505, 1116, 2217, 2948, 965, 467, 1109, 810, 315, 884, 992, 1668, 836, 1221, 1387, 1412, 617, 1406, 610, 630, 2202, 200, 146, 901, 205, 535, 357, 551, 472, 1354, 688, 567, 410, 1600, 1718, 1440, 775, 608, 623, 674, 906, 2667, 3055, 541, 780, 623, 222, 1340, 527, 897, 539, 1751, 778, 2164, 885, 1334, 2473, 182, 956, 2378, 602, 1313, 841, 621, 538, 841, 1040, 564, 858, 1709, 155, 3638, 612, 1080, 531, 924, 1012, 189, 560, 740, 520, 1801, 411, 697, 816, 3228, 757, 621, 466, 359, 185, 613, 648, 1064, 570, 695, 1113, 866, 551, 649, 886, 431, 507, 1159, 639, 1806, 606, 1754, 253, 220, 1611, 2142, 750, 684, 1112, 506, 2175, 644, 378, 527, 1430, 800, 586, 974, 853, 161, 506, 1906, 4287, 1320, 614, 924, 312, 4050, 592, 918, 385, 510, 326, 3228, 1052, 569, 1553, 558, 532, 274, 650, 1209, 1495, 725, 1285, 1242, 570, 710, 797, 286, 613, 618, 1769, 581, 1118, 924, 242, 785, 1199, 883, 270, 1130, 1269, 560, 820, 295, 1346, 491, 551, 610, 1400, 576, 743, 758, 439, 1307, 1183, 228, 413, 796, 657, 902, 377, 274, 1731, 934, 1369, 551, 1447, 244, 1592, 685, 1433, 1143, 2909, 908, 701, 1736, 2165, 352, 1713, 1462, 667, 1379, 644, 940, 613, 686, 2923, 2493, 979, 1827, 872, 1301, 932, 2337, 2810, 2587, 628, 2263, 346, 1125, 567, 571, 590, 243, 333, 2654, 694, 146, 650, 1602, 623, 1218, 622, 1361, 782, 829, 4271, 489, 592, 2796, 604, 2013, 941, 891, 1102, 785, 620, 751, 443, 887, 760, 654, 1134, 796, 534, 250, 1154, 417, 648, 523, 2140, 1041, 938, 785, 834, 539, 1058, 867, 4280, 669, 658, 427, 629, 1241, 1465, 2899, 843, 729, 1038, 543, 1244, 2165, 209, 307, 778, 502, 606, 332, 826, 4017, 734, 2420, 173, 2121, 588, 572, 755, 761, 810, 1845, 933, 438, 447, 2076, 814, 751, 552, 286, 1532, 868, 377, 826, 687, 858, 2618, 749, 586, 1056, 586, 794, 1811, 590, 1367, 377, 373, 970, 837, 2084, 665, 850, 665, 783, 900, 1984, 1562, 202, 706, 1755, 503, 1752, 1096, 631, 916, 636, 922, 426, 518, 777, 1181, 1056, 1096, 2899, 1496, 804, 1689, 515, 682, 4089, 1100, 230, 521, 595, 507, 1187, 1664, 80, 778, 634, 288, 1232, 312, 218, 284, 1945, 523, 573, 320, 3010, 1738, 680, 841, 768, 657, 2485, 965, 1746, 613, 1315, 711, 1608, 523, 1024, 1731, 575, 1889, 603, 2771, 1129, 550, 726, 1706, 765, 601, 574, 625, 863, 617, 306, 881, 516, 1960, 1299, 1377, 638, 787, 759, 1592, 870, 468, 293, 4929, 902, 644, 838, 817, 1418, 2140, 1852, 1135, 1256, 266, 2394, 1569, 488, 804, 517, 947, 761]



```python
train_data['review'].str.split()
```




    0        ["With, all, this, stuff, going, down, at, the...
    1        ["\"The, Classic, War, of, the, Worlds\", by, ...
    2        ["The, film, starts, with, a, manager, (Nichol...
    3        ["It, must, be, assumed, that, those, who, pra...
    4        ["Superbly, trashy, and, wondrously, unpretent...
                                   ...                        
    24995    ["It, seems, like, more, consideration, has, g...
    24996    ["I, don't, believe, they, made, this, film., ...
    24997    ["Guy, is, a, loser., Can't, get, girls,, need...
    24998    ["This, 30, minute, documentary, Buñuel, made,...
    24999    ["I, saw, this, movie, as, a, child, and, it, ...
    Name: review, Length: 25000, dtype: object




```python
## Alphabet length using pandas
train_word_length = train_data['review'].str.split().apply(len) 
train_eumjeol_length = train_data['review'].str.replace(" ", "").apply(len)
# train_length = train_data['review'].apply(len)
print(type(train_eumjeol_length))

train_eumjeol_length.head()
```

    <class 'pandas.core.series.Series'>





    0    1872
    1     791
    2    2074
    3    1869
    4    1867
    Name: review, dtype: int64




```python
# 그래프에 대한 이미지 사이즈 선언
# figsize: (가로, 세로) 형태의 튜플로 입력
plt.figure(figsize=(12, 5))
# 히스토그램 선언
    # bins: 히스토그램 값들에 대한 버켓 범위
    # range: x축 값의 범위
    # alpha: 그래프 색상 투명도
    # color: 그래프 색상
    # label: 그래프에 대한 라벨
plt.hist(len_tokenized_review, bins=200, alpha=0.5, color= 'r', label='word')
plt.hist(eumjeol_reviews, bins=200, alpha=0.5, color= 'b', label='eumjeol')

# plt.yscale('log')
# 그래프 제목
plt.title('Log-Histogram of length of review')
plt.legend()
# 그래프 x 축 라벨
plt.xlabel('Length of review')
# 그래프 y 축 라벨
plt.ylabel('Number of review')
```




    Text(0, 0.5, 'Number of review')




    
![png](../assets/images/ai/sequence-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__15_1.webp)
    



```python
def summary_token_len(x):
    print('문장 최대길이: {}'.format(np.max(x)))
    print('문장 최소길이: {}'.format(np.min(x)))
    print('문장 평균길이: {:.2f}'.format(np.mean(x)))
    print('문장 길이 표준편차: {:.2f}'.format(np.std(x)))
    print('문장 중간길이: {}'.format(np.median(x)))
    # 사분위의 대한 경우는 0~100 스케일로 되어있음
    print('제 1 사분위 길이: {}'.format(np.percentile(x, 25)))
    print('제 3 사분위 길이: {}'.format(np.percentile(x, 75)))

summary_token_len(len_tokenized_review)
```

    문장 최대길이: 2470
    문장 최소길이: 10
    문장 평균길이: 233.79
    문장 길이 표준편차: 173.73
    문장 중간길이: 174.0
    제 1 사분위 길이: 127.0
    제 3 사분위 길이: 284.0



```python
plt.figure(figsize=(3, 5))
# 박스플롯 생성
# 첫번째 파라메터: 여러 분포에 대한 데이터 리스트를 입력
# labels: 입력한 데이터에 대한 라벨
# showmeans: 평균값을 마크함

plt.boxplot(len_tokenized_review,
             tick_labels=['counts'],
             showmeans=True)
# plt.yscale('log')
plt.ylabel('Log scale')
plt.show()
```


    
![png](../assets/images/ai/sequence-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__17_0.webp)
    


###  WordCloud


```python
from wordcloud import WordCloud, STOPWORDS

my_stopword = ['br', 'movie', 'movies',
               'seen', 'film', 'seem', 'one',
               'seems', 'look', 'time', 'make',
               'see', 'made', 'show', 'will', 'something'
               'even', 'people', 'scene', 'thing'] + list(STOPWORDS)
```


```python

# cloud = WordCloud(stopwords=STOPWORDS,width=800, height=600).generate(" ".join(train_data['review']))
# print(STOPWORDS)
mytext = " ".join(train_data['review']) # '_'.join(['a', 'b', 'c']) 라 하면 "a_b_c"


# stop_words = ["br", "even", "little", "said"] + list(STOPWORDS)
# cloud = WordCloud(stopwords=STOPWORDS, width=800, height=600)
cloud = WordCloud(stopwords=my_stopword, width=800, height=600)


cloud_str = cloud.generate(mytext) #리스트를 문자열로 변환

plt.figure(figsize=(8, 6))
plt.imshow(cloud_str, interpolation='bicubic')
plt.axis('off')
plt.show()
```

    {'again', 'http', 'also', "we'll", 'k', 'she', 'hers', 'few', 'ever', 'my', 'once', 'theirs', "here's", "doesn't", 'between', "you're", "i'm", 'down', 'otherwise', 'only', 'were', 'most', 'was', "you'd", 'he', 'could', 'after', "when's", 'for', 'themselves', "it's", 'myself', "won't", 'then', "couldn't", 'both', "she's", 'while', 'no', 'any', "you've", 'himself', 'being', 'all', 'here', 'ours', 'so', 'since', 'there', 'doing', 'not', "we're", 'they', 'this', 'having', 'had', 'is', "shan't", "what's", 'below', 'through', 'from', 'shall', 'which', 'i', 'yourselves', 'should', "we've", "let's", "why's", 'as', "isn't", 'ourselves', 'ought', 'an', 'itself', 'off', 'these', 'be', 'but', 'at', 'very', "didn't", 'do', "who's", 'have', 'herself', "i've", "how's", 'com', 'cannot', "he'll", 'r', "she'd", 'we', 'to', 'more', 'by', 'its', "i'd", "shouldn't", 'yours', "hasn't", 'before', 'other', "wouldn't", 'further', 'or', 'when', 'them', 'like', 'such', 'been', 'me', 'own', 'therefore', 'who', 'where', 'www', 'am', 'has', 'the', "they've", 'during', 'it', "he's", 'each', 'if', 'on', 'get', 'does', 'you', 'our', 'did', 'in', "we'd", 'whom', "weren't", 'your', "he'd", 'because', "can't", 'same', "there's", 'his', "mustn't", 'out', 'with', 'until', "don't", 'just', 'a', 'into', 'nor', "they'll", "that's", "haven't", 'how', "they're", 'too', 'what', 'their', 'would', 'why', "where's", 'under', 'however', 'else', 'against', 'him', 'her', "aren't", 'than', 'yourself', 'over', 'some', 'up', "they'd", 'above', "you'll", "i'll", 'about', 'that', 'can', "hadn't", "wasn't", 'hence', 'of', "she'll", 'and', 'those', 'are'}



    
![png](../assets/images/ai/sequence-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__20_1.webp)
    


### 데이터 분포


```python
fig, axe = plt.subplots(figsize = (6, 4))
print("긍정 리뷰 개수: {}".format(train_data['sentiment'].value_counts()[1]))
print("부정 리뷰 개수: {}".format(train_data['sentiment'].value_counts()[0]))
fig.set_size_inches(4, 3)
a = sns.countplot(x = 'sentiment', data = train_data, hue = "sentiment")
# a = sns.catplot(x ='sentiment', data = train_data, hue = "sentiment",
#             kind="count")
```

    긍정 리뷰 개수: 12500
    부정 리뷰 개수: 12500



    
![png](../assets/images/ai/sequence-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__22_1.webp)
    



```python
## String
str_ex1 = '텐서플로우와 머신러닝을 이용한 자연어 처리'
print(str_ex1.split(sep=' '))

## pd.Series
str_pd = pd.Series('텐서플로우와 머신러닝을 이용한 자연어 처리')
print(str_pd.str.split(' '))

A = str_pd.str.split(' ')
A[0]
```

    ['텐서플로우와', '머신러닝을', '이용한', '자연어', '처리']
    0    [텐서플로우와, 머신러닝을, 이용한, 자연어, 처리]
    dtype: object





    ['텐서플로우와', '머신러닝을', '이용한', '자연어', '처리']




```python
df = pd.DataFrame([[1, 2], [3, 4]], columns= ['A', 'B'])
print(df)
## apply + 함수
def add_one(x):
    x += 1
    return x

## Apply column
df['A'] = df['A'].apply(add_one)
print(df)
print('='*50)

## Apply dataframe
df = df.apply(add_one)
print(df)
print('='*50)

## apply + lambda
df['A'] = df['A'].apply(lambda x: x+1)
print(df)
```

       A  B
    0  1  2
    1  3  4
       A  B
    0  2  2
    1  4  4
    ==================================================
       A  B
    0  3  3
    1  5  5
    ==================================================
       A  B
    0  4  3
    1  6  5



```python
## using Pandas
train_word_counts = train_data['review'].str.split().apply(len)
# train_word_counts2
```


```python
plt.figure(figsize=(6, 4))
k = plt.hist(train_word_counts, bins=50, facecolor='r', alpha = .5, label='train')
# sns.histplot(train_word_counts) # works well

plt.title('Histogram of word count in review', fontsize=15)
# plt.yscale('log')
plt.legend()
plt.xlabel('Number of words', fontsize=10)
plt.ylabel('Number of reviews', fontsize=10)
```




    Text(0, 0.5, 'Number of reviews')




    
![png](../assets/images/ai/sequence-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_6%EC%B0%A8%EC%8B%9C__DeepRNN__26_1.webp)
    



```python
summary_token_len(train_word_counts)
```

    문장 최대길이: 2470
    문장 최소길이: 10
    문장 평균길이: 233.79
    문장 길이 표준편차: 173.73
    문장 중간길이: 174.0
    제 1 사분위 길이: 127.0
    제 3 사분위 길이: 284.0


### 특수문자, 대,소문자


```python
## 의문문
# sentence = "apple"
# print("a" in sentence) # True
train_data['review'].apply(lambda x: '?' in x)
```




    True




```python
qmarks = np.mean(train_data['review'].apply(lambda x: '?' in x)) # 물음표가 구두점으로 쓰임
fullstop = np.mean(train_data['review'].apply(lambda x: '.' in x)) # 마침표
capital_first = np.mean(train_data['review'].apply(lambda x: x[0].isupper())) #  첫번째 대문자
capitals = np.mean(train_data['review'].apply(lambda x: max([y.isupper() for y in x]))) # 대문자가 몇개
numbers = np.mean(train_data['review'].apply(lambda x: max([y.isdigit() for y in x]))) # 숫자가 몇개)

print('물음표가있는 질문: {:.2f}%'.format(qmarks * 100))
print('마침표가 있는 질문: {:.2f}%'.format(fullstop * 100))
print('첫 글자가 대문자 인 질문: {:.2f}%'.format(capital_first * 100))
print('대문자가있는 질문: {:.2f}%'.format(capitals * 100))
print('숫자가있는 질문: {:.2f}%'.format(numbers * 100))
```

    물음표가있는 질문: 29.55%
    마침표가 있는 질문: 99.69%
    첫 글자가 대문자 인 질문: 0.00%
    대문자가있는 질문: 99.59%
    숫자가있는 질문: 56.66%


### HTML tag 제거


```python
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
## nltk 토큰나이징

import nltk
nltk.download("punkt")
nltk.download('stopwords')
from nltk.corpus import stopwords

import re
```

    [nltk_data] Downloading package punkt to
    [nltk_data]     C:\Users\user\AppData\Roaming\nltk_data...
    [nltk_data]   Package punkt is already up-to-date!
    [nltk_data] Downloading package stopwords to
    [nltk_data]     C:\Users\user\AppData\Roaming\nltk_data...
    [nltk_data]   Package stopwords is already up-to-date!



```python
html_text = \
'''
<p> O’er all the hilltops<br>
    Is quiet now,<br>
    In all the treetops<br>
    Hearest thou<br>
    Hardly a breath;<br>
    The birds are asleep in the trees:<br>
    Wait, soon like these<br>
    Thou too shalt rest.
</p>
'''
print('[1] html_text', html_text)

html_text_soup = BeautifulSoup(html_text, 'html').get_text()
print('[2] html_text_soup: get_text()\n',html_text_soup)
print('[3] html_text_resub\n', re.sub("[^a-zA-Z]", " ",html_text_soup))
```

    [1] html_text 
    <p> O’er all the hilltops<br>
        Is quiet now,<br>
        In all the treetops<br>
        Hearest thou<br>
        Hardly a breath;<br>
        The birds are asleep in the trees:<br>
        Wait, soon like these<br>
        Thou too shalt rest.
    </p>
    
    [2] html_text_soup: get_text()
     
     O’er all the hilltops
        Is quiet now,
        In all the treetops
        Hearest thou
        Hardly a breath;
        The birds are asleep in the trees:
        Wait, soon like these
        Thou too shalt rest.
    
    
    [3] html_text_resub
       O er all the hilltops     Is quiet now      In all the treetops     Hearest thou     Hardly a breath      The birds are asleep in the trees      Wait  soon like these     Thou too shalt rest   



```python
review = train_data['review'][0] # 리뷰 중 하나를 가져온다.
review_soup = BeautifulSoup(review).get_text() # HTML 태그 제거
# review_text = BeautifulSoup(review, "html").get_text() # HTML 태그 제거

review_text = re.sub("[^a-zA-Z]", " ", review_soup) # 영어 문자를 제외한 나머지는 모두 공백으로 바꾼다.

print('review:'.ljust(15), review) # <br /><br />Bottom line
print('review_soup:'.ljust(15), review_soup) # (which i think is most people).
print('review_text:'.ljust(15), review_text) # which i think is most people
```

    review:         "With all this stuff going down at the moment with MJ i've started listening to his music, watching the odd documentary here and there, watched The Wiz and watched Moonwalker again. Maybe i just want to get a certain insight into this guy who i thought was really cool in the eighties just to maybe make up my mind whether he is guilty or innocent. Moonwalker is part biography, part feature film which i remember going to see at the cinema when it was originally released. Some of it has subtle messages about MJ's feeling towards the press and also the obvious message of drugs are bad m'kay.<br /><br />Visually impressive but of course this is all about Michael Jackson so unless you remotely like MJ in anyway then you are going to hate this and find it boring. Some may call MJ an egotist for consenting to the making of this movie BUT MJ and most of his fans would say that he made it for the fans which if true is really nice of him.<br /><br />The actual feature film bit when it finally starts is only on for 20 minutes or so excluding the Smooth Criminal sequence and Joe Pesci is convincing as a psychopathic all powerful drug lord. Why he wants MJ dead so bad is beyond me. Because MJ overheard his plans? Nah, Joe Pesci's character ranted that he wanted people to know it is he who is supplying drugs etc so i dunno, maybe he just hates MJ's music.<br /><br />Lots of cool things in this like MJ turning into a car and a robot and the whole Speed Demon sequence. Also, the director must have had the patience of a saint when it came to filming the kiddy Bad sequence as usually directors hate working with one kid let alone a whole bunch of them performing a complex dance scene.<br /><br />Bottom line, this movie is for people who like MJ on one level or another (which i think is most people). If not, then stay away. It does try and give off a wholesome message and ironically MJ's bestest buddy in this movie is a girl! Michael Jackson is truly one of the most talented people ever to grace this planet but is he guilty? Well, with all the attention i've gave this subject....hmmm well i don't know because people can be different behind closed doors, i know this for a fact. He is either an extremely nice but stupid guy or one of the most sickest liars. I hope he is not the latter."
    review_soup:    "With all this stuff going down at the moment with MJ i've started listening to his music, watching the odd documentary here and there, watched The Wiz and watched Moonwalker again. Maybe i just want to get a certain insight into this guy who i thought was really cool in the eighties just to maybe make up my mind whether he is guilty or innocent. Moonwalker is part biography, part feature film which i remember going to see at the cinema when it was originally released. Some of it has subtle messages about MJ's feeling towards the press and also the obvious message of drugs are bad m'kay.Visually impressive but of course this is all about Michael Jackson so unless you remotely like MJ in anyway then you are going to hate this and find it boring. Some may call MJ an egotist for consenting to the making of this movie BUT MJ and most of his fans would say that he made it for the fans which if true is really nice of him.The actual feature film bit when it finally starts is only on for 20 minutes or so excluding the Smooth Criminal sequence and Joe Pesci is convincing as a psychopathic all powerful drug lord. Why he wants MJ dead so bad is beyond me. Because MJ overheard his plans? Nah, Joe Pesci's character ranted that he wanted people to know it is he who is supplying drugs etc so i dunno, maybe he just hates MJ's music.Lots of cool things in this like MJ turning into a car and a robot and the whole Speed Demon sequence. Also, the director must have had the patience of a saint when it came to filming the kiddy Bad sequence as usually directors hate working with one kid let alone a whole bunch of them performing a complex dance scene.Bottom line, this movie is for people who like MJ on one level or another (which i think is most people). If not, then stay away. It does try and give off a wholesome message and ironically MJ's bestest buddy in this movie is a girl! Michael Jackson is truly one of the most talented people ever to grace this planet but is he guilty? Well, with all the attention i've gave this subject....hmmm well i don't know because people can be different behind closed doors, i know this for a fact. He is either an extremely nice but stupid guy or one of the most sickest liars. I hope he is not the latter."
    review_text:     With all this stuff going down at the moment with MJ i ve started listening to his music  watching the odd documentary here and there  watched The Wiz and watched Moonwalker again  Maybe i just want to get a certain insight into this guy who i thought was really cool in the eighties just to maybe make up my mind whether he is guilty or innocent  Moonwalker is part biography  part feature film which i remember going to see at the cinema when it was originally released  Some of it has subtle messages about MJ s feeling towards the press and also the obvious message of drugs are bad m kay Visually impressive but of course this is all about Michael Jackson so unless you remotely like MJ in anyway then you are going to hate this and find it boring  Some may call MJ an egotist for consenting to the making of this movie BUT MJ and most of his fans would say that he made it for the fans which if true is really nice of him The actual feature film bit when it finally starts is only on for    minutes or so excluding the Smooth Criminal sequence and Joe Pesci is convincing as a psychopathic all powerful drug lord  Why he wants MJ dead so bad is beyond me  Because MJ overheard his plans  Nah  Joe Pesci s character ranted that he wanted people to know it is he who is supplying drugs etc so i dunno  maybe he just hates MJ s music Lots of cool things in this like MJ turning into a car and a robot and the whole Speed Demon sequence  Also  the director must have had the patience of a saint when it came to filming the kiddy Bad sequence as usually directors hate working with one kid let alone a whole bunch of them performing a complex dance scene Bottom line  this movie is for people who like MJ on one level or another  which i think is most people   If not  then stay away  It does try and give off a wholesome message and ironically MJ s bestest buddy in this movie is a girl  Michael Jackson is truly one of the most talented people ever to grace this planet but is he guilty  Well  with all the attention i ve gave this subject    hmmm well i don t know because people can be different behind closed doors  i know this for a fact  He is either an extremely nice but stupid guy or one of the most sickest liars  I hope he is not the latter  



```python
stopwords.words('english') # No korean data
stop_words = set(stopwords.words('english')) # 영어 불용어들의 set을 만든다.

review_text = review_text.lower()
# A.split = None (the default value) means split according to any whitespace,
splitted_words = review_text.split() # 소문자 변환 후 단어마다 나눠서 단어 리스트로 만든다.
# print(len(splitted_words)) # 437
words = [w for w in splitted_words if w not in stop_words] # 불용어 제거한 리스트를 만든다
# print(len(words)) # 219
```


```python
print(review_text)
print(words)
```

     with all this stuff going down at the moment with mj i ve started listening to his music  watching the odd documentary here and there  watched the wiz and watched moonwalker again  maybe i just want to get a certain insight into this guy who i thought was really cool in the eighties just to maybe make up my mind whether he is guilty or innocent  moonwalker is part biography  part feature film which i remember going to see at the cinema when it was originally released  some of it has subtle messages about mj s feeling towards the press and also the obvious message of drugs are bad m kay visually impressive but of course this is all about michael jackson so unless you remotely like mj in anyway then you are going to hate this and find it boring  some may call mj an egotist for consenting to the making of this movie but mj and most of his fans would say that he made it for the fans which if true is really nice of him the actual feature film bit when it finally starts is only on for    minutes or so excluding the smooth criminal sequence and joe pesci is convincing as a psychopathic all powerful drug lord  why he wants mj dead so bad is beyond me  because mj overheard his plans  nah  joe pesci s character ranted that he wanted people to know it is he who is supplying drugs etc so i dunno  maybe he just hates mj s music lots of cool things in this like mj turning into a car and a robot and the whole speed demon sequence  also  the director must have had the patience of a saint when it came to filming the kiddy bad sequence as usually directors hate working with one kid let alone a whole bunch of them performing a complex dance scene bottom line  this movie is for people who like mj on one level or another  which i think is most people   if not  then stay away  it does try and give off a wholesome message and ironically mj s bestest buddy in this movie is a girl  michael jackson is truly one of the most talented people ever to grace this planet but is he guilty  well  with all the attention i ve gave this subject    hmmm well i don t know because people can be different behind closed doors  i know this for a fact  he is either an extremely nice but stupid guy or one of the most sickest liars  i hope he is not the latter  
    ['stuff', 'going', 'moment', 'mj', 'started', 'listening', 'music', 'watching', 'odd', 'documentary', 'watched', 'wiz', 'watched', 'moonwalker', 'maybe', 'want', 'get', 'certain', 'insight', 'guy', 'thought', 'really', 'cool', 'eighties', 'maybe', 'make', 'mind', 'whether', 'guilty', 'innocent', 'moonwalker', 'part', 'biography', 'part', 'feature', 'film', 'remember', 'going', 'see', 'cinema', 'originally', 'released', 'subtle', 'messages', 'mj', 'feeling', 'towards', 'press', 'also', 'obvious', 'message', 'drugs', 'bad', 'kay', 'visually', 'impressive', 'course', 'michael', 'jackson', 'unless', 'remotely', 'like', 'mj', 'anyway', 'going', 'hate', 'find', 'boring', 'may', 'call', 'mj', 'egotist', 'consenting', 'making', 'movie', 'mj', 'fans', 'would', 'say', 'made', 'fans', 'true', 'really', 'nice', 'actual', 'feature', 'film', 'bit', 'finally', 'starts', 'minutes', 'excluding', 'smooth', 'criminal', 'sequence', 'joe', 'pesci', 'convincing', 'psychopathic', 'powerful', 'drug', 'lord', 'wants', 'mj', 'dead', 'bad', 'beyond', 'mj', 'overheard', 'plans', 'nah', 'joe', 'pesci', 'character', 'ranted', 'wanted', 'people', 'know', 'supplying', 'drugs', 'etc', 'dunno', 'maybe', 'hates', 'mj', 'music', 'lots', 'cool', 'things', 'like', 'mj', 'turning', 'car', 'robot', 'whole', 'speed', 'demon', 'sequence', 'also', 'director', 'must', 'patience', 'saint', 'came', 'filming', 'kiddy', 'bad', 'sequence', 'usually', 'directors', 'hate', 'working', 'one', 'kid', 'let', 'alone', 'whole', 'bunch', 'performing', 'complex', 'dance', 'scene', 'bottom', 'line', 'movie', 'people', 'like', 'mj', 'one', 'level', 'another', 'think', 'people', 'stay', 'away', 'try', 'give', 'wholesome', 'message', 'ironically', 'mj', 'bestest', 'buddy', 'movie', 'girl', 'michael', 'jackson', 'truly', 'one', 'talented', 'people', 'ever', 'grace', 'planet', 'guilty', 'well', 'attention', 'gave', 'subject', 'hmmm', 'well', 'know', 'people', 'different', 'behind', 'closed', 'doors', 'know', 'fact', 'either', 'extremely', 'nice', 'stupid', 'guy', 'one', 'sickest', 'liars', 'hope', 'latter']



```python
clean_review = ' '.join(words) # 단어 리스트들을 다시 하나의 글로 합친다.
print(clean_review)
```

    stuff going moment mj started listening music watching odd documentary watched wiz watched moonwalker maybe want get certain insight guy thought really cool eighties maybe make mind whether guilty innocent moonwalker part biography part feature film remember going see cinema originally released subtle messages mj feeling towards press also obvious message drugs bad kay visually impressive course michael jackson unless remotely like mj anyway going hate find boring may call mj egotist consenting making movie mj fans would say made fans true really nice actual feature film bit finally starts minutes excluding smooth criminal sequence joe pesci convincing psychopathic powerful drug lord wants mj dead bad beyond mj overheard plans nah joe pesci character ranted wanted people know supplying drugs etc dunno maybe hates mj music lots cool things like mj turning car robot whole speed demon sequence also director must patience saint came filming kiddy bad sequence usually directors hate working one kid let alone whole bunch performing complex dance scene bottom line movie people like mj one level another think people stay away try give wholesome message ironically mj bestest buddy movie girl michael jackson truly one talented people ever grace planet guilty well attention gave subject hmmm well know people different behind closed doors know fact either extremely nice stupid guy one sickest liars hope latter



```python
def preprocessing( review, remove_stopwords = False ):
    # 불용어 제거는 옵션으로 선택 가능하다.

    # 1. HTML 태그 제거
    review_text = BeautifulSoup(review).get_text()

    # 2. 영어가 아닌 특수문자들을 공백(" ")으로 바꾸기
    review_text = re.sub("[^a-zA-Z]", " ", review_text)

    # 3. 대문자들을 소문자로 바꾸고 공백단위로 텍스트들 나눠서 리스트로 만든다.
    words = review_text.lower().split()

    if remove_stopwords:
        # 4. 불용어들을 제거

        #영어에 관련된 불용어 불러오기
        stops = set(stopwords.words("english"))
        # 불용어가 아닌 단어들로 이루어진 새로운 리스트 생성
        words = [w for w in words if not w in stops]
        # 5. 단어 리스트를 공백을 넣어서 하나의 글로 합친다.
        clean_review = ' '.join(words)

    else: # 불용어 제거하지 않을 때
        clean_review = ' '.join(words)

    return clean_review
```


```python
clean_train_reviews =  reviews.apply(preprocessing, args = False)

# clean_train_reviews = []
# for review in train_data['review']:
#     clean_train_reviews.append(preprocessing(review, remove_stopwords = True))

# 전처리한 데이터 출력
clean_train_reviews[1]
```




    'the classic war of the worlds by timothy hines is a very entertaining film that obviously goes to great effort and lengths to faithfully recreate h g wells classic book mr hines succeeds in doing so i and those who watched his film with me appreciated the fact that it was not the standard predictable hollywood fare that comes out every year e g the spielberg version with tom cruise that had only the slightest resemblance to the book obviously everyone looks for different things in a movie those who envision themselves as amateur critics look only to criticize everything they can others rate a movie on more important bases like being entertained which is why most people never agree with the critics we enjoyed the effort mr hines put into being faithful to h g wells classic novel and we found it to be very entertaining this made it easy to overlook what the critics perceive to be its shortcomings'




```python
clean_train_df = pd.DataFrame({'review': clean_train_reviews, 'sentiment': train_data['sentiment']})


print(type(clean_train_df.review))
print(clean_train_df.head())

clean_train_df.to_csv('./csv/clean_train_data.csv', index = False)
```

    <class 'pandas.core.series.Series'>
                                                  review  sentiment
    0  with all this stuff going down at the moment w...          1
    1  the classic war of the worlds by timothy hines...          1
    2  the film starts with a manager nicholas bell g...          0
    3  it must be assumed that those who praised this...          0
    4  superbly trashy and wondrously unpretentious s...          1


## Text similarity를 이용한 영화 추천 시스템

### CountVectorizer


```python
## CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
```


```python
text_data = ['나는 배가 고프다',
             '내일 점심 뭐먹지',
             '내일 공부 해야겠다',
             '점심 먹고 공부 해야지']

## 영어

# count_vectorizer = CountVectorizer(stop_words=["the", "a", "an", "is", "not"])
# print(count_vectorizer.fit_transform(text_data).toarray())

count_vectorizer = CountVectorizer()
count_vectorizer.fit(text_data)
print(count_vectorizer.vocabulary_)
```

    {'나는': 2, '배가': 6, '고프다': 0, '내일': 3, '점심': 7, '뭐먹지': 5, '공부': 1, '해야겠다': 8, '먹고': 4, '해야지': 9}



```python
# Make Document-Term Matrix (DTM)

sentence = [text_data[0]] # ['나는 배가 고프다']
print(count_vectorizer.transform(sentence))
print(count_vectorizer.transform(sentence).toarray())
print("="*50)
print("vocabulary_: \n")
display(count_vectorizer.vocabulary_)
print("="*50)
print("Document-Term Matrix (DTM): CountVectorizer \n")
print(count_vectorizer.transform(text_data).toarray())
```

      (0, 0)	1
      (0, 2)	1
      (0, 6)	1
    [[1 0 1 0 0 0 1 0 0 0]]
    ==================================================
    vocabulary_: 
    



    {'나는': 2,
     '배가': 6,
     '고프다': 0,
     '내일': 3,
     '점심': 7,
     '뭐먹지': 5,
     '공부': 1,
     '해야겠다': 8,
     '먹고': 4,
     '해야지': 9}


    ==================================================
    Document-Term Matrix (DTM): CountVectorizer 
    
    [[1 0 1 0 0 0 1 0 0 0]
     [0 0 0 1 0 1 0 1 0 0]
     [0 1 0 1 0 0 0 0 1 0]
     [0 1 0 0 1 0 0 1 0 1]]



```python
## TfidfVectorizer
# text_data = ['나는 배가 고프다',
#              '내일 점심 뭐먹지',
#              '내일 공부 해야겠다',
#              '점심 먹고 공부 해야지']
text_data = ["먹고 싶은 사과",
             "먹고 싶은 바나나",
             "길고 노란 바나나 바나나",
             "저는 과일이 좋아요"]

tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.fit(text_data)
display(tfidf_vectorizer.vocabulary_)

print("="*50)
print("Document-Term Matrix (DTM): TfidfVectorizer \n")
text_idf_arr = tfidf_vectorizer.transform(text_data).toarray()
print(text_idf_arr)
```


    {'먹고': 3,
     '싶은': 6,
     '사과': 5,
     '바나나': 4,
     '길고': 1,
     '노란': 2,
     '저는': 7,
     '과일이': 0,
     '좋아요': 8}


    ==================================================
    Document-Term Matrix (DTM): TfidfVectorizer 
    
    [[0.         0.         0.         0.52640543 0.         0.66767854
      0.52640543 0.         0.        ]
     [0.         0.         0.         0.57735027 0.57735027 0.
      0.57735027 0.         0.        ]
     [0.         0.47212003 0.47212003 0.         0.7444497  0.
      0.         0.         0.        ]
     [0.57735027 0.         0.         0.         0.         0.
      0.         0.57735027 0.57735027]]


### 코사인 유사도를 이용한 추천 시스템


```python
data = pd.read_csv('./csv/movies_metadata.csv', low_memory=False)
data.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adult</th>
      <th>belongs_to_collection</th>
      <th>budget</th>
      <th>genres</th>
      <th>homepage</th>
      <th>id</th>
      <th>imdb_id</th>
      <th>original_language</th>
      <th>original_title</th>
      <th>overview</th>
      <th>...</th>
      <th>release_date</th>
      <th>revenue</th>
      <th>runtime</th>
      <th>spoken_languages</th>
      <th>status</th>
      <th>tagline</th>
      <th>title</th>
      <th>video</th>
      <th>vote_average</th>
      <th>vote_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>False</td>
      <td>{'id': 10194, 'name': 'Toy Story Collection', ...</td>
      <td>30000000</td>
      <td>[{'id': 16, 'name': 'Animation'}, {'id': 35, '...</td>
      <td>http://toystory.disney.com/toy-story</td>
      <td>862</td>
      <td>tt0114709</td>
      <td>en</td>
      <td>Toy Story</td>
      <td>Led by Woody, Andy's toys live happily in his ...</td>
      <td>...</td>
      <td>1995-10-30</td>
      <td>373554033.0</td>
      <td>81.0</td>
      <td>[{'iso_639_1': 'en', 'name': 'English'}]</td>
      <td>Released</td>
      <td>NaN</td>
      <td>Toy Story</td>
      <td>False</td>
      <td>7.7</td>
      <td>5415.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>False</td>
      <td>NaN</td>
      <td>65000000</td>
      <td>[{'id': 12, 'name': 'Adventure'}, {'id': 14, '...</td>
      <td>NaN</td>
      <td>8844</td>
      <td>tt0113497</td>
      <td>en</td>
      <td>Jumanji</td>
      <td>When siblings Judy and Peter discover an encha...</td>
      <td>...</td>
      <td>1995-12-15</td>
      <td>262797249.0</td>
      <td>104.0</td>
      <td>[{'iso_639_1': 'en', 'name': 'English'}, {'iso...</td>
      <td>Released</td>
      <td>Roll the dice and unleash the excitement!</td>
      <td>Jumanji</td>
      <td>False</td>
      <td>6.9</td>
      <td>2413.0</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 24 columns</p>
</div>




```python
# 상위 2만개의 샘플을 data에 저장
data = data.head(20000)
# overview 열에 존재하는 모든 결측값을 전부 카운트하여 출력
print('overview 열의 결측값의 수:',data['overview'].isnull().sum())
# 결측값을 빈 값으로 대체
data['overview'] = data['overview'].fillna('')
```

    overview 열의 결측값의 수: 135



```python
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['overview'])
print('TF-IDF 행렬의 크기(shape) :',tfidf_matrix.shape)
```

    TF-IDF 행렬의 크기(shape) : (20000, 47487)



```python
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print('코사인 유사도 연산 결과 :',cosine_sim.shape)
```

    코사인 유사도 연산 결과 : (20000, 20000)



```python
title_to_index = dict(zip(data['title'], data.index))

# 영화 제목 Father of the Bride Part II의 인덱스를 리턴
idx = title_to_index['Father of the Bride Part II']
print(idx)

```

    4



```python
def get_recommendations(title, cosine_sim=cosine_sim):
    # 선택한 영화의 타이틀로부터 해당 영화의 인덱스를 받아온다.
    idx = title_to_index[title]

    # 해당 영화와 모든 영화와의 유사도를 가져온다.
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 영화들을 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 영화를 받아온다.
    sim_scores = sim_scores[1:11]

    # 가장 유사한 10개의 영화의 인덱스를 얻는다.
    movie_indices = [idx[0] for idx in sim_scores]

    # 가장 유사한 10개의 영화의 제목을 리턴한다.
    return data['title'].iloc[movie_indices]

```


```python
get_recommendations('The Dark Knight Rises')
```




    12481                            The Dark Knight
    150                               Batman Forever
    1328                              Batman Returns
    15511                 Batman: Under the Red Hood
    585                                       Batman
    9230          Batman Beyond: Return of the Joker
    18035                           Batman: Year One
    19792    Batman: The Dark Knight Returns, Part 1
    3095                Batman: Mask of the Phantasm
    10122                              Batman Begins
    Name: title, dtype: object




```python
np.sqrt(4*(3**2))
```




    6.0




```python
a = np.array([1, 2, 3, 4])
b = np.array([4, 5, 6, 7])

(a*b).sum()/(np.sqrt((a*a).sum())*np.sqrt((b*b).sum()))
```




    0.9759000729485332


