

// 请求首页数据
export const getData = () => {
    // 返回一个promise对象 /home/getData是后端接口名称
    return http.get('/home/getData')
}
