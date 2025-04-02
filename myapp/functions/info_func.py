import requests
import time

def get_subject_content(subject_id: int):
    """
    在此使用bgm api 获取条目的数据
    :param subject_id: 条目id
    :return:带有各项数据的字典
    """
    s = time.time()
    url = f'https://api.bgm.tv/v0/subjects/{subject_id}'


    headers = {
        "Authorization": "Bearer OSjDnIB7tooPNrlJn9WSmWHgPbuVrTzGWVnOcZGD",
        "User-Agent": 'asaceed/tracker'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {'success':True,'data':data}
    else:
        return {'success':False,'code':response.status_code}


