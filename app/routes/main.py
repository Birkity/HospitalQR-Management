from flask import render_template, redirect, url_for, flash, request, current_app
from . import main
from ..models import Payment
from ..services.payment_gateway import ChapaPayment

@main.route('/payment')
def payment():
    return render_template('payment.html', chapa_public_key=current_app.config['CHAPA_PUBLIC_KEY'])

@main.route('/payment_callback', methods=['GET', 'POST'])
def payment_callback():
    tx_ref = request.args.get('tx_ref')
    if tx_ref:
        payment = Payment.find_by_transaction_id(tx_ref)
        if payment:
            chapa = ChapaPayment()
            verification = chapa.verify_payment(tx_ref)
            if verification.get('status') == 'success':
                Payment.update_one({"_id": payment['_id']}, {"$set": {"status": "completed"}})
                flash('Payment successful, thank you!', 'success')
                return redirect(url_for('main.payment_success'))
            else:
                flash(f'Payment verification failed: {verification.get("message", "An error occurred.")}', 'error')
        else:
            flash('Payment not found.', 'error')
    else:
        flash('Transaction reference not provided.', 'error')
    return redirect(url_for('main.index'))

@main.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')