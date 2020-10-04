from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from covidrest.utils import *
from django import forms

def index(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)
        print(request.POST)
        if form.is_valid():
            c = form.cleaned_data["country"]
            d = form.cleaned_data["date"]
            d = d.strftime("%Y-%m-%d")
            if c == 'all':
                res = getConfirmedDayAllCummilated(d)
                for re in res:
                    re['country'] = re.pop('Country/Region')
            else:
                res = getConfirmedDayCummilated(d,c)
                res = [{'country':c,'Value':res}]
        
        context = {
            'res': res,
            'form':form

                    }
            
        return render(request, 'index.html', context)
        
    else:
        res = getConfirmedDayAllCummilated('2020-02-23')
    
        print(type(res[0]))
        for re in res:
            re['country'] = re.pop('Country/Region')
    
        form = CreateNewList()

        context = {
            'res': res,
            'form':form

        }
        return render(request, 'index.html', context)

def forma(request):
    form = CreateNewList()
    

    context = {
        'form': form

    }
    return render(request, 'form.html', context)

class CreateNewList(forms.Form):
    countries=[('all','all'),('Afghanistan', 'Afghanistan'), ('Albania', 'Albania'), ('Algeria', 'Algeria'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Antigua and Barbuda', 'Antigua and Barbuda'), ('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Austria', 'Austria'), ('Azerbaijan', 'Azerbaijan'), ('Bahamas, The', 'Bahamas, The'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Barbados', 'Barbados'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'), ('Benin', 'Benin'), ('Bhutan',
'Bhutan'), ('Bolivia', 'Bolivia'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Brazil', 'Brazil'), ('Brunei', 'Brunei'), ('Bulgaria', 'Bulgaria'), ('Burkina Faso', 'Burkina Faso'), ('Cabo Verde', 'Cabo Verde'), ('Cambodia', 'Cambodia'), ('Cameroon', 'Cameroon'), ('Cape Verde', 'Cape Verde'), ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'), ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Congo (Brazzaville)', 'Congo (Brazzaville)'), ('Congo (Kinshasa)', 'Congo (Kinshasa)'), ('Costa Rica', 'Costa Rica'), ("Cote d'Ivoire", "Cote d'Ivoire"), ('Croatia', 'Croatia'), ('Cuba', 'Cuba'), ('Cyprus', 'Cyprus'), ('Czechia', 'Czechia'), ('Djibouti', 'Djibouti'), ('Dominican Republic', 'Dominican Republic'), ('East Timor', 'East Timor'), ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'), ('El Salvador', 'El Salvador'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'), ('Estonia', 'Estonia'), ('Eswatini', 'Eswatini'), ('Ethiopia', 'Ethiopia'), ('Fiji', 'Fiji'), ('Finland', 'Finland'), ('Gabon', 'Gabon'), ('Gambia, The', 'Gambia, The'), ('Georgia', 'Georgia'), ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Greece', 'Greece'), ('Guatemala', 'Guatemala'), ('Guinea', 'Guinea'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'), ('Holy See', 'Holy See'), ('Honduras', 'Honduras'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran', 'Iran'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Korea, South', 'Korea, South'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'), ('Liberia', 'Liberia'), ('Liechtenstein', 'Liechtenstein'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Madagascar', 'Madagascar'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'), ('Malta', 'Malta'), ('Martinique', 'Martinique'), ('Mauritania',
'Mauritania'), ('Mauritius', 'Mauritius'), ('Mexico', 'Mexico'), ('Moldova', 'Moldova'), ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Morocco', 'Morocco'), ('Namibia', 'Namibia'), ('Nepal', 'Nepal'), ('New Zealand', 'New Zealand'), ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('North Macedonia', 'North Macedonia'), ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Panama', 'Panama'), ('Papua New Guinea', 'Papua New Guinea'), ('Paraguay', 'Paraguay'), ('Peru', 'Peru'), ('Philippines', 'Philippines'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Qatar', 'Qatar'), ('Romania', 'Romania'), ('Russia', 'Russia'), ('Rwanda', 'Rwanda'), ('Saint Lucia', 'Saint Lucia'), ('Saint Vincent and the Grenadines',
'Saint Vincent and the Grenadines'), ('San Marino', 'San Marino'), ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa'), ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'), ('Suriname', 'Suriname'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Taiwan*', 'Taiwan*'), ('Tanzania', 'Tanzania'), ('Thailand', 'Thailand'), ('Togo', 'Togo'), ('Trinidad and Tobago', 'Trinidad and Tobago'), ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('United Arab Emirates', 'United Arab Emirates'), ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan'), ('Venezuela', 'Venezuela'), ('Vietnam', 'Vietnam'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe')]
    country = forms.CharField(max_length=100, label='country',widget=forms.Select(choices=countries), required=False,initial=None)
    date = forms.DateField(input_formats=['%Y-%m-%d'],label='date',widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    cummilated= forms.BooleanField(label='cummilated',initial=False,required=False)


class ConfirmedView(APIView):
    def get(self, request):
        date = self.request.query_params.get('date')
        country = self.request.query_params.get('country')
        cummilated = self.request.query_params.get('cummilated')
        print(cummilated)
        if cummilated == "True":
            if country is None:
                res = getConfirmedDayAllCummilated(date)
                
            else:
                res = getConfirmedDayCummilated(date,country)
                
        else:
            if country is None:
                res = getConfirmedDayAll(date)
                
            else:
                res = getConfirmedDay(date,country)
            
        return Response(res)

    def put(self, request):
        date = self.request.query_params.get('date')
        country = self.request.query_params.get('country')
        cummilated = self.request.query_params.get('cummilated')
        putsi = self.request.data
        if country is not None and date is not None and cummilated != "True":
            
            updateExistingConfirmed(date,country,'',putsi["Value"])

        return Response("content updated sucessfully")

    def delete(self, request):
        date = self.request.query_params.get('date')
        country = self.request.query_params.get('country')
        cummilated = self.request.query_params.get('cummilated')
        putsi = self.request.data
        if country is not None and date is not None and cummilated != "True":
            
            DeleteExistingConfirmed(date,country,'',putsi["Value"])
        return Response("content deleted sucessfully")

    def post(self, request):
        
        return Response("content inserted sucessfully")
# Create your views here.
