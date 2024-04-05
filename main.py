import os
import time
import requests
import requests
import hashlib
import json
from tqdm import tqdm
from urllib.parse import urljoin

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("请选择目标：".center(50))
        print("     1. Forge       ||       4. Optifine".ljust(50))
        print("     2. Fabric      ||       5. Liteloader".ljust(50))
        print("     3. MineCraft   ||       6. 退出".ljust(50))
        print("")
        print("")
        choice = input("请输入对应的数字：")

        if choice == "1":
            forge()
        elif choice == "2":
            Fabric()
        elif choice == "3":
            MineCraft()
        elif choice == "4":
            Optifine()
        elif choice == "5":
            Liteloader()
        elif choice == "6":
            print("准备退出")
            print("如果你同为MC玩家，你也热爱PVP游戏之类的话\n可以加入我们的群聊: 680900369")
            time.sleep(3)
            exit()
        else:
            print("无效的选择，请重新输入。")
            time.sleep(1.5)
def Optifine():
    def get_optifine_files():
        url = "https://optifine.cn/api"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("files", [])
        else:
            print(f"获取OptiFine文件信息失败。状态码：{response.status_code}")
            return []


    def calculate_md5(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


    def download_optifine_file(file_info, selected_version):
        file_name = file_info['name']
        version = file_info['version']

        if version != selected_version:
            return

        download_url = f"https://optifine.cn/download/{file_name}"
        response = requests.get(download_url)

        if response.status_code == 200:
            directory = f"versions/Optifine/{version}"
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            md5_value = calculate_md5(file_path)
            with open(os.path.join(directory, "md5.txt"), 'a') as f:
                f.write(f"{file_name}: {md5_value}\n")

            print(f"下载文件 {file_name} 成功！")
        else:
            print(f"下载文件 {file_name} 失败。状态码：{response.status_code}")

    def a():
        optifine_files = get_optifine_files()

        if optifine_files:
            # 提示用户选择版本号
            print("可用版本号列表：")
            for file_info in optifine_files:
                print(file_info['version'])
            selected_version = input("请输入要下载的版本号: ")

            for file_info in optifine_files:
                download_optifine_file(file_info, selected_version)
        else:
            print("没有找到OptiFine文件。")
    a()
def MineCraft():
    def download_file(url, filename):
        # 检查文件是否已经存在
        if os.path.exists(filename):
            print(f"文件 {filename} 已经下载.")
            return

        # 下载文件
        response = requests.get(url)

        # 创建文件的目录
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # 将文件保存到硬盘
        with open(filename, 'wb') as file:
            file.write(response.content)

        # 计算文件的SHA-256哈希值
        with open(filename, 'rb') as file:
            bytes = file.read() # 读取整个文件为字节
            readable_hash = hashlib.sha256(bytes).hexdigest()
            print(f'文件的SHA-256哈希值是: {readable_hash}')

        # 将哈希值保存到一个文件中
        with open(os.path.join(os.path.dirname(filename), 'sha256.txt'), 'w') as file:
            file.write(readable_hash)

    def download_minecraft_versions():
        # 下载并解析JSON文件
        response = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
        version_manifest = json.loads(response.text)

        # 提示用户选择版本号
        print("可用版本号列表：")
        for version_info in version_manifest['versions']:
            print(version_info['id'])

        version = input("请输入要下载的版本号: ")

        # 遍历所有的版本
        for version_info in version_manifest['versions']:
            if version_info['id'] == version:
                print(f"正在下载版本 {version_info['id']}...")
                # 获取每个版本的详细信息
                response = requests.get(version_info['url'])
                version_detail = json.loads(response.text)
                # 下载jar文件
                download_file(version_detail['downloads']['server']['url'], f'versions/Minecraft/{version_info["id"]}/{version_info["id"]}.jar')
                return

        print(f"找不到版本号为 {version} 的Minecraft版本。")
    download_minecraft_versions()

def Liteloader():
    def download_file(url, filename):
        # 下载文件
        response = requests.get(url)

        # 检查目录是否存在，不存在则创建
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # 将文件保存到硬盘
        with open(filename, 'wb') as file:
            file.write(response.content)

        # 计算文件的SHA-256哈希值
        with open(filename, 'rb') as file:
            bytes = file.read()  # 读取整个文件为字节
            readable_hash = hashlib.sha256(bytes).hexdigest()
            print(f'文件的SHA-256哈希值是: {readable_hash}')
        # 将哈希值保存到一个文件中
        with open(filename + '.txt', 'w') as file:
            file.write(readable_hash)

    def download_liteloader_versions():
        # 下载并解析 JSON 文件
        response = requests.get('http://dl.liteloader.com/versions/versions.json')
        liteloader_data = json.loads(response.text)

        # 确保版本信息存在且是一个字典
        if 'versions' in liteloader_data and isinstance(liteloader_data['versions'], dict):
            # 提示用户选择版本号
            print("可用版本号列表：")
            for version in liteloader_data['versions']:
                print(version)

            version = input("请输入要下载的版本号: ")

            # 检查用户输入的版本号是否存在
            if version not in liteloader_data['versions']:
                print(f"版本号 {version} 不存在。")
                return

            version_info = liteloader_data['versions'][version]

            print(f"正在下载版本 {version}...")

            # 获取版本详细信息
            if 'repo' in version_info and 'url' in version_info['repo']:
                repo_url = version_info['repo']['url']

                # 创建版本号文件夹
                version_folder = os.path.join('./versions/LiteLoader', version)
                os.makedirs(version_folder, exist_ok=True)

                # 下载并保存 jar 文件
                jar_filename = f"{version}.jar"
                download_file(f"{repo_url}/{jar_filename}", os.path.join(version_folder, jar_filename))

                # 下载并保存校验和文件（假设存在）
                if 'checksum' in version_info and 'url' in version_info['checksum']:
                    checksum_filename = f"{version}.checksum"
                    download_file(f"{repo_url}/{version_info['checksum']['url']}", os.path.join(version_folder, checksum_filename))
                else:
                    print(f"版本 {version} 没有校验和文件。")
            else:
                print(f"版本 {version} 的信息中缺少 'repo' 字段或 'url' 字段。")
        else:
            print("版本信息不是一个字典。")
    download_liteloader_versions()
def Fabric():
    os.system('cls' if os.name == 'nt' else 'clear')
    # 创建目录
    if not os.path.exists('versions/Fabric'):
        os.makedirs('versions/Fabric')

    # 获取版本信息
    print("正在获取游戏版本")
    response = requests.get("https://meta.fabricmc.net/v2/versions")
    data = response.json()

    # 用户输入要下载的版本号
    version = input('请输入要下载的版本号: ')

    # 检查'game'键是否存在
    if 'game' not in data:
        print("没有找到任何游戏版本。响应数据: {data}")

    # 是否找到目标版本的标志
    found_target_version = False

    # 遍历每个游戏版本
    for game_version in data['game']:
        game_version_number = game_version['version']

        # 如果游戏版本号与用户输入的版本号匹配，则进行下载
        if game_version_number == version:
            found_target_version = True
            print(f"正在处理游戏版本: {game_version_number}")

            # 获取每个游戏版本的加载器版本信息
            loader_response = requests.get(f"https://meta.fabricmc.net/v2/versions/loader/{game_version_number}")
            loader_data = loader_response.json()

            # 遍历每个加载器版本
            for loader_version in loader_data:
                loader_version_number = loader_version['loader']['version']
                print(f"正在处理加载器版本: {loader_version_number}")

                # 获取下载信息
                download_url = f"https://meta.fabricmc.net/v2/versions/loader/{game_version_number}/{loader_version_number}/server/jar"
                print(f"正在从以下地址下载: {download_url}")
                file_response = requests.get(download_url)
                file_path = f"versions/fabric/{game_version_number}/{loader_version_number}/server.jar"
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
                print(f"成功下载到: {file_path}")

                # 计算md5
                md5 = hashlib.md5()
                md5.update(file_response.content)
                md5_value = md5.hexdigest()

                # 保存md5到txt文件
                with open(f"{file_path}.md5.txt", 'w') as f:
                    f.write(md5_value)
                print(f"MD5值为: {md5_value}")
            break

    if not found_target_version:
        print(f"找不到版本号为 {version} 的Fabric版本。")
        time.sleep(1.5)

def forge():
    def get_forge_versions(minecraft_version):
        url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{minecraft_version}"
        response = requests.get(url)
        if response.ok:
            versions = response.json()
            return versions
        else:
            print("获取Forge版本失败")
            return None

    def get_existing_forge_versions(subfolder):
        existing_versions = set()
        for root, dirs, files in os.walk(subfolder):
            for file in files:
                if file.startswith("forge-") and file.endswith("-installer.jar"):
                    version = file.split("-")[2]
                    existing_versions.add(version)
        return existing_versions

    def download_forge_installer(minecraft_version, forge_version, subfolder):
        url = f"https://bmclapi2.bangbang93.com/forge/download"
        params = {
            "mcversion": minecraft_version,
            "version": forge_version,
            "category": "installer",
            "format": "jar"
        }
        response = requests.get(url, params=params)
        if response.ok:
            download_url = response.url
            print(f"重定向链接: {download_url}")
            filename = f"forge-{minecraft_version}-{forge_version}-installer.jar"
            download_url = urljoin(download_url, filename)
            print(f"下载链接: {download_url}")
            response_download = requests.get(download_url, stream=True)
            if response_download.ok:
                if not os.path.exists(subfolder):
                    os.makedirs(subfolder)
                filepath = os.path.join(subfolder, filename)
                total_size = int(response_download.headers.get('content-length', 0))
                with open(filepath, 'wb') as file, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response_download.iter_content(chunk_size=1024):
                        size = file.write(chunk)
                        bar.update(size)
                print(f"{filepath} 下载成功。")
            else:
                print(f"下载Forge安装器失败：{download_url}")
        else:
            print(f"获取Forge下载链接失败：{url}")

    minecraft_version = str(input("请输入要下载的版本号: "))
    versions = get_forge_versions(minecraft_version)
    if versions:
        subfolder = f"versions/Forge/{minecraft_version}"
        existing_versions = get_existing_forge_versions(subfolder)
        for version_info in versions:
            forge_version = version_info['version']
            if forge_version not in existing_versions:
                download_forge_installer(minecraft_version, forge_version, subfolder)
            else:
                print(f"版本 “{forge_version}” 已存在，跳过下载。")
    else:
        print(f"“ {minecraft_version}” 版本没有找到Forge版本。")
        time.sleep(1.5)

if __name__ == "__main__":
    main()
