function showNeeds()
{
  if ($(".needs-zoom").find("a").text()=='&rarr;')
  {
    $(".needs-list").width(840);
    $(".needs-zoom").find("a").text("&larr;");
    $(".provides-list").hide();
  }
  else
  {
    $(".needs-list").width(420);
    $(".needs-zoom").find("a").text("&rarr;");
    $(".provides-list").show();
  }
}

function showProvides()
{
  if ($(".provides-zoom").find("a").text()=='&larr;')
  {
    $(".provides-list").width(840);
    $(".provides-zoom").find("a").text("&rarr;");
    $(".needs-list").hide();
  }
  else
  {
    $(".provides-list").width(420);
    $(".provides-zoom").find("a").text("&larr;");
    $(".needs-list").show();
  }
}


