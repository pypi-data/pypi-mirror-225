import os


# download_byte参数过滤器
def donwload_byte_filtering(
        Max_Thread: int = 0,
        Max_Rerty: int = 3,
        Time_Sleep: [float, int] = 0,
        Request_Timeout: [float, int] = 10,
        urls: list = None,
        headers: [dict[str, any], None] = None,
        cookie: [dict[str, any], None] = None,
        param: [dict[str, any], None] = None,
        data: [dict[str, any], None] = None,
        proxies: [dict[str, any], None] = None,
        verify: bool = True,
        path_: str = './',
        type_: str = '',
        Name_Rules: str = 'default',
        titles: [list, None] = None,
        Save_Error_Log: bool = True,
        Show_Progress_Bar: bool = False,
        Show_Error_Info: bool = True
):
    '''
    该方法为内部方法，是用于判断设置的参数是否正常，如果输入的参数出现问题，将抛出异常
    '''

    if type(Max_Thread) != int:
        raise '设置的MAX_THREAD不为整型'
    else:
        pass

    if type(Max_Rerty) != int:
        raise '设置的MAX_RETRY不为整型'
    else:
        pass

    if type(Time_Sleep) != float or type(Time_Sleep) != int:
        raise '设置的Time_Sleep不为整型或浮点型'
    else:
        pass

    if type(Request_Timeout) != float or type(Request_Timeout) != int:
        raise '设置的的Request_Timeout不为整型或浮点型'
    else:
        pass

    if type(urls) != list:
        raise '设置的的urls不为列表'

    if type(titles) != list:
        raise '设置的的titles不为列表'

    if Name_Rules != 'default' and Name_Rules != 'title':
        raise '设置的Name_Rules并不存在'
    else:
        pass

    if titles != None and len(titles) == len(urls) and Name_Rules.lower() == 'title':
        pass
    elif titles == None and Name_Rules.lower() == 'default':
        pass
    elif titles == None and Name_Rules.lower() == 'title':
        raise '当前命名模式为title,但并未设置titles'
    elif titles != None and Name_Rules.lower() == 'default':
        raise '当前命名模式为default,但设置了titles'
    elif titles != None and len(titles) != len(urls):
        raise '当前传入的urls与titles的长度不符'
    else:
        pass

    if Save_Error_Log != True and Save_Error_Log != False:
        raise '错误日志保存只支持传入布尔类型'
    else:
        pass

    if Show_Progress_Bar != True and Show_Progress_Bar != False:
        raise '进度条设置只支持传入布尔类型'
    else:
        pass

    if Show_Error_Info != True and Show_Error_Info != False:
        raise '错误信息显示只支持传入布尔类型'
    else:
        pass

    if len(urls) < 1 or urls == None:
        raise '未传入urls或urls为空'
    else:
        pass

    if type(type_) != str:
        raise 'type_只支持传入字符串类型'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    return True


def donwload_byte_function_filtering(
        url: str = None,
        headers: [dict[str, any], None] = None,
        cookie: [dict[str, any], None] = None,
        param: [dict[str, any], None] = None,
        data: [dict[str, any], None] = None,
        proxies: [dict[str, any], None] = None,
        verify: bool = True,
        path_: str = './',
        name: str = '',
        type_: str = ''
):
    if len(url) < 1 or url == None:
        raise '未传入url或url为空'
    else:
        pass

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    return True


# open_js参数过滤器
def open_js_filtering(
        path_: str = '',
        encoding: str = 'utf-8',
        cwd: any = None
):
    if os.path.isfile(path_):
        pass
    else:
        raise '未找到该文件'
    return True


# save_to_csv参数过滤器
def save_to_csv_filtering(
        path_: str = '',
        file_name: str = '',
        data: list = None,
        mode: str = 'w',
        encoding: str = 'utf-8',
        errors=None,
        newline=None
):
    if file_name == '' or file_name == None or type(file_name) != str:
        raise '当前传入的file_name为空或者传入了非字符串类型的file_name'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    if mode != 'a' and mode != 'w':
        raise '写入csv只支持"a"和"w"两种模式'
    else:
        pass

    if data == None or data == [] or type(data) != list:
        raise '当前传入的data为空或者传入了非列表类型的data'
    else:
        pass

    return True


def save_to_xlsx_filtering(
        path_: str = '',
        file_name: str = '',
        data: dict = None,
        mode: str = 'w',
        sheet_name: str = "Sheet1",
        columns: any = None,
        header: bool = True,
        index: bool = True,
):
    if file_name == '' or file_name == None or type(file_name) != str:
        raise '当前传入的file_name为空或者传入了非字符串类型的file_name'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    if mode != 'a' and mode != 'w':
        raise '写入xlsx只支持"a"和"w"两种模式'
    else:
        pass

    if data == None or data == {} or type(data) != dict:
        raise '当前传入的data为空或者传入非字典类型的data'
    else:
        pass

    if type(header) != bool:
        raise 'header只支持传入布尔类型'
    else:
        pass

    if type(index) != bool:
        raise 'index只支持传入布尔类型'
    else:
        pass

    if mode == 'a':
        if os.path.isfile(path_ + file_name):
            pass
        else:
            raise '当前模式为追加写入,但并未发现指定文件'
    else:
        pass

    return True


def save_to_mysql_filtering(
        host: str = 'localhost',
        port: int = 3306,
        user: str = 'root',
        password: str = '',
        database: str = '',
        charset: str = 'utf8'
):
    if database == '' or type(database) != str:
        raise '传入的database为空或传入了非字符串类型的database'
    else:
        pass

    if password == '' or type(password) != str:
        raise '传入的password为空或传入了非字符串类型的password'
    else:
        pass

    if host == '' or type(host) != str:
        raise '传入的host为空或传入了非字符串类型的host'
    else:
        pass

    if user == '' or type(user) != str:
        raise '传入的user为空或传入了非字符串类型的user'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True


def save_to_redis_filtering(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        password: str = '',
        pool_size: int = 10
):
    if database == '' or type(database) != str:
        raise '传入的database为空或传入了非字符串类型的database'
    else:
        pass

    if password == '' or type(password) != str:
        raise '传入的password为空或传入了非字符串类型的password'
    else:
        pass

    if host == '' or type(host) != str:
        raise '传入的host为空或传入了非字符串类型的host'
    else:
        pass

    if pool_size == '' or type(pool_size) != int:
        raise '传入的pool_size为空或传入了非整型类型的pool_size'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True


def save_to_mongo_filtering(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        user: str = '',
        password: str = '',
        pool_size: int = 10,
        collection: str = ''
):
    if database == '' or type(database) != str:
        raise '传入的database为空或传入了非字符串类型的database'
    else:
        pass

    if password == '' or type(password) != str:
        raise '传入的password为空或传入了非字符串类型的password'
    else:
        pass

    if user == '' or type(user) != str:
        raise '传入的user为空或传入了非字符串类型的user'
    else:
        pass

    if host == '' or type(host) != str:
        raise '传入的host为空或传入了非字符串类型的host'
    else:
        pass

    if collection == '' or type(collection) != str:
        raise '传入的collection为空或传入了非字符串类型的collection'
    else:
        pass

    if pool_size == '' or type(pool_size) != int:
        raise '传入的pool_size为空或传入了非整型类型的pool_size'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True
