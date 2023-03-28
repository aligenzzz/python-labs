from text_statistics import TextStatistics
from interactive_container import InteractiveContainer

def task1():
    text = TextStatistics('text_files/text.txt')
    # text.print_file()
    print("Amount of all sentences in text =", text.sentences_amount())
    print("Amount of declarative sentences in text =", text.declarative_sentences_amount())
    print("Amount of non-declarative sentences in text =", text.non_declarative_sentences_amount())
    sentences_average_length = text.sentences_average_length()
    print("Average length of the sentence =", sentences_average_length[0], "words,",
          sentences_average_length[1], "characters")
    print("Average length of the word in the text =", text.words_average_length(), "characters")
    print(text.top_k_n_grams(5, 2), '\n')

def task2():
    while True:
        username = input("Enter username: ")
        container = InteractiveContainer(username)

        while True:
            command = input("Do you want load data? (yes/no) ")
            if command == "yes":
                container.load()
                break
            elif command == "no":
                container.load_username()
                break

        while True:
            command = input("Enter command: ")
            if command.startswith("add"):
                args = command.split()[1:]
                container.add(*args)
            elif command.startswith("remove"):
                key = command.split()[1]
                container.remove(key)
            elif command.startswith("find"):
                args = command.split()[1:]
                container.find(*args)
            elif command == "list":
                container.list()
            elif command.startswith("grep"):
                pattern = command.split()[1]
                container.grep(pattern)
            elif command == "save":
                container.save()
            elif command == "load":
                container.load()
            elif command == "switch":
                while True:
                    command = input("Do you want save data? (yes/no) ")
                    if command == "yes":
                        container.save()
                        break
                    elif command == "no":
                        break
                break
            elif command == "help":
                container.help()
            elif command == "exit":
                while True:
                    command = input("Do you want save data? (yes/no) ")
                    if command == "yes":
                        container.save()
                        break
                    elif command == "no":
                        break
                return
            else:
                print("Unknown command :(")


if __name__ == "__main__":
    task1()
    task2()




