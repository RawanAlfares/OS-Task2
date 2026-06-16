import sys

def print_state(available, max_matrix, allocation, need):

    print("\nAVAILABLE:")
    for value in available:
        print(value, end=" ")
    print()

    print("\nMAX MATRIX:")
    for i in range(len(max_matrix)):
        print("P" + str(i), end=": ")
        for value in max_matrix[i]:
            print(value, end=" ")
        print()

    print("\nALLOCATION MATRIX:")
    for i in range(len(allocation)):
        print("P" + str(i), end=": ")
        for value in allocation[i]:
            print(value, end=" ")
        print()

    print("\nNEED MATRIX:")
    for i in range(len(need)):
        print("P" + str(i), end=": ")
        for value in need[i]:
            print(value, end=" ")
        print()

# ================= method that read file ==================== 
def load_input():
    try:
        with open("input.txt","r") as f:
            lines = [line.strip() for line in f if line.strip()]
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
    
    for i in range(Processes):
        row = []
        for j in range(Resources):
            row.append(max_matrix[i][j] - allocated[i][j])
        need.append(row)

    print("cant read")
    return Processes, Resources, max_matrix, available, allocated ,need

#=================== method that cheks if the system is safe or not ==============
def is_safe(process,resources,available,allocated,need):
    worked=[False]*process
    available_copy=available[:]
    safeProc =[]

    while len(safeProc)<process:
        found=False
        for p in range (process):
            if not worked[p]:
                can_run=True 
                for r in range (resources):
                    if need[p][r]>available_copy[r]:
                        can_run=False
                        break
                if can_run:
                    for r in range (resources): 
                        available_copy[r]+=allocated[p][r]
                    worked[p]=True
                    safeProc.append(p)
                    found=True
        if not found:
            break

    if all(worked):
        return True , safeProc
    else:
        return False,[]


#================= method request resources to process , if the system remains in safe state it cont =========     
def request_resources(pid, processes, resources, request, available, need, allocated, max_matrix):
    #check process ID
    if pid < 0 or pid >= processes:
        print(f"Invalid process ID P{pid}")
        return False, []

    #check request length
    if len(request) != resources:
        print(f"Request must have exactly {resources} resource values")
        return False, []

    #check negative values and request <= need
    for r in range(resources):
        if request[r] < 0:
            print("Invalid: Request values cannot be negative")
            return False, []

        if request[r] > need[pid][r]:
            print(f"Request denied: request exceeds maximum need for P{pid}")
            return False, []

    #check request <= available
    for r in range(resources):
        if request[r] > available[r]:
            print("Request denied: resources are not available")
            return False, []

    #temporarily allocate resources
    available_copy = available[:]

    allocated_copy = []
    for row in allocated:
        allocated_copy.append(row[:])

    need_copy = []
    for row in need:
        need_copy.append(row[:])

    for r in range(resources):
        available_copy[r] -= request[r]
        allocated_copy[pid][r] += request[r]
        need_copy[pid][r] -= request[r]

    #check if the new state is safe
    safe, safe_proc = is_safe(processes, resources, available_copy, allocated_copy, need_copy)

    if safe:
        for r in range(resources):
            available[r] = available_copy[r]
            allocated[pid][r] = allocated_copy[pid][r]
            need[pid][r] = need_copy[pid][r]

        print("Request granted.")
        print("Safe sequence:", end=" ")
        for p in safe_proc:
            print("P" + str(p), end=" ")
        print()

        return True, safe_proc

    else:
        print("Request denied: system would be in unsafe state.")
        return False, []
    


#================= method that releases resources from specific process ========
def release_resources(pid ,processes,resources, release,available,need,allocated , max_matrix):
    #check if the id process is valid
    if pid <0 or pid>=processes:
        print(f"Invalid process ID P{pid}")
        return False, f"Invalid process ID P{pid}."
    
    #check if the release length is available
    if len(release)!=resources:
        print(f"release must have exactly {resources} resource values")
        return False, f"Release vector must have exactly {resources} values."
    
    #check if release in range of process needs
    for p in range(len(release)):
        if release[p]<0:
            print("Invalid: Release values can not be negative")
            return False, "Release values cannot be negative."
        
        if release[p]>allocated[pid][p]:
            print (f"Invalid release: P{pid}"
                   f"but tried to release {release}.")
            return False ,(f"Invalid release: P{pid} only holds {allocated[pid]} "
                           f"but tried to release {release}.")

    for p in range(resources):
        available[p]+=release[p]
        allocated[pid][p]-=release[p]
        need[pid][p]+=release[p]

    return True,""

#============method that simulate process execition in safe order
def run_simulation( Processes, Resources, available, allocation, need):
    safe, seq = is_safe( Processes, Resources, available, allocation, need)
    if not safe:
        print("System is NOT in a safe state. Cannot run simulation.")
        return

    print(f"\nSafe sequence found: {' -> '.join('P'+str(p) for p in seq)}")
    print("\nSimulating process execution...\n")

    avail_sim = available[:]
    alloc_sim = [row[:] for row in allocation]

    for pid in seq:
        print(f"  P{pid} is executing...")
        for j in range(Resources):
            avail_sim[j] += alloc_sim[pid][j]
            alloc_sim[pid][j] = 0
        print(f"  P{pid} finished. Available -> {avail_sim}")

    # Update real state
    for j in range(Resources):
        available[j] = avail_sim[j]
    for i in range( Processes):
        for j in range(Resources):
            allocation[i][j] = alloc_sim[i][j]
    
    for i in range( Processes):
        for j in range(Resources):
            need[i][j]=0

    print("\nAll processes completed successfully.")



# ============ helpper function for reading rq and rl
def RQ_RL(parts, Resources):
    """Parse 'RQ/RL <pid> r0 r1 ... rm-1' into (pid, [resources])."""
    if len(parts) != 2 + Resources:
        return None, None, f"Expected: RQ/RL <process_id> followed by {Resources} resource values."
    try:
        pid = int(parts[1])
        resources = list(map(int, parts[2:2+Resources]))
        return pid, resources, None
    except ValueError:
        return None, None, "Process ID and resource values must be integers."


# =========== main method ============
def main():
    print("Program loaded successfully")
    Processes, Num_Res, max_matrix, available, allocated ,need= load_input()
    print(f"\nBanker's Algorithm loaded: { Processes} processes, {Num_Res} resource types.")
    print("Commands: RQ <pid> <r...>  |  RL <pid> <r...>  |  *  |  RUN  |  EXIT\n")

    while True:
        try:
            command = input("banker> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0].upper()

        if cmd == 'EXIT':
            print("PRAY FOR GAZA!")
            break

        elif cmd == '*':
            print_state(available, max_matrix, allocated, need)

        elif cmd == 'RQ':
            pid, resources, err = RQ_RL(parts, Num_Res)
            if err:
                print(f"Error: {err}")
                continue
            granted, info = request_resources(
                pid ,Processes,Num_Res, resources,available,need,allocated , max_matrix)
            if granted:
                seq_str = ' -> '.join('P' + str(p) for p in info)
                print(f"Request GRANTED for P{pid}.")
                print(f"Safe sequence: {seq_str}")
            else:
                print(f"Request DENIED for P{pid}. Reason: {info}")

        elif cmd == 'RL':
            pid, resources, err = RQ_RL(parts, Num_Res)
            if err:
                print(f"Error: {err}")
                continue
            success,msg= release_resources(pid ,Processes,Num_Res,resources,available,need,allocated ,max_matrix)
            
            if success:
                print(f"Resources successfully released by P{pid}.")
                print(f"Updated Available: {available}")
            else:
                print(f"Release FAILED. Reason: {msg}")

        elif cmd == 'RUN':
            run_simulation( Processes, Num_Res, available, allocated, need)

        else:
            print(f"Unknown command '{cmd}'. Valid commands: RQ, RL, *, RUN, EXIT")


if __name__ == '__main__':
    main()
