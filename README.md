# RRT
## RRT Project — Robot Path Planning

- This project implements the **RRT (Rapidly-exploring Random Tree)** algorithm for 2D robot path planning using **Python**, **NumPy**, and **Matplotlib**.
- The goal is to compute an efficient path from a **start position** to a **target goal**, while **avoiding obstacles** on a grid-based map.

## Setup

1. Create a virtual environment:  
   `python -m venv .venv`
2. Activate the virtual environment:  
   `.venv\Scripts\activate`
3. Install all dependencies from requirements.txt:  
   `pip install -r requirements.txt`

## How to Run
 
- To execute the main script, use the following command: `python main.py`
- At runtime, you will be prompted to select a grid number (1-11).
- Then, the algorithm will attempt to compute and visualize a path from start to goal in real-time using Matplotlib.

## Create Your Own Map

- You can create **custom environments** by drawing your own maps! Use **Paint** (or any image editor) to design your environment. The program will interpret the **black colored shapes as obstacles**, and the white area as free space.
- Once your map is saved, it will be processed and added to the `test_images` folder.
- For more help with creating and using custom maps, check:  **`readImages.py`** and **`plotting.py`**

Here are some examples of the RRT algorithm finding a path in a custom map:  
![RRT Path Example](result_images/test6_2.png)

This test was done with the classic RRT algorithm  
![RRT Path Example](result_images/testChaos.png)

This test was done with the RRT algorithm after some improvements were added
![RRT Path Example](result_images/chaosMode.png)
