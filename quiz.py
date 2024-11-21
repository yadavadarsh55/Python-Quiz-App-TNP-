import json
import os
import random

class QuizApp:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()
        
        self.quizzes = {
            "Python": [
                {"question": "What is the output of print(2 ** 3)?", "options": ["6", "8", "9", "16"], "answer": 1},
                {"question": "Which of the following is immutable?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": 3},
                {"question": "How do you define a function in Python?", "options": ["def", "function", "define", "func"], "answer": 0},
                {"question": "What does the len() function do?", "options": ["Find length of an object", "Find type of an object", "Find maximum value", "Find minimum value"], "answer": 0},
                {"question": "What is the output of bool([])?", "options": ["True", "False", "Error", "None"], "answer": 1}
            ],
            "DSA": [
                {"question": "What is the time complexity of binary search?", "options": ["O(log n)", "O(n)", "O(n^2)", "O(1)"], "answer": 0},
                {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Heap", "Tree"], "answer": 1},
                {"question": "What is the worst-case time complexity of quicksort?", "options": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], "answer": 1},
                {"question": "Which data structure uses FIFO?", "options": ["Queue", "Stack", "Heap", "Graph"], "answer": 0},
                {"question": "What is a full binary tree?", "options": ["Every node has 0 or 2 children", "All leaves are at the same level", "All nodes have 2 children", "All levels are filled"], "answer": 0}
            ],
            "DBMS": [
                {"question": "Which command retrieves data from a database?", "options": ["SELECT", "DELETE", "INSERT", "UPDATE"], "answer": 0},
                {"question": "Which key uniquely identifies a record?", "options": ["Primary Key", "Foreign Key", "Candidate Key", "Super Key"], "answer": 0},
                {"question": "What does ACID stand for?", "options": ["Atomicity, Consistency, Isolation, Durability", "Addition, Consistency, Integrity, Data", "Atomicity, Change, Isolation, Durability", "Atomicity, Consistency, Integrity, Durability"], "answer": 0},
                {"question": "Which normal form removes partial dependency?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": 1},
                {"question": "What is a foreign key?", "options": ["A primary key in another table", "A unique key", "A key in the same table", "A composite key"], "answer": 0}
            ]
        }

    def load_users(self):
        if not os.path.exists(self.users_file):
            return {}
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def register(self):
        print("\n--- REGISTER ---")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        username = input("Username: ")
        password = input("Password: ")

        if username in self.users:
            print("Username already exists!")
            return False

        self.users[username] = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
            "scores": {"Python": 0, "DSA": 0, "DBMS": 0}
        }
        self.save_users()
        print("Registration Successful!")
        return True

    def login(self):
        print("\n--- LOGIN ---")
        username = input("Username: ")
        password = input("Password: ")

        if username in self.users and self.users[username]["password"] == password:
            print("Login Successful!")
            return username
        else:
            print("Invalid Credentials!")
            return None

    def attempt_quiz(self, subject):
        print(f"\n--- {subject} QUIZ ---")
        questions = random.sample(self.quizzes[subject], 5)
        score = 0
        total_questions = len(questions)

        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}: {q['question']}")
            for j, option in enumerate(q['options'], 1):
                print(f"{j}. {option}")
            
            try:
                answer = int(input("Your answer (1-4): ")) - 1
                if 0 <= answer < 4:
                    if answer == q['answer']:
                        print("Correct!")
                        score += 1
                    else:
                        print(f"Wrong! Correct answer was: {q['options'][q['answer']]}")
                else:
                    print("Invalid input!")
            except ValueError:
                print("Invalid input!")

        return score, total_questions

    def show_result(self, username, subject, score, total):
        print("\n--- QUIZ RESULT ---")
        percentage = (score / total) * 100
        print(f"{subject} Quiz Score: {score}/{total}")
        print(f"Percentage: {percentage:.1f}%")

        # Update user's best score
        if username:
            user_data = self.users[username]
            previous_best = user_data["scores"].get(subject, 0)
            user_data["scores"][subject] = max(previous_best, percentage)
            self.save_users()

        if percentage == 100:
            print("Perfect Score! 🏆")
        elif percentage >= 80:
            print("Excellent Performance! 👍")
        elif percentage >= 60:
            print("Good Job! Keep Practicing! 📚")
        else:
            print("Need More Practice! 🔍")

    def run(self):
        current_user = None
        while True:
            print("\n--- QUIZ APPLICATION ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Choose option (1-3): ")

            if choice == '1':
                self.register()
            elif choice == '2':
                current_user = self.login()
                if current_user:
                    while True:
                        print("\nChoose a Subject:")
                        print("1. Python")
                        print("2. DSA")
                        print("3. DBMS")
                        print("4. Logout")

                        subject_choice = input("Choose option (1-4): ")

                        if subject_choice == '1':
                            score, total = self.attempt_quiz("Python")
                            self.show_result(current_user, "Python", score, total)
                        elif subject_choice == '2':
                            score, total = self.attempt_quiz("DSA")
                            self.show_result(current_user, "DSA", score, total)
                        elif subject_choice == '3':
                            score, total = self.attempt_quiz("DBMS")
                            self.show_result(current_user, "DBMS", score, total)
                        elif subject_choice == '4':
                            current_user = None
                            break
                        else:
                            print("Invalid option!")
            elif choice == '3':
                print("Goodbye! 👋")
                break
            else:
                print("Invalid option!")

def main():
    app = QuizApp()
    app.run()

if __name__ == "__main__":
    main()
