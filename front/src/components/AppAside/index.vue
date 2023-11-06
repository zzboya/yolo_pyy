<template>
    <!-- 菜单栏 -->
    <el-aside width="200px" class="aside">
        <el-menu :router="true" default-active="$route.path" @open="handleOpen" @close="handleClose"
        background-color="#2d3a4b" text-color="whitesmoke" active-text-color="#ffd04b">
            <!-- 首页 -->
            <el-menu-item index="/layout/index">
                <i class="el-icon-location"></i>
                <span>首页</span>
            </el-menu-item>
            <!-- 个人中心 -->
            <el-menu-item  index="/layout/profile">
                <i class="el-icon-user"></i>
                <span>个人中心</span>
            </el-menu-item>
            <!-- 图像增强 -->
            <el-menu-item  index="/layout/imageprocessing">
                <i class="el-icon-picture"></i>
                <span>甘蔗幼苗检测</span>
            </el-menu-item>

            <!-- 历史查询 -->
            <el-menu-item index="/layout/history">
                <i class="el-icon-data-line"></i>
                <span>信息查询</span>
            </el-menu-item>
        </el-menu>
    </el-aside>
</template>

<script>
    export default {
        methods:{
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            }
        }
    }
</script>

<style>
    .layout-container{
        padding: 0;
        margin: 0;
        height: 100%;
    }
    .aside{
        background-color: #2d3a4b;
        color:whitesmoke;
    }
    .el-menu {
        text-align: left;
        font-weight:900;
        /* 去掉侧边栏右侧的白边 */
        border-right:none ; 
        width:100%;
    }
</style>