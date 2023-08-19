# Test file names

# Response format tester

# Playground for testing responses, prompts etc.
import sys
sys.path.append("..")

import re

from agent_zero import AgentZero

response_tester = AgentZero()

def is_valid_filename(filename):
    # Check if the filename has a valid extension
    if not re.match(r'^\w+\.\w+$', filename):
        return False   
    # Check for illegal characters
    illegal_characters = '<>:"/\\|?*'
    if any(char in filename for char in illegal_characters):
        return False
    # Check for reserved words (Windows)
    reserved_words = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"] # Add more as needed
    if filename.split('.')[0].upper() in reserved_words:
        return False
    return True

examples = [
    "def greet(name):\n    print(f'Hello, {name}! Welcome to the party!')",
    "SELECT * FROM products WHERE price < 10;",
    "<h1>This is a sample HTML page</h1>",
    "public class Car {\n    private String brand;\n    public Car(String brand) {\n        this.brand = brand;\n    }\n}",
    "import matplotlib.pyplot as plt\nplt.plot([1, 2, 3], [3, 2, 1])\nplt.show()",
    "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
    "let x = 10;\nlet y = 20;\nconsole.log(x + y);",
    "CREATE TABLE students (id INT, name VARCHAR(50), age INT);",
    "for i in range(5):\n    print(i ** 2)",
    "const add = (a, b) => a + b;\nconsole.log(add(3, 4));",
    "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return(fibonacci(n-1) + fibonacci(n-2))",
    "SELECT COUNT(*) FROM orders WHERE status = 'pending';",
    "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())",
    "class Cat:\n    def meow(self):\n        print('Meow!')",
    "const array = [1, 2, 3, 4, 5];\nconst sum = array.reduce((a, b) => a + b, 0);\nconsole.log(sum);",
    "Once upon a time, there was a brave programmer who wrote elegant code.",
    "INSERT INTO employees (name, position) VALUES ('Alice', 'Engineer');",
    "<svg height=\"100\" width=\"100\">\n  <circle cx=\"50\" cy=\"50\" r=\"40\" stroke=\"black\" stroke-width=\"3\" fill=\"red\" />\n</svg>",
    "using System;\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"C# is cool!\");\n    }\n}",
    "git add .\ngit commit -m 'Added new features'\ngit push origin master"
]

example_cnt = len(examples)
correctly_processed = 0

for index, example in enumerate(examples):
    print(f"Generating filename {index + 1} of {example_cnt}...")
    filename = response_tester.generate_filename(example)
    if  is_valid_filename(filename):
        correctly_processed += 1
        print(f"Filename: {filename}\n")

print(f"Correctly processed {correctly_processed} out of {example_cnt} examples. Success rate: {correctly_processed / example_cnt * 100}%")