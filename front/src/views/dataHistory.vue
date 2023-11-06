<template>
    <div class="table">
        <div class="title">
            <span>数据历史查询</span> 
        </div>
        <el-card class="card">
        <el-table class="middle" :data="tableData" stripe border highlight-current-row
        :header-cell-style="{background:'#409EFF',color:'#FFFFFF'}">
            <el-table-column type="index" label="编号" width="100px"></el-table-column>
            <el-table-column  label="图像" align="center">
                <template slot-scope="scope">
                <img :src="scope.row.image" width="75" height="50" class="tableImg" @click="onpreview(scope.row.image)"/>
                <el-image-viewer
                    v-if="showviewer"
                    :on-close="closeviewer"
                    :url-list="urlList"
                    style="width: 80%; height: 80%; margin-left: 10%; margin-top: 5%"/>
                </template>

            </el-table-column>
            <el-table-column prop="name" label="图像名" align="center"></el-table-column>
            <el-table-column prop="createtime" label="检测日期" align="center"></el-table-column>
            <el-table-column prop="number" label="幼苗数" align="center"></el-table-column>
            <el-table-column prop="number" label="杂草数" align="center"></el-table-column>
            <el-table-column prop="number" label="缺苗数" align="center"></el-table-column>
            <!-- <el-table-column prop="remarks" label="备注" align="center"></el-table-column> -->
            <el-table-column
                fixed="right"
                label="操作"
                width="300">
                <template slot-scope="label">
                    <el-button  @click="deleteClick(label.row)"  type="text" size="small">删除</el-button>
                </template>
            </el-table-column>

        </el-table>

        <el-pagination
        @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="page"
                :page-sizes="[1,10,15,30,50]"
                :page-size="10"
                layout="total, sizes, prev, pager, next"
                :total="total" class="bottom">
        </el-pagination>
    </el-card>

    </div>



    
</template>

<script>
import elImageViewer from 'element-ui/packages/image/src/image-viewer'
export default{
    components: { elImageViewer },
    data() {
            return {
                showviewer: false,
                urlList: [],

                srcList:[],
                searchfile:"",
                download_type:"",
                oridialogVisible: false,
                resdialogVisible: false,
                dialogFormVisible: false,   
                editNotavailable:true,   
                page:1,
                total:0,
                allPage:0,
                size:10,
                formLabelWidth: '120px',
                form: {
                    data_file: '',
                    algorithm_types: '',
                    file_size: '',
                    created_time: '',
                    remarks: '',
                    username: '',
                    result_file: '',
                },
                tableData:[],
                searchForm: {
                    search:'',
                },          
                imgTypes:[
                {
                    value:'image.png',
                    name:'png'
                },
                {
                    value:'image.jpg',
                    name:'jpg'
                },
                ],
            }
        },


    mounted() {
    var url = "get_data_list/?page="+ this.page +"&size=" + this.size
    this.$http.get(url).then(response => {
        console.log(response.data)
            this.total = response.data.count;
            this.allPage = Math.ceil(this.total /this.size) ;
            this.tableData = response.data.results;

            })
    },   
    methods: {
                // 关闭查看器
        closeviewer() {
            this.showviewer = false
            this.urlList = []
        },
        onpreview(url) {
            this.urlList=[url]
            this.showviewer = true
        },
        handleSizeChange(val){
            this.size = val
            var url = "get_data_list/?search="+this.searchfile+"&page="+ this.page +"&size=" + this.size 
            this.$http.get(url).then(response => {
                this.total = response.data.count;
                this.allPage = Math.ceil(this.total /this.size) ;
                this.tableData = response.data.results;
                })
        },

        handleCurrentChange(val){
            this.page = val
            var url = "get_data_list/?search="+this.searchfile+"&page="+ this.page +"&size=" + this.size 
            this.$http.get(url).then(response => {
                this.total = response.data.count;
                this.allPage = Math.ceil(this.total /this.size) ;
                this.tableData = response.data.results;
                })
        },

        deleteClick(val){
            var msg = "确定删除？"
            if (confirm(msg)==true){ 
                console.log(val.id)
                var url = "get_data_list/?nid="+ val.id
                this.$http.post(url).then(response => {
                    var url = "get_data_list/?search="+this.searchfile+ "&page="+ this.page +"&size=" + this.size 
                    this.$http.get(url).then(response => {
                    this.total = response.data.count;
                    this.allPage = Math.ceil(this.total /this.size) ;
                    this.tableData = response.data.results;
                    })
                })
 
            }
            
        },

    downloadImage(tp) {
        var urls = ''
        if (tp == "ori"){
            urls = this.form.data_file
        }
        else{
            urls = this.form.result_file
        }
      if(this.download_type!="")
      {
        var xhr = new XMLHttpRequest();
      xhr.open('GET', urls, true);
      xhr.responseType = 'blob';
      xhr.onload = () => {
        var imgBlob = xhr.response;
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var img = new Image();
        var urlCreator = window.URL || window.webkitURL;
        img.onload = () => {
          canvas.width = img.naturalWidth;
          canvas.height = img.naturalHeight;
          ctx.drawImage(img, 0, 0);
          canvas.toBlob((blob) => {
            var imageUrl = urlCreator.createObjectURL(blob);
            var link = document.createElement('a');
            link.href = imageUrl;
            link.download = this.download_type;// 'image.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          },  this.download_type); // 指定转换后的图片格式
        };
        img.src = urlCreator.createObjectURL(imgBlob);
        };
            xhr.send();
            }
            else{
                alert("格式错误")
            }
            },
        handleClose(done) {
                this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => {});
            }

        },


}
</script>

<style scoped>

 .top{
    height: 5%;
    margin: 5px;

}
.card{
   
    background-color: #f6f7fb ;
}
.title{
    padding-left: 18px;
    height: 40px;
    background: white;
    font-weight: bold;
    align-self: center;
    line-height: 40px;
}
</style>