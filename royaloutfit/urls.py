from django.urls import path

from royaloutfit import views

urlpatterns=[

    path('',views.login1,name='login1'),
    path('/logout',views.logout,name='logout'),

    path('verify_designer',views.verify_designer,name='verify_designer'),
    path('accept_designer/<int:id>', views.accept_designer, name='accept_designer'),
    path('reject_designer/<int:id>', views.reject_designer, name='reject_designer'),
    path('viewcompailnts',views.viewcompailnts,name='viewcompailnts'),
    path('block',views.block,name='block'),
    path('block_designer/<int:id>', views.block_designer, name='block_designer'),
    path('unblock_designer/<int:id>', views.unblock_designer, name='unblock_designer'),
    path('search_designer', views.search_designer, name='search_designer'),
    path('searchcomplaints', views.searchcomplaints, name='searchcomplaints'),
    path('viewrateing',views.viewrateing,name='viewrateing'),
    path('block1',views.block1,name='block1'),

    path('Coordinator',views.Coordinator,name='Coordinator'),
    path('manufacture',views.manufacture,name='manufacuture'),
    path('designer_register',views.designer_register,name='designer_register'),
    path('registration',views.registration,name='registration'),
    path('sendreplay/<int:id>',views.sendreplay,name='sendreplay'),
    path('searchrating',views.searchrating,name='searchrating'),
    path('add_reply',views.add_reply,name='add_reply'),
    path('adddesign',views.adddesign,name='adddesign'),
    path('editdesign/<int:id>',views.editdesign,name='editdesign'),
    path('deletedesign/<int:id>',views.deletedesign,name='deletedesign'),
    path('deletedesigners/<int:id>',views.deletedesigners,name='deletedesigners'),
    path('editdesigners/<int:id>',views.editdesigners,name='editdesigners'),
    path('edit_designers_post',views.edit_designers_post,name='edit_designers_post'),
    path('add_design_post', views.add_design_post, name='add_design_post'),
    path('add_designers_post', views.add_designers_post, name='add_designers_post'),

    path('customisedesign',views.customisedesign,name='customisedesign'),
    path('designhome',views.designhome,name='designhome'),
    path('managedesign',views.managedesign,name='managedesign'),
    path('more_designs/<int:id>', views.more_designs,name='more_designs'),
    path('add_more_designs',views.add_more_designs,name='add_more_designs'),
    path('add_more_design_post',views.add_more_design_post,name='add_more_design_post'),
    path('adddesigners',views.adddesigners,name='adddesigners'),
    path('searchdesigners',views.searchdesigners,name='searchdesigners'),
    path('acceptdesign/<int:id>',views.acceptdesign,name='acceptdesign'),
    path('unblocktailorshop/<int:id>',views.unblocktailorshop,name='unblocktailorshop'),
    path('blocktailorshop/<int:id>',views.blocktailorshop,name='blocktailorshop'),
    path('rejectdesign/<int:id>',views.rejectdesign,name='rejectdesign'),
    path('searchtailorshop', views.searchtailorshop, name='searchtailorshop'),
    path('searchdesign', views.searchdesign, name='searchdesign'),
    path('searchcustomisedesign', views.searchcustomisedesign, name='searchcustomisedesign'),
    path('blockdesigners/<int:id>', views.blockdesigners, name='blockdesigners'),
    path('unblockdesigners/<int:id>', views.unblockdesigners, name='unblockdesigners'),
    path('searchdesigners', views.searchdesigners, name='searchdesigners'),

    path('addts',views.addts,name='addts'),
    path('Block_unblockdesigners',views.Block_unblockdesigners,name='Block_unblockdesigners'),
    path('delete_design/<int:id>', views.delete_design, name='delete_design'),


    path('manufacturehome',views.manufacturehome,name='manufacturehome'),
    path('manage_designers',views.manage_designers,name='manage_designers'),
    path('searchviewrating',views.searchviewrating,name='searchviewrating'),
    path('viewrating',views.viewrating,name='viewrating'),
    path('login_code',views.login_code,name='login_code'),
    path('edit_design_post',views.edit_design_post,name='edit_design_post'),
    path('chatwithuser', views.chatwithuser, name='chatwithuser'),

    # ///////////////////////////////// USER ////////////////////////////////////////////////

    path('user_register', views.user_register, name='user_register'),
    path('user_register_post', views.user_register_post, name='user_register_post'),
    path('user_home', views.user_home, name='user_home'),

    path('wardrobe/', views.wardrobe_list, name='wardrobe_list'),
    path('wardrobe_add', views.add_wardrobe, name='add_wardrobe'),
    path('edit_wardrobe/<int:w_id>', views.edit_wardrobe, name='edit_wardrobe'),
    path('delete_wardrobe/<int:w_id>', views.delete_wardrobe, name='delete_wardrobe'),
    path('search_wardrobe', views.search_wardrobe, name='search_wardrobe'),
    path('dress_recommendation', views.dress_recommendation, name='dress_recommendation'),

]
