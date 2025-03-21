from django.shortcuts import render
from django.http import HttpResponse
from task.forms import TaskModelForm
from task.models import Task

# Create your views here.
def user_dashboard(req):
    return render(req, "dashboard/manager-dashboard.html")


def manager_dashboard(req):
    return render(req, "dashboard/user-dashboard.html")


def test(req):
    context={
        "fruits":["Apple", "Mango", "Banana", "Orange", "Jacfruits"]
    }
    return render(req, "test.html", context)


def create_task(req):
    # employees = Employee.objects.all()
    form = TaskModelForm()

    if req.method == "POST":
        form = TaskModelForm(req.POST)
        if form.is_valid():
            form.save()


            return render(req, "dashboard/task_form.html", {"form":form, "message": "task added successfully"})
        

            # data = form.cleaned_data
            # title = data.get("title")
            # description = data.get("description")
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to")

            # task = Task.objects.create(title=title, description=description, due_date=due_date)

            # for employee_id in assigned_to:
            #     employee = Employee.objects.get(id=employee_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse("Task added successfully.")

    

    context={
        "form": form
    }
    return render(req, "dashboard/task_form.html", context)


def show_tasks(req):
    tasks = Task.objects.all()
    return render(req, 'show_tasks.html',{"tasks":tasks})