from spprval.database.DBWrapper import DBWrapper


def create_processed_dict_act(act_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_act_names()
    act_dict = df_all_names.set_index("work_name").to_dict()["processed_name"]
    result_dict = {}
    for act in act_names:
        if act in act_dict:
            result_dict[act] = act_dict[act]
        else:
            result_dict[act] = act
    return result_dict


def create_processed_dict_act_swapped(act_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_act_names()
    act_dict = df_all_names.set_index("work_name").to_dict()["processed_name"]
    result_dict = {}
    for act in act_names:
        if act in act_dict:
            if act_dict[act] in result_dict:
                result_dict[act_dict[act]].append(act)
            else:
                result_dict[act_dict[act]] = [act]
        else:
            result_dict[act] = [act]
    return result_dict


def create_granulary_dict_act(act_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_act_names()
    act_dict = df_all_names.set_index("work_name").to_dict()["granulary_name"]
    result_dict = {}
    for act in act_names:
        if act in act_dict:
            result_dict[act] = act_dict[act]
        else:
            result_dict[act] = act
    return result_dict


def create_granulary_dict_act_aswapped(act_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_act_names()
    act_dict = df_all_names.set_index("work_name").to_dict()["granulary_name"]
    result_dict = {}
    for act in act_names:
        if act in act_dict:
            if act_dict[act] in result_dict:
                result_dict[act_dict[act]].append(act)
            else:
                result_dict[act_dict[act]] = [act]
        else:
            result_dict[act] = [act]
    return result_dict


def create_granulary_dict_res(res_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_res_names()
    res_dict = df_all_names.set_index("name").to_dict()["granulary_name"]
    result_dict = {}
    for res in res_names:
        if res in res_dict:
            result_dict[res] = res_dict[res]
        else:
            result_dict[res] = res
    return result_dict


def create_granulary_dict_res_swapped(res_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_res_names()
    res_dict = df_all_names.set_index("name").to_dict()["granulary_name"]
    result_dict = {}
    for res in res_names:
        if res in res_dict:
            if res_dict[res] in result_dict:
                result_dict[res_dict[res]].append(res)
            else:
                result_dict[res_dict[res]] = [res]
        else:
            result_dict[res] = [res]
    return result_dict


def create_processed_dict_res(res_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_res_names()
    res_dict = df_all_names.set_index("name").to_dict()["processed_name"]
    result_dict = {}
    for res in res_names:
        if res in res_dict:
            result_dict[res] = res_dict[res]
        else:
            result_dict[res] = res
    return result_dict


def create_processed_dict_res_swapped(res_names):
    db = DBWrapper("http://10.32.15.31:8000")
    df_all_names = db.get_res_names()
    res_dict = df_all_names.set_index("name").to_dict()["processed_name"]
    result_dict = {}
    for res in res_names:
        if res in res_dict:
            if res_dict[res] in result_dict:
                result_dict[res_dict[res]].append(res)
            else:
                result_dict[res_dict[res]] = [res]
        else:
            result_dict[res] = [res]
    return result_dict
