import os
import time
import random
import datetime
import openai
import qrcode

class Number:
    def __init__(self, number):
        "Class for a number"
        self.number = number
        self.pynumber = number + 1
        self.traits = {}

    def numtype(self):
        "Returns the type of the number"
        if isinstance(self.number, int):
            self.traits["Type"] = "Integer"
            return "Integer"
        elif isinstance(self.number, float):
            self.traits["Type"] = "Float"
            return "Float"

    def prime(self):
        "Returns whether the number is prime"
        if self.traits["Type"] == "Float":
            return "Is a float"

        if self.number < 2:
            self.traits["Prime"] = False
            return False

        for i in range(2, self.number):
            if self.number % i == 0:
                self.traits["Prime"] = False
                return False

        self.traits["Prime"] = True
        return True

    def evenodd(self):
        "Returns whether the number is even or odd"
        if self.number % 2 == 0:
            self.traits["Even or Odd"] = "Even"
            return "Even" 
        elif isinstance(self.number, float):
            self.traits["Even or Odd"] = False
        else:
            self.traits["Even or Odd"] = "Odd"
            return "Odd"

    def palindrome(self):
        "Returns whether the number is a palindrome"
        number_str = str(self.number)
        reversed_str = number_str[::-1]
        self.traits["Palindrome"] = number_str == reversed_str
        return number_str == reversed_str

    def strobogrammatic(self):
        "Returns whether the number is strobogrammatic"
        strobogrammatic_digits = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}
        num_str = str(self.number)
        left = 0
        right = len(num_str) - 1

        while left <= right:
            if num_str[left] not in strobogrammatic_digits or num_str[right] not in strobogrammatic_digits:
                self.traits["Strobogrammatic"] = False
                return False
            if num_str[left] != strobogrammatic_digits[num_str[right]]:
                self.traits["Strobogrammatic"] = False
                return False

            left += 1
            right -= 1
        self.traits["Strobogrammatic"] = True
        return True

    def strobogrammaticdifferent(self):
        "Returns whether the number is a strobogrammatic different"
        digits = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}
        num_str = str(self.number)
        upsidedownstr = ""
        for char in num_str[::-1]:
            if char in digits.keys():
                upsidedownstr += digits[char]
            else:
                self.traits["Strobogrammatic Different"] = False
                return False
        self.traits["Strobogrammatic Different"] = num_str != upsidedownstr
        return num_str != upsidedownstr

    def square(self):
        "Returns whether the number is a square"
        if self.traits["Type"] == "Float":
            return "Is a float"
        if self.number < 0:
            self.traits["Square"] = False
            return False
        for i in range(self.number):
            if i * i == self.number:
                self.traits["Square"] = True
                return True
        self.traits["Square"] = False
        return False

    def cube(self):
        "Returns whether the number is a cube"
        if self.traits["Type"] == "Float":
            return "Is a float"
        if self.number < 0:
            self.traits["Cube"] = False
            return False
        for i in range(self.number):
            if i * i * i == self.number:
                self.traits["Cube"] = True
                return True
        self.traits["Cube"] = False
        return False

    def __str__(self):
        "Returns a string representation of the number"
        funcs = [self.numtype, self.evenodd, self.prime, self.palindrome, self.strobogrammatic, self.strobogrammaticdifferent, self.square, self.cube]
        for func in funcs:
            func()
        traits_str = "\n".join([f"{k}: {v}" for k, v in self.traits.items()])
        return f"""NUMBER ({self.number})

TRAITS
{traits_str}"""

class Chatbot:
    def ___init__(self, name, description, key):
        "Class for a chatbot. Uses openai's API, so it needs a key. Description is the chatbot's description, do not include the chatbot's name."
        self.name = name
        self.description = description
        openai.api_key = key
        self.messages = []
        self.messages.append({"role":"system","content": f"You are {name}. {description}"})

    def chat(self, message):
        "Chat with the chatbot"
        self.messages.append({"role":"user","content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # other models include gpt-4 or gpt-3.5-turbo
            messages=self.messages
        )
        reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role":"system","content": reply})
        return reply
    
    def clear(self):
        "Clears the chat"
        self.messages = []
        self.messages.append({"role":"system","content": self.description})

class Imagebot:
    def __init__(self, key):
        "Class for an imagebot. Uses openai's API, so it needs a key."
        openai.api_key = key

    def generate(self, prompt, width, height):
        """Generates an image from a prompt
        The width of the image. Must be 256, 512, or 1024.
        The height of the image. Must be 256, 512, or 1024."""
        if width not in [256, 512, 1024] or height not in [256, 512, 1024]:
            return "Invalid width or height. Width and height must be 256, 512, or 1024."
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size = f"{width}x{height}"
        )
        return f"""View at:
{response["url"]}"""

class Random:
    def __init__(self):
        pass
    
    def integer(self, min, max):
        "Returns a random integer between min and max"
        return random.randint(min, max)
    
    def float(self, min, max):
        "Returns a random float between min and max"
        return random.uniform(min, max)
    
    def choice(self, list):
        "Returns a random choice from a list"
        return random.choice(list)
    
def clear():
    "Clears console"
    os.system("cls")

def wait(secs):
    "Waits for a number of seconds"
    time.sleep(secs)
    
def getdate():
    "Returns the date"
    return datetime.datetime.now().strftime("%d/%m/%Y")

def gettime():
    "Returns the time"
    return datetime.datetime.now().strftime("%H:%M")

def qrcode(text, filename):
    """Generates a QR Code for the specified text to a certain file
    Filename must be a .png file, include .png in the filename"""
    img = qrcode.make(text)
    img.save(filename)