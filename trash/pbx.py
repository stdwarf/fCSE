@bp.route('/get_clid', methods=['GET', 'POST'])
def get_clid():
    form = ClidLoginForm()
    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        conn = get_ldap_connection()
        usr = form.username.data+'@'+current_app.config['LDAP_HOST']
        pwd = form.password.data
        try:
            conn.simple_bind_s(usr, pwd)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('pbx/login.html', form=form)
        except ldap.SERVER_DOWN:
            flash('AD server not available')
            return render_template('pbx/login.html', form=form)
        for i in range(1010, 1111):
            try:
                ldap_filter = f'telephoneNumber={i}'
                data_id = conn.search_s(current_app.config['LDAP_BASE_DN'], ldap.SCOPE_SUBTREE, ldap_filter,
                                 current_app.config['LDAP_FILTER_CLID'])
                for data in data_id:
                    if data[0][1]['telephoneNumber'][0].decode('utf-8') is not None:
                        clid_name = data[0][1]['name'][0].decode('utf-8')
                        clid_num = data[0][1]['telephoneNumber'][0].decode('utf-8')
                        email = data[0][1]['mail'][0].decode('utf-8')
                        if 'displayName' in data[0][1]:
                            fullname = data[0][1]['displayName'][0].decode('utf-8')
                        else:
                            fullname = ''
                        if 'department' in data[0][1]:
                            department = data[0][1]['department'][0].decode('utf-8')
                        else:
                            department = ''
                        if 'division' in data[0][1]:
                            division = data[0][1]['division'][0].decode('utf-8')
                        else:
                            division = ''
                        if 'title' in data[0][1]:
                            title = data[0][1]['title'][0].decode('utf-8')
                        else:
                            title = ''

                        if 'address' in data[0][1]:
                            address = data[0][1]['address'][0].decode('utf-8')
                        else:
                            address = ''
                        print(f"- NUM: {clid_num} - NAME: {clid_name} - FULLNAME: {fullname}")
                    else: continue
                user = Clid.query.filter_by(clid_num=clid_num).first()
                if user is None:
                    u = Clid(clid_name=clid_name,
                             clid_num=clid_num,
                             email=email,
                             fullname=fullname,
                             department=department,
                             division=division,
                             title=title,
                             address=address)
                    db.session.add(u)
                    db.session.commit()
                else:
                    user.clid_name = clid_name
                    user.clid_num = clid_num
                    user.email = email
                    user.fullname = fullname
                    user.department = department
                    user.division = division
                    user.title = title
                    user.address = address
                    db.session.commit()
            except:
                flash("Something happen")
                continue
        conn.unbind_s()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('pbx.index')
        return redirect(next_page)
    return render_template("pbx/login.html", title='Sign In', form=form)