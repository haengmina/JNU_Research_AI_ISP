# Infinite-ISP 종합 가이드

Infinite-ISP는 하드웨어 ISP의 모든 측면을 고려하여 설계된 풀스택 ISP 개발 플랫폼입니다. 이 플랫폼은 Python으로 작성된 카메라 파이프라인 모듈 컬렉션, 고정 소수점(fixed-point) 참조 모델, 최적화된 RTL 설계, FPGA 통합 프레임워크, 그리고 Xilinx® Kria KV260 개발 보드 및 Efinix® Titanium Ti180 J484 개발 키트에서 즉시 사용 가능한 관련 펌웨어를 포함하고 있습니다. 또한, 다양한 센서 및 애플리케이션에 맞춰 ISP 파이프라인의 매개변수를 조정할 수 있는 독립형 Python 기반 튜닝 도구(Tuning Tool)를 제공합니다. 마지막으로, 필요한 드라이버와 커스텀 애플리케이션 개발 스택을 제공하여 Infinite-ISP를 Linux 플랫폼으로 이식할 수 있는 소프트웨어 솔루션도 포함하고 있습니다.

## 레포지토리 구성
| 번호 | 저장소 이름 | 설명 |
|---------| -------------  | ------------- |
| 1 | **[Infinite-ISP_AlgorithmDesign](https://github.com/10x-Engineers/Infinite-ISP)** | 알고리즘 개발을 위한 Infinite-ISP 파이프라인의 Python 기반 모델 |
| 2 | **[Infinite-ISP_ReferenceModel](https://github.com/10x-Engineers/Infinite-ISP_ReferenceModel)** | 하드웨어 구현을 위한 Infinite-ISP 파이프라인의 Python 기반 고정 소수점 모델 |
| 3 | **[Infinite-ISP_RTL](https://github.com/10x-Engineers/Infinite-ISP_RTL)** | 참조 모델을 기반으로 한 이미지 신호 처리기(ISP)의 RTL Verilog 설계 |
| 4 | **[Infinite-ISP_AutomatedTesting](https://github.com/10x-Engineers/Infinite-ISP_AutomatedTesting)** | 비트 단위까지 정확한 설계를 보장하기 위한 이미지 신호 처리기의 블록 및 멀티 블록 레벨 자동화 테스트 프레임워크 |
| 5 | **FPGA 구현** | 다음 보드에서의 Infinite-ISP FPGA 구현: <br> <ul><li>Xilinx® Kria KV260의 XCK26 Zynq UltraScale + MPSoC **[Infinite-ISP_FPGA_XCK26](https://github.com/10x-Engineers/Infinite-ISP_FPGA_XCK26)** </li></ul> |
| 6 | **[Infinite-ISP_FPGABinaries](https://github.com/10x-Engineers/Infinite-ISP_FPGABinaries)** | Xilinx® Kria KV260의 XCK26 Zynq UltraScale + MPSoC 및 Efinix® Titanium Ti180 J484 개발 키트를 위한 FPGA 바이너리(비트스트림 + 펌웨어 실행 파일) |
| 7 | **[Infinite-ISP_TuningTool](https://github.com/10x-Engineers/Infinite-ISP_TuningTool)** | Infinite-ISP를 위한 캘리브레이션 및 분석 도구 모음 |
| 8 | **[Infinite-ISP_Firmware](https://github.com/10x-Engineers/Infinite-ISP_Firmware)** | Kria KV260의 내장 Arm® Cortex®A53 프로세서를 위한 펌웨어 |
| 9 | **[Infinite-ISP_LinuxCameraStack](https://github.com/10x-Engineers/Infinite-ISP_LinuxCameraStack.git)** | Infinite-ISP의 Linux 지원 확장 및 Linux 기반 카메라 애플리케이션 스택 개발 |

**[액세스 요청](https://docs.google.com/forms/d/e/1FAIpQLSfOIldU_Gx5h1yQEHjGbazcUu0tUbZBe0h9IrGcGljC5b4I-g/viewform?usp=sharing)**: Infinite-ISP_RTL, Infinite-ISP_AutomatedTesting 및 Infinite-ISP_FPGA_XCK26 저장소에 대한 액세스 권한을 요청하세요.

---

## 1. Infinite-ISP 알고리즘 설계

## Infinite-ISP 알고리즘 설계: ISP 알고리즘 개발을 위한 Python 기반 모델
Infinite-ISP 알고리즘 설계는 센서로부터 입력된 RAW 이미지를 출력 RGB 이미지로 변환하기 위해 애플리케이션 레벨에서 구현된 카메라 파이프라인 모듈의 모음입니다. Infinite-ISP는 각 모듈 레벨에서 간단한 것부터 복잡한 알고리즘까지 포함하는 것을 목표로 합니다.


![](assets/infinite-isp-architecture-initial.png)

`Infinite-ISP v1.1`을 위한 ISP 파이프라인

### 목표
인터넷에는 많은 오픈소스 ISP가 있습니다. 대부분은 개별 기여자들에 의해 개발되었으며, 각각 고유한 강점을 가지고 있습니다. 이 프로젝트는 모든 오픈소스 ISP 개발을 한 곳에 집중시켜 모든 ISP 개발자들이 기여할 수 있는 단일 플랫폼을 제공하는 것을 목표로 합니다. InfiniteISP는 기존의 알고리즘뿐만 아니라 최신 딥러닝 알고리즘도 포함하여 두 가지를 깔끔하게 비교할 수 있도록 할 것입니다. 이 프로젝트는 아이디어에 제한이 없으며, 복잡성에 관계없이 파이프라인의 전체 결과를 향상시키는 모든 알고리즘을 포함하는 것을 목표로 합니다.


### 기능 비교 매트릭스

유명한 openISP와의 기능 비교입니다.

InfiniteISP는 **3A 알고리즘**도 시뮬레이션합니다.

| Module | 설명 | infiniteISP | openISP |
| --- | --- | --- | --- |
| Crop | 이미지 영역 자르기 | 베이어 패턴 안전 크롭 | ---- |
| Dead Pixel Correction (DPC) | 결함 픽셀을 주변 픽셀로 복원 | 수정된 [Yongji et al, Dynamic Defective Pixel Correction for Image Sensor](https://ieeexplore.ieee.org/document/9194921) | 예 |
| Black Level Correction (BLC) | 센서 기본 노이즈 오프셋 제거 | 캘리브레이션 / 센서 의존 <br> - 설정에서 BLC 적용 | 예 |
| Opto-Electronic Conversion Function (OECF) | 빛과 센서 간 비선형적 응답을 보정/선형화 | 캘리브레이션 / 센서 의존 <br> - 설정에서 LUT 구현 | ---- |
| Anti-Aliasing Filter | 앨리어싱(계단현상) 억제 필터 | ---- | 예 |
| Digital Gain | 밝기 증가를 위한 전체 디지털 게인 곱셈 | 설정 파일에서 게인 적용 | 밝기 대비 제어 |
| Lens Shading Correction (LSC) | 렌즈 비네팅(가장자리 어두워짐) 현상 교정 | 구현 예정 | ---- |
| Bayer Noise Reduction (BNR) | 컬러 보간 전 RAW 도메인에서 고주파 노이즈 제거 | [Tan et al의 Green Channel Guiding Denoising](https://www.researchgate.net/publication/261753644_Green_Channel_Guiding_Denoising_on_Bayer_Image) | 크로마 노이즈 필터링 |
| White Balance (WB) | 흰색이 정상적으로 보이도록 수동 게인 적용 | 설정 파일에서 WB 게인 적용 | 예 |
| Demosaic | 베이어 패턴(단일색)을 RGB 풀 컬러 이미지로 복원 | [Malvar He Cutler](https://www.ipol.im/pub/art/2011/g_mhcd/article.pdf) 디모자이킹 알고리즘 | 예 <br> - Malvar He Cutler|
| **3A Algorithms** | **자동 노출 및 자동 화이트 밸런스** | **AE & AWB** | ---- |
| Auto White Balance (AWB) | 조명 환경을 분석하여 알맞은 흰색 비율 자동 추정 | - [Grey World](https://www.sciencedirect.com/science/article/abs/pii/0016003280900587) <br> - [Norm 2](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/12/1/art00008) <br> - [PCA 알고리즘](https://opg.optica.org/josaa/viewmedia.cfm?uri=josaa-31-5-1049&seq=0) | ---- |
| Auto Exposure (AE) | 화면 밝기 기반으로 최적의 적정 노출값 자동 추정 | - 왜도 기반 [자동 노출](https://www.atlantis-press.com/article/25875811.pdf) | ---- |
| Color Correction Matrix (CCM) | 센서 색상을 sRGB 등 표준 색상으로 맞추는 3x3 변환 | 캘리브레이션 / 센서 의존 <br> - 설정에서 3x3 CCM 적용 | 예 <br> - 4x3 CCM |
| Gamma Tone Mapping | 시각 특성에 맞춰 비선형적인 톤/밝기 교정 | 설정 파일에서 RGB 감마 LUT 적용 | 예 <br> - YUV 및 RGB 도메인|
| Color Space Conversion (CSC) | RGB 색상을 YUV(휘도와 색차) 영역으로 변환 | YCbCr 디지털 <br> - BT 601 <br> - BT 709 <br> | 예 <br> - YUV 아날로그 |
| Color Saturation Enhancement | 전반적인 색감 향상을 위한 채도 증폭 | YUV/YCrCb 도메인의 크로마 채널에 채도 게인 적용| 예|
| Local Dynamic Contrast Improvement (LDCI) | 명암비를 개선하고 디테일을 살리는 국부적 톤 매핑 | 수정된 [대비 제한 적응형 히스토그램 균등화](https://arxiv.org/ftp/arxiv/papers/2108/2108.12818.pdf#:~:text=The%20technique%20to%20equalize%20the,a%20linear%20trend%20(CDF)) | ---- |
| Edge Enhancement / Sharpen | 경계선을 선명하게 강화하여 이미지 디테일 향상 | 강도 조절이 가능한 간단한 언샤프 마스킹 | 예 |
| 2D Noise Reduction (2DNR) | YUV 공간에서 2차적으로 평면의 자글자글한 노이즈 제거 | [비지역 평균 필터](https://www.ipol.im/pub/art/2011/bcm_nlm/article.pdf) | 예 <br> - NLM 필터 <br> - 양방향 노이즈 필터|
| Hue Saturation Control | 이미지의 전체 색조(Hue) 및 채도(Sat) 조절 | ---- | 예 |
| RGB Conversion | YUV 공간에서의 처리를 마친 후 RGB 포맷으로 다시 역변환 | YUV에서 RGB로 역변환 적용 - CSC와 동일한 표준| 아니오|
| Scale | 이미지 해상도를 원하는 크기로 축소/확대 (Bilinear 등) | - 정수 스케일링 <br> - 비정수 스케일링 | ---- |
| False Color Suppression | 고주파 엣지 영역에서 발생하는 가짜 색상 억제 | ---- | 예 |
| YUV Conversion Format | 최종 출력/인코딩을 위해 서브샘플링 포맷 변경 | - YUV - 444 <br> - YUV - 422 <br> | ---- |


### 의존성
이 프로젝트는 `Python_3.9.12`와 호환됩니다.

의존성은 [requirements.txt](requirements.txt) 파일에 나열되어 있습니다.

이 프로젝트는 pip 패키지 매니저가 사전 설치되어 있다고 가정합니다.

### 실행 방법
파이프라인을 실행하려면 다음 단계를 따르세요:
1. 다음 명령으로 레포지토리를 클론합니다:
```shell
git clone https://github.com/10xEngineersTech/Infinite-ISP_ReferenceModel
```

2. requirements 파일에서 모든 의존성을 설치합니다:
```shell
## Conda 환경을 사용하는 경우, 먼저 환경 내에 pip를 설치하는 것을 권장합니다.
## conda install pip
pip install -r requirements.txt
```
3. [isp_pipeline.py](isp_pipeline.py)를 실행합니다:
```shell
python isp_pipeline.py
```

#### 예제

[in_frames/normal](in_frames/normal) 폴더에 튜닝된 설정과 함께 몇 개의 샘플 이미지가 이미 프로젝트에 추가되어 있습니다. 이 중 하나를 실행하려면 설정 파일 이름을 제공된 샘플 설정 중 하나로 교체하면 됩니다. 예를 들어 `Indoor1_2592x1536_12bit_RGGB.raw`에서 파이프라인을 실행하려면 [isp_pipeline.py](isp_pipeline.py)에서 설정 파일 이름과 데이터 경로를 다음과 같이 교체하세요:

```python
CONFIG_PATH = './config/Indoor1_2592x1536_12bit_RGGB-configs.yml'
RAW_DATA = './in_frames/normal/data'
```

### 여러 이미지/데이터셋에서 파이프라인 실행 방법

[isp_pipeline_multiple_images.py](isp_pipeline_multiple_images.py)라는 또 다른 스크립트가 있으며, 두 가지 모드로 Infinite-ISP를 여러 이미지에서 실행합니다:


1. 데이터셋 처리
    <br>여러 이미지를 실행합니다. RAW 이미지는 `<filename>-configs.yml` 이름의 자체 설정 파일이 있어야 합니다. 여기서 `<filename>`은 RAW 파일명이며, 그렇지 않으면 기본 설정 파일 [configs.yml](config/configs.yml)이 사용됩니다.

    NEF, DNG, CR2와 같은 RAW 이미지 포맷의 경우, 이러한 RAW 파일 메타데이터에 제공된 센서 정보를 추출하고 기본 설정 파일을 업데이트하는 기능도 제공합니다.

2. 비디오 모드
   <br>데이터셋의 각 이미지는 순서대로 비디오 프레임으로 간주됩니다. 모든 이미지는 [configs.yml](config/configs.yml)의 동일한 설정 파라미터를 사용하며, 한 프레임에서 계산된 3A 통계는 다음 프레임에 적용됩니다.

레포지토리를 클론하고 모든 의존성을 설치한 후 다음 단계를 따르세요:

1. `DATASET_PATH`를 데이터셋 폴더로 설정합니다. 예를 들어 이미지가 [in_frames/normal/data](in_frames/normal/data) 폴더에 있는 경우:
```python
DATASET_PATH = './in_frames/normal/data'
```

2. 데이터셋이 다른 git 레포지토리에 있는 경우 루트 디렉토리에서 다음 명령을 사용하여 서브모듈로 추가할 수 있습니다. 명령에서 `<url>`은 `https://github.com/<user>/<repository_name>`과 같은 git 레포지토리 주소이고, `<path>`는 서브모듈을 추가할 레포지토리 내 위치입니다. Infinite ISP의 경우 `<path>`는 `./in_frames/normal/<dataset_name>`이어야 합니다. `<dataset_name>`은 `data`가 아니어야 합니다. [in_frames/normal/data](in_frames/normal/data) 디렉토리가 이미 존재하기 때문입니다.

```shell
git submodule add <url> <path>
git submodule update --init --recursive
```


4. git 레포지토리를 서브모듈로 추가한 후 [isp_pipeline_dataset.py](isp_pipeline_dataset.py)의 `DATASET_PATH` 변수를 `./in_frames/normal/<dataset_name>`으로 업데이트합니다. Git은 서브모듈을 사용하여 레포지토리의 하위 폴더를 가져오는 것을 허용하지 않습니다. 전체 레포지토리만 추가한 다음 폴더에 접근할 수 있습니다. 서브모듈의 하위 폴더에서 이미지를 사용하려면 [isp_pipeline_dataset.py](isp_pipeline_dataset.py) 또는 [video_processing.py](video_processing.py)의 `DATASET_PATH` 변수를 적절히 수정하세요.

```python
DATASET_PATH = './in_frames/normal/<dataset_name>'
```

5. `isp_pipeline_dataset.py` 또는 `video_processing.py`를 실행합니다.
6. 처리된 이미지는 [out_frames](out_frames/) 폴더에 저장됩니다.

### 테스트 벡터 생성
개별 또는 다중 모듈을 테스트 대상 장치(DUT)로 하여 여러 이미지에 대한 테스트 벡터를 생성하는 방법은 제공된 [지침](test_vector_generation/README.md)을 참조하세요.

### 기여하기

Pull Request를 하기 전에 [기여 가이드라인](docs/CONTRIBUTIONS.md)을 읽어주세요.

### 결과
다음은 시중의 경쟁 ISP와 비교한 이 파이프라인의 결과입니다.
우리 ISP의 출력은 오른쪽에, 기준이 되는 ground truth는 왼쪽에 표시됩니다.


&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **ground truth**     &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **infiniteISP**
![](assets/Indoor1.png)
![](assets/Outdoor1.png)
![](assets/Outdoor2.png)
![](assets/Outdoor3.png)
![](assets/Outdoor4.png)

PSNR 및 SSIM 이미지 품질 메트릭 기반의 위 결과 비교

| 이미지    | PSNR  | SSIM  |
|-----------|-------|-------|
| Indoor1   |20.0974     |0.8599
|Outdoor1   |21.8669     |0.9277
|Outdoor2   |20.3430     |0.8384
|Outdoor3   |19.3627     |0.8027
|Outdoor4   |20.7741     |0.8561

### 사용자 가이드

[isp_pipeline.py](isp_pipeline.py)를 실행하여 프로젝트를 실행할 수 있습니다. 이것은 [configs.yml](config/configs.yml)에서 모든 알고리즘 파라미터를 로드하는 메인 파일입니다.
설정 파일에는 파이프라인에 구현된 각 모듈에 대한 태그가 포함되어 있습니다. 각 모듈에 대한 간략한 설명과 사용법은 다음과 같습니다:

#### 플랫폼

| platform            | 설명 |
| -----------         | --- |
| filename            | 파이프라인 실행을 위한 파일 이름을 지정합니다. 파일은 [in_frames/normal](in_frames/normal) 디렉토리에 위치해야 합니다
| disable_progress_bar| 시간이 소요되는 모듈에 대한 진행률 표시줄을 활성화하거나 비활성화합니다
| leave_pbar_string   | 완료 시 진행률 표시줄을 숨기거나 표시합니다

#### 센서 정보

| sensor Info   | 설명 |
| -----------   | --- |
| bayer_pattern | RAW 이미지의 베이어 패턴을 소문자로 지정합니다 <br> - `bggr` <br> - `rgbg` <br> - `rggb` <br> - `grbg`|
| range         | 사용되지 않음 |
| bit_depth        | RAW 이미지의 비트 깊이 |
| width         | 입력 RAW 이미지의 너비 |
| height        | 입력 RAW 이미지의 높이 |
| hdr           | 사용되지 않음 |

#### 크롭

| crop          | 설명 |
| -----------   | --- |
| is_enable      | 이 모듈을 활성화하거나 비활성화합니다. 활성화되면 베이어 패턴이 유지되는 경우에만 크롭합니다
| is_debug       | 모듈 디버그 로그를 출력하는 플래그
| new_width     | 크롭 후 입력 RAW 이미지의 새 너비
| new_height    | 크롭 후 입력 RAW 이미지의 새 높이

#### 불량 픽셀 보정

| dead_pixel_correction | 설명 |
| -----------           |   ---   |
| is_enable              | 이 모듈을 활성화하거나 비활성화합니다
| is_debug               | 모듈 디버그 로그를 출력하는 플래그
| dp_threshold          | DPC 모듈을 튜닝하기 위한 임계값. 임계값이 낮을수록 더 많은 픽셀이 불량으로 감지되어 보정됩니다

#### HDR 스티칭

구현 예정

#### 블랙 레벨 보정

| black_level_correction  | 설명 |
| -----------             |   ---   |
| is_enable                | 이 모듈을 활성화하거나 비활성화합니다
| r_offset                | 레드 채널 오프셋
| gr_offset               | Gr 채널 오프셋
| gb_offset               | Gb 채널 오프셋
| b_offset                | 블루 채널 오프셋
| is_linear                | 선형화를 활성화하거나 비활성화합니다. 활성화되면 BLC 오프셋은 0에 매핑되고 포화는 사용자가 지정한 최대 비트 범위에 매핑됩니다
| r_sat                   | 레드 채널 포화 레벨
| gr_sat                  | Gr 채널 포화 레벨
| gb_sat                  | Gb 채널 포화 레벨
| b_sat                   | 블루 채널 포화 레벨

#### 광전자 변환 함수

| OECF  | 설명 |
| -----------     |   ---   |
| is_enable        | 이 모듈을 활성화하거나 비활성화합니다
| r_lut           | OECF 곡선을 위한 룩업 테이블. 이 곡선은 대부분 센서에 따라 다르며 표준 기법을 사용한 캘리브레이션으로 구합니다

#### 디지털 게인

| digital_gain    | 설명 |
| -----------     |   ---   |
| is_enable        | 이것은 필수 모듈이며 비활성화할 수 없습니다
| is_debug         | 모듈 디버그 로그를 출력하는 플래그
| gain_array      | 게인 배열. 사용자는 여기에 나열된 게인 중 하나를 선택할 수 있습니다. 이 모듈은 AE 모듈과 함께 작동합니다 |
| current_gain    | 0부터 시작하는 현재 게인 인덱스 |

#### 렌즈 쉐이딩 캘리브레이션

구현 예정

#### 베이어 노이즈 감소

| bayer_noise_reduction   | 설명 |
| -----------             |   ---   |
| is_enable                | 활성화되면 사용자가 지정한 파라미터를 사용하여 베이어 도메인에서 노이즈를 감소시킵니다 |
| filt_window             | 홀수 윈도우 크기여야 합니다
| r_std_dev_s               | 레드 채널 가우시안 커널 강도. 강도가 높을수록 블러링이 강해집니다. 0이 될 수 없습니다
| r_std_dev_r               | 레드 채널 범위 커널 강도. 강도가 높을수록 에지가 더 잘 보존됩니다. 0이 될 수 없습니다
| g_std_dev_s               | Gr 및 Gb 가우시안 커널 강도
| g_std_dev_r               | Gr 및 Gb 범위 커널 강도
| b_std_dev_s               | 블루 채널 가우시안 커널 강도
| b_std_dev_r               | 블루 채널 범위 커널 강도


#### 화이트 밸런스

| white_balance           | 설명 |
| -----------             |   ---   |
| is_enable                | 활성화되면 사용자가 지정한 화이트 밸런스 게인을 적용합니다 |
| is_auto                  | true이면 3A - AWB를 활성화하고 사용자가 지정한 WB 게인을 사용하지 않습니다 |
| r_gain                  | 레드 채널 게인 |
| b_gain                  | 블루 채널 게인 |

#### 3A - 자동 화이트 밸런스 (AWB)
| auto_white_balance      | 설명 |
| -----------             |   ---   |
| is_debug         | 모듈 디버그 로그를 출력하는 플래그|
| underexposed_percentage   | AWB 게인 계산 전에 제외할 어두운 픽셀의 %를 설정합니다|
| overexposed_percentage    | AWB 게인 계산 전에 제외할 포화 픽셀의 %를 설정합니다|
| algorithm               | 다음 알고리즘 중 하나를 선택할 수 있습니다 <br> - `grey_world`  <br> - `norm_2`  <br> - `pca` |
| percentage              | [0 - 100] - PCA 알고리즘에서 어두운-밝은 픽셀 비율을 선택하는 파라미터 |

#### 색상 보정 매트릭스 (CCM)

| color_correction_matrix                 | 설명 |
| -----------                             |   ---   |
| is_enable                                | 활성화되면 사용자가 지정한 3x3 CCM을 3D RGB 이미지에 적용합니다 (행 합이 1인 규칙) |
| corrected_red                           | CCM의 1행
| corrected_green                         | CCM의 2행
| corrected_blue                          | CCM의 3행

#### 감마 보정
| gamma_correction        | 설명 |
| -----------             |   ---   |
| is_enable                | 활성화되면 LUT를 사용하여 톤 매핑 감마를 적용합니다 |
| gamma_lut_8                | 8비트 감마 곡선을 위한 룩업 테이블 |
| gamma_lut_10                | 10비트 감마 곡선을 위한 룩업 테이블 |
| gamma_lut_12               | 12비트 감마 곡선을 위한 룩업 테이블 |
| gamma_lut_14              | 14비트 감마 곡선을 위한 룩업 테이블 |

#### 3A - 자동 노출
| auto_exposure      | 설명
|--------------------|----------------------------------------------------------------------------------------------|
| is_enable           | 활성화되면 3A-자동 노출 알고리즘을 적용합니다                                         |
| is_debug            | 모듈 디버그 로그를 출력하는 플래그                                                             |
| center_illuminance | 왜도 계산을 위한 중심 조도 값, 0에서 255 사이. 기본값은 90 |
| histogram_skewness | 히스토그램 왜도 범위는 정확한 노출 계산을 위해 0에서 1 사이여야 합니다   |

#### 색공간 변환 (CSC)

| color_space_conversion | 설명                                                                             |
|------------------------|-------------------------------------------------------------------------------------|
| is_enable               | 이것은 필수 모듈이며 비활성화할 수 없습니다                                   |
| conv_standard          | 변환에 사용할 표준 <br> - `1` : Bt.709 HD <br> - `2` : Bt.601/407 |

#### 색상 채도 향상 (CSE)

| color_saturation_enhancement | 설명                                                                             |
|------------------------|-------------------------------------------------------------------------------------|
| is_enable               | 활성화되면 색상 채도 향상이 크로마 채널에 적용됩니다|                                  |
| saturation_gain         | 색상 채도를 얼마나 증가시킬지 제어하는 양의 실수 게인으로, 두 크로마 채널 모두에 적용됩니다 |

#### 대비 향상

| ldci       | 설명                                                                      |
|------------|----------------------------------------------------------------------------- |
| is_enable   | 활성화되면 Y 채널에 지역 동적 대비 향상이 적용됩니다  |
| clip_limit | 향상할 디테일의 양을 제어하는 클리핑 제한             |
| wind       | 필터를 적용할 윈도우 크기                                              |

#### 에지 향상 / 샤프닝

| Sharpening         | 설명                                           |
|--------------------|---------------------------------------------------|
| is_enable           | 활성화되면 샤프닝을 적용합니다 |
| sharpen_sigma      | 가우시안 필터의 표준 편차를 정의합니다 |
| sharpen_strength   | 고주파 성분에 적용되는 샤프닝 강도를 제어합니다  |


#### 2D 노이즈 감소

| 2d_noise_reduction | 설명                                           |
|--------------------|---------------------------------------------------|
| is_enable           | 활성화되면 2D 노이즈 감소를 적용합니다 |
| algorithm          | 다음 알고리즘 중 하나를 선택할 수 있습니다  <br> - `nlm`  <br> - `ebf` |
| window_size        | 비지역 평균 적용을 위한 검색 윈도우 크기   |
| patch_size         | 평균 필터 적용을 위한 패치 크기               |
| wts                | 스무딩 강도 파라미터                    |
| wind               | 엔트로피 기반 양방향 필터 적용을 위한 윈도우 크기           |
| sigma              | 엔트로피 기반 양방향 필터의 범위 및 공간 커널 파라미터                            |

#### 스케일링

| scale            | 설명 |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------
| is_enable         | 활성화되면 입력 이미지를 다운스케일합니다
| is_debug          | 모듈 디버그 로그를 출력하는 플래그
| new_width        | 출력 이미지의 다운스케일된 너비
| new_height       | 출력 이미지의 다운스케일된 높이
| is_hardware       | true이면 하드웨어 친화적인 다운스케일링 기법을 적용합니다. 이것은 3가지 입력 크기 중 하나에만 적용할 수 있으며 다음으로 다운스케일할 수 있습니다 <br> - `2592x1944` → `1920x1080` 또는 `1280x960` 또는 `1280x720` 또는 `640x480` 또는 `640x360`  <br> - `2592x1536` → `1280x720` 또는 `640x480` 또는 `640x360` <br> - `1920x1080` → `1280x720` 또는 `640x480` 또는 `640x360`  |
| algorithm             | 소프트웨어 친화적 스케일링. isHardware가 비활성화된 경우에만 사용 <br> - `Nearest_Neighbor` <br> - `Bilinear`
| upscale_method   | isHardware가 활성화된 경우에만 사용. 업스케일링 방법, 위 알고리즘 중 하나 사용 가능
| downscale_method | isHardware가 활성화된 경우에만 사용. 다운스케일링 방법, 위 알고리즘 중 하나 사용 가능

#### YUV 포맷
| yuv_conversion_format     | 설명                                                |
|---------------------------|--------------------------------------------------------|
| is_enable                  | 이 모듈을 활성화하거나 비활성화합니다                        |
| conv_type                 | YCbCr을 YUV로 변환할 수 있습니다 <br> - `444` <br> - `422` |


### FAQ
**왜 infiniteISP라고 이름 지었나요?**

ISP는 하드웨어에 종속적입니다. 하드웨어 제한으로 인해 알고리즘이 최고의 성능을 발휘하는 데 제한이 있습니다. InfiniteISP는 이러한 제한을 어느 정도 제거하고 알고리즘이 최상의 결과를 목표로 최대한의 잠재력을 발휘할 수 있도록 하는 것을 목표로 합니다.

**infiniteISP에 머신러닝을 포함하는 알고리즘도 포함되나요?**

네, 물론입니다. 이는 주로 머신러닝 모델이 기존 모델보다 훨씬 더 나은 결과를 제공하는 것으로 나타났기 때문입니다. 계획은 다음과 같습니다:

- `v0.x`부터 `v1.0`까지의 릴리스는 기존 레벨에서 기본 ISP 파이프라인을 구축하는 것을 포함합니다.

- `v1.0` 릴리스는 기존 레벨에서 구현된 모든 카메라 파이프라인 모듈을 갖게 됩니다. **이 릴리스는 주로 하드웨어 ISP로 쉽게 포팅될 수 있는 알고리즘을 포함할 것입니다**

- `v1.x.x` 릴리스는 `v2.0` 릴리스까지 이러한 기존 알고리즘의 모든 필요한 개선 사항을 포함할 것입니다

- `v2.0` 릴리스부터 infiniteISP는 특정 알고리즘에 대한 머신러닝 모델 구현을 시작할 것입니다.

- `v3.0` 릴리스에서 infiniteISP는 기존 알고리즘과 딥러닝 알고리즘 모두를 갖게 됩니다 (모든 파이프라인 모듈이 아닌 특정 모듈에 대해)

### 라이선스
이 프로젝트는 Apache 2.0 라이선스 하에 제공됩니다 ([LICENSE](LICENSE) 파일 참조).

### 감사의 글
- 이 프로젝트는 [cruxopen/openISP](https://github.com/cruxopen/openISP.git)에서 영감을 받아 시작되었습니다

### 오픈소스 ISP 목록
- [openISP](https://github.com/cruxopen/openISP.git)
- [Fast Open Image Signal Processor](https://github.com/QiuJueqin/fast-openISP.git)
- [AbdoKamel - simple-camera-pipeline](https://github.com/AbdoKamel/simple-camera-pipeline.git)
- [Mushfiqulalam - isp](https://github.com/mushfiqulalam/isp)
- [Karaimer - A Software Platform for Manipulating the Camera Imaging Pipeline](https://karaimer.github.io/camera-pipeline)
- [rawpy](https://github.com/letmaik/rawpy.git)


---

## 2. Infinite-ISP 참조 모델

## Infinite-ISP 참조 모델(Reference Model): 카메라 파이프라인 모듈의 RTL 구현을 위한 Python 기반 모델

### 개요
Infinite-ISP 참조 모델은 Infinite-ISP 파이프라인의 Python 기반 고정 소수점(fixed-point) 구현체입니다. 센서의 입력 RAW 이미지를 출력 RGB 이미지로 변환하도록 설계된 포괄적인 카메라 파이프라인 모듈 모음입니다. 이 모델은 파이프라인의 기능과 동작에 대한 엄격한 테스트, 검증 및 확인을 가능하게 하는 RTL 코드 생성을 돕는 참조 구현을 제공합니다.

이 모델은 Gaussian 및 Sigmoid와 같은 복잡한 함수에 룩업 테이블(LUT)을 사용하며, 나눗셈 및 제곱근에 대해 고정 소수점 숫자 또는 커스텀 근사치를 적용하여 이미지 품질 손실을 최소화하면서 최적화합니다.

현재 상태에서 이 모델은 모듈별로 단순한 알고리즘을 구현하고 있으며, 향후 버전에서는 RTL 친화적인 복잡한 알고리즘을 통합할 계획입니다.

![](docs/assets/infinite-isp-architecture.png)

`InfiniteISP_ReferenceModel v1.0`의 ISP 파이프라인

### 주요 내용

1. **RTL 친화적 코드**: 룩업 테이블, 커스텀 근사치 및 정수 연산과 같은 최적화를 통해 RTL로 직접 변환할 수 있는 카메라 파이프라인 모듈의 Python 구현을 제공합니다.

2. **데이터셋 처리**: 서로 다르거나 동일한 설정 파일을 사용하여 여러 이미지에 대해 실행할 수 있도록 지원합니다.

3. **비디오 처리**: 프레임 간에 작동하는 3A 통계(3A Statistics) 데이터가 흐르는 순차 프레임 처리가 가능한 비디오 처리 스크립트도 포함하고 있습니다.

### 목표
Infinite-ISP_ReferenceModel의 주요 목표는 카메라 파이프라인 모듈을 RTL 친화적인 구현으로 변환하는 과정을 간소화하는 오픈 소스 Python 기반 모델을 만드는 것입니다. 이를 통해 하드웨어 설계와의 원활한 통합을 가능하게 하고 효율적인 이미지 처리 시스템 개발을 단순화합니다. 최적화된 알고리즘과 비디오 처리 기능을 제공함으로써, 이 모델은 이미지 처리 프로젝트 및 RTL 구현을 담당하는 개발자들에게 귀중한 도구가 되는 것을 목표로 합니다.

## 기능 목록
아래 표는 모델의 기능 목록을 제공합니다. 모델 버전 `1.0`은 각 모듈에 대해 하드웨어 친화적이고 단순한 알고리즘을 구현합니다.

| 모듈 | Infinite-ISP_ReferenceModel 설명 | 
| -------------  | ------------- |         
| Crop | 베이어 패턴(Bayer pattern)을 고려하여 이미지를 자름 | 
| Dead Pixel Correction | 수정된 Yongji et al, Dynamic Defective Pixel Correction for Image Sensor 알고리즘 적용 |
| Black Level Correction | 캘리브레이션/센서 의존적 <br> - 튜닝 도구를 사용하여 조정 가능한 설정 파일의 매개변수 적용 |
| Optical Electronic Transfer Function (OECF) | 캘리브레이션/센서 의존적 <br> - 설정 파일의 LUT 구현 |
| Digital Gain | 설정 파일의 게인 값 적용 <br> - 자동 모드에서는 디지털 게인 선택을 위해 AE 피드백 통합 |
| Bayer Noise Reduction | Green Channel Guiding Denoising by Tan et al <br> - LUT를 통한 Chroma 및 Spatial 필터 구현 |
| Auto White Balance | 향상된 Gray World 알고리즘 <br> - 최적 임계값 내에서 AWB 통계 계산 |
| White Balance | WB 게인 곱셈 <br> - 튜닝 도구를 사용하여 조정 가능한 설정 파일의 매개변수 적용 |
| Demosaic | Malwar He Cutler’s 데모자이킹 알고리즘 |
| Color Correction Matrix | 캘리브레이션/센서 의존적 <br> - 튜닝 도구를 사용하여 조정 가능한 설정 파일의 3x3 CCM 적용 |
| Gamma Correction | 설정 파일의 LUT 구현 |
| Auto Exposure | Auto Exposure <br> - 왜도(skewness) 기반의 AE 통계 계산 |
| Color Space Conversion | YCbCr 디지털 <br> - BT 601 <br> - Bt 709 |
| Sharpening | 강도 조절이 가능한 단순한 언샤프 마스킹(unsharp masking) |
| Noise Reduction | Non-local means filter <br> - LUT를 통한 명암 레벨 차이 구현 |
| RGB Conversion | YCbCr 디지털 이미지를 RGB로 변환 |
| Invalid Region Crop | 이미지를 고정된 크기로 자름 |
| On Screen Display | 왼쪽 상단에 10x 로고 추가 | 
| Scale | Nearest Neighbor <br> - 정수 스케일링 |
| YUV Format | YUV <br> - 444 <br> - 422 |

### 의존성
이 프로젝트는 `Python_3.9.12`와 호환됩니다.

의존성 목록은 requirements.txt 파일에 나열되어 있습니다.

이 프로젝트는 pip 패키지 관리자가 설치되어 있다고 가정합니다.

### 실행 방법
파이프라인을 실행하려면 다음 단계를 따르세요.
1. 다음 명령어를 사용하여 저장소를 클론합니다.
```shell
git clone https://github.com/10xEngineersTech/Infinite-ISP_ReferenceModel
```

2. 다음 명령어를 실행하여 requirements 파일의 모든 요구 사항을 설치합니다.
```shell
pip install -r requirements.txt
```
3. isp_pipeline.py를 실행합니다.
```shell
python isp_pipeline.py
```

#### 예시
프로젝트의 in_frames/normal 폴더에 이미 튜닝된 설정이 포함된 몇 가지 샘플 이미지가 추가되어 있습니다. 이 중 하나를 실행하려면 설정 파일 이름을 제공된 샘플 설정 중 하나로 바꾸기만 하면 됩니다. 예를 들어 `Indoor1_2592x1536_12bit_RGGB.raw`에서 파이프라인을 실행하려면 isp_pipeline.py에서 설정 파일 이름과 데이터 경로를 다음과 같이 변경합니다.

```python
CONFIG_PATH = './config/Indoor1_2592x1536_12bit_RGGB-configs.yml'
RAW_DATA = './in_frames/normal/data'
```

### 다중 이미지/데이터셋에서 파이프라인 실행 방법
다중 이미지에서 Infinite-ISP를 실행하는 두 가지 스크립트가 있습니다.

1. isp_pipeline_dataset.py 
    <br >여러 이미지를 실행합니다. 각 RAW 이미지는 파일명이 `<filename>.raw`일 때 `<filename>-configs.yml`이라는 이름의 자체 설정 파일을 가져야 하며, 그렇지 않으면 기본 설정 파일인 configs.yml이 사용됩니다.

2. video_processing.py 
   <br> 데이터셋의 각 이미지를 순차적인 비디오 프레임으로 간주합니다. 모든 이미지는 configs.yml의 동일한 설정 매개변수를 사용하며, 한 프레임에서 계산된 3A 통계가 다음 프레임에 적용됩니다.

저장소를 클론하고 모든 의존성을 설치한 후 다음 단계를 따르세요.

1. `DATASET_PATH`를 데이터셋 폴더로 설정합니다. 예를 들어 이미지가 in_frames/normal/data 폴더에 있는 경우:
```python
DATASET_PATH = './in_frames/normal/data'
```

2. 데이터셋이 다른 git 저장소에 있는 경우, 루트 디렉토리에서 다음 명령어를 사용하여 서브모듈로 사용할 수 있습니다. 여기서 `<url>`은 git 저장소 주소이고, `<path>`는 서브모듈을 추가할 위치입니다. Infinite-ISP의 경우 `<path>`는 `./in_frames/normal/<dataset_name>`이어야 합니다. in_frames/normal/data 디렉토리가 이미 존재하므로 `<dataset_name>`은 `data`가 아니어야 함을 유의하세요.

```shell
git submodule add <url> <path>
git submodule update --init --recursive
``` 

4. git 저장소를 서브모듈로 추가한 후 isp_pipeline_dataset.py의 `DATASET_PATH` 변수를 `./in_frames/normal/<dataset_name>`으로 업데이트합니다. Git은 서브모듈을 사용하여 저장소의 하위 폴더만 가져오는 것을 허용하지 않습니다. 전체 저장소를 추가한 후 해당 폴더에 접근해야 합니다. 서브모듈의 하위 폴더에 있는 이미지를 사용하려면 isp_pipeline_dataset.py 또는 video_processing.py의 `DATASET_PATH` 변수를 그에 맞게 수정하세요.

```python
DATASET_PATH = './in_frames/normal/<dataset_name>'
```

5. `isp_pipeline_dataset.py` 또는 `video_processing.py`를 실행합니다.
6. 처리된 이미지는 out_frames 폴더에 저장됩니다.

### 기여하기
풀 리퀘스트(Pull Request)를 보내기 전에 기여 가이드라인을 읽어주시기 바랍니다.

### 결과
다음은 시장 경쟁력이 있는 ISP와 이 파이프라인의 결과를 비교한 것입니다.
우리 ISP의 출력은 오른쪽에 표시되어 있으며, 기준이 되는 그라운드 트루스(ground truths)는 왼쪽에 표시되어 있습니다.

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **그라운드 트루스** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **infiniteISP_RM** 
!
!
!
!
!

PSNR 및 SSIM 이미지 품질 메트릭을 기반으로 한 위 결과의 비교표입니다.

| 이미지 | PSNR | SSIM |
|-----------|-------|-------|
| Indoor1 | 22.5788 | 0.8923 |
| Outdoor1 | 19.1544 | 0.9048 |
| Outdoor2 | 18.8681 | 0.8071 |
| Outdoor3 | 17.2825 | 0.7304 |
| Outdoor4 | 19.9814 | 0.8198 |

### 사용자 가이드
더 포괄적인 알고리즘 문서와 Python 모델 사용 방법을 이해하려면 사용자 가이드를 방문하세요.

### 라이선스
이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다 (LICENSE 파일 참조).

### 연락처
문의 사항이나 피드백이 있으시면 언제든지 연락해 주시기 바랍니다.

이메일: isp@10xengineers.ai
웹사이트: http://www.10xengineers.ai
링크드인: https://www.linkedin.com/company/10x-engineers/

---

## 3. Infinite-ISP RTL

## Infinite-ISP RTL

Infinite-ISP_RTL은 Infinite-ISP(이미지 신호 처리기)를 위한 RTL 개발을 포함하는 프로젝트입니다. 이 저장소는 [Infinite-ISP_ReferenceModel](https://github.com/10x-Engineers/Infinite-ISP_ReferenceModel) (RM)을 참조로 사용하며, 참조 모델의 비트 단위까지 정확한(bit-accurate) 변환을 보장합니다. 이러한 워크플로우는 하드웨어 설계와 알고리즘 개발 분야 모두의 전문 지식 통합을 용이하게 합니다. 참조 모델(RM)의 각 블록은 RTL 저장소 내의 해당 Verilog 모듈에 매핑됩니다. FPGA 통합 및 재사용성 향상을 위해 이러한 모듈은 ISP와 VIP의 두 그룹으로 분류됩니다.

![](doc/assets/Infinite-ISP_v1.0-pipeline.png)

`Infinite-ISP_RTL v1.0`의 ISP RTL 파이프라인

### 목표
인터넷에는 많은 오픈 소스 ISP들이 존재합니다. 대부분은 개별 기여자들에 의해 개발되었으며 각기 장단점이 있습니다. 또한, 일반적으로 소프트웨어 기반이며 RTL 지원이 부족한 경우가 많습니다. 이 프로젝트는 모든 오픈 소스 ISP 개발을 한곳으로 집중시켜, ISP 개발자들이 알고리즘 개발부터 FPGA 및 ASIC 준비를 위한 후속 단계까지 기여할 수 있는 단일 플랫폼을 제공하는 것을 목표로 합니다.

### 액세스 권한을 얻는 방법
액세스하려면 **링크**의 요청 양식을 작성해 주세요. 10xEngineers에서 영업일 기준 1일 이내에 저장소 액세스 권한을 승인해 드립니다. 액세스 상태를 확인하는 이메일 알림을 받게 됩니다.

### 리소스 사용률

아래는 Xilinx® Vivado IDE v2022.1을 사용하여 Xilinx® Kria KV260 개발 보드용으로 컴파일된 리소스 사용률 표입니다.

**ISP 리소스 사용률 (2048x1536 해상도):**

| 블록 이름 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | LUT | FF | BRAM | DSP |
| ------------------- | :---------: | :---------: | :---------: | :---------: |
| Crop | 159 | 144 | 0 | 0 |
| DPC | 652 | 642 | 4 | 0 |
| BLC | 117 | 120 | 0 | 4 |
| OECF | 37 | 62 | 2 | 0 |
| DG | 250 | 17 | 0 | 1 |
| BNR | 10087 | 6567 | 20 | 25 |
| WB | 33 | 44 | 0 | 1 |
| Demosaic | 739 | 628 | 4 | 0 |
| AE | 2308 | 2242 | 0 | 5 |
| AWB | 803 | 922 | 1 | 0 |
| CCM | 136 | 263 | 0 | 9 |
| GC | 31 | 67 | 1.5 | 0 |
| CSC | 281 | 387 | 0 | 13 |
| 2DNR | 23210 | 4403 | 8 | 0 |
| isp_top | 38771 | 16694 | 40.5 | 58 |

**VIP 리소스 사용률 (2048x1536 해상도):**

| 블록 이름 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | LUT | FF | BRAM | DSP |
| ------------------- | :---------: | :---------: | :---------: | :---------: |
| RGBC | 388 | 231 | 0 | 0 |
| IRC | 124 | 42 | 0 | 0 |
| Scale | 381 | 184 | 0 | 0 |
| OSD | 1021 | 532 | 1 | 0 |
| YUV Conv | 31 | 54 | 0 | 0 |
| vip_top | 1983 | 1251 | 1 | 0 |

**ISP 파이프라인 리소스 사용률 (2048x1536 해상도):**

| 블록 이름 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | LUT | FF | BRAM | DSP |
| ------------------- | :---------: | :---------: | :---------: | :---------: |
| isp_top + vip_top | 40754 | 17945 | 41.5 | 58 |

### 라이선스
이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다 (LICENSE 파일 참조).

### 감사의 글
- Infinite-ISP_RTL 프로젝트는 bxinquan/zynqmp_cam_isp_demo로부터 영감을 받아 시작되었습니다.

### 연락처
문의 사항이나 피드백이 있으시면 언제든지 연락해 주시기 바랍니다.

이메일: isp@10xengineers.ai
웹사이트: http://www.10xengineers.ai
링크드인: https://www.linkedin.com/company/10x-engineers/

---

## 4. Infinite-ISP FPGA Binaries

## Infinite-ISP FPGA Binaries
[Xilinx® Kria™ KV260 비전 AI 스타터 키트](./binaries/xilinx_xck26) 및 [Efinix® Titanium Ti180 J484 개발 키트](./binaries/efinix_ti180)를 위한 Infinite-ISP 이미지 신호 처리(ISP) 파이프라인 FPGA 바이너리입니다. 각 바이너리 파일은 FPGA 비트스트림과 그에 대응하는 펌웨어 실행 파일로 구성되어 있습니다.

### 디렉토리 구조

- 이 저장소의 디렉토리 구조는 다음과 같습니다:
```plaintext
메인 디렉토리(Infinite-ISP_FPGABinaries)
│
├── binaries
│   ├── xilinx_xck26
│   └── efinix_ti180
│         
│
├── doc
│   ├── xilinx_xck26
│   ├── efinix_ti180
│   ├── assets
│   └── user_guide
│  
│   
├── scripts
    ├── xilinx_xck26
    └── efinix_ti180
```
* **binaries**: Xilinx® Kria™ KV260 비전 AI 스타터 키트 및 Efinix® Titanium Ti180 J484 개발 키트를 위한 바이너리 파일을 포함합니다.
* **doc**: 사용자 가이드 및 구성 메뉴를 포함합니다.
* **scripts**: 파일 변환을 위한 Python 스크립트를 포함합니다.

### 라이선스
이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다 ([LICENSE](LICENSE) 파일 참조).

### 연락처
문의 사항이나 피드백이 있으시면 언제든지 연락해 주시기 바랍니다.

이메일: isp@10xengineers.ai

웹사이트: http://www.10xengineers.ai

링크드인: https://www.linkedin.com/company/10x-engineers/

---

## 5. Infinite-ISP Firmware

## Infinite-ISP_Firmware
Xilinx® Kria™ KV260 비전 AI 스타터 키트에 탑재된 XCK26 Zynq® UltraScale+™ MPSoC용 Infinite-ISP 이미지 신호 처리(ISP) 파이프라인 펌웨어입니다.

곧 출시 예정입니다!

### 연락처
문의 사항이나 피드백이 있으시면 언제든지 연락해 주시기 바랍니다.

이메일: isp@10xengineers.ai

웹사이트: http://www.10xengineers.ai

링크드인: https://www.linkedin.com/company/10x-engineers/

---

## 6. Infinite-ISP Tuning Tool

## Infinite-ISP Tuning Tool
### 개요

Infinite-ISP Tuning Tool은 [Infinite-ISP_ReferenceModel](https://github.com/10xEngineersTech/Infinite-ISP_ReferenceModel) 및 [Infinite-ISP_Firmware](https://github.com/10xEngineersTech/Infinite-ISP_Firmware)의 다양한 모듈을 튜닝하기 위해 특별히 설계된 콘솔 기반 ISP(이미지 신호 처리기) 튜닝 애플리케이션입니다. Infinite-ISP 파이프라인과 함께 작동하는 것 외에도, 이 튜닝 도구는 이미지 품질 분석을 수행하기 위한 독립형 애플리케이션으로도 사용할 수 있습니다.

이 교차 플랫폼(cross-platform) 애플리케이션은 이미지 센서에서 직접 들어오는 Bayer RAW 이미지를 캘리브레이션하기 위한 다양한 알고리즘을 제공합니다.


![](docs/assets/Tuning_Tool_Block_Diagram.png)


### 사용법

Tuning Tool은 Infinite-ISP_ReferenceModel 및 Infinite-ISP_Firmware와 함께 작동하도록 설계되었습니다. Infinite-ISP_ReferenceModel의 설정 파일을 사용하고, 캘리브레이션을 수행하며, 파이프라인에서 사용할 수 있는 튜닝된 매개변수로 설정 파일을 업데이트합니다. 자세한 내용은 [사용자 가이드](https://github.com/10xEngineersTech/Infinite-ISP_TuningTool/blob/white_balance_update/docs/Tuning%20Tool%20User%20Guide.pdf)를 참조하세요.

Infinite-ISP Tuning Tool은 이미지 품질 분석을 위한 독립형 애플리케이션으로 별도로 사용할 수 있습니다. 이 포괄적인 도구 세트는 사용자에게 캘리브레이션 모듈에 대한 정밀한 제어를 제공할 뿐만 아니라, 분석 모듈을 사용하여 이미지의 품질을 분석할 수 있게 해줍니다. 사용 용도에 따라 다음과 같이 세 가지 범주로 나뉩니다:

- 캘리브레이션 도구 (Calibration Tools)

- 분석 도구 (Analysis Tools)

- 설정 파일 생성기 (Configuration Files Generator)

### 주요 기능
Infinite-ISP Tuning Tool은 다음과 같은 기능을 제공합니다.

| 모듈 | 설명 |
| ----------------- | ------------------------------------------------------------------ |
| Black Level Calibration (BLC) | 각 채널(R, Gr, Gb, B)에 대한 RAW 이미지의 블랙 레벨을 계산합니다. |
| White Balance (WB) | ColorChecker RAW 또는 RGB 이미지에서 화이트 밸런스 게인(R 게인 및 B 게인)을 계산합니다. |
| Color Correction Matrix (CCM) | ColorChecker RAW 또는 RGB 이미지를 사용하여 3x3 색 보정 행렬을 계산합니다. |
| Gamma | 사용자 정의 감마 곡선을 sRGB 색 공간 감마(≈ 2.2)와 비교합니다. |
| Bayer Noise Level Estimation | ColorChecker RAW 이미지에서 6개 그레이스케일 패치의 노이즈 레벨을 추정합니다. |
| Luminance Noise Level Estimation | ColorChecker RAW 또는 RGB 이미지에서 6개 그레이스케일 패치의 휘도 노이즈 레벨을 추정합니다. |
| Configuration Files | Infinite-ISP_ReferenceModel 및 FPGA 펌웨어를 위한 설정 파일을 생성합니다. |



### 시작하기

#### 사전 요구 사항
이 프로젝트는 `Python_3.10.11`과 호환됩니다. <br>
<br>의존성 목록은 requirements.txt 파일에 나열되어 있습니다. <br>
<br>이 프로젝트는 pip 패키지 관리자가 설치되어 있다고 가정합니다. <br>
#### 도구 설정
Tuning Tool을 사용하려면 다음 단계를 따르세요:
- 다음 명령어를 사용하여 저장소를 클론합니다:
    ```shell
    git clone https://github.com/10xEngineersTech/InfiniteISP_TuningTool.git
    ```

- 다음 명령어를 실행하여 requirements 파일의 모든 요구 사항을 설치합니다:
    ```shell
    pip install -r requirements.txt
    ```


#### 실행 방법
저장소를 클론하고 모든 의존성을 설치한 후 다음 단계를 따르세요:

- 터미널을 열고 프로젝트 디렉토리로 이동합니다.

- 다음 명령어를 실행하여 Python으로 tuning_tool.py 파일을 실행합니다:
    ```shell
    python tuning_tool.py
    ```
    
위의 단계를 따르면 도구가 시작되고 콘솔이 지워지며 환영 메시지가 표시됩니다.
#### 예시
Tuning Tool을 성공적으로 실행하면 사용 가능한 모든 모듈 목록이 포함된 메인 메뉴가 나타납니다.

!

- 특정 모듈을 실행하려면 위아래 화살표 버튼을 사용하여 메뉴에서 해당 옵션을 선택하기만 하면 됩니다. 예를 들어, 블랙 레벨 캘리브레이션(BLC) 모듈을 시작하려면 옵션 1을 선택합니다.

- 각 모듈의 첫 번째 단계는 해당 모듈의 특정 기능과 요구 사항을 설명하는 메인 메뉴를 표시하는 것입니다. 메뉴는 모듈과 관련된 캘리브레이션 또는 분석을 수행하기 위한 필요한 단계와 옵션을 안내합니다.

- 각 모듈은 고유한 기능에 따라 서로 다른 요구 사항과 하위 메뉴를 가집니다. 필요한 입력이 제공되면 해당 모듈 전용 알고리즘이 실행됩니다.

 - 모듈이 완료되면 해당 모듈을 다시 시작하거나, 메인 메뉴로 돌아가서 다른 모듈을 선택하거나, Tuning Tool을 종료할 수 있는 옵션이 제공됩니다. 이를 통해 여러 모듈을 편리하게 탐색하고 미세 조정할 수 있습니다.


### 기여하기

풀 리퀘스트(Pull Request)를 보내기 전에 기여 가이드라인을 읽어주시기 바랍니다.

### 사용자 가이드
더 포괄적인 문서와 Tuning Tool을 효과적으로 사용하는 방법을 이해하려면 사용자 가이드를 방문하세요. 

### 라이선스
이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다 (LICENSE 파일 참조).


### 연락처
문의 사항이나 피드백이 있으시면 언제든지 연락해 주시기 바랍니다.

이메일: isp@10xengineers.ai

웹사이트: http://www.10xengineers.ai

링크드인: https://www.linkedin.com/company/10x-engineers/

---

