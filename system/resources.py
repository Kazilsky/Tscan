import psutil


class ResourceInfo:

    @property
    def cpu_usage(self):
        return psutil.cpu_percent(interval=None)

    @property
    def memory(self):
        return psutil.virtual_memory()

    @property
    def swap(self):
        return psutil.swap_memory()