class InternetCheck:

    def check_connectivity(self):
        raise NotImplementedError(
            "Проверка доступности интернета ещё не реализована."
        )

    def check_open_ports(self):
        raise NotImplementedError(
            "Проверка открытых портов ещё не реализована."
        )

    def check_dns_leak(self):
        raise NotImplementedError(
            "Проверка DNS leak ещё не реализована."
        )

    def check_webrtc_leak(self):
        raise NotImplementedError(
            "Проверка WebRTC leak ещё не реализована."
        )

    def check_vpn(self):
        raise NotImplementedError(
            "Проверка VPN ещё не реализована."
        )