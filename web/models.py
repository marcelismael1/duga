from flask import Flask, render_template, url_for, redirect, request, jsonify
import pymongo
from app import db
import uuid

class Alldata:

	def adddata(self):


		alldata = {
		"_id" : uuid.uuid4().hex,
		"systemip" : request.form.get("systemip"),
		"systemname" : request.form.get("systemname"),
		"systemgroup" :request.form.get("systemgroup"),
		"activation" : request.form.get("activation"),
		"scantype" : request.form.get("scantype"),
		"frequency" :request.form.get("frequency"),
		"scantype" : request.form.get("scantype"),
		

		}


		db.alldata.insert_one(alldata)

		return jsonify(alldata), 200


