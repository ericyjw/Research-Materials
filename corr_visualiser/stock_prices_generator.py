from data_processor import DataProcessor
from vae import Vae
from data_analyser import DataAnalyser
import numpy as np

import sys

argv = sys.argv
num_of_stocks = argv[1]
num_of_iterations = argv[2]

data_processor = DataProcessor()
data_processor.load_data_from_csv(num_of_stocks)
data_processor.process_stocks_df()
processed_data = data_processor.process_raw_stocks_data()

training_set = {}
testing_set = {}
simulation = {}
for code in processed_data:
    vae = Vae(processed_data[code])
    '''
        high_train_set -> each stock's first 80%
        high_test_set -> each stock's remaining 20%

        training_set -> each stock's generated samples for train set
        testing_set -> each stock's generated sample for test set 
    '''
    code_training_set, code_testing_set = vae.split_dataset()
    training_set[code] = code_training_set
    testing_set[code] = code_testing_set
    vae.build_model()

    iter_simulation = []
    for i in range(num_of_iterations):
        vae.train_model(code_training_set)
        simulated = vae.simluate(code_testing_set)

        iter_simulation.append(simulated)
    
    simulation[code] = iter_simulation

data_analyser = DataAnalyser(processed_data, training_set, testing_set, simulated)
data_analyser.plot_2_chart_iter_365days(simulation)
data_analyser.plot_2_chart_iter_whole_period(simulation)
data_analyser.calculate_corr(simulation)