# 使用 VS Code 创建 FastAPI 项目

本教程从空文件夹开始，完成 Python 环境准备、虚拟环境创建、依赖安装、`main.py` 编写、服务启动和接口测试。

## 1. 准备软件

安装以下软件：

- Python 3.10 或更高版本
- Visual Studio Code
- VS Code 扩展：`Python`（发布者为 Microsoft）

安装 Python 时勾选 **Add Python to PATH**。安装完成后打开 PowerShell，检查版本：

```powershell
python --version
```

如果系统找不到 `python`，也可以尝试 `py --version`。

## 2. 创建并打开项目

在 PowerShell 中执行：

```powershell
cd D:\练习
mkdir week2-fastapi-chat-api
cd week2-fastapi-chat-api
code .
```

如果文件夹已经存在，只需进入文件夹并执行 `code .`。也可以在 VS Code 中选择 **文件 > 打开文件夹**，然后选择项目文件夹。

## 3. 在 VS Code 中打开终端

在 VS Code 菜单中选择 **终端 > 新建终端**。确认终端当前路径是项目根目录：

```text
D:\练习\week2-fastapi-chat-api
```

后续命令都在这个终端中执行。

## 4. 创建并激活虚拟环境

虚拟环境可以让每个项目使用独立的 Python 依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

激活成功后，终端提示符前通常会出现 `(.venv)`。

如果 PowerShell 提示禁止运行脚本，先只为当前终端临时放开限制，再重新激活：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 5. 选择 VS Code Python 解释器

1. 按 `Ctrl+Shift+P` 打开命令面板。
2. 输入并选择 **Python: Select Interpreter**。
3. 选择项目中的 `.venv\Scripts\python.exe`。

这可以确保 VS Code 运行和检查代码时使用当前项目的虚拟环境。

## 6. 创建并安装依赖

先确认终端前面显示 `(.venv)`，并检查当前使用的是项目虚拟环境中的 Python：

```powershell
python -c "import sys; print(sys.executable)"
```

输出路径应以 `.venv\Scripts\python.exe` 结尾。然后升级虚拟环境中的依赖安装工具：

```powershell
python -m pip install --upgrade pip
```

### 方法一：从零安装项目依赖

直接安装 FastAPI 和用于启动服务的 Uvicorn：

```powershell
python -m pip install fastapi==0.116.1 "uvicorn[standard]==0.35.0"
```

- `fastapi`：用于编写 API 接口
- `uvicorn`：用于运行 FastAPI 应用
- `[standard]`：额外安装常用的性能和开发依赖，例如自动重载所需组件

安装完成后，在项目根目录新建 `requirements.txt`，记录项目直接使用的依赖：

```text
fastapi==0.116.1
uvicorn[standard]==0.35.0
```

也可以让 `pip` 自动把当前虚拟环境中的全部依赖及其版本写入文件：

```powershell
python -m pip freeze > requirements.txt
```

注意：`>` 会覆盖 `requirements.txt` 原有内容。执行前应确认已经激活本项目的 `.venv`，否则可能把系统 Python 或其他项目的依赖也写进去。

检查生成的文件：

```powershell
Get-Content requirements.txt
```

### 方法二：根据已有文件恢复依赖

当项目中已经有 `requirements.txt` 时，不需要逐个安装，直接执行：

```powershell
python -m pip install -r requirements.txt
```

`-r` 表示读取文件，并安装其中列出的全部依赖。这也是下载现有项目或换电脑后最常用的安装方式。

### 验证安装结果

查看已安装的 FastAPI 和 Uvicorn：

```powershell
python -m pip show fastapi
python -m pip show uvicorn
```

也可以进行一次导入检查：

```powershell
python -c "import fastapi, uvicorn; print('依赖安装成功')"
```

如果没有报错，就说明当前虚拟环境已经可以使用。查看该环境中的全部依赖可执行：

```powershell
python -m pip list
```

### 下载失败时的处理

如果默认下载源连接失败，改用官方 PyPI：

```powershell
python -m pip install -r requirements.txt -i https://pypi.org/simple
```

网络较慢时可以延长超时时间：

```powershell
python -m pip install -r requirements.txt -i https://pypi.org/simple --timeout 60
```

如果提示没有权限，请先确认虚拟环境已激活。项目依赖不需要使用管理员权限，也不建议安装到系统 Python 中。

## 7. 创建 `main.py`

在项目根目录创建 `app` 文件夹，再在其中创建 `main.py`。此时结构如下：

```text
week2-fastapi-chat-api/
|-- .venv/
|-- app/
|   `-- main.py
|-- requirements.txt
`-- README.md
```

将以下完整代码写入 `app/main.py`：

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Week 2 FastAPI Chat API",
    description="A small API for learning HTTP, JSON, request bodies, and Swagger.",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, examples=["What is FastAPI?"])


class ChatResponse(BaseModel):
    answer: str
    question: str
    source: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    answer = f"You asked: {request.question}"
    return ChatResponse(
        answer=answer,
        question=request.question,
        source="fixed-response",
    )
```

`app = FastAPI(...)` 创建应用；`@app.get` 和 `@app.post` 分别定义 GET 和 POST 接口；继承 `BaseModel` 的类用于检查请求和响应的 JSON 结构。

## 8. 启动服务

确保终端位于项目根目录且虚拟环境已激活，然后运行：

```powershell
python -m uvicorn app.main:app --reload
```

- `app.main` 表示 `app/main.py`
- 最后的 `app` 表示代码中的 `app = FastAPI(...)`
- `--reload` 表示保存代码后自动重启开发服务器

看到 `Uvicorn running on http://127.0.0.1:8000` 表示启动成功。这个终端需要保持运行。

## 9. 测试接口

在浏览器打开自动生成的 Swagger 页面：

```text
http://127.0.0.1:8000/docs
```

打开健康检查地址 `http://127.0.0.1:8000/health`，预期返回：

```json
{"status":"ok"}
```

也可以新建一个 VS Code 终端，用 PowerShell 测试聊天接口：

```powershell
$body = @{ question = "What is FastAPI?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat -ContentType "application/json" -Body $body
```

预期响应：

```json
{
  "answer": "You asked: What is FastAPI?",
  "question": "What is FastAPI?",
  "source": "fixed-response"
}
```

## 10. 停止和再次启动

在运行服务的终端中按 `Ctrl+C` 停止服务。

以后重新打开项目时，只需要执行：

```powershell
cd D:\练习\week2-fastapi-chat-api
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

## 常见问题

### `ModuleNotFoundError: No module named 'fastapi'`

通常是没有安装依赖，或者 VS Code 使用了错误的 Python。依次执行：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip show fastapi
```

然后在 VS Code 中重新选择 `.venv\Scripts\python.exe`。

### `Error loading ASGI app. Could not import module ...`

确认终端位于项目根目录，并使用：

```powershell
python -m uvicorn app.main:app --reload
```

### 端口 8000 已被占用

换一个端口启动：

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

文档地址会变为 `http://127.0.0.1:8001/docs`。
