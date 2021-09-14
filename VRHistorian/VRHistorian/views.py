from time import sleep

# import signal
# import psutil
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.conf import settings
from VRHistorian.settings import base

import os
import sys
import subprocess


def upload(request):
    if request.method == 'GET':
        return render(request, os.path.join(base.BASE_DIR, 'static/templates/upload.html'))
    elif request.method == 'POST':
        content = request.FILES.get("img", None)
        if not content:
            return HttpResponse("没有上传内容")
        # 获取上传文件的内容
        position = os.path.join(base.MEDIA_ROOT, content.name)
        # 获取上传文件的文件名，并将其存储到指定位置
        storage = open(position, 'wb+')  # 打开存储文件
        for chunk in content.chunks():  # 分块写入文件
            storage.write(chunk)
        storage.close()  # 写入完成后关闭文件
        return HttpResponse("上传成功")  # 返回客户端信息
    else:
        return HttpResponseRedirect("不支持的请求方法")


def upload_multi(request):
    if request.method == 'GET':
        return render(request, os.path.join(base.BASE_DIR, 'static/templates/upload_multi.html'))
    elif request.method == 'POST':
        content = request.FILES.getlist("img_multi")
        if not content:
            return HttpResponse("没有上传内容")
        # 对多个文件分批次写入
        for f in content:
            # 获取上传文件的内容
            position = os.path.join(base.MEDIA_ROOT, f.name)
            # 取文件名，并将其存储到指定位置
            storage = open(position, 'wb+')  # 打开存储文件
            for chunk in f.chunks():  # 分块写入文件
                storage.write(chunk)
            storage.close()  # 写入完成后关闭文件
        return HttpResponse("上传成功")  # 返回客户端信息
    else:
        return HttpResponseRedirect("不支持的请求方法")


def clear_olds(request):
    def clear_jpg_files(file_dir):
        result = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == '.jpeg' or \
                        os.path.splitext(file)[1].lower() == '.png' or os.path.splitext(file)[1].lower() == '.gif' or \
                        os.path.splitext(file)[1].lower() == '.psd':
                    result.append(os.path.join(root, file))
        for f in result:
            os.remove(f)

    clear_jpg_files(base.MEDIA_ROOT)
    return HttpResponse("服务器端所有图片清除完毕")


def view_imgs_all(request):
    def get_img_files(file_dir):
        result = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == '.jpeg' or \
                        os.path.splitext(file)[1].lower() == '.png' or os.path.splitext(file)[1].lower() == '.gif' or \
                        os.path.splitext(file)[1].lower() == '.psd':
                    result.append(os.path.join(file))
        return result
    if len(get_img_files(base.MEDIA_ROOT)) == 0:
        return HttpResponse("当前保存的图片数量为0")
    if len(get_img_files(base.MEDIA_ROOT)) >= 2:
        args = ''
        for f in get_img_files(base.MEDIA_ROOT):
            args = args + f + ' '
        print(args)
        return HttpResponse(args)


def pano(request):
    def get_file_name(file_dir):
        result = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == '.jpeg' or \
                        os.path.splitext(file)[1].lower() == '.png' or os.path.splitext(file)[1].lower() == '.gif' or \
                        os.path.splitext(file)[1].lower() == '.psd':
                    result.append(os.path.join(file))
        return result

    def start_img_sk(args_input):
        print('change dir:', base.MEDIA_ROOT)
        os.chdir(os.path.join(base.MEDIA_ROOT, ''))
        # 此处需将image-sk程序加到PATH里
        # subprocess.call(args_input, 64, os.path.join(base.MEDIA_ROOT, 'image-stitching'), shell=True)
        os.system('./image-stitching ' + args)
        sleep(5000)

    if len(get_file_name(base.MEDIA_ROOT)) == 0:
        return HttpResponse("未发现可用JPG图片片段")
    if len(get_file_name(base.MEDIA_ROOT)) >= 2:
        args = ''
        for f in get_file_name(base.MEDIA_ROOT):
            args = args + f + ' '
        print(args)
        # HttpResponse("正在拼接中,稍后可下载")
        if start_img_sk(args):
            return HttpResponse("拼接流程执行完毕")
        else:
            return HttpResponse("拼接流程执行失败")


def download(request):
    if os.path.exists(os.path.join(base.MEDIA_ROOT, 'out.jpg')):
        file_out = open(os.path.join(base.MEDIA_ROOT, 'out.jpg'), 'rb')
        response = FileResponse(file_out)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment;filename="out.jpg"'
        return response
    else:
        return HttpResponse("未发现目标图片，可能拼接失败")

# def getAllPid():
#     pid_dict = {}
#     pids = psutil.pids()
#     for pid in pids:
#         p = psutil.Process(pid)
#         pid_dict[pid] = p.name()
#         # print("pid-%d,pname-%s" %(pid,p.name()))
#     return pid_dict
#
#
# def kill(pid):
#     try:
#         os.kill(pid, signal.SIGABRT)
#         print('已杀死pid为%s的进程')
#     except Exception as e:
#         print('没有如此进程!!!')
