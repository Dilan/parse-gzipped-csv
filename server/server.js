var zlib = require('zlib');
var http = require('http');

var chunk;
zlib.gzip(new Buffer(
    'line1----------------------------------------------------------\n' +
    'line2----------------------------------------------------------\n' +
    'line3----------------------------------------------------------\n'
), function(err, data){
    chunk = data;
});

var port = process.argv[2] || 1337;
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html', 'Content-Encoding': 'gzip'});

    setTimeout(function() {
        res.write(chunk);
    }, 1000);

    setTimeout(function() {
        res.end();
    }, 2000);

}).listen(port);

console.log('Start listen port', port);
