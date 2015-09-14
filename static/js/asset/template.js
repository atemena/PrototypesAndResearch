$(document).ready(function() {
      /**
       * Ensure images fill their container's dimensions
       * This should be called on all media gallery images once they have loaded
       */
      $('.hs_mediaGallery img:not(".hs_isProcessed")').one('load', function () {
        var $this = $(this);
        var $parent = $this.parent();
        var containerW = $parent.outerWidth();
        var containerH = $parent.outerHeight();
        var containerAspect = containerW / containerH;
        var imageAspect = $this.width() / $this.height();

        if (containerAspect < imageAspect) {
          $this.addClass('hs_reverseImageScaling');
        }

        // Do not process this image on subsequent checks
        $this.addClass('hs_isProcessed');
      }).each(function() {
        if (this.complete) $(this).load();
      });

      // Message controls drop down
      $('.hs_stream').on('click', '.hs_message .hs_messageOptions .hs_messageDropDownBtn', function (e) {
        e.preventDefault();
        $(this).parent().find('.hs_moreOptionsMenu').toggle();
      });

      $('.hs_stream').on('mouseleave', '.hs_message .hs_messageOptions .hs_moreOptionsMenu', function () {
        $(this).hide();
      });

      // Comment entry box
      var $commentContentText = $('.hs_commentContentText');
      var $commentEntryArea = $('.hs_commentEntryArea');

      $commentEntryArea.val($commentEntryArea.data('placeholder'))
        .on('focus', function () {
          $commentContentText.toggleClass('hasFocus');

          if ($commentEntryArea.val() === $commentEntryArea.data('placeholder')) {
            $commentEntryArea.val('');
          }
        }).on('blur', function () {
          $commentContentText.toggleClass('hasFocus');

          if ($commentEntryArea.val() === '') {
            $commentEntryArea.val($commentEntryArea.data('placeholder'));
          }
        });

      // Top bar controls and drop downs
      $('.hs_topBarControlsBtn').click(function(e) {
        e.preventDefault();

        var $this = $(this);
        var $previousButton = $('.hs_topBarControlsBtn').filter('.active');
        var $previousDropdown = $('.hs_topBarDropdown').filter('.active');
        var dropdownDataValue = $this.data('dropdown');
        var previousDropdownDataValue = '';

        // Hide the previous drop down
        if ($previousDropdown.length) {
          previousDropdownDataValue = $previousDropdown.data('dropdown');
          $previousDropdown.hide().removeClass('active');
          $previousButton.removeClass('active');
        }

        // Show the drop down associated with the clicked control button
        if (dropdownDataValue !== previousDropdownDataValue) {
          var $currentDropdown = $('.hs_dropdown' + dropdownDataValue);

          $this.addClass('active');
          $currentDropdown.addClass('active').show();

          if (dropdownDataValue == 'Search' || dropdownDataValue == 'WriteMessage') {
            $currentDropdown.find('input[type="text"]').first().focus();
          }
        }
      });
    });