# movieInfoGen
使用[Rhilip/PT-help](https://github.com/Rhilip/PT-help)中movieInfoGen的API，添加了一些需要的小功能（如格式化种子文件名，通过种子文件名来查询影片之类的
主要用处是在发种时自动填写种子详情

###接口URL： 
> https://api.tongyifan.me/gen

###请求参数：
> 就一个参数[n]，来源是发布时的种子文件名，在upload.php中document.getElementById("torrent").value;即可获取

###其他的话：
如果解析不出来就看服务器心情返回数据/报错（你个辣鸡不写异常处理
然后这是我第一次用Python，各位大佬们轻拍
然后的然后，欢迎报bug欢迎pr

然后，没了
