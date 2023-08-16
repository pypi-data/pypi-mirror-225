from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER


class ETAttrMarker(object):
    
    def __init__(self, x=0, y=0, size=None, markerType=None):
        
        self.__x = x + config.MARGIN
        self.__y = y + config.MARGIN
        self.__markerType = markerType
        self.__size = size 
        
        self._styleClass = "defaultattrmarker attrmarker"   

        self._build()    
        
    def _build(self):
        
        if(self.__markerType=='optional'):
            self._attrMarker = config.DWG.polyline(points= [ 
                                                            (self.__x                 , self.__y+(self.__size/2) ), 
                                                            (self.__x+self.__size     , self.__y+(self.__size/2) ),

                                                            (self.__x+(self.__size/2) , self.__y+(self.__size/2) ),
                                                            
                                                            (self.__x+(self.__size/2) , self.__y                 ),
                                                            (self.__x+(self.__size/2) , self.__y+self.__size     ), 
                                                            
                                                            (self.__x+(self.__size/2) , self.__y+(self.__size/2) ),
                                                            
                                                            (self.__x+(self.__size * 0.15) , self.__y+(self.__size * 0.15)),
                                                            (self.__x+(self.__size * 0.85) , self.__y+(self.__size * 0.85)), 
                                                            
                                                            (self.__x+(self.__size/2) , self.__y+(self.__size/2) ),
                                                            
                                                            (self.__x+(self.__size * 0.15) , self.__y+(self.__size * 0.85)),
                                                            (self.__x+(self.__size * 0.85) , self.__y+(self.__size * 0.15))
                                                            
                                                            ]) 
        elif(self.__markerType=='id'):
            self._attrMarker = config.DWG.polyline(points= [ 
                                                            (self.__x+self.__size * 0.375   , self.__y), 
                                                            (self.__x+self.__size * 0.25    , self.__y + self.__size ),

                                                            (self.__x+self.__size * (0.25 + 0.25/3) , self.__y+(self.__size * (1/3)) ),

                                                            (self.__x+(self.__size * 0.10) , self.__y+(self.__size * (1/3))),
                                                            (self.__x+(self.__size * 0.90) , self.__y+(self.__size * (1/3))), 

                                                            (self.__x+self.__size * (0.625 + 0.25/3) , self.__y+(self.__size * (1/3)) ),
                                                            
                                                            (self.__x+self.__size * 0.75   , self.__y), 
                                                            (self.__x+self.__size * 0.625   , self.__y + self.__size ),
                                                            
                                                            (self.__x+ self.__size * (0.625 + 0.125/3) , self.__y+(self.__size * (2/3)) ),
                                                            
                                                            (self.__x+(self.__size * 0.10) , self.__y+(self.__size * (2/3))),
                                                            (self.__x+(self.__size * 0.90) , self.__y+(self.__size * (2/3)))
                                                            
                                                            ]) 
        else:
            self._attrMarker = config.DWG.circle(center=(self.__x+(self.__size/2) , self.__y+(self.__size/2)), r=self.__size*0.4)             
            
        self._attrMarker['class'] = self._styleClass 
        
        
    def addToGroup(self, group):
        group.add(self._attrMarker)