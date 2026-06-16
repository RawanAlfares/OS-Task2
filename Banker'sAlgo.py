import sys

from matplotlib import lines

# method that read file 
def load_input():
    try:
        with open("input.txt", 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in f:
                line=line.strip()
                if line:
                    lines.append(line)     
    except FileNotFoundError:
        print(f"Error: File 'input.txt' not found.")
        sys.exit(1)

    Processes=0
    Resources=0
    max_matrix=[]
    available=[]
    allocated=[]
    need=[]

    i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('N') and '=' in line:
            Processes=int(line.split("=")[1].strip())
        elif line.startswith('M') and '=' in line and line != 'MAX':
            Resources=int(line.split("=")[1].strip())
        elif line == 'MAX':
            i+=1
            while i < len(lines) and len(max_matrix) < Processes:
                row=lines[i].split()
                if len(row)==Resources:
                    max_matrix.append(list(map(int,row)))
                    i+=1
                else:
                    break
                continue
        elif line == 'AVAILABLE':
            i += 1
            row2=lines[i].split()
            available = list(map(int,row2))
        i += 1
    if Processes==0 or Resources==0 or len(max_matrix)!=Processes or len(available)!=Resources:
        print("Error: Invalid input file format.")
        sys.exit(1)
    
    # initialize allocated list by 0 
    for _ in range(Processes):
        row=[]
        for _ in range(Resources):
            row.append(0)
        allocated.append(row)
    return Processes, Resources, max_matrix, available, allocated


# method checks if the process requeset remains the system in safe state 
def request_resources(pid ,processes,resources, request,available,need,allocated , max_matrix):

    #check if the id process is valid
    if pid <0 or pid>=processes:
        print(f"Invalid process ID P{pid}")
        return False
    
    #check if the request length is available
    if len(request)!=resources:
        print(f"equest must have exactly {resources} resource values")
        return False
    
    #check if request in range of process needs
    for p in range(len(request)):
        if request[p]<0:
            print("Invalid , Request values can not be negative")
            return False
        if request[p]>need[pid][p]:
            print (f"Request exceeds maximum need for P{pid}")
            return False
    
    #check if the request in range of available processes
    for p in range(len(request)):
        if request[p]>available[p]:
            print (f"Resources not available")
            return False
    
    #Resources are temporarily allocated to the process to check whether the system remains in a safe state.    
    available_copy=available[:]
    allocated_copy=[]
    need_copy=[]
    for row in allocated:
        allocated_copy.append(row[:])
    for row in need:
        need_copy.append(row[:])
    
    for p in range(resources):
        available_copy[p]-=request[p]
        need_copy[pid][p]-=request[p]
        allocated_copy[pid][p]+=request[p]

    # check wether the system remians in safe state
    ''' call is_safe() '''

'''
   if safe:
        # Commit
        for p in range(resources):
            available[p]= available_copy[p]
            allocated[pid][p]= allocated_copy[pid][p]
            need[pid][p]= need_copy[pid][p]
        return True, seq
    else:
        return False, "This request would lead to an unsafe state."
'''
