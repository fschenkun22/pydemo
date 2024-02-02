import sqlalchemy
from sqlalchemy import text,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import select



from sqlalchemy.orm import DeclarativeBase

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = sqlalchemy.create_engine('mysql://root:123456@localhost:3306/orm_test', echo=True)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True) #定义id字段为int
    name: Mapped[str] = mapped_column(String(30)) #定义name字段为str
    fullname: Mapped[Optional[str]] = mapped_column(String(50)) #定义fullname字段为str，可选 官网缺少mapped_column(String(50)) 
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan") # 虚拟自定义 addresses 字段为List[Address]，关联Address表，级联删除 ;Mapped[List["Address"]] 是一个类型注解，表示 addresses 的类型是一个 Address 类的列表

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

Base.metadata.create_all(engine)


with Session(engine) as session:
    # spongebob = User(
    #     name="spongebob",
    #     fullname="Spongebob Squarepants",
    #     addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    # )
    # sandy = User(
    #     name="sandy",
    #     fullname="Sandy Cheeks",
    #     addresses=[
    #         Address(email_address="sandy@sqlalchemy.org"),
    #         Address(email_address="sandy@squirrelpower.org"),
    #     ],
    # )
    # patrick = User(name="patrick", fullname="Patrick Star")
    # session.add_all([spongebob, sandy, patrick])
    # # 删除sandy
    
    # session.commit()

    # stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    # for user in session.scalars(stmt):
    #     print(user)
    stmt = (
         select(Address)
         .join(Address.user)
         .where(User.name == "sandy")
         .where(Address.email_address == "sandy@sqlalchemy.org")
     )
    sandy_address = session.scalars(stmt).one()


    print('------------------------------------------')
    print(sandy_address)
    print('------------------------------------------')

    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
    # sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

    session.commit()

    print('------------------------------------------')
    print(patrick)
    print('------------------------------------------')