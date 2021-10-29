ChipCount = input("Indtast antal chips: ")
NumberStart = input("Indtast første rytternummer: ")
ChipStart = input("Indtast første chip: ")
FileName = "B2BB-" + str(ChipCount) + "-" + str(NumberStart) + "-" + str(ChipStart) + ".csv"

f = open(FileName, "w")
for x in range(0, int(ChipCount)):
    # Bruges når Timing & Scoring sender hele batch koden med rygnr med 3 cifre.
    # Batch = 6-575,140-13237-0-
    # line=str(x)+"\t" + Batch +f"{x:03}"+"\n"

    #Bruges når Timing & Scoring sender rygnr som data med 7 cifre.
    line=str(x+int(NumberStart))+"\t"+f"{x+int(ChipStart):07}"+"\n"
    f.write(line)
f.close()
print("Tabel genereret: " + FileName)
