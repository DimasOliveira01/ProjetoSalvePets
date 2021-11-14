function atualizarDoacao(v)
{
    document.getElementById('doar').innerHTML = "Doar R$ " + v;
    switch(v){
        case 20:
            document.getElementById("doar").href="https://pag.ae/7XDvbF6CG/button";
            document.getElementById("valor").value=20  
            break;
        case 50:
            document.getElementById("doar").href="https://pag.ae/7XDvnBuw4/button";
            document.getElementById("valor").value=50
            break;
        case 100:
            document.getElementById("doar").href="https://pag.ae/7XDvnLTsK/button";
            document.getElementById("valor").value=100
            break;
    }
}

function validateSize(input) {
    const fileSize = input.files[0].size / 1024 / 1024; // in MiB
    var aviso = document.getElementById("tamanhoImagem")
    var foto = document.getElementById("foto")

    // Só permite imagens jpeg, jpg, png, bmp pelo front-end
    if (/\.(jpe?g|png|bmp)$/i.test(input.files[0].name) == false){
        aviso.innerHTML = "Os formatos de imagem permitidos são PNG, JPG, JPEG e BMP.";
        aviso.className = "alert alert-danger";
        aviso.setAttribute("role", "alert");
        foto.value = ""
    } else {
        // Não permite imagens maiores que 2 MB pelo front-end
        if (fileSize > 2) {
            aviso.innerHTML = "O tamanho da imagem deve ser menor que 2 MB";
            aviso.className = "alert alert-danger";
            aviso.setAttribute("role", "alert");
            foto.value = ""
        } else {
            aviso.innerHTML = "";
            aviso.className = "";
        }
    }
}

function updateTextInput()
{
    var value = document.getElementById("range").value;
    var img = document.getElementById('imageRange');
    img.height = value

    if (value >= 40 && value < 67){
        document.getElementById("btn-pequeno-porte").setAttribute("class", "btn btn-primary active")
        document.getElementById("btn-medio-porte").setAttribute("class", "btn btn-primary")
        document.getElementById("btn-grande-porte").setAttribute("class", "btn btn-primary")
    }
    else if (value >= 67 && value < 94){
        document.getElementById("btn-pequeno-porte").setAttribute("class", "btn btn-primary")
        document.getElementById("btn-medio-porte").setAttribute("class", "btn btn-primary active")
        document.getElementById("btn-grande-porte").setAttribute("class", "btn btn-primary")
    }
    else if (value >= 94 && value <= 120){
        document.getElementById("btn-pequeno-porte").setAttribute("class", "btn btn-primary")
        document.getElementById("btn-medio-porte").setAttribute("class", "btn btn-primary")
        document.getElementById("btn-grande-porte").setAttribute("class", "btn btn-primary active")
    }
}

function SetSize(porte)
{
    var tamanho;

    switch (porte){
        case 'pequeno':
            tamanho = 40
            break;
        case 'medio':
            tamanho = 80
            break;
        case 'grande':
            tamanho = 120
            break;
    }

    document.getElementById("range").value = tamanho;
    updateTextInput();
}