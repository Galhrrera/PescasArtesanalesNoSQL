var table_name = document.title;
//console.log("El nombre de la página y de la tabla es: " + titulo);

var selectMetodos = document.getElementById("select_metodos");
var selectCuencas = document.getElementById("select_cuencas")
var selectPescasUpdate = document.getElementById("update_id");
var selectPescasDelete = document.getElementById("delete_id");
var selectMetodosUpdate = document.getElementById("select_metodos_update");
var selectCuencasUpdate = document.getElementById("select_cuencas_update")

var modal = document.getElementById("myModal");
var closeModalBtn = document.getElementById("close");

var btn_Create = document.getElementById("btn_Create");

var modalText = document.getElementById("modal_text");



closeModalBtn.onclick = function () {
    modal.style.display = "none";
}

// READ
window.onload = function () {
    eel.read(table_name)(get_data);
    eel.read("metodos")(loadSelectMetodos)
    eel.read("cuencas")(loadSelectCuencas)
    eel.read("pescas")(loadSelectPescas)
    modalText.innerHTML = "";
}

//Limpiar inputs
function clean_inputs() {
    inputs = document.getElementsByClassName("crud_input");
    selects = document.getElementsByClassName("crud_select");
    for (let i of inputs) { i.value = ""; }
    for (let s of selects) { s.value = ""; }
}

function get_data(output) {
    json_list = JSON.parse(output);
    string = "<thead><tr><th>Cuenca</th><th>Método</th><th>Fecha</th><th>Total peso</th></thead><tbody>";
    json_list.forEach(row => string = string.concat("<tr><td>", row['cuenca'], "</td><td>", row['metodo'], "</td><td>", row['fecha'].replace(" 00:00:00", ""), "</td><td>", row['peso'], "</td>"));
    string = string.concat("</tbody>");
    document.getElementById("data").innerHTML = string;
}

//Actuaizar tablas
function update_table() {
    eel.read(table_name)(get_data);
    eel.read("cuencas")(loadSelectCuencas);
    eel.read("metodos")(loadSelectMetodos);
    eel.read("pescas")(loadSelectPescas);
}

// CREATE
document.querySelector(".crud_create").onclick = function () {
    alert(table_name)
    id_cuenca = document.getElementById("select_cuencas");
    id_metodo = document.getElementById("select_metodos");
    fecha = document.getElementById("input_fecha");
    peso = document.getElementById("input_peso");
    args = [id_cuenca.value, id_metodo.value, fecha.value, peso.value];
    alert(args)
    if (!args[0] || !args[1] || !args[2] || !args[3]) {
        if(!args[0]) {
            modal.style.display = "block"
            modalText.innerHTML = "Debe seleccionar un valor para todos los campos - Falta Cuenca";
            clean_inputs();
        }
        else if (!args[1]){
            modal.style.display = "block"
            modalText.innerHTML = "Debe seleccionar un valor para todos los campos - Falta Método";
            clean_inputs();
        }
        else if (!args[2]){
            modal.style.display = "block"
            modalText.innerHTML = "Debe seleccionar un valor para todos los campos - Falta fecha";
            clean_inputs();
        }
        else {
            modal.style.display = "block"
            modalText.innerHTML = "Debe seleccionar un valor para todos los campos - Falta peso";
            clean_inputs();
        }

    }
    else {
        try {
            query = {
                "cuenca": id_cuenca.value,
                "metodo": id_metodo.value,
                "fecha": fecha.value,
                "peso": peso.value
            }

            eel.create(query, table_name);
            update_table();
            modal.style.display = "block"
            modalText.innerHTML = "Pesca creada correctamente";
            clean_inputs()
        }
        catch (error) {
            console.log(error);
        }
    }

}

// UPDATE
document.querySelector(".crud_update").onclick = function () {
    update_id = document.getElementById("update_id");
    update_id_value = update_id.value
    update_new_cuenca = document.getElementById("select_cuencas_update");
    update_new_metodo = document.getElementById("select_metodos_update");
    update_new_fecha = document.getElementById("input_fecha_update");
    update_new_peso = document.getElementById("input_peso_update");
    update_args = [update_id_value, update_new_cuenca.value, update_new_metodo.value, update_new_fecha.value, update_new_peso.value];
    alert(update_args)
    if (!update_args[0] || !update_args[1] || !update_args[2] || !update_args[3] || !update_args[4]) {
        if (!update_args[0]){
            modal.style.display = "block"
            modalText.innerHTML = "Todas las entradas deben tener datos - Falta la pesca que desea actualizar";
            clean_inputs()
        }
        else if(!update_args[1]){
            modal.style.display = "block"
            modalText.innerHTML = "Todas las entradas deben tener datos - Falta Cuenca";
            clean_inputs()
        }
        else if (!update_args[2]){
            modal.style.display = "block"
            modalText.innerHTML = "Todas las entradas deben tener datos - Falta Método";
            clean_inputs()
        }
        else if (!update_args[3]){
            modal.style.display = "block"
            modalText.innerHTML = "Todas las entradas deben tener datos - Falta fecha";
            clean_inputs()
        }
        else{
            modal.style.display = "block"
            modalText.innerHTML = "Todas las entradas deben tener datos - Falta peso";
            clean_inputs()
        }
    }
    else {
        argumentos = {
            "cuenca": update_new_cuenca.value,
            "metodo": update_new_metodo.value,
            "fecha": update_new_fecha.value,
            "peso": update_new_peso.value
        }
        try {
            eel.update(update_id.value, argumentos, table_name);
            update_table();
            modal.style.display = "block"
            modalText.innerHTML = "Pesca "+ update_args[0] +"  Actualizada correctamente";
        } catch (error) {
            console.log(error);
        }
    }
    clean_inputs()

}
// DELETE
document.querySelector(".crud_delete").onclick = function () {
    delete_id = document.getElementById("delete_id");

    if (!delete_id.value) {
        modal.style.display = "block"
        modalText.innerHTML = "Debe seleccionar una pesca";
        clean_inputs()
    }
    else {
        eel.delete(delete_id.value, table_name);
        update_table();
        modal.style.display = "block"
        modalText.innerHTML = "Pesca "+delete_id.value+" eliminada correctamente";
        clean_inputs()
    }
    clean_inputs()
}

//ADICIONALES
function loadSelectMetodos(output) {
    json_list = JSON.parse(output);
    string_select = "<option disabled selected value style='color:whitesmoke'></option>";
    json_list.forEach(row => string_select = string_select.concat("<option value='", row['metodo'], "'>", row['metodo'], "</option>"));
    selectMetodos.innerHTML = string_select;
    selectMetodosUpdate.innerHTML = string_select;
}

function loadSelectCuencas(output) {
    json_list = JSON.parse(output);
    string_select = "<option disabled selected value style='color:whitesmoke'></option>";
    json_list.forEach(row => string_select = string_select.concat("<option value='", row['cuenca'], "'>", row['cuenca'],"</option>"));
    selectCuencas.innerHTML = string_select
    selectCuencasUpdate.innerHTML = string_select
}

function loadSelectPescas(output) {
    json_list = JSON.parse(output);
    string_select_update = "<option disabled selected value style='color:whitesmoke'></option>";
    string_select_delete = "<option disabled selected value style='color:whitesmoke'></option>";
    json_list.forEach(row => string_select_update = string_select_update.concat("<option value='", row['_id'], "'>", row['cuenca'], " - ", row['metodo'], " - ", row['fecha'].replace(" 00:00:00", ""), " - ", row['peso']));
    json_list.forEach(row => string_select_delete = string_select_delete.concat("<option value='", row['_id'], "'>", row['cuenca'], " - ", row['metodo'], " - ", row['fecha'].replace(" 00:00:00", ""), " - ", row['peso']));
    selectPescasUpdate.innerHTML = string_select_update
    selectPescasDelete.innerHTML = string_select_delete
}

closeModalBtn.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}