f = open("chip.csv", "w")
for x in range(1, 351):
    line=str(x)+"\t6-575,140-13237-0-"+f"{x:03}"+"\n"
    f.write(line)
f.close()
