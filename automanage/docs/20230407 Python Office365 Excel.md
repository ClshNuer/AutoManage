# Python Office365 Excel

<!--last modify: 20230812-->



常用库：xlwings、xlsxwriter、xlrd、xlwt、pandas、win32com、xlutils等

- 参考
  - docs
    - [Python 操作 Excel 用到的库](https://zhuanlan.zhihu.com/p/566726405)

## 0x00 xlwt

### 0x00x000 create data

```python
import xlwt

# Define the movie data as a list of tuples
movie_data = [
    ('影片', '综合票房', '票房占比', '排片场次'),
    ('如果声音记不得', 361.57, 33.3, 95371),
    ('赤狐先生', 194.23, 17.8, 79980),
    ('除暴', 130.05, 11.8, 42457),
    ('疯狂原始人2', 120.72, 10.9, 40697)
]

# Create a new workbook and worksheet
wb = xlwt.Workbook()
sh1 = wb.add_sheet('电影')

# Write the movie data to the worksheet using a for loop
for row_idx, row_data in enumerate(movie_data):
    for col_idx, cell_data in enumerate(row_data):
        sh1.write(row_idx, col_idx, cell_data)

# Save the workbook
wb.save('01_电影数据.xlsx')

# python 01_xlwt_create_data_excel.py
```

### 0x00x00x xx

- xlwt

  ```python
  # import xlwt
  try:
      import xlwt
  except:
      # pip install xlwt
      import os
      os.system('pip install xlwt')
      import xlwt
  
  # create excel
  wb = xlwt.Workbook()
  
  # add sheet
  sheet_test = wb.add_sheet('data')
  
  # write data to sheet
  row = col = 0
  sheet_test.write(row, col, 'data_name' )
  
  # save excel
  wb.save('test.xlsx')
  ```

- example

  ```python
  # xlwt.Workbook()
  def reset_workbook(self):
          self._workbook = Workbook()
          self._sheets = {}
          self._columns = defaultdict(list)
          self._current_index = defaultdict(lambda: 1)
          self._generated_sheet_name_dict = {}
  
  def open(self, file_path: str) -> None:
          try:
              import xlwt
          except ImportError:
              warnings.warn(import_error_msg_template.format("excel"))
              raise
  
          self._workbook = xlwt.Workbook()
  
  def create_workbook_with_sheet(name):
      """Removes non-alpha-numerical values in name."""
      book = xlwt.Workbook()
      valid_name = re.sub(r'[^\\.0-9a-zA-Z]+', '', os.path.basename(name))
      sheet1 = book.add_sheet(valid_name)
      return book, sheet1
  ```

  ```python
  # xlwt.Workbook.add_sheet()
  def write_cells(book):
      sheet = book.add_sheet('Content')
      sheet.write(0,0,'A1',style1)
      sheet.write(0,1,'B1',style2)
      sheet.write(0,2,'C1',style3)
  
  def create_workbook_with_sheet(name):
      """Removes non-alpha-numerical values in name."""
      book = xlwt.Workbook()
      valid_name = re.sub(r'[^\\.0-9a-zA-Z]+', '', os.path.basename(name))
      sheet1 = book.add_sheet(valid_name)
      return book, sheet1
  
  def create(self, sheet="Sheet"):
          fd = BytesIO()
          try:
              book = xlwt.Workbook()
              book.add_sheet(sheet)
              book.save(fd)
              fd.seek(0)
              self.open(fd)
          finally:
              fd.close()
  
          self._extension = None
  ```

  ```python
  # xlwt.Workbook.add_sheet.write()
  def test_intersheets_ref(self):
          book = xlwt.Workbook()
          sheet_a = book.add_sheet('A')
          sheet_a.write(0, 0, 'A1')
          sheet_a.write(0, 1, 'A2')
          sheet_b = book.add_sheet('B')
          sheet_b.write(0, 0, xlwt.Formula("'A'!$A$1&'A'!$A$2"))
          out = BytesIO()
          book.save(out)
  
  def saveToExcel(videoInfoList):
      workbook=xlwt.Workbook()
      sheet1=workbook.add_sheet('sheet1',cell_overwrite_ok=True)
  
      k=0
      for i in range(10000):
          for j in range(9):
              print('正在写入的行和列是',i,j)
              sheet1.write(i,j,videoInfoList[k])
              k+=1
      workbook.save('E:\\\\MyFile\\\\PythonSpider\\\\91Best\\\\top78000.xls')
  
  def write_excel_xls(path, sheet_name, value):
      index = len(value)  # 获取需要写入数据的行数
      workbook = xlwt.Workbook()  # 新建一个工作簿
      sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
      for i in range(0, index):
          for j in range(0, len(value[i])):
              sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
      workbook.save(path)  # 保存工作簿
      print("xls格式表格写入数据成功！")
  ```

## 0x01 xlrd

### 0x01x000 read_data

```python
import xlrd

# Open the Excel file using a context manager
with xlrd.open_workbook('01_电影数据.xlsx') as wb:
    # Get the first sheet
    sh1 = wb.sheet_by_index(0)

    # Print the number of rows and columns
    print(f'sheet里面一共有{sh1.nrows}行 {sh1.ncols}列的数据')

    # Get the value of a single cell
    print(f'第一行第二列的值：{sh1.cell_value(0,1)}')

    # Get the values of an entire row or column using list comprehension
    row_values = [sh1.cell_value(0, col) for col in range(sh1.ncols)]
    col_values = [sh1.cell_value(row, 0) for row in range(sh1.nrows)]
    print(row_values)
    print(col_values)

    # Iterate over all cells using nested loops
    for row_idx in range(sh1.nrows):
        for col_idx in range(sh1.ncols):
            print(f'第{row_idx}行 第{col_idx}列的数据是 {sh1.cell_value(row_idx, col_idx)}')
            
# python 02_xlrd_read_data_excel.py
```

### 0x01x00x xx

- xlrd

  ```python
  # import xlrd
  try:
      import xlrd
  except:
      # pip install xlrd
      import os
      os.system('pip install xlrd')
      import xlrd
  
  # open excel
  wb = xlrd.open_workbook('test.xlsx')
  
  # sheet num
  sheet_num = wb.nsheets
  # sheet name
  sheet_list = wb.sheet_names()
  
  # select sheet
  sheet_name = sheet_list[0]
  
  # select sheet object
  sheet_name = wb.sheet_by_index(0)
  sheet_name = wb.sheet_by_name(f'{sheet_list[0]}')
  
  # sheet_name row, col
  nrows = sheet_name.nrows
  ncols = sheet_name.ncols
  
  # obtain data[row, col]
  data_cell = sheet_name.cell_value(0,0)
  data_cell = sheet_name.cell(0,0).value
  data_cell = sheet_name.row(0)[0].value
  
  # obtain data[row]
  data_row = sheet_name.row_values(0)
  
  # obtain data[col]
  data_col = sheet_name.col_values(0)
  
  # obtain data all
  for row in range(sheet_name.nrows):
      for col in range(sheet_name.ncols):
          print(row, col, sheet_name.cell_value(row, col))
  ```

- example

  ```python
  # xlrd.open_workbook()
  def setUp(self):
          path = from_sample('biff4_no_format_no_window2.xls')
          self.book = open_workbook(path)
          self.sheet = self.book.sheet_by_index(0)
  
  def xlsx_do_file(afile):
      try:
          axl = open_workbook(afile)
      except XLRDError as e:
          log_error(str(e), afile)
          return
      xlsx_do_xlsx(axl, afile)
  
  def get_sheet(sheet_index):
      workbook = xlrd.open_workbook(workbook_origin_path)
      sheet_name = workbook.sheet_names()[sheet_index]
      return workbook.sheet_by_name(sheet_name)
  ```

  ```python
  # xlrd.open_workbook.sheet_names()
  def get_sheet(sheet_index):
      workbook = xlrd.open_workbook(workbook_origin_path)
      sheet_name = workbook.sheet_names()[sheet_index]
      return workbook.sheet_by_name(sheet_name)
  
  def read_excel_xls(path):
      data = []
      workbook = xlrd.open_workbook(path)  # 打开工作簿
      sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
      worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
      if worksheet.nrows == 1:
          print("目前是第一行")
      else:
          for i in range(1, worksheet.nrows): #从第二行取值
              dataTemp = []
              for j in range(0, worksheet.ncols):
                  #print(worksheet.cell_value(i, j), "\\t", end="")  # 逐行逐列读取数据
                  dataTemp.append(worksheet.cell_value(i, j))
              data.append(dataTemp)
      return data
  
  def parse_excel(dtype, addr, fline, tline, nan):
      try:
          import xlrd
      except ImportError:
          raise ImportError('DaPy uses "xlrd" to parse a excel file, '+\\
                            'please try command: pip install xlrd.')
  
      book = xlrd.open_workbook(addr)
      for sheet, name in zip(book.sheets(), book.sheet_names()):
          try: 
              series_set = SeriesSet(None, None, nan)
              for cols in range(sheet.ncols):
                  column = Series(sheet.col_values(cols))
                  title = column[tline].strip() if tline >= 0 else None
                  series_set.append_col(column[fline:], title)
              yield series_set, name
          except UnicodeEncodeError:
              warn('can not decode characters, use `DaPy.io.encode()` to fix.')
  ```

  ```python
  # xlrd.open_workbook.sheet_by_index()
  def extract_column_names(path, dialect, **kwargs):
      book = xlrd.open_workbook(path, on_demand=True)
      sheet = book.sheet_by_index(0)
      headers = sheet.row_values(0)
  
      return headers
  
  def read_xls(self, file):
          try:
              workbook = xlrd.open_workbook(file)
              sheet1 = workbook.sheet_by_index(0)
              column = sheet1.col_values(3)
              return self.filter(column)
          except Exception as e:
              exit(e)
  
  def read_excel(self, excel_file):
          data = xlrd.open_workbook(excel_file)
          table = data.sheet_by_index(0)
          nrows = table.nrows
          for r in range(nrows):
              key = table.cell(r, 0).value
              val = table.cell(r, 1).value
              self.trans_resource[key] = val
  ```

  ```python
  # xlrd.open_workbook.sheet_by_name()
  def get_sheet(sheet_index):
      workbook = xlrd.open_workbook(workbook_origin_path)
      sheet_name = workbook.sheet_names()[sheet_index]
      return workbook.sheet_by_name(sheet_name)
  
  def read_xlsx_file(path, file_name):
  	book = xlrd.open_workbook(path + file_name)
  	sh = book.sheet_by_name("Sheet1")
  	list = []
  	for i in range(1, sh.nrows):
  		list.append(sh.row_values(i))
  	return list
  
  def parse_excel(input_filename):
      with open_workbook(input_filename) as wb:
          service_sheet = wb.sheet_by_name('Service')
          services = list(parse_service_sheet(service_sheet))
      return services
  ```

  ```python
  # xlrd.open_workbook.sheet_by_name.cell()
  def test_ignore_diagram(self):
          sheet = self.book.sheet_by_name(u('Blätt3'))
          cell = sheet.cell(0, 0)
          self.assertEqual(cell.ctype, xlrd.book.XL_CELL_NUMBER)
          self.assertEqual(cell.value, 100)
          self.assertTrue(cell.xf_index > 0)
  
  def test_get_from_merged_cell(self):
          sheet = self.book.sheet_by_name(u('ÖÄÜ'))
          cell = sheet.cell(2, 2)
          self.assertEqual(cell.ctype, xlrd.book.XL_CELL_TEXT)
          self.assertEqual(cell.value, 'MERGED CELLS')
          self.assertTrue(cell.xf_index > 0)
  
  def test_calculated_cell(self):
          sheet2 = self.book.sheet_by_name('PROFILELEVELS')
          cell = sheet2.cell(1, 3)
          self.assertEqual(cell.ctype, xlrd.book.XL_CELL_NUMBER)
          self.assertAlmostEqual(cell.value, 265.131, places=3)
          self.assertTrue(cell.xf_index > 0)
  ```

  ```python
  # xlrd.open_workbook.sheet_by_name.row_values()
  def read_xlsx_file(path, file_name):
  	book = xlrd.open_workbook(path + file_name)
  	sh = book.sheet_by_name("Sheet1")
  	list = []
  	for i in range(1, sh.nrows):
  		list.append(sh.row_values(i))
  	return list
  
  def getXY(filename):
      import xlrd
      data = xlrd.open_workbook(filename)  # 打开excel
      table = data.sheet_by_name("test")  # 读sheet
      nrows = table.nrows  # 获得行数
  
      xy = []
      for i in range(1, nrows):  #
          rows = table.row_values(i)  # 行的数据放在数组里:
          if rows[0].strip()!='':
              result = []
              result.append(float(rows[0].split(',')[1]))
              result.append(float(rows[0].split(',')[2]))
              xy.append(result)
              
      print(xy)
      return xy
  
  def import_project(self):
          filepath = QFileDialog.getOpenFileName(self, 'Import project', 
                                                          self.path_projects)[0]
          book = xlrd.open_workbook(filepath)
          for obj_type, obj_class in (('nodes', Node), ('links', Link)):
              sheet = book.sheet_by_name(obj_type)
              properties = sheet.row_values(0)
              for row in range(1, sheet.nrows):
                  obj_class(self, **dict(zip(properties, sheet.row_values(row))))
          self.view.generate_objects()
  ```

## 0x02 xlutils

```python
import xlrd
from xlutils.copy import copy

# Open the Excel file using a context manager
with xlrd.open_workbook('01_电影数据.xlsx') as read_book:
    # Copy the data to a new workbook
    wb = copy(read_book)

    # Select the first sheet
    sh = wb.get_sheet(0)

    # Write the new row of data using the write_row method
    new_row = ['保家卫国', 113, 5.1, 490]
    sh.write_row(5, 0, new_row)

    # Add a new sheet for the summary data
    sh2 = wb.add_sheet('汇总数据')

    # Calculate the sum of the values in the fourth column using list comprehension
    count = sum([rs.cell_value(i, 3) for i in range(1, rs.nrows)])

    # Write the summary data to the new sheet
    sh2.write(0, 0, '总票房')
    sh2.write(0, 1, count)

    # Save the modified workbook
    wb.save('02_电影数据(修改).xlsx')
    
    # python 03_xlutils_modify_data_excel.py
```

## 0x03 excel xlwt

```python
# import xlwt
try:
    import xlwt
except:
    # pip install xlwt
    import os
    os.system('pip install xlwt')
    import xlwt

# import xlrd
try:
    import xlrd
except:
    # pip install xlrd
    import os
    os.system('pip install xlrd')
    import xlrd

# import xlutils
try:
    import xlutils
    from xlutils.copy import copy
except:
    # pip install xlutils
    import os
    os.system('pip install xlutils')
    import xlutils
    from xlutils.copy import copy

# create excel
wbw = xlwt.Workbook()
excel_name = 'test.xlsx'

# add data_sheet1
data_sheet1 = wbw.add_sheet('data_sheet1')

# write data to data_sheet1
row = col = 3
i = j = 0
for i in range(row):
    for j in range(col):
        data_sheet1.write(i, j, i + j)

wbw.save(excel_name)

# copy data_sheet1 to data_sheet2
# open excel
rb_excel = xlrd.open_workbook(excel_name)

# copy data_sheet
wbc = copy(rb_excel)

""" # add data to data_sheet1
ds2 = wbc.get_sheet(0)

k = 0
for k in range(i + 1):
    ds2.write(k, i + 1, k + i + 1)

k = 0
for k in range(j + 1):
    ds2.write(j + 1, k, k + j + 1)

ds2.write(i + 1, j + 1, i + j + 2)

wbc.save(excel_name) """

# select data_sheet1
ds1 = rb_excel.sheet_by_index(0)

# add data_sheet2
data_sheet2 = wbc.add_sheet('data_sheet2')

# copy to data_sheet2
i = j = 0
for i in range(ds1.nrows):
    for j in range(ds1.ncols):
        data_sheet2.write(i, j, ds1.cell_value(i, j))

wbc.save(excel_name)

# statistics to data_sheet3 from data_sheet1
# add data_sheet3
data_sheet3 = wbc.add_sheet('data_sheet3')

row_sum = col_sum = 0
ds3 = rb_excel.sheet_by_index(0)

i = j = 0
for j in range(ds3.ncols):
    i = col_sum = 0
    for i in range(ds3.nrows):
        col_sum += ds3.cell_value(i, j)
    data_sheet3.write(0, j, col_sum)

wbc.save(excel_name)
```

## 0x04 excel style

```python
import xlwt
wb = xlwt.Workbook()
sh = wb.add_sheet('data')

ft = xlwt.Font()
ft.name = '微软雅黑' #字体
ft.colour_index = 2 #颜色
ft.height = 11 * 20 #字体大小
ft.bold = True
ft.italic = True
ft.underline = True

sh.row(3).height_mismatch = True
sh.row(3).height = 10 * 256 #单元格高度
sh.col(3).width = 0 * 256 #单元格宽度

style = xlwt.XFStyle()
style.font = ft
sh.write(1, 1, 'data1', style)

alg = xlwt.Alignment()
alg.horz = 2 #1 左，2 中，3 右
alg.vert = 1 #0 上，1 中，2 下
style2 = xlwt.XFStyle()
style2.alignment = alg
sh.write(2, 2, 'data2', style2)

# 边框
# 细实线 1，小粗实线 2，细虚线 3，中细虚线 4，大粗实线 5，双线 6，细点虚线 7；
# 大粗虚线 8，细点划线 9，粗点划先 10，细双点划线 11，粗双点划线 12，斜点划线 13
border = xlwt.Borders()
border.left = 1
border.right = 1
border.top = 1
border.bottom = 1

border.left_colour = 1
border.right_colour = 2
border.top_colour = 3
border.bottom_colour = 4

style3 = xlwt.XFStyle()
style3.borders = border
sh.write(3, 3, 'data3', style3)

# 背景颜色
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 5

style4 = xlwt.XFStyle()
style4.borders = border
sh.write(3, 3, 'data3', style4)

style5 = xlwt.easyxf('font: bold on, color_index 6; align: vert center, horiz center')
def read_data():
    wb = xlrd.open_workbook('')
    sh = wb.sheet_by_index(0)
    fen_type = {}
    count_price = []

    for r in range(sh.nrows):
        count = sh.cell_value(r, 3) * sh.cell_value(r, 4)
        count_price.append(count)
        key = sh.cell_value(r, 0)
        if fen_type.get(key):
            fen_type[key] += count
        else:
            fen_type[ey] = count
        
    return fen_type, count_price
```



## 0x04 openpyxl

```python
import openpyxl

# 创建excel
def create_xlsx_by_openpyxl(self, xlsx_path, sheet_names):
    wb = openpyxl.Workbook()
    sheet = wb.active
    wb.remove(sheet)
    wb = openpyxl.load_workbook(xlsx_path)
    for sheet_name in sheets_name:
        if sheet_name in wb.sheetnames: # wb.sheetnames 所有sheet
            logger.debug(f"Sheet '{sheet_name}' already exists in '{xlsx_path}'. Overwriting content...")
            ws = wb[sheet_name]
            ws.delete_rows(1, ws.max_row)
        else:
            wb.create_sheet(sheet_name)
            logger.debug(f"Create sheet '{sheet_name}' in '{xlsx_path}'.")
    wb.save(xlsx_path)
```

可以使用`pandas.ExcelWriter`类来创建Excel文件，而不是使用`pandas.DataFrame.to_excel`函数。这样可以避免在写入大型数据集时出现内存问题。

wb.create_sheet(sheet) # 如果存在sheet，则不会创建新的sheet；若要覆盖现有sheet，可使用openpyxl.Workbook 类的active 属性来获取现有sheet，然后覆盖

## 0x05 csv

`csv` 库是 Python 内置的用于读写 CSV 文件的库，但是它不支持读取多个 sheet 的 Excel 文件。如果你需要读取 Excel 文件中的多个 sheet，可以使用 `pandas` 库。

