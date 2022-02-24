import os
import pandas as pd


def ToExcel(path, excel_name, **params):
    path = os.path.join(path, excel_name)  # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='openpyxl')  # 指定引擎openpyxl
    for i in params.keys():
        df = params.get(i)
        df.to_excel(writer, sheetname=i)  # 存到指定的sheet
    writer.save()  # 存檔生成excel檔案


