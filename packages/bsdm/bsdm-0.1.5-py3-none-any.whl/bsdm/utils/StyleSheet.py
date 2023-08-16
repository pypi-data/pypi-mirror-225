import re
import json

import utils.config as config

from utils.logger import LOGGER

class StyleSheet: 
    
    __STYLESHEET = None

    @classmethod
    def __cleanElementString(cls, elementString):
        _elementString =  re.sub('/\*.*\*/', '', elementString) # remove comme (/* comment */ like)
        return _elementString
    
    @classmethod
    def __transformCSSToDict(cls, cssElements):
        
        _keysValues = re.compile(r"([\w(\);\s\#\"\-\.]+):([\w:\(\)\s\#\"\-\.]*)[\W\n]*")
    
        _jsonElementItems= {}
            
        for _keyValue in _keysValues.finditer(cssElements):
            _jsonElementItems[_keyValue.group(1).strip()] = _keyValue.group(2).strip()
        
        return(_jsonElementItems)
    
    @classmethod
    def __substituteVar(cls, cssStyleSheet, styleSheetVar):

        _cssStyleSheet = cssStyleSheet
        
        for var  in styleSheetVar:
            _cssStyleSheet = re.sub('var\s*\(\s*\-\-'+var+'\s*\)', styleSheetVar[var], _cssStyleSheet)
        
        return _cssStyleSheet
    
    @classmethod
    def __loadElementsStyle(cls, cssStyleSheet, styleSheetVar):
        
        _cssStyleSheet = re.sub('/\*.*\*/', '',  cssStyleSheet)                            # remove comme (/* comment */ like)        
        _cssStyleSheet = StyleSheet.__substituteVar(_cssStyleSheet, styleSheetVar)
        
        _elementPattern = re.compile(r"\.([a-zA-Z0-9:\(\);\s\#\"\-\.\_]+)[\s]*{\s*([a-zA-Z0-9(\);\s\#\"\-\.\_]+:[a-zA-Z0-9:\(\);\s\#\"\-\.\_]*)}")
        
        _elementStyle = {}
        
        for _element in _elementPattern.finditer(_cssStyleSheet):
            _elementStyle[_element.group(1).strip()] = StyleSheet.__transformCSSToDict(_element.group(2))
        
        return _elementStyle

    @classmethod
    def __listVars(cls, cssStyleSheet):
        _styleSheetVars = {}

        _cssStyleSheet = StyleSheet.__cleanElementString(cssStyleSheet)
        
        _varPattern = re.compile(r"\-\-([a-zA-Z0-9\s\-]+:[a-zA-Z0-9\s\#\"\-\.]+);")

        for _var in _varPattern.finditer(_cssStyleSheet):
            tmp = _var.group(1).split(":")
            _styleSheetVars[tmp[0].strip()] = tmp[1].replace('"','').strip()
            
        return _styleSheetVars

    @classmethod
    def loadFromCSSStyleSheet(cls, cssStyleSheet):
        _styleSheetVars = StyleSheet.__listVars(cssStyleSheet)    
        StyleSheet.__STYLESHEET = StyleSheet.__loadElementsStyle(cssStyleSheet, _styleSheetVars) 
        config.STYLESHEET = StyleSheet.__STYLESHEET