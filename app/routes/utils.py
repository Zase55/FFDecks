def get_data_by_request_type(request):
    if request.content_type == "application/json":
        form_data = request.get_json()
    elif request.content_type == "application/x-www-form-urlencoded":
        form_data = request.form.to_dict()
    else:
        raise Exception("Tipo de petición no contemplada.")
    return form_data
