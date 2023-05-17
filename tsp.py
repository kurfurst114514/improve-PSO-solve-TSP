import copy
import random
import math
import operator as op

fitlist=[]

class Map:
    def __init__(self,length_x,length_y) -> None:
        self.List_point=[]
        self.length_x=length_x
        self.length_y=length_y

    def add_point(self,x,y):
        self.List_point.append([x,y])

class Indiv:
    def __init__(self) -> None:
        self.path=[]
        self.pbest=[]
        self.pbest_len=10000000000
        self.v=Velocity()

class Velocity():
    def __init__(self) -> None:
        self.velocity=[]

    @staticmethod
    def vv_add(a,b):
        result=Velocity()
        if(len(a.velocity)!=0):
            for v in a.velocity:
                ver=[v[1],v[0]]
                for i in range(len(result.velocity)):
                    if(not op.eq(v,result.velocity[i]) and not op.eq(ver,result.velocity[i])):
                        result.velocity.append(v)
        if(len(b.velocity)!=0):
            for v in b.velocity:
                ver=[v[1],v[0]]
                for i in range(len(result.velocity)):
                    if(not op.eq(v,result.velocity[i]) and not op.eq(ver,result.velocity[i])):
                        result.velocity.append(v)
        result.velocity+=b.velocity
        return result

    @staticmethod
    def vp_add(a,div):
        for v in a.velocity:
            index_1=0
            index_2=0
            for p in range(len(div.path)):
                if(op.eq(div.path[p],v[0])):
                    index_1=p
                if(op.eq(div.path[p],v[1])):
                    index_2=p
            tmp=copy.deepcopy(div.path[index_1])
            div.path[index_1]=copy.deepcopy(div.path[index_2])
            div.path[index_2]=tmp
        return div

    @staticmethod
    def pp_sub(a,b):
        result=Velocity()
        for i in range(len(a)):
            if(not op.eq(a[i],b[i])):
                vi=[a[i],b[i]]
                vervi=[vi[1],vi[0]]
                flag=True
                for i in range(len(result.velocity)):
                    if(op.eq(result.velocity[i],vi) or op.eq(result.velocity[i],vervi)):
                        flag=False
                        break
                if(flag):
                    result.velocity.append(vi)
        return result

    @staticmethod
    def cv_mult(c,a):
        result=Velocity()
        for i in range(int(c*len(a.velocity))):
            result.velocity.append(a.velocity[i])
        return result

        

    
