$(document).ready(function(){
    console.log("Hey, I'm ready!")
    $('#comment_id').submit(function(){ // listen for when the #first_search element is submitted
        console.log('submit disabled')
        var data = $('#comment_form').serialize()
        $.ajax({
            url: '/send_message',
            method: 'POST',
            data: data
        })
        .done(function(response){
            console.log("responsen = ", response)
            $('#comment_sent').html(response) // manipulate the dom when the response comes back
            console.log(response);
        })
        console.log('ajax entered')
        return false;  // return false to disable the normal submission of the form
    });
});