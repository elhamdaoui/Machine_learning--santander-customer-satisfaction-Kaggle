
def count_classifiers(nm):
        with open(nm+".amh") as f:
                i=0
                mn,mx=2,-1
                for l in f:
                        if "score" in l:
                                i+=1
                                sc=float(l.split(":")[1].split(",")[0])
                                if sc>mx:mx=sc
                                if sc<mn:mn=sc
                return nm+" : "+str(i)+" classifiers with score between "+str(mn)+" and "+str(mx)

paths=['BAGC','DTC','LR','ETC','GBC','KNN','RFC']
with open("infos_classifiers.txt","w") as f:
        lns=[]
        for cls in paths:
                lns.append(count_classifiers(cls))
        f.writelines(lns)
