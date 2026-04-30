import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

# 타겟 폴더 경로
folder_path = "/home/mini/isp/Infinite/Infinite-ISP/in_frames/normal/"

# 폴더 내의 모든 .raw 파일 찾기
raw_files = glob.glob(os.path.join(folder_path, "*.raw"))

if not raw_files:
    print("해당 폴더에 RAW 파일이 존재하지 않습니다.")
    exit()

print(f"총 {len(raw_files)}개의 RAW 파일을 찾았습니다. 창을 닫으면 다음 사진이 열립니다.\n")

for file_path in raw_files:
    filename = os.path.basename(file_path)
    
    # 파일명 기반으로 해상도 및 비트 심도 추론 (기본값 세팅)
    width = 2592
    height = 1536
    bit_depth = 12
    
    # 파일명에서 '가로x세로_숫자bit' 패턴 찾기
    res_match = re.search(r'(\d+)x(\d+)_(\d+)bit', filename, re.IGNORECASE)
    if res_match:
        width = int(res_match.group(1))
        height = int(res_match.group(2))
        bit_depth = int(res_match.group(3))
        
    print(f"이미지 여는 중: {filename} (해상도: {width}x{height}, Bit: {bit_depth})")

    try:
        # 비트 심도에 따라 읽어오는 데이터 크기 지정 (12-bit는 16-bit 정수로 읽음)
        if bit_depth > 8:
            raw_data = np.fromfile(file_path, dtype=np.uint16)
        else:
            raw_data = np.fromfile(file_path, dtype=np.uint8)

        # 1차원 데이터를 2차원(세로 x 가로) 이미지 형태로 변환
        raw_image = raw_data.reshape((height, width))

        # 화면에 렌더링
        plt.figure(figsize=(10, 6))
        plt.imshow(raw_image, cmap='gray')
        plt.title(f"{filename}\n({width}x{height}, {bit_depth}-bit)")
        plt.colorbar(label='Pixel Value')
        
        # 블로킹 모드로 띄워서 창을 닫아야 다음 사진으로 넘어가게 함
        plt.show(block=True)
        
    except ValueError:
        print(f" ❌ 오류: {filename} 의 파일 크기가 {width}x{height} 해상도와 맞지 않습니다.")
    except Exception as e:
        print(f" ❌ 오류 발생: {e}")
