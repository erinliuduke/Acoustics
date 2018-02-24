from scipy.signal import cheby2, lfilter
import csv
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import sys

fs = 130000

time = 4

#running average get time section, fft get phase comparison, multichannels

def cheby2_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = cheby2(order, 5, [low, high], btype='bandpass')
    return b, a

def cheby2_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = cheby2_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def moving_average(a, n = fs*0.004*3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == "__main__":
    data = []
    freq = int(sys.argv[1])
    process = subprocess.Popen(["/home/robot/Desktop/mcc-libusb/sampling", time, fs], stdout = subprocess.PIPE)
    stddata, stderror = process.communicate()

    datas = stddata.split("\n")

    for d in datas:
        try:
            p = float(d)
            data.append(p)
        except:
            continue

    # with open("data.csv", 'rb') as filec:
    #     reader = csv.reader(filec)
    #     for row in reader:
    #         try:
    #             p = float(row[0])
	# 	#print p
    #             data.append(p)
    #         except:
    #             continue
    try:
        out = cheby2_bandpass_filter(data, freq-1000, freq+1000, fs)
    except Exception as e:
        print(e)
    outw = max(moving_average(out))
    time = np.linspace(0, fs*0.004*3, num=len(outw))
    #print out[0]
    # with open("out.csv", 'wb') as write:
    #     writer = csv.writer(write)
    #     for point in out:
    #         writer.writerow([round(point, 4)])
    #plt.plot(data)
    # print len(data)
    #print out
    plt.plot(time, out)
    # subprocess.call(["rm", "testcsv"])
    # subprocess.call(["gcc", "-o", "testcsv", "testcsv.c", "-lfftw3", "-lm"])
    plt.show()
