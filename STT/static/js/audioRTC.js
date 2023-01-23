var isEdge = navigator.userAgent.indexOf('Edge') !== -1 && (!!navigator.msSaveOrOpenBlob || !!navigator.msSaveBlob);
 
 
var recorder; // globally accessible
var microphone;  // 麦克风
// 捕获麦克风
function captureMicrophone(callback) {
  console.log("捕获麦克风函数调用")
  if (microphone) {
      callback(microphone);
      return;
  }
  // 没有媒体设置告知版本低
  if (typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
      var sys = isAndroidOrIOSOrPc();
      if (sys == "pc") {
          layer.msg("该浏览器不支持语音录入，<br>请使用谷歌、火狐等主流浏览器。", { area: ['320px', '80px'] });
      } else if (sys == "ios") {
          layer.msg("该浏览器不支持语音录入，<br>请将您的IOS操作系统升级最新版本，并使用safari浏览器打开使用。", { area: ['320px', '80px'] });
      } else if (sys == "android") {
          layer.msg("该浏览器不支持语音录入，<br>请使用系统自带浏览器打开使用。", { area: ['320px', '80px'] });
      } else {
          layer.msg("您当前的操作系统不支持语音录入。", { area: ['300px', '50px'] });
      }
  }
 // 获取设备的录音权限
  navigator.mediaDevices.getUserMedia({
      audio: isEdge ? true : { echoCancellation: false }
  }).then(function(mic) {
    console.log("获取麦克风成功回调",mic)
      callback(mic);
  }).catch(function(error) {
    console.log("获取麦克风失败回调",error)
    layer.msg("该浏览器不支持语音录入。<br>或您拒绝了语音授权", { area: ['300px', '60px'] });
      // 禁用麦克风走这里-》禁用语音按钮
      // 按钮背景换成语音
      $("#recordMess").css({
        "background":"url(images/noyuyin.png) no-repeat center",
        "background-size":" 100% 100%",
        })
        $("#recordMess").attr('disabled',true);
        $('#chatform').children("#messCon").show();
        $('#chatform').children("#talkmess_btn").hide();
  })
}
// 开始录音
function startRec() {
 
    var options = {
        type: 'audio',
        numberOfAudioChannels: 1,
        checkForInactiveTracks: false,
        bufferSize: 4096,
        recorderType: StereoAudioRecorder
    };
   
    if (recorder) {
        recorder.destroy();
        recorder = null;
    }
    // recordre 实例
    recorder = RecordRTC(microphone, options);
    recorder.startRecording(); //开始录音
  };
  //停止录音的回调
function stopRecordingCallback() {
    // 
    console.log("停止录音回调")
        var internalRecorder = recorder.getInternalRecorder();
        console.log("停止录音回调internalRecorder",internalRecorder)
        // 左声道
        var leftchannel = internalRecorder.leftchannel;
        // 右声道
        var rightchannel = internalRecorder.rightchannel;
        console.log("左声道",leftchannel)
        console.log(("啦啦啦",internalRecorder.blob,window.URL||webkitURL).createObjectURL(internalRecorder.blob))
        console.log("internalRecorderBlob",internalRecorder.blob)
          // 将录音文件 以文件对象形式传给后端
        var form = new FormData()
        form.append("upfile",internalRecorder.blob,"recorder.wav");
        console.log("form",form)
        $.ajax({
          url: '后端接口地址',
          type:'POST',
          cache: false,
          processData: false,
          contentType: false,
          data: form,
          success: function(data){
            console.log("后端返回数据对象",data)
          // 根据数据进行具体操作
           
        
          },
          error:function (err) { 
            console.log("ajaxerr",err)
           }
      })
   
  }
  var flagvoice=false;	
  $("#recordMess").click(function() {
          if(flagvoice){
              $(this).css({
                  "background":"url(images/yuyin.png) no-repeat center",
                  "background-size":" 100% 100%",
              })
              $('#chatform').children("#messCon").show();
              $('#chatform').children("#talkmess_btn").hide();
              flagvoice=false;
          }else{
        $(this).css({
          "background":"url(images/wenben.png) no-repeat center",
          "background-size":" 100% 100%",
        })
        $('#chatform').children("#messCon").hide();
        $('#chatform').children("#talkmess_btn").show();
        flagvoice=true;
      }
      //  ---------------获取麦克风权限 START--------
      if (!microphone) {
        captureMicrophone(function(mic) {
          console.log("获取语音权限",mic)
            microphone = mic;
        });
        return;
      }
      //  ---------------获取麦克风权限 END--------
      })
      var posStart = 0;//初始化起点坐标
var posEnd = 0;//初始化终点坐标
//长按
	var btnElem=document.getElementById("talkmess_btn");//获取ID
	btnElem.addEventListener("touchstart", function(event) {
    event.stopPropagation(); // 阻止冒泡
		event.preventDefault();//阻止浏览器默认行为
		posStart = 0;
		posStart = event.touches[0].pageY;//获取起点坐标
    // btnElem.value = '松开 结束';
    btnElem.innerText = '松开 结束';
		$("#audiobg").show();
		// $("#audiobg>p").hide();
		console.log("start");
    console.log(posStart+'---------开始坐标');
    // 开始录音
    startRec()
	});
    btnElem.addEventListener("touchend", function(event) {
        event.stopPropagation();
            event.preventDefault();
            posEnd = 0;
            posEnd = event.changedTouches[0].pageY;//获取终点坐标
        // btnElem.value = '按住 说话';
        btnElem.innerText = '按住 说话';
            console.log("End");
            console.log(posEnd+'---------结束坐标');
            if(posStart - posEnd < 100 ){
                // $("#audiobg>p").hide();
                console.log("发送成功");
          // recStop()
          recorder.stopRecording(stopRecordingCallback);
            }else{
                // $("#audiobg>p").show();
                console.log("取消发送");
                console.log("Cancel");
            };
        $("#audiobg").hide();
        
        });
        // 获取文件名的随机字符串
function getRandomString() {
    if (window.crypto && window.crypto.getRandomValues && navigator.userAgent.indexOf('Safari') === -1) {
        var a = window.crypto.getRandomValues(new Uint32Array(3)),
            token = '';
        for (var i = 0, l = a.length; i < l; i++) {
            token += a[i].toString(36);
        }
        return token;
    } else {
        return (Math.random() * new Date().getTime()).toString(36).replace(/\./g, '');
    }
}
// 文件名
function getFileName(fileExtension) {
  var d = new Date();
  var year = d.getFullYear();
  var month = d.getMonth();
  var date = d.getDate();
  return 'RecordRTC-' + year + month + date + '-' + getRandomString() + '.' + fileExtension;
}
// 下载录音
function downloadRecording(){
  console.log("下载录音")
  if(!recorder || !recorder.getBlob()) return;
 
   
    var blob = recorder.getBlob();
    var file = new File([blob], getFileName('wav'), {
        type: 'audio/wav'
    });
    invokeSaveAsDialog(file); // 该方法在recorderRTC.js中已有
}
// 下载按钮绑定点击事件
var download = document.getElementById("download")
    download.addEventListener("click",function(){
      downloadRecording()
})
// 释放麦克风
function releaseMicrophone(){
    if(microphone) {
      microphone.stop();
      microphone = null;
    }
   
  }
  // 判断设备是否是ios
var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
//停止录音的回调
function stopRecordingCallback() {
  // --------此处省略结束录音回调函数，代码同上，仅追加对于ios的判断--------------
  if(isSafari){
    releaseMicrophone()
  }
}
// 开始录音
function startRec() {
    // -----------新增补充代码 start-------------
      if (!microphone) {
        captureMicrophone(function(mic) {
            microphone = mic;
            // click(btnStartRecording);
            startRec()
        });
        return;
      }
    // -----------新增补充代码 end-------------
      var options = {
          type: 'audio',
          numberOfAudioChannels: 1,
          checkForInactiveTracks: false,
          bufferSize: 4096,
          sampleRate:48000,
          recorderType: StereoAudioRecorder
      };
     
      if (recorder) {
          recorder.destroy();
          recorder = null;
      }
      // recordre 实例
      recorder = RecordRTC(microphone, options);
      recorder.startRecording(); //开始录音
    };