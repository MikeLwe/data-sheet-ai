import csv

def read_csv():
    path = input("Enter the path of the file you want to submit: ")
    with open(path, mode ='r')as file:
        content = csv.reader(file)
    return content



if __name__ == '__main__':
    read_csv()
