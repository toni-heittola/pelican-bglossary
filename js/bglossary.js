$(document).ready(function(){
    function search_clear(){
        $('#bglossary-search').val('');
        $(".alphabet").each(function(){
            $(this).fadeIn(100);
            var alphabet = $(this).data('alphabet');
            $(this).parent().find(".bglossary-item[data-alphabet='"+alphabet+"']").each(function(){
                $(this).fadeIn(100);
            });
        });
    }

    $('.bglossary-lang-selector').click(function (){
        var lang = $(this).data('lang');
        if($(this).hasClass('btn-default')){
            $(this).removeClass('btn-default');
            $('.'+lang).hide();
        }else{
            $(this).addClass('btn-default');
            $('.'+lang).show();
        }
    });

    $('.btoc-container a, .bglossary-container a').click(function (){
        search_clear();
    });

    $('#bglossary-search-clear').click(function (){
        search_clear();
    });

    $('#bglossary-search').keyup(function (){
        var filter = $(this).val();
        var count = 0;

        $("h1.alphabet").each(function(){
            var active_items = false;
            var alphabet = $(this).data('alphabet');

            $(this).parent().find(".bglossary-item[data-alphabet='"+alphabet+"']").each(function(){
                if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                    $(this).fadeOut(100);
                } else {
                    active_items = true;
                    $(this).fadeIn(100);
                    count++;
                }
            });

            $(".bglossary-item[data-alphabet='"+alphabet+"']").each(function(){
                //console.log($(this).text());
                if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                    $(this).fadeOut(100);
                } else {
                    active_items = true;
                    $(this).fadeIn(100);
                    count++;
                }
            });

            if(active_items){
                 $(this).fadeIn(100);
            }else{
                $(this).fadeOut(100);
            }
        });

        $("tr.alphabet").each(function(){
            var active_items = false;
            var alphabet = $(this).data('alphabet');

            $(".bglossary-item[data-alphabet='"+alphabet+"']").each(function(){
                if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                    $(this).fadeOut(100);
                } else {
                    active_items = true;
                    $(this).fadeIn(100);
                    count++;
                }
            });

            if(active_items){
                 $(this).fadeIn(100);
            }else{
                $(this).fadeOut(100);
            }
        });
    });
    search_clear();
});