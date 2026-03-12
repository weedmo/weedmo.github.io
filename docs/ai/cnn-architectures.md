# CNN 아키텍처


## 강의_3기_AI개론_11차시__CNN_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_11차시__CNN_.ipynb)

# 11장 CNN을 활용한 이미지 인식

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
import torch
from torch import nn, optim
from torchinfo import summary
from torchviz import make_dot
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
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

### GPU 확인하기


```python
# 디바이스 할당

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
```

    cpu


## CNN의 처리 개요


```python
data_root = './data'

# 샘플 손글씨 숫자 데이터 가져오기
transform = transforms.Compose([
    transforms.ToTensor(),
])

train_set = datasets.MNIST(
    root = data_root,
    train = True,
    download = True,
    transform = transform)

image, label = train_set[0]  # torch.Size([1, 28, 28])
image = image.view(1,1,28,28)
```

    Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz to ./data/MNIST/raw/train-images-idx3-ubyte.gz


    100%|██████████| 9.91M/9.91M [00:00<00:00, 52.6MB/s]


    Extracting ./data/MNIST/raw/train-images-idx3-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz to ./data/MNIST/raw/train-labels-idx1-ubyte.gz


    100%|██████████| 28.9k/28.9k [00:00<00:00, 2.04MB/s]


    Extracting ./data/MNIST/raw/train-labels-idx1-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw/t10k-images-idx3-ubyte.gz


    100%|██████████| 1.65M/1.65M [00:00<00:00, 14.1MB/s]


    Extracting ./data/MNIST/raw/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 404: Not Found
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz


    100%|██████████| 4.54k/4.54k [00:00<00:00, 7.70MB/s]


    Extracting ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw
    



```python
# 대각선상에만 가중치를 갖는 특수한 합성곱 함수를 만듦
conv1 = nn.Conv2d(1, 1, 3)
print("conv1.weight.shape = ", conv1.weight.shape) # [outputs, channel, kernel size (3x3)]
print("="*50)
print("conv1.weight = \n", conv1.weight)
print("conv1.bias = ", conv1.bias)

# bias를 0으로
nn.init.constant_(conv1.bias, 0.0)
# conv1.bias.data = torch.tensor([0]).float()
```

    conv1.weight.shape =  torch.Size([1, 1, 3, 3])
    ==================================================
    conv1.weight = 
     Parameter containing:
    tensor([[[[-0.0957,  0.1489, -0.0058],
              [ 0.0169, -0.1085, -0.1669],
              [-0.1860,  0.1392, -0.2057]]]], requires_grad=True)
    conv1.bias =  Parameter containing:
    tensor([-0.1928], requires_grad=True)





    Parameter containing:
    tensor([0.], requires_grad=True)




```python

# weight를 특수한 값으로
w1_np = np.array([[0,0,1],[0,1,0],[1,0,0]])
print("w1_np = \n", w1_np)
w1 = torch.tensor(w1_np).float() # torch.Size([3, 3])
w1 = w1.view(1,1,3,3)
conv1.weight.data = w1
# conv1.weight
```

    w1_np = 
     [[0 0 1]
     [0 1 0]
     [1 0 0]]



```python
# 손글씨 숫자에 3번 합성곱 처리를 함
import cv2

image, label = train_set[0] # torch.Size([1, 28, 28])
image = image.view(1,1,28,28)
w1 = conv1(image)
w2 = conv1(w1)
w3 = conv1(w2)
images = [image, w1, w2, w3]
```


```python
# 결과 화면 출력

plt.figure(figsize=(5, 1))
for i in range(4):
    size = (28 - i*2)
    ax = plt.subplot(1, 4, i+1)
    img = images[i].data.numpy()
    plt.imshow(img.reshape(size, size),cmap='gray_r')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__15_0.webp)
    


### nn.Conv2d 와 nn.MaxPool2d


```python
# CNN 모델 전반 부분, 레이어 함수 정의
# torch.nn.Conv2d(in_channels, out_channels, kernel_size,
#                 stride=1, padding=0, dilation=1, groups=1,
#                 bias=True, padding_mode='zeros', device=None, dtype=None)

conv1 = nn.Conv2d(3, 32, 3)
relu = nn.ReLU(inplace=True)
conv2 = nn.Conv2d(32, 32, 3)
maxpool = nn.MaxPool2d((2, 2))

print("conv1.weight.shape = \n", conv1.weight.shape)
```

    conv1.weight.shape = 
     torch.Size([32, 3, 3, 3])



```python
# conv1 확인
print("conv1")
print(conv1)

# conv1 내부 변수의 shape 확인
print(conv1.weight.shape) # torch.Size([32, 3, 3, 3]), (N, C, H, W)
print(conv1.bias.shape)

# conv2 내부 변수의 shape 확인
print("="*50)
print("conv2")
print(conv2.weight.shape)
print(conv2.bias.shape)
```

    conv1
    Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1))
    torch.Size([32, 3, 3, 3])
    torch.Size([32])
    ==================================================
    conv2
    torch.Size([32, 32, 3, 3])
    torch.Size([32])



```python
# conv1의 weight[0]는 0번째 출력 채널의 가중치
w = conv1.weight[0]

# weight[0]의 shape과 값 확인
print(w.shape)
print(w.data.numpy())
```

    torch.Size([3, 3, 3])
    [[[ 0.016   0.1674  0.0329]
      [-0.1008 -0.0676 -0.101 ]
      [ 0.0564  0.1219 -0.1526]]
    
     [[-0.1257 -0.1425 -0.1288]
      [ 0.0243  0.0016 -0.122 ]
      [ 0.0139 -0.0518  0.1894]]
    
     [[-0.0984 -0.0113 -0.1561]
      [ 0.      0.006   0.0492]
      [-0.0433  0.1602  0.1758]]]



```python
# 더미로 입력과 같은 사이즈를 갖는 텐서를 생성
inputs = torch.randn(100, 3, 32, 32)
print(inputs.shape)

## image show
plt.imshow(inputs[0].permute(1, 2, 0))
plt.show()
```

    WARNING:matplotlib.image:Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers). Got range [-3.3060312..3.282588].


    torch.Size([100, 3, 32, 32])



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__20_2.webp)
    



```python
inputs.shape
```




    torch.Size([100, 3, 32, 32])




```python
# CNN 전반부 처리 시뮬레이션

x1 = conv1(inputs) # input size = torch.Size([100, 3, 32, 32])
x2 = relu(x1)
x3 = conv2(x2)
x4 = relu(x3)
x5 = maxpool(x4)
```


```python
# 각 변수의 shape 확인

print(inputs.shape)
print(x1.shape)
print(x2.shape)
print(x3.shape)
print(x4.shape)
print(x5.shape)
```

    torch.Size([100, 3, 32, 32])
    torch.Size([100, 32, 30, 30])
    torch.Size([100, 32, 30, 30])
    torch.Size([100, 32, 28, 28])
    torch.Size([100, 32, 28, 28])
    torch.Size([100, 32, 14, 14])


### nn.Sequential


```python
# conv1 = nn.Conv2d(3, 32, 3)
# relu = nn.ReLU(inplace=True)
# conv2 = nn.Conv2d(32, 32, 3)
# maxpool = nn.MaxPool2d((2, 2))

# 함수 정의
features = nn.Sequential(
    conv1,
    relu,
    conv2,
    relu,
    maxpool
)

# 동작 테스트
outputs = features(inputs)
```


```python
# 동작 테스트
outputs = features(inputs)

# 결과 확인
print(outputs.shape)
```

    torch.Size([100, 32, 14, 14])


### nn.Flatten


```python
# 함수 정의
flatten = nn.Flatten()

# 동작 테스트
outputs2 = flatten(outputs)

# 결과 확인
print(outputs.shape)
print(outputs2.shape)
```

    torch.Size([100, 32, 14, 14])
    torch.Size([100, 6272])


### eval_loss(손실 계산)


```python
# 손실 계산용
def eval_loss(loader, device, net, criterion):

    # 데이터로더에서 처음 한 개 세트를 가져옴
    for images, labels in loader:
        break

    # 디바이스 할당
    inputs = images.to(device)
    labels = labels.to(device)

    # 예측 계산
    outputs = net(inputs)

    # 손실 계산
    loss = criterion(outputs, labels)

    return loss
```

### fit(학습)


```python
# 학습용 함수
def fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history):

    # tqdm 라이브러리 임포트
    from tqdm.notebook import tqdm

    base_epochs = len(history) # => 0
    batch_size_train = len(train_loader)
    batch_size_test = len(test_loader)

    for epoch in range(base_epochs, num_epochs+base_epochs):
        train_loss = 0
        train_acc = 0
        val_loss = 0
        val_acc = 0

        # 훈련 페이즈
        net.train() # dropout, batch normalization 활성화
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

            # 손실과 정확도 계산
        avg_train_loss = train_loss / batch_size_train
        avg_train_acc = train_acc / batch_size_train

        # 예측 페이즈
        net.eval()
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

            # 손실과 정확도 계산
        avg_val_loss = val_loss / batch_size_test
        avg_val_acc = val_acc / batch_size_test

        print (f'Epoch [{(epoch+1)}/{num_epochs+base_epochs}], loss: {avg_train_loss:.5f} acc: {avg_train_acc:.5f} val_loss: {avg_val_loss:.5f}, val_acc: {avg_val_acc:.5f}')
        item = np.array([epoch+1, avg_train_loss, avg_train_acc, avg_val_loss, avg_val_acc])
        history = np.vstack((history, item))
    return history
```

### eval_history(학습 로그)


```python
# 학습 로그 해석

def evaluate_history(history):
    # 손실과 정확도 확인
    print(f'초기상태 : 손실 : {history[0,3]:.5f}  정확도 : {history[0,4]:.5f}')
    print(f'최종상태 : 손실 : {history[-1,3]:.5f}  정확도 : {history[-1,4]:.5f}' )

    num_epochs = len(history)
    unit = num_epochs / 10

    # 학습 곡선 출력(손실)
    plt.figure(figsize=(9,8))
    plt.plot(history[:,0], history[:,1], 'b', label='훈련')
    plt.plot(history[:,0], history[:,3], 'k', label='검증')
    plt.xticks(np.arange(0,num_epochs+1, unit))
    plt.xlabel('반복 횟수')
    plt.ylabel('손실')
    plt.title('학습 곡선(손실)')
    plt.legend()
    plt.show()

    # 학습 곡선 출력(정확도)
    plt.figure(figsize=(9,8))
    plt.plot(history[:,0], history[:,2], 'b', label='훈련')
    plt.plot(history[:,0], history[:,4], 'k', label='검증')
    plt.xticks(np.arange(0,num_epochs+1,unit))
    plt.xlabel('반복 횟수')
    plt.ylabel('정확도')
    plt.title('학습 곡선(정확도)')
    plt.legend()
    plt.show()
```

### show_images_labels(예측 결과 표시)


```python
# 이미지와 라벨 표시
def show_images_labels(loader, classes, net, device):

    # 데이터로더에서 처음 1세트를 가져오기
    for images, labels in loader:
        break
    # 표시 수는 50개
    n_size = min(len(images), 50)
    print("n_size = ", n_size)

    if net is not None:
      # 디바이스 할당
      inputs = images.to(device)
      labels = labels.to(device)

      # 예측 계산
      outputs = net(inputs)
      predicted = torch.max(outputs,1)[1]
      #images = images.to('cpu')

    # 처음 n_size개 표시
    plt.figure(figsize=(20, 15))
    for i in range(n_size):
        ax = plt.subplot(5, 10, i + 1)
        label_name = classes[labels[i]]
        # net이 None이 아닌 경우는 예측 결과도 타이틀에 표시함
        if net is not None:
          predicted_name = classes[predicted[i]]
          # 정답인지 아닌지 색으로 구분함
          if label_name == predicted_name:
            c = 'k'
          else:
            c = 'b'
          ax.set_title(label_name + ':' + predicted_name, c=c, fontsize=20)
        # net이 None인 경우는 정답 라벨만 표시
        else:
          ax.set_title(label_name, fontsize=20)
        # 텐서를 넘파이로 변환
        image_np = images[i].numpy().copy()
        # 축의 순서 변경 (channel, row, column) -> (row, column, channel)
        img = np.transpose(image_np, (1, 2, 0))
        # 값의 범위를[-1, 1] -> [0, 1]로 되돌림
        img = (img + 1)/2
        # 결과 표시
        plt.imshow(img)
        ax.set_axis_off()
    plt.show()

```

### torch_seed(난수 초기화)


```python
# 파이토치 난수 고정

def torch_seed(seed=123):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True #
    torch.use_deterministic_algorithms = True
```

### 데이터 준비


```python
# Transforms의 정의

# transformer1 1계 텐서화

transform1 = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5),
    transforms.Lambda(lambda x: x.view(-1)),
])

# transformer2 정규화만 실시

# 검증 데이터용 : 정규화만 실시
transform2 = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5),
])
```


```python
# 데이터 취득용 함수 datasets

data_root = './data'

# 훈련 데이터셋 (1계 텐서 버전)
train_set1 = datasets.CIFAR10(
    root = data_root,
    train = True,
    download = True,
    transform = transform1)

# 검증 데이터셋 (1계 텐서 버전)
test_set1 = datasets.CIFAR10(
    root = data_root,
    train = False,
    download = True,
    transform = transform1)

# 훈련 데이터셋 (3계 텐서 버전)
train_set2 = datasets.CIFAR10(
    root =  data_root,
    train = True,
    download = True,
    transform = transform2)

# 검증 데이터셋 (3계 텐서 버전)
test_set2 = datasets.CIFAR10(
    root = data_root,
    train = False,
    download = True,
    transform = transform2)
```

    Downloading https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz to ./data/cifar-10-python.tar.gz


    100%|██████████| 170M/170M [00:07<00:00, 24.3MB/s]


    Extracting ./data/cifar-10-python.tar.gz to ./data
    Files already downloaded and verified
    Files already downloaded and verified
    Files already downloaded and verified


### 데이터셋 확인


```python
len(train_set1)
```




    50000




```python
image1, label1 = train_set1[0] # 3 x 32 x 32 = [3072]
image2, label2 = train_set2[0]

print(image1.shape)
print(image2.shape)
```

    torch.Size([3072])
    torch.Size([3, 32, 32])



```python
# 데이터로더 정의

# 미니 배치 사이즈 지정
batch_size = 100

# 훈련용 데이터로더
# 훈련용이므로 셔플을 True로 설정
train_loader1 = DataLoader(train_set1, batch_size=batch_size, shuffle=True)

# 검증용 데이터로더
# 검증용이므로 셔플하지 않음
test_loader1 = DataLoader(test_set1,  batch_size=batch_size, shuffle=False)

# 훈련용 데이터로더
# 훈련용이므로 셔플을 True로 설정
train_loader2 = DataLoader(train_set2, batch_size=batch_size, shuffle=True)

# 검증용 데이터로더
# 검증용이므로 셔플하지 않음
test_loader2 = DataLoader(test_set2,  batch_size=batch_size, shuffle=False)

```


```python
len(train_loader1)
```




    500




```python
# train_loader1에서 한 세트 가져오기
for images1, labels1 in train_loader1:
    break

# train_loader2에서 한 세트 가져오기
for images2, labels2 in train_loader2:
    break

#
print(images1.shape)
print(images2.shape)
```

    torch.Size([100, 3072])
    torch.Size([100, 3, 32, 32])



```python
# 정답 라벨 정의
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 검증 데이터의 처음 50개를 출력
show_images_labels(test_loader2, classes, None, None)
```

    n_size =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__48_1.webp)
    


### 학습용 파라미터 설정


```python
# 입력 차원수는 3*32*32=3072
n_input = image1.view(-1).shape[0]

# 출력 차원수
# 분류 클래스의 수이므로　10
n_output = len(set(list(labels1.data.numpy())))
# np.unique(labels1.data.numpy()).size
# 은닉층의 노드수
n_hidden = 128

# 결과 확인
print(f'n_input: {n_input}  n_hidden: {n_hidden} n_output: {n_output}')
```

    n_input: 3072  n_hidden: 128 n_output: 10



```python
# 모델 정의
# 3072입력 10출력 1은닉층을 포함한 신경망 모델

class Net(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super().__init__()

        # 은닉층 정의(은닉층의 노드수 : n_hidden)
        self.l1 = nn.Linear(n_input, n_hidden)

        # 출력층의 정의
        self.l2 = nn.Linear(n_hidden, n_output)

        # ReLU 함수 정의
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x1 = self.l1(x)
        x2 = self.relu(x1)
        x3 = self.l2(x2)
        return x3
```

### 모델 인스턴스 생성과 GPU 할당


```python
# 모델 인스턴스 생성
net = Net(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = torch.optim.SGD(net.parameters(), lr=lr)
```


```python
# 모델 개요 표시 1

print(net)
```

    Net(
      (l1): Linear(in_features=3072, out_features=128, bias=True)
      (l2): Linear(in_features=128, out_features=10, bias=True)
      (relu): ReLU(inplace=True)
    )



```python
# 모델 개요 표시 2

summary(net, (100, 3072), depth=1)
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    Net                                      [100, 10]                 --
    ├─Linear: 1-1                            [100, 128]                393,344
    ├─ReLU: 1-2                              [100, 128]                --
    ├─Linear: 1-3                            [100, 10]                 1,290
    ==========================================================================================
    Total params: 394,634
    Trainable params: 394,634
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 39.46
    ==========================================================================================
    Input size (MB): 1.23
    Forward/backward pass size (MB): 0.11
    Params size (MB): 1.58
    Estimated Total Size (MB): 2.92
    ==========================================================================================




```python
# 손실 계산
loss = eval_loss(test_loader1, device, net, criterion)

# 손실 계산 그래프 시각화
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__56_0.svg)
    


### 학습


```python
# 난수 초기화
torch_seed()

# 모델 인스턴스 생성
net = Net(n_input, n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history = np.zeros((0,5))

# 학습
history = fit(net, optimizer, criterion, num_epochs, train_loader1, test_loader1, device, history)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/10], loss: 1.94965 acc: 0.32218 val_loss: 1.79424, val_acc: 0.37710



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/10], loss: 1.73836 acc: 0.39598 val_loss: 1.68423, val_acc: 0.41850



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/10], loss: 1.65492 acc: 0.42398 val_loss: 1.62226, val_acc: 0.43860



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/10], loss: 1.60225 acc: 0.44256 val_loss: 1.58253, val_acc: 0.45150



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/10], loss: 1.56317 acc: 0.45540 val_loss: 1.55320, val_acc: 0.46170



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/10], loss: 1.53229 acc: 0.46760 val_loss: 1.52983, val_acc: 0.46830



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/10], loss: 1.50488 acc: 0.47688 val_loss: 1.51209, val_acc: 0.47400



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/10], loss: 1.48005 acc: 0.48632 val_loss: 1.49287, val_acc: 0.47750



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/10], loss: 1.45687 acc: 0.49624 val_loss: 1.47964, val_acc: 0.48740



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/10], loss: 1.43482 acc: 0.50422 val_loss: 1.46307, val_acc: 0.48860


### 평가


```python
# 평가
evaluate_history(history)
```

    초기상태 : 손실 : 1.79424  정확도 : 0.37710
    최종상태 : 손실 : 1.46307  정확도 : 0.48860



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__60_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__60_2.webp)
    


### 모델 정의(CNN)


```python
class CNN(nn.Module):
  def __init__(self, n_output, n_hidden):
    super().__init__()
    self.conv1 = nn.Conv2d(3, 32, 3)
    self.conv2 = nn.Conv2d(32, 32, 3)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d((2,2))
    self.flatten = nn.Flatten()
    self.l1 = nn.Linear(6272, n_hidden)
    self.l2 = nn.Linear(n_hidden, n_output)

    self.features = nn.Sequential(
        self.conv1,
        self.relu,
        self.conv2,
        self.relu,
        self.maxpool)

    self.classifier = nn.Sequential(
       self.l1,
       self.relu,
       self.l2)

  def forward(self, x):
    x1 = self.features(x)
    x2 = self.flatten(x1)
    x3 = self.classifier(x2)
    return x3
```

### 모델 인스턴스 생성


```python
# 모델 인스턴스 생성
net = CNN(n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = torch.optim.SGD(net.parameters(), lr=lr)
```


```python
# 모델 개요 표시 1

print(net)
```

    CNN(
      (conv1): Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1))
      (conv2): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (relu): ReLU(inplace=True)
      (maxpool): MaxPool2d(kernel_size=(2, 2), stride=(2, 2), padding=0, dilation=1, ceil_mode=False)
      (flatten): Flatten(start_dim=1, end_dim=-1)
      (l1): Linear(in_features=6272, out_features=128, bias=True)
      (l2): Linear(in_features=128, out_features=10, bias=True)
      (features): Sequential(
        (0): Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1))
        (1): ReLU(inplace=True)
        (2): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
        (3): ReLU(inplace=True)
        (4): MaxPool2d(kernel_size=(2, 2), stride=(2, 2), padding=0, dilation=1, ceil_mode=False)
      )
      (classifier): Sequential(
        (0): Linear(in_features=6272, out_features=128, bias=True)
        (1): ReLU(inplace=True)
        (2): Linear(in_features=128, out_features=10, bias=True)
      )
    )



```python
# 모델 개요 표시2

summary(net, (100,3,32,32), depth = 2)
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    CNN                                      [100, 10]                 --
    ├─Sequential: 1-1                        [100, 32, 14, 14]         9,248
    │    └─Conv2d: 2-1                       [100, 32, 30, 30]         896
    ├─Sequential: 1-4                        --                        (recursive)
    │    └─ReLU: 2-2                         [100, 32, 30, 30]         --
    ├─Sequential: 1-5                        --                        (recursive)
    │    └─Conv2d: 2-3                       [100, 32, 28, 28]         9,248
    ├─Sequential: 1-4                        --                        (recursive)
    │    └─ReLU: 2-4                         [100, 32, 28, 28]         --
    ├─Sequential: 1-5                        --                        (recursive)
    │    └─MaxPool2d: 2-5                    [100, 32, 14, 14]         --
    ├─Flatten: 1-6                           [100, 6272]               --
    ├─Sequential: 1-7                        [100, 10]                 --
    │    └─Linear: 2-6                       [100, 128]                802,944
    │    └─ReLU: 2-7                         [100, 128]                --
    │    └─Linear: 2-8                       [100, 10]                 1,290
    ==========================================================================================
    Total params: 823,626
    Trainable params: 823,626
    Non-trainable params: 0
    Total mult-adds (Units.MEGABYTES): 886.11
    ==========================================================================================
    Input size (MB): 1.23
    Forward/backward pass size (MB): 43.22
    Params size (MB): 3.26
    Estimated Total Size (MB): 47.71
    ==========================================================================================




```python
# 손실 계산
loss = eval_loss(test_loader2, device, net, criterion)

# 손실 계산 그래프 시각화
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__67_0.svg)
    


### 결과(CNN)


```python
# 난수 초기화
torch_seed()

# 모델 인스턴스 생성
net = CNN(n_output, n_hidden).to(device)

# 손실 함수： 교차 엔트로피 함수
criterion = nn.CrossEntropyLoss()

# 학습률
lr = 0.01

# 최적화 함수: 경사 하강법
optimizer = optim.SGD(net.parameters(), lr=lr)

# 반복 횟수
num_epochs = 10

# 평가 결과 기록
history2 = np.zeros((0,5))

# 학습
history2 = fit(net, optimizer, criterion, num_epochs, train_loader2, test_loader2, device, history2)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/10], loss: 2.08246 acc: 0.26084 val_loss: 1.86593, val_acc: 0.34690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/10], loss: 1.78080 acc: 0.37296 val_loss: 1.67678, val_acc: 0.40950



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/10], loss: 1.61318 acc: 0.43058 val_loss: 1.53056, val_acc: 0.45960



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/10], loss: 1.48527 acc: 0.47320 val_loss: 1.44834, val_acc: 0.49010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/10], loss: 1.40808 acc: 0.49936 val_loss: 1.37022, val_acc: 0.51260



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/10], loss: 1.34984 acc: 0.52108 val_loss: 1.33102, val_acc: 0.52650



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/10], loss: 1.30325 acc: 0.53764 val_loss: 1.29277, val_acc: 0.53840



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/10], loss: 1.25244 acc: 0.55482 val_loss: 1.25406, val_acc: 0.55170



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/10], loss: 1.20528 acc: 0.57400 val_loss: 1.23566, val_acc: 0.56080



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/10], loss: 1.15801 acc: 0.59202 val_loss: 1.18459, val_acc: 0.58010



```python
# 평가

evaluate_history(history2)
```

    초기상태 : 손실 : 1.86593  정확도 : 0.34690
    최종상태 : 손실 : 1.18459  정확도 : 0.58010



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__70_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__70_2.webp)
    



```python
# 처음 50개 데이터 표시

show_images_labels(test_loader2, classes, net, device)
```

    n_size =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_11%EC%B0%A8%EC%8B%9C__CNN__71_1.webp)
    



## 강의_3기_AI개론_12차시__SGD_Adam_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_12차시__SGD_Adam_.ipynb)

# 12장 튜닝 기법

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
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader

```


```python
# plt.rcParams.items()
```


```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

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



```python
# 분류 클래스 명칭 리스트
# CIFAR10
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 분류 클래스 수,　10
n_output = len(list(set(classes)))
# n_output = len(set(classes))

# 결과 확인
print(n_output)
```

    10


## 과학습의 대응 방법

### 드랍 아웃 함수 동작 확인


```python
# 드랍 아웃 실험용 더미 데이터 작성

torch.manual_seed(123)
inputs = torch.randn(1, 10)
print(inputs)
```

    tensor([[-0.1115,  0.1204, -0.3696, -0.2404, -1.1969,  0.2093, -0.9724, -0.7550,
              0.3239, -0.1085]])



```python
# 드랍 아웃 함수 정의
dropout = nn.Dropout(0.5)

# 훈련 페이즈에서의 거동
dropout.train()
print("dropout.training = ", dropout.training) #
outputs = dropout(inputs)
print(outputs)

# 예측 페이즈에서의 거동
print("="*50)
dropout.eval()
print("dropout.training = ", dropout.training)
outputs = dropout(inputs)
print(outputs)
```

    dropout.training =  True
    tensor([[-0.0000,  0.2407, -0.0000, -0.4808, -0.0000,  0.0000, -1.9447, -0.0000,
              0.6478, -0.2170]])
    ==================================================
    dropout.training =  False
    tensor([[-0.1115,  0.1204, -0.3696, -0.2404, -1.1969,  0.2093, -0.9724, -0.7550,
              0.3239, -0.1085]])


## 공통 함수의 라이브러리화


```python
# # 공통 함수 다운로드
!git clone https://github.com/wikibook/pythonlibs.git

# # 공통 함수 불러오기
from pythonlibs.torch_lib1 import *

# # 공통 함수 확인
print(README)
```

    Cloning into 'pythonlibs'...
    remote: Enumerating objects: 25, done.[K
    remote: Counting objects: 100% (25/25), done.[K
    remote: Compressing objects: 100% (16/16), done.[K
    remote: Total 25 (delta 6), reused 25 (delta 6), pack-reused 0 (from 0)[K
    Receiving objects: 100% (25/25), 21.10 MiB | 19.24 MiB/s, done.
    Resolving deltas: 100% (6/6), done.
    Common Library for PyTorch
    Author: M. Akaishi


## 데이터 준비


```python
# Transforms의 정의

transform = transforms.Compose([
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
    transform = transform)

# 검증 데이터셋
test_set = datasets.CIFAR10(
    root = data_root,
    train = False,
    download = True,
    transform = transform)
```

    Downloading https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz to ./data/cifar-10-python.tar.gz


    100%|██████████| 170M/170M [00:05<00:00, 31.1MB/s]


    Extracting ./data/cifar-10-python.tar.gz to ./data
    Files already downloaded and verified



```python
# 미니 배치 사이즈 지정
batch_size = 100

# 훈련용 데이터로더
# 훈련용이므로 셔플을 True로 설정
train_loader = DataLoader(train_set,
    batch_size = batch_size, shuffle = True)

# 검증용 데이터로더
# 검증용이므로 셔플하지 않음
test_loader = DataLoader(test_set,
    batch_size = batch_size, shuffle = False) # len(test_set)

# next(iter(train_loader))[0].shape # torch.Size([100, 3, 32, 32])
```


```python
# 처음 50개 이미지 출력
show_images_labels(test_loader, classes, None, None)
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__21_0.webp)
    


## 층을 깊게 쌓은 모델 구현하기


```python
class CNN_v2(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=(1,1))
        self.conv2 = nn.Conv2d(32, 32, 3, padding=(1,1))
        self.conv3 = nn.Conv2d(32, 64, 3, padding=(1,1))
        self.conv4 = nn.Conv2d(64, 64, 3, padding=(1,1))
        self.conv5 = nn.Conv2d(64, 128, 3, padding=(1,1))
        self.conv6 = nn.Conv2d(128, 128, 3, padding=(1,1))
        self.relu = nn.ReLU(inplace=True)
        self.flatten = nn.Flatten()
        self.maxpool = nn.MaxPool2d((2,2))
        self.l1 = nn.Linear(4*4*128, 128)
        self.l2 = nn.Linear(128, num_classes)

        self.features = nn.Sequential(
            self.conv1,
            self.relu,
            self.conv2,
            self.relu,
            self.maxpool,
            self.conv3,
            self.relu,
            self.conv4,
            self.relu,
            self.maxpool,
            self.conv5,
            self.relu,
            self.conv6,
            self.relu,
            self.maxpool,
            )

        self.classifier = nn.Sequential(
            self.l1,
            self.relu,
            self.l2
        )

    def forward(self, x):
        x1 = self.features(x)
        x2 = self.flatten(x1)
        x3 = self.classifier(x2)
        return x3
```


```python
# 손실 계산 그래프 시각화
net = CNN_v2(n_output).to(device)
criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__24_0.svg)
    



```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
lr = 0.01
net = CNN_v2(n_output).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=lr)
history = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 50
history = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/50], loss: 0.02303 acc: 0.10000 val_loss: 0.02303, val_acc: 0.10000



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/50], loss: 0.02303 acc: 0.10000 val_loss: 0.02303, val_acc: 0.10000



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/50], loss: 0.02302 acc: 0.10000 val_loss: 0.02302, val_acc: 0.10000



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/50], loss: 0.02302 acc: 0.10842 val_loss: 0.02302, val_acc: 0.10170



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/50], loss: 0.02302 acc: 0.13026 val_loss: 0.02302, val_acc: 0.17460



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/50], loss: 0.02301 acc: 0.16746 val_loss: 0.02300, val_acc: 0.19090



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/50], loss: 0.02298 acc: 0.18536 val_loss: 0.02294, val_acc: 0.21840



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/50], loss: 0.02245 acc: 0.21884 val_loss: 0.02097, val_acc: 0.23860



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/50], loss: 0.02016 acc: 0.26152 val_loss: 0.01946, val_acc: 0.29340



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/50], loss: 0.01907 acc: 0.31276 val_loss: 0.01891, val_acc: 0.31430



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/50], loss: 0.01797 acc: 0.35134 val_loss: 0.01699, val_acc: 0.38670



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/50], loss: 0.01697 acc: 0.38422 val_loss: 0.01625, val_acc: 0.41410



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/50], loss: 0.01629 acc: 0.40634 val_loss: 0.01560, val_acc: 0.42870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/50], loss: 0.01574 acc: 0.42162 val_loss: 0.01614, val_acc: 0.41770



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/50], loss: 0.01530 acc: 0.43782 val_loss: 0.01511, val_acc: 0.44100



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/50], loss: 0.01482 acc: 0.45892 val_loss: 0.01441, val_acc: 0.47230



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/50], loss: 0.01442 acc: 0.47328 val_loss: 0.01401, val_acc: 0.48600



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/50], loss: 0.01399 acc: 0.49358 val_loss: 0.01419, val_acc: 0.48750



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/50], loss: 0.01356 acc: 0.51322 val_loss: 0.01344, val_acc: 0.51200



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/50], loss: 0.01312 acc: 0.53244 val_loss: 0.01295, val_acc: 0.53320



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [21/50], loss: 0.01260 acc: 0.54886 val_loss: 0.01234, val_acc: 0.55380



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [22/50], loss: 0.01219 acc: 0.56632 val_loss: 0.01208, val_acc: 0.56660



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [23/50], loss: 0.01176 acc: 0.58132 val_loss: 0.01205, val_acc: 0.57050



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [24/50], loss: 0.01143 acc: 0.59390 val_loss: 0.01157, val_acc: 0.58640



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [25/50], loss: 0.01099 acc: 0.61028 val_loss: 0.01120, val_acc: 0.59660



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [26/50], loss: 0.01063 acc: 0.62464 val_loss: 0.01097, val_acc: 0.61150



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [27/50], loss: 0.01023 acc: 0.64048 val_loss: 0.01107, val_acc: 0.60870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [28/50], loss: 0.00987 acc: 0.65190 val_loss: 0.01052, val_acc: 0.63410



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [29/50], loss: 0.00956 acc: 0.66656 val_loss: 0.01003, val_acc: 0.64890



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [30/50], loss: 0.00919 acc: 0.68016 val_loss: 0.00976, val_acc: 0.65600



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [31/50], loss: 0.00887 acc: 0.68872 val_loss: 0.00976, val_acc: 0.65950



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [32/50], loss: 0.00858 acc: 0.69868 val_loss: 0.00948, val_acc: 0.66890



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [33/50], loss: 0.00825 acc: 0.71334 val_loss: 0.00987, val_acc: 0.65870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [34/50], loss: 0.00796 acc: 0.72344 val_loss: 0.00919, val_acc: 0.68030



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [35/50], loss: 0.00762 acc: 0.73620 val_loss: 0.00939, val_acc: 0.67430



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [36/50], loss: 0.00734 acc: 0.74322 val_loss: 0.00929, val_acc: 0.67910



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [37/50], loss: 0.00707 acc: 0.75332 val_loss: 0.00939, val_acc: 0.68690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [38/50], loss: 0.00676 acc: 0.76416 val_loss: 0.00923, val_acc: 0.68910



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [39/50], loss: 0.00643 acc: 0.77690 val_loss: 0.00930, val_acc: 0.69350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [40/50], loss: 0.00617 acc: 0.78578 val_loss: 0.00927, val_acc: 0.69530



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [41/50], loss: 0.00589 acc: 0.79472 val_loss: 0.00950, val_acc: 0.68780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [42/50], loss: 0.00560 acc: 0.80366 val_loss: 0.00934, val_acc: 0.70240



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [43/50], loss: 0.00530 acc: 0.81412 val_loss: 0.00919, val_acc: 0.70460



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [44/50], loss: 0.00498 acc: 0.82586 val_loss: 0.00946, val_acc: 0.70290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [45/50], loss: 0.00473 acc: 0.83450 val_loss: 0.01020, val_acc: 0.68780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [46/50], loss: 0.00439 acc: 0.84554 val_loss: 0.01047, val_acc: 0.69070



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [47/50], loss: 0.00409 acc: 0.85482 val_loss: 0.01021, val_acc: 0.69160



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [48/50], loss: 0.00379 acc: 0.86824 val_loss: 0.01048, val_acc: 0.69790



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [49/50], loss: 0.00348 acc: 0.87920 val_loss: 0.01061, val_acc: 0.70270



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [50/50], loss: 0.00318 acc: 0.88910 val_loss: 0.01101, val_acc: 0.69860



```python
evaluate_history(history)
```

    초기상태 : 손실 : 0.02303  정확도 : 0.10000
    최종상태 : 손실 : 0.01101 정확도 : 0.69860



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__27_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__27_2.webp)
    


## 최적화 함수 선택

### 모멘텀 설정


```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
lr = 0.01
net = CNN_v2(n_output).to(device)
criterion = nn.CrossEntropyLoss()

# 최적화 함수에 모멘텀 값 설정
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)
history2 = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 20
history2 = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history2)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/20], loss: 0.02286 acc: 0.12124 val_loss: 0.02051, val_acc: 0.24080



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/20], loss: 0.01800 acc: 0.33642 val_loss: 0.01524, val_acc: 0.42710



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/20], loss: 0.01413 acc: 0.48200 val_loss: 0.01265, val_acc: 0.54390



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/20], loss: 0.01160 acc: 0.58314 val_loss: 0.01092, val_acc: 0.61290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/20], loss: 0.00968 acc: 0.65812 val_loss: 0.00887, val_acc: 0.68770



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/20], loss: 0.00815 acc: 0.71094 val_loss: 0.00826, val_acc: 0.71040



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/20], loss: 0.00686 acc: 0.76058 val_loss: 0.00765, val_acc: 0.73660



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/20], loss: 0.00583 acc: 0.79706 val_loss: 0.00726, val_acc: 0.75350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/20], loss: 0.00491 acc: 0.82626 val_loss: 0.00709, val_acc: 0.76350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/20], loss: 0.00421 acc: 0.85188 val_loss: 0.00785, val_acc: 0.75440



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/20], loss: 0.00340 acc: 0.87918 val_loss: 0.00756, val_acc: 0.76870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/20], loss: 0.00283 acc: 0.89888 val_loss: 0.00788, val_acc: 0.76930



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/20], loss: 0.00235 acc: 0.91628 val_loss: 0.00895, val_acc: 0.74930



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/20], loss: 0.00190 acc: 0.93238 val_loss: 0.00996, val_acc: 0.75730



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/20], loss: 0.00159 acc: 0.94376 val_loss: 0.00988, val_acc: 0.76600



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/20], loss: 0.00134 acc: 0.95216 val_loss: 0.01132, val_acc: 0.75400



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/20], loss: 0.00127 acc: 0.95392 val_loss: 0.01084, val_acc: 0.76470



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/20], loss: 0.00104 acc: 0.96336 val_loss: 0.01188, val_acc: 0.76610



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/20], loss: 0.00096 acc: 0.96612 val_loss: 0.01390, val_acc: 0.75650



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/20], loss: 0.00088 acc: 0.96932 val_loss: 0.01271, val_acc: 0.76330



```python
evaluate_history(history2)
```

    초기상태 : 손실 : 0.02051  정확도 : 0.24080
    최종상태 : 손실 : 0.01271 정확도 : 0.76330



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__32_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__32_2.webp)
    


### Adam 함수 사용


```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
net = CNN_v2(n_output).to(device)
criterion = nn.CrossEntropyLoss()

# 최적화 함수를 Adam으로 교체
optimizer = optim.Adam(net.parameters())
history3 = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 20
history3 = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history3)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/20], loss: 0.01599 acc: 0.41138 val_loss: 0.01251, val_acc: 0.54530



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/20], loss: 0.01100 acc: 0.60582 val_loss: 0.01017, val_acc: 0.63780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/20], loss: 0.00886 acc: 0.68580 val_loss: 0.00896, val_acc: 0.68720



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/20], loss: 0.00738 acc: 0.73916 val_loss: 0.00795, val_acc: 0.72130



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/20], loss: 0.00621 acc: 0.78130 val_loss: 0.00715, val_acc: 0.75080



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/20], loss: 0.00534 acc: 0.81154 val_loss: 0.00712, val_acc: 0.75570



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/20], loss: 0.00451 acc: 0.84036 val_loss: 0.00714, val_acc: 0.76190



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/20], loss: 0.00375 acc: 0.86806 val_loss: 0.00735, val_acc: 0.76740



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/20], loss: 0.00308 acc: 0.89048 val_loss: 0.00792, val_acc: 0.76050



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/20], loss: 0.00250 acc: 0.91074 val_loss: 0.00868, val_acc: 0.76510



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/20], loss: 0.00201 acc: 0.92756 val_loss: 0.00994, val_acc: 0.76490



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/20], loss: 0.00169 acc: 0.94052 val_loss: 0.01072, val_acc: 0.75970



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/20], loss: 0.00146 acc: 0.94828 val_loss: 0.01099, val_acc: 0.75710



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/20], loss: 0.00129 acc: 0.95406 val_loss: 0.01236, val_acc: 0.75800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/20], loss: 0.00123 acc: 0.95614 val_loss: 0.01213, val_acc: 0.75500



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/20], loss: 0.00105 acc: 0.96330 val_loss: 0.01296, val_acc: 0.75240



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/20], loss: 0.00098 acc: 0.96622 val_loss: 0.01316, val_acc: 0.74750



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/20], loss: 0.00098 acc: 0.96628 val_loss: 0.01438, val_acc: 0.74470



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/20], loss: 0.00093 acc: 0.96794 val_loss: 0.01480, val_acc: 0.75860



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/20], loss: 0.00077 acc: 0.97378 val_loss: 0.01433, val_acc: 0.75310



```python
evaluate_history(history3)
```

    초기상태 : 손실 : 0.01251  정확도 : 0.54530
    최종상태 : 손실 : 0.01433 정확도 : 0.75310



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__36_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__36_2.webp)
    


### 결과 비교


```python
# 결과 비교(검증 데이터의 정확도)
plt.figure(figsize=(9,8))
plt.plot(history[:,0], history[:,4], label='SGD', c='k',ls='dashed' )
plt.plot(history2[:,0], history2[:,4], label='SGD momentum=0.9', c='k')
plt.plot(history3[:,0], history3[:,4], label='Adam', c='b')
plt.title('최적화 함수 비교 결과(검증 데이터의 정확도)')
plt.xlabel('반복 횟수')
plt.ylabel('정확도')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__38_0.webp)
    


## 드랍 아웃 (Dropout)


```python
# 모델 정의

class CNN_v3(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=(1,1))
        self.conv2 = nn.Conv2d(32, 32, 3, padding=(1,1))
        self.conv3 = nn.Conv2d(32, 64, 3, padding=(1,1))
        self.conv4 = nn.Conv2d(64, 64, 3, padding=(1,1))
        self.conv5 = nn.Conv2d(64, 128, 3, padding=(1,1))
        self.conv6 = nn.Conv2d(128, 128, 3, padding=(1,1))
        self.relu = nn.ReLU(inplace=True)
        self.flatten = nn.Flatten()
        self.maxpool = nn.MaxPool2d((2,2))
        self.l1 = nn.Linear(4*4*128, 128)
        self.l2 = nn.Linear(128, 10)
        self.dropout1 = nn.Dropout(0.2)
        self.dropout2 = nn.Dropout(0.3)
        self.dropout3 = nn.Dropout(0.4)

        self.features = nn.Sequential(
            self.conv1,
            self.relu,
            self.conv2,
            self.relu,
            self.maxpool,
            self.dropout1,
            self.conv3,
            self.relu,
            self.conv4,
            self.relu,
            self.maxpool,
            self.dropout2,
            self.conv5,
            self.relu,
            self.conv6,
            self.relu,
            self.maxpool,
            self.dropout3,
            )

        self.classifier = nn.Sequential(
            self.l1,
            self.relu,
            self.dropout3,
            self.l2
        )

    def forward(self, x):
        x1 = self.features(x)
        x2 = self.flatten(x1)
        x3 = self.classifier(x2)
        return x3
```


```python
# 손실 계산 그래프 시각화
net = CNN_v3(n_output).to(device)
criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__41_0.svg)
    



```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
net = CNN_v3(n_output).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters())
history = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 50
history = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/50], loss: 0.01706 acc: 0.36640 val_loss: 0.01291, val_acc: 0.52560



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/50], loss: 0.01274 acc: 0.53650 val_loss: 0.01046, val_acc: 0.62190



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/50], loss: 0.01108 acc: 0.60248 val_loss: 0.00986, val_acc: 0.64780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/50], loss: 0.00991 acc: 0.64668 val_loss: 0.00858, val_acc: 0.69520



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/50], loss: 0.00908 acc: 0.68170 val_loss: 0.00779, val_acc: 0.72800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/50], loss: 0.00841 acc: 0.70578 val_loss: 0.00748, val_acc: 0.73610



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/50], loss: 0.00794 acc: 0.72386 val_loss: 0.00716, val_acc: 0.75060



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/50], loss: 0.00753 acc: 0.73912 val_loss: 0.00698, val_acc: 0.75490



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/50], loss: 0.00715 acc: 0.75206 val_loss: 0.00637, val_acc: 0.78290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/50], loss: 0.00684 acc: 0.76330 val_loss: 0.00684, val_acc: 0.76890



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/50], loss: 0.00662 acc: 0.77024 val_loss: 0.00657, val_acc: 0.77470



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/50], loss: 0.00643 acc: 0.77688 val_loss: 0.00629, val_acc: 0.78820



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/50], loss: 0.00624 acc: 0.78442 val_loss: 0.00594, val_acc: 0.79780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/50], loss: 0.00597 acc: 0.79274 val_loss: 0.00579, val_acc: 0.80790



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/50], loss: 0.00583 acc: 0.79728 val_loss: 0.00601, val_acc: 0.80180



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/50], loss: 0.00572 acc: 0.80336 val_loss: 0.00574, val_acc: 0.80800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/50], loss: 0.00551 acc: 0.80806 val_loss: 0.00592, val_acc: 0.79930



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/50], loss: 0.00545 acc: 0.81150 val_loss: 0.00605, val_acc: 0.80170



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/50], loss: 0.00531 acc: 0.81578 val_loss: 0.00554, val_acc: 0.81620



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/50], loss: 0.00526 acc: 0.81584 val_loss: 0.00565, val_acc: 0.81670



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [21/50], loss: 0.00511 acc: 0.82310 val_loss: 0.00569, val_acc: 0.81300



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [22/50], loss: 0.00507 acc: 0.82492 val_loss: 0.00572, val_acc: 0.81480



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [23/50], loss: 0.00498 acc: 0.82546 val_loss: 0.00540, val_acc: 0.82600



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [24/50], loss: 0.00498 acc: 0.82744 val_loss: 0.00548, val_acc: 0.81800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [25/50], loss: 0.00482 acc: 0.83118 val_loss: 0.00570, val_acc: 0.81530



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [26/50], loss: 0.00476 acc: 0.83398 val_loss: 0.00549, val_acc: 0.81970



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [27/50], loss: 0.00472 acc: 0.83668 val_loss: 0.00538, val_acc: 0.82570



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [28/50], loss: 0.00474 acc: 0.83604 val_loss: 0.00551, val_acc: 0.81810



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [29/50], loss: 0.00458 acc: 0.84072 val_loss: 0.00560, val_acc: 0.82160



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [30/50], loss: 0.00459 acc: 0.83894 val_loss: 0.00524, val_acc: 0.82900



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [31/50], loss: 0.00451 acc: 0.84376 val_loss: 0.00524, val_acc: 0.83260



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [32/50], loss: 0.00448 acc: 0.84620 val_loss: 0.00540, val_acc: 0.82550



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [33/50], loss: 0.00440 acc: 0.84592 val_loss: 0.00538, val_acc: 0.82730



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [34/50], loss: 0.00433 acc: 0.84826 val_loss: 0.00524, val_acc: 0.83040



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [35/50], loss: 0.00440 acc: 0.84622 val_loss: 0.00533, val_acc: 0.83070



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [36/50], loss: 0.00433 acc: 0.84856 val_loss: 0.00530, val_acc: 0.83090



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [37/50], loss: 0.00428 acc: 0.85002 val_loss: 0.00551, val_acc: 0.82670



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [38/50], loss: 0.00421 acc: 0.85340 val_loss: 0.00536, val_acc: 0.83010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [39/50], loss: 0.00419 acc: 0.85436 val_loss: 0.00554, val_acc: 0.82750



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [40/50], loss: 0.00420 acc: 0.85218 val_loss: 0.00551, val_acc: 0.83090



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [41/50], loss: 0.00414 acc: 0.85538 val_loss: 0.00554, val_acc: 0.82690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [42/50], loss: 0.00410 acc: 0.85678 val_loss: 0.00533, val_acc: 0.83280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [43/50], loss: 0.00409 acc: 0.85778 val_loss: 0.00545, val_acc: 0.82690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [44/50], loss: 0.00403 acc: 0.85872 val_loss: 0.00552, val_acc: 0.82860



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [45/50], loss: 0.00398 acc: 0.86124 val_loss: 0.00554, val_acc: 0.82280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [46/50], loss: 0.00400 acc: 0.86014 val_loss: 0.00533, val_acc: 0.82940



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [47/50], loss: 0.00399 acc: 0.86098 val_loss: 0.00536, val_acc: 0.83470



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [48/50], loss: 0.00395 acc: 0.86294 val_loss: 0.00555, val_acc: 0.83180



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [49/50], loss: 0.00393 acc: 0.86204 val_loss: 0.00535, val_acc: 0.83450



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [50/50], loss: 0.00390 acc: 0.86488 val_loss: 0.00531, val_acc: 0.83480



```python
evaluate_history(history)
```

    초기상태 : 손실 : 0.01291  정확도 : 0.52560
    최종상태 : 손실 : 0.00531 정확도 : 0.83480



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__44_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__44_2.webp)
    


## 배치 정규화


```python
class CNN_v4(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=(1,1))
        self.conv2 = nn.Conv2d(32, 32, 3, padding=(1,1))
        self.conv3 = nn.Conv2d(32, 64, 3, padding=(1,1))
        self.conv4 = nn.Conv2d(64, 64, 3, padding=(1,1))
        self.conv5 = nn.Conv2d(64, 128, 3, padding=(1,1))
        self.conv6 = nn.Conv2d(128, 128, 3, padding=(1,1))
        self.relu = nn.ReLU(inplace=True)
        self.flatten = nn.Flatten()
        self.maxpool = nn.MaxPool2d((2,2))
        self.l1 = nn.Linear(4*4*128, 128)
        self.l2 = nn.Linear(128, 10)
        self.dropout1 = nn.Dropout(0.2)
        self.dropout2 = nn.Dropout(0.3)
        self.dropout3 = nn.Dropout(0.4)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(32)
        self.bn3 = nn.BatchNorm2d(64)
        self.bn4 = nn.BatchNorm2d(64)
        self.bn5 = nn.BatchNorm2d(128)
        self.bn6 = nn.BatchNorm2d(128)

        self.features = nn.Sequential(
            self.conv1,
            self.bn1,
            self.relu,
            self.conv2,
            self.bn2,
            self.relu,
            self.maxpool,
            self.dropout1,
            self.conv3,
            self.bn3,
            self.relu,
            self.conv4,
            self.bn4,
            self.relu,
            self.maxpool,
            self.dropout2,
            self.conv5,
            self.bn5,
            self.relu,
            self.conv6,
            self.bn6,
            self.relu,
            self.maxpool,
            self.dropout3,
            )

        self.classifier = nn.Sequential(
            self.l1,
            self.relu,
            self.dropout3,
            self.l2
        )

    def forward(self, x):
        x1 = self.features(x)
        x2 = self.flatten(x1)
        x3 = self.classifier(x2)
        return x3
```


```python
# 난수 고정
torch_seed(1234)

# 모델 인스턴스 생성
net = CNN_v4(n_output).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters())
history = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 50
history = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/50], loss: 0.01528 acc: 0.43470 val_loss: 0.01214, val_acc: 0.55300



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/50], loss: 0.01144 acc: 0.59318 val_loss: 0.00939, val_acc: 0.66280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/50], loss: 0.00985 acc: 0.65654 val_loss: 0.00916, val_acc: 0.66870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/50], loss: 0.00897 acc: 0.68818 val_loss: 0.00826, val_acc: 0.72070



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/50], loss: 0.00826 acc: 0.71466 val_loss: 0.00745, val_acc: 0.73780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/50], loss: 0.00782 acc: 0.73358 val_loss: 0.00764, val_acc: 0.73690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/50], loss: 0.00740 acc: 0.74790 val_loss: 0.00617, val_acc: 0.78970



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/50], loss: 0.00705 acc: 0.76186 val_loss: 0.00612, val_acc: 0.78980



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/50], loss: 0.00668 acc: 0.77510 val_loss: 0.00656, val_acc: 0.78210



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/50], loss: 0.00640 acc: 0.78562 val_loss: 0.00543, val_acc: 0.81470



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/50], loss: 0.00619 acc: 0.79262 val_loss: 0.00553, val_acc: 0.81700



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/50], loss: 0.00595 acc: 0.79942 val_loss: 0.00579, val_acc: 0.80710



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/50], loss: 0.00572 acc: 0.80792 val_loss: 0.00553, val_acc: 0.81370



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/50], loss: 0.00553 acc: 0.81402 val_loss: 0.00522, val_acc: 0.83010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/50], loss: 0.00530 acc: 0.82250 val_loss: 0.00503, val_acc: 0.83100



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/50], loss: 0.00516 acc: 0.82656 val_loss: 0.00530, val_acc: 0.82570



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/50], loss: 0.00501 acc: 0.83194 val_loss: 0.00509, val_acc: 0.83200



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/50], loss: 0.00481 acc: 0.83874 val_loss: 0.00494, val_acc: 0.83980



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/50], loss: 0.00464 acc: 0.84418 val_loss: 0.00457, val_acc: 0.85220



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/50], loss: 0.00452 acc: 0.84624 val_loss: 0.00479, val_acc: 0.84800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [21/50], loss: 0.00442 acc: 0.85170 val_loss: 0.00483, val_acc: 0.84570



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [22/50], loss: 0.00431 acc: 0.85694 val_loss: 0.00453, val_acc: 0.85200



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [23/50], loss: 0.00423 acc: 0.85944 val_loss: 0.00465, val_acc: 0.85180



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [24/50], loss: 0.00414 acc: 0.86174 val_loss: 0.00449, val_acc: 0.85640



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [25/50], loss: 0.00399 acc: 0.86660 val_loss: 0.00435, val_acc: 0.85700



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [26/50], loss: 0.00391 acc: 0.87126 val_loss: 0.00469, val_acc: 0.85420



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [27/50], loss: 0.00377 acc: 0.87372 val_loss: 0.00458, val_acc: 0.85880



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [28/50], loss: 0.00372 acc: 0.87420 val_loss: 0.00457, val_acc: 0.85300



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [29/50], loss: 0.00364 acc: 0.87772 val_loss: 0.00457, val_acc: 0.85820



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [30/50], loss: 0.00357 acc: 0.88054 val_loss: 0.00486, val_acc: 0.84910



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [31/50], loss: 0.00350 acc: 0.88028 val_loss: 0.00449, val_acc: 0.86350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [32/50], loss: 0.00345 acc: 0.88308 val_loss: 0.00445, val_acc: 0.86280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [33/50], loss: 0.00331 acc: 0.88866 val_loss: 0.00437, val_acc: 0.86590



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [34/50], loss: 0.00324 acc: 0.89076 val_loss: 0.00471, val_acc: 0.86070



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [35/50], loss: 0.00317 acc: 0.89258 val_loss: 0.00441, val_acc: 0.86410



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [36/50], loss: 0.00311 acc: 0.89514 val_loss: 0.00456, val_acc: 0.86290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [37/50], loss: 0.00312 acc: 0.89386 val_loss: 0.00447, val_acc: 0.86610



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [38/50], loss: 0.00306 acc: 0.89698 val_loss: 0.00443, val_acc: 0.86450



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [39/50], loss: 0.00300 acc: 0.89802 val_loss: 0.00447, val_acc: 0.86440



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [40/50], loss: 0.00289 acc: 0.90246 val_loss: 0.00463, val_acc: 0.86520



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [41/50], loss: 0.00289 acc: 0.90152 val_loss: 0.00460, val_acc: 0.86280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [42/50], loss: 0.00283 acc: 0.90374 val_loss: 0.00470, val_acc: 0.86310



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [43/50], loss: 0.00284 acc: 0.90410 val_loss: 0.00448, val_acc: 0.86800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [44/50], loss: 0.00276 acc: 0.90616 val_loss: 0.00448, val_acc: 0.86810



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [45/50], loss: 0.00275 acc: 0.90514 val_loss: 0.00438, val_acc: 0.86970



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [46/50], loss: 0.00269 acc: 0.90808 val_loss: 0.00465, val_acc: 0.86320



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [47/50], loss: 0.00267 acc: 0.91102 val_loss: 0.00457, val_acc: 0.86990



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [48/50], loss: 0.00259 acc: 0.91300 val_loss: 0.00453, val_acc: 0.86730



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [49/50], loss: 0.00254 acc: 0.91284 val_loss: 0.00451, val_acc: 0.86760



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [50/50], loss: 0.00254 acc: 0.91330 val_loss: 0.00471, val_acc: 0.86690



```python
evaluate_history(history)
```

    초기상태 : 손실 : 0.01214  정확도 : 0.55300
    최종상태 : 손실 : 0.00471 정확도 : 0.86690



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__49_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__49_2.webp)
    


## 데이터 증강 기법


```python
# 훈련 데이터용: 정규화에 반전과 RandomErasing 추가
transform_train = transforms.Compose([
  transforms.RandomHorizontalFlip(p=0.5), # 랜덤으로 좌우 반전
  transforms.RandomRotation(30),  # 랜덤으로 -30~30도 회전
  transforms.ColorJitter(brightness=0.5, contrast=0.5),  # 밝기, 대비 조절
  transforms.ToTensor(),
  transforms.Normalize(0.5, 0.5),
  transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False)
])

# class RandomErasing(
#     p: float = 0.5, # Probability that the Random Erasing operation will be performed.
#     scale: Any = (0.02, 0.33), # Range of proportion of erased area against the input image area.
#     ratio: Any = (0.3, 3.3), # Aspect ratio range of the erased rectangle.
#     value: int = 0,
#     inplace: bool = False
# )
```


```python
# transfrom_train을 사용한 데이터셋 정의
train_set2 = datasets.CIFAR10(
    root = data_root,
    train = True,
    download = True,
    transform = transform_train) # n = 50000

# traisform_train을 사용한 데이터로더 정의
batch_size = 100
train_loader2 = DataLoader(train_set2, batch_size=batch_size, shuffle=True)
```

    Files already downloaded and verified



```python
# 새로운 훈련 데이터의 처음 50개 표시

# 난수 고정
# torch_seed(12345)

show_images_labels(train_loader2, classes, None, None)
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__53_0.webp)
    



```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
net = CNN_v4(n_output).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters())
history = np.zeros((0, 5))
```


```python
# 학습
# 동일한 모델에서 train_loader2로 데이터를 변경

num_epochs = 100
history = fit(net, optimizer, criterion, num_epochs,
        train_loader2, test_loader, device, history)
```


      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [1/100], loss: 0.01909 acc: 0.28624 val_loss: 0.01492, val_acc: 0.43330



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [2/100], loss: 0.01633 acc: 0.39462 val_loss: 0.01272, val_acc: 0.53950



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [3/100], loss: 0.01525 acc: 0.44124 val_loss: 0.01203, val_acc: 0.55940



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [4/100], loss: 0.01460 acc: 0.46666 val_loss: 0.01097, val_acc: 0.59450



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [5/100], loss: 0.01405 acc: 0.49264 val_loss: 0.01097, val_acc: 0.60270



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [6/100], loss: 0.01367 acc: 0.50700 val_loss: 0.00968, val_acc: 0.65150



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [7/100], loss: 0.01323 acc: 0.52248 val_loss: 0.00940, val_acc: 0.65820



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [8/100], loss: 0.01291 acc: 0.53722 val_loss: 0.00897, val_acc: 0.68570



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [9/100], loss: 0.01260 acc: 0.54792 val_loss: 0.00879, val_acc: 0.68760



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [10/100], loss: 0.01245 acc: 0.55782 val_loss: 0.00822, val_acc: 0.70140



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [11/100], loss: 0.01219 acc: 0.56516 val_loss: 0.00829, val_acc: 0.69980



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [12/100], loss: 0.01208 acc: 0.57138 val_loss: 0.00781, val_acc: 0.71990



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [13/100], loss: 0.01188 acc: 0.57888 val_loss: 0.00825, val_acc: 0.69420



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [14/100], loss: 0.01169 acc: 0.58570 val_loss: 0.00767, val_acc: 0.73030



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [15/100], loss: 0.01155 acc: 0.59370 val_loss: 0.00746, val_acc: 0.74000



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [16/100], loss: 0.01138 acc: 0.59840 val_loss: 0.00736, val_acc: 0.74180



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [17/100], loss: 0.01123 acc: 0.60944 val_loss: 0.00750, val_acc: 0.74150



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [18/100], loss: 0.01105 acc: 0.61722 val_loss: 0.00728, val_acc: 0.74580



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [19/100], loss: 0.01095 acc: 0.61762 val_loss: 0.00722, val_acc: 0.74990



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [20/100], loss: 0.01074 acc: 0.62700 val_loss: 0.00677, val_acc: 0.76910



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [21/100], loss: 0.01057 acc: 0.63530 val_loss: 0.00682, val_acc: 0.76630



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [22/100], loss: 0.01052 acc: 0.64064 val_loss: 0.00659, val_acc: 0.77010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [23/100], loss: 0.01031 acc: 0.64692 val_loss: 0.00641, val_acc: 0.77840



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [24/100], loss: 0.01021 acc: 0.65134 val_loss: 0.00638, val_acc: 0.77990



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [25/100], loss: 0.01017 acc: 0.65226 val_loss: 0.00628, val_acc: 0.78550



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [26/100], loss: 0.00999 acc: 0.65648 val_loss: 0.00659, val_acc: 0.77610



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [27/100], loss: 0.00992 acc: 0.66218 val_loss: 0.00642, val_acc: 0.77660



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [28/100], loss: 0.00968 acc: 0.66978 val_loss: 0.00606, val_acc: 0.79070



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [29/100], loss: 0.00950 acc: 0.67684 val_loss: 0.00587, val_acc: 0.80350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [30/100], loss: 0.00944 acc: 0.67974 val_loss: 0.00579, val_acc: 0.80410



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [31/100], loss: 0.00923 acc: 0.68678 val_loss: 0.00582, val_acc: 0.80350



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [32/100], loss: 0.00916 acc: 0.68824 val_loss: 0.00568, val_acc: 0.80420



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [33/100], loss: 0.00911 acc: 0.68886 val_loss: 0.00576, val_acc: 0.80600



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [34/100], loss: 0.00906 acc: 0.69312 val_loss: 0.00554, val_acc: 0.81220



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [35/100], loss: 0.00892 acc: 0.69842 val_loss: 0.00540, val_acc: 0.81810



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [36/100], loss: 0.00884 acc: 0.69916 val_loss: 0.00560, val_acc: 0.80830



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [37/100], loss: 0.00881 acc: 0.69796 val_loss: 0.00541, val_acc: 0.81530



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [38/100], loss: 0.00864 acc: 0.70714 val_loss: 0.00529, val_acc: 0.81650



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [39/100], loss: 0.00864 acc: 0.70732 val_loss: 0.00530, val_acc: 0.82240



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [40/100], loss: 0.00861 acc: 0.70976 val_loss: 0.00535, val_acc: 0.81900



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [41/100], loss: 0.00848 acc: 0.71040 val_loss: 0.00508, val_acc: 0.82800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [42/100], loss: 0.00845 acc: 0.71416 val_loss: 0.00511, val_acc: 0.82990



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [43/100], loss: 0.00837 acc: 0.71588 val_loss: 0.00513, val_acc: 0.82560



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [44/100], loss: 0.00838 acc: 0.71636 val_loss: 0.00513, val_acc: 0.82560



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [45/100], loss: 0.00836 acc: 0.71560 val_loss: 0.00520, val_acc: 0.82630



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [46/100], loss: 0.00824 acc: 0.71866 val_loss: 0.00508, val_acc: 0.82460



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [47/100], loss: 0.00821 acc: 0.72232 val_loss: 0.00508, val_acc: 0.82770



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [48/100], loss: 0.00816 acc: 0.72570 val_loss: 0.00518, val_acc: 0.82670



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [49/100], loss: 0.00811 acc: 0.72672 val_loss: 0.00507, val_acc: 0.82880



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [50/100], loss: 0.00811 acc: 0.72316 val_loss: 0.00486, val_acc: 0.83420



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [51/100], loss: 0.00805 acc: 0.72550 val_loss: 0.00502, val_acc: 0.82920



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [52/100], loss: 0.00804 acc: 0.72694 val_loss: 0.00503, val_acc: 0.83090



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [53/100], loss: 0.00793 acc: 0.73008 val_loss: 0.00492, val_acc: 0.83440



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [54/100], loss: 0.00795 acc: 0.72896 val_loss: 0.00489, val_acc: 0.83540



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [55/100], loss: 0.00793 acc: 0.73024 val_loss: 0.00497, val_acc: 0.83040



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [56/100], loss: 0.00785 acc: 0.73370 val_loss: 0.00478, val_acc: 0.84020



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [57/100], loss: 0.00788 acc: 0.73582 val_loss: 0.00484, val_acc: 0.83520



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [58/100], loss: 0.00787 acc: 0.73234 val_loss: 0.00472, val_acc: 0.84030



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [59/100], loss: 0.00776 acc: 0.73724 val_loss: 0.00464, val_acc: 0.84440



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [60/100], loss: 0.00772 acc: 0.73860 val_loss: 0.00494, val_acc: 0.83260



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [61/100], loss: 0.00773 acc: 0.73612 val_loss: 0.00467, val_acc: 0.84380



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [62/100], loss: 0.00768 acc: 0.74134 val_loss: 0.00492, val_acc: 0.83360



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [63/100], loss: 0.00770 acc: 0.73904 val_loss: 0.00466, val_acc: 0.84390



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [64/100], loss: 0.00769 acc: 0.73768 val_loss: 0.00470, val_acc: 0.83980



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [65/100], loss: 0.00767 acc: 0.74166 val_loss: 0.00476, val_acc: 0.83290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [66/100], loss: 0.00762 acc: 0.73976 val_loss: 0.00463, val_acc: 0.84040



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [67/100], loss: 0.00759 acc: 0.74436 val_loss: 0.00463, val_acc: 0.84290



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [68/100], loss: 0.00756 acc: 0.74104 val_loss: 0.00470, val_acc: 0.83770



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [69/100], loss: 0.00758 acc: 0.74248 val_loss: 0.00487, val_acc: 0.83830



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [70/100], loss: 0.00747 acc: 0.74422 val_loss: 0.00454, val_acc: 0.84520



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [71/100], loss: 0.00747 acc: 0.74526 val_loss: 0.00453, val_acc: 0.84930



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [72/100], loss: 0.00747 acc: 0.74640 val_loss: 0.00451, val_acc: 0.84690



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [73/100], loss: 0.00747 acc: 0.74662 val_loss: 0.00463, val_acc: 0.84710



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [74/100], loss: 0.00740 acc: 0.75070 val_loss: 0.00453, val_acc: 0.84650



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [75/100], loss: 0.00739 acc: 0.74802 val_loss: 0.00453, val_acc: 0.84610



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [76/100], loss: 0.00744 acc: 0.74570 val_loss: 0.00457, val_acc: 0.84780



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [77/100], loss: 0.00741 acc: 0.74688 val_loss: 0.00439, val_acc: 0.85030



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [78/100], loss: 0.00732 acc: 0.75102 val_loss: 0.00436, val_acc: 0.84900



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [79/100], loss: 0.00735 acc: 0.75086 val_loss: 0.00435, val_acc: 0.85230



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [80/100], loss: 0.00732 acc: 0.75116 val_loss: 0.00462, val_acc: 0.84310



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [81/100], loss: 0.00728 acc: 0.75200 val_loss: 0.00426, val_acc: 0.85560



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [82/100], loss: 0.00725 acc: 0.75360 val_loss: 0.00438, val_acc: 0.85010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [83/100], loss: 0.00718 acc: 0.75484 val_loss: 0.00439, val_acc: 0.85010



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [84/100], loss: 0.00723 acc: 0.75180 val_loss: 0.00446, val_acc: 0.85080



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [85/100], loss: 0.00724 acc: 0.75460 val_loss: 0.00438, val_acc: 0.85210



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [86/100], loss: 0.00717 acc: 0.75600 val_loss: 0.00448, val_acc: 0.85250



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [87/100], loss: 0.00724 acc: 0.75446 val_loss: 0.00441, val_acc: 0.85280



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [88/100], loss: 0.00722 acc: 0.75380 val_loss: 0.00435, val_acc: 0.85320



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [89/100], loss: 0.00717 acc: 0.75504 val_loss: 0.00440, val_acc: 0.85190



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [90/100], loss: 0.00715 acc: 0.75584 val_loss: 0.00422, val_acc: 0.85560



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [91/100], loss: 0.00714 acc: 0.75746 val_loss: 0.00451, val_acc: 0.84120



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [92/100], loss: 0.00711 acc: 0.75714 val_loss: 0.00457, val_acc: 0.84820



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [93/100], loss: 0.00713 acc: 0.75748 val_loss: 0.00438, val_acc: 0.84870



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [94/100], loss: 0.00707 acc: 0.76024 val_loss: 0.00440, val_acc: 0.85050



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [95/100], loss: 0.00712 acc: 0.75752 val_loss: 0.00433, val_acc: 0.85420



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [96/100], loss: 0.00706 acc: 0.76022 val_loss: 0.00435, val_acc: 0.85400



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [97/100], loss: 0.00709 acc: 0.75894 val_loss: 0.00436, val_acc: 0.85380



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [98/100], loss: 0.00706 acc: 0.75904 val_loss: 0.00438, val_acc: 0.85440



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [99/100], loss: 0.00710 acc: 0.75758 val_loss: 0.00448, val_acc: 0.84800



      0%|          | 0/500 [00:00<?, ?it/s]


    Epoch [100/100], loss: 0.00698 acc: 0.76160 val_loss: 0.00426, val_acc: 0.85370



```python
evaluate_history(history)
```

    초기상태 : 손실 : 0.01492  정확도 : 0.43330
    최종상태 : 손실 : 0.00426 정확도 : 0.85370



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__56_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__56_2.webp)
    



```python
show_images_labels(test_loader, classes, net, device)
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__57_0.webp)
    



```python
# 잘못 예측한 38번째 데이터 추출
for images, labels in test_loader:
    break
image = images[37]
label = labels[37]

# 이미지 확인
plt.figure(figsize=(3,3))
w = image.numpy().copy()
w2 = np.transpose(w, (1, 2, 0))
w3 = (w2 + 1)/2
plt.title(classes[label])
plt.imshow(w3)
plt.show()
```


    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__58_0.webp)
    



```python
# 예측 값 출력
image = image.view(1, 3, 32, 32)
image = image.to(device)
output = net(image)

# 라벨 별 확률 값 출력
probs = torch.softmax(output, dim=1)
probs_np = probs.data.to('cpu').numpy()[0]
print(probs_np)
values = np.frompyfunc(lambda x: f'{x:.04f}', 1, 1)(probs_np)
values
names = np.array(classes)
tbl = np.array([names, values]).T
tbl
```

    [0.0002 0.4003 0.0001 0.0003 0.     0.0006 0.     0.     0.0015 0.5971]





    array([['plane', '0.0002'],
           ['car', '0.4003'],
           ['bird', '0.0001'],
           ['cat', '0.0003'],
           ['deer', '0.0000'],
           ['dog', '0.0006'],
           ['frog', '0.0000'],
           ['horse', '0.0000'],
           ['ship', '0.0015'],
           ['truck', '0.5971']], dtype=object)



## 칼럼 배치 정규화를 사용할 때 주의할 점

### 잘못된 모델 클래스 정의의 예시


```python
class CNN_v5(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=(1,1))
        self.conv2 = nn.Conv2d(32, 32, 3, padding=(1,1))
        self.conv3 = nn.Conv2d(32, 64, 3, padding=(1,1))
        self.conv4 = nn.Conv2d(64, 64, 3, padding=(1,1))
        self.conv5 = nn.Conv2d(64, 128, 3, padding=(1,1))
        self.conv6 = nn.Conv2d(128, 128, 3, padding=(1,1))
        self.relu = nn.ReLU(inplace=True)
        self.flatten = nn.Flatten()
        self.maxpool = nn.MaxPool2d((2,2))
        self.l1 = nn.Linear(4*4*128, 128)
        self.l2 = nn.Linear(128, 10)
        self.dropout1 = nn.Dropout(0.2)
        self.dropout2 = nn.Dropout(0.3)
        self.dropout3 = nn.Dropout(0.4)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)

        self.features = nn.Sequential(
            self.conv1,
            self.bn1,
            self.relu,
            self.conv2,
            self.bn1,
            self.relu,
            self.maxpool,
            self.dropout1,
            self.conv3,
            self.bn2,
            self.relu,
            self.conv4,
            self.bn2,
            self.relu,
            self.maxpool,
            self.dropout2,
            self.conv5,
            self.bn3,
            self.relu,
            self.conv6,
            self.bn3,
            self.relu,
            self.maxpool,
            self.dropout3,
            )

        self.classifier = nn.Sequential(
            self.l1,
            self.relu,
            self.dropout3,
            self.l2
        )

    def forward(self, x):
        x1 = self.features(x)
        x2 = self.flatten(x1)
        x3 = self.classifier(x2)
        return x3
```


```python
# 난수 고정
torch_seed()

# 모델 인스턴스 생성
net = CNN_v5(n_output).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters())
history = np.zeros((0, 5))
```


```python
# 학습

num_epochs = 50
history = fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history)
```


```python
# 손실 계산 그래프 시각화
net = CNN_v5(n_output).to(device)
criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_12%EC%B0%A8%EC%8B%9C__SGD_Adam__65_0.svg)
    


## 칼럼 배치 정규화에서 처리하는 내용


```python
# 입력용 더미 데이터 작성

torch.manual_seed(123)
inputs = torch.randn(1, 1, 10)
print(inputs)
```

    tensor([[[-0.1115,  0.1204, -0.3696, -0.2404, -1.1969,  0.2093, -0.9724,
              -0.7550,  0.3239, -0.1085]]])



```python
# 입력 미니 배치 데이터의 통계량 산출

i_mean = inputs.mean()
i_var = inputs.var(unbiased=True)
i_std = inputs.std(unbiased=False)
print(i_mean, i_std, i_var)
```

    tensor(-0.3101) tensor(0.4867) tensor(0.2632)



```python
# BN 함수의 정의

bn = nn.BatchNorm1d(1)
print(bn.running_mean) # 러닝 평균 (배치 평균의 지수 이동 평균)
print(bn.running_var) # 러닝 분산 (배치 분산의 지수 이동 평균)
print(bn.weight.data) # 배치 정규화 스케일링
print(bn.bias.data) # 배치 정규화 이동
```

    tensor([0.])
    tensor([1.])
    tensor([1.])
    tensor([0.])



```python
# BN 함수의 유사 호출

bn.train()
print('===훈련 페이즈 1===')
outputs1 = bn(inputs)
print(outputs1.data)
print(bn.running_mean)
print(bn.running_var)

bn.eval()
print('===예측 페이즈 1===')
outputs2 = bn(inputs)
print(outputs2.data)
print(bn.running_mean)
print(bn.running_var)

bn.train()
print('===훈련 페이즈 2===')
outputs3 = bn(inputs)
print(outputs3.data)
print(bn.running_mean)
print(bn.running_var)

bn.eval()
print('===예측 페이즈 2===')
outputs4 = bn(inputs)
print(outputs4.data)
print(bn.running_mean)
print(bn.running_var)

```

    ===훈련 페이즈 1===
    tensor([[[ 0.4081,  0.8844, -0.1224,  0.1431, -1.8222,  1.0671, -1.3608,
              -0.9143,  1.3027,  0.4142]]])
    tensor([-0.0310])
    tensor([0.9263])
    ===예측 페이즈 1===
    tensor([[[-0.0836,  0.1573, -0.3518, -0.2176, -1.2114,  0.2496, -0.9781,
              -0.7523,  0.3688, -0.0805]]])
    tensor([-0.0310])
    tensor([0.9263])
    ===훈련 페이즈 2===
    tensor([[[ 0.4081,  0.8844, -0.1224,  0.1431, -1.8222,  1.0671, -1.3608,
              -0.9143,  1.3027,  0.4142]]])
    tensor([-0.0589])
    tensor([0.8600])
    ===예측 페이즈 2===
    tensor([[[-0.0567,  0.1933, -0.3351, -0.1957, -1.2271,  0.2892, -0.9850,
              -0.7507,  0.4128, -0.0535]]])
    tensor([-0.0589])
    tensor([0.8600])



```python
# 훈련 페이즈의 출력

xt = (inputs - i_mean)/i_std * bn.weight + bn.bias
print(xt.data)

print(outputs1.data)
```

    tensor([[[ 0.4081,  0.8845, -0.1224,  0.1431, -1.8223,  1.0671, -1.3608,
              -0.9143,  1.3027,  0.4142]]])
    tensor([[[ 0.4081,  0.8844, -0.1224,  0.1431, -1.8222,  1.0671, -1.3608,
              -0.9143,  1.3027,  0.4142]]])



```python
# 예측 페이즈의 출력

xp = (inputs-bn.running_mean)/torch.sqrt(bn.running_var)
print(xp.data)

print(outputs4.data)
```

    tensor([[[-0.0567,  0.1933, -0.3351, -0.1957, -1.2271,  0.2892, -0.9850,
              -0.7507,  0.4128, -0.0535]]])
    tensor([[[-0.0567,  0.1933, -0.3351, -0.1957, -1.2271,  0.2892, -0.9850,
              -0.7507,  0.4128, -0.0535]]])



```python
# running_mean과 runnung_var의 계산식

# 초깃값
mean0 = 0
var0 = 1
momentum = bn.momentum
print("momentum = ", momentum)
# 이동 평균 계산 1회차
mean1 = (1-momentum) * mean0 +  momentum * i_mean
var1 = (1-momentum) * var0 +  momentum * i_var
print(mean1, var1)

# 이동 평균 계산 2회차
mean2 = (1-momentum) * mean1 +  momentum * i_mean
var2 = (1-momentum) * var1 +  momentum * i_var
print(mean2, var2)
```


## 강의_3기_AI개론_13차시__AlexNet_GoogleNet_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_13차시__AlexNet_GoogleNet_.ipynb)

# 13장 영상 분류 사전 학습 모델 활용하기 1

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
```

    Successfully installed torchviz-0.0.2
    Successfully installed torchinfo-1.6.5


* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


```python
# 라이브러리 임포트

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 폰트 관련 용도
import matplotlib.font_manager as fm

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
import torch.nn as nn
import torch.optim as optim
from torchinfo import summary
from torchviz import make_dot
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
```

    c:\Users\user\anaconda3\envs\torchgpu_py3.9\lib\site-packages\google\protobuf\runtime_version.py:112: UserWarning: Protobuf gencode version 5.27.5 is older than the runtime version 5.28.2 at onnx/onnx-ml.proto. Please avoid checked-in Protobuf gencode that can be obsolete.
      warnings.warn(
    c:\Users\user\anaconda3\envs\torchgpu_py3.9\lib\site-packages\google\protobuf\runtime_version.py:112: UserWarning: Protobuf gencode version 5.27.5 is older than the runtime version 5.28.2 at onnx/onnx-operators-ml.proto. Please avoid checked-in Protobuf gencode that can be obsolete.
      warnings.warn(
    c:\Users\user\anaconda3\envs\torchgpu_py3.9\lib\site-packages\google\protobuf\runtime_version.py:112: UserWarning: Protobuf gencode version 5.27.5 is older than the runtime version 5.28.2 at onnx/onnx-data.proto. Please avoid checked-in Protobuf gencode that can be obsolete.
      warnings.warn(



```python
# warning 표시 끄기
import warnings
warnings.simplefilter('ignore')

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


### 공통 함수 불러오기


```python
# 공통 함수 다운로드
!git clone https://github.com/wikibook/pythonlibs.git

# 공통 함수 불러오기
from pythonlibs.torch_lib1 import *
# from torch_lib1 import *


# 공통 함수 확인
print(README)
```

    Common Library for PyTorch
    Author: M. Akaishi


## 적응형 풀링 함수(nn.AdaptiveAvgPool2d 함수)


```python
# nn.AdaptiveAvgPool2d 정의
p = nn.AdaptiveAvgPool2d((1,1))
print(p)

# 선형 함수의 정의
l1 = nn.Linear(32, 10)
print(l1)
```

    AdaptiveAvgPool2d(output_size=(1, 1))
    Linear(in_features=32, out_features=10, bias=True)



```python
m = nn.AdaptiveAvgPool2d((5, 7))
input = torch.randn(1, 64, 8, 9)
print(m(input).shape)

input2 = torch.randn(1, 64, 32, 30)
print(m(input2).shape)
```

    torch.Size([1, 64, 5, 7])
    torch.Size([1, 64, 5, 7])



```python
# 사전 학습 모델 시뮬레이션
inputs = torch.randn(100, 32, 16, 16)
m1 = p(inputs)
m2 = m1.view(m1.shape[0],-1)
m3 = l1(m2)

# shape 확인
print(m1.shape)
print(m2.shape)
print(m3.shape)
```

    torch.Size([100, 32, 1, 1])
    torch.Size([100, 32])
    torch.Size([100, 10])


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
  transforms.ToTensor(),
  transforms.Normalize(0.5, 0.5), 
  transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False)
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
    root = data_root, train = True,
    download = True, transform = transform_train)

# 검증 데이터셋
test_set = datasets.CIFAR10(
    root = data_root, train = False, 
    download = True, transform = transform)
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

## AlexNet 불러 오기

### 모델 불러오기


```python
#  라이브러리 임포트
from torchvision import models

dir(models)
```




    ['AlexNet',
     'AlexNet_Weights',
     'ConvNeXt',
     'ConvNeXt_Base_Weights',
     'ConvNeXt_Large_Weights',
     'ConvNeXt_Small_Weights',
     'ConvNeXt_Tiny_Weights',
     'DenseNet',
     'DenseNet121_Weights',
     'DenseNet161_Weights',
     'DenseNet169_Weights',
     'DenseNet201_Weights',
     'EfficientNet',
     'EfficientNet_B0_Weights',
     'EfficientNet_B1_Weights',
     'EfficientNet_B2_Weights',
     'EfficientNet_B3_Weights',
     'EfficientNet_B4_Weights',
     'EfficientNet_B5_Weights',
     'EfficientNet_B6_Weights',
     'EfficientNet_B7_Weights',
     'EfficientNet_V2_L_Weights',
     'EfficientNet_V2_M_Weights',
     'EfficientNet_V2_S_Weights',
     'GoogLeNet',
     'GoogLeNetOutputs',
     'GoogLeNet_Weights',
     'Inception3',
     'InceptionOutputs',
     'Inception_V3_Weights',
     'MNASNet',
     'MNASNet0_5_Weights',
     'MNASNet0_75_Weights',
     'MNASNet1_0_Weights',
     'MNASNet1_3_Weights',
     'MaxVit',
     'MaxVit_T_Weights',
     'MobileNetV2',
     'MobileNetV3',
     'MobileNet_V2_Weights',
     'MobileNet_V3_Large_Weights',
     'MobileNet_V3_Small_Weights',
     'RegNet',
     'RegNet_X_16GF_Weights',
     'RegNet_X_1_6GF_Weights',
     'RegNet_X_32GF_Weights',
     'RegNet_X_3_2GF_Weights',
     'RegNet_X_400MF_Weights',
     'RegNet_X_800MF_Weights',
     'RegNet_X_8GF_Weights',
     'RegNet_Y_128GF_Weights',
     'RegNet_Y_16GF_Weights',
     'RegNet_Y_1_6GF_Weights',
     'RegNet_Y_32GF_Weights',
     'RegNet_Y_3_2GF_Weights',
     'RegNet_Y_400MF_Weights',
     'RegNet_Y_800MF_Weights',
     'RegNet_Y_8GF_Weights',
     'ResNeXt101_32X8D_Weights',
     'ResNeXt101_64X4D_Weights',
     'ResNeXt50_32X4D_Weights',
     'ResNet',
     'ResNet101_Weights',
     'ResNet152_Weights',
     'ResNet18_Weights',
     'ResNet34_Weights',
     'ResNet50_Weights',
     'ShuffleNetV2',
     'ShuffleNet_V2_X0_5_Weights',
     'ShuffleNet_V2_X1_0_Weights',
     'ShuffleNet_V2_X1_5_Weights',
     'ShuffleNet_V2_X2_0_Weights',
     'SqueezeNet',
     'SqueezeNet1_0_Weights',
     'SqueezeNet1_1_Weights',
     'SwinTransformer',
     'Swin_B_Weights',
     'Swin_S_Weights',
     'Swin_T_Weights',
     'Swin_V2_B_Weights',
     'Swin_V2_S_Weights',
     'Swin_V2_T_Weights',
     'VGG',
     'VGG11_BN_Weights',
     'VGG11_Weights',
     'VGG13_BN_Weights',
     'VGG13_Weights',
     'VGG16_BN_Weights',
     'VGG16_Weights',
     'VGG19_BN_Weights',
     'VGG19_Weights',
     'ViT_B_16_Weights',
     'ViT_B_32_Weights',
     'ViT_H_14_Weights',
     'ViT_L_16_Weights',
     'ViT_L_32_Weights',
     'VisionTransformer',
     'Weights',
     'WeightsEnum',
     'Wide_ResNet101_2_Weights',
     'Wide_ResNet50_2_Weights',
     '_GoogLeNetOutputs',
     '_InceptionOutputs',
     '__builtins__',
     '__cached__',
     '__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__path__',
     '__spec__',
     '_api',
     '_meta',
     '_utils',
     'alexnet',
     'convnext',
     'convnext_base',
     'convnext_large',
     'convnext_small',
     'convnext_tiny',
     'densenet',
     'densenet121',
     'densenet161',
     'densenet169',
     'densenet201',
     'detection',
     'efficientnet',
     'efficientnet_b0',
     'efficientnet_b1',
     'efficientnet_b2',
     'efficientnet_b3',
     'efficientnet_b4',
     'efficientnet_b5',
     'efficientnet_b6',
     'efficientnet_b7',
     'efficientnet_v2_l',
     'efficientnet_v2_m',
     'efficientnet_v2_s',
     'get_model',
     'get_model_builder',
     'get_model_weights',
     'get_weight',
     'googlenet',
     'inception',
     'inception_v3',
     'list_models',
     'maxvit',
     'maxvit_t',
     'mnasnet',
     'mnasnet0_5',
     'mnasnet0_75',
     'mnasnet1_0',
     'mnasnet1_3',
     'mobilenet',
     'mobilenet_v2',
     'mobilenet_v3_large',
     'mobilenet_v3_small',
     'mobilenetv2',
     'mobilenetv3',
     'optical_flow',
     'quantization',
     'regnet',
     'regnet_x_16gf',
     'regnet_x_1_6gf',
     'regnet_x_32gf',
     'regnet_x_3_2gf',
     'regnet_x_400mf',
     'regnet_x_800mf',
     'regnet_x_8gf',
     'regnet_y_128gf',
     'regnet_y_16gf',
     'regnet_y_1_6gf',
     'regnet_y_32gf',
     'regnet_y_3_2gf',
     'regnet_y_400mf',
     'regnet_y_800mf',
     'regnet_y_8gf',
     'resnet',
     'resnet101',
     'resnet152',
     'resnet18',
     'resnet34',
     'resnet50',
     'resnext101_32x8d',
     'resnext101_64x4d',
     'resnext50_32x4d',
     'segmentation',
     'shufflenet_v2_x0_5',
     'shufflenet_v2_x1_0',
     'shufflenet_v2_x1_5',
     'shufflenet_v2_x2_0',
     'shufflenetv2',
     'squeezenet',
     'squeezenet1_0',
     'squeezenet1_1',
     'swin_b',
     'swin_s',
     'swin_t',
     'swin_transformer',
     'swin_v2_b',
     'swin_v2_s',
     'swin_v2_t',
     'vgg',
     'vgg11',
     'vgg11_bn',
     'vgg13',
     'vgg13_bn',
     'vgg16',
     'vgg16_bn',
     'vgg19',
     'vgg19_bn',
     'video',
     'vision_transformer',
     'vit_b_16',
     'vit_b_32',
     'vit_h_14',
     'vit_l_16',
     'vit_l_32',
     'wide_resnet101_2',
     'wide_resnet50_2']




```python
# net = models.alexnet(pretrained = True)

weights = models.AlexNet_Weights.IMAGENET1K_V1
net = models.alexnet(weights = weights)

# weights.transforms()
```


```python
print(net)
```

    AlexNet(
      (features): Sequential(
        (0): Conv2d(3, 64, kernel_size=(11, 11), stride=(4, 4), padding=(2, 2))
        (1): ReLU(inplace=True)
        (2): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
        (3): Conv2d(64, 192, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2))
        (4): ReLU(inplace=True)
        (5): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
        (6): Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (7): ReLU(inplace=True)
        (8): Conv2d(384, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (9): ReLU(inplace=True)
        (10): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (11): ReLU(inplace=True)
        (12): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
      )
      (avgpool): AdaptiveAvgPool2d(output_size=(6, 6))
      (classifier): Sequential(
        (0): Dropout(p=0.5, inplace=False)
        (1): Linear(in_features=9216, out_features=4096, bias=True)
        (2): ReLU(inplace=True)
        (3): Dropout(p=0.5, inplace=False)
        (4): Linear(in_features=4096, out_features=4096, bias=True)
        (5): ReLU(inplace=True)
        (6): Linear(in_features=4096, out_features=1000, bias=True)
      )
    )



```python
# 모델 개요 표시 2
# net = net.to(device)
summary(net,(100, 3, 112, 112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    AlexNet                                  [100, 1000]               --
    ├─Sequential: 1-1                        [100, 256, 2, 2]          --
    │    └─Conv2d: 2-1                       [100, 64, 27, 27]         23,296
    │    └─ReLU: 2-2                         [100, 64, 27, 27]         --
    │    └─MaxPool2d: 2-3                    [100, 64, 13, 13]         --
    │    └─Conv2d: 2-4                       [100, 192, 13, 13]        307,392
    │    └─ReLU: 2-5                         [100, 192, 13, 13]        --
    │    └─MaxPool2d: 2-6                    [100, 192, 6, 6]          --
    │    └─Conv2d: 2-7                       [100, 384, 6, 6]          663,936
    │    └─ReLU: 2-8                         [100, 384, 6, 6]          --
    │    └─Conv2d: 2-9                       [100, 256, 6, 6]          884,992
    │    └─ReLU: 2-10                        [100, 256, 6, 6]          --
    │    └─Conv2d: 2-11                      [100, 256, 6, 6]          590,080
    │    └─ReLU: 2-12                        [100, 256, 6, 6]          --
    │    └─MaxPool2d: 2-13                   [100, 256, 2, 2]          --
    ├─AdaptiveAvgPool2d: 1-2                 [100, 256, 6, 6]          --
    ├─Sequential: 1-3                        [100, 1000]               --
    │    └─Dropout: 2-14                     [100, 9216]               --
    │    └─Linear: 2-15                      [100, 4096]               37,752,832
    │    └─ReLU: 2-16                        [100, 4096]               --
    │    └─Dropout: 2-17                     [100, 4096]               --
    │    └─Linear: 2-18                      [100, 4096]               16,781,312
    │    └─ReLU: 2-19                        [100, 4096]               --
    │    └─Linear: 2-20                      [100, 1000]               4,097,000
    ==========================================================================================
    Total params: 61,100,840
    Trainable params: 61,100,840
    Non-trainable params: 0
    Total mult-adds (G): 20.46
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 96.44
    Params size (MB): 244.40
    Estimated Total Size (MB): 355.90
    ==========================================================================================




```python
## Access to the layers

print(net.classifier)
print(net.classifier[6])
print(net.classifier[6].in_features)
print(net.classifier[6].out_features)
print(net.classifier[6].bias)

```

    Sequential(
      (0): Dropout(p=0.5, inplace=False)
      (1): Linear(in_features=9216, out_features=4096, bias=True)
      (2): ReLU(inplace=True)
      (3): Dropout(p=0.5, inplace=False)
      (4): Linear(in_features=4096, out_features=4096, bias=True)
      (5): ReLU(inplace=True)
      (6): Linear(in_features=4096, out_features=1000, bias=True)
    )
    Linear(in_features=4096, out_features=1000, bias=True)
    4096
    1000
    Parameter containing:
    tensor([ 5.3252e-02,  5.6475e-02,  1.2015e-02,  1.0475e-02,  1.4073e-02,
             2.4921e-02,  4.5943e-02, -1.2418e-02, -5.2491e-02, -1.5580e-02,
            -2.1215e-02, -3.3407e-02,  9.5835e-03,  1.8659e-02,  7.1095e-03,
            -2.5249e-02, -2.9553e-03,  6.2285e-03, -3.0338e-02,  1.7713e-02,
             4.8128e-02,  5.5310e-02,  4.2137e-02, -3.4339e-02,  1.1161e-02,
            -3.7005e-02, -3.7998e-02, -2.2497e-02, -1.3564e-02,  1.1125e-01,
             3.1010e-02,  6.8569e-03, -1.5973e-02, -9.2437e-03,  4.3681e-02,
            -2.6168e-02, -3.0454e-03,  2.6335e-02,  1.0302e-02,  2.9396e-02,
            -1.6149e-02,  3.0833e-02,  4.0436e-02,  6.6803e-02,  2.4527e-02,
             4.6312e-02,  6.1914e-03,  8.0594e-02,  5.9732e-02,  6.1413e-02,
             1.6579e-03,  6.7179e-02, -4.2294e-03, -1.4659e-02, -6.7676e-02,
            -8.3818e-03, -5.8036e-02,  8.1914e-03,  3.9684e-02,  2.8477e-02,
            -1.2424e-01,  3.9262e-02,  9.1787e-03,  6.8728e-02,  4.0663e-02,
            -1.0124e-02,  1.2239e-02, -2.7275e-03, -2.1134e-02,  9.3186e-02,
             4.6140e-03,  2.6338e-02,  4.4615e-02, -1.2071e-02, -3.0606e-02,
             6.9681e-02,  4.3573e-02, -7.0400e-03,  3.4302e-02,  1.8671e-02,
            -2.3980e-03, -7.9588e-03, -2.6701e-02, -2.3112e-02, -2.1024e-02,
             7.5927e-03, -4.0854e-02,  9.6504e-02,  1.6273e-02,  6.8265e-02,
            -1.2029e-02,  1.8616e-02, -2.3254e-02,  6.6254e-04,  6.5770e-02,
             2.0797e-02,  4.6046e-02, -1.2563e-02,  1.5837e-02, -6.2019e-02,
             1.6890e-02,  2.9346e-02,  1.2199e-02,  1.1579e-01,  1.8052e-02,
             8.3501e-02,  4.6795e-02, -5.9661e-03,  4.3978e-02, -8.9776e-02,
            -8.6210e-02,  4.8310e-02, -2.1315e-02,  7.1201e-03, -3.1428e-02,
            -2.2256e-02,  9.2478e-02,  5.7419e-02, -2.9094e-04, -1.5966e-02,
             9.0139e-02, -1.8068e-02,  5.2080e-02, -1.0922e-02, -5.9916e-02,
             6.9528e-02, -4.0415e-03, -2.4078e-02,  1.2984e-02,  8.9963e-03,
            -3.2033e-02,  1.7807e-03,  3.9556e-02, -7.1310e-03, -8.6408e-02,
            -5.2836e-02, -3.0279e-02, -2.9701e-03,  2.8985e-02, -6.0586e-03,
            -1.5632e-02, -1.5263e-02, -1.4647e-02, -6.3525e-02, -3.9613e-02,
            -7.7837e-03, -7.8425e-03,  7.1100e-04, -7.7680e-04,  4.9023e-02,
            -2.2289e-03,  6.4397e-03, -9.0882e-02,  4.1336e-02, -6.3460e-03,
             1.4306e-02,  3.8303e-03, -3.1278e-02, -7.2626e-02, -3.5031e-02,
            -2.1359e-02,  6.8324e-02,  4.5042e-02,  2.8514e-02,  3.2959e-02,
            -4.6693e-02, -1.0623e-02, -6.0456e-02,  2.3472e-02,  1.9999e-02,
             2.5433e-02,  7.6092e-02, -6.2514e-03, -2.5429e-02,  6.6237e-02,
            -5.7913e-02, -1.8797e-02,  4.2716e-02,  5.1821e-02, -6.9029e-02,
            -1.5346e-02,  2.3568e-02,  5.2703e-02,  5.5551e-02, -8.4720e-03,
            -1.2149e-02, -2.7647e-03, -1.4819e-03, -2.3124e-02,  8.9908e-03,
            -3.7236e-03,  5.5263e-02,  3.0676e-02, -3.2228e-02, -6.9401e-03,
             5.0185e-02,  2.8821e-02,  3.6680e-03, -2.8823e-02,  5.0426e-02,
            -1.0344e-01, -2.1276e-03,  4.3640e-02,  3.0670e-02,  1.1708e-02,
            -8.2692e-03, -8.7994e-04, -7.9968e-03, -5.8294e-02,  7.0524e-02,
            -2.0286e-02,  2.0245e-03, -5.0412e-03, -1.7596e-02,  2.1311e-03,
            -1.2316e-02,  1.5342e-02,  3.2776e-02,  5.1759e-03, -4.1486e-02,
            -7.3661e-03, -1.9380e-02,  3.3047e-02,  8.3802e-02, -1.9553e-02,
             7.2874e-02, -3.5580e-03, -8.1869e-02,  2.6474e-02,  4.9446e-02,
             2.9175e-02, -7.6044e-02, -2.3432e-02,  2.2784e-02,  1.0188e-02,
             1.0420e-02,  5.3774e-03,  5.4046e-02,  1.4067e-02,  4.0287e-02,
            -4.9321e-02, -1.4429e-02, -4.6192e-02, -1.4586e-02, -2.6139e-02,
            -4.2562e-04, -5.0145e-02,  3.3987e-02, -5.3159e-02, -5.5430e-02,
             3.6954e-03, -1.1041e-03,  2.8349e-02, -4.4211e-02,  5.9482e-02,
            -1.5721e-02, -2.6858e-02,  2.9261e-02,  9.5011e-03,  2.4154e-03,
             1.3513e-02,  2.8245e-02, -6.4663e-02,  5.3230e-02, -4.3924e-02,
             3.4698e-04,  1.7564e-02, -9.1725e-02, -2.3233e-02,  2.2276e-02,
             4.0636e-02,  5.2172e-02,  3.5888e-02,  6.8130e-03,  1.0692e-02,
             2.1173e-03, -1.7580e-03, -2.7247e-03, -4.8340e-02,  1.3375e-02,
            -2.6605e-02,  8.5712e-02, -7.3576e-02,  2.3194e-02,  5.6535e-02,
             3.6531e-02,  7.1076e-02, -2.0128e-02, -5.6684e-02,  4.1176e-02,
            -1.7057e-02,  1.3072e-03,  1.3561e-02, -8.1499e-02, -1.9378e-02,
             3.5581e-02,  3.2518e-02,  6.2056e-02, -3.8972e-02,  4.0444e-02,
            -3.7356e-02, -2.5330e-02, -4.5012e-02, -5.6890e-02, -6.5692e-02,
             5.4484e-02,  4.5054e-02, -7.4308e-02,  1.1787e-03,  5.3284e-04,
            -6.7275e-02, -5.6026e-02, -7.0426e-02,  6.4871e-02,  4.1639e-02,
             8.3475e-02,  3.5982e-02,  2.0956e-02,  2.5103e-02, -1.6456e-02,
            -1.1024e-02, -2.6935e-02, -9.1414e-03, -5.0469e-02,  5.2238e-02,
            -2.6817e-02,  1.4414e-02, -1.0621e-01, -4.6598e-02, -2.5114e-02,
             8.4723e-03, -2.5711e-02,  9.3712e-02,  7.2801e-02,  2.5253e-02,
             2.1812e-02,  3.3336e-02,  1.6326e-02, -5.2736e-02,  5.5630e-02,
            -1.3830e-02, -4.0054e-02,  8.7340e-03,  3.1333e-02,  3.4241e-02,
            -5.1627e-02,  2.7252e-02,  2.6041e-02, -5.2250e-02,  2.6162e-02,
             5.1007e-02,  2.8195e-02, -2.4470e-02,  1.2946e-02,  5.2765e-02,
            -1.8762e-02, -3.1476e-02,  5.5163e-04,  1.0595e-02,  6.4026e-02,
            -1.0145e-02,  6.1711e-02,  2.9520e-02,  3.8700e-02,  4.4010e-02,
             2.8614e-02,  5.7040e-02,  4.6143e-02, -3.3167e-02,  2.5789e-02,
            -9.9446e-03, -3.0128e-03,  9.8479e-03,  3.3981e-02, -1.5649e-02,
            -9.9509e-03,  4.9874e-02, -6.3548e-04,  2.8995e-02,  7.9144e-03,
            -6.2499e-02, -5.1307e-02,  2.6480e-02,  1.4117e-02, -2.4593e-02,
             9.7300e-03, -1.0901e-02,  2.7393e-02,  1.5526e-02,  4.2757e-02,
            -4.2605e-02,  1.3845e-02, -1.6240e-02,  4.3815e-02, -2.3015e-03,
            -2.2745e-03,  2.7163e-02,  3.5608e-02, -3.9027e-02,  7.4795e-02,
             2.9545e-03,  2.4383e-02,  3.8495e-03,  7.3041e-03, -3.5850e-02,
             9.0172e-02, -1.9558e-03, -9.6829e-02, -6.6019e-02, -1.2339e-01,
             8.5293e-02, -2.8016e-02, -4.2111e-02,  3.4543e-03, -5.9704e-03,
            -4.0699e-02,  9.3167e-02,  3.8482e-03, -4.1334e-03,  9.7206e-03,
             1.7187e-02, -1.8781e-02, -2.0588e-02,  6.4882e-02,  6.1634e-02,
            -4.5338e-05, -4.7090e-02, -1.3213e-01,  2.8466e-02, -2.8057e-02,
             5.8503e-02,  6.6895e-02, -3.4372e-02, -1.4239e-02, -3.0599e-02,
             1.9456e-02, -3.3238e-02, -2.4988e-02, -9.0367e-05, -4.6692e-02,
            -4.8098e-02,  1.9271e-02,  2.4073e-02,  2.2539e-02, -5.8785e-03,
             1.5558e-02,  4.0886e-03, -7.8306e-02,  8.6316e-02, -1.4157e-02,
             8.7703e-02,  1.1080e-02,  2.4186e-02,  8.9802e-04, -1.2056e-02,
            -1.7418e-02, -3.5627e-03, -3.2366e-02, -1.3965e-03, -2.6253e-02,
            -2.4457e-02,  1.6563e-02, -1.8416e-02, -1.0767e-01,  9.6398e-03,
             4.2801e-02,  6.0262e-02,  3.9423e-02, -7.1208e-02,  3.1756e-02,
            -5.8451e-02, -4.1126e-02, -3.6470e-02,  3.2047e-02,  1.0938e-02,
             1.5454e-01,  3.8895e-02,  4.0750e-02,  2.8544e-02, -8.7241e-02,
             4.4254e-02, -5.8567e-03, -2.4539e-02, -3.7177e-02, -6.1798e-02,
             2.9119e-03, -1.5438e-02, -6.9551e-02, -1.3111e-01,  2.5559e-02,
             1.5085e-02,  7.0103e-02,  3.3266e-02, -2.6814e-02, -1.1635e-01,
            -1.3400e-02,  1.0656e-01, -1.6285e-01,  3.3475e-02, -3.2177e-02,
             4.8456e-02, -1.1730e-02, -8.8067e-02, -3.5880e-02,  1.3474e-02,
            -2.0326e-02, -1.2884e-01, -5.6742e-02, -6.5963e-02,  1.2026e-02,
            -2.5221e-02, -2.3785e-02, -9.6762e-03, -3.7816e-02,  1.9221e-02,
             4.8619e-03, -2.4410e-03, -2.6034e-02, -1.9117e-02, -8.2225e-04,
             1.7868e-02, -2.7427e-02,  4.1341e-02,  2.4172e-02,  6.8962e-02,
             6.3656e-02,  4.3324e-02, -1.6802e-02, -1.7103e-02,  3.2263e-02,
            -4.4776e-02, -8.3217e-02, -1.8283e-02,  5.8367e-02,  3.1406e-02,
             5.6282e-02, -1.1132e-01,  7.2988e-02, -1.0903e-01,  2.9206e-02,
            -2.7821e-02, -1.2398e-01, -2.5645e-02, -5.7258e-02,  8.1258e-03,
             2.6332e-02, -2.0495e-02, -4.6250e-02,  2.8908e-03,  9.5556e-02,
             4.4201e-02, -2.7812e-03,  2.2221e-03, -4.5316e-02, -4.3130e-02,
            -5.8415e-02,  3.2564e-02,  5.7614e-02, -7.8569e-02, -6.7936e-02,
            -6.6392e-03,  4.6499e-02, -5.6938e-02,  6.3510e-02,  6.6341e-02,
             1.3054e-02, -1.0774e-02, -5.5007e-02,  4.9877e-02,  2.0793e-02,
             1.5054e-02, -1.7921e-02, -6.6430e-02,  5.9132e-02,  2.1106e-02,
             1.8961e-02, -1.0129e-02,  1.8008e-02, -3.5435e-02,  1.4764e-02,
            -7.5889e-03, -8.3661e-02, -5.2211e-02,  6.8491e-02, -2.9039e-02,
            -1.9383e-02,  1.5508e-02, -1.8306e-02, -3.6809e-03,  5.0420e-02,
            -5.5348e-02,  5.0071e-03,  3.2704e-03, -5.4693e-03,  8.3264e-02,
            -2.6980e-02, -3.8524e-02,  7.7673e-02,  3.8679e-02, -4.3476e-02,
            -6.3778e-02,  7.1726e-03,  3.6365e-02,  3.5581e-02,  1.8565e-02,
            -1.5428e-02,  3.9404e-02,  1.0108e-02,  9.3341e-03, -4.7146e-02,
             3.6313e-02,  1.3648e-03,  4.9428e-02,  1.1902e-02, -6.4542e-03,
            -4.9254e-02, -1.1963e-01,  9.9042e-02, -2.6934e-02, -7.8272e-02,
             5.6361e-03,  1.2645e-02, -3.9618e-03,  2.2964e-02, -3.2064e-02,
            -4.6960e-02, -3.3381e-02,  2.9637e-02, -3.6173e-02,  3.0285e-03,
             1.7763e-02, -2.4117e-02, -5.6028e-02,  3.5110e-02,  7.2502e-02,
            -5.6726e-02, -6.1277e-02, -6.2330e-02, -6.4275e-02, -2.1981e-02,
            -1.6378e-02, -7.2263e-02,  3.9917e-02, -9.7765e-02, -4.7685e-02,
            -1.9302e-03, -2.4836e-02,  2.4878e-03,  5.6834e-02,  1.0820e-02,
            -3.2613e-02,  2.7537e-02,  5.3602e-03,  1.1122e-02, -3.4763e-02,
             3.4889e-02,  1.1450e-02, -3.3565e-02,  1.8182e-02, -2.5285e-02,
             7.6259e-02, -1.7923e-02,  8.6244e-03, -5.6801e-02, -2.0029e-02,
            -7.3464e-03,  7.8287e-03, -2.6822e-02,  4.8273e-03,  9.6238e-02,
             1.8904e-02,  3.5164e-02,  7.9271e-02, -1.4469e-02,  8.4794e-02,
             2.3145e-02, -4.8635e-02, -1.8980e-02,  1.3211e-02, -1.1367e-02,
             5.6345e-02, -3.2129e-02,  9.4927e-03, -4.3672e-02, -5.8385e-02,
             2.4477e-02, -4.1123e-02, -1.7410e-02, -2.2212e-02, -4.1425e-02,
             4.2289e-02,  8.7909e-02,  2.7870e-02, -7.8393e-02,  6.7135e-04,
             3.5587e-03, -2.1712e-02,  2.3001e-02, -8.1032e-02,  7.3319e-03,
            -3.3296e-04,  1.6864e-02,  1.7028e-02,  4.5052e-02,  2.4304e-03,
            -7.4777e-02,  6.0089e-02,  6.9517e-02, -5.7710e-02,  4.6902e-03,
            -3.8819e-03, -5.8210e-02, -1.1185e-03,  9.0919e-02, -8.7339e-03,
             6.4967e-02,  1.8759e-02, -5.0487e-02, -4.9778e-02,  4.9940e-02,
             2.3460e-02, -1.4869e-02,  7.7824e-03, -2.4576e-02, -4.5487e-02,
            -2.6208e-02,  1.3017e-01,  1.6476e-02, -3.0707e-02, -2.2029e-02,
            -2.6967e-02,  5.2982e-03,  1.7465e-02, -9.5463e-02, -8.5460e-02,
            -2.0266e-03, -2.9333e-03, -6.4850e-02,  7.8749e-02,  1.2722e-01,
            -3.0474e-02,  7.9202e-03, -1.4629e-02,  4.9757e-02, -6.1835e-02,
             4.2074e-02,  7.3102e-03,  4.7387e-02, -1.0757e-02,  6.5734e-02,
            -4.5547e-03,  2.7735e-03,  2.9592e-02,  5.8648e-03, -1.2238e-01,
             5.7966e-02,  6.0513e-02, -1.6859e-02, -4.4747e-02, -3.4610e-02,
             4.5194e-02,  6.8550e-04, -3.0971e-02,  6.2202e-02, -3.6581e-02,
            -2.7143e-02,  1.4357e-02, -2.3183e-03, -1.3557e-03, -2.3419e-02,
             7.2945e-02, -1.6167e-02, -6.4322e-02, -6.6394e-02,  8.7976e-03,
             5.5808e-03,  3.4428e-02,  4.3121e-02, -9.2526e-02, -6.9069e-02,
             7.7242e-03,  5.1836e-03, -5.7449e-02, -2.2806e-02, -4.3065e-02,
             1.4340e-01,  3.4542e-02, -3.3381e-02,  6.8073e-02, -4.3122e-02,
            -4.7611e-02,  1.2633e-02,  5.0245e-03,  5.3107e-02,  6.6606e-02,
             7.7941e-04,  2.1567e-02,  2.8193e-02, -6.4781e-03,  4.6802e-02,
            -8.1779e-02,  4.5102e-02,  4.3365e-02,  5.0884e-02,  5.0874e-03,
            -4.0991e-02, -5.6369e-02,  4.3932e-02, -1.1832e-02, -3.3235e-02,
            -7.4081e-02, -3.1906e-02,  1.6910e-02, -3.5907e-02,  1.9498e-03,
             3.7387e-03,  7.7815e-02, -3.8847e-02, -5.2373e-02,  3.9722e-02,
            -1.2653e-02, -4.8730e-02,  2.3529e-02,  1.2015e-02, -2.3584e-02,
            -4.2143e-03, -7.1829e-02, -8.9830e-02, -1.8455e-02, -5.9362e-02,
             1.7717e-02,  5.4384e-02,  3.6537e-03,  5.3803e-03,  7.9031e-02,
             2.2240e-02, -1.0549e-02, -4.5449e-03, -2.8834e-02, -1.0402e-02,
             2.6980e-03, -4.7863e-02, -7.3498e-04,  8.8465e-02, -2.0006e-02,
            -1.0358e-02, -1.3307e-02,  2.0518e-02,  5.8219e-03, -4.0321e-02,
            -8.3064e-03, -4.7484e-02, -7.1105e-02,  2.8095e-02,  7.1692e-03,
             5.3178e-02, -7.2905e-03, -2.0805e-02, -6.9260e-02,  4.5134e-02,
            -1.2814e-02,  1.2746e-02, -4.9280e-03,  2.4691e-02, -3.4422e-02,
             6.3144e-02, -2.1781e-02, -5.0597e-02, -7.5548e-02, -3.2391e-02,
             1.2470e-02, -6.6609e-02, -3.3134e-02, -2.6591e-02, -4.1465e-02,
            -1.8827e-02, -3.0473e-04,  1.5325e-02, -4.7332e-02, -5.5676e-02,
             2.1460e-02,  1.9186e-02,  5.3556e-03, -3.1528e-02,  9.7987e-03,
            -5.7906e-02, -3.7041e-02,  2.0125e-02, -5.3023e-03,  3.0509e-03,
             3.0903e-02, -1.9810e-02, -2.5124e-02,  2.5123e-02,  2.1905e-02,
             1.6592e-03,  8.0100e-03,  2.1628e-02, -4.9679e-02, -6.8297e-02,
             2.9881e-03,  1.1875e-02, -6.6792e-02,  1.3855e-02,  6.1322e-02,
             7.8280e-02,  4.3107e-02, -4.0548e-02,  1.3512e-02,  3.3229e-02,
            -5.1434e-02, -7.5863e-02, -3.1879e-02, -1.8831e-02, -5.0711e-03,
             4.9725e-02,  8.4448e-03,  3.9326e-02,  7.1417e-02,  4.9369e-02,
            -2.7340e-02,  7.9479e-02,  1.8443e-04,  3.4903e-02,  2.6848e-02,
             2.9325e-02,  2.4565e-02,  1.3714e-02,  1.0439e-02,  8.2166e-02,
             2.2898e-02, -4.9901e-02, -1.2849e-01,  4.4965e-02,  5.4320e-02,
             3.0903e-02,  2.7644e-02, -5.0354e-02, -2.5691e-02, -6.2493e-03,
             2.7136e-02,  1.1583e-02,  1.8871e-02, -3.5744e-02, -6.0619e-02,
            -1.2422e-02, -1.4326e-02, -9.8677e-02, -3.8423e-02, -3.8647e-02,
            -9.1581e-02, -4.2368e-02, -4.9885e-02, -1.6033e-02, -4.5562e-02,
             2.4515e-02, -2.1699e-02,  3.7827e-03, -3.4757e-02, -4.1276e-02,
             3.3561e-02,  5.7945e-02,  6.3927e-02,  7.1584e-03,  2.8452e-02,
             1.1123e-01, -2.2850e-02,  1.3239e-02, -8.6398e-02,  4.5526e-02,
            -2.9062e-03,  6.4437e-02,  2.3639e-02, -6.8218e-02,  3.5062e-02,
            -1.6846e-02,  2.8718e-02,  2.8398e-02, -9.9861e-04, -4.5618e-03,
             3.5558e-02,  4.4268e-02,  7.9080e-02,  1.6179e-02, -5.6045e-03,
            -3.0647e-02,  2.7647e-02, -1.0381e-01, -3.2340e-02, -8.2798e-03,
            -1.2683e-02, -6.8346e-02, -8.5445e-03, -1.1209e-02,  3.1321e-02,
            -1.0558e-02, -2.0959e-02,  3.0059e-02, -5.2112e-02,  2.3731e-02],
           device='cuda:0', requires_grad=True)


## 최종 레이어 함수 교체하기


```python
# 난수 고정
torch_seed()

# 최종 레이어 함수 교체
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, n_output)

# features 마지막의 MaxPool2d 제거
# net.features = net.features[:-1]

# AdaptiveAvgPool2d 제거
# net.avgpool = nn.Identity()
```


```python
# 모델 개요 표시 1
print(net)
```

    AlexNet(
      (features): Sequential(
        (0): Conv2d(3, 64, kernel_size=(11, 11), stride=(4, 4), padding=(2, 2))
        (1): ReLU(inplace=True)
        (2): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
        (3): Conv2d(64, 192, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2))
        (4): ReLU(inplace=True)
        (5): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
        (6): Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (7): ReLU(inplace=True)
        (8): Conv2d(384, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (9): ReLU(inplace=True)
        (10): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (11): ReLU(inplace=True)
        (12): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=False)
      )
      (avgpool): AdaptiveAvgPool2d(output_size=(6, 6))
      (classifier): Sequential(
        (0): Dropout(p=0.5, inplace=False)
        (1): Linear(in_features=9216, out_features=4096, bias=True)
        (2): ReLU(inplace=True)
        (3): Dropout(p=0.5, inplace=False)
        (4): Linear(in_features=4096, out_features=4096, bias=True)
        (5): ReLU(inplace=True)
        (6): Linear(in_features=4096, out_features=10, bias=True)
      )
    )



```python
# 손실 계산 그래프 시각화
net = net.to(device)
criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__30_0.svg)
    


## 학습과 결과 평가

### 초기 설정


```python
# 난수 고정
torch_seed()

# 사전 학습 모델 불러오기
# pretraind = True로 학습을 마친 파라미터도 함께 불러오기
weights = models.AlexNet_Weights.IMAGENET1K_V1
net = models.alexnet(weights = weights)

# 최종 레이어 함수 입력 차원수 확인
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, n_output)

# 최종 레이어 함수 교체
net.fc = nn.Linear(in_features, n_output)

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)

# history 파일 초기화
history = np.zeros((0, 5))
```

### 학습


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
        train_loader, test_loader, device, history)
```


      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.88723 acc: 0.68882 val_loss: 0.52400, val_acc: 0.81490



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.64617 acc: 0.77202 val_loss: 0.46861, val_acc: 0.83910



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.56864 acc: 0.80250 val_loss: 0.41946, val_acc: 0.85550



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.51698 acc: 0.81954 val_loss: 0.38899, val_acc: 0.86610



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.47502 acc: 0.83350 val_loss: 0.39600, val_acc: 0.86080


### 학습 결과 평가


```python
# 결과 요약
evaluate_history(history)
```

    초기상태 : 손실 : 0.52400  정확도 : 0.81490
    최종상태 : 손실 : 0.39600 정확도 : 0.86080



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__37_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__37_2.webp)
    



```python
# 이미지와 정답, 예측 결과를 함께 표시
show_images_labels(test_loader, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__38_1.webp)
    


## GoogLeNet 불러 오기

### 모델 불러오기


```python
#  라이브러리 임포트
from torchvision import models

# dir(models)
weights = models.GoogLeNet_Weights.IMAGENET1K_V1
net = models.googlenet(weights=weights)
```


```python
# 모델 개요 표시 1
print(net)
```

    GoogLeNet(
      (conv1): BasicConv2d(
        (conv): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool1): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (conv2): BasicConv2d(
        (conv): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (conv3): BasicConv2d(
        (conv): Conv2d(64, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool2): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception3a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(192, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(192, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception3b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 96, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool3): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception4a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(480, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 208, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(208, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 48, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(480, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(112, 224, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(224, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4c): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4d): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 144, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(144, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(144, 288, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(288, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4e): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(528, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(528, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception5a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception5b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 384, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 48, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(48, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (aux1): None
      (aux2): None
      (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
      (dropout): Dropout(p=0.2, inplace=False)
      (fc): Linear(in_features=1024, out_features=1000, bias=True)
    )



```python
# 모델 개요 표시 2
# net = net.to(device)
summary(net, (100, 3, 224, 224))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    GoogLeNet                                [100, 1000]               --
    ├─BasicConv2d: 1-1                       [100, 64, 112, 112]       --
    │    └─Conv2d: 2-1                       [100, 64, 112, 112]       9,408
    │    └─BatchNorm2d: 2-2                  [100, 64, 112, 112]       128
    ├─MaxPool2d: 1-2                         [100, 64, 56, 56]         --
    ├─BasicConv2d: 1-3                       [100, 64, 56, 56]         --
    │    └─Conv2d: 2-3                       [100, 64, 56, 56]         4,096
    │    └─BatchNorm2d: 2-4                  [100, 64, 56, 56]         128
    ├─BasicConv2d: 1-4                       [100, 192, 56, 56]        --
    │    └─Conv2d: 2-5                       [100, 192, 56, 56]        110,592
    │    └─BatchNorm2d: 2-6                  [100, 192, 56, 56]        384
    ├─MaxPool2d: 1-5                         [100, 192, 28, 28]        --
    ├─Inception: 1-6                         [100, 256, 28, 28]        --
    │    └─BasicConv2d: 2-7                  [100, 64, 28, 28]         --
    │    │    └─Conv2d: 3-1                  [100, 64, 28, 28]         12,288
    │    │    └─BatchNorm2d: 3-2             [100, 64, 28, 28]         128
    │    └─Sequential: 2-8                   [100, 128, 28, 28]        --
    │    │    └─BasicConv2d: 3-3             [100, 96, 28, 28]         18,624
    │    │    └─BasicConv2d: 3-4             [100, 128, 28, 28]        110,848
    │    └─Sequential: 2-9                   [100, 32, 28, 28]         --
    │    │    └─BasicConv2d: 3-5             [100, 16, 28, 28]         3,104
    │    │    └─BasicConv2d: 3-6             [100, 32, 28, 28]         4,672
    │    └─Sequential: 2-10                  [100, 32, 28, 28]         --
    │    │    └─MaxPool2d: 3-7               [100, 192, 28, 28]        --
    │    │    └─BasicConv2d: 3-8             [100, 32, 28, 28]         6,208
    ├─Inception: 1-7                         [100, 480, 28, 28]        --
    │    └─BasicConv2d: 2-11                 [100, 128, 28, 28]        --
    │    │    └─Conv2d: 3-9                  [100, 128, 28, 28]        32,768
    │    │    └─BatchNorm2d: 3-10            [100, 128, 28, 28]        256
    │    └─Sequential: 2-12                  [100, 192, 28, 28]        --
    │    │    └─BasicConv2d: 3-11            [100, 128, 28, 28]        33,024
    │    │    └─BasicConv2d: 3-12            [100, 192, 28, 28]        221,568
    │    └─Sequential: 2-13                  [100, 96, 28, 28]         --
    │    │    └─BasicConv2d: 3-13            [100, 32, 28, 28]         8,256
    │    │    └─BasicConv2d: 3-14            [100, 96, 28, 28]         27,840
    │    └─Sequential: 2-14                  [100, 64, 28, 28]         --
    │    │    └─MaxPool2d: 3-15              [100, 256, 28, 28]        --
    │    │    └─BasicConv2d: 3-16            [100, 64, 28, 28]         16,512
    ├─MaxPool2d: 1-8                         [100, 480, 14, 14]        --
    ├─Inception: 1-9                         [100, 512, 14, 14]        --
    │    └─BasicConv2d: 2-15                 [100, 192, 14, 14]        --
    │    │    └─Conv2d: 3-17                 [100, 192, 14, 14]        92,160
    │    │    └─BatchNorm2d: 3-18            [100, 192, 14, 14]        384
    │    └─Sequential: 2-16                  [100, 208, 14, 14]        --
    │    │    └─BasicConv2d: 3-19            [100, 96, 14, 14]         46,272
    │    │    └─BasicConv2d: 3-20            [100, 208, 14, 14]        180,128
    │    └─Sequential: 2-17                  [100, 48, 14, 14]         --
    │    │    └─BasicConv2d: 3-21            [100, 16, 14, 14]         7,712
    │    │    └─BasicConv2d: 3-22            [100, 48, 14, 14]         7,008
    │    └─Sequential: 2-18                  [100, 64, 14, 14]         --
    │    │    └─MaxPool2d: 3-23              [100, 480, 14, 14]        --
    │    │    └─BasicConv2d: 3-24            [100, 64, 14, 14]         30,848
    ├─Inception: 1-10                        [100, 512, 14, 14]        --
    │    └─BasicConv2d: 2-19                 [100, 160, 14, 14]        --
    │    │    └─Conv2d: 3-25                 [100, 160, 14, 14]        81,920
    │    │    └─BatchNorm2d: 3-26            [100, 160, 14, 14]        320
    │    └─Sequential: 2-20                  [100, 224, 14, 14]        --
    │    │    └─BasicConv2d: 3-27            [100, 112, 14, 14]        57,568
    │    │    └─BasicConv2d: 3-28            [100, 224, 14, 14]        226,240
    │    └─Sequential: 2-21                  [100, 64, 14, 14]         --
    │    │    └─BasicConv2d: 3-29            [100, 24, 14, 14]         12,336
    │    │    └─BasicConv2d: 3-30            [100, 64, 14, 14]         13,952
    │    └─Sequential: 2-22                  [100, 64, 14, 14]         --
    │    │    └─MaxPool2d: 3-31              [100, 512, 14, 14]        --
    │    │    └─BasicConv2d: 3-32            [100, 64, 14, 14]         32,896
    ├─Inception: 1-11                        [100, 512, 14, 14]        --
    │    └─BasicConv2d: 2-23                 [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-33                 [100, 128, 14, 14]        65,536
    │    │    └─BatchNorm2d: 3-34            [100, 128, 14, 14]        256
    │    └─Sequential: 2-24                  [100, 256, 14, 14]        --
    │    │    └─BasicConv2d: 3-35            [100, 128, 14, 14]        65,792
    │    │    └─BasicConv2d: 3-36            [100, 256, 14, 14]        295,424
    │    └─Sequential: 2-25                  [100, 64, 14, 14]         --
    │    │    └─BasicConv2d: 3-37            [100, 24, 14, 14]         12,336
    │    │    └─BasicConv2d: 3-38            [100, 64, 14, 14]         13,952
    │    └─Sequential: 2-26                  [100, 64, 14, 14]         --
    │    │    └─MaxPool2d: 3-39              [100, 512, 14, 14]        --
    │    │    └─BasicConv2d: 3-40            [100, 64, 14, 14]         32,896
    ├─Inception: 1-12                        [100, 528, 14, 14]        --
    │    └─BasicConv2d: 2-27                 [100, 112, 14, 14]        --
    │    │    └─Conv2d: 3-41                 [100, 112, 14, 14]        57,344
    │    │    └─BatchNorm2d: 3-42            [100, 112, 14, 14]        224
    │    └─Sequential: 2-28                  [100, 288, 14, 14]        --
    │    │    └─BasicConv2d: 3-43            [100, 144, 14, 14]        74,016
    │    │    └─BasicConv2d: 3-44            [100, 288, 14, 14]        373,824
    │    └─Sequential: 2-29                  [100, 64, 14, 14]         --
    │    │    └─BasicConv2d: 3-45            [100, 32, 14, 14]         16,448
    │    │    └─BasicConv2d: 3-46            [100, 64, 14, 14]         18,560
    │    └─Sequential: 2-30                  [100, 64, 14, 14]         --
    │    │    └─MaxPool2d: 3-47              [100, 512, 14, 14]        --
    │    │    └─BasicConv2d: 3-48            [100, 64, 14, 14]         32,896
    ├─Inception: 1-13                        [100, 832, 14, 14]        --
    │    └─BasicConv2d: 2-31                 [100, 256, 14, 14]        --
    │    │    └─Conv2d: 3-49                 [100, 256, 14, 14]        135,168
    │    │    └─BatchNorm2d: 3-50            [100, 256, 14, 14]        512
    │    └─Sequential: 2-32                  [100, 320, 14, 14]        --
    │    │    └─BasicConv2d: 3-51            [100, 160, 14, 14]        84,800
    │    │    └─BasicConv2d: 3-52            [100, 320, 14, 14]        461,440
    │    └─Sequential: 2-33                  [100, 128, 14, 14]        --
    │    │    └─BasicConv2d: 3-53            [100, 32, 14, 14]         16,960
    │    │    └─BasicConv2d: 3-54            [100, 128, 14, 14]        37,120
    │    └─Sequential: 2-34                  [100, 128, 14, 14]        --
    │    │    └─MaxPool2d: 3-55              [100, 528, 14, 14]        --
    │    │    └─BasicConv2d: 3-56            [100, 128, 14, 14]        67,840
    ├─MaxPool2d: 1-14                        [100, 832, 7, 7]          --
    ├─Inception: 1-15                        [100, 832, 7, 7]          --
    │    └─BasicConv2d: 2-35                 [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-57                 [100, 256, 7, 7]          212,992
    │    │    └─BatchNorm2d: 3-58            [100, 256, 7, 7]          512
    │    └─Sequential: 2-36                  [100, 320, 7, 7]          --
    │    │    └─BasicConv2d: 3-59            [100, 160, 7, 7]          133,440
    │    │    └─BasicConv2d: 3-60            [100, 320, 7, 7]          461,440
    │    └─Sequential: 2-37                  [100, 128, 7, 7]          --
    │    │    └─BasicConv2d: 3-61            [100, 32, 7, 7]           26,688
    │    │    └─BasicConv2d: 3-62            [100, 128, 7, 7]          37,120
    │    └─Sequential: 2-38                  [100, 128, 7, 7]          --
    │    │    └─MaxPool2d: 3-63              [100, 832, 7, 7]          --
    │    │    └─BasicConv2d: 3-64            [100, 128, 7, 7]          106,752
    ├─Inception: 1-16                        [100, 1024, 7, 7]         --
    │    └─BasicConv2d: 2-39                 [100, 384, 7, 7]          --
    │    │    └─Conv2d: 3-65                 [100, 384, 7, 7]          319,488
    │    │    └─BatchNorm2d: 3-66            [100, 384, 7, 7]          768
    │    └─Sequential: 2-40                  [100, 384, 7, 7]          --
    │    │    └─BasicConv2d: 3-67            [100, 192, 7, 7]          160,128
    │    │    └─BasicConv2d: 3-68            [100, 384, 7, 7]          664,320
    │    └─Sequential: 2-41                  [100, 128, 7, 7]          --
    │    │    └─BasicConv2d: 3-69            [100, 48, 7, 7]           40,032
    │    │    └─BasicConv2d: 3-70            [100, 128, 7, 7]          55,552
    │    └─Sequential: 2-42                  [100, 128, 7, 7]          --
    │    │    └─MaxPool2d: 3-71              [100, 832, 7, 7]          --
    │    │    └─BasicConv2d: 3-72            [100, 128, 7, 7]          106,752
    ├─AdaptiveAvgPool2d: 1-17                [100, 1024, 1, 1]         --
    ├─Dropout: 1-18                          [100, 1024]               --
    ├─Linear: 1-19                           [100, 1000]               1,025,000
    ==========================================================================================
    Total params: 6,624,904
    Trainable params: 6,624,904
    Non-trainable params: 0
    Total mult-adds (G): 149.84
    ==========================================================================================
    Input size (MB): 60.21
    Forward/backward pass size (MB): 5162.66
    Params size (MB): 26.50
    Estimated Total Size (MB): 5249.37
    ==========================================================================================



## 파인 튜닝 없이 사용하기
### 영상 읽기


```python
### Step 2: Read image
## rgb format, <class 'torch.Tensor'>
from torchvision.io import read_image

net.eval()

filename = "./beagle.jpg"
img = read_image(filename) # torch.Size([3, 366, 640]) 
img = img.to(device)

##
print("img type = ", type(img))
print("img shape = ", img.shape) # torch.Size([3, 366, 640]))
```

    img type =  <class 'torch.Tensor'>
    img shape =  torch.Size([3, 366, 640])


### 영상 변환


```python
# preprocess
# Scaling pixel values down to the [0, 1] range from their original [0, 255] range before applying normalization.
# ImageClassification(
#     crop_size=[224]
#     resize_size=[256]
#     mean=[0.485, 0.456, 0.406]
#     std=[0.229, 0.224, 0.225]
#     interpolation=InterpolationMode.BILINEAR
# )

preprocess = weights.transforms()
print(preprocess)
```

    ImageClassification(
        crop_size=[224]
        resize_size=[256]
        mean=[0.485, 0.456, 0.406]
        std=[0.229, 0.224, 0.225]
        interpolation=InterpolationMode.BILINEAR
    )


### 변환 영상 확인하기


```python
batch = preprocess(img).unsqueeze(0).to(device)
print(batch.shape)

##
processed_img = batch.data[0]
plt_img = processed_img.permute(1, 2, 0)

# plt_img.shape
plt.imshow(plt_img.cpu().numpy())
plt.grid(visible = None)
plt.axis("off")
plt.show()
```

    Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers). Got range [-2.0665298..2.3611333].


    torch.Size([1, 3, 224, 224])



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__49_2.webp)
    



```python
# Step 5: Use the model and print the predicted category
net = net.to(device)
prediction = net(batch).softmax(1) # (1, 1000)
class_id = prediction.argmax().item() 
print("class id = ", class_id)
```

    class id =  162


### 결과 확인 하기


```python
display("category = \n", weights.meta["categories"])
print("category number = ", len(weights.meta["categories"]))
```


    'category = \n'



    ['tench',
     'goldfish',
     'great white shark',
     'tiger shark',
     'hammerhead',
     'electric ray',
     'stingray',
     'cock',
     'hen',
     'ostrich',
     'brambling',
     'goldfinch',
     'house finch',
     'junco',
     'indigo bunting',
     'robin',
     'bulbul',
     'jay',
     'magpie',
     'chickadee',
     'water ouzel',
     'kite',
     'bald eagle',
     'vulture',
     'great grey owl',
     'European fire salamander',
     'common newt',
     'eft',
     'spotted salamander',
     'axolotl',
     'bullfrog',
     'tree frog',
     'tailed frog',
     'loggerhead',
     'leatherback turtle',
     'mud turtle',
     'terrapin',
     'box turtle',
     'banded gecko',
     'common iguana',
     'American chameleon',
     'whiptail',
     'agama',
     'frilled lizard',
     'alligator lizard',
     'Gila monster',
     'green lizard',
     'African chameleon',
     'Komodo dragon',
     'African crocodile',
     'American alligator',
     'triceratops',
     'thunder snake',
     'ringneck snake',
     'hognose snake',
     'green snake',
     'king snake',
     'garter snake',
     'water snake',
     'vine snake',
     'night snake',
     'boa constrictor',
     'rock python',
     'Indian cobra',
     'green mamba',
     'sea snake',
     'horned viper',
     'diamondback',
     'sidewinder',
     'trilobite',
     'harvestman',
     'scorpion',
     'black and gold garden spider',
     'barn spider',
     'garden spider',
     'black widow',
     'tarantula',
     'wolf spider',
     'tick',
     'centipede',
     'black grouse',
     'ptarmigan',
     'ruffed grouse',
     'prairie chicken',
     'peacock',
     'quail',
     'partridge',
     'African grey',
     'macaw',
     'sulphur-crested cockatoo',
     'lorikeet',
     'coucal',
     'bee eater',
     'hornbill',
     'hummingbird',
     'jacamar',
     'toucan',
     'drake',
     'red-breasted merganser',
     'goose',
     'black swan',
     'tusker',
     'echidna',
     'platypus',
     'wallaby',
     'koala',
     'wombat',
     'jellyfish',
     'sea anemone',
     'brain coral',
     'flatworm',
     'nematode',
     'conch',
     'snail',
     'slug',
     'sea slug',
     'chiton',
     'chambered nautilus',
     'Dungeness crab',
     'rock crab',
     'fiddler crab',
     'king crab',
     'American lobster',
     'spiny lobster',
     'crayfish',
     'hermit crab',
     'isopod',
     'white stork',
     'black stork',
     'spoonbill',
     'flamingo',
     'little blue heron',
     'American egret',
     'bittern',
     'crane bird',
     'limpkin',
     'European gallinule',
     'American coot',
     'bustard',
     'ruddy turnstone',
     'red-backed sandpiper',
     'redshank',
     'dowitcher',
     'oystercatcher',
     'pelican',
     'king penguin',
     'albatross',
     'grey whale',
     'killer whale',
     'dugong',
     'sea lion',
     'Chihuahua',
     'Japanese spaniel',
     'Maltese dog',
     'Pekinese',
     'Shih-Tzu',
     'Blenheim spaniel',
     'papillon',
     'toy terrier',
     'Rhodesian ridgeback',
     'Afghan hound',
     'basset',
     'beagle',
     'bloodhound',
     'bluetick',
     'black-and-tan coonhound',
     'Walker hound',
     'English foxhound',
     'redbone',
     'borzoi',
     'Irish wolfhound',
     'Italian greyhound',
     'whippet',
     'Ibizan hound',
     'Norwegian elkhound',
     'otterhound',
     'Saluki',
     'Scottish deerhound',
     'Weimaraner',
     'Staffordshire bullterrier',
     'American Staffordshire terrier',
     'Bedlington terrier',
     'Border terrier',
     'Kerry blue terrier',
     'Irish terrier',
     'Norfolk terrier',
     'Norwich terrier',
     'Yorkshire terrier',
     'wire-haired fox terrier',
     'Lakeland terrier',
     'Sealyham terrier',
     'Airedale',
     'cairn',
     'Australian terrier',
     'Dandie Dinmont',
     'Boston bull',
     'miniature schnauzer',
     'giant schnauzer',
     'standard schnauzer',
     'Scotch terrier',
     'Tibetan terrier',
     'silky terrier',
     'soft-coated wheaten terrier',
     'West Highland white terrier',
     'Lhasa',
     'flat-coated retriever',
     'curly-coated retriever',
     'golden retriever',
     'Labrador retriever',
     'Chesapeake Bay retriever',
     'German short-haired pointer',
     'vizsla',
     'English setter',
     'Irish setter',
     'Gordon setter',
     'Brittany spaniel',
     'clumber',
     'English springer',
     'Welsh springer spaniel',
     'cocker spaniel',
     'Sussex spaniel',
     'Irish water spaniel',
     'kuvasz',
     'schipperke',
     'groenendael',
     'malinois',
     'briard',
     'kelpie',
     'komondor',
     'Old English sheepdog',
     'Shetland sheepdog',
     'collie',
     'Border collie',
     'Bouvier des Flandres',
     'Rottweiler',
     'German shepherd',
     'Doberman',
     'miniature pinscher',
     'Greater Swiss Mountain dog',
     'Bernese mountain dog',
     'Appenzeller',
     'EntleBucher',
     'boxer',
     'bull mastiff',
     'Tibetan mastiff',
     'French bulldog',
     'Great Dane',
     'Saint Bernard',
     'Eskimo dog',
     'malamute',
     'Siberian husky',
     'dalmatian',
     'affenpinscher',
     'basenji',
     'pug',
     'Leonberg',
     'Newfoundland',
     'Great Pyrenees',
     'Samoyed',
     'Pomeranian',
     'chow',
     'keeshond',
     'Brabancon griffon',
     'Pembroke',
     'Cardigan',
     'toy poodle',
     'miniature poodle',
     'standard poodle',
     'Mexican hairless',
     'timber wolf',
     'white wolf',
     'red wolf',
     'coyote',
     'dingo',
     'dhole',
     'African hunting dog',
     'hyena',
     'red fox',
     'kit fox',
     'Arctic fox',
     'grey fox',
     'tabby',
     'tiger cat',
     'Persian cat',
     'Siamese cat',
     'Egyptian cat',
     'cougar',
     'lynx',
     'leopard',
     'snow leopard',
     'jaguar',
     'lion',
     'tiger',
     'cheetah',
     'brown bear',
     'American black bear',
     'ice bear',
     'sloth bear',
     'mongoose',
     'meerkat',
     'tiger beetle',
     'ladybug',
     'ground beetle',
     'long-horned beetle',
     'leaf beetle',
     'dung beetle',
     'rhinoceros beetle',
     'weevil',
     'fly',
     'bee',
     'ant',
     'grasshopper',
     'cricket',
     'walking stick',
     'cockroach',
     'mantis',
     'cicada',
     'leafhopper',
     'lacewing',
     'dragonfly',
     'damselfly',
     'admiral',
     'ringlet',
     'monarch',
     'cabbage butterfly',
     'sulphur butterfly',
     'lycaenid',
     'starfish',
     'sea urchin',
     'sea cucumber',
     'wood rabbit',
     'hare',
     'Angora',
     'hamster',
     'porcupine',
     'fox squirrel',
     'marmot',
     'beaver',
     'guinea pig',
     'sorrel',
     'zebra',
     'hog',
     'wild boar',
     'warthog',
     'hippopotamus',
     'ox',
     'water buffalo',
     'bison',
     'ram',
     'bighorn',
     'ibex',
     'hartebeest',
     'impala',
     'gazelle',
     'Arabian camel',
     'llama',
     'weasel',
     'mink',
     'polecat',
     'black-footed ferret',
     'otter',
     'skunk',
     'badger',
     'armadillo',
     'three-toed sloth',
     'orangutan',
     'gorilla',
     'chimpanzee',
     'gibbon',
     'siamang',
     'guenon',
     'patas',
     'baboon',
     'macaque',
     'langur',
     'colobus',
     'proboscis monkey',
     'marmoset',
     'capuchin',
     'howler monkey',
     'titi',
     'spider monkey',
     'squirrel monkey',
     'Madagascar cat',
     'indri',
     'Indian elephant',
     'African elephant',
     'lesser panda',
     'giant panda',
     'barracouta',
     'eel',
     'coho',
     'rock beauty',
     'anemone fish',
     'sturgeon',
     'gar',
     'lionfish',
     'puffer',
     'abacus',
     'abaya',
     'academic gown',
     'accordion',
     'acoustic guitar',
     'aircraft carrier',
     'airliner',
     'airship',
     'altar',
     'ambulance',
     'amphibian',
     'analog clock',
     'apiary',
     'apron',
     'ashcan',
     'assault rifle',
     'backpack',
     'bakery',
     'balance beam',
     'balloon',
     'ballpoint',
     'Band Aid',
     'banjo',
     'bannister',
     'barbell',
     'barber chair',
     'barbershop',
     'barn',
     'barometer',
     'barrel',
     'barrow',
     'baseball',
     'basketball',
     'bassinet',
     'bassoon',
     'bathing cap',
     'bath towel',
     'bathtub',
     'beach wagon',
     'beacon',
     'beaker',
     'bearskin',
     'beer bottle',
     'beer glass',
     'bell cote',
     'bib',
     'bicycle-built-for-two',
     'bikini',
     'binder',
     'binoculars',
     'birdhouse',
     'boathouse',
     'bobsled',
     'bolo tie',
     'bonnet',
     'bookcase',
     'bookshop',
     'bottlecap',
     'bow',
     'bow tie',
     'brass',
     'brassiere',
     'breakwater',
     'breastplate',
     'broom',
     'bucket',
     'buckle',
     'bulletproof vest',
     'bullet train',
     'butcher shop',
     'cab',
     'caldron',
     'candle',
     'cannon',
     'canoe',
     'can opener',
     'cardigan',
     'car mirror',
     'carousel',
     "carpenter's kit",
     'carton',
     'car wheel',
     'cash machine',
     'cassette',
     'cassette player',
     'castle',
     'catamaran',
     'CD player',
     'cello',
     'cellular telephone',
     'chain',
     'chainlink fence',
     'chain mail',
     'chain saw',
     'chest',
     'chiffonier',
     'chime',
     'china cabinet',
     'Christmas stocking',
     'church',
     'cinema',
     'cleaver',
     'cliff dwelling',
     'cloak',
     'clog',
     'cocktail shaker',
     'coffee mug',
     'coffeepot',
     'coil',
     'combination lock',
     'computer keyboard',
     'confectionery',
     'container ship',
     'convertible',
     'corkscrew',
     'cornet',
     'cowboy boot',
     'cowboy hat',
     'cradle',
     'crane',
     'crash helmet',
     'crate',
     'crib',
     'Crock Pot',
     'croquet ball',
     'crutch',
     'cuirass',
     'dam',
     'desk',
     'desktop computer',
     'dial telephone',
     'diaper',
     'digital clock',
     'digital watch',
     'dining table',
     'dishrag',
     'dishwasher',
     'disk brake',
     'dock',
     'dogsled',
     'dome',
     'doormat',
     'drilling platform',
     'drum',
     'drumstick',
     'dumbbell',
     'Dutch oven',
     'electric fan',
     'electric guitar',
     'electric locomotive',
     'entertainment center',
     'envelope',
     'espresso maker',
     'face powder',
     'feather boa',
     'file',
     'fireboat',
     'fire engine',
     'fire screen',
     'flagpole',
     'flute',
     'folding chair',
     'football helmet',
     'forklift',
     'fountain',
     'fountain pen',
     'four-poster',
     'freight car',
     'French horn',
     'frying pan',
     'fur coat',
     'garbage truck',
     'gasmask',
     'gas pump',
     'goblet',
     'go-kart',
     'golf ball',
     'golfcart',
     'gondola',
     'gong',
     'gown',
     'grand piano',
     'greenhouse',
     'grille',
     'grocery store',
     'guillotine',
     'hair slide',
     'hair spray',
     'half track',
     'hammer',
     'hamper',
     'hand blower',
     'hand-held computer',
     'handkerchief',
     'hard disc',
     'harmonica',
     'harp',
     'harvester',
     'hatchet',
     'holster',
     'home theater',
     'honeycomb',
     'hook',
     'hoopskirt',
     'horizontal bar',
     'horse cart',
     'hourglass',
     'iPod',
     'iron',
     "jack-o'-lantern",
     'jean',
     'jeep',
     'jersey',
     'jigsaw puzzle',
     'jinrikisha',
     'joystick',
     'kimono',
     'knee pad',
     'knot',
     'lab coat',
     'ladle',
     'lampshade',
     'laptop',
     'lawn mower',
     'lens cap',
     'letter opener',
     'library',
     'lifeboat',
     'lighter',
     'limousine',
     'liner',
     'lipstick',
     'Loafer',
     'lotion',
     'loudspeaker',
     'loupe',
     'lumbermill',
     'magnetic compass',
     'mailbag',
     'mailbox',
     'maillot',
     'maillot tank suit',
     'manhole cover',
     'maraca',
     'marimba',
     'mask',
     'matchstick',
     'maypole',
     'maze',
     'measuring cup',
     'medicine chest',
     'megalith',
     'microphone',
     'microwave',
     'military uniform',
     'milk can',
     'minibus',
     'miniskirt',
     'minivan',
     'missile',
     'mitten',
     'mixing bowl',
     'mobile home',
     'Model T',
     'modem',
     'monastery',
     'monitor',
     'moped',
     'mortar',
     'mortarboard',
     'mosque',
     'mosquito net',
     'motor scooter',
     'mountain bike',
     'mountain tent',
     'mouse',
     'mousetrap',
     'moving van',
     'muzzle',
     'nail',
     'neck brace',
     'necklace',
     'nipple',
     'notebook',
     'obelisk',
     'oboe',
     'ocarina',
     'odometer',
     'oil filter',
     'organ',
     'oscilloscope',
     'overskirt',
     'oxcart',
     'oxygen mask',
     'packet',
     'paddle',
     'paddlewheel',
     'padlock',
     'paintbrush',
     'pajama',
     'palace',
     'panpipe',
     'paper towel',
     'parachute',
     'parallel bars',
     'park bench',
     'parking meter',
     'passenger car',
     'patio',
     'pay-phone',
     'pedestal',
     'pencil box',
     'pencil sharpener',
     'perfume',
     'Petri dish',
     'photocopier',
     'pick',
     'pickelhaube',
     'picket fence',
     'pickup',
     'pier',
     'piggy bank',
     'pill bottle',
     'pillow',
     'ping-pong ball',
     'pinwheel',
     'pirate',
     'pitcher',
     'plane',
     'planetarium',
     'plastic bag',
     'plate rack',
     'plow',
     'plunger',
     'Polaroid camera',
     'pole',
     'police van',
     'poncho',
     'pool table',
     'pop bottle',
     'pot',
     "potter's wheel",
     'power drill',
     'prayer rug',
     'printer',
     'prison',
     'projectile',
     'projector',
     'puck',
     'punching bag',
     'purse',
     'quill',
     'quilt',
     'racer',
     'racket',
     'radiator',
     'radio',
     'radio telescope',
     'rain barrel',
     'recreational vehicle',
     'reel',
     'reflex camera',
     'refrigerator',
     'remote control',
     'restaurant',
     'revolver',
     'rifle',
     'rocking chair',
     'rotisserie',
     'rubber eraser',
     'rugby ball',
     'rule',
     'running shoe',
     'safe',
     'safety pin',
     'saltshaker',
     'sandal',
     'sarong',
     'sax',
     'scabbard',
     'scale',
     'school bus',
     'schooner',
     'scoreboard',
     'screen',
     'screw',
     'screwdriver',
     'seat belt',
     'sewing machine',
     'shield',
     'shoe shop',
     'shoji',
     'shopping basket',
     'shopping cart',
     'shovel',
     'shower cap',
     'shower curtain',
     'ski',
     'ski mask',
     'sleeping bag',
     'slide rule',
     'sliding door',
     'slot',
     'snorkel',
     'snowmobile',
     'snowplow',
     'soap dispenser',
     'soccer ball',
     'sock',
     'solar dish',
     'sombrero',
     'soup bowl',
     'space bar',
     'space heater',
     'space shuttle',
     'spatula',
     'speedboat',
     'spider web',
     'spindle',
     'sports car',
     'spotlight',
     'stage',
     'steam locomotive',
     'steel arch bridge',
     'steel drum',
     'stethoscope',
     'stole',
     'stone wall',
     'stopwatch',
     'stove',
     'strainer',
     'streetcar',
     'stretcher',
     'studio couch',
     'stupa',
     'submarine',
     'suit',
     'sundial',
     'sunglass',
     'sunglasses',
     'sunscreen',
     'suspension bridge',
     'swab',
     'sweatshirt',
     'swimming trunks',
     'swing',
     'switch',
     'syringe',
     'table lamp',
     'tank',
     'tape player',
     'teapot',
     'teddy',
     'television',
     'tennis ball',
     'thatch',
     'theater curtain',
     'thimble',
     'thresher',
     'throne',
     'tile roof',
     'toaster',
     'tobacco shop',
     'toilet seat',
     'torch',
     'totem pole',
     'tow truck',
     'toyshop',
     'tractor',
     'trailer truck',
     'tray',
     'trench coat',
     'tricycle',
     'trimaran',
     'tripod',
     'triumphal arch',
     'trolleybus',
     'trombone',
     'tub',
     'turnstile',
     'typewriter keyboard',
     'umbrella',
     'unicycle',
     'upright',
     'vacuum',
     'vase',
     'vault',
     'velvet',
     'vending machine',
     'vestment',
     'viaduct',
     'violin',
     'volleyball',
     'waffle iron',
     'wall clock',
     'wallet',
     'wardrobe',
     'warplane',
     'washbasin',
     'washer',
     'water bottle',
     'water jug',
     'water tower',
     'whiskey jug',
     'whistle',
     'wig',
     'window screen',
     'window shade',
     'Windsor tie',
     'wine bottle',
     'wing',
     'wok',
     'wooden spoon',
     'wool',
     'worm fence',
     'wreck',
     'yawl',
     'yurt',
     'web site',
     'comic book',
     'crossword puzzle',
     'street sign',
     'traffic light',
     'book jacket',
     'menu',
     'plate',
     'guacamole',
     'consomme',
     'hot pot',
     'trifle',
     'ice cream',
     'ice lolly',
     'French loaf',
     'bagel',
     'pretzel',
     'cheeseburger',
     'hotdog',
     'mashed potato',
     'head cabbage',
     'broccoli',
     'cauliflower',
     'zucchini',
     'spaghetti squash',
     'acorn squash',
     'butternut squash',
     'cucumber',
     'artichoke',
     'bell pepper',
     'cardoon',
     'mushroom',
     'Granny Smith',
     'strawberry',
     'orange',
     'lemon',
     'fig',
     'pineapple',
     'banana',
     'jackfruit',
     'custard apple',
     'pomegranate',
     'hay',
     'carbonara',
     'chocolate sauce',
     'dough',
     'meat loaf',
     'pizza',
     'potpie',
     'burrito',
     'red wine',
     'espresso',
     'cup',
     'eggnog',
     'alp',
     'bubble',
     'cliff',
     'coral reef',
     'geyser',
     'lakeside',
     'promontory',
     'sandbar',
     'seashore',
     'valley',
     'volcano',
     'ballplayer',
     'groom',
     'scuba diver',
     'rapeseed',
     'daisy',
     "yellow lady's slipper",
     'corn',
     'acorn',
     'hip',
     'buckeye',
     'coral fungus',
     'agaric',
     'gyromitra',
     'stinkhorn',
     'earthstar',
     'hen-of-the-woods',
     'bolete',
     'ear',
     'toilet tissue']


    category number =  1000



```python
category_name = weights.meta["categories"][class_id]
category_name
```




    'beagle'



## 최종 레이어 함수 교체하기 (전이 학습)



```python
# 모델 개요 표시 1
print(net)
```

    GoogLeNet(
      (conv1): BasicConv2d(
        (conv): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool1): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (conv2): BasicConv2d(
        (conv): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (conv3): BasicConv2d(
        (conv): Conv2d(64, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool2): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception3a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(192, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(192, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception3b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 96, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool3): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception4a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(480, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 208, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(208, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 48, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(480, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(112, 224, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(224, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4c): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4d): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 144, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(144, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(144, 288, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(288, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4e): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(528, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(528, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception5a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception5b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 384, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 48, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(48, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (aux1): None
      (aux2): None
      (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
      (dropout): Dropout(p=0.2, inplace=False)
      (fc): Linear(in_features=1024, out_features=1000, bias=True)
    )



```python
# 모델 개요 표시 
summary(net,(100, 3, 112, 112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    GoogLeNet                                [100, 1000]               --
    ├─BasicConv2d: 1-1                       [100, 64, 56, 56]         --
    │    └─Conv2d: 2-1                       [100, 64, 56, 56]         9,408
    │    └─BatchNorm2d: 2-2                  [100, 64, 56, 56]         128
    ├─MaxPool2d: 1-2                         [100, 64, 28, 28]         --
    ├─BasicConv2d: 1-3                       [100, 64, 28, 28]         --
    │    └─Conv2d: 2-3                       [100, 64, 28, 28]         4,096
    │    └─BatchNorm2d: 2-4                  [100, 64, 28, 28]         128
    ├─BasicConv2d: 1-4                       [100, 192, 28, 28]        --
    │    └─Conv2d: 2-5                       [100, 192, 28, 28]        110,592
    │    └─BatchNorm2d: 2-6                  [100, 192, 28, 28]        384
    ├─MaxPool2d: 1-5                         [100, 192, 14, 14]        --
    ├─Inception: 1-6                         [100, 256, 14, 14]        --
    │    └─BasicConv2d: 2-7                  [100, 64, 14, 14]         --
    │    │    └─Conv2d: 3-1                  [100, 64, 14, 14]         12,288
    │    │    └─BatchNorm2d: 3-2             [100, 64, 14, 14]         128
    │    └─Sequential: 2-8                   [100, 128, 14, 14]        --
    │    │    └─BasicConv2d: 3-3             [100, 96, 14, 14]         18,624
    │    │    └─BasicConv2d: 3-4             [100, 128, 14, 14]        110,848
    │    └─Sequential: 2-9                   [100, 32, 14, 14]         --
    │    │    └─BasicConv2d: 3-5             [100, 16, 14, 14]         3,104
    │    │    └─BasicConv2d: 3-6             [100, 32, 14, 14]         4,672
    │    └─Sequential: 2-10                  [100, 32, 14, 14]         --
    │    │    └─MaxPool2d: 3-7               [100, 192, 14, 14]        --
    │    │    └─BasicConv2d: 3-8             [100, 32, 14, 14]         6,208
    ├─Inception: 1-7                         [100, 480, 14, 14]        --
    │    └─BasicConv2d: 2-11                 [100, 128, 14, 14]        --
    │    │    └─Conv2d: 3-9                  [100, 128, 14, 14]        32,768
    │    │    └─BatchNorm2d: 3-10            [100, 128, 14, 14]        256
    │    └─Sequential: 2-12                  [100, 192, 14, 14]        --
    │    │    └─BasicConv2d: 3-11            [100, 128, 14, 14]        33,024
    │    │    └─BasicConv2d: 3-12            [100, 192, 14, 14]        221,568
    │    └─Sequential: 2-13                  [100, 96, 14, 14]         --
    │    │    └─BasicConv2d: 3-13            [100, 32, 14, 14]         8,256
    │    │    └─BasicConv2d: 3-14            [100, 96, 14, 14]         27,840
    │    └─Sequential: 2-14                  [100, 64, 14, 14]         --
    │    │    └─MaxPool2d: 3-15              [100, 256, 14, 14]        --
    │    │    └─BasicConv2d: 3-16            [100, 64, 14, 14]         16,512
    ├─MaxPool2d: 1-8                         [100, 480, 7, 7]          --
    ├─Inception: 1-9                         [100, 512, 7, 7]          --
    │    └─BasicConv2d: 2-15                 [100, 192, 7, 7]          --
    │    │    └─Conv2d: 3-17                 [100, 192, 7, 7]          92,160
    │    │    └─BatchNorm2d: 3-18            [100, 192, 7, 7]          384
    │    └─Sequential: 2-16                  [100, 208, 7, 7]          --
    │    │    └─BasicConv2d: 3-19            [100, 96, 7, 7]           46,272
    │    │    └─BasicConv2d: 3-20            [100, 208, 7, 7]          180,128
    │    └─Sequential: 2-17                  [100, 48, 7, 7]           --
    │    │    └─BasicConv2d: 3-21            [100, 16, 7, 7]           7,712
    │    │    └─BasicConv2d: 3-22            [100, 48, 7, 7]           7,008
    │    └─Sequential: 2-18                  [100, 64, 7, 7]           --
    │    │    └─MaxPool2d: 3-23              [100, 480, 7, 7]          --
    │    │    └─BasicConv2d: 3-24            [100, 64, 7, 7]           30,848
    ├─Inception: 1-10                        [100, 512, 7, 7]          --
    │    └─BasicConv2d: 2-19                 [100, 160, 7, 7]          --
    │    │    └─Conv2d: 3-25                 [100, 160, 7, 7]          81,920
    │    │    └─BatchNorm2d: 3-26            [100, 160, 7, 7]          320
    │    └─Sequential: 2-20                  [100, 224, 7, 7]          --
    │    │    └─BasicConv2d: 3-27            [100, 112, 7, 7]          57,568
    │    │    └─BasicConv2d: 3-28            [100, 224, 7, 7]          226,240
    │    └─Sequential: 2-21                  [100, 64, 7, 7]           --
    │    │    └─BasicConv2d: 3-29            [100, 24, 7, 7]           12,336
    │    │    └─BasicConv2d: 3-30            [100, 64, 7, 7]           13,952
    │    └─Sequential: 2-22                  [100, 64, 7, 7]           --
    │    │    └─MaxPool2d: 3-31              [100, 512, 7, 7]          --
    │    │    └─BasicConv2d: 3-32            [100, 64, 7, 7]           32,896
    ├─Inception: 1-11                        [100, 512, 7, 7]          --
    │    └─BasicConv2d: 2-23                 [100, 128, 7, 7]          --
    │    │    └─Conv2d: 3-33                 [100, 128, 7, 7]          65,536
    │    │    └─BatchNorm2d: 3-34            [100, 128, 7, 7]          256
    │    └─Sequential: 2-24                  [100, 256, 7, 7]          --
    │    │    └─BasicConv2d: 3-35            [100, 128, 7, 7]          65,792
    │    │    └─BasicConv2d: 3-36            [100, 256, 7, 7]          295,424
    │    └─Sequential: 2-25                  [100, 64, 7, 7]           --
    │    │    └─BasicConv2d: 3-37            [100, 24, 7, 7]           12,336
    │    │    └─BasicConv2d: 3-38            [100, 64, 7, 7]           13,952
    │    └─Sequential: 2-26                  [100, 64, 7, 7]           --
    │    │    └─MaxPool2d: 3-39              [100, 512, 7, 7]          --
    │    │    └─BasicConv2d: 3-40            [100, 64, 7, 7]           32,896
    ├─Inception: 1-12                        [100, 528, 7, 7]          --
    │    └─BasicConv2d: 2-27                 [100, 112, 7, 7]          --
    │    │    └─Conv2d: 3-41                 [100, 112, 7, 7]          57,344
    │    │    └─BatchNorm2d: 3-42            [100, 112, 7, 7]          224
    │    └─Sequential: 2-28                  [100, 288, 7, 7]          --
    │    │    └─BasicConv2d: 3-43            [100, 144, 7, 7]          74,016
    │    │    └─BasicConv2d: 3-44            [100, 288, 7, 7]          373,824
    │    └─Sequential: 2-29                  [100, 64, 7, 7]           --
    │    │    └─BasicConv2d: 3-45            [100, 32, 7, 7]           16,448
    │    │    └─BasicConv2d: 3-46            [100, 64, 7, 7]           18,560
    │    └─Sequential: 2-30                  [100, 64, 7, 7]           --
    │    │    └─MaxPool2d: 3-47              [100, 512, 7, 7]          --
    │    │    └─BasicConv2d: 3-48            [100, 64, 7, 7]           32,896
    ├─Inception: 1-13                        [100, 832, 7, 7]          --
    │    └─BasicConv2d: 2-31                 [100, 256, 7, 7]          --
    │    │    └─Conv2d: 3-49                 [100, 256, 7, 7]          135,168
    │    │    └─BatchNorm2d: 3-50            [100, 256, 7, 7]          512
    │    └─Sequential: 2-32                  [100, 320, 7, 7]          --
    │    │    └─BasicConv2d: 3-51            [100, 160, 7, 7]          84,800
    │    │    └─BasicConv2d: 3-52            [100, 320, 7, 7]          461,440
    │    └─Sequential: 2-33                  [100, 128, 7, 7]          --
    │    │    └─BasicConv2d: 3-53            [100, 32, 7, 7]           16,960
    │    │    └─BasicConv2d: 3-54            [100, 128, 7, 7]          37,120
    │    └─Sequential: 2-34                  [100, 128, 7, 7]          --
    │    │    └─MaxPool2d: 3-55              [100, 528, 7, 7]          --
    │    │    └─BasicConv2d: 3-56            [100, 128, 7, 7]          67,840
    ├─MaxPool2d: 1-14                        [100, 832, 4, 4]          --
    ├─Inception: 1-15                        [100, 832, 4, 4]          --
    │    └─BasicConv2d: 2-35                 [100, 256, 4, 4]          --
    │    │    └─Conv2d: 3-57                 [100, 256, 4, 4]          212,992
    │    │    └─BatchNorm2d: 3-58            [100, 256, 4, 4]          512
    │    └─Sequential: 2-36                  [100, 320, 4, 4]          --
    │    │    └─BasicConv2d: 3-59            [100, 160, 4, 4]          133,440
    │    │    └─BasicConv2d: 3-60            [100, 320, 4, 4]          461,440
    │    └─Sequential: 2-37                  [100, 128, 4, 4]          --
    │    │    └─BasicConv2d: 3-61            [100, 32, 4, 4]           26,688
    │    │    └─BasicConv2d: 3-62            [100, 128, 4, 4]          37,120
    │    └─Sequential: 2-38                  [100, 128, 4, 4]          --
    │    │    └─MaxPool2d: 3-63              [100, 832, 4, 4]          --
    │    │    └─BasicConv2d: 3-64            [100, 128, 4, 4]          106,752
    ├─Inception: 1-16                        [100, 1024, 4, 4]         --
    │    └─BasicConv2d: 2-39                 [100, 384, 4, 4]          --
    │    │    └─Conv2d: 3-65                 [100, 384, 4, 4]          319,488
    │    │    └─BatchNorm2d: 3-66            [100, 384, 4, 4]          768
    │    └─Sequential: 2-40                  [100, 384, 4, 4]          --
    │    │    └─BasicConv2d: 3-67            [100, 192, 4, 4]          160,128
    │    │    └─BasicConv2d: 3-68            [100, 384, 4, 4]          664,320
    │    └─Sequential: 2-41                  [100, 128, 4, 4]          --
    │    │    └─BasicConv2d: 3-69            [100, 48, 4, 4]           40,032
    │    │    └─BasicConv2d: 3-70            [100, 128, 4, 4]          55,552
    │    └─Sequential: 2-42                  [100, 128, 4, 4]          --
    │    │    └─MaxPool2d: 3-71              [100, 832, 4, 4]          --
    │    │    └─BasicConv2d: 3-72            [100, 128, 4, 4]          106,752
    ├─AdaptiveAvgPool2d: 1-17                [100, 1024, 1, 1]         --
    ├─Dropout: 1-18                          [100, 1024]               --
    ├─Linear: 1-19                           [100, 1000]               1,025,000
    ==========================================================================================
    Total params: 6,624,904
    Trainable params: 6,624,904
    Non-trainable params: 0
    Total mult-adds (G): 38.41
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 1304.99
    Params size (MB): 26.50
    Estimated Total Size (MB): 1346.54
    ==========================================================================================




```python
print(net.fc)
print(net.fc.in_features)
print(net.fc.out_features)
```

    Linear(in_features=1024, out_features=1000, bias=True)
    1024
    1000



```python
torch_seed()
in_features = net.fc.in_features
net.fc = nn.Linear(in_features, n_output)
```


```python
# 모델 개요 표시 1
print(net)
```

    GoogLeNet(
      (conv1): BasicConv2d(
        (conv): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool1): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (conv2): BasicConv2d(
        (conv): Conv2d(64, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
        (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (conv3): BasicConv2d(
        (conv): Conv2d(64, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
      )
      (maxpool2): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception3a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(192, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(192, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(192, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception3b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 192, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 96, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(256, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool3): MaxPool2d(kernel_size=3, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception4a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(480, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 96, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(96, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(96, 208, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(208, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(480, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(16, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(16, 48, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(480, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(112, 224, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(224, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4c): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 24, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(24, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(24, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4d): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(512, 112, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(112, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 144, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(144, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(144, 288, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(288, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(512, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(512, 64, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(64, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception4e): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(528, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(528, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(528, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (maxpool4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=True)
      (inception5a): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 256, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(256, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 160, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(160, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(160, 320, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(320, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 32, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(32, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(32, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (inception5b): Inception(
        (branch1): BasicConv2d(
          (conv): Conv2d(832, 384, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
        )
        (branch2): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 192, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(192, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(192, 384, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(384, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch3): Sequential(
          (0): BasicConv2d(
            (conv): Conv2d(832, 48, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(48, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): BasicConv2d(
            (conv): Conv2d(48, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
        (branch4): Sequential(
          (0): MaxPool2d(kernel_size=3, stride=1, padding=1, dilation=1, ceil_mode=True)
          (1): BasicConv2d(
            (conv): Conv2d(832, 128, kernel_size=(1, 1), stride=(1, 1), bias=False)
            (bn): BatchNorm2d(128, eps=0.001, momentum=0.1, affine=True, track_running_stats=True)
          )
        )
      )
      (aux1): None
      (aux2): None
      (avgpool): AdaptiveAvgPool2d(output_size=(1, 1))
      (dropout): Dropout(p=0.2, inplace=False)
      (fc): Linear(in_features=1024, out_features=10, bias=True)
    )



```python
# 손실 계산 그래프 시각화
net = net.to(device)
criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__60_0.svg)
    


## 학습과 결과 평가

### 초기 설정


```python
# 난수 고정
torch_seed()

# 사전 학습 모델 불러오기
# pretraind = True로 학습을 마친 파라미터도 함께 불러오기
weights = models.GoogLeNet_Weights.IMAGENET1K_V1
net = models.googlenet(weights=weights)

# 최종 레이어 함수 입력 차원수 확인
in_features = net.fc.in_features
net.fc = nn.Linear(in_features, n_output)

# 최종 레이어 함수 교체
net.fc = nn.Linear(in_features, n_output)

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)

# history 파일 초기화
history = np.zeros((0, 5))
```

### 학습


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
        train_loader, test_loader, device, history)
```


      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.82228 acc: 0.72988 val_loss: 0.31814, val_acc: 0.89200



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.41222 acc: 0.86000 val_loss: 0.23791, val_acc: 0.91640



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.33283 acc: 0.88782 val_loss: 0.20396, val_acc: 0.92910



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.28708 acc: 0.90082 val_loss: 0.19425, val_acc: 0.93320



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.24786 acc: 0.91622 val_loss: 0.17743, val_acc: 0.94010


### 학습 결과 평가


```python
# 결과 요약
evaluate_history(history)
```

    초기상태 : 손실 : 0.31814  정확도 : 0.89200
    최종상태 : 손실 : 0.17743 정확도 : 0.94010



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__67_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__67_2.webp)
    



```python
# 이미지와 정답, 예측 결과를 함께 표시
show_images_labels(test_loader, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_13%EC%B0%A8%EC%8B%9C__AlexNet_GoogleNet__68_1.webp)
    



## 강의_3기_AI개론_14차시__VGG_ResNet_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/basic/강의_3기_AI개론_14차시__VGG_ResNet_.ipynb)

# 14장 영상 분류 사전 학습 모델 활용하기 2 (ResNet, VGG-19)

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
```

    Successfully installed torchviz-0.0.2
    Successfully installed torchinfo-1.6.5


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


### 공통 함수 불러오기


```python
# 공통 함수 다운로드
!git clone https://github.com/wikibook/pythonlibs.git

# 공통 함수 불러오기
from pythonlibs.torch_lib1 import *


# 공통 함수 확인
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
  transforms.ToTensor(),
  transforms.Normalize(0.5, 0.5), 
  transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False)
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

## ResNet18 불러오기

### 모델 불러오기


```python
#  라이브러리 임포트
from torchvision import models


# 사전 학습 모델 불러오기
weights = models.ResNet18_Weights.IMAGENET1K_V1
net = models.resnet18(weights = weights)
# pretraind = True로 학습을 마친 파라미터를 동시에 불러오기
# net = models.resnet18(pretrained = True)
```

### 모델 구조 확인


```python
# 모델 개요 표시 1

print(net)
# net.layer1[0].bn1
```

    ResNet(
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
      (fc): Linear(in_features=512, out_features=1000, bias=True)
    )



```python
# 모델 개요 표시 2
net = net.to(device)
summary(net,(100,3,112,112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    ResNet                                   [100, 1000]               --
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
    ├─Linear: 1-10                           [100, 1000]               513,000
    ==========================================================================================
    Total params: 11,689,512
    Trainable params: 11,689,512
    Non-trainable params: 0
    Total mult-adds (G): 48.54
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 1009.64
    Params size (MB): 46.76
    Estimated Total Size (MB): 1071.46
    ==========================================================================================




```python
print(net.fc)
print(net.fc.in_features)
print(net.fc.out_features)
```

    Linear(in_features=512, out_features=1000, bias=True)
    512
    1000


## 최종 레이어 함수 교체하기


```python
# 난수 고정
torch_seed()

# 최종 레이어 함수의 입력 차원수 확인
fc_in_features = net.fc.in_features

# 최종 레이어 함수 교체
net.fc = nn.Linear(fc_in_features, n_output)
```


```python
# 모델 개요 표시 1
print(net)
```

    ResNet(
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
# 모델 개요 표시 2

net = net.to(device)
summary(net,(100, 3, 224, 224))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    ResNet                                   [100, 10]                 --
    ├─Conv2d: 1-1                            [100, 64, 112, 112]       9,408
    ├─BatchNorm2d: 1-2                       [100, 64, 112, 112]       128
    ├─ReLU: 1-3                              [100, 64, 112, 112]       --
    ├─MaxPool2d: 1-4                         [100, 64, 56, 56]         --
    ├─Sequential: 1-5                        [100, 64, 56, 56]         --
    │    └─BasicBlock: 2-1                   [100, 64, 56, 56]         --
    │    │    └─Conv2d: 3-1                  [100, 64, 56, 56]         36,864
    │    │    └─BatchNorm2d: 3-2             [100, 64, 56, 56]         128
    │    │    └─ReLU: 3-3                    [100, 64, 56, 56]         --
    │    │    └─Conv2d: 3-4                  [100, 64, 56, 56]         36,864
    │    │    └─BatchNorm2d: 3-5             [100, 64, 56, 56]         128
    │    │    └─ReLU: 3-6                    [100, 64, 56, 56]         --
    │    └─BasicBlock: 2-2                   [100, 64, 56, 56]         --
    │    │    └─Conv2d: 3-7                  [100, 64, 56, 56]         36,864
    │    │    └─BatchNorm2d: 3-8             [100, 64, 56, 56]         128
    │    │    └─ReLU: 3-9                    [100, 64, 56, 56]         --
    │    │    └─Conv2d: 3-10                 [100, 64, 56, 56]         36,864
    │    │    └─BatchNorm2d: 3-11            [100, 64, 56, 56]         128
    │    │    └─ReLU: 3-12                   [100, 64, 56, 56]         --
    ├─Sequential: 1-6                        [100, 128, 28, 28]        --
    │    └─BasicBlock: 2-3                   [100, 128, 28, 28]        --
    │    │    └─Conv2d: 3-13                 [100, 128, 28, 28]        73,728
    │    │    └─BatchNorm2d: 3-14            [100, 128, 28, 28]        256
    │    │    └─ReLU: 3-15                   [100, 128, 28, 28]        --
    │    │    └─Conv2d: 3-16                 [100, 128, 28, 28]        147,456
    │    │    └─BatchNorm2d: 3-17            [100, 128, 28, 28]        256
    │    │    └─Sequential: 3-18             [100, 128, 28, 28]        8,448
    │    │    └─ReLU: 3-19                   [100, 128, 28, 28]        --
    │    └─BasicBlock: 2-4                   [100, 128, 28, 28]        --
    │    │    └─Conv2d: 3-20                 [100, 128, 28, 28]        147,456
    │    │    └─BatchNorm2d: 3-21            [100, 128, 28, 28]        256
    │    │    └─ReLU: 3-22                   [100, 128, 28, 28]        --
    │    │    └─Conv2d: 3-23                 [100, 128, 28, 28]        147,456
    │    │    └─BatchNorm2d: 3-24            [100, 128, 28, 28]        256
    │    │    └─ReLU: 3-25                   [100, 128, 28, 28]        --
    ├─Sequential: 1-7                        [100, 256, 14, 14]        --
    │    └─BasicBlock: 2-5                   [100, 256, 14, 14]        --
    │    │    └─Conv2d: 3-26                 [100, 256, 14, 14]        294,912
    │    │    └─BatchNorm2d: 3-27            [100, 256, 14, 14]        512
    │    │    └─ReLU: 3-28                   [100, 256, 14, 14]        --
    │    │    └─Conv2d: 3-29                 [100, 256, 14, 14]        589,824
    │    │    └─BatchNorm2d: 3-30            [100, 256, 14, 14]        512
    │    │    └─Sequential: 3-31             [100, 256, 14, 14]        33,280
    │    │    └─ReLU: 3-32                   [100, 256, 14, 14]        --
    │    └─BasicBlock: 2-6                   [100, 256, 14, 14]        --
    │    │    └─Conv2d: 3-33                 [100, 256, 14, 14]        589,824
    │    │    └─BatchNorm2d: 3-34            [100, 256, 14, 14]        512
    │    │    └─ReLU: 3-35                   [100, 256, 14, 14]        --
    │    │    └─Conv2d: 3-36                 [100, 256, 14, 14]        589,824
    │    │    └─BatchNorm2d: 3-37            [100, 256, 14, 14]        512
    │    │    └─ReLU: 3-38                   [100, 256, 14, 14]        --
    ├─Sequential: 1-8                        [100, 512, 7, 7]          --
    │    └─BasicBlock: 2-7                   [100, 512, 7, 7]          --
    │    │    └─Conv2d: 3-39                 [100, 512, 7, 7]          1,179,648
    │    │    └─BatchNorm2d: 3-40            [100, 512, 7, 7]          1,024
    │    │    └─ReLU: 3-41                   [100, 512, 7, 7]          --
    │    │    └─Conv2d: 3-42                 [100, 512, 7, 7]          2,359,296
    │    │    └─BatchNorm2d: 3-43            [100, 512, 7, 7]          1,024
    │    │    └─Sequential: 3-44             [100, 512, 7, 7]          132,096
    │    │    └─ReLU: 3-45                   [100, 512, 7, 7]          --
    │    └─BasicBlock: 2-8                   [100, 512, 7, 7]          --
    │    │    └─Conv2d: 3-46                 [100, 512, 7, 7]          2,359,296
    │    │    └─BatchNorm2d: 3-47            [100, 512, 7, 7]          1,024
    │    │    └─ReLU: 3-48                   [100, 512, 7, 7]          --
    │    │    └─Conv2d: 3-49                 [100, 512, 7, 7]          2,359,296
    │    │    └─BatchNorm2d: 3-50            [100, 512, 7, 7]          1,024
    │    │    └─ReLU: 3-51                   [100, 512, 7, 7]          --
    ├─AdaptiveAvgPool2d: 1-9                 [100, 512, 1, 1]          --
    ├─Linear: 1-10                           [100, 10]                 5,130
    ==========================================================================================
    Total params: 11,181,642
    Trainable params: 11,181,642
    Non-trainable params: 0
    Total mult-adds (G): 181.36
    ==========================================================================================
    Input size (MB): 60.21
    Forward/backward pass size (MB): 3973.95
    Params size (MB): 44.73
    Estimated Total Size (MB): 4078.89
    ==========================================================================================




```python
# 손실 계산 그래프 시각화

criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__27_0.svg)
    



```python
# 모델 개요 표시 1
print(net)
```

    ResNet(
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
# 모델 개요 표시 2
net = net.to(device)
summary(net,(100,3,112,112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    ResNet                                   [100, 10]                 --
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



## 학습과 결과 평가

### 초기 설정


```python
# 난수 고정
torch_seed()

# 사전 학습 모델 불러오기
weights = models.ResNet18_Weights.IMAGENET1K_V1
net = models.resnet18(weights = weights)

# 최종 레이어 함수 입력 차원수 확인
fc_in_features = net.fc.in_features

# 최종 레이어 함수 교체
net.fc = nn.Linear(fc_in_features, n_output)

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)

# history 파일 초기화
history = np.zeros((0, 5))
```

### 학습


```python
# 학습
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
        train_loader, test_loader, device, history)
```


      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.60050 acc: 0.79544 val_loss: 0.30019, val_acc: 0.89720



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.32100 acc: 0.88816 val_loss: 0.23029, val_acc: 0.92010



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.25802 acc: 0.91102 val_loss: 0.19530, val_acc: 0.93400



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.21796 acc: 0.92298 val_loss: 0.17268, val_acc: 0.94230



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.19113 acc: 0.93398 val_loss: 0.17815, val_acc: 0.94070


### 학습 결과 평가


```python
# 결과 요약
evaluate_history(history)
```

    초기상태 : 손실 : 0.30019  정확도 : 0.89720
    최종상태 : 손실 : 0.17815 정확도 : 0.94070



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__36_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__36_2.webp)
    



```python
# 이미지와 정답, 예측 결과를 함께 표시
show_images_labels(test_loader, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__37_1.webp)
    


## VGG-19-BN 활용하기

### 모델 불러오기


```python
# 사전 학습 모델 불러오기
from torchvision import models

weights = models.VGG19_BN_Weights.DEFAULT
net = models.vgg19_bn(weights = weights)
```

### 모델 구조 확인


```python
# 모델 개요 표시 1
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


최종 레이어 함수는``classifier[6]``임을 알 수 있다.


```python
# 최종 레이어 함수 확인
print(net.classifier[6])

```

    Linear(in_features=4096, out_features=1000, bias=True)


### 최종 레이어 함수 교체


```python
# 난수 고정
torch_seed()

# 최종 레이어 함수 교체
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, n_output)

# features 마지막의 MaxPool2d 제거
net.features = net.features[:-1]

# AdaptiveAvgPool2d 제거
net.avgpool = nn.Identity()
```


```python
# 모델 개요 표시 2
net = net.to(device)
summary(net,(100,3,112,112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    VGG                                      [100, 10]                 --
    ├─Sequential: 1-1                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-1                       [100, 64, 112, 112]       1,792
    │    └─BatchNorm2d: 2-2                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-3                         [100, 64, 112, 112]       --
    │    └─Conv2d: 2-4                       [100, 64, 112, 112]       36,928
    │    └─BatchNorm2d: 2-5                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-6                         [100, 64, 112, 112]       --
    │    └─MaxPool2d: 2-7                    [100, 64, 56, 56]         --
    │    └─Conv2d: 2-8                       [100, 128, 56, 56]        73,856
    │    └─BatchNorm2d: 2-9                  [100, 128, 56, 56]        256
    │    └─ReLU: 2-10                        [100, 128, 56, 56]        --
    │    └─Conv2d: 2-11                      [100, 128, 56, 56]        147,584
    │    └─BatchNorm2d: 2-12                 [100, 128, 56, 56]        256
    │    └─ReLU: 2-13                        [100, 128, 56, 56]        --
    │    └─MaxPool2d: 2-14                   [100, 128, 28, 28]        --
    │    └─Conv2d: 2-15                      [100, 256, 28, 28]        295,168
    │    └─BatchNorm2d: 2-16                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-17                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-18                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-19                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-20                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-21                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-22                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-23                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-24                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-25                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-26                        [100, 256, 28, 28]        --
    │    └─MaxPool2d: 2-27                   [100, 256, 14, 14]        --
    │    └─Conv2d: 2-28                      [100, 512, 14, 14]        1,180,160
    │    └─BatchNorm2d: 2-29                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-30                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-31                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-32                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-33                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-34                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-35                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-36                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-37                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-38                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-39                        [100, 512, 14, 14]        --
    │    └─MaxPool2d: 2-40                   [100, 512, 7, 7]          --
    │    └─Conv2d: 2-41                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-42                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-43                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-44                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-45                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-46                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-47                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-48                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-49                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-50                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-51                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-52                        [100, 512, 7, 7]          --
    ├─Identity: 1-2                          [100, 512, 7, 7]          --
    ├─Sequential: 1-3                        [100, 10]                 --
    │    └─Linear: 2-53                      [100, 4096]               102,764,544
    │    └─ReLU: 2-54                        [100, 4096]               --
    │    └─Dropout: 2-55                     [100, 4096]               --
    │    └─Linear: 2-56                      [100, 4096]               16,781,312
    │    └─ReLU: 2-57                        [100, 4096]               --
    │    └─Dropout: 2-58                     [100, 4096]               --
    │    └─Linear: 2-59                      [100, 10]                 40,970
    ==========================================================================================
    Total params: 139,622,218
    Trainable params: 139,622,218
    Non-trainable params: 0
    Total mult-adds (G): 500.04
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 5947.40
    Params size (MB): 558.49
    Estimated Total Size (MB): 6520.94
    ==========================================================================================




```python
# 손실 계산 그래프 시각화

criterion = nn.CrossEntropyLoss()
loss = eval_loss(test_loader, device, net, criterion)
g = make_dot(loss, params=dict(net.named_parameters()))
display(g)
```


    
![svg](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__48_0.svg)
    


### 초기 설정


```python
# 난수 고정
torch_seed()

# 사전 학습 모델 불러오기
net = models.vgg19_bn(pretrained = True)

# 최종 레이어 함수 교체
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, n_output)

# features 마지막의 MaxPool2d 제거
net.features = net.features[:-1]

# AdaptiveAvgPool2d 제거
net.avgpool = nn.Identity()

# 모델을 GPU로 전송
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)

# history 초기화
history = np.zeros((0, 5))

```

### 학습


```python
num_epochs = 5
history = fit(net, optimizer, criterion, num_epochs, 
          train_loader, test_loader, device, history)
```


      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [1/5], loss: 0.49669 acc: 0.83160 val_loss: 0.19144, val_acc: 0.93610



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [2/5], loss: 0.24048 acc: 0.91826 val_loss: 0.15483, val_acc: 0.94740



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [3/5], loss: 0.18289 acc: 0.93778 val_loss: 0.13438, val_acc: 0.95410



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [4/5], loss: 0.15228 acc: 0.94810 val_loss: 0.12692, val_acc: 0.95720



      0%|          | 0/1000 [00:00<?, ?it/s]


    Epoch [5/5], loss: 0.13073 acc: 0.95556 val_loss: 0.12888, val_acc: 0.95750


### 결과 확인


```python
# 결과 요약
evaluate_history(history)
```

    초기상태 : 손실 : 0.19144  정확도 : 0.93610
    최종상태 : 손실 : 0.12888 정확도 : 0.95750



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__54_1.webp)
    



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__54_2.webp)
    



```python
# 이미지와 정답, 예측 결과를 함께 표시
show_images_labels(test_loader, classes, net, device)
```

    len(images) =  50



    
![png](../assets/images/ai/cnn-architectures/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EA%B0%9C%EB%A1%A0_14%EC%B0%A8%EC%8B%9C__VGG_ResNet__55_1.webp)
    


## CIFAR-10에 전이 학습을 적용한 경우 (parameters freezing)


```python
# 사전 학습 모델 불러오기
weights = models.ResNet18_Weights.IMAGENET1K_V1
net = models.resnet18(weights = weights)
next(iter(net.parameters())).requires_grad
```




    True




```python
print(net)
```

    ResNet(
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
# 전이 학습

# 사전 학습 모델 불러오기
weights = models.ResNet18_Weights.IMAGENET1K_V1
net = models.resnet18(weights = weights)

# 모든 파라미터의 경사 계산을 OFF로 설정
for param in net.parameters():
    param.requires_grad = False

# 난수 고정
torch_seed()

# 최종 레이어 함수 교체
net.fc = nn.Linear(net.fc.in_features, n_output)

# GPU 사용
net = net.to(device)

# 학습률
lr = 0.001

# 손실 함수 정의
criterion = nn.CrossEntropyLoss()

# 최적화 함수 정의
# 파라미터 변경은 최종 레이어 함수로 한정
optimizer = optim.SGD(net.fc.parameters(), lr=lr, momentum=0.9)

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



```python
# 결과 요약
evaluate_history(history)
```

## 범용적인 사전 학습 모델을 작성하는 법

### 모델 불러오기


```python
# 사전 학습 모델 불러오기
from torchvision import models

weights = models.VGG19_BN_Weights.DEFAULT
net = models.vgg19_bn(weights = weights)
```

### 모델 개요 표시 1


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


### 중간 텐서 확인


```python
# 원본 데이터 사이즈의 경우(배치사이즈 100)
net = net.to(device)
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
# 실습용 데이터 사이즈의 경우(배치사이즈 100)
summary(net, (100, 3, 112, 112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    VGG                                      [100, 1000]               --
    ├─Sequential: 1-1                        [100, 512, 3, 3]          --
    │    └─Conv2d: 2-1                       [100, 64, 112, 112]       1,792
    │    └─BatchNorm2d: 2-2                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-3                         [100, 64, 112, 112]       --
    │    └─Conv2d: 2-4                       [100, 64, 112, 112]       36,928
    │    └─BatchNorm2d: 2-5                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-6                         [100, 64, 112, 112]       --
    │    └─MaxPool2d: 2-7                    [100, 64, 56, 56]         --
    │    └─Conv2d: 2-8                       [100, 128, 56, 56]        73,856
    │    └─BatchNorm2d: 2-9                  [100, 128, 56, 56]        256
    │    └─ReLU: 2-10                        [100, 128, 56, 56]        --
    │    └─Conv2d: 2-11                      [100, 128, 56, 56]        147,584
    │    └─BatchNorm2d: 2-12                 [100, 128, 56, 56]        256
    │    └─ReLU: 2-13                        [100, 128, 56, 56]        --
    │    └─MaxPool2d: 2-14                   [100, 128, 28, 28]        --
    │    └─Conv2d: 2-15                      [100, 256, 28, 28]        295,168
    │    └─BatchNorm2d: 2-16                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-17                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-18                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-19                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-20                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-21                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-22                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-23                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-24                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-25                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-26                        [100, 256, 28, 28]        --
    │    └─MaxPool2d: 2-27                   [100, 256, 14, 14]        --
    │    └─Conv2d: 2-28                      [100, 512, 14, 14]        1,180,160
    │    └─BatchNorm2d: 2-29                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-30                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-31                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-32                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-33                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-34                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-35                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-36                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-37                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-38                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-39                        [100, 512, 14, 14]        --
    │    └─MaxPool2d: 2-40                   [100, 512, 7, 7]          --
    │    └─Conv2d: 2-41                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-42                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-43                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-44                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-45                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-46                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-47                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-48                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-49                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-50                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-51                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-52                        [100, 512, 7, 7]          --
    │    └─MaxPool2d: 2-53                   [100, 512, 3, 3]          --
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
    Total mult-adds (G): 500.45
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 5948.19
    Params size (MB): 574.71
    Estimated Total Size (MB): 6537.96
    ==========================================================================================



### 레이어 함수 교체하기


```python
# 난수 고정
torch_seed()

# 최종 레이어 함수 교체
in_features = net.classifier[6].in_features
net.classifier[6] = nn.Linear(in_features, n_output)
```


```python
# features의 마지막 요소(MaxPool2d)를 제거
net.features = net.features[:-1]
print(net.features)
```

    Sequential(
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
    )



```python
# avgpool에 위치한AdaptiveAvgPool2d을 아무것도 하지 않는 함수(nn.Identity)로 치환
net.avgpool = nn.Identity()
```

### 결과 확인


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
      )
      (avgpool): Identity()
      (classifier): Sequential(
        (0): Linear(in_features=25088, out_features=4096, bias=True)
        (1): ReLU(inplace=True)
        (2): Dropout(p=0.5, inplace=False)
        (3): Linear(in_features=4096, out_features=4096, bias=True)
        (4): ReLU(inplace=True)
        (5): Dropout(p=0.5, inplace=False)
        (6): Linear(in_features=4096, out_features=10, bias=True)
      )
    )



```python
# 실습용 데이터 사이즈로 중간 텐서 확인(배치사이즈 100)
net = net.to(device)
summary(net,(100, 3, 112, 112))
```




    ==========================================================================================
    Layer (type:depth-idx)                   Output Shape              Param #
    ==========================================================================================
    VGG                                      [100, 10]                 --
    ├─Sequential: 1-1                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-1                       [100, 64, 112, 112]       1,792
    │    └─BatchNorm2d: 2-2                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-3                         [100, 64, 112, 112]       --
    │    └─Conv2d: 2-4                       [100, 64, 112, 112]       36,928
    │    └─BatchNorm2d: 2-5                  [100, 64, 112, 112]       128
    │    └─ReLU: 2-6                         [100, 64, 112, 112]       --
    │    └─MaxPool2d: 2-7                    [100, 64, 56, 56]         --
    │    └─Conv2d: 2-8                       [100, 128, 56, 56]        73,856
    │    └─BatchNorm2d: 2-9                  [100, 128, 56, 56]        256
    │    └─ReLU: 2-10                        [100, 128, 56, 56]        --
    │    └─Conv2d: 2-11                      [100, 128, 56, 56]        147,584
    │    └─BatchNorm2d: 2-12                 [100, 128, 56, 56]        256
    │    └─ReLU: 2-13                        [100, 128, 56, 56]        --
    │    └─MaxPool2d: 2-14                   [100, 128, 28, 28]        --
    │    └─Conv2d: 2-15                      [100, 256, 28, 28]        295,168
    │    └─BatchNorm2d: 2-16                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-17                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-18                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-19                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-20                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-21                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-22                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-23                        [100, 256, 28, 28]        --
    │    └─Conv2d: 2-24                      [100, 256, 28, 28]        590,080
    │    └─BatchNorm2d: 2-25                 [100, 256, 28, 28]        512
    │    └─ReLU: 2-26                        [100, 256, 28, 28]        --
    │    └─MaxPool2d: 2-27                   [100, 256, 14, 14]        --
    │    └─Conv2d: 2-28                      [100, 512, 14, 14]        1,180,160
    │    └─BatchNorm2d: 2-29                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-30                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-31                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-32                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-33                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-34                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-35                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-36                        [100, 512, 14, 14]        --
    │    └─Conv2d: 2-37                      [100, 512, 14, 14]        2,359,808
    │    └─BatchNorm2d: 2-38                 [100, 512, 14, 14]        1,024
    │    └─ReLU: 2-39                        [100, 512, 14, 14]        --
    │    └─MaxPool2d: 2-40                   [100, 512, 7, 7]          --
    │    └─Conv2d: 2-41                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-42                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-43                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-44                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-45                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-46                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-47                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-48                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-49                        [100, 512, 7, 7]          --
    │    └─Conv2d: 2-50                      [100, 512, 7, 7]          2,359,808
    │    └─BatchNorm2d: 2-51                 [100, 512, 7, 7]          1,024
    │    └─ReLU: 2-52                        [100, 512, 7, 7]          --
    ├─Identity: 1-2                          [100, 512, 7, 7]          --
    ├─Sequential: 1-3                        [100, 10]                 --
    │    └─Linear: 2-53                      [100, 4096]               102,764,544
    │    └─ReLU: 2-54                        [100, 4096]               --
    │    └─Dropout: 2-55                     [100, 4096]               --
    │    └─Linear: 2-56                      [100, 4096]               16,781,312
    │    └─ReLU: 2-57                        [100, 4096]               --
    │    └─Dropout: 2-58                     [100, 4096]               --
    │    └─Linear: 2-59                      [100, 10]                 40,970
    ==========================================================================================
    Total params: 139,622,218
    Trainable params: 139,622,218
    Non-trainable params: 0
    Total mult-adds (G): 500.04
    ==========================================================================================
    Input size (MB): 15.05
    Forward/backward pass size (MB): 5947.40
    Params size (MB): 558.49
    Estimated Total Size (MB): 6520.94
    ==========================================================================================


