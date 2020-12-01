<template>
  <div id="app">
    <div class="mb5">
      <el-switch
        v-model="value"
        inactive-color="#13ce66"
        active-value="TWITTER"
        inactive-value="FILE"
        active-text="Twitter"
        inactive-text="File Upload"
      >
      </el-switch>
    </div>
    <div v-if="value == 'FILE'">
      <FileUpload />
    </div>
    <div v-if="value == 'TWITTER'">
      <Twitter />
    </div>
  </div>
</template>

<script>
import FileUpload from "./components/FileUpload.vue";
import Twitter from "./components/Twitter.vue";

export default {
  name: "App",
  components: {
    FileUpload,
    Twitter,
  },
  data() {
    return {
      value: "TWITTER",
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.mb5 {
  margin-bottom: 50px;
}
</style>
