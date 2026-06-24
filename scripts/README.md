批量转换脚本 — 使用说明

- **脚本位置**: `scripts/batch_convert.py`
- **功能**: 将 PDF/Word/PPT/Excel/HTML/EPUB/CSV 等文档批量转换为 Markdown (.md)
- **需要**: markitdown 已安装（`pip install 'markitdown[all]'`）

## 快速使用

### 方式一：双击 bat 文件（最简单）
1. 将 `convert.bat` 复制到需要转换的文件夹
2. 双击运行
3. 转换后的 `.md` 文件会保存在 `md_output` 子文件夹中

也可以将文件/文件夹直接拖拽到 `convert.bat` 图标上。

### 方式二：命令行
```powershell
# 递归转换当前目录，输出到 md_output
python scripts/batch_convert.py . --out md_output --recursive

# 转换单个文件
python scripts/batch_convert.py document.pdf

# 只转换特定类型
python scripts/batch_convert.py . --exts pdf,docx --recursive

# 添加更多格式（如图片、音频）
python scripts/batch_convert.py . --exts pdf,docx,jpg,png,mp3 --recursive
```

## 支持的格式（默认）
- PDF (.pdf)
- Word (.docx, .doc)
- PowerPoint (.pptx, .ppt)
- Excel (.xlsx, .xls)
- CSV (.csv)
- HTML (.html, .htm)
- EPUB (.epub)
- Jupyter Notebook (.ipynb)
- Outlook 邮件 (.msg)

其他格式（图片、音频、ZIP 等）可通过 `--exts` 参数手动指定。

## 故障排查

| 问题 | 解决方法 |
|------|---------|
| `No matching files found` | 确认文件夹中有支持的格式，或用 `--exts` 指定扩展名 |
| `markitdown is not installed` | 运行 `pip install 'markitdown[all]'` |
| 代理/网络错误 | 脚本已自动清除代理设置。如果还出错，检查系统环境变量 |
