function atualizarDoacao(v)
{
    document.getElementById('doar').innerHTML = "Doar R$ " + v;
    switch(v){
        case 20:
            document.getElementById("doar").href="https://pag.ae/7XDvbF6CG/button"  
            break;
        case 50:
            document.getElementById("doar").href="https://pag.ae/7XDvnBuw4/button"  
            break;
        case 100:
            document.getElementById("doar").href="https://pag.ae/7XDvnLTsK/button"  
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