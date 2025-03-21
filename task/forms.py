from django import forms
from task.models import Task



""" If we want to create form menually """

# class TaskForm(forms.Form):
#     title = forms.CharField(max_length=250, required=True, label="Task title")
#     description = forms.CharField(widget=forms.Textarea, required=True, label="Task description")
#     due_date = forms.DateField(widget=forms.SelectDateWidget, required=True, label="Due date")
#     assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Assigned to", choices=[])

#     def __init__(self, *args, **kwargs):
#         employees = kwargs.pop("employees",[])
#         super().__init__(*args, **kwargs)
#         self.fields["assigned_to"].choices = [(emp.id, emp.name) for emp in employees]


class StyleFormMixin:

    common_classes ="border-2 focus:outline-none px-3 py-1 rounded"

    def apply_style_widget(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f'{self.common_classes} w-full'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{self.common_classes} w-full',
                    'rows':2
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.common_classes
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class':f'{self.common_classes} w-full'
                })


""" Create form using model """
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task

        # """ If we want visible specific field as per our needs we can use this code  """  
        #       
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.Select
        }

        # """ If we want to remove field we can use exclude """

        # exclude = ['title', 'description', 'due_date', 'assigned_to']



        # """ If we want to add style menualy """

        # widgets= {
        #     'title': forms.TextInput(attrs={
        #         'class': "border-2 focus:outline-none w-full px-3 py-1 rounded"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border-2 focus:outline-none w-full px-3 py-1 rounded"
        #     }),

        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class':'border-2 focus:outline-none px-3 py-1 rounded'
        #     }),
        #     'assigned_to': forms.Select(attrs={
        #         'class': 'border-2 focus:outline-none px-3 py-1 rounded'
        #     })
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widget()
