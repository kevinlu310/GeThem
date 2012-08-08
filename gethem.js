function showNeeds()
{
  if ($(".needs-zoom").find("a").text()=='>>')
  {
    $(".needs-list").width(840);
    $(".needs-zoom").find("a").text("<<");
    $(".provides-list").hide();
  }
  else
  {
    $(".needs-list").width(420);
    $(".needs-zoom").find("a").text(">>");
    $(".provides-list").show();
  }
}

function showProvides()
{
  if ($(".provides-zoom").find("a").text()=='<<')
  {
    $(".provides-list").width(840);
    $(".provides-zoom").find("a").text(">>");
    $(".needs-list").hide();
  }
  else
  {
    $(".provides-list").width(420);
    $(".provides-zoom").find("a").text("<<");
    $(".needs-list").show();
  }
}

