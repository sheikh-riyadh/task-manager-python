from django.shortcuts import render,redirect
from django.http import HttpResponse
from task.forms import TaskModelForm,TaskDetailModelForm
from task.models import Task, TaskDetail, Project, Employee
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required





def is_manager(user):
    return user.groups.filter(name="Manager").exists()


def is_employee(user):
    return user.groups.filter(name="Employee").exists()

# Create your views here.
@user_passes_test(is_manager, login_url="sign-in")
def manager_dashboard(req):

    # Get the request type
    request_type = req.GET.get("type","all-task")
    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    tasks = None


    
    
    
    count = base_query.aggregate(
        total_task = Count("id"),
        completed=Count("id", filter=Q(status='COMPLETED')),
        in_progress = Count("id", filter=Q(status="IN_PROGRESS")),
        pending=Count("id", filter=Q(status='PENDING'))
    )

    if request_type=="completed":
        tasks = base_query.filter(status="COMPLETED").all()
    elif request_type=="pending":
        tasks = base_query.filter(status="PENDING").all()
    elif request_type=="in-progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    else:
        tasks = base_query.all()
        


    context ={
        "tasks": tasks,
        "count": count,
        "selected":request_type

    }
    return render(req, "dashboard/manager-dashboard.html",context)


@user_passes_test(is_employee, login_url='sign-in')
def employee_dashboard(req):
    return render(req, "dashboard/user-dashboard.html")


def test(req):
    context={
        "fruits":["Apple", "Mango", "Banana", "Orange", "Jacfruits"]
    }
    return render(req, "test.html", context)

# Create a new task
@login_required
@permission_required('task.add_task')
def create_task(req):
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if req.method == "POST":
        task_form = TaskModelForm(req.POST)
        task_detail_form = TaskDetailModelForm(req.POST, req.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():  # Ensure both forms are valid
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  # Don't save yet
            task_detail.task = task  # Assign the related task
            task_detail.save()  # Now save

            messages.success(req, "Created task successfully")
            return redirect("create-task")
        else:
            messages.error(req, "There was an error in the form. Please check your inputs.")

    context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(req, "dashboard/task_form.html", context)

# Update task which is user want
@login_required
@permission_required('task.change_task')
def update_task(req,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)


    if req.method == "POST":
        task_form = TaskModelForm(req.POST, instance = task)
        task_detail_form = TaskDetailModelForm(req.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():  # Ensure both forms are valid
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  # Don't save yet
            task_detail.task = task  # Assign the related task
            task_detail.save()  # Now save

            messages.success(req, "Updated task successfully")
            return redirect("manager-dashboard")
        else:
            messages.error(req, "There was an error in the form. Please check your inputs.")

    context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(req, "dashboard/task_form.html", context)

@login_required
@permission_required('task.delete_task')
def delete_task(req, id):
    if req.method=="POST":
        task = Task.objects.get(id=id)
        print(task.title)
        task.delete()
        messages.success(req,"Deleted successfully..!")
        return redirect("manager-dashboard")
    else:
        messages.error(req,"Something went wrong..!")
        return redirect("manager-dashboard")


@login_required
@permission_required('task.view_task')
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