from dataclasses import dataclass
from datetime import datetime

class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        key = tuple(kwargs.get(attr) for attr in cls.__singleton_attributes__)
        if key not in cls.instances:
            cls.instances[key] = super().__call__(*args, **kwargs)
        else:
            # 更新属性
            instance = cls.instances[key]
            for attr, value in kwargs.items():
                if attr not in cls.__singleton_attributes__:
                    setattr(instance, attr, value)
        return cls.instances[key]

@dataclass
class NetValueData(metaclass=SingletonMeta):
    __singleton_attributes__ = ('date', 'prodcode')
    date:datetime
    prodcode:str
    prodname:str
    netvalue:float
    cum_netvalue:float
    netasset:float = None
    shares:float = None

@dataclass
class MailHeaderData():
    Date:datetime
    sender_name:str
    sender_addr:str
    receriver_name:str
    receriver_addr:str
    cc_name:str
    cc_addr:str
    Subject:str

