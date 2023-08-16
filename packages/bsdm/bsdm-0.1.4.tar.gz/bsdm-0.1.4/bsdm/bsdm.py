# bsdm.py

import argparse

import svgwrite
from svgwrite import cm, mm, px  

from pathlib import Path

import utils.config as config

from utils.logger import LOGGER
from utils.StyleSheet import StyleSheet

from classes.Block import Block


def checkArgs():
    """
Checks and saves arguments passed when calling the program.

Returns the list of arguments if successful.
Otherwise, terminates the program.

Arguments: none
    """    
    
    parser = argparse.ArgumentParser(
        prog='BSDM',
        description='Beautiful SVG Data Model',
        epilog='Generate SVG beautiful diagram with CSS from Oracle Data Modeler.')

    parser.add_argument('-c','--css_file', required=False, help='css filename')
    parser.add_argument('data_model', help='Oracle Data Model directory')
    parser.add_argument('-o', '--output_svg_file', help='SVG output filename') 

    args = parser.parse_args()
    
    return args
    
    
def setOutputSVGPath(output_svg_file_arg):
    """
Builds, if necessary, the path for the program's output SVG file.

Returns a clean path corresponding to the one passed as argument.

Arguments:
output_svg_file_arg: a string designating the output SVG file.    
    """
    
    if(output_svg_file_arg):
        _svg_file_path = output_svg_file_arg
    else :
        _svg_file_path = "./data_model.svg"
    _svg_file_path = Path(_svg_file_path).resolve()
    _svg_file_path.parent.mkdir(parents=True, exist_ok=True)

    return _svg_file_path


def getInputCSS(input_css_file):
    """
Builds, if necessary, the path for the SVG CSS style file.

Returns a string containing the CSS style ot None if no CSS file passed in argument

Arguments:
input_css_file: a string designating the input CSS file.    
    """
    
    if(input_css_file):
        _css_file_path = input_css_file
    else :
        return None
    
    _css_file_path = Path(_css_file_path).resolve()

    if(_css_file_path.exists() and _css_file_path.is_file()):
        with open(str(_css_file_path), "r") as _css_file :
            return _css_file.read() 

    LOGGER.warning('Problem with CSS file. Skipping it')

    return None


def bsdm():

    args = checkArgs()
    
    LOGGER.info('BSDM is not what you think!')
    LOGGER.info(args.css_file + ", " +  args.output_svg_file + ", " +  args.data_model)    

    output_svg_path = setOutputSVGPath(args.output_svg_file)
    cssStyleSheet = getInputCSS(args.css_file)  
    
    createDrawing(output_svg_path, cssStyleSheet)

    
    _block = Block(50, 50, 'first_block')
    _block.setTitle('TLÉç')
    _block.addAttr('Kouroukoukou', id=True, mandatory=False, deprecated=False)
    _block.addAttr('attttribute attrt  attr', id=False, mandatory=True, deprecated=True)
    _block.update()
        
    
#    createDrawing(output_svg_path, cssStyleSheet)
#    _block.update(x=200, y=200)
    
    saveDrawing()


def createDrawing(output_svg_path, cssStyleSheet):
    config.DWG = svgwrite.Drawing(str(output_svg_path), debug=True)
    if(cssStyleSheet is not None) :
        config.DWG.embed_stylesheet(cssStyleSheet)
        StyleSheet.loadFromCSSStyleSheet(cssStyleSheet)        


def saveDrawing():
    config.DWG.save()

def main():
    bsdm()

if __name__ == "__main__":
    main()
    
    