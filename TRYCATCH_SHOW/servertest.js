var express = require('express');
var app = express();

var server = require('http').createServer(app);
var path = require("path");

var WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({ port: 8181 });
    var client=null;
    var inter=null;
    var time=[];
    var data=[];
    wss.on('connection', function (ws) {
        console.log('client connection')
        client=ws;
        inter =setInterval(function(){
            data.push(Math.random());
            time.push(new Date().toLocaleTimeString());
            let msg ={
                chart:0,
                time:time,
                data:data
            }
            try {
                client.send(JSON.stringify(msg) );
            } catch (error) {
                console.log('disconnect')
            }
           
        },1000)
        ws.onmessage=function(message){
            // console.log('mss',message)
            var msg = JSON.parse(message.data);
            if(msg.event==1){
                clearInterval(inter);
                client=null;
            }
        }
        
        ws.on('close', function(close) {
            try{

            }catch(e){
                console.log('刷新页面了');
                client=null;
                time=[];
                data=[];
            }
        });

        ws.on('error', function(error) {
            try{

            }catch(e){
                console.log(error);
                client=null;
                time=[];
                data=[];
            }
        });


    })