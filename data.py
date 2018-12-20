# -*- coding: utf-8 -*-
"""
ディレクトリ上のすべてのTubデータを先頭から順番に読み込み、
PubPilot/PubImageが送信するメッセージに変換

Usage:
    data.py [--tub=TUB_DIR]

Options:
    --tub=TUB_DIR               タブディレクトリのパス。
"""
import os
import docopt
import glob
import json
from datetime import datetime

class Tubs:
    def __init__(self, tub_dir):
        if tub_dir is None:
            raise Exception('no tub_dir')
        self.tub_dir = os.path.expanduser(tub_dir)
        if not os.path.exists(self.tub_dir):
            raise Exception('{} is not exists'.format(self.tub_dir))
        if not os.path.isdir(self.tub_dir):
            raise Exception('{} is not a directory'.format(self.tub_dir))
        
        records = glob.glob(os.path.join(self.tub_dir, 'record_*.json'))
        images = glob.glob(os.path.join(self.tub_dir, '*_cam-image_array_.jpg'))

        record_dict = {}
        for record in records:
            cnt = int(record.rsplit('record_')[-1].rsplit('.json')[0])
            record_dict[cnt] = record
        
        self.sorted_records = []
        sorted_record_keys = sorted(list(record_dict.keys()))
        for sorted_record_key in sorted_record_keys:
            self.sorted_records.append(record_dict[sorted_record_key])
        
        image_dict = {}
        for image in images:
            cnt = int(os.path.basename(image).rsplit('_cam-image_array_.jpg')[0])
            image_dict[cnt] = image
        
        self.sorted_images = []
        sorted_image_keys = sorted(list(image_dict.keys()))
        for sorted_image_key in sorted_image_keys:
            self.sorted_images.append(image_dict[sorted_image_key])

        if sorted_record_keys != sorted_image_keys:
            raise Exception('unmatch magic numner no_records={}, no_images={}'.format(
                str(sorted_record_keys - sorted_image_keys), str(sorted_image_keys - sorted_record_keys)
            ))
    
    def __call__(self):
        for index in range(len(self.sorted_records)):
            yield TubRecord(self.sorted_records[index]).get(), TubImage(self.sorted_images[index]).get()
    

class Tub:
    def eval_file(self, path):
        if path is None:
            raise Exception('no record_path')
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            raise Exception('{} is not exists'.format(path))
        if not os.path.isfile(path):
            raise Exception('{} is not a file'.format(path))
        return path

class TubRecord(Tub):
    def __init__(self, path):
        with open(self.eval_file(path), 'r') as f:
            org_dict = json.load(f)
        self.throttle = org_dict['user/throttle']
        self.angle = org_dict['user/angle']

    def get(self):
        return {
            "throttle":     self.throttle,
            "angle":        self.angle,
            "timestamp":    str(datetime.now())
        }

class TubImage(Tub):
    def __init__(self, path):
        with open(self.eval_file(path), 'br') as f:
            self.image = f.read()

    def get(self):
        return self.image


if __name__ == '__main__':
    #print('[__main__] start')
    # 引数情報の収集
    args = docopt.docopt(__doc__)

    
    tub_dir = args['--tub']
    if tub_dir is None:
        tub_dir='tub'
    
    tubs = Tubs(tub_dir)
    for record,image in tubs():
        print(' data=' + str(record))
        #print(' image=' + str(image))
    #print('[__main__] end')