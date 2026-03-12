# 객체 탐지


## 강의_3기_AI개론_15차시__Transfer_learning_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_15차시__Transfer_learning_.ipynb)

# 15장 사용자 정의 데이터를 활용한 이미지 분류

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    debconf: unable to initialize frontend: Dialog
    debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 76, <> line 4.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Processing triggers for fontconfig (2.12.6-0ubuntu2) ...
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 31 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
w = !apt install tree
print(w[-2])
```

    'apt' is not recognized as an internal or external command,


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
from torch import tensor
import torch.nn as nn
import torch.optim as optim
from torchinfo import summary
from torchviz import make_dot
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

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


### 공통 함수 불러오기


```python
# 공통 함수 다운로드
!git clone https://github.com/wikibook/pythonlibs.git

# # 공통 함수 불러오기
from pythonlibs.torch_lib1 import *


# # 공통 함수 확인
print(README)
```

    Common Library for PyTorch
    Author: M. Akaishi


## 데이터 준비

### 데이터 다운로드, 압축 해제, 트리 구조 출력


```python
# 데이터 다운로드
w = !wget -nc https://download.pytorch.org/tutorial/hymenoptera_data.zip

# 결과 확인
print(w[-2])
```

    2022-04-10 14:24:10 (46.5 MB/s) - ‘hymenoptera_data.zip’ saved [47286322/47286322]



```python
# 압축 해제
w = !unzip -o hymenoptera_data.zip

# 결과 확인
print(w[-1])
```

      inflating: hymenoptera_data/val/bees/abeja.jpg  



```python
# 트리 구조 출력
!tree hymenoptera_data
```

    Folder PATH listing for volume 드라이브D
    Volume serial number is 00000092 32BC:C9D8
    D:\ONEDRIVE\DOCUMENTS\LECTURE_2019\ACADEMY\30_SPARKX\01_AI_BASIC\15_TRANSFER_LEARNING\HYMENOPTERA_DATA
    ├───train
    │   ├───ants
    │   └───bees
    └───val
        ├───ants
        └───bees


### Transforms 정의


```python
# Transforms 정의
# 훈련 데이터 : 정규화에 반전과 RandomErasing 추가
# 입력 이미지를 주어진 크기(resize: 224×224)로 조정, scale은 원래 이미지를 임의의 크기(0.5~1.0(50~100%))만큼 면적을 무작위로 자르겠다는 의미

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p = 0.5),
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5),
    transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False)
])

# 검증 데이터 : 정규화
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5)
])


```

### 데이터셋 정의


```python
# 베이스 디렉터리
data_dir = 'hymenoptera_data'

# 훈련 데이터 디렉터리와 검증 데이터 디렉터리 지정
import os
train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'val')

# join 함수 결과 확인
print(train_dir, test_dir)

# 분류하려는 클래스의 리스트 작성
classes = ['ants', 'bees']
```

    hymenoptera_data\train hymenoptera_data\val



```python
# 데이터셋 정의

# 훈련용
train_data = datasets.ImageFolder(train_dir, 
                                  transform=train_transform)
# 훈련 데이터 이미지 출력용
train_data2 = datasets.ImageFolder(train_dir, 
                                   transform=test_transform)
# 검증용
test_data = datasets.ImageFolder(test_dir, 
                                 transform=test_transform)
```


```python
# 데이터 건수 확인

print(f'훈련 데이터 : {len(train_data)} 건')
print(f'검증 데이터 : {len(test_data)} 건')
```

    훈련 데이터 : 244 건
    검증 데이터 : 153 건



```python
# 검증 데이터　
# 처음 10개와 마지막 10개 이미지 출력

plt.figure(figsize=(15, 4))
for i in range(10):
    ax = plt.subplot(2, 10, i + 1)
    image, label = test_data[i]
    img = (np.transpose(image.numpy(), (1, 2, 0)) + 1)/2
    plt.imshow(img)
    ax.set_title(classes[label])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax = plt.subplot(2, 10, i + 11)
    image, label = test_data[-i-1]
    img = (np.transpose(image.numpy(), (1, 2, 0)) + 1)/2
    plt.imshow(img)
    ax.set_title(classes[label])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__22_0.webp)
    


### 데이터로더 정의


```python
# 데이터로더 정의

batch_size = 10

# 훈련용
train_loader = DataLoader(train_data, 
      batch_size=batch_size, shuffle=True)

# 검증용
test_loader = DataLoader(test_data, 
      batch_size=batch_size, shuffle=False)

# 이미지 출력용
train_loader2 = DataLoader(train_data2, 
      batch_size=50, shuffle=True)
test_loader2 = DataLoader(test_data, 
      batch_size=50, shuffle=True)
```

### 이미지 출력


```python
# 검증 데이터(50건)
torch_seed()
show_images_labels(test_loader2, classes, None, None)
```

    len(images) =  50



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__26_1.webp)
    


## 파인 튜닝의 경우


```python
# 파인 튜닝의 경우

# 사전 학습 모델 불러오기
# VGG-19-BN 모델을 학습이 끝난 파라미터와 함께 불러오기
# from torchvision import models
# net = models.vgg19_bn(pretrained = True)
weights = models.VGG19_BN_Weights.DEFAULT
net = models.vgg19_bn(weights = weights)
```


```python
print(net)
```

    VGG(
      (features): Sequential(
        (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (2): ReLU(inplace=True)
        (3): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (4): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (5): ReLU(inplace=True)
        (6): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (7): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (8): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (9): ReLU(inplace=True)
        (10): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (11): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (12): ReLU(inplace=True)
        (13): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (14): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (15): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (16): ReLU(inplace=True)
        (17): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (18): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (19): ReLU(inplace=True)
        (20): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (21): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (22): ReLU(inplace=True)
        (23): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (24): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (25): ReLU(inplace=True)
        (26): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (27): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (28): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (29): ReLU(inplace=True)
        (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (31): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (32): ReLU(inplace=True)
        (33): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (34): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (35): ReLU(inplace=True)
        (36): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (37): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (38): ReLU(inplace=True)
        (39): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (40): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (41): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (42): ReLU(inplace=True)
        (43): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (44): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (45): ReLU(inplace=True)
        (46): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (47): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (48): ReLU(inplace=True)
        (49): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (50): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        (51): ReLU(inplace=True)
        (52): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
      )
      (avgpool): AdaptiveAvgPool2d(output_size=(7, 7))
      (classifier): Sequential(
        (0): Linear(in_features=25088, out_features=4096, bias=True)
        (1): ReLU(inplace=True)
        (2): Dropout(p=0.5, inplace=False)
        (3): Linear(in_features=4096, out_features=4096, bias=True)
        (4): ReLU(inplace=True)
        (5): Dropout(p=0.5, inplace=False)
        (6): Linear(in_features=4096, out_features=1000, bias=True)
      )
    )



```python
summary(net, (100, 3, 224, 224))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    VGG                                      [100, 1000]               --
    ├─Sequential: 1-1                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-1                       [100, 64, 224, 224]       1,792
    │    └─BatchNorm2d: 2-2                  [100, 64, 224, 224]       128
    │    └─ReLU: 2-3                         [100, 64, 224, 224]       --
    │    └─Conv2d: 2-4                       [100, 64, 224, 224]       36,928
    │    └─BatchNorm2d: 2-5                  [100, 64, 224, 224]       128
    │    └─ReLU: 2-6                         [100, 64, 224, 224]       --
    │    └─MaxPool2d: 2-7                    [100, 64, 112, 112]       --
    │    └─Conv2d: 2-8                       [100, 128, 112, 112]      73,856
    │    └─BatchNorm2d: 2-9                  [100, 128, 112, 112]      256
    │    └─ReLU: 2-10                        [100, 128, 112, 112]      --
    │    └─Conv2d: 2-11                      [100, 128, 112, 112]      147,584
    │    └─BatchNorm2d: 2-12                 [100, 128, 112, 112]      256
    │    └─ReLU: 2-13                        [100, 128, 112, 112]      --
    │    └─MaxPool2d: 2-14                   [100, 128, 56, 56]        --
    │    └─Conv2d: 2-15                      [100, 256, 56, 56]        295,168
    │    └─BatchNorm2d: 2-16                 [100, 256, 56, 56]        512
    │    └─ReLU: 2-17                        [100, 256, 56, 56]        --
    │    └─Conv2d: 2-18                      [100, 256, 56, 56]        590,080
    │    └─BatchNorm2d: 2-19                 [100, 256, 56, 56]        512
    │    └─ReLU: 2-20                        [100, 256, 56, 56]        --
    │    └─Conv2d: 2-21                      [100, 256, 56, 56]        590,080
    │    └─BatchNorm2d: 2-22                 [100, 256, 56, 56]        512
    │    └─ReLU: 2-23                        [100, 256, 56, 56]        --
    │    └─Conv2d: 2-24                      [100, 256, 56, 56]        590,080
    │    └─BatchNorm2d: 2-25                 [100, 256, 56, 56]        512
    │    └─ReLU: 2-26                        [100, 256, 56, 56]        --
    │    └─MaxPool2d: 2-27                   [100, 256, 28, 28]        --
    │    └─Conv2d: 2-28                      [100, 512, 28, 28]        1,180,160
    │    └─BatchNorm2d: 2-29                 [100, 512, 28, 28]        1,024
    │    └─ReLU: 2-30                        [100, 512, 28, 28]        --
    │    └─Conv2d: 2-31                      [100, 512, 28, 28]        2,359,808
    │    └─BatchNorm2d: 2-32                 [100, 512, 28, 28]        1,024
    │    └─ReLU: 2-33                        [100, 512, 28, 28]        --
    │    └─Conv2d: 2-34                      [100, 512, 28, 28]        2,359,808
    │    └─BatchNorm2d: 2-35                 [100, 512, 28, 28]        1,024
    │    └─ReLU: 2-36                        [100, 512, 28, 28]        --
    │    └─Conv2d: 2-37                      [100, 512, 28, 28]        2,359,808
    │    └─BatchNorm2d: 2-38                 [100, 512, 28, 28]        1,024
    │    └─ReLU: 2-39                        [100, 512, 28, 28]        --
    │    └─MaxPool2d: 2-40                   [100, 512, 14, 14]        --
    │    └─Conv2d: 2-41                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-42                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-43                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-44                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-45                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-46                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-47                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-48                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-49                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-50                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-51                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-52                        [100, 512, 14, 14]        --
    │    └─MaxPool2d: 2-53                   [100, 512, 7, 7]          --
    ├─AdaptiveAvgPool2d: 1-2                 [100, 512, 7, 7]          --
    ├─Sequential: 1-3                        [100, 1000]               --
    │    └─Linear: 2-54                      [100, 4096]               102,764,544
    │    └─ReLU: 2-55                        [100, 4096]               --
    │    └─Dropout: 2-56                     [100, 4096]               --
    │    └─Linear: 2-57                      [100, 4096]               16,781,312
    │    └─ReLU: 2-58                        [100, 4096]               --
    │    └─Dropout: 2-59                     [100, 4096]               --
    │    └─Linear: 2-60                      [100, 1000]               4,097,000
    ==========================================================================================
    Total params: 143,678,248
    Trainable params: 143,678,248
    Non-trainable params: 0
    Total mult-adds (T): 1.96
    ==========================================================================================
    Input size (MB): 60.21
    Forward/backward pass size (MB): 23770.71
    Params size (MB): 574.71
    Estimated Total Size (MB): 24405.63
    ==========================================================================================




```python

# 난수 고정
torch_seed()

# 최종 노드의 출력을 2로 변경
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, 2)

# AdaptiveAvgPool2d 함수 제거
net.avgpool = nn.Identity()

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(),lr=lr,momentum=0.9)

# history 파일도 동시에 초기화
history = np.zeros((0, 5))
```


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
          train_loader, test_loader, device, history)
```


      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.42943 acc: 0.78000 val_loss: 0.10684, val_acc: 0.96250



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.18828 acc: 0.92000 val_loss: 0.11837, val_acc: 0.96875



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.21427 acc: 0.91200 val_loss: 0.10815, val_acc: 0.96250



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.14176 acc: 0.93600 val_loss: 0.17399, val_acc: 0.95000



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.16827 acc: 0.91400 val_loss: 0.10927, val_acc: 0.96875



```python
# 결과 확인
evaluate_history(history)
```

    초기상태 : 손실 : 0.10684  정확도 : 0.96250
    최종상태 : 손실 : 0.10927 정확도 : 0.96875



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__33_1.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__33_2.webp)
    



```python
# 난수 고정
torch_seed()

# 검증 데이터 결과 출력
show_images_labels(test_loader2, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__34_1.webp)
    



## 전이 학습의 경우


```python
# VGG-19-BN 모델을 학습이 끝난 파라미터와 함께 불러오기
# from torchvision import models
# net = models.vgg19_bn(pretrained = True)
weights = models.VGG19_BN_Weights.DEFAULT
net = models.vgg19_bn(weights = weights)

# 모든 파라미터의 경사 계산을 OFF로 설정
for param in net.parameters():
    param.requires_grad = False

# 난수 고정
torch_seed()

# 최종 노드의 출력을 2로 변경
# 이 노드에 대해서만 경사 계산을 수행하게 됨
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, 2)

# AdaptiveAvgPool2d 함수 제거
net.avgpool = nn.Identity()

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수로 교차 엔트로피 사용
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
# 파라미터 수정 대상을 최종 노드로 제한
optimizer = optim.SGD(net.classifier[6].parameters(),lr=lr,momentum=0.9)

# history 파일도 동시에 초기화
history = np.zeros((0, 5))
```


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
          train_loader, test_loader, device, history)
```


      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.45079 acc: 0.77600 val_loss: 0.13135, val_acc: 0.96250



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.22003 acc: 0.92000 val_loss: 0.12127, val_acc: 0.96250



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.23990 acc: 0.90400 val_loss: 0.11304, val_acc: 0.95625



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.19803 acc: 0.90400 val_loss: 0.12182, val_acc: 0.95625



      0%|          | 0/25 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.20835 acc: 0.88600 val_loss: 0.11390, val_acc: 0.96250



```python
# 결과 확인
evaluate_history(history)
```

    초기상태 : 손실 : 0.13135  정확도 : 0.96250
    최종상태 : 손실 : 0.11390 정확도 : 0.96250



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__38_1.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__38_2.webp)
    



```python
# 난수 고정
torch_seed()

# 검증 데이터 결과 출력
show_images_labels(test_loader2, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__39_1.webp)
    


## 사용자 정의 데이터를 사용하는 경우
시베리안 허스키와 늑대 이미지를 사용함

### 데이터 다운로드, 압축 해제


```python
# 데이터 다운로드
w = !wget https://github.com/makaishi2/pythonlibs/raw/main/images/dog_wolf.zip
print(w[-2])

# 압축 해제
!unzip dog_wolf.zip | tail -n 1

# 트리 구조 확인
!tree dog_wolf
```

    2022-04-10 14:43:13 (142 MB/s) - ‘dog_wolf.zip’ saved [21811374/21811374]
      inflating: dog_wolf/train/wolf/wolf-09.png  
    dog_wolf
    ├── test
    │   ├── dog
    │   │   ├── dog-21.png
    │   │   ├── dog-22.png
    │   │   ├── dog-23.png
    │   │   ├── dog-24.png
    │   │   └── dog-25.png
    │   └── wolf
    │       ├── wolf-21.png
    │       ├── wolf-22.png
    │       ├── wolf-23.png
    │       ├── wolf-24.png
    │       └── wolf-25.png
    └── train
        ├── dog
        │   ├── dog-01.png
        │   ├── dog-02.png
        │   ├── dog-03.png
        │   ├── dog-04.png
        │   ├── dog-05.png
        │   ├── dog-06.png
        │   ├── dog-07.png
        │   ├── dog-08.png
        │   ├── dog-09.png
        │   ├── dog-10.png
        │   ├── dog-11.png
        │   ├── dog-12.png
        │   ├── dog-13.png
        │   ├── dog-14.png
        │   ├── dog-15.png
        │   ├── dog-16.png
        │   ├── dog-17.png
        │   ├── dog-18.png
        │   ├── dog-19.png
        │   └── dog-20.png
        └── wolf
            ├── wolf-01.png
            ├── wolf-02.png
            ├── wolf-03.png
            ├── wolf-04.png
            ├── wolf-05.png
            ├── wolf-06.png
            ├── wolf-07.png
            ├── wolf-08.png
            ├── wolf-09.png
            ├── wolf-10.png
            ├── wolf-11.png
            ├── wolf-12.png
            ├── wolf-13.png
            ├── wolf-14.png
            ├── wolf-15.png
            ├── wolf-16.png
            ├── wolf-17.png
            ├── wolf-18.png
            ├── wolf-19.png
            └── wolf-20.png
    
    6 directories, 50 files


### Transforms 정의


```python
# Transforms 정의

# 검증 데이터 : 정규화
test_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5)
])

# 훈련 데이터 : 정규화에 반전과 RandomErasing 추가
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5), 
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5),
    transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False)   
])
```

### 데이터셋 정의


```python
# 데이터셋 정의

data_dir = 'dog_wolf'

import os
train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'test')

classes = ['dog', 'wolf']

train_data = datasets.ImageFolder(train_dir, 
            transform=train_transform)
train_data2 = datasets.ImageFolder(train_dir, 
            transform=test_transform)
test_data = datasets.ImageFolder(test_dir, 
            transform=test_transform)
```


```python
# 데이터 건수 확인

print(f'학습 데이터 : {len(train_data)} 건')
print(f'검증 데이터 : {len(test_data)} 건')
```

    학습 데이터 : 40 건
    검증 데이터 : 10 건


### 데이터로더 정의


```python
# 데이터로더 정의

batch_size = 5
# 훈련 데이터
train_loader = DataLoader(train_data, 
            batch_size=batch_size, shuffle=True)
# 훈련 데이터, 이미지 출력용
train_loader2 = DataLoader(train_data2, 
            batch_size=40, shuffle=False)
# 검증 데이터
test_loader = DataLoader(test_data, 
            batch_size=batch_size, shuffle=False)
# 검증데이터, 이미지 출력용
test_loader2 = DataLoader(test_data, 
            batch_size=10, shuffle=True)
```

### 이미지 출력


```python
# 훈련 데이터(40건)
show_images_labels(train_loader2, classes, None, None)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__51_0.webp)
    



```python
# 검증 데이터(10건)
torch_seed()
show_images_labels(test_loader2, classes, None, None)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__52_0.webp)
    


### 모델 정의


```python
# 사전 학습 모델 불러오기
net = models.vgg19_bn(pretrained = True)

for param in net.parameters():
    param.requires_grad = False

# 난수 고정
torch_seed()

# 마지막 노드 출력을 2로 변경
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, 2)

# AdaptiveAvgPool2d 함수 제거
net.avgpool = nn.Identity()

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
# 파라미터 수정 대상을 최종 노드로 제한
optimizer = optim.SGD(net.classifier[6].parameters(),lr=lr,momentum=0.9)

# history 파일도 동시에 초기화
history = np.zeros((0, 5))
```


```python
# 학습
num_epochs = 10
history = fit(net, optimizer, criterion, num_epochs, 
          train_loader, test_loader, device, history)
```


      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [1/10], loss: 0.12345 acc: 0.65000 val_loss: 0.07783, val_acc: 1.00000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [2/10], loss: 0.07584 acc: 0.85000 val_loss: 0.04895, val_acc: 0.90000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [3/10], loss: 0.03976 acc: 0.92500 val_loss: 0.05762, val_acc: 0.80000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [4/10], loss: 0.04213 acc: 0.92500 val_loss: 0.03992, val_acc: 1.00000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [5/10], loss: 0.01836 acc: 0.97500 val_loss: 0.02970, val_acc: 1.00000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [6/10], loss: 0.02144 acc: 0.97500 val_loss: 0.04182, val_acc: 0.90000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [7/10], loss: 0.03019 acc: 0.95000 val_loss: 0.03631, val_acc: 0.90000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [8/10], loss: 0.04319 acc: 0.92500 val_loss: 0.03186, val_acc: 1.00000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [9/10], loss: 0.01086 acc: 1.00000 val_loss: 0.02766, val_acc: 1.00000



      0%|          | 0/8 [00:00<?, ?it/s]


    Epoch [10/10], loss: 0.04419 acc: 0.92500 val_loss: 0.03189, val_acc: 1.00000



```python
# 결과 확인
evaluate_history(history)
```

    초기상태 : 손실 : 0.07783  정확도 : 1.00000
    최종상태 : 손실 : 0.03189 정확도 : 1.00000



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__56_1.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__56_2.webp)
    



```python
# 예측 결과 출력
torch_seed()
show_images_labels(test_loader2, classes, net, device)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_15%EC%B0%A8%EC%8B%9C__Transfer_learning__57_0.webp)
    



## 강의_3기_AI개론_16차시__model_from_scratch_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_16차시__model_from_scratch_.ipynb)

# 16장 Model Build from Scratch

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```

    debconf: unable to initialize frontend: Dialog
    debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 76, <> line 4.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Processing triggers for fontconfig (2.12.6-0ubuntu2) ...
    /usr/share/fonts: caching, new cache contents: 0 fonts, 1 dirs
    /usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 3 dirs
    /usr/share/fonts/truetype/humor-sans: caching, new cache contents: 1 fonts, 0 dirs
    /usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
    /usr/share/fonts/truetype/nanum: caching, new cache contents: 31 fonts, 0 dirs
    /usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
    /root/.local/share/fonts: skipping, no such directory
    /root/.fonts: skipping, no such directory
    /var/cache/fontconfig: cleaning cache directory
    /root/.cache/fontconfig: not cleaning non-existent cache directory
    /root/.fontconfig: not cleaning non-existent cache directory
    fc-cache: succeeded



```python
# 필요 라이브러리 설치

!pip install torchviz | tail -n 1
!pip install torchinfo | tail -n 1
w = !apt install tree
print(w[-2])
```

    'apt' is not recognized as an internal or external command,


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
from torchinfo import summary
from torchviz import make_dot
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

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


### 공통 함수 불러오기


```python
# 공통 함수 다운로드
!git clone https://github.com/wikibook/pythonlibs.git

# # 공통 함수 불러오기
from pythonlibs.torch_lib1 import *


# # 공통 함수 확인
print(README)
```

    Common Library for PyTorch
    Author: M. Akaishi


## 데이터 준비


```python
# 분류 클래스명 정의

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 분류 클래스 수는 10
n_output = len(classes)
```


```python
# Transforms 정의

# 학습 데이터용 : 정규화에 반전과 RandomErasing 추가
transform_train = transforms.Compose([
  transforms.Resize(112),
  transforms.RandomHorizontalFlip(p=0.5),
  transforms.RandomRotation(20),
  transforms.ToTensor(),
  transforms.Normalize(0.5, 0.5), 
])

# 검증 데이터용 : 정규화만 실시
transform = transforms.Compose([
  transforms.Resize(112),
  transforms.ToTensor(),
  transforms.Normalize(0.5, 0.5)
])
```


```python
# 데이터 취득용 함수 dataset
data_root = './data'

train_set = datasets.CIFAR10(
    root = data_root, 
    train = True,
    download = True, 
    transform = transform_train)

# 검증 데이터셋
test_set = datasets.CIFAR10(
    root = data_root, 
    train = False, 
    download = True, 
    transform = transform)
```

    Files already downloaded and verified
    Files already downloaded and verified



```python
# 배치 사이즈 지정
batch_size = 50

# 데이터로더

# 훈련용 데이터로더
# 훈련용이므로 셔플을 True로 설정함
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)

# 검증용 데이터로더
# 검증용은 셔플이 필요하지 않음
test_loader = DataLoader(test_set,  batch_size=batch_size, shuffle=False) 
```

## 모델 만들기

## BasicBlock


```python
import torch.nn as nn
from typing import Optional

class BasicBlock(nn.Module):
    expansion = 1  # Output channels are the same as input channels
    
    def __init__(self, inplanes: int, planes: int, stride: int = 1,
                 downsample: Optional[nn.Module] = None, groups: int = 1,
                 dilation: int = 1, norm_layer: Optional[nn.Module] = None):
        super().__init__()
        
        # Normalization layer (default to BatchNorm2d if not specified)
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d

        # First convolutional layer (3x3 conv, stride is applied)
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride,
                               padding=dilation, groups=groups, bias=False, dilation=dilation)
        self.bn1 = norm_layer(planes)  # BatchNorm2d after the first convolution
        self.relu = nn.ReLU(inplace=True)  # ReLU activation function

        # Second convolutional layer (3x3 conv, no stride)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1,
                               padding=dilation, groups=groups, bias=False, dilation=dilation)
        self.bn2 = norm_layer(planes)  # BatchNorm2d after the second convolution

        # Optional downsample layer (to adjust dimensions of input and output if necessary)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x  # Store the input for the residual connection

        # Apply the first convolutional layer followed by BatchNorm and ReLU
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        # Apply the second convolutional layer followed by BatchNorm
        out = self.conv2(out)
        out = self.bn2(out)

        # If downsampling is needed (i.e., the dimensions don't match), apply the downsample layer
        if self.downsample is not None:
            identity = self.downsample(x)

        # Add the residual (skip connection)
        out += identity
        out = self.relu(out)  # Apply ReLU activation after adding the residual

        return out

```

## Bottleneck


```python
import torch.nn as nn
from typing import Optional

class Bottleneck(nn.Module):
    expansion = 4  # Output channel expansion factor

    def __init__(self, inplanes: int, planes: int, stride: int = 1,
                 downsample: Optional[nn.Module] = None, groups: int = 1, 
                 base_width: int = 64, dilation: int = 1,
                 norm_layer: Optional[nn.Module] = None):
        super().__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d

        # Width for the 1x1 and 3x3 convolutions
        width = int(planes * (base_width / 64.)) * groups

        # 1x1 Convolution (Reduce dimensions)
        self.conv1 = nn.Conv2d(inplanes, width, kernel_size=1, stride=1, bias=False)
        self.bn1 = norm_layer(width)

        # 3x3 Convolution (Main computation)
        self.conv2 = nn.Conv2d(width, width, kernel_size=3, stride=stride, padding=dilation,
                               groups=groups, dilation=dilation, bias=False)
        self.bn2 = norm_layer(width)

        # 1x1 Convolution (Expand dimensions)
        self.conv3 = nn.Conv2d(width, planes * self.expansion, kernel_size=1, stride=1, bias=False)
        self.bn3 = norm_layer(planes * self.expansion)

        # Downsample layer for residual connection
        self.downsample = downsample
        self.stride = stride
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        identity = x

        # First layer: 1x1 Convolution
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        # Second layer: 3x3 Convolution
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        # Third layer: 1x1 Convolution
        out = self.conv3(out)
        out = self.bn3(out)

        # Residual connection
        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

```

# ResNet18 from scratch


```python
import torch
import torch.nn as nn
from typing import Type, List, Optional
# Type[nn.Module] =  BasicBlock (nn.Module을 상속한 클래스)
# Optional[nn.Module] = nn.Linear(...) 또는 None (nn.Module 인스턴스 또는 None)

# BasicBlock for ResNet18
class BasicBlock(nn.Module):
    expansion = 1  # Number of output channels will be same as input channels
    
    def __init__(self, inplanes: int, planes: int, stride: int = 1,
                 downsample: Optional[nn.Module] = None, groups: int = 1,
                 dilation: int = 1, norm_layer: Optional[nn.Module] = None):
        super().__init__()
        
        # Default normalization layer is BatchNorm2d
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d

        # First Convolution Layer
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride,
                               padding=dilation, groups=groups, bias=False, dilation=dilation)
        self.bn1 = norm_layer(planes)
        self.relu = nn.ReLU(inplace=True)

        # Second Convolution Layer
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1,
                               padding=dilation, groups=groups, bias=False, dilation=dilation)
        self.bn2 = norm_layer(planes)

        # Downsample layer for matching dimensions
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x  # Store the input for the skip connection

        # Apply first convolution and batch normalization
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        # Apply second convolution and batch normalization
        out = self.conv2(out)
        out = self.bn2(out)

        # If downsampling is required, apply it to the identity
        if self.downsample is not None:
            identity = self.downsample(x)

        # Add the residual (skip connection)
        out += identity
        out = self.relu(out)  # Final ReLU activation

        return out

# ResNet18 Model
class ResNet18(nn.Module):
    def __init__(self, block: Type[nn.Module], layers: List[int], num_classes: int = 1000,
                 groups: int = 1, width_per_group: int = 64, 
                 norm_layer: Optional[nn.Module] = None):
        super().__init__()

        # Default normalization layer is BatchNorm2d
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self._norm_layer = norm_layer

        # Initialize parameters
        self.inplanes = 64
        self.dilation = 1
        self.groups = groups
        self.base_width = width_per_group

        # Initial Convolution Layer (7x7 Conv)
        self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = norm_layer(self.inplanes)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # ResNet layers (consists of blocks of BasicBlock)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)

        # Fully connected layer
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        # Initialize parameters
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def _make_layer(self, block: Type[nn.Module], planes: int, blocks: int, stride: int = 1) -> nn.Sequential:
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion, kernel_size=1, stride=stride, bias=False),
                self._norm_layer(planes * block.expansion),
            )

        layers = [block(self.inplanes, planes, stride, downsample, groups=self.groups, 
                        dilation=self.dilation, norm_layer=self._norm_layer)]
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes, stride=1, downsample=None, groups=self.groups, 
                                dilation=self.dilation, norm_layer=self._norm_layer))

        return nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Initial layers
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        # Apply ResNet layers (BasicBlock residual layers)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        # Pooling and fully connected layer
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

# Function to instantiate the ResNet18 model
def resnet18(num_classes: int = 1000, norm_layer: Optional[nn.Module] = None) -> ResNet18:
    """Constructs a ResNet-18 model."""
    return ResNet18(
        block=BasicBlock,  # Use the BasicBlock for ResNet-18
        layers=[2, 2, 2, 2],  # ResNet-18 has 2 blocks per stage
        num_classes=num_classes,
        norm_layer=norm_layer
    )

# Example usage
net = resnet18(num_classes=10)  # Example for 10 classes (e.g., CIFAR-10)

```


```python
print(net)
```

    ResNet18(
      (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
      (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (relu): ReLU(inplace=True)
      (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
      (layer1): Sequential(
        (0): BasicBlock(
          (conv1): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (1): BasicBlock(
          (conv1): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (layer2): Sequential(
        (0): BasicBlock(
          (conv1): Conv2d(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (downsample): Sequential(
            (0): Conv2d(64, 128, kernel_size=(1, 1), stride=(2, 2), bias=False)
            (1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (1): BasicBlock(
          (conv1): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (layer3): Sequential(
        (0): BasicBlock(
          (conv1): Conv2d(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (downsample): Sequential(
            (0): Conv2d(128, 256, kernel_size=(1, 1), stride=(2, 2), bias=False)
            (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (1): BasicBlock(
          (conv1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (layer4): Sequential(
        (0): BasicBlock(
          (conv1): Conv2d(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (downsample): Sequential(
            (0): Conv2d(256, 512, kernel_size=(1, 1), stride=(2, 2), bias=False)
            (1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (1): BasicBlock(
          (conv1): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn1): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          (relu): ReLU(inplace=True)
          (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
          (bn2): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
      (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
      (fc): Linear(in_features=512, out_features=10, bias=True)
    )



```python
net = net.to(device)
summary(net,(100, 3, 112, 112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    ResNet18                                 [100, 10]                 --
    ├─Conv2d: 1-1                            [100, 64, 56, 56]         9,408
    ├─BatchNorm2d: 1-2                       [100, 64, 56, 56]         128
    ├─ReLU: 1-3                              [100, 64, 56, 56]         --
    ├─MaxPool2d: 1-4                         [100, 64, 28, 28]         --
    ├─Sequential: 1-5                        [100, 64, 28, 28]         --
    │    └─BasicBlock: 2-1                   [100, 64, 28, 28]         --
    │    │    └─Conv2d: 3-1                  [100, 64, 28, 28]         36,864
    │    │    └─BatchNorm2d: 3-2             [100, 64, 28, 28]         128
    │    │    └─ReLU: 3-3                    [100, 64, 28, 28]         --
    │    │    └─Conv2d: 3-4                  [100, 64, 28, 28]         36,864
    │    │    └─BatchNorm2d: 3-5             [100, 64, 28, 28]         128
    │    │    └─ReLU: 3-6                    [100, 64, 28, 28]         --
    │    └─BasicBlock: 2-2                   [100, 64, 28, 28]         --
    │    │    └─Conv2d: 3-7                  [100, 64, 28, 28]         36,864
    │    │    └─BatchNorm2d: 3-8             [100, 64, 28, 28]         128
    │    │    └─ReLU: 3-9                    [100, 64, 28, 28]         --
    │    │    └─Conv2d: 3-10                 [100, 64, 28, 28]         36,864
    │    │    └─BatchNorm2d: 3-11            [100, 64, 28, 28]         128
    │    │    └─ReLU: 3-12                   [100, 64, 28, 28]         --
    ├─Sequential: 1-6                        [100, 128, 14, 14]        --
    │    └─BasicBlock: 2-3                   [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-13                 [100, 128, 14, 14]        73,728
    │    │    └─BatchNorm2d: 3-14            [100, 128, 14, 14]        256
    │    │    └─ReLU: 3-15                   [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-16                 [100, 128, 14, 14]        147,456
    │    │    └─BatchNorm2d: 3-17            [100, 128, 14, 14]        256
    │    │    └─Sequential: 3-18             [100, 128, 14, 14]        8,448
    │    │    └─ReLU: 3-19                   [100, 128, 14, 14]        --
    │    └─BasicBlock: 2-4                   [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-20                 [100, 128, 14, 14]        147,456
    │    │    └─BatchNorm2d: 3-21            [100, 128, 14, 14]        256
    │    │    └─ReLU: 3-22                   [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-23                 [100, 128, 14, 14]        147,456
    │    │    └─BatchNorm2d: 3-24            [100, 128, 14, 14]        256
    │    │    └─ReLU: 3-25                   [100, 128, 14, 14]        --
    ├─Sequential: 1-7                        [100, 256, 7, 7]          --
    │    └─BasicBlock: 2-5                   [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-26                 [100, 256, 7, 7]          294,912
    │    │    └─BatchNorm2d: 3-27            [100, 256, 7, 7]          512
    │    │    └─ReLU: 3-28                   [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-29                 [100, 256, 7, 7]          589,824
    │    │    └─BatchNorm2d: 3-30            [100, 256, 7, 7]          512
    │    │    └─Sequential: 3-31             [100, 256, 7, 7]          33,280
    │    │    └─ReLU: 3-32                   [100, 256, 7, 7]          --
    │    └─BasicBlock: 2-6                   [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-33                 [100, 256, 7, 7]          589,824
    │    │    └─BatchNorm2d: 3-34            [100, 256, 7, 7]          512
    │    │    └─ReLU: 3-35                   [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-36                 [100, 256, 7, 7]          589,824
    │    │    └─BatchNorm2d: 3-37            [100, 256, 7, 7]          512
    │    │    └─ReLU: 3-38                   [100, 256, 7, 7]          --
    ├─Sequential: 1-8                        [100, 512, 4, 4]          --
    │    └─BasicBlock: 2-7                   [100, 512, 4, 4]          --
    │    │    └─Conv2d: 3-39                 [100, 512, 4, 4]          1,179,648
    │    │    └─BatchNorm2d: 3-40            [100, 512, 4, 4]          1,024
    │    │    └─ReLU: 3-41                   [100, 512, 4, 4]          --
    │    │    └─Conv2d: 3-42                 [100, 512, 4, 4]          2,359,296
    │    │    └─BatchNorm2d: 3-43            [100, 512, 4, 4]          1,024
    │    │    └─Sequential: 3-44             [100, 512, 4, 4]          132,096
    │    │    └─ReLU: 3-45                   [100, 512, 4, 4]          --
    │    └─BasicBlock: 2-8                   [100, 512, 4, 4]          --
    │    │    └─Conv2d: 3-46                 [100, 512, 4, 4]          2,359,296
    │    │    └─BatchNorm2d: 3-47            [100, 512, 4, 4]          1,024
    │    │    └─ReLU: 3-48                   [100, 512, 4, 4]          --
    │    │    └─Conv2d: 3-49                 [100, 512, 4, 4]          2,359,296
    │    │    └─BatchNorm2d: 3-50            [100, 512, 4, 4]          1,024
    │    │    └─ReLU: 3-51                   [100, 512, 4, 4]          --
    ├─AdaptiveAvgPool2d: 1-9                 [100, 512, 1, 1]          --
    ├─Linear: 1-10                           [100, 10]                 5,130
    ==========================================================================================
    Total params: 11,181,642
    Trainable params: 11,181,642
    Non-trainable params: 0
    Total mult-adds (G): 48.49
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 1008.85
    Params size (MB): 44.73
    Estimated Total Size (MB): 1068.63
    ==========================================================================================




```python
# 손실 계산 그래프 시각화

criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__25_0.svg)
    



```python
# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)

# history 파일 초기화
history = np.zeros((0, 5))
```


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
        train_loader, test_loader, device, history)
```


      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [1/5], loss: 1.67881 acc: 0.37534 val_loss: 1.40021, val_acc: 0.48730



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [2/5], loss: 1.30478 acc: 0.52360 val_loss: 1.18151, val_acc: 0.57310



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [3/5], loss: 1.13530 acc: 0.59180 val_loss: 1.03601, val_acc: 0.63070



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [4/5], loss: 1.00664 acc: 0.64066 val_loss: 1.04888, val_acc: 0.63230



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.91432 acc: 0.67626 val_loss: 0.89390, val_acc: 0.68010



```python
# 결과 요약
evaluate_history(history)
```

    초기상태 : 손실 : 1.40021  정확도 : 0.48730
    최종상태 : 손실 : 0.89390 정확도 : 0.68010



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__28_1.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__28_2.webp)
    



```python
# 이미지와 정답, 예측 결과를 함께 표시
show_images_labels(test_loader, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_16%EC%B0%A8%EC%8B%9C__model_from_scratch__29_1.webp)
    



## 강의_3기_AI개론_17차시__FasterRCNN_MaskedRCNN_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_17차시__FasterRCNN_MaskedRCNN_.ipynb)

# 17장 객체 검출 (Two-stage object detection)
- RCNN, Fast/Faster RCNN, Masked RCNN

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
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
# 폰트 관련 용도
import matplotlib.font_manager as fm

import torch
from torchvision.io import read_image
from torchvision import models, datasets, transforms
from torchinfo import summary
from torchviz import make_dot
from torch import nn, optim
import torchvision.transforms.functional as F
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
# GPU 디바이스 할당

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
```

    cuda:0


## Faster R-CNN 사용하기


```python
''' 
The model builder above accepts the following values as the weights parameter. 
FasterRCNN_ResNet50_FPN_Weights.DEFAULT is equivalent to FasterRCNN_ResNet50_FPN_Weights.COCO_V1. 
You can also use strings, e.g. weights='DEFAULT' or weights='COCO_V1'.

The inference transforms are available at FasterRCNN_ResNet50_FPN_Weights.COCO_V1.transforms 
and perform the following preprocessing operations: 
Accepts PIL.Image, batched (B, C, H, W) and single (C, H, W) image torch.Tensor objects. 
The images are rescaled to [0.0, 1.0].
'''
```


```python
## Pretrained object detection model list
dir(models.detection)
```




    ['FCOS',
     'FCOS_ResNet50_FPN_Weights',
     'FasterRCNN',
     'FasterRCNN_MobileNet_V3_Large_320_FPN_Weights',
     'FasterRCNN_MobileNet_V3_Large_FPN_Weights',
     'FasterRCNN_ResNet50_FPN_V2_Weights',
     'FasterRCNN_ResNet50_FPN_Weights',
     'KeypointRCNN',
     'KeypointRCNN_ResNet50_FPN_Weights',
     'MaskRCNN',
     'MaskRCNN_ResNet50_FPN_V2_Weights',
     'MaskRCNN_ResNet50_FPN_Weights',
     'RetinaNet',
     'RetinaNet_ResNet50_FPN_V2_Weights',
     'RetinaNet_ResNet50_FPN_Weights',
     'SSD300_VGG16_Weights',
     'SSDLite320_MobileNet_V3_Large_Weights',
     '__builtins__',
     '__cached__',
     '__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__path__',
     '__spec__',
     '_utils',
     'anchor_utils',
     'backbone_utils',
     'faster_rcnn',
     'fasterrcnn_mobilenet_v3_large_320_fpn',
     'fasterrcnn_mobilenet_v3_large_fpn',
     'fasterrcnn_resnet50_fpn',
     'fasterrcnn_resnet50_fpn_v2',
     'fcos',
     'fcos_resnet50_fpn',
     'generalized_rcnn',
     'image_list',
     'keypoint_rcnn',
     'keypointrcnn_resnet50_fpn',
     'mask_rcnn',
     'maskrcnn_resnet50_fpn',
     'maskrcnn_resnet50_fpn_v2',
     'retinanet',
     'retinanet_resnet50_fpn',
     'retinanet_resnet50_fpn_v2',
     'roi_heads',
     'rpn',
     'ssd',
     'ssd300_vgg16',
     'ssdlite',
     'ssdlite320_mobilenet_v3_large',
     'transform']



### 모델 불러 오기


```python
weights= models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT
fasterRCNN = models.detection.fasterrcnn_resnet50_fpn(weights=weights)
```

### 모델 구조 확인


```python
print(fasterRCNN) # PyTorch의 torchvision 라이브러리는 RGB 형식을 사용
```

    FasterRCNN(
      (transform): GeneralizedRCNNTransform(
          Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
          Resize(min_size=(800,), max_size=1333, mode='bilinear')
      )
      (backbone): BackboneWithFPN(
        (body): IntermediateLayerGetter(
          (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
          (bn1): FrozenBatchNorm2d(64, eps=0.0)
          (relu): ReLU(inplace=True)
          (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
          (layer1): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
                (1): FrozenBatchNorm2d(256, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer2): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(256, 512, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(512, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (3): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer3): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(512, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(512, 1024, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(1024, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (3): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (4): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (5): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer4): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(1024, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(1024, 2048, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(2048, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(2048, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(2048, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
        )
        (fpn): FeaturePyramidNetwork(
          (inner_blocks): ModuleList(
            (0): Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (1): Conv2dNormActivation(
              (0): Conv2d(512, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (2): Conv2dNormActivation(
              (0): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (3): Conv2dNormActivation(
              (0): Conv2d(2048, 256, kernel_size=(1, 1), stride=(1, 1))
            )
          )
          (layer_blocks): ModuleList(
            (0-3): 4 x Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            )
          )
          (extra_blocks): LastLevelMaxPool()
        )
      )
      (rpn): RegionProposalNetwork(
        (anchor_generator): AnchorGenerator()
        (head): RPNHead(
          (conv): Sequential(
            (0): Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (1): ReLU(inplace=True)
            )
          )
          (cls_logits): Conv2d(256, 3, kernel_size=(1, 1), stride=(1, 1))
          (bbox_pred): Conv2d(256, 12, kernel_size=(1, 1), stride=(1, 1))
        )
      )
      (roi_heads): RoIHeads(
        (box_roi_pool): MultiScaleRoIAlign(featmap_names=['0', '1', '2', '3'], output_size=(7, 7), sampling_ratio=2)
        (box_head): TwoMLPHead(
          (fc6): Linear(in_features=12544, out_features=1024, bias=True)
          (fc7): Linear(in_features=1024, out_features=1024, bias=True)
        )
        (box_predictor): FastRCNNPredictor(
          (cls_score): Linear(in_features=1024, out_features=91, bias=True)
          (bbox_pred): Linear(in_features=1024, out_features=364, bias=True)
        )
      )
    )



```python
fasterRCNN = fasterRCNN.to(device)
```

### 추론 하기


```python
## 결과 형식 확인
fasterRCNN.eval() ## 추론 모드드

x = [torch.rand(3, 300, 400).to(device), 
     torch.rand(3, 500, 400).to(device)]

```


```python
predictions = fasterRCNN(x)
print("Faster RCNN outputs = \n")
display(predictions)

plt.imshow(x[1].cpu().permute(1, 2, 0))
plt.title("torch.rand(3, 300, 400)")
plt.show()
```

    Faster RCNN outputs = 
    



    [{'boxes': tensor([], device='cuda:0', size=(0, 4), grad_fn=<StackBackward0>),
      'labels': tensor([], device='cuda:0', dtype=torch.int64),
      'scores': tensor([], device='cuda:0', grad_fn=<IndexBackward0>)},
     {'boxes': tensor([], device='cuda:0', size=(0, 4), grad_fn=<StackBackward0>),
      'labels': tensor([], device='cuda:0', dtype=torch.int64),
      'scores': tensor([], device='cuda:0', grad_fn=<IndexBackward0>)}]



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__19_2.webp)
    



```python
# Wrapper model for compatibility with summary
# summary(fasterRCNN, input_size= (3, 226, 226)) # error

class FasterRCNNWrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        # Convert the 4D tensor into a list of 3D tensors
        x = [img for img in x]
        # Get the predictions from the model
        output = self.model(x)
        # Return a placeholder tensor for torchinfo (e.g., batch of dummy boxes)
        
        return output

# Wrap the model
wrapped_model = FasterRCNNWrapper(fasterRCNN)
# Generate the model summary
summary(wrapped_model, input_size=(2, 3, 226, 226))  #  cpu to cuda
# print("1", fasterRCNN.backbone.body.conv1.weight.device)
```




    ==============================================================================================================
    Layer (type:depth-idx)                                       Output Shape              Param #
    ==============================================================================================================
    FasterRCNNWrapper                                            [0, 4]                    --
    ├─FasterRCNN: 1-1                                            [0, 4]                    --
    │    └─GeneralizedRCNNTransform: 2-1                         [2, 3, 800, 800]          --
    │    └─BackboneWithFPN: 2-2                                  [2, 256, 13, 13]          --
    │    │    └─IntermediateLayerGetter: 3-1                     [2, 2048, 25, 25]         23,454,912
    │    │    └─FeaturePyramidNetwork: 3-2                       [2, 256, 13, 13]          3,344,384
    │    └─RegionProposalNetwork: 2-3                            [1000, 4]                 --
    │    │    └─RPNHead: 3-3                                     [2, 3, 200, 200]          593,935
    │    │    └─AnchorGenerator: 3-4                             [159882, 4]               --
    │    └─RoIHeads: 2-4                                         [0, 4]                    --
    │    │    └─MultiScaleRoIAlign: 3-5                          [2000, 256, 7, 7]         --
    │    │    └─TwoMLPHead: 3-6                                  [2000, 1024]              13,895,680
    │    │    └─FastRCNNPredictor: 3-7                           [2000, 91]                466,375
    ==============================================================================================================
    Total params: 41,755,286
    Trainable params: 41,532,886
    Non-trainable params: 222,400
    Total mult-adds (G): 268.85
    ==============================================================================================================
    Input size (MB): 1.23
    Forward/backward pass size (MB): 2974.49
    Params size (MB): 167.02
    Estimated Total Size (MB): 3142.74
    ==============================================================================================================



### COCO labels 확인


```python
coco_labels_list = weights.meta["categories"]
print("COCO v1 dataset  = ", len(coco_labels_list)) # 80 + dummy 11
display(coco_labels_list)
```

    COCO v1 dataset  =  91



    ['__background__',
     'person',
     'bicycle',
     'car',
     'motorcycle',
     'airplane',
     'bus',
     'train',
     'truck',
     'boat',
     'traffic light',
     'fire hydrant',
     'N/A',
     'stop sign',
     'parking meter',
     'bench',
     'bird',
     'cat',
     'dog',
     'horse',
     'sheep',
     'cow',
     'elephant',
     'bear',
     'zebra',
     'giraffe',
     'N/A',
     'backpack',
     'umbrella',
     'N/A',
     'N/A',
     'handbag',
     'tie',
     'suitcase',
     'frisbee',
     'skis',
     'snowboard',
     'sports ball',
     'kite',
     'baseball bat',
     'baseball glove',
     'skateboard',
     'surfboard',
     'tennis racket',
     'bottle',
     'N/A',
     'wine glass',
     'cup',
     'fork',
     'knife',
     'spoon',
     'bowl',
     'banana',
     'apple',
     'sandwich',
     'orange',
     'broccoli',
     'carrot',
     'hot dog',
     'pizza',
     'donut',
     'cake',
     'chair',
     'couch',
     'potted plant',
     'bed',
     'N/A',
     'dining table',
     'N/A',
     'N/A',
     'toilet',
     'N/A',
     'tv',
     'laptop',
     'mouse',
     'remote',
     'keyboard',
     'cell phone',
     'microwave',
     'oven',
     'toaster',
     'sink',
     'refrigerator',
     'N/A',
     'book',
     'clock',
     'vase',
     'scissors',
     'teddy bear',
     'hair drier',
     'toothbrush']


### 폴더 내 영상 읽기


```python
data_dir = "./figure"

img_path = os.path.join(data_dir, "dog.jpg")
img = read_image(img_path).to(device)

print('img type = ', type(img))
print("image shape = ", img.shape)
```

    img type =  <class 'torch.Tensor'>
    image shape =  torch.Size([3, 576, 768])


### 영상 전처리


```python
fasterRCNN = fasterRCNN.to(device)
preprocess = weights.transforms() # 학습 자료에 맞에 조정
fasterRCNN
```




    FasterRCNN(
      (transform): GeneralizedRCNNTransform(
          Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
          Resize(min_size=(800,), max_size=1333, mode='bilinear')
      )
      (backbone): BackboneWithFPN(
        (body): IntermediateLayerGetter(
          (conv1): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
          (bn1): FrozenBatchNorm2d(64, eps=0.0)
          (relu): ReLU(inplace=True)
          (maxpool): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
          (layer1): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
                (1): FrozenBatchNorm2d(256, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(64, eps=0.0)
              (conv2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(64, eps=0.0)
              (conv3): Conv2d(64, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(256, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer2): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(256, 512, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(512, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (3): Bottleneck(
              (conv1): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(128, eps=0.0)
              (conv2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(128, eps=0.0)
              (conv3): Conv2d(128, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(512, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer3): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(512, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(512, 1024, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(1024, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (3): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (4): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (5): Bottleneck(
              (conv1): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(256, eps=0.0)
              (conv2): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(256, eps=0.0)
              (conv3): Conv2d(256, 1024, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(1024, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
          (layer4): Sequential(
            (0): Bottleneck(
              (conv1): Conv2d(1024, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
              (downsample): Sequential(
                (0): Conv2d(1024, 2048, kernel_size=(1, 1), stride=(2, 2), bias=False)
                (1): FrozenBatchNorm2d(2048, eps=0.0)
              )
            )
            (1): Bottleneck(
              (conv1): Conv2d(2048, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
            )
            (2): Bottleneck(
              (conv1): Conv2d(2048, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn1): FrozenBatchNorm2d(512, eps=0.0)
              (conv2): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
              (bn2): FrozenBatchNorm2d(512, eps=0.0)
              (conv3): Conv2d(512, 2048, kernel_size=(1, 1), stride=(1, 1), bias=False)
              (bn3): FrozenBatchNorm2d(2048, eps=0.0)
              (relu): ReLU(inplace=True)
            )
          )
        )
        (fpn): FeaturePyramidNetwork(
          (inner_blocks): ModuleList(
            (0): Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (1): Conv2dNormActivation(
              (0): Conv2d(512, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (2): Conv2dNormActivation(
              (0): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1))
            )
            (3): Conv2dNormActivation(
              (0): Conv2d(2048, 256, kernel_size=(1, 1), stride=(1, 1))
            )
          )
          (layer_blocks): ModuleList(
            (0-3): 4 x Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            )
          )
          (extra_blocks): LastLevelMaxPool()
        )
      )
      (rpn): RegionProposalNetwork(
        (anchor_generator): AnchorGenerator()
        (head): RPNHead(
          (conv): Sequential(
            (0): Conv2dNormActivation(
              (0): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (1): ReLU(inplace=True)
            )
          )
          (cls_logits): Conv2d(256, 3, kernel_size=(1, 1), stride=(1, 1))
          (bbox_pred): Conv2d(256, 12, kernel_size=(1, 1), stride=(1, 1))
        )
      )
      (roi_heads): RoIHeads(
        (box_roi_pool): MultiScaleRoIAlign(featmap_names=['0', '1', '2', '3'], output_size=(7, 7), sampling_ratio=2)
        (box_head): TwoMLPHead(
          (fc6): Linear(in_features=12544, out_features=1024, bias=True)
          (fc7): Linear(in_features=1024, out_features=1024, bias=True)
        )
        (box_predictor): FastRCNNPredictor(
          (cls_score): Linear(in_features=1024, out_features=91, bias=True)
          (bbox_pred): Linear(in_features=1024, out_features=364, bias=True)
        )
      )
    )




```python
batch_img = preprocess(img) # 
batch_img.shape
```




    torch.Size([3, 576, 768])




```python
batch_img = batch_img.unsqueeze(0)
# batch_img = batch_img.to(device)
```

### 모델 예측


```python
import time
fasterRCNN.eval()

start = time.time()
pred = fasterRCNN(batch_img)
stop = time.time()
print(f"estimation time = {(stop - start)*1000:.3f}ms")

pred
```




    [{'boxes': tensor([[130.3126, 225.0357, 319.0403, 534.0589],
              [163.7504, 104.9969, 570.4412, 448.7537],
              [127.9439, 139.2940, 277.1543, 382.7612],
              [471.6621,  79.2776, 680.4760, 169.9647],
              [129.2778, 231.7216, 218.7447, 381.2831],
              [467.3390,  83.1568, 678.7368, 167.9611],
              [711.6593,  29.0584, 760.4049, 244.5217],
              [132.6494, 122.8677, 409.6773, 420.0911],
              [676.1831,  98.1239, 718.5799, 155.4015],
              [126.9611, 132.6783, 436.8705, 404.2952],
              [ 58.3749,  85.2088, 103.5193, 127.3281],
              [599.1298, 105.8067, 619.8306, 122.4434],
              [ 55.8846,  86.5438,  84.3360, 135.6524],
              [134.2069, 215.0720, 322.5725, 536.2981],
              [ 58.4227,  79.5715, 106.2005, 127.5270],
              [600.6806, 107.6764, 613.7610, 120.5343],
              [718.4550,  28.6718, 766.1320, 269.9488],
              [124.7195, 138.1096, 591.1942, 512.2091],
              [677.8379,  32.0160, 744.9001, 163.6230],
              [ 69.7168,  86.9616, 100.3568, 123.6976],
              [237.5230, 179.8376, 575.6920, 418.8686],
              [121.5356, 147.1317, 309.2010, 412.5814],
              [606.6609, 107.8231, 618.9048, 121.8843],
              [ 87.6799,  71.3497, 111.0981,  86.6945],
              [129.7706, 233.7621, 219.1420, 378.7996]], device='cuda:0',
             grad_fn=<StackBackward0>),
      'labels': tensor([18,  2,  2,  3,  2,  8, 64,  2, 64, 15, 64,  1, 64, 17,  4,  1, 72, 15,
              64,  4, 15, 62,  1, 31, 62], device='cuda:0'),
      'scores': tensor([0.9960, 0.9841, 0.8145, 0.7615, 0.6086, 0.5446, 0.3389, 0.3327, 0.2993,
              0.2790, 0.2676, 0.2547, 0.2136, 0.2028, 0.2025, 0.1514, 0.1428, 0.1047,
              0.0956, 0.0849, 0.0809, 0.0671, 0.0607, 0.0524, 0.0516],
             device='cuda:0', grad_fn=<IndexBackward0>)}]



### 분류 및 Bounding box 확인하기


```python
pred_dict = pred[0]
print("pred_dict = \n", pred_dict)
print("keys = ", pred_dict.keys())
print("labels = ", pred_dict["labels"])
print("scores = ", pred_dict["scores"])
```

    pred_dict = 
     {'boxes': tensor([[130.3126, 225.0357, 319.0403, 534.0589],
            [163.7504, 104.9969, 570.4412, 448.7537],
            [127.9439, 139.2940, 277.1543, 382.7612],
            [471.6621,  79.2776, 680.4760, 169.9647],
            [129.2778, 231.7216, 218.7447, 381.2831],
            [467.3390,  83.1568, 678.7368, 167.9611],
            [711.6593,  29.0584, 760.4049, 244.5217],
            [132.6494, 122.8677, 409.6773, 420.0911],
            [676.1831,  98.1239, 718.5799, 155.4015],
            [126.9611, 132.6783, 436.8705, 404.2952],
            [ 58.3749,  85.2088, 103.5193, 127.3281],
            [599.1298, 105.8067, 619.8306, 122.4434],
            [ 55.8846,  86.5438,  84.3360, 135.6524],
            [134.2069, 215.0720, 322.5725, 536.2981],
            [ 58.4227,  79.5715, 106.2005, 127.5270],
            [600.6806, 107.6764, 613.7610, 120.5343],
            [718.4550,  28.6718, 766.1320, 269.9488],
            [124.7195, 138.1096, 591.1942, 512.2091],
            [677.8379,  32.0160, 744.9001, 163.6230],
            [ 69.7168,  86.9616, 100.3568, 123.6976],
            [237.5230, 179.8376, 575.6920, 418.8686],
            [121.5356, 147.1317, 309.2010, 412.5814],
            [606.6609, 107.8231, 618.9048, 121.8843],
            [ 87.6799,  71.3497, 111.0981,  86.6945],
            [129.7706, 233.7621, 219.1420, 378.7996]], device='cuda:0',
           grad_fn=<StackBackward0>), 'labels': tensor([18,  2,  2,  3,  2,  8, 64,  2, 64, 15, 64,  1, 64, 17,  4,  1, 72, 15,
            64,  4, 15, 62,  1, 31, 62], device='cuda:0'), 'scores': tensor([0.9960, 0.9841, 0.8145, 0.7615, 0.6086, 0.5446, 0.3389, 0.3327, 0.2993,
            0.2790, 0.2676, 0.2547, 0.2136, 0.2028, 0.2025, 0.1514, 0.1428, 0.1047,
            0.0956, 0.0849, 0.0809, 0.0671, 0.0607, 0.0524, 0.0516],
           device='cuda:0', grad_fn=<IndexBackward0>)}
    keys =  dict_keys(['boxes', 'labels', 'scores'])
    labels =  tensor([18,  2,  2,  3,  2,  8, 64,  2, 64, 15, 64,  1, 64, 17,  4,  1, 72, 15,
            64,  4, 15, 62,  1, 31, 62], device='cuda:0')
    scores =  tensor([0.9960, 0.9841, 0.8145, 0.7615, 0.6086, 0.5446, 0.3389, 0.3327, 0.2993,
            0.2790, 0.2676, 0.2547, 0.2136, 0.2028, 0.2025, 0.1514, 0.1428, 0.1047,
            0.0956, 0.0849, 0.0809, 0.0671, 0.0607, 0.0524, 0.0516],
           device='cuda:0', grad_fn=<IndexBackward0>)


### Bounding box 그리기


```python
threshold = 0.7
indices = pred_dict['scores'] >= threshold
print("indices = ", indices)
pred_boxes = pred_dict['boxes'][indices]
pred_labels = pred_dict['labels'][indices]
pred_scores = pred_dict['scores'][indices]

print("pred_boxes = \n", pred_boxes)
print("pred_labels = \n", pred_labels)
print("pred_scores = \n", pred_scores)

```

    indices =  tensor([ True,  True,  True,  True, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False], device='cuda:0')
    pred_boxes = 
     tensor([[130.3126, 225.0357, 319.0403, 534.0589],
            [163.7504, 104.9969, 570.4412, 448.7537],
            [127.9439, 139.2940, 277.1543, 382.7612],
            [471.6621,  79.2776, 680.4760, 169.9647]], device='cuda:0',
           grad_fn=<IndexBackward0>)
    pred_labels = 
     tensor([18,  2,  2,  3], device='cuda:0')
    pred_scores = 
     tensor([0.9960, 0.9841, 0.8145, 0.7615], device='cuda:0',
           grad_fn=<IndexBackward0>)



```python
import random

image = img.permute(1, 2, 0).cpu().numpy()
color_array = [[random.randint(0, 255) for _ in range(3)] for _ in range(91)]

for i in range(len(pred_boxes)):
    x_min = int(pred_boxes[i][0])
    y_min = int(pred_boxes[i][1])
    x_max = int(pred_boxes[i][2])
    y_max = int(pred_boxes[i][3])

    color = color_array[pred_labels[i]]

    cv2.rectangle(image,
                      pt1=(x_min, y_min),
                      pt2=(x_max, y_max),
                      color=color,
                      thickness=2)
    
    cv2.putText(image,
                    text=coco_labels_list[pred_labels[i]] + ' {:.2f}'.format(pred_scores[i].item()),
                    org=(x_min + 10, y_min - 10),  # must be int
                    fontFace=0,
                    fontScale=0.8,
                    color=color, thickness = 2)

plt.figure(figsize=(8, 6))
plt.imshow(image)
plt.grid(None)
plt.axis("off")
plt.show()
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__35_0.webp)
    


# 의미적 분할 (Semantic segmentation)



```python
# plt.rcParams["savefig.bbox"] = 'tight'
# def show(imgs):
#     # if not isinstance(imgs, list):
#     #     imgs = [imgs]
#     fig, axs = plt.subplots(ncols=len(imgs), figsize = (12, 6),  squeeze=False) # returned as a 2D array even if there is only one row or column of subplots.

#     for i, img in enumerate(imgs):
#         img = img.detach()
#         img = F.to_pil_image(img) # permute dimension
#         axs[0, i].imshow(np.asarray(img))
#         # axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
#         axs[0, i].axis("off")
```

### Draw 함수 정의


```python

# plt.rcParams["savefig.bbox"] = 'tight' # 모든 저장 시 여백 최소화
def show(imgs : list):
    if not isinstance(imgs, list):
        imgs = [imgs]
    
    fig, axs = plt.subplots(ncols=len(imgs), figsize = (12, 6),  squeeze=False) # returned as a 2D array even if there is only one row or column of subplots.

    for i, img in enumerate(imgs):
        # img = img.detach().permute(1, 2, 0)
        img = F.to_pil_image(img) # permute dimension
        axs[0, i].imshow(img)
        # axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
        axs[0, i].axis("off")
```

### 이미지 list 만들기


```python
from torchvision.utils import make_grid
from torchvision.io import read_image

data_dir = "./figure"

img1 = read_image(os.path.join(data_dir, "dog.jpg"))
img2 = read_image(os.path.join(data_dir, "peoples.jpg"))

img_list = [img1, img2]
show(img_list)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__41_0.webp)
    


### Bounding box 그리기 함수


```python
# draw_bounding_boxes(image:Tensor, boxes:Tensor, labels:List[str], colors:List[str] , width:int=1)
# find /usr/share/fonts -name "*.ttf"

from torchvision.utils import draw_bounding_boxes
from PIL import Image

pred_boxes = torch.tensor([[50, 50, 100, 200], 
                           [210, 150, 350, 430]], dtype=torch.float) #  (xmin, ymin, xmax, ymax) format.
labels = ["1", "2"]
colors = ["blue", "yellow"]
result = draw_bounding_boxes(img1, pred_boxes, labels, colors=colors, width=5, 
                            #  font="C:\\Windows\\Fonts\\arial.ttf", # window case
                            font = font_name,
                             font_size= 20) # boxes.shape torch.Size([2, 4])
show(result)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__43_0.webp)
    



```python
weights= models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT
fasterRCNN = models.detection.fasterrcnn_resnet50_fpn(weights=weights).to(device)
```


```python

transforms = weights.transforms()
images = [transforms(d).to(device) for d in img_list]
```


```python

fasterRCNN.eval()
outputs = fasterRCNN(images)
```


```python
print(outputs[0]["labels"])
print(outputs[0]["scores"])
print(outputs[0]["boxes"])
len(outputs)
```

    tensor([18,  2,  2,  3,  2,  8, 64,  2, 64, 15, 64,  1, 64, 17,  4,  1, 72, 15,
            64,  4, 15, 62,  1, 31, 62])
    tensor([0.9960, 0.9841, 0.8145, 0.7615, 0.6086, 0.5446, 0.3389, 0.3327, 0.2993,
            0.2790, 0.2676, 0.2547, 0.2136, 0.2028, 0.2025, 0.1514, 0.1428, 0.1047,
            0.0956, 0.0849, 0.0809, 0.0671, 0.0607, 0.0524, 0.0516],
           grad_fn=<IndexBackward0>)
    tensor([[130.3126, 225.0357, 319.0403, 534.0589],
            [163.7504, 104.9968, 570.4410, 448.7537],
            [127.9440, 139.2940, 277.1543, 382.7611],
            [471.6621,  79.2776, 680.4758, 169.9647],
            [129.2778, 231.7217, 218.7447, 381.2831],
            [467.3391,  83.1568, 678.7368, 167.9612],
            [711.6593,  29.0584, 760.4049, 244.5217],
            [132.6494, 122.8677, 409.6776, 420.0912],
            [676.1831,  98.1239, 718.5799, 155.4015],
            [126.9611, 132.6782, 436.8708, 404.2953],
            [ 58.3749,  85.2088, 103.5193, 127.3281],
            [599.1298, 105.8067, 619.8306, 122.4434],
            [ 55.8846,  86.5438,  84.3359, 135.6524],
            [134.2069, 215.0720, 322.5725, 536.2981],
            [ 58.4227,  79.5715, 106.2005, 127.5270],
            [600.6807, 107.6764, 613.7610, 120.5343],
            [718.4550,  28.6718, 766.1320, 269.9487],
            [124.7196, 138.1096, 591.1943, 512.2091],
            [677.8379,  32.0160, 744.9001, 163.6229],
            [ 69.7168,  86.9616, 100.3568, 123.6976],
            [237.5229, 179.8376, 575.6920, 418.8686],
            [121.5356, 147.1316, 309.2010, 412.5809],
            [606.6609, 107.8231, 618.9048, 121.8843],
            [ 87.6799,  71.3497, 111.0981,  86.6945],
            [129.7706, 233.7621, 219.1420, 378.7995]], grad_fn=<StackBackward0>)





    2




```python
score_threshold = .7
dogs_with_boxes = [
    draw_bounding_boxes(img, boxes=output['boxes'][output['scores'] > score_threshold], width=4)
    for img, output in zip(img_list, outputs)]
show(dogs_with_boxes)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__48_0.webp)
    


## Semantic Segmentation 모델 불러 오기


```python
dir(models.segmentation)
```




    ['DeepLabV3',
     'DeepLabV3_MobileNet_V3_Large_Weights',
     'DeepLabV3_ResNet101_Weights',
     'DeepLabV3_ResNet50_Weights',
     'FCN',
     'FCN_ResNet101_Weights',
     'FCN_ResNet50_Weights',
     'LRASPP',
     'LRASPP_MobileNet_V3_Large_Weights',
     '__builtins__',
     '__cached__',
     '__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__path__',
     '__spec__',
     '_utils',
     'deeplabv3',
     'deeplabv3_mobilenet_v3_large',
     'deeplabv3_resnet101',
     'deeplabv3_resnet50',
     'fcn',
     'fcn_resnet101',
     'fcn_resnet50',
     'lraspp',
     'lraspp_mobilenet_v3_large']




```python
# from torchvision.models.segmentation import fcn_resnet50, FCN_ResNet50_Weights

weights = models.segmentation.FCN_ResNet50_Weights.DEFAULT
model = models.segmentation.fcn_resnet50(weights=weights, progress=True).to(device)

```


```python
transforms = weights.transforms(resize_size = None)
print(transforms)
```

    SemanticSegmentation(
        resize_size=None
        mean=[0.485, 0.456, 0.406]
        std=[0.229, 0.224, 0.225]
        interpolation=InterpolationMode.BILINEAR
    )


### 모델 추론


```python
batch = torch.stack([transforms(d) for d in img_list]).to(device)
batch.shape
```




    torch.Size([2, 3, 576, 768])




```python
model.eval()
output = model(batch)['out'] # [batch_size, num_classes, height, width]
# print(output.shape, output.min().item(), output.max().item()) # logits
print(output.shape) # logits

```

    torch.Size([2, 21, 576, 768])


### class dictionary 만들기


```python
sem_class_to_idx = {cls: idx for idx, cls in enumerate(weights.meta["categories"])}
sem_class_to_idx
```




    {'__background__': 0,
     'aeroplane': 1,
     'bicycle': 2,
     'bird': 3,
     'boat': 4,
     'bottle': 5,
     'bus': 6,
     'car': 7,
     'cat': 8,
     'chair': 9,
     'cow': 10,
     'diningtable': 11,
     'dog': 12,
     'horse': 13,
     'motorbike': 14,
     'person': 15,
     'pottedplant': 16,
     'sheep': 17,
     'sofa': 18,
     'train': 19,
     'tvmonitor': 20}



### Class score map


```python
normalized_masks = torch.softmax(output, dim=1) # torch.Size([2, 21, 576, 768]), [batch_size, num_classes, height, width]
normalized_masks
```




    tensor([[[[9.9247e-01, 9.9247e-01, 9.9247e-01,  ..., 9.9076e-01,
               9.9076e-01, 9.9076e-01],
              [9.9247e-01, 9.9247e-01, 9.9247e-01,  ..., 9.9076e-01,
               9.9076e-01, 9.9076e-01],
              [9.9247e-01, 9.9247e-01, 9.9247e-01,  ..., 9.9076e-01,
               9.9076e-01, 9.9076e-01],
              ...,
              [9.9625e-01, 9.9625e-01, 9.9625e-01,  ..., 9.5328e-01,
               9.5328e-01, 9.5328e-01],
              [9.9625e-01, 9.9625e-01, 9.9625e-01,  ..., 9.5328e-01,
               9.5328e-01, 9.5328e-01],
              [9.9625e-01, 9.9625e-01, 9.9625e-01,  ..., 9.5328e-01,
               9.5328e-01, 9.5328e-01]],
    
             [[4.6047e-04, 4.6047e-04, 4.6047e-04,  ..., 1.2888e-04,
               1.2888e-04, 1.2888e-04],
              [4.6047e-04, 4.6047e-04, 4.6047e-04,  ..., 1.2888e-04,
               1.2888e-04, 1.2888e-04],
              [4.6047e-04, 4.6047e-04, 4.6047e-04,  ..., 1.2888e-04,
               1.2888e-04, 1.2888e-04],
              ...,
              [2.1855e-05, 2.1855e-05, 2.1855e-05,  ..., 4.2934e-04,
               4.2934e-04, 4.2934e-04],
              [2.1855e-05, 2.1855e-05, 2.1855e-05,  ..., 4.2934e-04,
               4.2934e-04, 4.2934e-04],
              [2.1855e-05, 2.1855e-05, 2.1855e-05,  ..., 4.2934e-04,
               4.2934e-04, 4.2934e-04]],
    
             [[3.6939e-05, 3.6939e-05, 3.6939e-05,  ..., 1.0244e-04,
               1.0244e-04, 1.0244e-04],
              [3.6939e-05, 3.6939e-05, 3.6939e-05,  ..., 1.0244e-04,
               1.0244e-04, 1.0244e-04],
              [3.6939e-05, 3.6939e-05, 3.6939e-05,  ..., 1.0244e-04,
               1.0244e-04, 1.0244e-04],
              ...,
              [2.5353e-05, 2.5353e-05, 2.5353e-05,  ..., 7.2889e-04,
               7.2889e-04, 7.2889e-04],
              [2.5353e-05, 2.5353e-05, 2.5353e-05,  ..., 7.2889e-04,
               7.2889e-04, 7.2889e-04],
              [2.5353e-05, 2.5353e-05, 2.5353e-05,  ..., 7.2889e-04,
               7.2889e-04, 7.2889e-04]],
    
             ...,
    
             [[1.2218e-04, 1.2218e-04, 1.2218e-04,  ..., 8.8024e-05,
               8.8024e-05, 8.8024e-05],
              [1.2218e-04, 1.2218e-04, 1.2218e-04,  ..., 8.8024e-05,
               8.8024e-05, 8.8024e-05],
              [1.2218e-04, 1.2218e-04, 1.2218e-04,  ..., 8.8024e-05,
               8.8024e-05, 8.8024e-05],
              ...,
              [2.3560e-04, 2.3560e-04, 2.3560e-04,  ..., 8.6903e-04,
               8.6903e-04, 8.6903e-04],
              [2.3560e-04, 2.3560e-04, 2.3560e-04,  ..., 8.6903e-04,
               8.6903e-04, 8.6903e-04],
              [2.3560e-04, 2.3560e-04, 2.3560e-04,  ..., 8.6903e-04,
               8.6903e-04, 8.6903e-04]],
    
             [[1.4883e-03, 1.4883e-03, 1.4883e-03,  ..., 1.4384e-04,
               1.4384e-04, 1.4384e-04],
              [1.4883e-03, 1.4883e-03, 1.4883e-03,  ..., 1.4384e-04,
               1.4384e-04, 1.4384e-04],
              [1.4883e-03, 1.4883e-03, 1.4883e-03,  ..., 1.4384e-04,
               1.4384e-04, 1.4384e-04],
              ...,
              [1.2433e-04, 1.2433e-04, 1.2433e-04,  ..., 5.8434e-04,
               5.8434e-04, 5.8434e-04],
              [1.2433e-04, 1.2433e-04, 1.2433e-04,  ..., 5.8434e-04,
               5.8434e-04, 5.8434e-04],
              [1.2433e-04, 1.2433e-04, 1.2433e-04,  ..., 5.8434e-04,
               5.8434e-04, 5.8434e-04]],
    
             [[1.5103e-03, 1.5103e-03, 1.5103e-03,  ..., 5.2474e-04,
               5.2474e-04, 5.2474e-04],
              [1.5103e-03, 1.5103e-03, 1.5103e-03,  ..., 5.2474e-04,
               5.2474e-04, 5.2474e-04],
              [1.5103e-03, 1.5103e-03, 1.5103e-03,  ..., 5.2474e-04,
               5.2474e-04, 5.2474e-04],
              ...,
              [1.9979e-05, 1.9979e-05, 1.9979e-05,  ..., 4.0208e-04,
               4.0208e-04, 4.0208e-04],
              [1.9979e-05, 1.9979e-05, 1.9979e-05,  ..., 4.0208e-04,
               4.0208e-04, 4.0208e-04],
              [1.9979e-05, 1.9979e-05, 1.9979e-05,  ..., 4.0208e-04,
               4.0208e-04, 4.0208e-04]]],
    
    
            [[[9.8051e-01, 9.8051e-01, 9.8051e-01,  ..., 9.9728e-01,
               9.9728e-01, 9.9728e-01],
              [9.8051e-01, 9.8051e-01, 9.8051e-01,  ..., 9.9728e-01,
               9.9728e-01, 9.9728e-01],
              [9.8051e-01, 9.8051e-01, 9.8051e-01,  ..., 9.9728e-01,
               9.9728e-01, 9.9728e-01],
              ...,
              [9.4728e-01, 9.4728e-01, 9.4728e-01,  ..., 9.9812e-01,
               9.9812e-01, 9.9812e-01],
              [9.4728e-01, 9.4728e-01, 9.4728e-01,  ..., 9.9812e-01,
               9.9812e-01, 9.9812e-01],
              [9.4728e-01, 9.4728e-01, 9.4728e-01,  ..., 9.9812e-01,
               9.9812e-01, 9.9812e-01]],
    
             [[2.6462e-04, 2.6462e-04, 2.6462e-04,  ..., 1.2735e-05,
               1.2735e-05, 1.2735e-05],
              [2.6462e-04, 2.6462e-04, 2.6462e-04,  ..., 1.2735e-05,
               1.2735e-05, 1.2735e-05],
              [2.6462e-04, 2.6462e-04, 2.6462e-04,  ..., 1.2735e-05,
               1.2735e-05, 1.2735e-05],
              ...,
              [1.2839e-04, 1.2839e-04, 1.2839e-04,  ..., 2.7916e-05,
               2.7916e-05, 2.7916e-05],
              [1.2839e-04, 1.2839e-04, 1.2839e-04,  ..., 2.7916e-05,
               2.7916e-05, 2.7916e-05],
              [1.2839e-04, 1.2839e-04, 1.2839e-04,  ..., 2.7916e-05,
               2.7916e-05, 2.7916e-05]],
    
             [[7.9368e-05, 7.9368e-05, 7.9368e-05,  ..., 9.0630e-06,
               9.0630e-06, 9.0630e-06],
              [7.9368e-05, 7.9368e-05, 7.9368e-05,  ..., 9.0630e-06,
               9.0630e-06, 9.0630e-06],
              [7.9368e-05, 7.9368e-05, 7.9368e-05,  ..., 9.0630e-06,
               9.0630e-06, 9.0630e-06],
              ...,
              [3.6166e-04, 3.6166e-04, 3.6166e-04,  ..., 2.9523e-05,
               2.9523e-05, 2.9523e-05],
              [3.6166e-04, 3.6166e-04, 3.6166e-04,  ..., 2.9523e-05,
               2.9523e-05, 2.9523e-05],
              [3.6166e-04, 3.6166e-04, 3.6166e-04,  ..., 2.9523e-05,
               2.9523e-05, 2.9523e-05]],
    
             ...,
    
             [[1.0186e-04, 1.0186e-04, 1.0186e-04,  ..., 5.8825e-05,
               5.8825e-05, 5.8825e-05],
              [1.0186e-04, 1.0186e-04, 1.0186e-04,  ..., 5.8825e-05,
               5.8825e-05, 5.8825e-05],
              [1.0186e-04, 1.0186e-04, 1.0186e-04,  ..., 5.8825e-05,
               5.8825e-05, 5.8825e-05],
              ...,
              [1.8186e-03, 1.8186e-03, 1.8186e-03,  ..., 2.1664e-04,
               2.1664e-04, 2.1664e-04],
              [1.8186e-03, 1.8186e-03, 1.8186e-03,  ..., 2.1664e-04,
               2.1664e-04, 2.1664e-04],
              [1.8186e-03, 1.8186e-03, 1.8186e-03,  ..., 2.1664e-04,
               2.1664e-04, 2.1664e-04]],
    
             [[9.5048e-04, 9.5048e-04, 9.5048e-04,  ..., 1.4954e-04,
               1.4954e-04, 1.4954e-04],
              [9.5048e-04, 9.5048e-04, 9.5048e-04,  ..., 1.4954e-04,
               1.4954e-04, 1.4954e-04],
              [9.5048e-04, 9.5048e-04, 9.5048e-04,  ..., 1.4954e-04,
               1.4954e-04, 1.4954e-04],
              ...,
              [8.1609e-04, 8.1609e-04, 8.1609e-04,  ..., 7.0914e-05,
               7.0914e-05, 7.0914e-05],
              [8.1609e-04, 8.1609e-04, 8.1609e-04,  ..., 7.0914e-05,
               7.0914e-05, 7.0914e-05],
              [8.1609e-04, 8.1609e-04, 8.1609e-04,  ..., 7.0914e-05,
               7.0914e-05, 7.0914e-05]],
    
             [[1.1444e-02, 1.1444e-02, 1.1444e-02,  ..., 4.8827e-05,
               4.8827e-05, 4.8827e-05],
              [1.1444e-02, 1.1444e-02, 1.1444e-02,  ..., 4.8827e-05,
               4.8827e-05, 4.8827e-05],
              [1.1444e-02, 1.1444e-02, 1.1444e-02,  ..., 4.8827e-05,
               4.8827e-05, 4.8827e-05],
              ...,
              [1.2948e-03, 1.2948e-03, 1.2948e-03,  ..., 5.0746e-05,
               5.0746e-05, 5.0746e-05],
              [1.2948e-03, 1.2948e-03, 1.2948e-03,  ..., 5.0746e-05,
               5.0746e-05, 5.0746e-05],
              [1.2948e-03, 1.2948e-03, 1.2948e-03,  ..., 5.0746e-05,
               5.0746e-05, 5.0746e-05]]]], device='cuda:0',
           grad_fn=<SoftmaxBackward0>)




```python

dog_and_person_masks = [
    normalized_masks[img_idx, sem_class_to_idx[cls]]
    for img_idx in range(len(img_list)) for cls in ('dog', 'person')    
]
show(dog_and_person_masks)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__60_0.webp)
    



```python
for cls in ('dog', 'person'):
    print(sem_class_to_idx[cls])
```

    12
    15



```python
class_dim = 1
boolean_dog_masks = (normalized_masks.argmax(dim = class_dim) == sem_class_to_idx['person']) | \
                    (normalized_masks.argmax(dim = class_dim) == sem_class_to_idx['dog'])  
# normalized_masks.shape # torch.Size([2, 21, 576, 768])
# boolean_dog_masks.shape # torch.Size([2, 576, 768])
```


```python
# torch.full((2, 3), 0.1, dtype = torch.bool)
# torch.ones((3, 4), dtype=torch.bool)
# torch.zeros((2, 3), dtype=torch.bool).float()
```




    tensor([[True, True, True],
            [True, True, True]])




```python
print(f"shape = {boolean_dog_masks.shape}, dtype = {boolean_dog_masks.dtype}")
show([m.float() for m in boolean_dog_masks])
```

    shape = torch.Size([2, 576, 768]), dtype = torch.bool



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__64_1.webp)
    


### Segmentation 마스크 


```python
from torchvision.utils import draw_segmentation_masks

dogs_with_masks = [
    draw_segmentation_masks(img, masks=mask, colors= "red", alpha=0.6)
    for img, mask in zip(img_list, boolean_dog_masks)
]
show(dogs_with_masks)
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_17%EC%B0%A8%EC%8B%9C__FasterRCNN_MaskedRCNN__66_0.webp)
    



## 강의_3기_AI개론_18차시__SSD_Yolo_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_18차시__SSD_Yolo_.ipynb)

# 18 객체 검출 (One-stage object detection)
- SSD, YOLO

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
# w = !apt install tree
# print(w[-2])
```

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
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

import os
import numpy as np
import matplotlib.pyplot as plt
# 폰트 관련 용도
import matplotlib.font_manager as fm
import cv2

import torch
from torch import nn, optim
import torchvision.transforms.functional as F
from torch.utils.data import DataLoader
from torchvision.io import read_image
from torchvision import models, datasets, transforms
from torchinfo import summary
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


## SSD 모델 사용하기

### 모델 불러 오기


```python
## Pretrained object detection model list
dir(models.detection)
```




    ['FCOS',
     'FCOS_ResNet50_FPN_Weights',
     'FasterRCNN',
     'FasterRCNN_MobileNet_V3_Large_320_FPN_Weights',
     'FasterRCNN_MobileNet_V3_Large_FPN_Weights',
     'FasterRCNN_ResNet50_FPN_V2_Weights',
     'FasterRCNN_ResNet50_FPN_Weights',
     'KeypointRCNN',
     'KeypointRCNN_ResNet50_FPN_Weights',
     'MaskRCNN',
     'MaskRCNN_ResNet50_FPN_V2_Weights',
     'MaskRCNN_ResNet50_FPN_Weights',
     'RetinaNet',
     'RetinaNet_ResNet50_FPN_V2_Weights',
     'RetinaNet_ResNet50_FPN_Weights',
     'SSD300_VGG16_Weights',
     'SSDLite320_MobileNet_V3_Large_Weights',
     '__builtins__',
     '__cached__',
     '__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__path__',
     '__spec__',
     '_utils',
     'anchor_utils',
     'backbone_utils',
     'faster_rcnn',
     'fasterrcnn_mobilenet_v3_large_320_fpn',
     'fasterrcnn_mobilenet_v3_large_fpn',
     'fasterrcnn_resnet50_fpn',
     'fasterrcnn_resnet50_fpn_v2',
     'fcos',
     'fcos_resnet50_fpn',
     'generalized_rcnn',
     'image_list',
     'keypoint_rcnn',
     'keypointrcnn_resnet50_fpn',
     'mask_rcnn',
     'maskrcnn_resnet50_fpn',
     'maskrcnn_resnet50_fpn_v2',
     'retinanet',
     'retinanet_resnet50_fpn',
     'retinanet_resnet50_fpn_v2',
     'roi_heads',
     'rpn',
     'ssd',
     'ssd300_vgg16',
     'ssdlite',
     'ssdlite320_mobilenet_v3_large',
     'transform']




```python
## load model
# from torchvision.models.detection import ssd300_vgg16 # input image 300x300, backbone vgg16

weights = models.detection.SSD300_VGG16_Weights.COCO_V1 # 2014
ssd300 = models.detection.ssd300_vgg16(weights = weights)
# weights.transforms()

```

### 모델 확인 하기


```python
print(ssd300)
```

    SSD(
      (backbone): SSDFeatureExtractorVGG(
        (features): Sequential(
          (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (1): ReLU(inplace=True)
          (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (3): ReLU(inplace=True)
          (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
          (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (6): ReLU(inplace=True)
          (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (8): ReLU(inplace=True)
          (9): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
          (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (11): ReLU(inplace=True)
          (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (13): ReLU(inplace=True)
          (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (15): ReLU(inplace=True)
          (16): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
          (17): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (18): ReLU(inplace=True)
          (19): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (20): ReLU(inplace=True)
          (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          (22): ReLU(inplace=True)
        )
        (extra): ModuleList(
          (0): Sequential(
            (0): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            (1): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (2): ReLU(inplace=True)
            (3): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (4): ReLU(inplace=True)
            (5): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (6): ReLU(inplace=True)
            (7): Sequential(
              (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=False)
              (1): Conv2d(512, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(6, 6), dilation=(6, 6))
              (2): ReLU(inplace=True)
              (3): Conv2d(1024, 1024, kernel_size=(1, 1), stride=(1, 1))
              (4): ReLU(inplace=True)
            )
          )
          (1): Sequential(
            (0): Conv2d(1024, 256, kernel_size=(1, 1), stride=(1, 1))
            (1): ReLU(inplace=True)
            (2): Conv2d(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
            (3): ReLU(inplace=True)
          )
          (2): Sequential(
            (0): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1))
            (1): ReLU(inplace=True)
            (2): Conv2d(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
            (3): ReLU(inplace=True)
          )
          (3-4): 2 x Sequential(
            (0): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1))
            (1): ReLU(inplace=True)
            (2): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1))
            (3): ReLU(inplace=True)
          )
        )
      )
      (anchor_generator): DefaultBoxGenerator(aspect_ratios=[[2], [2, 3], [2, 3], [2, 3], [2], [2]], clip=True, scales=[0.07, 0.15, 0.33, 0.51, 0.69, 0.87, 1.05], steps=[8, 16, 32, 64, 100, 300])
      (head): SSDHead(
        (classification_head): SSDClassificationHead(
          (module_list): ModuleList(
            (0): Conv2d(512, 364, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (1): Conv2d(1024, 546, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (2): Conv2d(512, 546, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (3): Conv2d(256, 546, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (4-5): 2 x Conv2d(256, 364, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          )
        )
        (regression_head): SSDRegressionHead(
          (module_list): ModuleList(
            (0): Conv2d(512, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (1): Conv2d(1024, 24, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (2): Conv2d(512, 24, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (3): Conv2d(256, 24, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (4-5): 2 x Conv2d(256, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
          )
        )
      )
      (transform): GeneralizedRCNNTransform(
          Normalize(mean=[0.48235, 0.45882, 0.40784], std=[0.00392156862745098, 0.00392156862745098, 0.00392156862745098])
          Resize(min_size=(300,), max_size=300, mode='bilinear')
      )
    )



```python
summary(ssd300, (1, 3, 300, 300))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    SSD                                      [97, 4]                   --
    ├─GeneralizedRCNNTransform: 1-1          [1, 3, 300, 300]          --
    ├─SSDFeatureExtractorVGG: 1-2            [1, 256, 1, 1]            512
    │    └─Sequential: 2-1                   [1, 512, 38, 38]          --
    │    │    └─Conv2d: 3-1                  [1, 64, 300, 300]         (1,792)
    │    │    └─ReLU: 3-2                    [1, 64, 300, 300]         --
    │    │    └─Conv2d: 3-3                  [1, 64, 300, 300]         (36,928)
    │    │    └─ReLU: 3-4                    [1, 64, 300, 300]         --
    │    │    └─MaxPool2d: 3-5               [1, 64, 150, 150]         --
    │    │    └─Conv2d: 3-6                  [1, 128, 150, 150]        73,856
    │    │    └─ReLU: 3-7                    [1, 128, 150, 150]        --
    │    │    └─Conv2d: 3-8                  [1, 128, 150, 150]        147,584
    │    │    └─ReLU: 3-9                    [1, 128, 150, 150]        --
    │    │    └─MaxPool2d: 3-10              [1, 128, 75, 75]          --
    │    │    └─Conv2d: 3-11                 [1, 256, 75, 75]          295,168
    │    │    └─ReLU: 3-12                   [1, 256, 75, 75]          --
    │    │    └─Conv2d: 3-13                 [1, 256, 75, 75]          590,080
    │    │    └─ReLU: 3-14                   [1, 256, 75, 75]          --
    │    │    └─Conv2d: 3-15                 [1, 256, 75, 75]          590,080
    │    │    └─ReLU: 3-16                   [1, 256, 75, 75]          --
    │    │    └─MaxPool2d: 3-17              [1, 256, 38, 38]          --
    │    │    └─Conv2d: 3-18                 [1, 512, 38, 38]          1,180,160
    │    │    └─ReLU: 3-19                   [1, 512, 38, 38]          --
    │    │    └─Conv2d: 3-20                 [1, 512, 38, 38]          2,359,808
    │    │    └─ReLU: 3-21                   [1, 512, 38, 38]          --
    │    │    └─Conv2d: 3-22                 [1, 512, 38, 38]          2,359,808
    │    │    └─ReLU: 3-23                   [1, 512, 38, 38]          --
    │    └─ModuleList: 2-2                   --                        --
    │    │    └─Sequential: 3-24             [1, 1024, 19, 19]         12,848,640
    │    │    └─Sequential: 3-25             [1, 512, 10, 10]          1,442,560
    │    │    └─Sequential: 3-26             [1, 256, 5, 5]            360,832
    │    │    └─Sequential: 3-27             [1, 256, 3, 3]            328,064
    │    │    └─Sequential: 3-28             [1, 256, 1, 1]            328,064
    ├─SSDHead: 1-3                           [1, 8732, 91]             --
    │    └─SSDRegressionHead: 2-3            [1, 8732, 4]              --
    │    │    └─ModuleList: 3-29             --                        534,648
    │    └─SSDClassificationHead: 2-4        [1, 8732, 91]             --
    │    │    └─ModuleList: 3-30             --                        12,163,242
    ├─DefaultBoxGenerator: 1-4               [8732, 4]                 --
    ==========================================================================================
    Total params: 35,641,826
    Trainable params: 35,603,106
    Non-trainable params: 38,720
    Total mult-adds (G): 34.88
    ==========================================================================================
    Input size (MB): 1.08
    Forward/backward pass size (MB): 208.89
    Params size (MB): 142.57
    Estimated Total Size (MB): 352.53
    ==========================================================================================



### 데이터 준비


```python
## Image preprocessing
transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor()
])

# transform = transforms.Compose([
#     transforms.Resize((300, 300)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.48235, 0.45882, 0.40784],  # Mean values for COCO (normalized to [0, 1])
#         std=[0.00392156862745098, 0.00392156862745098, 0.00392156862745098]  # Scale pixel values to [0, 1]
#     )
# ])
```


```python
# VOCDetection 데이터셋 불러오기
dataset = datasets.VOCDetection(root = "./VOC_dataset/VOC2012", 
                                year = "2012",
                                image_set = "val", # Use "train", "val", or "trainval"
                                download=True,
                                transform = transform # Apply preprocessing pipeline
                                )  

# data_loader = DataLoader(dataset, batch_size=1, shuffle=False)
```

    Using downloaded and verified file: ./VOC_dataset/VOC2012\VOCtrainval_11-May-2012.tar
    Extracting ./VOC_dataset/VOC2012\VOCtrainval_11-May-2012.tar to ./VOC_dataset/VOC2012


### 입력 영상 확인하기


```python
idx = torch.randint(len(dataset), size = (1, ))
image, annotation = dataset[idx.item()]


plt.imshow(image.permute(1, 2, 0))
plt.grid(None)
plt.axis("off")
plt.show()
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__20_0.webp)
    


### 모델 예측


```python
import time

idx = torch.randint(len(dataset), size = (1, ))
image_jpg, annotation = dataset[idx.item()]
image = image_jpg.unsqueeze(0).to(device)

ssd300.eval()
start = time.time()
with torch.no_grad():
    prediction = ssd300(image)
stop = time.time()
print(f"estimation time = {(stop - start)*1000:.3f}ms")
prediction = prediction[0] # batch remove
prediction
```

    estimation time = 185.503ms





    {'boxes': tensor([[1.1262e+02, 6.5100e+01, 2.1513e+02, 1.8358e+02],
             [8.8847e+01, 6.2713e+01, 2.4138e+02, 2.5318e+02],
             [8.2444e+00, 1.4865e+02, 2.9779e+02, 2.9904e+02],
             [2.4332e+02, 3.4011e+00, 2.9987e+02, 1.3884e+02],
             [1.8608e+01, 2.8053e+01, 6.6836e+01, 2.1345e+02],
             [6.5991e+00, 1.7761e+02, 1.5280e+02, 2.9850e+02],
             [1.1509e+02, 6.3359e+01, 1.7068e+02, 1.6076e+02],
             [1.5691e+02, 8.5306e+01, 2.3508e+02, 1.8724e+02],
             [7.1447e+01, 7.7665e+01, 1.6359e+02, 2.0069e+02],
             [2.5747e+02, 3.0218e+01, 2.9824e+02, 8.5727e+01],
             [2.4039e+01, 2.4206e+02, 5.2521e+01, 2.7752e+02],
             [2.7608e+01, 2.5449e+02, 4.7232e+01, 2.7788e+02],
             [1.2059e+02, 1.0803e+02, 1.5563e+02, 1.8187e+02],
             [1.4902e+02, 1.0802e+02, 1.9267e+02, 1.8077e+02],
             [1.3566e+01, 5.9837e+01, 2.9061e+02, 2.9515e+02],
             [1.3296e+02, 1.4723e+02, 2.0539e+02, 1.8141e+02],
             [1.2713e+02, 1.3802e+02, 2.1133e+02, 2.0558e+02],
             [3.2951e+01, 2.3434e+02, 2.3441e+02, 2.9992e+02],
             [1.3268e+02, 1.2623e+02, 1.7042e+02, 1.8729e+02],
             [1.1654e+02, 6.5065e+01, 1.6978e+02, 1.0808e+02],
             [2.6553e+01, 4.5842e+01, 5.2569e+01, 1.5028e+02],
             [1.8091e+02, 0.0000e+00, 3.0000e+02, 1.2458e+02],
             [2.0823e+00, 2.0143e+01, 4.6297e+01, 2.0735e+02],
             [2.4797e+02, 3.4914e+01, 2.8237e+02, 9.8553e+01],
             [2.4879e+01, 1.4781e+02, 5.2215e+01, 1.9713e+02],
             [1.5745e+02, 9.3629e+01, 2.0591e+02, 1.6235e+02],
             [2.7077e+01, 9.3283e+01, 5.0884e+01, 1.9975e+02],
             [1.1815e+02, 1.3531e+02, 1.9542e+02, 1.7165e+02],
             [2.3157e+02, 1.2944e+02, 2.6351e+02, 1.9811e+02],
             [2.0102e+01, 2.4127e+02, 6.5305e+01, 2.9298e+02],
             [1.7710e+02, 1.0589e+02, 2.1826e+02, 1.6936e+02],
             [2.2639e+02, 1.2053e+02, 2.9165e+02, 2.0699e+02],
             [1.6301e+02, 1.2347e+02, 2.0437e+02, 1.8570e+02],
             [1.3836e+02, 8.3384e+01, 1.9517e+02, 1.2312e+02],
             [1.1054e+02, 8.4607e+01, 1.7236e+02, 1.1847e+02],
             [2.0724e+02, 6.5498e+01, 2.8422e+02, 2.0185e+02],
             [2.6934e+00, 2.0977e+02, 3.9960e+01, 2.8771e+02],
             [2.6683e+02, 1.4120e+02, 2.9494e+02, 2.2982e+02],
             [1.2180e+02, 9.9138e+01, 1.7816e+02, 1.4173e+02],
             [2.0152e+02, 1.0903e+02, 2.3390e+02, 1.8048e+02],
             [0.0000e+00, 2.2842e+02, 1.1478e+02, 3.0000e+02],
             [2.6364e+02, 0.0000e+00, 2.9973e+02, 7.6078e+01],
             [2.4596e+02, 1.2570e+02, 2.7778e+02, 2.0292e+02],
             [1.9314e+01, 2.5186e+02, 3.6432e+01, 2.7902e+02],
             [1.4996e+02, 1.4922e+02, 1.8758e+02, 2.0706e+02],
             [1.2033e+01, 6.2718e+01, 2.9159e+02, 2.9673e+02],
             [1.1332e+02, 1.1368e+02, 1.6910e+02, 1.5642e+02],
             [1.3049e+02, 1.6908e+02, 2.0806e+02, 1.9631e+02],
             [9.2237e+01, 4.6891e+01, 2.1070e+02, 1.2619e+02],
             [2.0608e+02, 1.1134e+02, 2.3711e+02, 1.4633e+02],
             [1.6260e+02, 1.1726e+02, 2.2606e+02, 1.5392e+02],
             [2.1294e+02, 1.0853e+02, 2.5202e+02, 1.7428e+02],
             [2.3360e+02, 7.7548e+01, 2.9801e+02, 2.5035e+02],
             [7.2506e+00, 4.1083e+01, 3.4351e+01, 1.3887e+02],
             [9.9559e+01, 1.0104e+02, 1.5327e+02, 1.3836e+02],
             [1.0502e+02, 7.4723e+01, 1.4589e+02, 1.2955e+02],
             [2.0783e+02, 3.6051e+01, 2.9338e+02, 1.9183e+02],
             [1.6495e+02, 1.0280e+02, 2.2831e+02, 1.3913e+02],
             [1.0848e+02, 9.8211e+01, 1.3508e+02, 1.7177e+02],
             [5.5352e+01, 7.2755e+01, 1.9565e+02, 1.4870e+02],
             [2.4863e+01, 3.7728e+01, 5.6120e+01, 1.0224e+02],
             [1.4976e+02, 7.4522e+01, 1.8808e+02, 1.4709e+02],
             [1.6498e+02, 1.1065e+02, 2.5745e+02, 2.1685e+02],
             [1.5889e+02, 1.3491e+02, 2.2578e+02, 1.6964e+02],
             [1.9150e+02, 1.0100e+02, 2.4268e+02, 1.4255e+02],
             [3.4547e+01, 2.6295e+02, 5.0502e+01, 2.8572e+02],
             [2.6314e+01, 1.4489e+02, 5.1329e+01, 2.1413e+02],
             [0.0000e+00, 1.3025e+02, 2.6878e+01, 1.7329e+02],
             [6.5246e+01, 1.0600e+00, 1.4453e+02, 5.3497e+01],
             [1.7806e+02, 7.2294e+01, 3.0000e+02, 1.5203e+02],
             [2.2755e+02, 7.5259e-01, 2.9246e+02, 8.6693e+01],
             [4.9127e+01, 0.0000e+00, 1.1652e+02, 8.1133e+01],
             [1.6532e+02, 1.4815e+02, 2.0229e+02, 2.0515e+02],
             [1.7039e+02, 8.4908e+01, 2.2574e+02, 1.2609e+02],
             [4.1368e+01, 4.8671e+01, 7.0007e+01, 1.4585e+02],
             [2.2277e+02, 1.0083e+02, 2.7534e+02, 1.4145e+02],
             [2.6426e+02, 1.1098e+02, 2.9474e+02, 1.9126e+02],
             [3.4430e+00, 2.6317e+02, 3.3318e+01, 3.0000e+02],
             [2.3276e+02, 9.4717e+01, 2.6556e+02, 1.6255e+02],
             [4.3765e+01, 1.6596e+02, 1.1121e+02, 2.9378e+02],
             [1.3776e+02, 1.3873e+02, 1.6569e+02, 2.2108e+02],
             [5.3676e+01, 1.0546e+02, 2.0609e+02, 1.8247e+02],
             [2.2202e+01, 2.5698e+02, 5.1517e+01, 2.9284e+02],
             [9.3237e+01, 2.8046e+02, 1.0717e+02, 3.0000e+02],
             [1.2574e+02, 1.6765e+02, 2.0966e+02, 2.3383e+02],
             [0.0000e+00, 7.6399e+01, 7.8534e+01, 3.0000e+02],
             [3.8097e+01, 4.0502e+01, 7.4172e+01, 9.4964e+01],
             [2.0467e+02, 1.3025e+02, 3.0000e+02, 2.8190e+02],
             [1.7996e+02, 1.4716e+02, 2.1229e+02, 1.8205e+02],
             [2.4392e+01, 2.7371e+02, 5.7802e+01, 3.0000e+02],
             [1.9919e+02, 8.7053e+01, 2.9711e+02, 2.4591e+02],
             [1.2975e+02, 4.3949e+01, 2.7434e+02, 1.2061e+02],
             [6.1990e+00, 7.5520e+01, 3.5306e+01, 1.7568e+02],
             [1.8482e+02, 0.0000e+00, 3.0000e+02, 4.4032e+01],
             [5.2050e+00, 9.1122e+01, 3.6830e+01, 1.7597e+02],
             [1.0655e+02, 1.3738e+02, 1.7566e+02, 2.1477e+02],
             [1.1943e+02, 1.4556e+02, 1.5214e+02, 2.0964e+02],
             [2.2517e+02, 8.4079e+01, 2.7898e+02, 1.2491e+02],
             [2.6137e+02, 5.0318e+01, 2.9895e+02, 1.1613e+02],
             [2.7024e+02, 4.6286e+01, 2.9800e+02, 8.2859e+01],
             [8.6794e+01, 2.8234e+02, 9.8415e+01, 3.0000e+02],
             [7.7143e+01, 2.8459e+02, 8.8786e+01, 3.0000e+02],
             [1.3975e+02, 4.1382e+01, 2.9931e+02, 2.7759e+02],
             [3.4274e+00, 1.8143e+02, 3.7327e+01, 2.5543e+02],
             [2.1211e+02, 1.0421e+02, 2.4400e+02, 1.3496e+02],
             [1.6164e+02, 3.0446e+01, 2.9376e+02, 2.8220e+02],
             [9.7141e+01, 0.0000e+00, 3.0000e+02, 7.2839e+01],
             [9.0797e+00, 2.0628e+02, 1.4903e+02, 3.0000e+02],
             [2.8739e+01, 2.6654e+02, 4.7588e+01, 2.8149e+02],
             [7.6200e+01, 1.9732e+02, 1.4245e+02, 3.0000e+02],
             [1.8015e+02, 1.5688e+02, 1.9724e+02, 1.7510e+02],
             [1.0035e+02, 1.3206e+02, 1.5161e+02, 1.7284e+02],
             [1.2896e+02, 1.8451e+02, 2.0478e+02, 2.1493e+02],
             [1.5009e+02, 1.6989e+02, 1.8568e+02, 2.3226e+02],
             [2.0381e+02, 1.1824e+02, 2.6472e+02, 1.5338e+02],
             [4.5271e+01, 4.8017e+01, 5.9255e+01, 7.5684e+01],
             [2.4736e+02, 1.5845e+02, 2.7825e+02, 2.3631e+02],
             [0.0000e+00, 2.6236e-01, 3.9252e+01, 8.3543e+01],
             [1.8883e+02, 1.4010e+02, 2.0275e+02, 1.6926e+02],
             [2.3475e+02, 6.9016e+01, 2.6614e+02, 1.3673e+02],
             [0.0000e+00, 1.2234e+02, 2.6402e+02, 2.9557e+02],
             [9.0739e+01, 3.4670e+01, 1.5800e+02, 1.0362e+02],
             [7.0053e-01, 1.9191e+02, 2.5623e+01, 2.7361e+02],
             [0.0000e+00, 2.6236e-01, 3.9252e+01, 8.3543e+01],
             [1.8613e+02, 1.5526e+02, 2.0546e+02, 1.7521e+02],
             [1.4005e+01, 0.0000e+00, 8.4360e+01, 6.2809e+01],
             [2.0693e+02, 1.1127e+02, 2.8560e+02, 2.7764e+02],
             [2.1205e+01, 2.5996e+02, 3.5240e+01, 2.8987e+02],
             [3.4355e+01, 4.6169e+01, 5.0254e+01, 7.4532e+01],
             [2.3790e+02, 2.7117e+01, 2.6618e+02, 9.5413e+01],
             [2.1104e+02, 1.1435e+02, 2.3033e+02, 1.3614e+02],
             [2.3719e+01, 2.6946e+02, 3.4947e+01, 2.9880e+02],
             [5.4845e+01, 3.0641e+00, 8.4185e+01, 4.3762e+01],
             [1.2977e+02, 2.6673e+02, 1.6623e+02, 2.9949e+02],
             [7.7951e+01, 0.0000e+00, 1.4502e+02, 7.8170e+01],
             [4.4531e+01, 2.5518e+02, 5.9404e+01, 2.7930e+02],
             [2.7620e+01, 2.7103e+02, 4.5167e+01, 2.9764e+02],
             [2.1352e+02, 8.0281e+01, 2.5375e+02, 1.3187e+02],
             [2.4486e+01, 8.5836e+01, 5.1876e+01, 1.8861e+02],
             [0.0000e+00, 5.5516e+01, 1.0116e+01, 9.3727e+01],
             [1.3284e+00, 1.6610e+02, 5.0052e+01, 3.0000e+02],
             [1.3115e+01, 2.6681e+02, 2.7784e+01, 2.9891e+02],
             [2.7369e+00, 2.0024e+02, 3.1214e+01, 2.4118e+02],
             [1.6958e+02, 1.3649e+02, 2.0467e+02, 1.7422e+02],
             [3.4733e+01, 2.7246e+02, 5.2063e+01, 2.9659e+02],
             [1.1108e+02, 1.6895e+02, 1.7180e+02, 1.9890e+02],
             [2.2348e+01, 2.0286e+02, 5.5345e+01, 2.6822e+02],
             [2.1609e+02, 1.2373e+02, 2.4961e+02, 1.9544e+02],
             [1.8280e+02, 1.4747e+02, 1.9556e+02, 1.6378e+02],
             [4.8337e-01, 2.6548e+02, 1.8968e+01, 3.0000e+02],
             [8.0369e+01, 1.7715e+02, 2.9349e+02, 2.9746e+02],
             [3.6577e+01, 1.0696e+02, 5.1737e+01, 1.4984e+02],
             [0.0000e+00, 1.5419e+02, 2.8511e+01, 1.8973e+02],
             [1.1500e+00, 8.0133e+01, 2.2933e+01, 1.6802e+02],
             [1.2527e+01, 6.0236e+01, 2.8842e+02, 2.9003e+02],
             [9.2530e+00, 1.9297e+01, 3.1482e+01, 7.1072e+01],
             [2.6988e+02, 5.5862e+01, 2.9933e+02, 9.7382e+01],
             [1.6196e+01, 2.6468e+02, 4.6781e+01, 2.9977e+02],
             [1.0586e+00, 2.3826e+02, 6.0510e+01, 3.0000e+02],
             [2.2275e+02, 1.1363e+02, 2.3515e+02, 1.4041e+02],
             [1.4553e+01, 0.0000e+00, 1.4937e+02, 9.3181e+01],
             [1.8520e+01, 2.3740e+02, 3.6157e+01, 2.6781e+02],
             [1.9543e+00, 7.3124e+01, 4.0074e+01, 1.3744e+02],
             [2.5311e+01, 2.7842e+02, 3.4296e+01, 3.0000e+02],
             [6.5246e+01, 1.0600e+00, 1.4453e+02, 5.3497e+01],
             [6.2167e+00, 7.3394e+01, 6.4603e+01, 1.7249e+02],
             [4.3474e+01, 1.1921e+02, 6.7450e+01, 2.1057e+02],
             [0.0000e+00, 4.3247e+01, 1.6312e+02, 2.9152e+02],
             [2.9164e+01, 6.7715e+01, 5.5653e+01, 1.1601e+02],
             [6.0237e+00, 6.0450e+01, 1.9032e+01, 9.1025e+01],
             [2.8704e+02, 5.2506e+01, 2.9997e+02, 8.1833e+01],
             [6.1451e+00, 3.0641e+01, 1.7065e+01, 7.5105e+01],
             [1.0072e+02, 2.7757e+02, 1.1564e+02, 3.0000e+02],
             [2.7481e+02, 4.9030e+01, 2.9209e+02, 7.9942e+01],
             [2.8040e+02, 0.0000e+00, 3.0000e+02, 1.3579e+02],
             [2.6483e+02, 4.1991e+01, 2.9167e+02, 8.4969e+01],
             [1.4296e+02, 7.8226e+00, 2.6265e+02, 9.8022e+01],
             [2.5156e+02, 3.6799e+01, 2.8027e+02, 9.1022e+01],
             [1.1677e+01, 2.0524e+02, 2.7458e+01, 2.3653e+02],
             [2.8534e+02, 1.1165e+02, 2.9798e+02, 1.6020e+02],
             [2.3253e+02, 1.6188e+02, 2.8907e+02, 2.0202e+02],
             [1.4264e+01, 2.3510e+02, 8.2463e+01, 2.9864e+02],
             [2.1017e+00, 0.0000e+00, 3.4675e+01, 8.8614e+01],
             [1.7790e+00, 4.1898e+01, 2.2267e+01, 1.3345e+02],
             [1.1363e+02, 2.6574e+02, 1.4332e+02, 2.9985e+02],
             [2.8704e+02, 5.2506e+01, 2.9997e+02, 8.1833e+01],
             [2.5011e+02, 6.3502e-01, 2.8413e+02, 7.0594e+01],
             [7.0394e+01, 2.7544e+02, 9.9670e+01, 3.0000e+02],
             [1.6091e+02, 1.7158e+02, 2.5516e+02, 2.9511e+02],
             [2.8069e+01, 2.7779e+02, 4.3785e+01, 3.0000e+02],
             [9.8555e+00, 1.1961e+02, 6.6770e+01, 2.0918e+02],
             [2.2301e+02, 1.1039e+02, 2.4986e+02, 1.4078e+02],
             [3.9344e+00, 2.5360e+02, 4.8506e+01, 2.9934e+02],
             [2.7471e+02, 6.5201e+01, 2.9317e+02, 8.5715e+01],
             [2.1740e+01, 1.9924e+02, 3.3347e+01, 2.3876e+02],
             [0.0000e+00, 1.8690e+02, 2.6029e+01, 2.3328e+02],
             [3.4590e+01, 2.2481e+02, 7.2581e+01, 2.8204e+02],
             [0.0000e+00, 2.3549e+02, 2.8934e+01, 2.9230e+02],
             [1.1500e+00, 8.0133e+01, 2.2933e+01, 1.6802e+02],
             [2.9411e+02, 1.1617e+02, 3.0000e+02, 1.3939e+02]], device='cuda:0'),
     'scores': tensor([0.9462, 0.1989, 0.1664, 0.1032, 0.0894, 0.0836, 0.0830, 0.0819, 0.0794,
             0.0723, 0.0723, 0.0720, 0.0700, 0.0675, 0.0648, 0.0641, 0.0613, 0.0606,
             0.0600, 0.0597, 0.0590, 0.0560, 0.0547, 0.0541, 0.0538, 0.0532, 0.0518,
             0.0517, 0.0501, 0.0501, 0.0498, 0.0497, 0.0493, 0.0491, 0.0490, 0.0475,
             0.0475, 0.0471, 0.0465, 0.0463, 0.0462, 0.0459, 0.0454, 0.0445, 0.0434,
             0.0433, 0.0432, 0.0425, 0.0419, 0.0419, 0.0419, 0.0416, 0.0416, 0.0409,
             0.0404, 0.0398, 0.0398, 0.0397, 0.0396, 0.0395, 0.0387, 0.0385, 0.0382,
             0.0369, 0.0369, 0.0366, 0.0363, 0.0354, 0.0352, 0.0350, 0.0349, 0.0345,
             0.0343, 0.0341, 0.0339, 0.0331, 0.0327, 0.0324, 0.0323, 0.0320, 0.0320,
             0.0318, 0.0317, 0.0317, 0.0316, 0.0315, 0.0313, 0.0308, 0.0308, 0.0307,
             0.0304, 0.0302, 0.0302, 0.0301, 0.0300, 0.0297, 0.0297, 0.0297, 0.0297,
             0.0297, 0.0295, 0.0294, 0.0294, 0.0293, 0.0293, 0.0293, 0.0292, 0.0291,
             0.0291, 0.0289, 0.0284, 0.0282, 0.0282, 0.0281, 0.0279, 0.0277, 0.0277,
             0.0277, 0.0276, 0.0273, 0.0272, 0.0272, 0.0271, 0.0271, 0.0270, 0.0270,
             0.0268, 0.0267, 0.0265, 0.0265, 0.0264, 0.0262, 0.0261, 0.0259, 0.0259,
             0.0258, 0.0258, 0.0257, 0.0256, 0.0255, 0.0255, 0.0254, 0.0254, 0.0252,
             0.0251, 0.0251, 0.0250, 0.0249, 0.0249, 0.0247, 0.0245, 0.0243, 0.0241,
             0.0240, 0.0238, 0.0237, 0.0236, 0.0235, 0.0231, 0.0229, 0.0229, 0.0229,
             0.0228, 0.0228, 0.0228, 0.0227, 0.0225, 0.0224, 0.0221, 0.0220, 0.0220,
             0.0220, 0.0220, 0.0219, 0.0218, 0.0217, 0.0216, 0.0216, 0.0216, 0.0214,
             0.0212, 0.0211, 0.0211, 0.0211, 0.0210, 0.0210, 0.0208, 0.0207, 0.0207,
             0.0206, 0.0205, 0.0205, 0.0205, 0.0203, 0.0203, 0.0203, 0.0202, 0.0202,
             0.0201, 0.0201], device='cuda:0'),
     'labels': tensor([16, 16,  2, 64, 44,  2, 16, 16, 16, 86, 44, 44, 16, 16, 64, 16, 16,  2,
             16, 16, 44, 64, 44, 86, 47, 16, 44, 16, 86, 44, 16, 86, 16, 16, 16, 16,
             44, 86, 16, 16,  2, 64, 86, 44, 16, 61, 16, 16, 16, 62, 16, 16, 86, 44,
             16, 16, 64, 16, 16, 16, 44, 16, 16, 16, 16, 44, 44, 62, 31, 16, 64,  1,
             16, 16, 44, 16, 86, 62, 16,  2, 16, 16, 44,  1, 16,  2, 44, 86, 52, 62,
             64, 16, 44, 64, 47, 16, 16, 16, 86, 31,  1,  1, 16, 44, 62, 64, 64,  4,
             44,  2, 52, 16, 16, 16, 16, 44, 86, 31, 52, 16,  4, 16, 44, 27, 52,  1,
             62, 44, 44, 86, 62, 44,  1, 47,  1, 44, 44, 16, 47,  1,  2, 62, 62, 52,
             44, 16, 44, 86, 52, 62, 62, 44, 62, 47, 86,  1, 62, 62,  2, 62,  1, 44,
             47, 62, 27, 47, 44,  2, 47,  1, 62,  1,  1, 62, 64, 62, 64, 62, 62,  1,
             86,  4, 44, 44, 47, 31, 64,  1, 62, 62, 47, 62, 44, 31, 62,  1, 44, 44,
             44,  1], device='cuda:0')}



### Bounding box 그리기


```python

image = image.cpu().data[0]
image = transforms.functional.to_pil_image(image)
image = np.array(image)

threshold=0.5

for box, label, score in zip(prediction["boxes"], prediction["labels"], prediction["scores"]):
    if score > threshold:
        box = list(map(int, box))
        print(box)
        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2, cv2.LINE_AA)

fig, axs = plt.subplots(1, 2, figsize = (10, 5))

axs[0].imshow(image_jpg.permute(1, 2, 0))
axs[0].grid(None)
axs[1].imshow(image)
axs[1].grid(None)
plt.show()

```

    [112, 65, 215, 183]



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__24_1.webp)
    


## SSD + CV DNN 얼굴검출
- https://github.com/spmallick/learnopencv/tree/master/AgeGender


```python
import numpy as np
import sys
import cv2
import pandas as pd
img = cv2.imread('./figure/king_face.png')

if img is None:
    print('image read failed')
    sys.exit()

## tensorflow model   
model = './opencv_face_detector/opencv_face_detector_uint8.pb'
config = './opencv_face_detector/opencv_face_detector.pbtxt'

face_net = cv2.dnn.readNet(model, config)
# face_net.getLayerNames()

if face_net.empty():
    print('Net open failed')
    sys.exit()

# blobFromImage(image[, scalefactor[, size[, mean[, swapRB[, crop[, ddepth]]]]]]) -> retval
blob = cv2.dnn.blobFromImage(img, 1, (300, 300), (104, 177, 123),
                            swapRB=False)

face_net.setInput(blob)
out = face_net.forward()

labels = ["img_id", "is_face", "confidence", "left", "top", "right", "bottom"]
out_df = pd.DataFrame(out[0][0], columns = labels)
print(out_df)

```

         img_id  is_face  confidence      left       top     right    bottom
    0       0.0      1.0    0.989431  0.825202  0.502988  0.893821  0.658601
    1       0.0      1.0    0.950553  0.147596  0.511079  0.215222  0.681570
    2       0.0      1.0    0.947276  0.288199  0.444965  0.359195  0.628823
    3       0.0      1.0    0.920967  0.499137  0.392986  0.589955  0.570557
    4       0.0      1.0    0.835135  0.642767  0.463616  0.720524  0.659535
    ..      ...      ...         ...       ...       ...       ...       ...
    195     0.0      0.0    0.000000  0.000000  0.000000  0.000000  0.000000
    196     0.0      0.0    0.000000  0.000000  0.000000  0.000000  0.000000
    197     0.0      0.0    0.000000  0.000000  0.000000  0.000000  0.000000
    198     0.0      0.0    0.000000  0.000000  0.000000  0.000000  0.000000
    199     0.0      0.0    0.000000  0.000000  0.000000  0.000000  0.000000
    
    [200 rows x 7 columns]



```python

detect = out[0, 0, :, :]
h, w = img.shape[:2]

for i in range(detect.shape[0]):
    confidence = detect[i, 2] # (0, 1, confidence, x1, y1, x2, y2)
    
    if confidence > 0.15:
        # out matrix에서 x1, y1, x2, y2 값이 0 ~1로 normalize 되어 있음
        
        x1 = int(detect[i, 3]*w)
        y1 = int(detect[i, 4]*h)
        x2 = int(detect[i, 5]*w)
        y2 = int(detect[i, 6]*h)
        
        cv2.rectangle(img, (x1, y1), (x2, y2),
                     (0, 0, 255), 2)
        
        text = 'Face: {}%'.format(round(confidence*100, 2))
        cv2.putText(img, text, (x1, y1-1), cv2.FONT_HERSHEY_SIMPLEX,
                   0.8, (0, 0, 255), 1, cv2.LINE_AA)
        
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(figsize = (8,8))
plt.imshow(img)
plt.grid(None)
plt.axis("off")
plt.show()
```


    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__27_0.webp)
    


## Yolo v3 객체검출 with opencv dnn


```python
# https://pjreddie.com/darknet/yolo/

# NMSBoxes(bboxes, scores, score_threshold, nms_threshold) -> indices
# nms_threshold: nms_threshold a threshold used in non maximum suppression

# getPerfProfile() -> retval, timings
# .   @brief Returns overall time for inference and timings (in ticks) for layers.

# https://github.com/pjreddie/darknet/blob/master/data/coco.names
```


```python
## Automating with K-Means in Python

import numpy as np
from sklearn.cluster import KMeans

# Example bounding boxes (width, height)
bboxes = np.array([[32, 32], [64, 64], 
                   [128, 128], [256, 256], 
                   [512, 512], [128, 64], 
                   [64, 128], [256, 128]])

# Perform K-means clustering with k=9
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(bboxes)

# Output anchor boxes
anchors = kmeans.cluster_centers_
print("Anchors:", anchors)

```

    Anchors: [[512.  512. ]
     [ 83.2  83.2]
     [256.  192. ]]



```python
import sys
import numpy as np
import cv2

# 모델 & 설정 파일
model = './yolo_v3_pb/yolov3.weights'
config = './yolo_v3_pb/yolov3.cfg'
class_labels = './yolo_v3_pb/coco.names'

# 테스트 이미지 파일
img_files = ['./figure/dog.jpg', 
             './figure/person.jpg', 
             './figure/sheep.jpg', 
             './figure/kite.jpg']


# 네트워크 생성
net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    sys.exit()

# 클래스 이름 불러오기
classes = []
with open(class_labels, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# colors = np.random.uniform(0, 255, size=(len(classes), 3))
# colors = np.array([[0, 0, 255], 
#                    [255, 0, 0],
#                    [0, 255, 0],
#                    [0, 255, 255],
#                    [255, 255, 0],
#                    [255, 0, 255]])

# 출력 레이어 이름 받아오기
net.getUnconnectedOutLayers()
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
print(output_layers)
```

    ['yolo_82', 'yolo_94', 'yolo_106']



```python
# outs는 3개의 ndarray 리스트.
# output_layers = ['yolo_82', 'yolo_94', 'yolo_106']
# output_layers[0].shape = (507, 85), 13*13*3
# output_layers[1].shape = (2028, 85), 26*26*3
# output_layers[2].shape = (8112, 85), 52*52*3
import time

confThreshold = 0.5
nmsThreshold = 0.4

# 실행
print(img_files)
for i in img_files:
    img = cv2.imread(i)

    if img is None:
        continue

    # 블롭 생성 & 추론
    blob = cv2.dnn.blobFromImage(img, 1/255., (320, 320), swapRB=True)
    # blob = cv2.dnn.blobFromImage(img, 1/255., (416, 416), swapRB=True)
    # blob = cv2.dnn.blobFromImage(img, 1/255., (608, 608), swapRB=True)

    net.setInput(blob)
    outs = net.forward(output_layers) 

    # outs[0].shape=(507, 85), 13*13*3=507
    # outs[1].shape=(2028, 85), 26*26*3=2028
    # outs[2].shape=(8112, 85), 52*52*3=8112

    h, w = img.shape[:2]

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            # detection: 4(bounding box) + 1(objectness_score) + 80(class confidence)
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confThreshold:
                # 바운딩 박스 중심 좌표 & 박스 크기
                cx = int(detection[0] * w)
                cy = int(detection[1] * h)
                bw = int(detection[2] * w)
                bh = int(detection[3] * h)

                # 바운딩 박스 좌상단 좌표
                sx = int(cx - bw / 2)
                sy = int(cy - bh / 2)

                boxes.append([sx, sy, bw, bh])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    # 비최대 억제, Non Max Suppression
# https://deep-learning-study.tistory.com/403
# nmsThreshold: Determines the IoU (Intersection over Union) threshold
# A higher value results in more boxes being retained.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    for i in indices:
#         i = i[0]
        sx, sy, bw, bh = boxes[i]
        label = f'{classes[class_ids[i]]}: {confidences[i]:.2}'
        # color = colors[class_ids[i]]
        color = (0, 0, 255)
        cv2.rectangle(img, (sx, sy, bw, bh), color, 2)
        cv2.putText(img, label, (sx, sy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

    t, _ = net.getPerfProfile() # Total number of ticks spent during the last forward() call.
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 1, cv2.LINE_AA)
    
    img  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.grid(None)
    plt.axis("off")
    plt.show()
```

    ['./figure/dog.jpg', './figure/person.jpg', './figure/sheep.jpg', './figure/kite.jpg']



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__32_1.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__32_2.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__32_3.webp)
    



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__32_4.webp)
    


## Yolo v10 객체검출 with pytorch


```python
!pip install ultralytics
```


```python
from ultralytics import YOLO
```


```python
## coco dataset
# 클래스 이름 불러오기
# classNames = []
with open(class_labels, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#               "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
#               "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#               "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#               "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
#               "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
#               "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
#               "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
#               "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
#               "teddy bear", "hair drier", "toothbrush"
#               ]
```


```python
import time

data_dir = "./figure"

img_path = os.path.join(data_dir, "peoples.jpg")
img = cv2.imread(img_path)

if img is None:
    print("Image read failed")
    sys.exit()

model = YOLO("yolo11x.pt")  # load a pretrained model (recommended for training)

start = time.time()
detection = model(img, verbose=False)[0]
stop = time.time()
on_time = (stop - start)*1000
print(f"estimation time = {on_time:.3f}ms")
fps = f'{1000 / on_time:.4f} fps'
CONFIDENCE_THRESHOLD = 0.6

for data in detection.boxes.data.tolist():
        confidence = data[4]
        if confidence < CONFIDENCE_THRESHOLD:
            continue
        
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(img, classNames[label]+ ' ' +str(round(confidence, 2))+'%', 
        (xmin, ymin-5), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 1)        

    
        cv2.putText(img, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)


img  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.grid(None)
plt.axis("off")
plt.show()
```

    estimation time = 701.129ms



    
![png](../assets/images/ai/object-detection/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_18%EC%B0%A8%EC%8B%9C__SSD_Yolo__37_1.webp)
    

