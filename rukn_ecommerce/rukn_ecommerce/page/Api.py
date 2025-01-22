import frappe
import requests

base_url = 'https://api.zid.sa/v1'
store_id = '683282'
Manager_Token = 'eyJpdiI6IkxXcW12M0FJNW9zRVNCMmNGMU9ncGc9PSIsInZhbHVlIjoiL3NoajJPWTljc1o4a3JNakQ3dkNVUk8zNjc5U09RMTNEK1pRN1M3KzF5R1ExMnVpb0N5ellNUTNuTmdGZTl2bCtlTXFmd28zUksxTVJTTmpCaUo4MEZweituOTFqTUxveTR0U1lBUElJUnpEUFFhZzJwWVUyN3ZqQjBuMmRVT2ZxdGljc21PcnlQZ01JaXFJT2hheGtrM0tuZ0RsTlVaRmdMZklNR0g5K2FReXZWT2Jlc2hwWm84M3g3UGwvODN0bzZJbXRCNG4xMzM3TXRPVERDdVFUWjhpM1pLRXBJdVZmNlg5K3pLN2tFOD0iLCJtYWMiOiI2ODA0ZjMwOGU2NzZlNjYyMjhkYjNmODhjNWU4YmZjMmUyOTAzNTUyNTM5MjYzNjRhODNlMWEwMWU5ZDE3MDJlIiwidGFnIjoiIn0='
auth = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0Mjk2IiwianRpIjoiNzZlNjQzMTgxZjFiNTA5ZDgxNmVkZTk2M2Q0NmU2MDY4ZjNjMWY2OGNlN2RkZDE5OGMwOTRlYWZmNTcxMDZkZmExNWE3Y2I5N2FiN2UxMDUiLCJpYXQiOjE3MzcwNDkzMjQuMjMyNDI0LCJuYmYiOjE3MzcwNDkzMjQuMjMyNDI3LCJleHAiOjE3Njg1ODUzMjQuMTU4NTcxLCJzdWIiOiI3Mjk1OTciLCJzY29wZXMiOlsidGhpcmRfYWNjb3VudF9yZWFkIiwidGhpcmRfdmF0X3JlYWQiLCJ0aGlyZF9jYXRlZ29yaWVzX3JlYWQiLCJ0aGlyZF9jYXRlZ29yaWVzX3dyaXRlIiwidGhpcmRfY3VzdG9tZXJzX3JlYWQiLCJ0aGlyZF9jdXN0b21lcnNfd3JpdGUiLCJ0aGlyZF9vcmRlcl9yZWFkIiwidGhpcmRfb3JkZXJfd3JpdGUiLCJ0aGlyZF9jb3Vwb25zX3dyaXRlIiwidGhpcmRfZGVsaXZlcnlfb3B0aW9uc19yZWFkIiwidGhpcmRfZGVsaXZlcnlfb3B0aW9uc193cml0ZSIsInRoaXJkX2FiYW5kb25lZF9jYXJ0c19yZWFkIiwidGhpcmRfcGF5bWVudF9yZWFkIiwidGhpcmRfd2ViaG9va19yZWFkIiwidGhpcmRfd2ViaG9va193cml0ZSIsInRoaXJkX3Byb2R1Y3RfcmVhZCIsInRoaXJkX3Byb2R1Y3Rfd3JpdGUiLCJ0aGlyZF9jb3VudHJpZXNfcmVhZCIsInRoaXJkX2NhdGFsb2dfd3JpdGUiLCJ0aGlyZF9zdWJzY3JpcHRpb25fcmVhZCIsInRoaXJkX2ludmVudG9yeV9yZWFkIiwidGhpcmRfanNfd3JpdGUiLCJ0aGlyZF9jcmVhdGVfb3JkZXIiLCJ0aGlyZF9wcm9kdWN0X3N0b2NrX3JlYWQiLCJ0aGlyZF9wcm9kdWN0X3N0b2NrX3dyaXRlIiwidGhpcmRfaW52ZW50b3J5X3dyaXRlIiwiZW1iZWRkZWRfYXBwc190b2tlbnNfd3JpdGUiLCJ0aGlyZF9sb3lhbHR5X3JlYWQiLCJ0aGlyZF9sb3lhbHR5X3dyaXRlIiwidGhpcmRfb3JkZXJfcmV2ZXJzZV93cml0ZSIsInRoaXJkX29yZGVyX3JldmVyc2VfcmVhZCIsInRoaXJkX3Byb2R1Y3RfYXZhaWxhYmlsaXR5X25vdGlmaWNhdGlvbnNfcmVhZCIsInRoaXJkX3Byb2R1Y3RfYXZhaWxhYmlsaXR5X25vdGlmaWNhdGlvbnNfd3JpdGUiXX0.TZbdwNkKIss4MDAuKnvAFLA_oEc3o-8icFZbyNZLBAI7pE87KksHAum4W3h-2-lmF-z9XVleeFcbrTtOSq3HM78aln5k9UJXI2Y-UNx8L_xWcUSA01IwtxeAC2Wtqqoi7u_BnTvk5XgoUHyhr8nZhfnyHOEOoblDdUuwRpz8-8ebYnCTtiIsWwVY2gQf4G6F2Coq1gaIz05BsQG3BL05cFz0XvOzOQCKkEREbCFENLKxPreIsufR1OSloE3hiZdTIiFIp9RFMbj94RJRRDOPaAq0AmcGThlnHB_qC7Amg6WZa30WMaWI3VuatlcAwW38luLMcnnvr08sW4rSr4WQ6Qi7792YwZyElvuD46rPZT8BD4dbHCVk_vD2wJkNXMXoixXCrnYkjP5BJf-GJzf36bSoY7nux1872MwfILS2J-8ZqhZqrbaOGY3xD0DrBl7Y3NEBiP8PcyKGjSS2_hcB2criEtvXvZcNx_0zdQCNYQOris4whRIweisCqHuj3I6w_5JgtVTROGgxzYKCF48yryApGe5rnKMsWhiHEIqjqcRpTyIEljhLrt6JBH0mqVSllIC0XP41RxRuHo0gPxSDOpUg1UrS6-SX23GrVTywb3LgSF4fXTrvXl7Ndo77dgXGsmV13ciwPPN_QMkwq2XPMh64gbJkEm6JIUbGwMXX3Qs'

@frappe.whitelist()
def get_salla_products(pagination_link=None, page=1, per_page=10):
	products_url = base_url + f"/products?per_page={per_page}&page={page}"
	if pagination_link:
		products_url = pagination_link

	# salla_settings = frappe.get_single("Salla Settings")
	headers = {
		"Accept": "application/json",
        "Store-Id":f"{store_id}",
        "X-Manager-Token":f"{Manager_Token}",
		"Authorization": f"""Bearer {auth}""",
	}

	response = requests.get(products_url, headers=headers)
	response_data = response.json()

	if response.status_code == 200:
		# pagination = response_data["pagination"]
		# links = pagination["links"]
		products = response_data["results"]


		sync_items = frappe.get_list("Item", {"salla_item_id": ["!=", None]}, pluck="salla_item_id")

		for product in products:
			product["synced"] = True if str(product["id"]) in sync_items else False

		return {
			"products": products,
			# "nextUrl": links["next"] if "next" in links else "",
			# "prevUrl": links["previous"] if "previous" in links else "",
			"countProductsSalla": response_data["count"],
		}
	else:
		error_message = response_data["error"]["message"]
		frappe.throw(error_message)


@frappe.whitelist()
def sync_product(product_id):
	# salla_settings = frappe.get_single("Salla Settings")
	# product_id = int(product_id)
	product_url = base_url + f"/products/{product_id}"

	headers = {
		"Accept": "application/json",
		"Store-Id":f"{store_id}",
		"X-Manager-Token":f"{Manager_Token}",
		"Authorization": f"""Bearer {auth}""",
	}

	response = requests.get(product_url, headers=headers)

	if response.status_code == 200:
		product = response.json()
		make_item(product, salla_settings={})
		return True
	else:
		return False


def make_item(product, salla_settings):
	try:
		item = frappe.get_doc("Item", f"""{product["slug"]}-{product["id"]}""")
		item.update(
			{"item_name": product["name"], "description": product["description"],}
		)
		item.save()

	except frappe.DoesNotExistError:
		frappe.clear_messages()
		item = frappe.new_doc("Item")
		item.update(
			{
				"item_code": f"""{product["slug"]}-{product["id"]}""",
				"salla_item_id": product["id"],
				"item_name": product["name"],
				"description": product["description"],
				"is_stock_item": True,
				"item_group": 'Products',
			}
		)
		item.save()

	return item


@frappe.whitelist()
def get_product_count():

    state = {
        "erpnextCount": 0,
		"syncedCount":  0,
    }

    try:
        items = frappe.db.get_list("Item", {"variant_of": ["is", "not set"]})
        try:
            sync_items = frappe.db.get_list("Item", {"salla_item_id": ["!=", None]})
        except Exception:
            sync_items = []
        
        state['erpnextCount'] = len(items) or 0
        state['syncedCount'] = len(sync_items) or 0

    except Exception as e:
        print(e)

    return state