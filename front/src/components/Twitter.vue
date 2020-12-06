<template>
  <div>
    <el-form class="form" @submit.native.prevent="submit">
      <el-input
        placeholder="Input YOUR account name"
        v-model="input"
      ></el-input>
      <el-button
        @click="submit"
        v-bind:disabled="loading"
      >submit</el-button>
    </el-form>
    <div class="image-container"
      v-loading="loading"
      element-loading-text=""
      element-loading-spinner="el-icon-loading"      
    >
      <div v-for="datum in data" v-bind:key="datum.img_url">
        <el-image
          :src="datum.img_url"
          style="width: 200px; height: 200px"
          fit="contain"
        ></el-image>
        <p v-if="datum.result && datum.result[0]">
          {{ datum.result[0].AgeRange.Low }} -
          {{ datum.result[0].AgeRange.High }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Twitter",
  data: function () {
    return {
      input: "",
      data: [],
      loading: false,
    };
  },
  methods: {
    submit: function () {
      if (this.loading == true) {
        return
      }
      this.loading = true;
      this.data = [];
      const vm = this;
      this.$axios
        .get("http://localhost:8080/twitter/" + this.input)
        .then(function (response) {
          const res = response.data;
          Object.keys(res).forEach(function (key) {
            var datum = this[key];
            if (datum.result.FaceDetails.length > 0) {
              vm.data.push({
                img_url: datum.filename,
                result: datum.result.FaceDetails,
              });
            }
          }, res);
          if (vm.data.length == 0) {
            vm.$message({
              message: '認識できる顔画像が見つかりませんでした',
              type: 'warning'
            });
          }
        })
        .catch(function (error) {
          console.log(error);
          vm.$message.error('エラーが発生しました');
        })
        .finally(() => {
          vm.loading = false;
        });
    },
  },
};
</script>
<style scoped>
.image-container {
  width: 80%;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-top: 25px;
}

.upload {
  margin-right: 20px;
}

.upload:hover {
  color: #409eff;
}

.form {
  max-width: 720px;
  margin: 0 auto;
}
</style>