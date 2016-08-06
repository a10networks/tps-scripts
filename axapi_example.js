#!/usr/bin/env node

// Eric Chou ericc@a10networks.com
// Node.js v6.3.1, NPM request v2.74.0
// For demo, rough around the edges

var request = require('request');

// Set the headers
var headers = {
    'Content-Type': 'application/json'
}

// Configure the request
var options = {
    url: 'https://192.168.199.152/axapi/v3/auth/',
    method: 'POST',
    headers: headers,
    rejectUnauthorized: false,
    json: {"credentials":{"username": "admin", "password": "a10"}}
}

// 1. Authorized for signature via HTTPS
// 2. Using common headers, endpoints, and POST Body to make changes
// 3. Save changes and log out

function requestCallback(error, response, body) {

    if (!error && response.statusCode == 200) {
        var signature = body['authresponse']['signature'];
        console.info("Signature for session: ", signature);

        // All operations from here on out should have the common headers
        var common_headers = {'Content-Type': 'application/json', 'Authorization': 'A10 ' + signature}

        // Example for show version GET
        var options = {
            url: 'https://192.168.199.152/axapi/v3/version/oper',
            method: 'GET',
            headers: common_headers,
            rejectUnauthorized: false,
        }

        // Start the request for show version
        request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body);
            }
        })

        // Example for POST to change hostname
        var options = {
            url: 'https://192.168.199.152/axapi/v3/hostname/',
            method: 'POST',
            headers: common_headers,
            rejectUnauthorized: false,
            json: {"hostname": {"value":"TH4435-New"}}
        }

        request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body);
            }
        })

        // Save and Exit
        var options = {
            url: 'https://192.168.199.152/axapi/v3/write/memory/',
            method: 'POST',
            headers: common_headers,
            rejectUnauthorized: false,
        }

        request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body);
            }
        })

        var options = {
            url: 'https://192.168.199.152/axapi/v3/logoff',
            method: 'POST',
            headers: common_headers,
            rejectUnauthorized: false,
        }

        request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body);
            }
        })

    }
    else {
        console.log("error: " + error)
        console.log("response.statusCode: " + response.statusCode)
        console.log("response.statusText: " + response.statusText)
        console.log(body)
    }
}

// Start the request for main loop
request(options, requestCallback);




