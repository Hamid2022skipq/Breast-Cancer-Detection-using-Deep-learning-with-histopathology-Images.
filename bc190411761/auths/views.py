import numpy as np
import tensorflow as tf
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.conf import settings
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import preprocess_input
from .models import Predict
from .forms import signup,PredictForm

# signup view function
def sign_up(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            fm = signup(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Account created Successfully!!')
                return redirect('/login/') 
        else:
            fm=signup()
        return render(request,'signup.html',{'form':fm})
    else:
        return redirect('/dashboard/') 

# login view function
def log_in(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,f'{uname} Successfully Login!!')
                    return redirect('/dashboard/')
        else:
            fm=AuthenticationForm()
        return render(request,'login.html',{'form':fm})
    else:
        return redirect('/dashboard/')    

# Image preprocess
def preprocess_image(image_path):

    # Mammographic image
    # img = load_img(image_path, target_size=(100, 100))
    # img_array = img_to_array(img)
    # mammogram = Image.fromarray(img_array.astype('uint8'))
    # grayscale_mammogram = mammogram.convert('L')
    # img_array = np.array(grayscale_mammogram)
    # img_array = np.expand_dims(img_array, axis=0)
    # preprocessed_img = preprocess_input(img_array)

    # Histopathology 
    img = load_img(image_path, target_size=(50, 50))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(img_array)
    return preprocessed_img

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PredictForm(request.POST,request.FILES)
            if fm.is_valid():
                frm =  fm.save()
                preprocessed_img = preprocess_image(frm.prediction_image.path)
                model = tf.keras.models.load_model('/home/hamid_ali/Documents/Uniproject/bc190411761/auths/static/BreastCNN.h5')
                predictions = model.predict(preprocessed_img)
                # print(predictions[0][1])
                print(predictions)
                prediction = "Image are malignant, cancer is detected." if predictions[0][0] <= 0.5 else "Image are benign, cancer is not detected"
                messages.success(request,f'{prediction}')
                return redirect('/prediction/')
        else:
            fm=PredictForm()
        return render(request,'dashboard.html',{"Name":request.user,'form':fm,})
    return redirect('/login/')

# prediction
def prediction(request):
    if request.user.is_authenticated:
        last_object = Predict.objects.order_by('-id').first()
        last_image = last_object.prediction_image
        return render(request,'prediction.html',{'image':last_image,'Name':request.user})
    else:
        return redirect('/login/')

# Log_out
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login/')
    else:
        return redirect('/login/')


# change password without old password
def change_pass1(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,f'{request.user} Successfully changed password!!')
                return redirect('/log_out/')
        else:
            fm= SetPasswordForm(user=request.user)
        return render(request,'changepass1.html',{'form':fm, 'Name':request.user})
    else:
        return redirect('/login/')
