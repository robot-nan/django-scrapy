SymbolRequestResponsehandler = function (feedHandler) {

    "use strict";

    this._markets = null;
    this._symbolTypes = null;

    this._currentlyProcessingRequest = false;

    this.fetchSymbolListAndInformation = function () {
        //If the market information has not been loaded yet
        if (!this._markets) {
            //If we are already processing one request now, ignore subsequent requests
            if (!this._currentlyProcessingRequest) {
                //When the WS API is available, change this code to use the API to get exchange and symbol type lists
                if (feedHandler._webSocketConnection) {
                    this._currentlyProcessingRequest = true;
                    if (!feedHandler._isConnectionReady) {
                        $(document).one('websocketsConnectionReady', function () {
                            feedHandler._webSocketConnection.send(JSON.stringify({"trading_times": "" + new Date().toISOString().slice(0, 10)}));
                        });
                    } else {
                        feedHandler._webSocketConnection.send(JSON.stringify({"trading_times": "" + new Date().toISOString().slice(0, 10)}));
                    }
                }
            }
        } else {
            this._currentlyProcessingRequest = false;
        }
    };

};

SymbolRequestResponsehandler.prototype.getSymbolTypeList = function () {
    "use strict";
    this.fetchSymbolListAndInformation();
    return this._symbolTypes;
};

SymbolRequestResponsehandler.prototype.getSymbolList = function () {
    "use strict";
    this.fetchSymbolListAndInformation();
    return this.markets;
};

SymbolRequestResponsehandler.prototype.process = function (data) {
    "use strict";
    this._markets = [];
    this._symbolTypes = [];

    for (var marketIndex = 0; marketIndex < data.trading_times.markets.length; marketIndex++) {
        var marketFromResponse = data.trading_times.markets[marketIndex];
        this._symbolTypes.push(marketFromResponse.name);
        var market = {
            name: marketFromResponse.name, //Same as symbolType
            submarkets: []
        };

        for (var subMktIndx = 0; subMktIndx < marketFromResponse.submarkets.length; ++subMktIndx) {
            var submarket = marketFromResponse.submarkets[subMktIndx];
            var submarketObj = {
                name: submarket.name,
                symbols: []
            };
            for (var symbIndx = 0; symbIndx < submarket.symbols.length; symbIndx++) {
                var eachSymbol = submarket.symbols[symbIndx];
                if (!eachSymbol.feed_license || eachSymbol.feed_license !== 'chartonly') {
                    submarketObj.symbols.push({
                        symbol: eachSymbol.symbol,
                        symbol_display: eachSymbol.name
                    });
                }
            }
            market.submarkets.push(submarketObj);
        }

        this._markets.push(market);
    }

    $(document).trigger('marketsLoaded');
    this._currentlyProcessingRequest = false;
};
