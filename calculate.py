#!/usr/bin/python3
#coding=utf-8
"""
Calculate the total amount in CNY of given csv file and writes the results on `results.csv`.
@file: calculate.py
@author: vincent cheung
"""

import csv
import argparse
import sys
import os
import pandas as pd
import numpy as np
import time

from gen_template_csv import gen_csv
from rate_scraper import get_rate

if __name__ == '__main__':
    # Parse CMD line parameters
    parser = argparse.ArgumentParser('Amount calculator for HKD&CNY.')
    parser.add_argument('-f','--file',type=str,help='Input csv file, deafult:templeate.csv',default='template.csv')
    parser.add_argument('-g','--gencsv', action="store_true",default=False)
    parser.add_argument('-gf','--gen_csv_path',type=str, help='Generate template csv file, deafult:./templeate.csv',default='template.csv')
    args = parser.parse_args()
    
    ## Generate template csv file and exits.
    if args.gencsv:
        gen_csv(args.gen_csv_path)
        sys.exit(0)

    # Read the csv file.
    if not os.path.isfile(args.file):
        print (u'The input:{} is not a file or does not exist'.format(args.file))
        sys.exit(0)

    df = pd.read_csv(args.file, encoding='utf-8')
    ## Header like 
    # '序号,日期,市内交通费人民币,市内交通费港币,长途交通费人民币,长途交通费港币,餐费人民币,餐费港币,其他费用人民币,其他费用港币'
    ## Replace Nan to zero
    df.fillna(0.0, inplace=True)

    data={'日期':[],'市内交通费':[],'长途交通费':[],'餐费':[],'其他费用':[],'备注':[]}
    ## Iterate each record
    for index, row in df.iterrows():
        date = row['日期']
        print ('Processing record on date:{}'.format(date))
        rate, info_str = get_rate(date)

        # Calculate the CNY seperately.
        # Summup according to the items in K3 ERP system.
        local_fee = row['市内交通费港币']/100.0*rate + row['市内交通费人民币']
        traverse_fee = row['长途交通费港币']/100.0*rate + row['长途交通费人民币']
        meal_fee = row['餐费港币']/100.0*rate + row['餐费人民币']
        other_fee = row['其他费用港币']/100.0*rate + row['其他费用人民币']
        
        # Collect data
        data['日期'].append(date)
        data['市内交通费'].append(local_fee)
        data['长途交通费'].append(traverse_fee)
        data['餐费'].append(meal_fee)
        data['其他费用'].append(other_fee)
        data['备注'].append(info_str)
        
        ## Sleep for 0.2 seconds in case of server error
        time.sleep(0.2)
    # Write down the results as csv files
    print ('')
    frame = pd.DataFrame(data, columns=['日期', '市内交通费', '长途交通费','餐费','其他费用','备注'])
    frame.to_csv('results.csv',encoding='utf-8', float_format='%.2f')
    print ('Write Done resutls.csv')
