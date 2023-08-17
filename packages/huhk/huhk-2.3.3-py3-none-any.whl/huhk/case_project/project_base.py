import json
import os.path
import re
import time

import requests

from huhk.case_project.project_string import ProjectString
from huhk.unit_dict import Dict
from huhk.unit_fun import FunBase
from huhk import projects_path
from huhk.unit_logger import logger


class ProjectBase(ProjectString):
    def __init__(self, name=None, app_key=None, yapi_url=None, yapi_token=None, yapi_json_file=None, swagger_url=None):
        super().__init__(name, app_key, yapi_url, yapi_token, yapi_json_file, swagger_url)
        self.get_project()

    def get_service_value2(self, key=None, default=None):
        """获取项目本地变量"""
        this_path = self.get_setting_path2()
        value = ProjectBase.get_json_value(this_path, key=key, default=default)
        return value if value else ProjectBase.get_service_value(key=key, default=default)

    @staticmethod
    def get_service_value(key=None, default=None):
        path = ProjectBase.get_setting_path()
        return ProjectBase.get_json_value(path, key=key, default=default)

    @staticmethod
    def get_json_value(path, key=None, default=None):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fp:
                data = json.load(fp)
                return data.get(key, default) if key else data
        return default

    @staticmethod
    def set_json_value(path, key=None, value=None):
        FunBase.mkdir_file(path, is_py=False)
        data = ProjectBase.get_json_value(path) or {}
        data[key] = value
        with open(path, 'w') as fp:
            json.dump(data, fp, indent=4)

    @staticmethod
    def get_setting_path():
        setting_path = os.path.join(ProjectBase._get_project_dir(), "service", "setting.json")
        if not os.path.exists(setting_path):
            FunBase.mkdir_file(setting_path, is_py=False)
            FunBase.write_file(setting_path, "{}")
        return setting_path

    def get_setting_path2(self):
        setting_path = os.path.join(self.path.service_dir, self.name + "_setting.json")
        if not os.path.exists(setting_path):
            FunBase.mkdir_file(setting_path, is_py=False)
            FunBase.write_file(setting_path, "{}")
        return setting_path

    @staticmethod
    def _get_project_dir(path=None):
        path = path or projects_path
        for dirpath, dirnames, filenames in os.walk(path):
            if os.path.join("autotest", "codes") not in dirpath:
                if "apis" in dirnames and "asserts" in dirnames and "funs" in dirnames and "sqls" in dirnames \
                        and "__init__.py" in filenames:
                    return os.path.dirname(os.path.dirname(dirpath))
        if len(path) > 5:
            return ProjectBase._get_project_dir(os.path.dirname(path))
        return projects_path

    @staticmethod
    def set_service_value(key, value):
        ProjectBase.set_json_value(ProjectBase.get_setting_path(), key=key, value=value)

    def set_service_value2(self, key, value, _type=0):
        """设置项目本地变量"""
        ProjectBase.set_json_value(self.get_setting_path2(), key=key, value=value)

    def get_api_attribute(self, file_str, api_file):
        try:
            fun_list = re.findall(r"\ndef +([^_].+)?\((.*?)\):\s*"
                                  r"([\'\"]{3}"
                                  r"\s*(.*?)?\s*up_time=(\d+)?[\w\W]*?"
                                  r"(    params:[\w\W]*?)?(====[\w\W]*?)?"
                                  r"[\'\"]{3})?"
                                  r"[\w\W]*?_method *= *[\"\'](\S+?)[\"\']"
                                  r"[\w\W]*?_url *= *[\"\'](\S+?)[\"\']"
                                  r"[\w\W]*?(\n@allure.step\(|\ndef|$)", file_str)
            for fun in fun_list:
                self.this_fun_list.api[fun[0]].path = api_file
                self.this_fun_list.api[fun[0]].input = [i.split('=')[0].strip() for i in fun[1].split(',') if
                                                        len(i.split('=')) > 1 and i.strip()[0] != '_' and i.split('=')[
                                                            0].strip() != "headers"]
                self.this_fun_list.api[fun[0]].title = fun[3]
                self.this_fun_list.api[fun[0]].up_time = fun[4]
                self.this_fun_list.api[fun[0]].params = fun[5]
                self.this_fun_list.api[fun[0]].method = fun[7]
                self.this_fun_list.api[fun[0]].url = fun[8]
        except Exception as e:
            logger.error(str(e))

    def get_this_fun_list(self):
        try:
            last_time = self.get_service_value2("last_time")
            # self.set_service_value("last_time", time.time())
            service_dir = os.path.join(self.path.dir, 'service', self.name)
            for dirpath, dirnames, filenames in os.walk(service_dir):
                for filename in filenames:
                    key = filename.split("_")[0]
                    if key in self.this_file_list.keys() and filename[-3:] == ".py":
                        if not (key == "apis" and last_time and
                                os.stat(os.path.join(dirpath, filename)).st_mtime < last_time):
                            self.this_file_list[key].append(os.path.join(dirpath, filename))
            for api_file in self.this_file_list.get('apis'):
                file_str = FunBase.read_file(api_file)
                self.get_api_attribute(file_str, api_file)
        except Exception as e:
            print(str(e))

    def get_project(self):
        if self.app_key:
            project = requests.post(self.url + '/variable/variable/',
                                    json={"app_key": self.app_key, "environment": "sit"}).json()
            if project.get('project'):
                self.name = self.name or project.get('project')[0].get('code')
                if project.get('api_settings'):
                    self.api_type = project.get('api_settings')[0].get('api_type')
                    if self.api_type == 2:
                        self.yapi_file_str = requests.get(self.url + "/media/" +
                                                          project.get('api_settings')[0].get('file')).text
                    elif self.api_type in (0, 3):
                        self.swagger_url = self.swagger_url or project.get('api_settings')[0].get('url')
                    elif self.api_type == 1:
                        self.yapi_url = self.yapi_url or project.get('api_settings')[0].get('url').strip()
                        if self.yapi_url[-1] == "/":
                            self.yapi_url = self.yapi_url[:-1]
                        self.yapi_token = self.yapi_token or project.get('api_settings')[0].get('token')
            else:
                self.error = project.get('non_field_errors')[0]
                logger.error("该app_key: %s, 对应的项目不存在，项目创建：%s/admin/#/admin/autotest/project/", (
                    self.app_key, self.url[:-4]))
        self.name = self.name or "demo"
        self.name2 = self.name.title()
        projects_path = ProjectBase._get_project_dir()
        logger.info(f"项目路径：{projects_path}")
        self.path.service_dir = os.path.join(projects_path, "service", self.name)
        self.path.testcase_dir = os.path.join(projects_path, "testcase", self.name)
        self.path.api_dir = os.path.join(self.path.service_dir, "apis")
        self.path.fun_dir = os.path.join(self.path.service_dir, "funs")
        self.path.assert_dir = os.path.join(self.path.service_dir, "asserts")
        self.path.sql_dir = os.path.join(self.path.service_dir, "sqls")

    def get_list_menu_swagger(self):
        try:
            data = Dict(requests.get(self.swagger_url).json())
            for k, v in data.paths.items():
                api = Dict()
                api.path = data.basePath + k
                for k2, v2 in v.items():
                    api.method = k2
                    api.title = v2.get('summary', "")
                    api.up_time = int(time.time())
                    api.req_headers = [{'name': 'Content-Type', 'desc': '',
                                        'value': v2.consumes[
                                            0] if v2.consumes else "application/x-www-form-urlencoded"}]
                    api["req_params"] = []
                    api["req_query"] = []
                    api["req_body_other"] = []
                    api["res_body"] = []
                    for parameter in v2.get('parameters', []):
                        if parameter.get('in') == "body":
                            if parameter.get('name') not in ("params", "headers"):
                                if parameter.get("schema") and parameter.get("schema").get("$ref"):
                                    tmp = parameter.get("schema").get("$ref").split("/")
                                    if len(tmp) > 2:
                                        tmp2 = data.get(tmp[1], {}).get(tmp[2], {})
                                        for k3, v3 in tmp2.get('properties', {}).items():
                                            api["res_body"].append({'name': k3, 'desc': v3.get('description', "")})
                                else:
                                    api["res_body"].append({'name': parameter.get("name"),
                                                            'desc': parameter.get('description')})
                        elif parameter.get('in') in ("params", "path"):
                            api["req_params"].append({'name': parameter.get("name"),
                                                      'desc': parameter.get('description')})
                        elif parameter.get('in') == "query":
                            if parameter.get('name') not in ("params",):
                                api["req_query"].append({'name': parameter.get("name"),
                                                         'desc': parameter.get('description')})
                        else:
                            print("联系管理员维护类型：", parameter.get('in'))
                    self.api_list += [api]
        except Exception as e:
            logger.error("swagger获取接口失败")
            logger.error(str(e))
            self.api_list = []

    def get_list_menu(self):
        try:
            res = requests.get(self.yapi_url + "/api/project/get?token=" + self.yapi_token).text
            res_json = Dict(json.loads(res))
            base_path = res_json.data.basepath or ""
            data = {"token": self.yapi_token, "project_id": res_json.data.get("_id")}
            res = requests.get(self.yapi_url + "/api/interface/list_menu", data=data)
            res_json = Dict(json.loads(res.text))
            for menu in res_json.get("data"):
                self.api_list += menu.get('list')
            if base_path:
                for api in self.api_list:
                    api.path = base_path + api.path
        except Exception as e:
            logger.error("yapi获取接口失败")
            logger.error(str(e))
            self.api_list = []

    def get_list_json(self):
        if self.yapi_json_file:
            file_path = os.path.join(self.path.dir, 'file', self.yapi_json_file)
            if os.path.exists(file_path):
                value = FunBase.read_file(file_path)
                value = json.loads(value)
                for v in value:
                    self.api_list += v.get('list')
            else:
                assert not "Yapi的json文件在file中不存在"
        elif self.app_key:
            value = json.loads(self.yapi_file_str)
            for v in value:
                self.api_list += v.get('list')

    def write_api(self, row, _update=True):
        fun_name = self.get_fun_name(row.get("path"))
        if fun_name in self.this_fun_list.api.keys():
            up_time = self.this_fun_list.api[fun_name].up_time
            if not up_time or int(up_time) < row.get('up_time'):
                api_file_str = FunBase.read_file(self.this_fun_list.api[fun_name].path)
                ord_str = re.findall(
                    r'\n((@allure.step\(.*\) *\n)?def %s\(.+\)[\w\W]*?)(\n@allure.step\(|\ndef|$)' % fun_name,
                    api_file_str)
                new_str = self.get_api_fun_str(fun_name, row)
                api_file_str = api_file_str.replace(ord_str[0][0], new_str)
                FunBase.write_file(self.this_fun_list.api[fun_name].path, api_file_str)
        else:
            self.this_fun_list.api[fun_name] = self.get_path(fun_name)
            if os.path.exists(self.this_fun_list.api[fun_name].path):
                api_file_str = FunBase.read_file(self.this_fun_list.api[fun_name].path)
            else:
                api_file_str = self.get_api_header_str(self.this_fun_list.api[fun_name].import_path)
            api_file_str += self.get_api_fun_str(fun_name, row)
            FunBase.mkdir_file(self.this_fun_list.api[fun_name].path, is_py=False)
            init_dir = os.path.dirname(self.this_fun_list.api[fun_name].path)
            for i in range(self.this_fun_list.api[fun_name].import_path.count('.') - 2):
                init_path = os.path.join(init_dir, "__init__.py")
                if not os.path.exists(init_path) or not FunBase.read_file(init_path):
                    FunBase.write_file(init_path, self.get_api_init_str(
                        ".".join(self.this_fun_list.api[fun_name].import_path.split(".")[:-2-i])))
                init_dir = os.path.dirname(init_dir)
            FunBase.write_file(self.this_fun_list.api[fun_name].path, api_file_str)
            self.get_api_attribute(api_file_str, self.get_path(fun_name).path)

    def write_sql(self, fun_name, _update=False):
        sql_path = self.get_path(fun_name, fun_type='sqls')
        if os.path.exists(sql_path.path):
            file_str = FunBase.read_file(sql_path.path)
            ord_str = re.findall(
                r'\n((    @allure.step\(.*\) *\n)?    def sql_%s\(.+\)[\w\W]*?)(\n    @allure.step\(|\n    def|$)' %
                fun_name, file_str)
            if ord_str:
                if _update:
                    new_str = self.get_sql_fun_str(fun_name)
                    file_str = file_str.replace(ord_str[0][0], new_str)
                    FunBase.write_file(sql_path.path, file_str)
            else:
                tmp_list = file_str.split("if __name__ == '__main__':")
                tmp_list[0] += self.get_sql_fun_str(fun_name)
                file_str = "if __name__ == '__main__':".join(tmp_list)
                FunBase.write_file(sql_path.path, file_str)
        else:
            file_str = self.get_sql_header_str(sql_path.class_name) + self.get_sql_fun_str(fun_name)
            FunBase.mkdir_file(sql_path.path)
            FunBase.write_file(sql_path.path, file_str)

    def write_assert(self, fun_name, _update=False):
        sql_path = self.get_path(fun_name, fun_type='sqls')
        assert_path = self.get_path(fun_name, fun_type='asserts')
        if os.path.exists(assert_path.path):
            file_str = FunBase.read_file(assert_path.path)
            ord_str = re.findall(
                r'\n((    @allure.step\(.*\) *\n)?    def assert_%s\(.+\)[\w\W]*?)(\n    @allure.step\(|\n    def|$)' %
                fun_name, file_str)
            if ord_str:
                if _update:
                    new_str = self.get_assert_fun_str(fun_name)
                    file_str = file_str.replace(ord_str[0][0], new_str)
                    FunBase.write_file(assert_path.path, file_str)
            else:
                tmp_list = file_str.split("if __name__ == '__main__':")
                tmp_list[0] += self.get_assert_fun_str(fun_name)
                file_str = "if __name__ == '__main__':".join(tmp_list)
                FunBase.write_file(assert_path.path, file_str)
        else:
            file_str = self.get_assert_header_str(assert_path.class_name, sql_path) + self.get_assert_fun_str(fun_name)
            FunBase.mkdir_file(assert_path.path)
            FunBase.write_file(assert_path.path, file_str)

    def set_api_fun_header(self, fun_name):
        fun_name = fun_name.strip(" _")

        def _fun_header():
            return f"from {fun_path.import_path} import {fun_path.class_name}\n\n\n" \
                   f"class {fun_path2.class_name}({fun_path.class_name}):\n    pass\n\n"

        fun_path = self.get_path(fun_name, fun_type="funs")
        if fun_name.count('_') > 0:
            # path = fun_path.path.rsplit('_', 1)[0] + '.py'
            fun_path2 = self.get_path(fun_name.rsplit('_', 1)[0], fun_type='funs')
            path = fun_path2.path
            if os.path.exists(path):
                old_str = FunBase.read_file(path)
                old_str_l = re.findall(r'([\w\W]*?\n)(\s*class +.*\()(.*?)(\):[\w\W]*)', old_str)
                if old_str_l:
                    old_str_l = list(old_str_l[0])
                    if fun_path.class_name not in [i.strip() for i in old_str_l[2].split(',')]:
                        old_str_l[0] += f"from {fun_path.import_path} import {fun_path.class_name}\n"
                        old_str_l[2] += f", {fun_path.class_name}"
                    new_str = "".join(old_str_l)
                else:
                    new_str = _fun_header()
            else:
                new_str = _fun_header()
            FunBase.write_file(path, new_str)
            if fun_name.count('_') > 1:
                self.set_api_fun_header(fun_name.rsplit('_', 1)[0])
        else:
            print("Warning")

    def write_api_fun(self, fun_name, _update=False):
        fun_path = self.get_path(fun_name, fun_type='funs')

        if os.path.exists(fun_path.path):
            file_str = FunBase.read_file(fun_path.path).replace("    pass\n\n", "").replace("    pass\n", "")
            ord_str = re.findall(
                r'\n((    @allure.step\(.*\) *\n)?    def %s\(.+\)[\w\W]*?)(\n    @allure.step\(|\n    def|$)' %
                fun_name, file_str)
            if ord_str:
                if _update:
                    new_str = self.get_api_fun_fun_str(fun_name)
                    file_str = file_str.replace(ord_str[0][0], new_str)
                    FunBase.write_file(fun_path.path, file_str)
            else:
                file_str = self.get_api_fun_header_str2(fun_name, file_str)
                tmp_list = file_str.split("if __name__ == '__main__':")
                tmp_list[0] += self.get_api_fun_fun_str(fun_name)
                file_str = "if __name__ == '__main__':".join(tmp_list)
                FunBase.write_file(fun_path.path, file_str)
        else:
            file_str = self.get_api_fun_header_str(fun_name) + self.get_api_fun_fun_str(fun_name)
            FunBase.mkdir_file(fun_path.path)
            FunBase.write_file(fun_path.path, file_str)
            self.set_api_fun_header(fun_name)

    def write_testcase(self, fun_name, _update=False):
        fun_path = self.get_path(fun_name, fun_type='test')
        testcase_str_list = self.get_api_testcase_str(fun_name)
        if os.path.exists(fun_path.path):
            file_str = FunBase.read_file(fun_path.path).replace("    pass\n", "")
            ord_str_list = re.findall(r'\n    def test_(%s(?:__.+?)?)(?:_(\d+))?\(.+\):\n' % fun_name, file_str)
            if ord_str_list:
                ord_list = {j[0]: (int(j[1]) if j[1] else i + 1) for i, j in enumerate(ord_str_list)}
                i = len(ord_str_list)
                for case_name, fun_str in testcase_str_list.items():
                    if case_name in ord_list.keys():
                        if _update:
                            old_str = re.findall(r'(( *#.*\n|    @.*\n)*    def test_%s(?:_\d+)?\(.+\):[\w\W]+?\n+)'
                                                 r'(?:( *#.*\n|    @.*\n)*    def |$)?' % case_name, file_str)
                            fun_str = fun_str.replace(f"def test_{case_name}(",
                                                      f"def test_{case_name}{'_%03d' % ord_list.get(case_name)}(")
                            file_str = file_str.replace(old_str[0][0], fun_str)
                    else:
                        i += 1
                        tmp_list = file_str.split("if __name__ == '__main__':")
                        tmp_list[0] += fun_str.replace(f"def test_{case_name}(",
                                                       f"def test_{case_name}{'_%03d' % i}(")
                        file_str = "if __name__ == '__main__':".join(tmp_list)
            else:
                i = 0
                for case_name, fun_str in testcase_str_list.items():
                    i += 1
                    tmp_list = file_str.split("if __name__ == '__main__':")
                    tmp_list[0] += fun_str.replace(f"def test_{case_name}(", f"def test_{case_name}{'_%03d' % i}(")
                    file_str = "if __name__ == '__main__':".join(tmp_list)
            FunBase.write_file(fun_path.path, file_str)
        else:
            file_str = self.get_api_testcase_header_str(fun_name)
            i = 1
            for case_name, fun_str in testcase_str_list.items():
                file_str += fun_str.replace(f"def test_{case_name}(", f"def test_{case_name}{'_%03d' % i}(")
                i += 1
            FunBase.mkdir_file(fun_path.path, is_py=False)
            FunBase.write_file(fun_path.path, file_str)


if __name__ == "__main__":
    a = ProjectBase(name="app_t")
    a.dir = r"/"
    o = a.get_setting_path()
    print(o)
