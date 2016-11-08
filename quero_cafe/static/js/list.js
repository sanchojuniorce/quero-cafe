(function($)
{
    $('.show-modal-delete').click(function(e)
    {
        var action = $(this).data('action');
        var modal = $('#modal-delete');

        e.preventDefault();

        modal.find('form').attr('action', action);
        modal.modal('show');
    });

    $('.show-modal-justificativa').click(function(e)
    {
        var justificativa = $(this).data('justificativa');
        var modal = $('#modal-justificativa');

        e.preventDefault();

        modal.find('.modal-body p').html(justificativa);

        modal.modal('show');
    });
})
(jQuery);