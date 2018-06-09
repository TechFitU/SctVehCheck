from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from vehiclecheck.models import Cliente, Vehiculo

class ClienteLookup(LookupChannel):

    model = Cliente

    def get_query(self, q, request):
        return Cliente.objects.filter(
            Q(nombre__icontains=q) | Q(rfc__icontains=q)
            ).order_by('nombre')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s - %s" % (escape(obj.complete_name()), obj.rfc)


class VehiculoLookup(LookupChannel):

    model = Vehiculo

    def get_query(self, q, request):
        return Vehiculo.objects.filter(
            Q(placa__icontains=q) | Q(marca__icontains=q) | \
            Q(modelo__icontains=q) | Q(serie__icontains=q) | Q(tarjeta_circulacion__icontains=q) | \
            Q(cliente__nombre__icontains=q)
            ).order_by('-creado')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<b>%s</b> (<i>%s, serie %s</i>)" % (escape(obj.placa), escape(obj.marca), escape(obj.serie))

#Note that raw strings should always be escaped with the escape() function