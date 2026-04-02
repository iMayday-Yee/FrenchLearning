@echo off
REM 法语学习助手 - Windows 启动脚本

setlocal enabledelayedexpansion
cd /d "%~dp0"

set "BACKEND_DIR=%CD%\backend"
set "FRONTEND_DIR=%CD%\frontend"

echo ============================================
echo 法语学习助手 - 启动脚本
echo ============================================
echo.

REM 检查 Python
echo 检查依赖...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到 PATH
    pause
    exit /b 1
)
echo [✓] Python 已安装

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Node.js 未安装或未添加到 PATH
    pause
    exit /b 1
)
echo [✓] Node.js 已安装
echo.

REM 启动后端
echo 启动后端服务...
cd /d "%BACKEND_DIR%"

if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat
if exist "requirements.txt" (
    echo 安装后端依赖...
    pip install -q -r requirements.txt
)

echo 启动 Flask 应用...
start "French Learning Assistant - Backend" python app.py
echo [✓] 后端已启动

timeout /t 2 /nobreak

REM 启动前端
echo.
echo 启动前端应用...
cd /d "%FRONTEND_DIR%"

if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install -q
)

echo 启动 Vite 开发服务器...
start "French Learning Assistant - Frontend" cmd /k npm run dev
echo [✓] 前端已启动

echo.
echo ============================================
echo ��务已启动！
echo ============================================
echo.
echo 前端应用: http://localhost:3000
echo 后端 API: http://localhost:5000
echo.
echo 提示:
echo 1. 编辑 backend\config.py，填入 API 密钥
echo 2. 在浏览器访问上述地址
echo 3. 关闭窗口停止服务
echo.
pause
