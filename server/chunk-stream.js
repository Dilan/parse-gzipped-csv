var http = require('http');
var fs = require('fs');
var chunkingStreams = require('chunking-streams');

var LineCounter = chunkingStreams.LineCounter;
var SeparatorChunker = chunkingStreams.SeparatorChunker;
var SizeChunker = chunkingStreams.SizeChunker;

var port = process.argv[2] || 1337;
console.log('Start listen port', port);

http.createServer(function (req, res) {
    var input = fs.createReadStream(__dirname + '/data/test.csv.gz');
    var chunker = new SizeChunker({ chunkSize: 512 });

    /* var output = fs.createWriteStream(__dirname + '/../data/output.csv.gz'); */
    chunker.on('chunkStart', function(id, done) {
        done();
    });
    chunker.on('chunkEnd', function(id, done) {
        done();
    });

    chunker.on('end', function(chunk) {
        // emulate 3 sec timeout
        setTimeout(function() {
            res.end();
        }, 3000);
    });

    chunker.on('data', function(chunk) {
        res.write(chunk.data)
    });

    input.pipe(chunker);

}).listen(port);
