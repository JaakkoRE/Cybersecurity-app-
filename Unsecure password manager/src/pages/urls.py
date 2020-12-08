from django.urls import path

from .views import homePageView,addNewLogin,submitNewLogin,deleteAll, passwordsView, passwordListView, addPassWord,deletePassWord, testIfThereIsUser, addUserPassWord


urlpatterns = [
    path('', homePageView, name='home'),
    path('passwords', passwordsView, name='passwords'),
    path('passwordList', passwordListView, name='passwordList'),
    path('addPassWord', addPassWord, name='addPassWord'),
    path('deletePassWord', deletePassWord, name='deletePassWord'),
    path('deleteAll', deleteAll, name='deleteAll'),
    path('testIfThereIsUser', testIfThereIsUser, name='testIfThereIsUser'),
    path('addUserPassWord', addUserPassWord, name='addUserPassWord'),
    path('login/addNewLogin', addNewLogin, name='addNewLogin'),
    path('login/submitNewLogin', submitNewLogin, name='submitNewLogin'),
]
