import psycopg2
from nltk.tokenize import sent_tokenize
from transformers import BertTokenizer
from InstructorEmbedding import INSTRUCTOR
import logging
from termcolor import colored
import os
import getpass

class ColoredConsoleHandler(logging.StreamHandler):
    COLORS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta',
    }

    def emit(self, record):
        log_message = self.format(record)
        color = self.COLORS.get(record.levelname, 'white')
        print(colored(log_message, color))

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Create the colored console handler
console_handler = ColoredConsoleHandler()
console_handler.setLevel(logging.INFO)  # Set level for the console handler

formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)

# Model and Tokenizer
model = INSTRUCTOR('hkunlp/instructor-xl')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Connection parameters
db_params = {
    'dbname': 'docvectors',
    'user': 'stinkbait',
    'password': os.getenv('DB_PASSWORD') or getpass.getpass('Enter your database password: '),
    'host': 'stinkbaitdev-rdsinstance-5uba4woife74.cipydolsrn7q.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

# Create a connection and cursor
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

def close_connection():
    cursor.close()
    connection.close()