from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .core import main_run


@require_http_methods(["GET"])
def index(request):
    size_pop_type = request.GET.get('size_pop_type')
    l = request.GET.get('l')
    px = request.GET.get('px')
    runs = request.GET.get('runs')
    init = request.GET.get('init')
    estim = request.GET.get('estim')
    sel_type = request.GET.get('sel_type')

    if not size_pop_type or not l or not px or not runs or not init or not estim or not sel_type:
        return HttpResponseBadRequest()

    ids = main_run.start_one(init, estim, int(l), sel_type, float(px), size_pop_type, int(runs))

    return JsonResponse(ids, content_type="application/json", safe=False)


@require_http_methods(["GET"])
def status_last(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.info_about_last(run_id))


@require_http_methods(["GET"])
def get_info(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.get_info(run_id))


@require_http_methods(["GET"])
def get_chart(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.get_chart(run_id))


@require_http_methods(["GET"])
def available_runs(request):

    return HttpResponse(main_run.available_runs())
