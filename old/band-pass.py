import csv
import os
from scipy.signal import cheby2, lfilter

freq = 40000

bandpassw = 500

fs = 130000


#get bandpass filter parameter
def cheby2_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = cheby2(order, 5, [low, high], btype='bandpass')
    return b, a

#filter the data with bandpass
def cheby2_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = cheby2_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    #sampling
    datapath = "/Users/estellehe/Documents/Robo/Acoustic/data/"
    outpath = "/Users/estellehe/Documents/Robo/Acoustic/filtered_data/"

    for file in os.listdir(datapath):
        data0 = []
        data1 = []
        data2 = []
        out0 = []
        out1 = []
        out2 = []

        with open(os.path.join(datapath, file), 'rb') as filec:
            reader = csv.reader(filec)
            for row in reader:
                try:
                    data0.append(float(row[0]))
                    data1.append(float(row[1]))
                    data2.append(float(row[2]))
                except:
                    continue

        try:
            out0 = cheby2_bandpass_filter(data0, freq-bandpassw/2, freq+bandpassw/2, fs)
            out1 = cheby2_bandpass_filter(data1, freq-bandpassw/2, freq+bandpassw/2, fs)
            out2 = cheby2_bandpass_filter(data2, freq-bandpassw/2, freq+bandpassw/2, fs)
        except Exception as e:
            print(e)

        with open(os.path.join(outpath, file.replace(".csv", "_filtered.csv")), 'wb') as write:
            writer = csv.writer(write)
            for k in range(len(out0)):
                writer.writerow([round(out0[k], 4), round(out1[k], 4), round(out2[k], 4)])
