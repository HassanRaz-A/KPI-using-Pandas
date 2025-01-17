🚀 How to Run Your Python Dash App
Step 1: Install Required Libraries 📦
Before running the script, make sure you have the necessary Python libraries installed. Open your terminal (or command prompt) and run the following commands:

bash
Copy code
pip install pandas plotly dash
This will install Pandas, Plotly, and Dash, which are essential for data analysis, visualization, and creating web applications.

Step 2: Prepare Your CSV Files 📄
Make sure your CSV files are ready and placed in a specific folder on your computer. Your script will read these files to analyze and visualize data.

Step 3: Set the Style Sheet 🎨
Ensure you have a CSS file named style.css located in the same directory as your script. This will allow you to apply custom styles to your Dash app.

Step 4: Update the Script 📝
Copy the entire script into a new Python file (e.g., my_dash_app.py). Update the external_stylesheets path in the script with the correct path to your CSS file:

python
Copy code
app = Dash(__name__, external_stylesheets=[r"path/to/your/style.css"])
Step 5: Run the Script ▶️
Navigate to the directory where your script is saved using the terminal. Then, run the following command to start your Dash app:

bash
Copy code
python my_dash_app.py
Step 6: Open Your Browser 🌐
Once the script is running, you'll see an output like this in the terminal:

csharp
Copy code
Dash is running on http://127.0.0.1:8050/
Open your web browser and go to the provided URL (usually http://127.0.0.1:8050/). You'll see your Dash app interface!

Step 7: Interact with the App 🎛️
Enter the Folder Path: Type the path of the folder containing your CSV files in the input box.

Select a CSV File: Choose a CSV file from the dropdown menu to load its data.

Choose Plot Type: Pick a plot type (Scatter, Line, or Bar) to visualize your data.

Select Axes: Choose which data to plot on the X and Y axes.

Set Filters: Adjust the RSRP and CINR thresholds to filter the data as needed.

Select Cell ID: Optionally, choose a specific Cell ID to analyze.

View Graphs: Explore the interactive graphs generated by your selections.

Step 8: Analyze the Results 📊
Use the visualizations to gain insights into RSRP and CINR trends, analyze network performance, and make data-driven decisions.

Troubleshooting 🛠️
Error Messages: If you encounter errors while loading files, check the console for details. Ensure your CSV files are formatted correctly.

CSS Issues: Verify that the CSS path is correct if the app's appearance isn't as expected.

Library Import Errors: Make sure all necessary libraries are installed.
