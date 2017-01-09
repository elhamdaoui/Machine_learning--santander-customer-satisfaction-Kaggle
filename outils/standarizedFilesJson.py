


paths=['BAGC','DTC','LR','ETC','GBC','KNN','RFC']

#standarized the files
for path in paths:
    i=2
    with open(path+".amh","r") as fi:
        with open(path+"2.amh","w") as fo:
            lines=["{","\""+path+"_1\":"]
            for line in fi:
                if "}{" in line:
                    lines.append("},")
                    fo.writelines(lines)
                    lines=["\""+path+"_"+str(i)+"\":{"]
                    i+=1
                else:
                    lines.append(line)
            lines.append("}")
            fo.writelines(lines)
    #Done
