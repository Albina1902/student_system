from django.shortcuts import render, redirect, get_object_or_404
from .models import Group
from .forms import GroupForm

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

def group_create(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('group_list')
    return render(request, 'groups/group_form.html', {'form': form})

def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        form.save()
        return redirect('group_list')
    return render(request, 'groups/group_form.html', {'form': form})

def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'groups/group_delete.html', {'group': group})
