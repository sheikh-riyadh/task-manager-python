from django.shortcuts import render
from django.http import HttpResponse
from task.forms import TaskModelForm
from task.models import Task, TaskDetail, Project, Employee
from django.db.models import Q, Count

# Create your views here.
def manager_dashboard(req):
    tasks = Task.objects.all()
    context ={
        "tasks": tasks,
        "total_task": tasks.count(),
        "pending_task": tasks.filter(status="PENDING").count(),
        "in_progress": tasks.filter(status="IN_PROGRESS").count(),
        "completed_task": tasks.filter(status="COMPLETED").count()

    }
    return render(req, "dashboard/manager-dashboard.html",context)


def user_dashboard(req):
    
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
    # Ways of data retriving
    # ======================
    """
    1. data = Task.objects.all() {Get all the data from Task model}
    2. data = Task.objects.get(id=1) {Get the data with specific id}
    3. data = Task.objects.first() {Get the first data from Task model}
    4. data = Task.objects.get(title="demo title") {We can search with any field name which is available on models}

    """
    # tasks = Task.objects.all()


    # We can get the data with condition
    # ====================================

    """
    1. data = Task.objects.filter(status="PENDING") {We can filter the data with any field name which is are available in the model}
    2. data = Task.objects.exclude(status="IN_PROGRESS") {Get all the data without IN_PROGRESS}
    3. data = Task.objects.filter(status="CANCEL").exist() {Here we can get Boolean value if exist return True otherwise False}
    4. data = Task.objects.filter(t)

    """

    pending_tasks_data = Task.objects.filter(status="PENDING")



    # Now we will learn "select_related"
    # =================================

    """
    select_related to help optimize the query for "ForegingKey" and "OneToOneField"

    example
    =======
    1. tasks = Task.objects.select_related("details") {We can get the all the tasks with details optimize ways}

    2. task_details = TaskDetail.objects.select_related("task") {We can get task throw the TaskDetail because of reverse relation (Remember reverse relation work only OneToOneField if we use "select_related")}
    
    """

    tasks = Task.objects.select_related("details").all() #{We can access tasks details throw the tasks}
    tasks = TaskDetail.objects.select_related("task").all() #{We can access tasks throw the task details}
    tasks = Task.objects.select_related('project').all()
    tasks = Project.objects.prefetch_related("tasks").all()
    

    # We are going to use prefetch_related
    # ====================================

    """
    prefetch_related to help optimize the query for "reverse ForegingKey" and "ManyToManyField"

    1. tasks = Task.objects.prefetch_related("assigned_to").all() {We can see how many employee work on this task throw the Task model}

    """

    tasks = Task.objects.prefetch_related("assigned_to").all()
    tasks = Employee.objects.prefetch_related("task").all()
    tasks = Project.objects.prefetch_related("task").all()
    tasks= Employee.objects.annotate(completed_tasks=Count("task", filter=Q(task__is_completed=True)))



    return render(req, 'show_tasks.html',{"tasks":tasks, "pending_tasks":pending_tasks_data})