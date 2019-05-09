var express = require('express');
var app = express();
var http = require('http').Server(app);
var server = require('socket.io')(http);
// var yaml = require('yamljs'); //解析yml文件
var fs = require('fs');
var path = require('path');
var bodyParser = require('body-parser');


app.use(express.static('./'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

var log = console.log.bind(console);


app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});


//保存前端发送的base64图片
app.post('/saveInfo', function (req, res) {
    //接收前台POST过来的base64
    var imgData = req.body.imgData;
    //过滤data:URL
    var base64Data = imgData.replace(/^data:image\/\w+;base64,/, "");
    var dataBuffer = new Buffer(base64Data, 'base64');
    var filename = "./out/"+req.body.username+".png";
    //根据username命名文件
    fs.writeFile(filename, dataBuffer, function (err) {
        if (err) { 
            res.send({"state":"false",err});
        } else {
            log(filename+" : 保存成功");
            res.send({"state":"ok"});
        }
    });
});


var data = null;//需要实时传送的数据
var filePath = path.resolve('./assets/output/json');//数据保存的文件夹路径



server.on('connection', function (socket) {
    fileDisplay(filePath, function (data) {
        server.emit('message', data);
        // console.log(data.date);
    });
});

http.listen(3000, function () {
    console.log('listening on *:3000');
});




function fileDisplay(filePath, mySendfile) {  //根据文件路径读取文件，返回文件列表
    var jsonArray = []; //保存json文件在文件夹中的索引
    var jsonIndex = 0;  //jsonArray的索引，从0开始

    fs.readdir(filePath, function (err, files) { //开始读取文件夹
        if (err) {
            console.warn(err)
        } else {

            files.forEach(function (filename, index) {  //遍历读取到的文件列表，筛选出json文件
                const re = /(.json)$/;
                var filedir = path.join(filePath, filename);
                if (re.test(filedir)) {
                    jsonArray.push(index); //保存json文件在对应文件夹中的索引
                }
            });


            (function my_readFile(index) {  //index为jsonArray的索引，jsonArray[index]为json文件在文件夹中的索引

                if (index == jsonArray.length) {
                    console.log("已经读完文件");
                    return;
                }
                var filedir = path.join(filePath, files[jsonArray[index]]); //得到json文件的绝对路径
                console.log(filedir);
                fs.stat(filedir, function (eror, stats) {
                    if (eror) {
                        console.warn('获取文件stats失败');
                    } else {
                        data = JSON.parse(fs.readFileSync(filedir)); //读取json文件
                        data.date = Date.now(); //返回时间戳
                        mySendfile(data); //回调函数
                    }
                });

                setTimeout(function () {
                    my_readFile(++index);
                }, 200)

            })(jsonIndex);
            //根据文件路径获取文件信息，返回一个fs.Stats对象
        }
    });
}
