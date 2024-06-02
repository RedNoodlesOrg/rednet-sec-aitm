var socket = io();

socket.on('connect', function () {
    console.log('WebSocket connected');
});

socket.on('initial_logs', function (logs) {
    var logList = document.getElementById('logList');
    logs.forEach(function (log) {
        var listItem = document.createElement('li');
        listItem.textContent = log;
        logList.appendChild(listItem);
    });
});

socket.on('new_log', function (log) {
    var logList = document.getElementById('logList');
    var listItem = document.createElement('li');
    listItem.textContent = log;
    logList.appendChild(listItem);
});
