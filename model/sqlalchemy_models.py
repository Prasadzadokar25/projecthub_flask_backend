from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Numeric,
    Enum,
    JSON,
    ForeignKey,
    create_engine,
    func,
    text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

Base = declarative_base()


class AdClick(Base):
    __tablename__ = 'ad_clicks'
    click_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('advertisements.ad_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True, index=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AdImpression(Base):
    __tablename__ = 'ad_impressions'
    impression_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('advertisements.ad_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True, index=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AdvertisementPlan(Base):
    __tablename__ = 'advertisement_plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(100), nullable=True)
    tier = Column(String(10), nullable=True)
    cpm_rate = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'
    ad_id = Column(Integer, primary_key=True, autoincrement=True)
    is_creation = Column(Boolean, nullable=True, default=True)
    ad_title = Column(String(255), nullable=True)
    ad_description = Column(Text, nullable=True)
    ad_website = Column(String(255), nullable=True)
    ad_image = Column(String(255), nullable=True)
    ad_start_date = Column(DateTime, nullable=False)
    ad_end_date = Column(DateTime, nullable=False)
    ad_duration = Column(Integer, nullable=False)
    target_locations = Column(JSON, nullable=True)
    target_categories = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    payment_id = Column(String(100), nullable=True)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    ad_owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=True, index=True)
    platform_target = Column(JSON, nullable=True)
    priority_level = Column(Integer, nullable=True, default=1)
    ad_type = Column(String(50), nullable=True, default='banner')
    target_impression_count = Column(Integer, nullable=True, default=0)

    owner = relationship('User', back_populates='advertisements')


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    account_holder_name = Column(String(100), nullable=True)
    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(20), nullable=False)
    ifsc_code = Column(String(11), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_primary = Column(Boolean, nullable=True, default=False)


class CardItem(Base):
    __tablename__ = 'carditems'
    carditem_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=False, index=True)
    added_on = Column(DateTime, server_default=func.now())
    status = Column(Boolean, nullable=False, default=True)


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    category_description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    gst = Column(Integer, nullable=True)
    platform_fee_id = Column(Integer, ForeignKey('platform_fees.fee_id'), nullable=True, index=True)
    image = Column(String(255), nullable=True)


class CreationComment(Base):
    __tablename__ = 'creation_comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    comment_text = Column(Text, nullable=False)
    commented_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CreationLike(Base):
    __tablename__ = 'creation_likes'
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    liked_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CreationShare(Base):
    __tablename__ = 'creation_shares'
    # Not enough details in the dump; create common fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    shared_at = Column(DateTime, server_default=func.now())


class Creation(Base):
    __tablename__ = 'creations'
    creation_id = Column(Integer, primary_key=True, autoincrement=True)
    creation_title = Column(String(255), nullable=False)
    creation_description = Column(Text, nullable=False)
    creation_price = Column(Numeric(10, 2), nullable=False)
    creation_thumbnail = Column(String(255), nullable=False)
    creation_file = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False, index=True)
    keyword = Column(Text, nullable=True)
    creation_other_images = Column(Text, nullable=True)
    total_copy_sell = Column(Integer, nullable=True, default=0)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True, index=True)
    status = Column(Enum('underreview', 'publish', name='creation_status'), nullable=True, server_default='underreview')
    createtime = Column(DateTime, server_default=func.now())
    youtube_link = Column(Text, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='creations')


class GstRate(Base):
    __tablename__ = 'gst_rates'
    gst_id = Column(Integer, primary_key=True, autoincrement=True)
    gst_percentage = Column(Numeric(5, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class OrderDetail(Base):
    __tablename__ = 'order_details'
    order_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True, index=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    gst_amount = Column(Numeric(10, 2), nullable=True)
    platform_fee = Column(Numeric(10, 2), nullable=True)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True, index=True)
    payment_id = Column(Integer, ForeignKey('payments.payment_id'), nullable=True, index=True)
    order_date = Column(DateTime, server_default=func.now())


class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    razorpay_payment_id = Column(String(255), nullable=False)
    payment_amount = Column(Numeric(10, 2), nullable=False)
    gst_amount = Column(Numeric(10, 2), nullable=True)
    platform_fee = Column(Numeric(10, 2), nullable=True)
    payment_method = Column(String(50), nullable=True)
    currency = Column(String(10), nullable=True, server_default='INR')
    transaction_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Enum('pending', 'completed', 'failed', name='payment_status'), nullable=True, server_default='pending')
    payment_gateway_fee = Column(Numeric(10, 2), nullable=True)


class PlatformFee(Base):
    __tablename__ = 'platform_fees'
    fee_id = Column(Integer, primary_key=True, autoincrement=True)
    fee_percentage = Column(Numeric(5, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Rating(Base):
    __tablename__ = 'ratings'
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    creation_id = Column(Integer, ForeignKey('creations.creation_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    rating = Column(Numeric(3, 2), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_password = Column(String(255), nullable=False)
    user_description = Column(Text, nullable=True)
    user_contact = Column(String(20), nullable=True, unique=True)
    user_email = Column(String(255), nullable=True, unique=True)
    role = Column(String(50), nullable=False)
    wallet_money = Column(Numeric(10, 2), nullable=True, default=0.00)
    reference_code = Column(String(50), nullable=True, unique=True)
    profile_photo = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    loginType = Column(Enum('mobile', 'google', name='login_type'), nullable=False, server_default='mobile')
    google_uid = Column(String(255), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    creations = relationship('Creation', back_populates='user')
    advertisements = relationship('Advertisement', back_populates='owner')


class Withdrawal(Base):
    __tablename__ = 'withdrawals'
    withdrawal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey('bank_accounts.account_id'), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    withdrawal_date = Column(DateTime, server_default=func.now())
    status = Column(Enum('pending', 'completed', 'failed', name='withdrawal_status'), nullable=True, server_default='pending')


# Database engine/session helper
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:##Prasad25@localhost/projecthubdb')
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# To create all tables run:
# from model.sqlalchemy_models import Base, engine
# Base.metadata.create_all(engine)
