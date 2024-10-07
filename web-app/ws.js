$(document).ready(function() {
    var username = 'app';
    var password = 'Energia2025';
    var auth = 'Basic ' + btoa(username + ':' + password);
    var url_base = "http://localhost:5006"
    let listadoVotaciones = []
    let listaId="0";
    let idVotacion='0';
    // Cargar datos de la tabla "Listas Postulantes"
    function cargarListasPostulantes(id_votacion) {
        $.ajax({
            url: url_base.concat("/api/listas/list"),
            method: "GET",
            data: {
                idVotacion: id_votacion
            },
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', auth); // Autenticación básica
            },
            success: function(data) {
                let listasAccordion = $('#listasAccordion');
                listasAccordion.empty();
                data.forEach(function(lista) {
                    let acordeonItem = ''
                    acordeonItem = acordeonItem.concat("<div class='card'>");
                    acordeonItem = acordeonItem.concat("<div class='card-header' id='heading",lista.idLista,"'>");
                    acordeonItem = acordeonItem.concat("<h5 class='mb-0'>");
                    acordeonItem = acordeonItem.concat("<button class='btn btn-link' data-toggle='collapse' data-target='#collapse",lista.idLista,"' aria-expanded='true' aria-controls='collapse",lista.idLista,"'>");
                    acordeonItem = acordeonItem.concat("Votación ",lista.idVotacion," - Lista ",lista.idLista,"</button>");
                    acordeonItem = acordeonItem.concat("</h5>");
                    acordeonItem = acordeonItem.concat("</div>");
                    acordeonItem = acordeonItem.concat("<div id='collapse",lista.idLista,"' aria-labelledby='heading",lista.idLista,"' data-parent='#listasAccordion'>");
                    acordeonItem = acordeonItem.concat("<div class='card-body'>");
                    acordeonItem = acordeonItem.concat("<p><strong>IdVotacion:</strong> ",lista.idVotacion,"</p>");
                    acordeonItem = acordeonItem.concat("<p><strong>Summary:</strong> ",lista.summary,"</p>");
                    acordeonItem = acordeonItem.concat("<p><strong>Description:</strong> ",lista.description,"</p>");
                    acordeonItem = acordeonItem.concat("<p><strong>Votos Totales:</strong> ",lista.votos_total,"</p>");
                    acordeonItem = acordeonItem.concat("<p><strong>Escaños Asignados:</strong> ",lista.escanios_total,"</p>");
                    acordeonItem = acordeonItem.concat("<p><button class='btn btn-primary view-votar-btn' id='view-votar-btn' data-lista-id='",lista.idLista,"'>Cargar Votos</button></p>");
                    acordeonItem = acordeonItem.concat("<p><button class='btn btn-primary view-votaradd-btn' id='view-votaradd-btn' data-lista-id='",lista.idLista,"'>VOTAR</button></p>");
                    acordeonItem = acordeonItem.concat("</div>");
                    acordeonItem = acordeonItem.concat("</div>");
                    acordeonItem = acordeonItem.concat("</div>");
                    listasAccordion.append(acordeonItem);
                });
            },
            error: function(err) {
                console.error("Error al cargar las listas postulantes:", err);
            }
        });
    }
    
    // Cargar datos de la tabla "Votaciones"
    function cargarVotaciones() {
        var listadoVotaciones = [];
        $.ajax({
            url: url_base.concat("/api/votacion/list"),
            method: "GET",
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', auth); // Autenticación básica
            },
            success: function(data) {
                listadoVotaciones = data;
                setlistVotaciones(data);
                let votacionesTable = $('#votacionesTable tbody');
                votacionesTable.empty();
                listadoVotaciones.forEach(function(votacion) {
                    var reg = "";
                    reg = reg.concat("<tr>");
                    reg = reg.concat("<td>",votacion.idVotacion,"</td>");
                    reg = reg.concat("<td>",votacion.summary,"</td>");
                    reg = reg.concat("<td>",votacion.escanio_total,"</td>");
                    if (votacion.status == 'open'){
                        reg = reg.concat("<td class='table-success' align='center'>",votacion.status,"</td>");
                    }else if (votacion.status == 'closed'){
                        reg = reg.concat("<td class='table-danger' align='center'>",votacion.status,"</td>");
                    }else {
                        reg = reg.concat("<td class='table-warning' align='center'>",votacion.status,"</td>");
                    }
                    reg = reg.concat("<td align='right' width='180'>");
                    reg = reg.concat("<button class='view-lista-btn' id='view-lista-btn' data-id='",votacion.idVotacion,"'>Listas</button>");
                    if (votacion.status == 'open'){
                        reg = reg.concat("<button class='view-calcular-btn' id='view-calcular-btn' data-id='",votacion.idVotacion,"'>Calcular</button>");
                    }
                    reg = reg.concat("</td>");
                    reg = reg.concat("</tr>");
                    votacionesTable.append(reg);
                });
            },
            error: function(err) {
                console.error("Error al cargar las votaciones:", err);
            }
        });
    }

    // Llenar el select con las votaciones
    function setlistVotaciones(arr_lst){
        var selectListas = $('#selectListas');
        selectListas.empty();
        arr_lst.forEach(function(votacion) {
            var reg = "";
            reg = reg.concat("<option value='",votacion.idVotacion,"'>");
            reg = reg.concat(votacion.summary)
            reg = reg.concat("</option>");
            selectListas.append(reg);
        });
    }

    // Cargar Votos en Lista Seleccionada
    function cargarVotos() {
        const votos = $('#inputVotos').val(); // Obtener el valor del input de votos
    
        if (votos === "" || isNaN(votos)) {
            showMessageModal("Por favor ingrese una cantidad válida de votos.");
            return;
        }
    
        $.ajax({
            url: url_base.concat("/api/votos/set"),
            method: "POST",
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', auth); // Autenticación básica
            },
            data: JSON.stringify({
                idLista: listaId,  
                votos_cant: parseInt(votos)
            }),
            success: function(response) {
                $('#modalVotos').modal('hide'); // Cerrar el modal
                showMessageModal("Votos agregados exitosamente!");
                cargarListasPostulantes(idVotacion);
            },
            error: function() {
                showMessageModal("Ocurrió un error al agregar los votos.");
            }
        });
    }
    
    function calcularEscanio(id_votacion) {
        $.ajax({
            url: url_base.concat("/api/votacion/calcular"), // Cambia esto si es necesario
            method: "POST",
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', auth); // Autenticación básica
            },
            contentType: "application/json",
            data: JSON.stringify({
                idVotacion: id_votacion
            }),
            success: function(response) {
                showMessageModal("Se calculo correctamente el escaño");
            },
            error: function(error) {
                console.error("Error al guardar votación", error);
            }
        });
        cargarVotaciones();
        cargarListasPostulantes(id_votacion);
    }

    // Inicializar las tablas
    cargarVotaciones();
  
    
    //==========================================
    // Event listeners

    // Manejar el clic en el botón "Agregar Votación"
    $("#addVotacion").on("click", function() {
        $("#addVotacionModal").modal("show");
    });

    // Manejar el clic en el botón "Agregar Lista"
    $("#addLista").on("click", function() {
        $("#addListaModal").modal("show");
    });

    // Manejar el clic en el botón "Guardar" del modal
    $("#guardarVotacion").on("click", function() {
        const summary = $("#summary").val();
        const escanioTotal = $("#escanio_total").val();

        if (summary && escanioTotal) {
            $.ajax({
                url: url_base.concat("/api/votacion/add"), // Cambia esto si es necesario
                method: "POST",
                contentType: 'application/json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', auth); // Autenticación básica
                },
                contentType: "application/json",
                data: JSON.stringify({
                    summary: summary,
                    escanio_total: escanioTotal
                }),
                success: function(response) {
                    // Cerrar el modal
                    $("#addVotacionModal").modal("hide");
                    showMessageModal("Se agrego correctamente la Votacion");
                    // Limpiar los campos del modal
                    $("#summary").val('');
                    $("#escanio_total").val('');

                    // Recargar la tabla de votaciones
                    cargarVotaciones();
                },
                error: function(error) {
                    console.error("Error al guardar votación", error);
                }
            });
        } else {
            showMessageModal("Por favor, completa todos los campos.");
        }
    });

    // Manejar el clic en el botón "Guardar" del modal
    $("#guardarLista").on("click", function() {
        var idVotacion = $('.selectListas').val();
        var summary = $(".lista-summary").val();
        var description = $("#description").val();
        if (idVotacion && summary && description) {
            $.ajax({
                url: url_base.concat("/api/listas/add"), // Cambia esto si es necesario
                method: "POST",
                contentType: 'application/json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', auth); // Autenticación básica
                },
                data: JSON.stringify({
                    idVotacion: idVotacion,
                    summary: summary,
                    description: description
                }),
                success: function(response) {
                    
                    // Cerrar el modal
                    $("#addListaModal").modal("hide");
                    showMessageModal("Se guardo Correctamente");
                    // Limpiar los campos del modal
                    $("#idVotacion").val('');
                    $("#summary").val('');
                    $("#description").val('');

                    //Actulizar tablas
                    cargarVotaciones();
                    cargarListasPostulantes(idVotacion);
                },
                error: function(error) {
                    console.error("Error al guardar lista", error);
                }
            });
        } else {
            showMessageModal("Por favor, completa todos los campos.");
        }
    });

    $(document).on('click', '.view-lista-btn', function () {
        idVotacion = $(this).data('id');
        cargarListasPostulantes(idVotacion);
    });

    $(document).on('click', '#view-votar-btn', function (){
        listaId = $(this).data('lista-id'); // Obtener el idLista del botón
        $('#modalVotos').modal('show'); // Mostrar el modal
    });
    
    $(document).on('click', '#save-lista-votos', function (){
        cargarVotos();
    });

    $(document).on('click', '.view-calcular-btn', function () {
        idVotacion = $(this).data('id');
        calcularEscanio(idVotacion);
    });

    $(document).on('click', '#view-votaradd-btn', function (){
        listaId = $(this).data('lista-id'); // Obtener el idLista del botón
        $.ajax({
            url: url_base.concat("/api/votos/add"),
            method: "POST",
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', auth); // Autenticación básica
            },
            data: JSON.stringify({
                idLista: listaId
            }),
            success: function(response) {
                showMessageModal("Se sumo un Voto exitosamente!");
                cargarListasPostulantes(idVotacion);
            },
            error: function() {
                showMessageModal("Ocurrió un error al sumar el voto.");
            }
        });
        
    });

    function showMessageModal(message) {
        $('#messageModalBody').text(message);  // Agregar el mensaje al cuerpo del modal
        $('#messageModal').modal('show');  // Mostrar el modal
    }

    
});
