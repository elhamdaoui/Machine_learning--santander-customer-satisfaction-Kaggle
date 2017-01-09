sorted_classifiers=["None:0.0",]
with open("scoresClassifiers.txt","r") as fi:
    for line in fi:
        cls,score=line.split(":")
        score=score[:-1]
        for i in range(len(sorted_classifiers)):
            if float(score)>= float(sorted_classifiers[i].split(":")[1]):
                sorted_classifiers.insert(i,line[:-1])
                #print sorted_classifiers
                break
print "Fin, stock..."
with open("sortedClassifiers.txt","w") as fo:
    fo.writelines("\n".join(sorted_classifiers[:-1]))
print "Fin"
