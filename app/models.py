import enum
from app import db, login
from datetime import datetime
from flask_login import UserMixin


class BoolEnum(enum.Enum):
    yes = "yes"
    no = "no"


class LongBoolEnum(enum.Enum):
    yes = "yes"
    no = "no"
    true = "true"
    false = "false"
    off = "off"
    on = "on"


class Redirect_method(enum.Enum):
    user = 'user'
    uri_core = 'uri_core'
    uri_pjsip = 'uri_pjsip'


class Dtls_setup(enum.Enum):
    active = 'active'
    passive = 'passive'
    actpass = 'actpass'


class T38_udptl_ec(enum.Enum):
    none = 'none'
    fec = 'fec'
    redundancy = 'redundancy'


class Media_encryption(enum.Enum):
    no ='no'
    sdes = 'sdes'
    dtls = 'dtls'


class Callerid_privacy(enum.Enum):
    allowed_not_screened = 'allowed_not_screened'
    allowed_passed_screened = 'allowed_passed_screened'
    allowed_failed_screened = 'allowed_failed_screened'
    allowed = 'allowed'
    prohib_not_screened = 'prohib_not_screened'
    prohib_passed_screened = 'prohib_passed_screened'
    prohib_failed_screened = 'prohib_failed_screened'
    prohib = 'prohib'
    unavailable ='unavailable'


class Timers(enum.Enum):
    forced = 'forced'
    no = 'no'
    required = 'required'
    yes = 'yes'


class Dtmf_mode(enum.Enum):
    rfc4733 ='rfc4733'
    inband= 'inband'
    info = 'info'
    auto = 'auto'
    auto_info = 'auto_info'


class Direct_media_glare_mitigation(enum.Enum):
    none = 'none'
    outgoing = 'outgoing'
    incoming ='incoming'


class Connected_line_method(enum.Enum):
    invite = 'invite'
    reinvite = 'reinvite'
    update = 'update'


class Auth_type(enum.Enum):
    md5='md5'
    userpass = 'userpass'
    google_oauth = 'google_oauth'


class Dtls_fingerprint(enum.Enum):
    SHA1 = 'SHA-1'
    SHA256 = 'SHA-256'


class Callforward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exten = db.Column(db.String(4), index=True, unique=True)
    forward_phone = db.Column(db.String(11), index=True)
    timeout = db.Column(db.String(4))

    def __init__(self, exten, forward_phone , timeout):
        self.exten = exten
        self.forward_phone = forward_phone
        self.timeout = timeout

    def __repr__(self):
        return f'<Exten {self.exten}>'


class Clid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(254), index=True)
    clid_name = db.Column(db.String(254), index=True)
    clid_num = db.Column(db.String(5), index=True, unique=True)
    email = db.Column(db.String(254), index=True)
    department = db.Column(db.String(254), index=True)
    division = db.Column(db.String(254), index=True)
    title = db.Column(db.String(254), index=True)

    def __init__(self, clid_name, clid_num):
        self.clid_name = clid_name
        self.clid_num = clid_num

    def __repr__(self):
        return f'<CLIDNAME {self.clid_name}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fullname = db.Column(db.String(254), index=True)
    email = db.Column(db.String(120), index=True)
    company = db.Column(db.String(254), index=True)
    department = db.Column(db.String(254), index=True)
    title = db.Column(db.String(254), index=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref("user", lazy="dynamic"))

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.fullname}>'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', secondary='user_roles', backref=db.backref("role", lazy="dynamic"))

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'),unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))



class Ps_auths(db.Model):
    __tablename__ = 'ps_auths'
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.Enum(Auth_type), default='userpass')
    md5_cred = db.Column(db.String(40), nullable=True)
    realm = db.Column(db.String(40), nullable=True)
    refresh_token =db.Column(db.String(254), nullable=True)
    oauth_clientid =db.Column(db.String(254), nullable=True)
    oauth_secret =db.Column(db.String(254), nullable=True)
    password = db.Column(db.String(254), index=True, default='000000000')
    username = db.Column(db.String(254), index=True)
    r_auths = db.relationship('Ps_endpoints', backref='ps_auth')

    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<Username {self.username}, Password {self.password}>'


class Ps_aors(db.Model):
        __tablename__ = 'ps_aors'
        id = db.Column(db.Integer, primary_key=True)
        contact = db.Column(db.String(254), nullable=True)
        default_expiration = db.Column(db.Integer, nullable=True)
        mailboxes = db.Column(db.String(80), nullable=True)
        max_contacts = db.Column(db.Integer, nullable=True, default=1)
        minimum_expiration = db.Column(db.Integer, nullable=True)
        remove_existing = db.Column(db.String(40), nullable=True)
        qualify_frequency = db.Column(db.Integer, nullable=True)
        authenticate_qualify = db.Column(db.String(40), nullable=True)
        maximum_expiration = db.Column(db.Integer, nullable=True)
        outbound_proxy = db.Column(db.String(40), nullable=True)
        support_path = db.Column(db.String(40), nullable=True)
        qualify_timeout = db.Column(db.Float, nullable=True)
        voicemail_extension = db.Column(db.String(40), nullable=True)
        r_aors = db.relationship('Ps_endpoints',  backref='ps_aor')

        def __init__(self, id, max_contacts):
            self.id = id
            self.max_contacts = max_contacts


class Ps_endpoints(db.Model):
    __tablename__ = 'ps_endpoints'
    id = db.Column(db.Integer, primary_key=True)
    transport = db.Column(db.String(40), nullable=True, default='transport-udp')
    context = db.Column(db.String(254), index=True)
    disallow = db.Column(db.String(40), nullable=True, default='all')
    allow = db.Column(db.String(40), nullable=True, default='alaw')
    direct_media = db.Column(db.Enum(BoolEnum), default='no')
    connected_line_method = db.Column(db.Enum(Connected_line_method))
    direct_media_method = db.Column(db.Enum(Connected_line_method))
    direct_media_glare_mitigation = db.Column(db.Enum(Direct_media_glare_mitigation))
    disable_direct_media_on_nat = db.Column(db.Enum(BoolEnum))
    dtmf_mode = db.Column(db.Enum(Dtmf_mode))
    external_media_address = db.Column(db.String(40), nullable=True)
    force_rport = db.Column(db.Enum(BoolEnum))
    ice_support = db.Column(db.Enum(BoolEnum))
    identify_by = db.Column(db.String(80), nullable=True)
    mailboxes = db.Column(db.String(40), nullable=True)
    moh_suggest = db.Column(db.String(40), nullable=True)
    outbound_auth = db.Column(db.String(40), nullable=True)
    outbound_proxy = db.Column(db.String(40), nullable=True)
    rewrite_contact = db.Column(db.Enum(BoolEnum))
    rtp_ipv6 = db.Column(db.Enum(BoolEnum))
    rtp_symmetric = db.Column(db.Enum(BoolEnum))
    send_diversion = db.Column(db.Enum(BoolEnum))
    send_pai = db.Column(db.Enum(BoolEnum))
    send_rpid = db.Column(db.Enum(BoolEnum))
    timers_min_se = db.Column(db.Integer, nullable=True)
    timers = db.Column(db.Enum(Timers))
    timers_sess_expires = db.Column(db.Integer, nullable=True)
    callerid = db.Column(db.String(254), nullable=True)
    callerid_privacy = db.Column(db.Enum(Callerid_privacy))
    callerid_tag = db.Column(db.String(40), nullable=True)
    aggregate_mwi = db.Column(db.Enum(BoolEnum))
    trust_id_inbound = db.Column(db.Enum(BoolEnum))
    trust_id_outbound = db.Column(db.Enum(BoolEnum))
    use_ptime = db.Column(db.Enum(BoolEnum))
    use_avpf = db.Column(db.Enum(BoolEnum))
    media_encryption = db.Column(db.Enum(Media_encryption))
    inband_progress = db.Column(db.Enum(BoolEnum))
    call_group = db.Column(db.Integer)
    pickup_group = db.Column(db.Integer)
    named_call_group = db.Column(db.String(40), nullable=True)
    named_pickup_group = db.Column(db.String(40), nullable=True)
    device_state_busy_at = db.Column(db.Integer)
    fax_detect = db.Column(db.Enum(BoolEnum))
    t38_udptl = db.Column(db.Enum(BoolEnum))
    t38_udptl_ec = db.Column(db.Enum(T38_udptl_ec))
    t38_udptl_maxdatagram = db.Column(db.Integer)
    t38_udptl_nat = db.Column(db.Enum(BoolEnum))
    t38_udptl_ipv6 = db.Column(db.Enum(BoolEnum))
    tone_zone = db.Column(db.String(40), nullable=True)
    language = db.Column(db.String(40), nullable=True)
    one_touch_recording = db.Column(db.Enum(BoolEnum))
    record_on_feature = db.Column(db.String(40), nullable=True)
    record_off_feature = db.Column(db.String(40), nullable=True)
    rtp_engine = db.Column(db.String(40), nullable=True)
    allow_transfer = db.Column(db.Enum(BoolEnum))
    allow_subscribe = db.Column(db.Enum(BoolEnum))
    sdp_owner = db.Column(db.String(40), nullable=True)
    sdp_session = db.Column(db.String(40), nullable=True)
    tos_audio = db.Column(db.String(10), nullable=True)
    tos_video = db.Column(db.String(10), nullable=True)
    sub_min_expiry = db.Column(db.Integer)
    from_domain = db.Column(db.String(40), nullable=True)
    from_user = db.Column(db.String(40), nullable=True)
    mwi_from_user = db.Column(db.String(40), nullable=True)
    dtls_verify = db.Column(db.String(40), nullable=True)
    dtls_rekey = db.Column(db.String(40), nullable=True)
    dtls_cert_file = db.Column(db.String(254), nullable=True)
    dtls_private_key = db.Column(db.String(254), nullable=True)
    dtls_ca_file = db.Column(db.String(254), nullable=True)
    dtls_ca_path = db.Column(db.String(254), nullable=True)
    dtls_setup = db.Column(db.Enum(Dtls_setup))
    srtp_tag_32 = db.Column(db.Enum(BoolEnum))
    media_address = db.Column(db.String(40), nullable=True)
    redirect_method = db.Column(db.Enum(Redirect_method))
    set_var = db.Column(db.String(254), nullable=True)
    cos_audio = db.Column(db.Integer)
    cos_video = db.Column(db.Integer)
    message_context = db.Column(db.String(40), nullable=True)
    force_avp = db.Column(db.Enum(BoolEnum))
    media_use_received_transport = db.Column(db.Enum(BoolEnum))
    accountcode = db.Column(db.String(80), nullable=True)
    user_eq_phone = db.Column(db.Enum(BoolEnum))
    moh_passthrough = db.Column(db.Enum(BoolEnum))
    media_encryption_optimistic = db.Column(db.Enum(BoolEnum))
    rpid_immediate = db.Column(db.Enum(BoolEnum))
    g726_non_standard = db.Column(db.Enum(BoolEnum))
    rtp_keepalive = db.Column(db.Integer)
    rtp_timeout = db.Column(db.Integer)
    rtp_timeout_hold = db.Column(db.Integer)
    bind_rtp_to_media_address = db.Column(db.Enum(BoolEnum))
    voicemail_extension = db.Column(db.String(40), nullable=True)
    mwi_subscribe_replaces_unsolicited = db.Column(db.Enum(LongBoolEnum))
    deny = db.Column(db.String(254), nullable=True)
    permit = db.Column(db.String(254), nullable=True)
    acl = db.Column(db.String(40), nullable=True)
    contact_deny = db.Column(db.String(254), nullable=True)
    contact_permit = db.Column(db.String(254), nullable=True)
    contact_acl = db.Column(db.String(40), nullable=True)
    subscribe_context = db.Column(db.String(40), nullable=True)
    fax_detect_timeout = db.Column(db.Integer)
    contact_user = db.Column(db.String(254), nullable=True)
    preferred_codec_only = db.Column(db.Enum(BoolEnum))
    asymmetric_rtp_codec = db.Column(db.Enum(BoolEnum))
    rtcp_mux = db.Column(db.Enum(BoolEnum))
    allow_overlap = db.Column(db.Enum(BoolEnum))
    refer_blind_progress = db.Column(db.Enum(BoolEnum))
    notify_early_inuse_ringing = db.Column(db.Enum(BoolEnum))
    max_audio_streams = db.Column(db.Integer)
    max_video_streams = db.Column(db.Integer)
    webrtc = db.Column(db.Enum(BoolEnum))
    dtls_fingerprint = db.Column(db.Enum(Dtls_fingerprint))
    incoming_mwi_mailbox = db.Column(db.String(254), nullable=True)
    bundle = db.Column(db.Enum(BoolEnum))
    dtls_auto_generate_cert = db.Column(db.Enum(BoolEnum))
    follow_early_media_fork = db.Column(db.Enum(BoolEnum))
    accept_multiple_sdp_answers = db.Column(db.Enum(BoolEnum))
    suppress_q850_reason_headers = db.Column(db.Enum(BoolEnum))
    trust_connected_line = db.Column(db.Enum(LongBoolEnum))
    send_connected_line = db.Column(db.Enum(LongBoolEnum))
    ignore_183_without_sdp = db.Column(db.Enum(LongBoolEnum))
    codec_prefs_incoming_offer = db.Column(db.String(254), nullable=True)
    codec_prefs_outgoing_offer = db.Column(db.String(254), nullable=True)
    codec_prefs_incoming_answer = db.Column(db.String(254), nullable=True)
    codec_prefs_outgoing_answer = db.Column(db.String(254), nullable=True)
    stir_shaken = db.Column(db.Enum(LongBoolEnum))
    send_history_info = db.Column(db.Enum(LongBoolEnum))
    auth = db.Column(db.Integer, db.ForeignKey('ps_auths.id'))
    aor = db.Column(db.Integer, db.ForeignKey('ps_aors.id'))
#    ps_aor = db.relationship("Ps_aors", back_populates="r_aors", cascade='all,delete-orphan')
#    ps_auth = db.relationship("Ps_auths", back_populates="r_auths", cascade='all,delete-orphan')

    def __init__(self, id, context, dtmf_mode, callerid, call_group, pickup_group, auth ,aor):
        self.id = id
        self.context = context
        self.dtmf_mode = dtmf_mode
        self.callerid = callerid
        self.call_group = call_group
        self.pickup_group = pickup_group
        self.auth = auth
        self.aor = aor


@login.user_loader
def load_user(id):
    return User.query.get(int(id))