/***************************** Autocomplete ***************************/
$(function() {
    $( "#kingpin" ).autocomplete({
      source: function (request, response) {
                    $.ajax({
                        // type: "GET",
                        url: "/audience/queries/",
                        dataType: "json",
                        data: {
                            term: request.term
                        },
                        error: function (xhr, textStatus, errorThrown) {
                            // alert('Error: ' + xhr.responseText);
                            console.log('Error: ' + xhr.responseText);
                        },
                        success: function (data) {
                            response($.map(data, function (item) {
                                return {
                                    label: item.label,
                                    value: item.value
                                }
                            }));
                        }
                    });
                }
    });
  });

/***************************** Ajax Video Update ***************************/
function ajax_video_update(video_id, title, desc, thumb, saveButton, thumbParent, mainVideoTitle){
    var video_id = document.getElementById(video_id);
    var video_title = document.getElementById(title);
    var video_desc = document.getElementById(desc);
    var uploadButton = document.getElementById(saveButton);
    var fileSelect = document.getElementById(thumb);

    var hidden_video_title = document.getElementById('hidden-' + title);
    var hidden_video_desc = document.getElementById('hidden-' + desc);
    hidden_video_title.value = video_title.value;
    hidden_video_desc.value = video_desc.value;

    var main_video_title = $('#' + mainVideoTitle);
    main_video_title.text(video_title.value);


    if (fileSelect == null){
      var thumb_flag = false;
    }
    else{
      var thumb_flag = true;
      if(fileSelect.value == ""){
        thumb_flag = false;
      }
      else{
        $('#'+thumbParent).attr('style', 'display:none');
      }
    }
    uploadButton.innerHTML = 'Saving...';
            // sending form data    
            var myiframe = document.createElement('iframe');
            myiframe.setAttribute("name", "upload_iframe_myThumb");
            myiframe.setAttribute("id", "upload_iframe_myThumb");
             // name="upload_iframe_myThumb" id="upload_iframe_myThumb">
            myiframe.setAttribute("width", "0");
            myiframe.setAttribute("height", "0");
            myiframe.setAttribute("border", "0");
            myiframe.setAttribute("src","javascript:false;");
            myiframe.style.display = "none";
                        
            var form = document.createElement("form");
            form.setAttribute("target", "upload_iframe_myThumb");
            form.setAttribute("id", "myform_thumb_idsss");
            form.setAttribute("action", "/audience/ajax-handler/save_video_update");
            form.setAttribute("method", "post");
            form.setAttribute("enctype", "multipart/form-data");
            form.setAttribute("encoding", "multipart/form-data");
            form.style.display = "none";

            if(thumb_flag){
              form.appendChild(fileSelect);
            }
            form.appendChild(video_id);
            form.appendChild(hidden_video_title);
            form.appendChild(hidden_video_desc);
            document.body.appendChild(form);
            // form.prepend("{% csrf_token %}");
            document.body.appendChild(myiframe);
            iframeIdmyThumb = document.getElementById("upload_iframe_myThumb");
         
            // Add event...
            var eventHandlermyFile = function () {
                if (iframeIdmyThumb.detachEvent) 
                    iframeIdmyThumb.detachEvent("onload", eventHandlermyFile);
                else 
                    iframeIdmyThumb.removeEventListener("load", eventHandlermyFile, false);
                     
                response = getIframeContentJSON(iframeIdmyThumb);
                // uploaded_file_myFile(response);
                console.log(response);

              // $('#'+ videoDuration).text(eval(response).duration);
              // $('#'+ imgPreview).attr('style', 'display:none');
              // $('#'+ videoPreview).attr('style', 'display:initial');
              // $('#'+ videoPreview).attr('src', eval(response).video_path);

              // $('#'+ imgPreview).after('<input type="hidden" class="required" value="' + eval(response).video_path + '" name="video_path_'+ videoPreview[videoPreview.length - 1] +'">');

            }
                     
            if (iframeIdmyThumb.addEventListener) 
              iframeIdmyThumb.addEventListener("load", eventHandlermyFile, true);
            if (iframeIdmyThumb.attachEvent) 
              iframeIdmyThumb.attachEvent("onload", eventHandlermyFile);
            
         
            form.submit();
              uploadButton.innerHTML = 'Save';
          return;
}


/***************************** Ajax Video Upload ***************************/

function save_video(fileInput, saveButton, videoURL, videoDuration, videoPreview, imgPreview, youtubePreview, vimeoPreview){
    // event.preventDefault();
    var fileSelect = document.getElementById(fileInput);
    var uploadButton = document.getElementById(saveButton);
    var video_url = document.getElementById(videoURL);
    if(fileSelect.value =='' && video_url.value.trim() ==''){
        $('#errorForm').text(VIDEO_AND_URL_EMPTY);
        return;
    }
    else if(fileSelect.value !='' && video_url.value.trim() !=''){
      console.log(video_url.value.trim().toUpperCase());
      if(video_url.value.trim().toUpperCase() != "Insert URL (youtube or vimeo)".toUpperCase()){
        $('#errorForm').text(VIDEO_AND_URL_FILLED);
        return;
      }

    }

    // Update button text.
    uploadButton.innerHTML = 'Saving...';
    if(fileSelect.value == '' && video_url.value !=''){
        //save video url
        $('#'+ imgPreview).attr('style', 'display:none');

        if(video_url.value.indexOf("vimeo") > -1){
          // http://vimeo.com/102824093
          // <iframe src="//player.vimeo.com/video/102824093" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
          var mypath = video_url.value.split('/');
          mypath = '//player.vimeo.com/video/' + mypath[mypath.length - 1];
          $('#' + youtubePreview).attr('style', 'display:none');
          $('#' + videoPreview).attr('style', 'display:none');

          $('#' + vimeoPreview).attr('style', 'display:initial');
          $('#' + vimeoPreview).attr('src', mypath);
          $('#' + videoDuration).attr('style', 'display:none');
        }
        else if(video_url.value.indexOf("youtube") > -1){
          // youtube url
          //https://www.youtube.com/watch?v=eN9XX-dd0LQ
          // <iframe width="1280" height="720" src="//www.youtube.com/embed/80DJMfrW95U" frameborder="0" allowfullscreen></iframe>
          // get duration from ajax
            $.ajax({
                  url: '/audience/ajax-handler/save_video',
                  data: {data: "{'video_path': '" + video_url.value + "'}"},
                  type: 'POST',
                  success: function(data){
                    $('#'+ videoDuration).text(JSON.parse(data).duration);
                    console.log(data);
                  }
                });

          var mypath = video_url.value.split('=');
          mypath = 'https://www.youtube.com/v/' + mypath[mypath.length - 1];
          $('#' + videoPreview).attr('style', 'display:none');
          $('#' + vimeoPreview).attr('style', 'display:none');

          $('#' + youtubePreview).attr('src', mypath);
          $('#' + youtubePreview).attr('style', 'display:initial');
          // $('#' + videoDuration).attr('style', 'display:none');
        }
        else{
          $('#errorForm').text("Video URL not valid".toUpperCase());
          $('#'+ imgPreview).attr('style', 'display:initial');
        }

        
        uploadButton.innerHTML = 'Save';
        return;
    }
    // uploading a video clip
    if(!isAjaxUploadSupported()){
      // ajax upload not supported for IE
      console.log('Ajax upload not supported');
            var myiframe = document.createElement('iframe');
            myiframe.setAttribute("name", "upload_iframe_myFile");
            myiframe.setAttribute("id", "upload_iframe_myFile");
             // name="upload_iframe_myFile" id="upload_iframe_myFile">
            myiframe.setAttribute("width", "0");
            myiframe.setAttribute("height", "0");
            myiframe.setAttribute("border", "0");
            myiframe.setAttribute("src","javascript:false;");
            myiframe.style.display = "none";
                        
            var form = document.createElement("form");
            form.setAttribute("target", "upload_iframe_myFile");
            form.setAttribute("id", "myform_idsss");
            form.setAttribute("action", "/audience/ajax-handler/save_video");
            form.setAttribute("method", "post");
            form.setAttribute("enctype", "multipart/form-data");
            form.setAttribute("encoding", "multipart/form-data");
            form.style.display = "none";

            
            form.appendChild(fileSelect);
            document.body.appendChild(form);
            // form.prepend("{% csrf_token %}");
            document.body.appendChild(myiframe);
            iframeIdmyFile = document.getElementById("upload_iframe_myFile");
         
            // Add event...
            var eventHandlermyFile = function () {
                if (iframeIdmyFile.detachEvent) 
                    iframeIdmyFile.detachEvent("onload", eventHandlermyFile);
                else 
                    iframeIdmyFile.removeEventListener("load", eventHandlermyFile, false);
                     
                response = getIframeContentJSON(iframeIdmyFile);
                // uploaded_file_myFile(response);

              $('#'+ videoDuration).text(eval(response).duration);
              $('#'+ imgPreview).attr('style', 'display:none');
              $('#'+ videoPreview).attr('style', 'display:initial');
              $('#'+ videoPreview).attr('src', eval(response).video_path);

              $('#'+ imgPreview).after('<input type="hidden" class="required" value="' + eval(response).video_path + '" name="video_path_'+ videoPreview[videoPreview.length - 1] +'">');

              uploadButton.innerHTML = 'Save';
            }
                     
            if (iframeIdmyFile.addEventListener) 
              iframeIdmyFile.addEventListener("load", eventHandlermyFile, true);
            if (iframeIdmyFile.attachEvent) 
              iframeIdmyFile.attachEvent("onload", eventHandlermyFile);
            
         
            form.submit();

      return;
    }
    // Create a new FormData object.
    var formData = new FormData();
    var file = fileSelect.files[0];
    if (!file.type.match('video/mp4')) {
        uploadButton.innerHTML = 'Save';
        // alert('Unsupported format ! Use mp4 format !');
        $('#errorForm').text(UNSUPPORTED_VIDEO_FORMAT);
        return;
    }

    formData.append( fileInput, file );
    $.ajax({
      url: '/audience/ajax-handler/save_video',
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(data){
        $('#'+ videoDuration).text(JSON.parse(data).duration);
        $('#'+ imgPreview).attr('style', 'display:none');
        $('#'+ videoPreview).attr('style', 'display:initial');
        $('#'+ videoPreview).attr('src', JSON.parse(data).video_path);

        $('#'+ imgPreview).after('<input type="hidden" class="required" value="' + JSON.parse(data).video_path + '" name="video_path_'+ videoPreview[videoPreview.length - 1] +'">');

        uploadButton.innerHTML = 'Save';
      }
    });
    return;
}


function get_collection(name, topic){
    var name = $('#'+ name).val();
    var topic = $('#'+ topic +' option:selected').text();
    return {name: name, topic: topic}
}

function check_and_submit(){
    //event.preventDefault();
    // already added video may be deleted...
    for(i=1;i<video_count+1;i++){
      var fileSelect = document.getElementById('video-select-' + i.toString());
      var video_url = document.getElementById('url-' + i.toString());
      if(fileSelect.value !='' && video_url.value !=''){
        // alert('Either upload video or provide video url. Not both !');
        $('#errorForm').text(VIDEO_AND_URL_FILLED);
        return;
      }
    }
    $('input[name="redirect_field"]').val('default');
    $('#addContent').submit();
}

function validate_clips_and_submit(videos_count){
  if(parseInt(videos_count) == 0 ){
    $('#errorForm').text('You must add atleast one video !'.toUpperCase());
  }
  else{
    window.location.replace("/audience/addcontentaudience/");
  }
}

function isAjaxUploadSupported(){
  var input = document.createElement("input");
  input.type = "file";

  return (
      "multiple" in input &&
          typeof File != "undefined" &&
          typeof FormData != "undefined" &&
          typeof (new XMLHttpRequest()).upload != "undefined" );
}

function getIframeContentJSON(iframe){
  //IE may throw an "access is denied" error when attempting to access contentDocument on the iframe in some cases
  // try {
      // iframe.contentWindow.document - for IE<7
      var doc = iframe.contentDocument ? iframe.contentDocument: iframe.contentWindow.document,
          response;

      var innerHTML = doc.body.innerHTML;
      //plain text response may be wrapped in <pre> tag
      if (innerHTML.slice(0, 5).toLowerCase() == "<pre>" && innerHTML.slice(-6).toLowerCase() == "</pre>") {
          innerHTML = doc.body.firstChild.firstChild.nodeValue;
      }
      response = eval("(" + innerHTML + ")");
  // } catch(err){
      // response = {success: false};
  // }

  return response;
}