#!flask/bin/python
import os
import json, requests, uuid, logging, datetime, time
from flask import Flask, url_for, Response, jsonify, make_response, url_for
from flask import request
import pandas as pd
#from sklearn import linear_model
#import pickle
import threading
import subprocess

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def row_to_xml(row):
    xml = ['<item>']
    for i, col_name in enumerate(row.index):
        xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
    xml.append('</item>')
    return '\n'.join(xml)

def generate_run_id():
    return str(uuid.uuid4())

def generate_run_id_hex():
    return str(uuid.uuid4().hex)

def generate_http_response(code='0', status='', msg=''):
    d = dict();
    d['code'] = '0' if code == None else code
    d['status'] = '' if status == None else status
    d['msg'] = '' if msg == None else msg
    return json.dumps( d )

def json_response(key, value):
    if key == None:
        return ''
    data=[]
    item={}
    item[key] = value
    data.append(item)
    return json.dumps(data)


def encrypt_string(hash_string):
    import hashlib
    logging.debug('hashing input: ' + hash_string)
    sha_signature = \
        hashlib.sha256( hash_string.encode() ).hexdigest()
    return sha_signature


def is_str_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def validate_creds (json_body):
    email = key = None
    if json_body == None:
        return -1, 'Empty body';
    try:
        if "EMAIL" in json_body:
            email = json_body["EMAIL"]
        else:
            return -1, 'Missing key EMAIL';
        if "KEY" in json_body:
            key = json_body["KEY"]
        else:
            return -1, 'Missing key KEY';
    except Exception as inst:
        return -1, 'Missing keys or values not properly defined';

    sha_signature = encrypt_string( str(email.strip() + key.strip()) )
    logging.debug ('sha_signature: ' + sha_signature)
    try:
        auth = False
        with  open("white-list","r") as wh:
            for line in wh:
                if sha_signature in line:
                    auth = True
    finally:
        wh.close()

    if auth == True:
        return 0, ''
    else:
        return -1, 'Not authorized';


def extract_key_from_body (json_body, thekey):
    if json_body == None:
        return 'Empty body';
    try:
        if thekey in json_body:
            return json_body[thekey];
        else:
            return 'Missing key ' + thekey;
    except Exception as inst:
        return 'Missing keys or values not properly defined';




def generate_token_from_creds (email, apikey):
    return generate_run_id_hex()


def construct_token_from_creds(body):
    if body == None:
        return ['Error', 'Empty body']
    try:
        email = key = None
        if "EMAIL" in body:
            email = body["EMAIL"]
        else:
            return ['Error', 'Missing key EMAIL']
        if "KEY" in body:
            key = body["KEY"]
        else:
            return ['Error', 'Missing key KEY']
    except Exception as inst:
        return ['Error', 'Missing keys or values not defined']

    sha_signature = encrypt_string( str(email.strip() + key.strip()) )
    logging.debug ('sha_signature: ' + sha_signature)
    try:
        auth = False
        with  open("white-list","r") as wh:
            for line in wh:
                if sha_signature in line:
                    auth = True
    finally:
        wh.close()

    if auth == True:
        return [ 'token', generate_run_id_hex() ]
    else:
        return ['Error', 'Not authorized']


def checkEmptyString(data):
    return '' if data == None else data
