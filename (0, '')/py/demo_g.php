<script type="text/javascript" src="jquery1.7.js"></script>
<script type="text/javascript" src="jquery.flot.min.js"></script>
<script type="text/javascript" src="jquery.flot.time.js"></script>
<script type="text/javascript" src="jshashtable-2.1.js"></script>
<script type="text/javascript" src="jquery.numberformatter-1.2.3.min.js"></script>
<script type="text/javascript" src="jquery.flot.symbol.js"></script>
<script type="text/javascript" src="jquery.flot.axislabels.js"></script>
<script>
    var data = [];
    var dataset;
    var totalPoints = 100;
    var updateInterval = 1000;
    var now = new Date().getTime();


    function GetData() {
        data.shift();

        while (data.length < totalPoints) {
            var y = Math.random()* 100;
            //var y = new Array();
	    //y.push(25);
	    //y.push(35);
	    //y.push(45);
	    //y.push(65);
	    //y.push(75);
	    //y.push(85);

	    //for (i = 0;  i < y.length;  i++)
	    //{
            var temp = [now += updateInterval, y];
            data.push(temp);
	    //}
        }
    }
 
    var options = {
        series: {
            lines: {
                show: true,
                lineWidth: 1.5,
                fill: true
            }
        },
        xaxis: {
            mode: "time",
            tickSize: [2, "second"],
            tickFormatter: function(v, axis) {
                var date = new Date(v);

                if (date.getSeconds() % 20 == 0) {
                    var hours   = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                    var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
                    var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

                    return hours + ":" + minutes + ":" + seconds;
                } else {
                    return "";
                }
            },
            axisLabel: "Time",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 10
        },
        yaxis: {
            min: 0,
            max: 100,
            tickSize: 5,
            tickFormatter: function(v, axis) {
                if (v % 10 == 0) {
                    return v;
                } else {
                    return "";
                }
            },
            axisLabel: "CPU loading",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        },
        legend: {
            labelBoxBorderColor: "#fff"
        },
        grid: {
            backgroundColor: "#000000",
            tickColor: "#008040"
        }
    };

    $(document).ready(function() {
        GetData();

        dataset = [{
            label: "CPU",
            data: data,
            color: "#00FF00"
        }];

        $.plot($("#flot-placeholder1"), dataset, options);

        function update() {
            GetData();

            $.plot($("#flot-placeholder1"), dataset, options)
            setTimeout(update, updateInterval);
        }

        update();
    });
</script>
<!-- HTML -->
<div id="flot-placeholder1" style="width:550px;height:300px;margin:0 auto"></div>