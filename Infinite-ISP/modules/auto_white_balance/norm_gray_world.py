"""
File: norm_2.py
Description: Implementation of Norm GrayWorld - an AWB Algorithm
             (가중치 평균 알고리즘: 각 픽셀 값에 Norm-2를 적용하여 강렬한 색상에 가중치를 두어 평균을 계산함)
Code / Paper  Reference: https://www.sciencedirect.com/science/article/abs/pii/0016003280900587
Author: 10xEngineers

"""
import numpy as np


class NormGrayWorld:
    """
    Norm 2 Gray World 화이트 밸런스:
    RGB 채널들의 평균값을 계산하여 화이트 밸런스 게인(G/R 및 G/B)을 구함.
    이때 각 채널의 평균값은 단순 평균이 아닌 Norm-2(제곱합의 제곱근) 방식으로 계산됨.
    """

    def __init__(self, flatten_img):
        self.flatten_img = flatten_img

    def calculate_gains(self):
        """
        R, G, B 채널의 Norm 평균값을 사용하여 화이트 밸런스 게인을 계산함
        """
        avg_rgb = np.linalg.norm(self.flatten_img, axis=0)

        # Norm 평균 RGB 값으로부터 G/R, G/B 화이트 밸런스 게인을 계산함
        # 값이 없을 경우(nan) 0으로 처리함
        rgain = np.nan_to_num(avg_rgb[1] / avg_rgb[0])
        bgain = np.nan_to_num(avg_rgb[1] / avg_rgb[2])

        return rgain, bgain
