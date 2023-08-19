# Response format tester

# Playground for testing responses, prompts etc.
import sys
sys.path.append("..")

from agent_zero import AgentZero

filename_tester = AgentZero()

examples = [
    "SELECT * FROM users WHERE status = 'active;",
    "Code flows like a stream,\\nErrors dance in moonlit dreams,\\nFix and then compile",
    "plot(x, y, main='Scatter Plot'",
    "Water boils at 100°C (212°F at sea level.",
    'public static void main(String[] args { System.out.println("Java in the House!"); }',
    "Give me six hours to chop down a tree and I will spend the first four sharpening the axe. - Abraham Lincoln'",
    'puts "Ruby Rocks!',
    "To code or not to code, that is the question",
    '<book title="Coding for Bros" author="ChatGPT" /',
    "name: ChatGPT\\nversion: 4.0\\nstatus: Awesome'",
    "The mitochondria is the powerhouse of the cell",
    "for i in range(10): print(i",
    "A^2 + B^2 = C^2'",
    "git commit -m 'Fixed the bug",
    "Life is what happens when you're busy making other plans. - John Lennon'",
    "S = \\int_a^b f(x)dx'",
    "print('Swift is Swifty!",
    "The quick brown fox jumps over the lazy dog",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second",
    "INSERT INTO books (title, author VALUES ('The Coder's Guide', 'ChatGPT')",
    "The human body contains about 60% water.",
    "While x < 10:\\n  x += 1\\nprint(x'",
    "y = mx + b'",
    "docker run -p 8080:80 my-image'",
    "Be yourself; everyone else is already taken. - Oscar Wilde'",
    "\\frac{d}{dx} (x^n = nx^{n-1}",
    "console.log('TypeScript Rocks!",
    "Roses are red,\\nViolets are blue,\\nCode is sweet,\\nAnd so are you",
    "E = mc^2'",
    "DELETE FROM orders WHERE status = 'cancelled';'",
    "for i in range(10):\\n    print(f'Item {i+1}')",
    "def factorial(n):\\n    return n * factorial(n-1 if n > 1 else 1",
    "SELECT name, age FROM users WHERE age >= 21;",
    "class MyClass:\\n    def __init__(self, value):\\n        self.value = value\\n    def show_value(self):\\n        print(f'Value: {self.value}",
    "<div class='container'>\\n    <h1>Welcome to the Party!</h1>\\n    <p>Let's dance!</p>\\n</div>",
    "import numpy as np\\narr = np.array([1, 2, 3, 4, 5])\\nprint('Mean:', np.mean(arr)",
    "const express = require('express')\\nconst app = express()\\napp.get('/', (req, res) => res.send('Hello, World!'))\\napp.listen(3000, () => console.log('Server running on port 3000!)",
    "SELECT * FROM products WHERE price < 100 AND category = 'Electronics;",
    "The Earth orbits the Sun at an average distance of about 93 million miles (150 million kilometers).",
    "CREATE TABLE students (\\nid INT PRIMARY KEY,\\nname VARCHAR(50),\\nage INT\\n);",
    "print('Fibonacci sequence:', end=' ')\\nfor i in range(10):\\n    print(fibonacci(i), end=' '",
    "function greet(name) {\\n    console.log(`Hello, ${name}!`);\\n}",
    "Once you eliminate the impossible, whatever remains, no matter how improbable, must be the truth. - Sherlock Holmes'",
    "UPDATE customers SET status = 'active' WHERE last_purchase >= '2021-01-01';",
    "while True:\\n    print('Infinity loop!', end='\\r')",
    "The square root of 2, often known as root 2, is the positive algebraic number that, when multiplied by itself, equals the number 2. It's approximately 1.41421.",
    "React is a JavaScript library for building user interfaces. It's maintained by Facebook and a community of developers.",
    "The sine of an angle in a right triangle is the length of the opposite side divided by the length of the hypotenuse.",
    "The Milky Way is the galaxy that contains our Solar System, with the name describing the galaxy's appearance from Earth: a hazy band of light seen in the night sky.",
    "Don't cry because it's over, smile because it happened. - Dr. Seuss'",
    '{"response": "Embrace the journey, for it is filled with twists and turns!", "response_type": "markdown_text"}',
    '{"response": "def add(x, y): return x + y", "response_type": "python_code"}',
    '{"response": "f(x) = x^2 + 3x + 2", "response_type": "math_function"}',
    '{"response": \'echo "Hello, World!"\', "response_type": "bash_script"}',
    '{"response": \'{"name": "BroBot", "status": "Chillin\'}"\', "response_type": "json_object"}',
    '{"response": "<h1>Welcome to the Party!</h1>", "response_type": "html_code"}',
    '{"response": "In the forest of code, where logic trees grow, a coder wanders, learning as he goes.", "response_type": "poetic_verse"}',
    '{"response": "function greet() { alert(\'Hey Bro!\'); }", "response_type": "javascript_code"}',
    '{"response": "e^{i\\\\pi} + 1 = 0", "response_type": "complex_equation"}',
    '{"response": "Name,Age,Location\\\\nAlice,30,New York\\\\nBob,22,Chicago", "response_type": "table_data_csv"}',
]

example_cnt = len(examples)
correctly_processed = 0
try_again = True
num_of_tries = 5

for index, example in enumerate(examples):
    print(f"Processing example {index + 1} of {example_cnt}...")
    processed_response = filename_tester.process_response(example, try_again, num_of_tries)
    if processed_response['response'] is not None:
        correctly_processed += 1
        print(f"Processed response: {processed_response}\n")
    else:
        print(f"Invalid response: {example}\n")

print(f"Correctly processed {correctly_processed} out of {example_cnt} examples. Success rate: {correctly_processed / example_cnt * 100}%")
