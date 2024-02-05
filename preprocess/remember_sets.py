import os

# 데이터셋 디렉토리의 경로 설정
train_dir = '../dataset/raw/train'
test_dir = '../dataset/raw/test'

# train 디렉토리와 test 디렉토리에서 파일명을 읽어오기
train_list = os.listdir(train_dir)
test_list = os.listdir(test_dir)

# train_list.txt 파일에 train 디렉토리의 파일명 저장
with open('train_list.txt', 'w') as f:
    for filename in train_list:
        f.write(f"{filename}\n")

# test_list.txt 파일에 test 디렉토리의 파일명 저장
with open('test_list.txt', 'w') as f:
    for filename in test_list:
        f.write(f"{filename}\n")
