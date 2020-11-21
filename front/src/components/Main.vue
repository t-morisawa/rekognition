<template>
    <div>
        <form>
            <label>
                <input @change="selectedFile" type="file" name="file" multiple style="display:none;">
                <span class="upload">file upload</span>
            </label>
            <el-button @click="upload" type="submit">submit</el-button>
        </form>
        <div class="image-container">
            <div v-for="datum in data" v-bind:key="datum.id">
               <el-image 
                :src="datum.brobUrl"
                style="width: 200px; height: 200px"
                fit="contain"></el-image>
                <p v-if="datum.result">{{ datum.result[0].AgeRange.Low }} - {{ datum.result[0].AgeRange.High }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Main',
    data: function () {
        return {
            data: [],
        }
    },
    methods: {
        selectedFile: function (e) {
            e.preventDefault();
            let files = e.target.files;
            // this.uploadFiles = files;
            let data = [];
            for(let i = 0; i < files.length; i++) {
                const id = i;
                const key = 'image-' + String(i);
                const file = files[i];
                const brobUrl = window.URL.createObjectURL(file);
                const result = "";
                data.push({id, key, file, brobUrl, result});
            }
            this.data = data;
        },
        upload: function () {

            // FormData を利用して File を POST する
            let formData = new FormData();
            for(let i = 0; i < this.data.length; i++) {
                formData.append(this.data[i].key, this.data[i].file);
            }

            let config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            };

            let vm = this
            this.$axios
                .post('http://localhost:8080', formData, config)
                .then(function (response) {
                    for(let i = 0; i < vm.data.length; i++) {
                        vm.data[i].result = response.data[vm.data[i].key].result.FaceDetails;
                    }
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