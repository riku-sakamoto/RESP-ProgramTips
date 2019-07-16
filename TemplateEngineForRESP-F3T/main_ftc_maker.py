# -*- coding: utf-8 -*-


from jinja2 import Environment, FileSystemLoader
from Modeler.model import ModelManager
from RoofFunctions import trigonometric_function as trifunc


def generate_analysis_file(length_X:float,length_Y:float,span_X:int,span_Y:int):
  # モデルの生成（サンプル）
  Manager = ModelManager(trifunc.sin_sin,length_X,length_Y,span_X,span_Y)
  nodes = Manager.get_nodes_generator()
  columns = Manager.get_columns_generator(2,2)
  girders = Manager.get_girders_generator()

  # テンプレートファイルが配置されているディレクトリの指定
  env = Environment(loader=FileSystemLoader(("./Template"),encoding="utf-8"))

  # テンプレートファイル名の指定
  template = env.get_template("template.ftc")
  
  # テンプレートファイルを基に書き込む内容を作成
  # 辞書のキーはテンプレートファイル内の変数名
  out = template.render({"Nodes":nodes,"Columns":columns,"Girders":girders})

  # ファイルを新規作成し、書き込み
  with open("./FtcFiles/new_file.ftc","w",encoding="utf-8") as fw:
    fw.write(out)
  

if __name__ == "__main__":
  #長さX,長さY,長さZ,スパン数X,スパン数Y,スパン数Z
  length_X = 2000 #mm
  length_Y = 2000 #mm

  div_X = 10
  div_Y = 12

  generate_analysis_file(length_X,length_Y,div_X,div_Y)
  