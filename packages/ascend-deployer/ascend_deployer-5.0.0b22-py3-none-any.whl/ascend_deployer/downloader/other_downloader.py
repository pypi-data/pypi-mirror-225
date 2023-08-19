#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================

import json
import os
import time
from .download_util import calc_sha256, get_arch, get_specified_python, \
    DOWNLOAD_INST, CH, DownloadCheckError
from . import logger_config
from .software_mgr import get_software_name_version, get_software_other, get_software_framework

LOG = logger_config.LOG
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(CUR_DIR)


def download_software(software, dst, arch):
    """
    下载软件的其他资源
    """
    formal_name, version = get_software_name_version(software)
    others = get_software_other(formal_name, version)
    for item in others:
        filename = item.get("filename", "")
        if (
                "MindStudio" in filename
                and ("x86_64" in filename or "aarch64" in filename)
                and isinstance(arch, str)
                and arch not in filename
        ):
            others.remove(item)
            break
    download_dir = os.path.join(dst, "resources", "{0}_{1}".format(formal_name, version))
    if "DL" not in download_dir and "MEF" not in download_dir:
        if not os.path.exists(download_dir):
            os.makedirs(download_dir, mode=0o750, exist_ok=True)
        LOG.info('item:{} save dir: {}'.format(software, os.path.basename(download_dir)))
    results = []
    if formal_name == "CANN":
        if arch == "x86_64" or arch == "aarch64":
            others = (
                item
                for item in others
                if arch in item["filename"].replace("-", "_")
                   or "kernels" in item["filename"]
            )
        try:
            for item in others:
                if item.get("dest", None):
                    dest_file = os.path.join(dst, item.get('dest'), item.get('filename'))
                else:
                    dest_file = os.path.join(download_dir, item['filename'])
                if os.path.exists(dest_file) and 'sha256' in item:
                    file_hash = calc_sha256(dest_file)
                    if file_hash == item['sha256']:
                        print(item['filename'].ljust(60), 'exists')
                        LOG.info('{0} no need download again'.format(item['filename']))
                        continue
                ret = DOWNLOAD_INST.download(item['url'], dest_file)
                if ret:
                    if 'sha256' in item and not CH.check_hash(dest_file, item['sha256']):
                        LOG.info('the downloaded file：{} hash is not equal to the hash in file'.format(dest_file))
                        raise DownloadCheckError(dest_file)
                    print(item['filename'].ljust(60), 'download success')
                results.append(ret)
        finally:
            while '.part' in ','.join(os.listdir(download_dir)):
                time.sleep(1)
    else:
        for item in others:
            dest_file = os.path.join(download_dir, item['filename'])
            if os.path.exists(dest_file) and 'sha256' in item:
                file_hash = calc_sha256(dest_file)
                if file_hash == item['sha256']:
                    print(item['filename'].ljust(60), 'exists')
                    LOG.info('{0} no need download again'.format(item['filename']))
                    continue
            ret = DOWNLOAD_INST.download(item['url'], dest_file)
            if ret:
                if 'sha256' in item and not CH.check_hash(dest_file, item['sha256']):
                    LOG.info('the downloaded file：{} hash is not equal to the hash in file'.format(dest_file))
                    raise DownloadCheckError(dest_file)
                print(item['filename'].ljust(60), 'download success')
            results.append(ret)
    return all(results)


def download(os_list, software_list, dst):
    """
    按软件列表下载其他部分
    """
    if os_list is None:
        os_list = []
    arch = get_arch(os_list)
    LOG.info('software arch is {0}'.format(arch))

    results = {'ok': [], 'failed': []}
    no_frame_list = []
    for software in software_list:
        if "MindSpore" not in software and "Torch-npu" not in software and "TensorFlow" not in software:
            no_frame_list.append(software)
    for software in no_frame_list:
        res = download_software(software, dst, arch)
        if res:
            results.get('ok', []).append(software)
            continue
        results.get('failed', []).append(software)
    return results


def download_other_packages(os_list, dst=None):
    """
    download_other_packages

    :return:
    """
    if dst is None:
        base_dir = PROJECT_DIR
    else:
        base_dir = dst
    arch = get_arch(os_list)
    resources_json = os.path.join(CUR_DIR, 'other_resources.json')
    results = {'ok': [], 'failed': []}
    with open(resources_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            dest_file = os.path.join(base_dir, item['dest'], item['filename'])
            if os.path.exists(dest_file) and 'sha256' in item:
                file_hash = calc_sha256(dest_file)
                url_hash = item['sha256']
                if file_hash == url_hash:
                    print(item['filename'].ljust(60), 'exists')
                    LOG.info('{0} no need download again'.format(item['filename']))
                    continue
            if 'nexus' in item['filename']:
                if arch == "x86_64" and arch not in item['filename']:
                    continue
                if arch == "aarch64" and arch not in item['filename']:
                    continue
            LOG.info('download[{0}] -> [{1}]'.format(item['url'], os.path.basename(dest_file)))
            if DOWNLOAD_INST.download(item['url'], dest_file):
                if not CH.check_hash(dest_file, item['sha256']):
                    results.get('failed', []).append(item['filename'])
                    raise DownloadCheckError(dest_file)
                else:
                    results.get('ok', []).append(item['filename'])
                    print(item['filename'].ljust(60), 'download success')
                    continue
            results.get('failed', []).append(item['filename'])
    return results


def download_specified_python(dst=None):
    """
    download ascend_python_version=Python-3.7.5

    :return:
    """
    if dst is None:
        base_dir = PROJECT_DIR
    else:
        base_dir = dst
    specified_python = get_specified_python()
    resources_json = os.path.join(CUR_DIR, 'python_version.json')
    with open(resources_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        results = {'ok': [], 'failed': []}
        for item in data:
            if specified_python == item['filename'].rstrip('.tar.xz'):
                dest_file = os.path.join(base_dir, item['dest'], item['filename'])
                if os.path.exists(dest_file) and 'sha256' in item:
                    file_hash = calc_sha256(dest_file)
                    url_hash = item['sha256']
                    if file_hash == url_hash:
                        print(item['filename'].ljust(60), 'exists')
                        LOG.info('{0} no need download again'.format(item['filename']))
                        break
                LOG.info('download[{0}] -> [{1}]'.format(item['url'], os.path.basename(dest_file)))
                if DOWNLOAD_INST.download(item['url'], dest_file):
                    if not CH.check_hash(dest_file, item['sha256']):
                        results.get('failed', []).append(item['filename'])
                        raise DownloadCheckError(dest_file)
                    else:
                        results.get('ok', []).append(item['filename'])
                        print(item['filename'].ljust(60), 'download success')
                        break
                results.get('failed', []).append(item['filename'])
                break
        return results


def download_framework_whl(os_item, software, dst):
    """
    下载框架whl包
    """
    formal_name, version = get_software_name_version(software)
    download_dir = os.path.join(dst, "resources")
    results = []
    os_item_split = os_item.split("_")
    os_name, arch = "_".join(os_item_split[:2]), "_".join(os_item_split[2:])
    specified_python = get_specified_python()
    implement_flag = "cp37"
    if "Python-3.7" in specified_python:
        implement_flag = "cp37"
    if "Python-3.8" in specified_python:
        implement_flag = "cp38"
    if "Python-3.9" in specified_python:
        implement_flag = "cp39"
    whl_list = get_software_framework(formal_name, "linux_{}".format(arch), version)
    for item in whl_list:
        if item.get('python', 'cp37') != implement_flag:
            print("Try to get {} on {}, but it does not match {}".format
                  (item['filename'], item.get('python'), implement_flag))
            continue
        dest_file = os.path.join(download_dir, item['dest'],os.path.basename(item['url']))
        if os.path.exists(dest_file) and 'sha256' in item:
            file_hash = calc_sha256(dest_file)
            url_hash = item['sha256']
            if file_hash == url_hash:
                print(item['filename'].ljust(60), 'exists')
                LOG.info('{0} no need download again'.format(item['filename']))
                continue
            else:
                LOG.info('{0} need download again'.format(item['filename']))
        ret = DOWNLOAD_INST.download(item['url'], dest_file)
        if ret:
            if 'sha256' in item and not CH.check_hash(dest_file, item['sha256']):
                LOG.info('the downloaded file：{} hash is not equal to the hash in file'.format(dest_file))
                raise DownloadCheckError(dest_file)
            print(item['filename'].ljust(60), 'download success')
        results.append(ret)

    return all(results)


def download_ai_framework(os_list, software_list, dst):
    """
    按传参下载AI框架
    """
    results = {'ok': [], 'failed': []}
    framework_list = [software for software in software_list if
                      "MindSpore" in software or "Torch-npu" in software or "TensorFlow" in software]
    for os_item in os_list:
        for framework in framework_list:
            res = download_framework_whl(os_item, framework, dst)
            if res:
                results.get('ok', []).append(framework)
                continue
            results.get('failed', []).append(framework)
    return results
