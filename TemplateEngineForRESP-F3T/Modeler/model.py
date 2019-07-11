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
    for x in np.linspace(0,self.length_X,self.div_X):
      yield x
  
  @property
  def Y_coordinates(self):
    for y in np.linspace(0,self.length_Y,self.div_Y):
      yield y
  
  @property
  def Z_coordinates(self):
    for XY in self.XY_coordinates:
      yield 0.0
      yield self.roof_function(XY[0],XY[1])

  @property
  def XY_coordinates(self):
    return ((X,Y) for X in self.X_coordinates for Y in self.Y_coordinates)
  
  def set_nodes_dict(self):
    self.nodes_dict = { (XY[0],XY[1],0):Node("Node_%i_Z%i"%(i,self.get_story_name(Z)),XY[0],XY[1],0) for i,XY in enumerate(self.XY_coordinates) for Z in self.Z_coordinates}
  
  def get_story_name(self,Z:float):
    if Z == 0.0:
      return 0
    else:
      return 1

  def get_nodes_generator(self):
      nodes_generator = (node for node in self.nodes_dict.values())
      return nodes_generator

  def get_columns_generator(self):
    for XY in self.XY_coordinates:
      for Z,Z_next in self.extract_pairs_self_and_next(self.Z_coordinates):
        nodeI = self.search_node_from_coordinate(XY[0],XY[1],Z)
        nodeJ = self.search_node_from_coordinate(XY[0],XY[1],Z_next)
        yield Beam("C_%s_%s"%(nodeI.name,nodeJ.name),nodeI,nodeJ)
  
  def get_girders_generator(self):
    for Z in self.Z_coordinates:
      # X方向
      for X,X_next in self.extract_pairs_self_and_next(self.X_coordinates):
        for Y,Y_next in self.extract_pairs_self_and_next(self.Y_coordinates):
          nodeI_X = self.search_node_from_coordinate(X,Y,Z)
          nodeJ_X = self.search_node_from_coordinate(X_next,Y,Z)
          yield Beam("GX_%s_%s"%(nodeI_X.name,nodeJ_X.name),nodeI_X,nodeJ_X)
        
        nodeI_X = self.search_node_from_coordinate(X,Y_next,Z)
        nodeJ_X = self.search_node_from_coordinate(X_next,Y_next,Z)
        yield Beam("GX_%s_%s"%(nodeI_X.name,nodeJ_X.name),nodeI_X,nodeJ_X)
      
      # Y方向
      for Y,Y_next in self.extract_pairs_self_and_next(self.Y_coordinates):
        for X,X_next in self.extract_pairs_self_and_next(self.X_coordinates):
          nodeI_Y = self.search_node_from_coordinate(X,Y,Z)
          nodeJ_Y = self.search_node_from_coordinate(X,Y_next,Z)
          yield Beam("GY_%s_%s"%(nodeI_Y.name,nodeJ_Y.name),nodeI_Y,nodeJ_Y)
        
        nodeI_Y = self.search_node_from_coordinate(X_next,Y,Z)
        nodeJ_Y = self.search_node_from_coordinate(X_next,Y_next,Z)
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


