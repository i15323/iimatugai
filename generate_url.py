fname = input("File Name: ")
y = input("Year: ")
start_m = int(input("Start of Month: "))
end_m = int(input("End of Month: "))

# 生成
wfs = open(fname, "a", encoding="UTF-8")

for i in range(start_m, end_m + 1):
    for j in range(1, 32):
        wfs.write("http://www.1101.com/iimatugai/archive_more" + str(9).zfill(2) + str(i).zfill(2) + str(j).zfill(2) + ".html")
        wfs.write("\n")
