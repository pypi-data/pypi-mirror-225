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
from . import logger_config
from .download_util import get_download_path, calc_sha256, DOWNLOAD_INST, CH, DownloadCheckError, get_name_version

LOG = logger_config.LOG


class DLDownloadError(Exception):
    def __init__(self, err_os_list):
        self.err_os_list = err_os_list


def download_dl_mef_dependency(os_list, software_list, dst):
    """
    download_dl_dependency
    return:download result dict
    """
    download_dl = any("DL" in pkg_name for pkg_name in software_list)
    download_mef = any("MEF" in pkg_name for pkg_name in software_list)
    download_aarch64 = any("aarch64" in os_item for os_item in os_list)
    download_x86_64 = any("x86_64" in os_item for os_item in os_list)

    software_with_version_list = [get_name_version(item, std_out=False) for item in software_list]
    version = next((pkg_name.split("_")[1]
                    for pkg_name in software_with_version_list
                    if "DL" in pkg_name or "MEF" in pkg_name), "")
    project_dir = get_download_path()
    results = {'ok': [], 'failed': []}
    # download common resource
    for os_item in os_list:
        resources_json = os.path.join(project_dir, f'downloader/dependency/{version}/COMMON/{os_item}/resource.json')
        download_from_json(dst, resources_json, results)
    # download dl and mef resource if necessary
    for arch, is_download in (('aarch64', download_aarch64), ('x86_64', download_x86_64)):
        if not is_download:
            continue
        else:
            if download_dl:
                resources_json = os.path.join(project_dir, f'downloader/dependency/{version}/DL/{arch}/resource.json')
                download_from_json(dst, resources_json, results)
            if download_mef:
                resources_json = os.path.join(project_dir, f'downloader/dependency/{version}/MEF/{arch}/resource.json')
                download_from_json(dst, resources_json, results)
    return results


def download_from_json(dst, resources_json, results):
    with open(resources_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            dest_file = os.path.join(dst, item['dest'], item['filename'])
            if os.path.exists(dest_file) and 'sha256' in item:
                file_hash = calc_sha256(dest_file)
                url_hash = item['sha256']
                if file_hash == url_hash:
                    print(item['filename'].ljust(60), 'exists')
                    LOG.info('{0} no need download again'.format(item['filename']))
                    continue
            LOG.info('download[{0}] -> [{1}]'.format(item['url'], os.path.basename(dest_file)))
            if DOWNLOAD_INST.download(item['url'], dest_file):
                if 'sha256' in item and not CH.check_hash(dest_file, item['sha256']):
                    raise DownloadCheckError(dest_file)
                else:
                    results.get('ok', []).append(item.get('filename'))
                    print(item['filename'].ljust(60), 'download success')
                    continue
            print(item['filename'].ljust(60), 'download failed')
            results.get('failed', []).append(item.get('filename'))
