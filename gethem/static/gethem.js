function showNeeds()
{
  if ($(".needs-zoom").find("a").text()=='right')
  {
    $(".needs-list").width(840);
    $(".needs-zoom").find("a").text("left");
    $(".provides-list").hide();
  }
  else
  {
    $(".needs-list").width(420);
    $(".needs-zoom").find("a").text("right");
    $(".provides-list").show();
  }
}

function showProvides()
{
  if ($(".provides-zoom").find("a").text()=='left')
  {
    $(".provides-list").width(840);
    $(".provides-zoom").find("a").text("left");
    $(".needs-list").hide();
  }
  else
  {
    $(".provides-list").width(420);
    $(".provides-zoom").find("a").text("left");
    $(".needs-list").show();
  }
}

function sse()
{
	var source = new EventSource('http://localhost:5000/notification');
	source.onmessage = function (e) {
		alert(e.data);
	};
	source.addEventListener('message', function(e){
		alert(e.data);
	}, false);
}

function sock_js()
{
	var sock = new SockJS('http://localhost:5000/notification');
	sock.onopen = function() {
		console.log('open');
	};
	sock.onmessage = function(e) {
		console.log('message', e.data);
		alert(e.data);
	};
	sock.onclose = function() {
		console.log('close');
	};		
}

