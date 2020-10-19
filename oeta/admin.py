from django import forms
from django.contrib import admin

# Register your models here.
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from oeta.forms import StudentForm
from oeta.models import Subject, Question, Choice, ExamPaper, Student, ExamPaperSet


class ChoiceInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data['is_correct']:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count > 1:
            raise forms.ValidationError('Correct Answer should be one choice')
        elif count < 1:
            raise forms.ValidationError('You Must Select A Correct Answer')


class ChoiceInline(admin.TabularInline):
    model = Choice
    formset = ChoiceInlineFormset
    fields = ['title', 'is_correct']
    extra = 4
    max_num = 5


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subject._meta.fields]
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')
    search_fields = ('title',)
    autocomplete_fields = ('subject',)
    list_filter = ['subject__title']
    inlines = [ChoiceInline]


# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Choice._meta.fields]
#     list_display_links = ['title']
#     exclude = ('created_by', 'updated_by')
#     autocomplete_fields = ('question',)

class ExamPaperSetInline(admin.TabularInline):
    model = ExamPaperSet
    fields = ['set']
    readonly_fields = ['set']
    extra = 4
    max_num = 4


@admin.register(ExamPaper)
class ExamPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')
    # inlines = [ExamPaperSetInline]
    fieldsets = (
        ('Exam Details', {'fields': ('title', 'subject')}),
        ('Set Questions', {'fields': ('questions',)}),
        ('Assign Students', {'fields': ('students',)}),
        ('Publishing', {'fields': ('is_published',)}),
    )
    filter_horizontal = ('students',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super(ExamPaperAdmin, self).save_model(request, obj, form, change)


# @receiver(post_save, sender=ExamPaper)
# def save_exam_paper_set(sender, instance, **kwargs):
#     for i in range(ord('A'), ord('D')+1):
#         set = chr(i)
#         questions = ExamPaper.questions.through.objects.filter(exampaper_id=instance.pk).order_by("?")
#         if ExamPaperSet.objects.filter(exam_paper_id=instance.pk).exists():
#             ExamPaperSet.objects.filter(exam_paper_id=instance.pk).delete()
#         for q in questions:
#             eps = ExamPaperSet(exam_paper_id=instance.pk, question_id=q.question.id, set=set)
#             eps.save()
#             # ExamPaperSet.objects.create(exam_paper_id=instance.pk, question_id=q.question.id, set=set)

# @receiver(m2m_changed, sender=ExamPaper.questions.through)
# def exam_paper_questions_changed(sender, **kwargs):
#     instance = kwargs.pop('instance', None)
#     print(instance.questions)
#     # pk_set = kwargs.pop('pk_set', None)
#     # action = kwargs.pop('action', None)
#     # if action == "pre_add":
#     #     if 1 not in pk_set:
#     #         c = Category.objects.get(pk=1)
#     #         instance.category.add(c)
#     #         instance.save()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'address']
    list_display_links = ['__str__']
    # form = StudentForm
    exclude = ('created_by', 'updated_by')
    # search_fields = ('first_name', 'last_name', '__str__', 'email', 'phone')
    # fieldsets = (
    #     ('Personal Information', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
    #     ('Account Information', {'fields': ('email', 'password')}),
    # )
    fieldsets = (
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone', 'address')}
         ),
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password')}
         ),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions')}
         ),
        (None, {
            'classes': ('wide',),
            'fields': ('is_active',)}
         ),
    )
    add_fieldsets = (
            ('Personal Information', {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'phone', 'address')}
             ),
            ('Authentication', {
                'classes': ('wide',),
                'fields': ('email', 'password')}
             ),
            ('Permissions', {
                'classes': ('wide',),
                'fields': ('groups', 'user_permissions')}
             ),
            (None, {
                'classes': ('wide',),
                'fields': ('is_active',)}
             ),
        )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super(StudentAdmin, self).save_model(request, obj, form, change)
