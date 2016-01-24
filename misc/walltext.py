#!/usr/bin/env python3

import subprocess
import os
import time
import random

curr_dir = os.path.dirname(os.path.realpath(__file__))
curr_wall = curr_dir+"/"+"original.jpg"
notes = curr_dir+"/"+"notes.txt"

#--
text_color = "white"   # text color
size = "80"            # text size (real size depends on the scale factor of your wallpaper)
border = 480           # space around your text blocks
columns = 1            # (max) number of columns
n_lines = 3          # (max) number of lines per column
#--

def run_command(cmd):
    subprocess.call(["/bin/bash", "-c", cmd])

def get_value(cmd):
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8").strip()

def read_text(file):
    with open(file) as src:
        return [l.strip() for l in src.readlines()]

def slice_lines(lines, n_lines, columns):
    markers = [i for i in range(len(lines)) if i % n_lines == 0]
    last = len(lines); markers = markers+[last] if markers[-1] != last else markers
    textblocks = [lines[markers[i]:markers[i+1]] for i in range(len(markers)-1)]
    filled_blocks = len(textblocks)
    if filled_blocks < columns:
        for n in range(columns - filled_blocks):
            textblocks.insert(len(textblocks), [])
    for i in range(columns):
        textblocks[i] = ("\n").join(textblocks[i])
    return textblocks[:columns]

def create_section(psize, text, layer):
    run_command("convert -background none -fill "+text_color+" -border "+str(border)+\
                  " -bordercolor none -pointsize "+size+" -size "+psize+\
                  " caption:"+'"'+text+'" '+layer)

def combine_sections(layers):
    run_command("convert "+image_1+" "+image_2+" "+"+append "+span_image)
    pass

def set_overlay(): # Read the file "notes" as specified above, display text in columns
    boxes = slice_lines(read_text(notes), n_lines, columns)
    resolution = get_value('identify -format "%wx%h" '+curr_wall).split("x")
    w = str(int(int(resolution[0])/columns)-2*border)
    h = str(int(resolution[1])-2*border)
    layers = []
    for i in range(len(boxes)):
        layer = curr_dir+"/"+"layer_"+str(i+1)+".png"
        create_section(w+"x"+h, boxes[i], layer)
        layers.append(layer)
    run_command("convert "+(" ").join(layers)+" "+"+append "+curr_dir+"/"+"layer_span.png")
    wall_img = curr_dir+"/"+"walltext.jpg"
    run_command("convert "+curr_wall+" "+curr_dir+"/"+"layer_span.png"+" -background None -layers merge "+wall_img)
    run_command("gsettings set org.gnome.desktop.background picture-uri file:///"+wall_img)
    for img in [img for img in os.listdir(curr_dir) if img.startswith("layer_")]:
        os.remove(curr_dir+"/"+img)

def set_single_overlay(): # DEFAULT, read 1 line from "notes" file as specified above
    resolution = get_value('identify -format "%wx%h" '+curr_wall).split("x")
    w = str(int(int(resolution[0])/columns)-2*border)
    h = str(int(resolution[1])-2*border)
    layers = []

    layer = curr_dir+"/"+"layer_1.png"
    #print(w)
    #print(h)
    create_section(w+"x"+h, text_1, layer)
    layers.append(layer)

    run_command("convert "+(" ").join(layers)+" "+"+append "+curr_dir+"/"+"layer_span.png")
    wall_img = curr_dir+"/"+"walltext.jpg"
    run_command("convert "+curr_wall+" "+curr_dir+"/"+"layer_span.png"+" -background None -layers merge "+wall_img)
    run_command("gsettings set org.gnome.desktop.background picture-uri file:///"+wall_img)
    for img in [img for img in os.listdir(curr_dir) if img.startswith("layer_")]:
        os.remove(curr_dir+"/"+img)

print("Walltext started.")
print (curr_wall)
print (notes)

while True:
    text_1 = random.choice(open(notes).readlines())
    print(text_1)
    set_single_overlay()
    time.sleep(3600)

#    text_2 = read_text(notes)
#    if text_2 != text_1:
#        set_overlay()
