import os

from flask import Blueprint, render_template, send_from_directory

from seed.utils.helper import template_folder_path


bp = Blueprint('front', __name__)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def index(path):
    """
    如果是静态文件则利用seed_from_directory来进行加载
    """
    if path and os.path.exists(os.path.join(template_folder_path, path)):
        return send_from_directory(template_folder_path, path)

    return render_template('index.html')