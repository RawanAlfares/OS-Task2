#============ method that simulate process execition in safe order
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


