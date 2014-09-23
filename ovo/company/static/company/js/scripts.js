$( document ).ready(function() {
        $('input, textarea').placeholder();
         /***************************** Auto hide error on focus ***************************/

        $('.required').on('focus', function(){
           if($(this).hasClass('error')) {
             $(this).removeClass('error');
           }
        });

        /***************************** DATE PICKER ***************************/
        $( '#startdate' ).datepicker();
        $( '#enddate' ).datepicker();
        $( '#sell-stratdate' ).datepicker();
        $( '#sell-enddate' ).datepicker();

        /************************* CUSTOM SCROLLBAR *************************/
        $('.scroll').customScrollbar();

        /****************************MY WIDGETS******************************/
        //toggle content
        $('#my-widgets .widget-type .widget-type-name p').click(function() {
                $(this).parent().next().slideToggle('slow');
                $(this).parent().toggleClass('active');
                return false;
        }).parent().next().hide();

        $('#my-widgets .widget-list .widget .bar p').click(function() {
                $(this).parent().next().slideToggle('slow');
                $(this).parent().toggleClass('active');
                return false;
        }).parent().next().hide();

        /***************************** CHECKBOX LIST ***************************/

        var open = false;
        $("span.checkboxes_tit").click(function () {
                if (open == false) {
                        $(this).closest('div').find('.checkboxes_list').fadeIn("fast");
                        open = true;
                } else {
                        $(this).closest('div').find('.checkboxes_list').fadeOut("fast");
                        open = false;
                }
        });
        $("ul.checkboxes_list li").click(function () {
                setTimeout(function(){
                $("ul.checkboxes_list").fadeOut();
                }, 250);
                open = false;
        });

        /****************************ADD WEBSITES******************************/
        //toggle content
        $('#addedSites .addedSiteName p').click(function() {
                $(this).parent().next().slideToggle('slow');
                $(this).parent().toggleClass('active');
                return false;
        }).parent().next().hide();

        //add sections
        // $('.addwebsitesections').click(function() {
        //      $currentElem  = $(this).parent().parent().find('.sections');
        //      if ($currentElem.hasClass('inactive')){
        //              $currentElem.switchClass('inactive','active');
        //      } else {
        //              $numElem = $currentElem.find('.addSection').length;

        //              $currentElem.append('<div class="addSection"><div class="col-md-2"><input class="required" type="url" id="sectionurl'+$numElem+'" placeholder="URL" autocomplete="off"></div><div class="col-md-2"><input class="required" type="text" id="sectionname'+$numElem+'" placeholder="Section Name" autocomplete="off"></div></div>');
        //      }
        // })
        /****************************ADD VIDEOS******************************/
        //toggle content
        $('#addedVideos .addedVideo .addedVideoName p').click(function() {
                $(this).parent().next().slideToggle('slow');
                $(this).parent().toggleClass('active');
                return false;
        }).parent().next().hide();

        /******************************* MENU *********************************/
        $('#choose_sites').click(function() {
                //Change active status in menu
                $(this).switchClass('inactive','active');
                $('#choose_content').switchClass('active','inactive').removeClass('completed');
                $('#choose_widgets').switchClass('active','inactive').removeClass('completed');

                //Change active status in columns
                $('#choose_sites_list').switchClass('inactive','active');
                $('#choose_widgets_list').switchClass('active','inactive');
                $('#choose_content_list').switchClass('active','inactive');

                //Hide child elements that are inactive
                hideShowElements();
        });
        $('#choose_content').click(function() {
                var selected_websites = $('.i-ws:checkbox:checked').map(function() {
                    return this.value;
                }).get();
                // var selected_websites = get_checked_list('i-ws');
                var selected_sections = $('.i-s:checkbox:checked').map(function() {
                    return this.value;
                }).get();

                // var selected_sections = get_checked_list('i-s');
                // var chk_arr = document.getElementsByClassName('i-s');
                // var chklength = chk_arr.length;
                // var selected_sections = [];
                // for(k=0;k< chklength; k++){
                //     if(chk_arr[k].checked == true){
                //         selected_sections.push(chk_arr[k]);
                //     }
                // }
                if (selected_sections.length == 0){
                    console.log('select atleast one video');
                    return;
                }
                else {
                //Change active status in menu
                $(this).switchClass('inactive','active');
                $('#choose_sites').switchClass('active','inactive');
                $('#choose_widgets').switchClass('active','inactive').removeClass('completed');

                //Change active status in columns
                $('#choose_content_list').switchClass('inactive','active');
                $('#choose_sites_list').switchClass('active','inactive');
                $('#choose_widgets_list').switchClass('active','inactive');

                //Hide child elements that are inactive
                hideShowElements();

                // $('input:checkbox:checked.site').each(function(){
                //     alert(this.value);
                // });
                // var valArray = $("input:checkbox:checked").serializeArray();
                // alert(valArray);

                // var selected_content_owners = $('.i-cp:checkbox:checked').map(function() {
                //     return this.value;
                // }).get();
                // var selected_content_owners = get_checked_list('i-cp');
                // var selected_collections = $('.i-c:checkbox:checked').map(function() {
                //     return this.value;
                // }).get();
                // var selected_collections = get_checked_list('i-c');
                // console.log(selected_websites);
                // console.log(selected_sections);
                // console.log(selected_content_owners);
                // console.log(selected_collections);
                }
        });

        function get_checked_list(className){
            var chk_arr = document.getElementsByClassName(className);
            var chklength = chk_arr.length;
            var new_list = [];
            for(k=0;k< chklength; k++){
                if(chk_arr[k].checked == true){
                    new_list.push(chk_arr[k]);
                }
            }
            return new_list;
        }
    
        $('#choose_widgets').click(function() {
                var selected_collections = $('.i-c:checkbox:checked').map(function() {
                    return this.value;
                }).get();
                // var selected_collections = get_checked_list('i-c');
                // var selected_sections = get_checked_list('i-s');
                // var chk_arr1 = document.getElementsByClassName('i-c');
                // var chklength1 = chk_arr1.length;
                // var selected_collections = [];
                // for(k=0;k< chklength1; k++){
                //     if(chk_arr1[k].checked == true){
                //         selected_collections.push(chk_arr1[k]);
                //     }
                // }
                // var chk_arr2 = document.getElementsByClassName('i-s');
                // var chklength2 = chk_arr2.length;
                // var selected_sections = [];
                // for(k=0;k< chklength2; k++){
                //     if(chk_arr2[k].checked == true){
                //         selected_sections.push(chk_arr2[k]);
                //     }
                // }

                // if (selected_sections.length == 0){
                //     console.log('select atleast one video');
                //     return;
                // }
                if (selected_collections.length == 0){
                    console.log('select atleast one website section');
                    return;
                }
                else {

                //Change active status in menu
                $(this).switchClass('inactive','active');
                $('#choose_content').addClass('completed').switchClass('active','inactive');
                $('#choose_sites').addClass('completed').switchClass('active','inactive');

                //Change active status in columns
                $('#choose_widgets_list').switchClass('inactive','active');
                $('#choose_sites_list').switchClass('active','inactive');
                $('#choose_content_list').switchClass('active','inactive');

                //Hide child elements that are inactive
                hideShowElements();
                }
        });

        /********************** CHOOSE SITES/CONTENT **************************/
        //Display child elements
        $('#chooselists .item label:first-child').click(function() {
                $(this).parent().next().slideToggle('slow');
                $(this).parent().toggleClass('active');
                return false;
        }).parent().next().hide();

        //Deselect All
        $('.deselect').click(function(){
        $(this).parent().find('.active input:checkbox').removeAttr('checked');

                $(this).parent().find('.checkbox-white').each(function () {
                                if($(this).hasClass("w-active")) {
                                        $(this).removeClass("w-active").addClass("w-no-active");
                                }
                });
    });

        //Toggle child elements checked state
        $('#chooselists .checkall').on('click', function () {
                $(this).closest('fieldset').find(':checkbox').prop('checked', this.checked);
                var no_active = $(this).closest('fieldset').find('.w-no-active').length;
                var active = $(this).closest('fieldset').find('.w-active').length;
                var total = $(this).closest('fieldset').find('.checkbox-white').length;


                if ( no_active >= 1 && no_active < total ) {
                        $(this).closest('fieldset').find('.checkbox-white').switchClass('w-active','w-no-active');
                } else if ( no_active >=  total ) {
                        $(this).closest('fieldset').find('.checkbox-white').switchClass('w-no-active','w-active'); }
                else if ( active >=  total ) {
                        $(this).closest('fieldset').find('.checkbox-white').switchClass('w-active','w-no-active'); }
        });

        //If an item is inactive, disable click.
        $('#chooselists .inactive .item label').click(function() { return false;});

        function hideShowElements(){
                //Hide child elements that are inactive
                $('#chooselists .inactive .item').next().hide();
                $('#chooselists .inactive input:checkbox').hide();
                $('#chooselists .inactive .item').removeClass('active');

                //Show child elements that are active
                $('#chooselists .active input:checkbox').show();
                $('#chooselists .active .item').show();
        }

        hideShowElements();

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
                        if (self.val().trim() === '' || checked) {
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
                                diverror.innerHTML = "Attention fill in all fields!".toUpperCase();
                                break;
                }
        }

        /****************************VIDEOS *********************************/
        //OVERLAY
        type = $(this).attr('data-type');




        //SELECT-DESELECT VIDEOS
        $('.deselect-vid').click(function(){
                $('input[type=checkbox]').each(function () {
                        $(this).removeAttr('checked');
                        });

                        $('.checkbox-white').each(function () {
                                if($(this).hasClass("w-active")) {
                                        $(this).removeClass("w-active").addClass("w-no-active");
                                }
        });
        });

        $('.select-vid').click(function(){
                         $('input:checkbox').prop('checked', this.checked);

                                $('.checkbox-white').each(function () {
                                        if($(this).hasClass("w-no-active")) {
                                                $(this).removeClass("w-no-active").addClass("w-active");
                                        }
                                });
        });


        $('.original-ch').each(function () {
                        $(this).css("opacity","0");
                });


        $('.checkbox-white').click(function(){
                        if($(this).hasClass("w-active")) {
                $(this).removeClass("w-active").addClass("w-no-active");
                } else {
                $(this).removeClass("w-no-active").addClass("w-active");
                }
        });

        $('.radio-white-button').click(function(){
                if($(this).siblings('.radio-white').hasClass("w-active-radio")) {
                        $(this).siblings('.radio-white').removeClass("w-active-radio").addClass("w-no-active-radio");
                } else {
                        $(this).siblings('.radio-white').removeClass("w-no-active-radio").addClass("w-active-radio");
                }
        });

        /*$('.checkboxes_list li label').click(function(){
                        if($(this).siblings('.radio-white').hasClass("w-active")) {
                $(this).siblings('.radio-white').removeClass("w-active").addClass("w-no-active");
                } else {
                $(this).siblings('.radio-white').removeClass("w-no-active").addClass("w-active");
                }
        });*/


        $('.select-sites').click(function(){
                 $('input:checkbox').prop('checked', this.checked);

                 $('.checkbox-white').each(function () {
                        if($(this).hasClass("w-active")) {
                                $(this).switchClass('w-active','w-no-active');
                        } else if ($(this).hasClass("w-no-active")) {
                                $(this).switchClass('w-no-active','w-active');
                        }
                });
        });


        $('ul.checkboxes-container').each(function () {
                        $(this).children().first().addClass('first-list-child');
         });


        //NUEVO
        $('.checkall-cam').on('click', function () {
                $(this).closest('fieldset').find(':checkbox').prop('checked', this.checked);


                var no_active = $(this).closest('fieldset').find('.w-no-active-radio').length;
                var active = $(this).closest('fieldset').find('.w-active-radio').length;
                var total = $(this).closest('fieldset').find('.radio-white').length;


                if ( no_active >= 1 && no_active < total ) {
                        $(this).closest('fieldset').find('.radio-white').switchClass('w-active-radio','w-no-active-radio');
                } else if ( no_active >=  total ) {
                        $(this).closest('fieldset').find('.radio-white').switchClass('w-no-active-radio','w-active-radio'); }
                else if ( active >=  total ) {
                        $(this).closest('fieldset').find('.radio-white').switchClass('w-active-radio','w-no-active-radio'); }
        });




});
