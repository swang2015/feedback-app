from flask import Blueprint, render_template, url_for, redirect, escape, request
from flask_login import login_required, current_user
import random
from feedback import app, db
from feedback.model import SubPair, FeedbackCounter, Product, Feedback


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def index():
    return render_template('index.html')


def select_pair_id():
    pair_ids = [subpair.id for subpair in SubPair.query.filter(SubPair.answer_count <= app.config["MAX_ANSWER"]).all()]
    if not pair_ids:
        return 0
    return random.choice(pair_ids)


@main_blueprint.route("/start")
@login_required
def start():
    cntr = FeedbackCounter.query.filter_by(user_email=current_user.email).all()
    if not cntr:
        cnt = 0
        db.session.add(FeedbackCounter(current_user.email, cnt))
        db.session.commit()
    else:
        cnt = cntr[0].answer_count
    pid = select_pair_id()
    return redirect(url_for('main.feedback', pair_id=pid, user_done=cnt))


@main_blueprint.route("/feedback/<int:pair_id>")
@login_required
def feedback(pair_id):
    user_done = int(request.args.get("user_done"))

    if pair_id <= 0 or pair_id > app.config["MAX_PAIR"]:
        return redirect(url_for('main.index'))

    subpair = SubPair.query.filter_by(id=pair_id).one()

    data = {"orig": {}, "pc_sub": {}}

    orig_attr = Product.query.filter_by(code=subpair.orig_id).one()
    data["orig"] = {
        "prod_id": orig_attr.code,
        "prod_name": orig_attr.name_en,
        "size": orig_attr.net_content,
        "uom": orig_attr.net_content_unit,
        "brand": orig_attr.brand_en,
        "img_url": orig_attr.img_url if orig_attr.img_url else "/static/img/placeholder.png"
    }

    sub_attr = Product.query.filter_by(code=subpair.sub_id).one()
    data["pc_sub"] = {
        "prod_id": sub_attr.code,
        "prod_name": sub_attr.name_en,
        "size": sub_attr.net_content,
        "uom": sub_attr.net_content_unit,
        "brand": sub_attr.brand_en,
        "img_url": sub_attr.img_url if sub_attr.img_url else "/static/img/placeholder.png"
    }

    return render_template("feedback.html", pair_id=pair_id, subs=data, user_done=user_done)


@main_blueprint.route("/post_answer/<int:pair_id>", methods=['POST'])
def post_answer(pair_id):
    user = FeedbackCounter.query.filter_by(user_email=current_user.email).one()
    pair = SubPair.query.filter_by(id=pair_id).one()
    answer_map = request.form.copy()
    for pid, ans in answer_map.items():
        user.answer_count += 1
        pair.answer_count += 1
        db.session.add(Feedback(pair.orig_id, pair.sub_id, current_user.email, ans))
    db.session.commit()

    next_pid = select_pair_id()
    return redirect(url_for('main.feedback', pair_id=next_pid, user_done=user.answer_count))
