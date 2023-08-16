import re
import os
import inspect
import pkgutil
import weakref
import kevin_toolbox.nested_dict_list as ndl


class Registry:
    """
        注册器
            具有以下功能
            - 管理成员，包括添加 add()、获取 get() pop() 成员等
            - 支持通过装饰器 register() 来添加成员
            - 支持通过 collect_from_paths() 搜索指定的路径，当该路径下的模块被 register() 装饰器包裹或者通过 add() 添加成员时，将自动导入
            （用于解决python中的模块是惰性的问题）

        使用方法：
            以目录结构：
                xx/——— modules_dir
                 |       |——— a.py
                 |       |___ ...
                 |——— test.py
            为例。
            我们的目标是在 test.py 中，构建一个能够自动加载 modules_dir 中待注册成员的 Registry 实例。
            具体步骤如下：
                1. 在文件 test.py 中：
                    # 创建注册器实例
                    DB = Registry(uid="DB")
                    # 设置搜索路径
                    DB.collect_from_paths(path_ls=["xx/modules_dir"])

                2. 在 modules_dir 下需要加载的成员中，以 a.py 为例：
                    # 导入注册器实例
                    from xx.test import DB
                    # 使用 DB.register() 装饰器注册
                    @DB.register(name=":my_module")
                    class A:
                        ...
                    # 使用 add() 函数注册
                    DB.add(obj=233, name=":var:c")

                3. 在文件 test.py 中：
                    # 获取已注册成员
                    module = DB.get(name=":my_module")

                4. 如果需要在其他文件中获取已有注册器实例，除了用 import 之外，还可以直接用 uid
                    # 获取指定 uid 下的实例
                    temp = Registry(uid="DB")
    """
    name = "registry made by kevin"
    __instances = weakref.WeakValueDictionary()  # {uid: instance_i, ...} 用于保存创建的实例
    __counter = 0

    def __new__(cls, *args, **kwargs):
        """
            __new__函数返回的实例，将作为self参数被传入到__init__函数。
                如果__new__函数返回一个已经存在的实例（不论是哪个类的），__init__还是会被调用的，所以要特别注意__init__中对变量的赋值。
        """
        if "uid" in kwargs:
            uid = kwargs["uid"]
        else:
            while cls.__counter in cls.__instances:
                cls.__counter += 1
            uid = cls.__counter

        # 获取实例
        if uid in cls.__instances:
            # 返回已存在的实例
            self = cls.__instances[uid]
        else:
            # 传入 __init__ 中新建一个实例
            self = super().__new__(cls)
        return self

    def __init__(self, *args, **kwargs):
        """
            参数：
                uid:                <hashable> 实例的唯一标识符
                                        - 不设置。新建一个实例，并自动分配一个整数作为 uid（一般是此时已有实例的数量-1），
                                            并将该实例记录到类变量 instances_of_Registry 中。
                                        - 设置为 None。新建一个实例，但不记录到类变量 instances_of_Registry 中。
                                        - 设置为其他值。根据 uid 到类变量 instances_of_Registry 的已有实例中寻找相同的实例，
                                            若命中则返回已有实例，若无则以该 uid 新建一个实例并添加到 instances_of_Registry 中。
                                            （使用该特性可以构造单例模式）
                                        默认为不设置。
        """
        try:
            getattr(self, "uid")
        except:
            pass
        else:
            return  # 如果是从 __new__ 中获取的已有的实例则不重复进行参数赋值
        self.database = dict()
        #
        self.uid = kwargs.get("uid", Registry.__counter)
        self._path_to_collect = []
        self._item_to_add = []
        # 记录到 __instances 中
        if self.uid is not None:
            Registry.__instances[self.uid] = self

    def add(self, obj, name=None, b_force=False, b_execute_now=True):
        """
            注册

            参数：
                obj：            待注册成员
                                    可以是函数、类或者callable的实例
                                    也可以是各种 int、float、str变量
                                    总之一切对象皆可
                name：           <str> 成员名称
                                    默认为 None，此时将从被注册对象 obj 的属性中尝试推断出其名称。
                                        若 obj 中有 name 或者 __name__ 属性（优先选择name），则推断出的名称是 f'{obj.name}' 或者 f':{obj.__name__}'；
                                            进一步若有 version 属性，则为 f'{obj.name}:{obj.version}'
                                        否则报错。
                                        比如下面的类：
                                            class A:
                                                version="1.0"
                                        的默认注册名称将是 ":A:1.0"
                                        另一种等效的写法是：
                                            class A:
                                                name=":A:1.0"
                                    对于 int、str 和其他没有 name 或者 __name__ 属性的变量则必须要手动指定 name 参数。
                        需要注意的是，成员的名称确定了其在注册器内部 database 中的位置，名称的解释方式参考 get_value() 中的介绍。
                        因此不同的名称可能指向了同一个位置。
                b_force：          <boolean> 是否强制注册
                                    默认为 False，此时当 name 指向的位置上已经有成员或者需要强制修改database结构时，将不进行覆盖而直接跳过，注册失败
                                    当设置为 True，将会强制覆盖
                b_execute_now:      <boolean> 现在就执行注册
                                        默认为 True，否则将等到第一次执行 get() 函数时才会真正尝试注册

            返回：
                <boolean>   是否注册成功
        """
        # 检验参数
        if name is None:
            name = getattr(obj, "name", None)
            if name is not None:
                name = f'{name}'
            else:
                name = getattr(obj, "__name__", None)
                name = f':{name}' if name is not None else name
            if name is not None:
                version = getattr(obj, "version", None)
                if version is not None:
                    name += f':{version}'
        assert isinstance(name, (str,))

        #
        if not b_execute_now:
            self._item_to_add.append(dict(obj=obj, name=name, b_force=b_force, b_execute_now=True))
            return True

        # 尝试注册
        temp = ndl.set_value(var=ndl.copy_(var=self.database, b_deepcopy=False), name=name, value=obj,
                             b_force=True)
        # check
        if not b_force:
            inc_node_nums = ndl.count_leaf_node_nums(var=obj) if isinstance(obj, (list, dict)) else 1  # 应该增加的节点数量
            if ndl.count_leaf_node_nums(var=temp) != ndl.count_leaf_node_nums(var=self.database) + inc_node_nums:
                # print(f'registration failed, name {name} may be a conflict with an '
                #       f'existing member in {[i for i, j in ndl.get_nodes(var=self.database)]}')
                return False

        self.database = temp
        return True

    def get(self, name, b_pop=False, **kwargs):
        """
            获取

            参数：
                name:           <str> 成员名称
                b_pop:          <boolean> 取值的同时移除该成员
                                    默认为 False
                default:        默认值
                                    找不到时，若无默认值则报错，否则将返回默认值
        """
        # 加载待注册成员
        if len(self._item_to_add) > 0:
            for i in self._item_to_add:
                self.add(**i)
            self._item_to_add.clear()
        if len(self._path_to_collect) > 0:
            for i in self._path_to_collect:
                self.collect_from_paths(**i)
            self._path_to_collect.clear()

        return ndl.get_value(var=self.database, name=name, b_pop=b_pop, **kwargs)

    def clear(self):
        self.database.clear()

    # -------------------- 装饰器 --------------------- #

    def register(self, name=None, b_force=False, b_execute_now=True):
        """
            用于注册成员的装饰器
                成员可以是函数、类或者callable的实例

            参数：
                name：           <str> 成员名称
                                    默认为 None
                b_force：        <boolean> 是否强制注册
                                    默认为 False
                b_execute_now:  <boolean> 现在就执行注册
                                    默认为 True
                                （以上参数具体参考 add() 函数介绍）
        """

        def wrapper(obj):
            nonlocal self, name, b_force, b_execute_now
            self.add(obj, name=name, b_force=b_force, b_execute_now=b_execute_now)
            return obj

        return wrapper

    # -------------------- 通过路径添加 --------------------- #

    def collect_from_paths(self, path_ls=None, path_ls_to_exclude=None, b_execute_now=False):
        """
            遍历 path_ls 下的所有模块，并自动导入其中主要被注册的部分
                比如被 register() 装饰器包裹或者通过 add() 添加的部分

            参数：
                path_ls:            <list of paths> 需要搜索的目录
                path_ls_to_exclude: <list of paths> 需要排除的目录
                b_execute_now:      <boolean> 现在就执行导入
                                        默认为 False，将等到第一次执行 get() 函数时才会真正尝试导入

                        注意，在某个文件中使用 Registry 实例时，应尽量避免下面的情况：
                            1. 在当前脚本中显式导入该实例前，调用了其他脚本执行了该实例的 collect_from_paths() 函数，且设置 b_execute_now=True，
                                此时若导入的成员中有类，且该类继承自某个父类，且在初始化时使用了 super(xx,self).__init__ 继承初始化函数，将出现
                                TypeError: super(type, obj): obj must be an instance or subtype of type 的错误
                            2. 在模块的 __init__.py 文件中使用 collect_from_paths()
                        为了避免情况 1，应该尽量避免设置 b_execute_now=True。
                            或者省略 super(xx,self).__init__ 中的参数改为 super().__init__
        """
        # 检查调用位置
        caller_frame = inspect.stack()[1]
        assert os.path.basename(caller_frame.filename) != "__init__.py", \
            f'calling Registry.collect_from_paths() in __init__.py is forbidden, file: {caller_frame.filename}.\n' \
            f'you can call it in other files, and then import the result of the call in __init__.py'

        #
        if not b_execute_now:
            self._path_to_collect.append(
                dict(path_ls=path_ls, path_ls_to_exclude=path_ls_to_exclude, b_execute_now=True))
            return

        #
        if path_ls is not None:
            temp = []
            for path in filter(lambda x: os.path.isdir(x), path_ls):
                temp.append(path)
                for root, dirs, _ in os.walk(path, topdown=False):
                    temp.extend([os.path.join(root, i) for i in dirs])
            if path_ls_to_exclude is not None:
                for path_ex in path_ls_to_exclude:
                    if not os.path.exists(path_ex):
                        continue
                    for i in reversed(range(len(temp))):
                        if os.path.samefile(os.path.commonpath([path_ex, temp[i]]), path_ex):
                            temp.pop(i)
            # 从深到浅导入，可以避免继承引起的 TypeError: super(type, obj) 类型错误
            path_ls = list(set(temp))
            path_ls.sort(reverse=True)

        temp = None
        for loader, module_name, is_pkg in pkgutil.walk_packages(path_ls):
            module = loader.find_module(module_name).load_module(module_name)
            if temp is None:
                for name, obj in inspect.getmembers(module):
                    if getattr(obj, "name", None) == Registry.name and getattr(obj, "uid", None) == self.uid:
                        temp = obj
                        break
        if temp is not None:
            self.database = temp.database

    # -------------------- 其他 --------------------- #

    @property
    def instances_of_Registry(self):
        return dict(Registry.__instances)


UNIFIED_REGISTRY = Registry(uid="UNIFIED_REGISTRY")
