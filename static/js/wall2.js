$(document).ready(function(){
    // if (precheck.length() > 2){
    $('#fname').keyup(function(){ // listen for when the #first_search element is submitted
        console.log($('#fname').val(), "daniel")
        var data = $('#first_search').serialize()
        var precheck = $('#fname').val();
        if (precheck.length > 0){
            $.ajax({
                method: 'POST',
                url: '/usersearch',
                data: data
            })
            .done(function(response){
                $('#first_name_message').html(response) 
            })
        }
    });
    $('#first_search').submit(function(){ // listen for when the #first_search element is submitted
        console.log('submit disabled')
        $.ajax({
            url: '/usersearch',
            method: 'POST',
            data: $('#first_search').serialize()
        })
        .done(function(response){
            // $('#first_name_message').html(response) // manipulate the dom when the response comes back
            console.log(response);
        })
        return false;  // return false to disable the normal submission of the form
    });
    $('#comment_form').submit(function(){ // listen for when the #first_search element is submitted
        console.log('submit disabled   hooray')
        var data = $('#comment_form').serialize()
        $.ajax({
            url: '/send_message',
            method: 'POST',
            data: data
        })
        .done(function(response){
            $('#comment_id').val('')
            console.log("response = ", response)
            $('#comment_sent').html(response) // manipulate the dom when the response comes back
            console.log(response);
        })
        console.log('ajax entered')
        return false;  // return false to disable the normal submission of the form
    });
    // ##############################################################################################################################
    // console.log("Hey, I'm ready!")
    // $('#deleted_form').click(function(e){ // listen for when the #first_search element is submitted
    //     e.preventDefault();
    //     console.log('submit disabled   hooray  :)')
    //     var data = $('#deleted_form').serialize()
    //     $.ajax({
    //         url: '/delete',
    //         method: 'POST',
    //         data: data
    //     })
    //     .done(function(response){
    //         console.log("response = ", response)
    //         $('#message_deleted').html(response) // manipulate the dom when the response comes back
    //         console.log(response);
    //     })
    //     console.log('ajax entered')
    //     return false;  // return false to disable the normal submission of the form
    // });
});