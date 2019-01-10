$(document).ready(function() {
  var similarity_list = new Array()
  $('.similarity').each(function(index) {
    similarity_list.push($(this).text().replace('(', '').replace(')', '').split(',')[0])
    similarity_list.push($(this).text().replace('(', '').replace(')', '').split(',')[1])
  });

  var geo_dist_list = []
  $('.geo').each(function(index) {
    geo_dist_list.push($(this).text().replace('(', '').replace(')', '').split(',')[0]),
      geo_dist_list.push($(this).text().replace('(', '').replace(')', '').split(',')[1])

  });
  var geo_weight
  var geo_sim
  $('#submit_form').submit(function(e) {
    e.preventDefault()
    geo_weight = $('#input_geo_dist_weight').val(),
      sim_weight = $('#input_similarity_weight').val(),
    });

      for (var i = 0, l = similarity_list.length; i < l; i++) {
        for (var j = 0; j < geo_dist_list.length; j++) {

          if (geo_dist_list[j] == similarity_list[i]) {
            console.log(similarity_list[i]),
              console.log(geo_dist_list[j]),





          }

        }
      }





  console.log('-------*****----')


  $.ajax({
    type: 'post',
    data: $("#get_parameter").serialize(),
    success: function() {

    }
  });





});
