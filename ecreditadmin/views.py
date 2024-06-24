import json
from datetime import datetime, timedelta

import firebase_admin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials, db, storage, auth

from .utils import update_data, send_push_notification, update_transaction_status, \
    save_notification, update_social_links_data

cred = credentials.Certificate("firebaseconn/elitecredit-cred.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://elitecredit-83265-default-rtdb.firebaseio.com/',
    'storageBucket': 'elitecredit-83265.appspot.com'
})


@login_required
def main(request):
    context = {}
    try:
        # all users
        ref = db.reference("registeredUsers")
        user_data = ref.get()

        # Join dates visualise:
        join_dates_count = get_users_join_dates()
        labels, data = generate_chart_data(join_dates_count)

        # Convert data to JSON for passing to JavaScript
        join_date_data_json = json.dumps({
            "labels": labels,
            "data": data
        })

        total_items = count_items_in_reference('registeredUsers')

        context = {
            'total_users': total_items,
            'join_date_data_json': join_date_data_json,
            'user_data': user_data
        }
    except Exception as e:
        print(e)

    return render(request, "dashboard.html", context)

    # ref = db.reference("CompletedTasks")
    # completed_tasks_data = ref.get()
    #
    # if request.method == 'POST':
    #     user_id = request.POST.get('user_id')
    #     task_id = request.POST.get('task_id')
    #     new_status = request.POST.get('new_status')
    #     print("User ID:", user_id)  # Debugging output
    #     print("Task ID:", task_id)  # Debugging output
    #     print("New Status:", new_status)  # Debugging output
    #     task_ref = ref.child(user_id).child(task_id)
    #     print("Task Ref Path:", task_ref.path)  # Debugging output
    #     task_ref.update({'TaskStatus': new_status})
    #     return redirect('main')
    #
    # return render(request, 'show_data.html', {'completed_tasks_data': completed_tasks_data})


# def get_users_join_dates():
#     # Get a reference to the database
#     database = db.reference()
#
#     # Reference to the Users node in the database
#     users_ref = database.child('Users')
#
#     # Initialize a dictionary to store the count of users joined on each date
#     join_dates_count = {}
#
#     # Iterate over each user to get their join date
#     users_snapshot = users_ref.get()
#     if users_snapshot:
#         for user_uid, user_data in users_snapshot.items():
#             # Get the join date of the user
#             join_date_str = user_data.get('dateJoined')
#             if join_date_str:
#                 join_date = datetime.datetime.strptime(join_date_str, "%Y-%m-%d %H:%M:%S")
#                 # Count the number of users joined on this date
#                 join_date_str = join_date.strftime("%Y-%m-%d")
#                 join_dates_count[join_date_str] = join_dates_count.get(join_date_str, 0) + 1
#
#     return join_dates_count


def get_users_join_dates():
    # Get a reference to the database
    database = db.reference()

    # Reference to the Users node in the database
    users_ref = database.child('registeredUsers')

    # Initialize a dictionary to store the count of users joined on each date
    join_dates_count = {}

    # Iterate over each user to get their join date
    users_snapshot = users_ref.get()
    if users_snapshot:
        for user_uid, user_data in users_snapshot.items():
            # Get the join date of the user
            join_date_str = user_data.get('dateJoined')
            if join_date_str:
                join_date = datetime.strptime(join_date_str, "%Y-%m-%d")
                # Count the number of users joined on this date
                join_date_str = join_date.strftime("%Y-%m-%d")
                join_dates_count[join_date_str] = join_dates_count.get(join_date_str, 0) + 1

    return join_dates_count


def generate_chart_data(join_dates_count):
    # Convert dictionary to lists for Chart.js
    labels = list(join_dates_count.keys())
    data = list(join_dates_count.values())
    return labels, data


def get_total_loans_given():
    pass


@login_required
def dashboard(request):
    context = {}
    try:
        # all users
        ref = db.reference("registeredUsers")
        user_data = ref.get()
        # Join dates visualise:
        join_dates_count = get_users_join_dates()
        labels, data = generate_chart_data(join_dates_count)

        # Convert data to JSON for passing to JavaScript
        join_date_data_json = json.dumps({
            "labels": labels,
            "data": data
        })

        total_items = count_items_in_reference('registeredUsers')
        total_amount = get_total_loans_given()

        context = {
            'total_users': total_items,
            'total_amount': total_amount,
            'join_date_data_json': join_date_data_json,
            'user_data': user_data
        }
    except Exception as e:
        print(e)

    return render(request, "dashboard.html", context)


@login_required
def promo_code(request):
    context = {}
    try:
        ref = db.reference("PromoCodes")
        promoCodes = ref.get()

        ref_redeemed = db.reference("redeemedUsers")
        redeemed_users = ref_redeemed.get()

        if request.method == 'POST':
            promoCode = request.POST.get('promoCode').lower()
            # expireDate = request.POST.get('expireDate')
            amountWorth = request.POST.get('amountWorth')
            useLimit = request.POST.get('useLimit')
            daysActive = request.POST.get('activeDays')
            fullyRedeemed = request.POST.get('fullyRedeemed')

            # Get current date and time
            current_datetime = datetime.now()

            # Add one day
            next_day_datetime = current_datetime + timedelta(days=int(daysActive))

            # Format the datetime object as a string in the desired format
            next_day_formatted = next_day_datetime.strftime("%Y-%m-%d %H:%M:%S")

            dateIssued = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if fullyRedeemed:
                fullyRedeemed = True
            else:
                fullyRedeemed = False

            new_promo_code_ref = ref.push()

            new_promo_code_ref.set({
                'promoCode': promoCode,
                'expireDate': next_day_formatted,
                'fullyRedeemed': fullyRedeemed,
                'amountWorth': int(amountWorth),
                'dateIssued': dateIssued,
                'useLimit': int(useLimit),
                'usedLimit': 0

            })

            print("New promo code added : " + new_promo_code_ref.key)

        context = {
            'promoCodes': promoCodes,
            'redeemed_users': redeemed_users,
        }

    except Exception as e:
        print(f"error: {e} Occurred")

    return render(request, "promo-codes.html", context)


@login_required
def promo_code_update(request):
    try:
        ref = db.reference("PromoCodes")

        if request.method == 'POST':
            promo_id = request.POST.get('promo_id')
            new_status = request.POST.get('redeem_status')
            print("Promo ID:", promo_id)  # Debugging output
            print("New Status:", new_status)  # Debugging output

            promo_ref = ref.child(promo_id)
            print("Task Ref Path:", promo_ref.path)  # Debugging output

            if new_status == 'true':
                promo_status = True
            else:
                promo_status = False

            # Update Promo Status
            promo_ref.update({'fullyRedeemed': promo_status})

            return redirect('promo-codes')

    except Exception as e:
        print(f'error occurred {e}')

    return redirect('promo-codes')


@login_required
def users(request):
    context = {}
    try:
        ref = db.reference("registeredUsers")
        user_data = ref.get()
        context = {
            'user_data': user_data,
        }

    except Exception as e:
        print(f"error: {e} Occurred")

    return render(request, "users_list.html", context)


@login_required
def sms_view(request):
    context = {}
    try:
        ref = db.reference("UserMessages")
        sms_data = ref.get()

        context = {
            'sms_data': sms_data
        }

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            message_id = request.POST.get('message_id')
            action = request.POST.get('action')

            print("User ID:", user_id)  # Debugging output
            print("Message ID:", message_id)  # Debugging output
            print("New Action:", action)  # Debugging output

            sms_ref = ref.child(user_id).child(message_id)
            print("Ref Path:", sms_ref.path)  # Debugging output

            ref_data = sms_ref.delete()

            return JsonResponse({'message': 'Message deleted Successfully', 'success': True})

    except Exception as e:
        print(f'Error Occurred {e}')

    return render(request, "sms_view.html", context)


@login_required
def contact_view(request):
    context = {}
    try:
        ref = db.reference("MobileContacts")
        # ref.delete()
        contact_data = ref.get()

        context = {
            'contact_data': contact_data
        }

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            contact_id = request.POST.get('contact_id')
            action = request.POST.get('action')

            print("User ID:", user_id)  # Debugging output
            print("Contact ID:", contact_id)  # Debugging output
            print("New Action:", action)  # Debugging output

            contact_ref = ref.child(user_id).child(contact_id)
            print("Ref Path:", contact_ref.path)  # Debugging output

            if action == "delete":
                contact_ref.delete()
                return JsonResponse({'message': 'Contact deleted Successfully', 'success': True})

    except Exception as e:
        print(f'Error Occurred {e}')

    return render(request, "mobile-contacts.html", context)


@login_required
def personal_details(request):
    context = {}
    try:
        ref = db.reference("user_details")
        personal_data = ref.get()

        context = {
            'personal_data': personal_data
        }

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            new_status = request.POST.get('new_status')

            print("User ID:", user_id)  # Debugging output
            print("new Status:", new_status)  # Debugging output

            data_ref = ref.child(user_id)
            print("Docs Ref Path:", data_ref.path)  # Debugging output

            # Update Statuses
            data_ref.update({
                'status': new_status,

            })

            return JsonResponse(
                {'message': 'Document Status Updated Successfully', 'success': True})

    except Exception as e:
        print(f'Error Occurred {e}')
    return render(request, "personal_details.html", context)


@login_required
def upload_task_data(request):
    if request.method == 'POST':
        task_name = request.POST.get('taskName')
        taskRequiredSubmission = request.POST.get('taskRequiredSubmission')
        task_requirement = request.POST.get('taskRequirement')
        amount = request.POST.get('amount')
        task_type = request.POST.get('taskType')
        task_url = request.POST.get('taskUrl')
        task_description = request.POST.get('taskDescription')
        task_instruction = request.POST.get('taskInstruction')
        image_data = request.FILES.get('image')  # Get the uploaded image data

        try:
            # Handle image upload to Firestore
            image_url = upload_image_to_storage(image_data)

            task_date = datetime.now().isoformat()

            ref = db.reference("OfferTasks")
            new_task_ref = ref.push()
            new_task_ref.set({
                'taskName': task_name,
                'taskDateAdded': task_date,
                'taskType': task_type,
                'amount': int(amount),
                'image': image_url,
                'taskUrl': task_url,
                'taskId': new_task_ref.key,
                'taskRequiredSubmission': taskRequiredSubmission,
                'taskRequirement': task_requirement,
                'taskDescription': task_description,
                'taskInstruction': task_instruction
            })

            print("New task added successfully with key:", new_task_ref.key)

            return JsonResponse(
                {'message': 'Task added successfully', 'success': True})
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': f'Error Occurred {e}', 'success': False})


# def upload_image_to_storage(image_data):
#     # Initialize Firebase Cloud Storage
#     bucket = storage.bucket()
#
#     # Generate a unique filename or use the original filename
#     filename = image_data.name
#
#     # Create a blob object in the bucket
#     blob = bucket.blob(filename)
#
#     # Upload the image data
#     blob.upload_from_string(image_data.read(), content_type=image_data.content_type)
#
#     # Get the URL of the uploaded image
#     image_url = blob.public_url
#
#     return image_url

# def upload_image_to_storage(image_data):
#     # Initialize Firebase Cloud Storage
#     bucket = storage.bucket()
#
#     filename = image_data.name
#
#     # Define the path within the bucket (e.g., "images/my_image.jpg")
#     object_path = f"OfferImages/{filename}"
#
#     # Create a blob object in the bucket with the specified path
#     blob = bucket.blob(object_path)
#
#     # Upload the image data
#     blob.upload_from_string(image_data.read(), content_type=image_data.content_type)
#
#     # Get the URL of the uploaded image
#     image_url = blob.public_url
#
#     return image_url

def upload_image_to_storage(image_data):
    # Initialize Firebase Cloud Storage
    bucket = storage.bucket()

    filename = image_data.name

    # Define the path within the bucket (e.g., "images/my_image.jpg")
    object_path = f"OfferImages/{filename}"

    # Create a blob object in the bucket with the specified path
    blob = bucket.blob(object_path)

    # Upload the image data with public-read ACL
    blob.upload_from_string(
        image_data.read(),
        content_type=image_data.content_type,
        predefined_acl='publicRead'  # Set ACL to public-read
    )

    # Get the publicly accessible URL
    url = blob.public_url

    return url


@login_required
def documents_approve(request):
    context = {}
    try:
        ref = db.reference("DocumentUploads")
        documents_data = ref.get()

        context = {
            'documents_data': documents_data
        }

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            backpic_status = request.POST.get('backpic_status')
            frontpic_status = request.POST.get('frontpic_status')
            selfiepic_status = request.POST.get('selfiepic_status')

            docs_ref = ref.child(user_id)
            print("Docs Ref Path:", docs_ref.path)  # Debugging output

            # Update Statuses
            docs_ref.update({
                'backpic/status': backpic_status,
                'frontpic/status': frontpic_status,
                'selfiepic/status': selfiepic_status,
            })

            notification_ref = db.reference("Notifications")
            if backpic_status != "declined" and frontpic_status != "declined" and selfiepic_status != "declined":
                message_title = "Documents Approved"
                message = "Your documents have been approved. Login to apply a loan now"
                send_push_notification(user_id, message_title, message)
                save_notification(notification_ref, user_id, "Documents",
                                  "Documents were approved.You can apply loan now")
            else:
                message_title = "Some Documents were Declined"
                message = "Some of your documents were rejected. Login to check which one was rejected and update again"
                send_push_notification(user_id, message_title, message)
                save_notification(notification_ref, user_id, "Documents", "Some of your documents were rejected")

            return JsonResponse(
                {'message': 'Document Status Updated Successfully', 'success': True})

    except Exception as e:
        print(f'Error Occurred {e}')

    return render(request, "documents_approve.html", context)


@login_required
def clicks_add(request):
    try:
        if request.method == 'POST':
            ptcUrl = request.POST.get('ptcUrl')
            amountToEarn = request.POST.get('amountToEarn')
            completionTimes = request.POST.get('completionTimes')
            ptcType = request.POST.get('clickType')
            secondsToView = request.POST.get('secondsToView')

            date_added = datetime.now().isoformat()

            ref = db.reference("PtcItems")
            new_clicks_ref = ref.push()
            new_clicks_ref.set({
                'ptcUrl': ptcUrl,
                'amountToEarn': int(amountToEarn),
                'completionTimes': int(completionTimes),
                'ptcType': ptcType,
                'secondsToView': int(secondsToView),
                'dateAdded': date_added,
                'key': new_clicks_ref.key,
            })

            print("New clicks added successfully with key:", new_clicks_ref.key)

            return JsonResponse(
                {'message': 'Click added successfully', 'success': True})

    except Exception as e:
        return JsonResponse(
            {'message': f'Error Occurred {e}', 'success': False})


@login_required
def add_faq_get(request):
    context = {}
    try:
        ref = db.reference("faq")
        faq_items = ref.get()

        context = {
            'faqItem': faq_items
        }

        if request.method == 'POST':
            question = request.POST.get('question')
            answer = request.POST.get('answer')

            date_added = datetime.now().isoformat()

            ref = db.reference("faq")
            new_clicks_ref = ref.push()
            new_clicks_ref.set({
                'question': question,
                'answer': answer,
            })

            return JsonResponse(
                {'message': 'Faq Item added successfully', 'success': True})

    except Exception as e:
        print(f'error occurred: {e}')

    return render(request, "faq_items.html", context)


def get_uid():
    # Get a database reference
    ref = db.reference("Uids")

    # Retrieve data from Firebase
    uids = ref.get()

    return uids


@login_required
def notifications_send(request, uid=None):
    context = {}
    try:
        uids = get_uid()
        ref = db.reference("Notifications")
        notification_data = ref.get()

        context = {
            'notification_data': notification_data,
            'uids': uids,
            'uid': uid
        }

        if request.method == 'POST':
            user_id = request.POST.get('uid')
            message = request.POST.get('message')
            messageType = request.POST.get('type')

            # dateSent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_notification(ref, user_id, messageType, message)

    except Exception as e:
        print(f'error occurred {e}')

    return render(request, "notifications.html", context)


@login_required
def delete_notification(request):
    try:
        ref = db.reference("Notifications")
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            notification_id = request.POST.get('notification_id')

            notification_ref = ref.child(user_id).child(notification_id)
            print("Notification Ref Path:", notification_ref.path)  # Debugging output

            # delete notification
            notification_ref.delete()

            return JsonResponse(
                {'message': 'Notification Deleted Successfully', 'success': True})

    except Exception as e:

        return JsonResponse(
            {'message': f'Error Occurred {e}', 'success': False})


@login_required
def settings_links(request):
    try:
        if request.method == 'POST':
            acceptanceUseLink = request.POST.get('acceptanceUseLink')
            privacyPolicyLink = request.POST.get('privacyPolicyLink')
            termsLink = request.POST.get('termsLink')
            aboutLink = request.POST.get('aboutLink')

            # date_added = get_date()

            ref = db.reference("settingsLinks")
            ref.set({
                'acceptanceUseLink': acceptanceUseLink,
                'privacyPolicyLink': privacyPolicyLink,
                'termsLink': termsLink,
                'aboutLink': aboutLink
            })

            print("Links dded successfully")

            return JsonResponse(
                {'message': 'Links dded successfullyy', 'success': True})

    except Exception as e:
        return JsonResponse(
            {'message': f'Error Occurred {e}', 'success': False})


@login_required
def loan_requests(request):
    context = {}
    try:
        notification_ref = db.reference("Notifications")
        ref = db.reference("loan_applications")
        transaction_ref = db.reference("transactions")
        loan_applications = ref.get()

        context = {
            'loan_applications': loan_applications
        }

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            new_status = request.POST.get('new_status')
            transaction_key = request.POST.get('transaction_key')
            print("User ID:", user_id)  # Debugging output
            print("New Status:", new_status)
            print("key ", transaction_key)  # Debugging output
            loan_ref = ref.child(user_id)
            # trans_ref = transaction_ref.child(user_id).child(transaction_key)
            print("Task Ref Path:", loan_ref.path)  # Debugging output
            loan_ref.update({'status': new_status})
            # trans_ref.update({"status": new_status})

            message_type = "Account"
            message = f"Your loan application is {new_status}"

            update_transaction_status(user_id, transaction_key, new_status)
            send_push_notification(user_id, f"Loan {new_status}", f"Your loan application has been {new_status}")
            save_notification(notification_ref, user_id, message_type, message)

            return redirect('loan_requests')
    except Exception as e:
        print(f'error occurred {e}')
    return render(request, "loan_requests.html", context)


@login_required
def messages(request):
    context = {}

    try:
        ref = db.reference("ContactMessages")
        user_messages = ref.get()
        context = {
            'user_messages': user_messages,
        }
    except Exception as e:
        print(f"error: {e}")

    return render(request, "messages.html", context)


@login_required
def recent_activities(request):
    context = {}
    try:
        ref = db.reference("recentActivity")
        recent_activity_data = ref.get()

        context = {
            'recent_activity_data': recent_activity_data
        }
    except Exception as e:
        print(f"Error occurred: {e}")

    return render(request, 'history_activities.html', context)


@login_required
def transaction_history(request):
    context = {}
    try:
        ref = db.reference("transactions")
        transaction_activity_data = ref.get()

        context = {
            'transaction_activity_data': transaction_activity_data
        }
    except Exception as e:
        print(f"Error occurred: {e}")

    return render(request, 'transaction-activity.html', context)


@login_required
def tasks_attempt_stats(request):
    context = {}
    try:
        ref = db.reference("TaskAttempt")
        task_attempt_data = ref.get()

        context = {
            'task_attempt_data': task_attempt_data
        }
    except Exception as e:
        print(f'error occurred: {e}')

    return render(request, 'tasks_attempts_stats.html', context)


def count_items_in_reference(reference_path):
    # Get a reference to the database
    database = db.reference()

    # Get a reference to the specific path in the database
    ref = database.child(reference_path)

    # Retrieve the data from the reference
    data_path = ref.get()

    # If data is None or empty, return 0
    if data_path is None:
        return 0

        # Check if data is iterable and supports len()
    if hasattr(data_path, '__iter__') and hasattr(data_path, '__len__'):
        total_items_available = len(data_path)
    else:
        # If data does not support len(), manually count the number of items
        total_items_available = sum(1 for _ in data_path)

    return total_items_available


@login_required
def payment_details(request):
    context = {}
    try:
        ref = db.reference("PayoutDetails")
        payout_data = ref.get()

        context = {
            'payout_data': payout_data,
        }
    except Exception as e:
        print(f'error occurred {e}')

    return render(request, "payment_details.html", context)


def social_links_update(request):
    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        x_link = request.POST.get('x_link')
        facebook_link = request.POST.get('facebook_link')
        playstore_link = request.POST.get('playstore_link')
        update_social_links_data(youtube_link, x_link, facebook_link, playstore_link)
        return redirect('version-check')
    else:
        return redirect('version-check')


@login_required
def version_check(request):
    context = {}
    try:
        ref = db.reference("Versions")
        social_ref = db.reference("socialLinks")
        version_data = ref.get()
        social_links_data = social_ref.get()

        settings_links_ref = db.reference("settingsLinks")
        settings_links_data = settings_links_ref.get()

        context = {
            'version_data': version_data,
            'settings_links_data': settings_links_data,
            'social_links_data': social_links_data
        }

        if request.method == 'POST':
            version_name = request.POST.get('versionName')
            version_code = request.POST.get('versionCode')
            update_url = request.POST.get('updateUrl')
            payment_url = request.POST.get('payment_url')
            update_data(version_name, version_code, update_url, payment_url)
            return redirect('version-check')
        else:
            return render(request, "versions-check.html", context)

    except Exception as e:
        print(f'error occurred {e}')

    return render(request, "versions-check.html", context)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return JsonResponse({'message': 'User created successfully', 'uid': user.uid})
        except firebase_admin.auth.AuthError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('email').rstrip()
        # username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            return JsonResponse(
                {'redirect': reverse('dashboard'), 'message': 'Login success', 'success': True})

        else:
            # Return a JSON response with an error message
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)

    return render(request, 'login.html')


@login_required
def auth_email(request):
    context = {}
    return render(request, 'auth-email.html', context)
