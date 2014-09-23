/*
Author: Tristan Denyer (based on Charlie Griefer's original clone code, and some great help from Dan - see his comments in blog post)
Plugin and demo at http://tristandenyer.com/using-jquery-to-duplicate-a-section-of-a-form-maintaining-accessibility/
Ver: 0.9.4
Date: Aug 25, 2013
*/
$(function () {
    $('#btnAdd').click(function () {
        var num     = $('.clonedInput').length, // Checks to see how many "duplicatable" input fields we currently have
            newNum  = new Number(num + 1),      // The numeric ID of the new input field being added, increasing by 1 each time
            newElem = $('#entry' + num).clone().attr('id', 'entry' + newNum).fadeIn('slow'); // create the new element via clone(), and manipulate it's ID using newNum value
    
    /*  This is where we manipulate the name/id values of the input inside the new, cloned element
        Below are examples of what forms elements you can clone, but not the only ones.
        There are 2 basic structures below: one for an H2, and one for form elements.
        To make more, you can copy the one for form elements and simply update the classes for its label and input.
        Keep in mind that the .val() method is what clears the element when it gets cloned. Radio and checkboxes need .val([]) instead of .val('').
    */

        newElem.find('.inputurl').attr('id', 'ID' + newNum + '_url').attr('name', 'ID' + newNum + '_url').val('');

        newElem.find('.input_ln').attr('id', 'ID' + newNum + '_last_name').attr('name', 'ID' + newNum + '_last_name').val('');

        newElem.find('.inputsiten').attr('id', 'ID' + newNum + '_sitename').attr('name', 'ID' + newNum + 'sitename').val('');

        newElem.find('.inputusersxday').attr('id', 'ID' + newNum + '_usersxday').attr('name', 'ID' + newNum + '_usersxday').val('');

        newElem.find('.inputviewxday').attr('id', 'ID' + newNum + '_viewxday').attr('name', 'ID' + newNum + '_viewxday').val('');

        newElem.find('.inputusersxmonth').attr('id', 'ID' + newNum + '_usersxmonth').attr('name', 'ID' + newNum + '_usersxmonth').val('');

        newElem.find('.inputviewxmonth').attr('id', 'ID' + newNum + '_viewxmonth').attr('name', 'ID' + newNum + '_viewxmonth').val('');
		
        newElem.find('.inputsectionurl0').attr('id', 'ID' + newNum + '_sectionurl0').attr('name', 'ID' + newNum + '_sectionurl0').val('');
		
        newElem.find('.inputsectionname0').attr('id', 'ID' + newNum + '_sectionname0').attr('name', 'ID' + newNum + '_sectionname0').val('');


    // Insert the new element after the last "duplicatable" input field
        $('#entry' + num).before(newElem);
        $('#ID' + newNum + '_title').focus();

    // Enable the "remove" button. This only shows once you have a duplicated section.
        $('#btnDel').attr('disabled', false);
    });

    $('#btnDel').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this section? This cannot be undone."))
            {
                var num = $('.clonedInput').length;
                // how many "duplicatable" input fields we currently have
                $('#entry' + num).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                    if (num -1 === 1)
                $('#btnDel').attr('disabled', true);
                // enable the "add" button
                $('#btnAdd').attr('disabled', false).prop('value', "add section");});
            }
        return false; // Removes the last section you added
    });
    // Enable the "add" button
    $('#btnAdd').attr('disabled', false);
    // Disable the "remove" button
    $('#btnDel').attr('disabled', true);
});