# Python Office365 Word

<!--last modify: 20230814-->

常用库：python-docx、

- 参考：
  - docs：
    - [python-docx word](https://blog.csdn.net/naer_chongya/article/details/131429885)

## 0x01 python-docx

- paragraphs.style.name
  - {'Normal', 'Heading 2', 'Heading 3', 'Heading 1', 'Footer'}

```python
from docx import Document

# 打开 Word 文档
doc = Document('example.docx')

# 遍历文档中的段落
for para in doc.paragraphs:
    print(para.text)

paragraphs = {para.text: para.style.name for para in doc.paragraphs}
for key, value in paragraphs.items():
    print(f'{value}: {key}')

# 文本块，一个段落（Paragraph）可以包含多个文本块（Run），每个文本块可以有不同的格式（例如字体、颜色、大小等）。
# runs 属性是一个列表，包含了段落中的所有文本块。
for para in doc.paragraphs:
    inlines = para.runs
    for inline in inlines:
        logger.info(inline.text)

# 遍历文档中的表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

## 0x02 docx2pdf

```python
from docx2pdf import convert

def docx2pdf(self, file_path):
    """
    将 Word 文档转换为 PDF 文件。

    Args:
        file_path (str): 要转换的 Word 文档路径。
    """
    # 调用 docx2pdf 库将 Word 文档转换为 PDF 文件
    convert(file_path)
```

## 0x03 doc8

