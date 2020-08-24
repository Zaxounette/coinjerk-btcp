from app import db, bcrypt  # noqa: F401
import enum


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True)
    hashed_password = db.Column(db.String(64), nullable=False)

    invoices = db.relationship(
            'Invoice',
            backref='user',
            lazy=True
            )

    btcp_client_connector = db.relationship(
            'BTCPayClientConnector',
            backref='user',
            lazy=True,
            uselist=False,
            )

    streamelements_connector = db.relationship(
            'StreamElementsConnector',
            backref='user',
            lazy=True,
            uselist=False,
            )

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def authenticate(klass, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = klass.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return None

        return user

    def tip_page_export(self):
        exp = {
                'username': self.username,
                'display_name': self.username,
                }
        return exp

    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash(password)

    def pay_client(self):
        return self.btcp_client_connector.client

    def hash_password(password):
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)


class InvoiceStatus(enum.Enum):
    UNPAID = 0
    PAID = 1
    EXPIRED = 2


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # status holds valid values "paid", "unpaid", "expired"
    status = db.Column(db.Enum(InvoiceStatus))
    btcpay_invoice_id = db.Column(db.String(64))

    message = db.Column(db.String(255))
    email = db.Column(db.String(255))
    username = db.Column(db.String(255), default="Anonymous")

    user_id = db.Column(
            db.Integer, db.ForeignKey('user.id'), nullable=False
            )
    btcp_client_connector_id = db.Column(
            db.Integer,
            db.ForeignKey('btc_pay_client_connector.id'),
            nullable=False
            )


class BTCPayClientConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    client = db.Column(db.PickleType)
    user_id = db.Column(
            db.Integer, db.ForeignKey('user.id')
            )
    invoices = db.relationship(
            'Invoice',
            backref='btcp_client_connector',
            lazy=True,
            uselist=False,
            )


class StreamElementsConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jwt = db.Column(db.String(1024))
    channel_id = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
