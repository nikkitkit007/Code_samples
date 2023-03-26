from db_worker import UserWorker

user_worker = UserWorker()


def start():
    uid = 1
    user_data = {'data': {'lvl': 'start'}, 'phone': -1, 'sub_id': -1}
    user_worker.add(uid, user_data=user_data)
    print(user_worker.get(uid=uid))
    user_worker.update(uid, {'lvl': 'finish'})
    print(user_worker.get(uid=uid))
    user_worker.delete(uid=uid)


if __name__ == '__main__':
    start()
