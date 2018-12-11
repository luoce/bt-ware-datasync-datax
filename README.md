轻量级数据同步工具
==========
## 功能
        1.数据同步，支持不同数据库平台（参考datax支持）
        2.定时数据同步
        3.定时增量数据同步
        4.数据同步任务管理及执行日志查阅
        
## 依赖
        1.JDK 1.8+
        2.Python 2.7
        3.Flask （管理系统界面）
        4.Mongodb（记录执行记录）
        5.gunicorn（Flask启动服务器）
        
## 安装
#### 准备环境
        1.安装MongoDB
        2.安装Python 2.7
        3.安装pip
        4.安装JDK1.8并配置环境变量
        5.安装Datax
            Datax github：https://github.com/alibaba/DataX
        6.安装依赖Flask、flask_mongoengine、flask_apscheduler、gunicorn
            （启动时如果还有依赖问题，请按依赖提示安装依赖模块）
        
#### 配置文件
        cd <项目路径>
        vim config.py
        
#### 启动
        启动方式依赖gunicorn，请确保已经安装依赖模块。
        启动命令建议：gunicorn -b 0.0.0.0:5001 -D run:app
        不建议使用 -w 参数指定进程数，因为APScheduler初始化时会加载多次，顺便会加载数据库中标记为启动的任务，也会多次加载，多次运行。
        虽可以通过文件锁等方式解决重复加载问题，但还是变成了单点，前端管理后台访问频率相对较低，所以直接启动就好。
        后期将借助分布式锁，解决负载均衡下的任务调度问题，以避免单点故障。
        
#### 访问
        http://127.0.0.1:5001
        
#### 其他
        自行摸索
        
#### 计划
        1.增加用户、权限管理
        2.完善控制台、报表功能
        3.负载均衡及任务锁机制# bt-ware-datasync-datax
