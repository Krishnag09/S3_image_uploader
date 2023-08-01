# Project Name

This is a project in response to  Bowery farms take home assessment for backend engineer role.
## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)


## Introduction

A brief introduction to your project and what it does.

## Features

- running the project exposes an API at http://127.0.0.1:5000/api/ on local
- project comprises of a GET(used to perform sanitary test) and POST(image upload feature)
- Flask has been used as the python framework.
- rate limiting(per ip) for image upload(before uploading to S3) has been implemented using a key value pair in redis. 
- Flask does not allow for asynch calls(not the best deicison in hindsight), S3's config has been used to limit date of upload and enable/disable threads. One could use FAST API as alternate framework to do asynch processing. 

## Installation
unzip 

```bash
brew install redis
redis-server
python3 -m venv venv
cd bowery_photo_uploader
source venv/bin/activate
pip install -r requirements.txt
flask --app fileuploader run --debug
```

Might might need reactivating after installing requirements.txt.
You can replace the AWS credentials in config.json but it should work as is. 
The S3 upload limit can also be set by the same.


## Usage

- Use postman with POST as method,  "http://127.0.0.1:5000/api/upload" as url ,  form-data as body.
- Select file as key type, upload image test.png or any image of you choice.
- To run tests use  `python3 -m unittest fileuploader/tests/test_upload.py`
