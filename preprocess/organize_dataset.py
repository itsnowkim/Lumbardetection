import os
import shutil
from tqdm import tqdm

# 파일 목록을 읽어와서 이동할 경로를 결정하는 함수
def move_files(file_list, source_root, dest_root_images, dest_root_labels):
    # images, labels 하위 디렉토리가 없으면 생성
    if not os.path.exists(dest_root_images):
        os.makedirs(dest_root_images)
    if not os.path.exists(dest_root_labels):
        os.makedirs(dest_root_labels)

    # 파일 목록을 순회하며 파일 이동
    for file in tqdm(file_list):
        source_file = os.path.join(source_root, file)
        if file.endswith('.jpg') or file.endswith('.png'):  # 이미지 파일인 경우
            shutil.move(source_file, dest_root_images)
        elif file.endswith('.json'):  # 라벨 파일인 우
            file = file.split('.')[0] + '.txt'
            source_file = os.path.join(source_root, file)
            shutil.move(source_file, dest_root_labels)

# train_list.txt 파일을 읽어오기
with open('train_list.txt', 'r') as f:
    train_files = f.read().splitlines()

# test_list.txt 파일을 읽어오기
with open('test_list.txt', 'r') as f:
    test_files = f.read().splitlines()

# 파일 이동을 위한 루트 경로 설정
train_source_root = '../dataset/YOLODataset'
test_source_root = '../dataset/YOLODataset'
train_dest_root_images = '../dataset/train/images'
train_dest_root_labels = '../dataset/train/labels'
test_dest_root_images = '../dataset/test/images'
test_dest_root_labels = '../dataset/test/labels'

# 파일 이동 실행
print('train file 이동')
move_files(train_files, train_source_root, train_dest_root_images, train_dest_root_labels)
print('train file 이동 완료')

print('test file 이동')
move_files(test_files, test_source_root, test_dest_root_images, test_dest_root_labels)
print('test file 이동 완료')
