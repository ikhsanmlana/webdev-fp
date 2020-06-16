import datetime
from flask import render_template, flash, redirect, url_for, abort, request, Blueprint
from flaskclub import app, db, bcrypt
from flaskclub.forum.forms import PostForm, ReplyForm
from flaskclub.models import person, Post, Reply
from flask_login import login_user, current_user, logout_user, login_required
forum = Blueprint('forum', __name__)


@forum.route("/forums")
def forums():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page = 6)

    return render_template('forums.html', posts=posts)

@forum.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id) 
    replies = Reply.query.filter_by(post_id=post_id)
    return render_template('post.html', title=post.title, post=post, replies=replies)

@forum.route("/add_post", methods=['GET','POST']) 
@login_required 
def add_post():
	form = PostForm()

	if form.validate_on_submit():
	    post = Post(title=form.title.data, content=form.content.data, author=current_user)
	    db.session.add(post)
	    db.session.commit()
	    flash('Post has been created!', 'success')
	    return redirect(url_for('forum.forums'))

	return render_template('add_post.html', title='Add Post', form=form, legend="New Post")

@forum.route("/<int:post_id>/add_reply", methods=['GET','POST']) 
@login_required 
def add_reply(post_id):
	form = ReplyForm()

	if form.validate_on_submit():
	    reply = Reply(content=form.content.data, user_id=current_user.id, post_id=post_id, author=current_user)
	    db.session.add(reply)
	    db.session.commit()
	    flash('Reply has been posted!', 'success')
	    return redirect(url_for('forum.post', post_id=post_id))

	return render_template('add_reply.html', title='Post A Reply', form=form, legend="New Reply")

@forum.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('forum.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('add_post.html', title='Update Post',
                           form=form, legend='Update Post')

@forum.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('forum.forums'))
