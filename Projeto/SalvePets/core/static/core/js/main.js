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