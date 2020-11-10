<template>
    <div>
        <el-button @click="visible = true">Button</el-button>
        <el-dialog :visible.sync="visible" title="Hello world">
            <p>Try Element</p>
        </el-dialog>
        <form>
            <input @change="selectedFile" type="file" name="file" multiple>
            <el-button @click="upload" type="submit">file upload</el-button>
        </form>
        <div v-for="datum in data" v-bind:key="datum.id">
            <img :src="datum.brobUrl" height="200">
            <p v-if="datum.result">{{ datum.result[0].AgeRange.Low }} - {{ datum.result[0].AgeRange.High }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Main',
    data: function () {
        return {
            visible: false,
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
                const file = files[i];
                const brobUrl = window.URL.createObjectURL(file);
                const result = "";
                data.push({id, file, brobUrl, result});
            }
            this.data = data;
        },
        upload: function () {

            // FormData を利用して File を POST する
            let formData = new FormData();
            for(let i = 0; i < this.data.length; i++) {
                formData.append('image-' + String(i), this.data[i].file);
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
                    for(let i = 0; i < response.data.length; i++) {
                        vm.data[i].result = response.data[i].result.FaceDetails;
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
