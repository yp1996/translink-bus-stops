<template>
  <div class="BusAnimation" ref="main">
    <!--
   <l-map :zoom=13 :center="centrePoint" ref="map">
     <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png">
     </l-tile-layer>

   </l-map>
   <svg ref="svg">
           <div class="tooltip" ref="tooltip"></div>
      </svg> -->

    <div class="map" ref="map"></div>
  </div>
</template>

<style>

.BusAnimation {
  display: block;
  width: 800px;
  height: 800px;
}

.map {
  width: 800px;
  height: 800px;
}

</style>

<script>
import * as d3 from "d3";

export default {
  name: "BusAnimation",
  props: ["data"],

  data: function ()  {
  return {
     map: Object,
     svg: Object,
     tooltip: Object,
     g: Object
  }
  },

  mounted() {
    this.map = this.createMap()
    this.plotData();
  }, 

  methods: {

    createMap() {
      return this.$L.map(this.$refs.map).setView(this.centrePoint, 10.2);
    },

    plotData() {

    const width = 800;
    const height = 800;
    const numRoutes = 400;

    var vm = this; 

    let mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
    this.$L.tileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; ' + mapLink + ' Contributors',
            maxZoom: 18,
            }).addTo(this.map);

    // setup x 
    var xValue = function(d) { return d.Longitude;}, // data -> value
        xScale = d3.scaleLinear().range([width, 0]).domain([this.getXMin, this.getXMax]), // value -> display
        //xMap = function(d) { return xScale(xValue(d));}, // data -> display
        xAxis = d3.axisBottom().scale(xScale);

    // setup y
    var yValue = function(d) { return d.Latitude;}, // data -> value
        yScale = d3.scaleLinear().range([height,0]).domain([this.getYMin, this.getYMax]), // value -> display
        //yMap = function(d) { return yScale(yValue(d));}, // data -> display
        yAxis = d3.axisLeft().scale(yScale);
  

    // add the graph canvas to the body of the webpage

    this.svg = d3.select(this.map.getPanes().overlayPane).append("svg");

    this.g = this.svg.append("g").attr("class", "leaflet-zoom-hide");

    // add the tooltip area to the webpage
    this.tooltip = d3.select(this.$refs.main).append("div")
        .attr("style", "position: absolute; opacity: 0; background: #fff; z-index:999").attr("ref","tooltip");

    this.map.on("moveend", this.reset);

    this.data.forEach(function(d) {
      d.LatLng = new vm.$L.LatLng(d.Latitude,
                  d.Longitude)
    });

    var colour = d3.scaleOrdinal()
    .domain([0,400])
    .range(d3.schemePaired)

    this.g.selectAll("circle").data(this.data).enter()
    .append("circle").attr("class", "dot")
    .attr("pointer-events", "visible")
    .attr("r", 5)
    .attr("cx", function (d) {
      return vm.xMap(d);
    })
    .attr("cy", function(d) {
      return vm.yMap(d);
    })
    .style("fill", function(d) {
      return colour(d.Routes);
    })
    .on("mouseover", function(d) {
      vm.tooltipEnter(d);
      })
    .on("mouseout", function(d) {
      vm.tooltipExit();
    });


    this.reset();

    },

    getNumRoutes() {
      
    },

    reset() {
        var bounds = this.map.getBounds();
        var topLeft = this.map.latLngToLayerPoint(bounds.getNorthWest());
        var bottomRight = this.map.latLngToLayerPoint(bounds.getSouthEast());
        this.svg.attr("width", bottomRight.x - topLeft.x)
          .attr("height", bottomRight.y - topLeft.y)
          .style("left", topLeft.x + "px")
          .style("top", topLeft.y + "px");
        this.g.attr('transform', 'translate('+ -topLeft.x + ',' + -topLeft.y + ')');
        this.updatePositions();

    },

    updatePositions() {

        var vm = this;
        this.g.selectAll("circle").attr("cx", 
          function(d,i) { 
            return vm.xMap(d);
            }
        ).attr("cy", 
          function(d,i) { 
            return vm.yMap(d);
            }
        );
    },

    tooltipEnter(d) {

      this.tooltip.style('left', d3.event.pageX + 'px')
          .style('top', d3.event.pageY + 'px');

      this.tooltip.transition()
            .duration(200)
            .style("opacity", .9);
      this.tooltip.html(d.Name + "<br/> (" + d.Latitude
          + ", " + d.Longitude + ")" + "<br/>" + d.Routes)
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
    },

    tooltipExit() {

      this.tooltip.transition()
        .duration(500)
        .style("opacity", 0);
    },

    color() {
      return d3.scaleOrdinal(d3.schemeCategory10).domain([0, 400]);
    },

    xMap(d) {
      return this.map.latLngToLayerPoint(d.LatLng).x;
    },

    yMap(d) {
      return this.map.latLngToLayerPoint(d.LatLng).y;
    }

  },

  computed: {

    getXMax() {
      return d3.max(this.data, (d) => {return d.Longitude});
    },

    getXMin() {
      return d3.min(this.data, (d) => {return d.Longitude});
    },

    getYMax() {
      return d3.max(this.data, (d) => {return d.Latitude});
    },

    getYMin() {
      return d3.min(this.data, (d) => {return d.Latitude});
    },

    centrePoint() {

      let centreX = (parseFloat(this.getXMin) + parseFloat(this.getXMax)) / 2;
      let centreY = (parseFloat(this.getYMin) + parseFloat(this.getYMax)) / 2;
      return [centreY, centreX];
    },

  }
}

</script>
