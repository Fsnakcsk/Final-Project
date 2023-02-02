const putFile = file => {
    const albumBucketName = 'fsn-sound'; // S3의 버킷 이름
    const region = 'ap-northeast-2'; // 서울
    const accessKeyId = 'AKIAX2S4HYTUOY7MXY4O'; // IAM에서 생성한 사용자의 accessKeyId
    const secretAccessKey = 'lrY8n7fBFJZTDcRuGMyvHzVm4OUoBz'; // IAM에서 생성한 사용자의 secretAccessKey
    
    AWS.config.update({
      region,
      accessKeyId,
      secretAccessKey
    }); 
    
    const upload = new AWS.S3.ManagedUpload({
      params: {
        Bucket: albumBucketName,
        Key: file.name,
        Body: file,
        ACL: "public-read"
      }
    });
    
    const promise = upload.promise();
  
    promise.then(
      function(data) {
        console.log("Successfully uploaded photo.");
      },
      function(err) {
        return console.log("There was an error uploading your photo: ", err.message);
      }
    );
  };