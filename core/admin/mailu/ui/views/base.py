from mailu import models, ldap
from mailu.ui import ui, forms, access

import flask
import flask_login



@ui.route('/', methods=["GET"])
@access.authenticated
def index():
    return flask.redirect(flask.url_for('.user_settings'))


@ui.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():

        user = None

        if ldap.is_configured():
            user = ldap.get_user_by_mail(form.email.data)
            if user: 
                if user.check_password(form.pw.data) is False:
                    user = None

        if user is None: 
            user = models.User.login(form.email.data, form.pw.data)
            
        if user:
            flask.session.regenerate()
            flask_login.login_user(user)
            endpoint = flask.request.args.get('next', '.index')
            return flask.redirect(flask.url_for(endpoint)
                or flask.url_for('.index'))
        else:
            flask.flash('Wrong e-mail or password', 'error')
    return flask.render_template('login.html', form=form)


@ui.route('/logout', methods=['GET'])
@access.authenticated
def logout():
    flask_login.logout_user()
    flask.session.destroy()
    return flask.redirect(flask.url_for('.index'))


@ui.route('/announcement', methods=['GET', 'POST'])
@access.global_admin
def announcement():
    form = forms.AnnouncementForm()
    if form.validate_on_submit():
        for user in models.User.query.all():
            user.sendmail(form.announcement_subject.data,
                form.announcement_body.data)
        # Force-empty the form
        form.announcement_subject.data = ''
        form.announcement_body.data = ''
        flask.flash('Your announcement was sent', 'success')
    return flask.render_template('announcement.html', form=form)


@ui.route('/client', methods=['GET'])
def client():
    return flask.render_template('client.html')
