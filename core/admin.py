from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import PlayerRegistration,Setting

class PlayerRegistrationResource(resources.ModelResource):
    class Meta:
        model = PlayerRegistration
        fields = (
            'id', 'reg_id','user__username', 'player_name', 'father_name',
            'dob', 'gender', 'tshirt_size', 'mobile', 'wathsapp_number', 'email', 'adhar_card',
            'player_image', 'district', 'zone', 'pin_code', 'address', 'first_preference','batting_arm',
            'role', 'is_paid', 'tx_id', 'created'
        )
        export_order = fields
        
        import_id_fields = ['id']

class PlayerRegistrationAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('reg_id','player_name', 'district', 'zone', 'is_paid', 'created') 
    search_fields = ('reg_id','user__username', 'player_name', 'mobile',
        'email', 'adhar_card', 'district','tx_id'
    )
    list_filter = ('zone', 'is_paid', 'gender', 'district') 
    ordering = ('-created',) 
    readonly_fields = ('reg_id','zone', 'created') 

    resource_class = PlayerRegistrationResource  
    
    
admin.site.register(PlayerRegistration, PlayerRegistrationAdmin)
admin.site.register(Setting)