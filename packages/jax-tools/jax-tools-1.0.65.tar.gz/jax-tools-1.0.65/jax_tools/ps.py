import platform
import psutil

def get_process_info():
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(process.info)
    return processes

def print_process_info():
    processes = get_process_info()
    filtered_processes = [process for process in processes if process['cpu_percent'] is not None]
    sorted_processes = sorted(filtered_processes, key=lambda x: x['cpu_percent'], reverse=True)
    print("PID\tCPU%\tMemory%\tName")
    for process in sorted_processes:
        print(f"{process['pid']}\t{process['cpu_percent']}\t{process['memory_percent']}\t{process['name']}")

def main():
    system = platform.system()
    if system == 'Linux' or system == 'Darwin':
        print_process_info()
    else:
        print("Unsupported operating system.")

if __name__ == '__main__':
    main()
