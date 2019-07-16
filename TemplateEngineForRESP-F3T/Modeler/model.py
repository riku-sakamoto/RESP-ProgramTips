# -*- coding: utf-8 -*-

from collections import namedtuple
import itertools
import numpy as np

# 節点クラス
class Node(object):
  def __init__(self,name:str,X:float,Y:float,Z:float):
    self.name = name
    self.Coordinate = namedtuple("Coordinate",("X","Y","Z"))
    self.Coordinate.X = X
    self.Coordinate.Y = Y
    self.Coordinate.Z = Z

# Beamクラス
class Beam(object):
  def __init__(self,name:str,NodeI:Node,NodeJ:Node):
    self.name = name
    self.NodeI = NodeI
    self.NodeJ = NodeJ

# 全体モデル管理クラス
# 一層屋根付きモデル
class ModelManager(object):
  def __init__(self,roof_function,length_X:float,length_Y:float,div_X:int,div_Y:int):
    self.roof_function = roof_function
    self.length_X = length_X
    self.length_Y = length_Y

    self.div_X = div_X
    self.div_Y = div_Y

    self.nodes_dict = {}
    self.set_nodes_dict()

  @property
  def X_coordinates(self):
    for x in np.linspace(-self.length_X,self.length_X,self.div_X):
      yield x
  
  @property
  def Y_coordinates(self):
    for y in np.linspace(-self.length_Y,self.length_Y,self.div_Y):
      yield y

  @property
  def XY_coordinates(self):
    return ((X,Y) for X in self.X_coordinates for Y in self.Y_coordinates)
    
  def set_nodes_dict(self):
    # 基礎
    self.nodes_dict = { (XY[0],XY[1],0):Node(self.get_node_name(j,0),XY[0],XY[1],0) for j,XY in enumerate(self.XY_coordinates)}

    # 屋根面
    self.nodes_dict.update({(XY[0],XY[1],self.roof_function(XY[0],XY[1])):Node(self.get_node_name(j,self.roof_function(XY[0],XY[1])),XY[0],XY[1],self.roof_function(XY[0],XY[1]))\
       for j,XY in enumerate(self.XY_coordinates)})
  
  def get_node_name(self,j:int,Z:float):
    return "Node_%i_Z%i"%(j,self.get_story_name(Z))

  def get_story_name(self,Z:float):
    if Z == 0.0:
      return 0
    else:
      return 1

  def get_nodes_generator(self):
      nodes_generator = (node for node in self.nodes_dict.values())
      return nodes_generator

  def get_columns_generator(self,interval_X=1,interval_Y=1):
    for X in list(self.X_coordinates)[::interval_X]:
      for Y in list(self.Y_coordinates)[::interval_Y]:
        nodeI = self.search_node_from_coordinate(X,Y,0)
        nodeJ = self.search_node_from_coordinate(X,Y,self.roof_function(X,Y))
        yield Beam("C_%s_%s"%(nodeI.name,nodeJ.name),nodeI,nodeJ)
  
  def get_girders_generator(self):
    # X方向
    for X,X_next in self.extract_pairs_self_and_next(self.X_coordinates):
      for Y,Y_next in self.extract_pairs_self_and_next(self.Y_coordinates):
        nodeI_X = self.search_node_from_coordinate(X,Y,self.roof_function(X,Y))
        nodeJ_X = self.search_node_from_coordinate(X_next,Y,self.roof_function(X_next,Y))
        yield Beam("GX_%s_%s"%(nodeI_X.name,nodeJ_X.name),nodeI_X,nodeJ_X)
      
      nodeI_X = self.search_node_from_coordinate(X,Y_next,self.roof_function(X,Y_next))
      nodeJ_X = self.search_node_from_coordinate(X_next,Y_next,self.roof_function(X_next,Y_next))
      yield Beam("GX_%s_%s"%(nodeI_X.name,nodeJ_X.name),nodeI_X,nodeJ_X)
    
    # Y方向
    for Y,Y_next in self.extract_pairs_self_and_next(self.Y_coordinates):
      for X,X_next in self.extract_pairs_self_and_next(self.X_coordinates):
        nodeI_Y = self.search_node_from_coordinate(X,Y,self.roof_function(X,Y))
        nodeJ_Y = self.search_node_from_coordinate(X,Y_next,self.roof_function(X,Y_next))
        yield Beam("GY_%s_%s"%(nodeI_Y.name,nodeJ_Y.name),nodeI_Y,nodeJ_Y)
      
      nodeI_Y = self.search_node_from_coordinate(X_next,Y,self.roof_function(X_next,Y))
      nodeJ_Y = self.search_node_from_coordinate(X_next,Y_next,self.roof_function(X_next,Y_next))
      yield Beam("GY_%s_%s"%(nodeI_Y.name,nodeJ_Y.name),nodeI_Y,nodeJ_Y)

  def search_node_from_coordinate(self,X:float,Y:float,Z:float):
    node = self.nodes_dict[(X,Y,Z)]
    return node
  
  def extract_pairs_self_and_next(self,iterator):
    # イテレータのコピー
    now_iter,next_iter = itertools.tee(iterator)
    # 先に進めて置く
    next(next_iter)
    for value,value_next in zip(now_iter,next_iter):
      yield (value,value_next)


