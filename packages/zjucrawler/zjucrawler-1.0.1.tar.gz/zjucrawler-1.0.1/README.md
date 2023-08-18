# ZJU Crawler

## 介绍
浙江大学学生教师信息爬虫，从教务网、查老师获取对应信息。可以结合QQ机器人等食用。  
该包目前集成了两个爬虫：  

- 学生个人信息爬虫
    - 加权均绩
    - 加权四分制均绩（出国，旧）
    - 加权4.3分制均绩（出国，新）
    - 加权百分制成绩
    - 考试信息（时间、考场、……）
  
- 查老师网站老师信息爬虫（评分，对应课程等）  

未来将会添加学在浙大的爬虫（如果修好了）。  

## 安装
### PyPi
`pip install zjucrawler`

### 手动安装
下载后进入`setup.py`所在文件夹执行`pip install .`即可。  
也可以下载`.whl`文件安装。  

## 使用示例

### 导入
```python
import zjucrawler
# or:
from zjucrawler import chalaoshi # Chalaoshi website(unofficial)
from zjucrawler import zju # Fetch from official websites
```

### 教师

```python
import asyncio
from zjucrawler import chalaoshi # Chalaoshi website(unofficial)
async def main():
    teacher = input("teacher ID >>>")
    print(await chalaoshi.get_teacher_info(int(teacher))) # 获取教师信息
    # search_teachers 通过教师姓名/缩写获取教师列表
    # get_course_info 获取课程平均绩点、标准差
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### 学生

```python
import asyncio
from zjucrawler import zju # Fetch from official websites
async def main():
    username = input("username>>>")
    pwd = input("pwd>>>")
    test = zju.Fetcher(username, pwd, simulated=False) # simulated指定是否模拟浏览器进行登录
    print(await test.get_GPA()) # 获取全科均绩，不含弃修
    # get_avg_score 获取加权平均百分制成绩
    # get_abroad_GPA_old 出国均绩旧（4分制） -2021级
    # get_abroad_GPA_new 出国均绩新（4.3分制）2022级-
    exams = list(await test.get_all_exams()) # 获取所有考试信息
    print(exams)
    print(test.__dict__)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 注意事项

确保包中含有`security.js`.  
由于一些众所周知的神秘因素可能无法使用查老师（需要内网），请自行解决:)  