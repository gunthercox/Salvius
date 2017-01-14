from flask.views import MethodView


class Status(MethodView):

    def get_response_times(self, analytics_key):
        from jsondb.db import Database
        database = Database("settings.db")

        if analytics_key not in database:
            return []

        return database[analytics_key]

    def bytes2human(self, n):
        # http://code.activestate.com/recipes/578019
        # >>> bytes2human(10000)
        # '9.8K'
        # >>> bytes2human(100001221)
        # '95.4M'
        symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def get(self):
        from flask import jsonify
        import psutil
        from datetime import datetime

        data = {}

        disk_useage = psutil.disk_usage("/")
        disk_io_counters = psutil.disk_io_counters(perdisk=False)
        net_io_counters = psutil.net_io_counters(pernic=False)
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()

        data["cpu_percent"] = psutil.cpu_percent(interval=1, percpu=True)
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        data["boot_time"] = boot_time.strftime('%Y-%m-%d %H:%M:%S')

        data["disk_useage"] = {}
        data["disk_useage"]["free"] = self.bytes2human(disk_useage.free)
        data["disk_useage"]["percent"] = disk_useage.percent
        data["disk_useage"]["total"] = self.bytes2human(disk_useage.total)
        data["disk_useage"]["used"] = self.bytes2human(disk_useage.used)

        data["disk_io_counters"] = {}
        data["disk_io_counters"]["read"] = disk_io_counters.read_bytes
        data["disk_io_counters"]["write"] = disk_io_counters.write_bytes
        data["disk_io_counters"]["read_mb"] = self.bytes2human(
            disk_io_counters.read_bytes
        )
        data["disk_io_counters"]["write_mb"] = self.bytes2human(
            disk_io_counters.write_bytes
        )
        data["disk_io_counters"]["read_time"] = disk_io_counters.read_time
        data["disk_io_counters"]["write_time"] = disk_io_counters.write_time
        data["disk_io_counters"]["write_count"] = disk_io_counters.write_count

        # net_io_counters also supports dropin, dropout, errout
        data["net_io_counters"] = {}
        data["net_io_counters"]["received"] = net_io_counters.bytes_recv
        data["net_io_counters"]["sent"] = net_io_counters.bytes_sent
        data["net_io_counters"]["received_mb"] = self.bytes2human(
            net_io_counters.bytes_recv
        )
        data["net_io_counters"]["sent_mb"] = self.bytes2human(
            net_io_counters.bytes_sent
        )
        data["net_io_counters"]["packets_recv"] = net_io_counters.packets_recv
        data["net_io_counters"]["packets_sent"] = net_io_counters.packets_sent

        # virtual_memory also supports:
        # active, available, buffers, cached, inactive
        data["virtual_memory"] = {}
        data["virtual_memory"]["free"] = self.bytes2human(virtual_memory.free)
        data["virtual_memory"]["percent"] = virtual_memory.percent
        data["virtual_memory"]["total"] = self.bytes2human(
            virtual_memory.total
        )
        data["virtual_memory"]["used"] = self.bytes2human(virtual_memory.used)

        # swap_memory also supports sin, sout
        data["swap_memory"] = {}
        data["swap_memory"]["free"] = self.bytes2human(swap_memory.free)
        data["swap_memory"]["percent"] = swap_memory.percent
        data["swap_memory"]["total"] = self.bytes2human(swap_memory.total)
        data["swap_memory"]["used"] = self.bytes2human(swap_memory.used)

        # API response times
        data["api_response_time"] = self.get_response_times(
            "api_response_time"
        )
        data["web_response_time"] = self.get_response_times(
            "web_response_time"
        )

        return jsonify(data)
