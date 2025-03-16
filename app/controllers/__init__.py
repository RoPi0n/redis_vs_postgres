from quart import Blueprint

module = Blueprint(
    'controllers', __name__,
    template_folder='../templates/',
    static_folder='../templates/static',
    static_url_path='/static/'
)