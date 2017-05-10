$(function () {
    can_answer = true;
    note = false;

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
        note = !note;
        note_display();
    });

    $('.noteabort').click(function () {
        note = false;
        $('form textarea').val(original_note);
        note_display();
    });

    $('.notesave').click(function () {
        $('form').submit();
    });

    note_display();
});

function note_display() {
    if (note) {
        $('.question.actions').css('position', 'absolute').css('visibility', 'hidden');
        $('.notesection').css('position', 'relative').css('visibility', 'visible');
    } else {
        $('.notesection').css('position', 'absolute').css('visibility', 'hidden');
        $('.question.actions').css('position', 'relative').css('visibility', 'visible');
    }
}
