$(document).ready(function(){
    $('#emailchoice').keyup(function(){
        var data = $("#regForm").serialize() // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",
            url: "/email", // changed to email
            data: data
        })
        .done(function(res){
            $('#email_msg').html(res) // manipulate the dom when the response comes back
        })
    });
    // $('#fname').keyup(function(){ // listen for when the #first_search element is submitted
    //     console.log('keyup function')
    //     var data =$('#first_search').serialize()
    //     $.ajax({
    //         method: 'POST',
    //         url: '/usersearch',
    //         data: data
    //     })
    //     .done(function(response){
    //         $('#first_name_message').html(response) 
    //     })
    // });
    // $('#first_search').submit(function(){ // listen for when the #first_search element is submitted
    //     console.log('submit disabled')
    //     $.ajax({
    //         url: '/usersearch',
    //         method: 'POST',
    //         data: $('#first_search').serialize()
    //     })
    //     .done(function(response){
    //         $('#first_name_message').html(response) // manipulate the dom when the response comes back
    //         console.log(response);
    //     })
    //     return false;  // return false to disable the normal submission of the form
    // });
});
