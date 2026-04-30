"""
File: pca.py
Description: Implementation of PCA Illuminant Estimation - an AWB Algorithm
             (주성분 분석 알고리즘: 색상 분포에 PCA를 적용하여 조명의 방향성을 수학적으로 직접 추정해 냄)
Code / Paper  Reference: https://www.sciencedirect.com/science/article/abs/pii/0016003280900587
Author: 10xEngineers

"""
import numpy as np


class PCAIlluminEstimation:
    """
    PCA 조명 추정 (Illuminant Estimation):
    이 알고리즘은 색상 분포로부터 조명값을 직접 추정함.
    색상 분포 내 투영 거리를 이용해 밝은 픽셀과 어두운 픽셀을 선택한 후,
    주성분 분석(PCA)을 적용하여 조명의 방향성을 추정하는 수학적 방식.
    """

    def __init__(self, flatten_img, pixel_percentage):
        self.flatten_img = flatten_img
        self.pixel_percentage = pixel_percentage

    def calculate_gains(self):
        """
        R, G, B 채널에 PCA를 적용하여 화이트 밸런스 게인을 계산함
        """

        # 색상 분포 정보만 얻기 위해, 이미지를 N x 3 (N = 가로 * 세로 픽셀수) 크기의 평면 배열로 폄
        flat_img = self.flatten_img  # .flatten().reshape(-1,3)
        size = len(flat_img)

        # mean_vector는 평균 RGB 벡터를 자신의 크기(magnitude)로 나누어 구한 방향 벡터임.
        mean_rgb = np.mean(flat_img, axis=0)
        mean_vector = mean_rgb / np.linalg.norm(mean_rgb)

        # 밝고 어두운 픽셀을 구분하기 위해, 데이터가 평균 방향 벡터에 투영된 거리를 먼저 계산함.
        data_p = np.sum(flat_img * mean_vector, axis=1)

        # 밝고 어두운 픽셀 양끝값을 구하기 위해 투영 거리 배열을 오름차순으로 정렬함.
        sorted_data = np.argsort(data_p)

        # pixel_percentage 파라미터를 기준으로, 필터링할 밝은/어두운 픽셀의 개수를 계산함.
        index = int(np.ceil(size * (self.pixel_percentage / 100)))

        # 가장자리 양끝에 해당하는 밝은/어두운 픽셀의 인덱스만 획득함.
        filtered_index = np.concatenate(
            (sorted_data[0:index], sorted_data[-index:None])
        )
        # 위에서 얻은 인덱스를 바탕으로 원본 데이터 배열에서 실제 픽셀값들만 추출함.
        filtered_data = flat_img[filtered_index, :].astype(np.float32)

        # PCA(주성분 분석)를 위해 추출된 픽셀 데이터 행렬의 전치 행렬과 자기 자신의 내적(Dot product)을 구하여,
        # 3x3 크기의 공분산 행렬(sigma)을 만듦.
        sigma = np.dot(filtered_data.transpose(), filtered_data)

        # 3x3 행렬(sigma)의 고유값(Eigenvalues)과 고유벡터(Eigenvectors)를 계산함.
        eig_value, eig_vector = np.linalg.eig(sigma)

        # 이 중 가장 큰 고유값을 가진 고유벡터가 바로 조명 추정(Illuminant estimation)의 방향이 됨.
        eig_vector = eig_vector[:, np.argsort(eig_value)]
        avg_rgb = np.abs(eig_vector[:, 2])

        # 최종적으로 추출된 조명 방향 RGB 성분을 이용해 G/R 및 G/B 게인을 계산함.
        # 값이 없는(nan) 경우 0으로 처리함.
        rgain = np.nan_to_num(avg_rgb[1] / avg_rgb[0])
        bgain = np.nan_to_num(avg_rgb[1] / avg_rgb[2])
        return rgain, bgain
