import click
from mciam.huawei import listuser
import sys,os,json

# 获取用户家目录路径
user_home = os.path.expanduser("~")
config_dir = os.path.join(user_home, ".ciam")

# 确保配置文件夹存在
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

config_file_path = os.path.join(config_dir, "config.json")

def read_config_file():
    config_file_path = os.path.join(config_dir, "config.json")
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)
            return config_data
    else:
        return {}

@click.group()
def main():
    """一个云 IAM 服务的检查工具，用于检测 IAM 是否存在安全风险。"""
    pass

@main.group()
def huawei():
    """华为云 IAM 服务检测，依赖 Hcloud 工具实现,请先安装 Hcloud 工具。

    初始化Hcloud工具请使用命令: hcloud configure set --cli-agree-privacy-statement=true
    """
    pass

@huawei.command()
def SetAKSK():
    """交互式设置 AK 和 SK 并保存到 config.json 文件中"""
    ak = click.prompt("请输入 Access Key")
    sk = click.prompt("请输入 Secret Key")

    config_data = {
        "ak": ak,
        "sk": sk
    }

    # 将配置保存到 config.json 文件中
    with open(config_file_path, "w") as config_file:
        json.dump(config_data, config_file)

    click.echo("Access Key 和 Secret Key 已保存到 $home/.ciam/config.json 文件中")

@huawei.command()
@click.option('--ak', required=False, help='填入 Access Key')
@click.option('--sk', required=False, help='填入 Secret Key')
@click.option('-c','--check', is_flag=True, help='对用户进行检查')
@click.option('-a','--accesskey', is_flag=True, help='获取用户的AK信息')
@click.option('-o','--output', is_flag=True, help='将结果输出为csv文件')
def Listuser(ak,sk,check,accesskey,output):
    """获取用户清单"""
    # 在这里编写获取用户清单的代码
    if not ak:
        config_data = read_config_file()  # 从配置文件读取 AK 和 SK
        ak = config_data.get("ak")
    if not sk:
        config_data = read_config_file()  # 从配置文件读取 AK 和 SK
        sk = config_data.get("sk")
        
    credentials = {
        "ak": ak,
        "sk": sk,
    }
    listuser.list_user(credentials, check, accesskey, output)

if __name__ == '__main__':
    main()
