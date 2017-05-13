can_answer = true;
section = 0;

$(function () {
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

    $('.note.toggle').click(function () {
        if (section != 2) {
            section = 2;
        } else {
            section = 0;
        }
        display();
    });

    $('.comment.toggle').click(function () {
        if (section != 1) {
            section = 1;
        } else {
            section = 0;
        }
        display();
    });

    $('.comment.back.button').click(function () {
        section = 0;
        display();
    });

    $('.noteabort').click(function () {
        section = 0;
        display();
        $('form textarea').val(original_note);
    });

    $('.notesave').click(function () {
        $('form.note').submit();
    });

    $('.comment.submit').click(function () {
        $('form.comment').submit();
    });
});

function display() {
    if (section == 1) {
        $('.question.actions').css('position', 'absolute').css('visibility', 'hidden');
        $('.notesection').css('position', 'absolute').css('visibility', 'hidden');
        $('.comment.section').css('position', 'relative').css('visibility', 'visible');
    } else if (section == 2) {
        $('.question.actions').css('position', 'absolute').css('visibility', 'hidden');
        $('.comment.section').css('position', 'absolute').css('visibility', 'hidden');
        $('.notesection').css('position', 'relative').css('visibility', 'visible');
    } else {
        $('.notesection').css('position', 'absolute').css('visibility', 'hidden');
        $('.comment.section').css('position', 'absolute').css('visibility', 'hidden');
        $('.question.actions').css('position', 'relative').css('visibility', 'visible');
    }
}