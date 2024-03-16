#本节点原作者AlekPet，翻译人二狗子
import os
import importlib.util
import subprocess
import sys
import filecmp
import shutil
import __main__
import pkgutil
import re
import threading

python = sys.executable

# User extension files in custom_nodes
extension_folder = os.path.dirname(os.path.realpath(__file__))

# ComfyUI folders web
folder_web = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "web")
folder_web_extensions = os.path.join(folder_web, "extensions")
folder__web_lib = os.path.join(folder_web, 'lib')
extension_dirs = ["EG_GN_NODES",]
#
DEBUG = False
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
humanReadableTextReg = re.compile('(?<=[a-z])([A-Z])|(?<=[A-Z])([A-Z][a-z]+)')
module_name_cut_version = re.compile("[>=<]")

installed_modules = list(m[1] for m in pkgutil.iter_modules(None))

def log(*text):
    if DEBUG:
        print(''.join(map(str, text)))


def check_is_installed(module_name):    
    try:
        module_name_cut_index = module_name_cut_version.search(module_name)
        module_name_no_version = ""
        if(module_name_cut_index):
            module_name_cut_index = module_name_cut_index.start()
            module_name_no_version = module_name[:module_name_cut_index]
            modulImport = importlib.util.find_spec(module_name_no_version)
            
            if(modulImport is not None):
                return True
        
        if(module_name_no_version.lower() in installed_modules or module_name.lower() in installed_modules):                   
            return True
        
        return False 

    except ModuleNotFoundError:
        return False


def module_install_old(module_name, action='install'):
    if not module_name and not action:
        log(f'    [!] Action, module_name arguments is not corrects!')
        return

    command = f'"{python}" -m pip {action} {module_name}'
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ)
    action_capitalize = action.capitalize()

    if result.returncode != 0:
        log(f'    [E] {action_capitalize} module {module_name} is fail! Error code: {result.returncode}')

    log(f'    [*] {action_capitalize} module "{module_name}" successful')


def checkModules_old(nodeElement):
    file_requir = os.path.join(extension_folder, nodeElement, 'requirements.txt')
    if os.path.exists(file_requir):
        log("  -> File 'requirements.txt' found!")
        with open(file_requir, 'r', encoding="utf-8") as r:
            for m in r.readlines():
                m = m.strip()

                if m.startswith("#"):
                    log(f"    [!] Found comment skipping: '{m}'")
                    continue

                log(f"    [*] Check installed module '{m}'...")
                check_m = check_is_installed(m)
                if not check_m:
                    module_install(m)
                else:
                    log(f"    [*] Module '{m}' is installed!")


def information(datas):
    for info in datas:
        if DEBUG:
            print(info, end="")


def module_install(commands, cwd='.'):
    result = subprocess.Popen(commands, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    out = threading.Thread(target=information, args=(result.stdout,))
    err = threading.Thread(target=information, args=(result.stderr,))
    out.start()
    err.start()
    out.join()
    err.join()

    return result.wait()


def checkModules(nodeElement):
    file_requir = os.path.join(extension_folder, nodeElement, 'requirements.txt')
    if os.path.exists(file_requir):
        log("  -> File 'requirements.txt' found!")
        module_install([sys.executable, '-s', '-m', 'pip', 'install', '-r', file_requir])


def addFilesToFolder(folderSrc, folderDst, nodeElement):
    if os.path.exists(folderSrc):
        folder = os.path.split(folderSrc)[-1]
        log(f"  -> Find files javascipt in '{folder}' folder...")
        find_files = filecmp.dircmp(folderSrc, folderDst)
        if find_files.left_only or find_files.diff_files:
            listFiles = list(find_files.left_only)
            listFiles.extend(f for f in find_files.diff_files if f not in listFiles)

            log(f"    [*] Found files in '{folder}': {', '.join(listFiles)}")
            for f in listFiles:
                src_f = os.path.join(folderSrc, f)
                dst_f = os.path.join(folderDst, f)
                if os.path.exists(dst_f):
                    os.remove(dst_f)
                shutil.copy(src_f, dst_f)


def removeFilesOldFolder(folderSrc, folderDst, nodeElement):
    if os.path.exists(folderSrc):
        folder = os.path.split(folderDst)[-1]
        log(f"  -> Find old js files and remove in '{folder}' folder")
        find_files = filecmp.dircmp(folderDst, folderSrc)
        if find_files.common:
            listFiles = list()
            listFiles.extend(f for f in find_files.common if f not in listFiles)

            log(f"    [*] Found old files in '{folder}' folder: {', '.join(listFiles)}")
            for f in listFiles:
                dst_f = os.path.join(folderDst, f)
                if os.path.exists(dst_f):
                    log(f"    [*] File '{f}' is removed.")
                    os.remove(dst_f)


def addComfyUINodesToMapping(nodeElement):
    log(f"  -> Find class execute node <{nodeElement}>, add NODE_CLASS_MAPPINGS ...")
    node_folder = os.path.join(extension_folder, nodeElement)
    for f in os.listdir(node_folder):
        ext = os.path.splitext(f)
        # Find files extensions .py
        if os.path.isfile(os.path.join(node_folder, f)) and not f.startswith('__') and ext[1] == '.py' and ext[0] != '__init__':
            # remove extensions .py
            module_without_py = f.replace(ext[1], '')
            # Import module
            spec = importlib.util.spec_from_file_location(module_without_py, os.path.join(node_folder, f))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            classes_names = list(filter(lambda p: callable(getattr(module, p)) and p.find('Node') != -1, dir(module)))
            for class_module_name in classes_names:
                # Check module
                if class_module_name and class_module_name not in NODE_CLASS_MAPPINGS.keys():
                    log(f"    [*] Class node found '{class_module_name}' add to NODE_CLASS_MAPPINGS...")
                    NODE_CLASS_MAPPINGS.update({
                        class_module_name: getattr(module, class_module_name)
                    })
                    NODE_DISPLAY_NAME_MAPPINGS.update({
                        class_module_name: humanReadableTextReg.sub(" \\1\\2", class_module_name)
                    })


def checkFolderIsset():
    log(f"*  Check and make not isset dirs...")
    for d in extension_dirs:
        dir_ = os.path.join(folder_web_extensions, d)
        if not os.path.exists(dir_):
            log(f"* Dir <{d}> is not found, create...")
            os.mkdir(dir_)
            log(f"* Dir <{d}> created!")


def printColorInfo(text, color='\033[92m'):
    CLEAR = '\033[0m'
    print(f"{color}{text}{CLEAR}")


def installNodes():
    log(f"\n-------> AlekPet Node Installing [DEBUG] <-------")
    checkFolderIsset()
    web_extensions_dir = os.path.join(folder_web_extensions, extension_dirs[0])

    for nodeElement in os.listdir(extension_folder):
        if not nodeElement.startswith('__') and nodeElement.endswith('Node') and os.path.isdir(os.path.join(extension_folder, nodeElement)):
            log(f"* Node <{nodeElement}> is found, installing...")
            js_folder = os.path.join(extension_folder, nodeElement, "js")
            lib_folder = os.path.join(extension_folder, nodeElement, "lib")

            # Removes old files
            removeFilesOldFolder(js_folder, folder_web_extensions, nodeElement)

            # Add missing or updates files
            addFilesToFolder(js_folder, web_extensions_dir, nodeElement)
            addFilesToFolder(lib_folder, folder__web_lib, nodeElement)

            # Loading node info
            printColorInfo(f"Node -> {nodeElement} [Loading]")

            checkModules(nodeElement)
            addComfyUINodesToMapping(nodeElement)


installNodes()

import hashlib
import os
import json
from server import PromptServer
from aiohttp import web
from PIL import Image, ImageOps
import torch
import numpy as np
import folder_paths

# Directory node save settings
CHUNK_SIZE = 1024
dir_painter_node = os.path.dirname(__file__)
extension_path = os.path.join(os.path.abspath(dir_painter_node))
file_settings_path = os.path.join(extension_path,"settings_nodes.json")

# Function create file json file
def create_settings_json(filename="settings_nodes.json"):
    json_file = os.path.join(extension_path, filename)
    if not os.path.exists(json_file):
        print("File settings_nodes.json is not found! Create file!")
        with open(json_file, "w") as f:
            json.dump({}, f)
 
def get_settings_json(filename="settings_nodes.json", notExistCreate=True):
    json_file = os.path.join(extension_path, filename)
    if os.path.isfile(json_file):
        f = open(json_file, "rb")
        try:
            load_data = json.load(f)
            return load_data
        except Exception as e:
            print("Error load json file: ",e)
            if notExistCreate:
                f.close()
                os.remove(json_file)
                create_settings_json()
        finally:
            f.close()
            
    return {}    

# Load json file       
@PromptServer.instance.routes.get("/alekpet/loading_node_settings")
async def loadingSettings(request):
    load_data = get_settings_json()                           
    return web.json_response({"settings_nodes": load_data})

# Save data to json file 
@PromptServer.instance.routes.post("/alekpet/save_node_settings")
async def saveSettings(request):
    try:
        with open(file_settings_path, "wb") as f:
            while True:
                chunk = await request.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)        
        
        return web.json_response({"message": "Painter data saved successfully"}, status=200)

    except Exception as e:
        print("Error save json file: ", e)
        
# create file json 
create_settings_json()

class PainterNodeZWB(object):
    @classmethod
    def INPUT_TYPES(self):
        work_dir = folder_paths.get_input_directory()
        images = [img for img in os.listdir(work_dir) if os.path.isfile(os.path.join(work_dir, img))]
        return {"required":
                    {"image": (sorted(images), )},
                }


    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "painter_execute"

    CATEGORY = "2🐕/AlekPet画板中文版"

    def painter_execute(self, image):
        image_path = folder_paths.get_annotated_filepath(image)

        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (image, mask.unsqueeze(0))

    @classmethod
    def IS_CHANGED(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(self, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True
