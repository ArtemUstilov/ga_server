from django.core.serializers import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .core import main_run


@require_http_methods(["GET"])
def index(request):
    # size_pop_type = request.GET.get('size_pop_type')
    l = request.GET.get('l')
    n = request.GET.get('n')
    save_pair = bool(int(request.GET.get('save_pair')))
    px = request.GET.get('px')
    runs = request.GET.get('runs')
    init = request.GET.get('init')
    title = request.GET.get('title')
    estim = request.GET.get('estim')
    stop_confluence = request.GET.get('stop_confluence')
    use_mutation = bool(int(request.GET.get('use_mutation')))
    sel_type = request.GET.get('sel_type')

    sigma = request.GET.get('sigma')
    const_1 = request.GET.get('const_1')
    const_2 = request.GET.get('const_2')
    maxN = request.GET.get('maxN')
    random_state = request.GET.get('random_state')
    sel_param1 = request.GET.get('sel_param1')
    sel_param2 = request.GET.get('sel_param2')

    if not n or not px or not l or not runs or not init or not estim or not sel_type:
        return HttpResponseBadRequest()

    ids = main_run.start_one(
        init,
        estim,
        sel_type,
        int(l),
        int(n),
        float(px),
        bool(use_mutation),
        int(runs),
        save_pair,
        sigma,
        const_1,
        const_2,
        float(sel_param1) if sel_param1 else None,
        float(sel_param2) if sel_param2 else None,
        int(maxN),
        int(random_state),
        title,
        stop_confluence
    )

    return JsonResponse(ids, content_type="application/json", safe=False)


@require_http_methods(["GET"])
def status_last(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.info_about_last(run_id))


@require_http_methods(["GET"])
def get_info(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.get_info(run_id))


@require_http_methods(["POST"])
@csrf_exempt
def get_info_details(request):
    run_ids = request.POST.getlist('run_ids[]')
    res = []
    for i in run_ids:
        res.append(main_run.get_info_details(i))
    return HttpResponse(res)


@require_http_methods(["GET"])
def get_chart(request):
    run_id = request.GET.get('run_id')

    return HttpResponse(main_run.get_chart(run_id))


@require_http_methods(["GET"])
def available_runs(request):
    return HttpResponse(main_run.available_runs())
