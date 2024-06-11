# -*- coding: utf-8 -*-
import sys
import os
import shutil
from xml.dom import minidom
import xml.etree.ElementTree as ET
import subprocess


# 获取环境变量和路径
ProgramFiles_86 = os.environ.get('ProgramFiles(x86)', None)
seewo_path = os.path.join(ProgramFiles_86, 'Seewo', 'seewo')
seewo_path_EXEPath = os.path.join(seewo_path, 'seewo.exe')
seewo_path_xmlPath = os.path.join(seewo_path, 'install.xml')
runPath = os.path.dirname(os.path.abspath(__file__))
EXE_dirPath = os.path.join(runPath, 'install_dir')


del_folder = [os.path.join(seewo_path, 'venv')]
del_file = [seewo_path_xmlPath]



if not ProgramFiles_86:
    print("环境变量无法获取(ProgramFiles(x86))")
    sys.exit(1)

def copyMainFile(src_dir, dst_dir):
    """
    复制 src_dir 目录下的所有文件和子目录到 dst_dir。
    :param src_dir: 源目录路径
    :param dst_dir: 目标目录路径
    """
    if not os.path.exists(src_dir):
        raise ValueError("源目录", src_dir, "不存在")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    try:
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
        return True
    except Exception as e:
        print("复制文件时发生错误", {e})
        return False


def delete_folder(folder_path):
    """
    删除指定路径的文件夹及其内容。

    :param folder_path: str, 要删除的文件夹路径。
    """
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"文件夹 {folder_path} 已删除。")
            return True
        else:
            print(f"文件夹 {folder_path} 不存在。")
            return False
    except Exception as e:
        print(f"删除文件夹 {folder_path} 及其内容时发生错误: {e}")
        return False


def delete_file(file_path):
    """
    删除指定路径的文件。

    :param file_path: str, 要删除的文件的路径。
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"文件 {file_path} 已删除。")
            return True
        else:
            print(f"文件 {file_path} 不存在。")
            return False
    except Exception as e:
        print(f"删除文件 {file_path} 时发生错误: {e}")
        return False

def update_command_in_xml(file_path, new_command):
    """
    更新XML文件中<Command>标签的内容。
    :param file_path: str, XML文件的路径。
    :param new_command: str, 要设置的新<Command>标签内容。
    """
    try:
        new_command = '"' + str(new_command) + '"'
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        namespace = {'': 'http://schemas.microsoft.com/windows/2004/02/mit/task'}
        ET.register_namespace('', namespace[''])

        for command in root.findall('.//{http://schemas.microsoft.com/windows/2004/02/mit/task}Command'):
            command.text = new_command
        
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return True
    except Exception as e:
        print("修改xml文件发生错误", {e})
        return False

def import_xml_to_schtasks(xml_file_path):
    """
    导入修改后的XML文件到计划任务。
    :param xml_file_path: str, 修改后的XML文件路径。
    """
    try:
        print("导入修改后的 XML 文件...")
        result = subprocess.run(['schtasks', '/create', '/tn', 'SeewoNote5_Server', '/xml', xml_file_path], capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print("导入修改后的 XML 文件时发生错误。")
            print(result.stderr)
            sys.exit(result.returncode)
        else:
            print("计划任务已成功添加。")
            return True
    except Exception as e:
        print("执行schtasks命令时发生错误", {e})
        return False

def main():
    if os.path.isdir(seewo_path):
        print('警告', seewo_path, '目录已存在')

    if not copyMainFile(EXE_dirPath, seewo_path):
        print('在复制:', EXE_dirPath, '到目录:', seewo_path, '时发生错误, 无法继续安装')
        sys.exit(1)

    if not update_command_in_xml(seewo_path_xmlPath, seewo_path_EXEPath):
        print('修改xml文件', seewo_path_xmlPath, '时发生错误, 无法继续安装')
        sys.exit(1)

    if not import_xml_to_schtasks(seewo_path_xmlPath):
        print('安装xml文件', seewo_path_xmlPath, '时发生错误, 无法继续安装')
        sys.exit(1)

    for path_ in del_file:
        if not delete_file(path_):
            print('警告 清理文件', path_, '时发生错误')

    for path_ in del_folder:
        if not delete_file(path_):
            print('警告 清理文件夹', path_, '时发生错误')

if __name__ == '__main__':
    main()
