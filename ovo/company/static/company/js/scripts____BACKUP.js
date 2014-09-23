$( document ).ready(function() {
	/********************** CHOOSE SITES **************************/
	 $('#chooselists .item label').click(function() {
		$(this).parent().next().slideToggle('slow');
		$(this).parent().toggleClass('active');
		return false;
	}).parent().next().hide();
	
	//Deselect All
	$('.deselect').click(function(){
        $('input:checkbox').removeAttr('checked');
    });
	
	//Select All when Site selected
	$('.site').click(function(){
        $(this).$('input:checkbox').attr('checked','checked');
    });
	
	/*************************** FORM *****************************/
	//FORM VALIDATION	
	//CHECK EMPTY FIELDS ON SUMBIT
	// submit the form
	$('form').submit(function (e) {
		
		var error = 0;
		
		// loop through class name class="required"
		$('.required').each(function () {
			
			var self = $(this)
			// check shorthand if statement for input[type] detection
			var checked = (self.is(':checkbox') || self.is(':radio')) 
			? self.is(':not(:checked)') && $('input[name=' + self.attr('name') + ']:checked').length === 0 
			: false

			// run the empty/not:checked test
			if (self.val() === '' || checked) {
				self.addClass('error');
				error = 1;
			} else { self.removeClass('error'); } 
		})
		
		showError(error, 'errorForm');	
		
		if (error != 0) { 
			e.preventDefault();
		} 
	});
		
	//SHOW ERROR MESSAGE
	function showError(errornum,errorid){
		var diverror = document.getElementById(errorid);
		switch(errornum) {
			case 0:
				diverror.innerHTML = "";
				break;
			case 1:
				diverror.innerHTML = "Attention fill in all fields!";
				break;
		}
	}
	
	//ADD NEW WEBSITE FIELDS
	$(document).ready(function() {
		var InputsWrapper   = $("#websiteSections"); //Input boxes wrapper ID
		var AddButton       = $("#saveSection"); //Add button ID

		var x = InputsWrapper.length; //initlal text box count
		var FieldCount=1; //to keep track of text box added

		$(AddButton).click(function (e)  //on add input button click
		{
			FieldCount++; //text box added increment
			//add input box
			$(InputsWrapper).append('<div class="col-md-2"><input type="url" id="sectionurl'+ FieldCount +'" placeholder="URL"></div><div class="col-md-2"><input type="text" id="sectionname'+ FieldCount +'" placeholder="Section Name"></div>');
			return false;
		});

		$("body").on("click",".removeclass", function(e){ //user click on remove text
				if( x > 1 ) {
						$(this).parent('div').remove(); //remove text box
						x--; //decrement textbox
				}
		return false;
		}) 
	});
	
});