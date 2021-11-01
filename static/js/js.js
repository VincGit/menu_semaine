console.log("test");

var checkBox = document.getElementById("id_form-0-libre_choix");
console.log("test");
checkBox.onchange = function(){
  if(this.checked){
    console.log("checked");
    window.location.href = '/menu/generer_menu';
  }else{
    console.log("Unchecked");
    window.location.href = '/menu/generer_menu';
  }
};