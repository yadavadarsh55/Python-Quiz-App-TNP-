import os
import random

class QuizApp:
    def __init__(self):
        self.users_dir = 'users'
        self.quizzes_dir = 'quizzes'
        
        # Create directories if they don't exist
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.quizzes_dir, exist_ok=True)
        
        # Initialize quiz files if they don't exist
        self.initialize_quiz_files()

    def initialize_quiz_files(self):
        """Create quiz files for each subject if they don't exist."""
        quizzes = {
            "Python": [
                {"question": "What is the output of print(2 ** 3)?", "options": ["6", "8", "9", "16"], "answer": 1},
                {"question": "Which is immutable?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": 3},
                {"question": "How define a function?", "options": ["def", "function", "define", "func"], "answer": 0},
                {"question": "What does len() do?", "options": ["Find length", "Find type", "Find max", "Find min"], "answer": 0},
                {"question": "Output of bool([])?", "options": ["True", "False", "Error", "None"], "answer": 1}
            ],
            "DSA": [
                {"question": "Time complexity of binary search?", "options": ["O(log n)", "O(n)", "O(n^2)", "O(1)"], "answer": 0},
                {"question": "Data structure using LIFO?", "options": ["Queue", "Stack", "Heap", "Tree"], "answer": 1},
                {"question": "Worst-case time complexity of quicksort?", "options": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], "answer": 1},
                {"question": "Data structure using FIFO?", "options": ["Queue", "Stack", "Heap", "Graph"], "answer": 0},
                {"question": "What is a full binary tree?", "options": ["Every node has 0 or 2 children", "All leaves same level", "All nodes have 2 children", "All levels filled"], "answer": 0}
            ],
            "DBMS": [
                {"question": "Command to retrieve data?", "options": ["SELECT", "DELETE", "INSERT", "UPDATE"], "answer": 0},
                {"question": "Key uniquely identifying a record?", "options": ["Primary Key", "Foreign Key", "Candidate Key", "Super Key"], "answer": 0},
                {"question": "ACID stands for?", "options": ["Atomicity, Consistency, Isolation, Durability", "Addition, Consistency, Integrity, Data", "Atomicity, Change, Isolation, Durability", "Atomicity, Consistency, Integrity, Durability"], "answer": 0},
                {"question": "Normal form removing partial dependency?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": 1},
                {"question": "What is a foreign key?", "options": ["Primary key in another table", "Unique key", "Key in same table", "Composite key"], "answer": 0}
            ]
        }
        
        for subject, quiz_data in quizzes.items():
            quiz_file = os.path.join(self.quizzes_dir, f"{subject}_quiz.txt")
            if not os.path.exists(quiz_file):
                with open(quiz_file, 'w') as f:
                    for q in quiz_data:
                        f.write(f"{q['question']}|{','.join(q['options'])}|{q['answer']}\n")

    def register(self):
        """User registration using file-based storage."""
        print("\n--- REGISTER ---")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        username = input("Username: ")
        password = input("Password: ")

        # Check if user already exists
        user_file = os.path.join(self.users_dir, f"{username}.txt")
        if os.path.exists(user_file):
            print("Username already exists!")
            return False

        # Create user file
        with open(user_file, 'w') as f:
            f.write(f"Name:{name}\n")
            f.write(f"Email:{email}\n")
            f.write(f"Phone:{phone}\n")
            f.write(f"Password:{password}\n")
            f.write("Scores:Python:0,DSA:0,DBMS:0")

        print("Registration Successful!")
        return True

    def login(self):
        """User login using file-based storage."""
        print("\n--- LOGIN ---")
        username = input("Username: ")
        password = input("Password: ")

        user_file = os.path.join(self.users_dir, f"{username}.txt")
        
        if not os.path.exists(user_file):
            print("User not found!")
            return None

        # Read user file
        with open(user_file, 'r') as f:
            lines = f.readlines()
            stored_password = lines[3].strip().split(':')[1]
            
            if password == stored_password:
                print("Login Successful!")
                return username
            else:
                print("Invalid Credentials!")
                return None

    def load_quiz(self, subject):
        """Load quiz questions from file."""
        quiz_file = os.path.join(self.quizzes_dir, f"{subject}_quiz.txt")
        questions = []
        
        with open(quiz_file, 'r') as f:
            for line in f:
                question, options, answer = line.strip().split('|')
                questions.append({
                    "question": question,
                    "options": options.split(','),
                    "answer": int(answer)
                })
        
        return random.sample(questions, 5)

    def attempt_quiz(self, subject):
        """Conduct quiz for a subject."""
        print(f"\n--- {subject} QUIZ ---")
        questions = self.load_quiz(subject)
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

    def update_user_score(self, username, subject, percentage):
        """Update user's score in their file."""
        user_file = os.path.join(self.users_dir, f"{username}.txt")
        
        # Read existing user data
        with open(user_file, 'r') as f:
            lines = f.readlines()
        
        # Update scores line
        scores_line = lines[4].strip().split(':')
        scores = dict(zip(scores_line[1::2], map(float, scores_line[2::2])))
        scores[subject] = max(scores.get(subject, 0), percentage)
        
        # Rewrite file with updated scores
        lines[4] = f"Scores:{','.join(f'{k}:{v}' for k, v in scores.items())}\n"
        
        with open(user_file, 'w') as f:
            f.writelines(lines)

    def show_result(self, username, subject, score, total):
        """Display quiz result and update user's score."""
        print("\n--- QUIZ RESULT ---")
        percentage = (score / total) * 100
        print(f"{subject} Quiz Score: {score}/{total}")
        print(f"Percentage: {percentage:.1f}%")

        # Update user's best score
        if username:
            self.update_user_score(username, subject, percentage)

        if percentage == 100:
            print("Perfect Score! 🏆")
        elif percentage >= 80:
            print("Excellent Performance! 👍")
        elif percentage >= 60:
            print("Good Job! Keep Practicing! 📚")
        else:
            print("Need More Practice! 🔍")

    def run(self):
        """Main application loop."""
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
