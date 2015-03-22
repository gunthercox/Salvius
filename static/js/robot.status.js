window.Robot = window.Robot || {};

var Robot = Robot || {};

Robot.prototype.renderStatus = function() {
    var robot = this;

    $.ajax({
        type: "GET",
        url: "/api/device_ports/"
    }).success(function(data) {
        $(".usb-devices").empty().text(data.results.length);
    });

    $.ajax({
        type: "GET",
        url: "/api/status/"
    }).success(function(data) {

        new Chartist.Line(".api-response-time", {
            labels: new Array(data["api_response_time"].length),
            series: [
                data["api_response_time"]
            ]
        },
        {
            showPoint: false,
            lineSmooth: false
        });

        new Chartist.Line(".web-response-time", {
            labels: new Array(data["web_response_time"].length),
            series: [
                data["web_response_time"]
            ]
        },
        {
            showPoint: false,
            lineSmooth: true
        });

        var boot_time = moment(data["boot_time"], "YYYY-M-D h:mm:ss%S").calendar();
        var boot_time_from_now = moment(data["boot_time"], "YYYY-M-D h:mm:ss%S").fromNow()
        $(".js-boot-time").text(boot_time_from_now);
        $(".js-boot-time").attr("title", boot_time);

        $(".js-disk-useage").text(data["disk_useage"]["percent"] + "%");

        $(".js-virtual-memory-percent").text(data["virtual_memory"]["percent"] + "%");
        $(".js-virtual-memory-used").text(data["virtual_memory"]["used"]);
        $(".js-virtual-memory-total").text(data["virtual_memory"]["total"]);

        $(".js-swap-memory-percent").text(data["swap_memory"]["percent"] + "%");
        $(".js-swap-memory-used").text(data["swap_memory"]["used"]);
        $(".js-swap-memory-total").text(data["swap_memory"]["total"]);

        $(".js-cpu-percent-values").empty();

        var $cpu_table_headings = $(".js-cpu-percent-headings");
        var $cpu_table_values = $(".js-cpu-percent-values");
        $cpu_table_headings.empty();
        $cpu_table_values.empty();
        for (var i = 0; i < data["cpu_percent"].length; i++) {
            var head = $('<th class="text-center"></th>');
            head.text("CPU " + i);
            $cpu_table_headings.append(head);

            var block = $('<td></td>');
            block.text(data["cpu_percent"][i] + "%");
            $cpu_table_values.append(block);
        }

        new Chartist.Pie(".disk-io-counters", {
            labels: [data.disk_io_counters.read_mb, data.disk_io_counters.write_mb],
            series: [data.disk_io_counters.read, data.disk_io_counters.write]
        });

        new Chartist.Pie(".net-io-counters", {
            labels: [data.net_io_counters.received_mb, data.net_io_counters.sent_mb],
            series: [data.net_io_counters.received, data.net_io_counters.sent]
        });
        //data["disk_io_counters"]["packets_recv"]

    }).error(function() {
        robot.error("Unable to connect to status api.");
    });

    $.ajax({
        url: "http://api.travis-ci.org/repos?slug=gunthercox%2Fsalvius",
        jsonp: "callback",
        cache: true,
        dataType: "jsonp",
    }).success(function(data) {
        var status = $(".js-unit-test-status");

        if (data[0].last_build_status == 0) {
            status.text("Passing");
        } else {
            status.text("Failing");
        }

    }).error(function() {
        robot.error("Unable to connect to CI server api.");
    });
}
