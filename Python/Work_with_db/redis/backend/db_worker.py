import json

from datetime import datetime
from typing import Union
import redis


def int_dt_to_str(date_int):
    timestamp = datetime.fromtimestamp(date_int)
    return timestamp.strftime('%d.%m.%Y %H:%M:%S')


class UserWorker:
    def __init__(self, redis_host='localhost', redis_port: int = 6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.table_name = "user:"

    def add(self, uid, user_data: dict, update: bool = False):
        if update:
            if self.get(uid=uid):
                self.redis.set(name=self.table_name + str(uid), value=json.dumps(user_data))
        else:
            if self.get(uid=uid) is None:
                self.redis.set(name=self.table_name + str(uid), value=json.dumps(user_data))

    def get(self, uid: int = None) -> Union[dict, list]:
        if uid:
            return json.loads(self.redis.get(self.table_name + str(uid))) if self.redis.get(
                self.table_name + str(uid)) else None
        else:
            keys = self.redis.keys(self.table_name + "*")
            return [json.loads(val) for val in self.redis.mget(keys)]

    def update(self, uid: int, data: dict = None, sub_id: int = None, phone: int = None, append: bool = False):
        upd_user = self.get(uid)
        if data:
            if append:
                for k, v in data.items():
                    if k in upd_user['data']:
                        upd_user['data'][k].append(v)
                    else:
                        upd_user['data'][k] = [v]
            else:
                upd_user['data'].update(data)
        if sub_id:
            upd_user['sub_id'] = sub_id
        if phone:
            upd_user['phone'] = phone
        self.add(uid, upd_user, update=True)

    def delete(self, uid):
        self.redis.delete(self.table_name + str(uid))
