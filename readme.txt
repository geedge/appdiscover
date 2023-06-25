项目目标：发现一台主机上安装的软件，目前支持发现80个软件。
输入是目标主机的文件系统记录，就是主机上每个文件的绝对路径及文件权限等等息，如：
-rw-rw-r-- 1 zjh zjh       909 2023-05-10 14:51:21.162511430 +0800 /home/zjh/software/kafka_2.11-1.0.0/config/connect-console-source.properties
-rw-rw-r-- 1 zjh zjh      5807 2023-05-10 14:51:21.218512161 +0800 /home/zjh/software/kafka_2.11-1.0.0/config/connect-distributed.properties



main 执行文件
运行环境：ubuntu18.04
运行方法：./main
运行结果：直接得到软件发现结果

另外源代码：
main.py是源代码，pycharm直接运行即可，修改“文件系统记录”路径就好。
输入是文件系统记录，实例如llq.txt，lxy.txt，lyz.txt。
输出是软件发现结果。
