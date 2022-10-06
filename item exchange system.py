import csv
import os
import pandas as pd
import re

# 尝试对齐pandas中的显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# 检查是否存在用户和物品信息文件，没有则创建一个
def check():
    # 检查是否存在用户信息文件
    if os.path.exists("用户信息.csv"):
        pass
    else:
        df = pd.DataFrame(columns=["用户名", "联系方式", "家庭地址"])
        df.to_csv("./用户信息.csv")
    # 检查是否存在物品信息文件
    if os.path.exists("物品信息.csv"):
        pass
    else:
        df = pd.DataFrame(columns=["物品名称", "物品类别", "物品描述", "用户名", "联系方式", "家庭地址"])
        df.to_csv("./物品信息.csv")


# 通过用户名进行登录并返回用户信息，若首次登录，通过完善联系方式和家庭地址信息来完成注册，并将注册信息储存在用户信息.csv中
def register():
    # 创建用户信息字典
    with open("用户信息.csv", 'r', newline='', encoding="UTF-8") as f1:
        reader = csv.DictReader(f1)
        user_info_dict = {}
        for row in reader:
            user_info_dict[row["用户名"]] = row["联系方式"] + "," + row["家庭地址"]
    # 通过用户名进行登录
    username = input("请输入用户名：")
    if username in user_info_dict.keys():
        print("欢迎回来，%s" % username)
        user_info = [username, user_info_dict[username].split(",")[0], user_info_dict[username].split(",")[1]]
    # 首次登录则进行注册
    else:
        print("请提供联系方式和家庭地址来完成注册")
        input_value = input("请输入联系方式和家庭地址，用逗号分隔")
        phone_number = input_value.split(",")[0]
        address = input_value.split(",")[1]
        with open("用户信息.csv", 'a', newline='', encoding="UTF-8") as f2:
            csv.writer(f2).writerow([username, phone_number, address])
        user_info = [username, phone_number, address]
    # 返回用户信息
    return user_info


# 添加物品信息
def add(user_info):
    input_list = input("请输入物品名称、类别和描述，用逗号分隔").split(",")
    with open("物品信息.csv", 'a', newline='', encoding="UTF-8") as f:
        csv.writer(f).writerow([input_list[0], input_list[1], input_list[2], user_info[0], user_info[1], user_info[2]])
    print("物品信息已添加")


# 删除物品信息，只能删除自己添加的物品
def delete(user_info):
    print("以下是您添加的物品,格式为‘序号：物品名称,物品类别,物品描述’")
    with open("物品信息.csv", 'r', newline='', encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        row_num = 0
        num_of_item = 0
        row_num_list = []
        # 展示自己添加的物品信息和序号
        for row in reader:
            if row["用户名"] == user_info[0]:
                print(str(row_num) + ":" + row["物品名称"] + "," + row["物品类别"] + "," + row["物品描述"])
                num_of_item += 1
                row_num_list.append(row_num)
            row_num += 1
        if num_of_item == 0:
            print("您尚未添加任何物品")
        # 通过序号对应需要删除的物品
        delete_num = input("请输入您要删除的物品的序号")
        if delete_num.isdigit() and int(delete_num) in row_num_list:
            df = pd.read_csv("物品信息.csv")
            new_df = df.drop(index=int(delete_num))
            new_df.to_csv("./物品信息.csv", index=None)
            print("删除完成")
        # 防止删除其他人添加的物品
        else:
            print("非法输入")


# 显示物品列表
def show():
    dataframe = pd.read_csv("物品信息.csv")
    print(dataframe)


# 查找物品信息
def search():
    search_num = input("请输入查找对象：1为物品名称，2为物品类别，3为物品描述，4为用户名，5为联系方式，6为家庭地址")
    if search_num in ["1", "2", "3", "4", "5", "6"]:
        search_info = input("请输入查找信息")
        with open("物品信息.csv", 'r', newline='', encoding="UTF-8") as f:
            reader = csv.reader(f)
            count = 0
            # 用正则表达式匹配,有结果则输出该行信息
            for row in reader:
                if re.search(search_info, row[int(search_num) - 1]) is not None:
                    print(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5])
                    count += 1
            if count != 0:
                print("共查询到%d条结果" % count)
            if count == 0:
                print("未查询到结果")
    else:
        print("非法输入")


# 显示页面菜单
def menu():
    print("""
        —————————————————————物品交换系统———————————————————————--
        |         1 添加物品信息                                  |
        |         2 删除物品信息                                  |
        |         3 显示物品列表                                  |
        |         4 查找物品信息                                  |
        |         0 退出交换系统                                  |
        --------------------------------------------------------
        """)


# 主程序
def main():
    check()
    print("欢迎进入物品交换系统")
    user_info = register()
    flag_on = True
    while flag_on:
        menu()
        option = input("请选择：")  # 选择菜单项
        if option.isdigit():
            option = int(option)
            if option == 0:  # 退出选择界面
                print("您已经退出物品交换系统！")
                flag_on = False
            elif option == 1:  # 添加物品信息
                add(user_info)
            elif option == 2:  # 删除物品信息
                delete(user_info)
            elif option == 3:  # 显示物品列表
                show()
            elif option == 4:  # 查找物品信息
                search()


if __name__ == "__main__":
    main()
