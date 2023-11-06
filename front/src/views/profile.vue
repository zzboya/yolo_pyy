<template>
  <div class="content">
    <div class="main">
     

      <el-card class="right">
        <el-form ref="form" :model="userForm" :rules="regrules"  label-width="80px">
          <div class="info" >
            <el-form-item label="用户名">
              <el-col :span="9"> 
                <el-input v-model="userForm.username" :disabled="true"></el-input>
            </el-col>
            </el-form-item>
            <el-form-item label="电话">
              <el-col :span="9"> 
                <el-input v-model="userForm.phone" type='text'></el-input>
            </el-col>
            </el-form-item>
            <el-form-item label="邮件">
              <el-col :span="9"> 
                <el-input v-model="userForm.email" type='text'></el-input>
            </el-col>
            </el-form-item>
            <el-form-item label="旧密码">
              <el-col :span="9"> 
                <el-input v-model="userForm.password" type='password'></el-input>
            </el-col>
            </el-form-item>
            <el-form-item label="新密码">
              <el-col :span="9"> 
                <el-input v-model="userForm.newpassword" type='password'></el-input>
            </el-col>
            </el-form-item>
            <el-form-item label="确认密码">
              <el-col :span="9"> 
                <el-input v-model="userForm.reppassword" type='password'></el-input>
            </el-col>
            </el-form-item>
          </div>


          <el-form-item style="text-align: center">
            <el-button type="primary" @click="profile()"
              >修改信息</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>
  
<script>
import home from "./home.vue";
export default {
  components: { home },
  data() {
    var checkMobile = (rules,value,cb) => {
            const regMobile = /^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$/
    
            if(regMobile.test(value)){
              return cb()
            }
            cb(new Error('请输入合法的手机号'))
          }
        var  checkEmail = (rule, value, cb) => {
                let emailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;      
                if (emailReg.test(value) || value == '') {
                      return cb();                
                } 
                cb(new Error('请输入合法的邮箱'))
          }
    return {
      userForm: {
        username: '',
        password: '',
        newpassword:'',
        reppassword:'',
        email: '',
        phone: '',
      }, 

      regrules: {
        newpassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ],
        reppassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true,validator: checkEmail, trigger: "blur" } //
        ],
        phone: [
          { required: true, validator: checkMobile, trigger: "blur" }
        ],
      }

    };
  },
  mounted() {
    var url = "profile/?username="+sessionStorage.getItem('username')
    this.$http.get(url).then(response => {
       console.log(response.data)
       this.userForm.username = response.data.username;
       this.userForm.email = response.data.email;
       this.userForm.phone = response.data.phone;
    })
    }, 
  methods: {
    profile(){
      this.$refs.form.validate(valid => {
                if (!valid) return
                if (this.userForm.newpassword != this.userForm.reppassword)
                 {
                   alert("两次输入的密码不一致！");
                  return
                }
                this.$http.post('profile/',{
                  "username": this.userForm.username,
                  "password": this.userForm.password,
                  "newpassword": this.userForm.newpassword,
                  "email": this.userForm.email,
                  "phone": this.userForm.phone,
                }).then(response => {
                  if (response.data.msg == 'success')
                        {
                        alert("修改成功！请重新登录")
                        sessionStorage.removeItem('token'),
                        sessionStorage.removeItem('username'),
                        this.$router.push('/')
                        }
                    else
                        {
                          alert(response.data.msg)
                        }
                }).catch(error => {
                    {
                      alert('请核对账号密码并重试！')
                    }
                })
            })
        }
      },
  
};
</script>
  
<style scoped>
.main {
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
  height: 600px;
}

.right {
  background-color: #fff;
  margin-top: 30px;
  height: 600px;
  width: 960px;
}
.text1 {
  text-align: center;
  font-size: 20px;
}
.text2 {
  text-align: center;
  font-size: 14px;
  color: rgb(178, 169, 158);
}
</style>