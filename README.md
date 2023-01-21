# Email notification scripts

[中文](./README-cn.md)

## Overview

This project builds a simple and useful email notification script based on `Python 3.8`, which supports email authentication, group mailing, adding images and attachments.

## Features

* Support group sending.

* Specifying message content, supporting multiple formats, such as text, HTML, etc.

* Support users to add images and attachments (attachments will be sent in a compressed package).

* Support customizes the maximum attachment size (in MB)

## Usage 

The script is developed based on `Python 3.8`.

1. you need to install the dependency package

    ```git
    pip install pillow
    ```

2. Place ``mail.py`` in the right place in your project.

A simple example file ``demo.py`` is provided in the project, which the user can emulate for configuration

## Licensing

The script is protected by the [MIT](./LICENSE) license, which allows free use and distribution.
