import requests
import os
import time
import random


host = "https://ai-duke-api.xdf.cn/course/getCourseBaseResourceVo?courseId="
save_root = "./imgs"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "token": "c7280983-7466-4e0a-ab70-90534d73505f",
    "Content-Type": "application/x-www-form-urlencoded"
}


def download():
    for courseId in range(6538, 12000):
        data = {"courseId": courseId}
        r = requests.post(url=host + str(courseId), data=data, headers=headers).json()
        success = r["success"]
        if success:
            data = r["data"]
            if data:
                for i, item in enumerate(data["studentImgEvidenceList"]):
                    if i % 5: continue
                    imgUrl = item["imgUrl"]
                    print(courseId, imgUrl)
                    imgFile = requests.get(imgUrl)
                    open(os.path.join(save_root, imgUrl.split("/")[-1]), "wb").write(imgFile.content)
        time.sleep(random.randint(30, 60))


if __name__ == "__main__":
    download()
