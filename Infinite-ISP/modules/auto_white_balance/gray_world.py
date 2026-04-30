"""
File: gray_world.py
Description: Implementation of Gray_World - an AWB Algorithm
             (단순 평균 알고리즘: 이미지 전체 픽셀의 단순 산술 평균값을 구해 화면의 흰색 균형을 맞춤)
Code / Paper  Reference: https://www.sciencedirect.com/science/article/abs/pii/0016003280900587
Author: 10xEngineers

"""
import numpy as np


class GrayWorld:
    """
    Gray World 화이트 밸런스:
    RGB 채널들의 단순 평균값을 계산하여 화이트 밸런스 게인(G/R 및 G/B)을 구하는 알고리즘
    """

    def __init__(self, flatten_img):
        self.flatten_img = flatten_img

    def calculate_gains(self):
        """
        R, G, B 채널의 평균값을 사용하여 화이트 밸런스 게인을 계산함
        """
        avg_rgb = np.mean(self.flatten_img, axis=0)

        # 평균 RGB 값으로부터 G/R, G/B 화이트 밸런스 게인을 계산함
        # 값이 없을 경우(nan) 0으로 처리함
        rgain = np.nan_to_num(avg_rgb[1] / avg_rgb[0])
        bgain = np.nan_to_num(avg_rgb[1] / avg_rgb[2])

        return rgain, bgain
