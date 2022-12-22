# "你帮我助"物品交换信息系统
# 作者：孙翊然
import PySimpleGUI as sg
import os
import pandas as pd
import csv
import re


def check():
    # 检查是否存在用户信息文件
    if os.path.exists("用户信息.csv"):
        pass
    else:
        df = pd.DataFrame(columns=["用户名", "密码", "联系方式", "家庭地址"], index=None)
        df.to_csv("./用户信息.csv")
    # 检查是否存在注册待批准用户信息文件
    if os.path.exists("注册待批准用户信息.csv"):
        pass
    else:
        df = pd.DataFrame(columns=["用户名", "密码", "联系方式", "家庭地址"], index=None)
        df.to_csv("./注册待批准用户信息.csv")
    # 检查是否存在管理员信息文件
    if os.path.exists("管理员信息.csv"):
        pass
    else:
        df = pd.DataFrame(columns=["用户名", "密码"], index=None)
        df.to_csv("./管理员信息.csv")


class Item:  # 物品类
    def __init__(self, class_name, name, item_info, address, phone_num):
        self.class_name = class_name
        self.name = name
        self.item_info = item_info
        self.address = address
        self.phone_num = phone_num

    def search_item_attribute(self, class_name):  # 查找某一类型物品的属性
        with open(class_name + ".csv", "r", encoding="UTF-8") as f:
            attribute_list = f.readline().strip().split(",")
            attribute_str = ""
            for i in range(6, len(attribute_list)):
                attribute_str += attribute_list[i] + " "
        return attribute_str

    def save_class_name(self, class_name):  # 保存当期物品类型信息
        self.class_name = class_name

    def search_class_name(self):  # 查询当期物品类型信息
        return self.class_name


class User:  # 普通用户类
    def __init__(self, username, password, address, phone_num):
        self.username = username
        self.password = password
        self.address = address
        self.phone_num = phone_num

    def login(self, user, password):  # 普通用户登录
        df = pd.read_csv("用户信息.csv")  # 读取用户信息文件
        username_list = df["用户名"].tolist()
        password_list = df["密码"].tolist()
        if user in username_list and password in password_list:  # 通过文件中是否存在用户名和密码判断登录成功与否
            self.username = user  # 保存用户名
            return True
        else:
            return False

    def search_username(self):  # 查询用户名
        return self.username

    def register(self, username, password, address, phone_num):  # 普通用户注册
        if username != "" and password != "" and address != "" and phone_num != "":  # 注册信息写入注册待批准用户信息文件
            with open("注册待批准用户信息.csv", 'a', newline='', encoding="UTF-8") as f:
                csv.writer(f).writerow(
                    [username, password, address, phone_num])
                f.close()
            return True
        else:  # 信息若有一项未输入，则不能注册
            return False

    def add(self, class_name, information):  # 添加物品信息
        with open(class_name + ".csv", 'a', newline='', encoding="UTF-8") as f:
            f.write(information + "\n")
            f.close()

    def delete(self, class_name, information):  # 删除物品信息
        count = 0
        with open(class_name + ".csv", 'r', encoding="UTF-8") as f:  # 找到删除信息对应的行数
            reader = csv.reader(f)
            for row in reader:
                if information == row:
                    break
                else:
                    count += 1

        f.close()
        df = pd.read_csv(class_name + ".csv")
        df = df.drop([count - 1])
        df.to_csv(class_name + ".csv", index=None)  # 重新写入删除后的物品信息

    def show(self, class_name):  # 展示物品信息
        with open(class_name + ".csv", "r", encoding="UTF-8") as f:  # 只找出当前用户添加的物品
            reader = csv.reader(f)
            class_name_str = f.readline()
            info_list = []
            for row in reader:
                info_list.append(row)
        return class_name_str, info_list

    def search(self, class_name, name, explanation):  # 用户查找物品信息
        with open(class_name + ".csv", "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            class_name_str = f.readline()
            info_list = []
            for row in reader:
                if name == "":  # 只查找说明
                    if re.search(explanation, row[1]):
                        info_list.append(row)
                elif explanation == "":  # 只查找名称
                    if re.search(name, row[0]):
                        info_list.append(row)
                else:  # 名称和说明都查找
                    if re.search(name, row[0]) and re.search(explanation, row[1]):
                        info_list.append(row)
        return class_name_str, info_list


class Admin:  # 管理员类
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def admin_login(self, username, password):  # 管理员登录
        df = pd.read_csv("管理员信息.csv")  # 读取管理员信息文件
        username_list = df["用户名"].tolist()
        password_list = df["密码"].tolist()
        if username in username_list and password in password_list:  # 通过文件中是否存在用户名和密码判断登录成功与否
            return True
        else:
            return False

    def disapprove(self, num):  # 管理员不批准注册
        df = pd.read_csv("注册待批准用户信息.csv")
        df = df.drop([num - 1])  # 从待批准用户信息文件中删除该条信息
        df.to_csv("注册待批准用户信息.csv", index=None)

    def approve(self, num, info):  # 管理员批准注册
        df = pd.read_csv("注册待批准用户信息.csv")
        df = df.drop([num - 1])  # 从待批准用户信息文件中删除该条信息
        df.to_csv("注册待批准用户信息.csv", index=None)
        with open("用户信息.csv", "a") as f:  # 将通过注册的申请写入用户信息
            f.write(info + '\n')
            f.close()

    def create_new_item(self, name, attribute):  # 管理员创建新的物品类型
        with open("物品类型.txt", "r", encoding="UTF-8") as f:  # 判断是否已存在该物品类型
            name_list = []
            for line in f:
                name_list.append(line.strip())
        if name in name_list:  # 存在则返回否
            return False
        else:  # 不存在则向物品类型文件中添加该物品类型，并创建该物品类型存放物品信息的csv文件
            with open("物品类型.txt", "a", encoding="UTF-8") as f:
                f.write(name + "\n")
                f.close()
            with open(name + ".csv", "w", encoding="UTF-8") as f:
                writer = csv.writer(f)
                f.write('物品名称,物品说明,物品所在地址,联系人用户名,联系人手机,邮箱,' + attribute + "\n")
                f.close()
            return True

    def add_attribute(self, class_name, attribute):  # 管理员为物品类型添加属性
        df1 = pd.read_csv(class_name + ".csv")
        df2 = pd.DataFrame(columns=[attribute], index=None)
        new_df = df1.join(df2)  # 合并新旧属性
        new_df.to_csv(class_name + ".csv", index=None)

    def delete_attribute(self, class_name, attribute):  # 管理员为物品类型删除属性
        df1 = pd.read_csv(class_name + ".csv")
        new_df = df1.drop(columns=[attribute])  # 删除属性
        new_df.to_csv(class_name + ".csv", index=None)

    def detele_class(self, class_name):  # 管理员删除物品类型
        with open("物品类型.txt", "r", encoding="UTF-8") as f:  # 读取物品类型文件
            name_list = []
            for line in f:
                name_list.append(line.strip())
        f.close()
        name_list.remove(class_name)  # 去掉要删除的物品类型
        with open("物品类型.txt", "w", encoding="UTF-8") as f:  # 重新写入物品类型
            for i in name_list:
                f.write(i + "\n")
        f.close()
        os.remove("./" + class_name + '.csv')


class Window:  # 窗口类
    def __init__(self, theme='DarkAmber'):
        self.theme = theme

    def make_window_start(self):  # 创建开始界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("欢迎来到你帮我助系统")],
                  [sg.Text("请问您是")],
                  [sg.Button("普通用户"), sg.Button("管理员")]]

        return sg.Window('你帮我助系统', layout, finalize=True)

    def make_window_user_login(self):  # 创建普通用户登录界面
        sg.theme('DarkAmber')
        layout1 = [[sg.Text('用户名'), sg.Input(key='_USER_')],
                   [sg.Text('密码'), sg.Input(key='_PWD_')],
                   [sg.Button('登录'), sg.Button('注册')]]

        return sg.Window('普通用户登录/注册', layout1, finalize=True)

    def make_window_admin_login(self):  # 创建管理员登录界面
        sg.theme('DarkAmber')
        layout2 = [[sg.Text('用户名'), sg.Input(key='_USER_')],
                   [sg.Text('密码'), sg.Input(key='_PWD_')],
                   [sg.Button('管理员登录')]]

        return sg.Window('管理员登录', layout2, finalize=True)

    def make_window_user_register(self):  # 创建普通用户注册界面
        sg.theme('DarkAmber')
        layout3 = [[sg.Text('用户名'), sg.Input(key='_USER_')],
                   [sg.Text('密码'), sg.Input(key='_PWD_')],
                   [sg.Text('联系方式'), sg.Input(key='_PHONE_')],
                   [sg.Text('家庭地址'), sg.Input(key='_ADD_')],
                   [sg.Button('确定注册'), sg.Button('返回登录界面')]]

        return sg.Window('普通用户注册', layout3, finalize=True)

    def make_window_admin_menu(self):  # 创建管理员菜单
        sg.theme('DarkAmber')
        layout = [[sg.Button("批准注册用户信息")],
                  [sg.Button("设置新的物品类型")],
                  [sg.Button("修改(删除)物品类型")],
                  [sg.Button('退出')]]
        return sg.Window('管理员菜单', layout, finalize=True)

    def make_window_admin_approve_menu(self):  # 创建管理员通过用户注册菜单界面
        register_info_list = []
        with open("注册待批准用户信息.csv", 'r', newline='', encoding="UTF-8") as f:  # 读取文件，生成注册待批准用户信息列表
            lines = f.readlines()
            count = 1
            for line in lines[1:]:
                if line != "":
                    register_info_list.append([count, line])
                    count += 1

        sg.theme('DarkAmber')
        layout = [[sg.Text('注册待批准用户信息')],
                  [sg.Text('格式：序号 {用户名,密码,联系方式,家庭地址}')],
                  [sg.Listbox(values=register_info_list, size=(60, None), key='-LIST-', enable_events=True)],
                  [sg.Button("选择"), sg.Button('返回管理员菜单')]]
        return sg.Window('批准注册用户信息', layout, finalize=True)

    def make_window_admin_approve(self):  # 创建管理员通过用户注册界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("序号：" + str(num))],
                  [sg.Text("信息" + info)],
                  [sg.Button("通过"), sg.Button("不通过"), sg.Button("返回通过用户注册界面")]]
        return sg.Window('是否批准注册用户信息', layout, finalize=True)

    def make_window_admin_create_new_item(self):  # 创建管理员设置新物品类型界面
        sg.theme('DarkAmber')
        layout = [[sg.Text('物品类型'), sg.Input(key='_NAME_')],
                  [sg.Text('属性（用英文逗号分隔）'), sg.Input(key='_ATT_')],
                  [sg.Button("确定设置新物品"), sg.Button("返回管理员菜单")]]
        return sg.Window('设置新物品类型', layout, finalize=True)

    def make_window_admin_modify_item_menu(self):  # 创建管理员修改物品类型菜单界面
        with open('物品类型.txt', "r", encoding="UTF-8") as f:  # 读取文件，生成物品类型信息列表
            name_list = []
            for line in f:
                name_list.append(line.strip())
        sg.theme('DarkAmber')
        layout = [[sg.Text('请选择要修改/删除的物品类型')],
                  [sg.Listbox(values=name_list, size=(30, None), key='-ITEMLIST-', enable_events=True)],
                  [sg.Button("选择"), sg.Button('返回管理员菜单')]]
        return sg.Window("修改(删除)物品类型菜单", layout, finalize=True)

    def make_window_confirm_exit(self):  # 创建退出系统确认界面
        sg.theme('DarkAmber')
        layout = [[sg.Text('请问您确定要退出系统吗')],
                  [sg.Button("确定"), sg.Button('取消')]]
        return sg.Window("退出确认", layout, finalize=True)

    def make_window_admin_modify_item_choice(self, attribute):  # 创建管理员修改物品类型选项界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("该物品已有属性为：")],
                  [sg.Text(attribute)],
                  [sg.Button("增加属性"), sg.Input(key='_ADD_')],
                  [sg.Button("删除属性"), sg.Input(key='_DELETE_')],
                  [sg.Button("删除该物品类型")],
                  [sg.Button('返回')]]
        return sg.Window("修改(删除)物品类型选项", layout, finalize=True)

    def make_window_admin_confirm_delete_class(self, class_name):  # 创建管理员确认删除物品类型界面
        sg.theme('DarkAmber')
        layout = [[sg.Text('请问您确定要删除物品类型 ' + class_name + ' 吗')],
                  [sg.Button("确定"), sg.Button('取消')]]
        return sg.Window("删除物品类型确认", layout, finalize=True)

    def make_window_user_menu(self):  # 创建用户菜单界面
        with open('物品类型.txt', "r", encoding="UTF-8") as f:  # 读取文件，生成物品类型信息列表
            name_list = []
            for line in f:
                name_list.append(line.strip())
        sg.theme('DarkAmber')
        layout = [[sg.Text('请选择要操作的物品类型，支持增加、查询、修改、删除操作')],
                  [sg.Listbox(values=name_list, size=(30, None), key='-ITEMLIST-', enable_events=True)],
                  [sg.Button("选择"), sg.Button('退出')]]
        return sg.Window("用户菜单", layout, finalize=True)

    def make_window_user_menu_choice(self):  # 创建用户操作选项界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("请选择操作类型")],
                  [sg.Button("添加该类型物品")],
                  [sg.Button("删除该类型物品")],
                  [sg.Button("展示该类型所有物品")],
                  [sg.Button("查找该类型特定物品")],
                  [sg.Button('返回用户菜单')]]
        return sg.Window("物品操作选项", layout, finalize=True)

    def make_window_user_add(self, attribute):  # 创建用户添加物品界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("多个内容之间请用英文逗号隔开")],
                  [sg.Button("物品名称"), sg.Input(key='_NAME_')],
                  [sg.Button("物品说明"), sg.Input(key='_EXPL_')],
                  [sg.Button("物品所在地址"), sg.Input(key='_ADD_')],
                  [sg.Button("联系人手机"), sg.Input(key='_PHONUM_')],
                  [sg.Button("邮箱"), sg.Input(key='_EMAIL_')],
                  [sg.Button(attribute), sg.Input(key='_ATT_')],
                  [sg.Button("确定"), sg.Button('返回')]]
        return sg.Window("添加物品", layout, finalize=True)

    def make_window_user_delete(self, class_name, user):  # 创建用户删除物品信息界面
        with open(class_name + ".csv", "r", encoding="UTF-8") as f:  # 只找出当前用户添加的物品
            class_name_str = f.readline()
            reader = csv.reader(f)
            info_list = []
            for row in reader:
                if row[3] == user:
                    info_list.append(row)
        sg.theme('DarkAmber')
        layout = [[sg.Text("以下为您添加的物品，您只能删除自己添加的物品")],
                  [sg.Text(class_name)],
                  [sg.Text("属性为")],
                  [sg.Text(class_name_str)],
                  [sg.Listbox(values=info_list, size=(80, None), key='-LIST-', enable_events=True)],
                  [sg.Button("选择"), sg.Button('返回')]]
        return sg.Window('删除物品信息', layout, finalize=True)

    def make_window_user_show(self, class_name, class_name_str, info_list):  # 创建物品展示界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("已展示所有类型为" + class_name + "的物品")],
                  [sg.Text("属性为")],
                  [sg.Text(class_name_str)],
                  [sg.Listbox(values=info_list, size=(80, None))],
                  [sg.Button('返回')]]
        return sg.Window('显示物品信息', layout, finalize=True)

    def make_window_user_search(self):  # 创建物品查找界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("请输入查询内容，支持名称和说明同时查询")],
                  [sg.Button("物品名称"), sg.Input(key='_NAME_')],
                  [sg.Button("物品说明"), sg.Input(key='_EXPL_')],
                  [sg.Button("查找"), sg.Button('返回')]]
        return sg.Window("查找物品选项", layout, finalize=True)

    def make_window_user_search_show(self, class_name_str, info_list):  # 创建物品展示界面
        sg.theme('DarkAmber')
        layout = [[sg.Text("搜索结果如下：")],
                  [sg.Text("属性为")],
                  [sg.Text(class_name_str)],
                  [sg.Listbox(values=info_list, size=(80, None))],
                  [sg.Button('返回查找界面')]]
        return sg.Window('显示查找的物品信息', layout, finalize=True)


def main():  # 主程序
    global num  # 全局变量num,用于保存注册待批准信息编号
    global info  # 全局变量info,用于保存注册待批准信息内容
    check()  # 检查所需文件是否存在
    user1 = User(1, 1, 1, 1)
    window1 = Window()
    admin1 = Admin(1, 1)
    item1 = Item(1, 1, 1, 1, 1)
    window_user_login = None  # 声明窗口
    window_admin_login = None
    window_user_register = None
    window_admin_menu = None
    window_admin_approve_menu = None
    window_admin_approve = None
    window_admin_create_new_item = None
    window_admin_confirm_exit = None
    window_admin_modify_item_menu = None
    window_admin_modify_item_choice = None
    window_admin_confirm_delete_class = None
    window_user_menu = None
    window_user_menu_choice = None
    window_user_confirm_exit = None
    window_user_add = None
    window_user_delete = None
    window_user_show = None
    window_user_search = None
    window_user_search_show = None
    window_start = window1.make_window_start()  # 创建开始界面

    while True:
        window, event, value = sg.read_all_windows()
        if event == sg.WIN_CLOSED:  # 退出程序
            break
        if event == "确定" and window_admin_confirm_exit:
            break
        if event == "确定" and window_user_confirm_exit:
            break
        if event == '普通用户':  # 普通用户选择普通用户登录
            window_start.close()
            window_start = None
            window_user_login = window1.make_window_user_login()  # 生成普通用户登录界面
        if event == '登录':  # 普通用户选择登录
            user = value['_USER_']
            password = value['_PWD_']
            if user1.login(user, password):  # 提示登录成功与否
                window_user_login.close()
                window_user_login = None
                window_user_menu = window1.make_window_user_menu()
            else:
                sg.popup("用户名或密码不正确")
        if event == "退出" and window_user_menu:  # 用户选择退出系统
            window_user_menu.close()
            window_user_menu = None
            window_user_confirm_exit = window1.make_window_confirm_exit()  # 生成退出确认界面
        if event == "取消" and window_user_confirm_exit:  # 用户选择不退出
            window_user_confirm_exit.close()
            window_user_confirm_exit = None
            window_user_menu = window1.make_window_user_menu()
        if window_user_menu and event == "选择" and value['-ITEMLIST-']:  # 用户选择其中一种物品类型
            class_name = value['-ITEMLIST-'][0]
            item1.save_class_name(class_name)  # 储存物品类型信息
            window_user_menu.close()
            window_user_menu = None
            window_user_menu_choice = window1.make_window_user_menu_choice()
        if event == "返回用户菜单" and window_user_menu_choice:  # 用户返回用户菜单
            window_user_menu_choice.close()
            window_user_menu_choice = None
            window_user_menu = window1.make_window_user_menu()
        if event == "添加该类型物品" and window_user_menu_choice:  # 用户选择添加物品
            window_user_menu_choice.close()
            window_user_menu_choice = None
            class_name = item1.search_class_name()
            attribute = item1.search_item_attribute(class_name)
            window_user_add = window1.make_window_user_add(attribute)  # 添加物品
        if event == "返回" and window_user_add:  # 用户返回上一级界面
            window_user_add.close()
            window_user_add = None
            window_user_menu_choice = window1.make_window_user_menu_choice()
        if event == "确定" and window_user_add and value["_NAME_"] != "" and value['_EXPL_'] != "" and value[
            '_ADD_'] != "" and value['_PHONUM_'] != "" and value['_EMAIL_'] != "":  # 用户确定添加信息且信息不为空
            class_name = item1.search_class_name()
            name = value["_NAME_"]
            explain = value['_EXPL_']
            user = user1.search_username()
            address = value['_ADD_']
            phone_num = value['_PHONUM_']
            email = value['_EMAIL_']
            attribute_str = value['_ATT_']
            information = name + "," + explain + "," + address + "," + user + "," + phone_num + "," + email + "," + attribute_str  # 生成物品信息字符串
            user1.add(class_name, information)  # 添加物品信息
            sg.popup("添加成功")
        if event == "删除该类型物品":  # 用户选择删除物品
            window_user_menu_choice.close()
            window_user_menu_choice = None
            class_name = item1.search_class_name()
            user = user1.search_username()
            window_user_delete = window1.make_window_user_delete(class_name, user)  # 生成删除物品界面
        if event == "选择" and window_user_delete and value['-LIST-'] != "":  # 用户选择某一项物品进行删除
            class_name = item1.search_class_name()
            information = value['-LIST-'][0]
            print(information)
            user = user1.search_username()
            user1.delete(class_name, information)  # 删除该物品
            sg.popup("删除成功")
            window_user_delete.close()
            window_user_delete = None
            window_user_delete = window1.make_window_user_delete(class_name, user)  # 返回删除物品界面
        if event == "返回" and window_user_delete:  # 用户返回选项界面
            window_user_delete.close()
            window_user_delete = None
            window_user_menu_choice = window1.make_window_user_menu_choice()
        if event == "展示该类型所有物品":  # 用户选择展示物品
            window_user_menu_choice.close()
            window_user_menu_choice = None
            class_name = item1.search_class_name()
            class_name_str, info_list = user1.show(class_name)
            window_user_show = window1.make_window_user_show(class_name, class_name_str, info_list)  # 展示物品
        if event == "返回" and window_user_show:  # 返回选项界面
            window_user_show.close()
            window_user_show = None
            window_user_menu_choice = window1.make_window_user_menu_choice()
        if event == "查找该类型特定物品":  # 用户选择查找物品
            window_user_menu_choice.close()
            window_user_menu_choice = None
            window_user_search = window1.make_window_user_search()
        if event == "返回" and window_user_search:  # 返回选项界面
            window_user_search.close()
            window_user_search = None
            window_user_menu_choice = window1.make_window_user_menu_choice()
        if event == "查找":  # 用户点击查找
            if value['_NAME_'] == "" and value['_EXPL_'] == "":  # 判断查找内容是否为空
                sg.popup("查找内容不能为空")
            else:  # 进行查找
                name = value['_NAME_']
                explanation = value['_EXPL_']
                class_name = item1.search_class_name()
                class_name_str, info_list = user1.search(class_name, name, explanation)
                window_user_search.close()
                window_user_search = None
                window_user_search_show = window1.make_window_user_search_show(class_name_str, info_list)
        if event == "返回查找界面" and window_user_search_show:  # 用户返回查找界面
            window_user_search_show.close()
            window_user_search_show = None
            window_user_search = window1.make_window_user_search()
        if event == "注册":  # 普通用户选择注册
            window_user_login.close()
            window_user_login = None
            window_user_register = window1.make_window_user_register()  # 生成普通用户注册界面
        if event == "确定注册":  # 普通用户点击确定注册
            user = value['_USER_']
            password = value['_PWD_']
            phone_num = value['_PHONE_']
            address = value['_ADD_']
            if user1.register(user, password, address, phone_num):  # 信息完整，进行注册
                sg.popup("注册申请已提交，请等待管理员审核")
            else:  # 信息不完整，返回提示
                sg.popup("注册信息不完整")
        if event == "返回登录界面":  # 普通用户放弃注册，返回登录界面
            window_user_register.close()
            window_user_register = None
            window1.make_window_user_login()
        if event == '管理员':  # 打开管理员登录界面
            window_start.close()
            window_start = None
            window_admin_login = window1.make_window_admin_login()
        if event == '管理员登录':  # 管理员登录
            user = value['_USER_']
            password = value['_PWD_']
            if admin1.admin_login(user, password) and not window_admin_menu:  # 信息正确，返回管理员菜单
                window_admin_login.close()
                window_admin_login = None
                window_admin_menu = window1.make_window_admin_menu()
            else:  # 信息不正确，返回提示
                sg.popup("用户名或密码不正确")
        if event == "批准注册用户信息":  # 管理员选择批准注册用户信息
            window_admin_menu.close()
            window_admin_menu = None
            window_admin_approve_menu = window1.make_window_admin_approve_menu()  # 打开批准注册用户信息界面
        if event == "选择" and window_admin_approve_menu and value['-LIST-'] != "":  # 管理员选择其中一条用户注册申请
            num = value['-LIST-'][0][0]  # 注册申请的编号
            info = value['-LIST-'][0][1].strip()  # 注册申请的信息
            window_admin_approve = window1.make_window_admin_approve()  # 打开批准确认界面
            window_admin_approve_menu.close()
            window_admin_approve_menu = None
        if event == "返回管理员菜单" and window_admin_approve_menu:  # 管理员选择从批注注册界面返回管理员菜单
            window_admin_approve_menu.close()
            window_admin_approve_menu = None
            window_admin_menu = window1.make_window_admin_menu()
        if event == "不通过":  # 管理员选择不通过批准
            admin1.disapprove(num)
            sg.popup("已驳回申请")
            window_admin_approve.close()
            window_admin_approve = None
            window_admin_approve_menu = window1.make_window_admin_approve_menu()  # 回到批准菜单
        if event == "通过":  # 管理员选择通过批准
            admin1.approve(num, info)
            sg.popup("已通过申请")
            window_admin_approve.close()
            window_admin_approve = None
            window_admin_approve_menu = window1.make_window_admin_approve_menu()  # 回到批准菜单
        if event == "返回通过用户注册界面":  # 管理员从用户注册确认界面选择返回通过用户注册菜单界面
            window_admin_approve.close()
            window_admin_approve = None
            window_admin_approve_menu = window1.make_window_admin_approve_menu()
        if event == "设置新的物品类型":  # 管理员选择设置新物品类型
            window_admin_menu.close()
            window_admin_menu = None
            window_admin_create_new_item = window1.make_window_admin_create_new_item()
        if event == "确定设置新物品":  # 管理员选择确认设置新物品
            name = value['_NAME_']
            attribute = value['_ATT_']
            if name != "":  # 判断输入信息是否为空
                if admin1.create_new_item(name, attribute):  # 判断物品是否已经存在
                    sg.popup("新物品已设置")
                else:
                    sg.popup("该物品类型已存在")
            else:
                sg.popup("物品类型不能为空")
        if event == "修改(删除)物品类型":  # 管理员选择修改物品类型
            window_admin_menu.close()
            window_admin_menu = None
            window_admin_modify_item_menu = window1.make_window_admin_modify_item_menu()
        if event == "选择" and window_admin_modify_item_menu and value['-ITEMLIST-']:  # 管理员选择某一物品类型
            window_admin_modify_item_menu.close()
            window_admin_modify_item_menu = None
            class_name = value['-ITEMLIST-'][0]
            item1.save_class_name(class_name)  # 储存该物品类型
            attribute = item1.search_item_attribute(class_name)  # 返回该物品属性
            window_admin_modify_item_choice = window1.make_window_admin_modify_item_choice(attribute)  # 展示物品属性
        if event == "增加属性":  # 管理员选择增加属性
            if value['_ADD_'].strip() == "":  # 增加值不能为空值
                sg.popup("属性不能为空")
            else:
                class_name = item1.search_class_name()
                admin1.add_attribute(class_name, value['_ADD_'])  # 增加物品属性
                sg.popup("添加成功")
                window_admin_modify_item_choice.close()
                window_admin_modify_item_choice = None
                attribute = item1.search_item_attribute(class_name)
                window_admin_modify_item_choice = window1.make_window_admin_modify_item_choice(
                    attribute)  # 重新生成选项界面来反映发生的变化
        if event == "删除属性":  # 管理员选择删除属性
            if value['_DELETE_'].strip() == "":  # 删除值不能为空值
                sg.popup("属性不能为空")
            else:
                class_name = item1.search_class_name()
                admin1.delete_attribute(class_name, value['_DELETE_'])  # 删除物品属性
                sg.popup("删除成功")
                window_admin_modify_item_choice.close()
                window_admin_modify_item_choice = None
                attribute = item1.search_item_attribute(class_name)
                window_admin_modify_item_choice = window1.make_window_admin_modify_item_choice(
                    attribute)  # 重新生成选项界面来反映发生的变化
        if event == "删除该物品类型":  # 管理员选择删除物品类型
            class_name = item1.search_class_name()
            window_admin_confirm_delete_class = window1.make_window_admin_confirm_delete_class(class_name)  # 打开确认界面
        if event == "取消" and window_admin_confirm_delete_class:  # 管理员选择取消删除物品类型
            window_admin_confirm_delete_class.close()
            window_admin_confirm_delete_class = None
        if event == "确定" and window_admin_confirm_delete_class:  # 管理员确认删除物品类型
            class_name = item1.search_class_name()
            admin1.detele_class(class_name)  # 删除物品类型
            sg.popup("删除成功")
            window_admin_confirm_delete_class.close()
            window_admin_confirm_delete_class = None
            window_admin_modify_item_choice.close()
            window_admin_modify_item_choice = None
            window_admin_modify_item_menu = window1.make_window_admin_modify_item_menu()  # 返回物品类型菜单界面
        if event == "返回" and window_admin_modify_item_choice:  # 管理员选择从选项界面返回
            window_admin_modify_item_choice.close()
            window_admin_modify_item_choice = None
            window_admin_modify_item_menu = window1.make_window_admin_modify_item_menu()  # 返回物品类型菜单界面
        if event == "返回管理员菜单" and window_admin_modify_item_menu:  # 管理员返回管理员菜单
            window_admin_modify_item_menu.close()
            window_admin_modify_item_menu = None
            window_admin_menu = window1.make_window_admin_menu()
        if event == "返回管理员菜单" and window_admin_create_new_item:  # 管理员返回管理员菜单
            window_admin_create_new_item.close()
            window_admin_create_new_item = None
            window_admin_menu = window1.make_window_admin_menu()
        if event == "退出" and window_admin_menu:  # 管理员选择退出系统
            window_admin_menu.close()
            window_admin_menu = None
            window_admin_confirm_exit = window1.make_window_confirm_exit()  # 生成退出确认界面
        if event == "取消" and window_admin_confirm_exit:  # 管理员选择不退出
            window_admin_confirm_exit.close()
            window_admin_confirm_exit = None
            window_admin_menu = window1.make_window_admin_menu()


if __name__ == "__main__":
    main()
