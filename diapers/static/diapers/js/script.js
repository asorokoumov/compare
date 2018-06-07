

  $(document).ready(function(){
    window.onload = function () {
        document.getElementById("search_form").reset();
    }
    $('select#brand').change(function(){
        brand_id = $(this).val();
        brand_name = $(this).text();
        request_url = '/get_series/' + brand_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                $('select#series').find('option').remove().end()
                    .append('<option value="-1">Серия</option>')

                $.each(data, function(key, value){
                    $('select#series').append($("<option></option>").text(value).val(key));
                });
            }
        })

        series_id = $('select#series').val()
        request_url = '/get_sizes/' + brand_id + '/' + series_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                $('select#size').find('option').remove().end()
                    .append('<option value="-1">Размер</option>')

                $.each(data, function(key, value){
                    $('select#size').append($("<option></option>").text(value).val(value));

                });
            }
        })
    })
    $('select#series').change(function(){
        series_id = $(this).val();
        brand_id = $('select#brand').val();
        request_url = '/get_brands/' + brand_id + '/' + series_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                $.each(data, function(key, value){
                    $('select#brand').val(key);
                    brand_id = key;
                    brand_name = $('select#brand').text();
                    series_val = $('select#series').val()

                    request_url = '/get_series/' + brand_id + '/';
                    $.ajax({
                        url: request_url,
                        success: function(data){
                            $('select#series').find('option').remove().end()
                                .append('<option value="-1">Серия</option>')

                            $.each(data, function(key, value){
                                $('select#series').append($("<option></option>").text(value).val(key));

                            $('select#series').val(series_val);
                            });
                        }
                    })

                });
            }
        })



        request_url = '/get_sizes/' + brand_id + '/' + series_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                $('select#size').find('option').remove().end()
                    .append('<option value="-1">Размер</option>')

                $.each(data, function(key, value){
                    $('select#size').append($("<option></option>").text(value).val(value));

                });
            }
        })
    })
});