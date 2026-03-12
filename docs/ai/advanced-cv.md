# 고급 CV (Tracking/Detection)


## 강의_3기_AI응용_4차시__object_tracking_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_4차시__object_tracking_.ipynb)

# 4장 객체 추적과 움직임 (Object tracking and motion)


```python
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
from pathlib import Path
```

## 객체 추적


```python
folder = "fig"
```

### 평균 이동 (Mean shift)


```python
# (function) def meanShift( probImage: MatLike, window: Rect, criteria: TermCriteria
# ) -> tuple[int, Rect]

# probImage: 히스토그램 역투영 영상 (확률 영상)
# window: 초기 검색 영역 윈도우
# criteri: 종료 기준
```


```python
import sys
import numpy as np
import cv2


# 비디오 파일 열기
# cap = cv2.VideoCapture('./fig/Billard.mp4')
cap = cv2.VideoCapture(Path(folder, "Billard.mp4"))


if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

ret, frame = cap.read()

if not ret:
    print('frame read failed!')
    sys.exit()

(x, y, w, h) = cv2.selectROI('ROI', frame)
rc = (x, y, w, h)



roi = frame[y:y+h, x:x+w]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# HS 히스토그램 계산
channels = [0, 1]
ranges = [0, 180, 0, 256]
hist = cv2.calcHist([roi_hsv], channels, None, [90, 128], ranges)

# Mean Shift 알고리즘 종료 기준
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# 비디오 매 프레임 처리
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # HS 히스토그램에 대한 역투영
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    backproj = cv2.calcBackProject([frame_hsv], channels, hist, ranges, 1)

    # Mean Shift
    _, rc = cv2.meanShift(backproj, rc, term_crit)

    # 추적 결과 화면 출력
    cv2.rectangle(frame, rc, (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(20) == 27:
        break

cap.release()
cv2.destroyAllWindows()

```

### 캠시프트 (Camshift)


```python
import sys
import numpy as np
import cv2


# 비디오 파일 열기
cap = cv2.VideoCapture(Path(folder, "Billard.mp4"))

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

ret, frame = cap.read()

if not ret:
    print('frame read failed!')
    sys.exit()

(x, y, w, h) = cv2.selectROI('ROI', frame)
rc = (x, y, w, h)

roi = frame[y:y+h, x:x+w]
roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# HS 히스토그램 계산
channels = [0, 1]
ranges = [0, 180, 0, 256]
hist = cv2.calcHist([roi_hsv], channels, None, [90, 128], ranges)

# CamShift 알고리즘 종료 기준
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# 비디오 매 프레임 처리
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # HS 히스토그램에 대한 역투영
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    backproj = cv2.calcBackProject([frame_hsv], channels, hist, ranges, 1)

    # CamShift
    ret, rc = cv2.CamShift(backproj, rc, term_crit)

    # 추적 결과 화면 출력
    cv2.rectangle(frame, rc, (0, 0, 255), 2)
    cv2.ellipse(frame, ret, (0, 255, 0), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(60) == 27:
        break

cap.release()
cv2.destroyAllWindows()

```

## 모션 벡터 (Motion vector)

### Lucas-Kanade optical flow


```python
# def calcOpticalFlowPyrLK(
#     prevImg: MatLike, 첫 번째 frame
#     nextImg: MatLike, 두 번째 frame
#     prevPts: MatLike, 첫 번째 points
#     nextPts: MatLike,
#     status: MatLike | None = ...,
#     err: MatLike | None = ...,
#     winSize: Size = ...,
#     maxLevel: int = ...,
#     criteria: TermCriteria = ...,
#     flags: int = ...,
#     minEigThreshold: float = ...
# ) -> tuple[nextPts:MatLike, status:atLike, err:MatLike]
```


```python
import sys
import numpy as np
import cv2


# src1 = cv2.imread('fig/frame1.jpg')
# src2 = cv2.imread('fig/frame2.jpg')
src1 = cv2.imread(Path(folder, "frame1.jpg"))
src2 = cv2.imread(Path(folder, "frame2.jpg"))

if src1 is None or src2 is None:
    print('Image load failed!')
    sys.exit()

gray1 = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)

pt1 = cv2.goodFeaturesToTrack(gray1, 50, 0.01, 10)
pt2, status, err = cv2.calcOpticalFlowPyrLK(src1, src2, pt1, None)

dst = cv2.addWeighted(src1, 0.5, src2, 0.5, 0)

pt1
status
pt2
for i in range(pt2.shape[0]):
    if status[i, 0] == 0:
        continue

    cv2.circle(dst, tuple(pt1[i, 0].astype(int)), 4, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(dst, tuple(pt2[i, 0].astype(int)), 4, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.arrowedLine(dst, tuple(pt1[i, 0].astype(int)), tuple(pt2[i, 0].astype(int)), (0, 255, 0), 2)

cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()

```

### Dense optical flow


```python
# def calcOpticalFlowFarneback(
#     prev: MatLike, # 첫 번째 영상
#     next: MatLike, # 두 번째 영상
#     flow: MatLike, # None
#     pyr_scale: float, # 피라미드 영상 축소 비율
#     levels: int, # 피라미드 개수
#     winsize: int, # window 크기
#     iterations: int, # 알고리즘 반복 횟수
#     poly_n: int,  # 5 또는 7
#     poly_sigma: float, # 1.1 또는 1.5
#     flags: int # 0
# ) -> MatLike: ...
```


```python
import sys
import numpy as np
import cv2


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 255), lineType=cv2.LINE_AA)


    for (x1, y1), (_x2, _y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 128, 255), -1, lineType=cv2.LINE_AA)

    return vis


# cap = cv2.VideoCapture('fig/vtest.avi')
cap = cv2.VideoCapture(Path(folder, "vtest.avi"))

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# # cap.set(cv2.CAP_PROP_FPS, 30)


if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()

ret, frame1 = cap.read()

if not ret:
    print('frame read failed!')
    sys.exit()

gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame2 = cap.read()

    if not ret:
        print('frame read failed!')
        sys.exit()

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 13, 3, 5, 1.1, 0)

    cv2.imshow('frame2', draw_flow(gray2, flow))
    if cv2.waitKey(20) == 27:
        break

    gray1 = gray2

cv2.destroyAllWindows()

```


## 강의_3기_AI응용_4차시__RAFT_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_4차시__RAFT_.ipynb)

# Optical Flow: Predicting movement with the RAFT model

Optical flow is the task of predicting movement between two images, usually two
consecutive frames of a video. Optical flow models take two images as input, and
predict a flow: the flow indicates the displacement of every single pixel in the
first image, and maps it to its corresponding pixel in the second image. Flows
are (2, H, W)-dimensional tensors, where the first axis corresponds to the
predicted horizontal and vertical displacements.

The following example illustrates how torchvision can be used to predict flows
using our implementation of the RAFT model. We will also see how to convert the
predicted flows to RGB images for visualization.



```python
!pip install av
```

    Collecting av
      Downloading av-14.1.0-cp312-cp312-win_amd64.whl.metadata (4.8 kB)
    Downloading av-14.1.0-cp312-cp312-win_amd64.whl (30.6 MB)
       ---------------------------------------- 0.0/30.6 MB ? eta -:--:--
       ----------- ---------------------------- 8.9/30.6 MB 46.0 MB/s eta 0:00:01
       --------------------- ------------------ 16.3/30.6 MB 40.9 MB/s eta 0:00:01
       --------------------------------- ------ 25.4/30.6 MB 41.3 MB/s eta 0:00:01
       ---------------------------------------  30.4/30.6 MB 41.9 MB/s eta 0:00:01
       ---------------------------------------  30.4/30.6 MB 41.9 MB/s eta 0:00:01
       ---------------------------------------  30.4/30.6 MB 41.9 MB/s eta 0:00:01
       ---------------------------------------  30.4/30.6 MB 41.9 MB/s eta 0:00:01
       ---------------------------------------- 30.6/30.6 MB 19.6 MB/s eta 0:00:00
    Installing collected packages: av
    Successfully installed av-14.1.0



```python
import numpy as np
import torch
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F
import torchvision.transforms as T
import torchvision
```


```python
plt.rcParams["savefig.bbox"] = "tight"
# sphinx_gallery_thumbnail_number = 2


def plot(imgs, **imshow_kwargs):
    if not isinstance(imgs[0], list): 
        # Make a 2d grid even if there's just 1 row
        imgs = [imgs]

    num_rows = len(imgs)
    num_cols = len(imgs[0])
    _, axs = plt.subplots(nrows=num_rows, ncols=num_cols, squeeze=False)
    for row_idx, row in enumerate(imgs):
        for col_idx, img in enumerate(row):
            ax = axs[row_idx, col_idx]
            img = F.to_pil_image(img.to("cpu"))
            ax.imshow(np.asarray(img), **imshow_kwargs)
            # ax.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

    plt.tight_layout()
```

## Reading Videos Using Torchvision
We will first read a video using :func:`~torchvision.io.read_video`.
Alternatively one can use the new :class:`~torchvision.io.VideoReader` API (if
torchvision is built from source).
The video we will use here is free of use from `pexels.com
<https://www.pexels.com/video/a-man-playing-a-game-of-basketball-5192157/>`_,
credits go to `Pavel Danilyuk <https://www.pexels.com/@pavel-danilyuk>`_.




```python
import tempfile
from pathlib import Path
from urllib.request import urlretrieve


video_url = "https://download.pytorch.org/tutorial/pexelscom_pavel_danilyuk_basketball_hd.mp4"
video_path = Path(tempfile.mkdtemp()) / "basketball.mp4" # make temporary random folder
vs = urlretrieve(video_url, video_path) # tuple (video_path, address)
```


```python
vs
```




    (WindowsPath('C:/Users/user/AppData/Local/Temp/tmpl127vq_2/basketball.mp4'),
     <http.client.HTTPMessage at 0x2d17e849700>)



:func:`~torchvision.io.read_video` returns the video frames, audio frames and
the metadata associated with the video. In our case, we only need the video
frames.

Here we will just make 2 predictions between 2 pre-selected pairs of frames,
namely frames (100, 101) and (150, 151). Each of these pairs corresponds to a
single model input.




```python
from torchvision.io import read_video
frames, _, _ = read_video(str(video_path))
# print("shape = ", frames.shape) # torch.Size([333, 720, 1280, 3])
```

    c:\Users\user\anaconda3\envs\opencv_torch_py3.12\Lib\site-packages\torchvision\io\video.py:197: UserWarning: The pts_unit 'pts' gives wrong results. Please use pts_unit 'sec'.
      warnings.warn("The pts_unit 'pts' gives wrong results. Please use pts_unit 'sec'.")



```python
frames = frames.permute(0, 3, 1, 2)  # (N, H, W, C) -> (N, C, H, W)

img1_batch = torch.stack([frames[100], frames[150]]) # torch.Size([2, 3, 720, 1280])
img2_batch = torch.stack([frames[101], frames[151]]) # torch.Size([2, 3, 720, 1280])

plot(img1_batch)
plot(img2_batch)
```


    
![png](../assets/images/ai/advanced-cv/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__9_0.webp)
    



    
![png](../assets/images/ai/advanced-cv/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__9_1.webp)
    


The RAFT model that we will use accepts RGB float images with pixel values in
[-1, 1]. The frames we got from :func:`~torchvision.io.read_video` are int
images with values in [0, 255], so we will have to pre-process them. We also
reduce the image sizes for the example to run faster. Image dimension must be
divisible by 8.




```python
def preprocess(batch):
    transforms = T.Compose(
        [
            T.ConvertImageDtype(torch.float32),
            T.Normalize(mean=0.5, std=0.5),  # map [0, 1] into [-1, 1]
            T.Resize(size=(520, 960)),
        ]
    )
    batch = transforms(batch)
    return batch


# If you can, run this example on a GPU, it will be a lot faster.
device = "cuda" if torch.cuda.is_available() else "cpu"

img1_batch = preprocess(img1_batch).to(device)
img2_batch = preprocess(img2_batch).to(device)

print(f"shape = {img1_batch.shape}, dtype = {img1_batch.dtype}")
```

    shape = torch.Size([2, 3, 520, 960]), dtype = torch.float32


### Estimating Optical flow using RAFT (Recurrent All-Pairs Field Transforms for Optical Flow)
We will use our RAFT implementation from
:func:`~torchvision.models.optical_flow.raft_large`, which follows the same
architecture as the one described in the `original paper <https://arxiv.org/abs/2003.12039>`_.
We also provide the :func:`~torchvision.models.optical_flow.raft_small` model
builder, which is smaller and faster to run, sacrificing a bit of accuracy.




```python
from torchvision.models.optical_flow import raft_large

weights = torchvision.models.optical_flow.Raft_Large_Weights
model = raft_large(weights = weights, progress=False).to(device)
model = model.eval()

# list_of_flows = model(img1_batch.to(device), img2_batch.to(device))
list_of_flows = model(img1_batch, img2_batch) # length = 12 
print(f"type = {type(list_of_flows)}")
print(f"length = {len(list_of_flows)} = number of iterations of the model")
```

    c:\Users\user\anaconda3\envs\opencv_torch_py3.12\Lib\site-packages\torchvision\models\_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=Raft_Large_Weights.C_T_SKHT_V2`. You can also use `weights=Raft_Large_Weights.DEFAULT` to get the most up-to-date weights.
      warnings.warn(msg)


    type = <class 'list'>
    length = 12 = number of iterations of the model



```python
list_of_flows[-1].shape
```




    torch.Size([2, 2, 520, 960])



The RAFT model outputs lists of predicted flows where each entry is a
(N, 2, H, W) batch of predicted flows that corresponds to a given "iteration"
in the model. For more details on the iterative nature of the model, please
refer to the `original paper <https://arxiv.org/abs/2003.12039>`_. Here, we
are only interested in the final predicted flows (they are the most acccurate
ones), so we will just retrieve the last item in the list.

As described above, a flow is a tensor with dimensions (2, H, W) (or (N, 2, H,
W) for batches of flows) where each entry corresponds to the horizontal and
vertical displacement of each pixel from the first image to the second image.
Note that the predicted flows are in "pixel" unit, they are not normalized
w.r.t. the dimensions of the images.




```python
predicted_flows = list_of_flows[0] # torch.Size([2, 2, 520, 960])
print(f"dtype = {predicted_flows.dtype}")
print(f"shape = {predicted_flows.shape} = (N, 2, H, W)")
print(f"min = {predicted_flows.min()}, max = {predicted_flows.max()}")
```

    dtype = torch.float32
    shape = torch.Size([2, 2, 520, 960]) = (N, 2, H, W)
    min = -6.754632949829102, max = 7.502845764160156


## Visualizing predicted flows
Torchvision provides the :func:`~torchvision.utils.flow_to_image` utlity to
convert a flow into an RGB image. It also supports batches of flows.
each "direction" in the flow will be mapped to a given RGB color. In the
images below, pixels with similar colors are assumed by the model to be moving
in similar directions. The model is properly able to predict the movement of
the ball and the player. Note in particular the different predicted direction
of the ball in the first image (going to the left) and in the second image
(going up).




```python
from torchvision.utils import flow_to_image

flow_imgs = flow_to_image(predicted_flows)
# print(flow_imgs.shape) # torch.Size([2, 3, 520, 960])
# The images have been mapped into [-1, 1] but for plotting we want them in [0, 1]
img1_batch = [(img1 + 1) / 2 for img1 in img1_batch]

grid = [[img1, flow_img] for (img1, flow_img) in zip(img1_batch, flow_imgs)]
plot(grid)
```


    
![png](../assets/images/ai/advanced-cv/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_4%EC%B0%A8%EC%8B%9C__RAFT__18_0.webp)
    


## Bonus: Creating GIFs of predicted flows
In the example above we have only shown the predicted flows of 2 pairs of
frames. A fun way to apply the Optical Flow models is to run the model on an
entire video, and create a new video from all the predicted flows. Below is a
snippet that can get you started with this. We comment out the code, because
this example is being rendered on a machine without a GPU, and it would take
too long to run it.




```python
from torchvision.io import write_jpeg
for i, (img1, img2) in enumerate(zip(frames, frames[1:30])):
    # Note: it would be faster to predict batches of flows instead of individual flows
    img1 = preprocess(img1[None]).to(device)
    img2 = preprocess(img2[None]).to(device)

    list_of_flows = model(img1, img2)
    predicted_flow = list_of_flows[-1][0]
    flow_img = flow_to_image(predicted_flow).to("cpu")
    # output_folder = "C:/Users/user/output/"  # Update this to the folder of your choice
    output_folder = "/content/output/"
    write_jpeg(flow_img, output_folder + f"predicted_flow_{i}.jpg")
```

Once the .jpg flow images are saved, you can convert them into a video or a
GIF using ffmpeg with e.g.:

ffmpeg -f image2 -framerate 30 -i predicted_flow_%d.jpg -loop -1 flow.gif




## 강의_3기_AI응용_5차시__DeepCNN_trash_detection_

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/study-site/blob/main/notebooks/intermediate/강의_3기_AI응용_5차시__DeepCNN_trash_detection_.ipynb)

# 5장 Deep CNN

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
import os
import torch
from torch import nn, optim
from torch.utils.data import Dataset
from torchvision import models, transforms
from PIL import Image
from pathlib import Path
import ipdb
```

## Recycles image classification

### Pytorch custom 데이터셋 클래스


```python
# class PyTorch_Custom_Dataset_Class(Dataset):
#     def __init__(self):
#         super().__init__()
#         self.number = [i for i in range(10)]
#     def __getitem__(self, idx):
#         print("__getitem__ 실행")
#         return self.number[idx]
#     def __len__(self):
#         print("__len__ 실행")
#         return len(self.number)
#     def __str__(self):
#         print("Hello") 
```


```python
%%writefile Dataset_Class.py

import os
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from PIL import Image
import shutil

class PyTorch_Classification_Dataset_Class(Dataset):
    def __init__(self
                # , dataset_dir = "/content/Recycle_Classification_Dataset"
                # , dataset_dir = "Recycle_Classification_Dataset"
                , dataset_dir
                , transform):
        super().__init__()
        # if not os.path.isdir(dataset_dir):
        #     os.system("git clone https://github.com/JinFree/Recycle_Classification_Dataset.git") # 
        #     # os.system("rm -rf ./Recycle_Classification_Dataset/.git")
        #     # shutil.rmtree("./Recycle_Classification_Dataset/.git")
        #     shutil.rmtree(os.path.join(os.getcwd(), "Recycle_Classification_Dataset", ".git"))

        self.image_abs_path = dataset_dir
        self.transform = transform
        # if self.transform is None:
        #     self.transform = transforms.Compose([
        #             transforms.Resize(256)
        #             , transforms.RandomCrop(224)
        #             , transforms.ToTensor()
        #             , transforms.Normalize(mean=[0.485, 0.456, 0.406],
        #                     std=[0.229, 0.224, 0.225])
        #             ])
        self.label_list = os.listdir(self.image_abs_path) # ["can", "glass", "paper", "plastic"]
        self.label_list.sort()
        self.x_list = []
        self.y_list = []
        for label_index, label_str in enumerate(self.label_list):
            img_path = os.path.join(self.image_abs_path, label_str)  # ~/Recycle_Classification_Dataset
            img_list = os.listdir(img_path)
            for img in img_list:
                self.x_list.append(os.path.join(img_path, img))
                self.y_list.append(label_index)

    def __len__(self):
        return len(self.x_list)

    def __getitem__(self, idx):
        image = Image.open(self.x_list[idx])
        if image.mode != "RGB":
            image = image.convert('RGB')
        # if self.transform is not None:
        image = self.transform(image)
        return image, self.y_list[idx]

    def __save_label_map__(self, dst_text_path = "label_map.txt"):
        label_list = self.label_list
        f = open(dst_text_path, 'w')
        for i in range(len(label_list)):
            f.write(label_list[i]+'\n')
        f.close()

    def __num_classes__(self):
        return len(self.label_list)
```

    Overwriting Dataset_Class.py


### Model from scratch


```python
%%writefile Model_Class_From_the_Scratch.py

import torch
import torch.nn as nn
import torch.nn.functional as F


class MODEL_From_Scratch(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.classifier = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size = 3, stride = 2, padding = 1)
            , nn.BatchNorm2d(32)
            , nn.ReLU()
            , nn.Conv2d(32, 64, kernel_size = 3, stride = 2, padding = 1)
            , nn.BatchNorm2d(64)
            , nn.ReLU()
            , nn.Conv2d(64, 128, kernel_size = 3, stride = 2, padding = 1)
            , nn.BatchNorm2d(128)
            , nn.ReLU()
            , nn.AdaptiveAvgPool2d(1)
            , nn.Flatten()
            , nn.Linear(128, 512)
            , nn.ReLU()
            , nn.Dropout()
            , nn.Linear(512, 64)
            , nn.ReLU()
            , nn.Dropout()
            , nn.Linear(64, num_classes)
            # , nn.Softmax(dim=-1)
        )
    def forward(self, x):
        return self.classifier(x)
```

    Overwriting Model_Class_From_the_Scratch.py



```python
# dataset = PyTorch_Classification_Dataset_Class()
# print(len(dataset))
# dataset.__save_label_map__()
# print("class number = ", dataset.__num_classes__())
```

###  MobileNet class


```python
%%writefile Model_Class_Transfer_Learning_MobileNet.py

import torch
from torchvision import models
import torch.nn as nn
import torch.nn.functional as F

class MobileNet(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        weights = models.MobileNet_V2_Weights.IMAGENET1K_V2
        self.network = models.mobilenet_v2(weights=weights)
        num_ftrs = self.network.classifier[1].in_features
        self.network.classifier[1] = nn.Linear(num_ftrs, num_classes)
        # self.classifier = nn.Softmax(dim=-1)
   


    def forward(self, x):
        x = self.network(x)
        # x = self.classifier(x)
        return x
```

    Overwriting Model_Class_Transfer_Learning_MobileNet.py


### Training class


```python
# %%writefile PyTorch_Classification_Training_Class.py

import os
import torch
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn.functional as F
from tqdm import tqdm
import shutil

# from .Model_Class_From_the_Scratch import MODEL_From_Scratch
# from .Model_Class_Transfer_Learning_MobileNet import MobileNet
# from .Dataset_Class import PyTorch_Classification_Dataset_Class as Dataset

# window
from Model_Class_From_the_Scratch import MODEL_From_Scratch
from Model_Class_Transfer_Learning_MobileNet import MobileNet
from Dataset_Class import PyTorch_Classification_Dataset_Class as Dataset


class PyTorch_Classification_Training_Class():
    def __init__(self
                # , dataset_dir = "/content/Recycle_Classification_Dataset"
                # , dataset_dir = "./Recycle_Classification_Dataset" # window
                 , dataset_dir = os.path.join(os.getcwd(), "Recycle_Classification_Dataset")
                , batch_size = 16
                , train_ratio = 0.75
                ):
        if not os.path.isdir(dataset_dir):
            os.system("git clone https://github.com/JinFree/Recycle_Classification_Dataset.git")
            # os.system("rm -rf ./Recycle_Classification_Dataset/.git")
            shutil.rmtree(os.path.join(os.getcwd(), "Recycle_Classification_Dataset", ".git"))
            # dataset_dir = os.path.join(os.getcwd(), 'Recycle_Classification_Dataset')
        self.USE_CUDA = torch.cuda.is_available()
        self.DEVICE = torch.device("cuda" if self.USE_CUDA else "cpu")
        self.transform = transforms.Compose([
                transforms.Resize(256)
                , transforms.RandomCrop(224)
                , transforms.ToTensor()
                , transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
                ])
        dataset = Dataset(dataset_dir = dataset_dir, transform = self.transform)
        dataset.__save_label_map__()
        self.num_classes = dataset.__num_classes__()
        train_size = int(train_ratio * len(dataset))
        test_size = len(dataset) - train_size
        train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
        self.train_loader = torch.utils.data.DataLoader(
            train_dataset
            , batch_size=batch_size
            , shuffle=True
        )
        self.test_loader = torch.utils.data.DataLoader(
            test_dataset
            , batch_size=batch_size
            , shuffle=False
        )
        self.model = None
        self.model_str = None

    def prepare_network(self
            , is_scratch = True):
        if is_scratch:
            self.model = MODEL_From_Scratch(self.num_classes)
            self.model_str = "PyTorch_Training_From_Scratch"
        else:
            self.model = MobileNet(self.num_classes)
            self.model_str = "PyTorch_Transfer_Learning_MobileNet"
        self.model.to(self.DEVICE)
        self.model_str += ".pt"

    def training_network(self
            , learning_rate = 0.0001
            , epochs = 10
            , step_size = 3
            , gamma = 0.3):
        if self.model is None:
            self.prepare_network(False)
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        # step_size: 지정한 epoch마다 학습률을 감소, gamma: 학습률을 감소시킬 비율 (예: gamma=0.1이면 lr = lr * 0.1)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
        acc = 0.0
        for epoch in range(1, epochs + 1):
            print(f"Use CUDA = {torch.cuda.is_available()}")
            self.model.train()
            for data, target in tqdm(self.train_loader):
                data, target = data.to(self.DEVICE), target.to(self.DEVICE)
                optimizer.zero_grad()
                output = self.model(data)
                loss = F.cross_entropy(output, target)
                loss.backward()
                optimizer.step()
            scheduler.step()
            self.model.eval()
            test_loss = 0
            correct = 0
            with torch.no_grad():
                for data, target in tqdm(self.test_loader):
                    data, target = data.to(self.DEVICE), target.to(self.DEVICE)
                    output = self.model(data)
                    test_loss += F.cross_entropy(output, target, reduction='sum').item()
                    pred = output.max(1, keepdim=True)[1]
                    # correct += pred.eq(target.view_as(pred)).sum().item()
                    correct += (pred == target).float().mean().item()

            test_loss /= len(self.test_loader.dataset)
            test_accuracy = 100. * correct / len(self.test_loader.dataset)
            print('[{}] Test Loss: {:.4f}, Accuracy: {:.2f}%'.format(epoch, test_loss, test_accuracy))
            if acc < test_accuracy:
                acc = test_accuracy
                torch.save(self.model.state_dict(), self.model_str)
                print("model saved!")

if __name__ == "__main__":
    training_class = PyTorch_Classification_Training_Class()
    training_class.prepare_network(True) # Scratch model
    # training_class.prepare_network(False) # MobileNet
    training_class.training_network(learning_rate = 0.00001, epochs=10, step_size=3, gamma=0.3)

```


```python
%%writefile Inference_Cam.py

import torch
import cv2
from PIL import Image
from torchvision import transforms
import numpy as np
from Model_Class_From_the_Scratch import MODEL_From_Scratch
from Model_Class_Transfer_Learning_MobileNet import MobileNet


class Inference_Class():
    def __init__(self):
        USE_CUDA = torch.cuda.is_available()
        self.DEVICE = torch.device("cuda" if USE_CUDA else "cpu")
        self.model = None
        self.label_map = None
        self.transform_info = transforms.Compose(
                [
                transforms.Resize(size=(224, 224)),
                transforms.ToTensor()
                ])

    def load_model(self, is_train_from_scratch, label_map_file = "label_map.txt"):
        self.label_map = np.loadtxt(label_map_file, str, delimiter='\t')
        num_classes = len(self.label_map)
        model_str = None
        if is_train_from_scratch:
            self.model = MODEL_From_Scratch(num_classes).to(self.DEVICE)
            model_str = "PyTorch_Training_From_Scratch"
        else:
            self.model = MobileNet(num_classes).to(self.DEVICE)
            model_str = "PyTorch_Transfer_Learning_MobileNet"
        model_str += ".pt"
        self.model.load_state_dict(torch.load(model_str, map_location=self.DEVICE))
        self.model.eval()


    def inference_video(self, video_source="test_video.mp4"):
        cap = cv2.VideoCapture(video_source)
        if cap.isOpened():
            print("Video Opened")
        else:
            print("Video Not Opened")
            print("Program Abort")
            exit()
        cv2.namedWindow("Output", cv2.WINDOW_GUI_EXPANDED)
        with torch.no_grad():
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    output = self.inference_frame(frame)
                    cv2.imshow("Output", output)
                else:
                    break
                if cv2.waitKey(33) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        return

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s", "--is_scratch",
#             required=False,
#             action="store_true",
#             help="inference with model trained from the scratch")
#     parser.add_argument("-src", "--source",
#             required=False,
#             type=str,
#             default="./test_video.mp4",
#             help="OpenCV Video source")
#     args = parser.parse_args()
#     is_train_from_scratch = False
#     source = args.source
#     if args.is_scratch:
#         is_train_from_scratch = True
#     inferenceClass = Inference_Class()
#     inferenceClass.load_model(is_train_from_scratch)
#     inferenceClass.inference_video(source)

```

    Writing Inference_Cam.py


### 추론 클래스


```python
# 추론을 위한 클래스를 불러옵니다.
from Inference_Cam import Inference_Class

# 클래스를 초기화하고 모델을 불러옵니다.
inferenceClass = Inference_Class()
is_train_from_scratch = False
inferenceClass.load_model(is_train_from_scratch)
```


```python
from google.colab.patches import cv2_imshow
import cv2

def inference(input_image):
    cv_image = []
    if isinstance(input_image, str):
        cv_image = cv2.imread(input_image, cv2.IMREAD_COLOR)
    else:
        cv_image = np.copy(input_image)
    result_frame, label_text, class_prob = inferenceClass.inference_image(cv_image)
    print("입력 이미지는 {} % 확률로 {}으로 분류됩니다.".format((float)(class_prob) * 100, label_text))
    cv2_imshow(result_frame)
    # cv2.imshow(result_frame)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return result_frame
```


```python
# %cd /content
input_image_path = os.path.join(os.getcwd(), "test_image_1.jpg")
result = inference(input_image_path)
```

    입력 이미지는 98.406225 % 확률로 can으로 분류됩니다.



    
![png](../assets/images/ai/advanced-cv/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_5%EC%B0%A8%EC%8B%9C__DeepCNN_trash_detection__files/%EA%B0%95%EC%9D%98_3%EA%B8%B0_AI%EC%9D%91%EC%9A%A9_5%EC%B0%A8%EC%8B%9C__DeepCNN_trash_detection__21_1.webp)
    

