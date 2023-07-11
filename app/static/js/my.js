// 生成uuid
function generateUUID() {
    let d = new Date().getTime();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
        d += performance.now(); // use high-precision timer if available
    }
    return 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
  }
  

//   时间格式化输出
function format_time(time) {
    if (time == '') {
        var now = new Date();
    } else {
        var now = new Date(time);
    }
    // 获取年月日 获取时分秒
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var date = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();

    // 格式化数据，补零操作
    if (month < 10) { month = '0' + month; }
    if (date < 10) { date = '0' + date; }
    if (hour < 10) { hour = '0' + hour; }
    if (minute < 10) { minute = '0' + minute; }
    if (second < 10) { second = '0' + second; }

    // 拼接字符串
    var timeString = year + '-' + month + '-' + date + ' ' + hour + ':' + minute + ':' + second;
    return timeString
}