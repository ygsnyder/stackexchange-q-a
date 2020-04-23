var LintStream = require('jslint').LintStream;
const fs = require('fs');
const util = require('util');


var options = {
    "edition" : "latest",
    "length" : 100
},

l = new LintStream(options);

var fileName = 'Output.js';
var fileContents = fs.readFileSync('./Output.txt').toString();
// console.log(new Buffer(fileContents).toString("ascii"));
count = 1;
fileContents.split('\n').forEach((line)=>{
    l.write({file: fileName, body: line});   
})

l.on('data', function (chunk, encoding, callback) {
    // chunk is an object
    // chunk.file is whatever you supplied to write (see above)
    // assert.deepEqual(chunk.file, fileName);

    // chunk.linted is an object holding the result from running JSLint
    // chunk.linted.ok is the boolean return code from JSLINT()
    // chunk.linted.errors is the array of errors, etc.
    // see JSLINT for the complete contents of the object

        fs.appendFileSync('./lintedErrors.txt', `line: ${count},\n`, {'flags': 'a'});
        fs.appendFileSync('./lintedErrors.txt', util.inspect(chunk.linted.errors), {'flags': 'a'});
        fs.appendFileSync('./lintedErrors.txt', ',\n', {'flags': 'a'});
        count++;
    
});





