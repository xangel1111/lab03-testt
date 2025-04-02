from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet

def exam_list(request):
    """Vista para listar todos los exámenes"""
    exams = Exam.objects.all().order_by('-created_date')
    return render(request, 'quiz/exam_list.html', {'exams': exams})

def exam_detail(request, exam_id):
    """Vista para mostrar el detalle de un examen con sus preguntas"""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})

def exam_create(request, exam_id = None):
    if exam_id:
        exam = get_object_or_404(Exam, id=exam_id)
        form = ExamForm(request.POST or None, instance=exam)  # Usamos el examen existente si `exam_id` está presente
    else:
        exam = None
        form = ExamForm(request.POST or None)  # Si no existe `exam_id`, es una creación
    
    if request.method == 'POST':
        if form.is_valid():
            exam = form.save()  # Guarda el examen (ya sea nuevo o actualizado)
            if exam_id:
                messages.success(request, 'Examen actualizado correctamente.')
            else:
                messages.success(request, 'Examen creado correctamente.')
            return redirect('exam_detail', exam_id=exam.id)  # Redirige a la creación de preguntas para este examen
    
    return render(request, 'quiz/exam_form.html', {'form': form, 'exam': exam})

def question_create(request, exam_id):
    """Vista para añadir preguntas a un examen"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            with transaction.atomic():
                # Guardar la pregunta
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                
                # Procesar el formset para las opciones
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
                    
                    # Verificar que solo una opción sea marcada como correcta
                    correct_count = question.choices.filter(is_correct=True).count()
                    if correct_count != 1:
                        messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                    else:
                        messages.success(request, 'Pregunta añadida correctamente.')
                        
                    # Decidir a dónde redirigir
                    if 'add_another' in request.POST:
                        return redirect('question_create', exam_id=exam.id)
                    else:
                        return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()
    
    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
    })

def exam_delete(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    print(exam.delete())
    return redirect(reverse('exam_list'))

