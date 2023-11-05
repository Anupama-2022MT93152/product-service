import sys
from flask import Flask

product = Flask(__name__)

@product.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    product.run(host='0.0.0.0', port=5000)

is_64bits = sys.maxsize > 2**32

print(is_64bits)
print(sys.maxsize)