import sys

from matplotlib import lines

# method that read file 
def load():
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
    for i in range(Processes):
        row=[]
        for j in range(Resources):
            row.append(0)
        allocated.append(row)
    return Processes, Resources, max_matrix, available, allocated
