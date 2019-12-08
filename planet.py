#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 2 10:39:41 2019

@author: kamel
"""
class DataPath:
        """ This class will be used to define a new planet in our 
        universe"""
        def __init__(self):
            self._path = list()
            self._autonomy = list()
            self._time = list()
            self.proba = int()
        
        def _get_path(self):
            return self._path
        
        def _set_path(self, path_list):
            self._path = path_list
        
        def _get_autonomy(self):
            return self._autonomy
        
        def _set_autonomy(self, autonomy_list):
            self._autonomy = autonomy_list
            
        def _get_time(self):
            return self._time
             
        def _set_time(self, time_list):
            self._time = time_list
            
        def _get_proba(self):
            return self._proba
        
        def _set_proba(self, path_proba):
            self._proba = path_proba
            
        #def __repr__(self):
        #    return "<Path={} Fuel Level={}, Travel Length={}, Probability of Success={}>".format(
        #        self.path, self.autonomy, self.time, self.proba)
            
        path = property(_get_path,_set_path)
        autonomy = property(_get_autonomy,_set_autonomy)
        time = property(_get_time,_set_time)
        proba = property(_get_proba,_set_proba)

        
