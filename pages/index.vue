<template>
  <div class="container">
      <h1 class="title">
        Bus Stop Story
      </h1>
      <h2 class="subtitle">
        A visualization of bus stops operated by Translink
      </h2>
      <h3> A Map of All the Bus Stops </h3>
      <BusMap :data=loadData />
      <h3> Bus Stops By The Numbers </h3>
      <p> Here you can see all the bus appear in order of ascending number. </p>
      <BusAnimation :data=loadData />
  </div>
</template>

<script>
import * as d3 from "d3";
import BusMap from '~/components/BusMap.vue';
import BusAnimation from '~/components/BusAnimation.vue';
import fileData from '~/static/data/stop_data.json';

export default {

  components: {
    BusMap,
    BusAnimation
  },

  data() {
    return {
      loadData: fileData
    }
  },

}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.title {
  flex: auto;
}

.subtitle {
  flex: auto;
}

.BusAnimation {
  flex: auto;
}
</style>
