
## 运行环境

依赖及demo示例使用的版本，使用更新版本应该是OK的

python3.X

requests 2.18.4

selenium 3.11.0

pymysql 0.8.0

Appium-Python-Client 0.26

browsermob-proxy 0.8.0

## 框架说明

keywords: 页面元素操作关键字定义文件

pages: 页面元素定义文件

cases: 测试用例文件

config.Variable: 配置信息

verfiy: 断言关键字定义

utils: 常用工具类

mysqlfiles: 数据库结构定义文件

* 当用run_ui_tc.py执行用例时只会用到ui_report表，执行完后报告会写数据库，也可以把run_ui_tc.py中把写数据库的逻辑注释掉，就不需要数据库
* 当用run_ui_tc_db.py执行用例，参数中需要指定测试套件或测试用例数据库id, 测试环境数据库id（支持环境切换，如果执行web用例，环境为hosts列表在数据库中的id，如果执行app用例，环境为设备在数据库中的id）, 是否是批量执行（-m 为 yes，批量执行会生成html报告，否则无）, 和报告收件人邮箱（如果不指定则不发送邮件），run_ui_tc_ab.py一般作为UI自动化系统的后端使用。

### 用例执行
run_ui_tc.py执行用例：

* 执行用例由config.Variable.py中TESTSUITE_WEB和TESTSUITE_APP指定
* 执行命令

```
//执行web用例
python.exe run_ui_tc.py

//执行app用例
python.exe run_ui_tc.py -t app
```

run_ui_tc_db.py执行用例：

* 执行用例由命令参数指定
* 执行命令

```
//执行web用例
python.exe run_ui_tc_db.py -t web -s 111 -e 71 -m yes -r "reciever@163.com"

//执行app用例
python.exe run_ui_tc.py -t app -s 91 -e 1 -m yes -r "reciever@163.com"
```

