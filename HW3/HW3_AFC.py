import matplotlib.pyplot as plt
import numpy as np

def dReg(frequency):
    if frequency < 59.75:
        return 1
    elif 59.75 <= frequency < 59.98:
        return round((-1 / 0.23) * (frequency - 59.98), 2)      #59.98 Hz 為臨界值（參考點），代表頻率稍微高於理想值 60 Hz 的情況。此範圍通常被視為系統還可以接受的頻率範圍，但需要做一些功率調節來防止頻率進一步偏離理想值。
    elif 59.98 <= frequency < 60.02:
        return 0
    elif 60.02 <= frequency < 60.25:
        return round((-1 / 0.23) * (frequency - 60.02), 2)      #60.02 Hz 為臨界值（參考點），代表頻率稍微高於理想值 60 Hz 的情況。此範圍通常被視為系統還可以接受的頻率範圍，但需要做一些功率調節來防止頻率進一步偏離理想值。
    elif frequency >= 60.25:
        return -1
    else:
        return 0

#主程式
if __name__ == "__main__":
    frequency = np.arange(59.5, 60.5, 0.01)
    power_list = []
    for i in frequency:
        power_list.append(dReg(i))
    plt.scatter(x = frequency, y = power_list)
    plt.show()