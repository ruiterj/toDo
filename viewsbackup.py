from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import datetime
import math
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


day_plan = []  # Ensure day_plan is initialized here to avoid NameError

def overview(request):
    global day_plan

    # Define time slots
    time_slot_labels = [
        "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00",
        "11:00 - 12:00", "12:30 - 13:30", "13:30 - 14:30",
        "14:30 - 15:30", "15:30 - 16:30"
    ]

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'remove_day_plan':
            day_plan = []
        elif action == 'plan_day':
            day_plan = []
            high_priority_tasks = list(Task.objects.filter(priority='Urgent', status__in=['To do', 'In progress']))
            medium_priority_tasks = list(Task.objects.filter(priority='Medium', status__in=['To do', 'In progress']))
            low_priority_tasks = list(Task.objects.filter(priority='Low', status__in=['To do', 'In progress']))

            sorted_tasks = high_priority_tasks + medium_priority_tasks + low_priority_tasks
            temp_tasks = sorted_tasks.copy()
            fully_scheduled_tasks = set()

            while len(day_plan) < 8:
                tasks_remaining = False
                for task in temp_tasks:
                    if task.name in fully_scheduled_tasks or len(day_plan) >= 8:
                        continue

                    hours_to_schedule = min(2, task.effort)
                    if len(day_plan) + hours_to_schedule > 8:
                        hours_to_schedule = 8 - len(day_plan)

                    day_plan.extend([{'name': task.name, 'priority': task.priority, 'hours': 1}] * hours_to_schedule)
                    task.effort -= hours_to_schedule
                    tasks_remaining = True

                    if task.effort <= 0:
                        fully_scheduled_tasks.add(task.name)

                if not tasks_remaining:
                    break

    # Create a list of tuples pairing each time slot with a task (or None if there are no tasks for that slot)
    day_schedule = list(zip(time_slot_labels, day_plan + [None] * (len(time_slot_labels) - len(day_plan))))

    # Get the current date and week number
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_week = datetime.now().strftime('%U')

    context = {
        'day_schedule': day_schedule,
        'current_date': current_date,
        'current_week': current_week,
    }
    return render(request, 'overview.html', context)



def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.name = request.POST.get('task_name')
        task.priority = request.POST.get('task_priority')
        task.status = request.POST.get('task_status')
        task.effort = request.POST.get('task_effort')
        task.progress = request.POST.get('task_progress')
        task.team = request.POST.get('task_team')
        task.save()
        return redirect('tasks')

    context = {'task': task}
    return render(request, 'edit_task.html', context)

def index(request):
    return render(request, 'base.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def tasks_view(request):
    # Fetch all tasks that are either "To do" or "In progress"
    active_tasks = Task.objects.exclude(status='Finished')
    
    # Fetch all tasks that are marked as "Finished"
    finished_tasks = Task.objects.filter(status='Finished')

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_priority = request.POST.get('task_priority')
        task_status = request.POST.get('task_status')
        task_effort = request.POST.get('task_effort')
        task_progress = request.POST.get('task_progress')
        task_team = request.POST.get('task_team')

        # Create and save the new task
        Task.objects.create(
            name=task_name,
            priority=task_priority,
            status=task_status,
            effort=task_effort,
            progress=task_progress,
            team=task_team
        )
        return redirect('tasks')

    context = {
        'tasks': active_tasks,
        'finished_tasks': finished_tasks,
    }
    return render(request, 'tasks.html', context)


def push_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == 'To do':
        task.status = 'In progress'
    elif task.status == 'In progress':
        task.status = 'Finished'
        task.progress = 100
        task.finished_date = timezone.now()  # Set the finished date when the task is completed
    elif task.status == 'Finished':
        task.delete()  # Remove the task if it's already finished

    task.save()
    return redirect('tasks')

def update_day_plan_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_order = data.get('order')
        # Logic to save the new order to the session or database
        print(f"New day plan order received: {new_order}")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def finish_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            total_effort = task.effort  # Store the total effort

            if task.effort > 0:
                # Calculate progress increment based on 1 hour compared to total effort
                progress_increment = (1 / total_effort) * 100
                
                # Update progress
                task.progress = min(100, task.progress + progress_increment)
                

                if task.effort == 0 or task.progress >= 100:
                    task.status = 'Finished'
                    task.finished_date = datetime.now()
                
                task.save()
                
                return JsonResponse({
                    'status': 'success',
                    'task_name': task.name,
                    'new_progress': task.progress,
                    'remaining_effort': task.effort,
                    'finished_date': task.finished_date.strftime('%Y-%m-%d') if task.finished_date else None,
                })
            else:
                return JsonResponse({'status': 'failed', 'message': 'Task effort is already at zero.'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Task not found.'}, status=404)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'}, status=400)

def move_to_in_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 'In progress'
    task.save()
    return redirect('tasks')