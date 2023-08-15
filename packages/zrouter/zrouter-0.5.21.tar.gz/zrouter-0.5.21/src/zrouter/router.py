from zrouter.exceptions import MessagePrompt
from zrouter.utils.json import to_lowcase, iter_lowcase, iter_camel
from flask import Blueprint, request
from jsonschema.exceptions import ValidationError
import functools
import random
import os
import importlib
import inspect


class ParamMixin:
    @staticmethod
    def get_params():
        if request.method in ['GET', 'DELETE']:
            return to_lowcase({**request.args, **request.view_args})
        elif 'multipart/form-data' in request.content_type:
            return {
                'files': request.files,
                'params': to_lowcase(request.form.to_dict())
            }
        else:
            try:
                params = request.get_json()
                return iter_lowcase(params)
            except:
                return {
                    'data': request.get_data()
                }

    @staticmethod
    def clean_params(params):
        return {k: v for k, v in params.items() if v not in ('', 'null', None)}


def get_resource_classes_from_module(module):
    resource_classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and name.endswith("Resource"):
            resource_classes.append(obj)
    return resource_classes


def get_resource_classes(resources_package, resources_file):
    resource_classes = []
    for file in os.listdir(os.path.dirname(resources_file)):
        if file.endswith("_resource.py"):
            module_name = os.path.splitext(file)[0]
            module = importlib.import_module(
                f".{module_name}", resources_package)
            resource_classes += get_resource_classes_from_module(module)
    return resource_classes


class Router(ParamMixin, Blueprint):
    """路由"""

    def __init__(self, *args, **kwargs):
        Blueprint.__init__(self, *args, **kwargs)

    def verify_user(self):
        """用户验证，通过继承覆盖此方法实现具体逻辑"""
        return True

    def handle_error(self, e):
        """错误处理，通过继承覆盖此方法实现具体逻辑"""
        pass

    @staticmethod
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def wrap_view_func(self, func, open=False):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            params = self.clean_params(self.get_params())
            if not self.verify_user() and not open:
                return {'code': 401, 'msg': '用户无权限'}
            try:
                data = self.decorator(func)(**params)
            except MessagePrompt as e:
                return {'code': 500, 'msg': str(e)}
            except ValidationError as e:
                return {'code': 400, 'msg': str(e)}
            except Exception as e:
                self.handle_error(e)
                raise e
            if isinstance(data, dict):
                data = iter_camel(data)
            elif isinstance(data, list):
                data = [iter_camel(item) if isinstance(item, dict) else item
                        for item in data]
            elif data is None:
                pass
            elif isinstance(data, str):
                pass 
            else:
                return data
            return {'code': 200, 'msg': '操作成功', 'data': data}
        return wrapper

    def add_resource(self, rule, resource_class):
        http_methods = ['get', 'post', 'put', 'delete']

        for method_name in http_methods:
            if method_name in dir(resource_class):
                method = getattr(resource_class, method_name)
                open = getattr(method, 'open', False)
                method = functools.partial(method)
                endpoint = str(random.randint(10000000, 99999999))
                self.add_url_rule(rule, endpoint, self.wrap_view_func(method,
                                                                      open=open), methods=[method_name.upper()])

    def add_resources(self, resource_classes):
        for resource_class in resource_classes:
            self.add_resource(resource_class.path, resource_class)

    def auto_add_resources(self, resources_package, resources_file):
        resource_classes = get_resource_classes(
            resources_package, resources_file)
        self.add_resources(resource_classes)

    def add(self, rule, open=False, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, self.wrap_view_func(
                f, open=open,), **options)
        return decorator
