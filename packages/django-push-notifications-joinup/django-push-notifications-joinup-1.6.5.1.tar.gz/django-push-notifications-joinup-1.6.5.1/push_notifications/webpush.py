from . import NotificationError
from .conf import get_manager

from pywebpush import webpush
from pywebpush import WebPushException

from .models import WebPushDevice


class WebPushError(NotificationError):
	pass


def get_subscription_info(application_id, uri, browser, auth, p256dh):
	url = get_manager().get_wp_post_url(application_id, browser)
	return {
		"endpoint": "%s/%s" % (url, uri),
		"keys": {
			"auth": auth,
			"p256dh": p256dh
		}
	}


def webpush_send_bulk_message(devices, message, **kwargs):
	results = {
		"success": 0,
		"failure": 0,
		"results": []}
	exception_message = ''
	for device in devices:
		try:
			webpush_send_message(device, message, results=results, **kwargs)
		except WebPushError as e:
			if exception_message != '':
				exception_message += '\n\n'
			exception_message += f'{e} device pk: {device.pk}'

	ids_to_remove = []
	for result in results["results"]:
		if "error" in result:
			ids_to_remove.append(result["original_registration_id"])
	WebPushDevice.objects.filter(registration_id__in=ids_to_remove).update(active=False)

	if exception_message:
		raise WebPushError(exception_message)

	return results


def webpush_send_message(device, message, results=None, **kwargs):
	bulk = True
	if not results:
		bulk = False
		results = {
			"success": 0,
			"failure": 0,
			"results": []}
	try:
		response = webpush(
			subscription_info=get_subscription_info(device.application_id, device.registration_id, device.browser, device.auth, device.p256dh),
			data=message,
			vapid_private_key=get_manager().get_wp_private_key(device.application_id),
			vapid_claims=get_manager().get_wp_claims(device.application_id).copy())
		if response.ok:
			results["success"] += 1
			results["results"].append({'original_registration_id': device.registration_id})
		else:
			results["failure"] += 1
			results["results"].append(
				{'error': response.content,
				 'original_registration_id': device.registration_id})
		return results
	except WebPushException as e:
		exception_message = str(e)
		if "Push failed: 410 Gone" in exception_message or "NotRegistered" in exception_message or "InvalidRegistration" in exception_message or "UnauthorizedRegistration" in exception_message or "InvalidTokenFormat" in exception_message:
			results["failure"] += 1
			results["results"].append(
				{'error': exception_message,
				 'original_registration_id': device.registration_id})
			if not bulk:
				device.active = False
				device.save(update_fields=('active',))
			return results
		else:
			raise WebPushError(exception_message)
