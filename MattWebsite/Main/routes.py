from flask import render_template, request, Blueprint, url_for
from flask_login import current_user
from MattWebsite.models import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', _external=True)

@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='ProfilesPhotos/' + current_user.image_file)
    return render_template('home.html', posts=posts, image_file=image_file)
