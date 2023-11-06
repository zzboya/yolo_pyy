<template>
    <el-container direction="vertical" class="layout-container">
        <app-header></app-header>
        <app-section></app-section>
    </el-container>
</template>

<script>
    import AppHeader from '../../components/AppHeader';
    import AppSection from '../../components/AppSection'
    export default {
        components:{
            AppHeader,
            AppSection,
        }
    }
</script>

<style>
    .layout-container{
        padding: 0;
        margin: 0;
        height: 100vh;
    }
</style>