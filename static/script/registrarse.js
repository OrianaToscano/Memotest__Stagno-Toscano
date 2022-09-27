function registrarse(){
  let registro = document.getElementById("registrarse").elements;
  let nombre = registro["nombre"].value;
  let contra = registro["contra"].value;

  if(/^[a-z0-9]+$/i.test(nombre) == false || /^[a-z0-9]+$/i.test(contra) == false){
    return alert('Deben completarse todos los datos del formulario')
  }else{
    console.log(nombre, contra)
    $.ajax({
        url:"/registrarse",
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
        }, 
    });
  }  
};

