from mpi4py import MPI
import time



# bubble sort using mpi4py
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    l = ""
    # Define the array to be sorted
    with open('Input.txt', 'r') as file:
        for line in file:
            l = line.split()
    arr = [int(i) for i in l]
    # Split the array into chunks for each process
    chunk_size = len(arr) // size
    local_arr = arr[rank * chunk_size:(rank + 1) * chunk_size]

    # Perform local bubble sort
    start_time = time.time()

    bubble_sort(local_arr)

    # Gather all the sorted chunks
    sorted_arr = comm.gather(local_arr, root=0)

    # Merge and print the sorted array
    if rank == 0:
        sorted_arr = [item for sublist in sorted_arr for item in sublist]
        bubble_sort(sorted_arr)
        print("Sorted array:", sorted_arr)

    print("size: ", size, "Rank: ", rank, "Time: ", time.time() - start_time)

        
# from mpi4py import MPI
# import numpy as np

# def bubble_sort(data):
#     n = len(data)
#     for i in range(n):
#         for j in range(0, n-i-1):
#             if data[j] > data[j+1]:
#                 data[j], data[j+1] = data[j+1], data[j]

# if __name__ == "__main__":
#     comm = MPI.COMM_WORLD
#     rank = comm.Get_rank()
#     size = comm.Get_size()
#     l = ""
#     if rank == 0:
#         # Generate random data on the root process
#         with open('C:/Users/vlads/OneDrive/Рабочий стол/study/Kyiv uni/РПП/ParallelBubbleSortOmp/Input.txt', 'r') as file:
#             for l in file:
#                 l = line.split()
#         data = [int(i) for i in l]
#     else:
#         data = None

#     # Scatter data to all processes
#     local_data = np.empty(100 // size, dtype=int)
#     comm.Scatter(data, local_data, root=0)

#     # Each process sorts its own portion of data
#     bubble_sort(local_data)

#     # Gather sorted data from all processes
#     sorted_data = None
#     if rank == 0:
#         sorted_data = np.empty(100, dtype=int)
#     comm.Gather(local_data, sorted_data, root=0)

#     if rank == 0:
#         # Final sorting on the root process
#         bubble_sort(sorted_data)
#         print("Sorted data:", sorted_data)