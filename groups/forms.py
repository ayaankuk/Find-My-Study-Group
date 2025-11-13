from django import forms
from .models import StudyGroup, Topic, Course

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    def format_value(self, value):
        if value is None:
            return None
        # Ensure HTML5 datetime-local format (YYYY-MM-DDThh:mm)
        return value.strftime('%Y-%m-%dT%H:%M')

class StudyGroupForm(forms.ModelForm):
    topic_names = forms.CharField(
        required=False,
        help_text='Comma-separated topics (e.g., Midterm 1, Arrays, Recursion)'
    )

    class Meta:
        model = StudyGroup
        fields = ['title', 'course', 'room', 'meeting_time', 'description', 'topic_names']
        widgets = {
            'meeting_time': DateTimeLocalInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True, created_by=None):
        instance = super().save(commit=False)
        if created_by is not None:
            instance.created_by = created_by
        if commit:
            instance.save()
        # handle topics
        names = self.cleaned_data.get('topic_names', '')
        topics = []
        for raw in [n.strip() for n in names.split(',') if n.strip()]:
            t, _ = Topic.objects.get_or_create(name=raw)
            topics.append(t)
        if topics:
            instance.topics.set(topics)
        else:
            instance.topics.clear()
        if commit:
            instance.save()
        return instance
