var socket = io();

socket.on('connect', function () {
    console.log('WebSocket connected');
});

socket.on('new_event', function (log) {
    console.log(log);
});
