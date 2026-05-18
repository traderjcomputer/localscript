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
  - **多源问题处理**（**重要**）：
    - 如果同一功能有多个"源"或"变种"（如多个新闻网站、多个数据源），必须在脚本名或目录中明确标识源。
    - **方案 1 - 源标识后缀**：脚本名包含源名称，如 `news_spider_sina.py`, `news_spider_tencent.py`, `news_spider_netease.py`。
    - **方案 2 - 源隔离目录**：在类别下创建源子目录，如 `src/scraper/sina/news_spider.py`, `src/scraper/tencent/news_spider.py`。
    - 选择哪种方案由项目根据源的数量和复杂度决定，但**必须一致**，不能混用。
    - 源的名称必须清晰简洁，例如不要用 `news_spider_v1.py`、`news_spider_new.py` 这种模糊名称。
  - **禁止使用**：`script1.py`, `test.py`, `main.py`, `temp.py`, `misc.py`, `tmp` 等无意义的名称。
  - **禁止使用**：`news_spider_v1.py`, `news_spider_new.py`, `news_spider_backup.py` 等含有版本号或状态标记的名称。
  - 文件名即说明：看到文件名应该能理解脚本用途和对应的源，不需要额外文档。
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

## 数据存储与 Git 规范
本仓库的 `.gitignore` 遵循以下原则，所有开发者和 AI 必须遵守。

### 什么提交到 Git
- ✅ 所有脚本源代码（`.py` 文件）
- ✅ `requirements.txt` 和 `pyproject.toml`（依赖声明）
- ✅ `README.md` 和 `.github/copilot-instructions.md`（文档和规范）
- ✅ `src/lib/` 下的共享代码库
- ✅ 配置文件骨架（仅结构，不含敏感信息）
- ✅ `*/data/` 目录下的源输入数据（如果脚本需要）

### 什么不提交到 Git（由 .gitignore 自动忽略）
- ❌ `venv/` - 虚拟环境（每个开发者本地生成）
- ❌ `*/logs/` - 每个脚本的日志文件（运行时生成）
- ❌ `*/output/` - 每个脚本的输出数据（运行时生成）
- ❌ `*/temp/` - 每个脚本的临时文件（运行时生成）
- ❌ `*/config/` - 配置文件（可能包含敏感信息）
- ❌ `__pycache__/`, `*.pyc` - Python 缓存
- ❌ `.vscode/`, `.idea/` - IDE 个人配置
- ❌ `.DS_Store`, `Thumbs.db` - 操作系统文件

### 关键规范
1. **源数据**：如果脚本需要输入数据，必须放在 `*/data/` 目录，这些数据会被提交。
2. **输出数据**：脚本生成的输出数据放在 `*/output/`，**绝不提交**。
3. **日志文件**：所有脚本的日志都在 `*/logs/`，**绝不提交**。
4. **配置敏感信息**：
   - `*/config/` 下的配置文件骨架可以提交（仅包含结构）
   - 实际的 API Key、密码等敏感值，只能从环境变量或命令行参数注入
   - `*/config/` 本身在 `.gitignore` 中被忽略
5. **虚拟环境**：
   - 每个开发者在根目录运行 `python3 -m venv venv` 生成自己的虚拟环境
   - 虚拟环境**绝不提交**到 Git
6. **临时和缓存文件**：
   - 所有缓存和临时文件都在 `*/temp/`，**绝不提交**

### 为什么这样做
- **仓库大小**：避免提交生成的数据、日志、缓存，保持仓库精简
- **可复现性**：依赖版本明确（`requirements.txt`），输出可重新生成
- **安全性**：敏感信息不进入版本控制历史
- **团队协作**：每个开发者的本地环境独立，不会相互干扰
- **清晰性**：一目了然知道哪些是源代码，哪些是运行结果

## 日志管理规范（Logging Standards）
所有脚本必须实现**工业级日志**。日志文件位置：`src/<类别>/<脚本>/logs/`。

### 日志文件规范
- **文件位置**：`src/<类别>/<脚本>/logs/<日期>.log`，例如 `src/scraper/sina/logs/2026-04-30.log`
- **单文件大小限制**：单个 `.log` 文件不超过 **30MB**（超过后自动轮转）
- **文件夹总容量**：`logs/` 文件夹总大小不超过 **100MB**（超过后自动清理旧日志）
- **保留策略**：日志文件保留最近 **30 天**，更旧的日志自动删除

### 日志轮转策略（Rolling Policy）
脚本必须使用 `RotatingFileHandler` 或等效方案：
- **按大小轮转**：当单文件达到 30MB 时，自动轮转为 `.log.1`, `.log.2` 等
- **按时间轮转**：每天午夜 00:00 自动切换到新的日期文件
- **备份名称**：`<日期>.log.1`, `<日期>.log.2`（最多保留 3 个备份）

### 日志级别与内容规范

| 级别 | 用途 | 记录示例 | 频率 |
|------|------|--------|------|
| **DEBUG** | 开发调试 | 函数入参、中间变量、API 响应原文 | 仅开发环境 |
| **INFO** | 重要流程 | "开始爬取新闻"、"已处理 1000 条记录"、"数据导出成功" | 正常 |
| **WARNING** | 潜在问题 | "网络超时，重试第 2 次"、"字段缺失，使用默认值" | 按需 |
| **ERROR** | 错误 | "API 返回 500 错误"、"数据库连接失败" | 关键问题 |
| **CRITICAL** | 严重故障 | "脚本主进程崩溃"、"存储空间不足无法继续" | 极少 |

### 什么必须记录（✅ DO）
- ✅ 脚本启动时间和版本信息：`Script started. Version: 1.0, PID: 12345`
- ✅ 关键业务流程：`Starting to fetch news from API`, `Processed 100 items`
- ✅ 重试和失败恢复：`Request failed, retrying (attempt 2/3)`, `Recovered from network error`
- ✅ 数据统计摘要：`Total records processed: 5000, Success: 4950, Failed: 50`
- ✅ 异常堆栈跟踪：使用 `logger.exception()` 记录完整的错误信息
- ✅ 脚本结束状态：`Script completed successfully in 123.45 seconds` 或 `Script failed with error: XXX`
- ✅ 性能指标：`Average response time: 250ms, Total requests: 1000`

### 什么禁止记录（❌ DON'T）
- ❌ 敏感信息：API Key、密码、令牌、个人隐私数据
- ❌ 整个 API 响应体（如果包含大量数据）：只记录摘要或状态码
- ❌ 用户输入的完整内容（如果是敏感数据）：只记录摘要或 hash
- ❌ 系统路径或用户名：除非必要调试
- ❌ 频繁的重复日志：例如循环体内每次都记录相同信息（应改为循环后记录统计）

### 日志格式标准
```
%(asctime)s | %(name)s | %(levelname)-8s | %(message)s
```

示例：
```
2026-04-30 14:23:45,678 | scraper.sina | INFO     | Starting to fetch news from https://news.sina.com.cn
2026-04-30 14:23:50,123 | scraper.sina | INFO     | Successfully fetched 50 articles
2026-04-30 14:24:15,456 | scraper.sina | WARNING  | Request timeout, retrying (attempt 2/3)
2026-04-30 14:25:00,789 | scraper.sina | ERROR    | Failed after 3 attempts. Error: Connection refused
2026-04-30 14:25:01,234 | scraper.sina | INFO     | Script completed with 50 successes, 0 failures in 76.23 seconds
```

### 关键风险与对策（CRITICAL）

**风险 1：日志丢失（Crash Loss）**
- 问题：Python 日志库使用缓冲区。当脚本突然崩溃、被强杀或系统故障时，缓冲区的日志还未写入磁盘，就丢失了。
- 后果：最需要日志的时刻（崩溃发生）反而最容易丢失日志。
- **强制要求**：
  - ✅ 关键日志（ERROR、CRITICAL、业务流程的结束）**必须**立即调用 `logger.flush()` 或 `handler.flush()` 确保写入磁盘
  - ✅ 在脚本主函数最外层**必须**使用 try-except-finally 确保即使发生异常也能刷新和记录
  - ⚠️ 考虑使用异步日志或无缓冲模式（需深入测试性能影响）

**风险 2：日志洪泛（Log Flooding）**
- 问题：在循环或高频操作中每次都记录日志，导致文件极速增长，可能在几分钟内突破 30MB 限制。
- 后果：日志轮转失效，磁盘满，脚本无法继续运行。
- **强制要求**：
  - ✅ 循环体内**禁止**频繁记录相同或类似日志，**必须**改为循环后记录统计摘要
  - ✅ 例如：❌ `for item in items: logger.info(f"Processing {item}")` 必须改为 ✅ `logger.info(f"Processed {len(items)} items")`
  - ✅ 高频操作（如网络请求）**只能**记录异常，不能记录成功日志

**风险 3：敏感信息泄露（Information Disclosure）**
- 问题：日志存储在本地文件系统。如果包含 API Key、密码等敏感信息，可能被恶意访问者获取。
- **强制要求**：
  - ✅ 任何敏感信息都**禁止**进入日志，包括 API Key、令牌、密码、个人隐私数据
  - ✅ 如果**必须**记录某个值，**必须**使用 hash 或掩码（如 `api_key=sk_***abc123`）

### 日志规范强制要求清单

| 项目 | 要求级别 | 说明 |
|------|---------|------|
| 文件位置 | ✅ 强制 | `src/<类别>/<脚本>/logs/<日期>.log` |
| 单文件 30MB 限制 | ✅ 强制 | 必须自动轮转 |
| 文件夹 100MB 限制 | ✅ 强制 | 必须自动清理旧日志 |
| 30 天保留策略 | ✅ 强制 | 必须自动删除超过 30 天的日志 |
| 关键日志立即 flush | ✅ 强制 | ERROR、CRITICAL、流程结束必须 flush |
| 循环内禁止频繁日志 | ✅ 强制 | 循环后记录统计摘要 |
| 敏感信息禁止 | ✅ 强制 | 不能写 API Key、密码 |
| 日志格式统一 | ✅ 强制 | `%(asctime)s \| %(name)s \| %(levelname)-8s \| %(message)s` |
| 脚本启动日志 | ✅ 强制 | 必须记录启动时间、版本、PID |
| 脚本结束日志 | ✅ 强制 | 必须记录完成状态、耗时、成功失败统计 |
| 异常堆栈记录 | ✅ 强制 | 用 `logger.exception()` 记录完整堆栈 |
| 重试日志 | ✅ 强制 | 每次重试必须记录 WARNING |

### 待验证与后续改进
以下方面已知存在问题，需要实战验证和后续版本改进：
- **日志缓冲与崩溃恢复**：如何正确处理信号（SIGTERM、SIGINT）和异常以确保日志被完整刷新
- **多进程/异步日志协调**：在多进程或异步场景下确保日志不交错、不丢失
- **性能影响**：频繁 flush 和缓冲刷新对脚本性能的实际影响
- **阈值调整**：30MB 和 100MB 是否合理，需根据实际运行数据调整
- **日志监控工具**：后续应提供工具来检测日志丢失和洪泛问题

## 脚本健壮性与错误处理规范
所有脚本必须实现以下错误处理和恢复机制，确保在各种异常情况下能正确记录和恢复。

### 异常分类与处理
脚本应该识别并区分以下类型的异常：

| 异常类型 | 示例 | 处理策略 |
|---------|------|--------|
| **网络异常** | 连接超时、DNS 失败、API 返回 5xx | 自动重试（指数退避），日志记录重试次数 |
| **数据异常** | 字段缺失、格式错误、编码问题 | 跳过此项或使用默认值，记录 WARNING |
| **资源异常** | 磁盘满、内存不足、文件权限错误 | 记录 CRITICAL，优雅退出 |
| **业务异常** | API 返回 4xx、无效参数、业务规则不符 | 根据具体情况决定（重试、跳过、失败） |
| **系统异常** | KeyboardInterrupt、SIGTERM、进程崩溃 | 清理资源，刷新日志，记录最后状态 |

### 重试策略（Retry Pattern）
对于网络请求或 API 调用，应实现以下重试机制：
- **重试次数**：最多 3 次
- **重试等待**：使用指数退避（1秒、2秒、4秒）
- **不重试的错误**：API 返回 4xx（除 429）、无效参数、鉴权失败
- **必须记录**：每次重试都记录 WARNING，包括重试次数和等待时间
- 示例：`2026-04-30 14:25:00 | scraper.sina | WARNING  | Request failed (500), retrying in 2 seconds (attempt 2/3)`

### 脚本退出规范
- **正常退出**（exit code 0）：所有任务完成，数据已保存，日志已刷新
- **部分成功退出**（exit code 1）：有失败项但整体可接受，记录失败统计，日志已刷新
- **失败退出**（exit code 2）：无法继续，记录错误原因，日志已刷新
- **系统错误退出**（exit code >128）：系统级别错误（如 SIGTERM = 143），资源已清理

### 数据一致性保证
- **原子操作**：写文件时先写临时文件，成功后重命名，失败时删除临时文件
- **断点续传**：对于长流程，记录检查点，允许从检查点恢复而不重新开始
- **输出验证**：输出文件生成后必须验证（检查大小、行数、格式），异常则删除

### 当前版本约束
本版本日志规范标记为初版，以下方面需要后续深入打磨和实战验证：
- 日志缓冲与崩溃恢复的完整解决方案
- 多进程/异步场景下的日志协调
- 日志大小阈值的实际数据验证

## 其他规则打磨计划
以下规则需要继续深入和完善：
- **配置管理**：环境变量、配置文件、参数优先级
- **依赖冲突**：版本兼容性问题处理
- **性能监控**：脚本执行时间、资源使用统计
- **数据质量**：输出数据的验证和质量检查
- **并发控制**：多脚本运行时的资源竞争和锁机制
- **备份与恢复**：数据丢失或损坏时的恢复方案



## 目录组织与规模控制
- `src/`：主脚本目录。
- `src/<类别>/`：按功能类别分组。类别应该用英文单词表示，如 `scraper`, `data_process`, `api_serve`, `analysis`。
  - 每个类别名称应该清晰表达其用途，看到名称就知道该目录里的脚本做什么。
- `src/<类别>/<脚本>.py`：脚本文件。
- **多源隔离结构**（当脚本有多个源/变种时）：
  - **选择方案**：`src/<类别>/<源>/<脚本>.py`，例如 `src/scraper/sina/news_spider.py`, `src/scraper/tencent/news_spider.py`。
  - 源目录名必须清晰，如 `sina`, `tencent`, `netease`，禁止用 `source1`, `src_a` 等模糊名称。
- `src/lib/`：共享代码库。所有脚本可以导入这里的模块。
- 每个脚本的工作目录可包含子目录：
  - `logs/` - 日志文件
  - `output/` - 输出数据
  - `temp/` - 临时文件
  - `config/` - 配置文件（结构定义，不含敏感值）
  - `data/` - 输入数据（如需要）
- 脚本数量超过 10 个时，建议在每个类别或源目录下添加 `README.md`，列出该目录的所有脚本及其功能说明。
- **禁止使用**：目录名 `misc/`, `temp/`, `test/`, `old/`, `source1/`, `src_a/` 等无意义的名称。

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
| `src/scraper/google/news_spider.py` | 从 Google News 爬取新闻文章 | ✅ 活跃 |
| `src/scraper/sina/news_spider.py` 或 `src/scraper/news_spider_sina.py` | 爬取新浪新闻数据 | 示例 |
| `src/scraper/tencent/news_spider.py` 或 `src/scraper/news_spider_tencent.py` | 爬取腾讯新闻数据 | 示例 |
| `src/data_process/csv_cleaner.py` | 清理 CSV 文件 | 示例 |
| `src/api_serve/serve_data.py` | 启动数据 API 服务 | 示例 |

## 违规示例（严禁）
- ❌ 脚本名：`script.py`, `test.py`, `tmp.py`, `main.py` - 不清晰，违反命名规范
- ❌ **命名冲突**：多个新闻爬虫都叫 `news_spider.py`，导致无法区分 - 应该用 `news_spider_sina.py`, `news_spider_tencent.py` 或 `src/scraper/sina/news_spider.py`
- ❌ 混用两种源隔离方案：有些脚本用 `news_spider_sina.py`，有些用 `src/scraper/sina/news_spider.py` - 必须统一
- ❌ 模糊的源名称：`news_spider_v1.py`, `news_spider_new.py`, `news_spider_backup.py` - 应该用清晰的源标识
- ❌ 无意义的源目录：`src/scraper/source1/`, `src/scraper/src_a/` - 应该用 `sina`, `tencent` 等具体名称
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
- **让同一功能的多个源或变种可以并存，无命名冲突**，通过源标识或源目录区分。
- 让 AI 和新开发者进来时，看到具体、明确、可验证的规范，无法故意曲解。
- 让脚本执行环境独立、输出隔离、便于维护和调试。
