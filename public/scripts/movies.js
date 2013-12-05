(function ($) {
  $(function() {
    $("#dp1").datepicker();
    $("#dp2").datepicker();
    $("#ds1").slider();
    $("#ds2").slider();
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!

    var yyyy = today.getFullYear();
    if(dd<10){dd='0'+dd;} if(mm<10){mm='0'+mm;} today = mm+'-'+dd+'-'+yyyy;
    $("#dp2").val(today);
    $('#filter-btn').click(function(){
      var data = {};
      data['genre'] = $('#genre_select').val();
      data['start_date'] = $('#dp1').val();
      data['end_date'] = $('#dp2').val();
      data['critic_rating'] = $('#ds1').data('slider').getValue();
      data['audience_rating'] = $('#ds2').data('slider').getValue();
      $.get("/dvds", data, function(data){
        $('#results').empty();
        var json_data = JSON.parse(data);
        var str = '<table class="table table-striped table-bordered table-condensed">';
        $.each(json_data, function(key, value) {
          var movie_title = value.title.split('(')[0].split('/')[0];
          var torrent_magnet = "javascript:void(0)";
          var torrent_link = "javascript:void(0)";
          if (value.torrents !== undefined && value.torrents !== null){
            if (value.torrents[0] !== undefined && value.torrents[0] !== null){
              torrent_magnet = value.torrents[0].torrent_magnet;
              torrent_link = value.torrents[0].torrent_link;
            }
          }

          str = str+'<tr><td>'+ movie_title +'</td><td>' + new Date(
            value.dvd_release_date).toDateString() + '</td><td>'+
          value.critic_rating+'%</td><td>'+value.audience_rating+
          '%</td><td><a href="'+torrent_magnet+'"><img src="images/magnet_1.png"></a></td><td><a href="'+
          torrent_link+'"><img src="images/down.png" width="16" height="16"></a></td></tr>';
        });
        str = str+'</table>';
        $('#results').append(str);
      });
    });
  });
})(jQuery);

