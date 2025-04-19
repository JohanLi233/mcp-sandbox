# MCP Sandbox

[![Python 版本](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![许可证](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![UV](https://img.shields.io/badge/UV-包管理器-blueviolet)](https://github.com/astral-sh/uv)
[![MCP](https://img.shields.io/badge/MCP-兼容-brightgreen)](https://github.com/estitesc/mission-control-link)

中文 | [English](README.md)

Python MCP Sandbox是一个交互式Python代码执行环境，允许用户和LLM在隔离的Docker容器中安全地执行Python代码和安装包。

## 功能特点

- 🐳 **Docker隔离**：在隔离的Docker容器中安全运行Python代码
- 📦 **包管理**：轻松安装和管理Python包
- 📊 **文件生成**：支持生成文件并通过网络链接访问

## 安装

```bash
# 克隆仓库
git clone https://github.com/JohanLi233/python-mcp-sandbox.git
cd python-mcp-sandbox

# 安装依赖
pip install -r requirements.txt

# 激活虚拟环境

# 启动服务器
python main.py
```

默认的SSE端点是http://localhost:8000/sse，你可以通过MCP Inspector或任何支持SSE连接的客户端与其交互。

### 可用工具

1. **create_sandbox**：创建一个新的Python Docker沙盒，并返回其ID，用于后续的代码执行和包安装
2. **list_sandboxes**：列出所有已存在的沙盒（Docker容器），可复用已有的sandbox_id
3. **execute_python_code**：在指定的Docker沙盒中执行Python代码
4. **install_package_in_sandbox**：在指定的Docker沙盒中安装Python包
5. **check_package_status**：检查Docker沙盒中包的安装状态

## 项目结构

```
python-mcp-sandbox/
├── main.py                    # 应用程序入口点
├── requirements.txt           # 项目依赖
├── Dockerfile                 # Python容器的Docker配置
├── results/                   # 生成文件的目录
├── mcp_sandbox/               # 主包目录
│   ├── __init__.py
│   ├── models.py              # Pydantic模型
│   ├── api/                   # API相关组件
│   │   ├── __init__.py
│   │   └── routes.py          # API路由定义
│   ├── core/                  # 核心功能
│   │   ├── __init__.py
│   │   ├── docker_manager.py  # Docker容器管理
│   │   └── mcp_tools.py  # MCP 工具
│   └── utils/                 # 实用工具
│       ├── __init__.py
│       ├── config.py          # 配置常量
│       ├── file_manager.py    # 文件管理
│       └── task_manager.py    # 周期性任务管理
└── README.md                  # 项目文档
```

## 示例提示词

```
我已为你配置了一个Python代码执行沙盒。你可以按照以下步骤运行Python代码：

1. 首先，使用"list_sandboxes"工具查看所有已存在的沙盒（Docker容器）。
   - 你可以复用已有的sandbox_id，如果已有沙盒，则不要创建。
   - 如需新建沙盒，请使用"create_sandbox"工具。
   - 每个沙盒都是独立的Python环境，sandbox_id是后续所有操作的必需参数。

2. 如果需要安装包，使用"install_package_in_sandbox"工具
   - 参数：sandbox_id和package_name（例如，numpy, pandas）
   - 这会启动异步安装，并立即返回状态

3. 安装包后，你可以使用"check_package_status"工具检查其安装状态
   - 参数：sandbox_id和package_name（要检查的包名）
   - 如果包仍在安装中，你需要使用此工具再次检查

4. 使用"execute_python_code"工具运行代码
   - 参数：sandbox_id和code（Python代码）
   - 返回输出、错误和任何生成文件的链接
   - 所有生成的文件都存储在沙盒内，file_links字段为直接HTTP链接

工作流示例：
- 先用list_sandboxes查看可用沙盒，或用create_sandbox新建 → 获取sandbox_id
- 使用install_package_in_sandbox安装必要的包（如pandas、matplotlib），带sandbox_id参数
- 使用check_package_status验证包安装，带相同的sandbox_id参数
- 使用execute_python_code运行代码，带sandbox_id参数

代码执行发生在安全的沙盒中。生成的文件（图像、CSV等）会作为HTTP链接提供，可直接浏览器访问或嵌入，无需下载。

注意不要在Python代码中直接使用plt.show()。对于可视化：
- 保存图形到文件请用plt.savefig()，不要用plt.show()
- 数据请用df.to_csv()、df.to_excel()等方法保存为文件
- 所有保存的文件都会自动作为HTTP链接出现在结果中，可直接打开或嵌入
``` 
