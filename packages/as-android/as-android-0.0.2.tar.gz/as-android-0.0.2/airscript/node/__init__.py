from typing import Union


class Selector:
    def __init__(self, mode: int = 0):
        pass

    def find(self) -> 'Node':
        return Node()

    def find_all(self) -> '[Node]':
        return [Node()]

    def id(self, nid: str):
        return self

    def text(self, ntext: str):
        return self

    def type(self, ntype: str):
        return self

    def desc(self, ndesc: str):
        return self

    def hintText(self, nhintText: str):
        return self

    def packageName(self, npackageName: str):
        return self

    def path(self, pathstr: str):
        return self

    def inputType(self, ntype: int):
        return self

    def childCount(self, nccount: int):
        return self

    def inputType(self, ninputtype: int):
        return self

    def maxTextLength(self, nmax: int):
        return self

    def clickable(self, nclickable: bool):
        return self

    def checkable(self, ncheckable: bool):
        return self

    def checked(self, nchecked: bool):
        return self

    def editable(self, neditable: bool):
        return self

    def enabled(self, nenabled: bool):
        return self

    def dismissable(self, ndismissable: bool):
        return self

    def focusable(self, nfocusable: bool):
        return self

    def focused(self, nfocused: bool):
        return self

    def longClickable(self, nlongClickable: bool):
        return self

    def visible(self, nvisible: bool):
        return self

    def parent(self, *n: Union[float, int]):
        """
        获取父控件

        :param n: 获取第n个父元素,默认获取所有父元素
                        (2):获取爷爷元素
                        (3):获取太爷爷元素
                        (1,3):获取第1和第3个父元素
                        (1.3):获取第1-3 之间的所有父元素
        """
        return self

    def child(self, *n: Union[float, int]):
        """
        获取孩子控件

        :param n:可以填写多个数字
                不填写任何参数,获取所有孩子控件;
                当数字为正整数(例如1):获取第1个孩子控件;
                当数字为负整数(例如:-1) 获取倒数第1个孩子;
                当数字为正小数(例如:1.3):获取1-3之间的所有孩子;
                当数字为负小数(例如:-1.3):获取倒数 1-3之间的所有孩子;
        """
        return self

    def brother(self, *n: Union[float, int]):
        """
        获取兄弟控件

        :param n: 获取第n个兄弟控件|
                () 默认不填:获取所有兄弟控件|
                (1) 获取第一个兄弟控件 |
                (1,2) 获取第1和第2个兄弟控件|
                (1.4) 获取1-4之间的所有兄弟控件|
                (0.1) 获取当前控件的下一个兄弟控件|
                (-0.1) 获取当前空间的上一个兄弟控件|
                (-1) 获取倒数第1个兄弟控件
        """
        return self


class Rect:
    def __init__(self):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        pass

    def width(self):
        return 0;

    def height(self):
        return 0;

    def centerX(self):
        return 0;

    def centerY(self):
        return 0;


class Node:
    def __int__(self):
        self.id = ""
        self.text = ""
        self.type = ""
        self.desc = ""
        self.hintText = ""
        self.packageName = ""
        self.rect = Rect()
        self.childCount = 0
        self.inputType = 0
        self.maxTextLength = 0
        self.clickable = True
        self.checkable = True
        self.checked = True
        self.editable = True
        self.enabled = True
        self.visible = True
        self.dismissable = True
        self.focusable = True
        self.focused = True
        self.longClickable = True

        pass

    def find(self, sel: Selector):
        return self

    def find_all(self, sel: Selector):
        return [self]

    def click(self):
        return True

    def long_click(self):
        return True

    def slide(self, ori: int):
        """
        滑动

        :param ori: 滑动的方向;
                    -1:向前滑动;
                    1:向后滑动
        """
        return True

    def input(self, msg: str):
        """
        输入信息

        :param msg: 输入的信息
        """
        return True

