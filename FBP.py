import sys
import os
import tqdm
import math
import numpy as np
from util import IOutil


def FBPrec(inpath): #入力：サイノグラム(csv) 検出器数 x 投影数

    tmp = inpath + "/*.csv"
    infile = IOutil.ChooseFiles(tmp)
    os.makedirs("./output", exist_ok=True)

    inputcsv = np.loadtxt(infile, delimiter=',')
    height = inputcsv.shape[0]
    width = inputcsv.shape[1]

    fourier1d = np.empty((height, width), dtype='complex')
    filtered = np.empty((height, width), dtype='complex')
    filter = np.empty(int(width / 2))

    output = np.zeros((width, width))

    testcount = 10
    testoutput = np.zeros((testcount,width,width))

    filtertype = 0
    sharp = 5
    filtername = ["NO FILTER","RAM-LAK","SHEPP-LOGAN","BUTTERWORTH","PARZEN","HANN","HAMMING"]

    print("choose filter type:")
    print(" 0 No Filter (Default)")
    print(" 1 Ram-Lak")
    print(" 2 Shepp-Logan")
    print(" 3 Butterworth")
    print(" x4 Parzen")
    print(" x5 Hann")
    print(" x6 Hamming")
    tmp = input()

    if int(tmp) >= 1 and int(tmp) <= 3:
        filtertype = int(tmp)

    for i in range(len(filter)):
        if filtertype == 0:
            filter[i] = 1
        elif filtertype == 1:
            filter[i] = i / len(filter)
        elif filtertype == 2:
            filter[i] = (i / len(filter)) * np.sinc(0.5 * i / len(filter))
        elif filtertype == 3:
            filter[i] = (i / len(filter)) * (1 / (np.sqrt(1 + (i / len(filter))**(2 * sharp))))

    for i in range(height):
        fourier1d[i] = np.fft.fft(inputcsv[i]) #入力要素数Nに対しN/2(ナイキスト周波数)までが正の周波数，(N/2)+1から負の周波数となる
        fourier1d[i] = fourier1d[i] / (width / 2)
        fourier1d[i][0] /= 2

        # # for debug
        # plt.plot(inputcsv[i])
        # plt.xlim([0,width])
        # plt.show()

        for j in range(width):
            if j >= width / 2:
            #if (j >= width / 4 and j < width / 2) or (j >= width / 2 and j < width * 3 / 4):
                fourier1d[i][j] = 0
            else:
                fourier1d[i][j] *= filter[j]

        filtered[i] = np.fft.ifft(fourier1d[i])
        filtered[i] = np.real(filtered[i] * width)

        # # for debug
        # plt.plot(fourier1d[i])
        # plt.xlim([0,width])
        # plt.show()
        #
        # plt.plot(filtered[i])
        # plt.xlim([0,width])
        # plt.show()

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
