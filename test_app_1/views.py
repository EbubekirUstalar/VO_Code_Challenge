import json

from django.http import HttpResponse
from django.shortcuts import render

from test_app_1.models import Warehouse, SKU, Purchase_Order, Plain_Carton_Line_Item

def index(request):
    return render(request, 'test_page.html')

def generate_suggestions(output, required_pcs_fba_send_number, country, item, check_repeat):
    if country not in output.keys():
        output[country] = {}
        output[country]["source_warehouses"] = {}

    if item.purchase_order.warehouse.id not in output[country]["source_warehouses"].keys():
        output[country]["source_warehouses"][item.purchase_order.warehouse.id] = {}
        output[country]["source_warehouses"][item.purchase_order.warehouse.id]["carton_qty_for_matrix"] = 0
        output[country]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"] = {}

    needed_carton_count_for_sku = int(required_pcs_fba_send_number / item.pcs_per_carton + 0.5)
    qty_cartons_in_plan = 0
    if needed_carton_count_for_sku >= item.cartons_left_cached:
        qty_cartons_in_plan = item.cartons_left_cached
    else:
        qty_cartons_in_plan = needed_carton_count_for_sku

    if output[country]["source_warehouses"][item.purchase_order.warehouse.id]["carton_qty_for_matrix"] + qty_cartons_in_plan >= needed_carton_count_for_sku:
        qty_cartons_in_plan = needed_carton_count_for_sku - output[country]["source_warehouses"][item.purchase_order.warehouse.id]["carton_qty_for_matrix"]

    if check_repeat and item.sku_obj.id in output["amazon.de"]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"] and item.id in output["amazon.de"]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"][item.sku_obj.id]["plain_carton_line_items"]:
        qty_cartons_in_plan = output["amazon.de"]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"][item.sku_obj.id]["plain_carton_line_items"][item.id]["qty_cartons_in_plan"] - item.cartons_left_cached
    if qty_cartons_in_plan > 0:
        if item.sku_obj.id not in output[country]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"]:
            output[country]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"][item.sku_obj.id] = {}
            output[country]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"][item.sku_obj.id]["plain_carton_line_items"] = {}
        output[country]["source_warehouses"][item.purchase_order.warehouse.id]["carton_qty_for_matrix"] += qty_cartons_in_plan
        output[country]["source_warehouses"][item.purchase_order.warehouse.id]["skus_that_need_to_be_send"][item.sku_obj.id]["plain_carton_line_items"][item.id]= {"id":item.id, "qty_cartons_in_plan": qty_cartons_in_plan}

    return output

def fba_send_in_suggestions():
    output = {}
    plain_carton_line_items = Plain_Carton_Line_Item.objects.filter(cartons_left_cached__gt = 0, purchase_order__status="Received")
    for plain_carton_line_item in plain_carton_line_items:
        if plain_carton_line_item.sku_obj.required_pcs_fba_send_in_GERMANY > 0:
            output = generate_suggestions(output, plain_carton_line_item.sku_obj.required_pcs_fba_send_in_GERMANY, "amazon.de", plain_carton_line_item, check_repeat=False)
        if plain_carton_line_item.sku_obj.required_pcs_fba_send_in_FRANCE > 0:
            output = generate_suggestions(output, plain_carton_line_item.sku_obj.required_pcs_fba_send_in_FRANCE, "amazon.fr", plain_carton_line_item, check_repeat=True)
    return output

def ajax_get_table_data(request):
    response_dict = []
    action = request.POST.get('action', '')
    suggestions = fba_send_in_suggestions()

    if action == "dt_sugg_fba_send_ins":
        warehouses = Warehouse.objects.all()
        for wh in warehouses:
            response_dict.append({
                "warehouse_id": wh.id,
                "warehouse": wh.warehouse_name,
                "amazon_de": suggestions["amazon.de"]["source_warehouses"][wh.id]["carton_qty_for_matrix"],
                "amazon_fr": suggestions["amazon.fr"]["source_warehouses"][wh.id]["carton_qty_for_matrix"],

            })

    return HttpResponse(json.dumps({"data": response_dict}), content_type='application/json')