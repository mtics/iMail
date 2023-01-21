# 邮件通知脚本

[EN](./README.md)

## 概述

本项目基于`Python 3.8`构建了一个简单实用的邮件通知脚本，它支持邮箱认证、群发、添加图片和附件。

## 功能 

* 支持群发； 

* 指定消息内容，支持多个格式，如文本，HTML等；

* 支持用户添加图片、附件（附件会以打包形式发送）；

* 支持自定义最大附件大小（单位为MB）


## 使用 

该脚本基于`Python 3.8`进行开发。

首先，需要安装依赖包

```git
pip install pillow
```

然后，将`mail.py`放置到项目中的合适位置即可。

## 使用 

项目中提供了一个简单的示例文件`demo.py`，用户可以仿照它进行配置

## 许可 

该脚本由[MIT](./LICENSE)许可证保护，允许自由使用和分发。
