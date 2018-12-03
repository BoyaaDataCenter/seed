import os
from pathlib import Path

from flask import Blueprint, render_template, send_from_directory


bp = Blueprint('front', __name__)

static_folder_path = os.path.join(
    Path(os.path.dirname(os.path.realpath(__file__))).parent, 'static'
)

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def index(path):
    """
    如果是静态文件则利用seed_from_directory来进行加载
    """
    if path and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)

    return render_template('index.html')