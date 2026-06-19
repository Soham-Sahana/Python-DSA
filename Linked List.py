class Node:
    def __init__(self,info):
        self.info=info
        self.link=None

class LinkedList:
    def __init__(self):
        self.start=None
    def insert(self):
        info=int(input("Enter any number:"))
        temp=Node(info)
        if self.start is None:
            self.start=temp
        else:
            t1=self.start
            while t1.link is not None:
                t1 = t1.link
            t1.link=temp
    def delete_node(self):
        if self.start is None:
            print('List is empty:')
        else:
            self.start=self.start.link
    def print_list(self):
        if self.start is None:
            print('List is empty:')
        else:
            t2=self.start
            while t2 is not None:
                print(t2.info,end=" ")
                t2=t2.link
            print()
    def menu(self):
        print("1.ADD\n2.Delete\n3.Print\n.4Exit")
        return int(input("Enter your choice:"))
    def run(self):
        while True:
            choice=self.menu()
            if choice == 1:
                self.insert()
            elif choice == 2:
                self.delete_node()
            elif choice == 3:
                self.print_list()
            elif choice == 4:
                exit()
            else:
                print("Invalid entry/choice...")

if __name__=="__main__":
    sl=LinkedList()
    sl.run()