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


