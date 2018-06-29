class QuestionReader:
    """
    Reads questions from file and stores them
    """
    list_of_questions = []

    def __init__(self):
        self.read_questions()

    def read_questions(self):
        """
        Reads questions from file
        """
        try:
            with open('questions.txt', 'r') as f:
                self.list_of_questions = f.readlines()
        except FileNotFoundError:
            print("File not found. Error in question.py")
            exit()
