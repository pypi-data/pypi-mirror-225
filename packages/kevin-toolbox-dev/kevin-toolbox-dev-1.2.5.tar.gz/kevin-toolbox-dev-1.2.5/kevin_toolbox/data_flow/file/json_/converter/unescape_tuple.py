def unescape_tuple(x):
    """
        将 tuple 进行反转义
            转义：     x ==> f"<eval>{x}"
            反转义：   f"<eval>{x}" ==> x

        为什么要进行转义？
            由于 json 中会将 tuple 作为 list 进行保存，因此在保存过程中会丢失相应信息。
    """
    if isinstance(x, str) and x.startswith("<eval>"):
        x = x[6:]
        if not x.startswith("<eval>"):
            x = eval(x)
        return x
    else:
        return x


if __name__ == '__main__':
    print(unescape_tuple("<eval>(1, 2, \"'1'\")"))
    # (1, 2, "\'1\'")
    print(unescape_tuple("<eval><eval>233"))
    # "<eval>233"
