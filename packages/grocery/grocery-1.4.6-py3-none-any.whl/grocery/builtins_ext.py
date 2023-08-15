from collections import Counter as BuiltInCounter
import operator
from enum import Enum


class list_ext(list):
    def __cmp_dict(self, dictionary: dict, **kwargs):
        if not isinstance(dictionary, dict):
            return False
        for key__cmp, val in kwargs.items():
            key, cmp = key__cmp.split('__')
            if not getattr(operator, cmp)(dictionary.get(key), val):
                return False
        return True

    def filter_dict(self, *args, **kwargs):
        for item in self:
            if self.__cmp_dict(item, **kwargs):
                yield item

    def group(self, num):
        """将列表以n个为一组进行分组"""
        for i in range(0, len(self), num):
            yield self[i:i + num]


class Counter(BuiltInCounter):
    def __add__(self, other):
        """与builtin的Counter一样，只是Counter相加后，不过滤值为0的key"""
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count + other[elem]
            result[elem] = newcount
        for elem, count in other.items():
            if elem not in self:
                result[elem] = count
        return result


class EnumExt(Enum):
    @classmethod
    def labels(cls):
        """
        示例：
        {
            cls.key1 = 'label1',
            cls.key2 = 'label2'
        }
        """
        return {}

    @classmethod
    def enum_list(cls, label=True):
        if label:
            return [(cls.labels().get(item), item.value) for item in cls]
        return [(item.name, item.value) for item in cls]

    @classmethod
    def choices(cls, blank=False):
        # 返回适用于Django字段为choices类型的列表
        choice_list = [(item.value, cls.labels().get(item, item.name)) for item in cls]

        if blank:
            choice_list.insert(0, ('', ''))
        return choice_list

    @classmethod
    def get_val_by_label(cls, label):
        label_val_map = {v: k for k, v in cls.labels().items()}
        print(label_val_map)
        return label_val_map.get(label).value
