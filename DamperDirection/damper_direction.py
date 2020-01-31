# -*- coding:utf-8 -*-

import numpy as np
import pylab as plt


class Damper(object):
  '''ダンパークラス'''
  def __init__(self,angle_radian:float,coefficient:float,alpha:float):
    self.rad = angle_radian
    self.coeff = coefficient
    self.alpha = alpha

  @property
  def direction_vector(self):
    return np.array([np.cos(self.rad),np.sin(self.rad)])
  
  def get_damping_force_value(self,velocity):
    '''減衰力を返す'''
    return self.coeff*np.abs(velocity)**self.alpha
  
  # 
  def plot_force_vectors_for_velocities(self,velocity_vector):
    '''減衰力ベクトルを返す'''
    velocity = np.dot(self.direction_vector,velocity_vector)
    force_value = self.get_damping_force_value(velocity)
    force_sign = -1.0*np.sign(velocity)
    return force_sign*force_value*self.direction_vector

class LeanedPairDampers(object):
  '''組み合わせダンパークラス'''
  def __init__(self,Damper1:Damper,Damper2:Damper):
    self.Damper1 = Damper1
    self.Damper2 = Damper2
  
  def compute_force_vector(self,velocity_vector):
    '''合力ベクトルを計算する'''
    force_vector_1 = self.Damper1.plot_force_vectors_for_velocities(velocity_vector)
    force_vector_2 = self.Damper2.plot_force_vectors_for_velocities(velocity_vector)
    return force_vector_1 + force_vector_2


class VectorUtils:
  '''ベクトル計算用のクラス'''
  @staticmethod
  def get_angle_degree(vector):
    theta = np.arctan2(vector[1],vector[0])
    return theta*180.0/np.pi

  @staticmethod
  def get_angle_rad(vector):
    theta = np.arctan2(vector[1],vector[0])
    return theta


class DamperEffectivenessPlot(object):
  '''描画用のクラス'''
  def __init__(self,dampPair:LeanedPairDampers,velocity_value,row,col,pos):
    self.LeanedPairDampers = dampPair
    self.velocity_value = velocity_value
    self.row = row
    self.col = col
    self.pos = pos
  
  def force_vector_generator(self,rad_range):
    '''合力ベクトルを生成するジェネレータ'''
    for rad in rad_range:
      velocity_vector = self.velocity_value * np.array([np.cos(rad),np.sin(rad)])
      force_vector = self.LeanedPairDampers.compute_force_vector(velocity_vector)
      yield force_vector
  
  def force_vector_comp_parallel_to_velocity_generator(self,rad_range):
    '''速度ベクトルに平行な合力ベクトルの大きさを生成するジェネレータ'''
    for rad in rad_range:
      velocity_vector = self.velocity_value * np.array([np.cos(rad),np.sin(rad)])
      force_vector = self.LeanedPairDampers.compute_force_vector(velocity_vector)
      yield abs(np.dot(force_vector,velocity_vector))/np.linalg.norm(velocity_vector)

  def plot_force_value(self,fig):
    '''合力ベクトルの大きさを図化する関数'''
    ax = fig.add_subplot(self.row,self.col,self.pos,polar=True)
    rad_range = np.arange(0,2*np.pi,0.01)
    force_lst = [np.linalg.norm(force_vector) for force_vector in self.force_vector_generator(rad_range)]
    plt.polar(rad_range,force_lst)

    y_max = np.ceil(max(force_lst)) + 100
    ax.set_ylim([0,y_max])
  
  def plot_force_vector_comp_parallel_to_velocity(self,fig):
    '''速度ベクトルに平行な合力ベクトルの大きさを図化する'''
    ax = fig.add_subplot(self.row,self.col,self.pos,polar=True)
    rad_range = np.arange(0,2*np.pi,0.01) 
    force_lst = list(self.force_vector_comp_parallel_to_velocity_generator(rad_range))
    plt.polar(rad_range,force_lst)
    y_max = np.ceil(max(force_lst)) + 100
    ax.set_ylim([0,y_max])
  
  def plot_force_vector_angle(self,fig):
    '''合力ベクトルの角度を図化する'''
    ax = fig.subplot(self.row,self.col,self.pos,polar=True)
    degree_range = np.arange(0,180,1)[1:]
    value_lst = []
    for deg in degree_range:
      rad = deg*np.pi/180
      velocity_vector = np.array([np.cos(rad),np.sin(rad)])
      force_vector = self.LeanedPairDampers.compute_force_vector(velocity_vector)
      theta = VectorUtils.get_angle_rad(force_vector)
      value_lst.append(theta*180/np.pi)
    
    plt.plot(degree_range,value_lst)
    plt.plot(degree_range,[deg-180 for deg in degree_range])
    ax.set_xlim([0,180])


  def plot_force_vectors_for_velocities(self,fig):
    '''合力ベクトルを速度ベクトルの角度を5度ずつ変化させて図化する'''
    ax = fig.add_subplot(self.row,self.col,self.pos)
    # 必ず45度が入るようにした
    rad_range = [theta*np.pi/180.0 for theta in np.arange(0,360,5)]
    force_vector_lst = list(self.force_vector_generator(rad_range))
    for force_vector in force_vector_lst:
      plt.quiver(0,0,force_vector[0],force_vector[1],angles='xy',scale_units='xy',scale=1,width=0.005)

    max_force_ceil = np.ceil(max([np.linalg.norm(vec) for vec in force_vector_lst]))+100
    ax.set_xlim([-max_force_ceil,max_force_ceil])
    ax.set_ylim([-max_force_ceil,max_force_ceil])
  
  def plot_force_vector(self,velocity_vector):
    '''速度ベクトルから合力ベクトルを計算する'''
    ax = plt.subplot(self.row,self.col,self.pos)
    force_vector = self.LeanedPairDampers.compute_force_vector(velocity_vector)
    plt.quiver(0,0,force_vector[0],force_vector[1],angles='xy',scale_units='xy',scale=1,width=0.01,color="r",label="Damping Force")
    plt.quiver(0,0,velocity_vector[0],velocity_vector[1],angles='xy',scale_units='xy',scale=1,width=0.01,label="Velocity")

    max_value = max([np.linalg.norm(velocity_vector),np.linalg.norm(force_vector)])
    ax.set_xlim([-max_value,max_value])
    ax.set_ylim([-max_value,max_value])
    plt.legend()


if __name__ == "__main__":
  angle = 45.0*np.pi/180.0

  alpha = 0.5
  coeff = 20.0 #mm系
  # alpha = 2.0
  # coeff = 0.001 #mm系
  Damp1 = Damper(angle,coeff,alpha)
  Damp2 = Damper(-angle,coeff,alpha)
  PairViscousDamp = LeanedPairDampers(Damp1,Damp2)
  ViscousPlotter = DamperEffectivenessPlot(PairViscousDamp,650,1,2,2)

  alpha = 1.0
  coeff = 0.8 #mm系
  Damp1 = Damper(angle,coeff,alpha)
  Damp2 = Damper(-angle,coeff,alpha)
  PairOilDamp = LeanedPairDampers(Damp1,Damp2)
  OilPlotter = DamperEffectivenessPlot(PairOilDamp,650,1,2,1)

  fig = plt.figure(figsize=(10,5))
  OilPlotter.plot_force_value(fig)
  ViscousPlotter.plot_force_value(fig)
  plt.show()

  fig2 = plt.figure(figsize=(10,5))
  OilPlotter.plot_force_vectors_for_velocities(fig2)
  ViscousPlotter.plot_force_vectors_for_velocities(fig2)
  plt.show()

  fig3 = plt.figure(figsize=(10,5))
  velocity_vector = 650*np.array([np.cos(30.0*np.pi/180.0),np.sin(30.0*np.pi/180.0)])
  OilPlotter.plot_force_vector(velocity_vector)
  ViscousPlotter.plot_force_vector(velocity_vector)
  plt.show()
