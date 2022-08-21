auto.waitFor();
var str = "";
var width = device.width;
var height = device.height;
str += "屏幕宽度:" + width;
str += "\n屏幕高度:" + height;
toast(str);

app.launchApp("微信");
toast("打开微信...");
sleep(2000);
className("android.view.View").text("四川大学微服务").findOne().parent().parent().parent().parent().click();
className("android.widget.TextView").text("微服务").findOne().parent().parent().click();
sleep(2000);
text("健康每日报").findOne().click();
sleep(2000);
swipe(width / 2, height - 600, width / 2, 0, 500);
runtime.requestPermissions(["access_fine_location"])
text("所在地点（请打开手机位置功能，并在手机权限设置中选择允许微信访问位置信息）").findOne().parent().click();
sleep(5000);
if(text("确定").exists()){
    text("确定").findOne().click();
}

var i = 4;
while(i --){
    swipe(width / 2, height - 600, width / 2, 0, 200);
}
text("提交信息").findOne().click();
sleep(200);
text("确定").findOne().click();
toast("结束")