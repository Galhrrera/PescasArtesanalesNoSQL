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
                "cuenca": create_name.value
            }
            eel.create(data, table_name);
            update_table();
            modal.style.display = "block"
            modalText.innerHTML = "Método creado correctamente";
            clean_inputs();
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
    string_table = "<thead><tr><th>Cuenca hidrográfica</th></tr></thead><tbody>";  ;
    string_select = "<option disabled selected value style='color:#whitesmoke'></option>"
    json_list.forEach(row => string_table = string_table.concat("<tr><td>", row['cuenca'], "</td></tr>"));
    json_list.forEach(row => string_select = string_select.concat("<option value='", row['_id'], "'>", row['cuenca'], "</option>"));
    string_table = string_table.concat("</tbody>");
    document.getElementById("data").innerHTML = string_table;
    document.getElementById("update_id").innerHTML = string_select;
    document.getElementById("delete_id").innerHTML = string_select;
}

//UPDATE
document.querySelector(".crud_update").onclick = function (){ 
    update_id = document.getElementById("update_id"); //El ID de la cuenca actual
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
                "cuenca": update_new_name.value
            }
            eel.update(update_id.value, args_json, table_name);
            update_table();
            modal.style.display = "block"
            modalText.innerHTML = "Método: "+update_args[0]+ " actualizado correctamente";
            clean_inputs();
        } catch (error) {
            console.log(error);
        }
    }
} 

//DELETE
document.querySelector(".crud_delete").onclick = function () {
    delete_id = document.getElementById("delete_id");
    if (!delete_id.value) {
        modal.style.display = "block"
        modalText.innerHTML = "Debe seleccionar la cuenca que desea eliminar";
        clean_inputs();
    }
    else {
        eel.delete(delete_id.value, table_name)(deleteRegistro);
    }
}

function deleteRegistro(output) {
    if (output != null) {
        clean_inputs();
        let array = output.split(" ");
        array[0] = array[0].replace('"', '');
        if (array[0] == "[ERROR]") {
            modal.style.display = "block"
            modalText.innerHTML = output;
            clean_inputs();
            return
        }
        else {
            update_table();
            modal.style.display = "block"
            modalText.innerHTML = "Cuenca " + delete_id.value + " eliminada correctamente";
            clean_inputs();
        }
    }
    else {
        update_table();
        modal.style.display = "block"
        modalText.innerHTML = "Cuenca " + delete_id.value + " eliminada correctamente";
        clean_inputs();
    }
}

//Limpiar inputs
function clean_inputs() {
    inputs = document.getElementsByClassName("crud_input");
    selects = document.getElementsByClassName("crud_select");
    for (let i of inputs) { i.value = ""; }
    for (let s of selects) { s.value = ""; }
}

closeModalBtn.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
