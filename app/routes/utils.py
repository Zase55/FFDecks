def get_data_by_request_type(request):
    # Determinar si los datos vienen en formato JSON o desde un formulario
    if request.content_type == "application/json":
        # Procesar datos como JSON
        form_data = request.get_json()
    elif request.content_type == "application/x-www-form-urlencoded":
        # Procesar datos desde un formulario
        form_data = request.form.to_dict()
    else:
        raise Exception("Tipo de petición no contemplada.")
    return form_data
