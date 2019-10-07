# **Attendance**

此程序为电子科技大学宜宾研究院信通401考勤程序，具有学生信息录入，RFID卡号读取，课程表录入，并==依据课程表对学生进行教研室考勤，自动标记无课同学迟到或未到的同学==。

## 界面预览

#### 平时打卡界面

<img src="https://github.com/UESTC-ICT401/Attendance/blob/master/github_images/1570365331368.png" alt="1570365331368" style="zoom: 80%;" />



#### 注册界面

<img src="https://github.com/UESTC-ICT401/Attendance/blob/master/1570365430311.png" alt="1570365430311" style="zoom:60%;" />

#### 课程注册界面

<img src="https://github.com/UESTC-ICT401/Attendance/blob/master/1570365470730.png" alt="1570365470730" style="zoom:80%;" />

#### 菜单选择项

<img src="https://github.com/UESTC-ICT401/Attendance/blob/master/1570365503871.png" alt="1570365503871" style="zoom:80%;" />



## 上手指南

### 安装要求

二次开发者：

1. mysql5.7
2. python3.6+pymysq+pyqt5
3. 自建数据库与表格

401使用者：

1. 校园卡

### 数据库构成

| 数据库名                     | attendance_schema_401 |
| ---------------------------- | --------------------- |
| 表(record_table)             | 考勤记录表            |
| 表(course_table)             | 课程信息表            |
| 表(stu_info_table)           | 学生信息表            |
| 表(stu_course_mapping_table) | 学生-课程映射表       |

#### course_table

![1570361651748](https://github.com/UESTC-ICT401/Attendance/blob/master/1570361651748.png)

#### record_table

![1570361693323](https://github.com/UESTC-ICT401/Attendance/blob/master/1570361693323.png)

####  stu_info_table

![1570361734165](https://github.com/UESTC-ICT401/Attendance/blob/master/1570361734165.png)

#### stu_course_mapping_table

![1570361785355](https://github.com/UESTC-ICT401/Attendance/blob/master/1570361785355.png)



## 提交日志

*刘鑫：*

2019/9/26 22:30:创建Repository，已完成串口读取程序，Class student、Class sql_operate以及最初的UI框架。

2019/10/1 22:36:实现选择串口，读取RFID，并且学生注册插入数据库。Notice：修改了郑文student_register类，添加了必需的信号连接以及回调函数。喝了酒，今天到此结束。

2019/10/2 14:06:重新调整结构，数据库连接在每个操作前重新建立，使用完毕进行关闭。增加信号与槽实现跨线程UI的更新，实现基本打卡功能。

2019/10/3 16:09:规范日志输出格式，更好定位运行状态以及bug所在，重命名数据库表明，将sheet(页）修改为table(表），新增course类，听从在北京人人网工作的同学的建议，修改查课程表思路，新增student_course_mapping_table作为学生和课程表的映射关系记录，并且在课程表中增加有效性这一栏，每周日自动定期将过期课程标记。

2019/10/4 12:00 调整串口线程与UI线程的通信，都改用信号与槽的方式。将串口读取修改为非阻塞式，避免串口抖动产生多余字符影响后续打卡操作，利用开关串口进行切换。注意：在修改的过程中，发现任何一个Thread对象，都只能启动一次，否则会报错！一个子线程意外停止或手动结束，都必须重新创建线程对象。到此，明显的Bug已经被修复。

2019/10/5 16:16 在注册时加入信息完整性校验，并且实现课程表导入，以及学生-课程表映射表的写入，自此，完整的学生注册功能完成。

2019/10/5 22:48 加入了8:30 14:30 19:30 自动查询课程表，未打卡，且没课的同学将被标记迟到录入数据库的机制，实现原理：首先找出此时此刻正在上的课以及正在上课的同学，获取他们的学号，并与已经打卡的同学做并集，最后与人员信息表做差集，求出迟到的人，最后保存结果在临时表中，插入考勤记录后删除临时表。

sql语句：

```python
        sql = '''CREATE TABLE tmp AS  
                (
                    SELECT stuID,name,team FROM stu_info_table
                    WHERE stuID NOT IN
                    (SELECT stuID FROM record_table WHERE time BETWEEN "{0}" AND "{1}") 
                    AND stuID NOT IN
                    (
                        SELECT stuID FROM stu_course_mapping_table WHERE course_id  
                        IN (SELECT course_id FROM course_table WHERE lesson_weekday ='{2}'  
                        AND effectiveness = 1 
                        AND (CURRENT_TIME() BETWEEN start_time AND end_time))
                    )
                )'''.format(start_time,end_time,now_weekday)
```

2019/10/6 19:17 加入课程注册功能，测试后添加了所有课程至数据库。自此，信通401考勤系统主体功能基本实现。开始进行内测。

2019/10/7 12:52 加入窗口透明度以及电子科技大学宜宾研究院的背景图片



*郑文：*

2019/9/28 14:30: 添加register界面，包含用户信息，课表信息的显示

2019/10/6 11:20：添加课程注册界面

## 作者

1. 刘鑫 （xinliu1996@163.com）
   - 主题框架
   - 数据库设计
   - 后台搭建
   - UI设计
2. 郑文（）
   - UI设计





## 鸣谢

该项目参考重庆理工大学电子创新竞赛实验基地门禁考勤程序。

感谢信通401的同门师兄弟的测试。

