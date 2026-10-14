class SecurityCheck:

    def check_processes(self):
        raise NotImplementedError

    def check_systemd_services(self):
        raise NotImplementedError

    def check_temperature(self):
        raise NotImplementedError

    def check_updates(self):
        raise NotImplementedError

    def check_system_logs(self):
        raise NotImplementedError