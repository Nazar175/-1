 function validate() {
            let valid = false;
            
            let disciplineId = document.getElementById("discipline_id");
            let disciplineName = document.getElementById("discipline_name");
            
            console.log(disciplineId.value, disciplineName.value);
            
            if (disciplineId.value.trim() !== "" && disciplineName.value.trim() !== "") {
                valid = true;
            }
            
            if (valid) {
                document.getElementById("success").style.display = "block";
                document.getElementById("error").style.display = "none";
            } else {
                document.getElementById("success").style.display = "none";
                document.getElementById("error").style.display = "block";
            }
            
            return valid;
        }
 function send(){

}