<template>
    <el-header height="50px" class="header">
        <h3 class="title">
            甘蔗苗情检测系统
        </h3>
        <div class="info">
            <span class="show"><i class="el-icon-user"> {{user.username}} </i></span>
            
            <el-dropdown @command="handleCommand">
                <span class="el-dropdown-link">
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item icon="el-icon-user" command="c">修改信息</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-s-fold" command="q">退出系统</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </el-header>
</template>

<script>
    export default{
        data() {
            return {
                user:{
                    username:'',
                    gender:0
                },

            }
        },
        methods: {
            // getInfo(){
            //     const user=JSON.parse(localStorage.getItem('et2111elementui'))
            //     if(!user){
            //         this.$message({
            //             type:'error',
            //             message:'你还没有登录请先登录'
            //         })
            //         setTimeout(() => {
            //             this.$router.push('/')
            //         }, 1500);
            //         return
            //     }
            //     this.user=user
            // },
            handleCommand(command) {
                switch (command) {
                    case 'q':
                        sessionStorage.removeItem('token'),
                        sessionStorage.removeItem('username'),
                        this.$router.push('/')
                        break;
                    case 'c':
                        this.$router.push('/layout/profile')
                        break;
                    default:
                        break;
                }
            },
        },
        created() {
            this.user.username = sessionStorage.getItem('username')
        },
        
    }
</script>

<style scoped>
    .header{
        background-color: #409EFF;
        display: flex;
        /* 内侧的h2和div一左一右排列 */
        justify-content: space-between;
        align-items: center;
        /* 设置文字颜色 */
        color:whitesmoke;
    }

    .header .info{
        margin-right: 30px;
    }
        /* 下拉菜单  注意组件名可以直接使用，会自带class属性 */
    /* .el-dropdown {
        margin-left: 20px;
    } */
    .el-dropdown-link {
        color: white;
        cursor: pointer;
        font-weight: bolder;
    }
</style>