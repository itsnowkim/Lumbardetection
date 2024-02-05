import os
import shutil
import json
from eraserectangle import clean_bbox
from PIL import Image
from tqdm import tqdm

def copy_dataset(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for item in tqdm(os.listdir(source_dir)):
        s = os.path.join(source_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

def resize_imgs(directory):
    for root, dirs, files in tqdm(os.walk(directory)):
        for file in files:
            if file.endswith('.jpeg') or file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                original_width, original_height = img.size
                scale_width, scale_height = 640 / original_width, 640 / original_height
                
                img = img.resize((640, 640))
                new_path = os.path.splitext(img_path)[0] + '.png'
                img.save(new_path)
                os.remove(img_path)  # 원본 이미지 파일 삭제

                json_path = os.path.splitext(img_path)[0] + '.json'
                if os.path.exists(json_path):
                    with open(json_path, 'r') as json_file:
                        data = json.load(json_file)
                        data['imageHeight'] = 640
                        data['imageWidth'] = 640
                        data['imagePath'] = os.path.basename(new_path)

                        for shape in data['shapes']:
                            for point in shape['points']:
                                # 각 좌표를 새로운 이미지 크기에 맞게 조정
                                point[0] = point[0] * scale_width
                                point[1] = point[1] * scale_height

                    with open(json_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)

def split_dataset(dest_dir, test_ratio):
    train_dir = os.path.join(dest_dir, 'train')
    test_dir = os.path.join(dest_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # 파일별 클래스 분포 구하기
    print("파일별 클래스 분포 구하기")
    file_to_classes = {}
    class_to_files = {}
    files = [f for f in os.listdir(dest_dir) if f.endswith('.json')]
    for file in tqdm(files):
        with open(os.path.join(dest_dir, file), 'r') as json_file:
            data = json.load(json_file)
            file_to_classes[file] = set()
            for shape in data['shapes']:
                class_name = shape['label']
                file_to_classes[file].add(class_name)
                if class_name in class_to_files:
                    class_to_files[class_name].add(file)
                else:
                    class_to_files[class_name] = {file}

    # 클래스별 파일 개수가 적은 순으로 정렬
    sorted_classes = sorted(class_to_files.items(), key=lambda item: len(item[1]))

    allocated_files = set()
    train_files = set()
    test_files = set()

    print("train, test 나누기")
    for class_name, files in sorted_classes:
        # 파일 리스트를 배열로 변환하여 분할
        files_list = list(files)
        n_test = int(len(files_list) * test_ratio)
        class_test_files = set(files_list[:n_test])
        class_train_files = set(files_list[n_test:])

        # 중복되지 않게 파일 할당
        test_files = test_files.union(class_test_files.difference(allocated_files))
        train_files = train_files.union(class_train_files.difference(allocated_files))

        # 할당된 파일 업데이트
        allocated_files.update(class_test_files)
        allocated_files.update(class_train_files)

    print(f"train : {len(train_files)} test : {len(test_files)}")

    # 파일 이동 로직
    print("train, test 에 맞게 이동")
    for file_name in tqdm(train_files.union(test_files)):
        base_name = os.path.splitext(file_name)[0]
        img_file = base_name + '.png'  # 가정: 이미지는 이미 .png로 변환됨
        target_dir = train_dir if file_name in train_files else test_dir
        shutil.move(os.path.join(dest_dir, file_name), os.path.join(target_dir, file_name))
        if os.path.exists(os.path.join(dest_dir, img_file)):
            shutil.move(os.path.join(dest_dir, img_file), os.path.join(target_dir, img_file))

if __name__ == '__main__':
    source_dir = 'C:\\Users\\taesh\\Dropbox\\006_researchdata\\0002_Lat_Lxray_label\\dataset'
    dest_dir = '../dataset'

    print('dataset copy 시작')
    copy_dataset(source_dir, dest_dir)
    print('dataset copy 종료')

    print('annotation bbox 제거 시작')
    clean_bbox(dest_dir)
    print('annotation bbox 제거 종료')

    print('img resolution 변경 시작')
    resize_imgs(dest_dir)
    print('img resolution 변경 종료')

    print('train, test dataset 폴더 나누기 시작')
    split_dataset(dest_dir, 0.2)
    print('train, test dataset 폴더 나누기 종료')