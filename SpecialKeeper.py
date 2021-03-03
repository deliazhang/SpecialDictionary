import numpy as np
import pickle
from Specials import *
from datetime import date

class SpecialDictKeeper(object):

    def __init__(self, debug=False):
        self.__length  = 10
        self.__history = history()
        self.debug     = debug
        self.__new     = False
        self.__deleted = SpecialDict(dict())

    def loadKeeper(self, path):
        self.__check_handler(path)
        with open(path, 'rb') as f:
            self.__dict__.update(pickle.load(f))
        self.__dicts.status()

    def saveKeeper(self, path):
        self.__check_handler(path)
        with open(path, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def createKeeper(self, name=''):
        self.__new   = True
        self.instruction()
        self.__add_history('init')
        self.__dicts = SpecialDictList(name)

    def get_Special(self, n):
        return self.__dicts.pick(n)

    def add_Special(self, data, lock=False, comment=''):
        """
            This function format the dictionary to the SpecialDict format 
            with data format specified by 'keys'

        Args:
            keys    (list)         : list of keys acceptable 
            data    (dict)         : data in dictionary form, keys must be identical to 'keys'
            comment (str, optional): comment. Defaults to ''

        Returns:
            dict:  return the formatted SpecialDict
        """        
        
        print( '-- total %i items are presented'%len(data) )
        keys  = self.__dicts.format
        d1    = { k:v for k,v in {k:v if k in keys else print('-- item %s is rejected, remove it and try again'%k) for k,v in data.items() }.items() if v is not None }
        d2    = list(None if k in d1.keys() else print('-- item %s is absent'%k) for k in keys )
        print( '-- total %i items are accepted'%len(d2) )
        
        self.__dicts.keep(d1, lock=lock, comment=comment, count=len(d2))
        self.__add_history('add')
        self.__clear()

    def delete_Special(self, n):
        self.__dicts.delete(n)
        self.__clear()

    def __clear(self):
        self.__dicts.clear(self.__length)
        self.__deleted = self.__dicts.deleted
        self.__dicts.delete_reset()

        if isinstance(self.__deleted, SpecialDict):
            self.__add_history('del')

    def recover(self):
        """recover the last deleted one"""
        self.__dicts.recover(self.__deleted)
        self.__add_history('recover')
        self.__deleted =  SpecialDict(dict())

    def instruction(self):
        print('-------------------------- Special Dict Keeper Helper --------------------------')
        print('You are creating a SpecialDictKeeper, which is composed of a SpecialDictList full of SpecialDicts.')
        print('Follow the following steps to setup a DictKeeper:')
        print('\t 1) Give a path to create a pickle file with keeper_handler(path)')
        print('\t 2) Give a (nested) list of strings that represents the keys for the SpecialDicts with set_format(list)')
        print('\t 3) The default length of SpecialDictList is 10. Set it to another number or zero for infinity with set_length(n)')
        print('Now you are done! Use special_push() to push a dictionary to the SpecialDictList')

    def __add_history(self, keyword):
        ## viable keywords are 'init', 'add', 'del', 'set_key', 'change_key', 'recover', 'lock_lst
        date = self.__get_date()
        if keyword == 'init':
            self.__history.add('SpecialDictKeeper created')
        if keyword == 'add':
            self.__history.add('A SpecialDict is added to %s'%(self.__dicts.title))
        if keyword == 'del':
            self.__history.add('A SpecialDict[%s] is deteled from %s'%(self.__deleted.date, self.__dicts.title))
        if keyword == 'set_key':
            self.__history.add('The format\'s changed')
        if keyword == 'change_key':
            self.__history.add('The format\'s changed')
        if keyword == 'lock_lst':
            self.__history.add('The SpecialKeeer is locked')
        if keyword == 'unlock_lst':
            self.__history.add('The SpecialKeeer is unlocked')
        if keyword == 'lock':
            self.__history.add('A SpecialDict is locked')
        if keyword == 'unlock':
            self.__history.add('A SpecialDict is unlocked')
        else:
            self.print('Unknow keywords, cannot update history.')
            return

        self.__history.update()




    def __check_handler(self, path):
        assert self.__new != os.path.exists(path), 'new for new keeper, \nold for old keeper, \nbut all have to be a good one'
    
    def __check_keys(self, keys, __check_0=[]):
        for key in keys:
            if not isinstance(key, str):
                if isinstance(key, list):
                    self.__check_keys(key, __check_0)
                else:
                    __check_0.append(False)
            else:
                __check_0.append(True)
        self.print(__check_0)
        return all(__check_0)

    def __get_date(self):
        return date.today().strftime('%B %d, %y')

    def set_length(self, n):
        self.__length = n if n > 0 else np.inf

    def print(self, message):
        if self.debug:
            print(message)

    @property
    def history(self):
        self.__history.print()
    @property
    def status(self):
        self.__dicts.status()

    def set_format(self, keys):
        assert self.__new, 'format already exist'
        assert self.__check_keys(keys), 'Key has to be string'
        self.__dicts.set_format(keys)
        self.__add_history('set_key')

    def change_format(self, keys):
        assert not self.__new, ''
        assert self.__check_keys(keys), 'Key has to be string'
        self.__dicts.set_format(keys)
        self.__add_history('change_key')

    def lock_Keeper(self):
        self.__dicts.add_lock()
        self.__add_history('lock_lst')

    def unlock_Keeper(self):
        self.__dicts.remove_lock()
        self.__add_history('unlock_lst')

    def lock_Special(self, n):
        self.__dicts.lock_dict(n)
        self.__add_history('lock')

    def unlock_Special(self, n):
        self.__dicts.unlock_dict(n)
        self.__add_history('unlock')