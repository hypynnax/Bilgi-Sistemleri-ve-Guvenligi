matris = [[0] * 20 for _ in range(20)]

#Bu kısım ortasında büyük bir şekilde baş harfi yazıyor
#for i in range(4,17):
#    matris[i][2] = 1
#    matris[i][3] = 1
#    matris[i][16] = 1
#    matris[i][17] = 1
#
#for i in range(5,16):
#    matris[i][i-1] = 1
#    matris[i][i] = 1
#
#for x in matris:
#    for y in x:
#        print(y, end='    ')
#    print("\n")

#Bu kısım sol üste harfi küçük bir şekilde yazıyor
matris[0][0] = 1
matris[1][0] = 1
matris[2][0] = 1
matris[3][0] = 1
matris[1][1] = 1
matris[2][2] = 1
matris[0][3] = 1
matris[1][3] = 1
matris[2][3] = 1
matris[3][3] = 1

for x in matris:
    for y in x:
        print(y, end='    ')
    print("\n")