can_answer = true;
notes = false;
comments = false;

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
                    if ($('.comment.text').length) {
                        comments = true;
                        display()
                    }
                }
            });
        }
    });

    $('.note.toggle').click(function () {
        notes = !notes;
        display();
    });

    $('.comment.toggle').click(function () {
        comments = !comments;
        display();
    });

    $('.comment.back.button').click(function () {
        comments = false;
        display();
    });

    $('.noteabort').click(function () {
        notes = false;
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
    if (comments == 1) {
        $('.comment.section').css('position', 'relative').css('visibility', 'visible');
    } else {
        $('.comment.section').css('position', 'absolute').css('visibility', 'hidden');
    }
    if (notes == 1) {
        $('.notesection').css('position', 'relative').css('visibility', 'visible');
        $('.question.actions').css('position', 'absolute').css('visibility', 'hidden');
    } else {
        $('.notesection').css('position', 'absolute').css('visibility', 'hidden');
        $('.question.actions').css('position', 'relative').css('visibility', 'visible');
    }
}
