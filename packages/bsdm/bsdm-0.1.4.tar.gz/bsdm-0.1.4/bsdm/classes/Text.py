from svgwrite import cm, mm, px  
from math import ceil

import tkinter as Tkinter
import tkinter.font as tkFont

import re

import utils.config as config

from utils.logger import LOGGER



class Text(object):
    
    _TK_ROOT = Tkinter.Tk() 
        
    def __init__(self, x=0, y=0, text='', styleClass=None):
        self._x = x 
        self._y = y 
        self._text = text
        self._styleClass = "defaulttext " + styleClass
        self._size = None
        
        self._build()    

    def update(self, x=None, y=None, text=None, styleClass=None):
        
        if(x is not None):
            self._x = x 
        if(y is not None):
            self._y = y 
        if(text is not None):
            self._text = text
        if(styleClass is not None):
            self._styleClass = "defaulttext " + styleClass
        
        self._build()     

    def _build(self):
        self._size = Text.getTextMetrics(self._text, self._styleClass)           
        
        """
        self._entityBlock = config.DWG.rect(insert=( (self._x + config.MARGIN) * px, (self._y +config.MARGIN) * px), 
                                            size=((self._size['width']) * px, self._size['height'] * px),
                                            stroke_width=0)               
        """
        
        #+ 10 car 10 = margin. TODO: handles margin with CSS        
        self._entity = config.DWG.text(self._text, 
                                        insert=( (self._x + config.MARGIN) * px, 
                                        (self._y + self._size['height']*0.75 + config.MARGIN) * px))
        self._entity['class'] = self._styleClass     

    def _getSize(self):
        return self._size

    def getHeight(self):
        return self._getSize()['height']
        
    def getWidth(self):
        return self._getSize()['width']
        

    def addToGroup(self, group):
        """
        group.add(self._entityBlock)  
        """
        group.add(self._entity)
        


    @classmethod
    def __handleFontSize(cls, font_size):
        _font_size = re.sub(r'[^0-9\.]', '', font_size) 
        _font_units = re.sub(r'[^a-zA-Z]', '', font_size) 
        
        if(_font_units == 'px'):
            _font_size = 0 - int(ceil(float(_font_size)))
            
        return _font_size        

    @classmethod
    def __handleFontWeight(cls, font_weight):
        if(font_weight is None or font_weight != 'bold'):
            return Tkinter.font.NORMAL
        return Tkinter.font.BOLD
    
    @classmethod    
    def __handleFontWeight(cls, font_weight):
        if(font_weight is None or font_weight != 'bold'):
            return Tkinter.font.NORMAL
        return Tkinter.font.BOLD    
    
    @classmethod
    def __handleFontStyle(cls, font_style):
        if(font_style is None or font_style != 'italic'):
            return Tkinter.font.ROMAN
        return Tkinter.font.ITALIC    
    
    @classmethod
    def __handleFontDecoration(cls, fontDecoration):

        _fontDecoration = {}
        _fontDecoration['overstrike'] = 0
        _fontDecoration['underline'] = 0    
        
        if(fontDecoration is not None) :       
            if('line-through' in fontDecoration.lower()):
                _fontDecoration['overstrike'] = 1          
            if('underline' in fontDecoration.lower()):
                _fontDecoration['underline'] = 1      
        
        return _fontDecoration   
    
    @classmethod
    def __getTextMetrics(cls, text, fontFamily, fontSize, fontStyle=None, fontWeight=None, fontDecoration=None):

        font = None
        
        _fontSize = Text.__handleFontSize(fontSize)
        _fontWeight = Text.__handleFontWeight(fontWeight)
        _fontStyle = Text.__handleFontStyle(fontStyle)
        _fontDecoration = Text.__handleFontDecoration(fontDecoration)
        
        """    
        print("family= "+str(fontFamily)) 
        print("size= "+str(_fontSize))
        print("weight= "+str(_fontWeight)) 
        print("slant= "+str(_fontStyle))
        print("overstrike= "+str(_fontDecoration['overstrike']))
        print("underline= "+str(_fontDecoration['underline'] ))
        """
        
        font = tkFont.Font( family=fontFamily, 
                            size=_fontSize, 
                            weight=_fontWeight, 
                            slant=_fontStyle, 
                            overstrike=_fontDecoration['overstrike'],
                            underline=_fontDecoration['underline'] )
        
        if (font is not None) :
            _text_metrics = {}
            _text_metrics['width'] = font.measure(text)
            _text_metrics['height'] = font.metrics('linespace')
            return _text_metrics
        
        return None    
    
    @classmethod  
    def getTextMetrics(cls, text, styleClass):
        
        _textFontFamily = config.DEFAULTFONTFAMILY
        _textFontSize = config.DEFAULTFONTSIZE
        _textFontStyle = config.DEFAULTFONTSTYLE
        _textFontWeight = config.DEFAULTFONTWEIGHT 
        _textFontDecoration = config.DEFAULTFONTDECORATION       
        
        _textStyles = styleClass.split()
        
        for _textStyle in _textStyles :
            
            _textStyle = config.STYLESHEET[_textStyle] 
            
            try: 
                _textFontFamily = _textStyle['font-family']
            except:
                pass
            
            try: 
                _textFontSize = _textStyle['font-size']
            except:
                pass    
            
            try: 
                _textFontStyle = _textStyle['font-style']
            except:
                pass
            
            try: 
                _textFontWeight = _textStyle['font-weight']
            except:
                pass
            

            try: 
                _textFontDecoration = _textStyle['text-decoration']
            except:
                continue      
            
            
        
        return Text.__getTextMetrics(text, _textFontFamily, _textFontSize, fontStyle=_textFontStyle, fontWeight=_textFontWeight, fontDecoration=_textFontDecoration)        
  