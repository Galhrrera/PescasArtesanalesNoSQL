var modal = document.getElementById("myModal");
var closeModalBtn = document.getElementById("close");

var btn_Create = document.getElementById("btn_Create");

var modalText = document.getElementById("modal_text");

// Obtiene el nombre de la tabla según el nombre del archivo
let table_name = document.title;
console.log("la tabla es: " + table_name);

// Actualizar tablas
function update_table() {
    eel.read(table_name)(get_data);
}

// CREATE
document.querySelector(".crud_create").onclick = function (){ 
    create_name = document.getElementById("create_name");
    if(!create_name.value) {       
        modal.style.display = "block"
        modalText.innerHTML = "La entrada no puede estar vacía";
        clean_inputs();
    }
    else {
        try {
            data = {
                "metodo": create_name.value
            }
            eel.create(data, table_name)(showModals);
        } catch (error) {
            console.log(error)
        }
    }
    clean_inputs();
}  

// READ
window.onload = function () {
    eel.read(table_name)(get_data);
}

function get_data(output){
    
    json_list = JSON.parse(output);
    string_table = "<thead><tr><th>Método de pesca</th></tr></thead><tbody>";  ;
    string_select = "<option disabled selected value style='color:#whitesmoke'></option>"
    json_list.forEach(row => string_table = string_table.concat("<tr><td>", row['metodo'], "</td></tr>"));
    json_list.forEach(row => string_select = string_select.concat("<option value='", row['_id'], "'>", row['metodo'], "</option>"));
    string_table = string_table.concat("</tbody>");
    document.getElementById("data").innerHTML = string_table;
    document.getElementById("update_id").innerHTML = string_select;
    document.getElementById("delete_id").innerHTML = string_select;
}

//UPDATE
document.querySelector(".crud_update").onclick = function (){ 
    update_id = document.getElementById("update_id"); //El ID del método actual
    update_new_name = document.getElementById("update_name"); //El nuevo nombre
    update_args = [update_id.value, update_new_name.value];
    if(!update_args[0] || !update_args[1]) {
        if(!update_args[0]){
            modal.style.display = "block"
            modalText.innerHTML = "La entrada no puede estar vacía - Falta el método que desea modificar";
            clean_inputs();
        }
        else if(!update_args[1]){
            modal.style.display = "block"
            modalText.innerHTML = "La entrada no puede estar vacía - Falta el nuevo nombre";
            clean_inputs();
        }
    }
    else {
        try {
            args_json = {
                "metodo": update_new_name.value
            }
            eel.update(update_id.value, args_json, table_name)(showModals);
        } catch (error) {
            console.log(error);
        }
    }
} 

//DELETE
document.querySelector(".crud_delete").onclick = function (){ 
    delete_id = document.getElementById("delete_id");
    if(!delete_id.value){
        modal.style.display = "block"
        modalText.innerHTML = "Debe seleccionar el método que desea eliminar";
        clean_inputs();
    }
    else {
        eel.delete(delete_id.value, table_name)(showModals);
    }
}


//ShowModals
function showModals(output){
    if (output[2] == "M" && output[3] == "S" && output[4] == "G") {
        modal.style.display = "block"
        modalText.innerHTML = output.replace("[MSG] ", "");
        clean_inputs();
    }
    else if (output[2] == "E" && output[3] == "R" && output[4] == "R" && output[5] == "O" && output[6] == "R") {
        modal.style.display = "block"
        modalText.innerHTML = output.replace("[ERROR] ", "")
        clean_inputs();
    }
    update_table()
}

//Limpiar inputs
function clean_inputs() {
    inputs = document.getElementsByClassName("crud_input");
    selects = document.getElementsByClassName("crud_select");
    for (let i of inputs) { i.value = ""; }
    for (let s of selects) { s.value = ""; }
}


//modals
closeModalBtn.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

