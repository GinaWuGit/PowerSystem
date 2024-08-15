import matplotlib.pyplot as plt
import csv

class CSVReader:
    def __init__(self, file):
        self.file = file
        self.time_data = []
        self.load_data = []
        self.mppt_data = []

    '''讀取CSV內容，將資料放到data的list中'''
    def read(self):
        with open(self.file, newline='') as f:              #newline='': 確保不會在文件中插入額外的空行
            reader = csv.reader(f, delimiter = '\t')        #將每行數據分割為三部分(假設數據在 CSV 文件中使用制表符 (\t) 作為分隔符。如果文件使用逗號（,）或其他分隔符，則需要調整 split 方法的參數)
            next(reader)                                    # Skip header row
            for row in reader:
                self.time_data.append(row[0])
                self.load_data.append(float(row[1]))
                self.mppt_data.append(float(row[2]))
            return self.time_data, self.load_data, self.mppt_data

class Control:
    def __init__(self, soc, solar_list, load_list) -> None:
        self.soc = soc
        self.battery_capacity = 200     #Unit:kW
        self.solar_list = solar_list
        self.load_list = load_list
        self.grid_list = []
        self.battery_power = []
        self.soc_list = []
    
    def cal(self):
        for solar, load in zip(self.solar_list, self.load_list):
            self.soc_list.append(self.soc)
            self.calculate(solar, load)
    
    def calculate(self, solar, load):
        net_energy = solar - load
        grid = battery_power = 0

        if 10 < self.soc <= 90:
            battery_power = net_energy

        elif self.soc > 90:
            if net_energy > 0:
                grid = -net_energy              #太陽能太多，送市電(將多餘能量回送到電網，表示能量從系統流出到電網，在能量流動模型中，我們將這個多餘的能量標記為負值)
            else:
                battery_power = net_energy
        
        elif self.soc <= 10:
            if solar >= load:
                net_energy = self.battery_capacity + solar - load       #在太陽能滿足負載後，將剩餘能量用於充電所需的能量
            elif solar < load:
                net_energy = self.battery_capacity + load - solar       #用市電充電:滿足負載需求、充滿電池（達到最大電池容量）所需的額外能量

            grid = net_energy                                           #需要從市電中獲取 net_energy 的能量來補充系統需求
            battery_power = -net_energy + load                          #-net_energy :從市電中獲取的能量，由於市電需要補充到電池中，所以取負值

        self.grid_list.append(grid)
        self.battery_power.append(battery_power)
        self.soc += self.calculate_soc(battery_power)

    def calculate_soc(self, battery_power):
        return battery_power / self.battery_capacity

class Dual_Axis:
    def __init__(self):
        self.fig, self.ax1 = plt.subplots(figsize = (12, 8), dpi = 80)   #plt.subplots(): 用於創建圖表（Figure）和子圖（Axes）
        self.ax2 = self.ax1.twinx()                                      #與 ax1 共享同一個 X 軸的基礎上，創建一個新的 Y 軸
    
    def plot(self, list1, list2, color1, color2, label1 = 'list1', label2 = 'list2'):
        self.ax1.plot(list1, color1, label = label1)
        self.ax2.plot(list2, color2, label = label2)
    
    def draw(self, pause_time = 1):
        self.fig.tight_layout()
        plt.draw()
        plt.pause(pause_time)

if __name__ == '__main__':
    csv_reader = CSVReader('./60kw_power_0.csv')
    time, load, solar = csv_reader.read()
    
    control = Control(40, solar, load)      #初始化 SOC 為 40，將讀取的太陽能發電量mppt和負載load數據傳遞給它
    dual_axis = Dual_Axis()
    control.cal()

    dual_axis.plot(control.grid_list, control .soc_list, 'r--', 'g-', 'Grid_power', 'Soc')
    dual_axis.ax1.plot(control.solar_list, 'y-', label='Solar_power')
    dual_axis.ax1.plot(control.battery_power, 'g--', label='Battery_power')
    dual_axis.ax1.plot(control.load_list, 'b-', label='Load_power')
    dual_axis.ax1.legend(loc=2)
    dual_axis.ax2.legend()
    plt.show()


 








