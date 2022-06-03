function validation() {
  const url = document.forms[0].keywords.value;
  const domain = url.split("/")[2];
  const domains = ["www.youtube.com", "m.youtube.com", "youtu.be"];
  if (url == "" || !domain in domains) {
    alert("YouTube動画のURLを入力してください");
    return false;
  } else {
    return true;
  }
}
