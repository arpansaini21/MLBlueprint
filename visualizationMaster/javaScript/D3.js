<!DOCTYPE html>
<meta charset="utf-8">
<script src="https://d3js.org/d3.v6.min.js"></script>
<body>
<script>
  var data = [30, 86, 168, 281, 303, 365];
  d3.select("body").selectAll("div")
    .data(data)
    .enter().append("div")
    .style("width", function(d) { return d + "px"; })
    .text(function(d) { return d; });
</script>
</body>
