#standarized the files
i=2
with open("GBC2.amh","r") as fi:
    with open("GBC.amh","a") as fo:
        for line in fi:
            lines=[line,]
            fo.writelines(lines)
#Done
