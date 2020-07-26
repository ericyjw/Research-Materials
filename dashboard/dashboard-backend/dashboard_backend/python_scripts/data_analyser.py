import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

real_data = {}
simulated_data = {}


class DataAnalyser:
    def __init__(self, merged_df, processed_data):
        super().__init__()

        self.merged_df = merged_df
        self.processed_data = processed_data
        # self.training_set = training_set
        # self.testing_set = testing_set
        # self.simulated = simulated

    # def plot_2_chart_iter_365days(self, simulation):
    #     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))

    #     code_names = []
    #     for code in self.processed_data:
    #         code_names.append(code)

    #     code = code_names[0]
    #     code_max_high = self.processed_data[code][1]
    #     ax1.plot(code_max_high * self.testing_set[code].flatten(), label='{} real data'.format(code),linewidth=5)
    #     for i in range(len(simulation[code])):
    #         ax1.plot(code_max_high * simulation[code][i].flatten(), label='{} simulated data {}'.format(code, i))

    #     ax1.legend(loc='upper left')

    #     code = code_names[1]
    #     code_max_high = self.processed_data[code][1]
    #     ax2.plot(code_max_high * self.testing_set[code].flatten(), label='{} real data'.format(code),linewidth=5)
    #     for i in range(len(simulation[code])):
    #         ax2.plot(code_max_high * simulation[code][i].flatten(), label='{} simulated data {}'.format(code, i))

    #     ax2.legend(loc='upper left')

    #     plt.show()

    # def plot_2_chart_iter_whole_period(self, simulation):
    #     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))

    #     code_names = []
    #     for code in self.processed_data:
    #         code_names.append(code)

    #     code = code_names[0]
    #     code_max_high = self.processed_data[code][1]
    #     code_x_test = self.testing_set[code]
    #     code_x_train = self.training_set[code]
    #     ax1.plot(code_max_high * np.append(code_x_train, code_x_test).flatten(), label='{} real data'.format(code))
    #     for i in range(len(simulation[code])):
    #         ax1.plot(code_max_high * np.append(code_x_train, simulation[code][i]).flatten(), label='{} simulated data {}'.format(code, i))

    #     ax1.legend(loc='upper left')

    #     code = code_names[1]
    #     code_max_high = self.processed_data[code][1]
    #     code_x_test = self.testing_set[code]
    #     code_x_train = self.training_set[code]
    #     ax2.plot(code_max_high * np.append(code_x_train, code_x_test).flatten(), label='{} real data'.format(code))
    #     for i in range(len(simulation[code])):
    #         ax2.plot(code_max_high * np.append(code_x_train, simulation[code][i]).flatten(), label='{} simulated data {}'.format(code, i))

    #     ax2.legend(loc='upper left')

    #     plt.show()

    def get_reports(self, report_name, window_size):
        print('===== Divide Processed Stocks Data into Window Size =====')
        datasets = []
        key_0 = list(self.processed_data.keys())[0]
        num_of_window = math.ceil(
            len(self.processed_data[key_0][0]) / window_size)

        for i in range(num_of_window):
            data = {}
            for k in self.processed_data:
                start_index = i * window_size
                end_index = i * window_size + window_size
                max_index = len(self.processed_data[k][0])

                if end_index > max_index:
                    end_index = max_index

                data[k] = (self.processed_data[k][0][start_index:end_index],
                           self.processed_data[k][1], {'window_period_start': self.merged_df.index[start_index],
                                                       'window_period_end': self.merged_df.index[end_index]})
            datasets.append(data)

        print('===== Calculate Correlation for Each Dataset =====')
        corr_dfs = []
        time_series_plts = []
        for index in range(len(datasets)):
            ds = datasets[index]
            actual_data = {}
            plt.figure()

            for k in ds:
                normalised_data = ds[k][0]
                max_high = ds[k][1]
                actual_high = normalised_data * float(max_high)
                actual_data[k] = actual_high.flatten()

                plt.plot(actual_data[k], label=k)

            # time-series graph
            key_0 = list(ds.keys())[0]
            start_date = ds[key_0][2]['window_period_start']
            end_date = ds[key_0][2]['window_period_end']
            plt.title("From {} To {}".format(start_date, end_date))
            plt.legend(loc='upper left')

            graph_chart_path = os.path.join('temp', 'graph_chart', report_name)
            if not os.path.exists(graph_chart_path):
                os.makedirs(graph_chart_path)
            plt_file = plt.savefig(os.path.join(graph_chart_path, "{}_{}.png".format(report_name, index)))
            time_series_plts.append(plt_file)
            
            plt.close()

            # corr_csv
            actual_data_df = pd.DataFrame(data=actual_data)
            corr_dfs.append(actual_data_df.corr())

            # gephi_report

            # metrics_csv

        return time_series_plts, corr_dfs

    def calculate_corr(self, ):

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
                simulated_high = self.processed_data[code][1] * \
                    simulation[code][i]
                corr_simulated_iter_data['{}_High_Iter {}'.format(
                    code, i)] = simulated_high.flatten()

            corr_simulated_iter_df = pd.DataFrame(
                data=corr_simulated_iter_data)
            print(corr_simulated_iter_df.corr())
            corr_simulated_iter_df.corr().to_csv(
                'result/corr_simulated_iter_{}.csv'.format(i))

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
