
## 运行环境

依赖及demo示例使用的版本，使用更新版本应该是OK的

``
python3.X

requests 2.18.4

selenium 3.11.0

pymysql 0.8.0

Appium-Python-Client 0.26

browsermob-proxy 0.8.0
``

## 框架说明
* 框架说明 <br/>
keywords: 页面元素操作关键字定义文件

pages: 页面元素定义文件

cases: 测试用例文件

config.Variable: 配置信息

verfiy: 断言关键字定义

utils: 常用工具类

mysqlfiles: 数据库结构定义文件

* 当用run_tui_tc.py执行用例时只会用到ui_report表，执行完后报告会写数据库，

