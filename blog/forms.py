from django import forms
from .models import Post, Comment, registerCamera, City, State, Location
CRIMETYPE_CHOICES = (('All', 'All'), ('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'),
                     ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes'))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class CameraForm(forms.ModelForm):

    class Meta:
        model = registerCamera
        fields = {'address', 'pincode', 'state', 'city'}

######################################################################################################################################################
                                                                #EDIT STARTS#
######################################################################################################################################################


class BlogForm(forms.ModelForm):
    pincode = forms.CharField(widget=forms.TextInput
                              (attrs={'placeholder': 'Enter Six-Digit Pincode'}))

    class Meta:
        model = Post
        fields = ('title', 'location', 'pincode', 'state', 'city',
                  'content', 'crimetype1', 'crimetype2', 'crimetype3', 'crimetype4', 'photo1', 'photo2', 'photo3', 'photo4')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(
                    state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by(
                'name')



# class SortCityForm(form.Form):
#     citylist = getCity()
#     cityname = forms.ChoiceField(citylist)
    

class SortCrimeType(forms.Form):
    crimetype = forms.ChoiceField(choices=CRIMETYPE_CHOICES)

# class Checkbox(forms.Form):
#     give_All = forms.BooleanField()

#     def __init__(self):
#         if check_something():
#             self.fields['give_All'].initial  = False
    

class SortLocation(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SortLocation, self).__init__(*args, **kwargs)
        self.fields['state'].required = False
        self.fields['city'].required = False


    class Meta:
        model = Location
        fields = ('state','city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(
                    state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by(
                'name')


######################################################################################################################################################
                                                                #EDIT STOPS#
######################################################################################################################################################
