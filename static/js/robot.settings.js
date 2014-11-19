/*window.Robot = window.Robot || {};

Robot = Robot || {};

var Settings = function() {

}

Settings.prototype.

Robot.Settings = Settings;*/

function renderBooleanInput(key, value) {
    var control = $('<div class="checkbox"></div>');
    var label = $('<label></label>');
    var input = $('<input type="checkbox">');
    var text = $('<span></span>');

    var caption = key[0].toUpperCase() + key.slice(1);
    caption = caption.replace("_", " ");

    text.text(caption);

    control.append(label);
    control.append(input);
    control.append(text);

    if (value) {
        input.attr("checked", true);
    }

    $(".js-settings-form").append(control);

    input.on("change", function() {
        // TODO: Save the value in the api
        // TODO: Revert the value if there is an error saving
    });
}

function renderStringInput(key, value) {
    var control = $('<div class="form-group"></div>');
    var label = $('<label></label>');
    var input = $('<input type="text" class="form-control">');

    var caption = key[0].toUpperCase() + key.slice(1);
    caption = caption.replace("_", " ");

    label.text(caption);

    control.append(label);
    control.append(input);

    input.val(value);

    $(".js-settings-form").append(control);

    input.on("change", function() {
        // TODO: Save the value in the api
        // TODO: Revert the value if there is an error saving
    });
}

function renderObjectInput(key, value) {
    var control = $('<div class="form-group"></div>');
    var label = $('<label></label>');
    var input = $('<textarea class="form-control" disabled></textarea>');

    var caption = key[0].toUpperCase() + key.slice(1);
    caption = caption.replace("_", " ");

    label.text(caption);

    control.append(label);
    control.append(input);

    input.val(JSON.stringify(value));

    $(".js-settings-form").append(control);

    input.on("change", function() {
        // TODO: Save the value in the api
        // TODO: Revert the value if there is an error saving
    });
}

function renderControl(key, value) {
    var type = typeof(value);

    if (type === "boolean") {
        renderBooleanInput(key, value);
    } else if (type === "string") {
        renderStringInput(key, value);
    } else {
        renderObjectInput(key, value) 
    }
}

$.ajax({
    type: "GET",
    url: robot.urls.api_settings
}).success(function(data) {
    for (key in data) {
        renderControl(key, data[key]);
    }

    robot.urls["camera_image_url"] = data.camera_image_url;
    robot.urls["arduino_ip"] = data.arduino_ip;

    $(".js-camera-url").val(robot.urls.camera_image_url);
    $(".js-arduino-url").val(robot.urls.arduino_ip);
    robot.loadSensorData();
}).error(function() {
    robot.error("Unable to load settings");
});
