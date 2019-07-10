# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:04:51 2018

@author: sakamoto
"""

import pandas as pd
import csv

class FormatChanger(object):
    def __init__(self,str_fixed_format:str):
        num_1 = str_fixed_format.index("F")
        num_2 = str_fixed_format.index(".")
        
        self.number_of_items = int(str_fixed_format[:num_1])
        self.number_of_one_section = int(str_fixed_format[num_1+1:num_2])
        self.round_number = int(str_fixed_format[num_2+1:])
    
    def convert_to_formatted_value(self,str_value:str):
        # 固定書式に変換
        str_change_format="%"+str(self.number_of_one_section)+"."+str(self.round_number)+"f"
        str_value = str_change_format%float(str_value)
        return str_value
    
    def convert_to_formatted_values_text(self,str_value_lst:list):
        # 固定書式に変換した文字列群を出力
        text=""
        for i in range(len(str_value_lst)):
            # 変換された値を取得
            value = self.convert_to_formatted_value(str_value_lst[i])

            # 改行コードを入れるか
            # 三項演算子を用いています
            value += "\n" if int(i + 1) % self.number_of_items == 0 else ""
            
            # 文字列群に追加
            text+=value
        return text
    


if __name__=="__main__":
    
    # 固定書式の指定
    str_fixed_format="7F10.1"
    
    # 読み込みcsvファイル名
    csv_file_name = "data.csv"
    
    # 出力テキストファイル名
    text_file_name = "sample.dat"

    
    # csvの読み込み
    DataFrame= pd.read_csv(csv_file_name)
    acc_lst = list(DataFrame.iloc[:,1])
    
    FormatChanger = FormatChanger(str_fixed_format)
    acc_text=FormatChanger.convert_to_formatted_values_text(acc_lst[1:])
    
    with open(text_file_name,"w") as fw:
        writer = csv.writer(fw, lineterminator='\n') # 改行コード（\n）を指定しておく
        fw.write(acc_text)
    