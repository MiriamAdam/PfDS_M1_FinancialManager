"""
Reports API Controller

Provides REST endpoints for generating financial reports and charts.
Delegates business logic to the ReportsService.
"""

from datetime import datetime
from flask import Blueprint, request, send_file, jsonify
from backend.app_context import reports_service

reports_api = Blueprint('reports_api', __name__)

@reports_api.route('/monthly-income-share-chart', methods=['GET'])
def get_monthly_income_share_chart():
    """
    Returns a donut-chart with income shares by sub-categories for a specified month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))

        img = reports_service.get_monthly_income_share_chart_img(year, month)
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@reports_api.route('/monthly-spending-share-chart', methods=['GET'])
def get_monthly_spending_share_chart():
    """
    Returns a donut-chart with expense shares by categories for a specified month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))

        img = reports_service.get_monthly_spending_share_chart_img(year, month)
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@reports_api.route('/monthly-summary', methods=['GET'])
def get_monthly_summary_chart():
    """
    Returns the account balance history for the last 30 days as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        img = reports_service.get_monthly_summary_chart_img()
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@reports_api.route('/bar-chart', methods=['GET'])
def get_bar_chart():
    """
    Returns a bar chart that shows each set budget in relation to its spent amount in the current month as a PNG image stream.
    The function delegates the calculation and chart creation to the reports service
    and packages the result for transmission as an HTTP response.
    """
    try:
        img = reports_service.get_bar_chart_img()
        img.seek(0)

        return send_file(
            img,
            mimetype='image/png',
            as_attachment=False,
            download_name='spending.png',
        )

    except Exception as e:
        print(f"Chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({'error': str(e)}), 500