import copy
from kevin_toolbox.nested_dict_list import traverse


def copy_(var, b_deepcopy=False):
    """
        复制嵌套字典列表 var，并返回其副本

        参数：
            var
            b_deepcopy:         <boolean> 是否进行深拷贝
                                    默认为 False 此时仅复制结构，但叶节点仍在 var 和其副本之间共享
                                    当设置为 True 时，进行完全的深拷贝
    """
    if b_deepcopy:
        return copy.deepcopy(var)

    return traverse(var=[var], match_cond=lambda _, __, value: isinstance(value, (list, dict,)),
                    action_mode="replace", converter=lambda _, value: value.copy(),
                    traversal_mode="dfs_pre_order", b_traverse_matched_element=True)[0]


if __name__ == '__main__':
    x = dict(acc=[0.66, 0.78, 0.99], )
    copy_(var=x, b_deepcopy=False)
