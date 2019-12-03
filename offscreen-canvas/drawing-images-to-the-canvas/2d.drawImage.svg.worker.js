// DO NOT EDIT! This test has been generated by tools/gentest.py.
// OffscreenCanvas test in a worker:2d.drawImage.svg
// Description:drawImage() of an SVG image
// Note:

importScripts("/resources/testharness.js");
importScripts("/2dcontext/resources/canvas-tests.js");

var t = async_test("drawImage() of an SVG image");
var t_pass = t.done.bind(t);
var t_fail = t.step_func(function(reason) {
    throw reason;
});
t.step(function() {

var offscreenCanvas = new OffscreenCanvas(100, 50);
var ctx = offscreenCanvas.getContext('2d');

var promise = new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/images/green.svg');
    xhr.responseType = 'blob';
    xhr.send();
    xhr.onload = function() {
        resolve(xhr.response);
    };
});
promise.then(function(response) {
    ctx.drawImage(response, 0, 0);
    _assertPixelApprox(offscreenCanvas, 50,25, 0,255,0,255, "50,25", "0,255,0,255", 2);
}).then(t_pass, t_fail);

});
done();
