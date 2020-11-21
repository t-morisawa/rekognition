<template>
    <div>
        <form>
            <el-input placeholder="TwitterJP" v-model="input"></el-input>
            <el-button @click="submit" type="submit">submit</el-button>
        </form>
        <div class="image-container">
            <div v-for="datum in data" v-bind:key="datum.img_url">
               <el-image 
                :src="datum.img_url"
                style="width: 200px; height: 200px"
                fit="contain"></el-image>
                <p v-if="datum.result && datum.result[0]">
                    {{ datum.result[0].AgeRange.Low }} - {{ datum.result[0].AgeRange.High }}
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Main',
    data: function () {
        return {
            input: '',
            data: [],
        }
    },
    methods: {
        submit: function () {
            const vm = this;
            this.$axios
                .get('http://localhost:8080/twitter/' + this.input)
                .then(function (response) {
                    // response.data.forEach(datum => {
                    //     vm.data.push({
                    //         "filename": datum.img_url,
                    //         "result": datum.result.FaceDetails,
                    //     });
                    // });
                    const res = response.data
                    Object.keys(res).forEach(function(key) {
                        var datum = this[key];
                        vm.data.push({
                            "img_url": datum.filename,
                            "result": datum.result.FaceDetails,
                        });
                    }, res);
                    console.log(vm.data)
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    }
}
</script>
<style scoped>
.image-container {
    width: 80%;
    margin: 0 auto;
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

.upload {
    margin-right: 20px;
}

.upload:hover {
    color: #409EFF;
}
</style>