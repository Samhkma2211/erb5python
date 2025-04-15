from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inquiry
from django.core.mail import send_mail


# Create your views here.
def create_inquiry(request):
    if request.method == "POST":
        try:
            dog_id = int(request.POST.get("dog_id", "0"))
            inquiry_type = request.POST.get("inquiry_type", "General Inquiry")
            name = request.POST.get('name', "").strip()
            email = request.POST.get('email', "").strip()
            phone = request.POST.get('phone', "").strip()
            message = request.POST.get('message', "").strip()
            user_id = int(request.POST.get('user_id', "0"))
            
            # Validate required fields
            if not all([inquiry_type, name, email, phone]):
                messages.error(request, "Please fill in all required fields")
                if dog_id > 0:
                    return redirect('adoption:dog_detail', dog_id=dog_id)
                else:
                    return redirect('faq')
            
            # Check for duplicate dog inquiries if user is authenticated
            if request.user.is_authenticated and user_id > 0:
                if dog_id > 0:
                    has_inquired = Inquiry.objects.filter(dog_id=dog_id, user_id=user_id).exists()
                    if has_inquired:
                        messages.error(request, "You have already made an inquiry for this dog")
                        return redirect('adoption:dog_detail', dog_id=dog_id)
                    
            # Create and save the inquiry
            inquiry_obj = Inquiry(
                inquiry_type=inquiry_type,
                dog_id=dog_id,
                name=name,
                email=email,
                phone=phone,
                message=message,
                user_id=user_id 
            )
            inquiry_obj.save()
            
            # Send email notification
            # send_mail(
            #     'Dog Adoption Inquiry',
            #     f'There has been an inquiry for dog ID {dog_id}. Sign into the admin panel for more info',
            #     '@gmail.com',  # admin from email
            #     [],  # to email
            #     fail_silently=False
            # )
            
            messages.success(request, "Your inquiry has been submitted successfully!")

            if dog_id > 0:
                return redirect('adoption:dog_detail', dog_id=dog_id)
            else:
                return redirect('faq')

            
        except ValueError as e:
            messages.error(request, "Invalid data format. Please check your input.")
            if dog_id > 0:
                return redirect('adoption:dog_detail', dog_id)
            else:
                return redirect('faq')


        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            if dog_id > 0:
                return redirect('adoption:dog_detail', dog_id)
            else:
                return redirect('faq')

    
    if dog_id > 0:
        return render(request, 'adoption:dog_detail', dog_id=dog_id)
    else:
        return render(request, 'faq')
    #return render(request, 'inquiries/inquiry.html')


# def delete_inquirys(request, inquiry_id):
#     inquiry_obj = get_object_or_404(inquiry, pk=inquiry_id)
#     inquiry_obj.delete()
#     return redirect('dashboard')


    
#     context = {
#         'form': form
#     }
#     return render(request, 'inquirys/inquiry.html', context)
