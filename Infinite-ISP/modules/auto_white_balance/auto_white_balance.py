"""
File: auto_white_balance.py
Description: 3A - AWB Runs the AWB algorithm based on selection from config file
             (AWB 메인 컨트롤러: configs.yml 설정에 따라 하위 알고리즘을 선택하고 전처리를 수행하여 최종 게인값을 계산함)
Code / Paper  Reference: https://www.sciencedirect.com/science/article/abs/pii/0016003280900587
                         https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/12/1/art00008
                         https://opg.optica.org/josaa/viewmedia.cfm?uri=josaa-31-5-1049&seq=0
Author: 10xEngineers Pvt Ltd
------------------------------------------------------------
"""
import time
import numpy as np
from modules.auto_white_balance.gray_world import GrayWorld as GW
from modules.auto_white_balance.norm_gray_world import NormGrayWorld as NGW
from modules.auto_white_balance.pca import PCAIlluminEstimation as PCA


class AutoWhiteBalance:
    """
    자동 화이트 밸런스(AWB) 모듈
    """

    def __init__(self, raw, sensor_info, parm_awb):

        self.raw = raw

        self.sensor_info = sensor_info
        self.parm_awb = parm_awb
        self.enable = parm_awb["is_enable"]
        self.bit_depth = sensor_info["bit_depth"]
        self.is_debug = parm_awb["is_debug"]
        self.underexposed_percentage = parm_awb["underexposed_percentage"]
        self.overexposed_percentage = parm_awb["overexposed_percentage"]
        self.flatten_img = None
        self.bayer = self.sensor_info["bayer_pattern"]
        # self.img = img
        self.algorithm = parm_awb["algorithm"]

    def determine_white_balance_gain(self):
        """
        AWB 알고리즘을 사용하여 Raw 이미지에 적용할 화이트 밸런스 게인값을 결정함
        """

        max_pixel_value = 2**self.bit_depth
        approx_percentage = max_pixel_value / 100
        # 화이트 밸런스 게인 계산의 정확도를 위해 노출 과다 및 노출 부족 픽셀을 제거함
        overexposed_limit = (
            max_pixel_value - (self.overexposed_percentage) * approx_percentage
        )
        underexposed_limit = (self.underexposed_percentage) * approx_percentage

        if self.is_debug:
            print("   - AWB - Underexposed Pixel Limit = ", underexposed_limit)
            print("   - AWB - Overexposed Pixel Limit  = ", overexposed_limit)

        if self.bayer == "rggb":

            r_channel = self.raw[0::2, 0::2]
            gr_channel = self.raw[0::2, 1::2]
            gb_channel = self.raw[1::2, 0::2]
            b_channel = self.raw[1::2, 1::2]

        elif self.bayer == "bggr":
            b_channel = self.raw[0::2, 0::2]
            gb_channel = self.raw[0::2, 1::2]
            gr_channel = self.raw[1::2, 0::2]
            r_channel = self.raw[1::2, 1::2]

        elif self.bayer == "grbg":
            gr_channel = self.raw[0::2, 0::2]
            r_channel = self.raw[0::2, 1::2]
            b_channel = self.raw[1::2, 0::2]
            gb_channel = self.raw[1::2, 1::2]

        elif self.bayer == "gbrg":
            gb_channel = self.raw[0::2, 0::2]
            b_channel = self.raw[0::2, 1::2]
            r_channel = self.raw[1::2, 0::2]
            gr_channel = self.raw[1::2, 1::2]

        g_channel = (gr_channel + gb_channel) / 2
        bayer_channels = np.dstack((r_channel, g_channel, b_channel))
        # print(bayer_channels.shape)

        bad_pixels = np.sum(
            np.where(
                (bayer_channels < underexposed_limit)
                | (bayer_channels > overexposed_limit),
                1,
                0,
            ),
            axis=2,
        )
        self.flatten_img = bayer_channels[bad_pixels == 0]
        # print(self.flatten_raw.shape)

        if self.algorithm == "norm_2":
            rgain, bgain = self.apply_norm_gray_world()
        elif self.algorithm == "pca":
            rgain, bgain = self.apply_pca_illuminant_estimation()
        else:
            rgain, bgain = self.apply_gray_world()

        # r_gain과 b_gain이 정상 범위를 벗어나는지 확인 (항상 1 이상이어야 함)
        rgain = 1 if rgain <= 1 else rgain
        bgain = 1 if bgain <= 1 else bgain

        if self.is_debug:
            print("   - AWB Actual Gains: ")
            print("   - AWB - RGain = ", rgain)
            print("   - AWB - Bgain = ", bgain)

        return rgain, bgain

    def apply_gray_world(self):
        """
        Gray World 화이트 밸런스:
        RGB 채널들의 평균값을 이용해 화이트 밸런스 게인(G/R 및 G/B)을 계산함
        """

        gwa = GW(self.flatten_img)
        return gwa.calculate_gains()

    def apply_norm_gray_world(self):
        """
        Norm 2 Gray World 화이트 밸런스:
        RGB 채널들의 평균값을 이용해 화이트 밸런스 게인(G/R 및 G/B)을 계산함.
        각 채널의 평균값은 일반적인 평균이 아닌 Norm-2를 이용해 구함.
        """

        ngw = NGW(self.flatten_img)
        return ngw.calculate_gains()

    def apply_pca_illuminant_estimation(self):
        """
        PCA 조명 추정 (Illuminant Estimation):
        이 알고리즘은 색상 분포로부터 조명값을 직접 추정함.
        색상 분포 상의 투영 거리(projection distance)를 이용해 밝은 픽셀과 어두운 픽셀을 선택한 후,
        주성분 분석(PCA)을 적용하여 조명의 방향을 추정하는 방식.
        """
        pixel_percentage = self.parm_awb["percentage"]
        pca = PCA(self.flatten_img, pixel_percentage)
        return pca.calculate_gains()

    def execute(self):
        """
        자동 화이트 밸런스 모듈 실행
        """
        print("Auto White balancing = " + str(self.enable))

        # 이 모듈은 화이트 밸런스의 'is_enable'과 'is_auto' 파라미터가 모두 True일 때만 활성화됨.
        if self.enable is True:
            start = time.time()
            rgain, bgain = self.determine_white_balance_gain()
            print(f"  Execution time: {time.time() - start:.3f}s")
            return np.array([rgain, bgain])
        return None
