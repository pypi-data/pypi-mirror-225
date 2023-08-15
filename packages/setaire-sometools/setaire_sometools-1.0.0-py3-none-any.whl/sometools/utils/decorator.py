import re
import argparse
import inspect


class UnknowArgsTypeError(Exception):
    pass


class Command:
    """将函数转换为终端命令的装饰器

        使用方式:
        ```
        @Conmand
        def foo(a:int, b:int):
            print(a+b)

        foo.shell()
        ```
    """

    def __init__(self, f):
        self.__f = f

    def get_argset(self, argspec: inspect.FullArgSpec):
        argset = set(argspec.args or [])
        if argspec.varargs:
            argset.add(argspec.varargs)
        if argspec.varkw:
            argset.add(argspec.varkw)

        kwargs = argspec.kwonlydefaults or {}
        kwargset = set(kwargs.keys())
        return argset | kwargset

    def check_args_type(self, annotations: dict, argset: set):
        for arg in argset:
            if not annotations.get(arg):
                raise UnknowArgsTypeError(f"必须说明参数 {arg} 的数据类型")

    def parse_doc(self, doc: str, argset: set):
        description = []
        flag = True
        args_help_map = {}

        for line in doc.split("\n"):
            line = line.lstrip("\r\t ")
            if " " in line:
                k, v = line.split(" ", 1)
                if k in argset:
                    flag = False
                    args_help_map[k] = v
                    continue
            elif not line:
                flag = False
            if flag:
                description.append(line)

        description = "\n".join(description)
        return args_help_map, description

    def shell(self):
        f = self.__f

        argspec = inspect.getfullargspec(f)
        argset = self.get_argset(argspec)
        self.check_args_type(argspec.annotations, argset)

        args_help_map, description = self.parse_doc(f.__doc__ or "", argset)
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description
        )

        for i, arg in enumerate(argspec.args):
            helptxt = f"{args_help_map.get(arg, '')}"
            if argspec.defaults:
                j = i - len(argspec.args) + len(argspec.defaults)
                if j >= 0:
                    parser.add_argument(
                        f"--{arg}", nargs="?", default=argspec.defaults[j], type=argspec.annotations.get(arg), help=f"{helptxt}, 默认 {argspec.defaults[j]}")
                else:
                    parser.add_argument(
                        arg, type=argspec.annotations.get(arg), help=helptxt)
            else:
                parser.add_argument(
                    arg, type=argspec.annotations.get(arg), help=helptxt)

        if argspec.varargs:
            helptxt = f"{args_help_map.get(argspec.varargs, '')}"
            parser.add_argument(argspec.varargs, nargs="*",
                                type=argspec.annotations.get(argspec.varargs), help=helptxt)
        if argspec.kwonlydefaults:
            for k, v in argspec.kwonlydefaults.items():
                helptxt = f"{args_help_map.get(k, '')}"
                parser.add_argument(f"-{k}", default=v,
                                    type=argspec.annotations.get(k), help=f"{helptxt}, 默认 {v}")
        if argspec.varkw:
            helptxt = f"{args_help_map.get(argspec.varkw, '')}"
            parser.add_argument(
                f"--{argspec.varkw}", nargs="*", action='append', type=argspec.annotations.get(argspec.varkw), help=helptxt)
        args = parser.parse_args()

        def get_kw():
            kw = {}
            if argspec.varkw:
                for itemlist in getattr(args, argspec.varkw) or []:
                    for i in itemlist:
                        k, v = re.split(r"=", i, maxsplit=1)
                        kw[k] = v
            return kw

        def get_default_kw():
            default_kw = {}
            if argspec.kwonlydefaults:
                for arg in argspec.kwonlydefaults.keys():
                    default_kw[arg] = getattr(args, arg)
            return default_kw

        def get_varargs():
            if argspec.varargs:
                return getattr(args, argspec.varargs)
            return []

        def get_args():
            return [getattr(args, arg) for arg in argspec.args]

        return f(
            *get_args(),
            *get_varargs(),
            **get_default_kw(),
            **get_kw()
        )

    def __call__(self, *args, **kw):
        return self.__f(*args, **kw)
