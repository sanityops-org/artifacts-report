# TC-002: Anthropic PDF Skill - Skill 评估用例

## 元信息
- **来源项目**: anthropics/skills
- **许可证**: Proprietary（源码可用，非开源）
- **工件类型**: Skill (SKILL.md)
- **采集日期**: 2026-10-10
- **采集方式**: 直接提取自 skills/pdf/SKILL.md

## 原始工件内容

```markdown
---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
 text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
 reader = PdfReader(pdf_file)
 for page in reader.pages:
 writer.add_page(page)

with open("merged.pdf", "wb") as output:
 writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
 writer = PdfWriter()
 writer.add_page(page)
 with open(f"page_{i+1}.pdf", "wb") as output:
 writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90) # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
 writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
 for page in pdf.pages:
 text = page.extract_text()
 print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
 for i, page in enumerate(pdf.pages):
 tables = page.extract_tables()
 for j, table in enumerate(tables):
 print(f"Table {j+1} on page {i+1}:")
 for row in table:
 print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
 all_tables = []
 for page in pdf.pages:
 tables = page.extract_tables()
 for table in tables:
 if table: # Check if table is not empty
 df = pd.DataFrame(table[1:], columns=table[0])
 all_tables.append(df)

# Combine all tables
if all_tables:
 combined_df = pd.concat(all_tables, ignore_index=True)
 combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Sacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1 # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
 text += f"Page {i+1}:\n"
 text += pytesseract.image_to_string(image)
 text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
 page.merge_page(watermark)
 writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
 writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
 writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
 writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md
```

## 评估维度

### 1. Skill 元数据完整性 (Metadata Completeness)
- [ ] YAML frontmatter 包含必需的 name 字段
- [ ] description 清晰描述触发条件和功能范围
- [ ] license 信息明确标注

### 2. 触发条件明确性 (Trigger Conditions)
- [ ] 触发词覆盖全面（PDF、提取、合并、分割等）
- [ ] 边界情况处理（扫描PDF、加密PDF）
- [ ] 与其他 Skill 的区分度明确

### 3. 指令结构化 (Instruction Structure)
- [ ] 使用清晰的层级标题（Overview、Quick Start、各功能模块）
- [ ] 代码示例与说明配比合理
- [ ] 包含 Quick Reference 速查表

### 4. 代码示例质量 (Code Example Quality)
- [ ] 示例完整可直接运行
- [ ] 涵盖主要使用场景（读取、写入、转换、OCR）
- [ ] 包含常见陷阱提示（如 Unicode 下标问题）

### 5. 可维护性 (Maintainability)
- [ ] 模块化组织（基础操作、高级功能、命令行工具）
- [ ] 外部依赖明确（pypdf、pdfplumber、reportlab 等）
- [ ] 有指向 REFERENCE.md 的扩展阅读链接

## 评分标准
| 维度 | 权重 | 得分 (1-5) | 备注 |
|------|------|------------|------|
| Skill 元数据完整性 | 15% | | |
| 触发条件明确性 | 20% | | |
| 指令结构化 | 25% | | |
| 代码示例质量 | 25% | | |
| 可维护性 | 15% | | |
| **总分** | 100% | | |

## 测试建议

### 正向测试用例
1. 用户请求"提取 PDF 文本"，验证 Skill 是否正确触发
2. 用户请求"合并多个 PDF"，验证代码示例可用性
3. 用户提及扫描 PDF，验证 OCR 流程是否被推荐

### 边界测试用例
1. 加密 PDF 的处理提示
2. 超大 PDF 文件的内存管理建议
3. 复杂表格的提取准确性

### 负面测试用例
1. 非 PDF 文件请求时是否误触发
2. 代码示例中是否存在已弃用的 API
3. 依赖库版本兼容性说明是否缺失

## 备注
- 该 Skill 是 Anthropic 官方文档处理能力的实现参考
- 采用 Proprietary 许可，仅适合结构大纲引用（≤10行），不宜完整复制
- 展示了 Skill 设计的最佳实践：YAML frontmatter + 结构化 Markdown + 丰富代码示例
