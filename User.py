# -*- coding: utf-8 -*-
"""
create table if not exists `users` (
     `id` int(10) unsigned not null auto_increment,
     `username` varchar(32)  default '',
     `username_zh` varchar(32)  default '',
     `password` varchar(32)  default '',
     `email` varchar(64)  default '',
     `identity_number` varchar(18)  default '',
     `cell_phone` varchar(11)  default '',
     `ip_addr` varchar(32)  default '',
     `living_place` varchar(100)  default '',
     PRIMARY KEY (`id`)) ENGINE=MyISAM DEFAULT CHARSET=utf8;

alter table `users` (
     `id` int(10) unsigned not null auto_increment,
     `username` varchar(32)  default '',
     `username_zh` varchar(32)  default '',
     `password` varchar(32)  default '',
     `email` varchar(64)  default '',
     `identity_number` varchar(18)  default '',
     `cell_phone` varchar(11)  default '',
     `ip_addr` varchar(32)  default '',
     `living_place` varchar(100)  default '',
     PRIMARY KEY (`id`)) ENGINE=MyISAM DEFAULT CHARSET=utf8;

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('mysql://root:toor@127.0.0.1:3306/sdb?charset=utf8')

class user_model(Base):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine':'MyISAM','mysql_charset':'utf8'}

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(32))
    username_zh = Column(String(32))
    password = Column(String(50))
    email = Column(String(64))
    identity_number = Column(String(18))
    cell_phone = Column(String(11))
    ip_addr = Column(String(32))
    living_place = Column(String(100))
