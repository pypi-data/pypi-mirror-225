import pandas as pd
import matplotlib.pyplot as plt


class PumpFailureAnalyzer:
    def __init__(self,excel_path):
        self.data = self.import_data_from_excel(excel_path)
        self.failure_timestamps = []


        # 读取数据
    def import_data_from_excel(self,excel_path):
        """
        使用pandas 从 Excel文件中导入数据，并返回一个DataFrame对象
        :return:data
        """
        data = pd.read_excel(excel_path)
        return data




        # 检测断泵故障
    def detect_failure(self):
        """
        压力和流量测点分析故障
        :return: 故障判断结果（True或False）
        """



        for i in range(3,len(self.data)):
            timestamp = self.data.loc[i][ 'timing']
            oil_flow = self.data.loc[i]['oilFlow']
            inlet_oil_pres = self.data.loc[i][ 'inletOilPres']
            Serial = self.data.loc[i]['Serial']

            if self.check_pressure_trend(i,inlet_oil_pres) or self.check_pressure_value(i,inlet_oil_pres) :
                print(f"n = {Serial},{timestamp}:压力异常，疑似断泵！")
                self.failure_timestamps.append(timestamp)
            if self.check_flow_trend(i,oil_flow) or self.check_flow_value(i,oil_flow):
                print(f"n = {Serial},{timestamp}:流量异常，疑似断泵！")
                self.failure_timestamps.append(timestamp)

        # 判断压力变化趋势和压力数值是否异常
    def check_pressure_trend(self,i,inlet_oil_pres):
        pressure_change_rate = (self.data.iloc[i]['inletOilPres']-self.data.iloc[i-4]['inletOilPres'])/self.data.iloc[i-4]['inletOilPres']

        if pressure_change_rate <= -0.04 :
            return True
        else:
            return False

    def check_pressure_value(self,i,inlet_oil_pres):

        if self.data.iloc[i]['inletOilPres']<0.303 *  0.8:
            return True
        else:
            return False


        # 判断流量变化趋势和流量数值是否异常
    def check_flow_trend(self,i,oil_flow):
        flow_change_rate = (self.data.iloc[i]['oilFlow']-self.data.iloc[i-4]['oilFlow'])/self.data.iloc[i-4]['oilFlow']

        if flow_change_rate <= -0.05 :
            return True
        else:
            return False

    def check_flow_value(self,i,oil_flow):

        if self.data.iloc[i]['oilFlow']<337 *  0.9:
            return True
        else:
            return False


        # 将监测结果保存到csv文件中
    def save_results_to_csv(self,output_path):
        results = pd.DataFrame({'timestamp':self.failure_timestamps})
        results.to_csv(output_path,index=False)
        print(f"检测结果已保存至 {output_path}")


        # 可视化数据
    def visualize_data(self):


        fig, ax1 = plt.subplots(constrained_layout=True)
        ax2 = ax1.twinx()
        line1, = ax1.plot( self.data['Serial'],self.data['oilFlow'], '-',color='r',linewidth = 2.0,label = 'oilFlow' )
        line2, = ax2.plot( self.data['Serial'],self.data['inletOilPres'], '-', color='b', linewidth=2.0,label = 'inlet_oil_Pres')
        plt.legend((line1,line2),('oilFlow','inlet_oil_pres'),frameon=False,loc="lower right",fontsize='small')
        ax1.set_title('oilFlow and inletoilpres')
        ax1.set_ylabel('oilFlow',fontsize = 14)
        ax2.set_ylabel('inlet_oil_pres', fontsize=12)
        plt.show()






