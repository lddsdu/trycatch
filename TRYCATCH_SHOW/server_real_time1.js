(function () {

    var express = require('express');
    var app = express();
    var http = require('http').Server(app);
    var server = require('socket.io')(http);
    var fs = require('fs');
    var nodePath = require('path');
    var chokidar = require('chokidar'); //监听文件变化
    var bodyParser = require('body-parser');
    var child_process = require('child_process');
    var mysql = require('mysql');
    var cookieParser = require('cookie-parser');



    //自己定义的router
    var index = require('./routes/index.js')();
    var sign = require('./routes/sign.js')();

    app.use(express.json({limit: '50mb'}));
    app.use(express.static('./'));
    // app.use(bodyParser.json());
    // app.use(bodyParser.urlencoded({ extended: false }));
    app.use(bodyParser.json({limit:"50mb"}));
    app.use(bodyParser.urlencoded({limit:'50mb',extended:true}));
    app.use(cookieParser());

   


    app.use('/', index);//对所有路径应用这个路由
    app.use('/', sign);//对登陆注册应用这个路由



    var log = console.log.bind(console);
    var jsonData = null;//需要实时传送的数据
    var child = null; //点击开始后创建的子进程
    var json_path = nodePath.resolve('./assets/output/json');//需要实时更新的json数据保存的文件夹路径
    var keyImg_path = nodePath.resolve('./assets/output/keyImg');//需要监听的关键图片(表格里的数据)文件夹;



    //保存前端发送的图片和json
    app.post('/saveInfo', function (req, res) {
        var imgData = req.body.imgData;//接收前台POST过来的base64
        var base64Data = imgData.replace(/^data:image\/\w+;base64,/, "");//过滤data:URL
        var dataBuffer = new Buffer(base64Data, 'base64');
        var img_url = "/home/intel/files/listen/" + req.body.username + ".png"; //根据username命名文件
        fs.writeFile(img_url, dataBuffer, function (err) { //写入图片
            if (err) {
                res.send({ "state": "false", err });
            } else {
                log(img_url + " : 保存成功");
                res.send({ "state": "ok" });
            }
        });

        var jsonUrl = "./out/json/" + req.body.username + ".json";
        var person = {};
        person.name = req.body.username;
        person.age = req.body.age;
        person.gender = req.body.gender;
        person.img = req.body.username + ".jpg";
        fs.writeFile(jsonUrl, JSON.stringify(person), function (err) {
            if (err) {
                log({ "state": "false", err });
            } else {
                log(jsonUrl + " : 保存成功");
            }
        })


    });

    
    //创建子进程
    function createChild() {
        log("python服务已经启动");
        child = child_process.spawn('bash', ['/home/intel/facereco_multiprocessing/start.sh']);

        child.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        child.stderr.on('data', (data) => {
            // res.send({ state: "false" });
            console.log(`stderr: ${data}`);
        });
    }
    //关闭子进程
    // function closeChild(child) { 
    //     log("python服务已经关闭");
    //     child.kill();
    // }

    function closeChild() {
        log("python服务已经关闭");
        close_child = child_process.spawn('bash', ['/home/intel/facereco_multiprocessing/stop.sh']);

        close_child.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        close_child.stderr.on('data', (data) => {
            // res.send({ state: "false" });
            console.log(`stderr: ${data}`);
        });
    }

    app.post('/cmd', function (req, res) {
        var start = req.body.start;
        if (start == "true") {
            try {
                createChild();
            } catch (error) {
                res.send({ state: "false",});
                log("启动python服务失败",error);
                return;
            }
            res.send({ state: "start" });
        }
        else {
            try {
                closeChild();
                // closeChild(child);
            } catch (error) {
                res.send({ state: "false",});
                log("关闭python服务失败",error);
                return;
            }
            res.send({ state: "off" });
        }

    })


    server.on('connection', function (socket) {
        console.log("开始一个连接");
        socket.on('disconnect', function () {
            console.log("一个连接断开");
        });
    });




    function watch_json_folder(filePath) {  //根据文件路径读取文件，返回文件列表

        var watcher = chokidar.watch(filePath, {
            ignored: /(^|[\/\\])\../,
            persistent: true
        });

        watcher.on('add', function (path) {
            log(`File ${path} has been added`);
            const re = /(.json)$/;  //判断json文件的正则表达式
            if (re.test(path)) { //只读取json文件

                try {
                    jsonData = JSON.parse(fs.readFileSync(path)); //读取json文件
                } catch (error) {
                    log("加入的json文件有误");
                }

                if (jsonData) {
                    var img_url = nodePath.basename(path).split("_")[0] + "_rendered.png"; //json对应的图片名
                    jsonData.date = Date.now(); //返回时间戳
                    jsonData.imgUrl = img_url;  //返回对应图片地址

                    if (server) { //保持连接状态的话就向客户端发送新添加的信息。
                        server.emit('message', jsonData);
                    }
                    else {
                        log("没有客户端连接,此时生成的信息将不能传输到客户端");
                    }
                }

            }
            
            else { //当传入其他文件时给出提示信息
                log("what you added is not a json format file");
                // data = fs.readFileSync(path);
            }

        });

        watcher.on('change', function (path) {
            log(`File ${path} has been changed`);
            const re = /(.json)$/;  //判断json文件的正则表达式
            if (re.test(path)) { //只读取json文件

                try {
                    jsonData = JSON.parse(fs.readFileSync(path)); //读取json文件
                } catch (error) {
                    log("加入的json文件有误");
                }

                if (jsonData) {
                    var img_url = nodePath.basename(path).split("_")[0] + "_rendered.png"; //json对应的图片名
                    jsonData.date = Date.now(); //返回时间戳
                    jsonData.imgUrl = img_url;  //返回对应图片地址

                    if (server) { //保持连接状态的话就向客户端发送新添加的信息。
                        server.emit('message', jsonData);
                    }
                    else {
                        log("没有客户端连接,此时生成的信息将不能传输到客户端");
                    }
                }

            }
            
            else { //当传入其他文件时给出提示信息
                log("what you changed is not a json format file");
            }

        });

    }


    function watch_keyImg_folder(filePath) {  //监听保存key img的文件夹,有新图片生成则把图片路径传给客户端

        var watcher = chokidar.watch(filePath, {
            ignored: /(^|[\/\\])\../,
            persistent: true
        });

        watcher.on('add', function (path) {
            log(`File ${path} has been added`);
            const re = /(.png)$/;  //判断png文件的正则表达式
            if (re.test(path)) { //只读取png文件

                if (server) { //保持连接状态的话就向客户端发送新添加的信息。
                    server.emit('keyImg', path);
                }
                else {
                    log("没有客户端连接,此时生成的信息将不能传输到客户端");
                }

            }

            else { //当传入其他文件时给出提示信息
                log("what you added is not a png format file");
            }

        });

        watcher.on('change', function (path) {
            log(`File ${path} has been changed`);
            const re = /(.png)$/;  //判断png文件的正则表达式
            if (re.test(path)) { //只读取png文件

                if (server) { //保持连接状态的话就向客户端发送新添加的信息。
                    server.emit('keyImg', path);
                }
                else {
                    log("没有客户端连接,此时生成的信息将不能传输到客户端");
                }

            }

            else { //当传入其他文件时给出提示信息
                log("what you changed is not a png format file");
            }

        });
    }


    http.listen(3000, function () {
        console.log('listening on *:3000');
    });

    watch_json_folder(json_path);//监听json文件夹
    watch_keyImg_folder(keyImg_path);//监听img文件夹




})();



