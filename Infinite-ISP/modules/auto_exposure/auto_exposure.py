"""
File: auto_exposure.py
Description: 3A-AE 반복문을 통해 자동 노출 알고리즘 실행
Code / Paper  Reference: https://www.atlantis-press.com/article/25875811.pdf
                         http://tomlr.free.fr/Math%E9matiques/Math%20Complete/Probability%20and%20statistics/CRC%20-%20standard%20probability%20and%20Statistics%20tables%20and%20formulae%20-%20DANIEL%20ZWILLINGER.pdf
Author: 10xEngineers Pvt Ltd
------------------------------------------------------------
"""
import time
import numpy as np


class AutoExposure:
    """
    자동 노출 모듈
    """

    def __init__(self, img, sensor_info, parm_ae):
        self.img = img
        self.enable = parm_ae["is_enable"]
        self.is_debug = parm_ae["is_debug"]
        self.center_illuminance = parm_ae["center_illuminance"]
        self.histogram_skewness_range = parm_ae["histogram_skewness"]
        self.sensor_info = sensor_info
        self.param_ae = parm_ae
        self.bit_depth = sensor_info["bit_depth"]

        # AE 피드백 루프에 포함된 파이프라인 모듈들
        # wb(화이트 밸런스) 모듈의 이름이 wbc(화이트 밸런스 보정)로 변경됨
        # gc(감마 보정) 모듈의 이름이 gcm(감마 보정 모듈)으로 변경됨

    def get_exposure_feedback(self):
        """
        디지털 게인을 조절하여 올바른 노출값 구하기
        """
        # AE 계산을 위해 이미지를 8비트로 변환
        self.img = self.img >> (self.bit_depth - 8)
        self.bit_depth = 8

        # 노출 지표 계산
        return self.determine_exposure()

    def determine_exposure(self):
        """
        히스토그램의 휘도 왜도를 이용한 이미지 노출 추정
        """

        # plt.imshow(self.img)
        # plt.show()

        # 휘도 히스토그램을 위해 먼저 이미지를 그레이스케일(흑백)로 변환함
        # AE-통계로 사용되는 이미지의 평균 휘도값도 반환함
        grey_img, avg_lum = self.get_greyscale_image(self.img)
        print("Average luminance is = ", avg_lum)

        # AE 통계를 위한 히스토그램 왜도 계산
        skewness = self.get_luminance_histogram_skewness(grey_img)

        # 범위 가져오기
        upper_limit = self.histogram_skewness_range
        lower_limit = -1 * upper_limit

        if self.is_debug:
            print("   - AE - Histogram Skewness Range = ", upper_limit)

        # 왜도가 범위 내에 있는지 확인
        if skewness < lower_limit:
            return -1
        elif skewness > upper_limit:
            return 1
        else:
            return 0

    def get_greyscale_image(self, img):
        """
        이미지를 그레이스케일로 변환
        """
        # 휘도를 얻기 위해 각 RGB 픽셀에 [0.299, 0.587, 0.144]를 곱함
        grey_img = np.clip(
            np.dot(img[..., :3], [0.299, 0.587, 0.144]), 0, (2**self.bit_depth)
        ).astype(np.uint16)
        return grey_img, np.average(grey_img, axis=(0, 1))

    def get_luminance_histogram_skewness(self, img):
        """
        왜도 계산 참조 문헌:
        Zwillinger, D. and Kokoska, S. (2000). CRC Standard Probability and Statistics
        Tables and Formulae. Chapman & Hall: New York. 2000. Section 2.2.24.1
        """

        # 왜도를 계산하기 위해 먼저 중심 휘도를 뺌
        img = img.astype(np.float64) - self.center_illuminance

        # 표본 왜도는 피셔-피어슨 왜도 계수로 계산됨, 
        # 즉 (m_3 / m_2**(3/2)) * g_1
        # 여기서 m_2는 2차 모멘트(분산)이고 m_3는 3차 모멘트 왜도임

        img_size = img.size
        m_2 = np.sum(np.power(img, 2)) / img_size
        m_3 = np.sum(np.power(img, 3)) / img_size

        g_1 = np.sqrt(img_size * (img_size - 1)) / (img_size - 2)
        skewness = np.nan_to_num((m_3 / abs(m_2) ** (3 / 2)) * g_1)

        if self.is_debug:
            print("   - AE - Histogram Skewness = ", skewness)

        return skewness

    def execute(self):
        """
        자동 노출 실행
        """
        print("Auto Exposure= " + str(self.enable))

        if self.enable is False:
            return None
        else:
            start = time.time()
            ae_feedback = self.get_exposure_feedback()
            print(f"  Execution time: {time.time()-start:.3f}s")
            return ae_feedback
