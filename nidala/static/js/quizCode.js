/**
 * Created by mjansrud on 15.03.2017.
 */

//Global variables
//Need to be able to cancel the interval
var interval;
var language

function configureEditor(lang, correct){

    //Set global variables
    language = lang;

    //Editor
    editor = ace.edit("editor");
    if(correct){
        editor.container.style.pointerEvents = "none"
        editor.container.style.opacity = 0.8
        editor.renderer.setStyle("disabled", true)
        editor.blur()
    }
    editor.getSession().setMode("ace/mode/" + language.toLowerCase());

    //Input
    input = ace.edit("input");
    input.container.style.pointerEvents = "none"
    input.container.style.opacity = 0.8
    input.renderer.setStyle("disabled", true)
    input.blur()
    input.getSession().setMode("ace/mode/" + language.toLowerCase());

    //Output
    output = ace.edit("output");
    output.container.style.pointerEvents = "none"
    output.container.style.opacity = 0.8
    output.renderer.setStyle("disabled", true)
    output.blur()

    switch (language) {
        case "PYTHON":
            language = 116;
            break;
        case "JAVA":
            language = 10;
            break;
        case "JAVASCRIPT":
            language = 35;
            break;
    }
}

//Create functions to be able to call the sphere engine API
$(function () {

    function createStatusMessage(message) {
        $("#submit").html('<i class="fa fa-cog fa-spin"></i> ' + message);
        output.getSession().setValue(message);
    }

    function fetchStatus(id) {
        createStatusMessage("Skaffer resultat ...")
        $.ajax({
            type: "GET",
            url: "http://aecae34f.compilers.sphere-engine.com/api/v3/submissions/" + id + "?access_token=27a39299db2cb8376648f2d1adc907ce&withOutput=true&withSource=true&withCmpinfo=true",
            success: function (result) {
                createStatusMessage("Validerer resultat ...")
                json = $.parseJSON(result);
                console.log(json);

                if (json.status == 0) {
                    //Submission has completed
                    clearInterval(interval);
                    $("#submit").attr("disabled", false);
                    if (json.output) {
                        output.getSession().setValue(json.output);
                        if ($("#answer").html() == String(json.output.replace(/[^a-z0-9\s]/gi, '')).trim()) {
                            $("#submit").html('<i class="fa fa-check"></i> Du svarte riktig!');
                        } else {
                            $("#submit").html('<i class="fa fa-times"></i> Du svarte feil!');
                        } 
                        textarea = $('textarea[name="answer"]');
                        textarea.html(String(json.output.replace(/[^a-z0-9\s]/gi, '')).trim());
                        $("#submit").off().trigger("click");
                    } else if (json.cmpinfo) {
                        output.getSession().setValue(json.cmpinfo);
                        $("#submit").html('<i class="fa fa-times"></i> Kompileringsfeil! Prøv igjen');
                    } else if (json.error && json.error != 'OK') {
                        output.getSession().setValue(json.error);
                        $("#submit").html('<i class="fa fa-times"></i> Feil! Prøv igjen');
                    } else if (!json.output) {
                        output.getSession().setValue("Tomt resultat");
                        $("#submit").html("Svar");
                    }
                }
            }
        });
    }

    $("#submit").click(function (event) {
        event.preventDefault();
        createStatusMessage("Oppretter innlevering ... ");
        $.ajax({
            type: "POST",
            url: "http://aecae34f.compilers.sphere-engine.com/api/v3/submissions?access_token=27a39299db2cb8376648f2d1adc907ce",
            data: {
                language: language,
                source: $("#usable").html() + '\n' + editor.getValue()
            },
            success: function (result) {
                $("#submit").attr("disabled", true);
                json = $.parseJSON(result);
                console.log(json);
                interval = setInterval(function () {
                    fetchStatus(json.id);
                }, 2000);
                createStatusMessage("Kompilerer ... id: " + json.id)
            }
        });

    });

});
