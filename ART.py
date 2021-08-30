import sys
import os
import tqdm
import math
import numpy as np
from util import IOutil


def ARTrec(): #入力：サイノグラム(csv)

    tmp = inpath + "/*.csv"
    infile = IOutil.ChooseFiles(tmp)
    os.makedirs("./output", exist_ok=True)

    inputcsv = np.loadtxt(infile, delimiter=',')
    height = inputcsv.shape[0]
    width = inputcsv.shape[1]

    sysmat = np.empty((height * width, width * width)) #投影数 x 画素数のシステム行列
    output = np.zeros((width, width))


    center = width / 2

    for y in tqdm.tqdm(range(width)):
        for x in tqdm.tqdm(range(width), leave=False):
            theta = 0
            origx = x
            origy = y
            relx = origx - center + 0.5
            rely = width - origy - 1 - center + 0.5
            for angle in range(height):
            #for angle in range(testcount):
                if theta >= math.pi / 4: #投影角が45度を超えたら画像を90度右回転させ投影角を-45度に
                    theta -= math.pi / 2
                    tmpx = origx
                    origx = width - origy - 1
                    origy = tmpx
                    relx = origx - center + 0.5
                    rely = width - origy - 1 - center + 0.5
                for p in range(width):
                    offsetD = (width - p - 1 - center + 0.5) / math.cos(theta) #offset of the detector
                    b = offsetD - rely + relx * math.tan(theta)
                    if b <= 0.5 * (1 - math.tan(theta)) and b >= - 0.5 * (1 - math.tan(theta)):
                        #output[y][x] += int(inputcsv[angle][p])
                        output[y][x] += int(np.real(filtered[angle][p]))
                        sysmat[height * angle + p][width * y + x]
                        #testoutput[angle][y][x] += int(inputcsv[angle][p]) #for debug
                    elif b <= 0.5 * (1 + math.tan(theta)) and b >= -0.5 * (1 + math.tan(theta)):
                        #output[y][x] += int(inputcsv[angle][p]) * (0.5 * (1 / math.tan(theta) + 1) - abs(b) / math.tan(theta))
                        output[y][x] += int(np.real(filtered[angle][p])) * (0.5 * (1 / math.tan(theta) + 1) - abs(b) / math.tan(theta))
                        #testoutput[angle][y][x] += int(inputcsv[angle][p]) * (0.5 * (1 / math.tan(theta) + 1) - abs(b) / math.tan(theta)) #for debug
                theta += math.radians(360 / height)

    # for y in range(width):
    #     for x in range(width):
    #         output[y][x] /= height


    outfile = "./output/reconstructed.csv"
    with open(outfile, 'w') as of:
        np.savetxt(outfile, output, fmt='%d', delimiter=',')

    # for debug
    # for i in range(testcount):
    #     testoutfile = "./output/reconstructed(test)" + str(i) + ".csv"
    #     with open(testoutfile, 'w') as of:
    #         np.savetxt(testoutfile, testoutput[i], fmt='%d', delimiter=',')
