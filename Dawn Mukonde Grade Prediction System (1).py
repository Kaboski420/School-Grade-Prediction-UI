#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from sklearn.linear_model import LinearRegression

# Define the correct admin password
admin_password = "0000"

# Define the model and column names as global variables
model = None
model_columns = None

def predict_grades_single(features):
    global model, model_columns  # Access the global model and column names

    # Load the dataset into a Pandas DataFrame
    data = pd.read_csv('StudentsPerformance (1).csv')  # Replace 'your_dataset.csv' with the actual filename/path

    # Remove trailing whitespaces from column names
    data.columns = data.columns.str.strip()

    # Select the relevant columns for training and prediction
    selected_features = ['Student Number', 'Attendance (%)', 'Gender', 'Race/Ethnicity', 'Parental level of education', 'Lunch Type', 'Test Preparation Course']
    target_variables = ['Mathematics', 'English', 'Biology', 'Physics', 'Chemistry', 'ICT']

    # Convert categorical variables into numerical representations (one-hot encoding)
    data_encoded = pd.get_dummies(data[selected_features])

    # Create a linear regression model and fit it to the entire dataset
    model = LinearRegression()
    model.fit(data_encoded, data[target_variables])

    # Store the column names
    model_columns = data_encoded.columns

    # Prepare input data for prediction
    input_data = pd.DataFrame([features], columns=selected_features)
    input_data_encoded = pd.get_dummies(input_data)

    # Check for missing columns in input_data_encoded
    missing_cols = set(model_columns) - set(input_data_encoded.columns)
    for col in missing_cols:
        input_data_encoded[col] = 0

    # Reorder columns to match the order in the trained model
    input_data_encoded = input_data_encoded[model_columns]

    # Make predictions
    predictions = model.predict(input_data_encoded)

    return dict(zip(target_variables, predictions[0]))

def predict_grades_bulk(file_path):
    global model  # Access the global model

    if model is None:
        messagebox.showerror("Error", "Model not initialized. Perform single prediction first.")
        return

    # Load the dataset into a Pandas DataFrame
    data = pd.read_csv(file_path)

    # Remove trailing whitespaces from column names
    data.columns = data.columns.str.strip()

    # Select the relevant columns for prediction
    selected_features = ['Student Number', 'Attendance (%)', 'Gender', 'Race/Ethnicity', 'Parental level of education', 'Lunch Type', 'Test Preparation Course']
    target_variables = ['Mathematics', 'English', 'Biology', 'Physics', 'Chemistry', 'ICT']

    # Convert categorical variables into numerical representations (one-hot encoding)
    data_encoded = pd.get_dummies(data[selected_features])

    # Check for missing columns in data_encoded
    missing_cols = set(model_columns) - set(data_encoded.columns)
    for col in missing_cols:
        data_encoded[col] = 0

    # Reorder columns to match the order in the trained model
    data_encoded = data_encoded[model_columns]

    # Make predictions
    predictions = model.predict(data_encoded)

    # Create a new DataFrame with predicted grades and student numbers
    #output_data = pd.DataFrame(predictions, columns=model_columns[1:])
    output_data = pd.DataFrame(predictions, columns=target_variables)
    output_data['Student Number'] = data_encoded['Student Number']

    return output_data

def login_button_click():
    entered_username = entry_username.get()
    entered_password = entry_password.get()

    if entered_password == admin_password:
        # Clear the password entry field
        entry_password.delete(0, tk.END)

        # Hide the login page
        frame_login.pack_forget()

        # Show the prediction page
        frame_prediction.pack()
    else:
        messagebox.showerror("Error", "Incorrect password. Access denied.")

def predict_button_click():
    features = {
        'Student Number': int(entry_student_number.get()),
        'Attendance (%)': float(entry_attendance.get()),
        'Gender': entry_gender.get(),
        'Race/Ethnicity': entry_race.get(),
        'Parental level of education': entry_education.get(),
        'Lunch Type': entry_lunch.get(),
        'Test Preparation Course': entry_prep.get()
    }

    try:
        predicted_grades = predict_grades_single(features)
        formatted_grades = "\n".join([f"{subject}: {int(round(grade))}" for subject, grade in predicted_grades.items()])
        result_text.set("Predicted Grades:\n" + formatted_grades)
    except Exception as e:
        result_text.set("Error: " + str(e))

def bulk_predict_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            output_data = predict_grades_bulk(file_path)
            output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if output_file_path:
                output_data.to_csv(output_file_path, index=False)
                messagebox.showinfo("Bulk Prediction", "Prediction completed. Output CSV file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Bulk Prediction", "No file selected.")

# Create the UI window
window = tk.Tk()
window.title("Grade Prediction")
window.geometry("600x600")

# Create the login page
frame_login = tk.Frame(window, bg="#506180")

label_username = tk.Label(frame_login, text="Enter Username:", font=("Arial", 14), bg="#506180")
label_username.pack()
entry_username = tk.Entry(frame_login, font=("Arial", 14))
entry_username.pack()

label_password = tk.Label(frame_login, text="Enter Password:", font=("Arial", 14), bg="#506180")
label_password.pack()
entry_password = tk.Entry(frame_login, show="*", font=("Arial", 14))
entry_password.pack()

button_login = tk.Button(frame_login, text="Login", command=login_button_click, font=("Arial", 14))
button_login.pack()

# Create the prediction page (initially hidden)
frame_prediction = tk.Frame(window, bg="#506180")

label_attendance = tk.Label(frame_prediction, text="Attendance (%)", font=("Arial", 14), bg="#506180")
label_attendance.pack()
entry_attendance = tk.Entry(frame_prediction, font=("Arial", 14))
entry_attendance.pack(pady=10)

label_student_number = tk.Label(frame_prediction, text="Student Number", font=("Arial", 14), bg="#506180")
label_student_number.pack()
entry_student_number = tk.Entry(frame_prediction, font=("Arial", 14))
entry_student_number.pack(pady=10)

label_gender = tk.Label(frame_prediction, text="Gender", font=("Arial", 14), bg="#506180")
label_gender.pack()
entry_gender = tk.Entry(frame_prediction, font=("Arial", 14))
entry_gender.pack(pady=10)

label_race = tk.Label(frame_prediction, text="Race/Ethnicity", font=("Arial", 14), bg="#506180")
label_race.pack()
entry_race = tk.Entry(frame_prediction, font=("Arial", 14))
entry_race.pack(pady=10)

label_education = tk.Label(frame_prediction, text="Parental Level of Education", font=("Arial", 14), bg="#506180")
label_education.pack()
entry_education = tk.Entry(frame_prediction, font=("Arial", 14))
entry_education.pack(pady=10)

label_lunch = tk.Label(frame_prediction, text="Lunch Type", font=("Arial", 14), bg="#506180")
label_lunch.pack()
entry_lunch = tk.Entry(frame_prediction, font=("Arial", 14))
entry_lunch.pack(pady=10)

label_prep = tk.Label(frame_prediction, text="Test Preparation Course", font=("Arial", 14), bg="#506180")
label_prep.pack()
entry_prep = tk.Entry(frame_prediction, font=("Arial", 14))
entry_prep.pack(pady=10)

button_predict = tk.Button(frame_prediction, text="Single Prediction", command=predict_button_click, font=("Calibri", 14))
button_predict.pack()

button_bulk_predict = tk.Button(frame_prediction, text="Bulk Prediction", command=bulk_predict_button_click, font=("Calibri", 14))
button_bulk_predict.pack()

result_text = tk.StringVar()
result_label = tk.Label(frame_prediction, textvariable=result_text, font=("Arial", 14), justify='left', bg="#506180")
result_label.pack(pady=10)

# Run the UI
frame_login.pack(fill="both", expand=True)
window.mainloop()


# In[ ]:




