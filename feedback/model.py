from datetime import datetime
from feedback import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, confirmed, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<user {}>'.format(self.email)


class FeedbackCounter(db.Model):
    user_email = db.Column(db.String(255), primary_key=True)
    answer_count = db.Column(db.Integer())

    def __init__(self, email, cnt):
        self.user_email = email
        self.answer_count = cnt


class SubPair(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    orig_id = db.Column(db.String(63))
    sub_id = db.Column(db.String(63))
    answer_count = db.Column(db.Integer)

    def __init__(self, orig_id, sub_id, cnt):
        self.orig_id = orig_id
        self.sub_id = sub_id
        self.answer_count = cnt


class Product(db.Model):
    brand_en = db.Column(db.Text())
    brand_id = db.Column(db.Text())
    code = db.Column(db.String(63), unique=True, primary_key=True)
    name_en = db.Column(db.Text())
    net_content = db.Column(db.Float())
    net_content_unit = db.Column(db.Text())
    url_en = db.Column(db.Text())
    mch = db.Column(db.Text())
    img_url = db.Column(db.Text())

    def __init__(self, brand_en, brand_id, code, name_en, net_content, net_content_unit, url_en, mch, img_url):
        self.brand_en = brand_en
        self.brand_id = brand_id
        self.code = code
        self.name_en = name_en
        self.net_content = net_content
        self.net_content_unit = net_content_unit
        self.url_en = url_en
        self.mch = mch
        self.img_url = img_url


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orig_id = db.Column(db.String(63))
    sub_id = db.Column(db.String(63))
    answer = db.Column(db.String(4), nullable=True)
    user_email = db.Column(db.String(255))
    date_time = db.Column(db.DateTime)

    def __init__(self, orig_id, sub_id, user_email, answer):
        self.orig_id = orig_id
        self.sub_id = sub_id
        self.answer = answer
        self.user_email = user_email
        self.date_time = datetime.now()


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_nb = db.Column(db.String(63))
    code_pc = db.Column(db.String(63))
    name_en_nb = db.Column(db.String(255))
    name_en_pc = db.Column(db.String(255))
    coSim = db.Column(db.Float())
    name_similarity = db.Column(db.Float())
    name_similarity_hj = db.Column(db.Float())
    name_similarity_n = db.Column(db.Float())
    name_similarity_pd = db.Column(db.Float())
    pprob = db.Column(db.Float())
    pprob_hj = db.Column(db.Float())
    pprob_n = db.Column(db.Float())
    pprob_pd = db.Column(db.Float())
    idf_sim = db.Column(db.Float())
    ah5_swapable = db.Column(db.Integer())
    root_prob = db.Column(db.Float())
    spacy_tm = db.Column(db.Float())
    img_sim = db.Column(db.Float())
    same_mch = db.Column(db.Integer())
    same_ah4 = db.Column(db.Integer())
    same_ah5 = db.Column(db.Integer())
    same_ah6 = db.Column(db.Integer())
    same_ncunit = db.Column(db.Integer())
    rrf = db.Column(db.Float())

