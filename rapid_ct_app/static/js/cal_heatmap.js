var cal = new CalHeatMap();
var startDate = null;
var endDate = null;
  cal.init({
    start: new Date(2015, 0),
    range: 10,
    domain: "month",
    subDomain: "day",
    data: heatmapdata,    
  onClick: function(date, nb) {
    if (startDate === null || startDate && endDate) {
      startDate = date;
      endDate = null;
      this.highlight();
    } else if (endDate === null) {
      endDate = date;        
      console.log(startDate, endDate);
      var dates= [];
      for (var d=startDate.getTime(); d<endDate.getTime(); d+=24*60*60*1000) {
        dates.push(new Date(d));
      }
      this.highlight(dates);
    } else {
      
    }
  }    
  });
cal.highlight(["now", new Date(2015, 1, 15)]);
//debugger;