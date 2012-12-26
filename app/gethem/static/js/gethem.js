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
    $(".provides-zoom").find("a").text("right");
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
		var data = jQuery.parseJSON(e.data);
		if (data.type == 'provide') {
			var doc = '<strong><a href=\"/u/'+data.user+'/\">'+data.user+'</a></strong><a href=\"/provides/'+data.pid+'\">&nbsp;'+data.title+'</a><small>&mdash; '+data.ts+'</small>';
			console.log(doc);
			//$(".post:begin").append(doc);
			var container = document.getElementById('provide_post');
			var newpost = document.createElement('li');
			newpost.innerHTML = doc;
			container.insertBefore(newpost, container.firstChild);
		}
		else if (data.type == 'need') {
			var doc = '<li><strong><a href=\"/u/'+data.user+'/\">'+data.user+'</a></strong><a href=\"/needs/'+data.pid+'\">&nbsp;'+data.title+'</a><small>&mdash; {{'+data.ts+'</small></li>';
			console.log(doc);
			//$(".post:begin").append(doc);
			var container = document.getElementById('need_post');
			var newpost = document.createElement('li');
			newpost.innerHTML = doc;
			container.insertBefore(newpost, container.firstChild);
		}
	};
	sock.onclose = function() {
		console.log('close');
	};		
}

