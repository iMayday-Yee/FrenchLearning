#!/bin/bash

# 前端构建
cd /path/to/frontend
npm install
npm run build

# 后端依赖
cd /path/to/backend
pip install -r requirements.txt

# 重启服务
sudo systemctl restart french-backend
sudo nginx -s reload
