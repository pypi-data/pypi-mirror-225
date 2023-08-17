#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:chengduairport
# py_name :processing_txt
# software: PyCharm
# datetime:2021/3/3 13:45
"""文件类工具"""
from django.utils.encoding import escape_uri_path  # 用于解决中文命名文件乱码问题
from django.http import StreamingHttpResponse
from basic_type_operations.date_operation import DateOperation
from basic_type_operations.str_operation import StringOperation
import datetime as dt
from django.conf import settings
from PIL import Image
import filetype, linecache, os, urllib, time, math, zipfile, \
    tarfile, imghdr, uuid, shutil, requests, glob, mimetypes
import pandas as pd
from shutil import copy2, rmtree
import patoolib  # pip install patool
from pathlib import Path

PassExPrentFile = ["png", "jpg", "doc", "pdf", "xlsx", 'docx', 'xls', 'zip', 'mp4']
passFile = ['.doc', '.docx']
picEx = ["png", "jpg"]


class FileZIPOperation(object):
    # <editor-fold desc="zip下载器">
    def zip_download(self, urllist, namelist):
        count = 0
        dir = os.path.abspath('.')
        for item in urllist:
            if os.path.exists(os.path.join(dir, namelist[count] + '.zip')):
                count = count + 1
            else:
                try:
                    # print('正在下载' + namelist[count])
                    work_path = os.path.join(dir, namelist[count] + '.zip')
                    urllib.request.urlretrieve(item, work_path)
                    count = count + 1
                except:
                    continue

    # </editor-fold>
    # <editor-fold desc="# zip的压缩和解密">
    # 打包目录为zip文件（未压缩）
    def zip_make(self, source_dir, output_filename):
        """
        make_zip(r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage', "copyimage.zip")
        :param source_dir:
        :param output_filename:
        :return:
        """
        zipf = zipfile.ZipFile(output_filename, 'w')
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()

    # zip解压缩
    def zip_unpack(self, zip_path, dst_dir, ):
        # dst_dir = os.getcwd() + '/extract'  # 解压目录
        # zip_path = os.getcwd() + '/tk_mysql_dump_Release_20200717.zip'  # 压缩包路径
        FileOperation.makedirs(dst_dir)
        try:
            shutil.unpack_archive(zip_path, dst_dir, zip_path.split(".")[-1])
        except:
            with zipfile.ZipFile(zip_path, 'r') as f:
                f.extractall(dst_dir)

    # zip解加密压缩包
    def zip_extract(self, zip_path, dst_dir, pwd):
        """
        p = 'di201805'
    path = r'F:\python学习资料\新建文件夹\解压后'
        :param mypath:
        :return:
        """
        # zfile = zipfile.ZipFile(r"F:\jiyiproj\automaticoffice\002common\文件以及文件夹\extract\C语言编程精粹.PDF.zip")
        zfile = zipfile.ZipFile(zip_path)
        zfile.extractall(path=dst_dir, pwd=str(pwd).encode('utf-8'))

    # </editor-fold>
    # <editor-fold desc="tar.gz 打包 压缩">
    # 打包目录为zip文件（未压缩）
    # 一次性打包整个根目录。空子目录会被打包。
    # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    def tar_gz_make(self, source_dir, output_filename, ):
        """
        tar_gz_make("copyimage.tar.gz", r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage')
        :param output_filename:
        :param source_dir:
        :return:
        """
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    # 逐个添加文件打包，未打包空子目录。可过滤文件。
    # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    # 多个不同目录下的文件打包成一个tar
    def tar_gz_files_make(self, source_dir, output_filename, ):
        """
        make_targz_one_by_one("copyimage.tar.gz", r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage')
        :param output_filename:
        :param source_dir:
        :return:
        """
        tar = tarfile.open(output_filename, "w:gz")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile)
        tar.close()

    # 多个不同目录下的文件打包成一个tar
    def tar_gz_any_files_make(self, output_filename, source_dir_lis):
        """
        # make_targz_many('/home/zlp/zlp.tar.gz', ['/home/zlp/result', '/home/zlp/Desktop/teston2'])
        :param output_filename:
        :param source_dir:
        :return:
        """
        with tarfile.open(output_filename, "w:gz") as tar:
            for dir in source_dir_lis:
                tar.add(dir, arcname=os.path.basename(dir))

    def tar_gz_unpack(self, tar_gz_path, dst_dir):
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            tar.extractall(dst_dir)

    # </editor-fold>
    # <editor-fold desc="rar压缩和解压缩">
    def rar_unpack(self, rar_path, dst_dir):
        patoolib.extract_archive(rar_path, outdir=dst_dir)

    # </editor-fold>
    def get_archive_formats(self, ):
        return shutil.get_archive_formats()

    def make_archive(self, base_name, format, root_dir=None, base_dir=None):
        """
        Create an archive file (eg. zip or tar).
        :param base_name: 是要创建的文件的名称，减去任何特定于格式的扩展名;
        :param format:“格式”是存档格式：“zip”，“tar”，“gztar”，“bztar”或“xztar”之一。或任何其他注册格式。
        :param root_dir: 是一个目录，将成为存档的根目录
        :param base_dir: “base_dir”是我们开始存档的目录
       “root_dir”和“base_dir”都默认为当前目录。返回存档文件的名称。
        :return:
            print(FileZIPOperation().make_archive("dirs/dirs111", "bztar", root_dir="dirs",
                                          base_dir="dirs"))
                                          生成
        # print(FileZIPOperation().make_archive("dirs", "gztar"))
        # print(FileZIPOperation().make_archive("dirs", "tar"))
        # print(FileZIPOperation().make_archive("dirs", "xztar"))
        # print(FileZIPOperation().make_archive("dirs", "zip"))
        """
        shutil.make_archive(base_name, format, root_dir=root_dir, base_dir=base_dir, )

    def send_zip(self, url, zip_path, headers=None):
        files = {'app_filename': (zip_path, open(zip_path, 'rb'), 'application/x-zip-compressed')}
        # files ={'app_filename':open('portal-1.0-SNAPSHOT-fat.jar.zip','rb')} 和上面的功能一样
        if not headers:
            headers = {
                'Authorization': '6bae7b70-8dae-4f74-9631-680b9501b52',
                'cookie': "_ga=GA1.3.733851079.1534745675; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1537859803; _ga=GA1.3.733851079.1534745675; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1537859803",
            }
        res = requests.post(url, files=files, headers=headers)
        return res.json()


class FileBasicOperation(object):
    # <editor-fold desc="删除文件或者文件夹">
    def remove_path(self, path):
        """
        :param path: 文件或者文件夹路径,文件架空不空都强删
        :return:
         os.remove#删除文件
        os.rmdir#删除文件夹（只能删除空文件夹）
        os.removedirs#移除目录(必须是空目录)
        shutil.rmtree#删除文件夹
        """
        if os.path.isfile(path):
            os.remove(path)
        else:
            rmtree(path)

    def delete(self, path):
        FileBasicOperation().remove_path(path)

    # </editor-fold>
    # <editor-fold desc="创建文件夹">
    def makedirs(self, path):
        path_obj = Path(path)
        if not path_obj.suffix and not path_obj.exists():
            path_obj.absolute().mkdir(parents=True)
        elif path_obj.suffix and not path_obj.absolute().parent.exists():
            path_obj.absolute().parent.mkdir(parents=True)
        return path_obj.absolute()

    # </editor-fold>
    # <editor-fold desc="获取桌面路径">
    # 这样做的好处是可以把数据放在桌面上，在不同的电脑上都能调用代码对数据进行处理。
    # 如果是在一条电脑上把桌面路径固定在字符串中，则换一台电脑就必须修改桌面路径。
    def get_desktop_path(self, ):
        return os.path.join(os.path.expanduser("~"), 'Desktop')

    # </editor-fold>
    # <editor-fold desc="获取文件的大小,结果保留两位小数，单位为MB">
    @staticmethod
    def file_size(file):
        fsize = os.path.getsize(file)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    # </editor-fold>
    # <editor-fold desc="获取文件的访问时间">
    @staticmethod
    def file_access_time(file):
        t = os.path.getatime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件的创建时间">
    @staticmethod
    def file_create_time(file):
        t = os.path.getctime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件的修改时间">
    @staticmethod
    def file_modify_time(file):
        t = os.path.getmtime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件时间">
    def get_file_time(self, file):
        from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
        from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
        fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)
        CloseHandle(fh)
        return createTimes, accessTimes, modifyTimes

    # </editor-fold>
    # <editor-fold desc="修改文件时间">
    def modify_file_time(self, file, create_time=None, modify_time=None, access_time=None, offset=(0, 0, 0),
                         format="%Y-%m-%d %H:%M:%S"):
        from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
        from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
        from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
        if not create_time:
            create_time = FileBasicOperation.file_create_time(file)
        if not modify_time:
            modify_time = FileBasicOperation.file_modify_time(file)
        if not access_time:
            access_time = FileBasicOperation.file_access_time(file)
        fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(create_time, format, offset[0])))
        modifyTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(modify_time, format, offset[1])))
        accessTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(access_time, format, offset[2])))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)

    # </editor-fold>
    # <editor-fold desc="获取文件某一行/文件内容">
    @staticmethod
    def getlines(file, line=None):
        """
        :param file: 目标文件
        :param line: 行
        :return:
        """
        if not line:
            return linecache.getline(file, line)
        else:
            return linecache.getlines(file)

    # </editor-fold>
    # <editor-fold desc="读取文件最后n行">
    @staticmethod
    def get_last_lines(file, n):
        blk_size_max = 4096
        n_lines = []
        with open(file, 'rb') as fp:
            fp.seek(0, os.SEEK_END)
            cur_pos = fp.tell()
            while cur_pos > 0 and len(n_lines) < n:
                blk_size = min(blk_size_max, cur_pos)
                fp.seek(cur_pos - blk_size, os.SEEK_SET)
                blk_data = fp.read(blk_size)
                assert len(blk_data) == blk_size
                lines = blk_data.decode().split('\r\n')
                # adjust cur_pos
                if len(lines) > 1 and len(lines[0]) > 0:
                    n_lines[0:0] = lines[1:]
                    cur_pos -= (blk_size - len(lines[0]))
                else:
                    n_lines[0:0] = lines
                    cur_pos -= blk_size
                fp.seek(cur_pos, os.SEEK_SET)
        if len(n_lines) > 0 and len(n_lines[-1]) == 0:
            del n_lines[-1]
        return n_lines[-n:]

    # </editor-fold>
    # <editor-fold desc="扫描输出所有的子目录（子文件夹）">
    # 扫描输出所有的子目录（子文件夹）
    # 使用os.walk输出某个目录下的所有文件   er
    @staticmethod
    def dir_son_names(dir_path):
        """
        :param dir_path: 目标文件夹
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            """
            print("现在的目录：", curDir)
            print("该目录下包含的子目录：", str(dirs))
            print("该目录下包含的文件：", str(files))
            """
            for _dir in dirs:
                lis.append(os.path.join(curDir, _dir))
        return lis

    # </editor-fold>
    # <editor-fold desc="输出所有文件">
    # 扫描输出所有文件的路径
    @staticmethod
    def file_paths(dir_path):
        """

        :param dir_path: 目标文件夹
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                lis.append(os.path.join(curDir, file))
        return lis

    # </editor-fold>
    # <editor-fold desc="输出指定类型文件">
    @staticmethod
    def file_endswith_path(dir_path, endswith):
        """

        :param dir_path:目录地址
        :param endswith: 文件结尾
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            lis.append([os.path.join(curDir, file) for file in files if file.endswith(endswith)])
        res = (x for j in lis for x in j)
        return list(res)

    # </editor-fold>
    # <editor-fold desc="文件去重-相同日期文件">
    @staticmethod
    def file_qch_date(dir_path):
        wj_names = os.listdir(dir_path)
        wj_list = []
        num = 0
        for wj in wj_names:
            new_wj = wj[:-11]
            if new_wj not in wj_list:
                wj_list.append(new_wj)
            else:
                os.remove(dir_path + "\\" + wj)
                num += 1
        return num

    # </editor-fold>
    # <editor-fold desc="找指定时间段条件的文件">
    @staticmethod
    def file_move(dir_path, start_date, end_date):
        # 本文件移动至对应新建文件夹，非本月文件直接删除
        """
        :param file_dir_path: 目标文件夹
        :return:
        """
        # # 日期格式：xxxx-xx eg:2020-07-01
        # # 生成日期区间-字符串类型
        date_xl_str = [str(i)[:10] for i in pd.date_range(start_date, end_date, freq='D')]
        # # # 创建指定文件夹
        _new_dir_path = os.getcwd() + '\\' + start_date + "~" + end_date
        try:
            os.mkdir(_new_dir_path)
        except:
            pass
        # time_data = []
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                old_dir_path = os.path.join(curDir, file)
                # time_data.append(str(time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(old_dir_path)))))
                new_dir_path = os.path.join(_new_dir_path, file)
                # file_date = file.split("_")[-1][:10]
                # 文件创建时间
                file_date = str(time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(old_dir_path))))
                # print(old_dir_path, '*******', new_dir_path, '*******', file_date)
                try:
                    # os.rename(old_dir_path, new_dir_path) if file_date in date_xl_str else os.remove(old_dir_path)
                    if file_date in date_xl_str:
                        # os.rename(old_dir_path, new_dir_path)  # 把文件移动到另外一个文件夹
                        copy2(old_dir_path, new_dir_path)
                except Exception as e:
                    # os.remove(old_dir_path)
                    pass

    # </editor-fold>
    # <editor-fold desc="文件或者文件夹-重新命名">
    @staticmethod
    def path_renames(old_path_name, new_path_name):
        # os.rename(old_file_path, new_file_path)# 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
        try:
            # 是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名
            os.renames(old_path_name, new_path_name)
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="创建具有顺序的文件夹或者文件">
    @staticmethod
    def file_number(cap_num, path_name_end=None, to_dir=None):
        """
        :param cap_num:创建个数
        :param path_name_end: 文件的后缀名 如txt, 不传创建文件夹
        :param to_dir: 存储路径
        :return:
        """
        try:
            cap_num_t = cap_num
            cap_count = 0
            while cap_num:
                cap_count = cap_count + 1
                cap_num = math.floor(cap_num / 10)
            fix = '%0' + str(cap_count) + 'd'  # 得到图片保存的前缀，比如001.png，0001.png
            cap_cnt = 1
            if not os.path.exists(to_dir):
                os.makedirs(to_dir)
            while cap_num_t:
                if path_name_end:
                    if to_dir:
                        path = os.path.join(to_dir, str(fix % cap_cnt) + '.' + path_name_end)
                    else:
                        path = str(fix % cap_cnt) + '.' + path_name_end
                    with open(path, mode="w", encoding="utf-8") as f:  # 写文件,当文件不存在时,就直接创建此文件
                        pass
                else:
                    if to_dir:
                        path = os.path.join(to_dir, str(fix % cap_cnt))
                    else:
                        path = str(fix % cap_cnt)
                    os.makedirs(path)
                cap_cnt = cap_cnt + 1
                cap_num_t -= 1
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="生成以时间戳和文件名称命名的文件或文件夹">
    @staticmethod
    def file_datetime(name_start=None, to_Dir=None):
        """
        :param name_start: 文件名或者文件名称 a.txt a
        :param rootDir: 存储路径
        :return:
        """
        name_end = None
        if '.' in name_start:
            name_end = name_start.split('.')[1]
            name_start = name_start.split('.')[0]
        date = dt.datetime.now().strftime('%Y%m%d%H%M%S%f')
        if name_end:
            if to_Dir:
                path = os.path.join(to_Dir, str(name_start) + str(date) + '.' + name_end)
            else:
                path = str(name_start) + str(date) + '.' + name_end
            f = open(path, 'w')
            f.close()
        else:
            if name_start:
                if to_Dir:
                    path = os.path.join(to_Dir, str(name_start) + str(date))
                else:
                    path = str(name_start) + str(date)
            else:
                if to_Dir:
                    path = os.path.join(to_Dir, str(date))
                else:
                    path = str(date)
            os.mkdir(path)
        return path

    # </editor-fold>
    # <editor-fold desc="过滤指定文件">
    @staticmethod
    def filter_files(file_list, endswith):
        def is_index(n):
            if n.endswith(endswith):
                return n

        file_list = list(filter(is_index, file_list))
        return file_list

    # </editor-fold>
    # <editor-fold desc="文件排序">
    @staticmethod
    def file_sort_absolute(dir_path, endswith):
        """
        :param path:文件位置
        :param endswith: 文件以什么结尾比如py，xls,word,txt等
        :param absolute: True是返回绝对路径，Flase是返回相对路径
        :return: 列表内都是文件的绝对路径
        """
        file_list = os.listdir(dir_path)
        length = len(endswith) + 1
        file_list = FileBasicOperation.filter_files(file_list, endswith)
        file_list.sort(key=lambda x: int(x[:-length]) if x.endswith(endswith) else False)
        file_list = [os.path.join(dir_path, i) for i in file_list]
        return file_list

    # </editor-fold>
    # <editor-fold desc="不全是num的文件数字排序">
    @staticmethod
    def file_other_sort(dir_path, endswith, split=None, location=None):
        """
        :param path:文件位置
        :param endswith: 文件以什么结尾比如py，xls,word,txt等
        :param split: split 右边是数字
        :param location:
        需要配合 split进行使用
        right 右边是数字 left 左边是数字
        1 拆分后索引1的位置是数字，2 拆分后索引2的位置是数字 .。。
        ‘create’ 按照文件创建时间进行排序
        ‘modify’ 按照文件修改时间进行排序
        ‘access’ 按照文件访问时间进行排序
        None 默认排序
        :param absolute: True是返回绝对路径，Flase是返回相对路径
        :return: 列表内都是文件的绝对路径
        """
        file_list = os.listdir(dir_path)
        file_list = FileBasicOperation.filter_files(file_list, endswith)
        length = len(endswith) + 1
        if split:
            if location not in ['right', "left", "create", "modify", "access", None] and not isinstance(location, int):
                raise ValueError(f"location not value {location}")
            if location == None:
                location = "create"
            if location in ["create", "modify", "access", ]:
                file_list = [os.path.join(dir_path, i) for i in file_list]
                if location == "create":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_create_time(x) if x.endswith(endswith) else False)
                elif location == "modify":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_modify_time(x) if x.endswith(endswith) else False)
                elif location == "access":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_modify_time(x) if x.endswith(endswith) else False)
                return file_list
            elif location == "right":
                file_list.sort(key=lambda x: int(x[:-length].split(split)[-1]) if x.endswith(endswith) else False)
            elif location == "left":
                file_list.sort(key=lambda x: int(x[:-length].split(split)[0]) if x.endswith(endswith) else False)
            elif isinstance(location, int):
                file_list.sort(key=lambda x: int(x[:-length].split(split)[location]) if x.endswith(endswith) else False)
        else:
            file_list.sort(key=lambda x: x if x.endswith(endswith) else False)
        file_list = [os.path.join(dir_path, i) for i in file_list]
        return file_list

    # </editor-fold>
    # <editor-fold desc="文件夹数字排序">
    @staticmethod
    def dir_num_sort(dir_path, absolute=True):
        """

        :param dir_path: 文件位置
        :param absolute: 返回绝对位置
        :return:
        """
        rootpath = os.listdir(dir_path)
        rootpath = [dir_path for dir_path in rootpath if '.' not in dir_path]
        rootpath.sort(key=lambda x: int(x))
        if absolute:
            rootpath = [dir_path + '\\' + i for i in rootpath]
        return rootpath

    # </editor-fold>
    # <editor-fold desc="文件移动到另外一个问价夹内">
    @staticmethod
    def files_move(file, to_dir):
        """
        :param path:文件地址
        :param to_dir: 存储文件夹
        :return:
        """
        try:
            copy2(file, to_dir)
            # 将目标文件移动到目标文件夹里，
            # shutil.move(r'.\practice.txt', r'.\文件夹1/')
            # 将目标文件移动到目标文件夹里的同时，能够对其进行重命名
            # shutil.move(r'.\practice.txt', r'.\文件夹1/new.txt')
            # 如果我们需要移动某个或某些文件到新的文件夹，并且需重命名文件，
            # 则我们并不需要用 os.rename 先命名文件再用
            # shutil.move 将其移动的指定文件夹，而是可以用 shutil.move 一步到位
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="文件批量改名">
    @staticmethod
    def file_many_rename(dir_path, endswith):
        """

        :param dir_path:目录地址
        :param endswith: 文件结尾
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            lis.append([os.path.join(curDir, file) for file in files if
                        file.endswith(endswith)
                        ]
                       )
        res = (x for j in lis for x in j)
        lisdir = list(res)
        fileNum = len(str(len(lisdir)))
        formatting_new = '%0' + str(fileNum) + 'd'
        for index, i in enumerate(lisdir):
            to_pa = i
            new = formatting_new % (index + 1)
            path = '\\'.join(i.split('\\')[:-1])
            file_name: str = i.split('\\')[-1]
            file_before = file_name.split('.')[0]
            if file_before.strip('0').isdigit():
                new_i = new + '.' + endswith
                new_path = os.path.join(path, new_i)
            elif file_before[:fileNum].strip('0').isdigit():
                new_path = new + file_before[fileNum:] + '.' + endswith
            else:
                new_path = new + file_before + '.' + endswith
            os.renames(to_pa, new_path)

    # </editor-fold>
    # <editor-fold desc="文件匹配">
    def glob(self, re_, root_dir, dir_fd=None, recursive=False):
        """

        :param endswith:
        :param root_dir:
        :param dir_fd:
        :param recursive:
        :return:
        glob 函数支持三种格式的语法：
* 匹配单个或多个字符
? 匹配任意单个字符
[] 匹配指定范围内的字符，如：[0-9]匹配数字。
        """
        # glob.glob("*.ipynb")
        # glob.glob("../09*/*.ipynb")
        # glob.glob("../[0-9]*")#匹配数字开头的文件夹名：
        # glob.glob("*.ipynb")
        return glob.glob(re_, root_dir=root_dir, dir_fd=dir_fd, recursive=recursive)
    # </editor-fold>


class FileOperation(FileZIPOperation, FileBasicOperation):
    @staticmethod
    def save_destination(dest, reqfile):
        if not os.path.exists(dest):
            if not isinstance(reqfile, bytes):
                with open(dest, "wb") as destination:
                    for chunk in reqfile.chunks():
                        destination.write(chunk)
            else:
                with open(dest, "wb") as destination:
                    destination.write(reqfile)

    @staticmethod
    def upload(FILES, file_type: str, **kwargs):
        """
            上传文件
        :return:
        """
        reqfile = FILES
        if kwargs:
            filename = kwargs['file_name']
            filename_old = kwargs['file_name']
        else:
            filename = reqfile.name
            filename_old = reqfile.name
        if str(filename).find('.') == -1:
            filename = filename + '.jpg'
            suffix = '.jpg'
        else:
            suffix = filename[filename.rfind('.'):]
        filename_old = filename
        if StringOperation.check_contain_zh_cn(filename) and imghdr.what(reqfile):
            filename_old = filename
            filename = str(uuid.uuid1()) + suffix

        current_time = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        current_time_str = dt.datetime.now().strftime("%Y%m%d %H:%M:%S")

        pathdir = os.path.join(settings.MEDIA_ROOT, file_type, current_time).replace('\\', '/')
        pathRela = os.path.join(file_type, current_time, filename).replace('\\', '/')
        dest = os.path.join(settings.MEDIA_ROOT, file_type, current_time, filename).replace('\\', '/')

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        thumb_flag = False
        if not isinstance(reqfile, bytes):
            if imghdr.what(reqfile):  # 是图片类型
                thumb_flag = True
                img_ = Image.open(reqfile).convert('RGB')
                width, height = img_.size
                size = (480, 480)
                img_.thumbnail(size, Image.ANTIALIAS)
                thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumb', file_type, current_time).replace('\\', '/')
                if not os.path.exists(thumb_path):
                    os.makedirs(thumb_path)
                # print(thumb_path)
                # 保存
                img_.save(thumb_path + '/' + filename, quality=70)
        FileOperation.save_destination(dest, reqfile)
        res = {
            'original': settings.HTTP_HEAD + '/media/' + pathRela,
            'short_url': pathRela
        }
        if thumb_flag:
            res['thumb'] = settings.HTTP_HEAD + '/media/thumb/' + pathRela
        return res

    @staticmethod
    def file_upload(FILES, file_type: str, **kwargs):
        """
            上传文件
        :return:
        """
        try:
            reqfile = FILES
            filename = reqfile.name
            suffix = filename[filename.rfind('.'):]
            kind = filetype.guess(reqfile)
            if kind is None and suffix not in passFile:
                raise Exception('未知混乱或无效的文件')
            if kind and kind.extension not in PassExPrentFile:
                raise Exception('不允许的文件类型')
            current_time = dt.datetime.now().strftime("%Y%m%d%H%M%S")
            if StringOperation.check_contain_zh_cn(filename):
                filename = str(uuid.uuid1()) + suffix

            pathdir = os.path.join(settings.MEDIA_ROOT, file_type, current_time).replace('\\', '/')
            pathRela = os.path.join(file_type, current_time, filename).replace('\\', '/')
            dest = os.path.join(settings.MEDIA_ROOT, file_type, current_time, filename).replace('\\', '/')
            if not os.path.exists(pathdir):
                os.makedirs(pathdir)
            FileOperation.save_destination(dest, reqfile)
            res = {
                'original': settings.HTTP_HEAD + '/media/' + pathRela,
                'short_url': pathRela
            }
            return res
        except Exception as e:
            raise Exception('文件传输过程中发生异常，或者您上传了不允许的文件')

    @staticmethod
    def file_iterator(file_name):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    @staticmethod
    def download(request, file_name, file_path):
        response = StreamingHttpResponse(FileOperation.file_iterator(file_path))
        file_end = file_path.split('.')[-1]
        agent = request.META.get('HTTP_USER_AGENT')
        if agent.upper().find("MSIE") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gbk').decode('latin-1')
        elif agent.upper().find("EDGE") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gb2312')
        elif agent.upper().find("TRIDENT") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gb2312')
        else:
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                escape_uri_path(file_name + f'.{file_end}'))
        response["Access-Control-Expose-Headers"] = "Content-Disposition"  # 为了使前端获取到Content-Disposition属性
        if file_end == "pdf":
            response["Content-type"] = "application/pdf"
        elif file_end == "zip":
            response["Content-type"] = "application/zip"
        elif file_end == "doc":
            response["Content-type"] = "application/msword"
        elif file_end == "xls":
            response["Content-type"] = "application/vnd.ms-excel"
        elif file_end == "xlsx":
            response["Content-type"] = "application/vnd.ms-excel"
        elif file_end == "docx":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_end == "doc":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_end == "ppt":
            response["Content-type"] = "application/vnd.ms-powerpoint"
        elif file_end == "pptx":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            response['Content-Type'] = 'application/octet-stream'
        return response
