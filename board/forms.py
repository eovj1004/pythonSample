from django import forms

from .models import UploadFileModel


class UploadFileForm(forms.ModelForm):
	'''
	Usage :
    # import UploadFileForm class 
    form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		form.save()
	'''
    class Meta:
        model = UploadFileModel
        fields = ('title', 'file')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
