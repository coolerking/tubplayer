# -*- coding: utf-8 -*-
"""
Tubディレクトリ上にあるデータを順番にMQTTブローカ(IBM Watson IoT Platform)へ
データがなくなるまで送信する。 

Usage:
    tubplayer.py [--conf=CONFIG_PATH] [--tub=TUB_DIR] [--interval=INTERVAL_SECS]

Options:
    --config=CONFIG_PATH      設定ファイルパス。
    --tub=TUB_DIR             送信するイメージファイルのパス。
    --interval=INTERVAL_SECS  publish間のインターバル時間（秒）。
"""
import os
import pytz
import json
import random
from datetime import datetime
import docopt
from time import sleep
import ibmiotf.device
from ibmiotf import MessageCodec, Message, InvalidEventException
#import ibmiotf.application

from data import Tubs

class ImageCodec(MessageCodec):
    """
    フォーマット形式'image'に対応するCodecクラス。
    
      deviceCli.setMessageCodec("image", ImageCodec)
    """
    
    @staticmethod
    def encode(data=None, timestamp=None):
        """
        data を送信可能なデータに変換する。
        dataは numpy.ndarray型式、各要素はuint8、全要素バイト数は57600、
        型式は(120, 160, 3)。

        引数
            data        送信データ(np.ndarray型式)
            timestamp   タイムスタンプ
        戻り値
            img         文字列化されたdata
        """
        #img = data.tostring()
        return data #img
    
    @staticmethod
    def decode(message):
        """
        文字列をnp.ndarray型式に戻し型を(120, 160, 3)に戻す。

        引数
            message     受信メッセージ
        戻り値
            Messageオブジェクト
        """
        #try:
        #    data = message.payload.decode('utf-8')
        #    data = np.fromstring(data, dtype=np.uint8)
        #    data = np.reshape(data, (120, 160, 3))
        #except ValueError as e:
        #    raise InvalidEventException("Unable to parse image.  payload=\"%s\" error=%s" % (message.payload, str(e)))
        timestamp = datetime.now(pytz.timezone('UTC'))
        
        # TODO: Flatten JSON, covert into array of key/value pairs
        return Message(message, timestamp)

def publish_forever(config_path='emperor.ini', generator=None, interval=10):
    """
    一定間隔でpublishを繰り返す。

    引数
        config_path     設定ファイルパス
        generator       Tubデータを送信メッセージジェネレータ
        interval        間隔
    """
    try:
        options = ibmiotf.device.ParseConfigFile(config_path)
        client = ibmiotf.device.Client(options)
        client.setMessageEncoderModule('image', ImageCodec)
        print('[publish_forever] config loaded')
    except ibmiotf.ConnectionException  as e:
        print('[publish_forever] config load failed ' + config_path)
        raise e

    client.connect()
    print('[publish_forever] connect client')

    try:
        for msg, image in generator():

            client.publishEvent(event='status', msgFormat='json', data=msg, qos=0)
            print('[publish_forever] published :' + json.dumps(msg))

            #sleep(interval)

            client.publishEvent(event='status', msgFormat='image', data=image, qos=0)
            print('[publish_forever] published image')

            sleep(interval)
    finally:
        client.disconnect()

if __name__ == '__main__':
    print('[tubplayer] start')
    args = docopt.docopt(__doc__)

    conf_path = args['--conf']
    if conf_path is None:
        conf_path = 'emperor.ini'
    
    interval = args['--interval']
    if interval is None:
        interval = 1.0/20.0 #20Hz default
    else:
        interval = float(interval)
    
    tub_dir = args['--tub']
    if tub_dir is None:
        tub_dir ='tub'
  
    generator = Tubs(tub_dir)

    publish_forever(conf_path, generator, interval)
    print('[tubplayer] end')