import matplotlib.pyplot as plt
import numpy as np
import csv

'''定義濾波器'''
class FIRFilter:
    '''初始化 FIR 濾波器'''
    def __init__(self, order):
        self.ORDER = order
        self.input_value = [0] * self.ORDER
        self.parameter = [1.0 / self.ORDER] * self.ORDER
    
    '''對單個輸入數據進行濾波處理'''
    def fir(self, newinData):
        # 移位暫存器
        for i in range(self.ORDER - 1, 0, -1):
            self.input_value[i] = self.input_value[i - 1]
        self.input_value[0] = newinData

        # FIR運算
        output = sum(self.parameter[i] * self.input_value[i] for i in range(self.ORDER))
        return output
    
'''負責處理太陽能數據，應用 FIR 濾波器，進行數據分析和可視化'''
class SolarDataProcessor:
    def __init__(self, filename, fir_order):
        self.filename = filename
        self.fir_filter = FIRFilter(fir_order)
        self.data = []
    
    def read_data(self):
        with open(self.filename, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.data.append(float(row[1]))
    
    def process_data(self):
        input_list = []
        output_list = []
        control_list = []
        original_ramp_rate = 0
        output_ramp_rate = 0

        # FIR 濾波處理和數據記錄
        for j in range(len(self.data)):
            i = self.data[j]
            input_list.append(i)
            original_ramp_rate += abs(self.data[j - 1] - i) if j > 0 else 0

            # FIR 濾波器處理
            output = self.fir_filter.fir(i)
            output_list.append(output)
            output_ramp_rate += abs(output_list[j - 1] - output_list[j]) if j > 0 else 0

            # 控制值計算
            control_list.append(i - output)
        
        original_ramp_rate /= len(self.data)
        output_ramp_rate /= len(self.data)

        return input_list, output_list, control_list, original_ramp_rate, output_ramp_rate

    def plot_data(self, input_list, output_list, control_list):
        x = np.arange(len(input_list))
        plt.plot(x, input_list, label = "input")
        plt.plot(x, output_list, label = "output")
        plt.plot(x, control_list, label = "control")
        plt.legend()
        plt.show()

# 主程式
if __name__ == "__main__":
    filename = 'solor_data_1.csv'
    fir_order = 150

    # 創建太陽能數據處理器
    processor = SolarDataProcessor(filename, fir_order)

    # 讀取數據
    processor.read_data()

    # 處理數據並獲取結果
    input_list, output_list, control_list, original_ramp_rate, output_ramp_rate = processor.process_data()

    # 打印平均斜率變化率
    print("original ramp rate = ", original_ramp_rate)
    print("output ramp rate = ", output_ramp_rate)

    # 繪製數據
    processor.plot_data(input_list, output_list, control_list)


