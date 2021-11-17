#!/usr/bin/env python
ChipCount = input("Indtast antal chips: ")
NumberStart = input("Indtast første rytter-chip: ")
ChipStart = input("Indtast første BB-chip: ")
FileName = "B2BB-" + str(ChipCount) + "-" + str(NumberStart) + "-" + str(ChipStart) + ".csv"

f = open(FileName, "w")
for x in range(0, int(ChipCount)):
    # Bruges når Timing & Scoring sender hele batch koden med rygnr med 3 cifre.
    # Batch = 6-575,140-13237-0-
    # line=str(x)+"\t" + Batch +f"{x:03}"+"\n"


    # XX-XXXXX
    line=str(x+int(NumberStart))+"\t"+f"{x+int(ChipStart):07}"[0:2] + "-" + f"{x+int(ChipStart):07}"[2:7] + "\n"
    f.write(line)
f.close()
print("Tabel genereret: " + FileName)
