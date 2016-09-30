window.Robot = window.Robot || {};



var api_chat = 'http://localhost:8000/api/robots/Salvius/devices/communication/commands/get_response';


var Robot = function(apiBase, options) {
    this.mobile = false;
    this.options = options;

    this.apiBase = apiBase;

    this.timers = {
        "rotationReset": 0,
        "angleReset": 0
    };

    this.load(apiBase);
}

Robot.prototype.load = function(apiBaseUrl) {
    var robot = this;

    var $get = $.ajax({
        url: apiBaseUrl,
        type: 'GET'
    });

    $get.done(function(data) {
        robot.build(data);
    });

};

Robot.prototype.build = function(data) {
    var robot = this;

    robot.activateCameras(data.robot.devices, function(cameraData) {

        console.log(cameraData);

        robot.options.camera.networkCamera({
            'url': cameraData.result,
            'stream': true
        });

    });
};

Robot.prototype.activateCameras = function(deviceList, callback) {
    var api_camera_image = '/devices/camera_one/commands/get_url';

    for (var i = 0; i < deviceList.length; i++) {
        if (deviceList[i].connection == 'camera') {
            $.ajax({
                url: robot.apiBase + api_camera_image,
                type: 'GET'
            }).done(function(data) {

                // Pass the results back to whatever the callback function was.
                callback(data);
            });
        }
    }
};

Robot.prototype.loading = function($container) {
    var spinner = $('<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>');
    $container.html(spinner);
};

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

    notification.onshow(function() {
        setTimeout(function() {
            notification.cancel();
        }, '5000');
    });
};

Robot.prototype.updateSessionLog = function(data, $session_log) {

    // If input text was provided
    if (data.input) {
        $session_log.append($('<div class="text"></div>').text(data.input.text));
    }

    // If response text was provided
    if (data.result) {
        $session_log.append($('<div class="text"></div>').text(data.result.text));
    }

    // Scroll to the bottom of the log window
    $session_log[0].scrollTop = $session_log[0].scrollHeight;
};

Robot.prototype.respond = function(text, $session_log, $statusIndicator) {
    var robot = this;
    var origional =  $statusIndicator;
    var container = $statusIndicator.parent();
    robot.loading(container);

    $.ajax({
        type: "POST",
        url: api_chat,
        data: JSON.stringify({'text': text}),
        contentType: "application/json"
    }).done(function(data) {
        data['input'] = {};
        data['input']['text'] = text;
        robot.updateSessionLog(data, $session_log);
        container.html(origional);
    });
};
