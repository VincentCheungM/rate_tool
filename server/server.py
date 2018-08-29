#!/usr/bin/python3
#coding=utf-8
"""
A flask based server for calculating.
@author: vincent cheung
@file: server.py
"""
from flask import Flask,render_template,request,redirect,url_for
from flask import send_file, Response
import os

import sys
sys.path.append('../')

from calculate import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Get the upload file
        f = request.files['file']
        # Read the upload CSV file
        # TODO: Check File funtion not yet implemented
        df = pd.read_csv(f, encoding='utf-8')
        ## Header like 
        head_str = u'序号,日期,市内交通费人民币,市内交通费港币,长途交通费人民币,长途交通费港币,餐费人民币,餐费港币,其他费用人民币,其他费用港币'
        head_str_list = head_str.split(',')
        #### Check upload file
        if len(head_str_list) != df.shape[1]:
            return 'Wrong file, please re-upload'
        for i,j in zip(df.head(0),head_str_list):
            if i != j:
               return 'Wrong file, please re-upload' 

        #### Start process upload file
        ## Replace Nan to zero
        df.fillna(0.0, inplace=True)
        data={'日期':[],'市内交通费':[],'长途交通费':[],'餐费':[],'其他费用':[],'备注':[]}
        ## Iterate each record in df
        for index, row in df.iterrows():
            date = row[u'日期']
            print ('Processing record on date:{}'.format(date))
            rate, info_str = get_rate(date)

            # Calculate the CNY seperately.
            # Summup according to the items in K3 ERP system.
            local_fee = row[u'市内交通费港币']/100.0*rate + row[u'市内交通费人民币']
            traverse_fee = row[u'长途交通费港币']/100.0*rate + row[u'长途交通费人民币']
            meal_fee = row[u'餐费港币']/100.0*rate + row[u'餐费人民币']
            other_fee = row[u'其他费用港币']/100.0*rate + row[u'其他费用人民币']
            
            # Collect data
            data['日期'].append(date)
            data['市内交通费'].append(local_fee)
            data['长途交通费'].append(traverse_fee)
            data['餐费'].append(meal_fee)
            data['其他费用'].append(other_fee)
            data['备注'].append(info_str)
            
            ## Sleep for 0.05 seconds in case of BOC server error
            # TODO: May cause error while the input dataframe is too big, which cause the http link broken
            time.sleep(0.05)

        ## Save resutls in csv format
        frame = pd.DataFrame(data, columns=['日期', '市内交通费', '长途交通费','餐费','其他费用','备注'])
        csv_buf = frame.to_csv(encoding='utf-8', float_format='%.2f')
        ## Return for download
        file_name = 'results.csv'
        response = Response(csv_buf, mimetype='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=results.csv;"        
        return response

    return render_template('index.html')

@app.route('/template.csv', methods=['POST', 'GET'])
def csv():
    ## Return file for download       
    return send_file('template.csv')


if __name__ == '__main__':
    app.run(debug=True)
