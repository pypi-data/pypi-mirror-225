/**
 * Module for gRPC Telemetry web UI.
 */
let grpctelemetry = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        listenIp: "#ys-listen-ip",
        listenPort: "#ys-listen-port",
        outputArea: "#ys-telemetry-output",
        tlsDeviceChkBox: "#ys-tls-device",

        localGetUri: '/grpctelemetry/servicer/output',
        localStartUri: '/grpctelemetry/servicer/start',
        localStopUri: '/grpctelemetry/servicer/',
        servicerListUri: '/grpctelemetry/servicer/list',
        outputConfigUri: "/grpctelemetry/servicer/config",
        primaryIPUri: "/grpctelemetry/servicer/ip",
    };

    let c = config;     // internal alias for brevity

    let state = {
        updater: null
    }

    function addOutput(input, output, indent=0) {
        if (Array.isArray(input)) {
            for (let obj of input) {
                output = addOutput(obj, output, 2);
            }
        } else if (typeof input == 'object') {
            for (let key of Object.keys(input)) {
                if (Array.isArray(input[key])) {
                    for (let obj of input[key]) {
                        output = addOutput(obj, output, 2);
                    }
                } else {
                    for (let i = indent; i > 0; i--) {
                        output += " ";
                    }
                    output += key + ':  ' + input[key] + "\n";
                }
            }
        } else {
            for (let i = indent; i > 0; i--) {
                output += " ";
            }
            output += input + "\n";
        }

        return output;
    }

    /**
     * Function: getOutPut
     *
     * Interval function to display servicer(s) output.
     */
    function getOutput() {
        $.getJSON(c.localGetUri, function(data) {
            if (data.output.length == 0) {
                return;
            }
            let output = '<pre>';
            for (let block of data.output) {
                output = addOutput(block, output);
                $("#ys-grpc-output").prepend(output += '</pre>');
                output = '<pre>';
            }
            // Prevent taking too much browser memory.
            while ($("#ys-grpc-output").children().length > 50) {
                $("#ys-grpc-output").children().last().remove();
            }
        }).fail(function(retObj) {
            alert(retObj.statusText);
        });
    }

    /**
     * startListening
     *
     * @param {string} secure device that contains server certificate/key.
     */
    function startListening(secure) {
        let port = $(c.listenPort).val();
        let address = $(c.listenIp).val()
        if (!port) {
            port = alert("Enter TCP port to listen on.");
            return;
        }
        getPromise(c.localStartUri, {address: address, port: port, secure: secure})
            .then(function(retObj) {
                alert(retObj.message);
                if (!retObj.result) {
                    return;
                }
                if (!state.updater) {
                    state.updater = setInterval(getOutput, 250);
                }
            }).fail(function(retObj) {
                alert(retObj.statusText);
            });
    };

    /**
     * stopListening
     *
     * @param {string} port to stop listening on.
     */
    function stopListening(port) {
        const stopUri = c.localStopUri + port + '/stop'
        getPromise(stopUri)
            .then(function(retObj) {
                alert(retObj.message);
                getServicers();
            }).fail(function(retObj) {
                alert(retObj.statusText);
            });
    };

    /**
     * getServicers
     *
     * Pop up dialog with table of active servisers which
     * users can choose to stop specific servisers.
     */
    function getServicers() {
        getPromise(c.servicerListUri)
        .then(function(retObj) {
            if (retObj.servers.length == 0) {
                alert("No live receivers");
                if (state.updater) {
                    clearInterval(state.updater);
                    state.updater = null;
                }
                return;
            }
            if (retObj.servers.length > 0 && !state.updater) {
                state.updater = setInterval(getOutput, 250);
            }
            let fileOut = retObj.fileout;
            let uriOut = retObj.uri;
            let table = '<table class="grpc-config"><th>IP Address</th><th>Port</th>';
            table += '<th>TLS</th>';
            for (let s of retObj.servers) {
                table += "<tr><td readonly>" + s[0] + "</td>";
                table += "<td readonly>" + s[1] + "</td>";
                table += "<td readonly>" + s[2] + "</td>";
                table += '<td><button "btn btn--small btn--primary"' + ' port=' + s[1];
                table += ' class="ys-server-stop">Stop</button></td>';
            }
            table += '<div class="row"><label><strong>Output file</strong></label></div>';
            table += '<div class="row"><input size="60" id="ys-output-file" value="'+ fileOut;
            table += '" placeholder="File path for telemtry output."/></div><hr>';
            table += '<div class="row"><lable><strong>Elasticsearch Output URI</strong></label></div>';
            table += '<div class="row"><input size="60" id="ys-output-uri" value="'+ uriOut;
            table += '" placeholder="example: http//localhost:9200"/></div><hr>';
            table += '<button "btn btn--small btn--primary" ';
            table += 'id="ys-output-config">Set Output(s)</button><hr>';

            $("#ys-servers-dialog").dialog({
                title: "Telemetry Receivers",
                width: "auto",
                height: "auto",
                buttons: {
                    "Exit": function () {
                        $(this).dialog("close");
                    }
                }
            }).html(table);
            $("#ys-servers-dialog").dialog("open");
            $(".ys-server-stop").click(function(){
                let port = $(this).attr("port");
                stopListening(port);
                $("#ys-servers-dialog").dialog("close");
            });
            $("#ys-output-config").click(function(){
                let port = $(this).attr("port");
                let file = $("#ys-output-file").val();
                let uri = $("#ys-output-uri").val();
                $("#ys-servers-dialog").dialog("close");
                outputConfig(port, file, uri);
            });
        }).fail(function(retObj) {
            alert(retObj.statusText);
        });
    }

    /**
     * checkServicers
     *
     * When navigating back and forth to the grpc telemetry page, make
     * sure any live servicers continue streaming data to the web page.
     */
     function checkServicers() {
        getPromise(c.servicerListUri)
        .then(function(retObj) {
            if (retObj.servers.length > 0 && !state.updater) {
                state.updater = setInterval(getOutput, 250);
            }
        }).fail(function(retObj) {
            alert(retObj.statusText);
        });
    }

    function outputConfig(port, file, uri) {
        let outputCfg = {
            port: port,
            file: file,
            uri: uri,
        }
        getPromise(c.outputConfigUri, outputCfg)
        .then(function(retObj) {
            getServicers();
        })
        .fail(function(retObj) {
            alert(retObj.statusText);
        });
    }

    function getPrimaryIP() {
        getPromise(c.primaryIPUri)
        .then(function (retObj) {
            let address = retObj.address;
            if (address) {
                $(c.listenIp).val(address);
            }
        })
    }

    /**
     * Public API.
     */
    return {
        config:config,
        startListening: startListening,
        getServicers: getServicers,
        checkServicers: checkServicers,
        getPrimaryIP: getPrimaryIP,
    };
}();
