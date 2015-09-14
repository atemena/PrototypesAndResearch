$(document).ready(function() {
    hsp.init({
        useTheme: true
    });

    $('.addImage').click(function(){
        var time = new Date();
        var now = time.getTime();
        console.log('in add image hahah');
        var url = 'http://pbs.twimg.com/ext_tw_video_thumb/617807567532638208/pu/img/vn8cFYlweYb_CNGq.jpg';
        $.ajax({
            url: '/hootsuite/shaSign',
            data: {
                'timestamp': now,
                'url': url
            }
        }).done(function(response){
            hsp.attachFileToMessage ({
                url: url,
                name: 'dopeness',
                extension: 'jpg',
                timestamp: now,
                token: response.token
            });
        });
    })

    $('._message_send').click(function(){
        hsp.composeMessage($('._message_text').val());
    });

    $('._user_search').click(function(){
        hsp.showUser($('._user_text').val());
    });

    $('._composeMessage').click(function(){
        hsp.composeMessage('- sending from the new Appdirecoty SDK');
    });

    $('._retweet').click(function(){
        hsp.retweet('545327211298185217');
    });

    $('._showUser').click(function(){
        hsp.showUser('Hootsuite');
    });

    $('._getTwitterAccounts').click(function(){
        hsp.getTwitterAccounts(function(data){
            log('gettwitteraccounts', data);
        })
    });

    $('._showStatusMessage').click(function(){
        hsp.showStatusMessage('New Appdirectory SDK', 'INFO');
    });

    $('._clearStatusMessage').click(function(){
        hsp.clearStatusMessage();
    });

    $('._showFollowDialog').click(function(){
        hsp.showFollowDialog('Hootsuite', true);
    });

    $('._customUserInfo').click(function(){
        hsp.customUserInfo({
          "fullName": "David Chan",
          "screenName": "@chandavid",
          "avatar": "https://d1cmhiswqj5a7e.cloudfront.net/http%3A%2F%2Fplacehold.it%2F30x30%2F444",
          "profileUrl": "https://twitter.com/chandavid",
          "userLocation": "Vancouver, BC",
          "bio": "JavaScript/web/martini developer. Working on @Hootsuite. Making by breaking.",
          "extra": [
            {"label": "Age", "value": "Unknown"},
            {"label": "Gender", "value": "Male"}
          ],
          "links": [
            {"label": "Hootsuite", "url": "https://hootsuite.com"},
            {"label": "Blog", "url": "https://blog.hootsuite.com"}
          ]
        });
    });

    $('._showImagePreview').click(function(){
        hsp.showImagePreview( 
            'http://www.adweek.com/files/imagecache/node-blog/blogs/hootsuite-owl-holidays-hed-2014.jpg', 
            'http://ow.ly/G4OlN');
    });

    $('._updatePlacementSubtitle').click(function(){
        hsp.updatePlacementSubtitle('New Appdirectory SDK');
    });

    $('._showCustomPopup').click(function(){
        hsp.showCustomPopup('https://hootsuite.com/holidayowl?hootPostID=ab9f1ce42ce8f04cb6595fee079f099e', 'App Popup', 800, 600);
    });

    $('._closeCustomPopup').click(function(){
        hsp.closeCustomPopup('2x6zyxglj36s4ockg8c8s0k4o3ibhago7n4','82802');
    });

    $(document).on('click', '._compose', function() {
        var $messageBox = $(this).closest('._messageBox');
        hsp.composeMessage($messageBox.find('._content').text());
    });

    hsp.bind('sendcomposedmsgtoapp', function(message){
        console.log('received composed message:', message);
    });

    hsp.bind('dropuser', function(username, tweetId){
        $('.hs_topBar').after(messageTemplate({
            input: 'user ' + username + ' dropped',
            username: username,
            avatar: 'http://avatars.io/twitter/' + username,
            messageId: parseInt(1000000*Math.random(), 10) //generate random message ID for demonstration purposes
        }));
    });

    hsp.bind('sendtoapp', function(message){
        var userid = message.post.user.userid;
        var username = message.post.user.username;
        var avatar;
        if (message.post.network == 'twitter') {
            avatar = 'http://avatars.io/twitter/' + username;
        } else {
            avatar = 'http://avatars.io/facebook/' + userid;
        }
        

        $('.hs_topBar').after(messageTemplate({
            input: message.post.content.body,
            username: username,
            avatar: avatar,
            messageId: parseInt(1000000*Math.random(), 10) //generate random message ID for demonstration purposes
        }));
    });

    hsp.bind('sendprofiletoapp', function(profile){

        if (profile.network == 'TWITTER') {
            avatar = 'http://avatars.io/twitter/' + profile.screen_name;
        } else {
            avatar = 'http://avatars.io/facebook/' + profile.id;
        }

        $('.hs_topBar').after(messageTemplate({
            input: 'Profile received: ' + profile.name,
            username: profile.name,
            avatar: avatar,
            messageId: parseInt(1000000*Math.random(), 10) //generate random message ID for demonstration purposes
        }));
    });

    hsp.bind('sendassignmentupdates', function(data){
        var $messageBox = $('._message_' + data.messageId);
        $messageBox.attr('assignmentId', data.assignmentId);

        //Let's play with the colors
        if (data.status == "OPENED") {
            $messageBox.addClass('hs_message_assigned');
            var $currentMessageAssignment = $messageBox.find('._messageAssignment');
            if ($currentMessageAssignment.length) {
                $currentMessageAssignment.remove();
            }
            $messageBox.prepend(window.assignedTemplate({
                name: data.toName
            }));

        } else if (data.status == "RESOLVED") {
            $messageBox.addClass('hs_message_assigned');
            var $currentMessageAssignment = $messageBox.find('._messageAssignment');
            if ($currentMessageAssignment.length) {
                $currentMessageAssignment.remove();
            }
            $messageBox.prepend(window.resolvedTemplate({}));
        }


    });

    $(document).on('click', '._assign', function() {
        var $messageBox = $(this).closest('._messageBox');
        var params = {
            messageId: $messageBox.attr('messageId'),
            message: $messageBox.find('._content').text(),
            messageAuthor: $messageBox.find('._username').text(),
            messageAuthorAvatar: $messageBox.find('.hs_avatarImage').attr('src')
        };

        $messageBox.addClass('_message_' + params.messageId);
        hsp.assignItem(params);
    });

    $(document).on('click', '._resolve', function() {
        var $messageBox = $(this).closest('._messageBox');
        if (!$messageBox.attr('assignmentId')) {
            alert('Please assign this ticket before resolving it.');
            return;
        }

        var params = {
            assignmentId: $messageBox.attr('assignmentId')
        };

        hsp.resolveItem(params);

    });

    window.assignedTemplate = _.template(
        '<div class="hs_assignment _messageAssignment">' +
            '<span class="icon-app-dir x-assigned-on"></span>' +
            '<span class="notes _notes">Message assigned to <b><%= name%></b></span>' +
        '</div>');

    window.resolvedTemplate = _.template(
        '<div class="hs_assignment _messageAssignment">' +
            '<span class="icon-app-dir x-resolved-on"></span>' +
            '<span class="notes _notes">Message resolved</span>' +
        '</div>');

    window.messageTemplate = _.template(
        '<div class="hs_message _messageBox" messageId="<%= messageId%>">' +
            '<div class="hs_messageOptions">' +
                '<button class="hs_messageOptionsBtn icon-app-dir x-compose _compose" title="Compose"></button>' +
                '<button class="hs_messageOptionsBtn hs_messageDropDownBtn icon-app-dir x-ellipsis"></button>' +
                '<div class="hs_moreOptionsMenu">' +
                    '<a class="hs_moreOptionsMenuItem _assign" href="#"><span class="icon-app-dir x-assigned"></span>Assign</a>' +
                    '<a class="hs_moreOptionsMenuItem _resolve" href="#"><span class="icon-app-dir x-resolved"></span>Resolve</a>' +
                '</div>' +
            '</div>' +
            '<div class="hs_avatar">' +
                '<img class="hs_avatarImage" src="<%= avatar %>" alt="Avatar">' +
                '<a href="#" class="hs_avatarLink"></a>' +
            '</div>' +
            '<div class="hs_content">' +
                '<a href="#" class="hs_userName _username" title="Username"><%= username %></a>' +
                '<a href="#" class="hs_postTime hs_isNewMessage" target="_blank" title="Sunday, September 14 2014 at 12:00pm via Hootsuite">now</a>' +
                '<div class="hs_contentText _content">' +
                    '<p><%= input %></p>' +
                '</div>' +
            '</div>' +
        '</div>');
});





