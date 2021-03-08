(function(){
    function pad(num, size) {
        var s = "000000000000" + num;
        return s.substr(s.length-size);
    }
    if (!String.prototype.format) {
      String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
          return typeof args[number] != 'undefined'
            ? args[number]
            : match
          ;
        });
      };
    }

    // Templates
    const dialogTemplate = Handlebars.compile(
        document.getElementById("dialog-template").innerHTML);
    const inputModelNameTemplate = Handlebars.compile(
        document.getElementById("input-modelName-template").innerHTML);

    $('form').on('submit', function(e) {
        console.log(e);
        const imageId = $('#input-imageId').val();
        const modelName = $('#input-modelName').val();
        const url = `/api/dialog/${imageId}?model=${modelName}`;
        $.getJSON(url, function(response) {
            $('#main').html(dialogTemplate(response.data[0]));
            // $('#response').html(JSON.stringify(response));
            // $('form')[0].reset();
        });
        e.preventDefault();
        return false;
    });
    
    // initialize Model select
    $.getJSON('/api/models', function(response) {
        $('#input-modelName').html(inputModelNameTemplate({models: response}));
    });
    
    // $.get('results/results.json', function(data) {
    //     var image_root = "/coco-images/val2014/";
    //     if (data.opts.sampleWords == 0)
    //         $('#heading').html('Encoder: ' + data.opts.encoder
    //                             + ', Decoder: ' + data.opts.decoder
    //                             + ', Beam size: ' + data.opts.beamSize
    //                             + '<br>' + 'Q-Bot: checkpoints/abot_rl.vd' //+ data.opts.qbot
    //                             + '<br>' + 'A-Bot: checkpoints/qbot_rl.vd'); //+ data.opts.abot);
    //     else
    //         $('#heading').html('Encoder: ' + data.opts.encoder
    //             + ', Decoder: ' + data.opts.decoder + ', Temperature: ' + data.opts.temperature);
    //
    //     var html = '';
    //     for (var i in data.data) {
    //         if (i % 4 == 0)
    //             html += "<div class='row'>"
    //         html += "<div class='col-xs-3'>"// + data.data[i].image_id
    //         html += "<img class='col-xs-12' src='{0}COCO_val2014_{1}.jpg'>".format(image_root, pad(parseInt(data.data[i].image_id), 12))
    //         html += "<p class='col-xs-12'; style='font-weight:400'><span> Caption: " + data.data[i].caption + "</span></p>"
    //         html += "<div class='col-xs-12'><ol style='margin-top:10px;'>"
    //         for (var j = 0; j < 10; j++) {
    //             html += "<li style='font-weight:400;'><span>" + data.data[i].dialog[j].question + "</span><span>" + data.data[i].dialog[j].answer + "</span></li>"
    //         }
    //         html += "</ol></div></div>"
    //         if (i % 4 == 3)
    //             html += "</div><hr>"
    //     }
    //     $('#main').html(html);
    // })
})();
