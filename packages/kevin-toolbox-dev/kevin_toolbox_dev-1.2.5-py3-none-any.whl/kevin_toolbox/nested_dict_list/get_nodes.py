from kevin_toolbox.nested_dict_list import traverse, get_value
from kevin_toolbox.nested_dict_list.name_handler import parse_name


def get_nodes(var, level=-1, b_strict=True):
    """
        获取嵌套字典列表 var 中所有叶节点
            以列表 [(name,value), ...] 形式返回，其中名字 name 的解释方式参考 name_handler.parse_name() 介绍

        参数：
            var:                待处理数据
                                    当 var 不是 dict 或者 list 时，返回空列表
            level:              <int> 获取第几层节点
                                    默认为 -1，获取叶节点
            b_strict:           <boolean> 当树结构的某个分枝上的深度不满足 level 的要求时，是否将路径末端的叶节点（当level为正数）或者
                                    路径首部的根节点（当level为负数）添加到输出中。
                                    例如，对于 {'d': {'c': 4}, 'c': 4}，
                                        当 b_strict=True 时，
                                            对于 level=-10 和 level=10 返回的都是 []
                                        当 b_strict=False 时，
                                            对于 level=-10 返回的是 [('', {'d': {'c': 4}, 'c': 4}), ]
                                            对于 level=10 返回的是 [(':c', 4), (':d:c', 4)]
                                    默认为 True，不添加。
    """
    assert isinstance(level, (int,))
    if level == 0:
        return [("", var)]
    res = []

    # 首先找出所有叶节点 level=-1
    def func(_, idx, v):
        nonlocal res
        if not isinstance(v, (list, dict,)):
            res.append((idx, v))
        return False

    traverse(var=var, match_cond=func, action_mode="skip", b_use_name_as_idx=True)

    if level != -1:
        names = set()
        if level < -1:
            for name, _ in res:
                root_node, _, node_ls = parse_name(name=name, b_de_escape_node=False)
                node_ls.insert(0, root_node)
                temp = [len(i) for i in node_ls[level + 1:]]
                temp = len(name) - sum(temp) - len(temp)
                if b_strict and temp < 0:
                    continue
                else:
                    temp = max(temp, 0)
                names.add(name[:temp])
        elif level > 0:
            for name, _ in res:
                root_node, _, node_ls = parse_name(name=name, b_de_escape_node=False)
                node_ls.insert(0, root_node)
                temp = [len(i) for i in node_ls[:level + 1]]
                temp = sum(temp) + level
                if b_strict and temp > len(name):
                    continue
                names.add(name[:temp])
        else:
            raise ValueError
        res.clear()
        for name in names:
            res.append((name, get_value(var=var, name=name)))

    return res


if __name__ == '__main__':
    import numpy as np

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]
    print(get_nodes(var=x, level=-1))
    print(get_nodes(var=x, level=-2))
    print(get_nodes(var=x, level=-3))
    print(get_nodes(var=x, level=-4))

    print(get_nodes(var=x, level=0))
    print(get_nodes(var=x, level=1))
    print(get_nodes(var=x, level=2))
    print(get_nodes(var=x, level=3))
    print(get_nodes(var=x, level=4))
    print(get_value(var=x, name=""))
