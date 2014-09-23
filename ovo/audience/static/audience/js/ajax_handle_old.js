
function ajax_request(s_handler, c_handler, input_data)
{
   $.ajax({
    type: "POST",
    url: "/audience/ajax-handler/" + s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}

function save_collection(name, topic){
	var name = $('#'+ name).val();
	var topic = $('#'+ topic +' option:selected').text();
	if (topic == 'Select topic for your collection.'){
		// alert('You must select a topic for your collection !');
		$('#errorForm').text(COLLECTION_TOPIC_EMPTY);
	}
	else{
		ajax_request("save_collection", 'save_collection_success', {data: "{'name': '" + name + "','topic': '" + topic +"'}"});
	}
}

function save_collection_success(data){
	$('#errorForm').text('');
	// $('#successForm').text('Collection saved !');
}

function add_new_video(){
	video_count = video_count + 1;


	$.ajax({
	    // type: "POST",
	    url: "/audience/country-api/",
	    
	    success: function(data) {
			var video_html = [];
			video_html.push('<!--video --><div class="addedVideo col-md-1" id="addedVideo-' + video_count.toString() +'"><div class="addedVideoName active"><p>Video title</p>');
			video_html.push('<a class="deleteVideo" onclick="delete_video(\'addedVideo-' + video_count.toString() +'\', \'video-preview-' + video_count.toString() +'\')">&mdash;</a></div><div id="video_' + video_count.toString() +'" class="videoitem col-md-1">');
			video_html.push('<fieldset><div class="border col-md-5"><input type="file" name="video-select-' + video_count.toString() +'" class="filebutton" value="upload" id="video-select-' + video_count.toString() +'"/>');
			video_html.push('</div><div class="col-md-4_5"><div class="col-md-10 center"><p>or</p></div><div class="col-md-9_10 border"><div class="col-md-9_10">');
			video_html.push('<input type="text" id="url-' + video_count.toString() +'" placeholder="Insert URL" class="url" autocomplete="off" name="video_url_' + video_count.toString() +'">');
			video_html.push('</div><div class="col-md-10 right"><a id="saveURL-' + video_count.toString() +'" class="save" onclick="save_video(\'video-select-' + video_count.toString() +'\', \'saveURL-' + video_count.toString() +'\', \'url-' + video_count.toString() +'\', \'video_duration_' + video_count.toString() +'\', \'video-preview-' + video_count.toString() +'\', \'img-preview-' + video_count.toString() +'\', \'youtube-preview-' + video_count.toString() +'\', \'vimeo-preview-' + video_count.toString() +'\')" name="video_save_' + video_count.toString() +'">Save</a>');
			video_html.push('</div></div></div></fieldset>');

			video_html.push('<div class="col-md-6"><select data-placeholder="Choose country to blacklist..." style="width:350px;" multiple class="chosen-select" id="blacklist_countries_' + video_count.toString() +'" name="blacklist_countries_' + video_count.toString() +'" >');
			var main_data = JSON.parse(data);
			var options_html = [];
			for(i=0;i<249;i++){
				options_html.push('<option value="' + main_data.data[i].code + '">'+ main_data.data[i].name +'</option>');
			// video_html.push('{% for each in all_countries %}<option value="{{each.code}}">{{each.name}}</option>{% endfor %}</select></div>');
			}
			var final_options_html = options_html.join('');
			video_html.push(final_options_html + '</select></div>');
			video_html.push('<br><br><div class="video col-md-4_7"><img src="/static/images/videopreview.jpg" id="img-preview-' + video_count.toString() +'">');
			video_html.push('<video width="530" height="316" controls id="video-preview-' + video_count.toString() +'" name="video-preview-' + video_count.toString() +'" style="display:none">');
			video_html.push('Your browser does not support the video tag.</video><iframe id="vimeo-preview-' + video_count.toString() +'" width="530" height="316" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="display:none"></iframe>');
		    video_html.push('<object id="youtube-preview-' + video_count.toString() +'" width="530" height="316" style="display:none"></object>');
			video_html.push('</div><div class="desc col-md-3_7"><div class="col-md-1">');
			video_html.push('<input type="text" class="required" id="video_title_' + video_count.toString() +'" name="video_title_' + video_count.toString() +'" placeholder="title" autocomplete="off">');
			video_html.push('<p class="time" id="video_duration_' + video_count.toString() +'">00:00:00</p><p class="dark">Description</p>');
			video_html.push('<textarea rows="4" cols="50" placeholder="Insert text" id="video_desc_' + video_count.toString() +'" name="video_desc_' + video_count.toString() +'"></textarea>');
			video_html.push('</div><div class="col-md-2"><p>Upload your thumb </p><input type="file" name="video-thumb-' + video_count.toString() +'" class="filebutton"/>');
			video_html.push('</div></div></div></div><!--end video-->');

			var final_video_html = video_html.join('');
			$('#addedVideos').append(final_video_html);
			$("#blacklist_countries_"+ video_count.toString()).chosen();
			// console.log(data);
	    }
	});
	

}

function delete_video(mainVideoDiv, videoElement){
	var video_path = $('#'+videoElement).attr('src');
	$('#'+mainVideoDiv).remove();
	ajax_request("delete_video", 'empty', {data: "{'video_path': '" + video_path + "'}"});
}

function set_video_details(video_title, video_description, video_path){
	$('#video-title').text(video_title);
	$('#video-description').text(video_description);
	$('#img-preview').attr('style', 'display:none');

	if(video_path.indexOf("vimeo") > -1){
		// http://vimeo.com/102824093
		// <iframe src="//player.vimeo.com/video/102824093" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
		var mypath = video_path.split('/');
		mypath = '//player.vimeo.com/video/' + mypath[mypath.length - 1];
		$('#youtube-preview').attr('style', 'display:none');
		$('#video-preview').attr('style', 'display:none');

		$('#vimeo-preview').attr('style', 'display:initial');
		$('#vimeo-preview').attr('src', mypath);
		$('#video-duration').attr('style', 'display:none');
	}
	else if(video_path.indexOf("youtube") > -1){
		// youtube url
		//https://www.youtube.com/watch?v=eN9XX-dd0LQ
		var mypath = video_path.split('=');
		mypath = 'https://www.youtube.com/embed/' + mypath[mypath.length - 1];
		$('#video-preview').attr('style', 'display:none');
		$('#vimeo-preview').attr('style', 'display:none');

		$('#youtube-preview').attr('src', mypath);
		$('#youtube-preview').attr('style', 'display:initial');
		$('#video-duration').attr('style', 'display:none');
	}
	else{
		// local video
		$('#youtube-preview').attr('style', 'display:none');
		$('#vimeo-preview').attr('style', 'display:none');

		$('#video-preview').attr('style', 'display:initial');
		$('#video-preview').attr('src', video_path);
		ajax_request("get_video_duration", 'video_duration_success', {data: "{'video_path': '" + video_path + "'}"});
	}


}

function video_duration_success(data){
	console.log(data);
	$('#video-duration').attr('style', 'display:initial');
	$('#video-duration').text(JSON.parse(data).duration);
}

function empty(){}