# RRT

RRT Project — Robot Path Planning

This project implements the RRT (Rapidly-exploring Random Tree) algorithm for 2D robot path planning using Python, NumPy, and Matplotlib.  
The goal is to compute a path from a start position to a target goal while avoiding obstacles on a grid map.

Setup

1. Create a virtual environment:  
   `python -m venv .venv`
2. Activate the virtual environment:  
   `.venv\Scripts\activate`
3. Install all dependencies from requirements.txt:  
   `pip install -r requirements.txt`

How to Run  

To execute the main script use the following commnand: `python main.py`    

At runtime, you will be prompted to select a grid number (1-11).  
The algorithm will attempt to compute and visualize a path from start to goal in real-time using Matplotlib.

You can create custom environments by drawing your own maps.  
You can use Paint, the program will interpret the black colored blocks as obstacles.  
After you run the `python readImages.py` command, the image will be saved in the `test_images` folder.

Here are some examples of the RRT algorithm finding a path in a custom map:  
![RRT Path Example](result_images/test6_2)
