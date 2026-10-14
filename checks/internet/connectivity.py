import time
import urllib.error
import urllib.request


class ConnectivityCheck:

    TARGETS = {
        "Google": "https://www.google.com/generate_204",
        "Cloudflare": "https://cp.cloudflare.com/generate_204",
    }

    def check(self, timeout=3):
        results = []

        for name, url in self.TARGETS.items():
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Tuscan/1.0"},
            )

            start = time.perf_counter()

            try:
                with urllib.request.urlopen(
                    request,
                    timeout=timeout,
                ) as response:
                    status = response.status

                results.append({
                    "name": name,
                    "available": 200 <= status < 400,
                    "status": status,
                    "latency_ms": round(
                        (time.perf_counter() - start) * 1000
                    ),
                    "error": None,
                })

            except urllib.error.HTTPError as error:
                results.append({
                    "name": name,
                    "available": True,
                    "status": error.code,
                    "latency_ms": round(
                        (time.perf_counter() - start) * 1000
                    ),
                    "error": f"HTTP {error.code}",
                })

            except (
                urllib.error.URLError,
                TimeoutError,
                OSError,
            ) as error:
                results.append({
                    "name": name,
                    "available": False,
                    "status": None,
                    "latency_ms": None,
                    "error": str(error),
                })

        return results