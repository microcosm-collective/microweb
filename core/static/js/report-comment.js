(function ($) {
  'use strict';

  var $modal = $('#modal-report-comment');
  var $form = $('#report-comment-form');
  var $type = $('#report-comment-type');
  var $note = $('#report-comment-note');
  var $submit = $form.find('.report-submit');
  var $cancel = $form.find('.report-cancel');
  var $close = $form.find('.report-close');
  var $actions = $form.find('.report-actions');
  var $error = $modal.find('.report-error');
  var $success = $modal.find('.report-success');
  var typesRequest = null;
  var activeButton = null;

  function showError(message) {
    $error.text(message).prop('hidden', false);
  }

  $(document).on('click', '.report-comment', function () {
    activeButton = $(this);
    $form.find('[name="commentId"]').val(activeButton.data('comment-id'));
    $note.val('');
    $error.prop('hidden', true).text('');
    $success.prop('hidden', true);
    $actions.prop('hidden', false);
    $close.prop('hidden', true);
    $type.empty().append($('<option>', {value: '', text: 'Loading reasons...'})).prop('disabled', true);
    $submit.prop('disabled', true);

    if (typesRequest) {
      typesRequest.abort();
    }

    $modal.modal('show');
    typesRequest = $.getJSON($form.data('types-url'))
      .done(function (data) {
        $type.empty().append($('<option>', {value: '', text: 'Choose a reason'}));
        $.each(data.reportTypes, function (_, reportType) {
          $type.append($('<option>', {value: reportType.key, text: reportType.title}));
        });
        $type.prop('disabled', false);
      })
      .fail(function (xhr, status) {
        if (status !== 'abort') {
          $type.empty().append($('<option>', {value: '', text: 'Reasons unavailable'}));
          showError((xhr.responseJSON && xhr.responseJSON.error) || 'Unable to load report reasons. Please try again.');
        }
      });
  });

  $type.on('change', function () {
    $submit.prop('disabled', !$type.val());
  });

  $form.on('submit', function (event) {
    var submitted = false;
    event.preventDefault();
    if (!$type.val()) {
      return;
    }

    $submit.prop('disabled', true).text('Submitting...');
    $error.prop('hidden', true).text('');
    $.ajax({
      url: $form.attr('action'),
      type: 'POST',
      data: $form.serialize()
    }).done(function () {
      submitted = true;
      $success.prop('hidden', false);
      $type.prop('disabled', true);
      $actions.prop('hidden', true);
      $close.prop('hidden', false);
      if (activeButton) {
        activeButton.text('Reported').prop('disabled', true);
      }
    }).fail(function (xhr) {
      showError((xhr.responseJSON && xhr.responseJSON.error) || 'Unable to submit this report. Please try again.');
    }).always(function () {
      $submit.text('Submit report').prop('disabled', submitted || !$type.val());
    });
  });
})(jQuery);
