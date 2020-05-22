function loadTweetContainer(tweetContainerID, fetchOneID) {
    console.log(myApp.staticUrl)
    const query = new URLSearchParams(window.location.search);
    let initial_url;
    let tweetContainer;

    if (tweetContainerID){
        tweetContainer = $("#" + tweetContainerID);
    } else {
        tweetContainer = $("#tweet-container");
    }

    initial_url = tweetContainer.attr("data-url") || '/api/tweet/';

    let tweetList = [];
    let nextTweetURL;

    function showAlert(message){
        var position = $('#customAlertContainer')
        var alertContent = '<div class="alert alert-warning alert-dismissible fade show" role="alert">' +
            '<strong>' + message + '!</strong> Un error ocurrio,' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
            '<span aria-hidden="true">&times;</span>' +
            '</button></div>'
        position.html(alertContent);
    }

    $(document.body).on("click", '#tweetLiked', function (event) {
        event.preventDefault();
        const this_ = $(this);
        const tweetId = this_.attr("data-id");
        const likedUrl = '/api/tweet/' + tweetId + '/liked/';

        $.ajax({
            method: "GET",
            url: likedUrl,
            success: function (data) {
                if(data.liked)
                    this_.text("Liked");
                else
                    this_.text("Unliked");
            },
            error: function (data) {
                console.log("error", data);
                showAlert(data.statusText);
            }
        })
    })

    $(document.body).on("click", '#retweetLink', function (event) {
        event.preventDefault();
        const url = "/api" + $(this).attr("href");
        $.ajax({
            method: "GET",
            url: url,
            success: function (data) {
                if (initial_url === "/api/tweet/") {
                    attachTweet(data, true);
                    updateHashLinks();
                }
            },
            error: function (data) {
                console.log("error", data);
                showAlert(data.statusText);
            }
        })
    })

    function updateHashLinks() {
        $('.media-body').each(function (data) {
            var hashTagRegex = /\B#(\w+)(?!.,;)/g;
            var userNameRegex = /\B@(\w+)(?!.,;)/g;
            var newText;

            newText = $(this).html().replace(hashTagRegex, "<a href='/tags/$1/'>#$1</a>");
            $(this).html(newText);

            newText = $(this).html().replace(userNameRegex, "<a href='/profiles/$1/'>@$1</a>");
            $(this).html(newText);
        })
    }

    function formatTweet(tweetValue) {
        let tweet;
        let container;
        let tweetUser;
        let tweetImage;
        let userImage;
        let tweetId = tweetValue.id;

        let preContent = "";

        let openingContainerDiv = '<div class="media">';

        if (tweetValue.id === fetchOneID){
            openingContainerDiv = '<div class="media media-focus">'
            setTimeout(function () {
                $('.media-focus').css("background-color", 'white')
            }, 2000)
        }

        if (tweetValue.parent){
            tweetUser = tweetValue.user.username;
            tweetId = tweetValue.parent.id;
            tweetValue = tweetValue.parent;
            preContent = '<span class="grey-color">@' +
                tweetUser + ' le metio leña</span><br/>'
        }

        let verb = 'Like';
        if (tweetValue.did_like)
            verb = 'Unlike'

        if(tweetValue.user.image != null){
            userImage = tweetValue.user.image;
        }
        else {
            userImage = myApp.staticUrl + '/default_avatar.jpg';
        }

        tweetImage = '<img src="' + userImage +
                '" style="height: 64px; width: 64px" class="align-self-center mr-3" ' +
                'alt="">';


        tweet = '<a href="' + tweetValue.user.url + '"><b>' +
            tweetValue.user.username + '</b></a><br/>' +
            tweetValue.content +
            '<p class="text-muted mt-1">' + tweetValue.date_display + '<p/>' +
            '<a class="mediaLink" href="/tweet/' + tweetId + '/">Ver</a> | ' +
            '<a class="mediaLink" id="retweetLink" href="/tweet/' + tweetId + '/retweet/">Quemar</a> | ' +
            '<a class="mediaLink" href="#" id="tweetLiked" data-id="' + tweetId + '">' +
            verb + '(' + tweetValue.likes +') </a>';


        container = openingContainerDiv + tweetImage +
            '<div class="media-body">' + preContent + tweet +
            '</div></div><hr/>';

        return container;
    }

    function attachTweet(tweetValue, preppend) {
        let tweetFormattedHTML;

        tweetFormattedHTML = formatTweet(tweetValue);

        if (preppend === true)
            tweetContainer.prepend(tweetFormattedHTML);
        else
            tweetContainer.append(tweetFormattedHTML);
    }

    function parseTweets() {
        if (tweetList === 0) {
            tweetContainer.text("No hay fuegos aun.");
        } else {
            // tweets exists
            $.each(tweetList, function (k, value) {
                if (value.parent) {
                    attachTweet(value, false);
                } else {
                    attachTweet(value);
                }
            });
        }
    }

    function fetchTweets(url) {
        let fetchURL;
        if (!url) {
            fetchURL = initial_url;
        } else {
            fetchURL = url;
        }
        $.ajax({
            url: fetchURL,
            data: {'q': query.get('q')},
            method: 'GET',
            success: function (data) {
                tweetList = data.results;
                if (data.next)
                    nextTweetURL = data.next;
                else
                    $('#loadMore').css('display', 'none');
                parseTweets();
                updateHashLinks();
            },
            error: function (data) {
                console.log("error", data);
                showAlert(data.statusText);
            }
        })
    }

    function fetchSingle(fetchOneID) {
        const fetchURL = '/api/tweet/' + fetchOneID + '/';
        $.ajax({
            url: fetchURL,
            method: 'GET',
            success: function (data) {
                tweetList = [data];
                parseTweets();
                updateHashLinks();
            },
            error: function (data) {
                console.log("error", data);
                showAlert(data.statusText);
            }
        })
    }

    if (fetchOneID){
        fetchSingle(fetchOneID);
    } else {
        fetchTweets();
    }


    $('#loadMore').click(function (event) {
        event.preventDefault();
        if (nextTweetURL) {
            fetchTweets(nextTweetURL);
        }
    })

    const tweetForm = $('#tweet-form');

    const charsStart = 320;
    let charsCurrent = 0;

    tweetForm.append("<span id='tweetCharsLeft'>" + charsStart + "</span>");

    $('#tweet-form textarea').keyup(function (event) {
        const tweetValue = $(this).val();
        const spanTweet = $('#tweetCharsLeft');
        charsCurrent = charsStart - tweetValue.length;
        spanTweet.text(charsCurrent);

        if (charsCurrent > 0) {
            spanTweet.removeClass("grey-color");
            spanTweet.removeClass("red-color");
        } else if (charsCurrent === 0) {
            spanTweet.addClass("grey-color");
            spanTweet.removeClass("red-color");
        } else if (charsCurrent < 0) {
            spanTweet.addClass("red-color");
            spanTweet.removeClass("grey-color");
        }
    })

    tweetForm.submit(function (event) {
        event.preventDefault();
        const this_ = $(this);
        const tweetData = $(this).serialize();

        if (charsCurrent >= 0) {
            $.ajax({
                url: '/api/tweet/create/',
                data: tweetData,
                method: 'POST',
                success: function (data) {
                    this_.find("input[type=text], textarea").val("");
                    $('#tweetCharsLeft').text(140);
                    attachTweet(data, true);
                    updateHashLinks();

                },
                error: function (data) {
                    console.log("error", data);
                    showAlert(data.statusText);
                }
            })
        } else {
            const message = "Muy Largo.";
            console.log("error", message);
            showAlert(message);
        }
    })
}