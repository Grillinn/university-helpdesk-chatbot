# scripts/generate_students.py
import pandas as pd
import numpy as np

def generate_student_data(num_students=80):
    """Generates sample student data for testing."""

    branches = ['CSE', 'ECE', 'IT']
    data = []

    for i in range(num_students):
        branch = np.random.choice(branches)
        physics = np.random.randint(50, 100)
        chemistry = np.random.randint(50, 100)
        math = np.random.randint(50, 100)
        total_percentage = (physics + chemistry + math) / 3
        loan_applied = np.random.choice(['Yes', 'No'], p=[0.625, 0.375])  # 50 out of 80 is 62.5%

        data.append({
            'Application ID': f'APP{1000 + i}',
            'Full Name': f'Student {i+1}',
            'Email': f'student{i+1}@example.com',
            'Phone': f'123-456-{7000 + i}',
            'Branch': branch,
            'Physics': physics,
            'Chemistry': chemistry,
            'Math': math,
            'Total %': total_percentage,
            'Document Submission Status': 'Pending',
            'Loan Applied': loan_applied,
            'Loan Eligibility Score': 0,
            'Final Admission Status': 'Pending',
            'Email Sent': 'No'
        })

    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    student_data = generate_student_data()
    student_data.to_excel('../data/students_data.xlsx', index=False)
    print("Student data generated and saved to data/students_data.xlsx")