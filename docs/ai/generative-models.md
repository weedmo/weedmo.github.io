# 생성 모델 (GAN/NeRF)


## 강의_3기_AI응용_7차시__style_transfer_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_7차시__style_transfer_.ipynb)

# 7장 스타일 전이 (Style transfer)

* "부록3 매트플롯립 입문"에서 한글 폰트를 올바르게 출력하기 위한 설치 방법을 설명했다. 설치 방법은 다음과 같다.


```python
# 한글 폰트 설치

!sudo apt-get install -y fonts-nanum* | tail -n 1
!sudo fc-cache -fv
!rm -rf ~/.cache/matplotlib
```


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
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

# Mac
# font_name = "AppleGothic"
```

* 모든 설치가 끝나면 한글 폰트를 바르게 출력하기 위해 **[런타임]** -> **[런타임 다시시작]**을 클릭한 다음, 아래 셀부터 코드를 실행해 주십시오.


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
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## Tensor 함수 정의


```python
def image_to_tensor(image_filepath, image_dimension=128):
    img = Image.open(image_filepath).convert('RGB')
    
    # display image to check 
    plt.figure()
    plt.title(image_filepath)
    plt.imshow(img)
    
    if max(img.size) <= image_dimension:
        img_size = max(img.size)
    else:
        img_size = image_dimension
  
    torch_transformation = torchvision.transforms.Compose([
        torchvision.transforms.Resize(img_size),
        torchvision.transforms.ToTensor()
    ])
  
    img = torch_transformation(img).unsqueeze(0)
  
    return img.to(device, torch.float)

style_image = image_to_tensor(os.path.join(os.getcwd(), "images/style.jpg"))
content_image = image_to_tensor(os.path.join(os.getcwd(),"images/content.jpg"))
```


    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__8_0.webp)
    



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__8_1.webp)
    


## Define gram matrix


```python
def gram_matrix(ip):
    num_batch, num_channels, height, width = ip.size()
    feats = ip.view(num_batch * num_channels, width * height)
    gram_mat = torch.mm(feats, feats.t()) 
    return gram_mat.div(num_batch * num_channels * width * height) # Different layers in a CNN produce feature maps of different sizes.
```

## Pretrained model


```python
weights = torchvision.models.VGG19_Weights.DEFAULT
vgg19_model = torchvision.models.vgg19(weights = weights).to(device)
print(vgg19_model)
```

    VGG(
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
        (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (17): ReLU(inplace=True)
        (18): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (20): ReLU(inplace=True)
        (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (22): ReLU(inplace=True)
        (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (24): ReLU(inplace=True)
        (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (26): ReLU(inplace=True)
        (27): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (29): ReLU(inplace=True)
        (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (31): ReLU(inplace=True)
        (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (33): ReLU(inplace=True)
        (34): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        (35): ReLU(inplace=True)
        (36): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
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
vgg19_model = vgg19_model.features
print(vgg19_model)                                                            
```

    Sequential(
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
      (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (17): ReLU(inplace=True)
      (18): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
      (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (20): ReLU(inplace=True)
      (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (22): ReLU(inplace=True)
      (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (24): ReLU(inplace=True)
      (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (26): ReLU(inplace=True)
      (27): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
      (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (29): ReLU(inplace=True)
      (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (31): ReLU(inplace=True)
      (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (33): ReLU(inplace=True)
      (34): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (35): ReLU(inplace=True)
      (36): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
    )



```python
for param in vgg19_model.parameters():
    param.requires_grad_(False)
```

## refine model for this task

### change maxpool layers to avgpool


```python
conv_indices = []

for i in range(len(vgg19_model)):
    if vgg19_model[i]._get_name() == 'MaxPool2d':
        vgg19_model[i] = nn.AvgPool2d(kernel_size=vgg19_model[i].kernel_size, 
                                      stride=vgg19_model[i].stride, 
                                      padding=vgg19_model[i].padding)
    if vgg19_model[i]._get_name() == 'Conv2d':
        conv_indices.append(i)
        
conv_indices = dict(enumerate(conv_indices, start = 1))
print("vgg19_model = \n", vgg19_model)
print(conv_indices)
```

    vgg19_model = 
     Sequential(
      (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (1): ReLU(inplace=True)
      (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (3): ReLU(inplace=True)
      (4): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (8): ReLU(inplace=True)
      (9): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (11): ReLU(inplace=True)
      (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (13): ReLU(inplace=True)
      (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (15): ReLU(inplace=True)
      (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (17): ReLU(inplace=True)
      (18): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (20): ReLU(inplace=True)
      (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (22): ReLU(inplace=True)
      (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (24): ReLU(inplace=True)
      (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (26): ReLU(inplace=True)
      (27): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (29): ReLU(inplace=True)
      (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (31): ReLU(inplace=True)
      (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (33): ReLU(inplace=True)
      (34): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (35): ReLU(inplace=True)
      (36): AvgPool2d(kernel_size=2, stride=2, padding=0)
    )
    {1: 0, 2: 2, 3: 5, 4: 7, 5: 10, 6: 12, 7: 14, 8: 16, 9: 19, 10: 21, 11: 23, 12: 25, 13: 28, 14: 30, 15: 32, 16: 34}


### clip until the last relevant layer


```python
layers = {1: 's', 2: 's', 3: 's', 4: 'sc', 5: 's'} #  style loss, content loss layers  
```

### nn.ModuleList vs nn.Sequential


```python
## nn.ModuleList

import torch
import torch.nn as nn

class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(10, 20),
            nn.Linear(20, 30),
            nn.Linear(30, 40)
        ])

    def forward(self, x):
        for layer in self.layers:  # Must manually apply each layer
            x = layer(x)
        return x

model = CustomModel()
x = torch.randn(1, 10)
output = model(x)
print(output.shape)  # torch.Size([1, 40])

```

    torch.Size([1, 40])



```python
## nn.Sequential

model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 30),
    nn.ReLU(),
    nn.Linear(30, 40)
)

x = torch.randn(1, 10)
output = model(x)  # No need to manually loop over layers
print(output.shape)  # torch.Size([1, 40])

```

    torch.Size([1, 40])



```python
vgg_layers = nn.ModuleList(vgg19_model)
vgg_layers
```




    ModuleList(
      (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (1): ReLU(inplace=True)
      (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (3): ReLU(inplace=True)
      (4): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (8): ReLU(inplace=True)
      (9): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (11): ReLU(inplace=True)
      (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (13): ReLU(inplace=True)
      (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (15): ReLU(inplace=True)
      (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (17): ReLU(inplace=True)
      (18): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (20): ReLU(inplace=True)
      (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (22): ReLU(inplace=True)
      (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (24): ReLU(inplace=True)
      (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (26): ReLU(inplace=True)
      (27): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (29): ReLU(inplace=True)
      (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (31): ReLU(inplace=True)
      (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (33): ReLU(inplace=True)
      (34): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (35): ReLU(inplace=True)
      (36): AvgPool2d(kernel_size=2, stride=2, padding=0)
    )




```python
display(conv_indices)
```


    {1: 0,
     2: 2,
     3: 5,
     4: 7,
     5: 10,
     6: 12,
     7: 14,
     8: 16,
     9: 19,
     10: 21,
     11: 23,
     12: 25,
     13: 28,
     14: 30,
     15: 32,
     16: 34}



```python
last_layer_idx = conv_indices[max(layers.keys())]
vgg_layers_trimmed = vgg_layers[:last_layer_idx+1]
vgg_layers_trimmed
```




    ModuleList(
      (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (1): ReLU(inplace=True)
      (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (3): ReLU(inplace=True)
      (4): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (8): ReLU(inplace=True)
      (9): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    )




```python

neural_style_transfer_model = nn.Sequential(*vgg_layers_trimmed) # ModuleList
print(neural_style_transfer_model)
```

    Sequential(
      (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (1): ReLU(inplace=True)
      (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (3): ReLU(inplace=True)
      (4): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
      (8): ReLU(inplace=True)
      (9): AvgPool2d(kernel_size=2, stride=2, padding=0)
      (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    )



```python
# initialize as the content image
# ip_image = content_image.clone()
# initialize as random noise:
ip_image = torch.randn(content_image.data.size(), device=device)

plt.figure()
plt.imshow(ip_image.squeeze(0).cpu().detach().numpy().transpose(1,2,0).clip(0,1))
plt.show()
```


    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__27_0.webp)
    



```python
layers.keys()
layers
```




    {1: 's', 2: 's', 3: 's', 4: 'sc', 5: 's'}



### Gram matrix


```python
ip_image.requires_grad_()
```




    tensor([[[[0.9685, 0.5018, 1.0000,  ..., 1.0000, 1.0000, 1.0000],
              [0.4308, 0.9483, 0.8263,  ..., 0.9796, 1.0000, 0.9929],
              [1.0000, 0.6389, 1.0000,  ..., 1.0000, 0.8779, 1.0000],
              ...,
              [0.9839, 1.0000, 0.7147,  ..., 0.4384, 0.3309, 0.5805],
              [1.0000, 0.6127, 1.0000,  ..., 0.2926, 0.2314, 0.3630],
              [0.6824, 1.0000, 0.7322,  ..., 0.1382, 0.1579, 0.3245]],
    
             [[0.0000, 0.2755, 0.0826,  ..., 0.2292, 0.4039, 0.0000],
              [0.2891, 0.2333, 0.3617,  ..., 0.4678, 0.0531, 0.3399],
              [0.2574, 0.2820, 0.2812,  ..., 0.3745, 0.4138, 0.2506],
              ...,
              [0.1301, 0.3148, 0.3671,  ..., 0.1476, 0.1007, 0.1166],
              [0.2558, 0.5799, 0.3098,  ..., 0.1776, 0.1467, 0.1793],
              [0.1558, 0.2935, 0.4051,  ..., 0.1051, 0.1772, 0.0319]],
    
             [[0.0035, 0.2902, 0.4329,  ..., 0.3850, 0.4592, 0.4918],
              [0.0298, 0.2934, 0.4216,  ..., 0.2762, 0.7895, 0.3405],
              [0.0135, 0.6228, 0.0931,  ..., 0.0626, 0.2484, 0.3067],
              ...,
              [0.5531, 0.3087, 0.5950,  ..., 0.3020, 0.5396, 0.1632],
              [0.4838, 0.4352, 0.3822,  ..., 0.1336, 0.4709, 0.3021],
              [0.6914, 0.5223, 0.6157,  ..., 0.3515, 0.2850, 0.1755]]]],
           device='cuda:0', requires_grad=True)




```python
def gram_matrix(input_tensor):  
    batch, channels, height, width = input_tensor.size()  
    features = input_tensor.view(channels, height * width)  
    gram = torch.mm(features, features.t())  
    return gram  
```


```python
num_epochs=1000
wt_style=1e6 #
wt_content=1  
style_losses = []
content_losses = []
optimizer = optim.Adam([ip_image.requires_grad_()], lr=0.1) # requires_grad=False => True

for curr_epoch in range(1, num_epochs+1): 
     
    ip_image.data.clamp_(0, 1) # Clamps all elements in input into the range [ min, max ].
    optimizer.zero_grad()
    epoch_style_loss = 0
    epoch_content_loss = 0

    for k in layers.keys(): # layers = {1: 's', 2: 's', 3: 's', 4: 'sc', 5: 's'} 
        if 'c' in layers[k]:
            target = neural_style_transfer_model[:conv_indices[k]+1](content_image).detach()
            ip = neural_style_transfer_model[:conv_indices[k]+1](ip_image)
            epoch_content_loss += torch.nn.functional.mse_loss(ip, target)
        if 's' in layers[k]:
            target = gram_matrix(neural_style_transfer_model[:conv_indices[k]+1](style_image)).detach()
            ip = gram_matrix(neural_style_transfer_model[:conv_indices[k]+1](ip_image))
            epoch_style_loss += torch.nn.functional.mse_loss(ip, target)

    epoch_style_loss *= wt_style
    epoch_content_loss *= wt_content
    total_loss = epoch_style_loss + epoch_content_loss
    # total_loss = epoch_style_loss*wt_style + epoch_content_loss*wt_content
    total_loss.backward()
    optimizer.step()

    if curr_epoch % 50 == 0:
        print(f"epoch number {curr_epoch}")
        print(f"style loss = {epoch_style_loss}, content loss = {epoch_content_loss}")
        plt.figure()
        plt.title(f"epoch number {curr_epoch}")
        plt.imshow(ip_image.data.clamp_(0, 1).squeeze(0).cpu().detach().numpy().transpose(1,2,0))
        plt.show()
        # style_losses += [epoch_style_loss]
        # content_losses += [epoch_content_loss]
        style_losses.append(epoch_style_loss.item())
        content_losses.append(epoch_content_loss.item())    
```

    epoch number 50
    style loss = 1549675.625, content loss = 6.785552978515625



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_1.webp)
    


    epoch number 100
    style loss = 405820.21875, content loss = 6.825432777404785



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_3.webp)
    


    epoch number 150
    style loss = 175832.9375, content loss = 6.8693928718566895



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_5.webp)
    


    epoch number 200
    style loss = 107132.3125, content loss = 6.882870674133301



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_7.webp)
    


    epoch number 250
    style loss = 74419.546875, content loss = 6.888459205627441



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_9.webp)
    


    epoch number 300
    style loss = 55290.75, content loss = 6.892725944519043



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_11.webp)
    


    epoch number 350
    style loss = 42981.4296875, content loss = 6.9012837409973145



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_13.webp)
    


    epoch number 400
    style loss = 34623.1328125, content loss = 6.909946441650391



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_15.webp)
    


    epoch number 450
    style loss = 28619.6796875, content loss = 6.916177749633789



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_17.webp)
    


    epoch number 500
    style loss = 24175.734375, content loss = 6.9187116622924805



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_19.webp)
    


    epoch number 550
    style loss = 20794.16015625, content loss = 6.919804573059082



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_21.webp)
    


    epoch number 600
    style loss = 18158.138671875, content loss = 6.921343803405762



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_23.webp)
    


    epoch number 650
    style loss = 16043.8134765625, content loss = 6.921295642852783



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_25.webp)
    


    epoch number 700
    style loss = 14302.953125, content loss = 6.920389652252197



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_27.webp)
    


    epoch number 750
    style loss = 12846.0888671875, content loss = 6.9187140464782715



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_29.webp)
    


    epoch number 800
    style loss = 11612.380859375, content loss = 6.916598796844482



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_31.webp)
    


    epoch number 850
    style loss = 10563.580078125, content loss = 6.914859771728516



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_33.webp)
    


    epoch number 900
    style loss = 9662.107421875, content loss = 6.914201736450195



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_35.webp)
    


    epoch number 950
    style loss = 8869.5400390625, content loss = 6.914239406585693



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_37.webp)
    


    epoch number 1000
    style loss = 8171.505859375, content loss = 6.9142255783081055



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__32_39.webp)
    



```python
plt.plot(range(50, 1000+1, 50), torch.tensor(style_losses), label='style_loss')
plt.plot(range(50, 1000+1, 50), torch.tensor(content_losses), label='content_loss')
plt.legend()
plt.show()
```


    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_7%EC%B0%A8%EC%8B%9C__style_transfer__33_0.webp)
    



## 강의_3기_AI응용_8차시__GAN_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_8차시__GAN_.ipynb)

# 8장 적대적 생성 신경망 (Generative adversarial network)

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
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=10).get_name()

# Window
# font_name = "NanumBarunGothic"

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
import numpy as np
import matplotlib.pyplot as plt


import cv2
import torch
from torch import nn, optim
from torchvision import transforms, datasets
from torchvision.utils import save_image
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torch.autograd import Variable

```


```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device = ", device)
```

    device =  cuda


## Vanilla GAN

### Vanilla GAN hyperparameters


```python
# Hyper-parameters & Variables setting
num_epoch = 1000
batch_size = 100
learning_rate = 0.0002
img_size = 28 * 28
num_channel = 1
dir_name = "GAN_results"

noise_size = 100
hidden_size1 = 256
hidden_size2 = 512
# hidden_size3 = 1024

# Create a directory for saving samples
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
```

### MNIST 데이터 


```python
# Dataset transform setting
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5)])
```


```python
# MNIST dataset setting
MNIST_dataset = datasets.MNIST(root='./',
                                train=True,
                                transform=transform,
                                download=True)

# Data loader
data_loader = DataLoader(dataset=MNIST_dataset,
                        batch_size=batch_size,
                        shuffle=True)
```

    100%|██████████| 9.91M/9.91M [00:02<00:00, 4.46MB/s]
    100%|██████████| 28.9k/28.9k [00:00<00:00, 164kB/s]
    100%|██████████| 1.65M/1.65M [00:01<00:00, 1.51MB/s]
    100%|██████████| 4.54k/4.54k [00:00<00:00, 4.55MB/s]


### 판별기 (Discriminator) 모델


```python
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(img_size, hidden_size2)
        self.linear2 = nn.Linear(hidden_size2, hidden_size1)
        self.linear3 = nn.Linear(hidden_size1, 1)
        self.leaky_relu = nn.LeakyReLU(0.2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.leaky_relu(self.linear1(x))
        x = self.leaky_relu(self.linear2(x))
        x = self.linear3(x)
        x = self.sigmoid(x)
        return x
```

### 생성기 (Generator) 모델


```python
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.linear1 = nn.Linear(noise_size, hidden_size1)
        self.linear2 = nn.Linear(hidden_size1, hidden_size2)
        self.linear3 = nn.Linear(hidden_size2, img_size)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.relu(self.linear1(x))
        x = self.relu(self.linear2(x))
        x = self.linear3(x)
        x = self.tanh(x)
        return x
```


```python
# Initialize generator/Discriminator
discriminator = Discriminator().to(device)
generator = Generator().to(device)
```

### Vanilla GAN 학습


```python
# Loss function & Optimizer setting
criterion = nn.BCELoss()
d_optimizer = optim.Adam(discriminator.parameters(), lr=learning_rate)
g_optimizer = optim.Adam(generator.parameters(), lr=learning_rate)
```


```python
# next(iter(data_loader))[0].shape  # torch.Size([100, 1, 28, 28])
# batch_size # 100
img_test = next(iter(data_loader))[0]
img_test.reshape(100, -1).shape
# print(len(data_loader))
```




    torch.Size([100, 784])




```python
"""
Training part
"""
for epoch in range(num_epoch):
    for i, (images, label) in enumerate(data_loader):

        # make ground truth (labels) -> 1 for real, 0 for fake
        real_label = torch.full((batch_size, 1), 1, dtype=torch.float32).to(device) # batch_size  100
        fake_label = torch.full((batch_size, 1), 0, dtype=torch.float32).to(device)

        # reshape real images from MNIST dataset
        real_images = images.reshape(batch_size, -1).to(device) # torch.Size([100, 784])

        # +---------------------+
        # |   train Generator   |
        # +---------------------+

        # Initialize grad
        g_optimizer.zero_grad()
        # d_optimizer.zero_grad()

        # make fake images with generator & noise vector 'z'
        z = torch.randn(batch_size, noise_size).to(device)
        fake_images = generator(z)
        
        # Compare result of discriminator with fake images & real labels
        # If generator deceives discriminator, g_loss will decrease
        # discriminator should be freezing
        g_loss = criterion(discriminator(fake_images), real_label)

        # Train generator with backpropagation
        g_loss.backward()
        g_optimizer.step()

        # +---------------------+
        # | train Discriminator |
        # +---------------------+

        # Initialize grad
        d_optimizer.zero_grad()
        g_optimizer.zero_grad()

        # make fake images with generator & noise vector 'z'
        z = torch.randn(batch_size, noise_size).to(device)
        fake_images = generator(z)

        # Calculate fake & real loss with generated images above & real images
        fake_loss = criterion(discriminator(fake_images), fake_label)
        real_loss = criterion(discriminator(real_images), real_label)
        d_loss = (fake_loss + real_loss) / 2

        # Train discriminator with backpropagation
        # In this part, we don't train generator
        d_loss.backward()
        d_optimizer.step()

        d_performance = discriminator(real_images).mean()
        g_performance = discriminator(fake_images).mean()

        if (i + 1) % 150 == 0:
            print("Epoch [ {}/{} ]  Step [ {}/{} ]  d_loss : {:.5f}  g_loss : {:.5f}"
                  .format(epoch, num_epoch, i+1, len(data_loader), d_loss.item(), g_loss.item()))

    # print discriminator & generator's performance
    print(" Epock {}'s discriminator performance : {:.2f}  generator performance : {:.2f}"
          .format(epoch, d_performance, g_performance))

    # Save fake images in each epoch
    samples = fake_images.reshape(batch_size, 1, 28, 28)
    save_image(samples, os.path.join(dir_name, 'GAN_fake_samples{}.png'.format(epoch + 1)))
```

## DCGAN

### DCGAN hyperparameters


```python
num_eps=10      # num_epoch
bsize=32        # batch_size 
lrate=0.001     # learning_rate
noise_size=64 # noise_size
img_size=64     # img_size
num_channel=1         # num_channel
```

### DCGAN 생성기


```python
class GANGenerator(nn.Module):
    def __init__(self):
        super(GANGenerator, self).__init__()
        self.inp_sz = img_size // 4
        self.lin = nn.Linear(noise_size, 128 * self.inp_sz ** 2)
        self.bn1 = nn.BatchNorm2d(128)
        self.up1 = nn.Upsample(scale_factor=2, mode ='nearest')
        self.cn1 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(128, 0.8)
        self.rl1 = nn.LeakyReLU(0.2, inplace=True)
        self.up2 = nn.Upsample(scale_factor=2)
        self.cn2 = nn.Conv2d(128, 64, 3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64, 0.8)
        self.rl2 = nn.LeakyReLU(0.2, inplace=True)
        self.cn3 = nn.Conv2d(64, num_channel, 3, stride=1, padding=1)
        self.act = nn.Tanh()

    def forward(self, x):
        x = self.lin(x)
        x = x.view(x.shape[0], 128, self.inp_sz, self.inp_sz)
        x = self.bn1(x)
        x = self.up1(x)
        x = self.cn1(x)
        x = self.bn2(x)
        x = self.rl1(x)
        x = self.up2(x)
        x = self.cn2(x)
        x = self.bn3(x)
        x = self.rl2(x)
        x = self.cn3(x)
        out = self.act(x)
        return out
```

### DCGAN 분류기


```python
# num_eps=10
# bsize=32
# lrate=0.001
# lat_dimension=64
# image_sz=64
# chnls=1
# logging_intv=200

class GANDiscriminator(nn.Module):
    def __init__(self):
        super(GANDiscriminator, self).__init__()

        def disc_module(ip_chnls, op_chnls, bnorm=True):
            mod = [nn.Conv2d(ip_chnls, op_chnls, 3, 2, 1), 
                   nn.LeakyReLU(0.2, inplace=True), 
                   nn.Dropout2d(0.25)]
            if bnorm:
                mod += [nn.BatchNorm2d(op_chnls, 0.8)]
            return mod

        self.disc_model = nn.Sequential(
            *disc_module(num_channel, 16, bnorm=False),
            *disc_module(16, 32),
            *disc_module(32, 64),
            *disc_module(64, 128),
        )

        # width and height of the down-sized image
        ds_size = img_size // 2 ** 4
        self.adverse_lyr = nn.Sequential(
            nn.Linear(128 * ds_size ** 2, 1), 
            nn.Sigmoid())

    def forward(self, x):
        x = self.disc_model(x)
        x = x.view(x.shape[0], -1)
        out = self.adverse_lyr(x)
        return out
```


```python
# instantiate the discriminator and generator models
gen = GANGenerator().to(device)
disc = GANDiscriminator().to(device)

# define the loss metric
adv_loss_func = torch.nn.BCELoss()
```


```python
# define the dataset and corresponding dataloader
data_loader = DataLoader(
    datasets.MNIST(
        root="./",
        download=True,
        transform=transforms.Compose(
            [transforms.Resize((img_size, img_size)), 
             transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
        ),
    ),
    batch_size=bsize,
    shuffle=True,
)

# define the optimization schedule for both G and D
opt_gen = optim.Adam(gen.parameters(), lr=lrate)
opt_disc = optim.Adam(disc.parameters(), lr=lrate)
```


```python
from tqdm import tqdm
os.makedirs("./DCGAN_results", exist_ok=True)

for ep in tqdm(range(num_eps)):
    for idx, (images, _) in enumerate(data_loader):

        # generate grounnd truths for real and fake images
        real_label = torch.full((images.shape[0], 1), 1, dtype = torch.float32).to(device)
        fake_label = torch.full((images.shape[0], 1), 0, dtype = torch.float32).to(device)

        # get a real image
        real_images = images.to(device)

        # train the generator model
        opt_gen.zero_grad()

        # generate a batch of images based on random noise as input
        noise = torch.randn(images.shape[0], noise_size).to(device)
        fake_images = gen(noise)

        # generator model optimization - how well can it fool the discriminator
        generator_loss = adv_loss_func(disc(fake_images), real_label)
        generator_loss.backward()
        opt_gen.step()

        # train the discriminator model
        opt_disc.zero_grad()

        # calculate discriminator loss as average of mistakes(losses) in confusing real images as fake and vice versa
        actual_image_loss = adv_loss_func(disc(real_images), real_label)
        fake_image_loss = adv_loss_func(disc(fake_images.detach()), fake_label)
        discriminator_loss = (actual_image_loss + fake_image_loss) / 2

        # discriminator model optimization
        discriminator_loss.backward()
        opt_disc.step()

        batches_completed = ep * len(dloader) + idx
        if batches_completed % 200 == 0:
            print(f"epoch number {ep} | batch number {idx} | generator loss = {generator_loss.item()} | discriminator loss = {discriminator_loss.item()}")
            save_image(fake_images.data[:25], f"DCGAN_results/{batches_completed}.png", nrow=5, normalize=True)
```

      0%|          | 0/10 [00:00<?, ?it/s]

    epoch number 0 | batch number 0 | generator loss = 3.9545516967773438 | discriminator loss = 0.2782806158065796
    epoch number 0 | batch number 200 | generator loss = 3.554192304611206 | discriminator loss = 0.03740197420120239
    epoch number 0 | batch number 400 | generator loss = 1.8775991201400757 | discriminator loss = 0.13742583990097046
    epoch number 0 | batch number 600 | generator loss = 4.771371841430664 | discriminator loss = 0.0422741174697876
    epoch number 0 | batch number 800 | generator loss = 6.1848835945129395 | discriminator loss = 0.06815836578607559
    epoch number 0 | batch number 1000 | generator loss = 6.0200371742248535 | discriminator loss = 0.012616288848221302
    epoch number 0 | batch number 1200 | generator loss = 3.3388099670410156 | discriminator loss = 0.20030230283737183
    epoch number 0 | batch number 1400 | generator loss = 3.468569755554199 | discriminator loss = 0.05986403673887253
    epoch number 0 | batch number 1600 | generator loss = 4.02747106552124 | discriminator loss = 0.15941214561462402
    epoch number 0 | batch number 1800 | generator loss = 1.9418367147445679 | discriminator loss = 0.19932261109352112


     10%|█         | 1/10 [00:49<07:22, 49.16s/it]

    epoch number 1 | batch number 125 | generator loss = 4.23289680480957 | discriminator loss = 0.04313182458281517
    epoch number 1 | batch number 325 | generator loss = 3.6431376934051514 | discriminator loss = 0.25708135962486267
    epoch number 1 | batch number 525 | generator loss = 3.278818368911743 | discriminator loss = 0.08988559246063232
    epoch number 1 | batch number 725 | generator loss = 2.4317989349365234 | discriminator loss = 0.05262760818004608
    epoch number 1 | batch number 925 | generator loss = 2.1540660858154297 | discriminator loss = 0.19819074869155884
    epoch number 1 | batch number 1125 | generator loss = 4.866243362426758 | discriminator loss = 0.07104020565748215
    epoch number 1 | batch number 1325 | generator loss = 4.817590713500977 | discriminator loss = 0.03069155663251877
    epoch number 1 | batch number 1525 | generator loss = 5.30476188659668 | discriminator loss = 0.1353522092103958
    epoch number 1 | batch number 1725 | generator loss = 3.282376766204834 | discriminator loss = 0.07071726024150848


     20%|██        | 2/10 [01:37<06:30, 48.86s/it]

    epoch number 2 | batch number 50 | generator loss = 5.153894424438477 | discriminator loss = 0.04896470159292221
    epoch number 2 | batch number 250 | generator loss = 4.530649185180664 | discriminator loss = 0.3270239531993866
    epoch number 2 | batch number 450 | generator loss = 8.000043869018555 | discriminator loss = 0.10126665979623795
    epoch number 2 | batch number 650 | generator loss = 6.198918342590332 | discriminator loss = 0.010016540065407753
    epoch number 2 | batch number 850 | generator loss = 5.983379364013672 | discriminator loss = 0.3273736536502838
    epoch number 2 | batch number 1050 | generator loss = 4.024206161499023 | discriminator loss = 0.038508810102939606
    epoch number 2 | batch number 1250 | generator loss = 0.7392721176147461 | discriminator loss = 0.15315017104148865
    epoch number 2 | batch number 1450 | generator loss = 3.7891921997070312 | discriminator loss = 0.1695229858160019
    epoch number 2 | batch number 1650 | generator loss = 4.046806335449219 | discriminator loss = 0.10749366879463196
    epoch number 2 | batch number 1850 | generator loss = 4.57669734954834 | discriminator loss = 0.12455864250659943


     30%|███       | 3/10 [02:27<05:44, 49.16s/it]

    epoch number 3 | batch number 175 | generator loss = 5.730733871459961 | discriminator loss = 0.12807787954807281
    epoch number 3 | batch number 375 | generator loss = 4.793088912963867 | discriminator loss = 0.37881994247436523
    epoch number 3 | batch number 575 | generator loss = 6.7368974685668945 | discriminator loss = 0.016468007117509842
    epoch number 3 | batch number 775 | generator loss = 5.118185997009277 | discriminator loss = 0.034300170838832855
    epoch number 3 | batch number 975 | generator loss = 5.057310581207275 | discriminator loss = 0.10720119625329971
    epoch number 3 | batch number 1175 | generator loss = 6.804218769073486 | discriminator loss = 0.008177373558282852
    epoch number 3 | batch number 1375 | generator loss = 3.3641469478607178 | discriminator loss = 0.10269354283809662
    epoch number 3 | batch number 1575 | generator loss = 5.981612205505371 | discriminator loss = 0.021350819617509842
    epoch number 3 | batch number 1775 | generator loss = 5.107820510864258 | discriminator loss = 0.2083660066127777


     40%|████      | 4/10 [03:16<04:55, 49.24s/it]

    epoch number 4 | batch number 100 | generator loss = 8.087093353271484 | discriminator loss = 0.09759678691625595
    epoch number 4 | batch number 300 | generator loss = 1.7739126682281494 | discriminator loss = 0.6854257583618164
    epoch number 4 | batch number 500 | generator loss = 8.029947280883789 | discriminator loss = 0.045721717178821564
    epoch number 4 | batch number 700 | generator loss = 3.9087915420532227 | discriminator loss = 0.16519811749458313
    epoch number 4 | batch number 900 | generator loss = 5.707446575164795 | discriminator loss = 0.08258886635303497
    epoch number 4 | batch number 1100 | generator loss = 1.5349751710891724 | discriminator loss = 0.53525710105896
    epoch number 4 | batch number 1300 | generator loss = 3.1992595195770264 | discriminator loss = 0.004317648708820343
    epoch number 4 | batch number 1500 | generator loss = 7.143947601318359 | discriminator loss = 0.0162322036921978
    epoch number 4 | batch number 1700 | generator loss = 4.835370063781738 | discriminator loss = 0.33377426862716675


     50%|█████     | 5/10 [04:12<04:18, 51.67s/it]

    epoch number 5 | batch number 25 | generator loss = 2.1899523735046387 | discriminator loss = 0.16276304423809052
    epoch number 5 | batch number 225 | generator loss = 5.253238677978516 | discriminator loss = 0.3563573360443115
    epoch number 5 | batch number 425 | generator loss = 7.449577808380127 | discriminator loss = 0.12209033966064453
    epoch number 5 | batch number 625 | generator loss = 3.859504222869873 | discriminator loss = 0.17049042880535126
    epoch number 5 | batch number 825 | generator loss = 4.514573574066162 | discriminator loss = 0.06178569048643112
    epoch number 5 | batch number 1025 | generator loss = 5.278169631958008 | discriminator loss = 0.027951447293162346
    epoch number 5 | batch number 1225 | generator loss = 6.560893535614014 | discriminator loss = 0.08444608002901077
    epoch number 5 | batch number 1425 | generator loss = 7.850395202636719 | discriminator loss = 0.25208404660224915
    epoch number 5 | batch number 1625 | generator loss = 4.836728096008301 | discriminator loss = 0.0652989074587822
    epoch number 5 | batch number 1825 | generator loss = 8.25395679473877 | discriminator loss = 0.03623552992939949


     60%|██████    | 6/10 [05:01<03:23, 50.85s/it]

    epoch number 6 | batch number 150 | generator loss = 11.474748611450195 | discriminator loss = 0.4834703803062439
    epoch number 6 | batch number 350 | generator loss = 4.103691101074219 | discriminator loss = 0.18094411492347717
    epoch number 6 | batch number 550 | generator loss = 5.099274635314941 | discriminator loss = 0.08729465305805206
    epoch number 6 | batch number 750 | generator loss = 3.8545188903808594 | discriminator loss = 0.06430787593126297
    epoch number 6 | batch number 950 | generator loss = 1.6146601438522339 | discriminator loss = 0.004101771395653486
    epoch number 6 | batch number 1150 | generator loss = 1.69037926197052 | discriminator loss = 0.0950821042060852
    epoch number 6 | batch number 1350 | generator loss = 3.2029476165771484 | discriminator loss = 0.01881629414856434
    epoch number 6 | batch number 1550 | generator loss = 6.5531840324401855 | discriminator loss = 0.05114094167947769
    epoch number 6 | batch number 1750 | generator loss = 8.155012130737305 | discriminator loss = 0.37255942821502686


     70%|███████   | 7/10 [05:51<02:31, 50.50s/it]

    epoch number 7 | batch number 75 | generator loss = 5.89101505279541 | discriminator loss = 0.029376033693552017
    epoch number 7 | batch number 275 | generator loss = 3.817337989807129 | discriminator loss = 0.02690809778869152
    epoch number 7 | batch number 475 | generator loss = 10.73667049407959 | discriminator loss = 0.1453002542257309
    epoch number 7 | batch number 675 | generator loss = 3.355811595916748 | discriminator loss = 0.22888179123401642
    epoch number 7 | batch number 875 | generator loss = 2.42566180229187 | discriminator loss = 0.4170704782009125
    epoch number 7 | batch number 1075 | generator loss = 4.84708833694458 | discriminator loss = 0.16885662078857422
    epoch number 7 | batch number 1275 | generator loss = 5.702351093292236 | discriminator loss = 0.03158178552985191
    epoch number 7 | batch number 1475 | generator loss = 6.083104133605957 | discriminator loss = 0.008439648896455765
    epoch number 7 | batch number 1675 | generator loss = 7.070625305175781 | discriminator loss = 0.25249427556991577


     80%|████████  | 8/10 [06:40<01:39, 49.86s/it]

    epoch number 8 | batch number 0 | generator loss = 4.203941822052002 | discriminator loss = 0.18343289196491241
    epoch number 8 | batch number 200 | generator loss = 2.7548460960388184 | discriminator loss = 0.017191078513860703
    epoch number 8 | batch number 400 | generator loss = 5.153848171234131 | discriminator loss = 0.2126798778772354
    epoch number 8 | batch number 600 | generator loss = 2.4082131385803223 | discriminator loss = 0.7340734004974365
    epoch number 8 | batch number 800 | generator loss = 1.9588088989257812 | discriminator loss = 0.7638360857963562
    epoch number 8 | batch number 1000 | generator loss = 3.1427531242370605 | discriminator loss = 0.04076611250638962
    epoch number 8 | batch number 1200 | generator loss = 9.426302909851074 | discriminator loss = 0.0671580359339714
    epoch number 8 | batch number 1400 | generator loss = 4.568195343017578 | discriminator loss = 0.2781957983970642
    epoch number 8 | batch number 1600 | generator loss = 3.1912214756011963 | discriminator loss = 0.04164225980639458
    epoch number 8 | batch number 1800 | generator loss = 4.669330596923828 | discriminator loss = 0.0010130235459655523


     90%|█████████ | 9/10 [07:28<00:49, 49.38s/it]

    epoch number 9 | batch number 125 | generator loss = 2.847745895385742 | discriminator loss = 0.2367047667503357
    epoch number 9 | batch number 325 | generator loss = 8.497081756591797 | discriminator loss = 0.6592368483543396
    epoch number 9 | batch number 525 | generator loss = 5.124856948852539 | discriminator loss = 0.05494079366326332
    epoch number 9 | batch number 725 | generator loss = 2.808432102203369 | discriminator loss = 0.08962322771549225
    epoch number 9 | batch number 925 | generator loss = 3.5111680030822754 | discriminator loss = 0.177422434091568
    epoch number 9 | batch number 1125 | generator loss = 4.133440017700195 | discriminator loss = 0.12160167098045349
    epoch number 9 | batch number 1325 | generator loss = 6.491473197937012 | discriminator loss = 0.011363385245203972
    epoch number 9 | batch number 1525 | generator loss = 1.895836591720581 | discriminator loss = 0.25524279475212097
    epoch number 9 | batch number 1725 | generator loss = 3.693697690963745 | discriminator loss = 0.03281675651669502


    100%|██████████| 10/10 [08:16<00:00, 49.69s/it]



## 강의_3기_AI응용_9차시__NeRF_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_9차시__NeRF_.ipynb)

# 9장 NeRF
This is a PyTorch implementation based on the paper: https://arxiv.org/abs/2003.08934. The code takes mostly after the officially tiny nerf implementation: https://colab.research.google.com/github/bmild/nerf/blob/master/tiny_nerf.ipynb

![image.png](data:image/png;base64,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)

## Imports + Data



```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.nn.init as init
import time
import numpy as np
import torch.nn.functional as F
import os
from tqdm import tqdm
from ipywidgets import interactive, widgets


device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
# if not os.path.exists('tiny_nerf_data.npz'):
#     !wget http://cseweb.ucsd.edu/~viscomp/projects/LF/papers/ECCV20/nerf/tiny_nerf_data.npz
```

## Encoding + Model

![nerf_arch.PNG](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnIAAAD+CAYAAAC+w+gfAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAADh4SURBVHhe7d0HnOR1ff9xkjxMVGJAUbHQUXoT6e1A2lGUcvR2Rz/q3XHHHSoKRo0tRLBgix0sqNgrSkRUUCmKJvlboomamGhssWvC9z/f3+0MM3Ov3WP39rX8bnx/H4/nw2nra2f3O7/77MzsskbJysrKysrKyspaLVcGuaysrKysrKys1XRlkMvKysrKysrKWk3XpAa5e++9NyIiIiIeALQyyEXEtPraHy6bEdSOiBhltDLIRcS0oqHLQO2IiFFGK4NcREwrGroM1I6IGGW0MshFxLSioctA7YiIUUYrg1xETCsausbzsW/ML6983zF4Xb/33HlGuf7WUwcuo3ZExCijlUEuIqZV/7A1kXt+u6yc+4w98Dqy7Kr9y+f+a2HvPLUjIkYZrQxyETGt+oevibzkuiPKdZ8ZfJZtIrf+YEG58Mq9e+epHRExymhlkIuIadU/fH3pZ4vLm24+udz5iyW9y+74+eLmfw8/eevy1d8vv+z2Hy8qV99wVLnmXUeXd94+r3zlN0vLS9+5/PzN/3pB72MPOGrz3mlqR0SMMloZ5CJiWnUHrZv+5fyy/5GblaPmbVd233+j8uVfLy2f/+HCcv1nT2uuf/Je6/due+f/LCmv/cjxZa1HPLh51u3uX11attvlceXlN85pPqZ7u6c87Ynllu9f1JymdkTEKKOVQS4iplV36Hru6w4t9/xuWXP6o1+fX17z4eMb9Xwd6mYd9oTebbve+MmTykP/8s/LIcdvWW74wrwVrj998a7l3Xec3pymdkTEKKOVQS4iptXw8NV15atnl7//+AnN6fEGueqwE7cqa6/zkGb4G77ujCW7Nb/BWk9TOyJilNHKIBcR02p4+Oo6+cKdeu+Pq3ba+76XVrvqs3gveOPhZd6iXcomW6xTbv/vRQPXHzRni7y0GhF/tGhlkIuIadU/ePV7/usPGzh/xGnb9n7Z4ePfnF+OPn37su56Dyu3/Whhc76+xFrfR/eK9973d+bqL0h0T1M7ImKU0cogFxHTqjto9au/vHDFq2YPXHbV245s3hPXf9lEPv29i8qC587qnad2RMQoo5VBLiKmVf/w1fXmfzi5vP3zcwcuq38Q+OzLdh+4bCJLXrRf82xd9zy1IyJGGa0MchExrfqHr64b7zqj9xus/epLqPVPjAxfPqz+bbnuny3ponZExCijlUEuIqZV/7BlonZExCijlUEuIqYVDV0GakdEjDJaGeQiYlrR0GWgdkTEKKOVQS4iphUNXQZqR0SMMloZ5CJiWtHQZaB2RMQoo5VBLiKmFQ1dBmpHRIwyWhnkImJa0dBloHZExCijlUEuIqYVDV0GakdEjDJaGeQiYlrR0GWgdkTEKKOVQS4iphUNXQZqR0SMMloZ5CJiWtHQRT757fPL1TccVT72jfnN+frfXn3hm59aXvDGw8tdv7x0hdsPo3ZExCijlUEuIqYVDV3DrnrbkWXeJbuWL/96ae+yUy7aqfnvqf7Ddy8sR5y27cDtCbUjIkYZrQxyETGtaOjq97bPnVZ2nrXBwH9E/3P/tbA8bsO1euefvNf65YNfO7t3nlA7ImKU0cogFxHTioaufnsdvEk58bwdy/nP3qtc+pKnNAPdaz9yfNlmp8f2bnPI8VuWv73+iIGPG0btiIhRRiuDXERMKxq6+j1kzQeVD//zueWrv7+s7L7/RuXZ184u17z76LLbUzbq3ebQE7Yqz37lwQMfN4zaERGjjFYGuYiYVjR09XvQn/9Z+dLPFjenn/u6Q8tR87Yr77ht7sAzcvscuml5xXuP6Z0n1I6IGGW0MshFxLSioatffRbu+ltPbU4///WHlae/9IDm5dWNN1+n3P2r5b+tusX265bbf7xo4OOGUTsiYpTRyiAXEdOKhq5+9ZcY6kun133m1HL+s/Yqd/5iSXP5qz54XDnv8j3LM1920ErfH1dROyJilNHKIBcR04qGrmH1b8bd9qOFK1xeX3K94+fLX3ZdGWpHRIwyWhnkImJa0dBloHZExCijlUEuIqYVDV0GakdEjDJaGeQiYlrR0GWgdkTEKKOVQS4iphUNXQZqR0SMMloZ5CJiWtHQZaB2RMQoo5VBLiKmFQ1dBmpHRIwyWhnkImJa0dBloHbESHlWZ5/PBGpHK9HKIBcREdFGNHQZqB2tRCuDXERERBvR0GWgdrQSrQxyERERbURDF/jD5cvKu489qly8y07llG23HnDadtuUfzrvbPy4HmpHK9HKIBcRD6jvfe97ZenSpXhdxB81GrqG/HTponLQJhuXbR79qHL+TjuW/TfeqKyxxhrlhK23LJfvvUd5zr57l58vuwQ/tofa0Uq0MshFxAPqu9/9blm8eDFeF/FHjYauPr975tKyw2PWLUv32K38X9/l+220YTl3xx0Gbjshakcr0cogFxEPqAxyEeOgoavPiw/Yr2z1qEcODHHVss5gt9vjHzdw2YSoHa1EK4NcRDygMshFjIOGrj7rrrlmueqg/Ve4/MRttionb7v1CpePi9rRSrQyyEXEjPrWt75V5syZ03PooYeWzTbbbOCyq6++Gj824o8KDV1jvnPxec174b554fyBy//38mVlw7XWKtfMPnDg8glRO1qJVga5iHhA5Rm5iHHQ0DWm/iZqHeR++4xLBy6/8bijm0Fupb/g0I/a0Uq0MshFxAMqg1zEOGjoGlP/5MgmD1+7fHX+Wb3L6rN09bdXbz7tpIHbrhS1o5VoZZCLiAdUBrmIcdDQ1ef2M+eWY7bconz4xOPKy2Yf2Lwv7p/PPwdvOyFqRyvRyiAXEQ+oH/zgB+WFL3whXhfxR42GriH1PXF1ePvZ0kV4/f1C7WglWhnkIiIi2oiGLgO1o5VoZZCLiIiIWA3QyiAXERERsRqglUEuIiIiYjVAK4Ncx6X/ODOobaG+gdoW6huobaG+gdoW6huobaC2gdoW6huobaG+gdoW6huoHe1EK4NcB21sA7Ut1DdQ20J9A7Ut1DdQ20J9A7UN1DZQ20J9A7Ut1DdQ20J9A7WjnWhlkOugjW2gtoX6BmpbqG+gtoX6BmpbqG+gtoHaBmpbqG+gtoX6BmpbqG+gdrQTrQxyHbSxDdS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdSOdqKVQa6DNraB2hbqG6htob6B2hbqG6htob6B2gZqG6htob6B2hbqG6htob6B2tFOtDLIddDGNlDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1A72olWBrkO2tgGaluob6C2hfoGaluob6C2hfoGahuobaC2hfoGaluob6C2hfoGakc70cog10Eb20BtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30DtaCdaGeQ6aGMbqG2hvoHaFuobqG2hvoHaFuobqG2gtoHaFuobqG2hvoHaFuobqB3tRCuDXAdtbAO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1o51oZZDroI1toLaF+gZqW6hvoLaF+gZqW6hvoLaB2gZqW6hvoLaF+gZqW6hvoHa0E60Mch20sQ3UtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UjnailUGugza2gdoW6huobaG+gdoW6huobaG+gdoGahuobaG+gdoW6huobaG+gdrRTrQyyHXQxjZQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQO9qJVga5DtrYBmpbqG+gtoX6BmpbqG+gtoX6BmobqG2gtoX6BmpbqG+gtoX6BmpHO9HKINdBG9tAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9A7WgnWhnkOmhjG6htob6B2hbqG6htob6B2hbqG6htoLaB2hbqG6htob6B2hbqG6gd7UQrg1wHbWwDtS3UN1DbQn0DtS3UN1DbQn0DtQ3UNlDbQn0DtS3UN1DbQn0DtaOdaGWQ66CNbaC2hfoGaluob6C2hfoGaluob6C2gdoGaluob6C2hfoGaluob6B2tBOtDHIdtLEN1LZQ30BtC/UN1LZQ30BtC/UN1DZQ20BtC/UN1LZQ30BtC/UN1I52opVBroM2toHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHa0U60Msh10MY2UNtCfQO1LdQ3UNtCfQO1LdQ3UNtAbQO1LdQ3UNtCfQO1LdQ3UDvaiVYGuQ7a2AZqW6hvoLaF+gZqW6hvoLaF+gZqG6htoLaF+gZqW6hvoLaF+gZqRzvRyiDXQRvbQG0L9Q3UtlDfQG0L9Q3UtlDfQG0DtQ3UtlDfQG0L9Q3UtlDfQO1oJ1oZ5DpoYxuobaG+gdoW6huobaG+gdoW6huobaC2gdoW6huobaG+gdoW6huoHe1EK4NcB21sA7Ut1DdQ20J9A7Ut1DdQ20J9A7UN1DZQ20J9A7Ut1DdQ20J9A7WjnWhlkOugjW2gtoX6BmpbqG+gtoX6BmpbqG+gtoHaBmpbqG+gtoX6BmpbqG+gdrQTrQxyHbSxDdS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdSOdqKVQa6DNraB2hbqG6htob6B2hbqG6htob6B2gZqG6htob6B2hbqG6htob6B2tFOtDLIddDGNlDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1A72olWBrkO2tgGaluob6C2hfoGaluob6C2hfoGahuobaC2hfoGaluob6C2hfoGakc70cog10Eb20BtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30DtaCdaGeQ6aGMbqG2hvoHaFuobqG2hvoHaFuobqG2gtoHaFuobqG2hvoHaFuobqB3tRCuDXAdtbAO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1o51oZZDroI1toLaF+gZqW6hvoLaF+gZqW6hvoLaB2gZqW6hvoLaF+gZqW6hvoHa0E60Mch20sQ3UtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UtlDfQO1RQCuDXAdtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UHsU0Mog10GbwEBtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30BtC/UN1B4FtDLIddAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtUcBrQxyHbQJDNS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdS2UN9A7VFAK4NcB20CA7Ut1DdQ20J9A7Ut1DdQ20J9A7UN1DZQ20J9A7Ut1DdQ20J9A7Ut1DdQexTQyiDXQZvAQG0L9Q3UtlDfQG0L9Q3UtlDfQG0DtQ3UtlDfQG0L9Q3UtlDfQG0L9Q3UHgW0Msh10CYwUNtCfQO1LdQ3UNtCfQO1LdQ3UNtAbQO1LdQ3UNtCfQO1LdQ3UNtCfQO1RwGtDHIdtAkM1LZQ30BtC/UN1LZQ30BtC/UN1DZQ20BtC/UN1LZQ30BtC/UN1LZQ30DtUUArg1wHbQIDtS3UN1DbQn0DtS3UN1DbQn0DtQ3UNlDbQn0DtS3UN1DbQn0DtS3UN1B7FNDKINdBm8BAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9AbQv1DdQeBbQyyHXQJjBQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQ20J9A7VHAa0Mch20CQzUtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UtlDfQO1RQCuDXAdtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UHsU0Jr0IPe1P1w2I4Y/eRNtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UHsU0Mog10GbwEBtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30BtC/UN1B4FtDLIddAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtUcBrQxyHbQJDNS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdS2UN9A7VFASx3kPvaN+eWV7zsGr+v3njvPKNffeurAZcOfvIk2gYHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHaFuobqD0KaGmD3D2/XVbOfcYeeB1ZdtX+5XP/tbB3fviTN9EmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtUcBLW2Qe8l1R5TrPjP4LNtEbv3BgnLhlXv3zg9/8ibaBAZqW6hvoLaF+gZqW6hvoLaF+gZqG6htoLaF+gZqW6hvoLaF+gZqW6hvoPYooLVKg9wt37+oXP/Z08pXf3/fZXf8fHHzv4efvHXv8tt/vKhcfcNR5Zp3HV3eefu88pXfLC0vfefy8zf/6wW9jz3gqM17p4c/eRNtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UFvxrM68MhPGerSmPMi99iPHl4PmbFEOPnaLctqCnZvL6vvcbvvR8pdHn7zX+r3b3vk/S5rbr/WIBzfPut39q0vLdrs8rrz8xjnl8z+87+XUpzztic1wWE/3vkgzgDaBgdoW6huobaG+gdoW6huobaG+gdoGahuobaG+gdoW6huobaG+gdoW6huoraChyzDWozXlQe7KV8/unX7xW5/WDGR1WKvnv/zrpWXWYU/oXd/1xk+eVB76l39eDjl+y3LDF+atcP3pi3ct777j9OZ074s0A2gTGKhtob6B2hbqG6htob6B2hbqG6htoLaB2hbqG6htob6B2hbqG6htob6B2goaugxjPVrT8h65+izcgufNKp/41nnN+fEGueqwE7cqa6/zkPLRr89f4bozluzW/AZrPd37Is0A2gQGaluob6C2hfoGaluob6C2hfoGahuobaC2hfoGaluob6C2hfoGaluob6C2goYuw1iP1rT9ssOcM7YfOL/T3ve9tNr13NcdWl7wxsPLvEW7lE22WKfc/t+LBq6vL9XmpdXpQX0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtRU0dBnGerSmZZCrf2rkhW9+6sBlR5y2be+XHT7+zfnl6NO3L+uu97Dm2bt6vr7EWt9H94r33vd35uovSHRP975IM4A2gYHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHaFuobqK2gocsw1qM1LYNc/TMjN3xx8D1vV73tyOY9cf2XTeTT37uoLHjurN753hdpBtAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtRU0dBnGerSmZZCrf8y3/kmR/svqs3RnX7b7wGUTWfKi/Xq/8Vr1vkgzgDaBgdoW6huobaG+gdoW6huobaG+gdoGahuobaG+gdoW6huobaG+gdoW6huoraChyzDWozUtg9y7vrT8N02H1ZdQ658Yoev61b8tV/8eXf9lvS/SDKBNYKC2hfoGaluob6C2hfoGaluob6C2gdoGaluob6C2hfoGaluob6C2hfoGaito6DKM9WhN2y87TLfeF2mKfvKTn+DlhDaBgdqT9e1vfxsvH0Z9A7Uno36f7u/3ivoGak/G/f0eVdQ3UHsy/pjvE7UN1J6sHB981J6Un+f4MBOoPRn3+z7R0GUY69Ea2UHuDW94Q5k1a1a5+eab8fp+K2yCr/1fOfwl15fd519e5r77zoHrjnv9TeXAZ19bDrry1WXJPX/oXb7kq/9bjnntR8sxr/7wwO37UXuy6n2aO3fuSjcZ9Rfe8Yuy37Kryt4XP7ec/5kfDFx36Ave3Nyvo17+3oHL53/q38oR17y7nP3xbw1c3kXtyagH6Q033LBcccUVKz1gD7cnuj/jfZ/qxxx5zXvKqe/8wsDt+1F7Muqeq/ep7kG6vt9w+9ybvlP2OP+KcuCzXlku+fJvB66b6veoovZk1O/PTD6eZuL7tCqPpZOuu7Xsdu4zV/heXHz7T5v7Uw1/7qfe8MVy1Cve17nNTwYu76L2ZE31PrX1sbQqx4e2Ppbu/V7nMfSmDcu9/zT540M13v2aaO/Zx/FVOj6MqfvsjA/+432XjXPcuOjz/91cXp138/fuu/0Qak9GfQzdr+P42KD1LxfNL689/JBy7aEHl9d1/vcDJxxTfv30JYPDWMdn5p1SXn7IQc3t6m2+cObc5vLPn3Fac9mrDptdXv/UQ8u7jz2q/Gzpovs+dqxHa2QHuap+E9ZYY42VbrDhDXDo37ypHHD5K8r+z3xZ+YuHrV3O/NA/NZfXB8q2R5/RHMDr9d3bL/jCz8qWh55YTnvXHb3LCLUnq96Pep+qiQ7Y1K8PiKe+5G3lyacuKGuvv2lZfM/vm8tPfPOny06nLWruV/8g+rSr3lF2Pn1JWfyV3/UuG0btyaoHgXp/1lprrQkP2MPt8e7PeN+n0993T9nysJPKBbf+Z+8yQu3Jqnuu3qeVHQj6u4vu/FV50onnlyOuflfZaI+DytZHnNa7blW+RxW1J6N+T+r3ZyYeTzP1fZrqY2nue+5qPuf6D8na621SZj/v9b3r6v2o11Xd+1ntcsal5bAXvqV3nlB7sqZ6n9r8WJrK8aHNj6XGe2aVe1++xkoHuuH2RPdrvL03E8fxVTk+VKe//6tl3a12LEdf+4HeZeMdNzaffVy55O7fND9UbDLrsN7th1F7supjqN6nCY/j3UGr49Lddy3n77Rj+eVli8tz9t27bL/uo8tvn3Fp7/qFu+5crj74gPJ/Y+fr8HbSNlv1rn/yYx9T3jHnyPK/ly8rN51yQtnk4WuXb144f/n1Yz1aIz3I1S9896A20QYb3gBnf+ybvdPbH3tOmf3cv29O73XRc8ohf/PG5ifR7vXVpvs+tXk2rv8yMtydqu6Q0EUH7BX6nZ9u+n8ae/hGm/XO1yH0hDfd3Dyr2L3+lLffVtbfed+By0h/c6r6DwLVeAfsgfYE94e+T3XYfuQTt1nh2QbS35yq/n9Qq/EOBP3d+Td/tzlA1dPnf/rfy8Mes37vulX5HlXD3ano/oPaZTyeZvr7NJXHUv/9qcPc1k87tTldP/cnHnBUM+R0r6/2W/q3ZdezOgf5vstIf3NVTPo+tfyxNJXjQ9sfS82zcnWQ6xpnoBtuj3e/xtt7M3kcn+rxoav+wNA/yI133HjExpuX8/7h+82+Xe/Je/duM2y4OxX1cdN/n/A4PjaEVVfss1dZvNsuzemfXLqw+Zh7zj2zOf/OzoC29wbrD9y++tSpJ/ZOz9pwg3LjcUf3zh/+xCeUFx+w3/LzYz1arR/k6hetbpCp6j8AdA1vMNoEXfUnnrM+8vXmdD0gb7THgeWvHrdhmXvj3c1l9YGy5iMfUw55/hs6Pyld0Pxk0f/x/bq9ujnoc72/uj8lDOs/YFO/33o77tU8uBd88edl53mLy6M227ast9M+zU/g9fqN95rd3J89L7iiud/jHQi696l+Pelzvb+G//Gphg/Y1O/q3p96mr5P+1zygrLBrk8p+z/96uan04tu+/HAx/fr3qdV3XvdZ4T7DR8IqF+d9dFv3DcgrOL3qOr26PO8v5YtW1b+4i/+YoX7NJ2Pp8l+nx7ox9LBz3lt7x+Yee/9Stnh+PllzUc9tux4ysXNZfWlr/pswv7PuKb5HtaXVvs/vl/367eqj6VVvU9tfCytyvHBeizde/sVq6YOb/3DHAx01O/qv1+096rJHMdX9bG0qseHbeecOTDI9es/btSX+B++wRPKnhde2Tw7Pnzbrm6v//HU/3n0f+7dy/q/Bt3jND2eBo7jY0NX1T/I1ZdJt+t7Ru7gTTdunqXr3rY+6/Y/yy5pdF+CrYNcfUbuD53rPnv6qWW9v3pYufucM5Z/zNjnSKv1g9yCBQuajTBVa6+99grfhO4BoNugTVDVqb++5DB8eX0J4rHb7dqc3nfJi8tWh5/cnD7xLbc0PyF1X5YY1u3ddddd+LneX7vuuusK96mq13U3KvW76vtChv9BqQ/wHU44r+x65rLm/IMesubyB07np54Ndz+gHHTFqwZu39W9T3VTD3+ek7H55pvjfbo///jQ/an6v0/1KfiDn/Oa5nR9lmGLQ08YuG2/7n1a1b237rrrrnB/7u8/PvXAe+4n/3Xgsql+j6rufaLPczIe/OAHr3Cf7u9wen8eT5P9Pj2Qj6X6/dj+uHMH3jdW1WdHHrPNzuWY13ykeV9cfaly0V2/bt7bU3/oO+MDXxu4fVf367eqj6VVuU9tfSytyvHBeiw1L4+uitevu+Ig95q1lg95v1n5D690v/r3Xj0/meP4qj6WqlU5Pow3yA0fN86/5T/KVk89pTzk4Y8sx/39JwZu26/b63889X8e/Z9397L+r0Hds/WyiX4wao7jY4NZVQe5w564aTlxm63KUzd7QvlV33vktn30o8pVB+3fO1+ve+5++5S1OsPvP59/TnNZHeTqS7Mvm31gOXW7bcp+G23YvPeu+Zixz5HWSL+0Wg9a/V/44X9Eu2gT1PcT7LPob8YdyupPqfV/917wvOan0u7ldZCrbyztnu/X31wVwxurbrr+nzQq6lf1qfn6Ew1dVw8Cmx90THP6zx70572XU+ozDvVp7/7bdvU3V8Xws1f9B+gu6k90f6ru96n+75xrP9icri8b1fc29d+uX39zqurn3n9/JrP36ss+x7/hk3jdVL5HVX9zqupBsP8+DR+gu6h/fx9PM/19WpXHUt13df/RdUe/8v3Ne3tOuv6z5TFb79S7vD6DUt9o33/brv7mqpjqfWrrY6ma6vGhrY+l5jdXJxjguqhfTXS/unuvnp7J4/iqHB8qGuTouLHhbvs3Pxgd/8ZPlYc+4tHN97H/Y7qGu1MxfByvVth7Y4NZ1X1G7kdLFpQNO8f87i8yVMdvvWU5Y4ftBm5f3yO3+TqP6J0ffmn17B13KAdtsvHy82M9WiM9yNUDWP3Cj/ePaNfwBqg/YT/lspeWBV/6n+b8OR//l4Hr66aqbyitp+tvr9U3nXave+y2u6z0GblV0b+x6ADdRf0Lbv2vgZ/Ihu9XPSh3D+T1p7eTr/9cc7q+R6a+jNJ/2y5qT1b/AYAO0F3D7ZXdn/7vU/1tvL0XPr85XX/rq76fpP+2/ag9Wd1/TCe79+pvm3V/mq4vyw3/VtZUvkcVtSer+4/peAforuH2ZB5PM/l9WpXHUn0DeffN13UAGn4jeX2jdn2bxcI7f1n+6rEbNP/w1Mu3Per03kuUw6g9WVO9T21+LE31+NDmx9K9N3X+gZ9ggOui/sruV3fv1dMzeRyf6vGha3iQo+NGfRzVX4ro3maLQ44feC9dP2pPVvc4PuHeGxu6qv6XVusvK2zWGdJ+Ovabp3eefXp5+IMfXL674ILe7Vc2yNX/r9mbbrL8/FiP1sgOcvUAtrJ/RLuGN8BmB84pa623cXnkE7Yuj9h4i+aNyvWNpfV0fV2+bq4LP/vD3u3rM3L1QVIfQPafH6mbaaIDdNdwu/522TqbbtXcp2qtx29U5rzqQ+XIl91YHv+kPcusxS9aflD72v81t6//SNU3BddnFOqvunf/IRpG7cmqD/yJDtBd/d3x7s9436f6U2n9vtaf4upPePUg3v//14/ak1Hvx1T2Xv1a15feuvfpYeuu17z/aFW/RxW1J6MemFd2gO4abk/m8TST36epPpbqP4b1mYB6f+oe3GCX/ZrLd5p7SfMyY/0zHvVZke7tn/Z37yy7nLm0eRmo3tfu5cOoPVlTuU9tfixVUzk+tPmx1Dwbt5IBrmu4Pd79Gm/vzdRxfFWOD9U5n/h2efwOezTHhu7gRseNenl9Faw+q13fyjTrkhcO/P/0o/Zk1P22sh8eGmND13cuPq95H9xe669XvnHBuc1ly/bYreyx3uOboa6e//CJxzWD2VuPfGq5Ze7JzW+5XrDTjs11d5w1rzzuYX/ZvCz7ikMOKk/fc/fm/+/rY/9f3R4tZZD70s8Wl2vedXR5x21ze5e99iPHl+e9/rDyqe9cMHDb8fS+SFNUX+te2T+iXbQJSH0Kd7w39ta/DTX8Xplh1J6slR2gu6g/nvrTeH3mYPjyen/G+5tXXdSejPoAWdkBuov6ZKLv04Wf+xFe3o/ak2HsvVX5HlXUnoz7u+8q6pMH+vs07Y+lzlBQhx96Rr7+2Qj6/vWj9mRN9316oL9HxvHhgX4s3fvDu1Y6wHVRH02w92biOG4cHyZSv391b9J1XdSejHqf7tfeq0PWJH1/4YXlWxfOL7/p+9MkKzXWozXtg9x7v3xmOezErcpn/v3i3mV1qLvkBfuWe363rOx/5Gblzl8sGfgY0vsizQDaBAZqW6hvoLaF+gZqW6hvoLaF+gZqG6htoLaF+gZqW6hvoLaF+gZqW6hvoLaChi7DWI/WtA5yt/94UXni1o8qt3z/ooHLt9xh3fKR/3duc/rcZ+xRnn3t7IHrSe+LNANoExiobaG+gdoW6huobaG+gdoW6huobaC2gdoW6huobaG+gdoW6huobaG+gdoKGroMYz1a0zrILfqbfcuu+21Ynv7SA8q8S3Ytn//hwnLXLy8tf/Ina5Q7fr64uU0d4o4750krfOyw3hdpBtAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtRU0dBnGerSmdZDb59BNy5WvXv5s24VX7l0OOX7LctuPFpY//bM/6d3milfNLrOP27J3fjy9L9IMoE1goLaF+gZqW6hvoLaF+gZqW6hvoLaB2gZqW6hvoLaF+gZqW6hvoLaF+gZqK2joMoz1aE3rILf7ARuVa99/bHP6Y9+YX9bbeO3m9EPWfFDvGbklL9qvzF24S+9jxtP7Is0A2gQGaluob6C2hfoGaluob6C2hfoGahuobaC2hfoGaluob6C2hfoGaluob6C2goYuw1iP1rQOchf/9T5lwfNmNac/8a3zml9sqKcPP2nr8pZPn9KcPmruduVNnzqp9zHj6X2RZgBtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UFtBQ5dhrEdrWge5+mdHDjx68/KGm04sC5+/b/OsXL28DnXHnrVDeek7jyrnXb7nCh9Hel+kGUCbwEBtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30BtC/UN1FbQ0GUY69Ga1kGu67P/uWCFy77ym6XNLz8MXz6e3hdpBtAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtRU0dBnGerSUQW469L5IM4A2gYHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHaFuobqK2gocsw1qOVQa6DNoGB2hbqG6htob6B2hbqG6htob6B2gZqG6htob6B2hbqG6htob6B2hbqG6g9CmhlkOugTWCgtoX6BmpbqG+gtoX6BmpbqG+gtoHaBmpbqG+gtoX6BmpbqG+gtoX6BmqPAloZ5DpoExiobaG+gdoW6huobaG+gdoW6huobaC2gdoW6huobaG+gdoW6huobaG+gdqjgFYGuQ7aBAZqW6hvoLaF+gZqW6hvoLaF+gZqG6htoLaF+gZqW6hvoLaF+gZqW6hvoPYooJVBroM2gYHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHaFuobqD0KaGWQ66BNYKC2hfoGaluob6C2hfoGaluob6C2gdoGaluob6C2hfoGaluob6C2hfoGao8CWhnkOmgTGKhtob6B2hbqG6htob6B2hbqG6htoLaB2hbqG6htob6B2hbqG6htob6B2qOA1qQHuVFEm8BAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9AbQv1DdQeBbQyyHXQJjBQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQ20J9A7VHAa0Mch20CQzUtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UtlDfQO1RQCuDXAdtAgO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1LdQ3UHsU0Mog10GbwEBtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30BtC/UN1B4FtDLIddAmMFDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1DbQn0DtUcBrQxyHbQJDNS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdS2UN9A7VFAK4NcB20CA7Ut1DdQ20J9A7Ut1DdQ20J9A7UN1DZQ20J9A7Ut1DdQ20J9A7Ut1DdQexTQyiDXQZvAQG0L9Q3UtlDfQG0L9Q3UtlDfQG0DtQ3UtlDfQG0L9Q3UtlDfQG0L9Q3UHgW0Msh10CYwUNtCfQO1LdQ3UNtCfQO1LdQ3UNtAbQO1LdQ3UNtCfQO1LdQ3UNtCfQO1RwGtDHIdtAkM1LZQ30BtC/UN1LZQ30BtC/UN1DZQ20BtC/UN1LZQ30BtC/UN1LZQ30DtUUArg1wHbQIDtS3UN1DbQn0DtS3UN1DbQn0DtQ3UNlDbQn0DtS3UN1DbQn0DtS3UN1B7FNDKINdBm8BAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9AbQv1DdQeBbQyyHXQJjBQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQ20J9A7VHAa0Mch20CQzUtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UjnailUGugza2gdoW6huobaG+gdoW6huobaG+gdoGahuobaG+gdoW6huobaG+gdrRTrQyyHXQxjZQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQO9qJVga5DtrYBmpbqG+gtoX6BmpbqG+gtoX6BmobqG2gtoX6BmpbqG+gtoX6BmpHO9HKINdBG9tAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9A7WgnWhnkOmhjG6htob6B2hbqG6htob6B2hbqG6htoLaB2hbqG6htob6B2hbqG6gd7UQrg1wHbWwDtS3UN1DbQn0DtS3UN1DbQn0DtQ3UNlDbQn0DtS3UN1DbQn0DtaOdaGWQ66CNbaC2hfoGaluob6C2hfoGaluob6C2gdoGaluob6C2hfoGaluob6B2tBOtDHIdtLEN1LZQ30BtC/UN1LZQ30BtC/UN1DZQ20BtC/UN1LZQ30BtC/UN1I52opVBroM2toHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHa0U60Msh10MY2UNtCfQO1LdQ3UNtCfQO1LdQ3UNtAbQO1LdQ3UNtCfQO1LdQ3UDvaiVYGuQ7a2AZqW6hvoLaF+gZqW6hvoLaF+gZqG6htoLaF+gZqW6hvoLaF+gZqRzvRyiDXQRvbQG0L9Q3UtlDfQG0L9Q3UtlDfQG0DtQ3UtlDfQG0L9Q3UtlDfQO1oJ1oZ5DpoYxuobaG+gdoW6huobaG+gdoW6huobaC2gdoW6huobaG+gdoW6huoHe1EK4NcB21sA7Ut1DdQ20J9A7Ut1DdQ20J9A7UN1DZQ20J9A7Ut1DdQ20J9A7WjnWhlkOugjW2gtoX6BmpbqG+gtoX6BmpbqG+gtoHaBmpbqG+gtoX6BmpbqG+gdrQTrQxyHbSxDdS2UN9AbQv1DdS2UN9AbQv1DdQ2UNtAbQv1DdS2UN9AbQv1DdSOdqKVQa6DNraB2hbqG6htob6B2hbqG6htob6B2gZqG6htob6B2hbqG6htob6B2tFOtDLIddDGNlDbQn0DtS3UN1DbQn0DtS3UN1DbQG0DtS3UN1DbQn0DtS3UN1A72olWBrkO2tgGaluob6C2hfoGaluob6C2hfoGahuobaC2hfoGaluob6C2hfoGakc70cog10Eb20BtC/UN1LZQ30BtC/UN1LZQ30BtA7UN1LZQ30BtC/UN1LZQ30DtaCdaGeQ6aGMbqG2hvoHaFuobqG2hvoHaFuobqG2gtoHaFuobqG2hvoHaFuobqB3tRCuDXAdtbAO1LdQ3UNtCfQO1LdQ3UNtCfQO1DdQ2UNtCfQO1LdQ3UNtCfQO1o51oZZDroI1toLaF+gZqW6hvoLaF+gZqW6hvoLaB2gZqW6hvoLaF+gZqW6hvoHa0E60Mch20sQ3UtlDfQG0L9Q3UtlDfQG0L9Q3UNlDbQG0L9Q3UtlDfQG0L9Q3UjnailUGugza2gdoW6huobaG+gdoW6huobaG+gdoGahuobaG+gdoW6huobaG+gdrRTrQyyHXQxjZQ20J9A7Ut1DdQ20J9A7Ut1DdQ20BtA7Ut1DdQ20J9A7Ut1DdQO9qJVga5DtrYBmpbqG+gtoX6BmpbqG+gtoX6BmobqG2gtoX6BmpbqG+gtoX6BmpHO9HKINdBG9tAbQv1DdS2UN9AbQv1DdS2UN9AbQO1DdS2UN9AbQv1DdS2UN9A7WgnWhnkOmhjG6htob6B2hbqG6htob6B2hbqG6htoLaB2hbqG6htob6B2hbqG6gd7UQrg1wHbWwDtS3UN1DbQn0DtS3UN1DbQn0DtQ3UNlDbQn0DtS3UN1DbQn0DtaOdaGWQ66CNbaC2hfoGaluob6C2hfoGaluob6C2gdoGaluob6C2hfoGaluob6B2tBOtDHIdtLEN1LZQ30BtC/UN1LZQ30BtC/UN1DZQ20BtC/UN1LZQ30BtC/UN1I52opVBroM2toHaFuobqG2hvoHaFuobqG2hvoHaBmobqG2hvoHaFuobqG2hvoHa0U60Msh10MY2UNtCfQO1LdQ3UNtCfQO1LdQ3UNtAbQO1LdQ3UNtCfQO1LdQ3UDvaiVYGuYiIiIjVAK0MchERERGrAVoZ5CIiIiJWA7QyyEVERESsBmhlkIuIiBgB1113XfnQhz6E18VooJVBLiIiYgS85S1vKR/4wAfwuhgNtDLIRUREjIAMcqOPVga5iIiIEZBBbvTRyiAXERGxGnr/+99f5syZ07PzzjuXPffcc+Cym266CT82Vk+0MshFRESMgDwjN/poZZCLiIgYARnkRh+tDHIREREjIIPc6KOVQS4iImIE1PfM3XzzzXhdjAZaGeQiIiIiVgO0MshFRERErAZoZZCLiIiIWA3QyiAXERHRQl/7w2UzgtrRTrQyyEVERLQQDV3jecdtc8snvnXeCpff/t+Lyke/Pr/c8v2LmvM3fGHeCrejdrQTrQxyERERLdQ/bE3k09+7qDzrFQfjda/58PFlnXXXLGct3a132cLn71u+8pulvfPUjnailUEuIiKihbqD1sqcvWz38sWfXoLXVTvP2mBgkPvg184uz3nNIb3z1I52opVBLiIiooW6g1Z15y+WlJv/9YLe+a/+frl7freszDlj+4HbVv/w3QvL6z52QvnYN+avMMhVh5+0de80taOdaGWQi4iIaKHuoPXWW04pe8/epDxpj/XKZX93QHPZGz95Urnrl5eWG+86o5x68c6921ZLXrRf2WXfDZvr/vb6I8ojHv3QFQa5ev3dv7q0OU3taCdaGeQiIiJaqDt09b//7ZkvO6jc89tl5e8/fkJzvr4H7ulXH9i7/pPfPr/86Z/+SXn1h47rXbbF9uuuMMgdffr25eZ/u7A5Te1oJ1oZ5CIiIlqoO3TVl1C7p+v72579yoPLbT9a2Jy/9gPHlstfflDv+jd96qSyxhprlOs+c2rvMhrkjjvnSc3QV09TO9qJVga5iIiIFuofvLq+/Oul5cTzduydv+GL88q8S3btnf/sfy4oD1nzQeXFb31a77JNt3xkOfPSwUFuz4M2bt53V09TO9qJVga5iIiIFuofvLo+/8OF5eU3zumdr39G5Nizdhi4zSvfd0zZff+NmvfTnfP0PcrDH/XQsskW65R3fen03m0OPzm/7LA6opVBLiIiooW6g1a/a9519MBvr1ZnLNmt+cWH/suq7jNuX/jJJb3TVf0DwUv/dv/eeWpHO9HKIBcREdFC3UGr35IXP2WFyz7+zfnlr19739+FW5mL/3qfcsfPF/fOUzvaiVYGuYiIiBbqH7663veVs/Dy+jfj6D/RNeztn59b3nv3mQOXUTvaiVYGuYiIiBbqH7ZM1I52opVBLiIiooVo6DJQO9qJVga5iIiIFqKhy0DtaCdaGeQiIiJaiIYuA7WjnWhlkIuIiGghGrr6felni5s/I1J/C/WW71+0wvXvvuP03n/KayLUjnailUEuIiKihWjo6nfuM/YoL7nuiHLKRTuV9TdZu/njwN3r6p8X2Xbnx5aFz9934GMItaOdaGWQi4iIaCEaurrqf3/1Y9+Y3zu/0RMfMXB+yYv2KxdeuXcGuRFDK4NcREREC9HQNZ4d91yv3PO7Zc3p1330hHL9Z08ry67aP4PciKGVQS4iIqKFaOgiL3vPnN5/f/XWHywoV7xqdnM6g9zooZVBLiIiooVo6Br2qe9c0BvcqvrfXd151gZlt6ds1LzcusGmDy9Xvf3IgY8ZRu1oJ1oZ5CIiIlqIhq5+t/7HxeXZ1943xNX/5urdv7q0fPGnlzQuecG+5YIr9i5f/vV9vwRBqB3tRCuDXERERAvR0NX1mX+/uGy65SPLE7Za7vEbrlWu/cCxA7fJS6ujh1YGuYiIiBaioctA7WgnWhnkIiIiWoiGLgO1o51oZZCLiIhoIRq6DNSOdqKVQS4iIiJiNUBrUoNcVlZWVlZWVlZWe1YGuaysrKysrKys1XRlkMvKysrKysrKWk1XBrmsrKysrKysrNV0ZZDLysrKysrKylpNVwa5rKysrKysrKzVdGWQy8rKysrKyspaLVcp/x82eorpuAUM9QAAAABJRU5ErkJggg==)

$$\gamma(p) = (\sin(2^0\pi p), \cos(2^0\pi p), \dots, \sin(2^{L-1}\pi p), \cos(2^{L-1}\pi p))$$


```python
def encoding(x, L=10):
  res = [x]
  for i in range(L):
    for fn in [torch.sin, torch.cos]:
      res.append(fn(2 ** i * torch.pi * x))
  return torch.cat(res,dim=-1)
```


```python
x = torch.Tensor([3.1,5.6,7.3]) # x, y, z
y = encoding(x,L=4)
y
```




    tensor([ 3.1000,  5.6000,  7.3000, -0.3090, -0.9511, -0.8090, -0.9511,  0.3090,
            -0.5878,  0.5878, -0.5878,  0.9511,  0.8090, -0.8090, -0.3090,  0.9511,
             0.9511, -0.5878,  0.3090,  0.3090, -0.8090,  0.5878,  0.5878,  0.9511,
            -0.8090, -0.8090,  0.3090])




```python
class NeRF(nn.Module):
  def __init__(self, pos_enc_dim=63, view_enc_dim=27, hidden=256) -> None:
     super().__init__()

     self.linear1 = nn.Sequential(nn.Linear(pos_enc_dim,hidden),nn.ReLU())

     self.pre_skip_linear = nn.Sequential()
     for _ in range(4):
      self.pre_skip_linear.append(nn.Linear(hidden,hidden))
      self.pre_skip_linear.append(nn.ReLU())

     self.linear_skip = nn.Sequential(nn.Linear(pos_enc_dim+hidden,hidden),nn.ReLU())

     self.post_skip_linear = nn.Sequential()
     for _ in range(2):
      self.post_skip_linear.append(nn.Linear(hidden,hidden))
      self.post_skip_linear.append(nn.ReLU())

     self.density_layer = nn.Sequential(nn.Linear(hidden,1),nn.ReLU())

     self.linear2 = nn.Linear(hidden,hidden)

     self.color_linear1 = nn.Sequential(nn.Linear(hidden+view_enc_dim,hidden//2),nn.ReLU())
     self.color_linear2 = nn.Sequential(nn.Linear(hidden//2,3), nn.Sigmoid())

  def forward(self, input):

    positions = input[...,:3]
    view_dirs = input[...,3:]

    # Encode
    pos_enc = encoding(positions,L=10)
    view_enc = encoding(view_dirs,L=4)

    x = self.linear1(pos_enc)
    x = self.pre_skip_linear(x)

    # Skip connection
    x = torch.cat([x,pos_enc],dim=-1)
    x = self.linear_skip(x)

    x = self.post_skip_linear(x)

    # Density
    sigma = self.density_layer(x)

    x = self.linear2(x)

    # View Encoding
    x = torch.cat([x,view_enc],dim=-1)
    x = self.color_linear1(x)

    # Color Prediction
    rgb = self.color_linear2(x)

    return torch.cat([sigma,rgb],dim=-1)

```

## Get Ray + Render


```python
## Meshgrid
W = 3; H = 4; focal = 1
i, j = torch.meshgrid(
      torch.arange(W, dtype=torch.float32, device=device),
      torch.arange(H, dtype=torch.float32, device=device),
      indexing='xy' # ensures that i represents the width and j represents the height, following standard image conventions.
  )

print("i = \n",  i)
print("j = \n",  j)
print('z = ')
print(torch.ones_like(i))

print("+"*50)
print("i = \n",  i)
print("-j = \n",  -j)
print('-z = ')
print(-torch.ones_like(i))

```

    i = 
     tensor([[0., 1., 2.],
            [0., 1., 2.],
            [0., 1., 2.],
            [0., 1., 2.]], device='cuda:0')
    j = 
     tensor([[0., 0., 0.],
            [1., 1., 1.],
            [2., 2., 2.],
            [3., 3., 3.]], device='cuda:0')
    z = 
    tensor([[1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.]], device='cuda:0')
    ++++++++++++++++++++++++++++++++++++++++++++++++++
    i = 
     tensor([[0., 1., 2.],
            [0., 1., 2.],
            [0., 1., 2.],
            [0., 1., 2.]], device='cuda:0')
    -j = 
     tensor([[-0., -0., -0.],
            [-1., -1., -1.],
            [-2., -2., -2.],
            [-3., -3., -3.]], device='cuda:0')
    -z = 
    tensor([[-1., -1., -1.],
            [-1., -1., -1.],
            [-1., -1., -1.],
            [-1., -1., -1.]], device='cuda:0')



```python
## image centering

dirs = torch.stack(
      [(i - W * .5) / focal, -(j - H * .5) / focal, -torch.ones_like(i, device = device)], -1
  )

# dirs = torch.stack(
#       [i, -j, -torch.ones_like(i, device = device)], -1
#   )

print(dirs)
print(dirs.shape)
dirs[..., None, :].shape
```

    
    tensor([[[-1.5000,  2.0000, -1.0000],
             [-0.5000,  2.0000, -1.0000],
             [ 0.5000,  2.0000, -1.0000]],
    
            [[-1.5000,  1.0000, -1.0000],
             [-0.5000,  1.0000, -1.0000],
             [ 0.5000,  1.0000, -1.0000]],
    
            [[-1.5000, -0.0000, -1.0000],
             [-0.5000, -0.0000, -1.0000],
             [ 0.5000, -0.0000, -1.0000]],
    
            [[-1.5000, -1.0000, -1.0000],
             [-0.5000, -1.0000, -1.0000],
             [ 0.5000, -1.0000, -1.0000]]], device='cuda:0')
    torch.Size([4, 3, 3])





    torch.Size([4, 3, 1, 3])




```python
## mat1*mat2
mat1 = torch.tensor([[1, 2, 3]])
mat2 = torch.full((3, 3), 10)
print(mat1)
print(mat2)
print(mat1*mat2)
print(torch.sum(mat1*mat2, -1))
```

    tensor([[1, 2, 3]])
    tensor([[10, 10, 10],
            [10, 10, 10],
            [10, 10, 10]])
    tensor([[10, 20, 30],
            [10, 20, 30],
            [10, 20, 30]])
    tensor([60, 60, 60])



```python
## torch.from_numpy
a =  np.array([1, 2, 4])

b = torch.tensor(a)
c = torch.from_numpy(a)


a[0] = 10

print(a)
print(b)
print(c)
```

    [10  2  4]
    tensor([1, 2, 4])
    tensor([10,  2,  4])



```python
## rand
near = 2; far = 6; N_samples = 6
z_vals = torch.linspace(near, far, steps=N_samples, device=device)
print("z_vals = \n", z_vals)

# torch.rand(*z_vals.shape[:-1], N_samples, device=device) * (far - near) / N_samples
torch.rand(*z_vals.shape[:-1], N_samples, device=device) * (far - near) / N_samples

```

    z_vals = 
     tensor([2.0000, 2.8000, 3.6000, 4.4000, 5.2000, 6.0000], device='cuda:0')





    tensor([0.0192, 0.0702, 0.6064, 0.1827, 0.3709, 0.2194], device='cuda:0')




```python
z_vals.shape[:-1]

scalar_val = torch.tensor(0)
print(scalar_val, scalar_val.shape)
```

    tensor(0) torch.Size([])



```python
## torch.cumprod
a = torch.arange(1, 4)
print('a = ', a)
print(torch.cumprod(a, dim = -1) )
```

    a =  tensor([1, 2, 3])
    tensor([1, 2, 6])



```python
def get_rays(H, W, focal, c2w):
  """
  Generate rays for a given camera configuration.

  Args:
    H: Image height.
    W: Image width.
    focal: Focal length.
    c2w: Camera-to-world transformation matrix (4x4).

  Returns:
    rays_o: Ray origins (H*W, 3).
    rays_d: Ray directions (H*W, 3).
  """
  device = c2w.device  # Get the device of c2w
  focal = torch.from_numpy(focal).to(device) # call by reference
  # print(type(H), type(W), type(focal), type(c2w))

  i, j = torch.meshgrid(
      torch.arange(W, dtype=torch.float32, device=device),
      torch.arange(H, dtype=torch.float32, device=device),
      indexing='xy' # ensures that i represents the width and j represents the height, following standard image conventions.
  )
  dirs = torch.stack(
      [(i - W * .5) / focal, -(j - H * .5) / focal, -torch.ones_like(i, device = device)], -1
  )
 # dirs = [H, W, 1, (x, y, z)] * c2w[:3, :3] (# Intrinsic matrix)
  rays_d = torch.sum(dirs[..., None, :] * c2w[:3, :3], -1)  # a cone beam model,forming a perspective projection
  # rays_d = torch.Size([100, 100, 3])
  rays_d = rays_d.view(-1, 3)
  # rays_d = torch.Size([10000, 3])
  rays_o = c2w[:3, -1].expand(rays_d.shape)
  # rays_o = torch.Size([10000, 3])
  return rays_o, rays_d

# rgb, depth, acc = render_rays(model, rays_o, rays_d, near=2., far=6., N_samples=n_samples, device=device, rand=True)
def render_rays(network_fn, rays_o, rays_d, near, far, N_samples, device, rand=False, embed_fn=None, chunk=1024*4):
    # This function processes large inputs in chunks to prevent memory overload when calling
    def batchify(fn, chunk):
        return lambda inputs: torch.cat([fn(inputs[i:i+chunk]) for i in range(0, inputs.shape[0], chunk)], 0) # [0, 4096, 8192]

    # Sampling
    z_vals = torch.linspace(near, far, steps=N_samples, device=device)

    if rand:
        z_vals += torch.rand(*z_vals.shape[:-1], N_samples, device=rays_o.device) * (far - near) / N_samples
    # z_vals shape = torch.Size([64])
   
    pts = rays_o[...,None,:] + rays_d[...,None,:] * z_vals[...,:,None] # z_vals shape = torch.Size([64, 1])
    # pts.shape = torch.Size([10000, 64, 3])

    # Normalize view directions
    view_dirs = rays_d / torch.norm(rays_d, dim=-1, keepdim=True)
    view_dirs = view_dirs[..., None, :].expand(pts.shape)

    input_pts = torch.cat((pts, view_dirs), dim=-1)
    raw = batchify(network_fn, chunk)(input_pts)

    # Apply activations here instead of in network
    sigma_a = raw[...,0]  # Shape: [batch, N_samples]
    rgb = raw[...,1:]    # Shape: [batch, N_samples, 3]

    # Improved volume rendering
    dists = z_vals[..., 1:] - z_vals[..., :-1]  # Shape: [batch, N_samples-1]
    dists = torch.cat([dists, torch.tensor([1e10], device=device)], -1)

    # No need to manually expand dists as broadcasting will handle it
    alpha = 1. - torch.exp(-sigma_a * dists)  # Shape: [batch, N_samples] , cdf of exponetial
    alpha = alpha.unsqueeze(-1)  # Shape: [batch, N_samples, 1] 

    ## Computing transmittance: Transmittance (T) represents how much light reaches each point.
    ones_shape = (alpha.shape[0], 1, 1)
    T = torch.cumprod(
        torch.cat([
            torch.ones(ones_shape, device=device),  # (10000, 1, 1)
            1. - alpha + 1e-10                      # (10000, 64, 1)
        ], dim=1),
        dim=1
    )[:, :-1]  # Shape: [batch, N_samples, 1]

    weights = alpha * T  # Shape: [batch, N_samples, 1]

    # Compute final colors and depths, accumulation
    rgb_map = torch.sum(weights * rgb, dim=1)  # Sum along sample dimension
    # rgb_map.shape = torch.Size([10000, 3])
    depth_map = torch.sum(weights.squeeze(-1) * z_vals, dim=-1)  # Shape: [batch]
    acc_map = torch.sum(weights.squeeze(-1), dim=-1)  # Shape: [batch]

    return rgb_map, depth_map, acc_map
```

## Train Loop


```python
def train(images,poses,H,W,focal,testpose,testimg,device):

    print(f"Using device: {device}")
    model = NeRF().to(device)

    criterion = nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(),lr=5e-4)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.99) # decays the learning rate (LR) by multiplying it by gamma=0.99 after each epoch
 
    n_iter = 1000
    n_samples = 64
    i_plot = 50
    psnrs = []
    iternums = []
    t = time.time()

    # Convert data to tensors and move to device ONCE
    images_tensor = torch.from_numpy(images).float().to(device)
    poses_tensor = torch.from_numpy(poses).float().to(device)

    for i in range(n_iter):

        img_i = np.random.randint(images.shape[0])

        target = images_tensor[img_i]  # Use the corresponding image
        pose = poses_tensor[img_i]     # Use the corresponding pose

        rays_o, rays_d = get_rays(H, W, focal, pose)

        optimizer.zero_grad()

        rgb, depth, acc = render_rays(model, rays_o, rays_d, near=2., far=6., N_samples=n_samples, device=device, rand=True)

        rgb = rgb.reshape(H,W,3)

        loss = criterion(rgb, target)

        loss.backward()
        optimizer.step()

        if i % i_plot == 0:
            print(f'Iteration: {i}, Loss: {loss.item():.6f}, Time: {(time.time() - t) / i_plot:.2f} secs per iter')
            t = time.time()

            with torch.no_grad():
                rays_o, rays_d = get_rays(H, W, focal, testpose)
                rgb, depth, acc = render_rays(model, rays_o, rays_d, near=2., far=6.,
                                           N_samples=n_samples, device=device)
                rgb = rgb.reshape(H, W, 3)
                loss = criterion(rgb, testimg)
                psnr = -10. * torch.log10(loss)

                psnrs.append(psnr.item())
                iternums.append(i)

                plt.figure(figsize=(10,4))
                plt.subplot(121)
                plt.imshow(rgb.cpu().detach())
                plt.title(f'Iteration: {i}')
                plt.subplot(122)
                plt.plot(iternums, psnrs)
                plt.title('PSNR')
                plt.show()

    return model
```

## Load Data


```python
file_path = os.path.join(os.getcwd(),'data', 'tiny_nerf_data.npz')
data = np.load(file_path)
images = data['images']
poses = data['poses']
focal = data['focal']
H, W = images.shape[1:3]
print("image shape = ", images.shape)
print("pose shape = ", poses.shape)
print("focal length = ", focal)

device = "cuda" if torch.cuda.is_available() else "cpu"

testimg, testpose = images[101], poses[101]
images = images[:100,...,:3]
poses = poses[:100]
plt.imshow(testimg)
plt.show()
testimg =  torch.from_numpy(testimg).float().to("cuda")
testpose = torch.from_numpy(testpose).float().to("cuda")
```

    image shape =  (106, 100, 100, 3)
    pose shape =  (106, 4, 4)
    focal length =  138.88887889922103



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__22_1.webp)
    


## Train


```python
model = train(images,poses,H,W,focal,testpose,testimg,device)
```

    Using device: cuda
    Iteration: 0, Loss: 0.081648, Time: 0.02 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_1.webp)
    


    Iteration: 50, Loss: 0.054801, Time: 0.81 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_3.webp)
    


    Iteration: 100, Loss: 0.101059, Time: 0.80 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_5.webp)
    


    Iteration: 150, Loss: 0.052301, Time: 0.80 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_7.webp)
    


    Iteration: 200, Loss: 0.042073, Time: 0.80 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_9.webp)
    


    Iteration: 250, Loss: 0.021877, Time: 0.78 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_11.webp)
    


    Iteration: 300, Loss: 0.017164, Time: 0.78 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_13.webp)
    


    Iteration: 350, Loss: 0.015522, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_15.webp)
    


    Iteration: 400, Loss: 0.015200, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_17.webp)
    


    Iteration: 450, Loss: 0.017326, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_19.webp)
    


    Iteration: 500, Loss: 0.010243, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_21.webp)
    


    Iteration: 550, Loss: 0.004872, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_23.webp)
    


    Iteration: 600, Loss: 0.007803, Time: 0.77 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_25.webp)
    


    Iteration: 650, Loss: 0.009860, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_27.webp)
    


    Iteration: 700, Loss: 0.005969, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_29.webp)
    


    Iteration: 750, Loss: 0.010574, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_31.webp)
    


    Iteration: 800, Loss: 0.007468, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_33.webp)
    


    Iteration: 850, Loss: 0.010832, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_35.webp)
    


    Iteration: 900, Loss: 0.010579, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_37.webp)
    


    Iteration: 950, Loss: 0.007801, Time: 0.76 secs per iter



    
![png](../assets/images/ai/generative-models/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_9%EC%B0%A8%EC%8B%9C__NeRF__24_39.webp)
    


## Render Video


```python
# Transformation matrices in PyTorch
trans_t = lambda t: torch.tensor([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, t],
    [0, 0, 0, 1]
], dtype=torch.float32)

rot_phi = lambda phi: torch.tensor([
    [1, 0, 0, 0],
    [0, torch.cos(phi), -torch.sin(phi), 0],
    [0, torch.sin(phi), torch.cos(phi), 0],
    [0, 0, 0, 1]
], dtype=torch.float32)

rot_theta = lambda th: torch.tensor([
    [torch.cos(th), 0, -torch.sin(th), 0],
    [0, 1, 0, 0],
    [torch.sin(th), 0, torch.cos(th), 0],
    [0, 0, 0, 1]
], dtype=torch.float32)

# Pose function with spherical coordinates
def pose_spherical(theta, phi, radius):
    c2w = trans_t(radius)
    c2w = torch.matmul(rot_phi(torch.Tensor([phi / 180. * np.pi])), c2w)
    c2w = torch.matmul(rot_theta(torch.Tensor([theta / 180. * np.pi])), c2w)
    c2w = torch.tensor([[-1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=torch.float32) @ c2w
    return c2w

# Function for rendering based on user input
def f(**kwargs):
    c2w = pose_spherical(**kwargs)
    rays_o, rays_d = get_rays(H, W, focal, c2w[:3, :4])  # Get rays (this is a placeholder)
    c2w, rays_o, rays_d = map(lambda t: t.to(device), (c2w, rays_o, rays_d))
    with torch.no_grad():
      rgb, depth, acc = render_rays(model, rays_o, rays_d, near=2., far=6., N_samples=64, device=device)  # Render rays
    rgb = rgb.reshape(H, W, 3).cpu().detach()
    img = torch.clamp(rgb, 0, 1).numpy()  # Clamp RGB values between 0 and 1 and convert to numpy

    plt.figure(2, figsize=(20, 6))
    plt.imshow(img)
    plt.show()

# Interactive slider setup for theta, phi, and radius
sldr = lambda v, mi, ma: widgets.FloatSlider(
    value=v,
    min=mi,
    max=ma,
    step=.01,
)

names = [
    ['theta', [100., 0., 360]],
    ['phi', [-30., -90, 0]],
    ['radius', [4., 3., 5.]],
]

interactive_plot = interactive(f, **{s[0]: sldr(*s[1]) for s in names})
output = interactive_plot.children[-1]
output.layout.height = '350px'
interactive_plot
```


    interactive(children=(FloatSlider(value=100.0, description='theta', max=360.0, step=0.01), FloatSlider(value=-…



```python
frames = []
for th in tqdm(np.linspace(0., 360., 120, endpoint=False)):
    c2w = pose_spherical(th, -30., 4.)
    rays_o, rays_d = get_rays(H, W, focal, c2w[:3,:4])
    c2w, rays_o, rays_d = map(lambda t: t.to(device), (c2w, rays_o, rays_d))
    with torch.no_grad():
      rgb, depth, acc = render_rays(model, rays_o, rays_d, near=2., far=6., N_samples=64, device = device)
    rgb = rgb.reshape(H, W, 3)
    frames.append((255*np.clip(rgb.cpu().detach().numpy(),0,1)).astype(np.uint8))

import imageio
f = 'video.mp4'
imageio.mimwrite(f, frames, fps=30, quality=7)
```

    100%|██████████| 120/120 [00:36<00:00,  3.29it/s]
    WARNING:imageio_ffmpeg:IMAGEIO FFMPEG_WRITER WARNING: input image is not divisible by macro_block_size=16, resizing from (100, 100) to (112, 112) to ensure video compatibility with most codecs and players. To prevent resizing, make your input image divisible by the macro_block_size or set the macro_block_size to 1 (risking incompatibility).



```python
from IPython.display import HTML
from base64 import b64encode
mp4 = open('video.mp4','rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
<video width=400 controls autoplay loop>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)
```





<video width=400 controls autoplay loop>
      <source src="data:video/mp4;base64,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" type="video/mp4">
</video>



