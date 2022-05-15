# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 15:16:54 2022

@author: James
"""

from PIL import Image
import numpy as np
import pprint
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from tqdm import tqdm

import os

class ImageToLego:
    
    def __init__(self, image_path):
        self.lego_image_size = (144, 144)
        self.image = Image.open(image_path)
        

        self.reference_colors = {
            (204, 170, 70) : "Yellow",
            (136, 156, 145) : "Teal",
            (117, 170, 201) : "Light Blue",
            (20, 38, 62) : "Dark Blue",
            (176, 33, 150) : "Pink",
            (79, 39, 27): "Brown",
            (106, 15, 22) : "Red",
            (255, 255, 255) : "White"
            }
        
        self.pyplot_colors = {
            (204, 170, 70) : "Yellow",
            (136, 156, 145) : "Teal",
            (117, 170, 201) : "Light Blue",
            (20, 38, 62) : "Dark Blue",
            (176, 33, 150) : "Pink",
            (79, 39, 27): "Brown",
            (106, 15, 22) : "Red",
            (255, 255, 255) : "White"
            }


    @property
    def image(self, image):
        self._image = image
        
    @image.setter
    def image(self, image):
        self._image = image
        self.i_width = self._image.size[0]
        self.i_height = self._image.size[1]

        if self.i_width < self.i_height:
            self.i_height_start = (self.i_height - self.i_width) / 2
            self.i_height_end = self.i_height - self.i_height_start
            self.i_width_start = 0
            self.i_width_end = self.i_width
        elif self.i_width > self.i_height:
            self.i_width_start = (self.i_width - self.i_height) / 2
            self.i_width_end = self.i_width - self.i_width_start
            self.i_height_start = 0
            self.i_height_end = self.i_height    
        else:
            self.i_width_start = 0
            self.i_width_end = self.i_width            
            self.i_height_start = 0
            self.i_height_end = self.i_height  
            
            
        self.step_size = (self.i_width_end -  self.i_width_start) / self.lego_image_size[0]

    def nearest_color(self, color):
        min_distance = 10000000.0
        min_color = None
        for ref_col in self.reference_colors:
            red_dist = (color[0] - ref_col[0]) ** 2
            green_dist = (color[1] - ref_col[1]) ** 2
            blue_dist = (color[2] - ref_col[2]) ** 2
            
            main_dist = np.sqrt(sum([red_dist + green_dist + blue_dist]))
            
            if main_dist < min_distance:
                min_distance = main_dist
                min_color = ref_col
                
        return min_color

    def get_instructions(self):
        if not hasattr(self, "instructions"):
            self.build_instructions(build_image = False)
        return self.instructions

    def build_instructions(self, build_image = True):
        



        self.instructions = []
        self.instruction_colors = {}
        
        if build_image:
            self.im = Image.new(mode="RGB", size=(144, 144))
        
        for idx_x, x in enumerate(np.arange(self.i_width_start+self.step_size, self.i_width_end + self.step_size, self.step_size)):
            for idx_y, y in enumerate(np.arange(self.i_height_start+self.step_size, self.i_height_end + self.step_size, self.step_size)):
                colors = [self._image.getpixel((int(x2),int(y2))) for x2 in range(int(x-self.step_size), int(x)) for y2 in range(int(y-self.step_size), int(y))]
                red = np.mean([color[0] for color in colors])
                green = np.mean([color[1] for color in colors])
                blue = np.mean([color[2] for color in colors])
                self.instruction_colors[(idx_x, idx_y)] = (red, green, blue)
                
                lego_color = self.nearest_color(
                    (int(red), int(green), int(blue))
                )
                
                self.instructions.append(self.reference_colors[lego_color])
                if build_image:
                    self.im.putpixel((idx_x, idx_y), lego_color)
                
        
        
    def build_plot(self, output_file = "LegoImage.png"):


        fig,ax = plt.subplots(1)
        plt.axis('off')
        ax.set_aspect('equal')
        
        if not hasattr(self, "im"):
            self.build_instructions(build_image = True)
        
        for xx in tqdm(range(self.lego_image_size[0])):
            for yy in range(self.lego_image_size[1]):
            
                color = list(self.im.getpixel((xx,yy)))
                
                color[0] = color[0] / 255.0
                color[1] = color[1] / 255.0
                color[2] = color[2] / 255.0
                
                circ = Circle((xx,self.lego_image_size[1] - yy),radius=0.25, color = tuple(color))
                ax.add_patch(circ)
                
        ax.set_xlim(0,144)
        ax.set_ylim(0,144)
        plt.savefig(output_file, bbox_inches='tight')
