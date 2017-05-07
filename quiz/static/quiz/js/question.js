$(function () {
    can_answer = true;

    $('.answer').click(function () {
        if (can_answer) {
            can_answer = false;
            button = $(this);
            $.ajax({
                type: "POST",
                url: '',
                data: {
                    'answer': $(this).html(),
                },
                success: function (data) {
                    if (data['correct']) {
                        button.addClass('green');
                        if (!$('.check.circle').length) {
                            $('.results .icon').remove();
                            $('.results').append('<i class="ui green check circle icon"></i>');
                        }
                    } else {
                        button.addClass('red');
                        if (!$('.results .icon').length) {
                            $('.results').append('<i class="ui red remove circle icon"></i>');
                        }
                    }
                }
            });
        }
    });
});