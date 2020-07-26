#!/usr/bin/python

import os
import sys
import getopt
# import pandas as pd
from data_processor import DataProcessor

def main(argv):
    data =''
    start_date = ''
    end_date = ''
    print("inside script")

    try:
        opts, args = getopt.getopt(argv, "d:s:e:", ["num_of_stocks=", "num_of_iterations="])
    except getopt.GetoptError:
        print('-d flag: javascript date')
        print('-s flag: start date')
        print('-e flag: end date')
        sys.exit(2)
    for opt, arg in opts:
        # print("opt", opt)
        # print("arg", arg)
        if opt == '-h':
            print('-d flag: javascript date')
            print('-s flag: start date')
            print('-e flag: end date')
            sys.exit()
        elif opt == ("-d", "--data"):
            data = arg
        elif opt in ("-s", "--start_date"):
            start_date = arg
        elif opt in ("-i", "--end_date"):
            end_date = arg

    print('Javascript Object: {}, length: {}'.format(type(data), len(data)))
    print('Start Date: {}'.format(start_date))
    print('End Date: {}'.format(end_date))


    # data_processor = DataProcessor()
    # data_processor.process_javascript_data(data, start_date, end_date)


if __name__ == "__main__":
    main(sys.argv[1:])


