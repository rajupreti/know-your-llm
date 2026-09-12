import psutil
import torch
import GPUtil


def check_storage():
    partitions = psutil.disk_partitions()
    total = used = free = 0
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total += usage.total
            used += usage.used
            free += usage.free
        except Exception:
            continue
    print("="*50)
    print()
    print(f"Total Storage: {total / 1024**3:.2f} GB")
    print(f"Used Storage: {used / 1024**3:.2f} GB")
    print(f"Free Storage: {free / 1024**3:.2f} GB")
    print()
    print("="*50)
    print()


def check_ram():
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024**3)
    used_ram = ram.used / (1024**3)
    free_ram = ram.free / (1024**3)

    print(f"Total RAM: {total_ram:.2f} GB")
    print(f"Used RAM: {used_ram:.2f} GB")
    print(f"Free RAM: {free_ram:.2f} GB")

    print()
    print("="*50)
    print()


def check_gpu():
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("No NVIDIA GPU detected.")
        return

    try:
        allocated_vram = torch.cuda.memory_allocated(0) / (1024**3)
        reserved_vram = torch.cuda.memory_reserved(0) / (1024**3)
    except Exception:
        print("No NVIDIA GPU detected.")
        return

    for gpu in gpus:
        gpu_name = gpu.name
        gpu_memory_total = gpu.memoryTotal / 1024
        gpu_memory_used = gpu.memoryUsed / 1024
        gpu_memory_free = gpu.memoryFree / 1024
        gpu_load = gpu.load * 100

        print(f"GPU: {gpu_name}")
        print(f"Total VRAM: {gpu_memory_total:.2f} GB")
        print(f"Used VRAM: {gpu_memory_used:.2f} GB")
        print(f"Free VRAM: {gpu_memory_free:.2f} GB")
        print(f"GPU Load: {gpu_load:.2f}%")
        print(f"Allocated VRAM: {allocated_vram:.2f} GB")
        print(f"Reserved VRAM: {reserved_vram:.2f} GB")
        print(f"GPU Temperature: {gpu.temperature} °C")

        print()
        print("="*50)
        print()


def check_processor():
    logical_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(interval=5)

    print(f"Physical Cores: {physical_cores}")
    print(f"Logical Cores: {logical_cores}")
    if cpu_freq:
        print(f"CPU Frequency: {cpu_freq.current / 1000:.2f} GHz")
    print(f"CPU Usage: {cpu_usage:.2f}%")

    print()
    print("="*50)
    print()


def main():
    check_storage()
    check_ram()
    check_gpu()
    check_processor()


if __name__ == "__main__":
    main()
