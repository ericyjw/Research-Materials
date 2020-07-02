#!/usr/bin/python

import os
import sys
import getopt
import pandas as pd


def main(argv):
    run_generator = False
    num_of_stocks = 100
    num_of_iterations = 10

    try:
        opts, args = getopt.getopt(argv, "hgs:i:", ["num_of_stocks=", "num_of_iterations="])
    except getopt.GetoptError:
        print('-g flag: running stocks data generator to generate more data')
        print('-s flag: number of stocks to evaluate')
        print('-i flag: number of iterations to evaluate')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-g flag: running stocks data generator to generate more data')
            print('-s flag: number of stocks to evaluate')
            print('-i flag: number of iterations to evaluate')
            sys.exit()
        elif opt == '-g':
            run_generator = True
        elif opt in ("-s", "--num_of_stocks"):
            num_of_stocks = arg
        elif opt in ("-i", "--num_of_iterations"):
            num_of_iterations = arg

    print('Running Stocks Data Generator: {}'.format(run_generator))
    print('Number of stocks evaluated: {}'.format(num_of_stocks))
    print('Number of iterations to evaluate: {}'.format(num_of_iterations))
    
    if run_generator:
        os.system('python3 stock_prices_generator.py {} {}'.format(num_of_stocks, num_of_iterations))
    
    curr_dir = os.getcwd()
    os.chdir('{}/gephi_visualisation'.format(curr_dir))
    os.system('mvn clean install')

    dir = '../result/'
    files = []
    for _, _, f in os.walk(dir):
        for file in f:
            if '.csv' in file:
                print('file: {}{}'.format(dir, file))
                filename = '{}{}'.format(dir, file)
                os.system(
                    'mvn exec:java -Dexec.mainClass=Main -Dexec.args="{}" -Dexec.cleanupDaemonThreads=false'.format(filename))


if __name__ == "__main__":
    main(sys.argv[1:])


