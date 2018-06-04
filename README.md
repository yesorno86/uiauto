
## 运行环境python3.X

### 需要额外安装的依赖库及demo示例使用的版本，使用更新版本应该是OK的

``
requests 2.18.4
selenium 3.11.0
pymysql 0.8.0
Appium-Python-Client 0.26
browsermob-proxy 0.8.0
``

## 说明
* 框架说明 <br/>
keywords:Webdriver关键字驱动，用来控制webdriverclick, sendkey, refresh 等事件，如下：

pages: 元素关键字，用于操作、定位元素配置，该页面继承BasePage,如下：

cases: 用例编写 web目录为新框架用例，用例按照功能编写，用例编写格式如下：

config.Variable: 项目配置，主要包含邮件等信息<br/>
verfiy: 为断言验证，支持字符、数字、包含验证。
utils: 常用工具类