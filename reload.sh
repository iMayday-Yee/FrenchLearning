#!/bin/bash

# 法语学习助手 - 平滑更新脚本（服务器部署版）
# 使用 reload 而非 restart，用户无感知

set -e

PROJECT_ROOT="/opt/FrenchLearning"

echo "============================================"
echo "法语学习助手 - 平滑更新"
echo "============================================"

cd "$PROJECT_ROOT"

echo "[1/5] Git pull..."
git pull

echo "[2/5] 平滑reload后端服务..."
sudo systemctl reload frenchlearning.service

echo "[3/5] 前端依赖安装..."
cd "$PROJECT_ROOT/frontend"
npm install

echo "[4/5] 前端构建..."
npm run build

echo "[5/5] 平滑reload Nginx..."
sudo systemctl reload nginx

echo ""
echo "============================================"
echo "更新完成！"
echo "============================================"
