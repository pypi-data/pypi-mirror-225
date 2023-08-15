#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  aliplat.py
@Date    :  2021/06/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import json
import math
import os
import time
from xml.dom.minidom import parseString

import aigpy
import requests
from aigpy.progressHelper import ProgressTool
from tqdm import tqdm

from b2a.common import printErr
from b2a.platformImp import *

requests.packages.urllib3.disable_warnings()


class AliUploadLink(object):
    def __init__(self, jsonData, localFilePath, remoteFilePath):
        self.list = jsonData.get('part_info_list', [])
        self.fileId = jsonData.get('file_id')
        self.fileSize = aigpy.fileHelper.getSize(localFilePath)
        self.uploadId = jsonData.get('upload_id')
        self.needUpload = True
        self.localFilePath = localFilePath
        self.remoteFilePath = remoteFilePath

        if 'rapid_upload' in jsonData and jsonData['rapid_upload']:
            self.needUpload = False
        if 'exist' in jsonData and jsonData['exist']:
            self.needUpload = False


class AliKey(object):
    def __init__(self):
        super().__init__()
        self.chunkSize = 1024 * 1024 * 10
        self.driveId = ''
        self.refreshToken = ''
        self.headers = None
        self.pathIds = {'/': 'root'}

    def token_refresh(self, refresh_token: str = None):
        # url = 'https://websv.aliyundrive.com/token/refresh'
        # json = {"refresh_token": self.refresh_token}
        url = 'https://api.aliyundrive.com/token/refresh'
        json = {"refresh_token": refresh_token, 'grant_type': 'refresh_token'}
        # r = requests.post(url, json=json, access_token=False)
        r = requests.post(url,
                          json=json,
                          headers={'content-type': 'application/json;charset=UTF-8'},
                          verify=False)
        try:
            self._refresh_token = r.json()['refresh_token']
            self._refresh_token_expires = time.time() + r.json()['expires_in']
        except KeyError:
            raise InvalidRefreshToken
        return r.json()

    def login(self, refreshToken: str) -> bool:
        try:
            post_json = self.token_refresh(refreshToken)
            self.headers = {
                'authorization': post_json['access_token'],
                'content-type': 'application/json;charset=UTF-8'
            }
            self.driveId = post_json['default_drive_id']
            self.refreshToken = post_json['refresh_token']
            return True
        except Exception as e:
            return False

    def __getPathId__(self, remotePath: str):
        if len(remotePath) <= 0:
            remotePath = '/'
        if remotePath in self.pathIds:
            return self.pathIds[remotePath]

        parent = ''
        paths = remotePath.split('/')
        for item in paths:
            key = parent + '/' + item
            key = key.replace('//', '/')
            if key not in self.pathIds:
                res = self.list(parent)
                if len(res) <= 0:
                    return None
                if key not in self.pathIds:
                    return None
            parent = key

        return self.pathIds[remotePath]

    def __updatePathId__(self, path: str, sid: str):
        self.pathIds[path] = sid

    def list(self, remotePath: str, nextMarker: str = None) -> List[FileAttr]:
        remotePath = remotePath.rstrip('/')
        sid = self.__getPathId__(remotePath)
        if not sid:
            return []

        retry = 3
        while True:
            try:
                retry -= 1
                requests_data = {"drive_id": self.driveId, "parent_file_id": sid, 'marker': nextMarker, 'limit': 100}
                requests_post = requests.post('https://api.aliyundrive.com/adrive/v3/file/list',
                                            data=json.dumps(requests_data),
                                            headers=self.headers,
                                            verify=False).json()
                if 'items' not in requests_post:
                    if retry > 0:
                        time.sleep(1)
                        continue
                    printErr("获取目录文件列表失败：" + requests_post['code'])
                    return []
                
                ret = []
                for item in requests_post['items']:
                    obj = FileAttr()
                    obj.isfile = item['type'] != 'folder'
                    obj.name = item['name']
                    obj.path = remotePath + '/' + item['name']
                    obj.uid = item['file_id']
                    obj.size = item['size'] if 'size' in item else 0
                    if not obj.isfile:
                        self.__updatePathId__(obj.path, obj.uid)

                    ret.append(obj)

                next_marker = requests_post.get('next_marker')
                if next_marker and nextMarker != requests_post['next_marker']:
                    ret.extend(self.list(remotePath, next_marker))

                return ret
            except Exception as e:
                printErr("获取目录文件列表失败：" + str(e))
                return []

    def __mkdir__(self, folderName, parentFolderId='root') -> (bool, str):
        folderName = folderName.strip('/')
        try:
            requests_data = {
                "drive_id": self.driveId,
                "parent_file_id": parentFolderId,
                "name": folderName,
                "check_name_mode": "refuse",
                "type": "folder"
            }
            post_json = requests.post('https://api.aliyundrive.com/v2/file/create',
                                      data=json.dumps(requests_data),
                                      headers=self.headers,
                                      verify=False).json()
            return True, post_json.get('file_id')
        except Exception as e:
            printErr("新建远程目录失败：" + str(e))
            return False, ''

    def __formatRemotePath__(self, remotePath: str) -> str:
        remotePath = remotePath.rstrip('/')
        remotePath = remotePath.replace('//', '/')
        return remotePath

    def mkdirs(self, remotePath: str) -> bool:
        remotePath = remotePath.rstrip('/')
        if self.__getPathId__(remotePath):
            return True

        parent = ''
        paths = remotePath.split('/')
        for item in paths:
            key = parent + '/' + item
            key = key.replace('//', '/')
            if key not in self.pathIds:
                check, keyId = self.__mkdir__(item, self.pathIds[parent])
                if not check:
                    return False
                self.__updatePathId__(key, keyId)
            parent = key

        return True

    def uploadLink(self, localFilePath: str, remoteFilePath: str) -> AliUploadLink:
        filesize = os.path.getsize(localFilePath)
        filename = os.path.basename(localFilePath)
        hashcode = aigpy.file.getHash(localFilePath)
        if filesize <= 0:
            return None

        remotePath = aigpy.path.getDirName(remoteFilePath)
        remotePath = self.__formatRemotePath__(remotePath)
        if not self.mkdirs(remotePath):
            return None

        try:
            part_info_list = []
            for i in range(0, math.ceil(filesize / self.chunkSize)):
                part_info_list.append({'part_number': i + 1})

            requests_data = {
                "drive_id": self.driveId,
                "part_info_list": part_info_list,
                "parent_file_id": self.__getPathId__(remotePath),
                "name": filename,
                "type": "file",
                "check_name_mode": "refuse",
                "size": filesize,
                "content_hash": hashcode,
                "content_hash_name": 'sha1'
            }

            requests_post_json = requests.post('https://api.aliyundrive.com/v2/file/create',
                                               data=json.dumps(requests_data),
                                               headers=self.headers,
                                               verify=False).json()

            ret = AliUploadLink(requests_post_json, localFilePath, remoteFilePath)
            return ret
        except Exception as e:
            printErr("获取上传链接失败：" + str(e))
            return None

    def __getXmlValue__(self, xml_string, tag_name):
        DOMTree = parseString(xml_string)
        DOMTree = DOMTree.documentElement
        tag = DOMTree.getElementsByTagName(tag_name)
        if len(tag) > 0:
            for node in tag[0].childNodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data
        return False

    def __uploadParts__(self, data, url, headers):
        retTry = 3
        msg = ''
        while retTry > 0:
            retTry -= 1
            try:
                res = requests.put(url=url,
                                   data=data,
                                   headers=headers,
                                   verify=False,
                                   timeout=None)
                if 400 <= res.status_code < 600:
                    # message = self.__getXmlValue__(res.text, 'Message')
                    # if message == 'Request has expired.':
                    #     part_upload_url_list = self.__getUploadUrl__(file_id, filesize, upload_id)
                    #     if part_upload_url_list == '':
                    #         return False
                    #     continue
                    code = self.__getXmlValue__(res.text, 'Code')
                    if code == 'PartAlreadyExist':
                        pass
                    else:
                        res.raise_for_status()
                        return False
                return True
            except Exception as e:
                msg = str(e)

        printErr('上传文件块失败：' + msg)
        return False

    def __uploadComplete__(self, fileId, uploadId):
        complete_data = {"drive_id": self.driveId,
                         "file_id": fileId,
                         "upload_id": uploadId
                         }
        requests_post_json = requests.post('https://api.aliyundrive.com/v2/file/complete',
                                           json.dumps(complete_data),
                                           headers=self.headers,
                                           verify=False).json()
        if 'file_id' in requests_post_json:
            return True
        return False

    def uploadFile(self, link: AliUploadLink) -> bool:
        if not link:
            return False
        if not link.needUpload:
            return True

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73",
            "Connection": "Keep-Alive",
            "Referer": "https://www.aliyundrive.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
        }

        totalSize = os.path.getsize(link.localFilePath)
        progress = tqdm(total=totalSize, desc="上传中", unit_scale=True)

        index = 0
        curcount = 0
        check = False

        with open(link.localFilePath, 'rb') as f:
            while True:
                chunk = f.read(self.chunkSize)
                check = self.__uploadParts__(chunk, link.list[index]['upload_url'], headers)
                if not check:
                    break
                progress.update(len(chunk))
                curcount += len(chunk)
                index += 1
                if curcount >= totalSize:
                    break
                if index >= len(link.list):
                    printErr(f"上传文件失败：list index{index} out of range{len(link.list)}")
                    check = False
                    break
        progress.close()

        if not check:
            return False

        return self.__uploadComplete__(link.fileId, link.uploadId)


class CheckFileExistCache(object):
    def __init__(self):
        self.fileMap = {}
        self.path = ''

    def setMap(self, path: str, fileAttrs: [FileAttr]):
        self.fileMap = {}
        for item in fileAttrs:
            if item.isfile:
                self.fileMap[item.name] = item
        self.path = path

    def getItem(self, name):
        if name in self.fileMap:
            return self.fileMap[name]
        return None


class AliPlat(PlatformImp):
    def __init__(self):
        super().__init__()
        self.name = '阿里'
        self.checkFileExistCache = CheckFileExistCache()

    def list(self, remotePath: str, includeSubDir: bool = False) -> List[FileAttr]:
        array = []
        res = self.key.list(remotePath)
        for item in res:
            array.append(item)
            if includeSubDir and not item.isfile:
                subarr = self.list(item.path, includeSubDir)
                array.extend(subarr)
        return array

    def downloadFile(self, fileAttr: FileAttr, localFilePath: str) -> bool:
        return False

    def uploadFile(self, localFilePath: str, remoteFilePath: str) -> bool:
        link = self.key.uploadLink(localFilePath, remoteFilePath)
        if not link:
            return False
        check = self.key.uploadFile(link)
        return check

    def downloadLink(self, remoteFilePath: str):
        return None

    def uploadLink(self, localFilePath: str, remoteFilePath: str):
        link = self.key.uploadLink(localFilePath, remoteFilePath)
        return link

    def isFileExist(self, remoteFilePath: str) -> bool:
        path = aigpy.path.getDirName(remoteFilePath)
        name = aigpy.path.getFileName(remoteFilePath)

        if path != self.checkFileExistCache.path:
            array = self.key.list(path)
            self.checkFileExistCache.setMap(path, array)

        return self.checkFileExistCache.getItem(name) is not None
