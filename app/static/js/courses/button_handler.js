$(function() {
    $('.btn_to_write').bind('click', function() {
        $('.btn_to_write').remove()
        let searchParams = new URLSearchParams(window.location.search)
        let param = searchParams.get('id')
        $.ajax({
            method: "POST",
            url: "/courses/add_to_course",
            dataType: 'json',
            data: { course_id: param }
            })
            .done(function(msgBackFromServer) {
                if (msgBackFromServer.status === 'success'){
                    // window.location = window.location.href
                    $(".psevdBot").html("Вы успешно записались на курс!");
                    $(".psevdBot").css({'color': '#D4D4D4'});
                    $(".psevdBot").show().fadeIn(300).delay(2000).fadeOut(400);
                }
                else{
                    alert('error')
                }
            });
    });
});