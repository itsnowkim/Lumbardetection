# Lumbardetection
 척추 측면 이미지를 통해 segmentation 하는 모델을 만들기

## Preprocessing
- `eraserectangle.py` : 필요 없는 bbox labeling 지우기
- `preprocess.py` : 640x640 size 로 img, annotation 좌표 convert, annotation file format 에 맞게 변환, 파일 복사, train/test 에 맞게 데이터 split
- `health_check.py` : class 별 비율 올바르게 분할되었는지 시각화하는 python script

## YOLO Format 으로 변환
```sh
labelme2yolo --json_dir dataset/train
labelme2yolo --json_dir dataset/test
```
와 같이 경로를 명시하면 yolo format 으로 convert 해 줌.

```sh
sh train.sh
```
train.sh 에 여러 test 할 config 명시하고 하거나, 따로 cfg 파일을 만들어서 해당 cfg 파일을 참조하도록 작성하면 간단하게 train 할 수 있음.