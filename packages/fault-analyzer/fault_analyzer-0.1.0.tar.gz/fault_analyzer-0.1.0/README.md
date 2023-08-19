# Pump Failure Analyzer

Pump Failure Analyzer 是一个用于分析水泵故障的 Python 工具。


## 安装

确保已经安装了 Python 3。然后使用以下命令安装 Pump Failure Analyzer：


## 使用方法

### 1. 准备数据

将要分析的水泵故障数据存储为 CSV 文件。确保文件中包含以下列：
- `timestamp`: 时间戳
- `oilFlow`: 油流量数据
- `inletOilPres`: 传感器2数据
- ...

示例数据文件可以在 `examples/` 目录中找到。

### 2. 运行分析

使用以下命令运行 Pump Failure Analyzer：


其中 `data.csv` 是你准备的数据文件路径，`result.csv` 是分析结果的输出文件路径。

### 3. 查看分析结果

分析结果将保存在 `result.csv` 文件中。你可以使用任何你喜欢的工具或库加载和查看结果文件。

## 特性

Pump Failure Analyzer 提供以下特性：

- 高效的水泵故障分析算法。
- 支持自定义数据列和输出结果。
- 简单易用的命令行界面。

## API 文档

当前版本的 Pump Failure Analyzer 不提供 API。

## 贡献

欢迎贡献代码、报告问题或提出改进建议。请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 获取更多信息。

## 版权和许可

版权所有 © 2023 hu nan

Pump Failure Analyzer 使用 MIT 许可证。请查看 [LICENSE](LICENSE) 获取更多信息。