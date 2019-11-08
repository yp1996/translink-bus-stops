<template>
  <div class="container">
      <h1 class="title">
        Bus Stop Story
      </h1>
      <h2 class="subtitle">
        A visualization of bus stops operated by Translink
      </h2>
      <BusAnimation :data=loadData />
  </div>
</template>

<script>
import * as d3 from "d3";
import BusAnimation from '~/components/BusAnimation.vue';
import fileData from '~/static/data/stop_data.json';

export default {

  components: {
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
