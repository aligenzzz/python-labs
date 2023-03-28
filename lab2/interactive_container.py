from json import load, dump
from re import match, compile

class InteractiveContainer:
    def __init__(self, username):
        self.username = username
        self.data = {}

    def add(self, *args):
        if self.username not in self.data:
            self.load()
            self.data[self.username] = args
        else:
            for element in args:
                if element not in self.data[self.username]:
                    self.data[self.username].append(element)

    def remove(self, element):
        if self.username not in self.data:
            print("The container is empty! Load data or add new elements!")
        elif element not in self.data[self.username]:
            print("There is no such element in the container :(")
        else:
            self.data[self.username].remove(element)

    def find(self, *args):
        if self.username not in self.data:
            print("The container is empty! Load data or add new elements!")
            return
        found_elements = [element for element in args if element in self.data[self.username]]
        if len(found_elements) == 0:
            print("No such elements :(")
        else:
            print("The found elements:", *found_elements)

    def list(self):
        if self.username not in self.data:
            print("The container is empty! Load data or add new elements!")
        else:
            print(self.data[self.username])

    def grep(self, regex):
        if self.username not in self.data:
            print("The container is empty! Load data or add new elements!")
            return
        matched_elements = [element for element in self.data[self.username] if match(compile(regex), element)]
        if len(matched_elements) == 0:
            print("No such elements :(")
        else:
            print("The matched elements:", *matched_elements)

    def save(self):
        if self.username not in self.data:
            self.data[self.username] = []#$
        with open('text_files/data.json', 'w') as file:
            dump(self.data, file)

    def load(self):
        with open('text_files/data.json', 'r') as file:
            self.data = load(file)

    def switch(self, username):
        self.username = username
        self.data = {}

    def load_username(self):
        with open('text_files/data.json', 'r') as file:
            self.data = load(file)
        if self.username in self.data:
            self.data[self.username] = []

    @staticmethod
    def help():
        print("add (elements) -- add one or more elements to the container")
        print("remove (element) -- delete element from container")
        print("find (elements) -- check if the element is presented in the container")
        print("list -- print all elements of the container")
        print("grep -- check the elements of the container by regular expression")
        print("save -- save container to file")
        print("load -- load container from file")
        print("switch -- change user")
        print("help -- see all commands")
        print("exit -- exit from program")
