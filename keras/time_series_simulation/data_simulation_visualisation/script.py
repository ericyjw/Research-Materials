#!/usr/bin/python

import os
import sys

os.system('echo {}'.format(sys.argv))
curr_dir = os.getcwd()
os.chdir('{}/gephi_visualisation'.format(curr_dir))
os.system('mvn clean install')
os.system('mvn exec:java -Dexec.mainClass=Main -Dexec.args="../corr_real.csv" -Dexec.cleanupDaemonThreads=false')
