OHLCRequestResponseHandler = function(feedHandler) {

  "use strict";

  this.feedHandler = feedHandler;
  this._barsKeyTable = {};
  this._barsTable = {};

  this.init();
};

OHLCRequestResponseHandler.prototype.init = function() {

  "use strict";

  this._barsKeyTable = this.feedHandler._db.getCollection('bars_key_table');
  this._barsTable = this.feedHandler._db.getCollection('bars_table');

  this.requestParameters = function(rangeStartDate, rangeEndDate) {

    var parseSuffixAndIntValue = this.parseSuffixAndIntValue(),
        suffix = parseSuffixAndIntValue.suffix,
        intVal = parseSuffixAndIntValue.intVal,
        totalSecondsInABar = this.totalSecondsInABar(suffix, intVal);
        //console.log(suffix, intVal, totalSecondsInABar);

    var count = Math.ceil((rangeEndDate - rangeStartDate) / totalSecondsInABar);
    //console.log('Number of bars requested : ', count);

    return {
      suffix : suffix,
      intVal : intVal,
      count : count,
      totalSecondsInABar  : totalSecondsInABar
    };

  };

  this.renderBars = function( tableID ) {
    var db_Bars = this._barsTable.chain()
                                 .find({barsKeyTableID : tableID})
                                 .find({'rendered' : false})
                                 .simplesort('time', false).data(),
        tableRow = this._barsKeyTable.findObject({barsKeyTableID : tableID});
    
    var 
        onErrorCallback = tableRow.onErrorCallback_chart,
        onDataCallback = tableRow.onDataCallback_chart,
        bars = [];
    db_Bars.forEach(function(eachBar) {
      bars.push({
        time : eachBar.time,
        open : eachBar.open,
        high : eachBar.high,
        low  : eachBar.low,
        close : eachBar.close
      });
      eachBar.rendered = true;
    });

    if (db_Bars && db_Bars.length > 0) {
      //don't mark the last bar rendered = true. because it is always changing
      db_Bars[db_Bars.length - 1].rendered = false;
    }
    this._barsTable.update(db_Bars);
    //console.log('Rendering bars', bars);
    console.log('Bars length', bars.length);

    if (bars.length === 0 && onErrorCallback)
    {
      console.log('Calling TV onErrorCallback');
      onErrorCallback("no data");
    } else if (onDataCallback)
    {
      console.log('Caling TV onDataCallback');
      //if onErrorCallback is undefined/NULL, that means it was on new Bar subscriber call
      if (!onErrorCallback) {
        bars.forEach(function (bar) {
          onDataCallback(bar);
        });
      } else {
        onDataCallback(bars);
      }
    }
  };

};

OHLCRequestResponseHandler.prototype.parseSuffixAndIntValue = function() {

  "use strict";

  var intValInString = TradingView.actualResolution.toUpperCase().replace('D', '').replace('M', '').replace('W', '');
  var intVal = intValInString === '' ? 1 : parseInt(intValInString);
  var suffix = TradingView.actualResolution.replace('' + intVal, '');
  //console.log('Suffix : ', suffix, " TradingView.actualResolution : ", TradingView.actualResolution);
  switch(suffix) {
    case '':
      if (intVal < 60) {
        suffix = 'M';
      } else {
        intVal /= 60;
        suffix = 'H';
      }
      break;
    case 'W':
      intVal *= 7;
      suffix = 'D';
      break;
    case 'M':
      intVal *= 30;
      suffix = 'D';
      break;
  }
  return {
    suffix : suffix,
    intVal : intVal
  };
};

OHLCRequestResponseHandler.prototype.totalSecondsInABar = function(suffix, intVal) {

  "use strict";

  var totalSecondsInABar = 0;
  switch(suffix) {
    case 'M':
      totalSecondsInABar = intVal * 60;
      break;
    case 'H':
      totalSecondsInABar = intVal * 60 * 60;
      break;
    case 'D':
      totalSecondsInABar = intVal * 24 * 60 * 60;
      break;
  }
  return totalSecondsInABar;
};

OHLCRequestResponseHandler.prototype.getBars = function(symbolInfo, rangeStartDate, rangeEndDate, onDataCallback, onErrorCallback, ignoreEndDate) {

  "use strict";

	var that = this;

	//	timestamp sample: 1399939200
	if (rangeStartDate > 0 && (rangeStartDate + "").length > 10) {
		throw "Got a JS time instead of Unix one.";
	}

  var tableRow = this._barsKeyTable.findObject({'key' : symbolInfo.ticker + TradingView.actualResolution}) || {},
      tableID = tableRow.barsKeyTableID || -1;
  if (tableID === -1) {
    tableID = new Date().getTime();
    this._barsKeyTable.insert({
      barsKeyTableID : tableID,
      key : symbolInfo.ticker + TradingView.actualResolution,
      onErrorCallback_chart : onErrorCallback,
      onDataCallback_chart : onDataCallback,
    });
    tableRow = this._barsKeyTable.findOne({barsKeyTableID : tableID});
  } else {
    //Update the callback functions
    tableRow.onDataCallback_chart = onDataCallback;
    tableRow.onErrorCallback_chart = onErrorCallback;
    this._barsKeyTable.update(tableRow);
  }

  var requestParameters = this.requestParameters(rangeStartDate, rangeEndDate),
      suffix = requestParameters.suffix,
      intVal = requestParameters.intVal,
      count = requestParameters.count,
      totalSecondsInABar = requestParameters.totalSecondsInABar;

  var dataExists = false;
  if (this._barsTable.findObject({'barsKeyTableID' : tableID})) {//Check if data exists
    var firstBar = this._barsTable.chain().find({'barsKeyTableID' : tableID}).simplesort('time', false).limit(1).data()[0],
        timeOfFirstBar = firstBar.time / 1000;

    //Bar history calls for chart moved to the left means, we do not need rangeEndDate to be latest bar time. The
    //rangeEndDate could be the time of the first bar on chart. There is some problem with the TradingView library
    //that it always sends the rangeEndDate as the current time. That increases COUNT parameter of the WS API call
    if (rangeStartDate < timeOfFirstBar) {
      console.log('Modfied end time!');
      rangeEndDate = timeOfFirstBar;
    }
    dataExists = true;
  }

  //We cannot request more than 500 candles at a time
  if (count > 500) {
    rangeStartDate = rangeEndDate - 450 * totalSecondsInABar;
  }
  
  //We cannot request more than 3 years old data
  var maxDateBackFromNow_seconds = Math.floor(moment.utc().valueOf() / 1000 - 3 * 365 * 24 * 60 * 60);
  if (rangeStartDate < maxDateBackFromNow_seconds) {
	  rangeStartDate = maxDateBackFromNow_seconds;
  }

  rangeEndDate += totalSecondsInABar;
  console.log('Request date range : ' , new Date(rangeStartDate * 1000), new Date(rangeEndDate * 1000),
                'Total Seconds in a bar : ', totalSecondsInABar,
                'Ignore End Date : ', ignoreEndDate);
  var requestObject = {
    "ticks_history": symbolInfo.ticker,
    "start": Math.floor(rangeStartDate),
    "end": ignoreEndDate || !dataExists ? 'latest' : Math.ceil(rangeEndDate), 
    //"count": count,
    "granularity":  suffix + intVal,
    "adjust_start_time": 1
  };
  console.log(JSON.stringify(requestObject));
  this.feedHandler._webSocketConnection.send(JSON.stringify(requestObject));

};

OHLCRequestResponseHandler.prototype.process = function( data ) {

  "use strict";

  if (!data.candles) return;
  console.log('Response number of bars (from WS API): ', data.candles.length);

  //Candles are returned with time in desc order
  var barsFromResponse = data.candles;

  var tableRow = this._barsKeyTable.findObject({'key' : data.echo_req.ticks_history + TradingView.actualResolution}) || {},
      tableID = tableRow.barsKeyTableID || -1;

  var that = this;

  barsFromResponse.forEach(function(eachData)
  {
      var time 	= parseInt(eachData.epoch) * 1000;
  		var open 	= parseFloat(eachData.open);
      var high 	= parseFloat(eachData.high);
      var low 	= parseFloat(eachData.low);
      var close = parseFloat(eachData.close);

      var bars = that._barsTable.chain().find({'barsKeyTableID' : tableID}).find({'time' : time}).limit(1).data();
      if(bars.length <= 0) {
        that._barsTable.insert({
          barsKeyTableID : tableID,
          time  : time,
  				open  : open,
  				high  : high,
  				low   : low ,
  				close : close,
          rendered : false
        });
      } else {
        bars[0].open  = open;
        bars[0].high  = high;
        bars[0].low   = low ;
        bars[0].close = close;
        that._barsTable.update(bars);
      }

  });

  this.renderBars( tableID );

  $(document).trigger('barsLoaded');

};

OHLCRequestResponseHandler.prototype.resetTableData = function(symbolInfo) {

  "use strict";
  
  var tableRow = this._barsKeyTable.findObject({'key' : symbolInfo.ticker + TradingView.actualResolution}) || {},
      tableID = tableRow.barsKeyTableID || -1,
      bars = this._barsTable.chain().find({'barsKeyTableID' : tableID}).data() || [];
  bars.forEach(function(bar) {
    bar.rendered = false;
  });
  this._barsTable.update(bars);
};
