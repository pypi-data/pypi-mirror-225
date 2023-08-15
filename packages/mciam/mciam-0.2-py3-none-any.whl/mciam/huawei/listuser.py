import sys, json, os
from tabulate import tabulate
from datetime import datetime, timedelta
import wcwidth,re,csv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from command.run import execute_command  # 注意这里的导入语法

ACCESS_MODE_TRANSLATIONS = {
    "console": "控制台访问",
    "default": "默认访问",
    "programmatic": "编程访问"
}

def cspm_check_user(user_info):
    check_userinfo = []
    check_userinfo.append(user_info[0])
    access_mode = user_info[3]
    last_login_time = user_info[4]
    modify_pwd_time = user_info[5]

    # 检查IAM用户是否使用了单一访问方式
    if access_mode == "programmatic" or access_mode == "console":
        check_userinfo.append("True")
    else:
        check_userinfo.append("False")
        # return False, "IAM用户使用了多个访问方式"
    if access_mode == "default" or access_mode == "console":
        # 检查用户是否超过30天未活动
        if last_login_time:
            last_login_time = re.sub(r"\.\d+", "", last_login_time)
            last_login_time = datetime.strptime(last_login_time, "%Y-%m-%d %H:%M:%S") if last_login_time else None
            if datetime.now() - last_login_time > timedelta(days=30):
                check_userinfo.append("True")
                #  return False, "IAM用户长时间未活动（超过30天）"
            else:
                check_userinfo.append("False")
        if modify_pwd_time:
            # 检查用户是否超过90天未修改密码
            modify_pwd_time_str = str(modify_pwd_time)  # 转换为字符串
            modify_pwd_time_str = re.sub(r"\.\d+", "", modify_pwd_time_str)
            modify_pwd_time = datetime.strptime(modify_pwd_time_str, "%Y-%m-%d %H:%M:%S") if modify_pwd_time_str else None
            if datetime.now() - modify_pwd_time > timedelta(days=90):
                check_userinfo.append("True")
                # return False, "IAM用户长时间未修改密码（超过90天）"
            else:
                check_userinfo.append("False")
    else:
        check_userinfo.append("Skip")
        check_userinfo.append("Skip")
    return check_userinfo

# 获取用户的AK信息
def get_user_ak_detail(credentials, ak,user_name):
    command = "hcloud IAM ShowPermanentAccessKey --cli-region=cn-north-4 --cli-access-key={} --cli-secret-key={} --access_key={}".format(credentials["ak"], credentials["sk"], ak)
    output, error, return_code = execute_command(command)
    if return_code == 0:
        data = json.loads(output)
        ak_info = [
            user_name,
            data["credential"]["access"],
            data["credential"]["status"],
            data["credential"]["last_use_time"],
        ]
        return ak_info
    else:
        print("Command execution error:", error)

# 获取用户的AK 列表
def get_user_token(credentials, user_id, user_name):
    command = "hcloud IAM ListPermanentAccessKeys --cli-region=cn-north-4 --cli-access-key={} --cli-secret-key={} --user_id={}".format(credentials["ak"], credentials["sk"], user_id)
    output, error, return_code = execute_command(command)
    accesskeys = []
    if return_code == 0:
        data = json.loads(output).get("credentials", [])
        for item in data:
            ak_info = get_user_ak_detail(credentials, item["access"],user_name)
            accesskeys.append(ak_info)
    else:
        print("Command execution error:", error)
    return accesskeys

def show_user(credentials, user_id):
    command = "hcloud IAM ShowUser --cli-region=cn-north-4 --cli-access-key={} --cli-secret-key={} --user_id={}".format(credentials["ak"], credentials["sk"], user_id)
    output, error, return_code = execute_command(command)
    if return_code == 0:
        data = json.loads(output)
        user_info = [
            data["user"]["name"],
            data["user"]["id"],
            data["user"]["enabled"],
            data["user"]["access_mode"],
            data["user"]["last_login_time"],
            data["user"]["modify_pwd_time"],
        ]
        return user_info
    else:
        return None
    

def list_user(credentials, perform_cspm_check, user_ak, output_csv):
    command = "hcloud IAM KeystoneListUsers --cli-region=cn-north-4 --cli-access-key={} --cli-secret-key={}".format(credentials["ak"], credentials["sk"])
    output, error, return_code = execute_command(command)
    if return_code == 0:
        try:
            data = json.loads(output)
            user_data = []
            if perform_cspm_check:
                # IAM 服务的 CSPM 检查
                for user in data.get("users", []):
                    user_id = user["id"]
                    user_info = show_user(credentials, user_id)
                    if user_info:
                        user_data.append(cspm_check_user(user_info))
                headers = ["用户名", "使用单一访问方式","超过30天未活动","超过90天未修改密码"]
            elif user_ak:
                # IAM 服务的 AK 列表
                undata = []
                for user in data.get("users", []):
                    user_id = user["id"]
                    undata.append(get_user_token(credentials, user_id, user["name"]))
                # 处理日期格式和数据重组
                for group in undata:
                    for item in group:
                        if datetime.now() - datetime.strptime(item[3], "%Y-%m-%dT%H:%M:%S.%fZ") > timedelta(days=90):
                            item.append("不合规")
                        else:
                            item.append("合规")
                        item[3] = datetime.strptime(item[3], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                        user_data.append(item)
                headers = ["用户名","Access Key", "状态", "最后使用时间","超过90天未使用"]
            else:
                # IAM 服务的用户列表
                for user in data.get("users", []):
                    user_id = user["id"]
                    user_info = show_user(credentials, user_id)
                    if user_info:
                        user_data.append(user_info)
                headers = ["用户名", "ID", "用户状态", "访问方式", "最后登录时间", "最后修改密码时间"]

            if output_csv:
                csv_filename = "huawei_iam.csv"
                with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(headers)
                    csv_writer.writerows(user_data)
                print("CSV 文件已保存为:", csv_filename)
            else:
                table = tabulate(user_data, headers=headers, tablefmt="grid", colalign=("left",))
                print(table)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response:", e)
    else:
        print("Command execution error:", error)

if __name__ == "__main__":
    perform_cspm_check = True
    # list_user(credentials,perform_cspm_check)
    get_user_token(credentials, "0fe9d5e86a344648b2f6c843770f890f")