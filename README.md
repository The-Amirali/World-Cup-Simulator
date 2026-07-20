This is a Python project that simulates the FIFA World Cup 2026 tournament. It uses Object-Oriented Programming (OOP) principles and the Poisson distribution to make match results as realistic as possible.

## Features
* **Data Loading & Sorting:** Reads 32 teams from a text/CSV file and automatically sorts them by FIFA rank for a fair seeding.
* **Group Stage:** Creates 8 groups (A to H), runs all 6 matches per group charkhi (round-robin), and ranks teams based on points, goal difference, and goals for.
* **Knockout Stage:** Simulates Round of 16, Quarterfinals, Semifinals, and the Final. If a match ends in a draw, it simulates Extra Time and Penalty Shootouts (with sudden death logic).
* **Mass Simulation:** Can run the entire tournament multiple times (like 1000 times) to calculate each team's percentage chance of winning the trophy.
* **Charts:** Uses Matplotlib to show the final winning probabilities in a simple horizontal bar chart.

## Libraries Used
* **NumPy:** Used for generating random goals based on the Poisson distribution.
* **Matplotlib:** Used to draw the final probability chart.
* **OS & CSV:** For checking file paths and parsing team data.

## Screenshot of project
* **Main manu:**
<img width="732" height="499" alt="mainmenu" src="https://github.com/user-attachments/assets/8f293404-adba-4281-b4e2-5dfbfc3c3d7e" />

* **Multiple simulations:**
<img width="584" height="1143" alt="multiplesimulations" src="https://github.com/user-attachments/assets/56be85ba-ddbd-4ad9-98a0-5d7d96ac2a5c" />

* **Matplotlib output:**
<img width="640" height="480" alt="matplotlibscreenshot" src="https://github.com/user-attachments/assets/469f60f8-d3d5-42e4-9d16-2a712b9faed7" />

## How to Run
1. Make sure you have `numpy` and `matplotlib` installed:
   ```bash
   pip install numpy matplotlib
   
2. Run the main script:
   ```bash
   python worldcup_simulator.py
Choose option 1 to load the data file (worldcup_2026_teams.txt), and then enjoy the simulation!
