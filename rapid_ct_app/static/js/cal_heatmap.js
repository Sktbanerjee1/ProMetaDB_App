var cal = new CalHeatMap();
var startDate = null;
var endDate = null;
  cal.init({
    range: 4,
    domain: "month",
    subDomain: "day",
    domainGutter: 0,
    domainMargin: 0,
    cellSize: 10,
    nextSelector: "#domainDynamicDimension-next",
    previousSelector: "#domainDynamicDimension-previous",
    data: heatmapdata,
    legend: [10, 15, 20, 25, 30],
    legendColors: {
      empty: "#DEE3DB",
      max: "#005522"
    }
  });
cal.highlight(["now"]);
//debugger;