var development = false;

var container;

function boot_seek(){
  mturk_blockbadworkers(boot);

}

$(document).ready(function() {
    mturk_ready(function() {
        mturk_blockbadworkers(boot);



    });
});

function isIE () {
  var myNav = navigator.userAgent.toLowerCase();
  return (myNav.indexOf('msie') != -1) ? parseInt(myNav.split('msie')[1]) : false;
}

function boot()
{
    console.log("Booting...");

    container = $("#container");

    if (isIE())
    {
        container.html("<p style='width:500px;'><strong>Sorry!</strong> This application does not currently support Internet Explorer. Please upgrade to a more modern browser to complete this HIT. We recommend <a href='http://www.google.com/chrome' target='_blank'>Google Chrome</a> or <a href='http://www.getfirefox.com' target='_blank'>Mozilla Firefox</a>.</p>");
        return;
    }

    var parameters = mturk_parameters();
    if (!parameters["id"])
    {
        brandingscreen();
        return;
    }

    if (!mturk_isassigned())
    {
        mturk_acceptfirst();
    }
    else
    {
        mturk_showstatistics();
    }

    mturk_disabletimer();

    function dispatch(training)
    {
        training = training ? 1 : 0;
        server_request("getjob", [parameters["id"], training], function(data) {
            loadingscreen(job_import(data));

        });
    }

    worker_isverified(function() {
        console.log("Worker is verified");
        dispatch(false);
        //alert(30);

    }, function() {
        console.log("Worker is NOT verified");
        dispatch(true);
    });
}

function build(job, callback){
    ui_build(job);
    setTimeout(callback, 100);

}

function loadingscreen(job)
{
    var ls = $("<div id='loadingscreen'></div>");
    ls.append("<div id='loadingscreeninstructions' class='button'>Show " +
        "Instructions</div>");
    ls.append("<div id='loadingscreentext'>Downloading the video...</div>");
    ls.append("<div id='loadingscreenslider'></div>");

    if (!mturk_isassigned())
    {
        ls.append("<div class='loadingscreentip'><strong>Tip:</strong> You " +
            "are strongly recommended to accept the task before the " +
            "download completes. When you accept, you will have to restart " +
            "the download.</div>");
    }

    ls.append("<div class='loadingscreentip'>You are welcome to work on " +
        "other HITs while you wait for the download to complete. When the " +
        "download finishes, we'll play a gentle musical tune to notify " +
        "you.</div>");

    container.html(ls);

    if (!development && !mturk_isoffline())
    {
        ui_showinstructions(job);
    }

    $("#loadingscreeninstructions").button({
        icons: {
            primary: "ui-icon-newwin"
        }
    }).click(function() {
        ui_showinstructions(job);
    });

    eventlog("preload", "Start preloading");

    preloadvideo(job.start, job.stop, job.frameurl,
        preloadslider($("#loadingscreenslider"), function(progress) {
            if (progress == 1)
            {
                if (!development && !mturk_isoffline())
                {
                    /*$("body").append('<div id="music"><embed src="magic.mp3">' +
                        '<noembed><bgsound src="magic.mp3"></noembed></div>');*/

                    window.setTimeout(function() {
                        $("#music").remove();
                    }, 2000);
                }

                ls.remove()

                build(job, function() {  go_seek_frame(); });

                mturk_enabletimer();

                eventlog("preload", "Done preloading");

            }
        })
    );

  var body = $("body");
  var minimum_reference = $("<div class='boundingbox ui-resizable ui-draggable ui-resizable-autohide' "
  +"aria-disabled='false' style='border-color: rgb(255, 0, 0); top: "
  +"132px; left: 85px; width: 23.5714px; height: 50.5714px; position: relative;'>"
	+"<div class='boundingboxtext' 'min_reference' style='display: "
  +"block; border-color: rgb(255, 255, 0);'>"
		+"<p>Minimum Reference</p>	</div>"
	+"<div class='fill' style='background-color: rgb(255, 0, 0);'></div>"
	+"<div class='ui-resizable-handle ui-resizable-n' style='z-index: 90; display: none;'></div>"
	+"<div class='ui-resizable-handle ui-resizable-w' style='z-index: 90; display: none;'></div>"
	+"<div class='ui-resizable-handle ui-resizable-s' style='z-index: 90; display: none;'></div>"
	+"<div class='ui-resizable-handle ui-resizable-e' style='z-index: 90; display: none;'></div></div>")
  body.append(minimum_reference);
   //go_seek_frame(0);
}

function brandingscreen()
{
    window.location.href = "/directory";



}
