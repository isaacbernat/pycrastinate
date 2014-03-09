from datetime import datetime

log_msg = {
    "name": "pycrastinate module: ",
    "mod_start": "{} start  {}",
    "mod_finish": "{} finish {}",
}


def print_log(func, params):
    log_func_info = log_msg["name"] + func.func_name
    print log_msg["mod_start"].format(datetime.now(), log_func_info)
    results = func(*params)
    print log_msg["mod_finish"].format(datetime.now(), log_func_info)
    return results
