# MarkItDown Toolkit

基于 [microsoft/markitdown](https://github.com/microsoft/markitdown) 的便携增强工具集。

## 新增功能

- **`convert.bat`** — Windows 一键批量转换，双击即可将当前目录下所有文件转为 Markdown
- **`scripts/batch_convert.py`** — 批量转换核心脚本，也支持命令行调用

## 快速开始

```bash
# 1. 安装 markitdown（只需要一次）
pip install markitdown[all]

# 2. 双击 convert.bat，或将文件/文件夹拖拽到 convert.bat 上
```

## 命令行用法

```bash
# 转换当前目录所有文件
python scripts/batch_convert.py . --out md_output --recursive

# 转换单个文件
python scripts/batch_convert.py example.pdf

# 指定输出目录
python scripts/batch_convert.py ./docs --out ./markdown --recursive
```

## 注意事项

- 如果系统有代理但无法联网，`convert.bat` 会自动清除代理变量
- 输出目录默认为源目录下的 `md_output/`
- 首次运行若未安装 markitdown，脚本会询问是否自动安装

## 许可证

MIT License（与上游一致）
