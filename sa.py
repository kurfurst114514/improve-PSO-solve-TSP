from tsp import *
from pso import *

class SA:
    def __init__(self,div,map) -> None:
        self.div=div
        self.map=map

    def fit_func(self,indiv):
        result=0
        for i in range(len(indiv)-1):
            direction=math.sqrt(math.pow(indiv[i][0]-indiv[i+1][0],2)+math.pow(indiv[i][1]-indiv[i+1][1],2))
            result+=direction
        return result

    def shake_func(self):
        result=copy.deepcopy(self.div)
        index1=random.randint(1,len(self.div.path)-2)
        index2=random.randint(1,len(self.div.path)-2)
        # dtmp=random.random()
        # delta=1
        # if(dtmp<0.5):
        #     delta=1
        # elif(dtmp>=0.5 and dtmp<0.8):
        #     delta=random.randint(1,2)
        # else:
        #     delta=random.randint(3,10)
        # dist=random.random()
        # if(dist>0.5):
        #     index2=index1+delta
        # else:
        #     index2=index1-delta
        # if(index2<1):
        #     index2=1
        # elif(index2>=len(self.div.path)-1):
        #     index2=len(self.div.path)-2
        u=min(index1,index2)
        v=max(index1,index2)
        while(u<=v):
            tmp=copy.deepcopy(result.path[u])
            result.path[u]=copy.deepcopy(result.path[v])
            result.path[v]=tmp
            u+=1
            v-=1
        return result
    
    def if_authority(self,diva,divb,k,T):
        delE=self.fit_func(diva)-self.fit_func(divb)
        a=self.fit_func(diva)
        b=self.fit_func(divb)
        if(delE<0):
            return True
        else:
            metro=math.pow(math.e,-(delE/(k*T)))
            if(random.random()<metro):
                return True
            else:
                return False

    def run_sa(self,L,k,T0,Te):
        T=T0
        while(T>Te):
            for i in range(L):
                newdiv=self.shake_func()
                flag=self.if_authority(newdiv.path,self.div.path,k,T)
                if(flag):
                    self.div=newdiv
            T=k*T
        return self.div
        
        
class PSO_3:
    def __init__(self,map) -> None:
        self.map=map
        self.group=[]
        self.gbest=[]
        self.gbest_len=100000000

    def gene_init_group(self,num):
        for i in range(num):
            undolist=copy.deepcopy(self.map.List_point)
            indiv=Indiv()
            indiv.path.append(undolist[0])
            startp=undolist[0]
            undolist.remove(undolist[0])
            while(len(undolist)!=0):
                index=random.randint(0,len(undolist)-1)
                indiv.path.append(undolist[index])
                undolist.remove(undolist[index])
            indiv.path.append(startp)
            indiv.pbest=copy.deepcopy(indiv.path)
            indiv.pbest_len=self.fit_func(indiv.path)
            self.group.append(indiv)
    
    def fit_func(self,indiv):
        result=0
        for i in range(len(indiv)-1):
            direction=math.sqrt(math.pow(indiv[i][0]-indiv[i+1][0],2)+math.pow(indiv[i][1]-indiv[i+1][1],2))
            result+=direction
        return result

    def update_pbest(self):
        for indiv in self.group:
            fit=self.fit_func(indiv.path)
            if(fit<indiv.pbest_len):
                indiv.pbest=copy.deepcopy(indiv.path)
                indiv.pbest_len=fit

    def update_gbest(self):
        for indiv in self.group:
            if(indiv.pbest_len<self.gbest_len):
                self.gbest=copy.deepcopy(indiv.pbest)
                self.gbest_len=indiv.pbest_len


    def update_v(self,w,c1,c2,div):
        tmp1=Velocity.cv_mult(w,div.v)
        tmp2=Velocity.cv_mult(c1*random.random(),Velocity.pp_sub(div.pbest,div.path))
        tmp3=Velocity.cv_mult(c2*random.random(),Velocity.pp_sub(self.gbest,div.path))
        vnext=Velocity.vv_add(tmp1,Velocity.vv_add(tmp2,tmp3))
        div=Velocity.vp_add(vnext,div)
        div.v=vnext

    def crossline(self,linea,lineb):
        flag01=linea[0][0]-lineb[0][0]
        flag02=linea[1][0]-lineb[1][0]
        flag11=linea[0][1]-lineb[0][1]
        flag12=linea[1][1]-lineb[1][1]
        if((flag01*flag02)<=0 and (flag11*flag12)<=0):
            return True
        return False

    def delete_cross(self,div):
        for i in range(0,len(div.path)-3):
            for j in range(i+1,len(div.path)-1):
                flag=self.crossline([div.path[i],div.path[i+1]],[div.path[j],div.path[j+1]])
                if(flag):
                    for k in range(0,int((j-i)/2)):
                        tmp=copy.deepcopy(div.path[j-k])
                        div.path[j-k]=copy.deepcopy(div.path[i+k+1])
                        div.path[i+k+1]=tmp

    def pso_algo(self,w,c1,c2,N,times,L,k,T0,Te):
        self.gene_init_group(N)
        for d in self.group:
            self.delete_cross(d)
        self.update_gbest()
        fitlist.append(self.gbest_len)
        for i in range(times):
            for d in self.group:
                self.update_v(w,c1,c2,d)
            for d in self.group:
                self.delete_cross(d)
            # for d in self.group:
            #     sa=SA(d,self.map)
            #     sa.run_sa(L,k,T0,Te)
            #L+=1
            
            #k+=(0.98-0.2)/times
            self.update_pbest()
            self.update_gbest()
            gbestdib=Indiv()
            gbestdib.path=self.gbest
            sa=SA(gbestdib,self.map)
            tmppath=sa.run_sa(L,k,T0,Te).path
            if(self.fit_func(tmppath)<self.gbest_len):
                self.gbest_len=self.fit_func(self.gbest)
                self.gbest=tmppath
            T0=T0*k
            print(self.gbest_len)
            fitlist.append(self.gbest_len)
            w-=(w-0.4*w)/times
            
        return self.gbest  