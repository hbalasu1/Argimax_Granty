var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io').listen(server);
server.listen(3000,function(){
 console.log('Server Running @ Port 3000');
});

app.use(express.static(__dirname + '/'));

var groveSensor = require('jsupm_grove');
var UVSensor = require('jsupm_guvas12d');
var temp = new groveSensor.GroveTemp(0);
var light = new groveSensor.GroveLight(2);
var myUVSensor = new UVSensor.GUVAS12D(3);
console.log(temp.name());
console.log(light.name());

// analog voltage, usually 3.3 or 5.0
var g_GUVAS12D_AREF = 5.0;
var g_SAMPLES_PER_QUERY = 1024;

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

function roundNum(num, decimalPlaces)
{
	var extraNum = (1 / (Math.pow(10, decimalPlaces) * 1000));
	return (Math.round((num + extraNum) * (Math.pow(10, decimalPlaces))) / Math.pow(10, decimalPlaces));
}

io.on('connection',function(sock){
        setInterval(function() {
        var celcius = temp.value() + 10;
		var lux = light.value();
        var date = new Date().getTime();
		var uv = roundNum(myUVSensor.value(g_GUVAS12D_AREF, g_SAMPLES_PER_QUERY), 6);
        sock.emit('temperatureUpdate', date, celcius, lux, uv);
        }, 5000);
});
