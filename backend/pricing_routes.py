# from flask import Blueprint, request, jsonify
#
# from backend.engine.pricing_engine import PricingEngine
#
# pricing_bp = Blueprint("pricing", __name__)
#
# @pricing_bp.route("/price", methods=["POST"])
# def price_option():
#     data = request.get_json()
#
#     try:
#         #Given the user inputs, calculates the price of the option
#         price, price_se = PricingEngine(data).price()
#
#         return jsonify({
#             "Estimated Price": float(price),
#             'Estimated Price Standard Error': float(price_se)
#         })
#
#     except Exception as e:
#         return jsonify({
#             "error": str(e)
#         }), 400