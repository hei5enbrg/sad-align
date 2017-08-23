## SAD alignment
import numpy as np
import matplotlib.pyplot as plt
import sys

PATH_TO = sys.argv[1]

wd_start, wd_stop = (2400, 4000) 
rwd_start, rwd_stop = (2500, 3900)
ref_sample =  22
# load traces
gettrace = np.load(PATH_TO + "traces_og.npy")
reftrace = gettrace[ref_sample][rwd_start:rwd_stop]
reflen = rwd_stop-rwd_start
sadlen = wd_stop-wd_start
num_of_traces = 100

plt.figure(1)
arr = None

for trace_no in range(0, num_of_traces):
    inputtrace = gettrace[trace_no]
    sadarray = np.empty(sadlen-reflen)

    for ptstart in range(wd_start, wd_stop-reflen):
        sadarray[ptstart-wd_start] = np.sum(np.abs(inputtrace[ptstart:(ptstart+reflen)] - reftrace))

    newmaxloc = np.argmin(sadarray)
    maxval = min(sadarray)

    shift = wd_start + newmaxloc - rwd_start

    plt.subplot(211)
    plt.plot(inputtrace, linewidth=.5)

    enable = 1
    if enable:
        if shift < 0:
            inputtrace = np.append(np.zeros(-shift), inputtrace[:shift])
        elif shift > 0:
            inputtrace = np.append(inputtrace[shift:], np.zeros(shift))

    plt.subplot(212)
    plt.plot(inputtrace, linewidth=.5)

    if arr == None:
        arr = inputtrace
    else:
        arr = np.vstack([arr, inputtrace])

plt.subplot(211)
plt.plot(gettrace[ref_sample], linewidth=.5)
plt.subplot(212)
plt.plot(gettrace[ref_sample], linewidth=.5)
# save aligned traces
np.save(PATH_TO + "traces_sad.npy", arr)
# plot traces
plt.show()



