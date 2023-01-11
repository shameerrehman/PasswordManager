//display modal on click
const modalWrapper = document.querySelector(".modals-wrapper");
if (modalWrapper){
    function displayModal(id){
        if (document.getElementById('close-modal').style.display == 'flex'){
            document.getElementById("signup-modal").style.display = 'none';
            document.getElementById("login-modal").style.display = 'none';
            document.getElementById("add-password-modal").style.display = 'none';
            modalWrapper.style.display = "none";
        }
        const modal = document.getElementById(id);
        modalWrapper.style.display = "flex";
        modal.style.display = "flex";
        close=document.getElementById('close-modal');
        close.style.display='flex';

        //close modal
        //const close=document.getElementById('close-modal')
        close.addEventListener("click", ()=>{
            modalWrapper.style.display = "none";
            modal.style.display = "none";
        })
    }
}


//copy to clipboard
const copies = document.querySelectorAll(".copy");
copies.forEach(copy =>{
    copy.onclick = () =>{
        let elementToCopy = copy.previousElementSibling;
        if (elementToCopy.className  !== "creds"){
            elementToCopy = elementToCopy.previousElementSibling;
            elementToCopy.type = "text";
            elementToCopy.select();
            document.execCommand("copy")
        }
        else{
            elementToCopy.select();
            document.execCommand("copy")

        }
    }
})

function viewPass(id) {
    var pass = document.getElementById("secret-id"+id);
    const icon = document.getElementById('see-pass'+id);
    if (pass.type === "password") {
        pass.type = "text";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    } else {
        pass.type = "password";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");    
    }
  }

  function update(input1, id) {
    if (input1.id == "secret-id"+id){
        var input2 = document.getElementById("pass"+id);
    }
    else{
        var input2 = document.getElementById("user"+id);
    }
    input2.value = input1.value;
  }