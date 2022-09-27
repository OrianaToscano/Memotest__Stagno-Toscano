function login(){
  let login = document.getElementById("login").elements;
  let nombre = login["nombre"].value;
  let contra = login["contra"].value;

  if(/^[a-z0-9]+$/i.test(nombre) == false || /^[a-z0-9]+$/i.test(contra) == false){
    return alert('Deben completarse todos los datos del formulario')
  }else{
    console.log(nombre, contra)
    $.ajax({
      url:"/login", 
      type:"POST",
      data: {nombre:nombre, contra:contra},
      success: function(respuesta){
        if(respuesta == 'True' ){
           window.location = "https://memotest.orianatoscano.repl.co/juego";  
            alert('bienvenide ' + nombre)// es legal?
        }else{
            alert(respuesta)
        }
      },
      error: function(error){
        console.log(error);
    }, });
  }
};
