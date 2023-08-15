import os
from clr_loader import get_coreclr
from pythonnet import set_runtime
import clr
import pandas as pd
import time
import sys
import decimal

filedir = os.path.dirname(os.path.abspath(__file__))
dllFolder = os.path.join(filedir, 'netcore')
rt = get_coreclr(runtime_config=os.path.join(dllFolder, "ProcessHost.runtimeconfig.json"))
set_runtime(rt)
sys.path.append(dllFolder)
# info = pythonnet.get_runtime_info()

clr.AddReference('System.Data.Common')
clr.AddReference('System.Data')
clr.AddReference("System.Collections")

import System
from System import Data, Decimal, DateTime
from System.Data import DataTable
from System.Data import DataColumn


# from System.IO import MemoryStream

def TableToDataFrame(dt):
    ''' Convert DataTable type to DataFrame type '''

    colTempCount = 0
    dic = {}
    while (colTempCount < dt.Columns.Count):
        li = []
        rowTempCount = 0
        column = dt.Columns[colTempCount]
        colName = column.ColumnName
        typeName = column.DataType.Name
        while (rowTempCount < dt.Rows.Count):
            result = dt.Rows[rowTempCount][colTempCount]
            try:
                if typeName == 'Decimal' and System.DBNull.Value != result:
                    li.append(Decimal.ToDouble(result))
                elif typeName != 'DateTime' and result == System.DBNull.Value:
                    li.append(None)
                else:
                    li.append(result)
            except Exception as err:
                print(err)

            rowTempCount = rowTempCount + 1

        colTempCount = colTempCount + 1
        dic.setdefault(colName, li)

    df = pd.DataFrame(dic)
    
    return (df)

def DataFrameToDic(df):
    ''' Convert DataFrame data type to dictionary type '''
    dic = df.to_dict(' list ')
    return dic

def TableToDataFrame2(dt):
    # 컬럼 이름 추출
    columns = [column.ColumnName for column in dt.Columns]
    decimal_cols = [column.ColumnName for column in dt.Columns if column.DataType.Name == "Decimal"]

    data = []
    for row in dt.Rows:
        data.append([row[column] for column in columns])

    df = pd.DataFrame(data, columns=columns)
    for dcol in decimal_cols:
        df[dcol] = pd.to_numeric(df[dcol], errors='ignore')
        print(df[dcol])

    return df

def TableToDataFrame_Test(dt):
    import System.Data
    # linq 사용하기 위해서는 다음 추가필요
    clr.AddReference("System.Core")

    sys.path.append(r'<path>')

    # 컬럼 이름 추출
    columns = [column.ColumnName for column in dt.Columns]

    # rows = dt.AsEumerable()
    rows = System.Data.DataTableExtensions.AsEnumerable(dt)
    df = pd.DataFrame.from_records(rows, columns=columns)
    return df


def DataFrameToTable(df, name):
    """ Convert DataFrame data type into DataTable data type """
    dtable = DataTable(name)

    # Add columns to the DataTable based on the columns in the pandas DataFrame
    for column_name in df.columns:
        column = DataColumn(column_name)
        if df.dtypes[column_name] == 'int64':
            column.DataType = System.Type.GetType('System.Int32')
        elif df.dtypes[column_name] == 'float64':
            column.DataType = System.Type.GetType('System.Single')
        elif column.DataType == 'bool':
            column.DataType = System.Type.GetType('System.Boolean')
        dtable.Columns.Add(column)

    # Add rows to the DataTable based on the rows in the pandas DataFrame
    for index, row in df.iterrows():
        data_row = dtable.NewRow()
        for column_name in df.columns:
            data_row[column_name] = row[column_name]
        dtable.Rows.Add(data_row)

    return dtable


def DictToArg(cs_dict):
    """
    Convert a C# arguments to a Python dictionary.

    :param cs_dict: C# arguments object
    :return: Python dictionary
    """
    pyth_dict = {}

    # Extract the key and value from the KeyValuePair object
    key = cs_dict.Key
    value = cs_dict.Value

    if isinstance(value, System.Decimal):
        value = float(str(cs_dict.Value))

    elif isinstance(value, System.DateTime):
        value = str(cs_dict.Value)

    else:
        value = cs_dict.Value

    # Add the key-value pair to the Python dictionary
    pyth_dict[key] = value

    return pyth_dict


def ExcRunToDataFrame(execution):
    """
    Convert List of Execution Run DataTypes to Pandas DataFrame
    """

    data = {}

    for run in execution.Runs:
        embedded_data = {
            "Run Index": run.Index,
            "Run Name": run.Name,
            "Start Time": run.StartTime,
            "End Time": run.EndTime,
        }
        elapsed_time = str(run.EndTime - run.StartTime).split('.')[0]
        embedded_data["Elapsed Time"] = elapsed_time

        for factor in run.Factors:
            value = factor.Value

            if isinstance(factor.Key, System.Double):
                value = round(float(value), 3)
            elif isinstance(factor.Key, System.Decimal):
                value = round(decimal.Decimal(value), 3)
            elif isinstance(factor.Key, int):
                value = int(value)

            if factor.Key not in embedded_data:
                embedded_data[factor.Key] = value

        for kpi in run.KPIs:
            kpi_value = round(kpi.Value, 3)

            if kpi.Key not in embedded_data:
                embedded_data[kpi.Key] = kpi_value

        embedded_data["Run State"] = run.State

        if run.IsSuccess:
            embedded_data["Engine Status"] = "Success"
        elif run.ErrorLog:
            embedded_data["Engine Status"] = "Fail"
            embedded_data["Error"] = str(run.ErroLog)
        else:
            embedded_data["Engine Status"] = '-'
        
        data[run.Index] = embedded_data

    df = pd.DataFrame.from_dict(data, orient='index')
    return df