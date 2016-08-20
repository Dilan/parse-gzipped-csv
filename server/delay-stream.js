var zlib = require('zlib');
var http = require('http');
var fs = require('fs');
var delay = require('delay-stream');

// read CSV --> gzip --> pipe to stream after 1 second
var port = process.argv[2] || 1337;
http.createServer(function (req, res) {
    res.writeHead(200, { 'Content-Encoding': 'gzip' });
    fs.createReadStream(__dirname + '/data/test.csv').pipe(zlib.createGzip()).pipe(delay(1000)).pipe(res);

}).listen(port);

console.log('Start listen port:', port);