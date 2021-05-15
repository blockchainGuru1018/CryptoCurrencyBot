var AJAX = false;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(HEAD|OPTIONS|TRACE|POST)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

if (AJAX) {
  window.setInterval(function() {
    $.ajax({
      url: "{{ url('bitcoin_arbitrage:realtime_spreads') }}",
      type: "GET",
      success: function (response, data) {
        
        var $pread_body = $('.spread-body')
        var spreads = response.spreads;
        
        spreads.forEach(_spread => {
          
          var id = _spread.id;
          var spread = _spread.spread;
          var recorded_date = _spread.recorded_date;
          var exchange_buy = _spread.xchange_buy;
          var exchange_sell = _spread.xchange_sell;
          var exchange_buy_name = exchange_buy.name;
          var exchange_sell_name = exchange_sell.name;
          var exchange_currency_pair = exchange_buy.currency_pair;
          var exchange_buy_last_ask_price = exchange_buy.last_ask_price;
          var exchange_sell_last_bid_price = exchange_sell.last_bid_price;
          
          $pread_body.append($(
            `<tr>
              <td>${id}</td>
              <td>${spread}</td>
              <td>${exchange_buy_name}<br/>${exchange_buy_last_ask_price }</td>
              <td>${exchange_sell_name}<br/>${exchange_sell_last_bid_price}</td>
              <td>${recorded_date}</td>
              <td>${exchange_currency_pair}</td>
            </tr>`
          ))
        
        });

      },
      error: function (response, code, error) {
          if (error.toLowerCase() == "method not allowed"  && code == "error")  {
              console.log("Something went wrong with your request")
              return
          }
          var error = response.statusText;
          console.log(error)
      },
    });
  }, 5000)
}

$(function() {
    function update() {
        $.getJSON("",
            function(json){
            $('#finance').text(json.query.results.quote.Change);
        });
    }
    setInterval(update, 5000);
    update();
});


