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
				URI: 'http://192.168.1.11/api/v1',
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
        app.receivedEvent('ready');
    },
    // Update DOM on a Received Event
    receivedEvent: function(state) {
      var parentElement = document.getElementById('content');
      var preLoadElement = parentElement.querySelector('.pre-load');
      var preLoginElement = parentElement.querySelector('.pre-login');
      var postLoginElement = parentElement.querySelector('.post-login');
          
      if (state == 'ready') {
          preLoadElement.setAttribute('style', 'display:none;');
          postLoginElement.setAttribute('style', 'display:none;');
          preLoginElement.setAttribute('style', 'display:block;');
          
      } else if (state == 'authorized') {
          preLoadElement.setAttribute('style', 'display:none;');
          postLoginElement.setAttribute('style', 'display:block;');
          preLoginElement.setAttribute('style', 'display:none;');
      }
    },
    
    htmlHandler: function(source, data) {
    				alert(data);
    },
    
    jsonHandler: function(msg) {
    				alert(msg.resource);
    				alert(msg.data.status);
    				navigator.notification.alert(msg.resource);
    },
    
    add: function() {
    					app.scanBarcode('/stock/add');
    },
    
    remove: function() {
    					resp = app.scanBarcode('/stock/remove');
    },
    
    manage: function() {
    					upc = app.scanBarcode(null);
    },
    
    query: function() {
    					upc = app.scanBarcode(null);
    },
    
    scanBarcode: function(uri, json = true) {
        cordova.plugins.barcodeScanner.scan(
            function (result) {
            				if (result.cancelled == true) {
            								return null;
            				} else if (json == false) {
            								app.httpHandler(uri, result.text)
            				} else {
            								data = {barcode: result.text, quantity: 1};
            								app.httpAction(uri, 'POST', data, app.jsonHandler);
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
        url: app.URI + '/auth/' + pin,
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
    
    httpAction: function (resource, method = 'GET', data = null, callback = null) {
      $.ajax({
        type: method,
        url: app.URI + resource,
        dataType: "json",
        data: data,
        success: function(data) {
          if (callback != null) {
          				var resp = new Object();
          				resp.data = data;
          				resp.resource = resource;
          				callback(resp);
          }
        },
        error: function(e) {
          alert('Error: ' + e.status);
        }
      });
    }
};