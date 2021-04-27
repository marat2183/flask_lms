$(function() {
    $('.append').bind('click', function() {
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
                    window.location = window.location.href
                }
                else{
                    alert('error')
                }
            });
    });
});