<template>
  <div class="login_container">
    <h2 class="login-title" style="color: antiquewhite;">欢迎使用甘蔗苗情检测系统</h2>
    <div class="login_box" v-if="isLogin">
        <el-form ref="loginFormRef" class="loginForm" :rules="loginrules" :model="loginForm" >
        <!--用户名-->
        <el-form-item  prop="username">
            <el-input v-model="loginForm.username" prefix-icon="el-icon-user" placeholder="用户名"></el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type='password' prefix-icon='el-icon-lock' placeholder="密码"></el-input>
        </el-form-item>
        <!--按钮-->
        <el-form-item class="btns">
                 <el-button type="primary" round @click='negateLogin()'>去注册</el-button>
                 <el-button type="primary" round @click='login()'>登录</el-button>
         </el-form-item>
      </el-form>
    </div>
    <div class="reg_box"  v-if= "!isLogin" >
        <el-form ref="regFormRef" class="loginForm" :rules="regrules" :model="regForm" >
        <!--用户名-->
        <el-form-item  prop="username">
            <el-input v-model="regForm.username" prefix-icon="el-icon-user" placeholder="用户名"></el-input>
        </el-form-item>
        <!--密码-->
        <el-form-item prop="password">
          <el-input v-model="regForm.password" type='password' prefix-icon='el-icon-lock' placeholder="密码"></el-input>
        </el-form-item>
        <!--邮箱-->
          <el-form-item prop="email">
          <el-input v-model="regForm.email" type='text' prefix-icon='el-icon-thumb' placeholder="邮箱"></el-input>
      </el-form-item>
          <!--手机号-->
          <el-form-item prop="phone">
          <el-input v-model="regForm.phone" type='text' prefix-icon='el-icon-phone' placeholder="手机号"></el-input>
        </el-form-item>
        <!--按钮-->
        <el-form-item class="btns">
          <el-button type="primary" round @click='negateLogin()'>去登录</el-button>
            <el-button type="primary" round @click='register()'>注册</el-button>
         </el-form-item>
      </el-form>
    </div>

  </div>
</template>
<script>
import axios from 'axios'
export default {
  data () { 
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
      isLogin: true,
      loginForm: {
        username: '',
        password: '',
        method: 'login',
        code: '',
        verifycodetoken: ''
      },
      regForm: {
        username: '',
        password: '',
        email: '',
        phone: '',
        method: 'register',
        code: '',
        verifycodetoken: ''
      },
      // verifyCode: require('../assets/logo.png'),
      verifyCode: '',
      loginrules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ]
      },
      regrules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 8, message: '长度在 3 到 8 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, validator: checkEmail, trigger: "blur" }
        ],
        phone: [
          { required: true, validator: checkMobile, trigger: "blur" }
        ],
      }
    }
  },
    methods: {
      negateLogin(){
        console.log("this.$refs.isLogin：",this.isLogin)
        this.isLogin = !this.isLogin; 
      },
      register () {
            this.$refs.regFormRef.validate(valid => {
                if (!valid) return
                this.$http.post('register/',{
                  "username": this.regForm.username,
                  "password": this.regForm.password,
                  "email": this.regForm.email,
                  "phone": this.regForm.phone,
                }).then(response => {
                  if (response.status == '200')
                        {
                        alert(response.data.msg)
                        this.isLogin = !this.isLogin; 
                        }
                    else
                        {
                          console.log("response",response.msg)
                          alert('账号已被注册，请重试！')
                        }
                }).catch(error => {
                    {
                      alert('error:',error)
                    }
                })
            })
        },
        login () {
            this.$refs.loginFormRef.validate(valid => {
                if (!valid) return
                this.$http.post('login/',{
                  "username": this.loginForm.username,
                  "password": this.loginForm.password,
                }).then(response => {
                  if (response.status == '200')
                        {
                        const token = response.data.auth_token
                        axios.defaults.headers.common["Authorization"] = "Token " + token.$route
                        console.log("response：",response.data.auth_token)
                        sessionStorage.setItem("token", token)
                        sessionStorage.setItem("username", response.data.username)
                        const toPath =  '/layout/index'
                        this.$router.push(toPath)
                        
                        }
                    else
                        {
                          alert('请核对账号密码并重试！')
                        }
                }).catch(error => {
                    {
                      alert('请核对账号密码并重试！')
                    }
                })
            })
        }
    },

    }
  


</script>
<style>
.login_container {
    /* 设置整个容器绝对定位 */
        position: absolute;
        /* 设置宽度占满屏幕 */
        width:100%;
        /* 设置高度占满首屏，注意必须设置参照物*/
        height:100%;
        /* 设置div的背景图 no-repeat 图片如果不够宽度或者高度，不重复排列*/
        background: url("../assets/26494390-71f3-11ec-861d-cd043e9d91d3.jpg") no-repeat;
        /* 设置背景图的宽高 */
        background-size: 100% 100%;
        /* 设置背景图固定在div中，不随着浏览器的缩放而缩放 */
        background-attachment: fixed;
}
.login_box {
  width: 450px;
  height: 280px;
  background-color: rgba(255, 255, 255, 0.6);
  background-color: #FFFF;
  /* 设置边框圆角 数字越大 边框越圆，如果设置为50% 则变为圆球 */
  border-radius: 15px;
  position: absolute;
  left: 50%;
  top: 45%;
  transform: translate(-50%, -50%);
}
.login-title {
  position: absolute;
  left: 50%;
  top: 10%;
  transform: translate(-50%, -50%);
}
.btns {
        display: flex;
        justify-content: flex-end;
    }
    h2{
        text-align:center;
        color: #444;
        margin-bottom: 20px;
    }
.loginForm {
    position: absolute;
    bottom: 0px;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
}

.reg_box {
  width: 450px;
  height: 380px;
  background-color: rgba(255, 255, 255, 0.6);
  background-color: #FFFF;
  /* 设置边框圆角 数字越大 边框越圆，如果设置为50% 则变为圆球 */
  border-radius: 15px;
  position: absolute;
  left: 50%;
  top: 45%;
  transform: translate(-50%, -50%);
}

.regForm {
    position: absolute;
    bottom: 0px;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
}


</style>