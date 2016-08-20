var http = require('http');
var zlib = require('zlib');

var url = process.argv[2]

http.get(url, function(res) {
    var gunzip = zlib.createGunzip();
    res.pipe(gunzip); //pipe to ungzip stream

    // save file
    res.pipe(require('fs').createWriteStream(__dirname + '/tmp/result-v1.csv.gz'));
    // ungzip to CSV and save file
    gunzip.pipe(require('fs').createWriteStream(__dirname + '/tmp/result-v2.csv'));


    var chunks = [];
    res.on('data', function(data) {
        console.log('chunk income ...');
        chunks.push(chunks);
    });
    res.on('end', function() {
        chunks.forEach(function(buffer) {
            zlib.gunzip(buffer, function(err, decoded) {
                console.log('Ungzip:');
                console.log(decoded.toString());
            });
        });

        /*
        var buffer = Buffer.concat(chunks);
        zlib.gunzip(buffer, function(err, decoded) {
            console.log(decoded.toString());
        });
        */
    });

    gunzip.on('data', function(data) {
        console.log('gunzip.on data');
        console.log(data.toString());

    }).on("end", function() {
        console.log('gunzip finish.');

    }).on("error", function(err) {
        console.log('Error', err);
    });
});
