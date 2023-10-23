$(document).ready(function(){
    $('.btn-overlay').click(function(){
        let botWrapper = $('.bot-wrapper');
        
        if (botWrapper.css('display') === 'none') {
            botWrapper.css('display', 'flex');
        } else {
            botWrapper.css('display', 'none');
        }
    });
});