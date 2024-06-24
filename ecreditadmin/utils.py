from datetime import datetime

from firebase_admin import messaging, db
from firebase_admin.exceptions import FirebaseError


def get_date():
    reply_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return reply_date


def update_data(version_name, version_code, update_url, payment_url):
    ref = db.reference('Versions')  # Reference to your data in the database
    ref.update({
        'dateUpdated': get_date(),
        'versionName': version_name,
        'versionCode': float(version_code),
        'updateUrl': update_url,
        'paymentUrl': payment_url,
    })


def update_coins_history(request, points, db, user_id, earned_from):
    # update coins history
    user_coins_ref = db.reference("CoinsHistory").child(user_id)
    new_coins_ref_data = user_coins_ref.push()
    new_coins_ref_data.set({
        'coinsEarned': points,
        'earnedFrom': earned_from,
        'dateEarned': get_date(),
        'status': 'Rewarded'
    })


def get_fcm_token(user_id):
    try:
        user_ref = db.reference('FcmTokens').child(user_id)
        user_data = user_ref.get()

        if user_data:
            return user_data
        else:
            return None
    except Exception as e:
        print(f"Token get error {e}")
        return None


def send_push_notification(user_id, title, message):
    """
    Sends a notification to the user when an action (e.g., approval) is performed.

    Args:
        user_id (str): The UID of the user to send the notification to.
        title (str): The title of the notification.
        message (str): The body of the notification.
    """
    # Get the user's FCM token from the Realtime Database
    fcm_token = get_fcm_token(user_id)
    if fcm_token:
        # Create a message to send to the user's FCM token
        notification_message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            token=fcm_token,
        )

        try:
            # Send the notification message
            response = messaging.send(notification_message)
            print(f'Successfully sent message: {response}')
        except FirebaseError as e:
            print(f'Error sending message: {e}')
    else:
        print(f'No FCM token found for user: {user_id}')


def update_transaction_status(uid, push_key, new_status):
    try:
        # Construct the path to the specific transaction
        path = f'transactions/{push_key}/'

        # Reference the path
        ref = db.reference(path)

        # Update the status field
        ref.update({'status': new_status})

        print(f'Successfully updated status to {new_status} for user {uid} and push key {push_key}')
    except Exception as e:
        print(f'Error occurred: {e}')


def save_notification(ref, user_id, message_type, message):
    dateSent = get_date()
    new_msg_ref = ref.child(user_id).push()
    new_msg_ref.set({
        'message': message,
        'messageType': message_type,
        'sentDate': dateSent
    })


def update_social_links_data(youtube_link, x_link, facebook_link, playstore_link):
    ref = db.reference('socialLinks')  # Reference to your data in the database
    ref.update({
        'youtube_link': youtube_link,
        'x_link': x_link,
        'facebook_link': facebook_link,
        'playstore_link': playstore_link,
    })
