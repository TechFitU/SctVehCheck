# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from vehiclecheck.models import VerificacionVehiculo, Vehiculo


from django.contrib.auth.decorators import login_required, permission_required

@login_required
def get_lastverification_by_vehicle(request, identificador):
    '''
    Se devuelve la ultima verificacion realizada al vehiculo cuyo identificador se pasa por parametro
    '''
    import json    
    try:
    	vehicle = get_object_or_404(Vehiculo, pk=identificador)
    	last_verification = VerificacionVehiculo.objects.filter(vehiculo_id = vehicle.serie).latest()
    	date = last_verification.fecha_verificacion    	
    	data = json.dumps("{0}-{1}-{2}".format(date.year, date.month, date.day))

    except ObjectDoesNotExist:
    	data = json.dumps(None)
    return HttpResponse(data , content_type="application/json")

@login_required
def show_verification(request, identificador):	
	verificacion = get_object_or_404(VerificacionVehiculo, pk=identificador)
	context = {
		"verificacion": verificacion
	}
	return render(request, "vehiclecheck/verification.html", context)