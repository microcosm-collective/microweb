(function(w,d,$,undefined){

  var FileHandler = (function(){

    function ArraytoFileList(files) {
      const dt = new DataTransfer();
      files.forEach(function (file) {
        dt.items.add(file);
      })
      return dt.files;
    }

    var fileHandler = function(opts){

      if (typeof opts.el !== 'undefined'){
        if (typeof opts.el === 'string'){
          this.el_name  = opts.el;
          this.$el      = $(this.el);
          this.el       = this.$el[0];
        }else if (typeof opts.el === 'object'){

          this.el      = opts.el;
          this.$el     = $(opts.el);
          this.el_name = '.'+this.el.className;

        }else{
          return false;
        }
      }

      if (typeof opts.dropzone !== 'undefined'){
        this.dropzone = opts.dropzone;
      }
      this.input = this.$el.find('input[type=file]')[0];

      this.event_type = false;

      this.stack = [];
      this.bind();

      return this;
    };

    fileHandler.prototype.removeFile = function(index){
      var sf = this.stack.slice(index, index+1)[0];
      this.stack = this.stack.filter(function (i) {
        return i !== sf;
      });

      var files = Array.from(this.input.files).filter(function (f) {
        return !(sf.name === f.name && sf.size === f.size && sf.lastModified === f.lastModified);
      });

      this.input.files = ArraytoFileList(files);

      if(typeof this.onRemove !== 'undefined' && typeof this.onRemove === 'function'){
        this.onRemove(this.stack);
      }
    };

    fileHandler.prototype.clear = function(){
      this.stack = [];
      this.input.files = ArraytoFileList([]);
    };

    fileHandler.prototype.parse = function(filesRaw){

      var reader, callback;

      var files = filesRaw.filter(function (f) {
        var match = this.stack.find(function (sf) {
          return sf.name === f.name && sf.size === f.size && sf.lastModified === f.lastModified;
        });

        return !match;
      }.bind(this));

      if (files.length < 1){
        return;
      }

      this.callback_counter = files.length;

      // ugly way of keeping track of the reader.onload async events
      // we only want to call our ondragged callback when all "files" have been loaded
      callback = $.proxy(function(e,i){

        var modified_attachment;

        // instance of progressevent assumes readasDataurl was triggered
        if (e instanceof ProgressEvent){
          modified_attachment = $.extend({},files[i], {
            data: e.target.result,
            fileRef: files[i],
          });
          // we use Array.unshift here to push image files to the front of the stack (ie. opposite of Array.push)
          // this makes it easier when we render to html (ie. will render all images first, then non-images)
          this.stack.unshift(modified_attachment);
        } else {
          modified_attachment = $.extend({},files[i], {
            fileRef: files[i],
          });
          this.stack.push(modified_attachment);
        }

        this.callback_counter--;

        if (this.callback_counter <= 0){
          if(typeof this.onDragged !== 'undefined' && typeof this.onDragged === 'function'){
            this.onDragged(this.stack);
          }

          this.event_type = false;
          this.input.files = ArraytoFileList(this.stack.map(function(f) {
            return f.fileRef;
          }));
        }
      },this);


      // loops and reads through all files recieved, skips files which are not images
      for(var i=0,j=files.length;i<j;i++){
        if (files[i].type.match('image.*')){

          reader = new FileReader();

          // we want to call the callback but keep this context of "this" within this
          // object and pass through "i" as a counter
          reader.onload = (function(i){
            return function(e){
              callback(e,i);
            };
          })(i);

          reader.readAsDataURL(files[i]);
        }else{
          callback(files[i],i);
        }
      }

      return this;

    };

    fileHandler.prototype.onDragged = function(fn){
      if(typeof fn === 'function'){
        this.onDragged = fn;
      }
      return this;
    };

    fileHandler.prototype.onRemove = function(fn){
      if(typeof fn === 'function'){
        this.onRemove = fn;
      }
      return this;
    };

    fileHandler.prototype.clickHandler = function(e){
      // noop
    };

    fileHandler.prototype.changeHandler = function(e){
      if (!this.event_type){
        this.event_type = "changed";
        this.parse(Array.from(e.target.files));
      }
    };

    fileHandler.prototype.dragHandler = function(e){
      e.stopPropagation();
      e.preventDefault();
    };

    fileHandler.prototype.dropHandler = function(e){
      var fileList = e.originalEvent.dataTransfer.files;

      e.stopPropagation();
      e.preventDefault();

      if (!this.event_type){
        this.event_type = "dropped";
        this.input.files = fileList
        this.parse(Array.from(fileList));
      }
    };

    fileHandler.prototype.bind = function(){

      var events = [
        ['change',    'input[type=file]', 'changeHandler'],
        ['click',     'input[type=file]', 'clickHandler']
        // ['drop',      this.dropzone,      'dropHandler'],
        // ['dragover',  this.dropzone,      'dragHandler']
      ];

      for(var i in events){
        this.$el.on(events[i][0], events[i][1], $.proxy(this[events[i][2]], this) );
      }

      this.$el.on('dragover', $.proxy(this.dragHandler,this));
      this.$el.on('drop', $.proxy(this.dropHandler,this));

    };

    return fileHandler;

  })();

  window.FileHandler = FileHandler;

})(window, document, jQuery);
