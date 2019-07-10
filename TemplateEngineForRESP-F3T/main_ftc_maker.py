# -*- coding: utf-8 -*-


from jinja2 import Environment, FileSystemLoader
from Modeler.model import ModelManager


def generate_analysis_file(length_X:float,length_Y:float,length_Z:float,span_X:int,span_Y:int,span_Z:int):
  # モデルの生成（サンプル）
  Manager = ModelManager(length_X,length_Y,length_Z,span_X,span_Y,span_Z)
  nodes = Manager.get_nodes_generator()
  columns = Manager.get_columns_generator()
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
  length_X = 3000 #mm
  length_Y = 3000 #mm
  length_Z = 20000 #mm

  div_X = 4
  div_Y = 3
  div_Z = 5

  generate_analysis_file(length_X,length_Y,length_Z,div_X,div_Y,div_Z)
  