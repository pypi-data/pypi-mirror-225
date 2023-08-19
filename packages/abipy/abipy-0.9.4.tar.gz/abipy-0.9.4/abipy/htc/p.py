#!/usr/bin/env python
from __future__ import annotations

from typing import List

from pydantic import BaseModel


def _find_submodels(self, class_type):
    """
    Warning: does not handle containers (list or dict)
    with models e.g. [instance_of_class_type,  ...]
    """
    desc_list = []
    for k, v in self:
        #print(type(k), type(v))
        print("k:", k, "v:", v)
        if isinstance(v, class_type):
            desc_list.append(v)

        elif isinstance(v, BaseModel):
            sub_list = _find_submodels(v, class_type)
            desc_list.extend(sub_list)

        elif isinstance(v, (list, tuple)):
            for o in v:
                if isinstance(o, class_type):
                    desc_list.append(o)
                elif isinstance(o, BaseModel):
                    sub_list = _find_submodels(o, class_type)
                    desc_list.extend(sub_list)

    return desc_list


def find_submodels(self, class_type):
    desc_list = _find_submodels(self, class_type)
    # Remove duplicated objects if any
    d = {id(desc): desc for desc in desc_list}
    return list(d.values())


class NestedModel(BaseModel):
    foo: int


class MyModel(BaseModel):
    bar: str = "hello"
    one: NestedModel
    two: NestedModel

class TopLevelModel(BaseModel):
    my_model1: MyModel
    info: str = "This is the top level model"
    my_model2: MyModel


my_model = MyModel(one=NestedModel(foo=1), two=NestedModel(foo=2))

mlist = find_submodels(my_model, NestedModel)
#print(mlist)
assert len(mlist) == 2 and all(isinstance(mod, NestedModel) for mod in mlist)
for mod in mlist:
    mod.foo *= 100

assert my_model.one.foo == 100
assert my_model.two.foo == 200

# Note that here we have two references to same object.
top_model = TopLevelModel(my_model1=my_model, my_model2=my_model)
mlist = find_submodels(top_model, NestedModel)
print(mlist)
assert len(mlist) == 2 and all(isinstance(mod, NestedModel) for mod in mlist)
for mod in mlist:
    mod.foo = mod.foo / 100

assert top_model.my_model1.one.foo == 1
assert top_model.my_model1.two.foo == 2


class ModelWithList(BaseModel):
    info: str = "This is the top level model"
    mlist: List[MyModel]
    items: List[int]


model1 = MyModel(one=NestedModel(foo=1), two=NestedModel(foo=2))
model2 = MyModel(one=NestedModel(foo=20), two=NestedModel(foo=40))

model_with_list = ModelWithList(mlist=[model1, model2], items=[1,2,3])

mlist = find_submodels(model_with_list, NestedModel)
print(mlist)
assert len(mlist) == 4 and all(isinstance(mod, NestedModel) for mod in mlist)
#for mod in mlist:
#    mod.foo = mod.foo / 100
