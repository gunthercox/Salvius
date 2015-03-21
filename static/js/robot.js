window.Robot = window.Robot || {};

var Robot = function() {
    this.mobile = false;

    this.urls = {
        "api_neck": "/neck/",
        "api_legs": "/legs/",
        "api_arms": "/arms/",
        "api_chat": "/api/chat/",
        "speech": "/api/speech/",
        "terminate": "/api/terminate/",
        "camera_image_url": "http://192.168.1.2/image/jpeg.cgi"
    };

    this.timers = {
        "rotationReset": 0,
        "angleReset": 0
    };
}

Robot.prototype.loading = function($container) {
    var spinner = $('<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>');
    $container.html(spinner);
}

Robot.prototype.error = function(message) {
    var message = message || "Error";

    // For browsers that do not support notifications
    if (!Notification) {
        alert(message);
        return;
    }

    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    var notification = new Notification('Warning', {
        icon: "/images/icon.png",
        body: message,
    });

}

Robot.prototype.terminate = function() {
    var message = "WARNING: Emergency shutdown operation will deactivate all systems on the robot."
    var request = new XMLHttpRequest();
    if (confirm(message)) {
        request.open("POST", this.urls.terminate, true);
        request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        request.send({});
    }
}

Robot.prototype.snapshot = function() {
    var check = confirm("Save camera image?");
    if (check == true) {
        window.open(Robot.urls.camera_image_url, "_blank");
    }
}

Robot.prototype.updateSessionLog = function(data, $session_log) {

    console.log(data.input, data.response);

    // If input text was provided
    if (data.input) {
        $session_log.append($('<div class="text"></div>').text(data.input));
    }

    // If response text was provided
    if (data.response) {
        $session_log.append($('<div class="text"></div>').text(data.response));
    }

    // Scroll to the bottom of the log window
    $session_log[0].scrollTop = $session_log[0].scrollHeight;
}

Robot.prototype.respond = function(text, $session_log, $statusIndicator) {
    var robot = this;
    var origional =  $statusIndicator;
    var container = $statusIndicator.parent();
    robot.loading(container);

    $.ajax({
        type: "POST",
        url: robot.urls.api_chat,
        data: JSON.stringify({text: text}),
        contentType: "application/json"
    }).done(function(data) {
        robot.updateSessionLog(data, $session_log);
        container.html(origional);
    });
}
