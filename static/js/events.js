var robot = new Robot();
robot.renderStatus();

var slideout = new Slideout({
    'panel': document.getElementById('panel'),
    'menu': document.getElementById('menu'),
    'padding': 256,
    'tolerance': 70
});
$(".toggle-menu").click(function() {
    slideout.toggle();
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

$("#write").click(function() {
    console.log("Write button not implemented");
});

$(".js-speech-text").keypress(function(e) {
    if(e.which == 13) {
        e.preventDefault();
        say();
    }
});

$(".js-capture-photo").click(function() {
    robot.snapshot();
});

$(".js-terminate").click(function() {
    robot.terminate();
});

$(".error-list").on("click", ".js-dismiss", function() {
    $(this).parents(".alert").remove();
    robot.error();
});

$("js-dismiss-all").click(function() {
    $(".error-list .alert").remove();
    robot.error();
});

$("#post").click(function() {
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

$("#say").click(function(e) {
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
        robot.error("Failed to post data");
    });
});

$(".chat-input").keyup(function(e) {
    if (e.keyCode == 13) {
        var text = $(this).val();
        var indicator = $(this).parent().find(".fa");
        var session_log = $(".chat-log");
        robot.respond(text, session_log, indicator);
        $(this).val("").focus();
    }
});

$(".js-rotate-head").on("input change", function(e) {
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

$(".js-angle-head").on("input change", function() {
    var input = $(this);
    var value = parseInt(input.val());

    // TODO: Send to api
});
