import os
import json
import pickle
from copy import deepcopy
from datetime import date
from dict_class import *

import numpy as np
from config import *


class SpecialDict(object):
    __format = ['date', 'data', 'comment', 'lock']

    def __init__(self, d1, lock=False, comment='', count=0):
        self.__date    = date.today().strftime('%B %d, %y')
        self.__data    = d1
        self.__lock    = lock
        self.__comment = comment
        self.__count   = count

    @property
    def date(self):
        return self.__date
    @property
    def lock(self):
        return self.__lock

    def add_lock(self):
        self.__lock    = True

    def remove_lock(self):
        self.__lock    = False

    def add_comment(self, words):
        self.__comment = words

    def get_status(self, print=True):
        status = 'date = %s \t length = %i \t lock = %s \t comment = %s'%(self.__date, self.__count, self.__lock, self.__comment)
        if print:   print(status)
        else:       return status
    

class SpecialDictList(object):
    __format = ['title', '__dictlist', 'lock', 'comment']

    def __init__(self, title):
        self.__title    = title
        self.__dictlist = []
        self.__lock     = False
        self.__comment  = ''
        self.__format   = []
        self.__deleted  = []

    def set_format(self, keys):
        if self.__lock:
            raise AttributeError("It is locked!")
        else:
            self.__format   = keys

    def set_comment(self, comment):
        self.__comment = comment

    def add_lock(self):
        self.__lock = True

    def remove_lock(self):
        self.__lock = False

    def status(self):
        print('Saved copies:\n\t # \t Date \t Lock \t Comment')
        for i, _dict in enumerate(self.__dictlist):
            print('\t %i \t %s'%(i+1, _dict.get_status(print=False)))

    @property
    def format(self):
        return self.__format

    @property
    def comment(self):
        return self.__comment

    @property
    def title(self):
        return self.__title

    @property
    def lock(self):
        return self.__lock

    @property
    def deleted(self):
        return self.__deleted
        
    def keep(self, d1, comment='', lock=False, count='N/A'):
        """
            This function saves the given dictionary

        Args:
            d1      (dict)          : [description]
            comment (str, optional) : [description]. Defaults to ''.
            lock    (bool, optional): [description]. Defaults to False.
        """ 
        if self.__lock:
            raise AttributeError("It is locked!")

        if not isinstance(count, int):
            count = len(d1)

        d = SpecialDict(d1, comment=comment, lock=lock, count=count)
        self.__dictlist.append(d)

    def delete(self, n):
        assert isinstance(n, int), 'index must be integer'
        if self.__lock:
             raise AttributeError("It is locked!")
        else:
            idx = n - 1
            self.__deleted = self.__dictlist.pop(idx)

    def recover(self, d):
        assert isinstance(d, SpecialDict), ''
        self.__dictlist.append(d)


    def pick(self, n):
        assert isinstance(n, int), 'Give which copy you want to read as integer'
        _dic    = self.__dictlist[n-1]
        _dic.get_status()

        special = AttrDict()
        special._freezed = True
        special.from_dict(_dic.__data)
        special.keys = _dic.__data.keys()

        return special


    def __clear(self, length):
        if len(self.__dictlist) > length:
            for i, dic in enumerate(self.__dictlist):
                if dic.__lock == True:
                    continue
                else:
                    self.__deleted = self.__dictlist.pop(i)
                    self.__clear(length)

    def clear(self, length):
        self.delete_reset()
        self.__clear(length)

    def delete_reset(self):
        self.__deleted = None

    def lock_dict(self, n):
        assert isinstance(n, int), 'index must be integer'
        if self.__lock:
             raise AttributeError("It is locked!")
        else:
            idx = n - 1
            self.__dictlist[idx].add_lock()

    def unlock_dict(self, n):
        assert isinstance(n, int), 'index must be integer'
        if self.__lock:
             raise AttributeError("It is locked!")
        else:
            idx = n - 1
            self.__dictlist[idx].remove_lock()



class history(object):
    def __init__(self, length=10):
        self.__list = []
        self.__date = []
        self.length = length

    def __get_date(self):
        return date.today().strftime('%B %d, %y')

    def add(self, line):
        assert isinstance(line, str), 'only strings are accepted in history'
        self.__list.append(line)
        self.__date.append(self.__get_date())
        self.__adjust()
    
    def set_length(self, n):
        assert isinstance(n, int), 'history length can only be integer'
        self.length = n

    def print(self):
        for i, date, line in enumerate(zip(self.__date, self.__list)):
            print('%i /t %s /t %s'%(i+1, date, line))

    def __adjust(self):
        self.__list = (self.__list.reverse()[:self.length]).reverse()
        self.__date = (self.__date.reverse()[:self.length]).reverse()

    def update(self):
        print(print('\t -- %s /t %s'%(self.__date[-1], self.__list[-1])))