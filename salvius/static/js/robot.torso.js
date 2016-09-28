window.Robot = window.Robot || {};

var Robot = Robot || {};



var joystick = new VirtualJoystick({
    mouseSupport: true,
    limitStickTravel: true,
    stickRadius: 50
});

animate();

function animate() {

    requestAnimationFrame(animate);

    if (joystick.right()) {
        console.log('right');
    }
    if (joystick.left()) {
        console.log('left');
    }
    if (joystick.up()) {
        console.log('up');
    }
    if (joystick.down()) {
        console.log('down');
    }
}
