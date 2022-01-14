


const imageFilter = function (req: any, file: any, cb: any) {
    // accept image only
    if (!file.originalname.match(/\.(mp4)$/)) {
        req.params.file_error =`Only video files are allowed, extension must be .mp4!`;
        console.log(req.params.file_error);
        return cb(null,false, req.params.file_error);
    }
    req.params.validate = 1;
    cb(null, true,req.params.validate);
};

export { imageFilter }