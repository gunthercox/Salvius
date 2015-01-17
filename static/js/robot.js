window.Robot = window.Robot || {};

var Robot = function() {
    this.activate();
    this.mobile = false;
}

Robot.prototype.urls = Robot.urls || {};
Robot.prototype.elements = Robot.elements || {};
Robot.prototype.timers = Robot.timers || {};

Robot.prototype.loading = function($container) {
    var spinner = $('<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>');
    $container.html(spinner);
}

Robot.prototype.error = function(error) {
    var error = error || "";

    if (error != "") {
        var template = $(
            '<div class="alert alert-warning">' + 
                '<button type="button" class="close" data-dismiss="alert">' +
                    '<span aria-hidden="true">&times;</span>' +
                '</button>' +
                '<p>' + error + '</p>' +
            '</div>'
        );
        $(".error-list").append(template);
    }

    // Change indicator led based on error count
    var errorCount = $(".error-list").find(".alert").length;
    if (errorCount > 0) {
        $(".js-warning").addClass("warning");
    } else {
        $(".js-warning").removeClass("warning");
    }
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

Robot.prototype.updateSessionLog = function(data) {

    // If input text was provided
    if (data.input) {
        this.elements.session_log.append($('<div class="text"></div>').text(data.input));
    }

    // If response text was provided
    if (data.response) {
        this.elements.session_log.append($('<div class="text"></div>').text(data.response[0]["text"]));
    }

    // Scroll to the bottom of the log window
    this.elements.session_log[0].scrollTop = this.elements.session_log[0].scrollHeight;
}

Robot.prototype.respond = function(text, $statusIndicator) {
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
        robot.updateSessionLog(data);
        container.html(origional);
    });
}

Robot.prototype.activate = function() {
    this.urls["api_neck"] = "/neck/";
    this.urls["api_legs"] = "/legs/";
    this.urls["api_arms"] = "/arms/";
    this.urls["api_chat"] = "/api/chat/";
    this.urls["speech"] = "/api/speech/";
    this.urls["terminate"] = "/api/terminate/";
    this.urls["camera_image_url"] = "http://192.168.1.2/image/jpeg.cgi";

    this.elements["terminate"] = $(".js-terminate");
    this.elements["session_log"] = $(".chat-log");
    this.elements["error_list"] = $(".error-list");
    this.elements["capture_photo"] = $(".js-capture-photo");
    this.elements["dismiss_all"] = $(".js-dismiss-all");
    this.elements["chat_input"] = $(".chat-input");
    this.elements["listen"] = $(".js-listen");
    this.elements["say"] = $("#say");
    this.elements["post"] = $("#post");
    this.elements["write"] = $("#write");
    this.elements["rotate_head"] = $(".js-rotate-head");
    this.elements["angle_head"] = $(".js-angle-head");

    this.timers["rotationReset"] = 0;
    this.timers["angleReset"] = 0;

    var robot = this;

    robot.elements.terminate.click(function() {
        robot.terminate();
    });

    robot.elements.error_list.on("click", ".js-dismiss", function() {
        $(this).parents(".alert").remove();
        robot.error();
    });

    robot.elements.dismiss_all.click(function() {
        $(".error-list .alert").remove();
        robot.error();
    });

    robot.elements.post.click(function() {
        var key = $("#key").val();
        var value = $("#value").val();
        var str = [key, value].join("=");
        $.ajax({
            type: "POST",
            url: robot.urls.arduino_ip,
            data: str,
            contentType: "application/x-www-form-urlencoded; charset=utf-8"
        }).success(function(data) {
            $("#key").val("");
            $("#value").val("");
            //TODO: UPDATE TABLE IF NEEDED WHEN POSTING Dx
            // if key in table table.key.val(key)
        }).error(function(data) {
            robot.error("Failure to post data.");
        });
    });

    robot.elements.say.click(function(e) {
        e.preventDefault();

        var value = $(".js-speech-text");

        var request_data = {
            "speech_text": value.val()
        };

        $.ajax({
            type: "POST",
            url: robot.urls.speech,
            data: JSON.stringify(request_data),
            contentType: "application/json"
        }).success(function(data) {
            value.val("");
        }).error(function(data) {
            robot.error("Failure to post data");
        });
    });

    robot.elements.write.click(function() {
        console.log("Write button not implemented");
    });

    robot.elements.chat_input.keyup(function(e) {
        if (e.keyCode == 13) {
            var text = $(this).val();
            var indicator = $(this).parent().find(".fa");
            robot.respond(text, indicator);
            $(this).val("").focus();
        }
    });

    robot.elements.capture_photo.click(function() {
        robot.snapshot();
    });

    robot.elements.rotate_head.on("input change", function(e) {
        // Display the value of the slider
        var input = $(this);
        var value = parseInt(input.val());
        input.parent().find("output").text(value);
    }).on("input change",  $.debounce(250, function(e) {

        var input = $(this);
        var value = parseInt(input.val());
        var previous_value = input.data("previous-value");
        var json_data = {
            "rotate": value
        };

        // Do not send a request if the value has not changed
        if (value != previous_value) {
            $.ajax({
                type: "PATCH",
                url: robot.urls["api_neck"],
                data: JSON.stringify(json_data),
                contentType: "application/json"
            });
        }

        input.data("previous-value", value);

    }));

    robot.elements.angle_head.on("input change", function() {
        var input = $(this);
        var value = parseInt(input.val());

        // TODO: Send to api
    });

    $(".tabs").on("click", ".tab-title", function(event) {
        event.preventDefault();
        event.stopPropagation();

        $(this).siblings().removeClass("active");
        $(this).addClass("active");

        var id = $(this).find("a").attr("href");
        $(id).siblings().removeClass("active");
        $(id).addClass("active");
    });

    $(".js-toggle-mobile").click(function(e) {
        e.preventDefault();

        $(this).find(".fa").toggleClass("fa-spin");
        robot.mobile = !robot.mobile;
    });
}
