from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models.address import Address
from users.forms import ProfileUpdateForm, AddressForm

@login_required
def profile_view(request):
    user = request.user
    profile_form = ProfileUpdateForm(instance=user)
    address_form = AddressForm()

    addresses = Address.objects.filter(user=user)
    address_forms = {addr.id: AddressForm(instance=addr) for addr in addresses}

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in your profile form.")

        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Address added successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in address form.")

        elif 'edit_address_id' in request.POST:
            addr_id = request.POST.get('edit_address_id')
            addr_obj = get_object_or_404(Address, id=addr_id, user=user)
            edit_form = AddressForm(request.POST, instance=addr_obj)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Address updated successfully.")
                return redirect('profile')
            else:
                address_forms[int(addr_id)] = edit_form

        elif 'delete_address_id' in request.POST:
            addr_id = request.POST.get('delete_address_id')
            addr_obj = get_object_or_404(Address, id=addr_id, user=user)
            addr_obj.delete()
            messages.success(request, "Address deleted successfully.")
            return redirect('profile')

    return render(request, 'users/profile.html', {
        'form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
        'address_forms': address_forms,
    })
