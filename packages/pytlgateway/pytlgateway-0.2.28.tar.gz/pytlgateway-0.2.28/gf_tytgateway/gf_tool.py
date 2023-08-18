import sys
import json
from datetime import datetime
import traceback
import argparse

from ..mongo_client_gateway import MongoClientTradeGateway
from .constants import (FILES, GATEWAY_NAME)
from .utils import str2bool


class GfTool(MongoClientTradeGateway):
    def __init__(self, config_filename, sync_pos,  end_time, gateway_name):
        MongoClientTradeGateway.__init__(self, config_filename, end_time, gateway_name)
        self.update_trade_date = self.date
        self.sync_pos = sync_pos
        self.load_tool_setting(config_filename)

    def load_tool_setting(self, config_filename):
        try:
            #config_filename = os.path.join(config_path, 'atx_server_config.json')
            f = open(config_filename, encoding='gbk')
            setting = json.load(f)
            #self.recv_msg_dir = setting['recv_msg_path'].replace('/', '\\')
            self.sync_position_open = setting['sync_position_open']
            self.sync_position_close = setting['sync_position_close']

        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            print(f"load config failed! (exception){err}")
            exit(0)
    
    def start(self):
        
        if self.sync_pos == True:
            self.date_change()
            _msg = "[gf_date_change] executed"
            self.send_to_user(logger=self.logger, url_list=self.url_list, msg=_msg)
    
    @MongoClientTradeGateway.error_handler
    def date_change(self):
        dt = datetime.now()
        self.logger.info(f"(dt){dt.hour}")
        if dt.hour <= self.sync_position_open and self.sync_pos == True:
            self.logger.info("[date_change] date_change_open")
            self.update_position_date_open()
        elif dt.hour < self.sync_position_close and dt.hour > self.sync_position_open:
            self.logger.info("[date_change] date_not_change")
        elif dt.hour >= self.sync_position_close and self.sync_pos == True:
            self.logger.info("[date_change] date_change_close")
            self.update_position_date_close()
        else:
            self.logger.info("[date_change] date_not_change")
            return




if __name__ == "__main__":

    description = "sync pos for gf_server"
    parser = argparse.ArgumentParser(description=description)

    _file_name = "C:\\Users\\Administrator\\Desktop\\gf_batandconfig\\gf_tool_setting.json"
    _date = datetime.now().strftime("%Y%m%d")
    parser.add_argument('-m', '--config_filename', dest='config_filename', type=str, default=_file_name)
    parser.add_argument('-p', '--date_change', dest='date_change', type=str2bool, default='T')
    end_time = "15:30"
    args = parser.parse_args()
    print (f"(args){args}")

    td = GfTool(args.config_filename, args.date_change, end_time, GATEWAY_NAME)

    td.start()