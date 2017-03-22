/**
 * Created by mjansrud on 15.03.2017.
 */

$(function () {
    $(".menu").mouseover(function () {
        var id = $(this).data("hash");
        $(".attempt").each(function () {
            $(this).hide();
        });
        $("#" + id).show();
    });
    $(".new-attempt").click(function (e) {
        e.preventDefault();
        var link = this;
        bootbox.confirm({
            title: "Nytt forsøk?",
            message: "Du kan maks ha " + $(link).data("attempts") + " forsøk pr øving.",
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
                    window.location.href = link.href; // similar behavior as clicking on a link (Increments browser history)
                }
            }
        });
    }); 
    $(".menu.uncorrect").click(function (e) {
      e.preventDefault();
    });
});
