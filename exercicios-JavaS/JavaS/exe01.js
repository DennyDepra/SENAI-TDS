function executar (event){
    event.preventDefault(); // impede o recerregamento da pagina

    const idade = parseInt(document.getElementById("IDidade").value);

    if(idade >140){
        alert("Idade invalida!!")
        return;
    }

    var resultado = document.getElementById("IDresultado");

    if(idade >= 18)
    resultado.innerHTML = "<span style='color: green'>MAIOR</span> de idade";
    else
        resultado.innerHTML = "<span style='color: red'> MENOR </span> de idade"
    
}

function resetar(){

        var resultado = document.getElementById("IDresultado");
        resultado.textContent = "";
        resultado.innerHTML = "";
}

