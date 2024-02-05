import os
import json
import numpy as np
import matplotlib.pyplot as plt

def read_class_distribution(directory):
    class_distribution = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                    for shape in data['shapes']:
                        class_name = shape['label']
                        if class_name in class_distribution:
                            class_distribution[class_name] += 1
                        else:
                            class_distribution[class_name] = 1
    return class_distribution

def visualize_and_save_combined_distribution(train_distribution, test_distribution, title, save_path):
    # 클래스 목록을 합집합으로 구하기
    classes = list(set(train_distribution.keys()) | set(test_distribution.keys()))
    classes.sort()  # 알파벳 순으로 정렬

    # train 및 test 카운트를 리스트로 추출 (클래스가 없는 경우 0으로 처리)
    train_counts = [train_distribution.get(cls, 0) for cls in classes]
    test_counts = [test_distribution.get(cls, 0) for cls in classes]

    # 바 차트 그리기 위한 위치 설정
    x = np.arange(len(classes))  # 클래스 레이블 위치
    width = 0.35  # 바의 너비

    plt.figure(figsize=(12, 8))
    bars_train = plt.bar(x - width/2, train_counts, width, label='Train', color='skyblue')
    bars_test = plt.bar(x + width/2, test_counts, width, label='Test', color='orange')

    # 각 바 위에 값 추가
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f'{int(height)}', ha='center', va='bottom')

    add_value_labels(bars_train)
    add_value_labels(bars_test)

    # 레이블, 제목, 눈금, 범례 추가
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(x, classes, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

if __name__ == '__main__':
    train_dir = '../dataset/train'
    test_dir = '../dataset/test'

    # Train 및 Test set의 클래스 분포 읽기
    train_distribution = read_class_distribution(train_dir)
    test_distribution = read_class_distribution(test_dir)

    # Train 및 Test set의 클래스 분포 시각화 및 저장
    visualize_and_save_combined_distribution(train_distribution, test_distribution, 'Combined Class Distribution', 'combined_distribution.png')
