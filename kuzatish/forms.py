from django.forms import ModelForm
from .models import Xodimlar, KeldiKetdi

class XodimlarForm(ModelForm):
    class Meta:
        model = Xodimlar
        fields = '__all__'

class KeldiKetdiForm(ModelForm):
    class Meta:
        model = KeldiKetdi
        fields = ['xodim', 'kelish_vaqti']