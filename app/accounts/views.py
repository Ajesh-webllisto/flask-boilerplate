from flask import Blueprint, current_app
from werkzeug.local import LocalProxy


accounts = Blueprint('accounts', __name__)
logger = LocalProxy(lambda: current_app.logger)

@accounts.route('/', methods=['GET'])
def status():
    return 'Accounts Running!'