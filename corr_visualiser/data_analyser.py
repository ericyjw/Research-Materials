import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

real_data = {}
simulated_data = {}

class DataAnalyser:
    def __init__(self, processed_data, training_set, testing_set, simulated):
        super().__init__()

        self.processed_data = processed_data
        self.training_set = training_set
        self.testing_set = testing_set
        self.simulated = simulated

    def plot_2_chart_iter_365days(self, simulation):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))

        code_names = []
        for code in self.processed_data:
            code_names.append(code)

        code = code_names[0]
        code_max_high = self.processed_data[code][1]
        ax1.plot(code_max_high * self.testing_set[code].flatten(), label='{} real data'.format(code),linewidth=5)
        for i in range(len(simulation[code])):
            ax1.plot(code_max_high * simulation[code][i].flatten(), label='{} simulated data {}'.format(code, i))
        
        ax1.legend(loc='upper left')

        code = code_names[1]
        code_max_high = self.processed_data[code][1]
        ax2.plot(code_max_high * self.testing_set[code].flatten(), label='{} real data'.format(code),linewidth=5)
        for i in range(len(simulation[code])):
            ax2.plot(code_max_high * simulation[code][i].flatten(), label='{} simulated data {}'.format(code, i))
        
        ax2.legend(loc='upper left')

        plt.show() 

    def plot_2_chart_iter_whole_period(self, simulation):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))

        code_names = []
        for code in self.processed_data:
            code_names.append(code)

        code = code_names[0]
        code_max_high = self.processed_data[code][1]
        code_x_test = self.testing_set[code]
        code_x_train = self.training_set[code]
        ax1.plot(code_max_high * np.append(code_x_train, code_x_test).flatten(), label='{} real data'.format(code))
        for i in range(len(simulation[code])):
            ax1.plot(code_max_high * np.append(code_x_train, simulation[code][i]).flatten(), label='{} simulated data {}'.format(code, i))
        
        ax1.legend(loc='upper left')

        code = code_names[1]
        code_max_high = self.processed_data[code][1]
        code_x_test = self.testing_set[code]
        code_x_train = self.training_set[code]
        ax2.plot(code_max_high * np.append(code_x_train, code_x_test).flatten(), label='{} real data'.format(code))
        for i in range(len(simulation[code])):
            ax2.plot(code_max_high * np.append(code_x_train, simulation[code][i]).flatten(), label='{} simulated data {}'.format(code, i))
        
        ax2.legend(loc='upper left')

        plt.show() 

    def calculate_corr(self, simulation):

        # Real Data
        corr_real_data = {}
        for code in self.processed_data:
            real_high = self.processed_data[code][1] * self.testing_set[code]
            corr_real_data['{}_High'.format(code)] = real_high.flatten()

        corr_real_df = pd.DataFrame(data=corr_real_data)
        print(corr_real_df.corr())
        corr_real_df.corr().to_csv('result/corr_real.csv')


        # Simulated Data
        for i in range(len(next(iter(simulation.values())))):
            # Each iteration
            corr_simulated_iter_data = {}
            for code in self.processed_data:
                simulated_high = self.processed_data[code][1] * simulation[code][i]
                corr_simulated_iter_data['{}_High_Iter {}'.format(code, i)] = simulated_high.flatten()
            
        
            corr_simulated_iter_df = pd.DataFrame(data = corr_simulated_iter_data)
            print(corr_simulated_iter_df.corr())
            corr_simulated_iter_df.corr().to_csv('result/corr_simulated_iter_{}.csv'.format(i))





        # code = code_names[0]
        # code_max_high = self.processed_data[code][1]
        # code_x_test = self.testing_set[code]
        # code_x_train = self.training_set[code]
        # ax1.plot(code_max_high * np.append(code_x_train, code_x_test).flatten(), label='{} real data'.format(code))
        # for i in range(len(simulation[code])):
        #     ax1.plot(code_max_high * np.append(code_x_train, simulation[code][i]).flatten(), label='{} simulated data {}'.format(code, i))
        
       





        # corr_simulated_data = {}
        # for code in processed_data:
        #     corr_real_data['{} High'.format(code)] = real_data[code]
        #     corr_simulated_data['{} High Simulated'.format(
        #         code)] = simulated_data[code]

        # corr_real_df = pd.DataFrame(data=corr_real_data)
        # corr_simulated_df = pd.DataFrame(data=corr_simulated_data)
        # combined_data = corr_real_data.update(corr_simulated_data)
        # corr_total_df = pd.DataFrame(data=combined_data)

        # print(corr_real_df.corr())
        # corr_real_df.corr().to_csv('corr_real.csv')

        # print(corr_simulated_df.corr())
        # corr_simulated_df.corr().to_csv('corr_simulated.csv')

        # print(corr_total_df.corr())
        # corr_total_df.corr().to_csv('corr_total.csv')