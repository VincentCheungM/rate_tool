#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Generate template CSV file.
@author: vincent cheung
"""

import csv
import os

def gen_csv(file_path='template.csv'):
    """
    Generate template csv file.
    Input:
    `file_path`: The file_path to generate the csv file, defaults `./template.csv`.
    """
    if os.path.exists(os.path.dirname(file_path)) is False and os.path.dirname(file_path) != '':
        os.makedirs(os.path.dirname(file_path))
    with open(file_path,'w') as f:
        f.writelines('序号,日期,市内交通费人民币,市内交通费港币,长途交通费人民币,长途交通费港币,餐费人民币,餐费港币,其他费用人民币,其他费用港币')
        f.close()
        print (u'The template has been generated as {}'.format(file_path))
        print (u'Done')

if __name__ == '__main__':
    gen_csv()
