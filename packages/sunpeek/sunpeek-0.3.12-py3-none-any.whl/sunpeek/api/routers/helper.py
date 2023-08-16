# -*- coding: utf-8 -*-
def update_obj(obj, update_model):
    update_dict = update_model.dict(exclude_unset=True)

    for key, val in update_dict.items():
        if val != getattr(obj, key):
            setattr(obj, key, val)

    return obj
