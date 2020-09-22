# by Sekomer 

import os
import sys
import random
import time
import heapq
import webbrowser
from math import ceil

# list of Server Units
number_of_units = 12
unit_objects = []

# 12 Units ( 128 CPU, 70TB Storage, 1TB RAM)

# quantity of cpu(unit) / ram(GB) and storage(GB)
class Unit(object):
    def __init__(self, name, number):
        # these are static
        self.name = name
        self.number = number
        self.cpu = 128
        self.ram = 1000
        self.storage = 70000
        # these are dynamic
        self.number_of_clients = 0
        self.client_list = list() 
        self.used_cpu = 0
        self.used_ram = 0
        self.used_storage = 0
    
    def heapify_for_cpu(self):
        return heapq.heapify(self.sort_clients_for_cpu)

    def sort_clients_for_cpu(self):
        return sorted(self.client_list, key= lambda x: x.cpu)

    def sort_clients_for_ram(self):
        return sorted(self.client_list, key= lambda x: x.ram)

    def sort_clients_for_storage(self):
        return sorted(self.client_list, key= lambda x: x.storage)

    # Changing the amount of used hardware
    def update_used_hardware(self, c_change, r_change, s_change):
        self.used_cpu += c_change
        self.used_ram += r_change
        self.used_storage += s_change   

    # Amount of used hardware, returns tuple(cpu,ram,storage)
    def used_hardware_data(self):
        return (self.used_cpu , 
                self.used_ram , 
                self.used_storage) 

    # Amount of available hardware, returns as tuple(cpu,ram,storage)
    def available_hardware(self):
        c, r, s = self.used_hardware_data()
        return (self.cpu - c,
                self.ram - r, 
                self.storage - s)

    # Adds a client to self unit and updates used hardware 
    def add_client(self, client):
        self.client_list.append(client)
        self.number_of_clients +=1
        self.update_used_hardware(client.cpu, client.ram, client.storage)

    # Removes a client from self unit and updates used hardware 
    def remove_client(self, client):
        self.client_list.remove(client)
        self.number_of_clients -= 1
        self.update_used_hardware(-client.cpu, -client.ram, -client.storage)
    
    # Returns percentage of available hardware as tuple(cpu,ram,storage)
    def available_hardware_percentage(self):
        return (100* ((self.cpu - self.used_cpu) / self.cpu)  ,
                100* ((self.ram - self.used_ram) / self.ram)   ,
                100* ((self.storage - self.used_storage) / self.storage) )

    def used_hardware_percentage(self):
        used = self.available_hardware_percentage()
        non = (100, 100, 100)
        result = tuple(map(lambda i, j: i - j, non, used))
        return result 


# Client class, holds id, cpu, ram, storage, unit(integer)
class Client(object):
    def __init__(self, client_id, cpu, ram, storage, unit):
        self.client_id = client_id
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.unit = unit

    def update_hardware(self):
        pass    


## Creating Server Units ##
for i in range(number_of_units):
    obj = Unit("unit" + str(i + 1), i + 1)
    unit_objects.append(obj)


text = """
[*] Welcome, enter the value of operation you'd like to do.
[1] Create a Client 
[2] Delete a Client
[3] Optimize Units ( for CPU or Default ) ***
[4] Show Clients of specific unit
[5] Show Available Hardware Bar per Unit
[6] Show Used Hardware Bar per Unit
[7] Open Github
[8] Create 10 random clients on random Units
[Else] Quit"""


# from a list of objects returns that has maximum of arg attribute
def return_max(iterable, arg):
    return eval(f"max(iterable, key = lambda x: x.{arg})")


# (100,80,15) => returns true
# returns if it's better or not to transfer that client
def compare_and_transfer_cpu(x_unit, y_unit, client_cpu):
    # if original is better, returns zero
    current_diff = abs(x_unit.used_cpu - y_unit.used_cpu) 
    candidate_diff = abs((x_unit.used_cpu - client_cpu) - (y_unit.used_cpu + client_cpu))
    if  current_diff < candidate_diff:
        return False

    return True


while True:
    os.system('cls')
    print(text); print();
    operation = input("[*]")

    if operation == "1":
        os.system('cls')
        print("[*] CREATING CLIENT")
        print("Enter your client id, needed cpu / ram / storage quantites (indicate if you want to choose specific unit)")
        
        client_id = input("Your Id (must be alphanumeric): ")
        if not client_id.isalnum() or client_id == "":
            print("Invalid input !")
            input("press enter to continue:")
            continue

        client_cpu = input("Amount of CPU (integer): ")
        if not str(client_cpu).isnumeric() or client_cpu == "":
            print("Invalid input !")
            input("press enter to continue:")
            continue

        elif int(client_cpu) > 128: 
            print("You can't take more than 128 CPU")
            input("press enter to continue:")
            continue

        client_ram = input("Amount of RAM(GB): ")
        if not str(client_ram).isnumeric() or client_ram == "":
            print("Invalid input !")
            input("press enter to continue:")
            continue

        elif int(client_ram) > 1000: 
            print("You can't take more than 1TB RAM")
            input("press enter to continue:")
            continue

        client_storage = input("Amount of Storage(GB): ")
        if not str(client_storage).isnumeric() or client_storage == "":
            print("Invalid input !")
            input("press enter to continue:")
            continue

        elif int(client_storage) > 70000: 
            print("You can't take more than 70TB Storage")
            input("press enter to continue:")
            continue

        client_cpu = int(client_cpu)
        client_ram = int(client_ram)
        client_storage = int(client_storage)

        avail = list()

        for i in unit_objects:
            a,b,c = i.available_hardware()
            if (a > client_cpu and b > client_ram and c > client_storage):
                avail.append(i.number)

        print()
        print("Available Units are:")
        print(avail)
        
        unit_choice = int(input("To Which Unit [1 to 12] ? / 0 for random: "))
        if not unit_choice in range(13):
            print("Invalid interval !")
            input("Press enter to continue")
            continue

        while True:

            # Checking if the random choosen or not
            if unit_choice == 0:
                rand = random.choice(avail)
                where = unit_objects[rand - 1]

            else:
                where = unit_objects[unit_choice - 1]
                    
            c, r, s = where.available_hardware() 

            if c < client_cpu or r < client_ram or s < client_storage:
                os.system('cls')
                print("This unit is full, try another one...")
                input("press enter to continue:")
                break

            else:
                new_client = Client(client_id, client_cpu, client_ram, client_storage, where.number)
                where.add_client(new_client)

                os.system('cls')
                print(f"[Client Added]",  
                      f"Client Id: {client_id} ", 
                      f"Client cpu: {client_cpu}CPUs",
                      f"Client ram: {client_ram}GB", 
                      f"Client storage: {client_storage}GB", sep="\n", end="\n")

                print(f"System usage of {where.name.upper()} after adding client: ", end="")
                c,r,s = where.used_hardware_percentage()
                print(f"CPU: %{c:.2f}, RAM: %{r:.2f}, Storage: %{s:.2f}")
                print()

                time.sleep(0.01)
                input("press enter to continue: ")
                break

        
    elif operation == "2":
        os.system('cls')
        which_unit = int(input("From which unit you'd like to delete client ? (1 to 12): "))
        where = unit_objects[which_unit - 1]

        if where in unit_objects:
            names = [(i, i.client_id) for i in where.client_list]
            for idd in names:
                print(idd[1], end="\n")
        
            deleting = input("Enter the ID you'd like to delete: ")
            flag = True
            for i in names:
                if i[1] == deleting:
                    flag = False
                    where.remove_client(i[0])
                    print(f"{deleting} is deleted from {where.name.upper()}...")
                    input("press enter to continue:")
                    break

            if flag:
                print("Wrong ID !!!")
                input("Press enter to continue :")

        else:
            os.system('cls')
            print("Incorrect Unit Number, try again...")
            time.sleep(3)


    elif operation == "3":
        os.system('cls')
        print("Optimization Options")
        print("[1] Optimize for CPUs", 
              "[2] Default Optimization", sep="\n")

        opt_type = input("Optimization Type: ")

        if opt_type == "1":
            #objects 
            client_number_sorted = sorted(unit_objects, key= lambda x: x.number_of_clients)
            crowded_units_list = [i for i in client_number_sorted if i.number_of_clients > 1]
            # ooof moment
            crowded_units_list = crowded_units_list[::-1]

            
            # If there are empty units and crowded units, biggest unit of crowded goes to empty one and comforts most used server
            if any(unit.used_cpu == 0 for unit in unit_objects):
                for crowded_unit in crowded_units_list:    
                    while any(unit.used_cpu == 0 for unit in unit_objects) and crowded_unit.number_of_clients > 1:
                        # index 0 is lowest, index -1 is max
                        cpu_sorted = sorted(unit_objects, key= lambda x: x.used_cpu)
                        clients_of_crowded = crowded_unit.sort_clients_for_cpu()
                        # biggest client of crowded unit
                        moving_client = clients_of_crowded[-1]
                        crowded_unit.remove_client(moving_client)                
                        # as soon as there are empty units we can use first one in the list
                        cpu_sorted[0].add_client(moving_client)
                        moving_client.unit = cpu_sorted[0].number 
                    
                    # if loop comes here that means unit.number_of_clients is no more greater than 1, so remove it and continue
                    crowded_units_list.remove(crowded_unit)

            # if there are no empty slots and there are some units with more than 1 client
            if not any(unit.used_cpu == 0 for unit in unit_objects) and crowded_units_list:
                cpu_sorted = sorted(unit_objects, key= lambda x: x.used_cpu)

                for unit in cpu_sorted[::-1]:
                    check = 0
                    
                    while True:
                        if not unit.number_of_clients > 1:
                            break

                        clients_of_crowded = unit.sort_clients_for_cpu()
                        # if sort doesn't change, break the while loop
                        if check == clients_of_crowded:
                            break

                        check = clients_of_crowded.copy()

                        # finding emptiest unit and checking if its the same unit or not
                        cpu_sorted = sorted(unit_objects, key= lambda x: x.used_cpu)
                        smallest_unit = cpu_sorted[0]
                        if smallest_unit == unit:
                            break

                        # checking if we can transfer smallest or biggest client of crowded unit
                        little, big = clients_of_crowded[0], clients_of_crowded[-1] 
                        if compare_and_transfer_cpu(unit, smallest_unit, big.cpu):    
                            unit.remove_client(big)
                            smallest_unit.add_client(big) 
                            big.unit = smallest_unit.number

                        
                        elif compare_and_transfer_cpu(unit, smallest_unit, little.cpu):
                            unit.remove_client(big)
                            smallest_unit.add_client(big)
                            little.unit = smallest_unit.number

        
        else:
            os.system('cls')
            print('Invalid Input !')
            continue


    elif operation == "4":
        os.system('cls')
        in_4 = int(input("Which Units Clients you'd like to see ? (1 to 12) : "))
        where = unit_objects[in_4 -1] 
        print()
        if in_4 in range(1,number_of_units + 1):
            if where.client_ids == {}:
                print("Empty Unit")
            else:
                print("{0} clients found on Unit {1}".format(where.number_of_clients, in_4))
                for num, i in enumerate(where.client_ids):
                    a,b,c = where.client_ids[i]
                    print(f"[{num + 1}]", i, f" CPUs:{a}, RAM:{b}GB, Storage:{c}GB", end = "\n")

            input("press enter to continue:")
            continue
                
        else:
            print("Wrong unit number! ")
            time.sleep(3)


    elif operation == "5":
        os.system('cls')
        print("AVAILABLE HARDWARE:")
        for num, unit in enumerate(unit_objects):
            c, r, s = unit.available_hardware_percentage()
            print(f"Unit{num + 1}:")
            print(f"Number of Clients: {unit.number_of_clients}")
            print(f"CPU: %{c:.2f}, RAM: %{r:.2f}, Storage: %{s:.2f}")
            for item in (c, r, s):
                percent = int(ceil(item/10))
                print("[" + "#" * (percent) + " "*(10-percent) + "]", end=" ")
            print()
            time.sleep(0.2)
        
        print()
        input("press enter to continue:")
        continue       

    elif operation == "6":
        os.system('cls')
        print("USED HARDWARE: (# is between 0 and 10)")
        for num, unit in enumerate(unit_objects):
            c, r, s = unit.used_hardware_percentage()
            print(f"Unit{num + 1}:")
            print(f"Number of Clients: {unit.number_of_clients}")
            print(f"CPU: %{c:.2f}, RAM: %{r:.2f}, Storage: %{s:.2f}")
            for item in (c, r, s):
                percent = int(ceil(item/10))
                print("[" + "#" * (percent) + " "*(10-percent) + "]", end=" ")
            print()
            time.sleep(0.2)
        
        print()
        input("press enter to continue:")
        continue       


    elif operation == "7":
        webbrowser.open("https://github.com/Sekomer/Server-Optimization-Model/blob/master/cloud_optimization.py", new = 2)   

    elif operation == "8":
        name = "qwertyuıopğüişlkjhgfdsazxcvbnmöç"
        client_types = ((1,8,250), (4,20,1000), (3,6,700))
        for _ in range(10):
            random_id = ''.join(random.choice(name) for i in range(5))
            random_client = random.choice(client_types)
            random_unit = random.choice(unit_objects) 
            a, b, c = random_client
            new_client = Client(random_id, a, b, c, random_unit.number)
            random_unit.add_client(new_client)


    else:
        for i in range(10): 
            os.system('cls')
            print("QUITING...")
            print("[" + "#" * (i+1) + " "*(9-i) + "]")
            time.sleep(0.2)

        os.system('cls')
        sys.exit()