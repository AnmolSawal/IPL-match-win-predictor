import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle

# Load the model
pipe = pickle.load(open('model.pkl', 'rb'))

# Teams and cities
teams = sorted(['Sunrisers Hyderabad',
                'Mumbai Indians',
                'Royal Challengers Bengaluru',
                'Kolkata Knight Riders',
                'Punjab Kings',
                'Chennai Super Kings',
                'Rajasthan Royals',
                'Delhi Capitals'])

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai',  'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Rajkot',
       'Kanpur', 'Bengaluru', 'Indore', 'Sharjah', 'Dubai', 'Navi Mumbai',
       'Lucknow', 'Guwahati', 'Mohali']

# Function to predict probability
def predict_probability():
        batting_team = batting_team_var.get()
        bowling_team = bowling_team_var.get()
        selected_city = city_var.get()
        target = int(target_var.get())
        score = int(score_var.get())
        wickets = int(wickets_var.get())
        overs = float(overs_var.get())

        run_left = target - score
        ball_left = 120 - int(overs * 6)
        wickets_left= 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (run_left * 6 / ball_left) if ball_left > 0 else 0

        df = pd.DataFrame({'batting_team': [batting_team],
                           'bowling_team': [bowling_team],
                           'city': [selected_city],
                           'run_left': [run_left],
                           'ball_left': [ball_left],
                           'wickets_Left': [wickets_left],
                           'target_runs': [target],
                           'crr': [crr],
                           'rrr': [rrr]})

        result = pipe.predict_proba(df)
        r_1 = round(result[0][0] * 100)
        r_2 = round(result[0][1] * 100)

        messagebox.showinfo("Prediction Result",
                            f"{batting_team}: {r_2}%\n{bowling_team}: {r_1}%")
   

# Create the main window
root = tk.Tk()
root.title("IPL Win Predictor(While chasing)")

# Batting team
tk.Label(root, text="Select the batting team:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
batting_team_var = tk.StringVar()
batting_team_dropdown = ttk.Combobox(root, textvariable=batting_team_var, values=teams, state="readonly")
batting_team_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Bowling team
tk.Label(root, text="Select the bowling team:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
bowling_team_var = tk.StringVar()
bowling_team_dropdown = ttk.Combobox(root, textvariable=bowling_team_var, values=teams, state="readonly")
bowling_team_dropdown.grid(row=1, column=1, padx=10, pady=5)

# City
tk.Label(root, text="Select the city:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
city_var = tk.StringVar()
city_dropdown = ttk.Combobox(root, textvariable=city_var, values=sorted(cities), state="readonly")
city_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Target
tk.Label(root, text="Target:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
target_var = tk.StringVar()
target_entry = tk.Entry(root, textvariable=target_var)
target_entry.grid(row=3, column=1, padx=10, pady=5)

# Score
tk.Label(root, text="Current Score:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
score_var = tk.StringVar()
score_entry = tk.Entry(root, textvariable=score_var)
score_entry.grid(row=4, column=1, padx=10, pady=5)

# Wickets
tk.Label(root, text="Wickets Down:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
wickets_var = tk.StringVar()
wickets_entry = tk.Entry(root, textvariable=wickets_var)
wickets_entry.grid(row=5, column=1, padx=10, pady=5)

# Overs
tk.Label(root, text="Overs completed:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
overs_var = tk.StringVar()
overs_entry = tk.Entry(root, textvariable=overs_var)
overs_entry.grid(row=6, column=1, padx=10, pady=5)

# Predict button
predict_button = tk.Button(root, text="Predict Probability", command=predict_probability)
predict_button.grid(row=7, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
