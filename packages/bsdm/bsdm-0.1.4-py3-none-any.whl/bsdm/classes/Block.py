from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.ETName import ETName
from classes.ETAttr import ETAttr


class Block(object): 
        
    def __init__(self, x, y, name):
        
        #self.__width = 500
        #self.__height = 300

        self.__title = None
        self.__attrs = []
        
        self.__group = None
        self.update(x, y, name)
        

        
    def update(self, x=None, y=None, name=None):
        if(x is not None):
            self.__x = x
        if(y is not None):
            self.__y = y
        if(name is not None):
            self.__name = name
        
        self.__group = config.DWG.g(id=self.__name, 
                                    stroke='green',
                                    stroke_width=1*px,
                                    fill='white'       )
        config.DWG.add(self.__group)

        self.__build()
        self.__addAll()
    
        

    
            
    def __build(self):
        _yOffset = 0
        _maxWidth = 0
        self.__height = 20   # 10 px default margin  
        self.__width  = 20 
        
        if(self.__title is not None):
            self.__title.update(self.__x, self.__y + _yOffset)
            _yOffset +=  self.__title.getHeight()
            _maxWidth = max(_maxWidth, self.__title.getWidth())
        
        for attr in self.__attrs:
            attr.update(self.__x, self.__y + _yOffset)
            _yOffset += attr.getHeight()
            _maxWidth = max(_maxWidth, attr.getWidth())
        
        self.__height += _yOffset
        self.__width += _maxWidth   
        
        self.__block = config.DWG.rect( insert=(self.__x * px, self.__y * px), 
                                        size=(self.__width * px, self.__height * px),
                                        rx = 10 * px,
                                        ry = 10 *px                      )
        self.__block['class'] = 'eteven'

    def __addAll(self):

        self.__group.add(self.__block)
        if(self.__title is not None):
            self.__title.addToGroup(self.__group)
        for attr in self.__attrs:
            attr.addToGroup(self.__group)

    
        """
        _yOffset = 0 
        _name = ETName(x, y, 'TITLÉ of thç block')
        
        _yOffset +=  _name.getSize()['height']
        
        _attr1 = ETAttr(x, y + _yOffset, 'Kouroukoukou', id=True, mandatory=False, deprecated=False)
        _attr1.update(text='Kouroukoukou')
        
        _yOffset +=  _attr1.getSize()['height']        
        
        _attr2 = ETAttr(x, y + _yOffset, 'attttribute attrt  attr', id=False, mandatory=True, deprecated=True)  
        
        _name.addToGroup(self.__group)
        _attr1.addToGroup(self.__group)
        _attr2.addToGroup(self.__group)
        """
        
    def setTitle(self, title):
        self.__title = ETName(0, 0, title)
        
    def addAttr(self, attrname, id=True, mandatory=False, deprecated=False):
        self.__attrs.append(ETAttr(0,0, attrname, id, mandatory, deprecated))
