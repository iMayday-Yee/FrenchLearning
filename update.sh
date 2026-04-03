#!/bin/bash

# 法语学习助手 - 一键更新脚本（服务器部署版）

set -e

PROJECT_ROOT="/opt/FrenchLearning"

echo "============================================"
echo "法语学习助手 - 一键更新"
echo "============================================"

cd "$PROJECT_ROOT"

echo "[1/5] Git pull..."
git pull

echo "[2/5] 重启后端服务..."
sudo systemctl restart frenchlearning.service

echo "[3/5] 前端依赖安装..."
cd "$PROJECT_ROOT/frontend"
npm install

echo "[4/5] 前端构建..."
npm run build

echo "[5/5] 重启 Nginx..."
sudo systemctl restart nginx

echo ""
echo "============================================"
echo "更新完成！"
echo "============================================"
