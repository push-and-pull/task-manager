# coding: utf-8

from django.shortcuts import render
from forms import UserRegisterForm
from django.shortcuts import render, HttpResponseRedirect


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "sign_in.html", {
                "form": form,
            })
        else:
            form.save()
            return HttpResponseRedirect('/tasks')
    else:
        form = UserRegisterForm()
        return render(request, "sign_in.html", {
            "form": form,
        })