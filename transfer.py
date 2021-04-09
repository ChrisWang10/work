import json
import os
import cv2
import numpy as np
from tqdm import tqdm
import random

"""
0: nose; 1: leftShoulder; 2: rightShoulder; 3: leftElbow; 4: rightElbow; 5: leftWistle; 6:rightWistle
"""
transfer_idx = [0, 2, 5, 3, 6, 4, 7]
openpose_json_path = "C:/Users/wangchao871/PycharmProjects/AutoLabel/json"
label_save_path = "C:/Users/wangchao871/Desktop/labels.txt"
img_root = "C:/Users/wangchao871/PycharmProjects/AutoLabel/imgs"

draw_ref = [[1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [0, 1], [0, 2]]


def random_color():
    return np.random.randint(0, 200), np.random.randint(0, 200), np.random.randint(0, 200)


def draw_keypoints(img_path, kps, hint):
    print(img_path)
    img = cv2.imread(img_path)
    for person_idx in kps:
        kp = kps[person_idx]
        color = random_color()
        # color = (51, 255, 51)
        for ref in draw_ref:
            if kp[3*ref[0]+2] > 0 and kp[3*ref[1]+2] > 0:
                cv2.line(img, (int(kp[3*ref[0]]), int(kp[3*ref[0]+1])), (int(kp[3*ref[1]]), int(kp[3*ref[1]+1])), color, thickness=6)
    img = cv2.resize(img, (960, 540))
    cv2.imshow("./test.jpg", img)
    cv2.waitKey(1000)

    flag = input(hint+" = is good?")
    if flag == "x":
        json_path = os.path.join(openpose_json_path, img_path.split("\\")[-1].split(".")[0]+"_keypoints.json")
        print(json_path)
        os.remove(json_path)


def json2label(json_path, save_path):
    files = os.listdir(json_path)
    for i, json_file in enumerate(files):
        hint = "{}/{}".format(i, len(files))
        json_dict = json.load(open(os.path.join(json_path, json_file), "r"))
        labels = json_dict["people"]

        one_file = {}
        for i, person in enumerate(labels):
            kps = person["pose_keypoints_2d"]
            label = []
            for idx in transfer_idx:
                label += [kps[3 * idx], kps[3 * idx + 1], 2 if kps[3 * idx + 2] > 0 else 0]
            one_file[i] = label
        # json.dump(one_file, open(os.path.join("./out", json_file.split(".")[0] + ".json"), "w"))
        draw_keypoints(os.path.join(img_root, json_file.split(".")[0].split("_")[0] + ".jpg"), one_file, hint)


if __name__ == '__main__':
    json2label(openpose_json_path, label_save_path)
