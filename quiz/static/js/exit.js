/**
 * Created by mjansrud on 15.03.2017.
 */

$(function () {
    $(".result").click(function (e) {
        e.preventDefault();
        var link = this;
        bootbox.confirm({
            title: "Avslutt?",
            message: "Er du sikker på at du ønsker å avslutte? Du trenger minimum " + $(link).data("pass-percent") + "% riktig for å bestå.",
            buttons: {
                cancel: {
                    label: '<i class="fa fa-times"></i> Avbryt'
                },
                confirm: {
                    label: '<i class="fa fa-check"></i> Bekreft'
                }
            },
            callback: function (confirmed) {
                if (confirmed) {
                    window.location.href = link.href;
                }
            }
        });
    });
});
