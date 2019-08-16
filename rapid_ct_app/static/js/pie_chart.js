var height = 180
var width = 180
var totalRadius = Math.min(width, height)/2
var donutHoleRadius = totalRadius * 0.4
var color = d3.scale.category10()

var svg = d3.select('#chart').append('svg').attr('width', width).attr('height', height)
  .append('g')
  .attr('transform', `translate(${width / 2}, ${height / 2})`)

var arc = d3.svg.arc().innerRadius(totalRadius - donutHoleRadius).outerRadius(totalRadius)

var pie = d3.layout.pie()
  .value((d) => d.value)
  .sort(null)

var path = svg
  .selectAll('path')
  .data(pie(piedata))
  .enter()
  .append('path')
  .attr('d', arc)
  .attr('fill', (d, i) => color(d.data.name))

var legendItemSize = 12
var legendSpacing = 2

var legend = svg
  .selectAll('.legend')
  .data(color.domain())
  .enter()
  .append('g')
  .attr('class', 'legend')
  .attr('transform', (d, i) => {
    var height = legendItemSize + legendSpacing
    var offset = height * color.domain().length / 2
    var x = legendItemSize * -2;
    var y = (i * height) - offset
    return `translate(${x}, ${y})`
  })

legend
  .append('rect')
  .attr('width', legendItemSize)
  .attr('height', legendItemSize)
  .style('fill', color);

legend
  .append('text')
  .attr('x', legendItemSize + legendSpacing)
  .attr('y', legendItemSize - legendSpacing)
  .text((d) => d)
