<template>
  <div class="content">
    <div class="main">
      <el-card class="aside"  v-show="active != 3">
        <div style="height: 400px">
          <el-steps
            direction="vertical"
            :active="active"
            finish-status="success"
          >
            <el-step title="参数设置"></el-step>
            <el-step title="上传图像"></el-step>
            <el-step title="处理结果"></el-step>
          </el-steps>
        </div>
      </el-card>

      <el-card class="right">
        <el-form ref="form" :model="form" label-width="80px">
          <div class="info" v-if="active === 1">
            <p>参数设置</p>

            <el-form-item label="模型选择">
              <el-select v-model="form.AIDetector_pytorch" placeholder="请选择模型">
                <el-option v-for="(item,index) in AIDetector_pytorchTypes" :key="index" :label="item.name" :value="item.value"/>
              </el-select>
            </el-form-item>
          
              <el-form-item label="Conf_thres">
                    <el-col :span="15">
                    <el-slider 
                    v-model="form.Conf_thres" 
                    show-input
                    :min="0"
                    :max="1"
                    :step="0.01"
                    >
                    </el-slider>
                    </el-col>
              </el-form-item>
          </div>

          <div class="info" v-if="active === 2">
            <el-form-item label="上传文件">
              <el-upload
              class="upload-demo"
                ref="upload"
                drag
                
                action
                :http-request="httpRequest"
                accept=".jpg,.jpeg,.png," 
                :headers="headers" 
                :show-file-list="true"
                multiple
              >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <div class="el-upload__tip" slot="tip">
                  只能上传符合格式的文件
                </div>
              </el-upload>
            </el-form-item>
          </div>

          <div class="info" v-if="active === 3">
            <el-row :gutter="20">
              <el-col :span="8"><div class="grid-content">
                <div>
                      <h4>原始图像</h4>
                      <el-image 
                      style="width: 675px; height: 450px"
                      :src=original_img
                      ></el-image>
                    </div></div></el-col>
                    <el-col :span="4"><div class="grid-content">   </div></el-col>
                  <el-col :span="8"><div class="grid-content">   
                <div>
                  <h4>检测结果</h4>
                  <el-image 
                  style="width: 675px; height: 450px"
                  :src=result_img
                  :preview-src-list=[result_img]>
                    <div slot="placeholder" class="image-slot">
                      加载中<span class="dot">...</span>
                </div>
              </el-image>
              <!-- 添加文本信息 -->
              <p style="font-size: 20px; font-weight: bold; color: #333; line-height: 1.5em;">幼苗数：{{seedlingCount}}</p>
              <p style="font-size: 20px; font-weight: bold; color: #333; line-height: 1.5em;">杂草数：{{weedCount}}</p>
              <p style="font-size: 20px; font-weight: bold; color: #333; line-height: 1.5em;">缺苗数：{{missingCount}}</p>
            </div></div></el-col>

            </el-row>

        </div>
            <br>
                <el-form-item style="text-align: center">
                  <el-button type="primary" @click="next" v-if="active == 1"
                    >下一步</el-button
                  >
                  <el-button type="primary" @click="pre" v-if="active == 2"
                    >上一步</el-button
                  >
                  <el-button type="primary" @click="onSubmitF" v-if="active ==2"
                    >提交图片</el-button
                  >
                  <el-button type="primary" @click="pre" v-if="active ==3"
                    >重新检测</el-button>
                  <el-button type="primary" @click="dialogVisible = true" v-if="active ==3"
                    >保存图片</el-button>
                </el-form-item>
        </el-form>
      </el-card>


    </div>
    <div>
      <el-dialog
          title="提示"
          :visible.sync="dialogVisible"
          width="30%"
          :before-close="handleClose">
          <span>选择下载类型</span>
              <el-select v-model="download_type" placeholder="请选择类型">
                <el-option v-for="(item,index) in imgTypes" :key="index" :label="item.name" :value="item.value"/>
              </el-select>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="downloadImage">确 定</el-button>
          </span>
        </el-dialog>
    </div>


  </div>
</template>
  
<script>
import home from "./home.vue";
export default {
  components: { home },
  data() {
    return {
      fileList:[],
      tableData:"",
      sumnum:"",

      download_type:"",
      dialogVisible: false,
      fullscreenLoading: false,
      active:1,
      headers: { "Content-Type": "multipart/form-data" },
      form: {
          remarks: '',
          AIDetector_pytorch:'',
          data_file: '',
          username:'',
          Conf_thres:0,
      },
      AIDetector_pytorchTypes:[],
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
        original_img: require("@/assets/load.png"),
        result_img: require("@/assets/load.png"),
    };
  },
  mounted() {
    var url = "imgprocess/"
    this.$http.get(url).then(response => {
     var  algorith_list = response.data.weights_dict_list
      for (var i = 0; i < algorith_list.length;i++)
        {  
            this.AIDetector_pytorchTypes.push(
            {
              value:algorith_list[i],
              name:algorith_list[i],
            }
          )
        }
 })
    },   


  methods: {
    httpRequest(option) {
        this.fileList.push(option)
      },
      onSubmitF() {
        //上传文件的需要formdata类型;所以要转
        const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        this.form.data_file = this.fileList[0].file
        this.form.file_size = String(((this.fileList[0].file.size)/(1024*1024)).toFixed(2))+"MB"
        this.form.username = sessionStorage.getItem('username')
        console.log(this.form)
        this.$http({
        method: 'post',
        url: '/imgprocess/',
        headers:this.headers,
        timeout: 30000,
        data: this.form
        }).then(response=>{
          loading.close();
          if (response.status == 200){
            alert("模型上传成功")
            this.active = 3
            this.result_img =   response.data.result_img
            this.original_img =  response.data.original_img
            this.seedlingCount = response.data.seedlingCount
            this.weedCount = response.data.weedCount
            this.missingCount = response.data.missingCount
            this.tableData = response.data.image_info
            this.sumnum = response.data.num
            console.log("this.tableData,",this.tableData)
          }
          else{
            alert("上传失败")
          }
          console.log("response",response)
        })
        },
    next() {
      this.$refs.form.validate((valid) => {
        console.log(valid, "valid");
        if (valid) {
          if (this.active++ > 2) this.active = 0;
        }
      });
    },
    pre() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.active-- < 2) this.active = 1;
        }
      });
    },
    downloadImage() {
      if(this.download_type!="")
      {
        var xhr = new XMLHttpRequest();
      xhr.open('GET', this.result_img, true);
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
};
</script>
  
<style scoped>
.main {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  background-color: #f5f5f5;
}

.aside {
  background-color: #fff;
  margin-top: 30px;
  margin-right: 30px;
  margin-left: 30px;
  width: 200px;
  height: 800px;
}

.right {
  background-color: #fff;
  margin-left: 30px;
  margin-top: 30px;
  height: 800px;
  width: 1600px;
}

.right2 {
  background-color: #fff;
  margin-left: 30px;
  margin-top: 30px;
  height: 720px;
  width: 400px;
}
.inrightdiv {
  height: 550px;
  width: 400px;
}
.text1 {
  text-align: center;
  font-size: 20px;
}
.text2 {
  text-align: center;
  font-size: 14px;
  color: rgb(31, 30, 29);
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>