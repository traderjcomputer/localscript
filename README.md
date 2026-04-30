# localscript

这是一个用于管理小型 Python 脚本仓库的规范文档。每个脚本应该独立完成一个明确任务，且优先使用 Typer 作为命令行入口。

## 仓库规则（House Rules）
- **第一条规则**：先读 README，再动手写代码。任何新代码必须符合本文档的所有规范。
- **单一功能原则**：一个脚本只能负责一个功能。功能定义指"完成一个独立的、不可再细分的业务流程"。禁止在一个脚本中混入多个无关功能。
- **依赖集中管理**：所有脚本依赖的第三方库必须集中在 `requirements.txt` 中。任何新增功能所需的库，都要先更新 `requirements.txt`。不允许在代码中 `import` 未在 `requirements.txt` 中列出的库。
- **安装依赖**：运行脚本前，必须先安装依赖：
  ```bash
  pip install -r requirements.txt
  ```
- **命名规范**：
  - 目录格式：`src/<类别>/`，类别名必须是英文小写单词或短语，用下划线分隔，如 `scraper`, `data_process`, `api_serve`。
  - 脚本格式：`src/<类别>/<功能>.py`，脚本名必须用英文小写单词或下划线分隔，如 `news_spider.py`, `csv_cleaner.py`。
  - **禁止使用**：`script1.py`, `test.py`, `main.py`, `temp.py`, `misc.py`, `tmp` 等无意义的名称。
  - 文件名即说明：看到文件名应该能理解脚本用途，不需要额外文档。
- **执行规范**：
  - 进入脚本所在目录后运行脚本：`cd src/<类别> && python <功能>.py`
  - 脚本的工作目录（`cwd`）就是该脚本所在目录。
  - 脚本中的所有相对路径都是相对于该脚本目录。例如，读写文件使用 `./data/`, `./output/`, `./logs/` 等相对路径。
  - 脚本生成的所有文件（数据、日志、临时文件、缓存）都必须放在脚本所在目录或其子目录内。**禁止在仓库根目录或其他脚本目录中生成文件**。
- **脚本内部结构**：
  - 脚本应使用 Typer 作为命令行入口。即使功能简单，也要实现一个 Typer 函数。
  - 脚本必须包含 `--help` 支持，说明脚本用途和参数含义。
  - 脚本应设定统一的参数规范：输入参数用 `--input` 或 `-i`，输出参数用 `--output` 或 `-o`。
- **敏感信息处理**：
  - 敏感信息（API Key、密码、数据库连接等）不能硬编码。必须从环境变量、配置文件或命令行参数读取。
  - 配置文件放在脚本目录下的 `config.json` 或 `config.yaml`。
  - 配置文件不应包含实际的敏感值，只包含配置结构。
- **日志与输出**：
  - 日志文件必须输出到脚本目录下的 `logs/` 子目录，文件名格式：`logs/YYYY-MM-DD.log` 或 `logs/run.log`。
  - 脚本生成的数据输出到 `output/` 或 `data/` 子目录。
  - 临时文件输出到 `temp/` 子目录（运行结束后应清理）。
  - 所有文件输出都应使用相对路径，例如 `./logs/`, `./output/`, `./temp/`。
- **脚本间调用规范**：
  - **禁止**脚本间直接相互调用（`import` 其他脚本）。
  - 如果需要共享代码，应提取到 `src/lib/` 目录下的公共模块，所有脚本可以共用。
  - 例如：`src/lib/common_utils.py` 可以被 `src/scraper/` 和 `src/data/` 中的脚本导入。
- **版本锁定**：
  - `requirements.txt` 中的库必须指定版本号（如 `requests>=2.31.0` 或 `pandas==2.2.2`），保证可复现性。
  - **禁止**使用 `库名` 这种无版本的写法。
- **新增脚本流程**：
  1. 先在本 README 的"脚本清单"部分描述新脚本的功能。
  2. 检查 `requirements.txt` 中是否包含所需的库；如果不包含，先添加。
  3. 创建脚本文件和必要的子目录（`logs/`, `output/`, `temp/`, `config/` 等）。
  4. 确保脚本可以独立运行，且所有文件输出在脚本目录内。
  5. 测试脚本从不同目录的行为，确保相对路径正确。
  6. 提交 git 时包括脚本、`requirements.txt` 变更、和 README 更新。

## 依赖管理
- `requirements.txt` 是本仓库的**唯一**依赖清单。所有脚本必须从这个文件安装依赖。
- 必须指定版本号，例如 `requests>=2.31.0` 或 `pandas==2.2.2`，不允许无版本的库。
- 新增依赖前，先确认该库是否真的必要。避免重复或过度依赖。
- 定期审查 `requirements.txt`，移除不再使用的库。

## 目录组织与规模控制
- `src/`：主脚本目录。
- `src/<类别>/`：按功能类别分组。类别应该用英文单词表示，如 `scraper`, `data_process`, `api_serve`, `analysis`。
  - 每个类别名称应该清晰表达其用途，看到名称就知道该目录里的脚本做什么。
- `src/<类别>/<脚本>.py`：脚本文件。
- `src/lib/`：共享代码库。所有脚本可以导入这里的模块。
- 每个脚本可包含子目录：
  - `logs/` - 日志文件
  - `output/` - 输出数据
  - `temp/` - 临时文件
  - `config/` - 配置文件（结构定义，不含敏感值）
  - `data/` - 输入数据（如需要）
- 脚本数量超过 10 个时，建议在每个类别目录下添加 `README.md`，列出该目录的所有脚本及其功能说明。
- **禁止使用**：目录名 `misc/`, `temp/`, `test/`, `old/` 等无意义的名称。

## 脚本示例（Typer 入口）
```python
import typer
import json
from pathlib import Path

app = typer.Typer()

@app.command()
def main(
    input_file: str = typer.Option(..., "--input", "-i", help="输入文件路径"),
    output_file: str = typer.Option("output.json", "--output", "-o", help="输出文件路径"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="是否显示详细日志"),
):
    """
    这是一个示例脚本，用于处理数据。
    
    示例：
        python example.py --input data.csv --output result.json --verbose
    """
    typer.echo(f"Reading from {input_file}")
    
    # 确保所有文件操作都在脚本目录内
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    # 处理逻辑
    with open(input_path, "r") as f:
        data = json.load(f)
    
    # 输出结果
    with open(output_path, "w") as f:
        json.dump(data, f)
    
    typer.echo(f"Wrote to {output_file}")

if __name__ == "__main__":
    app()
```

运行方式：
```bash
cd src/category
python example.py --help
python example.py --input data.csv --output result.json --verbose
```

## 运行方式
1. 在项目根目录创建并激活虚拟环境（只需一次）：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. 安装依赖（只需一次）：
   ```bash
   pip install -r requirements.txt
   ```
3. 进入要运行的脚本目录：
   ```bash
   cd src/<类别>
   ```
4. 运行脚本：
   ```bash
   python <脚本名>.py --help  # 查看帮助
   python <脚本名>.py --input data.csv --output result.json  # 执行脚本
   ```

> **重要**：只使用项目根目录的虚拟环境，避免重复创建。所有依赖从 `requirements.txt` 安装一次。

## 脚本清单
（新增脚本时，在此列出功能和位置）

| 脚本位置 | 功能说明 | 状态 |
|---------|--------|------|
| `src/scraper/news_spider.py` | 爬取新闻数据 | 示例 |
| `src/data_process/csv_cleaner.py` | 清理 CSV 文件 | 示例 |
| `src/api_serve/serve_data.py` | 启动数据 API 服务 | 示例 |

## 违规示例（严禁）
- ❌ 脚本名：`script.py`, `test.py`, `tmp.py`, `main.py` - 不清晰，违反命名规范
- ❌ 输出文件到根目录：脚本生成的文件在 `/Users/agentj/Documents/VSC/localscript/` 而不是脚本目录内
- ❌ 硬编码 API Key：`api_key = "sk_xxx"` 而不是从环境变量读取
- ❌ 脚本间调用：`from src.scraper.spider import func` 应改为从 `src/lib` 导入公共模块
- ❌ 混杂多个功能：一个脚本既爬数据、又处理数据、又生成报告
- ❌ 无版本号依赖：`requirements.txt` 中写 `requests` 而不是 `requests>=2.31.0`
- ❌ 每个脚本目录创建独立 venv：应使用根目录的虚拟环境

## 设计目的
- 让每个脚本的功能一目了然，避免故意混淆或模糊。
- 让依赖管理集中、版本可控、可复现。
- 让目录结构清晰，扩展到几百个脚本也不会混乱。
- 让 AI 和新开发者进来时，看到具体、明确、可验证的规范，无法故意曲解。
- 让脚本执行环境独立、输出隔离、便于维护和调试。
