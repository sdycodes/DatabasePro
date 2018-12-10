from django.shortcuts import render, render_to_response


def page_not_found(request):
    return render_to_response("panel/404.html")


def page_error(request):
    return render_to_response("panel/500.html")


def forbidden(request):
    return render_to_response("panel/403.html")


def method_not_allowed(request):
    return render_to_response("panel/405.html")


def service_unavailable(request):
    return render_to_response("panel/503.html")
