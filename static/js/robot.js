window.Robot = window.Robot || {};

var Robot = function() {
    this.activate();
    this.addEvents();
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
        var template = $('<div class="alert alert-warning">' + error +
        '<span class="js-dismiss close"></span></div>');
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
        this.elements.session_log.append($('<div class="text"></div>').text(data.response));
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
        data: JSON.stringify({text: text})
    }).done(function(data) {
        robot.updateSessionLog(data);
        container.html(origional);
    });
}

Robot.prototype.loadSensorData = function() {
    var robot = this;
    $.ajax({
        type: "GET", 
        url: robot.urls.arduino_ip, 
        data: { get_param: "value" }, 
        dataType: 'json'
    }).success(function(data) {
        $.each(data, function(index, element) {
            $(".sensorValues").append("<tr><td>" + index + "</td><td>" + element + "</td></tr>");
        });
        $(".filter").removeClass("hide");
    }).error(function() {
        robot.error("Arduino api is unavailable");
    });
}

Robot.prototype.renderLimbControl = function(container, limb) {

    $(container).html("");

    var template = $('<li class="list-group-item"></li>');

    var renderable_types = ["elbow", "shoulder", "wrist", "hip", "knee", "ankle"];
    for (var section in limb) {
        if ($.inArray(section, renderable_types) > -1) {

            var row = template.clone();

            //console.log(section, limb[section].joint_type);

            var control = $('<div><label></label><input type="number" min="0" max="100"></div>');
            control.find("label").text(section);
            control.find("input").val(limb[section].angle);
            control.find("input").data("url", limb[section].href);
            row.append(control);

            $(container).append(row);
        }
    }

    var robot = this;
    control.on("input", "input", function() {
        var value = $(this).val();
        value = { "angle": value };
        var data = $(this).data();

        $.ajax({
            type: "PATCH",
            url: data.url,
            data: JSON.stringify(value),
            contentType: "application/json"
        }).error(function() {
            robot.error("Unable to update limb field");
        });
    });
}

Robot.prototype.renderLimb = function(data, key, classes) {
    for (var i = 0; i < data[key].length; i++) {
        var limb = data[key][i];
        this.renderLimbControl(classes[i], limb);
    }
}

Robot.prototype.activate = function() {
    this.urls["api_settings"] = "/api/settings/";
    this.urls["api_chat"] = "/api/chat/";
    this.urls["api_legs"] = "/api/legs/";
    this.urls["api_arms"] = "/api/arms/";
    this.urls["api_listening"] = "/api/settings/listening";
    this.urls["terminate"] = "/api/terminate/";
    this.urls["camera_image_url"] = "";
    this.urls["ardunio_ip"] = "http://0.0.0.1/";

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
}

Robot.prototype.addEvents = function() {
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

    robot.elements.say.click(function() {
        var key = "say";
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
        }).error(function(data) {
            robot.error("Failure to post data");
        });
    });

    robot.elements.write.click(function() {
        console.log("Write button not implemented");
    });

    robot.elements.listen.click(function() {
        var control = $(this);
        var defautlText = control.html();
        control.toggleClass("btn-default btn-success");
        control.html("Listening");

        var state = control.hasClass("btn-success");

        var startListening = $.ajax({
            type: "POST",
            url: robot.urls.api_listening,
            data: JSON.stringify({listening: state})
        });

        startListening.done(function(data) {
            // TODO
        });

        startListening.error(function() {
            control.html(defautlText);
            control.toggleClass("btn-default btn-success");
            robot.error("Unable to set listening state to " + state);
        });
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

    robot.elements.rotate_head.on("input change", function() {
        var input = $(this);
        var value = parseInt(input.val());

        // Display the value of the slider
        input.parent().find("output").text(value);

        // TODO: Send to api
    });

    robot.elements.angle_head.on("input change", function() {
        var input = $(this);
        var value = parseInt(input.val());

        // TODO: Send to api
    });

    $(".js-camera-url").on("change", function() {
        robot.urls["camera_image_url"] = $(this).val();

        // TODO: GET THE DATA
        var data = {};

        $.ajax({
            type: "PUT",
            url: robot.urls.api_settings,
            data: JSON.stringify(data),
            contentType: "application/json"
        }).error(function() {
            robot.error("Error updating settings");
        });
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
