/*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
*/
var app = {
    // Application Server
    // SERVER: 'http://192.168.1.11',
    SERVER: 'https://smart-home-inventory.herokuapp.com',
    API_PATH: '/api/v1',
    
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        $(document).on('submit', '#api', function(e){
            e.preventDefault();
            var uri = app.API_PATH + "/product/" + $(this).find("input[name='barcode']").val()
            app.httpAction(uri, app.onProductUpdate, null, 'PUT', $(this).serialize());
        });
        $(document).on('click', '#cancel', function(e){
            app.receivedEvent('authorized');
        });
        app.receivedEvent('ready');
    },
    
    // Update DOM on a Received Event
    receivedEvent: function(state, html=null) {
        var parentElement = document.getElementById('content');
        var preLoadElement = parentElement.querySelector('.pre-load');
        var preLoginElement = parentElement.querySelector('.pre-login');
        var postLoginElement = parentElement.querySelector('.post-login');
        var dynamicElement = parentElement.querySelector('.dynamic-content');

        if (state == 'ready') {
            preLoadElement.setAttribute('style', 'display:none;');
            postLoginElement.setAttribute('style', 'display:none;');
            preLoginElement.setAttribute('style', 'display:block;');

        } else if (state == 'authorized') {
            preLoadElement.setAttribute('style', 'display:none;');
            postLoginElement.setAttribute('style', 'display:block;');
            preLoginElement.setAttribute('style', 'display:none;');
            dynamicElement.setAttribute('style', 'display:none;');
        } else if (state == 'product') {
            $('#dynamic').html(html);
            postLoginElement.setAttribute('style', 'display:none;');
            dynamicElement.setAttribute('style', 'display:block;');
        }
    },

    htmlHandler: function (results) {
        app.receivedEvent(results.landing, results.data);
    },

    barcodeHandler: function(code, landing) {
        switch (landing) {
            case "stock":
            title = "New Product";
            uri = "/";
            msg = "Enter Quantity";
            buttons = ['Add', 'Cancel'];
            app.httpAction(app.API_PATH + '/product/' + code, function(res) {
                if (res.data.is_present === true) {
                    title = res.data.name + ' (' + res.data.measurement + ')';
                    buttons = ['Remove', 'Cancel', 'Add'];
                    msg = msg + ' (' + res.data.stock + ' available)';
                }
                    
                navigator.notification.prompt(
                    msg,                   // message
                    function(r) {
                        if (res.data.is_present === true) {
                            if (r.buttonIndex === 1) {        // remove
                                uri = app.API_PATH + "/stock/remove";
                            } else if (r.buttonIndex === 3) { // add
                                uri = app.API_PATH + "/stock/add"                			
                            } else {  // cencel
                                return;
                            }
                        } else if (r.buttonIndex === 1) {        // add new product
                            app.httpAction('/product/' + code + '?app=1&stock=' +
                                           r.input1, app.htmlHandler, 'product');
                            return;
                        } else {  // cencel
                            return;
                        }	   

                        data = {barcode: code, quantity: r.input1};
                        app.httpAction(uri, app.onStockUpdate, null, 'POST', data);
                    },
                    title,      // title
                    buttons,    // buttonLabels
                    '1'         // defaultText
                );
            });
            break;

            case "profile":
            break;

            case "query":
            app.httpAction(app.API_PATH + '/product/' + code, function(res) {
                title = res.data.name + ' (' + res.data.measurement + ')';
                if (res.data.is_present === true) {
                    navigator.notification.alert(
                        'Brand: ' + res.data.brand + '\nStock: ' + res.data.stock, // message
                        null,
                        title,             // title
                        'Ok'                           // buttonName
                    );
                }
            });
            break;

            case "product":
            app.httpAction('/product/' + code + '?app=1', app.htmlHandler, landing);
            break;

            case "report":
            break;

            default:
            break;
        }			
    },

    onProductUpdate: function (results) {
        if (results.data.status === 'OK') {
            if (results.data.is_present === true) {
                var msg = 'Product Updated Successfully!';
            } else {
                var msg = 'Product Added Successfully!';
            }
            navigator.notification.alert(
                msg,                           // message
                null,
                results.data.name,             // title
                'Ok'                           // buttonName
            );
            app.receivedEvent('authorized');
        } else {
            navigator.notification.beep();
            navigator.notification.alert(
                results.data.error,         // message
                null,
                'Could not add product!',  // title
                'Ok'                        // buttonName
            );
        }          
    },

    onStockUpdate: function (results) {
        if (results.data.status !== 'OK') {
            navigator.notification.alert(
                results.data.error,         // message
                'Could not modify stock!',  // title
                'OK'                     // buttonName
            );
        } else {
            navigator.notification.beep();
            app.scanBarcode();
        }          
    },

    stock: function() {
        app.scanBarcode('stock');
    },

    product: function() {
        app.scanBarcode('product');
    },

    report: function() {
        app.scanBarcode('report');
    },

    profile: function() {
        app.scanBarcode('profile');
    },

    query: function() {
        app.scanBarcode('query');
    },

    scanBarcode: function(landing) {
        cordova.plugins.barcodeScanner.scan(
            function (result) {
                if (result.cancelled == true) {
                    return null;
                } else {
                    app.barcodeHandler(result.text, landing);
                }
            },
            function (error) {
                alert("Scanning failed: " + error);
                return null;
            },
            {
                preferFrontCamera : false, // iOS and Android
                showFlipCameraButton : false, // iOS and Android
                showTorchButton : true, // iOS and Android
                torchOn: false, // Android, launch with the torch switched on (if available)
                saveHistory: false, // Android, save scan history (default false)
                prompt : "Place a barcode inside the scan area", // Android
                resultDisplayDuration: 0, // Android, display scanned text for X ms. 0 suppresses it entirely, default 1500
                formats : "QR_CODE,UPC_A,UPC_E,EAN_8,EAN_13", // default: all but PDF_417 and RSS_EXPANDED
                orientation : "portrait", // Android only (portrait|landscape), default unset so it rotates with the device
                disableAnimations : true, // iOS
                disableSuccessBeep: false // iOS and Android
            }
        );
    },

    authorize: function (pin) {
        $.ajax({
            type: "GET",
            url: app.SERVER + app.API_PATH + '/auth/' + pin,
            dataType: "json",
            /* data: {identity: <username from form>, password: <password from form>}, */
            success: function(data) {
                if (data.status == "OK") {
                    app.receivedEvent('authorized');
                }
            },
            error: function(e) {
                alert('Error: ' + e.status);
            }
        });
    },

    httpAction: function (resource, callback, landing=null, method = 'GET', data = null) {
        datatype = "json";
        if (resource.indexOf(app.API_PATH) === -1) {
            datatype = "html";
        }

        $.ajax({
            type: method,
            url: app.SERVER + resource,
            dataType: datatype,
            data: data,
            success: function(data) {
                if (callback != null) {
                    var resp = new Object();
                    resp.data = data;
                    resp.landing = landing;
                    callback(resp);
                }
            },
            error: function(e) {
            alert('Error: ' + e.status);
            }
        });
    }
};