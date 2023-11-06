<template>
    <el-container class="section">
        <app-aside></app-aside>
        <app-main></app-main>
    </el-container>
</template>

<script>
    import AppAside from '../AppAside'
    import AppMain from '../AppMain'
    export default{
        components:{
            AppAside,
            AppMain,
        }
    }
</script>

<style scoped>
    .section{
        display: flex;
        flex:1;
    }
</style>