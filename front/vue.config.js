module.exports = {
    lintOnSave: false, // 是否关闭eslint语法检查，默认 true, 警告仅仅会被输出到命令行，且不会使得编译失败。
    assetsDir: 'static',
    devServer: {
      host:"0.0.0.0",
      port:8085,
      proxy: 'http://localhost:5013/'
    }
  }