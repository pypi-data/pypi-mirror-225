from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
import subprocess
import os
import importlib.util
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# Create your views here.
# @cache_page(60 * 15) # 单位：秒数，这里指缓存 15 分钟
def home(request):
    # 返回结果
    return render(request, 'home.html', {'active_menu': 'home',})

def rmsf(request):
    return render(request, 'rmsf.html',{'active_menu': 'rmsf',})

def batch(request):
    return render(request, 'batch.html',{'active_menu': 'batch',})

def moleccular(request):
    return render(request, 'molecular.html',{'active_menu': 'moleccular',})

def help(request):
    return render(request, 'help.html',{'active_menu': 'help',})

def submit_form_view(request):
    if request.method == 'POST':
        pdb_file = request.FILES.get('pdb_file', None)
        file_path1 = save_my_file_to_directory(pdb_file).replace("\\", "/")  # 将文件保存到指定目
        map_file = request.FILES.get('em_file', None)
        file_path2 = save_my_file_to_directory(map_file).replace("\\", "/")  # 将文件保存到指定目
        map_level = request.POST.get('map_level')
        mode = request.POST.get('mode')

        # do something with the uploaded files and form data  D:\python\python_practice\test01.py
        # module_path = 'D:/GiteeCode/python/python_practice/python_vscode/'  # 修改为需要导入的模块所在的文件夹路径
        module_path = 'D:/python/python_practice/'  # 修改为需要导入的模块所在的文件夹路径
        module_name = 'test01'  # 修改为需要导入的模块的名称

        # 动态导入模块
        spec = importlib.util.spec_from_file_location(module_name, module_path + '/' + module_name + '.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 调用需要执行的函数并传入参数
        # 函数名和参数需要根据实际代码进行修改
        arg1 = '1'
        arg2 = '1'
        arg3 = '2'
        result = getattr(module, 'compute')(arg1, arg2, arg3)

        # 输出计算结果
        print('----------------------------------------------------')
        print(result)
        # return render(request, "result.html", {"name": name, "file_url": file.name})
        return render(request, 'result.html', {"name": pdb_file.name, "file_url": file_path1,"name2": map_file.name, "file_url2": file_path2})
    else:
        return render(request, 'rmsf.html', {})  # replace the empty {} with context data if needed


def save_my_file_to_directory(my_file):
    file_name = my_file.name
    file_path = os.path.join('static/file', file_name).replace("\\", "/")   # 保存到指定目录下
    with open(file_path, 'wb+') as destination:
        for chunk in my_file.chunks():
            destination.write(chunk)
    return file_path


def mail(request):
    if request.method == 'POST':
        print('----------------------------------------------------')
    return render(request, 'batch.html')

@csrf_exempt
def send_email_with_attachment2(request):
    send_mail('Subject here', 'Here is the message.', 'ahangouth@163.com',
              ['1363664048@qq.com'], fail_silently=False)
    # email = EmailMessage('测试','这是封测试邮件', to=['1363664048@qq.com'])
    # email.send()
    return JsonResponse({'message': '邮件发送成功'})

