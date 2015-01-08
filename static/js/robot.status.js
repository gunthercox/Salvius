window.Robot = window.Robot || {};

var Robot = Robot || {};

Robot.prototype.renderStatus = function() {
    var robot = this;

    $.ajax({
        type: "GET",
        url: "/api/status/"
    }).success(function(data) {

        var boot_time = moment(data["boot_time"], "YYYY-M-D h:mm:ss%S").calendar();
        var boot_time_from_now = moment(data["boot_time"], "YYYY-M-D h:mm:ss%S").fromNow()
        $(".js-boot-time").text(boot_time_from_now);
        $(".js-boot-time").attr("title", boot_time);

        $(".js-disk-useage").text(data["disk_useage"]["percent"] + "%");
        $(".js-virtual-memory").text(data["virtual_memory"]["percent"] + "%");
        $(".js-swap-memory").text(data["swap_memory"]["percent"] + "%");

        $(".js-cpu-percent-values").empty();

        for (var i = 0; i < data["cpu_percent"].length; i++) {
            var head = $('<th class="text-center"></th>');
            head.text("CPU " + i);
            $(".js-cpu-percent-headings").append(head);

            var block = $('<td></td>');
            block.text(data["cpu_percent"][i] + "%");
            $(".js-cpu-percent-values").append(block);
        }

        //data["net_io_counter"]
        //data["disk_io_counters"]

    }).error(function() {
        robot.error("Unable to connect to status api.");
    });

}
