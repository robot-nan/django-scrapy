// (function(){if(!window.TradingView){var e={version:function(){return"0.8 dev"},gEl:function(a){return document.getElementById(a)},gId:function(){return"tradingview_"+(1048576*(1+Math.random())|0).toString(16).substring(1)},onready:function(a){window.addEventListener?window.addEventListener("DOMContentLoaded",a,!1):window.attachEvent("onload",a)},css:function(a){var b=document.getElementsByTagName("head")[0],d=document.createElement("style");d.type="text/css";d.styleSheet?d.styleSheet.cssText=a:(a=
//     document.createTextNode(a),d.appendChild(a));b.appendChild(d)},bindEvent:function(a,b,d){a.addEventListener?a.addEventListener(b,d,!1):a.attachEvent&&a.attachEvent("on"+b,d)},unbindEvent:function(a,b,d){a.removeEventListener?a.removeEventListener(b,d,!1):a.detachEvent&&a.detachEvent("on"+b,d)},widget:function(a){this.id=e.gId();var b=e.getUrlParams().symbol||a.symbol||"FX:SPX500";if(!a.datafeed)throw"Datafeed is not defined";this.options={width:a.width||800,height:a.height||500,symbol:b,interval:a.interval||
// "1",timezone:a.timezone||"",autosize:a.autosize,container:a.container_id||"",toolbar_bg:a.toolbar_bg||"f4f7f9",studies:a.studies||[],theme:a.theme||"",widgetbar_width:+a.widgetbar_width||void 0,datafeed:a.datafeed,path:a.library_path,enabledStudies:a.enabled_studies||[],enabledDrawings:a.enabled_drawings||[],disabledDrawings:a.disabled_drawings||[],savedData:a.savedData||void 0,locale:a.locale,overrides:a.overrides||{}};if(a.news&&a.news.length){this.options.news_vendors=[];for(b=0;b<a.news.length;b++)switch(a.news[b]){case "headlines":case "stocktwits":this.options.news_vendors.push(a.news[b])}this.options.news_vendors||
// delete this.options.news_vendors}isFinite(a.widgetbar_width)&&0<a.widgetbar_width&&(this.options.widgetbar_width=a.widgetbar_width);this._ready_handlers=[];this.create()}};e.widget.prototype={_messageTarget:function(){return e.gEl(this.id).contentWindow},create:function(){var a=this.render(),b=this,d;this.options.container?e.gEl(this.options.container).innerHTML=a:document.write(a);d=e.gEl(this.id);this.postMessage=e.postMessageWrapper(d.contentWindow,this.id);e.bindEvent(d,"load",function(){b.postMessage.get("widgetReady",
//     {},function(){var a;b._ready=!0;for(a=b._ready_handlers.length;a--;)b._ready_handlers[a].call(b);b.postMessage.post(d.contentWindow,"initializationFinished")})})},render:function(){window.Datafeed=this.options.datafeed;var a=(this.options.path||"")+"static/tv-chart.html?localserver=1&symbol="+encodeURIComponent(this.options.symbol)+"&interval="+encodeURIComponent(this.options.interval)+"&toolbarbg="+this.options.toolbar_bg.replace("#","")+(this.options.widgetbar_width?"&widgetbarwidth="+this.options.widgetbar_width:
//         "")+(this.options.studies?"&studies="+encodeURIComponent(this.options.studies.join("\u001f")):"")+(this.options.theme?"&theme="+encodeURIComponent(this.options.theme):"")+"&enabledStudies="+encodeURIComponent(JSON.stringify(this.options.enabledStudies))+"&enabledDrawings="+encodeURIComponent(JSON.stringify(this.options.enabledDrawings))+"&disabledDrawings="+encodeURIComponent(JSON.stringify(this.options.disabledDrawings))+"&overrides="+encodeURIComponent(JSON.stringify(this.options.overrides))+"&locale="+
//     encodeURIComponent(this.options.locale)+(this.options.timezone?"&timezone="+encodeURIComponent(this.options.timezone):"");this.options.savedData&&(window.__TVSavedChart=this.options.savedData);return'<iframe id="'+this.id+'" src="'+a+'"'+(this.options.autosize?' style="width: 100%; height: 100%;"':' width="'+this.options.width+'" height="'+this.options.height+'"')+' frameborder="0" allowTransparency="true" scrolling="no"></iframe>'},onChartReady:function(a){this._ready?a.call(this):this._ready_handlers.push(a)},
//     setSymbol:function(a,b){this.postMessage.post(this._messageTarget(),"changeSymbol",{symbol:a,interval:b})},createStudy:function(a,b){this.postMessage.post(this._messageTarget(),"createStudy",{name:a,lock:b})},createShape:function(a,b){this.postMessage.post(this._messageTarget(),"createShape",{point:a,options:b});var d=this;this.postMessage.on("onIconCreated",function(a){d.postMessage.on("onIconClicked",function(a){})})},removeIcon:function(a){},onSymbolChange:function(a){this.postMessage.on("onSymbolChange",
//         a)},onTick:function(a){this.postMessage.on("onTick",a)},remove:function(){var a=e.gEl(this.id);a.parentNode.removeChild(a)},onMarkClick:function(a){this.postMessage.on("onMarkClick",a)},onAutoSaveNeeded:function(a){this.postMessage.on("onAutoSaveNeeded",a)},save:function(a){this.postMessage.on("onChartSaved",a);this.postMessage.post(this._messageTarget(),"saveChart",{})},load:function(a){window.__TVSavedChart=a;this.remove();this.create()}};e.postMessageWrapper=function(){var a={},b={},d={},e,f=0,
//     g=0;window.addEventListener&&window.addEventListener("message",function(d){var c;try{c=JSON.parse(d.data)}catch(l){return}c.provider&&"TradingView"==c.provider&&("get"==c.type?b[c.name].call(c,c.data,function(a){e.postMessage(JSON.stringify({id:c.id,type:"on",name:c.name,client_id:c.client_id,data:a,provider:"TradingView"}),"*")}):"on"==c.type?a[c.client_id]&&a[c.client_id][c.id]&&(a[c.client_id][c.id].call(c,c.data),delete a[c.client_id][c.id]):"post"==c.type&&"function"===typeof b[c.name]&&b[c.name].call(c,
//     c.data,function(){}))});return function(h,c){a[c]={};e=d[c]=h;return{on:function(a,c){b[a]=c},get:function(b,e,k){b={id:f++,type:"get",name:b,client_id:c,data:e,provider:"TradingView"};a[c][b.id]=k;d[c].postMessage(JSON.stringify(b),"*")},post:function(a,b,c){b={id:g++,type:"post",name:b,data:c,provider:"TradingView"};a&&"function"===typeof a.postMessage&&a.postMessage(JSON.stringify(b),"*")}}}}();e.getUrlParams=function(){for(var a,b=/\+/g,d=/([^&=]+)=?([^&]*)/g,e=window.location.search.substring(1),
//                                                                                                                                                                                                                                                                                                                                                                                                                                                        f={};a=d.exec(e);)f[decodeURIComponent(a[1].replace(b," "))]=decodeURIComponent(a[2].replace(b," "));return f};window.TradingView&&jQuery?jQuery.extend(window.TradingView,e):window.TradingView=e}})();

/*
 This class implements interaction with UDF-compatible datafeed.
 Please remember this class is a separate component and may interact to other code through Datafeeds.DatafeedInterface interface functions ONLY

 See UDF protocol reference at
 https://docs.google.com/document/d/1rAigRhQUSLgLCzUAiVBJGAB7uchb-PzFVe0Bl8WTtF0
 */


Datafeeds = {};


Datafeeds.UDFCompatibleDatafeed = function(datafeedURL) {

    this._datafeedURL = datafeedURL;
    this._configuration = undefined;

    this._symbolSearch = null;
    this._symbolsStorage = null;
    this._pulseUpdater = new Datafeeds.PulseUpdater(this);

    this._enableLogging = false;
    this._initializationFinished = false;
    this._callbacks = {};

    this._initialize();
}


Datafeeds.UDFCompatibleDatafeed.prototype.on = function (event, callback) {

    if (!this._callbacks.hasOwnProperty(event)) {
        this._callbacks[event] = [];
    }

    this._callbacks[event].push(callback);
    return this;
}


Datafeeds.UDFCompatibleDatafeed.prototype._fireEvent = function(event, argument) {
    if (this._callbacks.hasOwnProperty(event)) {
        var callbacksChain = this._callbacks[event];
        for (var i = 0; i < callbacksChain.length; ++i) {
            callbacksChain[i](argument);
        }
        this._callbacks[event] = [];
    }
}


Datafeeds.UDFCompatibleDatafeed.prototype.onInitialized = function() {
    this._initializationFinished = true;
    this._fireEvent("initialized");
}



Datafeeds.UDFCompatibleDatafeed.prototype._logMessage = function(message) {
    if (this._enableLogging) {
        console.log(message);
    }
}


Datafeeds.UDFCompatibleDatafeed.prototype._initialize = function() {

    var that = this;
    $.ajax({url : this._datafeedURL + "/config", dataType : 'json'}).
    done(function(response) {
        var configurationData = response;
        that._setupWithConfiguration(configurationData);
    }).
    error(function(reason) {
        that._setupWithConfiguration({
            supports_search: false,
            supports_group_request: true
        });
    });
}


Datafeeds.UDFCompatibleDatafeed.prototype.setup = function(studyEngineOptions, callback) {

    if (this._configuration) {
        this._configuration.engine = studyEngineOptions;
        callback(this._configuration);
    }
    else {
        var that = this;
        this.on("configuration_ready", function() {
            that._configuration.engine = studyEngineOptions;
            callback(that._configuration);
        })
    }
}

Datafeeds.UDFCompatibleDatafeed.prototype.onReady = function(callback) {
    var that = this;
    if (this._configuration) {
        setTimeout(function() {
            callback(that._configuration);
        }, 0);
    } else {
        this.on('configuration_ready', function() {
            callback(that._configuration);
        });
    }
};

Datafeeds.UDFCompatibleDatafeed.prototype._setupWithConfiguration = function(configurationData) {
    this._configuration = configurationData;

    if (!configurationData.exchanges) {
        configurationData.exchanges = [];
    }

    if (!configurationData.symbolsTypes) {
        configurationData.symbolsTypes = [];
    }

    if (configurationData.supports_search == false && configurationData.supports_group_request == false) {
        throw "Unsupported datafeed configuration. Must either support search, or support group request";
    }

    if (configurationData.supports_search == false) {
        this._symbolSearch = new Datafeeds.SymbolSearchComponent(this);
    }

    if (configurationData.supports_group_request == true) {
        //	this component will call onInitialized() by itself
        this._symbolsStorage = new Datafeeds.SymbolsStorage(this);
    }
    else {
        this.onInitialized();
    }

    this._fireEvent("configuration_ready");
    this._logMessage("Initialized with " + JSON.stringify(configurationData));
}


//	===============================================================================================================================
//	The functions set below is the implementation of JavaScript API.

Datafeeds.UDFCompatibleDatafeed.prototype.getMarks = function (symbolInfo, rangeStart, rangeEnd, onDataCallback) {
}

Datafeeds.UDFCompatibleDatafeed.prototype.searchSymbolsByName = function(ticker, exchange, type, onResultReadyCallback) {
    var MAX_SEARCH_RESULTS = 30;

    if (this._configuration.supports_search) {

        $.ajax({url : this._datafeedURL + "/search?limit=" + MAX_SEARCH_RESULTS  +"&query=" + ticker + "&type=" + type + "&exchange=" + exchange, dataType : 'json'})
            .done(function (response) {
                var data = response;

                for (var i = 0; i < data.length; ++i) {
                    if (!data[i].params) {
                        data[i].params = [];
                    }
                }

                if (typeof data.s == "undefined" || data.s != "error") {
                    onResultReadyCallback(data)
                }
                else {
                    onResultReadyCallback([]);
                }

            })
            .error(function(reason) {
                onResultReadyCallback([]);
            })
    }
    else {

        if (!this._symbolSearch) {
            throw "Datafeed error: inconsistent configuration (symbol search)";
        }

        var searchArgument = {
            ticker: ticker,
            exchange: exchange,
            type: type,
            onResultReadyCallback: onResultReadyCallback
        };

        if (this._initializationFinished) {
            this._symbolSearch.searchSymbolsByName(searchArgument, MAX_SEARCH_RESULTS);
        }
        else {

            var that = this;

            this.on("initialized", function() {
                that._symbolSearch.searchSymbolsByName(searchArgument, MAX_SEARCH_RESULTS);
            });
        }
    }
}


//	BEWARE: this function does not consider symbol's exchange
Datafeeds.UDFCompatibleDatafeed.prototype.resolveSymbol = function(symbolName, onSymbolResolvedCallback, onResolveErrorCallback) {

    symbolName = symbolName.replace(":","");//remove special that our server doesn't support

    var that = this;

    if (!this._initializationFinished) {
        this.on("initialized", function() {
            that.resolveSymbol(symbolName, onSymbolResolvedCallback, onResolveErrorCallback);
        });

        return;
    }

    if (!this._configuration.supports_group_request) {
        var requestURL = this._datafeedURL + "/symbols?symbol=" + encodeURIComponent(symbolName);
        console.log(requestURL)
        this._logMessage(requestURL);
        $.ajax({url : requestURL, dataType : 'json'})
            .done(function (response) {
                var data = response;

                if (data.s && data.s != "ok") {
                    onResolveErrorCallback("unknown_symbol");
                }
                else {
                    onSymbolResolvedCallback(data)
                }
            })
            .error(function(reason) {
                onResolveErrorCallback("unknown_symbol");
            })
    }
    else {
        if (this._initializationFinished) {
            this._symbolsStorage.resolveSymbol(symbolName, onSymbolResolvedCallback, onResolveErrorCallback);
        }
        else {
            this.on("initialized", function() {
                that._symbolsStorage.resolveSymbol(symbolName, onSymbolResolvedCallback, onResolveErrorCallback);
            });
        }
    }
}



Datafeeds.UDFCompatibleDatafeed.prototype.getBars = function(symbolInfo, resolution, rangeStartDate, rangeEndDate, onDataCallback, onErrorCallback) {

    //	timestamp sample: 1399939200
    if (rangeStartDate > 0 && (rangeStartDate + "").length > 10) {
        throw "Got a JS time instead of Unix one.";
    }

    /*************************just fetch last three years data in D,W,M period******************************/
    rangeEndDate = parseInt(new Date().getTime() / 1000);
    switch(resolution+""){
        case "60":
            resolution = "1h";
            break;
        case "240":
            resolution = "4h";
            break;
        case "D":
            resolution = "1d";
            rangeStartDate = rangeEndDate - 3 * 365 * 24 * 60 * 60;
            break;
        case "W":
            resolution = "1w";
            rangeStartDate = rangeEndDate - 3 * 365 * 24 * 60 * 60;
            break;
        case "M":
            resolution = "mn";
            rangeStartDate = rangeEndDate - 3 * 365 * 24 * 60 * 60;
            break;

    }	var requestURL = this._datafeedURL + "/history" +
        //"?symbol=" + symbolInfo.ticker.toUpperCase() +
        "?symbol=" + symbolInfo.name +		"&resolution=" + resolution +
        "&from=" + rangeStartDate +
        "&to=" + rangeEndDate;

    this._logMessage("Requesting data from " + requestURL);

    $.ajax({url : requestURL, dataType : 'json'})
        .done(function (response) {
            var data = response;

            if (data.s != "ok") {
                if (!!onErrorCallback) {
                    onErrorCallback(data.s);
                }
                return;
            }

            var bars = [];

            //	data is JSON having format {s: "status", v: [volumes], t: [times], o: [opens], h: [highs], l: [lows], c:[closes]}
            var barsCount = data.t.length;

            var volumePresent = typeof data.v != "undefined";
            var ohlPresent = typeof data.o != "undefined";

            for (var i = 0; i < barsCount; ++i) {

                var barValue = {
                    time: data.t[i] * 1000,
                    close: data.c[i]
                };

                if (ohlPresent) {
                    barValue.open = data.o[i];
                    barValue.high = data.h[i];
                    barValue.low = data.l[i];
                }
                else {
                    barValue.open = barValue.high = barValue.low = barValue.close;
                }

                if (volumePresent) {
                    barValue.volume = data.v[i];
                }

                bars.push(barValue);
            }

            if (bars.length == 0) {
                onErrorCallback("no data");
            }
            else {
                onDataCallback(bars);
            }

        }).
    error(function (arg) {
        if (!!onErrorCallback) {
            onErrorCallback("network error: " + arg);
        }
    });
}


Datafeeds.UDFCompatibleDatafeed.prototype.subscribeBars = function(symbolInfo, resolution, onRealtimeCallback, listenerGUID) {
    this._pulseUpdater.subscribeDataListener(symbolInfo, resolution, onRealtimeCallback, listenerGUID);
}

Datafeeds.UDFCompatibleDatafeed.prototype.unsubscribeBars = function(listenerGUID) {
    this._pulseUpdater.unsubscribeDataListener(listenerGUID);
}

Datafeeds.UDFCompatibleDatafeed.prototype.calculateHistoryDepth = function(period, resolutionBack, intervalBack) {
}

//	==================================================================================================================================================
//	==================================================================================================================================================
//	==================================================================================================================================================

/*
 It's a symbol storage component for ExternalDatafeed. This component can
 * interact to UDF-compatible datafeed which supports whole group info requesting
 * do symbol resolving -- return symbol info by its name
 */
Datafeeds.SymbolsStorage = function(datafeed) {
    this._datafeed = datafeed;

    this._exchangesList = ["NYSE", "FOREX", "AMEX"];
    this._exchangesWaitingForData = {};
    this._exchangesDataCache = {};

    this._symbolsInfo = {};
    this._symbolsList = [];

    this._requestFullSymbolsList();
}




Datafeeds.SymbolsStorage.prototype._requestFullSymbolsList = function() {

    var that = this;
    var datafeed = this._datafeed;

    for (var i = 0; i < this._exchangesList.length; ++i) {

        var exchange = this._exchangesList[i];

        if (this._exchangesDataCache.hasOwnProperty(exchange)) {
            continue;
        }

        this._exchangesDataCache[exchange] = true;

        this._exchangesWaitingForData[exchange] = "waiting_for_data";

        var requestURL = datafeed._datafeedURL + "/symbol_info?group=" + exchange;
        this._datafeed._logMessage("requesting exnchage info from " + requestURL);

        $.ajax({url : requestURL ,  dataType : 'json'}).
        done(function(exchange) {
            return function(response) {
                that._onExchangeDataReceived(exchange, response);
                that._onAnyExchangeResponseReceived(exchange);
            }
        }(exchange)).
        error(function(exchange) {
            return function (reason) {
                that._onAnyExchangeResponseReceived(exchange);
            };
        }(exchange));
    }
}



Datafeeds.SymbolsStorage.prototype._onExchangeDataReceived = function(exchangeName, data) {

    function tableField(data, name, index) {
        return data[name] instanceof Array
            ? data[name][index]
            : data[name];
    }

    try
    {
        for (var symbolIndex = 0; symbolIndex < data.symbol.length; ++symbolIndex) {

            var symbolName = data.symbol[symbolIndex];
            var listedExchange = tableField(data, "exchange-listed", symbolIndex);
            var tradedExchange = tableField(data, "exchange-traded", symbolIndex);
            var fullName = tradedExchange + ":" + symbolName;

            //	This feature support is not implemented yet
            //	var hasDWM = tableField(data, "has-dwm", symbolIndex);

            var hasIntraday = tableField(data, "has-intraday", symbolIndex);

            var tickerPresent = typeof data["ticker"] != "undefined";

            this._symbolsInfo[fullName] = {
                name: symbolName,
                base_name: [listedExchange + ":" + symbolName],
                description: tableField(data, "description", symbolIndex),
                full_name: fullName,
                legs: [fullName],
                has_intraday: hasIntraday,
                has_no_volume: tableField(data, "has-no-volume", symbolIndex),
                listed_exchange: listedExchange,
                exchange: tradedExchange,
                minmov: tableField(data, "minmovement", symbolIndex) || tableField(data, "minmov", symbolIndex) ,
                pointvalue: tableField(data, "pointvalue", symbolIndex),
                pricescale: tableField(data, "pricescale", symbolIndex),
                type: tableField(data, "type", symbolIndex),
                ticker: tickerPresent ? tableField(data, "ticker", symbolIndex) : symbolName,
                timezone: tableField(data, "timezone", symbolIndex)
            };

            this._symbolsInfo[symbolName] = this._symbolsInfo[fullName];
            this._symbolsList.push(symbolName);
        }
    }
    catch (error) {
        throw "API error when processing exchange `" + exchangeName + "` symbol #" + symbolIndex + ": " + error;
    }
}


Datafeeds.SymbolsStorage.prototype._onAnyExchangeResponseReceived = function(exchangeName) {

    delete this._exchangesWaitingForData[exchangeName];

    var allDataReady = Object.keys(this._exchangesWaitingForData).length == 0;

    if (allDataReady) {
        this._symbolsList.sort();
        this._datafeed._logMessage("All exchanges data ready");
        this._datafeed.onInitialized();
    }
}


//	BEWARE: this function does not consider symbol's exchange
Datafeeds.SymbolsStorage.prototype.resolveSymbol = function(symbolName, onSymbolResolvedCallback, onResolveErrorCallback) {

    if (!this._symbolsInfo.hasOwnProperty(symbolName)) {
        onResolveErrorCallback("invalid symbol");
    }
    else {
        onSymbolResolvedCallback(this._symbolsInfo[symbolName]);
    };

}


//	==================================================================================================================================================
//	==================================================================================================================================================
//	==================================================================================================================================================

/*
 It's a symbol search component for ExternalDatafeed. This component can do symbol search only.
 This component strongly depends on SymbolsDataStorage and cannot work without it. Maybe, it would be
 better to merge it to SymbolsDataStorage.
 */

Datafeeds.SymbolSearchComponent = function(datafeed) {
    this._datafeed = datafeed;
}



//	searchArgument = { ticker, onResultReadyCallback}
Datafeeds.SymbolSearchComponent.prototype.searchSymbolsByName = function(searchArgument, maxSearchResults) {

    if (!this._datafeed._symbolsStorage) {
        throw "Cannot use local symbol search when no groups information is available";
    }

    var symbolsStorage = this._datafeed._symbolsStorage;

    var results = [];
    var queryIsEmpty = !searchArgument.ticker || searchArgument.ticker.length == 0;

    for (var i = 0; i < symbolsStorage._symbolsList.length; ++i) {
        var symbolName = symbolsStorage._symbolsList[i];
        var item = symbolsStorage._symbolsInfo[symbolName];

        if (searchArgument.type && searchArgument.type.length > 0 && item.type != searchArgument.type) {
            continue;
        }
        if (searchArgument.exchange && searchArgument.exchange.length > 0 && item.exchange != searchArgument.exchange) {
            continue;
        }
        if (queryIsEmpty || item.name.indexOf(searchArgument.ticker) == 0) {
            results.push({
                symbol: item.name,
                full_name: item.full_name,
                description: item.description,
                exchange: item.exchange,
                params: [],
                type: item.type
            });
        }

        if (results.length >= maxSearchResults) {
            break;
        }
    }

    searchArgument.onResultReadyCallback(results);
}



//	==================================================================================================================================================
//	==================================================================================================================================================
//	==================================================================================================================================================

/*
 It's a pulse updating component for ExternalDatafeed. It emulates realtime updates with periodic requests.
 */

Datafeeds.PulseUpdater = function(datafeed) {
    this._datafeed = datafeed;
    this._subscribers = {};

    this._requestsPending = 0;
    var that = this;

    var update = function() {
        if (that._requestsPending > 0) {
            return;
        }

        for (var listenerGUID in that._subscribers) {
            var subscriptionRecord = that._subscribers[listenerGUID];
            var resolution = subscriptionRecord.resolution;

            var datesRangeRight = parseInt((new Date().valueOf()) / 1000);

            //	BEWARE: please note we really need 2 bars, not the only last one
            //	see the explanation below. `10` is the `large enough` value to work around holidays
            var datesRangeLeft = datesRangeRight - that.periodLengthSeconds(resolution, 10);

            that._requestsPending++;

            (function(_subscriptionRecord) {

                that._datafeed.getBars(_subscriptionRecord.symbolInfo, resolution, datesRangeLeft, datesRangeRight, function(bars) {
                        that._requestsPending--;

                        //	means the subscription was cancelled while waiting for data
                        if (!that._subscribers.hasOwnProperty(listenerGUID)) {
                            return;
                        }

                        if (bars.length === 0) {
                            return;
                        }

                        var lastBar = bars[bars.length - 1];
                        if (!isNaN(_subscriptionRecord.lastBarTime) && lastBar.time < _subscriptionRecord.lastBarTime) {
                            return;
                        }

                        var subscribers = _subscriptionRecord.listeners;

                        //	BEWARE: this one isn't working when first update comes and this update makes a new bar. In this case
                        //	_subscriptionRecord.lastBarTime = NaN
                        var isNewBar = !isNaN(_subscriptionRecord.lastBarTime) && lastBar.time > _subscriptionRecord.lastBarTime;

                        //	Pulse updating may miss some trades data (ie, if pulse period = 10 secods and new bar is started 5 seconds later after the last update, the
                        //	old bar's last 5 seconds trades will be lost). Thus, at fist we should broadcast old bar updates when it's ready.
                        if (isNewBar) {

                            if (bars.length < 2) {
                                throw 'Not enough bars in history for proper pulse update. Need at least 2.';
                            }

                            var previousBar = bars[bars.length - 2];
                            for (var i = 0; i < subscribers.length; ++i) {
                                subscribers[i](previousBar);
                            }
                        }

                        _subscriptionRecord.lastBarTime = lastBar.time;

                        for (var i = 0; i < subscribers.length; ++i) {
                            subscribers[i](lastBar);
                        }
                    },

                    //	on error
                    function() {
                        that._requestsPending--;
                    });
            })(subscriptionRecord); //jshint ignore:line

        }
    };

    if (typeof updateFrequency != 'undefined' && updateFrequency > 0) {
    }
    setInterval(update, 10*1000);
}


Datafeeds.PulseUpdater.prototype.unsubscribeDataListener = function(listenerGUID) {
    this._datafeed._logMessage("Unsubscribing " + listenerGUID);
    delete this._subscribers[listenerGUID];
}


Datafeeds.PulseUpdater.prototype.subscribeDataListener = function(symbolInfo, resolution, newDataCallback, listenerGUID) {

    this._datafeed._logMessage("Subscribing " + listenerGUID);

    var key = symbolInfo.name + ", " + resolution;

    if (!this._subscribers.hasOwnProperty(listenerGUID)) {

        this._subscribers[listenerGUID] = {
            symbolInfo: symbolInfo,
            resolution: resolution,
            lastBarTime: NaN,
            listeners: []
        };
    }

    this._subscribers[listenerGUID].listeners.push(newDataCallback);
}


Datafeeds.PulseUpdater.prototype.periodLengthSeconds = function(resolution, requiredPeriodsCount) {
    var daysCount = 0;

    if (resolution == "D") {
        daysCount = requiredPeriodsCount;
    }
    else if (resolution == "M") {
        daysCount = 31 * requiredPeriodsCount;
    }
    else if (resolution == "W") {
        daysCount = 7 * requiredPeriodsCount;
    }
    else {
        daysCount = requiredPeriodsCount * resolution / (24 * 60);
    }

    return daysCount * 24 * 60 * 60;
}