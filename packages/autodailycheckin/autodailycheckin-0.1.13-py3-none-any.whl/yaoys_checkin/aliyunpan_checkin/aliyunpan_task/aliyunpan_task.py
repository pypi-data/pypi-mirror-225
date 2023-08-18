# -*- coding: utf-8 -*-
# @FileName  :album_task.py
# @Time      :2023/8/7 21:51
# @Author    :yaoys
# @Desc      : 阿里云盘相册相关的任务
import datetime
import os
import random
import re
import time
from urllib.parse import urlparse
import m3u8
import requests
from PIL import Image

# 上传文件名前缀
file_name_prex = '阿里云盘上传文件_'
# 上传文件夹名称
folder_name = '阿里云盘签到任务文件夹'
video_folder_name = 'video'
# 上传图片相册
upload_photo_album_name = '阿里云盘签到任务相册'
# 阿里盘酱酱ID
alipanpanjiang_id = 'ec11691148db442aa7aa374ca707543c'
# 创建手工相册名前缀，格式为'阿里云盘签到任务创建相册_'+当前日期
create_album_name = '阿里云盘签到任务创建相册'

video_file_type = ["avi", "flv", "mp4", "MOV"]


# 由于每个账号中drive_name名称不一致，比如有的账号备份盘drive_name叫做‘backup’，有的叫做Default，所以优先使用category进行匹配，如果category为空则使用drive_name
def get_user_drive_id(aligo=None, drive_name=None, category=None):
    if aligo is None:
        return None, 'aligo 为空'

    list_drive = aligo.list_my_drives()
    for i in range(len(list_drive)):
        if list_drive[i].drive_name is None:
            continue
        #    category不是空，优先使用
        if category is not None and len(category) > 0:
            if list_drive[i].drive_type == 'normal' and list_drive[i].status == 'enabled' and list_drive[i].category == category:
                return list_drive[i].drive_id, ''
        # 匹配相册时，由于category为空，所以使用名字
        else:
            if list_drive[i].drive_type == 'normal' and list_drive[i].status == 'enabled' and list_drive[i].drive_name == drive_name:
                return list_drive[i].drive_id, ''

    return None, '没有找到相应的drive'


# 创建快传分享文件夹
def create_quick_pass(aligo=None, access_token=None):
    if aligo is None:
        return False, 'aligo 为空'

    if access_token is None:
        return False, 'access_token为空'
    #     获取阿里云盘签到任务文件夹的id
    # 创建文件夹前首先获取备份盘的drive_id
    backup_drive_id = get_user_drive_id(aligo=aligo, category='backup')
    if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
        return False, f'获取 备份盘ID失败'

    # 获取文件夹
    folder_id = get_folder_id(aligo=aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
    if folder_id is None:
        # 创建文件夹
        folder_id = my_create_folder(aligo=aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
        if folder_id is None:
            return False, f'没有获取到*{folder_name}*文件夹,并且创建该文件夹失败，请手动完成'

    data = requests.post(url='https://api.aliyundrive.com/adrive/v1/share/create', headers={
        'Authorization': f'Bearer {access_token}'},
                         json={"drive_file_list": [{"drive_id": backup_drive_id[0], "file_id": folder_id}]}).json()

    if 'share_id' in data:
        return True, '创建快传分享成功'
    elif 'display_message' in data and 'code' in data and data['code'] == 'CreateShareCountExceed':
        return True, data['display_message']
    else:
        return False, '创建快传失败，发生未知错误'


# 通过手机播放视频
def play_video_by_mobile(aligo=None, access_token=None):
    if aligo is None:
        return False, 'aligo 为空'

    if access_token is None:
        return False, 'access_token为空'
        # 首先获取备份盘的drive_id
    backup_drive_id = get_user_drive_id(aligo=aligo, category='backup')
    if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
        return False, f'获取备份盘ID失败'

    # 获取文件夹下的视频
    folder_id = get_folder_id(aligo=aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
    if folder_id is None:
        return False, f'没有获取到*{folder_name}*文件夹'
    #  获取该文件夹下所有文件
    file_list = aligo.get_file_list(parent_file_id=folder_id, drive_id=backup_drive_id[0])
    if len(file_list) <= 0:
        return False, f'没有文件，请先上传多个大于30秒的视频至*{folder_name}*文件夹'

    file_id = None
    # 视频文件ID数组，便后后续随机选择视频播放
    file_id_list = list()
    for i in range(len(file_list)):
        if file_list[i].type is None or file_list[i].name is None:
            continue
        if file_list[i].type == 'file' and str(file_list[i].name).split('.')[1] in video_file_type:
            file_id = file_list[i].file_id
            file_id_list.append(file_id)

    if len(file_id_list) <= 0:
        return False, f'没有视频文件，请先上传多个大于30秒的视频至*{folder_name}*文件夹'

    # 随机选择视频
    file_id = random.choice(file_id_list)

    # 获取视频信息
    video_preview_play_info = aligo.get_video_preview_play_info(file_id=file_id, drive_id=backup_drive_id[0])
    # 获取播放总时长
    duration = video_preview_play_info.video_preview_play_info.meta.duration
    # 获取文件信息
    file_info = aligo.get_file(file_id=file_id, drive_id=backup_drive_id[0])
    # # 文件后缀
    file_extension = file_info.file_extension
    file_name = file_info.name

    # # 根据总时长划分每段请求的视频长度，以5为间隔
    # duration_list = numpy.arange(0, duration, 5, 'd')
    # count = 0
    # for i in range(len(list(duration_list))):
    #     if list(duration_list)[i] == 0:
    #         play_cursor = list(duration_list)[i] + round(random.random(), 6)
    #     else:
    #         play_cursor = list(duration_list)[i] + round(random.random(), 6)
    #     data = requests.post(
    #         'https://api.alipan.com/adrive/v2/video/update',
    #         headers={
    #             'Authorization': f'Bearer {access_token}'
    #         },
    #         json={
    #             "play_cursor": play_cursor,
    #             "file_extension": file_extension,
    #             "duration": duration,
    #             "name": file_name,
    #             "file_id": file_id,
    #             "drive_id": backup_drive_id[0]
    #         },
    #     )
    #     if data.status_code == 400:
    #         return False, data.text
    #     # 统计每个5秒间隔是不是全部播放
    #     if data.status_code == 200:
    #         count += 1
    #     # 以5为间隔休眠
    #     time.sleep(5)
    #
    # if count >= len(duration_list):
    #     return True, '使用手机播放视频30s完毕'
    # else:
    #     return False, '使用手机播放视频30s失败'

    # 设置播放多长时间，在手机上每次暂停会调用该请求记录当前播放位置，所以一次性播放30秒，当大于35秒时，选择35秒视频，否则选择全部时长
    if duration > 35:
        play_cursor = 35 + round(random.random(), 6)
    else:
        play_cursor = duration + round(random.random(), 6)
    data = requests.post(
        'https://api.alipan.com/adrive/v2/video/update',
        headers={
            'Authorization': f'Bearer {access_token}'
        },
        json={
            "play_cursor": play_cursor,
            "file_extension": file_extension,
            "duration": duration,
            "name": file_name,
            "file_id": file_id,
            "drive_id": backup_drive_id[0]
        },
    )
    if data.status_code == 400:
        return False, data.text
    # 是不是全部播放
    if data.status_code == 200:
        time.sleep(play_cursor)
        return True, '使用手机播放视频30s完毕'
    else:
        return False, '使用手机播放视频30s失败'


# 暂时不使用，使用Windows播放视频和使用手机一样，Windows会获取m3u8，但是实际上还是要使用手机的api更新播放进度，单纯请求m3u8没办法完成播放视频任务
def play_video_by_windows(aligo=None, access_token=None):
    if aligo is None:
        return False, 'aligo 为空'

    if access_token is None:
        return 'access_token为空', False
    # 首先获取备份盘的drive_id
    backup_drive_id = get_user_drive_id(aligo=aligo, category='backup')
    if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
        return False, f'获取备份盘ID失败'
    # 获取文件夹下的视频
    folder_id = get_folder_id(aligo=aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
    if folder_id is None:
        return False, f'没有获取到*{folder_name}*文件夹'
    #  获取该文件夹下所有文件
    file_list = aligo.get_file_list(parent_file_id=folder_id, drive_id=backup_drive_id[0])
    if len(file_list) <= 0:
        return False, f'没有视频文件，请先上传多个大于30秒的视频至*{folder_name}*文件夹'

    file_id = None
    # 视频文件ID数组，便后后续随机选择视频播放
    file_id_list = list()
    for i in range(len(file_list)):
        if file_list[i].type is None or file_list[i].name is None:
            continue
        if file_list[i].type == 'file' and str(file_list[i].name).split('.')[1] in video_file_type:
            file_id = file_list[i].file_id
            file_id_list.append(file_id)

    if len(file_id_list) <= 0:
        return False, f'没有视频文件，请先上传多个大于30秒的视频至*{folder_name}*文件夹'

    # 随机选择视频
    file_id = random.choice(file_id_list)

    # 获取文件信息
    file_info = aligo.get_file(file_id=file_id, drive_id=backup_drive_id[0])
    # # 文件后缀
    file_extension = file_info.file_extension
    file_name = file_info.name

    # 获取m3u8地址，然后分别请求每个m3u8,使用可以使用的清晰度
    video_preview_play_info_response = aligo.get_video_preview_play_info(file_id=file_id, drive_id=backup_drive_id[0])
    # 获取播放时长
    duration = video_preview_play_info_response.video_preview_play_info.meta.duration
    # 获取所有的清晰度
    live_transcoding_task_list = video_preview_play_info_response.video_preview_play_info.live_transcoding_task_list
    if len(live_transcoding_task_list) <= 0:
        return False, '没有可用的清晰度'
    # 遍历得到可以用的清晰度
    m3u8_url = None
    for i in range(len(live_transcoding_task_list)):
        if live_transcoding_task_list[i].status == "finished":
            m3u8_url = live_transcoding_task_list[i].url
            break

    if m3u8_url is None:
        return False, '没有解析出m3u8地址'
    # 解析host
    url_parse = urlparse(url=m3u8_url)
    if url_parse is None or url_parse.hostname is None or len(url_parse.hostname) <= 0:
        return False, '没有解析出host地址'
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Host': url_parse.hostname,
        'Origin': 'https://www.aliyundrive.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.aliyundrive.com/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    # 解析m3u8
    play_list = m3u8.load(m3u8_url, headers=header, verify_ssl=False)
    count = 0
    # 请求m3u8，请求的时长不超过35秒
    for index, segment in enumerate(play_list.segments):
        # ur = segment.uri
        duration = segment.duration
        absolute_uri = segment.absolute_uri
        requests.get(absolute_uri, headers=header, verify=False)

    time.sleep(3)
    if duration > 35:
        play_cursor = 35 + round(random.random(), 6)
    else:
        play_cursor = duration + round(random.random(), 6)
    # 请求最多35秒的视频
    data = requests.post(
        'https://api.alipan.com/adrive/v2/video/update',
        headers={
            'Authorization': f'Bearer {access_token}'
        },
        json={
            "play_cursor": play_cursor,
            "file_extension": file_extension,
            "duration": duration,
            "name": file_name,
            "file_id": file_id,
            "drive_id": backup_drive_id[0]
        },
    )
    if data.status_code == 400:
        return False, data.text
    # 统计是不是全部播放
    if data.status_code == 200:
        time.sleep(play_cursor)
        return True, '使用Windows播放视频30s完毕'
    else:
        return False, '使用Windows播放视频30s失败'


def follow_user(user_id=None, session=None, access_token=None, time_sleep=0):
    if access_token is None:
        return 'access_token为空', False
    if session is None:
        return 'session为空', False
    if user_id is None:
        user_id = alipanpanjiang_id
    try:
        resp = session.post('https://api.aliyundrive.com/adrive/v1/member/follow_user',
                            headers={
                                'Authorization': f'Bearer {access_token}'
                            },
                            body={
                                'user_id': user_id
                            })
        if resp.status_code == 200:
            return '订阅成功', True
    except Exception as e:
        return '订阅阿里盘酱酱出现异常，请手动尝试', False


# 捞好运瓶任务
def get_lucky_bittle(access_token=None, session=None, time_sleep=0):
    if access_token is None:
        return 'access_token为空', False
    if session is None:
        return 'session为空', False

    #     获取当前次数
    # {
    # 创建好运瓶限制
    # 	"createBottleLimit": 100,
    # 已使用好运瓶限制
    # 	"createBottleUsed": 0,
    # 捞取总数
    # 	"fishBottleLimit": 3,
    # 已经捞取数
    # 	"fishBottleUsed": 1
    # }
    try:
        resp = session.post('https://api.alipan.com/adrive/v1/bottle/getUserLimit',
                            headers={
                                'Authorization': f'Bearer {access_token}'
                            },
                            json={}).json()
        if 'fishBottleUsed' in resp and 'fishBottleLimit' in resp:
            fishBottleLimit = resp['fishBottleLimit']
            fishBottleUsed = resp['fishBottleUsed']
            for i in range(3):
                resp = session.post('https://api.alipan.com/adrive/v1/bottle/fish',
                                    headers={
                                        'Authorization': f'Bearer {access_token}'
                                    },
                                    json={})
                if resp.status_code == 200:
                    fishBottleUsed += 1

            if fishBottleUsed == 3:
                return f'已经成功捞取3次好运瓶', True
            else:
                return f'已经捞取{fishBottleUsed}次好运瓶,还需要手动捞取{3 - fishBottleUsed}次可领取奖励', False
    except Exception as e:
        return f'捞取好运瓶出现异常，请手动尝试', False


# 创建文件夹
def my_create_folder(aligo=None, _folder_name=None, time_sleep=0, drive_id=None, drive_name=None, category=None):
    if aligo is None:
        return None
    if _folder_name is None:
        _folder_name = folder_name

    if drive_id is None or len(drive_id) <= 0:
        # 首先获取备份盘的drive_id
        backup_drive_id = get_user_drive_id(aligo=aligo, drive_name=drive_name, category=category)
        if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
            return None
        else:
            drive_id = backup_drive_id[0]
    folder_id = None
    response = aligo.create_folder(name=_folder_name, check_name_mode='refuse', drive_id=drive_id)
    if response is not None:
        folder_id = response.file_id
    else:
        return None

    return folder_id


# 获取文件夹id根据名称
def get_folder_id(aligo=None, _folder_name=None, time_sleep=0, drive_id=None):
    if aligo is None:
        return None

    if drive_id is None:
        return None

    if _folder_name is None:
        _folder_name = folder_name

    folder_id = None
    # 获取备份盘下所有的文件夹，寻找默认名称为阿里云盘签到任务文件夹
    file_list = aligo.get_file_list(drive_id=drive_id)
    for i in range(len(file_list)):
        if file_list[i].type is None or file_list[i].name is None:
            continue
        if file_list[i].type == 'folder' and file_list[i].name == _folder_name:
            folder_id = file_list[i].file_id
            break

    return folder_id


# 删除上次创建的相册，
def delete_lastTime_album(aligo=None):
    if aligo is None:
        return False, 'aligo 为空'

    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    album_list = aligo.list_albums()
    if len(album_list) <= 0:
        return True, ''

    for i in range(len(album_list)):
        if album_list[i].type is None or album_list[i].name is None:
            continue
        if 'manual' == album_list[i].type and album_list[i].name == create_album_name:
            aligo.delete_album(album_list[i].album_id)
            break

    return True, ''


# 创建手工相册，也可以创建上传图片任务相册，根据type确定,album_type=0:创建上传图片任务相册，album_type=1：创建手工相册
def create_album(aligo=None, album_name=None, path=None, time_sleep=0, album_type=None):
    if aligo is None:
        return False, 'aligo 为空'

    if album_type is None:
        return False, 'album_type 为空'

    description = None
    if album_name is None:
        if album_type == 0:
            album_name = upload_photo_album_name
            description = upload_photo_album_name
        elif album_type == 1:
            album_name = create_album_name
            description = create_album_name
        else:
            return False, 'album_type 只能为0或者1'
    response = aligo.create_album(name=album_name, description=description)

    if response is not None:
        return response.album_id, True
    else:
        return None, False


# 此方法会删除 阿里云盘签到任务文件夹  下的所有文件
def delete_file(aligo=None, _folder_name=None, time_sleep=0):
    if aligo is None:
        return 'aligo 为空', False
    if _folder_name is None:
        _folder_name = folder_name

    try:
        #     获取 备份盘下 '阿里云盘签到任务文件夹'的ID
        # 首先获取备份盘的drive_id
        backup_drive_id = get_user_drive_id(aligo=aligo, category='backup')
        if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
            return f'获取 备份盘ID失败,无法删除文件,请手动删除', False

        folder_id = get_folder_id(aligo, _folder_name=_folder_name, drive_id=backup_drive_id[0])
        if folder_id is None:
            return f'获取 *{_folder_name}* 文件夹失败,无法删除文件,请手动删除', True
        else:
            #  获取该文件夹下所有文件
            file_list = aligo.get_file_list(parent_file_id=folder_id, drive_id=backup_drive_id[0])
            if len(file_list) <= 0:
                return '', True

            for i in range(len(file_list)):
                if file_list[i].type is None or file_list[i].name is None or file_list[i].mime_extension is None:
                    continue
                #     不删除视频文件
                elif file_list[i].category == 'video' and (file_list[i].type == 'file' and file_list[i].mime_extension in video_file_type):
                    continue
                else:
                    aligo.move_file_to_trash(file_id=file_list[i].file_id, drive_id=backup_drive_id[0])

            return '文件删除成功', True
    except Exception as e:
        raise Exception('删除文件:' + str(e))


# 删除该相册下的所有文件
def delete_photo_from_album(aligo=None, album_id=None, time_sleep=0):
    if aligo is None:
        return 'aligo 为空', False

    try:
        # 获取相册id
        album_list = aligo.list_albums()
        if len(album_list) <= 0:
            return '', True

        for i in range(len(album_list)):
            if album_list[i].type is None or album_list[i].name is None:
                continue

            if 'manual' == album_list[i].type and album_list[i].name == upload_photo_album_name:
                album_id = album_list[i].album_id
                break
        if album_id is None:
            return f'找不到名为 {upload_photo_album_name} 的相册', True
        # 获取相册图片
        photo_list = aligo.list_album_files(album_id)
        if len(photo_list) <= 0:
            return '相册中图片为空', True

        # 获取相册drive的id
        album_drive_id = get_user_drive_id(aligo=aligo, drive_name='alibum')
        if album_drive_id is None or len(album_drive_id) != 2:
            return '没有获取到相册drive的id', False, None

        for i in range(len(photo_list)):
            # batch_photo_id.append(response[i].file_id)
            aligo.move_file_to_trash(file_id=photo_list[i].file_id, drive_id=album_drive_id[0])

        return '删除照片成功', True
    except Exception as e:
        return '删除照片异常:' + str(e), False


# 上传10张照片,首先判断相册是否存在，相册不存在先创建相册，再上传图片并删除本地图片
def upload_photo(aligo=None, path=None, time_sleep=0):
    if aligo is None:
        return 'aligo 为空', False, None

    if path is None:
        return 'path 为空', False, None

    try:
        # 本地文件夹不存在，则创建
        if os.path.exists(path) is False:
            os.makedirs(path)
        #     获取相册列表
        list_albums = aligo.list_albums()
        albums_id = None
        for i in range(len(list_albums)):
            if list_albums[i].type is None or list_albums[i].name is None:
                continue
            if 'manual' == list_albums[i].type and list_albums[i].name == upload_photo_album_name:
                albums_id = list_albums[i].album_id
                break

        # 相册不存在，创建相册
        if albums_id is None:
            albums_id, is_success = create_album(aligo, album_type=0)
            if albums_id is None or is_success is False:
                return '创建相册失败,请手动完成该任务', False, None

        # # 获取所有的文件夹，寻找默认名称为阿里云盘签到任务文件夹
        # folder_id = get_folder_id(aligo, _folder_name=folder_name)
        # # auto_rename 自动重命名，存在并发问题
        # # refuse 同名不创建，直接返回已经存在的
        # # ignore 同名文件可创建
        # # 不存在则创建文件夹
        # if folder_id is None:
        #     folder_id = my_create_folder(aligo, _folder_name=folder_name)
        #     if folder_id is None:
        #         return '上传图片时创建文件夹失败', False, None

        #     生成10个图片，并上传，上传完毕后删除本地图片
        #     从本地添加需要先上传到相册，然后再移动到指定的相薄中
        success_count = 0
        # 获取相册drive的id
        album_drive_id = get_user_drive_id(aligo=aligo, drive_name='alibum')
        if album_drive_id is None or len(album_drive_id) != 2 or album_drive_id[0] is None:
            return '没有获取到相册drive的id', False, None

        # 生成10个图片并上传，上传成功后删除本地图片
        for i in range(10):
            im = Image.new('RGB', (200, 200), color="red")
            file_name = f'{str(int(round(time.time() * 1000))) + "_" + str(i + 1)}.jpg'
            im.save(f'{path + "/" + file_name}')
            # 先上传到默认的相册薄中，此时并未指定相册
            f = aligo.upload_file(f'{path + "/" + file_name}', parent_file_id='root', drive_id=album_drive_id[0])
            # 移动相片到指定的相薄
            result = aligo.add_files_to_album(files=[f], album_id=albums_id)
            # 上传成功后删除本地文件
            if result is not None:
                os.remove(path + "/" + file_name)
                success_count += 1

        if success_count == 10:
            return '', True, albums_id
        else:
            return '上传照片失败,请手动完成该任务', False, None

    except Exception as e:
        return '上传照片失败,请手动完成该任务', False, None


# 上传10个文件，首先创建一个文件夹，上传到指定的文件夹,首先判断文件夹是否存在，不存在则创建，如果存在则上传文件
def upload_file(aligo=None, path=None, time_sleep=0):
    if aligo is None:
        return False, 'aligo 为空'

    if path is None:
        return 'path 为空', False
    try:
        # 本地文件夹不存在，则创建
        if os.path.exists(path) is False:
            os.makedirs(path)
        # 获取所有的文件夹，寻找默认名称为阿里云盘签到任务文件夹
        # 首先获取备份盘的drive_id
        backup_drive_id = get_user_drive_id(aligo=aligo, category='backup')
        if backup_drive_id is None or len(backup_drive_id) != 2 or backup_drive_id[0] is None:
            return f'获取 备份盘ID失败', False

        folder_id = get_folder_id(aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
        # auto_rename 自动重命名，存在并发问题
        # refuse 同名不创建，直接返回已经存在的
        # ignore 同名文件可创建
        # 不存在创建文件夹
        if folder_id is None:
            folder_id = my_create_folder(aligo, _folder_name=folder_name, drive_id=backup_drive_id[0])
            if folder_id is None:
                return '上传文件时创建文件夹失败', False

        # 生成10个文件，并上传到该文件夹，然后删除文件
        success_count = 0

        for i in range(10):
            file_name = f'{str(int(round(time.time() * 1000))) + "_" + str(i + 1)}.txt'
            with open(path + '/' + file_name, encoding='utf-8', mode='w') as f:
                f.write(f'{str(int(round(time.time() * 1000))) + "_" + str(i + 1)}.txt')
            # 上传文件
            result = aligo.upload_files(file_paths=[path + '/' + file_name], parent_file_id=folder_id, drive_id=backup_drive_id[0])
            # 上传成功后删除文件
            if result is not None:
                os.remove(path + '/' + file_name)
                success_count += 1

        if success_count == 10:
            return '', True
        else:
            return '上传文件失败,请手动完成该任务', False
    except Exception as e:
        return f'上传文件失败,请手动完成该任务,错误信息：{e}', False
